# P3 data verification round for Morocco dataset (post-enrichment).
import json, os, re, collections, difflib

D = 'output/ma/2026-10-05'
issues = collections.defaultdict(list)
ALLOWED_TOP = {'org_id','wikidata_qid','basic_info','social_accounts','digital_assets','key_people','departments','recent_events','related_entities','core_business','industries','apec_stance','profile','collection_meta'}
ORGPAT = re.compile(r'^MA-(GOV|SOE|CORP|NGO|ACAD|MEDIA|FIN|INTL|PARTY|MIL)-[0-9]{3}$')
PPAT = re.compile(r'^MA-PERSON-[0-9]{6}$')

orgs = {}
for f in sorted(os.listdir(f'{D}/orgs')):
    if f.endswith('.json') and not f.startswith('_'):
        o = json.load(open(f'{D}/orgs/{f}', encoding='utf-8'))
        orgs[o['org_id']] = o

reg = json.load(open(f'{D}/id_registry.json', encoding='utf-8'))
regids = {r['org_id'] for r in reg['registry']}
preg = {p['person_id']: p for p in reg['person_registry']}

# 1. registry <-> profiles
if regids - set(orgs):
    extra = regids - set(orgs)
    issues['registry'].append(f'{len(extra)} registry org_ids without profile (resolve-registered refs, expected)')
for oid, o in orgs.items():
    if oid not in regids:
        issues['registry'].append(f'{oid}: profile not in registry')

# 2. phase / top-level / quotes compliance
for oid, o in orgs.items():
    cm = o.get('collection_meta', {})
    if cm.get('phase') != 'phase3_enriched':
        issues['phase'].append(oid)
    q = cm.get('quotes')
    if not isinstance(q, list) or len(q) < 3 or any(not isinstance(x, dict) for x in q):
        issues['quotes'].append(oid)
    extra = [k for k in o if k not in ALLOWED_TOP]
    if extra:
        issues['toplevel'].append(f'{oid}: {extra}')
    cb = o.get('core_business')
    if not cb or len(str(cb)) < 100:
        issues['core_business_short'].append(f"{oid}({len(str(cb or ''))})")

# 3. person_id refs valid + short format
for oid, o in orgs.items():
    for kp in (o.get('key_people') or []):
        pid = kp.get('person_id')
        if pid and not PPAT.match(pid):
            issues['bad_person_id'].append(f'{oid}: {pid}')
        elif pid and pid not in preg:
            issues['missing_person'].append(f'{oid}: {pid} {kp.get("name")}')

# 4. org_id refs valid (format + existence)
for oid, o in orgs.items():
    for r in (o.get('related_entities') or []):
        rid = r.get('org_id')
        if rid and rid not in orgs and rid not in regids:
            issues['dangling_org_ref'].append(f'{oid} -> {rid}')

# 5. self references
for oid, o in orgs.items():
    for r in (o.get('related_entities') or []):
        if r.get('org_id') == oid and r.get('relationship_type') != 'self':
            issues['self_ref'].append(oid)

# 6. duplicate persons by name (across orgs)
byname = collections.defaultdict(list)
for oid, o in orgs.items():
    for kp in (o.get('key_people') or []):
        nm = (kp.get('name') or '').strip()
        if nm:
            byname[nm].append((oid, kp.get('person_id')))
for nm, lst in byname.items():
    if len(lst) > 1:
        pids = {p for _, p in lst}
        flag = 'MIXED-IDS' if (len(pids - {None}) > 1) else 'multi-org'
        issues['dup_person'].append(f'{nm}: {len(lst)} orgs [{flag}]')

# 7. date sanity
for oid, o in orgs.items():
    fd = o['basic_info'].get('founded_date')
    if fd and not re.match(r'^\d{4}-\d{2}-\d{2}$', str(fd)):
        issues['bad_founded'].append(f'{oid}: {fd}')

# 8. recent_events source coverage
for oid, o in orgs.items():
    evs = o.get('recent_events') or []
    if len(evs) < 3:
        issues['events_lt3'].append(f'{oid}({len(evs)})')
    for ev in evs:
        if not ev.get('source'):
            issues['event_no_source'].append(oid); break

print('profiles:', len(orgs), '| registry orgs:', len(reg['registry']), '| person_registry:', len(preg))
for k, v in issues.items():
    print(f'\n== {k} ({len(v)}) ==')
    for line in v[:15]:
        print('  ', line)
if not issues:
    print('\nNO ISSUES')

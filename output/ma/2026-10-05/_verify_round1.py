# One-round cross verification of P1/P2 outputs for Morocco dataset.
# Checks: target<->profile, registry<->profile, person registry<->key_people,
# cache<->profile (names/website/founded), field sanity, duplicate detection.
import json, os, re, difflib, collections

D = 'output/ma/2026-10-05'
issues = collections.defaultdict(list)

targets = json.load(open(f'{D}/_target_orgs.json', encoding='utf-8'))
tmap = {t['id']: t for t in targets}
reg = json.load(open(f'{D}/id_registry.json', encoding='utf-8'))
preg = {p['person_id']: p for p in reg['person_registry']}

profiles = {}
for f in sorted(os.listdir(f'{D}/orgs')):
    if f.endswith('.json') and not f.startswith('_'):
        o = json.load(open(f'{D}/orgs/{f}', encoding='utf-8'))
        profiles[o['org_id']] = o

# 1. target <-> profile
if set(tmap) != set(profiles):
    issues['target_vs_profile'].append(f"ID set diff: only-target={set(tmap)-set(profiles)} only-profile={set(profiles)-set(tmap)}")
for oid, t in tmap.items():
    p = profiles.get(oid)
    if not p: continue
    if (t.get('wikidata_qid') or None) != (p['basic_info'].get('wikidata_qid') or None):
        issues['target_vs_profile'].append(f"{oid}: QID mismatch target={t.get('wikidata_qid')} profile={p['basic_info'].get('wikidata_qid')}")
    if t['category'] != p['basic_info']['org_type']:
        issues['target_vs_profile'].append(f"{oid}: category {t['category']} vs org_type {p['basic_info']['org_type']}")
    pname = p['basic_info'].get('name_en')
    if pname and pname not in (t.get('aliases') or []) + [t['name']]:
        issues['target_vs_profile'].append(f"{oid}: profile name_en {pname!r} not in target name/aliases")
    if p.get('collection_meta', {}).get('phase') != 'phase2_skeleton':
        issues['target_vs_profile'].append(f"{oid}: unexpected phase {p.get('collection_meta',{}).get('phase')}")

# 2. registry <-> profiles
reg_ids = {r['org_id'] for r in reg['registry']}
if reg_ids != set(profiles):
    issues['registry'].append(f"registry-profile diff: only-reg={reg_ids-set(profiles)} only-prof={set(profiles)-reg_ids}")
cnt = collections.Counter(o['basic_info']['org_type'] for o in profiles.values())
for t, c in cnt.items():
    expect = max(int(r['org_id'].split('-')[-1]) for r in reg['registry'] if r['org_id'].startswith(f"MA-{t}-"))
    if expect != c:
        issues['registry'].append(f"MA-{t}: counter max {expect} != count {c} (gaps?)")

# 3. person registry <-> key_people
refs = [(oid, kp['person_id']) for oid, o in profiles.items() for kp in (o.get('key_people') or [])]
for oid, pid in refs:
    if pid not in preg:
        issues['persons'].append(f"{oid} references missing person {pid}")
byname = collections.defaultdict(list)
for pid, p in preg.items():
    nm = (p.get('name') or '').strip().lower()
    if nm: byname[nm].append(pid)
for nm, ids in byname.items():
    if len(ids) > 1:
        issues['persons'].append(f"duplicate person name {nm!r}: {ids}")
for pid, p in preg.items():
    if not p.get('name'):
        issues['persons'].append(f"{pid}: empty name")
    if not p.get('wikidata_qid'):
        issues['persons'].append(f"{pid} ({p.get('name')}): no QID")

# 4. cache <-> profile
def cache_labels(qid):
    try:
        c = json.load(open(f'{D}/_cache/{qid}.json', encoding='utf-8'))
    except FileNotFoundError:
        return None
    w = c.get('wikidata') or {}
    labs = {k: v.get('value') for k, v in (w.get('labels') or {}).items()}
    claims = w.get('claims') or {}
    def first(pid_prop):
        cl = claims.get(pid_prop) or []
        if not cl: return None
        mw = cl[0].get('mainsnak', {}).get('datavalue', {}).get('value')
        return mw.get('id') if isinstance(mw, dict) and 'id' in mw else mw
    p856 = first('P856')
    p571 = first('P571')
    return labs, p856, p571

for oid, o in profiles.items():
    q = o['basic_info'].get('wikidata_qid')
    if not q: continue
    r = cache_labels(q)
    if r is None:
        issues['cache'].append(f"{oid}: cache missing for {q}")
        continue
    labs, p856, p571 = r
    en = labs.get('en')
    nen = o['basic_info'].get('name_en')
    if en and nen:
        sim = difflib.SequenceMatcher(None, en.lower(), nen.lower()).ratio()
        if sim < 0.40:
            issues['cache_name'].append(f"{oid}: profile name_en {nen!r} vs wikidata en label {en!r} (sim {sim:.2f})")
    if p856 and o['basic_info'].get('website') and p856 != o['basic_info']['website']:
        issues['cache_web'].append(f"{oid}: website {o['basic_info']['website']} vs wikidata P856 {p856}")

# 5. field sanity
for oid, o in profiles.items():
    bi = o['basic_info']
    if not bi.get('name_en'): issues['fields'].append(f"{oid}: name_en null")
    if not bi.get('name_original'): issues['fields'].append(f"{oid}: name_original null")
    if not bi.get('website'): issues['fields'].append(f"{oid}: website null")
    fd = bi.get('founded_date')
    if fd:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', fd):
            issues['fields'].append(f"{oid}: founded_date not strict: {fd}")
        else:
            y = int(fd[:4])
            if y < 1800 or y > 2026:
                issues['fields'].append(f"{oid}: founded year out of range: {fd}")
    for sa in (o.get('social_accounts') or []):
        u = sa.get('url') or ''
        if not u.startswith('http'):
            issues['fields'].append(f"{oid}: social url bad: {u}")

# 6. duplicate detection
wsl = collections.defaultdict(list)
for oid, o in profiles.items():
    w = (o['basic_info'].get('website') or '').lower().replace('https://','').replace('http://','').strip('/').replace('www.','')
    if w: wsl[w].append(oid)
for w, ids in wsl.items():
    if len(ids) > 1:
        issues['duplicates'].append(f"shared website {w}: {ids}")
names = [(oid, (o['basic_info'].get('name_en') or '')) for oid, o in profiles.items()]
for i in range(len(names)):
    for j in range(i+1, len(names)):
        a, b = names[i][1].lower(), names[j][1].lower()
        if a and b and difflib.SequenceMatcher(None, a, b).ratio() > 0.9:
            issues['duplicates'].append(f"similar names: {names[i]} vs {names[j]}")

print(f"profiles={len(profiles)} targets={len(tmap)} registry={len(reg['registry'])} person_registry={len(preg)}")
print(f"key_people refs={len(refs)}")
for k, v in issues.items():
    print(f"\n== {k} ({len(v)}) ==")
    for line in v[:40]:
        print('  ', line)
if not issues:
    print('\nNO ISSUES FOUND')

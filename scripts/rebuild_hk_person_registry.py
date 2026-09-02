"""Rebuild HK person_registry: dedupe, add missing disk persons, mark profiled."""
import json, glob, os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REG = 'output/hk/2026-07-24/id_registry.json'
PDIR = 'output/hk/2026-07-24/persons'

reg = json.load(open(REG, encoding='utf-8'))
pr = reg.get('person_registry') or []
print(f'person_registry entries (raw): {len(pr)}')

# Dedupe by person_id, prefer entries with richer info
by_id = {}
for e in pr:
    pid = e.get('person_id')
    if not re.match(r'^HK-PERSON-\d{6}$', pid or ''):
        continue
    if pid in by_id:
        old = by_id[pid]
        # merge: keep non-empty fields
        for k in ('name', 'wikidata_qid', 'source_orgs', 'notes'):
            if not old.get(k) and e.get(k):
                old[k] = e[k]
    else:
        by_id[pid] = dict(e)
print(f'unique valid person_ids: {len(by_id)}')

disk_files = sorted(glob.glob(os.path.join(PDIR, 'HK-PERSON-*.json')))
print(f'person files on disk: {len(disk_files)}')

added = 0
updated = 0
for f in disk_files:
    pid = os.path.basename(f).replace('.json', '')
    d = json.load(open(f, encoding='utf-8'))
    name = d.get('name_zh') or d.get('name') or pid
    qid = d.get('wikidata_qid')
    if pid in by_id:
        e = by_id[pid]
        changed = False
        if e.get('status') != 'profiled':
            e['status'] = 'profiled'; changed = True
        if not e.get('name') or e['name'] == pid:
            e['name'] = name; changed = True
        if qid and not e.get('wikidata_qid'):
            e['wikidata_qid'] = qid; changed = True
        if changed: updated += 1
    else:
        # derive source_orgs from work_experience org_ids
        srcs = []
        for we in d.get('work_experience') or []:
            oid = we.get('org_id')
            if oid and oid.startswith('HK-') and oid not in srcs:
                srcs.append(oid)
        by_id[pid] = {
            'person_id': pid,
            'name': name,
            'wikidata_qid': qid,
            'status': 'profiled',
            'source_orgs': srcs[:5],
        }
        added += 1

entries = sorted(by_id.values(), key=lambda e: e['person_id'])
reg['person_registry'] = entries
from collections import Counter
c = Counter(e.get('status') for e in entries)
reg['person_counters'] = dict(c)
reg.setdefault('counters', {})['persons_total'] = len(entries)

tmp = REG + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)
os.replace(tmp, REG)
print(f'added {added}, updated {updated}, total {len(entries)}')
print('status counts:', dict(c))

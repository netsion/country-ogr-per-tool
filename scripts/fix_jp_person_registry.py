"""Fix JP id_registry.json: deduplicate person entries, KEEP original person_ids."""
import json, sys, io, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from collections import defaultdict

base_dir = "D:/claude-workspace/apec-osint-tool/output/jp/2026-06-09"
reg_path = os.path.join(base_dir, "id_registry.json")

with open(reg_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

pr = data['person_registry']

# Group by person_id
by_pid = defaultdict(list)
for p in pr:
    by_pid[p['person_id']].append(p)

# Merge duplicates, keep original person_id
merged = []
for pid, entries in sorted(by_pid.items(), key=lambda x: x[0]):
    # Prefer entry with name + wikidata_qid
    def sort_key(e):
        has_name = 1 if e.get('name') else 0
        has_qid = 1 if e.get('wikidata_qid') else 0
        return -(has_name + has_qid)
    entries.sort(key=sort_key)

    base = dict(entries[0])
    # Merge missing fields from other entries
    for e in entries[1:]:
        if not base.get('name') and e.get('name'):
            base['name'] = e['name']
        if not base.get('wikidata_qid') and e.get('wikidata_qid'):
            base['wikidata_qid'] = e['wikidata_qid']
        if not base.get('source_orgs') and e.get('source_orgs'):
            base['source_orgs'] = e['source_orgs']
        if not base.get('name') and e.get('name_en'):
            base['name'] = e['name_en']
        # Merge org_ids if present
        if e.get('org_ids'):
            existing = set(base.get('org_ids', []))
            for oid in e['org_ids']:
                if oid not in existing:
                    base.setdefault('org_ids', []).append(oid)

    if not base.get('name') and base.get('name_en'):
        base['name'] = base['name_en']

    # Clean up: remove keys that aren't standard
    clean = {
        'person_id': pid,
        'name': base.get('name', ''),
        'wikidata_qid': base.get('wikidata_qid'),
        'status': base.get('status', 'listed'),
        'source_orgs': base.get('source_orgs', [])
    }
    merged.append(clean)

print(f"Merged {len(pr)} entries -> {len(merged)} unique persons")

# Update id_registry.json
data['person_registry'] = merged
# Update counter: find max person_id number
import re
max_num = 0
for p in merged:
    m = re.search(r'(\d+)$', p['person_id'])
    if m:
        max_num = max(max_num, int(m.group(1)))
data['person_id_counter'] = max_num

with open(reg_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Updated id_registry.json, max PID num: {max_num}")

# Rebuild person_list.json using update_person_list.py logic
person_sources = {}
for fpath in glob.glob(os.path.join(base_dir, "orgs", "*.json")):
    if os.path.basename(fpath) == "_index.json":
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        org = json.load(f)
    org_id = org['org_id']
    org_name = org['basic_info'].get('name_en', '')
    for kp in org.get('key_people', []):
        pid = kp.get('person_id')
        if pid:
            if pid not in person_sources:
                person_sources[pid] = []
            person_sources[pid].append({
                'org_id': org_id,
                'org_name': org_name,
                'position_title': kp.get('title', '')
            })

# Build person_list from merged registry
persons = []
for p in merged:
    pid = p['person_id']
    name = p.get('name', '')
    sources = person_sources.get(pid, [])

    name_zh = None
    name_en = name
    if '(' in name and ')' in name:
        parts = name.split('(')
        name_zh = parts[0].strip()
        name_en = parts[1].rstrip(')').strip()
    elif any('一' <= c <= '鿿' for c in name):
        name_zh = name
    else:
        name_en = name

    titles = [s['position_title'] for s in sources if s['position_title']]
    importance = 'low'
    for t in titles:
        tl = t.lower()
        high_kw = ['prime minister', 'president', 'chief justice', 'chief executive',
                   'chairman', 'ceo', 'managing director', 'minister of foreign affairs',
                   'minister of finance', 'minister of defence', 'minister of trade',
                   'minister of', '长官', '部长', 'governor', '中央银行', 'premier']
        medium_kw = ['vice minister', 'vice-minister', 'deputy minister', '次官',
                     '副部长', '第一次官', '第二次官', '副长官',
                     'judge', 'director', 'chief', 'senior', 'head',
                     'ambassador', '大使']
        if any(kw in tl for kw in high_kw):
            importance = 'high'
            break
        if any(kw in tl for kw in medium_kw):
            importance = 'medium'

    entry = {
        'person_id': pid,
        'wikidata_qid': p.get('wikidata_qid'),
        'name': name,
        'name_zh': name_zh,
        'name_en': name_en,
        'importance_level': importance,
        'importance_reason': '; '.join(titles[:2]) if titles else None,
        'source_orgs': sources[:5],
        'discovery_source': 'key_people',
        'nationality': 'JP',
        'notes': None
    }
    persons.append(entry)

by_imp = {}
for p in persons:
    by_imp[p['importance_level']] = by_imp.get(p['importance_level'], 0) + 1

plist = {
    'metadata': {
        'country': 'Japan',
        'country_iso': 'JP',
        'collection_date': '2026-06-12',
        'phase': 'phase4_person_list',
        'source_org_count': len(glob.glob(os.path.join(base_dir, 'orgs', '*.json'))) - 1,
        'total_persons': len(persons)
    },
    'persons': persons,
    'summary': {
        'by_importance_level': by_imp,
        'by_discovery_source': {'key_people': len(persons)},
        'data_quality': {
            'with_person_id': len(persons),
            'with_wikidata_qid': sum(1 for p in persons if p.get('wikidata_qid')),
            'without_person_id': 0
        }
    }
}

plist_path = os.path.join(base_dir, "person_list.json")
with open(plist_path, 'w', encoding='utf-8') as f:
    json.dump(plist, f, ensure_ascii=False, indent=2)

print(f"Updated person_list.json: {len(persons)} persons")
print(f"By importance: {by_imp}")

null_zh = [p for p in persons if not p.get('name_zh')]
print(f"Null name_zh: {len(null_zh)}")
for p in null_zh[:5]:
    print(f"  {p['person_id']}: {p['name_en']}")

# Verify: check that org key_people person_ids exist in registry
reg_pids = set(p['person_id'] for p in merged)
missing = 0
for fpath in glob.glob(os.path.join(base_dir, "orgs", "*.json")):
    if os.path.basename(fpath) == "_index.json":
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        org = json.load(f)
    for kp in org.get('key_people', []):
        pid = kp.get('person_id')
        if pid and pid not in reg_pids:
            missing += 1
            if missing <= 3:
                print(f"  WARNING: org {org['org_id']} references missing person_id {pid}")
print(f"Total missing person_id references: {missing}")

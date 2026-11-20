# -*- coding: utf-8 -*-
"""SD key_people: link by name to existing profiles; create skeletons for the rest."""
import glob, json, os, re
from collections import defaultdict
BASE = 'D:/ai-workspace/apec-osint-tool'
DIR = BASE + '/output/sd/2026-11-16'

def save(p, obj):
    payload = json.dumps(obj, ensure_ascii=False, indent=2) + '\n'
    tmp = p + '.tmp'
    for _ in range(6):
        try:
            with open(tmp, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(payload)
            os.replace(tmp, p)
            return
        except PermissionError:
            time.sleep(0.5)
    with open(p, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(payload)

import time

name2pid = defaultdict(set)
for f in glob.glob(DIR + '/persons/*.json'):
    if os.path.basename(f).startswith('_'): continue
    d = json.load(open(f, encoding='utf-8')); pid = d.get('person_id')
    if not pid: continue
    vals = [d.get('name'), d.get('name_zh'), d.get('name_en')] + list(d.get('aliases') or [])
    for v in vals:
        if isinstance(v, str) and v.strip(): name2pid[v.strip()].add(pid)

def parse_name(s):
    m = re.match(r'^(.*?)\s*[（(](.*)[）)]\s*$', s or '')
    if m: return m.group(1).strip(), m.group(2).strip()
    if re.search(r'[\u4e00-\u9fff]', s or ''): return s.strip(), None
    return None, s.strip()

reg = json.load(open(DIR + '/id_registry.json', encoding='utf-8'))
pre = reg.setdefault('person_registry', [])
mx = 0
for e in pre:
    m = re.match(r'SD-PERSON-(\d+)', e.get('person_id') or '')
    if m: mx = max(mx, int(m.group(1)))
for f in glob.glob(DIR + '/persons/*.json'):
    m = re.match(r'SD-PERSON-(\d+)', os.path.basename(f))
    if m: mx = max(mx, int(m.group(1)))
nextn = mx + 1

linked = 0
created = []
for f in glob.glob(DIR + '/orgs/*.json'):
    if os.path.basename(f).startswith('_'): continue
    d = json.load(open(f, encoding='utf-8')); dirty = False
    for x in d.get('key_people') or []:
        if not isinstance(x, dict) or (x.get('person_id') or '').strip(): continue
        nm = (x.get('name') or x.get('name_en') or '').strip()
        if not nm: continue
        zh, en = parse_name(nm)
        cands = set(name2pid.get(nm, set()))
        if not cands and zh: cands |= set(name2pid.get(zh, set()))
        if not cands and en: cands |= set(name2pid.get(en, set()))
        if len(cands) == 1:
            x['person_id'] = next(iter(cands)); linked += 1; dirty = True
            continue
        if len(cands) > 1: continue
        # skeleton
        pid = f'SD-PERSON-{nextn:06d}'; nextn += 1
        prof = {
            'person_id': pid, 'name': en or zh or nm, 'name_zh': zh or None,
            'name_en': en or nm, 'name_original': None, 'aliases': [],
            'gender': 'unknown', 'birth_date': None, 'birth_place': None,
            'nationality': 'SD', 'biography_summary': None,
            'current_positions': [x.get('title') or None],
            'work_experience': [{'organization': (d.get('basic_info') or {}).get('name_zh') or (d.get('basic_info') or {}).get('name_en'), 'org_id': d.get('org_id'), 'position': x.get('title') or None}],
            'education': [], 'political_stances': [], 'person_relationships': [],
            'major_achievements': [], 'family_members': [], 'social_accounts': [],
            'contacts': [], 'profile': None,
            'collection_meta': {'collection_date': '2026-11-20', 'phase': 'phase4_person_profile',
                                'data_sources': ['org_key_people'], 'completeness_score': 35,
                                'notes': '从组织 key_people 生成的骨架画像；待补全',
                                'quotes': [{'title': '来自组织 key_people', 'url': 'internal:' + str(d.get('org_id'))}]},
        }
        save(DIR + f'/persons/{pid}.json', prof)
        created += 1
        name2pid[nm].add(pid)
        if zh: name2pid[zh].add(pid)
        x['person_id'] = pid; dirty = True
    if dirty: save(f, d)

for pid in created:
    dd = json.load(open(DIR + f'/persons/{pid}.json', encoding='utf-8'))
    pre.append({'person_id': pid, 'name': dd.get('name') or '', 'status': 'listed',
                'source': 'org key_people skeleton'})
reg['person_registry'] = pre
save(DIR + '/id_registry.json', reg)
print(json.dumps({'linked_to_existing': linked, 'created_count': len(created)}, ensure_ascii=False))

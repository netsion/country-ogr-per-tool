# -*- coding: utf-8 -*-
"""Extract P4 person roster from enriched orgs; classify importance per skill §14.1;
output org_type x importance statistics + person_list draft."""
import json
import glob
import os
import re
import sys
import io
from collections import Counter, defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))

orgs = {}
for f in sorted(glob.glob(D + '/orgs/*.json')):
    if f.endswith('_index.json'):
        continue
    p = json.load(open(f, encoding='utf-8'))
    orgs[p['org_id']] = p

PRUNED = {o for o, p in orgs.items() if p['basic_info']['org_type'] == 'INTL'} | {
    'BO-PARTY-006', 'BO-PARTY-007', 'BO-PARTY-010', 'BO-PARTY-011'}

HIST = re.compile(r'前任|前校长|前总|前部长|前主席|前台长|前局长|前总统|前副|创始|创办|已故|历史|卸任|末任|临时台长\(历史\)')
HIGH = re.compile(r'总统|党主席|党魁|全国领袖|总司令|总检察长|监察专员|央行行长|中央银行行长')
MED = re.compile(r'部长|总裁|执行总裁|总经理|副校长|校长|院长|台长|社长|总编辑|主编|执行主任|主任|主席|秘书长|执行秘书|董事总经理|执行董事|代表|省长|市长|司令|总干事|总监')

def importance(title):
    t = title or ''
    if HIGH.search(t):
        return 'high'
    if MED.search(t):
        return 'medium'
    return 'low'

def is_historical(title, desc):
    return bool(HIST.search(title or '') or HIST.search((desc or '')[:80]))

# collect
persons = {}
hist_count = 0
for oid, p in sorted(orgs.items()):
    if oid in PRUNED:
        continue
    if p.get('collection_meta', {}).get('phase') != 'phase3_enriched':
        continue
    otype = p['basic_info']['org_type']
    oname = p['basic_info'].get('name_original') or ''
    for kp in p.get('key_people') or []:
        name = kp.get('name') or ''
        if not name:
            continue
        pid = kp.get('person_id')
        title = kp.get('title') or ''
        desc = kp.get('description') or ''
        key = pid or ('N:' + re.sub(r'\s+', '', name.lower()))
        if is_historical(title, desc):
            hist_count += 1
            continue
        if key in persons:
            persons[key]['orgs'].add(oid)
            continue
        persons[key] = {
            'name': name, 'title': title, 'pid': pid,
            'orgs': {oid}, 'org_type': otype, 'org': oname,
            'level': importance(title),
        }

lv = Counter(v['level'] for v in persons.values())
print('=== P4 PERSON ROSTER ===')
print('unique active persons: %d | historical excluded: %d' % (len(persons), hist_count))
print('by importance: high=%d medium=%d low=%d' % (lv['high'], lv['medium'], lv['low']))
print()
# org_type x importance crosstab
tab = defaultdict(Counter)
multi = 0
for v in persons.values():
    if len(v['orgs']) > 1:
        multi += 1
    tab[v['org_type']][v['level']] += 1
print('%-8s %5s %6s %6s %5s' % ('type', 'total', 'high', 'medium', 'low'))
tot = Counter()
for t in sorted(tab):
    c = tab[t]
    s = sum(c.values())
    tot += c
    print('%-8s %5d %6d %6d %5d' % (t, s, c['high'], c['medium'], c['low']))
print('%-8s %5d %6d %6d %5d' % ('TOTAL', sum(tot.values()), tot['high'], tot['medium'], tot['low']))
print()
print('persons in multiple orgs:', multi)
# high sample
print()
print('--- HIGH sample ---')
for v in persons.values():
    if v['level'] == 'high':
        print('  [%s] %s | %s | %s' % (v['org_type'], v['name'][:40], v['title'][:30], v['org'][:30]))

# save draft person_list for P4
out = []
for key, v in persons.items():
    out.append({
        'person_id': v['pid'],
        'name': v['name'],
        'title': v['title'],
        'org_type': v['org_type'],
        'source_orgs': sorted(v['orgs']),
        'importance_level': v['level'],
    })
out.sort(key=lambda x: (x['org_type'], {'high': 0, 'medium': 1, 'low': 2}[x['importance_level']]))
with open(D + '/person_list_p4_draft.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print()
print('draft saved: person_list_p4_draft.json (%d entries)' % len(out))

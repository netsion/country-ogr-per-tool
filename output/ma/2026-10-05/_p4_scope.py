# Rebuild P4 person list with scope rule: GOV/PARTY/MIL all levels; others high only.
import json, os, re, collections, datetime

D = 'output/ma/2026-10-05'
orgs = {}
for f in sorted(os.listdir(f'{D}/orgs')):
    if f.endswith('.json') and not f.startswith('_'):
        o = json.load(open(f'{D}/orgs/{f}', encoding='utf-8'))
        orgs[o['org_id']] = o

RANK = {'high': 0, 'medium': 1, 'low': 2}

def classify(title):
    t = title or ''
    if re.search(r'前(主席|总书记|校长|总干事|董事长|部长|总裁|院长|局长|大臣|理事|董事|指挥官|总司长|社长|台长|CEO|PDG)|前任|创始人|已故|名誉|荣誉|末任|Former|Ancien', t, re.I):
        return 'low'
    if re.search(r'副|国务秘书|部级代表', t):
        return 'medium'
    if re.search(r'国王|王储|政府首脑|首相|总书记|大臣|部长|总裁|董事长|行长|总干事|署长|台长|社长|总监察长|总司令|主席|校长|局长|理事长', t):
        return 'high'
    if re.search(r'秘书长|总监|司长|主任|理事|董事|总编辑|发言人|主编', t):
        return 'medium'
    return 'medium'

persons = {}
for oid, o in orgs.items():
    otype = o['basic_info']['org_type']
    for kp in (o.get('key_people') or []):
        pid = kp.get('person_id')
        nm = (kp.get('name') or '').strip()
        if not nm:
            continue
        key = pid or ('name:' + nm)
        lvl = classify(kp.get('title'))
        rec = persons.setdefault(key, {'person_id': pid, 'name': nm, 'orgs': [], 'levels': [], 'titles': []})
        rec['orgs'].append((oid, otype))
        rec['levels'].append(lvl)
        rec['titles'].append(kp.get('title') or '')

ALL = {'GOV', 'PARTY', 'MIL'}
ins_by = collections.Counter()
out_by = collections.Counter()
for k, rec in persons.items():
    rec['level'] = min(rec['levels'], key=lambda x: RANK[x])
    otypes = {t for _, t in rec['orgs']}
    rec['p4_collect'] = bool(otypes & ALL) or rec['level'] == 'high'
    if rec['p4_collect']:
        best = min(range(len(rec['levels'])), key=lambda i: RANK[rec['levels'][i]])
        ins_by[rec['orgs'][best][1]] += 1
    else:
        out_by[rec['orgs'][0][1]] += 1

plist = {}
for k, v in persons.items():
    plist[k] = {
        'person_id': v['person_id'], 'name': v['name'], 'level': v['level'],
        'p4_collect': v['p4_collect'], 'orgs': v['orgs'], 'title': v['titles'][0],
    }
json.dump(plist, open(f'{D}/_p4_person_list.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

p = json.load(open(f'{D}/_phase_progress.json', encoding='utf-8'))
p['p4_scope'] = {
    'rule': 'GOV/PARTY/MIL all levels; other types high only',
    'total_persons': len(persons),
    'in_scope': sum(1 for v in persons.values() if v['p4_collect']),
    'excluded': sum(1 for v in persons.values() if not v['p4_collect']),
    'in_scope_by_type': dict(ins_by),
    'list_file': '_p4_person_list.json',
    'decided_at': '2026-10-06',
}
p['last_updated'] = datetime.datetime.now().isoformat(timespec='seconds')
json.dump(p, open(f'{D}/_phase_progress.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

order = ['GOV', 'PARTY', 'MIL', 'SOE', 'CORP', 'FIN', 'ACAD', 'MEDIA', 'NGO', 'INTL']
print('=== P4 SCOPE: GOV/PARTY/MIL all levels; others high only ===')
print()
print(f"{'type':<6} {'persons':>8} {'in_p4':>6}")
tot = 0
for c in order:
    allv = [r for r in persons.values() if c in {t for _, t in r['orgs']}]
    inv = [r for r in allv if r['p4_collect']]
    print(f'{c:<6} {len(allv):>8} {len(inv):>6}')
    tot += len(inv)
print(f"{'TOTAL':<6} {len(persons):>8} {tot:>6}")
print()
print('excluded:', len(persons) - tot)

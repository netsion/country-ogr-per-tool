# Extract P4 person list from org key_people, dedupe, classify importance, stats by org_type x level.
import json, os, re, collections

D = 'output/ma/2026-10-05'
orgs = {}
for f in sorted(os.listdir(f'{D}/orgs')):
    if f.endswith('.json') and not f.startswith('_'):
        o = json.load(open(f'{D}/orgs/{f}', encoding='utf-8'))
        orgs[o['org_id']] = o

# person_id -> record; also dedupe null-id persons by latin name
persons = {}
def latin(nm):
    m = re.search(r'\(([^)]+)\)', nm or '')
    return (m.group(1) if m else nm or '').strip().lower()

def classify(title, org_type):
    t = (title or '')
    if re.search(r'前任|前^|创始人|历史|已故|名誉|former', t):
        return 'low'
    if re.search(r'国王|政府首脑|首相|王储|总书记|大臣|部长|总裁|董事长|行长|总干事|署长|台长|社长|总监察长|总司令|主席|校长|局长|理事长', t):
        return 'high'
    if re.search(r'副|国务秘书|部级代表|秘书长|总监|司长|主任|董事|理事|总编辑|发言人|主编', t):
        return 'medium'
    return 'medium'  # named officials default medium; unnamed-but-listed are still notable

RANK = {'high': 0, 'medium': 1, 'low': 2}
for oid, o in orgs.items():
    otype = o['basic_info']['org_type']
    for i, kp in enumerate(o.get('key_people') or []):
        pid = kp.get('person_id')
        nm = (kp.get('name') or '').strip()
        if not nm:
            continue
        key = pid or ('name:' + latin(nm))
        lvl = classify(kp.get('title'), otype)
        rec = persons.setdefault(key, {
            'person_id': pid, 'name': nm, 'orgs': [], 'levels': [], 'titles': [],
        })
        rec['orgs'].append((oid, otype))
        rec['levels'].append(lvl)
        rec['titles'].append(kp.get('title') or '')

# final level = highest across orgs
for rec in persons.values():
    rec['level'] = min(rec['levels'], key=lambda x: RANK[x])

# stats
cat_level = collections.Counter()
level_tot = collections.Counter()
by_orgtype_persons = collections.defaultdict(set)
for rec in persons.values():
    level_tot[rec['level']] += 1
    # attribute person to the org where their level was achieved (first org with best level)
    best = min(range(len(rec['levels'])), key=lambda i: RANK[rec['levels'][i]])
    otype = rec['orgs'][best][1]
    cat_level[(otype, rec['level'])] += 1
    by_orgtype_persons[otype].add(rec['name'])

print('=== P4 PERSON LIST ===')
print('unique persons:', len(persons))
print('by level:', dict(level_tot))
order = ['GOV', 'SOE', 'CORP', 'FIN', 'ACAD', 'MEDIA', 'PARTY', 'NGO', 'MIL', 'INTL']
print()
print(f"{'org_type':10s} {'high':>5s} {'medium':>7s} {'low':>5s} {'total':>6s}")
gt = collections.Counter()
for c in order:
    h = cat_level.get((c, 'high'), 0); m = cat_level.get((c, 'medium'), 0); l = cat_level.get((c, 'low'), 0)
    gt['high'] += h; gt['medium'] += m; gt['low'] += l
    print(f'{c:10s} {h:5d} {m:7d} {l:5d} {h+m+l:6d}')
print(f"{'TOTAL':10s} {gt['high']:5d} {gt['medium']:7d} {gt['low']:5d} {sum(gt.values()):6d}")
print()
# high list sample
print('--- HIGH (top leaders) ---')
for rec in sorted(persons.values(), key=lambda r: r['name']):
    if rec['level'] == 'high':
        best = min(range(len(rec['levels'])), key=lambda i: RANK[rec['levels'][i]])
        print(' ', rec['name'], '|', rec['titles'][best], '@', rec['orgs'][best][0])
# low list sample
print('--- LOW (sample 15) ---')
lows = [r for r in persons.values() if r['level'] == 'low']
for rec in lows[:15]:
    print(' ', rec['name'], '|', rec['titles'][0], '@', rec['orgs'][0][0])
print('  ... total low:', len(lows))
# with/without person_id
withid = sum(1 for r in persons.values() if r['person_id'])
print()
print('with registry person_id:', withid, '| to register in P4:', len(persons) - withid)
json.dump({k: {'person_id': v['person_id'], 'name': v['name'], 'level': v['level'],
               'orgs': v['orgs'], 'title': v['titles'][0]} for k, v in persons.items()},
          open(f'{D}/_p4_person_list.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved:', f'{D}/_p4_person_list.json')

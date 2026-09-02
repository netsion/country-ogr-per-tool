"""Reconcile null person_ids in HK org key_people against existing person registry; assign new IDs from 1207."""
import json, glob, os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ORG_DIR = 'output/hk/2026-07-24/orgs'
REG = 'output/hk/2026-07-24/id_registry.json'

def name_core(s):
    """Extract Chinese name core: strip parenthetical English, English words, spaces."""
    if not s: return ''
    s = s.split('(')[0].split('（')[0]
    s = re.sub(r'[A-Za-z·.\s/-]+', ' ', s).strip()
    return s.replace(' ', '')

# Build match map from registry (all entries: profiled + listed)
reg = json.load(open(REG, encoding='utf-8'))
pr = reg.get('person_registry') or []
by_core = {}
for e in pr:
    pid = e.get('person_id')
    n = e.get('name')
    if not pid or not n: continue
    c = name_core(n)
    if c and c not in by_core:
        by_core[c] = pid

# Existing explicit fixes
FIX = {
    '白德利': 'HK-PERSON-000512',
    '李佩诗': 'HK-PERSON-000706',
    '黄毓民': 'HK-PERSON-000218',
}

next_id = 1207
def mint():
    global next_id
    pid = f'HK-PERSON-{next_id:06d}'
    next_id += 1
    return pid

matched, minted, unresolved = [], [], []
for f in sorted(glob.glob(os.path.join(ORG_DIR, 'HK-*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    oid = d.get('org_id')
    changed = False
    for kp in d.get('key_people') or []:
        if kp.get('person_id') is not None: continue
        raw = kp.get('name') or ''
        core = name_core(raw)
        if not core:
            unresolved.append((oid, raw, 'no core name')); continue
        if '/' in core or '／' in raw:
            unresolved.append((oid, raw, 'composite name — manual')); continue
        pid = FIX.get(core) or by_core.get(core)
        if pid:
            kp['person_id'] = pid
            matched.append((oid, core, pid))
            changed = True
        else:
            pid = mint()
            kp['person_id'] = pid
            minted.append((oid, core, pid, kp.get('title') or ''))
            # add to map to dedupe within run
            by_core[core] = pid
            changed = True
    if changed:
        tmp = f + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as out:
            json.dump(d, out, ensure_ascii=False, indent=2)
        os.replace(tmp, f)

# Append minted persons to registry as 'listed'
new_entries = []
for oid, core, pid, title in minted:
    # find original display name from org file
    disp = core
    for f in glob.glob(os.path.join(ORG_DIR, 'HK-*.json')):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('org_id') != oid: continue
        for kp in d.get('key_people') or []:
            if kp.get('person_id') == pid:
                disp = kp.get('name'); break
        if disp != core: break
    new_entries.append({'person_id': pid, 'name': disp, 'wikidata_qid': None, 'status': 'listed', 'source_orgs': [oid]})

reg['person_registry'] = sorted(pr + new_entries, key=lambda e: e.get('person_id') or '')
reg['person_counters'] = {'listed': sum(1 for e in reg['person_registry'] if e.get('status')=='listed'),
                          'profiled': sum(1 for e in reg['person_registry'] if e.get('status')=='profiled')}
tmp = REG + '.tmp'
with open(tmp, 'w', encoding='utf-8') as out:
    json.dump(reg, out, ensure_ascii=False, indent=2)
os.replace(tmp, REG)

print(f'matched to existing IDs: {len(matched)}')
for m in matched: print(f'  {m[0]}: {m[1]} -> {m[2]}')
print(f'minted new IDs (from 1207): {len(minted)}')
for m in minted: print(f'  {m[0]}: {m[1]} -> {m[2]} ({m[3][:30]})')
print(f'unresolved (manual): {len(unresolved)}')
for u in unresolved: print(f'  {u[0]}: {u[1]!r} ({u[2]})')
print(f'registry person entries now: {len(reg["person_registry"])} (next_id ended at {next_id})')

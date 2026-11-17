"""Reconcile ID org key_people: remove mislinks, match nulls, mint new IDs, update registry."""
import json, glob, os, re, sys, io, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ORG_DIR = 'output/id/2026-07-27/orgs'
REG = 'output/id/2026-07-27/id_registry.json'

def norm(s):
    if not s: return ''
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', s.lower())

def latin_core(s):
    """Extract Latin name from '中文译名 (Latin Name)' format."""
    if not s: return ''
    m = re.search(r'\(([^)]+)\)', s)
    if m: return norm(m.group(1))
    return norm(s)

# --- registry map ---
reg = json.load(open(REG, encoding='utf-8'))
pr = reg.get('person_registry') or []
by_latin = {}
for e in pr:
    c = latin_core(e.get('name') or '')
    if c and len(c) >= 4 and c not in by_latin:
        by_latin[c] = e['person_id']

# find max existing person number
mx = 0
for f in glob.glob('output/id/2026-07-27/persons/ID-PERSON-*.json'):
    m = re.search(r'(\d{6})\.json$', f)
    if m: mx = max(mx, int(m.group(1)))
for e in pr:
    m = re.search(r'(\d{6})$', e.get('person_id') or '')
    if m: mx = max(mx, int(m.group(1)))
next_num = mx + 1
print(f'max existing person num: {mx}, minting from {next_num}')

UNI_KEEP = re.compile(r'校长|院長|院长|副校长|创始人|基金会|Rektor|rektor|yayasan|Yayasan|基金会主席|教授')

removed_mislinks = []
matched, minted = [], []

for f in sorted(glob.glob(os.path.join(ORG_DIR, 'ID-*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    oid = d.get('org_id') or (d.get('basic_info') or {}).get('org_id')
    kp = d.get('key_people') or []
    if not kp: continue
    changed = False
    new_kp = []
    for k in kp:
        pid = k.get('person_id')
        title = k.get('title') or ''
        name = k.get('name') or ''
        # 1. ACAD-003 prune: keep only university-related among the 90-person noise
        if oid == 'ID-ACAD-003' and pid and not UNI_KEEP.search(title):
            removed_mislinks.append((oid, pid, name[:30], title[:20]))
            changed = True
            continue
        new_kp.append(k)
    d['key_people'] = new_kp
    # 2. null matching
    for k in d['key_people']:
        if k.get('person_id') is not None: continue
        c = latin_core(k.get('name'))
        if not c or len(c) < 4: continue
        if c in by_latin:
            k['person_id'] = by_latin[c]
            matched.append((oid, k.get('name')[:25], by_latin[c]))
            changed = True
        else:
            pid = f'ID-PERSON-{next_num:06d}'
            next_num += 1
            k['person_id'] = pid
            by_latin[c] = pid
            minted.append((oid, k.get('name')[:30], pid, (k.get('title') or '')[:30]))
            changed = True
    if changed:
        tmp = f + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as o:
            json.dump(d, o, ensure_ascii=False, indent=2)
        os.replace(tmp, f)

# --- registry update: add minted as listed ---
new_entries = []
for oid, name, pid, title in minted:
    disp = name
    for f in glob.glob(os.path.join(ORG_DIR, 'ID-*.json')):
        d2 = json.load(open(f, encoding='utf-8'))
        if d2.get('org_id') != oid and (d2.get('basic_info') or {}).get('org_id') != oid: continue
        for k in d2.get('key_people') or []:
            if k.get('person_id') == pid:
                disp = k.get('name'); break
        break
    new_entries.append({'person_id': pid, 'name': disp, 'wikidata_qid': None, 'status': 'listed', 'source_orgs': [oid]})

reg['person_registry'] = sorted(pr + new_entries, key=lambda e: e.get('person_id') or '')
from collections import Counter
st = Counter(e.get('status') for e in reg['person_registry'])
reg['person_counters'] = dict(st)
reg['persons_count'] = len(reg['person_registry'])
tmp = REG + '.tmp'
with open(tmp, 'w', encoding='utf-8') as o:
    json.dump(reg, o, ensure_ascii=False, indent=2)
os.replace(tmp, REG)

print(f'mislinks removed: {len(removed_mislinks)} (ACAD-003 prune)')
print(f'matched to existing: {len(matched)}')
for m in matched[:30]: print('  ', m)
print(f'minted new IDs: {len(minted)} (range {next_num - len(minted)}-{next_num - 1})')
for m in minted[:20]: print('  ', m)
print(f'registry persons now: {len(reg["person_registry"])}')

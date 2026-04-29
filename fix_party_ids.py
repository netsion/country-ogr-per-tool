import json, glob

def load_json(fn):
    with open(fn, encoding='utf-8') as f:
        return json.load(f)

def save_json(fn, d):
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

base = 'output/my/2026-04-17/orgs'

# Search for person_ids by name keywords
def find_pid(keyword):
    for f in glob.glob('output/my/2026-04-17/persons/MY-PERSON-*.json'):
        try:
            with open(f, encoding='utf-8') as fh:
                d = json.load(fh)
            if keyword.lower() in d.get('name_en','').lower():
                return d['person_id']
        except: pass
    return None

fixes_log = []

# ===== FIX 1: MY-PARTY-001 (UMNO) =====
fn = f'{base}/MY-PARTY-001.json'
d = load_json(fn)
for re in d['related_entities']:
    if re.get('org_id') == 'MY-PARTY-011':
        re['org_id'] = 'MY-PARTY-006'
        fixes_log.append('UMNO related: MY-PARTY-011 (PBB) -> MY-PARTY-006 (name says PH)')
for kp in d['key_people']:
    n = kp.get('name', '')
    if 'Ahmad Zahid' in n or '\u963f\u672b\u624e\u5e0c' in n:
        kp['person_id'] = 'MY-PERSON-000017'
        fixes_log.append('UMNO key: Zahid -> MY-PERSON-000017')
save_json(fn, d)

# ===== FIX 2: MY-PARTY-002 (PKR) =====
fn = f'{base}/MY-PARTY-002.json'
d = load_json(fn)
# key[0] maps to Lee Shin Chen! Fix to Anwar
d['key_people'][0]['person_id'] = 'MY-PERSON-000126'
fixes_log.append('PKR key[0]: MY-PERSON-000001 (Lee Shin Chen!) -> MY-PERSON-000126 (Anwar)')
# key[1] maps to Abdul Wahid Omar! Fix to null (no Nurul Izzah file)
nurul_pid = find_pid('Nurul Izzah')
if nurul_pid:
    d['key_people'][1]['person_id'] = nurul_pid
    fixes_log.append(f'PKR key[1]: MY-PERSON-000002 -> {nurul_pid} (Nurul Izzah)')
else:
    d['key_people'][1]['person_id'] = None
    fixes_log.append('PKR key[1]: MY-PERSON-000002 -> null (Nurul Izzah no file)')
# related: PAS mislinked to BN
for re in d['related_entities']:
    if re.get('org_id') == 'MY-PARTY-005' and 'PAS' in re.get('org_name','').upper():
        re['org_id'] = 'MY-PARTY-004'
        fixes_log.append('PKR related: MY-PARTY-005 (BN) -> MY-PARTY-004 (name says PAS)')
# Link known persons
kp_links = {
    'Wan Azizah': 'MY-PERSON-000278',
    'Fuziah': 'MY-PERSON-000392',
    'Saifuddin Nasution': 'MY-PERSON-000100',
    'Chang Lih Kang': 'MY-PERSON-000236',
    'Fahmi Fadzil': 'MY-PERSON-000276',
}
for kp in d['key_people']:
    n = kp.get('name', '')
    for key, pid in kp_links.items():
        if key in n:
            kp['person_id'] = pid
            fixes_log.append(f'PKR key: {key} -> {pid}')
            break
save_json(fn, d)

# ===== FIX 3: MY-PARTY-003 (DAP) =====
fn = f'{base}/MY-PARTY-003.json'
d = load_json(fn)
dap_links = {
    'Anthony Loke': 'MY-PERSON-000106',
    'Gobind Singh': 'MY-PERSON-000010',
    'Lim Guan Eng': 'MY-PERSON-000104',
    'Nga Kor Ming': 'MY-PERSON-000131',
    'Steven Sim': 'MY-PERSON-000254',
    'Hannah Yeoh': 'MY-PERSON-000025',
    'Ramkarpal': 'MY-PERSON-000343',
    'Tan Kok Wai': 'MY-PERSON-000358',
}
for kp in d['key_people']:
    n = kp.get('name', '')
    for key, pid in dap_links.items():
        if key in n:
            kp['person_id'] = pid
            fixes_log.append(f'DAP key: {key} -> {pid}')
            break
save_json(fn, d)

# ===== FIX 4: MY-PARTY-004 (PAS) =====
fn = f'{base}/MY-PARTY-004.json'
d = load_json(fn)
pas_links = {'Tuan Ibrahim': 'MY-PERSON-000192', 'Idris Ahmad': 'MY-PERSON-000219'}
for kp in d['key_people']:
    n = kp.get('name', '')
    for key, pid in pas_links.items():
        if key in n:
            kp['person_id'] = pid
            fixes_log.append(f'PAS key: {key} -> {pid}')
            break
save_json(fn, d)

# ===== FIX 5: MY-PARTY-005 (BN) =====
fn = f'{base}/MY-PARTY-005.json'
d = load_json(fn)
bn_links = {
    'Mohamad Hasan': 'MY-PERSON-000107',
    'Wee Ka Siong': 'MY-PERSON-000018',
    'Johari': 'MY-PERSON-000145',
    'Noraini': 'MY-PERSON-000300',
    'Zambry': 'MY-PERSON-000108',
    'Najib': 'MY-PERSON-000231',
    'Azalina': 'MY-PERSON-000326',
}
for kp in d['key_people']:
    n = kp.get('name', '')
    for key, pid in bn_links.items():
        if key in n:
            kp['person_id'] = pid
            fixes_log.append(f'BN key: {key} -> {pid}')
            break
save_json(fn, d)

# ===== FIX 6: MY-PARTY-006 (PH) =====
fn = f'{base}/MY-PARTY-006.json'
d = load_json(fn)
ph_links = {
    'Wan Azizah': 'MY-PERSON-000278',
    'Anthony Loke': 'MY-PERSON-000106',
    'Mohamad Sabu': 'MY-PERSON-000121',
    'Saifuddin Nasution': 'MY-PERSON-000100',
    'Fahmi Fadzil': 'MY-PERSON-000276',
}
for kp in d['key_people']:
    n = kp.get('name', '')
    for key, pid in ph_links.items():
        if key in n:
            kp['person_id'] = pid
            fixes_log.append(f'PH key: {key} -> {pid}')
            break
save_json(fn, d)

# ===== FIX 7: MY-PARTY-007 (PN) =====
fn = f'{base}/MY-PARTY-007.json'
d = load_json(fn)
pn_links = {
    'Muhyiddin': 'MY-PERSON-000020',
    'Hamzah': 'MY-PERSON-000234',
    'Azmin': 'MY-PERSON-000109',
    'Sanusi': 'MY-PERSON-000298',
    'Takiyuddin': 'MY-PERSON-000186',
    'Radzi': 'MY-PERSON-000279',
}
for kp in d['key_people']:
    n = kp.get('name', '')
    for key, pid in pn_links.items():
        if key in n:
            kp['person_id'] = pid
            fixes_log.append(f'PN key: {key} -> {pid}')
            break
save_json(fn, d)

# ===== FIX 8: MY-PARTY-010 (AMANAH) =====
fn = f'{base}/MY-PARTY-010.json'
d = load_json(fn)
amanah_links = {
    'Mohamad Sabu': 'MY-PERSON-000121',
    'Mujahid': 'MY-PERSON-000380',
    'Mohd Hatta': 'MY-PERSON-000399',
    'Dzulkefly': 'MY-PERSON-000372',
    'Mahfuz': 'MY-PERSON-000272',
}
for kp in d['key_people']:
    n = kp.get('name', '')
    for key, pid in amanah_links.items():
        if key in n:
            kp['person_id'] = pid
            fixes_log.append(f'AMANAH key: {key} -> {pid}')
            break
save_json(fn, d)

# ===== FIX 9: MY-PARTY-013 (BERSATU) =====
fn = f'{base}/MY-PARTY-013.json'
d = load_json(fn)
for re in d['related_entities']:
    if re.get('org_id') == 'MY-PARTY-002' and 'UMNO' in re.get('org_name','').upper():
        re['org_id'] = 'MY-PERSON-000001'  # wrong, should be MY-PARTY-001
        # Actually let me fix properly
        re['org_id'] = 'MY-PARTY-001'
        fixes_log.append('BERSATU related: MY-PARTY-002 (PKR) -> MY-PARTY-001 (name says UMNO)')
save_json(fn, d)

# ===== FIX 10: MY-PARTY-015 (PBS) =====
fn = f'{base}/MY-PARTY-015.json'
d = load_json(fn)
for re in d['related_entities']:
    if re.get('org_id') == 'MY-PARTY-012' and 'GRS' in re.get('org_name','').upper():
        re['org_id'] = None
        fixes_log.append('PBS related: MY-PARTY-012 (GPS, Sarawak!) -> null (GRS is Sabah)')
    elif re.get('org_id') == 'MY-PARTY-007' and 'Barisan' in re.get('org_name',''):
        re['org_id'] = 'MY-PARTY-005'
        fixes_log.append('PBS related: MY-PARTY-007 (PN) -> MY-PARTY-005 (name says BN)')
    elif re.get('org_id') == 'MY-PARTY-016' and 'STAR' in re.get('org_name','').upper():
        re['org_id'] = None
        fixes_log.append('PBS related: MY-PARTY-016 (SUPP, Sarawak!) -> null (STAR is Sabah)')
# Also link Lo Su Fui
for kp in d['key_people']:
    if 'Lo Su Fui' in kp.get('name','') or '\u5415\u82cf\u5bcc' in kp.get('name',''):
        kp['person_id'] = 'MY-PERSON-000362'
        fixes_log.append('PBS key: Lo Su Fui -> MY-PERSON-000362')
        break
save_json(fn, d)

# ===== FIX 11: MY-PARTY-008 (MCA) =====
fn = f'{base}/MY-PARTY-008.json'
d = load_json(fn)
mca_links = {
    'Wee Jeck Seng': 'MY-PERSON-000312',
}
for kp in d['key_people']:
    n = kp.get('name', '')
    for key, pid in mca_links.items():
        if key in n:
            kp['person_id'] = pid
            fixes_log.append(f'MCA key: {key} -> {pid}')
            break
save_json(fn, d)

# ===== FIX 12: MY-PARTY-016 (SUPP) =====
fn = f'{base}/MY-PARTY-016.json'
d = load_json(fn)
supp_links = {
    'Sim Kui Hian': 'MY-PERSON-000301',
    'Richard Riot': 'MY-PERSON-000353',
    'Huang Tiong Sii': 'MY-PERSON-000354',
}
for kp in d['key_people']:
    n = kp.get('name', '')
    for key, pid in supp_links.items():
        if key in n:
            kp['person_id'] = pid
            fixes_log.append(f'SUPP key: {key} -> {pid}')
            break
save_json(fn, d)

print(f'Total fixes: {len(fixes_log)}')
for log in fixes_log:
    print(f'  {log}')

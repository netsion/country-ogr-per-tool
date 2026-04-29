import json

base = 'output/my/2026-04-17/orgs'

def load(fn):
    with open(f'{base}/{fn}', encoding='utf-8') as f:
        return json.load(f)

def save(fn, d):
    with open(f'{base}/{fn}', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

fixes = []

# ===== UMNO (MY-PARTY-001): rel[3] PAS linked to AMANAH =====
d = load('MY-PARTY-001.json')
for re in d['related_entities']:
    if re.get('org_id') == 'MY-PARTY-010' and 'PAS' in re.get('org_name','').upper():
        re['org_id'] = 'MY-PARTY-004'
        fixes.append('UMNO rel: MY-PARTY-010 (AMANAH!) -> MY-PARTY-004 (PAS)')
save('MY-PARTY-001.json', d)

# ===== DAP (MY-PARTY-003): 4 wrong person_ids =====
d = load('MY-PARTY-003.json')
dap_fixes = {
    'Lim Guan Eng': (None, 'MY-PERSON-000104'),  # was Sim Tze Tzin!
    'Tan Kok Wai': ('MY-PERSON-000014', 'MY-PERSON-000358'),  # was Oscar Ling!
    'Steven Sim': ('MY-PERSON-000205', 'MY-PERSON-000254'),  # was William Leong!
    'Ramkarpal': ('MY-PERSON-000215', 'MY-PERSON-000343'),  # was Rubiah Wang!
}
for kp in d['key_people']:
    n = kp.get('name', '')
    pid = kp.get('person_id')
    for key, (new_id, old_id) in dap_fixes.items():
        if key in n and pid == old_id:
            kp['person_id'] = new_id
            fixes.append(f'DAP key: {key} {old_id} -> {new_id}')
save('MY-PARTY-003.json', d)

# ===== BN (MY-PARTY-005): 5 wrong person_ids =====
d = load('MY-PARTY-005.json')
bn_fixes = {
    'Mohamad Hasan': (None, 'MY-PERSON-000107'),  # was Hasbi Habibollah!
    'Zambry': ('MY-PERSON-000128', 'MY-PERSON-000108'),  # was Jana Santhiran!
    'Johari': ('MY-PERSON-000274', 'MY-PERSON-000145'),  # was Abu Bakar Jais!
    'Najib': ('MY-PERSON-000013', 'MY-PERSON-000231'),  # was Tan Kar Hing!
    'Noraini': ('MY-PERSON-000299', 'MY-PERSON-000300'),  # was Aminolhuda!
}
for kp in d['key_people']:
    n = kp.get('name', '')
    pid = kp.get('person_id')
    for key, (new_id, old_id) in bn_fixes.items():
        if key in n and pid == old_id:
            kp['person_id'] = new_id
            fixes.append(f'BN key: {key} {old_id} -> {new_id}')
save('MY-PARTY-005.json', d)

# ===== PN (MY-PARTY-007): 3 wrong person_ids =====
d = load('MY-PARTY-007.json')
pn_fixes = {
    'Hamzah': ('MY-PERSON-000137', 'MY-PERSON-000234'),  # was Nordin Ahmad!
    'Azmin': (None, 'MY-PERSON-000109'),  # was Normah Osman!
    'Sanusi': ('MY-PERSON-000179', 'MY-PERSON-000298'),  # was Syed Saddiq!
}
for kp in d['key_people']:
    n = kp.get('name', '')
    pid = kp.get('person_id')
    for key, (new_id, old_id) in pn_fixes.items():
        if key in n and pid == old_id:
            kp['person_id'] = new_id
            fixes.append(f'PN key: {key} {old_id} -> {new_id}')
save('MY-PARTY-007.json', d)

# ===== AMANAH (MY-PARTY-010): 2 wrong person_ids =====
d = load('MY-PARTY-010.json')
amanah_fixes = {
    'Dzulkefly': ('MY-PERSON-000253', 'MY-PERSON-000372'),  # was Baharuddin Ahmad!
    'Mahfuz': (None, 'MY-PERSON-000272'),  # was Zahir Hassan!
}
for kp in d['key_people']:
    n = kp.get('name', '')
    pid = kp.get('person_id')
    for key, (new_id, old_id) in amanah_fixes.items():
        if key in n and pid == old_id:
            kp['person_id'] = new_id
            fixes.append(f'AMANAH key: {key} {old_id} -> {new_id}')
save('MY-PARTY-010.json', d)

# ===== SUPP (MY-PARTY-016): 2 wrong person_ids =====
d = load('MY-PARTY-016.json')
supp_fixes = {
    'Sim Kui Hian': (None, 'MY-PERSON-000301'),  # was Onn Abu Bakar!
    'Richard Riot': ('MY-PERSON-000345', 'MY-PERSON-000353'),  # was Ahmad Johnie!
}
for kp in d['key_people']:
    n = kp.get('name', '')
    pid = kp.get('person_id')
    for key, (new_id, old_id) in supp_fixes.items():
        if key in n and pid == old_id:
            kp['person_id'] = new_id
            fixes.append(f'SUPP key: {key} {old_id} -> {new_id}')
save('MY-PARTY-016.json', d)

# ===== PBS (MY-PARTY-015): Lo Su Fui wrong ID =====
d = load('MY-PARTY-015.json')
for kp in d['key_people']:
    if 'Lo Su Fui' in kp.get('name','') and kp.get('person_id') == 'MY-PERSON-000362':
        kp['person_id'] = 'MY-PERSON-000336'
        fixes.append('PBS key: Lo Su Fui MY-PERSON-000362 -> MY-PERSON-000336')
save('MY-PARTY-015.json', d)

print(f'Total fixes: {len(fixes)}')
for f in fixes:
    print(f'  {f}')

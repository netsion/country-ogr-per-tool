# Trim MA dataset to: ACAD=15, CORP=15, FIN=15 (user directive 2026-10-05).
# Removes 11 profiles, updates id_registry, records audit file, refreshes _target_orgs.json.
import json, os

D = 'output/ma/2026-10-05'

CUTS = {
    'MA-FIN-016':  'Defunct bank: merged into Attijariwafa Bank (MA-FIN-002, retained) in 2003; P1 entry itself marked defunct.',
    'MA-CORP-012': 'Lesieur Cristal: foreign-controlled (SIFCA/Savola) edible-oil processor; lowest strategic/OSINT value among 16 CORPs (energy, phosphate, telecom, retail, cement groups all retained).',
    'MA-ACAD-009': "Moulay Ismail University (Meknes): regional comprehensive university; tier already represented by retained majors.",
    'MA-ACAD-010': 'Mohamed I University (Oujda): regional university, eastern region; tier covered.',
    'MA-ACAD-011': 'Hassan First University (Settat): small regional university, weak data (score 13).',
    'MA-ACAD-012': 'Chouaib Doukkali University (El Jadida): small regional university, weak data (score 13, 0 social).',
    'MA-ACAD-013': 'Ibn Tofail University (Kenitra): regional university; tier covered.',
    'MA-ACAD-015': 'International University of Rabat: private university; weaker elite-network relevance than retained public grandes ecoles and Al Akhawayn.',
    'MA-ACAD-016': 'UM6SS: private health university; much smaller scope than retained UM6P; royal health angle coverable via P4 persons if needed.',
    'MA-ACAD-023': 'Centre national de la recherche scientifique (Q30284534): identity questionable - label collides with French CNRS; likely CNRST (funding agency); low OSINT value as collected.',
    'MA-ACAD-024': 'King Abdul-Aziz Al Saoud Foundation: small Saudi-funded Islamic-studies foundation; weak data (score 11, 0 social).',
}

# safety check: any cut org with key_people person_ids?
orphans = []
for oid in CUTS:
    p = f'{D}/orgs/{oid}.json'
    o = json.load(open(p, encoding='utf-8'))
    kps = o.get('key_people') or []
    if kps:
        orphans.append((oid, [kp.get('person_id') for kp in kps]))
print('cut orgs with key_people:', orphans or 'NONE - no person orphaning')

# 1. audit file
audit = {
    'action': 'p3_trim_2026-10-05',
    'directive': 'ACAD/CORP/FIN each trimmed to 15',
    'excluded': [{'org_id': k, 'reason': v} for k, v in CUTS.items()],
}
json.dump(audit, open(f'{D}/_excluded_orgs.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# 2. delete profile files
removed = []
for oid in CUTS:
    p = f'{D}/orgs/{oid}.json'
    if os.path.exists(p):
        os.remove(p); removed.append(oid)
print('profiles removed:', len(removed))

# 3. id_registry: drop entries (keep counters = max seq, gaps allowed as IDs are permanent)
reg = json.load(open(f'{D}/id_registry.json', encoding='utf-8'))
before = len(reg['registry'])
reg['registry'] = [r for r in reg['registry'] if r['org_id'] not in CUTS]
json.dump(reg, open(f'{D}/id_registry.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"registry: {before} -> {len(reg['registry'])}")

# 4. _target_orgs.json: drop cut entries so P3 reads the post-trim list
targets = json.load(open(f'{D}/_target_orgs.json', encoding='utf-8'))
tbefore = len(targets)
targets = [t for t in targets if t['id'] not in CUTS]
json.dump(targets, open(f'{D}/_target_orgs.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'_target_orgs: {tbefore} -> {len(targets)}')

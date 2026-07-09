"""Check KG orgs against actual schema enums."""
import json, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')

schema = json.load(open('.claude/skills/country-org-collector/org_profile_schema.json', encoding='utf-8'))
defs = schema.get('$defs', {})
IND = set(defs['industry_enum']['enum'])
RT = set(defs['relationship_type_enum']['enum'])

files = sorted(glob.glob('output/kg/2026-06-21/orgs/*.json'))
bad_rt = []  # truly invalid relationship_type
bad_ind = []  # truly invalid industries
bad_sa = []  # social_accounts not dict
bad_apec = []  # apec_stance not str/null
bad_core = []  # core_business not str/null

for f in files:
    d = json.load(open(f, encoding='utf-8'))
    pid = os.path.basename(f).replace('.json', '')
    for i, item in enumerate(d.get('related_entities', [])):
        rt = item.get('relationship_type', '')
        if rt and rt not in RT:
            bad_rt.append((pid, i, rt))
    for i, item in enumerate(d.get('industries', [])):
        if item and item not in IND:
            bad_ind.append((pid, i, item))
    for i, item in enumerate(d.get('social_accounts', [])):
        if not isinstance(item, dict):
            bad_sa.append((pid, i, type(item).__name__, str(item)[:80]))
            break
    if not isinstance(d.get('apec_stance'), (str, type(None))):
        bad_apec.append((pid, type(d.get('apec_stance')).__name__))
    if not isinstance(d.get('core_business'), (str, type(None))):
        bad_core.append((pid, type(d.get('core_business')).__name__))

print(f'=== invalid relationship_type ({len(bad_rt)}) ===')
for x in bad_rt[:30]: print(x)
print(f'=== invalid industries ({len(bad_ind)}) ===')
for x in bad_ind[:30]: print(x)
print(f'=== social_accounts not dict ({len(bad_sa)}) ===')
for x in bad_sa: print(x)
print(f'=== apec_stance not str ({len(bad_apec)}) ===')
for x in bad_apec: print(x)
print(f'=== core_business not str ({len(bad_core)}) ===')
for x in bad_core: print(x)

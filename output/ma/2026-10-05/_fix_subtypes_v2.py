# v2: re-apply name-based org_subtype overrides (v1 tuple unpacking bug made them all no-ops).
# Handles files already set to None by v1. Name overrides are decided on name+org_type alone.
import json, os

D = 'output/ma/2026-10-05/orgs'

# (name_contains, org_type, correct_subtype)
NAME_OVERRIDES = [
    ('justice and development party', 'PARTY', 'opposition_party'),  # PJD: opposition since Oct 2021
    ('educational, scientific and cultural', 'INTL', 'multilateral_org'),  # ICESCO
    ('arab civil aviation', 'INTL', 'regional_org'),
    ('local governments', 'INTL', 'regional_org'),
    ('caisse de', 'SOE', 'gov_investment_vehicle'),   # CDG
    ('maroc telecom', 'CORP', 'publicly_listed'),
    ('inwi', 'CORP', 'private_company'),
    ('orange', 'CORP', 'subsidiary'),
    ('ciments du maroc', 'CORP', 'publicly_listed'),  # both Casablanca-listed
    ('holcim', 'CORP', 'publicly_listed'),
]

changed = 0
for f in sorted(os.listdir(D)):
    if not f.endswith('.json') or f.startswith('_'):
        continue
    p = os.path.join(D, f)
    o = json.load(open(p, encoding='utf-8'))
    bi = o['basic_info']
    name = (bi.get('name_en') or '').lower()
    for key, want_type, new_val in NAME_OVERRIDES:
        if key in name and bi['org_type'] == want_type and bi.get('org_subtype') != new_val:
            old = bi.get('org_subtype')
            bi['org_subtype'] = new_val
            json.dump(o, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            changed += 1
            print(f"{f[:-5]:14s} {old!r} -> {new_val!r}")
            break
print('files changed:', changed)

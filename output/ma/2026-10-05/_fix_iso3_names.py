# Fix P1-propagated errors: country_iso3/hq_country_iso3 'MAP' -> 'MAR' (Morocco ISO 3166-1 alpha-3),
# and backfill MA-CORP-009 (Taqa Morocco) name fields from sourced _target_orgs.json entry.
import json, os

D = 'output/ma/2026-10-05/orgs'
changed = 0
for f in sorted(os.listdir(D)):
    if not f.endswith('.json') or f.startswith('_'):
        continue
    p = os.path.join(D, f)
    o = json.load(open(p, encoding='utf-8'))
    bi = o['basic_info']
    dirty = False
    if bi.get('country_iso3') == 'MAP':
        bi['country_iso3'] = 'MAR'; dirty = True
    if bi.get('hq_country_iso3') == 'MAP':
        bi['hq_country_iso3'] = 'MAR'; dirty = True
    if f == 'MA-CORP-009.json':
        # sourced from _target_orgs.json (Wikidata Q119439768): name 'Taqa Morocco',
        # alias 'طاقة المغرب', description states listing on Casablanca Stock Exchange
        bi['name_en'] = 'Taqa Morocco'
        bi['name_original'] = 'طاقة المغرب'
        bi['org_subtype'] = 'publicly_listed'
        dirty = True
    if dirty:
        json.dump(o, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        changed += 1
print('files changed:', changed)

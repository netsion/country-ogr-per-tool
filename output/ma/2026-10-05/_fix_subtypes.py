# One-off P2 fix: normalize org_subtype Title Case values to enum_reference.md snake_case enums.
# Unverifiable classifications are set to null (iron rule: prefer empty over fabricating); P3 re-verifies.
import json, os

D = 'output/ma/2026-10-05/orgs'

VALID = {
    'GOV': {'head_of_state','cabinet','ministry','statutory_board','regulatory_agency','legislature','judiciary','independent_organ','gov_department','local_government'},
    'SOE': {'state_owned_enterprise','sovereign_wealth_fund','gov_linked_company','gov_investment_vehicle'},
    'CORP': {'publicly_listed','private_company','startup','subsidiary','joint_venture','holding_company','conglomerate'},
    'NGO': {'charity','foundation','advocacy_group','professional_association','trade_union','humanitarian_org','religious_org','community_org'},
    'ACAD': {'university','research_institute','think_tank','polytechnic','vocational_school'},
    'MEDIA': {'broadcaster','newspaper','news_agency','digital_media','publisher'},
    'FIN': {'commercial_bank','investment_bank','insurance_company','asset_management','fintech','payment_institution'},
    'INTL': {'multilateral_org','regional_org','standards_body'},
    'PARTY': {'ruling_party','opposition_party','coalition'},
    'MIL': {'armed_forces','intelligence_agency','security_agency','defence_technology','military_academy'},
}

MAP_COMMON = {
    'ministry': 'ministry', 'executive branch': 'cabinet', 'legislature': 'legislature',
    'judiciary': 'judiciary', 'statutory board': 'statutory_board', 'independent organ': 'independent_organ',
    'university': 'university', 'research institute': 'research_institute',
    'engineering school': 'polytechnic', 'statistics institute': 'university',
    'public administration school': 'vocational_school',
    'tv channel': 'broadcaster', 'public broadcaster': 'broadcaster', 'newspaper': 'newspaper',
    'news agency': 'news_agency', 'online news': 'digital_media', 'news magazine': 'digital_media',
    'commercial bank': 'commercial_bank', 'insurance': 'insurance_company',
    'human rights': 'advocacy_group', "women's rights": 'advocacy_group',
    'trade union': 'trade_union', 'employers association': 'professional_association',
    'foundation': 'foundation', 'development': 'foundation', 'international cooperation': 'humanitarian_org',
    'sports federation': 'professional_association',
    'military': 'armed_forces', 'gendarmerie': 'armed_forces',
    'intelligence': 'intelligence_agency', 'police': 'security_agency',
    'conglomerate': 'conglomerate',
}

NAME_OVERRIDES = [
    # (name_contains, org_type, subtype)
    ('justice and development party', 'PARTY', 'opposition_party'),  # PJD: opposition since Oct 2021
    ('icesco', 'INTL', 'multilateral_org'),
    ('arab civil aviation', 'INTL', 'regional_org'),
    ('local governments', 'INTL', 'regional_org'),
    ('caisse de', 'SOE', 'gov_investment_vehicle'),   # CDG
    ('maroc telecom', 'CORP', 'publicly_listed'),
    ('inwi', 'CORP', 'private_company'),
    ('orange', 'CORP', 'subsidiary'),
    ('ciments du maroc', 'CORP', 'publicly_listed'),  # both Casablanca-listed
    ('holcim', 'CORP', 'publicly_listed'),
]

def fix(org_type, subtype, name_en):
    if subtype is None:
        return None, 'keep-null'
    norm = subtype.replace('_', ' ').strip().lower()
    # already valid (spaces or underscores)
    if norm.replace(' ', '_') in VALID[org_type]:
        return norm.replace(' ', '_'), 'already-valid'
    for key, val, want in NAME_OVERRIDES:
        if key in (name_en or '').lower() and org_type == want:
            return val, 'name-override'
    if org_type == 'SOE':
        return 'state_owned_enterprise', 'soe-default'
    if org_type == 'NGO' and norm == 'anti-corruption':
        return 'advocacy_group', 'mapped'
    if org_type == 'GOV' and norm == 'anti-corruption':
        return 'independent_organ', 'mapped'
    if org_type == 'GOV' and norm == 'regulator':
        return 'regulatory_agency', 'mapped'
    if norm in MAP_COMMON:
        mapped = MAP_COMMON[norm]
        return (mapped, 'mapped') if mapped in VALID[org_type] else (None, 'mapped-out-of-type')
    return None, 'null-unverifiable'

changed = 0
for f in sorted(os.listdir(D)):
    if not f.endswith('.json') or f.startswith('_'):
        continue
    p = os.path.join(D, f)
    o = json.load(open(p, encoding='utf-8'))
    bi = o['basic_info']
    old = bi.get('org_subtype')
    new, how = fix(bi['org_type'], old, bi.get('name_en'))
    if new != old:
        bi['org_subtype'] = new
        json.dump(o, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        changed += 1
        if old:
            print(f"{f[:-5]:14s} {how:20s} {old!r} -> {new!r}")
print('files changed:', changed)

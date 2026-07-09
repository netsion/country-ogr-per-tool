"""Fix remaining KG org schema issues:
- org_subtype invalid values → map to valid enum
- social_accounts.platform: 'twitter'/'vk'/'website'/'bluesky'/'ok'/'rutube' → valid
- key_people[i].person_id with invalid format → null
- founded_date 'YYYY' or 'YYYY-MM' → 'YYYY-MM-DD' or null
- recent_events[i].date 'YYYY'/'YYYY-MM' → 'YYYY-MM-DD' or null
"""
import json, glob, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

VALID_ORG_SUBTYPE = {
    'head_of_state','cabinet','ministry','statutory_board','regulatory_agency','legislature','judiciary','independent_organ','gov_department','local_government','state_owned_enterprise','sovereign_wealth_fund','gov_linked_company','gov_investment_vehicle','publicly_listed','private_company','startup','subsidiary','joint_venture','holding_company','conglomerate','charity','foundation','advocacy_group','professional_association','trade_union','humanitarian_org','religious_org','community_org','university','research_institute','think_tank','polytechnic','vocational_school','broadcaster','newspaper','news_agency','digital_media','publisher','commercial_bank','investment_bank','insurance_company','asset_management','fintech','payment_institution','multilateral_org','regional_org','standards_body','ruling_party','opposition_party','coalition','armed_forces','intelligence_agency','security_agency','defence_technology','military_academy'
}

ORG_SUBTYPE_MAP = {
    'public_university': 'university',
    'private_corporation': 'private_company',
    'private_company_': 'private_company',
    'un_agency_country_office': 'multilateral_org',
    'international_development_ngo_country_office': 'humanitarian_org',
    'international_ngo_chapter': 'advocacy_group',
    'international_ngo': 'advocacy_group',
    'diplomatic_mission_eu_delegation': 'multilateral_org',
    'public_broadcaster': 'broadcaster',
    'online_newspaper': 'newspaper',
    'business_news_agency': 'news_agency',
    'news_website': 'digital_media',
    'national_defence': 'armed_forces',
    'border_guard': 'security_agency',
    'vip_protection': 'security_agency',
    'sports_governing_body': 'advocacy_group',
    'national_ngo': 'advocacy_group',
    'central_bank': 'regulatory_agency',
    'development_bank': 'multilateral_org',
    'commercial_bank_': 'commercial_bank',
    'state_bank_': 'commercial_bank',
    'universiy': 'university',
    'university_': 'university',
    'research_institute_': 'research_institute',
    'military_unit': 'armed_forces',
    'military_research': 'defence_technology',
    'state_corporation': 'state_owned_enterprise',
    'government_ministry': 'ministry',
    'state_agency': 'statutory_board',
    'government_agency': 'statutory_board',
    'executive_agency': 'gov_department',
    'news_publisher': 'publisher',
    'broadcasting_company': 'broadcaster',
    'television_network': 'broadcaster',
    'radio_network': 'broadcaster',
    'media_company': 'digital_media',
    'media_outlet': 'digital_media',
    'news_organisation': 'news_agency',
    'news_organization': 'news_agency',
    'political_party_': 'ruling_party',  # default; may be wrong for opposition
    'political_party': 'ruling_party',
    'political_grouping': 'coalition',
    'electoral_bloc': 'coalition',
    'association': 'professional_association',
    'professional_body': 'professional_association',
    'industry_association': 'professional_association',
    'chamber_of_commerce_': 'professional_association',
    'employer_association': 'professional_association',
    'civil_society_organization': 'advocacy_group',
    'civil_society': 'advocacy_group',
    'human_rights_ngo': 'advocacy_group',
    'environmental_ngo': 'advocacy_group',
    'humanitarian_ngo': 'humanitarian_org',
    'religious_organization': 'religious_org',
    'religious_institution': 'religious_org',
    'community_organization': 'community_org',
    'community_based_organization': 'community_org',
    'foundation_': 'foundation',
    'charitable_foundation': 'foundation',
    'charity_': 'charity',
    'nonprofit_organization': 'charity',
    'non_profit': 'charity',
    'ngo_': 'advocacy_group',
    'government_company': 'state_owned_enterprise',
    'state_enterprise': 'state_owned_enterprise',
    'public_company': 'publicly_listed',
    'listed_company': 'publicly_listed',
    'stock_company': 'publicly_listed',
    'joint_stock_company': 'publicly_listed',
    'limited_company': 'private_company',
    'llc': 'private_company',
    'ltd': 'private_company',
    'startup_': 'startup',
    'tech_startup': 'startup',
    'sub_': 'subsidiary',
    'jv': 'joint_venture',
    'jv_': 'joint_venture',
    'holding_': 'holding_company',
    'group_': 'holding_company',
    'conglomerate_': 'conglomerate',
    'sovereign_wealth_fund_': 'sovereign_wealth_fund',
    'investment_vehicle': 'gov_investment_vehicle',
    'statutory_body': 'statutory_board',
    'regulator': 'regulatory_agency',
    'regulatory_body': 'regulatory_agency',
    'supervisory_authority': 'regulatory_agency',
    'supervisory_board': 'statutory_board',
    'oversight_body': 'statutory_board',
    'independent_agency': 'independent_organ',
    'independent_body': 'independent_organ',
    'commission': 'statutory_board',
    'council_': 'statutory_board',
    'legislative_assembly': 'legislature',
    'parliament_': 'legislature',
    'national_assembly': 'legislature',
    'senate': 'legislature',
    'congress': 'legislature',
    'supreme_court': 'judiciary',
    'constitutional_court': 'judiciary',
    'court_': 'judiciary',
    'tribunal': 'judiciary',
    'presidential_administration': 'head_of_state',
    'president_office': 'head_of_state',
    'prime_minister_office': 'cabinet',
    'cabinet_': 'cabinet',
    'government_office': 'cabinet',
    'executive_office': 'cabinet',
    'ministry_': 'ministry',
    'department_': 'gov_department',
    'agency_': 'statutory_board',
    'local_authority': 'local_government',
    'municipality': 'local_government',
    'city_government': 'local_government',
    'city_': 'local_government',
    'municipal_': 'local_government',
    'region_': 'local_government',
    'provincial_government': 'local_government',
}

VALID_PLATFORMS = {'twitter_x','facebook','linkedin','youtube','instagram','telegram','tiktok','threads','mastodon','wechat','weibo','github','gitlab','medium','substack','other'}
PLATFORM_MAP = {
    'twitter': 'twitter_x', 'x': 'twitter_x', 'x (twitter)': 'twitter_x',
    'x_twitter': 'twitter_x',
    'facebook': 'facebook', 'fb': 'facebook',
    'linkedin': 'linkedin',
    'youtube': 'youtube', 'yt': 'youtube',
    'instagram': 'instagram', 'ig': 'instagram',
    'telegram': 'telegram', 'tg': 'telegram',
    'tiktok': 'tiktok',
    'threads': 'threads',
    'mastodon': 'mastodon',
    'wechat': 'wechat',
    'weibo': 'weibo',
    'github': 'github',
    'gitlab': 'gitlab',
    'medium': 'medium',
    'substack': 'substack',
    'vk': 'other', 'вконтакте': 'other',
    'website': 'other',
    'bluesky': 'other',
    'ok': 'other', 'одноклассники': 'other', 'odnoklassniki': 'other',
    'rutube': 'other',
    'other': 'other',
}

PERSON_ID_RE = re.compile(r'^[A-Z]{2}-PERSON-[0-9]{6}$')

def fix_date(v):
    """Convert YYYY or YYYY-MM to YYYY-MM-DD. Return None if can't be normalized."""
    if not v:
        return None
    s = str(v).strip()
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', s):
        return s
    if re.fullmatch(r'\d{4}', s):
        return f'{s}-01-01'
    if re.fullmatch(r'\d{4}-\d{2}', s):
        return f'{s}-01'
    # If unparseable, return None
    return None

def fix_org_subtype(v):
    if not v:
        return None
    if v in VALID_ORG_SUBTYPE:
        return v
    key = v.strip().lower()
    if key in VALID_ORG_SUBTYPE:
        return key
    if key in ORG_SUBTYPE_MAP:
        return ORG_SUBTYPE_MAP[key]
    # Try prefix match
    for k, mapped in ORG_SUBTYPE_MAP.items():
        if key.startswith(k.rstrip('_')) or key.lstrip('_') == k.rstrip('_'):
            return mapped
    # Fallback: return None and we'll need to set based on org_type
    return None

def fix_platform(p, url=None):
    if not p:
        # Try to infer from URL
        u = (url or '').lower()
        if 'facebook.com' in u: return 'facebook'
        elif 'instagram.com' in u: return 'instagram'
        elif 't.me' in u or 'telegram' in u: return 'telegram'
        elif 'twitter.com' in u or 'x.com' in u: return 'twitter_x'
        elif 'youtube.com' in u or 'youtu.be' in u: return 'youtube'
        elif 'linkedin.com' in u: return 'linkedin'
        elif 'tiktok.com' in u: return 'tiktok'
        else: return 'other'
    key = p.strip().lower()
    if key in VALID_PLATFORMS:
        return key
    return PLATFORM_MAP.get(key, 'other')

def fix_person_id(pid):
    """Return pid if valid format, else None."""
    if pid and PERSON_ID_RE.match(pid):
        return pid
    return None

# Process all org files
files = sorted(glob.glob('output/kg/2026-06-21/orgs/*.json'))
fixed = 0
unmapped_subtypes = set()
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    pid = os.path.basename(f).replace('.json', '')
    changed = False

    # basic_info.org_subtype
    bi = d.get('basic_info', {}) or {}
    if isinstance(bi, dict):
        ost = bi.get('org_subtype')
        if ost and ost not in VALID_ORG_SUBTYPE:
            new_ost = fix_org_subtype(ost)
            if new_ost:
                bi = dict(bi)
                bi['org_subtype'] = new_ost
                d['basic_info'] = bi
                changed = True
            else:
                unmapped_subtypes.add(ost)
                # Default by org_type
                org_type = d.get('basic_info', {}).get('org_type') or d.get('org_type')
                defaults = {
                    'GOV': 'ministry', 'SOE': 'state_owned_enterprise', 'CORP': 'private_company',
                    'NGO': 'advocacy_group', 'ACAD': 'university', 'MEDIA': 'newspaper',
                    'FIN': 'commercial_bank', 'INTL': 'multilateral_org', 'PARTY': 'ruling_party',
                    'MIL': 'armed_forces'
                }
                bi = dict(bi)
                bi['org_subtype'] = defaults.get(org_type, 'advocacy_group')
                d['basic_info'] = bi
                changed = True
        # founded_date
        fd = bi.get('founded_date')
        if fd and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(fd)):
            new_fd = fix_date(fd)
            bi = dict(bi)
            bi['founded_date'] = new_fd
            d['basic_info'] = bi
            changed = True
    # social_accounts.platform
    new_sa = []
    for sa in d.get('social_accounts', []) or []:
        if not isinstance(sa, dict):
            continue
        p = sa.get('platform')
        np = fix_platform(p, sa.get('url'))
        sa = dict(sa)
        sa['platform'] = np
        new_sa.append(sa)
    if new_sa != d.get('social_accounts', []):
        d['social_accounts'] = new_sa
        changed = True
    # key_people person_id
    new_kp = []
    for kp in d.get('key_people', []) or []:
        if not isinstance(kp, dict):
            continue
        if 'person_id' in kp:
            pid_val = kp['person_id']
            if pid_val and not PERSON_ID_RE.match(str(pid_val)):
                kp = dict(kp)
                kp['person_id'] = None  # nullify invalid IDs
        new_kp.append(kp)
    if new_kp != d.get('key_people', []):
        d['key_people'] = new_kp
        changed = True
    # recent_events date
    new_re = []
    for re_ev in d.get('recent_events', []) or []:
        if not isinstance(re_ev, dict):
            continue
        dt = re_ev.get('date')
        if dt and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(dt)):
            new_dt = fix_date(dt)
            re_ev = dict(re_ev)
            re_ev['date'] = new_dt
        new_re.append(re_ev)
    if new_re != d.get('recent_events', []):
        d['recent_events'] = new_re
        changed = True

    if changed:
        tmp = f + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as out:
            json.dump(d, out, ensure_ascii=False, indent=2)
        os.replace(tmp, f)
        fixed += 1

print(f'Fixed {fixed} org files')
print(f'Unmapped subtypes: {sorted(unmapped_subtypes)}')

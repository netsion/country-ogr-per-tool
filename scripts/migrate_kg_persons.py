"""Migrate 26 nested KG person files (PERSON-000001..000026) to flat schema."""
import json, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')

PLATFORM_MAP = {
    'facebook': 'facebook',
    'fb': 'facebook',
    'instagram': 'instagram',
    'ig': 'instagram',
    'twitter': 'twitter',
    'x (twitter)': 'twitter',
    'x': 'twitter',
    'telegram (personal channel)': 'telegram',
    'telegram (presidential channel)': 'telegram',
    'telegram (official channel)': 'telegram',
    'telegram': 'telegram',
    'tg': 'telegram',
    'vk (вконтакте)': 'vk',
    'vk': 'vk',
    'вконтакте': 'vk',
    'youtube': 'youtube',
    'yt': 'youtube',
    'linkedin': 'linkedin',
    'tiktok': 'tiktok',
    'website': 'website',
    'одноклассники': 'odnoklassniki',
    'ok': 'odnoklassniki',
    'wechat': 'wechat',
    'weibo': 'weibo',
}

def normalize_platform(p):
    if not p:
        return None
    key = p.strip().lower()
    return PLATFORM_MAP.get(key, key if key in PLATFORM_MAP.values() else None)

def normalize_social_accounts(items):
    """Ensure each item is a dict with valid platform."""
    out = []
    if not isinstance(items, list):
        return out
    for item in items:
        if isinstance(item, str):
            # Bare string - try to detect from URL
            url_lower = item.lower()
            if 'facebook.com' in url_lower:
                p = 'facebook'
            elif 'instagram.com' in url_lower:
                p = 'instagram'
            elif 't.me' in url_lower or 'telegram' in url_lower:
                p = 'telegram'
            elif 'vk.com' in url_lower:
                p = 'vk'
            elif 'twitter.com' in url_lower or 'x.com' in url_lower:
                p = 'twitter'
            elif 'youtube.com' in url_lower or 'youtu.be' in url_lower:
                p = 'youtube'
            elif 'linkedin.com' in url_lower:
                p = 'linkedin'
            else:
                # Skip bare URL with no detectable platform
                continue
            out.append({'platform': p, 'url': item, 'username': None})
            continue
        if not isinstance(item, dict):
            continue
        p = item.get('platform') or item.get('type') or item.get('name')
        np = normalize_platform(p) if p else None
        if not np:
            # Try to infer from URL
            url = item.get('url', '')
            url_lower = (url or '').lower()
            for hint, plat in [('facebook.com','facebook'),('instagram.com','instagram'),('t.me','telegram'),('telegram','telegram'),('vk.com','vk'),('twitter.com','twitter'),('x.com','twitter'),('youtube.com','youtube'),('youtu.be','youtube'),('linkedin.com','linkedin'),('tiktok.com','tiktok')]:
                if hint in url_lower:
                    np = plat
                    break
        if not np:
            continue
        new_item = {'platform': np}
        if item.get('url'):
            new_item['url'] = item['url']
        if item.get('username') or item.get('handle') or item.get('account'):
            new_item['username'] = item.get('username') or item.get('handle') or item.get('account')
        if item.get('source'):
            new_item['source'] = item['source']
        out.append(new_item)
    return out

def migrate(d, pid):
    """Migrate nested person dict to flat schema."""
    bi = d.get('basic_info', {}) or {}
    flat = {'person_id': pid}
    # Direct fields
    if d.get('wikidata_qid'):
        flat['wikidata_qid'] = d['wikidata_qid']
    else:
        flat['wikidata_qid'] = None
    flat['name'] = bi.get('name') or d.get('name') or ''
    flat['name_en'] = bi.get('name_en') or d.get('name_en') or ''
    flat['name_zh'] = bi.get('name_zh') or d.get('name_zh') or bi.get('name_chinese')
    flat['aliases'] = bi.get('aliases') or d.get('aliases') or []
    flat['nationality'] = bi.get('nationality') or d.get('nationality') or 'KG'
    flat['gender'] = bi.get('gender') or d.get('gender')
    flat['birth_date'] = bi.get('birth_date') or d.get('birth_date')
    flat['birth_place'] = bi.get('birth_place') or d.get('birth_place')
    # contacts - usually empty in nested
    flat['contacts'] = d.get('contacts') or []
    # current_positions from positions_held
    ph = d.get('positions_held') or []
    cp = []
    if isinstance(ph, list):
        for pos in ph:
            if isinstance(pos, dict):
                # Compose a string
                cp.append(pos.get('title') or pos.get('position') or pos.get('role') or json.dumps(pos, ensure_ascii=False))
            else:
                cp.append(str(pos))
    flat['current_positions'] = cp
    # education from basic_info.education or education_details
    edu = bi.get('education') or d.get('education') or d.get('education_details') or []
    flat['education'] = edu
    # work_experience from career_history
    flat['work_experience'] = d.get('career_history') or d.get('work_experience') or []
    # person_relationships from related_entities
    flat['person_relationships'] = d.get('related_entities') or d.get('person_relationships') or []
    # social_accounts - normalize
    flat['social_accounts'] = normalize_social_accounts(d.get('social_accounts') or [])
    # family_members from family
    flat['family_members'] = d.get('family') or d.get('family_members') or []
    # political_stances from political_affiliations
    flat['political_stances'] = d.get('political_affiliations') or d.get('political_stances') or []
    # major_achievements from awards_honors
    flat['major_achievements'] = d.get('awards_honors') or d.get('major_achievements') or []
    # biography_summary from biography
    flat['biography_summary'] = d.get('biography') or d.get('biography_summary')
    # profile
    flat['profile'] = d.get('profile')
    # collection_meta
    flat['collection_meta'] = d.get('collection_meta') or {}
    return flat

# Find nested files
files = sorted(glob.glob('output/kg/2026-06-21/persons/KG-PERSON-*.json'))
migrated = 0
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    if 'basic_info' not in d or 'name' in d:
        continue
    pid = os.path.basename(f).replace('.json', '')
    new = migrate(d, pid)
    tmp = f + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as out:
        json.dump(new, out, ensure_ascii=False, indent=2)
    os.replace(tmp, f)
    migrated += 1
print(f'Migrated {migrated} files')

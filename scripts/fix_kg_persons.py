"""Fix KG person schema issues:
- nationality: 'Kyrgyz (...)' → 'KG'
- social_accounts.platform: twitter→twitter_x, vk→other, etc.
- family_members[i] string → dict
- family_members.relationship: 'spouse (...)' → 'spouse'
- person_relationships.relationship_type: non-enum → 'other' or proper enum
- political_stances[].stance_content: from stance/summary field
- major_achievements[].achievement: from title/summary field
"""
import json, glob, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

VALID_PLATFORMS = {'twitter_x','facebook','linkedin','youtube','instagram','telegram','tiktok','threads','mastodon','wechat','weibo','github','gitlab','medium','substack','other'}
PLATFORM_MAP = {
    'twitter': 'twitter_x',
    'x': 'twitter_x',
    'x (twitter)': 'twitter_x',
    'facebook': 'facebook',
    'fb': 'facebook',
    'linkedin': 'linkedin',
    'youtube': 'youtube',
    'yt': 'youtube',
    'instagram': 'instagram',
    'ig': 'instagram',
    'telegram': 'telegram',
    'tg': 'telegram',
    'tiktok': 'tiktok',
    'threads': 'threads',
    'mastodon': 'mastodon',
    'wechat': 'wechat',
    'weibo': 'weibo',
    'github': 'github',
    'gitlab': 'gitlab',
    'medium': 'medium',
    'substack': 'substack',
    'vk': 'other',
    'вконтакте': 'other',
    'odnoklassniki': 'other',
    'website': 'other',
}

FAMILY_MAP = {
    'spouse': 'spouse', 'wife': 'spouse', 'husband': 'spouse', '配偶': 'spouse', '妻子': 'spouse', '丈夫': 'spouse', 'супруга': 'spouse', 'супруг': 'spouse',
    'father': 'father', '父亲': 'father', 'отец': 'father',
    'mother': 'mother', '母亲': 'mother', 'мать': 'mother',
    'son': 'son', '儿子': 'son', 'сын': 'son',
    'daughter': 'daughter', '女儿': 'daughter', 'дочь': 'daughter',
    'brother': 'brother', '兄弟': 'brother', 'брат': 'brother',
    'sister': 'sister', '姐妹': 'sister', '妹妹': 'sister', '姐姐': 'sister', 'сестра': 'sister',
    'grandfather': 'grandfather', '祖父': 'grandfather', 'дед': 'grandfather', '外祖父': 'grandfather',
    'grandmother': 'grandmother', '祖母': 'grandmother', 'бабушка': 'grandmother', '外祖母': 'grandmother',
    'uncle': 'uncle', '叔父': 'uncle', '舅舅': 'uncle', 'дядя': 'uncle',
    'aunt': 'aunt', '姑母': 'aunt', '阿姨': 'aunt', '姨妈': 'aunt', 'тетя': 'aunt',
    'cousin': 'cousin', '表兄弟姐妹': 'cousin', '堂兄弟姐妹': 'cousin', 'двоюродный': 'cousin', 'двоюродная': 'cousin',
    'children': 'other', '子女': 'other', 'дети': 'other',
    'child': 'other',
}

VALID_FAMILY = {'spouse','father','mother','son','daughter','brother','sister','grandfather','grandmother','uncle','aunt','cousin','father_in_law','mother_in_law','brother_in_law','sister_in_law','son_in_law','daughter_in_law','other'}

VALID_PERSON_RT = {'spouse','parent','child','sibling','grandparent','grandchild','uncle_aunt','cousin','in_law','mentor','mentee','ally','rival','colleague','superior','subordinate','business_partner','political_ally','political_rival','associate','other'}

PERSON_RT_MAP = {
    'head_of_state': 'associate',
    'head_of_government': 'associate',
    'deputy': 'colleague',
    'minister': 'colleague',
    'ally': 'political_ally',
    'rival': 'political_rival',
    'opponent': 'political_rival',
    'colleague': 'colleague',
    'business_partner': 'business_partner',
    'partner': 'business_partner',
    'mentor': 'mentor',
    'mentee': 'mentee',
    'superior': 'superior',
    'subordinate': 'subordinate',
    'spouse': 'spouse',
    'parent': 'parent',
    'child': 'child',
    'sibling': 'sibling',
    'family': 'associate',
    'friend': 'associate',
    'son': 'child',
    'daughter': 'child',
    'father': 'parent',
    'mother': 'parent',
    'brother': 'sibling',
    'sister': 'sibling',
}

def map_platform(p):
    if not p:
        return None
    key = p.strip().lower()
    if key in VALID_PLATFORMS:
        return key
    return PLATFORM_MAP.get(key)

def map_family(rel):
    """Extract base family relation from strings like 'spouse (妻子 / супруга)'."""
    if not rel:
        return 'other'
    # Try exact match first
    r_lower = rel.strip().lower()
    if r_lower in VALID_FAMILY:
        return r_lower
    # Try parsing the leading word before any parenthesis
    base = re.split(r'[\s(]', rel.strip(), 1)[0].lower()
    if base in VALID_FAMILY:
        return base
    if base in FAMILY_MAP:
        return FAMILY_MAP[base]
    # Try Chinese
    for zh, en in [('配偶','spouse'),('妻子','spouse'),('丈夫','spouse'),('父亲','father'),('母亲','mother'),
                   ('儿子','son'),('女儿','daughter'),('兄弟','brother'),('姐妹','sister'),
                   ('祖父','grandfather'),('祖母','grandmother'),('外祖父','grandfather'),('外祖母','grandmother'),
                   ('子女','other')]:
        if zh in rel:
            return en
    # Try Russian
    for ru, en in [('супруга','spouse'),('супруг','spouse'),('отец','father'),('мать','mother'),
                   ('сын','son'),('дочь','daughter'),('брат','brother'),('сестра','sister'),
                   ('дед','grandfather'),('бабушка','grandmother'),('дядя','uncle'),('тетя','aunt')]:
        if ru in rel:
            return en
    return 'other'

def map_person_rt(rt):
    """Map arbitrary relationship_type to valid enum."""
    if not rt:
        return 'other'
    r_lower = rt.strip().lower()
    if r_lower in VALID_PERSON_RT:
        return r_lower
    base = re.split(r'[\s(]', rt.strip(), 1)[0].lower()
    if base in VALID_PERSON_RT:
        return base
    if base in PERSON_RT_MAP:
        return PERSON_RT_MAP[base]
    # Try keywords
    for keyword, mapping in [('former','associate'),('political','political_ally'),('ally','political_ally'),('rival','political_rival'),('oppos','political_rival'),('deputy','colleague'),('minister','colleague'),('chairman','colleague'),('ceo','colleague'),('founder','associate'),('member','colleague'),('head','associate'),('spouse','spouse'),('wife','spouse'),('husband','spouse'),('father','parent'),('mother','parent'),('son','child'),('daughter','child'),('brother','sibling'),('sister','sibling')]:
        if keyword in r_lower:
            return mapping
    return 'other'

def normalize_family_member(item):
    """Ensure family member is a dict with name and relationship."""
    if isinstance(item, str):
        # Bare string - probably a name, but no relationship
        if not item.strip():
            return None
        return {'name': item.strip(), 'relationship': 'other'}
    if not isinstance(item, dict):
        return None
    # If name is placeholder, skip
    name = item.get('name', '')
    if isinstance(name, str) and ('未公开' in name or 'placeholder' in name.lower() or name.startswith('(') or name.startswith('（')):
        return None
    # Map relationship
    rel = item.get('relationship', item.get('relation', 'other'))
    new_rel = map_family(rel)
    new_item = dict(item)
    new_item['relationship'] = new_rel
    return new_item

def normalize_political_stance(item):
    if not isinstance(item, dict):
        return None
    # If stance_content missing, try other field names
    new = dict(item)
    if not new.get('stance_content'):
        for k in ('stance','content','summary','description','statement','position','view','text'):
            if new.get(k):
                new['stance_content'] = new[k]
                break
    if not new.get('stance_content'):
        # Combine all string fields
        parts = []
        for k, v in list(new.items()):
            if isinstance(v, str) and v.strip() and k not in ('topic','source','date'):
                parts.append(v)
        if parts:
            new['stance_content'] = ' | '.join(parts)
        else:
            return None
    if not new.get('topic'):
        # Try to derive
        for k in ('topic','subject','issue','theme','category'):
            if new.get(k):
                new['topic'] = new[k]
                break
        if not new.get('topic'):
            new['topic'] = 'other'
    return new

def normalize_achievement(item):
    if isinstance(item, str):
        if not item.strip():
            return None
        return {'achievement': item.strip()}
    if not isinstance(item, dict):
        return None
    new = dict(item)
    if not new.get('achievement'):
        for k in ('title','name','summary','description','text','detail','details','honor','award','event'):
            if new.get(k):
                new['achievement'] = new[k]
                break
    if not new.get('achievement'):
        # Combine all string values
        parts = []
        for k, v in list(new.items()):
            if isinstance(v, str) and v.strip() and k not in ('date','year','source','url'):
                parts.append(v)
        if not parts:
            return None
        new['achievement'] = ' | '.join(parts)
    return new

def normalize_nationality(v):
    if not v:
        return 'KG'
    s = str(v).strip()
    # ISO2: 2 letters uppercase
    if re.fullmatch(r'[A-Z]{2}', s):
        return s
    if re.fullmatch(r'[a-z]{2}', s):
        return s.upper()
    # Map common
    if 'kyrgyz' in s.lower() or 'кыргыз' in s.lower() or '吉尔吉斯' in s:
        return 'KG'
    if 'russian' in s.lower() or 'russia' in s.lower() or 'российск' in s.lower() or '俄罗斯' in s:
        return 'RU'
    if 'kazakh' in s.lower() or 'kazakhstan' in s.lower() or 'казах' in s.lower() or '哈萨克' in s:
        return 'KZ'
    if 'uzbek' in s.lower() or 'uzbekistan' in s.lower() or 'узбек' in s.lower() or '乌兹别' in s:
        return 'UZ'
    # Default to KG for KG persons
    return 'KG'

def normalize_work_exp_role(item):
    """Ensure work_experience has the right keys."""
    if isinstance(item, str):
        return {'role': item}
    if not isinstance(item, dict):
        return None
    return item

# Process all person files
files = sorted(glob.glob('output/kg/2026-06-21/persons/KG-PERSON-*.json'))
fixed_count = 0
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    pid = os.path.basename(f).replace('.json', '')
    changed = False

    # nationality
    nat = d.get('nationality')
    if nat and (not isinstance(nat, str) or len(nat) != 2 or not nat.isalpha()):
        d['nationality'] = normalize_nationality(nat)
        changed = True
    elif not nat:
        d['nationality'] = 'KG'
        changed = True

    # social_accounts.platform
    new_sa = []
    for sa in d.get('social_accounts', []) or []:
        if isinstance(sa, str):
            # Skip bare strings, can't infer platform
            continue
        if not isinstance(sa, dict):
            continue
        p = sa.get('platform')
        if not p or p not in VALID_PLATFORMS:
            new_p = map_platform(p)
            if not new_p:
                # Try inferring from URL
                url = (sa.get('url') or '').lower()
                if 'facebook.com' in url: new_p = 'facebook'
                elif 'instagram.com' in url: new_p = 'instagram'
                elif 't.me' in url or 'telegram' in url: new_p = 'telegram'
                elif 'twitter.com' in url or 'x.com' in url: new_p = 'twitter_x'
                elif 'youtube.com' in url or 'youtu.be' in url: new_p = 'youtube'
                elif 'linkedin.com' in url: new_p = 'linkedin'
                elif 'tiktok.com' in url: new_p = 'tiktok'
                elif 'vk.com' in url: new_p = 'other'
                else:
                    new_p = 'other'
            sa = dict(sa)
            sa['platform'] = new_p
        new_sa.append(sa)
    if new_sa != d.get('social_accounts', []):
        d['social_accounts'] = new_sa
        changed = True

    # person_relationships.relationship_type
    new_pr = []
    for pr in d.get('person_relationships', []) or []:
        if not isinstance(pr, dict):
            continue
        rt = pr.get('relationship_type')
        if rt and rt not in VALID_PERSON_RT:
            pr = dict(pr)
            pr['relationship_type'] = map_person_rt(rt)
        elif not rt:
            pr = dict(pr)
            pr['relationship_type'] = 'other'
        # person_name field
        if not pr.get('person_name'):
            for k in ('name','related_person','target','counterpart','related_person_name'):
                if pr.get(k):
                    pr = dict(pr)
                    pr['person_name'] = pr[k]
                    break
        new_pr.append(pr)
    if new_pr != d.get('person_relationships', []):
        d['person_relationships'] = new_pr
        changed = True

    # family_members
    new_fm = []
    for fm in d.get('family_members', []) or []:
        normalized = normalize_family_member(fm)
        if normalized:
            new_fm.append(normalized)
    if new_fm != d.get('family_members', []):
        d['family_members'] = new_fm
        changed = True

    # political_stances
    new_ps = []
    for ps in d.get('political_stances', []) or []:
        normalized = normalize_political_stance(ps)
        if normalized:
            new_ps.append(normalized)
    if new_ps != d.get('political_stances', []):
        d['political_stances'] = new_ps
        changed = True

    # major_achievements
    new_ma = []
    for ma in d.get('major_achievements', []) or []:
        normalized = normalize_achievement(ma)
        if normalized:
            new_ma.append(normalized)
    if new_ma != d.get('major_achievements', []):
        d['major_achievements'] = new_ma
        changed = True

    # work_experience normalization
    new_we = []
    for we in d.get('work_experience', []) or []:
        normalized = normalize_work_exp_role(we)
        if normalized:
            new_we.append(normalized)
    if new_we != d.get('work_experience', []):
        d['work_experience'] = new_we
        changed = True

    if changed:
        tmp = f + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as out:
            json.dump(d, out, ensure_ascii=False, indent=2)
        os.replace(tmp, f)
        fixed_count += 1
print(f'Fixed {fixed_count} person files')

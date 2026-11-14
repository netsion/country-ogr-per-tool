# P3 数据质量检查 + P4 人物统计（组织类型 × 重要等级）
import json, glob, re
from collections import Counter, defaultdict

BASE = 'output/ng/2026-11-10'

def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

# ============ Part 1: P3 数据质量检查 ============
SOCIAL_ENUM = {'twitter': 3, 'facebook': 6, 'instagram': 8, 'youtube': 9, 'odnoklassniki': 10,
               'vkontakte': 11, 'weibo': 14, 'reddit': 15, 'tumblr': 16, 'linkedin': 17,
               'telegram': 19, 'whatsapp': 20, 'line': 21, 'wechat': 23, 'threads': 24,
               'snapchat': 25, 'tiktok': 29}
issues = defaultdict(list)
profiles = []
for fp in sorted(glob.glob(f'{BASE}/orgs/NG-*.json')):
    o = load(fp)
    if 'basic_info' not in o:
        continue  # _index.json 排除（glob NG-* 已滤）
    oid = o['org_id']
    cm = o.get('collection_meta', {})
    if cm.get('phase') != 'phase3_enriched':
        continue
    profiles.append(o)
    # 1. quotes
    q = cm.get('quotes') or []
    if len(q) < 2:
        issues['quotes<2'].append(oid)
    if q and not all(isinstance(x, dict) and x.get('url') for x in q):
        issues['quotes_format'].append(oid)
    # 2. recent_events 日期与来源
    for i, ev in enumerate(o.get('recent_events', [])):
        if not ev.get('date') or not re.match(r'^\d{4}-\d{2}-\d{2}$', str(ev.get('date'))):
            issues['re_date_missing'].append(f'{oid}[{i}]')
        if not ev.get('source'):
            issues['re_source_missing'].append(f'{oid}[{i}]')
    # 3. social v2
    for i, sa in enumerate(o.get('social_accounts', [])):
        p = sa.get('platform')
        if p == 'twitter_x':
            issues['sa_twitter_x'].append(f'{oid}[{i}]')
        elif p not in SOCIAL_ENUM:
            issues['sa_platform_illegal'].append(f'{oid}[{i}]={p}')
        elif sa.get('source') not in (SOCIAL_ENUM[p], None):
            issues['sa_source_code'].append(f'{oid}[{i}]')
        extra = set(sa.keys()) - {'platform', 'account_name', 'url', 'source', 'source_note', 'nickname', 'username', 'user_id'}
        if extra:
            issues['sa_extra_keys'].append(f'{oid}[{i}]={extra}')
    # 4. key_people 命名格式
    for i, kp in enumerate(o.get('key_people', [])):
        nm = kp.get('name', '')
        if nm and '(' not in nm and '（' not in nm:
            issues['kp_name_no_paren'].append(f'{oid}[{i}]={nm}')
        if 'source' in kp:
            issues['kp_extra_source'].append(oid)
    # 5. core_business 长度
    cb = o.get('core_business') or ''
    if len(cb) < 200:
        issues['core_business_short'].append(f'{oid}({len(cb)})')
    # 6. apec_stance
    ap = o.get('apec_stance') or ''
    if not ap:
        issues['apec_missing'].append(oid)
    elif '不是APEC成员' not in ap and '非APEC成员' not in ap:
        issues['apec_no_disclaimer'].append(oid)

print('=== Part 1: P3 数据质量检查（145 个 phase3 画像）===')
print(f'检查画像数: {len(profiles)}')
for k in sorted(issues):
    v = issues[k]
    print(f'  {k}: {len(v)}' + (f'  e.g. {v[:6]}' if len(v) <= 8 else f'  e.g. {v[:6]}...'))
if not issues:
    print('  全部通过 ✓')

# ============ Part 2: P4 人物统计 ============
# 2.1 收集 (person, org) 出现
reg = load(f'{BASE}/id_registry.json')
preg = reg.get('person_registry', [])
id2p = {p['person_id']: p for p in preg}
name2pid = {}
for p in preg:
    nm = p.get('name', '')
    m = re.search(r'\(([^)]+)\)\s*$', nm)
    key = (m.group(1) if m else nm).casefold().strip()
    name2pid[key] = p['person_id']

persons = {}  # pid_or_newkey -> record
order = []
for o in sorted(profiles, key=lambda x: x['org_id']):
    oid = o['org_id']
    otype = o['basic_info'].get('org_type')
    for kp in o.get('key_people', []):
        nm = kp.get('name', '')
        pid = kp.get('person_id')
        if not pid:
            m = re.search(r'\(([^)]+)\)\s*$', nm)
            key = 'new:' + ((m.group(1) if m else nm).casefold().strip())
            # 已注册但未回填 id 的，映射到 registry person
            pid = name2pid.get(key.replace('new:', '', 1) if key.startswith('new:') else key, None) or \
                  name2pid.get((m.group(1) if m else nm).casefold().strip(), None)
            if pid:
                k = pid
            else:
                k = key
        else:
            k = pid
        if k not in persons:
            persons[k] = {'name': nm, 'orgs': [], 'titles': []}
            order.append(k)
        persons[k]['orgs'].append(oid)
        persons[k]['titles'].append((otype, kp.get('title', ''), oid))

# 2.2 重要等级判定（按规则优先级）
def importance(person):
    for otype, title, oid in person['titles']:
        t = title or ''
        if re.search(r'总统|副总统|州长|首席大法官', t):
            return 'high'
        if re.search(r'参谋长', t):
            return 'high'
        if otype == 'PARTY' and re.search(r'全国主席', t):
            return 'high'
    for otype, title, oid in person['titles']:
        t = title or ''
        # 独立机构/监管机构/安全机构首长 → high
        if otype in ('GOV', 'MIL') and re.search(r'执行主席|督察长|总监察长|总队长|局长|署长|主席|行长|总干事|董事总经理|总经理|执行副总裁|执行副主席', t) \
           and not re.search(r'副|常务', t.split('(')[0]):
            # 排除部委机构（部长按 skill 属 medium）
            return 'high'
    for otype, title, oid in person['titles']:
        t = title or ''
        if re.search(r'部长|首席执行官|CEO|董事总经理|总经理|总裁|GMD|出版人|副校长|总编辑|局长|署长|总监|执行总监|执行董事|院长|董事长|主席|副主任|国务部长|创始人', t):
            return 'medium'
    return 'low'

for k, p in persons.items():
    p['imp'] = importance(p)
    # 主组织类型：registry source_orgs 首选，否则首次出现
    if k in id2p and id2p[k].get('source_orgs'):
        p['primary_org'] = id2p[k]['source_orgs'][0]
    else:
        p['primary_org'] = p['orgs'][0]
    p['primary_type'] = re.match(r'NG-([A-Z]+)-', p['primary_org']).group(1)

print('\n=== Part 2: P4 人物统计 ===')
print(f'去重后人物总数: {len(persons)}（含 registry 已注册 {len(preg)} 人）')
imp_c = Counter(p['imp'] for p in persons.values())
print(f'按重要等级: high={imp_c["high"]} medium={imp_c["medium"]} low={imp_c["low"]}')

mat = defaultdict(Counter)
for p in persons.values():
    mat[p['primary_type']][p['imp']] += 1
TYPES = ['GOV', 'SOE', 'FIN', 'CORP', 'ACAD', 'MEDIA', 'MIL', 'PARTY', 'NGO', 'INTL']
print('\n组织类型 × 重要等级（按主组织归类）:')
print(f'{"类型":<7}{"high":>6}{"medium":>8}{"low":>6}{"合计":>7}')
for t in TYPES:
    r = mat.get(t, Counter())
    print(f'{t:<7}{r.get("high",0):>6}{r.get("medium",0):>8}{r.get("low",0):>6}{sum(r.values()):>7}')
r = Counter()
for t in TYPES:
    for i in ('high', 'medium', 'low'):
        r[i] += mat.get(t, Counter()).get(i, 0)
print(f'{"合计":<7}{r["high"]:>6}{r["medium"]:>8}{r["low"]:>6}{sum(r.values()):>7}')

# 保存统计明细
out = {
    'generated': '2026-11-14',
    'total_persons': len(persons),
    'importance': dict(imp_c),
    'matrix': {t: dict(mat.get(t, Counter())) for t in TYPES},
    'persons': [{'key': k, 'name': p['name'], 'imp': p['imp'], 'primary_org': p['primary_org'],
                 'org_count': len(set(p['orgs']))} for k, p in persons.items()],
}
with open('scripts_tmp/p4_person_stats.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print('\n明细已存: scripts_tmp/p4_person_stats.json')

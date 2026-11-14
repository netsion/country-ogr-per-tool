# P4 人物裁剪方案生成器 v2（目标 ~200 人，OSINT 视角）
# 保留优先级：政治领袖高官 > 活跃的政党/政治/军事人物 > 关键经济机构首长 > 媒体/NGO/学术首长
import json, glob, re
from collections import Counter, defaultdict

BASE = 'output/ng/2026-11-10'

def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

reg = load(f'{BASE}/id_registry.json')
preg = reg.get('person_registry', [])
name2pid = {}
for p in preg:
    nm = p.get('name', '')
    m = re.search(r'\(([^)]+)\)\s*$', nm)
    key = (m.group(1) if m else nm).casefold().strip()
    name2pid[key] = p['person_id']

profiles = []
for fp in sorted(glob.glob(f'{BASE}/orgs/NG-*.json')):
    o = load(fp)
    if o.get('collection_meta', {}).get('phase') == 'phase3_enriched':
        profiles.append(o)

persons = {}
for o in profiles:
    oid = o['org_id']
    otype = o['basic_info'].get('org_type')
    for kp in o.get('key_people', []):
        nm = kp.get('name', '')
        pid = kp.get('person_id')
        if not pid:
            m = re.search(r'\(([^)]+)\)\s*$', nm)
            en = (m.group(1) if m else nm).casefold().strip()
            pid = name2pid.get(en)
            k = pid if pid else 'new:' + en
        else:
            k = pid
        if k not in persons:
            persons[k] = {'name': nm, 'apps': []}
        persons[k]['apps'].append({'org': oid, 'type': otype, 'title': kp.get('title', '')})

TUNABLE = {'acad_vc_scope': 'top5', 'media_per_outlet': 1, 'bank_chairmen': False}
WHITELIST_ACAD_VC = {'NG-ACAD-001', 'NG-ACAD-002', 'NG-ACAD-003', 'NG-ACAD-004', 'NG-ACAD-005'}
TOP_CORP_CHAIR = {'NG-CORP-001', 'NG-CORP-007', 'NG-CORP-006'}  # Dangote/BUA/Glo

def is_former(t):
    return bool(re.search(r'前|former', t))

def judge(k, p):
    for a in p['apps']:
        t = a['title'] or ''
        ot = a['type']; oid = a['org']
        former = is_former(t)
        dep = bool(re.search(r'Deputy|分管|代理', t))
        if re.search(r'总统|副总统|首席大法官|州长', t) and not former:
            return True, 'A-国家最高层', '总统/副总统/州长/首席大法官'
        if re.search(r'幕僚长|国家安全顾问', t) and oid == 'NG-GOV-002' and not former:
            return True, 'A-总统府核心', '总统幕僚长/国家安全顾问'
        if re.search(r'部长', t) and not former and not re.search(r'副部长', t):
            return True, 'B-现任部长', '内阁部长'
        if re.search(r'国务部长', t) and not former:
            return True, 'B-现任部长', '国务部长'
        if ot == 'MIL' and re.search(r'参谋长|督察长|总监察长|总队长|局长|总干事', t) and not former:
            return True, 'C-军情安全首长', '军种参谋长/情报与安全部队现任首长'
        if ot == 'GOV' and re.search(r'执行主席|主席|行长|董事总经理|总经理|执行副主席|关长|署长|局长|总干事|注册官|执行秘书', t) \
                and not former and not re.search(r'Deputy', t):
            return True, 'D-联邦机构首长', '监管/选举/执法/开发机构现任首长'
        if ot in ('SOE', 'FIN', 'CORP') and re.search(r'首席执行官|CEO|集团总经理|董事总经理|总裁|GMD|(?<!联合)创始人', t) \
                and not former and not re.search(r'Deputy', t):
            return True, 'E-经济体首长', '国企/银行/龙头企业现任CEO'
        if ot in ('FIN', 'CORP') and re.search(r'董事长', t) and not former and oid in TOP_CORP_CHAIR:
            return True, 'E-创始人级董事长', '创始人/控股股东董事长（Dangote/BUA/Glo）'
        if ot == 'PARTY' and re.search(r'全国主席|全国领袖|州长|候选人', t) and not former:
            return True, 'F-政党核心', '现任党魁/州长/总统候选人'
        if ot == 'MEDIA' and re.search(r'局长|总编辑|主编|出版人|董事总经理|总经理|首席执行官|创始人', t) and not former:
            return True, 'G-媒体首长', '媒体机构现任首长'
        if ot == 'NGO' and re.search(r'执行主任|执行总监|执行董事|首席执行官|全球总监|创始人|主任', t) and not former:
            return True, 'H-NGO首长', 'NGO 现任创始人/执行负责人'
        if ot == 'ACAD' and re.search(r'副校长', t) and not former and not dep:
            if TUNABLE['acad_vc_scope'] == 'all' or oid in WHITELIST_ACAD_VC:
                return True, 'I-大学副校长', '研究型大学现任副校长'
        if ot == 'INTL' and re.search(r'(?<!副)主席|(?<!副)院长|(?<!副)议长|(?<!副)总干事|(?<!副)主任', t) and not former:
            return True, 'J-国际组织首长', '驻尼国际组织现任首长'
    return False, 'cut', ''

kept, cut = {}, {}
for k, p in persons.items():
    keep, rule, reason = judge(k, p)
    if keep:
        kept[k] = {'name': p['name'], 'rule': rule, 'reason': reason, 'apps': p['apps']}
    else:
        cut[k] = {'name': p['name'], 'reason_type': reason, 'apps': p['apps']}

# MEDIA 每 outlet 限额
per = defaultdict(list)
for k, v in kept.items():
    if v['rule'] == 'G-媒体首长':
        for a in v['apps']:
            if a['type'] == 'MEDIA':
                per[a['org']].append(k)
for org, ks in per.items():
    uniq = list(dict.fromkeys(ks))
    for k in uniq[TUNABLE['media_per_outlet']:]:
        if k not in kept:
            continue  # 已在其他 outlet 循环中裁掉
        v = kept.pop(k)
        cut[k] = {'name': v['name'], 'reason_type': 'G-媒体超额', 'apps': v['apps']}

# NGO 每 org 限额 1
per_ngo = defaultdict(list)
for k, v in kept.items():
    if v['rule'] == 'H-NGO首长':
        for a in v['apps']:
            if a['type'] == 'NGO':
                per_ngo[a['org']].append(k)
for org, ks in per_ngo.items():
    uniq = list(dict.fromkeys(ks))
    for k in uniq[1:]:
        v = kept.pop(k)
        cut[k] = {'name': v['name'], 'reason_type': 'H-NGO超额', 'apps': v['apps']}

print(f'=== 裁剪方案 v2（TUNABLE={TUNABLE}）===')
print(f'总人物: {len(persons)} | 保留: {len(kept)} | 裁剪: {len(cut)}')
rk = Counter(v['rule'] for v in kept.values())
print('\n保留按规则:')
for r, c in rk.most_common():
    print(f'  {r}: {c}')
rc = Counter(v['reason_type'].split(':')[0] for v in cut.values())
print('\n裁剪按理由:')
for r, c in rc.most_common():
    print(f'  {r}: {c}')

json.dump({'tunable': TUNABLE, 'total': len(persons), 'kept_count': len(kept), 'cut_count': len(cut),
           'kept': {k: {'name': v['name'], 'rule': v['rule'], 'reason': v['reason'],
                        'orgs': sorted({a['org'] for a in v['apps']})} for k, v in kept.items()},
           'cut': {k: {'name': v['name'], 'reason_type': v['reason_type']} for k, v in cut.items()}},
          open('scripts_tmp/p4_trim_proposal.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('\n明细已存: scripts_tmp/p4_trim_proposal.json')

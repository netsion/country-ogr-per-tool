# -*- coding: utf-8 -*-
"""P4 人物清单重评：按 skill §14.1 标准用中/英/法语职位关键词 + 组织类型上下文重评 importance_level
输出：等级×来源组织类型 矩阵 + 更新 person_list.json（含 relevel_notes）
"""
import json
import os
import re
import sys, io
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r"D:\ai-workspace\apec-osint-tool\output\tg\2026-11-16"

# ── 1. 读取 org key_people（含 org_type 上下文）──
org_kp = defaultdict(list)  # org_id -> [(person_name, title, org_type)]
for p in __import__('glob').glob(os.path.join(BASE, 'orgs', '*.json')):
    d = json.load(open(p, encoding='utf-8'))
    ot = d['basic_info'].get('org_type')
    ph = (d.get('collection_meta') or {}).get('phase')
    if ph != 'phase3_enriched':
        continue
    for kp in d.get('key_people') or []:
        org_kp[d['org_id']].append((kp.get('name', ''), kp.get('title') or '', ot))

# ── 2. 评级规则（按 skill §14.1）──
HIGH_KW = [
    # 最高领导人/政府首脑
    '总统', '部长会议主席', '总理', 'president of the republic', 'prime minister',
    'head of state', 'head of government', 'chef de l', 'président du conseil',
    # 立法/司法最高
    '议长', '国民议会议长', '参议院议长', 'president of the national assembly',
    '最高法院长', '宪法法院长', 'president of the supreme court', 'president of the constitutional court',
    'totalité', 'président de la cour',
    # 军情最高
    '总参谋长', 'chef d etat-major', "chef d'état-major", 'chief of staff',
    '总局长', '宪兵总局长', '情报局局长', 'directeur général de l anr',
    # 央行
    'gouverneur', 'governor of the central bank', '行长 brv',
    # 党魁（各党主席/全国主席/执行书记以 party org_type 判定）
]
HIGH_ORG_TITLE = {  # 组织类型+职位组合升级为 high
    ('PARTY', '主席'), ('PARTY', '全国主席'), ('PARTY', '执行书记'), ('PARTY', '党魁'),
    ('PARTY', 'president'), ('PARTY', 'secrétaire'),
}
MED_KW = [
    '部长', '部长级', 'minister', 'ministre', '副总统', 'vice president', 'vice-président',
    '副校长', '副总', '副议长', '副秘书长', '副秘书', '秘书长', 'secrétaire général',
    'secretary general', 'deputy', 'vice', '.directeur', 'directeur général', 'directrice',
    'général', 'general director', 'managing director', 'ceo', 'chief executive',
    '台长', '社长', '总编辑', '主编', '院长', '校长', 'recteur', 'rector', 'président',
    '总司库', '司库', '总检察长', 'procureur', '庭长', '法官', 'judge', '总监',
    '指挥官', 'commandant', 'commander', '司令', '上校', 'colonel', '准将', 'général de brigade',
    '董事', 'chairman', 'chair', 'président du conseil', '监管', '专员', '协调员',
    'coordinator', 'coordonnateur', '执行主任', 'executive director', '发言人', 'spokesman',
]
HIST_KW = ['前', 'former', 'ex-', 'ancien', '已卸任', '历史', '创始人']  # 仅标记，不降级

def classify(title, org_type):
    t = (title or '').lower()
    if not t:
        return 'low'
    # high 语义（跨语言）
    for kw in HIGH_KW:
        if kw.lower() in t:
            return 'high'
    if (org_type, title.strip()) in HIGH_ORG_TITLE:
        return 'high'
    if org_type == 'PARTY' and any(k in title.lower() for k in ['主席', 'president', 'secrétaire général', 'secretary', '书记']):
        return 'high'
    # medium 语义
    for kw in MED_KW:
        if kw.lower() in t:
            return 'medium'
    return 'low'

# ── 3. 读取 person_list 并重评 ──
pl = json.load(open(os.path.join(BASE, 'person_list.json'), encoding='utf-8'))
persons = pl['persons'] if isinstance(pl, dict) and 'persons' in pl else pl

matrix = defaultdict(lambda: defaultdict(int))  # org_type -> level -> count
updated = 0
for p in persons:
    # 找该人物的来源组织上下文
    src_orgs = p.get('source_orgs') or []
    levels = []
    matched_orgs = []
    for so in src_orgs:
        oid = so.get('org_id') if isinstance(so, dict) else None
        if not oid or oid not in org_kp:
            continue
        matched_orgs.append((oid, org_kp[oid][0][2] if org_kp[oid] else None))
        for (nm, title, ot) in org_kp[oid]:
            # 粗略匹配：人名在 org_kp 名单中
            if nm and p.get('name_zh') and (nm.split(' (')[0] == p['name_zh'] or nm == p.get('name')):
                levels.append(classify(title, ot))
                break
    if not levels:
        # 回退：用清单里的 importance_reason（title 样本）按 GOV 语境评
        reason = p.get('importance_reason') or ''
        levels = [classify(reason.replace('; ', ' ').split(';')[0], 'OTHER')]
    lv = max(levels, key=['low', 'medium', 'high'].index) if levels else 'low'
    old = p.get('importance_level')
    if lv != old:
        p['importance_level_prev'] = old
        p['relevel_note'] = 'releveled by tg_p4_relevel.py (skill §14.1, bilingual keywords + org context)'
        updated += 1
    p['importance_level'] = lv
    for (oid, ot) in matched_orgs:
        matrix[ot or 'UNK'][lv] += 1

# 汇总
lv_count = defaultdict(int)
for p in persons:
    lv_count[p['importance_level']] += 1

# ── 4. 输出 ──
print(f'共 {len(persons)} 人，重评 {updated} 人')
print('等级分布:', dict(lv_count))
print()
print('=== 来源组织类型 × 重要等级 矩阵 ===')
print(f"{'类型':<8}{'high':>6}{'medium':>8}{'low':>6}{'合计':>6}")
tot = defaultdict(int)
for t in sorted(matrix):
    h, m, l = matrix[t].get('high', 0), matrix[t].get('medium', 0), matrix[t].get('low', 0)
    tot['high'] += h; tot['medium'] += m; tot['low'] += l
    print(f'{t:<8}{h:>6}{m:>8}{l:>6}{h+m+l:>6}')
print(f"{'合计':<8}{tot['high']:>6}{tot['medium']:>8}{tot['low']:>6}{sum(tot.values()):>6}")

# 高/中人物明细（P4 首批候选）
print()
print('=== HIGH 人物明细 ===')
for p in persons:
    if p['importance_level'] == 'high':
        srcs = ','.join((s.get('org_id') if isinstance(s, dict) else str(s)) for s in (p.get('source_orgs') or [])[:3])
        print(f"  {p['person_id']} | {p.get('name_zh') or p.get('name_en') or p.get('name')} | {p.get('importance_reason') or ''[:40]} | {srcs}")

# 备份并保存
bak = os.path.join(BASE, '_tmp', 'person_list.pre_relevel.json')
if not os.path.exists(bak):
    json.dump(pl, open(bak, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(pl, open(os.path.join(BASE, 'person_list.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print()
print('saved: person_list.json (backup: _tmp/person_list.pre_relevel.json)')

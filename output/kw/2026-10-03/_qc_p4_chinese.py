# -*- coding: utf-8 -*-
"""KW P4 中文规范 + 机械合规质检（按 person_collection_rules.md）"""
import json, glob, os, re

BASE = 'output/kw/2026-10-03'
AR = re.compile(r'[\u0600-\u06FF]')
ZH = re.compile(r'[\u4e00-\u9FFF]')

PLATFORMS = {'twitter_x','facebook','instagram','youtube','linkedin','telegram','tiktok','threads','mastodon','wechat','weibo','github','gitlab','medium','substack','other'}
REL_TYPES = {'spouse','parent','child','sibling','mentor','mentee','colleague','superior','subordinate','political_ally','political_rival','associate','other'}
FAM_REL = {'spouse','father','mother','son','daughter','brother','sister','grandfather','grandmother','uncle','aunt','cousin','other'}
DEGREES = {'primary','high_school','associate','bachelor','master','doctorate','professional','other',None}
CONTACT_TYPES = {'email','phone','fax','website','other'}
DATE_RE = re.compile(r'^\d{4}(-\d{2})?(-\d{2})?$')

issues = {}
def add(cat, pid, detail=''):
    issues.setdefault(cat, []).append((pid, detail))

def check_zh_text(pid, field, val):
    """中文字段不得含 ASCII 双引号（应使用「」）"""
    if isinstance(val, str) and '"' in val and ZH.search(val):
        add('ascii_quote_in_zh', pid, field)

for fp in sorted(glob.glob(f'{BASE}/persons/*.json')):
    pid = os.path.basename(fp).replace('.json', '')
    d = json.load(open(fp, encoding='utf-8'))
    # 1. name 本国官方语言（阿语）
    name = d.get('name') or ''
    if not AR.search(name):
        add('name_no_arabic', pid, name[:40])
    if ZH.search(name) and name.startswith(tuple('0123456789')) is False and ZH.match(name):
        add('name_starts_zh', pid, name[:40])
    # 2. name_zh 纯中文
    nz = d.get('name_zh') or ''
    if AR.search(nz):
        add('name_zh_has_arabic', pid, nz[:40])
    if not ZH.search(nz):
        add('name_zh_no_chinese', pid, nz[:40])
    # 3. current_positions 纯中文
    for cp in d.get('current_positions') or []:
        if isinstance(cp, str) and not ZH.search(cp):
            add('current_position_not_zh', pid, cp[:40])
    # 4. work_experience.organization 中文(阿语)
    for w in d.get('work_experience') or []:
        org = w.get('organization') or ''
        if not ZH.search(org):
            add('org_no_chinese', pid, org[:40])
        for f in ('start_date','end_date'):
            v = w.get(f)
            if v and not DATE_RE.match(str(v)):
                add('bad_date_format', pid, f'{f}={v}')
    # 5. education.institution 中文(阿语)
    for e in d.get('education') or []:
        inst = e.get('institution') or ''
        if inst and not ZH.search(inst):
            add('inst_no_chinese', pid, inst[:40])
        deg = e.get('degree')
        if deg not in DEGREES:
            add('bad_degree', pid, str(deg))
        for f in ('start_date','end_date'):
            v = e.get(f)
            if v and not DATE_RE.match(str(v)):
                add('bad_date_format', pid, f'{f}={v}')
    # 6. 关系/家人 person_name 中文(阿语)
    for r in d.get('person_relationships') or []:
        pn = r.get('person_name') or ''
        if pn and not ZH.search(pn):
            add('rel_name_no_chinese', pid, pn[:40])
        rt = r.get('relationship_type')
        if rt not in REL_TYPES:
            add('bad_rel_type', pid, str(rt))
    for f in d.get('family_members') or []:
        fn = f.get('name') or ''
        if fn and not ZH.search(fn):
            add('fam_name_no_chinese', pid, fn[:40])
        if f.get('relationship') not in FAM_REL:
            add('bad_fam_rel', pid, str(f.get('relationship')))
    # 7. 社媒枚举
    for s in d.get('social_accounts') or []:
        if s.get('platform') not in PLATFORMS:
            add('bad_platform', pid, str(s.get('platform')))
    # 8. contacts 枚举
    for c in d.get('contacts') or []:
        if c.get('type') not in CONTACT_TYPES:
            add('bad_contact_type', pid, str(c.get('type')))
    # 9. nationality
    if d.get('nationality') != 'KW':
        add('bad_nationality', pid, str(d.get('nationality')))
    # 10. 中文文本 ASCII 引号
    check_zh_text(pid, 'biography_summary', d.get('biography_summary'))
    cm = d.get('collection_meta') or {}
    check_zh_text(pid, 'notes', cm.get('notes'))

print('=== 中文规范/机械合规问题统计 ===')
total = 0
for cat, lst in sorted(issues.items(), key=lambda x: -len(x[1])):
    print(f'{cat}: {len(lst)}')
    for pid, det in lst[:4]:
        print(f'    {pid} | {det}')
    if len(lst) > 4: print(f'    ... (+{len(lst)-4})')
    total += len(lst)
print('TOTAL issues:', total)

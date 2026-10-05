# -*- coding: utf-8 -*-
"""P4 收尾修复：name_local 顶层字段 + work_experience 额外字段 + 自创 org_id 置 null"""
import json, os, re, glob

BASE = 'output/kw/2026-10-03'
reg = json.load(open(f'{BASE}/id_registry.json', encoding='utf-8'))
valid_orgs = {r['org_id'] for r in reg['registry']}
valid_persons = {r['person_id'] for r in reg.get('person_registry', [])}

# 数组允许字段（strict 白名单）
ALLOWED = {
    'work_experience': {'start_date', 'end_date', 'organization', 'org_id', 'position'},
    'education': {'institution', 'degree', 'field', 'start_date', 'end_date'},
    'political_stances': {'date', 'topic', 'stance_content', 'source'},
    'person_relationships': {'person_id', 'person_name', 'relationship_type', 'description'},
    'major_achievements': {'date', 'achievement', 'organization'},
    'social_accounts': {'platform', 'account_name', 'url', 'source'},
    'family_members': {'person_id', 'name', 'relationship', 'industry_or_organization'},
    'contacts': {'type', 'value', 'source'},
}
ORG_ID_RE = re.compile(r'^KW-[A-Z]+-\d{3}$')
ORGID_FIELDS = ('org_id', 'person_id')

stats = {'name_local': 0, 'extra_fields': 0, 'bad_orgid': 0, 'bad_personid': 0}
files = sorted(glob.glob(f'{BASE}/persons/*.json'))
for fp in files:
    d = json.load(open(fp, encoding='utf-8'))
    changed = False
    # 1. name_local 顶层字段 → 并入 aliases
    if 'name_local' in d:
        nl = d.pop('name_local')
        aliases = d.setdefault('aliases', [])
        if nl and nl not in aliases:
            aliases.append(nl)
        stats['name_local'] += 1
        changed = True
    # 2. 各数组额外字段删除 + org_id/person_id 校验
    for key, allowed in ALLOWED.items():
        for item in d.get(key) or []:
            if not isinstance(item, dict):
                continue
            for fld in list(item.keys()):
                if fld not in allowed:
                    item.pop(fld)
                    stats['extra_fields'] += 1
                    changed = True
            for fld in ORGID_FIELDS:
                v = item.get(fld)
                if v and isinstance(v, str):
                    if fld == 'org_id' and not ORG_ID_RE.match(v):
                        item[fld] = None
                        stats['bad_orgid'] += 1
                        changed = True
                    elif fld == 'person_id' and v not in valid_persons:
                        item[fld] = None
                        stats['bad_personid'] += 1
                        changed = True
    if changed:
        json.dump(d, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print(json.dumps(stats, ensure_ascii=False))
print('files scanned:', len(files))

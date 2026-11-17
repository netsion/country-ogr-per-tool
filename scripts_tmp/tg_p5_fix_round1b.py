# -*- coding: utf-8 -*-
"""P5-2 修复轮 1b（纠正过度剥离）：
从备份恢复 persons/，改用校验器白名单（WORK_FIELDS/REL_FIELDS）重做剥离，
并重做名称归一 + 合并改指（orgs 侧已修复，无需回滚）。
"""
import json, os, sys, io, glob, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.abspath('.agents/skills/country-org-collector/scripts'))
from validate_schema import _names_overlap, WORK_FIELDS, REL_FIELDS

BASE = os.path.abspath('output/tg/2026-11-16')
BK = os.path.join(BASE, '_tmp', 'p5_backup')

def wj(path, obj):
    tmp = path + '.p5tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)

def load(p):
    return json.load(open(p, encoding='utf-8'))

# ── 1. 恢复 persons/（TG-*.json 覆盖式还原）──
persons_dir = os.path.join(BASE, 'persons')
n_restore = 0
for f in glob.glob(os.path.join(BK, 'persons', 'TG-*.json')):
    shutil.copy2(f, persons_dir)
    n_restore += 1
print('persons/ 已从备份覆盖还原:', n_restore, '个文件')

# ── 2. canonical 映射 ──
org_canon, person_canon = {}, {}
for fp in glob.glob(os.path.join(BASE, 'orgs', 'TG-*.json')):
    d = load(fp)
    bi = d.get('basic_info') or {}
    zh, orig, en = bi.get('name_zh'), bi.get('name_original'), bi.get('name_en')
    org_canon[d['org_id']] = (f'{zh} ({orig or en})' if zh and (orig or en) and zh not in (orig or en)
                              else (zh or orig or en))
for fp in glob.glob(os.path.join(BASE, 'persons', 'TG-*.json')):
    d = load(fp)
    zh, en = d.get('name_zh'), d.get('name')
    person_canon[d['person_id']] = (f'{zh} ({en})' if zh and en and zh not in en else (zh or en or ''))

MERGES = {'TG-PERSON-000517': 'TG-PERSON-000379',
          'TG-PERSON-000489': 'TG-PERSON-000181',
          'TG-PERSON-000382': 'TG-PERSON-000190',
          'TG-PERSON-000068': 'TG-PERSON-000293',
          'TG-PERSON-000551': 'TG-PERSON-000539',
          'TG-PERSON-000342': 'TG-PERSON-000335'}

def fix_ref(cur, canon):
    if cur and canon and not _names_overlap(cur, canon):
        return canon
    return cur

stats = {'org_ref': 0, 'rel': 0, 'repoint': 0, 'strip': 0}
for fp in glob.glob(os.path.join(persons_dir, 'TG-*.json')):
    d = load(fp)
    dirty = False
    notes = d.setdefault('collection_meta', {}).setdefault('notes', '')
    for i, we in enumerate(d.get('work_experience') or []):
        oid = we.get('org_id')
        if oid and oid in org_canon:
            new = fix_ref(we.get('organization'), org_canon[oid])
            if new != we.get('organization'):
                we['organization'] = new; stats['org_ref'] += 1; dirty = True
        extra = set(we) - WORK_FIELDS
        if extra:
            for k in sorted(extra):
                notes = (notes + ' | ' if notes else '') + f'work_experience[{i}].{k} 原值「{we[k]}」已按校验器白名单剥离'
                del we[k]
            stats['strip'] += len(extra); dirty = True
    for i, rel in enumerate(d.get('person_relationships') or []):
        pid = rel.get('person_id')
        if pid and pid in MERGES:
            rel['person_id'] = MERGES[pid]; pid = MERGES[pid]
            stats['repoint'] += 1; dirty = True
        if pid and pid in person_canon:
            new = fix_ref(rel.get('person_name'), person_canon[pid])
            if new != rel.get('person_name'):
                rel['person_name'] = new; stats['rel'] += 1; dirty = True
        extra = set(rel) - REL_FIELDS
        if extra:
            for k in sorted(extra):
                notes = (notes + ' | ' if notes else '') + f'person_relationships[{i}].{k} 原值「{rel[k]}」已按校验器白名单剥离'
                del rel[k]
            stats['strip'] += len(extra); dirty = True
    if dirty:
        d['collection_meta']['notes'] = notes
        wj(fp, d)
print('纠正后修复:', stats)

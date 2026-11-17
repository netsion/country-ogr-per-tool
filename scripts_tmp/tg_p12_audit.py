# -*- coding: utf-8 -*-
"""TG P1/P2 数据一致性审计（只读，不修改任何数据）
检查项：ID 格式 / 骨架↔目标一致性 / registry 一致性 / 重复检测 / 缓存完整性 / 字段规范
"""
import json
import os
import re
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r"D:\ai-workspace\apec-osint-tool\output\tg\2026-11-16"
issues = []  # (level, code, detail)

def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

targets = load(os.path.join(BASE, "_target_orgs.json"))["organizations"]
registry = load(os.path.join(BASE, "id_registry.json"))
name_index = load(os.path.join(BASE, "_name_index.json"))

ID_RE = re.compile(r"^TG-(GOV|SOE|CORP|NGO|ACAD|MEDIA|FIN|INTL|PARTY|MIL)-\d{3}$")
PERSON_RE = re.compile(r"^TG-PERSON-\d{6}$")

# 1) 目标文件
t_ids = []
t_names = {}
t_qids = {}
for o in targets:
    oid = o.get("id", "")
    t_ids.append(oid)
    if not ID_RE.match(oid):
        issues.append(("ERROR", "ID_FORMAT", f"{oid}"))
    nm = o.get("name", "")
    key = re.sub(r"[^a-z0-9]", "", nm.lower())
    if key in t_names:
        issues.append(("WARN", "DUP_NAME_TARGET", f"{t_names[key]} <-> {oid} ({nm})"))
    t_names[key] = oid
    q = o.get("wikidata_qid")
    if q:
        if q in t_qids:
            issues.append(("ERROR", "DUP_QID_TARGET", f"{q}: {t_qids[q]} <-> {oid}"))
        t_qids[q] = oid

# 2) 骨架文件
org_dir = os.path.join(BASE, "orgs")
files = sorted(f for f in os.listdir(org_dir) if f.endswith(".json"))
s_by_id = {}
for fn in files:
    p = os.path.join(org_dir, fn)
    try:
        d = load(p)
    except Exception as e:
        issues.append(("ERROR", "JSON_INVALID", f"orgs/{fn}: {e}"))
        continue
    oid = d.get("org_id", "")
    s_by_id[oid] = d
    if fn != f"{oid}.json":
        issues.append(("ERROR", "FILE_ID_MISMATCH", f"orgs/{fn} -> org_id={oid}"))
    bi = d.get("basic_info") or {}
    # 骨架 ↔ 目标一致性
    t = next((x for x in targets if x["id"] == oid), None)
    if not t:
        issues.append(("ERROR", "SKELETON_NO_TARGET", oid))
        continue
    if (bi.get("name_en") or bi.get("name_original")) and t.get("name") and \
       bi.get("name_en", "").lower() not in (t["name"].lower(),) and \
       not any(a.lower() == bi.get("name_en", "").lower() for a in (t.get("aliases") or [])):
        issues.append(("WARN", "NAME_DIVERGE", f"{oid}: target='{t['name']}' skeleton='{bi.get('name_en')}'"))
    # 日期格式
    for fld in ("founded_date",):
        v = bi.get(fld)
        if v and not re.match(r"^\d{4}(-\d{2}(-\d{2})?)?$", str(v)):
            issues.append(("ERROR", "DATE_FORMAT", f"{oid}.{fld}={v}"))
    # key_people person_id 格式
    for kp in d.get("key_people") or []:
        pid = kp.get("person_id")
        if pid and not PERSON_RE.match(pid):
            issues.append(("ERROR", "PERSON_ID_FORMAT", f"{oid}: {pid}"))

# 3) 双向覆盖
missing_skel = [i for i in t_ids if i not in s_by_id]
extra_skel = [i for i in s_by_id if i not in t_ids]
if missing_skel:
    issues.append(("ERROR", "NO_SKELETON", ",".join(missing_skel)))
if extra_skel:
    issues.append(("ERROR", "SKELETON_EXTRA", ",".join(extra_skel)))

# 4) registry
reg_entries = registry.get("registry", [])
reg_ids = [r.get("org_id") for r in reg_entries]
if len(reg_ids) != len(set(reg_ids)):
    dup = {x for x in reg_ids if reg_ids.count(x) > 1}
    issues.append(("ERROR", "REG_DUP", ",".join(sorted(dup))))
reg_missing = [i for i in t_ids if i not in set(reg_ids)]
if reg_missing:
    issues.append(("ERROR", "REG_MISSING", ",".join(reg_missing)))
p_entries = registry.get("person_registry", [])
p_ids = [r.get("person_id") for r in p_entries]
if len(p_ids) != len(set(p_ids)):
    issues.append(("ERROR", "PERSON_REG_DUP", ""))
for pid in p_ids:
    if not PERSON_RE.match(pid or ""):
        issues.append(("ERROR", "PERSON_ID_FORMAT_REG", pid))
for r in p_entries:
    nm = r.get("name", "")
    key = re.sub(r"[^a-z0-9]", "", nm.lower())
    if key in t_names:
        pass  # 人名与组织名同名不算问题，仅组织间查重
p_names = {}
for r in p_entries:
    key = re.sub(r"[^a-z0-9]", "", (r.get("name") or "").lower())
    if key and key in p_names:
        issues.append(("WARN", "PERSON_DUP_NAME", f"{p_names[key]} <-> {r.get('person_id')} ({r.get('name')})"))
    p_names[key] = r.get("person_id")
# 骨架 key_people 引用的 person_id 必须在 registry
reg_p = set(p_ids)
for oid, d in s_by_id.items():
    for kp in d.get("key_people") or []:
        pid = kp.get("person_id")
        if pid and pid not in reg_p:
            issues.append(("ERROR", "PERSON_NOT_IN_REG", f"{oid}: {pid}"))

# 5) 缓存完整性
cache_dir = os.path.join(BASE, "_cache")
cache_files = [f for f in os.listdir(cache_dir) if f.endswith(".json")]
cached_qids = set()
for fn in cache_files:
    q = fn[:-5]
    cached_qids.add(q)
    try:
        load(os.path.join(cache_dir, fn))
    except Exception as e:
        issues.append(("ERROR", "CACHE_INVALID", f"{fn}: {e}"))
with_qid = {o["id"]: o["wikidata_qid"] for o in targets if o.get("wikidata_qid")}
no_cache = {oid: q for oid, q in with_qid.items() if q not in cached_qids}
if no_cache:
    issues.append(("ERROR", "QID_NO_CACHE", ",".join(f"{k}={v}" for k, v in no_cache.items())))

# 6) 名称索引
ni = name_index if isinstance(name_index, dict) else {}
if not ni:
    issues.append(("ERROR", "NAME_INDEX_EMPTY", ""))

# 汇总
errs = [i for i in issues if i[0] == "ERROR"]
warns = [i for i in issues if i[0] == "WARN"]
print(f"targets={len(targets)} skeletons={len(s_by_id)} registry={len(reg_ids)} persons={len(p_ids)} cache={len(cache_files)}")
print(f"ERRORS: {len(errs)}")
for lv, code, det in errs:
    print(f"  [{code}] {det}")
print(f"WARNINGS: {len(warns)}")
for lv, code, det in warns:
    print(f"  [{code}] {det}")

# -*- coding: utf-8 -*-
"""Refined language audit: strip parenthetical original text before Chinese-ratio."""
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
BASE = "output/ci/2026-10-06"
PERSONS = os.path.join(BASE, "persons")

def strip_parens(s):
    return re.sub(r"[（(][^()（）]*[)）]", "", s or "")

def cn_ratio(s):
    s = s or ""
    if not s.strip():
        return 0.0
    return len(re.findall(r"[\u4e00-\u9fff]", s)) / max(len(s.strip()), 1)

def core_cn(s):
    """Chinese ratio of string after removing parenthetical original text."""
    return cn_ratio(strip_parens(s))

files = sorted(f for f in os.listdir(PERSONS) if f.endswith(".json") and f != "_index.json")
C = Counter()
det = {k: [] for k in
       ["name_has_cn", "name_zh_bad", "bio_bad", "org_no_cn", "pos_no_cn",
        "currpos_no_cn", "inst_no_cn", "field_no_cn", "relname_no_cn",
        "famname_no_cn", "achv_no_cn", "topic_no_cn", "ascii_quote"]}

for fn in files:
    with open(os.path.join(PERSONS, fn), encoding="utf-8") as f:
        d = json.load(f)
    pid = d.get("person_id", fn[:-5])

    if d.get("name") and cn_ratio(d["name"]) > 0.3:
        C["name_has_cn"] += 1; det["name_has_cn"].append(pid)

    nz = (d.get("name_zh") or "").strip()
    if not nz:
        C["name_zh_empty"] += 1; det["name_zh_bad"].append(pid + "(empty)")
    elif core_cn(nz) < 0.4:
        C["name_zh_not_cn"] += 1; det["name_zh_bad"].append(pid + ":" + nz[:18])

    bio = (d.get("biography_summary") or "").strip()
    if len(bio) < 100 or core_cn(bio) < 0.4:
        C["bio_bad"] += 1; det["bio_bad"].append(pid + ("(len=%d)" % len(bio)))

    for i, w in enumerate(d.get("work_experience", []) or []):
        if (w.get("organization") or "") and core_cn(w.get("organization")) < 0.2:
            C["org_no_cn"] += 1; det["org_no_cn"].append(f"{pid}[{i}]" + (w.get("organization") or "")[:24])
        if (w.get("position") or "") and core_cn(w.get("position")) < 0.2:
            C["pos_no_cn"] += 1; det["pos_no_cn"].append(f"{pid}[{i}]" + (w.get("position") or "")[:24])

    for i, cp in enumerate(d.get("current_positions", []) or []):
        if isinstance(cp, str) and cp.strip() and core_cn(cp) < 0.2:
            C["currpos_no_cn"] += 1; det["currpos_no_cn"].append(f"{pid}[{i}]" + cp[:24])

    for i, e in enumerate(d.get("education", []) or []):
        if (e.get("institution") or "") and core_cn(e.get("institution")) < 0.2:
            C["inst_no_cn"] += 1; det["inst_no_cn"].append(f"{pid}[{i}]" + (e.get("institution") or "")[:24])
        if (e.get("field") or "") and core_cn(e.get("field")) < 0.2:
            C["field_no_cn"] += 1; det["field_no_cn"].append(f"{pid}[{i}]" + (e.get("field") or "")[:24])

    for r in d.get("person_relationships", []) or []:
        if (r.get("person_name") or "") and core_cn(r.get("person_name")) < 0.2:
            C["relname_no_cn"] += 1; det["relname_no_cn"].append(pid + (r.get("person_name") or "")[:24])
    for r in d.get("family_members", []) or []:
        if (r.get("name") or "") and core_cn(r.get("name")) < 0.2:
            C["famname_no_cn"] += 1; det["famname_no_cn"].append(pid + (r.get("name") or "")[:24])

    for a in d.get("major_achievements", []) or []:
        if (a.get("achievement") or "") and core_cn(a.get("achievement")) < 0.2:
            C["achv_no_cn"] += 1; det["achv_no_cn"].append(pid + (a.get("achievement") or "")[:24])
    for s in d.get("political_stances", []) or []:
        if (s.get("topic") or "") and core_cn(s.get("topic")) < 0.2:
            C["topic_no_cn"] += 1; det["topic_no_cn"].append(pid + (s.get("topic") or "")[:24])

    raw = json.dumps(d, ensure_ascii=False)
    for m in re.findall(r': ?"([^"]*[\u4e00-\u9fff][^"]*)"', raw):
        if '"' in m:
            C["ascii_quote"] += 1; det["ascii_quote"].append(pid); break

total_files = len(files)
print("REFINED LANGUAGE AUDIT — %d files" % total_files)
print("(parenthetical original text stripped before ratio; compliant 中文(原文) not flagged)")
for k in ["name_has_cn", "name_zh_empty", "name_zh_not_cn", "bio_bad", "org_no_cn", "pos_no_cn",
          "currpos_no_cn", "inst_no_cn", "field_no_cn", "relname_no_cn", "famname_no_cn",
          "achv_no_cn", "topic_no_cn", "ascii_quote"]:
    v = C.get(k, 0)
    print(f"  {k}: {v}")
print()
for k, items in det.items():
    if items:
        print(k, "->", items[:6])

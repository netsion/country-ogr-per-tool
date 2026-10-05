# -*- coding: utf-8 -*-
"""P3 output audit: field-level quality + binding rates + cross-consistency."""
import json
import glob
import os
import re
from collections import Counter, defaultdict

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
orgs = {}
for f in glob.glob(os.path.join(BASE, "orgs", "KW-*.json")):
    d = json.load(open(f, encoding="utf-8"))
    orgs[d["org_id"]] = d

issues = defaultdict(list)
AR_RE = re.compile(r"[\u0600-\u06FF]")

for oid, d in sorted(orgs.items()):
    bi, cm = d.get("basic_info", {}), d.get("collection_meta", {})
    kp, dept = d.get("key_people") or [], d.get("departments") or []
    ev, rel = d.get("recent_events") or [], d.get("related_entities") or []
    soc = d.get("social_accounts") or []

    # 铁律：事件来源与日期
    for e in ev:
        if not e.get("source"):
            issues["event_no_source"].append(f"{oid}:{e.get('date')}")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(e.get("date") or "")):
            issues["event_bad_date"].append(f"{oid}:{e.get('date')}")
        if not e.get("title") or not e.get("description"):
            issues["event_thin"].append(f"{oid}:{e.get('date')}")
    # quotes 规范
    q = cm.get("quotes") or []
    if not isinstance(q, list) or len(q) < 3 or not all(isinstance(x, dict) and x.get("url") for x in q):
        issues["quotes_bad"].append(oid)
    if cm.get("phase") != "phase3_enriched":
        issues["phase_wrong"].append(oid)
    # 关键描述字段
    if not d.get("core_business") or len(d["core_business"]) < 100:
        issues["core_business_short"].append(f"{oid}:{len(d.get('core_business') or '')}")
    if not bi.get("name_original"):
        issues["name_original_missing"].append(oid)
    if not bi.get("name_zh"):
        issues["name_zh_missing"].append(oid)
    if not bi.get("website"):
        issues["website_missing"].append(oid)
    fd = bi.get("founded_date")
    if fd and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(fd)):
        issues["founded_bad"].append(f"{oid}:{fd}")
    if d.get("apec_stance") is None:
        issues["apec_null"].append(oid)
    # 人名语言格式：应为 中文(阿拉伯语) 或纯中文——统计纯拉丁名
    for k in kp:
        n = k.get("name") or ""
        if re.match(r"^[A-Za-z .'\-]+$", n):
            issues["kp_latin_name"].append(f"{oid}:{n[:30]}")
        if not k.get("title"):
            issues["kp_no_title"].append(oid)
    # social platform 枚举粗查
    for s in soc:
        if s.get("platform") not in ("twitter_x","facebook","instagram","youtube","linkedin","tiktok","website","other","threads","whatsapp","snapchat"):
            issues["platform_odd"].append(f"{oid}:{s.get('platform')}")

# 跨文件一致性：同一人名多个 person_id / 同一 person_id 多个名字
pid2names, name2pids = defaultdict(set), defaultdict(set)
for oid, d in orgs.items():
    for k in d.get("key_people") or []:
        pid, n = k.get("person_id"), (k.get("name") or "").strip()
        if pid:
            pid2names[pid].add(n)
        if n:
            name2pids[n].add(pid)
for pid, names in pid2names.items():
    if len(names) > 1:
        issues["pid_multi_name"].append(f"{pid}: {sorted(names)[:3]}")
for n, pids in name2pids.items():
    real = {x for x in pids if x}
    if len(real) > 1:
        issues["name_multi_pid"].append(f"{n[:30]}: {sorted(real)}")

# trimmed 组织是否仍被引用
reg = json.load(open(os.path.join(BASE, "id_registry.json"), encoding="utf-8"))
trimmed = {r["org_id"] for r in reg["registry"] if r["status"] == "trimmed"}
for oid, d in orgs.items():
    for r in d.get("related_entities") or []:
        if r.get("org_id") in trimmed:
            issues["ref_to_trimmed"].append(f"{oid}->{r['org_id']}")

print(f"audited {len(orgs)} orgs")
if issues:
    for k, v in sorted(issues.items(), key=lambda x: -len(x[1])):
        print(f"  {k}: {len(v)} | sample: {v[:4]}")
else:
    print("no issues")

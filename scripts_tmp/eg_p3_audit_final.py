# -*- coding: utf-8 -*-
"""EG P3 comprehensive data audit (in-scope orgs only)."""
import json, glob, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from collections import Counter

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
reg = json.load(open(f"{BASE}/id_registry.json", encoding="utf-8"))
excluded = {e["org_id"] for e in reg["registry"] if "excluded" in (e.get("status") or "")}
AR = re.compile(r"[\u0600-\u06ff]")
APEC_OK = "不是APEC成员"

issues = Counter()
detail = {"no_source_ev": [], "apec_bad": [], "quotes_short": [], "biz_short": [],
          "kp_no_ar": 0, "kp_total": 0, "pid_null": 0, "zh_empty": [], "bad_dept": [],
          "bad_soc": [], "stance_null": []}
n_scope, ev_total, orgs_kp0 = 0, 0, []
soc_ok = soc_bad = quotes_ok = 0

for f in sorted(glob.glob(f"{BASE}/orgs/*.json")):
    if f.endswith("_index.json"):
        continue
    d = json.load(open(f, encoding="utf-8"))
    oid = d["org_id"]
    meta = d.get("collection_meta", {})
    ph = meta.get("phase") or ""
    if oid in excluded or "out_of_scope" in ph or "excluded" in ph:
        continue
    if not ph.startswith("phase3"):
        issues["not_enriched"] += 1
        continue
    n_scope += 1
    bi = d["basic_info"]
    # name_zh
    if not bi.get("name_zh"):
        detail["zh_empty"].append(oid)
    # key_people
    kps = d.get("key_people") or []
    if not kps:
        orgs_kp0.append(oid)
    for kp in kps:
        detail["kp_total"] += 1
        nm = kp.get("name") or ""
        if "(" in nm and AR.search(nm.split("(")[-1]):
            pass
        else:
            detail["kp_no_ar"] += 1
        if not kp.get("person_id"):
            detail["pid_null"] += 1
    # events
    evs = d.get("recent_events") or []
    ev_total += len(evs)
    for ev in evs:
        if not ev.get("source"):
            detail["no_source_ev"].append(f"{oid}: {ev.get('title','')[:30]}")
    # apec
    stance = d.get("apec_stance") or ""
    if not stance:
        detail["stance_null"].append(oid)
    elif APEC_OK not in stance:
        detail["apec_bad"].append(oid)
    # quotes
    q = meta.get("quotes") or []
    if not isinstance(q, list) or len(q) < 3 or any(not isinstance(x, dict) for x in q):
        detail["quotes_short"].append(oid)
    else:
        quotes_ok += 1
    # core_business
    biz = d.get("core_business") or ""
    if len(biz) < 200:
        detail["biz_short"].append(f"{oid}({len(biz)})")
    # departments dept_id
    for dp in d.get("departments") or []:
        did = dp.get("dept_id") or ""
        if not re.fullmatch(r"EG-[A-Z]+-\d{3}-DEPT-\d{3}", did):
            detail["bad_dept"].append(f"{oid}:{did}")
    # social source int
    for a in d.get("social_accounts") or []:
        s = a.get("source")
        if s is None or isinstance(s, int):
            soc_ok += 1
        else:
            soc_bad += 1
            detail["bad_soc"].append(oid)

print("=" * 62)
print(f"EG P3 数据质量审计（范围 {n_scope} 个已丰富组织）")
print("=" * 62)
print(f"1. key_people 总数: {detail['kp_total']}，person_id 空: {detail['pid_null']}（P4 补建档案后回填，预期态）")
print(f"2. key_people 命名 中文(阿语) 合规: {detail['kp_total']-detail['kp_no_ar']}/{detail['kp_total']}，不合规: {detail['kp_no_ar']}")
print(f"3. recent_events 总数: {ev_total}，缺 source: {len(detail['no_source_ev'])}")
for x in detail["no_source_ev"]:
    print(f"   !! {x}")
print(f"4. apec_stance: 空 {len(detail['stance_null'])}，含固定表述但缺失标准句 {len(detail['apec_bad'])}")
for x in detail["apec_bad"]:
    print(f"   !! 缺标准句: {x}")
print(f"5. quotes ≥3 对象数组: {quotes_ok}/{n_scope}，不达标: {len(detail['quotes_short'])}")
for x in detail["quotes_short"]:
    print(f"   !! {x}")
print(f"6. core_business ≥200字: 不达标 {len(detail['biz_short'])}")
for x in detail["biz_short"]:
    print(f"   !! {x}")
print(f"7. name_zh 空: {len(detail['zh_empty'])} {detail['zh_empty']}")
print(f"8. dept_id 格式违规: {len(detail['bad_dept'])}")
for x in detail["bad_dept"][:8]:
    print(f"   !! {x}")
print(f"9. social source 整数码: 合规 {soc_ok}，违规 {soc_bad}")
for x in detail["bad_soc"][:8]:
    print(f"   !! {x}")
print(f"10. 无 key_people 的已丰富组织: {len(orgs_kp0)} {orgs_kp0}")

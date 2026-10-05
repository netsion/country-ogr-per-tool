# -*- coding: utf-8 -*-
"""Extract unique P4 person worklist + stats by org_type x importance."""
import json
import glob
import os
import re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
TYPE_ORDER = ["GOV", "SOE", "FIN", "CORP", "ACAD", "MEDIA", "NGO", "PARTY", "MIL", "INTL"]

persons = {}  # key -> record
def upsert(key, rec):
    if key not in persons:
        persons[key] = rec
    else:
        # 保留类型优先级更高的归属，title 取更"高"的（简单策略：先到先得，类型序已排好）
        old = persons[key]
        if TYPE_ORDER.index(rec["org_type"]) < TYPE_ORDER.index(old["org_type"]):
            persons[key] = rec

for f in sorted(glob.glob(os.path.join(BASE, "orgs", "KW-*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    oid, bi = d["org_id"], d["basic_info"]
    otype = bi["org_type"]
    for k in d.get("key_people") or []:
        name = (k.get("name") or "").strip()
        if not name:
            continue
        pid = k.get("person_id") or None
        key = pid or ("name:" + name)
        upsert(key, {
            "person_id": pid, "name": name, "title": k.get("title"),
            "title_description": k.get("title_description"),
            "org_id": oid, "org_type": otype,
            "org_name": bi.get("name_en"),
        })

# 注册表中存在但未出现在任何 key_people 的人物（departments head 等来源）
reg = json.load(open(os.path.join(BASE, "id_registry.json"), encoding="utf-8"))
covered_pids = {p["person_id"] for p in persons.values() if p["person_id"]}
for p in reg.get("person_registry", []):
    if p["person_id"] not in covered_pids and p.get("status") in ("listed", "profiled"):
        upsert(p["person_id"], {
            "person_id": p["person_id"], "name": p.get("name"), "title": None,
            "title_description": None, "org_id": None, "org_type": "UNKNOWN",
            "org_name": None,
        })

# 重要等级分类（skill §14.1）
LOW_MARK = re.compile(r"^前|前会长|前主席|前大臣|前部长|前秘书长|前任|历史领导人|创始人(?!兼)|已故|卸任")
DEP_MARK = re.compile(r"副|次大臣|次官|deputy|Deputy|Vice|vice")
HIGH_MARK = re.compile(
    r"埃米尔|王储|首相|议长|大臣|部长|行长|总司令|总参谋长|董事长|董事会主席|董事会成员长|主席|"
    r"总干事|董事总经理|总裁|会长|校长|台长|局长|司令|院长|总监|CEO|Chief Executive|"
    r"Managing Director|Managing editor|主编|总编辑|Leader|领袖|秘书长"
)

stats = {}
rows = []
for key, p in persons.items():
    t = p.get("title") or ""
    if LOW_MARK.search(t):
        level = "low"
    elif DEP_MARK.search(t):
        level = "medium"
    elif HIGH_MARK.search(t):
        level = "high"
    else:
        level = "low"
    p["importance"] = level
    rows.append(p)
    stats.setdefault(p["org_type"], {}).setdefault(level, 0)
    stats[p["org_type"]][level] += 1

out = os.path.join(BASE, "_p4_person_list.json")
json.dump({"generated": "2026-10-05", "total": len(rows), "persons": rows},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print(f"unique persons: {len(rows)}")
order = ["GOV", "SOE", "FIN", "CORP", "ACAD", "MEDIA", "NGO", "PARTY", "MIL", "INTL", "UNKNOWN"]
print(f"{'type':8} {'high':>5} {'medium':>7} {'low':>5} {'total':>6}")
th = tm = tl = 0
for t in order:
    s = stats.get(t)
    if not s:
        continue
    h, m, l = s.get("high", 0), s.get("medium", 0), s.get("low", 0)
    th += h; tm += m; tl += l
    print(f"{t:8} {h:>5} {m:>7} {l:>5} {h+m+l:>6}")
print(f"{'TOTAL':8} {th:>5} {tm:>7} {tl:>5} {th+tm+tl:>6}")
print("saved:", out)

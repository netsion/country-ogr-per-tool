# -*- coding: utf-8 -*-
"""EG P4 people stats: refined importance classification (in-scope only) + cross-tab by org type."""
import json, glob, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from collections import Counter, defaultdict

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
reg = json.load(open(f"{BASE}/id_registry.json", encoding="utf-8"))
preg = {e["person_id"]: e for e in reg.get("person_registry", [])}
plist = json.load(open(f"{BASE}/person_list.json", encoding="utf-8"))["persons"]
plist_map = {p["person_id"]: p for p in plist}

# ---- collect key_people from in-scope enriched orgs ----
org_cat, org_name = {}, {}
persons = defaultdict(lambda: {"titles": [], "orgs": [], "cats": set(), "names": set()})
n_orgs = 0
for f in glob.glob(f"{BASE}/orgs/*.json"):
    if f.endswith("_index.json"):
        continue
    d = json.load(open(f, encoding="utf-8"))
    oid = d["org_id"]
    meta = d.get("collection_meta", {})
    if "excluded" in (meta.get("phase") or "") or "out_of_scope" in (meta.get("phase") or ""):
        continue
    n_orgs += 1
    bi = d["basic_info"]
    cat = bi.get("org_type", "?")
    org_cat[oid] = cat
    org_name[oid] = bi.get("name_en") or bi.get("name_zh")
    for kp in d.get("key_people", []) or []:
        pid = kp.get("person_id")
        nm = kp.get("name") or ""
        if pid:
            persons[pid]["titles"].append((kp.get("title") or "", oid, cat))
            persons[pid]["orgs"].append(oid)
            persons[pid]["cats"].add(cat)
            persons[pid]["names"].add(nm.split(" (")[0])

# ---- refined importance classifier ----
HIGH_KW = ["总统", "总理", "议长", "总参谋长", "总司令", "总导师", "最高统帅", "首席大法官",
           "央行行长", "中央银行行长", "国王", "王储", "埃米尔", "亲王", "党主席", "总书记"]
MED_KW = ["部长", "副议长", "副主席", "副校长", "副总统", "副总理", "总经理", "执行总裁",
          "首席执行官", "董事总经理", "董事长", "主席", "秘书长", "社长", "总编辑", "主编",
          "署长", "局长", "行长", "司令", "参谋长", "总监", "所长", "主任", "总裁",
          "理事", "代表", "执行主任", "执行董事", "COO", "CFO", "CEO"]
# org-head context: first/only key person of these orgs is high regardless of title quirks
ORG_HEAD_HIGH = {"EG-GOV-001", "EG-GOV-002", "EG-GOV-003", "EG-GOV-004", "EG-MIL-001",
                 "EG-MIL-005", "EG-FIN-001", "EG-INTL-001", "EG-PARTY-001", "EG-PARTY-013",
                 "EG-GOV-051", "EG-SOE-018", "EG-FIN-014"}

def classify(pid, titles):
    joined = " | ".join(t[0] for t in titles)
    # former/historical state heads stay high
    if re.search(r"(前|末任|已故)?总统", joined) or "总理" in joined:
        return "high"
    for kw in HIGH_KW:
        if kw in joined:
            return "high"
    # org-head boost
    for _, oid, _ in titles:
        if oid in ORG_HEAD_HIGH and len(persons[pid]["orgs"]) >= 1:
            # only if this org is among their affiliations and title is a leadership one
            t_for_org = [t for t, o, _ in titles if o == oid]
            if t_for_org and any(k in t_for_org[0] for k in ["主席", "长", "总", "秘书长", "统帅", "主", "总裁"]):
                return "high"
    for kw in MED_KW:
        if kw in joined:
            return "medium"
    return "low"

levels = {}
for pid, info in persons.items():
    lv = classify(pid, info["titles"])
    levels[pid] = lv
    if pid in plist_map:
        plist_map[pid]["importance_level"] = lv
        plist_map[pid]["importance_reason"] = " | ".join(t[0] for t in info["titles"])[:200]
        plist_map[pid]["in_p4_scope"] = True

# registry persons not referenced by any in-scope org → out of P4 scope
orphans = [p["person_id"] for p in plist if p["person_id"] not in persons]
for pid in orphans:
    if pid in plist_map:
        plist_map[pid]["in_p4_scope"] = False

# save refined person_list
out = []
for p in plist:
    p["importance_level"] = plist_map[p["person_id"]]["importance_level"]
    p["importance_reason"] = plist_map[p["person_id"]].get("importance_reason", p.get("importance_reason", ""))
    p["in_p4_scope"] = plist_map[p["person_id"]].get("in_p4_scope", False)
    out.append(p)
_orig = json.load(open(f"{BASE}/person_list.json", encoding="utf-8")); _orig["persons"] = out; json.dump(_orig, open(f"{BASE}/person_list.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- statistics ----
lv_count = Counter(levels.values())
cross = Counter()  # (org_cat, level) per person-title pair
for pid, info in persons.items():
    lv = levels[pid]
    for _, oid, cat in info["titles"]:
        cross[(cat, lv)] += 1

high_list = sorted([p for p, lv in levels.items() if lv == "high"])
print("=" * 60)
print(f"P4 范围: {n_orgs} 个在册组织引用的独立人物 = {len(persons)}")
print(f"注册未引用(范围外): {len(orphans)}")
print(f"精分级: high={lv_count.get('high',0)} medium={lv_count.get('medium',0)} low={lv_count.get('low',0)}")
print()
print("HIGH 名单:")
for pid in high_list:
    nm = sorted(persons[pid]["names"])[0]
    cats = ",".join(sorted(persons[pid]["cats"]))
    t0 = persons[pid]["titles"][0][0][:30]
    print(f"  {pid} | {nm} | [{cats}] | {t0}")
print()
print("org_type × level 矩阵 (人-职对):")
cats_all = sorted({c for c, _ in cross})
print(f"{'类型':<6}{'high':>6}{'medium':>7}{'low':>6}")
for c in cats_all:
    print(f"{c:<6}{cross.get((c,'high'),0):>6}{cross.get((c,'medium'),0):>7}{cross.get((c,'low'),0):>6}")

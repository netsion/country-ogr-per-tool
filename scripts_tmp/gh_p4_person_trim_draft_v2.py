# -*- coding: utf-8 -*-
"""P4 人物 OSINT 裁剪草案 v2：在 A+B（已确认163裁）基础上再压至 ~205。
硬保：GOV 全部 high/medium、MIL 全部、PARTY 全部、KUP 6。
其余类别仅保留掌门人级（战略机构 CEO/MD/DG/总编辑），其余裁剪。"""
import json, re, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pl = json.load(open(r"output/gh/2026-11-17/person_list.json", encoding="utf-8"))
targets = {t["org_id"]: t["category"] for t in json.load(
    open(r"output/gh/2026-11-17/_p3_final_targets.json", encoding="utf-8"))["targets"]}
draft = json.load(open(r"output/gh/2026-11-17/_p4_person_trim_DRAFT.json", encoding="utf-8"))
ab_ids = {e["person_id"] for e in draft["bucket_A_firm_trim"]} | {e["person_id"] for e in draft["bucket_B_borderline_keep"]}

# 已确认 A+B 的裁剪集合之外，还需再裁 ~89 人。
# —— 硬保条件 ——
HEAD_ROLE = re.compile(r"首席执行官|CEO|董事总经理|Managing Director|\bMD\b|总干事|秘书长|执行主任|执行董事|局长\(Commissioner-General\)|所长|总编辑|校长|院长 \(Rector|创办人|创始人|总裁")
# 战略机构掌门人白名单（SOE/CORP/FIN/MEDIA/ACAD/NGO 内保留的 org_id）
STRATEGIC = {
    "GH-SOE-001", "GH-SOE-002", "GH-SOE-003", "GH-SOE-004", "GH-SOE-007", "GH-SOE-013",  # COCOBOD/GNPC/VRA/ECG/GPHA/AT
    "GH-FIN-002",  # GCB（国有大行）
    "GH-CORP-001", "GH-CORP-002", "GH-CORP-003", "GH-CORP-042", "GH-CORP-058",  # AngloGold/MTN/GOIL/Zoomlion/McDan
    "GH-MEDIA-003",  # Graphic（官方 flagship）
    "GH-ACAD-008", "GH-ACAD-009",  # Noguchi（医研/生物线）/CSIR（科研网络）
    "GH-NGO-001", "GH-NGO-003",  # CDD/GII（反腐与治理观察线）
}
# GOV low 中的显式保留（政治领袖/关键高官）
GOV_LOW_KEEP = {"GH-PERSON-000031",  # 议长 Bagbin
                "GH-PERSON-000032",  # 代理首席大法官 Pwamang
                "GH-PERSON-000060",  # 少数党领袖 Afenyo-Markin
                "GH-PERSON-000082",  # EC 主席 Jean Mensa
                "GH-PERSON-000106",  # GRA 局长 Sarpong
                "GH-PERSON-000133"}  # NIA 执行秘书 Deku
KUP_IDS = {e["person_id"] for e in draft["bucket_keep_upgrade"]}

def role_of(p):
    return p.get("importance_reason") or ""

cuts, keeps = defaultdict(list), defaultdict(list)
for p in pl["persons"]:
    pid = p["person_id"]
    lvl = p.get("importance_level") or "low"
    cs = sorted(set(targets.get(s["org_id"], "?") for s in (p.get("source_orgs") or [])))
    src_ids = [s["org_id"] for s in (p.get("source_orgs") or [])]
    row = (pid, lvl, ",".join(cs), (p.get("name_en") or p.get("name") or "?"), role_of(p)[:60],
           "/".join((s.get("org_name") or "?")[:22] for s in (p.get("source_orgs") or [])[:2]))
    if pid in ab_ids:
        continue  # 已在 A+B（确认裁）
    # 硬保判定
    if pid in KUP_IDS:
        keeps["升格保留"].append(row); continue
    if "MIL" in cs or "PARTY" in cs:
        keeps["军事/活跃政党"].append(row); continue
    if "GOV" in cs and (lvl in ("high", "medium") or pid in GOV_LOW_KEEP):
        keeps["政治领袖/政府高官"].append(row); continue
    # 非优先类别：仅战略机构掌门人保留
    strategic_head = any(oid in STRATEGIC and HEAD_ROLE.search(role_of(p)) for oid in src_ids)
    if strategic_head and lvl != "low":
        keeps["战略机构掌门人"].append(row); continue
    if strategic_head and lvl == "low":
        # 战略机构的 low 掌门（如 GPHA 代理港长等）也裁——掌门人须 medium 以上
        cuts["战略机构低级成员"].append((row, "战略机构的低级岗位成员"))
        continue
    # GOV low 未进 GOV_LOW_KEEP 白名单 → 裁
    if "GOV" in cs:
        cuts["GOV非核心"].append((row, "GOV内非白名单人物（退休法官/委员/董事等）"))
        continue
    # 其余全部裁（非优先类别的非掌门人）
    cuts["非优先类别非掌门"].append((row, "非优先类别（%s）且非掌门人级" % ",".join(cs)))

total_keep = sum(len(v) for v in keeps.values())
total_cut = sum(len(v) for v in cuts.values())
print("=== 二轮裁剪草案 v2（在 A+B 确认基础上再裁）===")
print("保留 %d 人：" % total_keep)
for k, v in keeps.items():
    print("  %-14s %d" % (k, len(v)))
print("再裁 %d 人：" % total_cut)
for k, v in cuts.items():
    print("  %-16s %d" % (k, len(v)))
print()
print("--- 再裁名单明细 ---")
for k, v in cuts.items():
    print("== %s (%d) ==" % (k, len(v)))
    for row, why in sorted(v, key=lambda r: r[0][2]):
        print("  %s [%s] %s | %s | %s" % (row[0], row[2], row[3], row[4], why))

out = {
    "version": "P4-person-trim-DRAFT-v2", "date": "2026-11-18",
    "status": "DRAFT v2 - awaiting user confirmation",
    "framework": "硬保: GOV high/medium + MIL全部 + PARTY全部 + KUP6; 其余类别仅战略机构掌门人保留",
    "keep_buckets": {k: [{"person_id": r[0], "name": r[3], "role": r[4]} for r in v] for k, v in keeps.items()},
    "cut_buckets_v2": {k: [{"person_id": r[0][0], "name": r[0][3], "level": r[0][1],
                            "categories": r[0][2], "role": r[0][4], "orgs": r[0][5], "reason": r[1]} for r in v]
                       for k, v in cuts.items()},
    "stats": {"total": 457, "confirmed_ab": len(ab_ids), "v2_cut": total_cut,
              "p4_final_keep": total_keep},
}
json.dump(out, open(r"output/gh/2026-11-17/_p4_person_trim_DRAFT_v2.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("\nDRAFT v2 -> output/gh/2026-11-17/_p4_person_trim_DRAFT_v2.json")

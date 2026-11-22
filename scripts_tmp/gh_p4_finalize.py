# -*- coding: utf-8 -*-
"""固化 P4 人物裁剪 v3：生成 205 人最终目标清单 + P4 进度文件。"""
import json, os, sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"D:\claude-workspace\country-ogr-per-tool\output\gh\2026-11-17"

pl = json.load(open(os.path.join(BASE, "person_list.json"), encoding="utf-8"))["persons"]
targets = {t["org_id"]: t["category"] for t in json.load(
    open(os.path.join(BASE, "_p3_final_targets.json"), encoding="utf-8"))["targets"]}
ab = json.load(open(os.path.join(BASE, "_p4_person_trim_DRAFT.json"), encoding="utf-8"))
v3 = json.load(open(os.path.join(BASE, "_p4_person_trim_DRAFT_v3.json"), encoding="utf-8"))

cut = {e["person_id"] for e in ab["bucket_A_firm_trim"]}
cut |= {e["person_id"] for e in ab["bucket_B_borderline_keep"]}
cut |= {e["person_id"] for e in v3["keep_additions"]} & cut  # 拉回者从裁剪集移除
# 注：v3 裁剪桶已排除全部拉回者，无需再减；keep_additions 与 A/B 的重叠为冗余罗列
for b in v3["cut_buckets_v3"].values():
    cut |= {e["person_id"] for e in b}

CAT_ORDER = ["GOV", "MIL", "PARTY", "SOE", "INTL", "FIN", "CORP", "MEDIA", "ACAD", "NGO"]
LVL_ORDER = {"high": 0, "medium": 1, "low": 2}

def sort_key(p):
    cs = [targets.get(s["org_id"], "ZZZ") for s in (p.get("source_orgs") or [])]
    c = min(cs, key=lambda c: CAT_ORDER.index(c) if c in CAT_ORDER else 99) if cs else "ZZZ"
    return (LVL_ORDER.get(p.get("importance_level") or "low", 2),
            CAT_ORDER.index(c) if c in CAT_ORDER else 99, p["person_id"])

final = sorted([p for p in pl if p["person_id"] not in cut], key=sort_key)
assert len(final) == 205, len(final)

rows = [{
    "person_id": p["person_id"],
    "name_en": p.get("name_en") or p.get("name"),
    "name": p.get("name"),
    "importance_level": p.get("importance_level"),
    "importance_reason": p.get("importance_reason"),
    "source_orgs": [{"org_id": s["org_id"], "org_name": s.get("org_name"),
                     "category": targets.get(s["org_id"], "?")} for s in (p.get("source_orgs") or [])],
} for p in final]

out = {"version": "final_p4_person_targets_v1_osint", "count": len(rows), "targets": rows}
json.dump(out, open(os.path.join(BASE, "_p4_final_person_targets.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

pg = {"phase": "P4_person_enrichment", "started_at": "2026-11-18", "last_updated": "2026-11-18",
      "completed": [], "remaining": [r["person_id"] for r in rows], "current": [], "failed": [],
      "note": "OSINT v3 裁剪后 205 人；恒定4后台并发；顺序 high->medium->low, 类别 GOV优先"}
json.dump(pg, open(os.path.join(BASE, "_phase_progress.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

lv = Counter(r["importance_level"] for r in rows)
cc = Counter(min([targets.get(s["org_id"], "?") for s in r["source_orgs"]] or ["?"],
                 key=lambda c: CAT_ORDER.index(c) if c in CAT_ORDER else 99) for r in rows)
print("P4 最终目标: %d 人" % len(rows))
print("等级:", dict(lv))
print("主类别:", dict(cc))
print("前4个:", [r["person_id"] for r in rows[:4]])

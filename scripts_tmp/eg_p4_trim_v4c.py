# -*- coding: utf-8 -*-
"""Final micro-pass: 213 -> ~206, unify party-chair grading."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from collections import Counter
BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
meta = json.load(open(f"{BASE}/person_list.json", encoding="utf-8"))
plist = meta["persons"]

MICRO_CUT = {
  "EG-PERSON-000394": "U2_共和人民党参议院党团主席（党魁已保留，党团层）",
  "EG-PERSON-000167": "V2_Elsewedy 集团副总裁兼电缆板块CEO（集团CEO已保留）",
  "EG-PERSON-000169": "V2_Elsewedy 集团副总裁",
  "EG-PERSON-000335": "W2_Orman 总干事（董事会主席已保留）",
  "EG-PERSON-000397": "已裁(v4b)",
}
UPGRADE = {"EG-PERSON-000408": "high"}  # 社民党现主席，与其他党主席口径一致

final_ids = {p["person_id"]: p for p in plist if p.get("p4_scope")}
for pid in MICRO_CUT:
    if pid in final_ids:
        final_ids[pid]["p4_scope"] = False
        final_ids[pid]["p4_trim_reason"] = MICRO_CUT[pid]
for pid, lv in UPGRADE.items():
    if pid in final_ids:
        final_ids[pid]["importance_level"] = lv

final = [p for p in plist if p.get("p4_scope")]
cnt = Counter(p["importance_level"] for p in final)
meta["summary"]["p4_scope_total"] = len(final)
meta["summary"]["by_level"] = dict(cnt)
meta["summary"]["trim_version"] = "v4c_final_2026-11-17"
json.dump(meta, open(f"{BASE}/person_list.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
rec = json.load(open(f"{BASE}/_p3_reports/p4_trim_final.json", encoding="utf-8"))
rec["v4c_micro_cut"] = MICRO_CUT
rec["v4c_upgrade"] = UPGRADE
json.dump(rec, open(f"{BASE}/_p3_reports/p4_trim_final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"最终 P4 范围: {len(final)}  high={cnt.get('high',0)} medium={cnt.get('medium',0)} low={cnt.get('low',0)}")

# -*- coding: utf-8 -*-
"""EG P4 trim v4-final: land total at 200-210 via second-pass sieve."""
import json, sys, io, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from collections import Counter

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
meta = json.load(open(f"{BASE}/person_list.json", encoding="utf-8"))
plist = meta["persons"]
draft = json.load(open(f"{BASE}/_p3_reports/p4_trim_draft.json", encoding="utf-8"))
CUTS, RECLASS_UP = draft["cuts"], draft["reclass_up"]

cut_ids = set()
for ids in CUTS.values():
    cut_ids.update(ids)
SIEVE_KN = ["EG-PERSON-000236","EG-PERSON-000237","EG-PERSON-000248",
            "EG-PERSON-000309","EG-PERSON-000316","EG-PERSON-000332",
            "EG-PERSON-000355","EG-PERSON-000356","EG-PERSON-000357","EG-PERSON-000369",
            "EG-PERSON-000106","EG-PERSON-000107","EG-PERSON-000108","EG-PERSON-000123","EG-PERSON-000126","EG-PERSON-000127"]
cut_ids.update(SIEVE_KN)

scope = [p for p in plist if p.get("in_p4_scope", True) and p["person_id"] not in {"EG-PERSON-" + str(i).zfill(6) for i in []}]
kept = [p for p in scope if p["person_id"] not in cut_ids]

# ---- second-pass sieve (refined, target ~202) ----
V4B = {
  "K2_银行/交易所非执行荣誉董事长(执行层已保留)": [
    "EG-PERSON-000221",  # NBE 非执行主席
    "EG-PERSON-000224",  # Banque Misr 非执行主席
    "EG-PERSON-000258",  # 农业银行 非执行主席
    "EG-PERSON-000262",  # EGX 非执行主席
    "EG-PERSON-000228",  # 开罗银行(土资) 非执行主席
    "EG-PERSON-000166",  # Elsewedy 非执行董事长
  ],
  "O1_国企/承包商副董事长(非一把手)": [
    "EG-PERSON-000153",  # 阿拉伯承包商 第一副董事长
    "EG-PERSON-000154",  # 阿拉伯承包商 副董事长
  ],
  "P1_金融子板块/子公司层": [
    "EG-PERSON-000186",  # GB Capital CEO(集团CEO已保留)
    "EG-PERSON-000264",  # 埃及保险子公司董事长
    "EG-PERSON-000265",  # 埃及保险子公司CEO
  ],
  "Q2_媒体历史创刊主编(非现役)": [
    "EG-PERSON-000358",  # 曙光报 创刊期主编 2008-2009
    "EG-PERSON-000361",  # Youm7 创刊主编 2009
    "EG-PERSON-000331",  # 金字塔法语周刊主编
    "EG-PERSON-000330",  # 金字塔周刊主编(母报主编已保留)
  ],
  "R2_继任者已覆盖的前任": [
    "EG-PERSON-000371",  # UMS 前董事长(370 现任)
    "EG-PERSON-000376",  # UMS 代理董事长(370 现任, 代理段已结束)
    "EG-PERSON-000397",  # 光明党副主席(布拉米系, 现主席已保留)
    "EG-PERSON-000223",  # NBE 副CEO
    "EG-PERSON-000251",  # QNB 执行董事副CEO
    "EG-PERSON-000239",  # CIB 副CEO(零售数字)
    "EG-PERSON-000365",  # DNE 执行主编
  ],
  "S2_CIB职能层(E类漏网)": [
    "EG-PERSON-000240",  # 首席风险官
    "EG-PERSON-000241",  # 企业与投行部主管
    "EG-PERSON-000242",  # HR 主管
  ],
  "T2_Raya非执行董事(漏网)": [
    "EG-PERSON-000208",
  ],
}
sieve2 = set()
for ids in V4B.values():
    sieve2.update(ids)

final = [p for p in kept if p["person_id"] not in sieve2]
cut2 = [p for p in kept if p["person_id"] in sieve2]
cnt = Counter(p["importance_level"] for p in final)

print(f"v3后: {len(kept)} | 二筛: -{len(cut2)} | 最终: {len(final)}")
print(f"  high={cnt.get('high',0)} medium={cnt.get('medium',0)} low={cnt.get('low',0)}")

# fix 000055 display name (registry stored QID as name)
for p in plist:
    if p["person_id"] == "EG-PERSON-000055" and p.get("name","").startswith("Q"):
        p["name"] = "艾哈迈德·艾斯威迪 (Ahmed Elsewedy)"
        p["name_zh"] = "艾哈迈德·艾斯威迪"
        p["name_en"] = "Ahmed Elsewedy"
        print("fixed 000055 display name")

# apply flags
all_cut = set(cut_ids) | sieve2
for p in plist:
    pid = p["person_id"]
    in_final = pid in {q["person_id"] for q in final}
    p["p4_scope"] = in_final
    if not in_final:
        reasons = CUTS.get(pid, []) + [k for k, ids in V4B.items() if pid in ids]
        if pid in SIEVE_KN:
            reasons = reasons + ["v4一轮筛"]
        p["p4_trim_reason"] = "; ".join(reasons) if reasons else "v3/v4裁剪"
    if pid in RECLASS_UP:
        p["importance_level"] = RECLASS_UP[pid]

meta["persons"] = plist
meta["summary"] = {
    "p4_scope_total": len(final),
    "by_level": dict(cnt),
    "trimmed": len(all_cut),
    "trim_version": "v4_final_2026-11-17_osint_political_priority",
}
json.dump(meta, open(f"{BASE}/person_list.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

json.dump({"v3_cuts": CUTS, "v4_sieve": V4B, "reclass_up": RECLASS_UP},
          open(f"{BASE}/_p3_reports/p4_trim_final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("person_list.json finalized; trim record saved")

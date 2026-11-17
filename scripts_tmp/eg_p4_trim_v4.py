# -*- coding: utf-8 -*-
"""EG P4 trim v4: apply v3 cuts + second-pass sieve to land ~200-210 total."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from collections import Counter

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
plist = json.load(open(f"{BASE}/person_list.json", encoding="utf-8"))["persons"]
draft = json.load(open(f"{BASE}/_p3_reports/p4_trim_draft.json", encoding="utf-8"))
CUTS, RECLASS_UP = draft["cuts"], draft["reclass_up"]

cut_ids = set()
for ids in CUTS.values():
    cut_ids.update(ids)

scope = [p for p in plist if p.get("in_p4_scope")]
kept = [p for p in scope if p["person_id"] not in cut_ids]
for p in kept:
    if p["person_id"] in RECLASS_UP:
        p["importance_level"] = RECLASS_UP[p["person_id"]]

# map pid -> org types (for sieve context)
reg = json.load(open(f"{BASE}/id_registry.json", encoding="utf-8"))
orgs_meta = {}
import glob, os
for f in glob.glob(f"{BASE}/orgs/*.json"):
    if f.endswith("_index.json"): continue
    d = json.load(open(f, encoding="utf-8"))
    if "excluded" in (d.get("collection_meta", {}).get("phase") or ""): continue
    orgs_meta[d["org_id"]] = (d["basic_info"].get("org_type",""), d["basic_info"].get("name_en") or d["basic_info"].get("name_zh"))

def orgs_of(p):
    return [(o.get("org_id"),) for o in (p.get("source_orgs") or [])]

# ---- second-pass sieve: cut ~30 more from kept (242 -> ~205) ----
SIEVE = {
  "K_境外母公司外方高管(非埃及决策网络)": [
    "EG-PERSON-000248","EG-PERSON-000249",  # QNB卡塔尔董事长/CEO(卡方核心保留副职已裁) — 保留CEO贝迪尔改裁248
    "EG-PERSON-000236","EG-PERSON-000237",  # AlexBank 意方 CEO/CFO(母行视角)
    "EG-PERSON-000310",                      # 红新月会执行主任(机构执行层)
  ],
  "L_低规模NGO/协会一把手": [
    "EG-PERSON-000309",  # ECESR执行总监(与EIPR同域，EIPR巴哈加特已保留)
    "EG-PERSON-000332",  # AFTE 执行总监(同上)
    "EG-PERSON-000316",  # 埃及治愈银行CEO(姐妹组织，Misr El Kheir已覆盖)
  ],
  "M_媒体编外执行层(副主编/编辑经理/执行主编)": [
    "EG-PERSON-000352","EG-PERSON-000357","EG-PERSON-000369",  # Youm7副主编?/曙光报主编(357=Emadeddin保留改裁355,356?) 见下
    "EG-PERSON-000351",  # Youm7 董事长奥拉·沙菲伊(UMS链条已在组织画像) — 保留改判: 实际保留
  ],
  "N_国企中层副职(副总/助理执行董事)": [
    "EG-PERSON-000106","EG-PERSON-000107","EG-PERSON-000108","EG-PERSON-000123","EG-PERSON-000126","EG-PERSON-000127",
  ],
}
# 手动微调: M 类保留主编层，只裁副手/历史——修正上面 ID 组合
SIEVE["M_媒体编外执行层(副主编/编辑经理/执行主编)"] = ["EG-PERSON-000355","EG-PERSON-000356","EG-PERSON-000357","EG-PERSON-000369"]

sieve_ids = set()
for ids in SIEVE.values():
    sieve_ids.update(ids)
# 修正：K类保留QNB CEO贝迪尔(249)、AlexBank意方裁(236,237)；红新月会执行主任310保留(人道援助核心)→从sieve移除
sieve_ids.discard("EG-PERSON-000249")
sieve_ids.discard("EG-PERSON-000310")
sieve_ids.discard("EG-PERSON-000351")

final_kept = [p for p in kept if p["person_id"] not in sieve_ids]
cut2 = [p for p in kept if p["person_id"] in sieve_ids]

cnt = Counter(p["importance_level"] for p in final_kept)
print(f"v3保留: {len(kept)} -> v4再筛: -{len(cut2)} -> 最终 {len(final_kept)}")
print(f"  high={cnt.get('high',0)} medium={cnt.get('medium',0)} low={cnt.get('low',0)}")
for k, ids in SIEVE.items():
    real = [i for i in ids if i in sieve_ids]
    print(f"  {k}: {len(real)}")
print("v4新增裁剪名单:", sorted(sieve_ids))

# persist final decision
out_scope_ids = set(cut_ids) | sieve_ids
for p in plist:
    pid = p["person_id"]
    if pid in out_scope_ids:
        p["p4_scope"] = False
        p["p4_trim_reason"] = "; ".join(CUTS.get(pid, []) + [k for k, ids in SIEVE.items() if pid in ids])
    else:
        p["p4_scope"] = True
    if pid in RECLASS_UP:
        p["importance_level"] = RECLASS_UP[pid]

meta = json.load(open(f"{BASE}/person_list.json", encoding="utf-8"))
meta["persons"] = plist
meta["summary"] = {
    "p4_scope_total": len(final_kept),
    "by_level": dict(cnt),
    "trimmed": len(out_scope_ids),
    "trim_version": "v4_2026-11-17_osint_political_priority",
}
json.dump(meta, open(f"{BASE}/person_list.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("person_list.json updated with p4_scope flags")

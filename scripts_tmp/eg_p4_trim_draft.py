# -*- coding: utf-8 -*-
"""EG P4 trim proposal computation (draft, pending user confirmation)."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from collections import Counter

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
plist = json.load(open(f"{BASE}/person_list.json", encoding="utf-8"))["persons"]
pmap = {p["person_id"]: p for p in plist}

# ---- cut categories (OSINT draft v3, pending confirmation) ----
CUTS = {
  "A_已故人物(总统级除外)": ["EG-PERSON-000121","EG-PERSON-000155","EG-PERSON-000291","EG-PERSON-000404","EG-PERSON-000286","EG-PERSON-000427","EG-PERSON-000054"],
  "B_历史政党(NDP/FJP/解散党)次级与前任官员": ["EG-PERSON-000045","EG-PERSON-000415","EG-PERSON-000416","EG-PERSON-000417","EG-PERSON-000419","EG-PERSON-000422","EG-PERSON-000390","EG-PERSON-000400","EG-PERSON-000406","EG-PERSON-000410","EG-PERSON-000421","EG-PERSON-000423"],
  "C_学术与研究系统全体(校长/副校长/院长/研究所首脑)": ["EG-PERSON-000038","EG-PERSON-000267","EG-PERSON-000268","EG-PERSON-000269","EG-PERSON-000270","EG-PERSON-000271","EG-PERSON-000272","EG-PERSON-000273","EG-PERSON-000274","EG-PERSON-000275","EG-PERSON-000276","EG-PERSON-000277","EG-PERSON-000278","EG-PERSON-000279","EG-PERSON-000280","EG-PERSON-000281","EG-PERSON-000282","EG-PERSON-000283","EG-PERSON-000284","EG-PERSON-000285","EG-PERSON-000287","EG-PERSON-000288","EG-PERSON-000289","EG-PERSON-000290","EG-PERSON-000292","EG-PERSON-000293","EG-PERSON-000294","EG-PERSON-000295","EG-PERSON-000296","EG-PERSON-000297","EG-PERSON-000298","EG-PERSON-000299","EG-PERSON-000300","EG-PERSON-000301","EG-PERSON-000302","EG-PERSON-000303","EG-PERSON-000304","EG-PERSON-000305","EG-PERSON-000306","EG-PERSON-000307","EG-PERSON-000308"],
  "D_企业非执行/独立/代表董事": ["EG-PERSON-000133","EG-PERSON-000134","EG-PERSON-000135","EG-PERSON-000136","EG-PERSON-000137","EG-PERSON-000138","EG-PERSON-000139","EG-PERSON-000140","EG-PERSON-000141","EG-PERSON-000171","EG-PERSON-000175","EG-PERSON-000187","EG-PERSON-000197","EG-PERSON-000198","EG-PERSON-000199","EG-PERSON-000200","EG-PERSON-000201","EG-PERSON-000206","EG-PERSON-000207","EG-PERSON-000208","EG-PERSON-000209","EG-PERSON-000219","EG-PERSON-000220","EG-PERSON-000226","EG-PERSON-000232","EG-PERSON-000238","EG-PERSON-000243","EG-PERSON-000244","EG-PERSON-000245","EG-PERSON-000246","EG-PERSON-000247","EG-PERSON-000250","EG-PERSON-000256","EG-PERSON-000337","EG-PERSON-000338","EG-PERSON-000339","EG-PERSON-000340","EG-PERSON-000380","EG-PERSON-000381","EG-PERSON-000382","EG-PERSON-000383","EG-PERSON-000384","EG-PERSON-000385","EG-PERSON-000386","EG-PERSON-000387"],
  "E_企业C-suite非一把手(CFO/CTO/COO/CHRO/CMO/CCO/副CEO等)": ["EG-PERSON-000126","EG-PERSON-000127","EG-PERSON-000157","EG-PERSON-000158","EG-PERSON-000164","EG-PERSON-000168","EG-PERSON-000170","EG-PERSON-000184","EG-PERSON-000195","EG-PERSON-000196","EG-PERSON-000223","EG-PERSON-000227","EG-PERSON-000230","EG-PERSON-000231","EG-PERSON-000237","EG-PERSON-000239","EG-PERSON-000240","EG-PERSON-000241","EG-PERSON-000242","EG-PERSON-000252","EG-PERSON-000260","EG-PERSON-000261","EG-PERSON-000317","EG-PERSON-000318","EG-PERSON-000319","EG-PERSON-000320","EG-PERSON-000321","EG-PERSON-000322","EG-PERSON-000323","EG-PERSON-000324","EG-PERSON-000325"],
  "F_前任高管冗余(继任者已在列/重复ID)": ["EG-PERSON-000089","EG-PERSON-000097","EG-PERSON-000098","EG-PERSON-000103","EG-PERSON-000112","EG-PERSON-000125","EG-PERSON-000151","EG-PERSON-000165","EG-PERSON-000234","EG-PERSON-000396"],
  "G_媒体历史/执行层/主持人/离场所有人": ["EG-PERSON-000342","EG-PERSON-000346","EG-PERSON-000347","EG-PERSON-000348","EG-PERSON-000350","EG-PERSON-000353","EG-PERSON-000354","EG-PERSON-000355","EG-PERSON-000356","EG-PERSON-000359","EG-PERSON-000360","EG-PERSON-000361","EG-PERSON-000363","EG-PERSON-000364","EG-PERSON-000365","EG-PERSON-000373","EG-PERSON-000375","EG-PERSON-000377","EG-PERSON-000378","EG-PERSON-000379"],
  "H_NGO中层(副职/荣誉职务/时任者)": ["EG-PERSON-000313","EG-PERSON-000314","EG-PERSON-000315","EG-PERSON-000327","EG-PERSON-000336","EG-PERSON-000341"],
  "I_发言人/部长助理(非决策层)": ["EG-PERSON-000065","EG-PERSON-000066","EG-PERSON-000067","EG-PERSON-000068","EG-PERSON-000074","EG-PERSON-000075"],
  "J_现任职务无法核实": ["EG-PERSON-000053"],
}

RECLASS_UP = {  # LOW -> HIGH/MEDIUM (user priority & actual weight)
  "EG-PERSON-000033": "high",   # 大伊玛目（爱资哈尔）宗教政治领袖
  "EG-PERSON-000079": "high",   # 最高宪法法院院长
  "EG-PERSON-000081": "high",   # 国务院院长
  "EG-PERSON-000119": "medium", # NSPO 总干事
  "EG-PERSON-000401": "medium", # 布拉米 萨拉菲召唤精神领袖
  "EG-PERSON-000257": "medium", # 沙兹利中将（军方，虽任银行董事）
}

scope = [p for p in plist if p.get("in_p4_scope")]
cut_ids = {}
for k, ids in CUTS.items():
    for i in ids:
        cut_ids.setdefault(i, []).append(k)

kept = [p for p in scope if p["person_id"] not in cut_ids]
cut = [p for p in scope if p["person_id"] in cut_ids]

# apply reclass
for p in kept:
    pid = p["person_id"]
    if pid in RECLASS_UP:
        p["importance_level"] = RECLASS_UP[pid]

cnt = Counter(p["importance_level"] for p in kept)
cut_cnt = Counter(p["importance_level"] for p in cut)
print(f"P4 现范围: {len(scope)}")
print(f"拟裁剪: {len(cut)}")
for k, ids in CUTS.items():
    print(f"  {k}: {len(ids)}")
print(f"拟保留: {len(kept)}  -> high={cnt.get('high',0)} medium={cnt.get('medium',0)} low={cnt.get('low',0)}")
print(f"裁剪分布: high={cut_cnt.get('high',0)} medium={cut_cnt.get('medium',0)} low={cut_cnt.get('low',0)}")
# any HIGH cut? list them
hc = [p["person_id"] + " " + (p.get("name","")[:20]) for p in cut if p["importance_level"]=="high"]
print("被裁HIGH人物:", hc if hc else "无")
# reclassified
print("重分级(LOW→升级保留):", {k: RECLASS_UP[k] for k in RECLASS_UP})
# save draft
json.dump({"cuts": CUTS, "reclass_up": RECLASS_UP},
          open(f"{BASE}/_p3_reports/p4_trim_draft.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("draft saved: _p3_reports/p4_trim_draft.json")

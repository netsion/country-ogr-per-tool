# -*- coding: utf-8 -*-
"""Apply OSINT-trim exclusion for 39 EG orgs; build P3 progress + dispatch table."""
import json, sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import load_json, save_json

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"

REASONS = {
    "EG-FIN-015": "v1: 支付卡品牌非组织实体，信息并入CBE画像",
    "EG-CORP-015": "v1: Telecom Egypt全资子公司已并入WE品牌，母公司已单列",
    "EG-PARTY-012": "v1: 历史小党，无QID无维基无席位，当代影响力趋零",
    "EG-GOV-042": "v2: 财政部执行机构无独立政治角色，财政政策由MOF覆盖",
    "EG-SOE-010": "v2: 二级控股壳，航空基础设施由民航部+EgyptAir覆盖",
    "EG-SOE-016": "v2: 二级控股壳，经营性资产为主无政治决策角色",
    "EG-CORP-008": "v2: 地毯制造商，政治关联度低无决策网络价值",
    "EG-CORP-013": "v2: 消费电子零售商，纯消费行业",
    "EG-CORP-016": "v2: 水晶制品出口商，细分行业价值极低",
    "EG-CORP-017": "v2: 家电集团，政治/情报价值低",
    "EG-FIN-011": "v2: 行业性中等银行，无独立政治角色",
    "EG-FIN-012": "v2: 仅借用运河名义的中等银行",
    "EG-ACAD-008": "v2: 地方公立大学无独特情报密度",
    "EG-ACAD-009": "v2: 地方公立大学无独特情报密度",
    "EG-ACAD-011": "v2: 地方公立大学无独特情报密度",
    "EG-ACAD-012": "v2: 地方公立大学，运河情报由SCZone/SCA覆盖",
    "EG-ACAD-013": "v2: 私立大学，双边旗舰价值低于E-JUST",
    "EG-ACAD-015": "v2: 小型私立大学价值最低",
    "EG-ACAD-023": "v2: 医学机构政治价值低",
    "EG-NGO-004": "v2: 大型慈善但无政治杠杆，与Misr El Kheir/Orman重叠",
    "EG-NGO-007": "v2: 发展类NGO政治价值低",
    "EG-NGO-008": "v2: 权益类影响力低于EIPR/AFTE",
    "EG-NGO-009": "v2: 学生志愿网络情报密度最低",
    "EG-NGO-011": "v2: 医疗慈善无政治杠杆",
    "EG-NGO-012": "v2: 区域文化资助机构价值低",
    "EG-NGO-013": "v2: 国际网络分支本地价值低",
    "EG-MEDIA-002": "v2: Al-Ahram英文子品牌情报重叠",
    "EG-MEDIA-004": "v2: 与Akhbar El-Yom同集团姊妹报",
    "EG-MEDIA-009": "v2: 新华夫脱党党报，并入政党画像",
    "EG-MEDIA-011": "v2: 在线中型媒体可被主流覆盖",
    "EG-MEDIA-013": "v2: 历史报纸当代发行量极小",
    "EG-MEDIA-014": "v2: 历史刊物当代影响力低",
    "EG-MEDIA-018": "v2: UMS旗下频道，情报并入母公司",
    "EG-PARTY-002": "v2: 亲政府外围小党无独立政治角色",
    "EG-PARTY-009": "v2: 小党无议会存在感",
    "EG-PARTY-010": "v2: 微型党",
    "EG-PARTY-011": "v2: 2014年内讧后活动停滞边缘化",
    "EG-INTL-005": "v2: 文化对话机构政治价值低",
    "EG-INTL-006": "v2: 行业性区域组织，由红新月会/阿盟覆盖",
}

EXCLUDED = sorted(REASONS)
assert len(EXCLUDED) == 39, len(EXCLUDED)

t = load_json(f"{BASE}/_target_orgs.json")
tmap = {o["id"]: o for o in t["organizations"]}
for oid in EXCLUDED:
    tmap[oid]["excluded"] = True
save_json(f"{BASE}/_target_orgs.json", t)

reg = load_json(f"{BASE}/id_registry.json")
for e in reg["registry"]:
    if e["org_id"] in REASONS:
        e["status"] = "excluded"
        e["notes"] = (e.get("notes") or "") + " | osint-trim: " + REASONS[e["org_id"]]
save_json(f"{BASE}/id_registry.json", reg)

for oid in EXCLUDED:
    p = f"{BASE}/orgs/{oid}.json"
    d = load_json(p)
    d["collection_meta"]["phase"] = "excluded_osint_trim"
    d["collection_meta"]["notes"] = (d["collection_meta"].get("notes") or "") + "; excluded: " + REASONS[oid]
    save_json(p, d)

# audit record
save_json(f"{BASE}/_excluded_orgs.json", {
    "date": "2026-11-17",
    "criteria": "OSINT政治+情报价值导向裁剪 (v1三处+v2用户确认)",
    "count": len(EXCLUDED),
    "orgs": [{"org_id": k, "reason": v} for k, v in sorted(REASONS.items())],
})

# P3 progress: category order GOV->MIL->SOE->CORP->FIN->ACAD->NGO->MEDIA->PARTY->INTL
ORDER = ["GOV", "MIL", "SOE", "CORP", "FIN", "ACAD", "NGO", "MEDIA", "PARTY", "INTL"]
remaining = []
for cat in ORDER:
    for o in t["organizations"]:
        if not o.get("excluded") and o["category"] == cat:
            remaining.append(o["id"])
prog = {
    "phase": "P3_org_enrichment",
    "started_at": "2026-11-17T00:00:00",
    "last_updated": "2026-11-17T00:00:00",
    "completed": [],
    "remaining": remaining,
    "current": [],
    "failed": [],
    "excluded_count": len(EXCLUDED),
    "total_scope": len(remaining),
    "note": "rolling 4-concurrent dispatch (user-approved deviation from skill max-2)",
}
save_json(f"{BASE}/_phase_progress.json", prog)

from collections import Counter
c = Counter(tmap[oid]["category"] for oid in remaining)
print("remaining:", len(remaining), dict(sorted(c.items())))
print("excluded:", len(EXCLUDED))

# dispatch reference table (id|en|zh|ar)
lines = []
for oid in remaining:
    bi = load_json(f"{BASE}/orgs/{oid}.json")["basic_info"]
    en = (bi.get("name_en") or "").replace("|", "/")
    zh = (bi.get("name_zh") or "").replace("|", "/")
    ar = (bi.get("name_original") or "").replace("|", "/")
    lines.append(f"{oid}|{en}|{zh}|{ar}")
with open(f"{BASE}/_tmp/p3_dispatch_table.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("dispatch table written:", len(lines), "rows")

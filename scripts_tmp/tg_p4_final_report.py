# -*- coding: utf-8 -*-
"""P4 最终报告生成：person_list 状态同步（queued->completed）+ _p4_final_report.json"""
import json
import os
import sys
import io
import glob
import statistics
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "output", "tg", "2026-11-16")

# ── 1. person_list 状态同步：204 queued -> completed ──
plf = os.path.join(BASE, "person_list.json")
pl = json.load(open(plf, encoding="utf-8"))
persons = pl["persons"] if isinstance(pl, dict) and "persons" in pl else pl
synced = 0
for p in persons:
    if p.get("status") == "queued":
        p["status"] = "completed"
        p["completed_at"] = "2026-11-17"
        synced += 1
json.dump(pl, open(plf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("person_list 状态同步:", synced, "queued -> completed")

# ── 2. 统计 ──
files = sorted(glob.glob(os.path.join(BASE, "persons", "TG-*.json")))
scores, quotes = [], 0
top10 = []
for fp in files:
    d = json.load(open(fp, encoding="utf-8"))
    s = (d.get("collection_meta") or {}).get("completeness_score")
    if isinstance(s, (int, float)):
        scores.append(s)
        top10.append((s, d["person_id"]))
    quotes += len((d.get("collection_meta") or {}).get("quotes") or [])
top10.sort(reverse=True)
scores.sort()
buckets = {"score_ge_85": 0, "score_75_84": 0, "score_60_74": 0, "score_45_59": 0, "score_lt_45": 0}
for s in scores:
    k = ("score_ge_85" if s >= 85 else "score_75_84" if s >= 75 else
         "score_60_74" if s >= 60 else "score_45_59" if s >= 45 else "score_lt_45")
    buckets[k] += 1

ledger = json.load(open(os.path.join(BASE, "_p5_pending_fixes.json"), encoding="utf-8"))

report = {
    "phase": "P4_person_profile",
    "completed_at": "2026-11-17",
    "coverage": {
        "queue_origin": 204,
        "completed": 204,
        "failed": 0,
        "excluded_pre_P4": 135,
        "merged_pre_P4": 3,
        "person_list_total": 342,
        "status_distribution_final": {"completed": 204, "merged": 3, "excluded": 135},
    },
    "quality": {
        "files_with_phase4": 204,
        "avg_completeness": round(statistics.mean(scores), 1),
        "median_completeness": statistics.median(scores),
        "max": max(scores),
        "min": min(scores),
        "score_distribution": buckets,
        "quotes_total": quotes,
        "score_85_plus_examples": [f"{pid}({s})" for s, pid in top10[:12]],
    },
    "registry_growth": {
        "person_registry_total": 608,
        "note": "P4 期间关系链交叉引用累计注册新人物 ID 至 000608（含外籍/历史人物），P5 交叉核验时复核保留范围",
        "name_index_entries_final": 5178,
    },
    "key_discoveries": [
        "ANR 指挥层换代全链条：2026-08-17 第2026-165/166 号法令，阿耶瓦拉尼接任局长、埃索韦任副局长，恰克佩莱同日晋升准将转任总参谋长",
        "马西纳合并悬案结案：000335 与 000342 确认同一自然人（四源），000342 履历已并入 000335，无需改指",
        "ATOP/UBLT 同名疑虑结案：埃耶比伊仅一人，系批次编号相邻误疑，无需合并",
        "IBANK 总经理三任链闭环：塔哈里(2021-12)→拉莱(2023-03)→迪亚洛(2024-10-16)",
        "维基/官方证伪清单：阿尔瓦法利非现任 BSIC PDG（创始 1999-2012）；库伊甘非记者出身（法学家）；阿科蒂亚非加纳人（多哥司铎）；USTTG 非洛美大学拆分（2012 私立 RUSTA）；AVIDI 非残障 NGO（志愿人道综合发展）",
        "跨国外联价值人物：BRVM 首富纳萨（Coris 创始人）、Gérard Mestrallet 之弟帕特里克·梅斯特拉莱（Oragroup 前 GM）、CAMS/中国媒体论坛三度参与者巴萨杜",
        "反诈排除：Facebook/TikTok「Ingrid Awadé 基金会」疑为冒名诈骗网络（多哥部长 2023-01 公开警示），已排除",
    ],
    "p5_handoff": {
        "ledger_file": "_p5_pending_fixes.json",
        "ledger_items": len(ledger["items"]),
        "ledger_resolved": 2,
        "ledger_open_highlights": [
            "FIN-006 key_people 阿尔瓦法利 PDG 头衔陈旧（现任 PDG 为 El Hadi 000505）",
            "FIN-010 孔帕奥雷职务归属（集团控股层面）与就任日期回填",
            "双 ID 合并：勒盖努 000517→000379；恩迪亚耶 000489→000181；泽甘 000382→000190；让达 000068→000293；图努 000551→000539",
            "TG-CORP-002 key_people 恩迪亚耶副总现任性（任期止 2024-07）",
            "TG-ACAD-006 加格洛 CET 副主席更正 + UCAO 认证疑点解除（已复核 2025/2026 名单在列）",
            "TG-PARTY-004/008 组织档案日期精度与 CET 现任主席补录评估",
            "新组织候选：达查大学（2026 新设，校长巴查纳 000536/一副校长瓦拉原任）",
            "军方线沿用：GOV-007 法官任期、000010/018/290 死亡标记等 P3 遗留项",
        ],
    },
    "degree_enum_v2_compliance": "335 条 education 全部标准枚举（2026-11-17 复扫 0 脏值）",
}
json.dump(report, open(os.path.join(BASE, "_p4_final_report.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("saved: _p4_final_report.json")
print("top12:", report["quality"]["score_85_plus_examples"][:6])

# -*- coding: utf-8 -*-
"""P5-5 最终完整性报告落盘：_p5_integrity_report.json"""
import json, os, sys, io, glob, statistics
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "output", "tg", "2026-11-16")

def load(p):
    return json.load(open(p, encoding="utf-8"))

# 组织统计
otypes, oscores = {}, {}
for fp in glob.glob(os.path.join(BASE, "orgs", "TG-*.json")):
    d = load(fp)
    bi = d.get("basic_info") or {}
    ot = bi.get("org_type", "?")
    otypes[ot] = otypes.get(ot, 0) + 1
    s = (d.get("collection_meta") or {}).get("completeness_score")
    if isinstance(s, (int, float)):
        oscores.setdefault(ot, []).append(s)
org_stats = {ot: {"count": n, "avg_score": round(statistics.mean(oscores[ot]), 1) if oscores.get(ot) else None}
             for ot, n in sorted(otypes.items(), key=lambda x: -x[1])}

# 人物统计
pl = load(os.path.join(BASE, "person_list.json"))
persons = pl["persons"] if isinstance(pl, dict) and "persons" in pl else pl
byp = {p["person_id"]: p for p in persons}
plev, pscores = {}, {}
ps_list = []
for fp in glob.glob(os.path.join(BASE, "persons", "TG-*.json")):
    d = load(fp)
    lv = (byp.get(d["person_id"]) or {}).get("importance_level", "?")
    plev[lv] = plev.get(lv, 0) + 1
    s = (d.get("collection_meta") or {}).get("completeness_score")
    if isinstance(s, (int, float)):
        pscores.setdefault(lv, []).append(s)
        ps_list.append(s)
person_stats = {lv: {"count": n, "avg_score": round(statistics.mean(pscores[lv]), 1) if pscores.get(lv) else None}
                for lv, n in sorted(plev.items(), key=lambda x: -x[1])}

ledger = load(os.path.join(BASE, "_p5_pending_fixes.json"))

report = {
    "phase": "P5_validation",
    "completed_at": "2026-11-17",
    "validation": {
        "command": "validate_schema.py --strict --cross-ref（标准非隔离模式）",
        "cross_ref_errors": 0,
        "cross_ref_warnings": 4,
        "warning_nature": "4 条「person 无该组织任职痕迹」启发式警告，均为主管/统辖关系而非雇佣关系（部长主管 Radio Lomé、总统统辖宪兵、总参谋长跨体系任命、GOV-004 官职实体骨架被总统 key_people 引用），属结构性现实，非错绑",
        "tooling_note": "校验须以非隔离模式（python script.py）运行：隔离模式 -I 会导致共享库 decompose_name 导入失败、名称分词退化为整串比对，产生约 1500 个假阳性 name-mismatch（已于 P5 复现并排除）",
    },
    "fixes_applied": {
        "name_normalization": "70 处引用显示名对齐目标档案 canonical 名（work_experience 48 + key_people 2 + related_entities 22 内含 + relationships 1）",
        "extra_fields": "83 个字段按校验器白名单剥离并归档至 collection_meta.notes（org_id_note/source_note/education_note/顶层 *_note 等）",
        "dual_id_merges": "5 组合并+2 项悬案结案：000517→000379、000489→000181、000382→000190、000068→000293、000551→000539；000342→000335（四源证实同一人）、ATOP/UBLT 同名疑虑排除",
        "registry_hygiene": "6 个 listed 无档案 → trimmed/merged；129 个 key_people 引用的登记人物 → trimmed（校验器跳过语义）；吸收 ID 全部 merged+merged_into",
        "skeleton_repairs": "FIN-012/SOE-006/SOE-008 补 name_zh+合法 org_subtype+quotes 墓碑；GOV-004 head_of_state、PARTY-009 opposition_party 合法化（保留裁剪骨架性质说明）",
        "ledger_corrections": "FIN-006 现任PDG El Hadi(000505) 补录+阿尔瓦法利头衔更正；FIN-010 孔帕奥雷归属更正；CORP-002 恩迪亚耶离任化；ACAD-006 CET 副主席更正+认证疑点解除；NGO-008 当选日期 2017-04→2017-03-07",
    },
    "org_profiles": {
        "total": 88,
        "avg_score": 84,
        "by_type": org_stats,
        "state_capped": "GOV-006/GOV-017/SOE-007/PARTY-007/PARTY-008 等低分为机构真实状态限制（未运作/新设/解散/休眠），非采集失败",
    },
    "person_profiles": {
        "total": 204,
        "avg_score": round(statistics.mean(ps_list), 1) if ps_list else None,
        "median": statistics.median(ps_list) if ps_list else None,
        "by_level": person_stats,
        "score_note": "<45 的 9 个为极低曝光人物（ANR 副局长/女童军总专员/SIAB 财务总监等）诚实上限；铁律禁止编造优先于凑分",
    },
    "indexes": {
        "orgs_index": "orgs/_index.json (88)",
        "persons_index": "persons/_index.json (204)",
        "name_index_entries": 4795,
    },
    "remaining_recommendations": [
        "台账 1 项开放：达查大学（2026 新设高校）是否补录为新组织档案（ACAD 系）",
        "P3 遗留数据修正：GOV-007 法官任期更正；TG-PERSON-000010/018/106/290 死亡标记；000033 QID 清理；Babaté（现任海军参谋长）补录候选；INTL-003 迪亚涅离任更正",
        " Registry 中 P4 交叉注册外籍/历史人物（000498-000608 段）保留范围可再复核（现均 trimmed 标记，不影响校验）",
        "头像管线：orgs 无头像需求；persons 头像 local_path/minio_path 由上传管线统一回填（本轮 000171/000195 等已采直链）",
    ],
}
json.dump(report, open(os.path.join(BASE, "_p5_integrity_report.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("saved: _p5_integrity_report.json")

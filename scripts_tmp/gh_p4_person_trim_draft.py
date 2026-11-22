# -*- coding: utf-8 -*-
"""P4 人物 OSINT 裁剪草案：政治领袖/政府高官/活跃政党/军事 优先。
输出 DRAFT（_p4_person_trim_DRAFT.json），不改任何数据，待用户确认。"""
import json, re, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pl = json.load(open(r"output/gh/2026-11-17/person_list.json", encoding="utf-8"))
targets = {t["org_id"]: t["category"] for t in json.load(
    open(r"output/gh/2026-11-17/_p3_final_targets.json", encoding="utf-8"))["targets"]}

def cats(p):
    return sorted(set(targets.get(s["org_id"], "?") for s in (p.get("source_orgs") or [])))

def orgs_names(p):
    return "/".join((s.get("org_name") or "?")[:24] for s in (p.get("source_orgs") or [])[:2])

# ---------- 规则 ----------
# 低值角色模式（functional/board/former）
OPS = re.compile(
    r"董事会成员|Board Member|兼职委员|全职委员|当然兼职|公司秘书|首席财务官|CFO|首席技术官|CTO|"
    r"首席运营官|COO|财务经理|筹资经理|内部审计|市场主管|销售经理|商务发展|社交媒体经理|社媒|"
    r"节目经理|区域新闻编辑|主线新闻编辑|在线编辑|前 (总编辑|所长|副校长|代理首席执行官)|前任(代理)?首席执行官|"
    r"创始核心研究研究员|研究研究员（|代理教务长|学生事务长|注册主任|传播事务官|工程系统协调员|"
    r"司专员|中心主任（|研究院行政主管|副局长|副执行秘书")
# 高官/领袖模式（GOV/MIL/PARTY 内的 low 需保留并升格）
LEADER = re.compile(
    r"议长|大法官|首席大法官|少数党领袖|多数党领袖|党领袖|党魁|总书记|总司令|参谋长|司令|"
    r"警察总监|督察长|移民总长|总监察长|局长\(Commissioner-General\)|执行秘书 \(Executive|主席 \(Chairperson|"
    r"副校长|校长 (Chancellor|Vice-Chancellor)|院长 \(Rector|董事长|创始人、领袖|理事会主席|董事总经理|"
    r"首席执行官|总统任命成员|当然成员|区域民选代表|副主席（运营|副主席 \(Deputy Chairperson|委员 \(Commissioner\)|"
    r"副首席执行官")
# 明确例外
TRIM_EXCEPTION_IDS = {
    "GH-PERSON-000029",  # Yofi Grant GIPC前CEO（2025-02卸任，现任CEO为Madjie/另有人）——实际上他是前任
    "GH-PERSON-000164", "GH-PERSON-000165", "GH-PERSON-000166", "GH-PERSON-000167",  # GSSTC中心主任/行政
    "GH-PERSON-000107", "GH-PERSON-000108", "GH-PERSON-000109",  # GRA三司专员（中层税务官员）
    "GH-PERSON-000135", "GH-PERSON-000136",  # NIA两副执行秘书
    "GH-PERSON-000213",  # 水资源委工程协调员
    "GH-PERSON-000214",  # NEDCo董事会成员
    "GH-PERSON-000152",  # 标准局消费者代表董事
    "GH-PERSON-000114", "GH-PERSON-000115", "GH-PERSON-000116",  # GTEC董事会成员×3
    "GH-PERSON-000179", "GH-PERSON-000180", "GH-PERSON-000181", "GH-PERSON-000182",
    "GH-PERSON-000183", "GH-PERSON-000184", "GH-PERSON-000185", "GH-PERSON-000186",
    "GH-PERSON-000187", "GH-PERSON-000188", "GH-PERSON-000189", "GH-PERSON-000190",  # EPA董事会×12
    "GH-PERSON-000292", "GH-PERSON-000293",  # SSNIT董事会×2
    "GH-PERSON-000198", "GH-PERSON-000199", "GH-PERSON-000200", "GH-PERSON-000201", "GH-PERSON-000202",  # GIMPA委员×5
    "GH-PERSON-000216",  # GNPC前任代理CEO
    "GH-PERSON-000358", "GH-PERSON-000359",  # Multimedia COO/CFO
    "GH-PERSON-000360", "GH-PERSON-000361", "GH-PERSON-000362",  # Joy/Adom/库马西品牌GM
    "GH-PERSON-000366",  # New Times 前总编辑
    "GH-PERSON-000367",  # 旁观者报编辑（周报）
    "GH-PERSON-000373", "GH-PERSON-000375", "GH-PERSON-000376", "GH-PERSON-000378",
    "GH-PERSON-000379", "GH-PERSON-000380", "GH-PERSON-000381",  # Citi 节目/商务/销售/在线/区域/主线/社媒
    "GH-PERSON-000401",  # UDS前副校长
    "GH-PERSON-000406",  # Ashesi教务长
    "GH-PERSON-000413", "GH-PERSON-000414", "GH-PERSON-000420", "GH-PERSON-000427",  # 教务长代理/学生事务/注册主任/传播
    "GH-PERSON-000425",  # INRA前所长
    "GH-PERSON-000429", "GH-PERSON-000430", "GH-PERSON-000431", "GH-PERSON-000432",  # CEPA创始研究员×4（智库已停运）
    "GH-PERSON-000450", "GH-PERSON-000451", "GH-PERSON-000452",  # GII财务/筹资/ALAC专员
    "GH-PERSON-000449",  # 红十字会理事会副主席
    "GH-PERSON-000295", "GH-PERSON-000298", "GH-PERSON-000312",  # MTN CFO/CTO/公司秘书
    "GH-PERSON-000313", "GH-PERSON-000314", "GH-PERSON-000315", "GH-PERSON-000316",
    "GH-PERSON-000317", "GH-PERSON-000318", "GH-PERSON-000319",  # MTN董事会×7
    "GH-PERSON-000322", "GH-PERSON-000323",  # Niche两GM
    "GH-PERSON-000325", "GH-PERSON-000326", "GH-PERSON-000328",  # Zoomlion COO×2/执行官
    "GH-PERSON-000332",  # Niche市场主管
    "GH-PERSON-000334", "GH-PERSON-000336", "GH-PERSON-000337",  # Springfield COO/CFO/副总裁
    "GH-PERSON-000343",  # McDan内审
}
KEEP_UPGRADE_IDS = {
    "GH-PERSON-000019",  # CDD创始人 Gyimah-Boadi（民主治理学界元老）
    "GH-PERSON-000021",  # 前总统 Akufo-Addo
    "GH-PERSON-000023",  # Samia Nkrumah（恩克鲁玛之女，CPP领袖——历史线价值）
    "GH-PERSON-000395",  # Otumfuo Osei Tutu II（阿散蒂赫内，传统权威最高领袖）
    "GH-PERSON-000396",  # Sam E. Jonah（矿业巨子、UCC名誉校长）
    "GH-PERSON-000330",  # Ahmed Hussein-Suale（已故调查记者，TigerEye谱系节点）
    "GH-PERSON-000434",  # CDD联合创始人 Agyeman-Duah
}
# 国务委员会成员（总统任命咨询层——政治人物保留）
COS_IDS = {"GH-PERSON-000052", "GH-PERSON-000054", "GH-PERSON-000055",
           "GH-PERSON-000056", "GH-PERSON-000057"}

# ---------- 分档 ----------
A, B, KUP = [], [], []
for p in pl["persons"]:
    pid = p["person_id"]
    lvl = p.get("importance_level") or "low"
    cs = cats(p)
    row = (pid, lvl, ",".join(cs), (p.get("name_en") or p.get("name") or "?"),
           (p.get("importance_reason") or "")[:40], orgs_names(p))
    if not cs:
        A.append((row, "非P3目标组织遗留注册（外国历史人物/历史政党人物/重复条目），与96目标无关联"))
        continue
    if lvl in ("high", "medium"):
        continue  # 高/中值全部保留
    if pid in KEEP_UPGRADE_IDS:
        KUP.append((row, "低分但具特殊政治/情报价值，建议升格保留"))
        continue
    if pid in COS_IDS:
        B.append((row, "国务委员会成员（总统任命咨询层），政治人物——倾向保留"))
        continue
    if pid in TRIM_EXCEPTION_IDS:
        A.append((row, "功能性/董事会/中层角色或前任，OSINT优先级外"))
        continue
    if "MIL" in cs or "PARTY" in cs:
        continue  # 军事与活跃政党人物全保（用户优先级）
    if "GOV" in cs:
        if LEADER.search(p.get("importance_reason") or ""):
            continue  # GOV内高官/领袖关键词保留（议长/大法官/执行秘书/局长等）
        A.append((row, "GOV内非决策层角色且无领袖关键词"))
        continue
    # 其余类别 low：OPS模式裁剪，其余进B
    if OPS.search(p.get("importance_reason") or ""):
        A.append((row, "低值功能性角色"))
    else:
        B.append((row, "低级但角色不明——倾向裁剪，待复核"))

print("=== P4 人物 OSINT 裁剪草案 ===")
print("总人数 457；高级%d 中级%d 全保留" % (
    sum(1 for p in pl['persons'] if p.get('importance_level')=='high'),
    sum(1 for p in pl['persons'] if p.get('importance_level')=='medium')))
print("A组 坚定裁剪: %d" % len(A))
print("B组 边界（倾向保留）: %d" % len(B))
print("升格保留: %d" % len(KUP))
kept = 457 - len(A)
print("裁剪后 P4 规模: %d" % kept)
print()
print("--- A组名单（裁剪 %d）---" % len(A))
for row, why in sorted(A, key=lambda r: r[0][2]):
    print("  %s [%s] %s | %s | %s" % (row[0], row[2], row[3], row[4], why))
print()
print("--- B组（倾向保留 %d）---" % len(B))
for row, why in sorted(B, key=lambda r: r[0][2]):
    print("  %s [%s] %s | %s" % (row[0], row[2], row[3], row[4]))
print()
print("--- 升格保留 %d ---" % len(KUP))
for row, why in KUP:
    print("  %s [%s] %s | %s" % (row[0], row[2], row[3], row[4]))

draft = {
    "version": "P4-person-trim-DRAFT-v1", "date": "2026-11-18",
    "status": "DRAFT - awaiting user confirmation",
    "priority": "政治领袖/政府高官/活跃政党/军事优先",
    "bucket_A_firm_trim": [{"person_id": r[0], "level": r[1], "categories": r[2], "name": r[3],
                            "role": r[4], "orgs": r[5], "reason": w} for r, w in A],
    "bucket_B_borderline_keep": [{"person_id": r[0], "level": r[1], "categories": r[2], "name": r[3],
                                  "role": r[4], "orgs": r[5], "reason": w} for r, w in B],
    "bucket_keep_upgrade": [{"person_id": r[0], "level": r[1], "categories": r[2], "name": r[3],
                             "role": r[4], "orgs": r[5], "reason": w} for r, w in KUP],
    "stats": {"total": 457, "trim_A": len(A), "borderline_B": len(B),
              "keep_upgrade": len(KUP), "p4_after_trim": 457 - len(A)},
}
json.dump(draft, open(r"output/gh/2026-11-17/_p4_person_trim_DRAFT.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("\nDRAFT -> output/gh/2026-11-17/_p4_person_trim_DRAFT.json")

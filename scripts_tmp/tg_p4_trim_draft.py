# -*- coding: utf-8 -*-
"""P4 人物裁剪分析（OSINT 价值视角）：拟裁剪名单 + 理由，输出 _p4_trim_plan.json
原则（用户指示）：政治领袖高官、活跃政党/政治/军事人物优先保留；
裁剪候选 = 已故人物 / 休眠组织历史人物 / 前媒体台长 / 前企业高管 / 前公共机构负责人 / 事务性岗位
只生成计划文件，不修改 person_list.json / registry
"""
import json
import sys, io
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r"D:\ai-workspace\apec-osint-tool\output\tg\2026-11-16"
pl = json.load(open(BASE + r"\person_list.json", encoding="utf-8"))
persons = pl["persons"] if isinstance(pl, dict) and "persons" in pl else pl
by_id = {p["person_id"]: p for p in persons}

# ── 裁剪类别定义（person_id -> 理由）──
CULL = {}

# A. 已故人物（6）：组织档案 key_people 已记录其任职与去世，P4 深查无增量
for pid, r in {
    "TG-PERSON-000010": "PDR 创始主席 Ayéva，2025-12-15 去世（P3 多源核实）；任职信息已沉淀于 TG-PARTY-006 档案",
    "TG-PERSON-000018": "Caritas 董事会主席 Barrigah-Benissan（大主教），2024-08-04 去世（4+ 源）；已故宗教人物",
    "TG-PERSON-000209": "CAR 创始人/前总理阿博伊博，2020-05-30 去世（维基+RFI+DW）；前总理史实已记录",
    "TG-PERSON-000290": "FONGTO 主席 Agbove，2025-12 当选、2026-03-10 去世（讣告双源）；任职 3 个月即故",
    "TG-PERSON-000309": "JVE 创始人 Alouka，2026-08-31 法国去世（RFI/DW/维基多源）；继任未公布",
    "TG-PERSON-000218": "Juvento 历史党主席（据党史研究者记载，1950s 人物，组织已休眠）",
}.items():
    CULL[pid] = ("A_已故人物", r)

# B. 休眠组织历史人物（4）：Juvento 名义存续实质休眠（P3 核查结论）
for pid, r in {
    "TG-PERSON-000217": "Juvento 历史创始领导人（1950s），组织实质休眠",
    "TG-PERSON-000219": "Juvento 创始骨干（历史人物），组织实质休眠",
    "TG-PERSON-000220": "Juvento 前议员/党内书记（历史人物），组织实质休眠",
    "TG-PERSON-000228": "PSR 前总统候选人（2003 年），此后无现势职务记录",
}.items():
    CULL[pid] = ("B_休眠组织历史人物", r)

# C. 前媒体台长/社长（10）：历届任职已在 org 档案沿革记录，全部已卸任
for pid, r in {
    "TG-PERSON-000263": "ATOP 首任社长（1975-1976，历史任职）",
    "TG-PERSON-000264": "ATOP 社长（1976-1986，历史任职）",
    "TG-PERSON-000265": "ATOP 社长（1987-1991，历史任职）",
    "TG-PERSON-000266": "ATOP 社长（1991-2001，历史任职）",
    "TG-PERSON-000267": "ATOP 社长（2002-2006，历史任职）",
    "TG-PERSON-000268": "ATOP 社长（2006-2018，已卸任）",
    "TG-PERSON-000273": "TVT 前台长（临时，2023-2025，已被 2025-09 同批换帅免职）",
    "TG-PERSON-000274": "TVT 前台长（2018-2023，已卸任）",
    "TG-PERSON-000275": "TVT 前台长（2006-2018，已卸任）",
    "TG-PERSON-000278": "Radio Lomé 前台长（至 2025-09，已被同批换帅更替）",
}.items():
    CULL[pid] = ("C_前媒体负责人", r)

# D. 前企业高管（13）：继任者现势人物已在档，卸任者增量低
for pid, r in {
    "TG-PERSON-000091": "Togo Telecom 前总经理（2019-2022），继任者 Legagneur 在档",
    "TG-PERSON-000094": "CEET 前总经理（2022-2026），2026-06 已换人",
    "TG-PERSON-000095": "CEET 前代行总经理（2021-2022），历史任职",
    "TG-PERSON-000096": "CEET 前总经理（2020-2021），历史任职",
    "TG-PERSON-000100": "Togo Invest 首任总经理（仅姓氏'Mme Lana'可考，无法建档）",
    "TG-PERSON-000101": "Togo Invest 第二任总经理（前任），继任者在档",
    "TG-PERSON-000120": "BOAD 副行长（2020-2025 任期已满，卸任）",
    "TG-PERSON-000146": "BIA-Togo 董事长（2013 年时任，历史信息）",
    "TG-PERSON-000153": "Coris Togo 前总经理（2018-2026，调任科特迪瓦子公司）",
    "TG-PERSON-000166": "UTB 前总经理（2018-2024，已卸任）",
    "TG-PERSON-000177": "SIAB 总经理（2012 年时任，历史信息）",
    "TG-PERSON-000192": "BCP 集团前国际业务总经理（ex- 前缀，卸任）",
    "TG-PERSON-000193": "ABG 集团前总经理（至 2017-01，卸任逾 8 年）",
}.items():
    CULL[pid] = ("D_前企业高管", r)

# E. 前公共机构/NGO 负责人（18）：卸任或极早期任职
for pid, r in {
    "TG-PERSON-000011": "PSR 前党主席/创党领袖（已卸任，继任者沃卢在档）",
    "TG-PERSON-000015": "BCEAO 总干事（1955-1974，50 年前历史任职）",
    "TG-PERSON-000017": "BOAD 首任行长（1975-1981，历史任职）",
    "TG-PERSON-000033": "BOAD 前行长（1982-1994，历史任职；且系 QID 占位名 Q135988805 待清理）",
    "TG-PERSON-000121": "BOAD 前行长（1995-2006）；其贝宁前总统身份属贝宁数据集范围",
    "TG-PERSON-000125": "ARAA 首任执行署长（2024 已卸任荣休）",
    "TG-PERSON-000196": "ADDI 创党人 Adodo（1991 创党，现势职务与生命状态均无来源）",
    "TG-PERSON-000211": "CAR 前任主席（2008 起，已被现主席达特更替）",
    "TG-PERSON-000215": "PDR 前重要成员（2006 年退党，退党近 20 年）",
    "TG-PERSON-000216": "PDR 前重要成员（2006 年退党，退党近 20 年）",
    "TG-PERSON-000232": "卡拉大学前校长（2016-2023，已由现校长更替）",
    "TG-PERSON-000236": "ENA 前院长（2020-2023，2023 转任洛美大学校长后 2025 又卸任；双重前职）",
    "TG-PERSON-000238": "ITRA 前院长（已由杜蒂 2024-01 更替）",
    "TG-PERSON-000244": "UCAO-UUT 前秘书长（已卸任）",
    "TG-PERSON-000245": "UCAO-UUT 前校长（已卸任）",
    "TG-PERSON-000247": "EAMAU 前总干事（2024-12 已由 Boukar 更替）",
    "TG-PERSON-000249": "EAMAU 前理事会主席（已卸任）",
    "TG-PERSON-000254": "INAT/INFA 前总干事（2016-2024，已由巴马齐更替）",
    "TG-PERSON-000298": "大赦国际多哥前主席（卸任）",
    "TG-PERSON-000299": "大赦国际多哥前主席（卸任）",
    "TG-PERSON-000304": "Espoir Vie 前董事会主席（2020 年时在任，已更替）",
    "TG-PERSON-000312": "WiLDAF 前区域协调员（已由姆布鲁更替）；其在 UN 环境职位可经交叉核验时顺带记录",
    "TG-PERSON-000328": "Miawodo 前主任（法国 EdM 派驻，已离任）",
    "TG-PERSON-000341": "ANR 前局长（2014-2018，历史任职）",
}.items():
    CULL[pid] = ("E_前公共机构/NGO负责人", r)

# F. 事务性/技术岗位（现势但 OSINT 增量低，均为部门内二级岗）
for pid, r in {
    "TG-PERSON-000027": "国民议会第一财务官（questeur，议会事务性职位）",
    "TG-PERSON-000028": "国民议会第二财务官（事务性职位）",
    "TG-PERSON-000029": "国民议会第三财务官（事务性职位）",
    "TG-PERSON-000030": "国民议会第一议会秘书（事务性职位）",
    "TG-PERSON-000031": "国民议会第二议会秘书（事务性职位）",
    "TG-PERSON-000032": "国民议会第三议会秘书（事务性职位）",
    "TG-PERSON-000056": "CNDH 普通委员（人事已在 TG-GOV-012 档案全量记录）",
    "TG-PERSON-000058": "CNDH 普通委员",
    "TG-PERSON-000059": "CNDH 普通委员",
    "TG-PERSON-000060": "CNDH 普通委员",
    "TG-PERSON-000061": "CNDH 普通委员",
    "TG-PERSON-000062": "CNDH 普通委员",
    "TG-PERSON-000063": "CNDH 普通委员",
    "TG-PERSON-000067": "ARCOP 争议解决委员会普通成员",
    "TG-PERSON-000068": "ARCOP 争议解决委员会普通成员",
    "TG-PERSON-000069": "ARCOP 争议解决委员会普通成员",
    "TG-PERSON-000079": "洛美港法律事务部部长（部门二级事务官，官网组织页全量提取）",
    "TG-PERSON-000080": "洛美港人力资源部部长（同上）",
    "TG-PERSON-000081": "洛美港商务部部长（同上）",
    "TG-PERSON-000082": "洛美港运营部部长（同上）",
    "TG-PERSON-000083": "洛美港技术部部长（同上）",
    "TG-PERSON-000084": "洛美港财务会计部部长（同上）",
    "TG-PERSON-000085": "洛美港港务长/海务部部长（同上）",
    "TG-PERSON-000086": "洛美港医疗与社会中心主任（同上）",
    "TG-PERSON-000087": "洛美港信息系统部部长（同上）",
    "TG-PERSON-000088": "洛美港综合行政管理部部长（同上）",
    "TG-PERSON-000089": "洛美港内部审计部部长（同上）",
    "TG-PERSON-000114": "Ecobank Togo 董事（ETI 常驻代表，集团指派职务）",
    "TG-PERSON-000115": "Ecobank Togo 执行董事（董事会成员）",
    "TG-PERSON-000130": "BOA-Togo 董事（BOA West Africa 代表）",
    "TG-PERSON-000131": "BOA-Togo 董事",
    "TG-PERSON-000132": "BOA-Togo 董事",
    "TG-PERSON-000133": "BOA-Togo 董事",
    "TG-PERSON-000184": "ASKY 洛美枢纽经理（运营层）",
    "TG-PERSON-000239": "ITRA 昆虫学研究员（技术岗）",
    "TG-PERSON-000252": "IAEC 教务长（事务岗）",
    "TG-PERSON-000257": "UBLT 副校监（事务岗）",
    "TG-PERSON-000258": "UBLT 教务长（事务岗）",
    "TG-PERSON-000261": "UBLT 法律顾问（事务岗）",
    "TG-PERSON-000279": "Radio Lomé 高频部门主任（技术岗）",
    "TG-PERSON-000280": "Radio Lomé 传播专员（事务岗）",
    "TG-PERSON-000282": "Togo First 编辑部秘书（事务岗）",
    "TG-PERSON-000283": "Togo First 记者（事务岗）",
    "TG-PERSON-000285": "IciLomé 编辑/署名作者（事务岗）",
    "TG-PERSON-000286": "IciLomé 记者/撰稿人（事务岗）",
    "TG-PERSON-000288": "L'Union 记者（小报，事务岗）",
    "TG-PERSON-000300": "大赦国际 2026 青年代表（象征性职位）",
    "TG-PERSON-000307": "AGBO-ZEGUE 会计师（事务岗）",
    "TG-PERSON-000308": "AGBO-ZEGUE 项目专员（执行层）",
    "TG-PERSON-000310": "JVE 顾问（事务岗）",
    "TG-PERSON-000315": "AVIDI 计算机专员（技术岗）",
    "TG-PERSON-000318": "CREDO 董事会秘书（事务岗）",
    "TG-PERSON-000319": "CREDO 董事会司库（事务岗）",
    "TG-PERSON-000321": "CREDO 执行秘书（事务岗）",
    "TG-PERSON-000322": "CREDO 执行司库（事务岗）",
    "TG-PERSON-000323": "CREDO 传播专员（事务岗）",
    "TG-PERSON-000325": "Miawodo 行政与财务负责人（事务岗）",
    "TG-PERSON-000326": "Miawodo 垃圾管理部门负责人（执行层）",
    "TG-PERSON-000327": "Miawodo 小微企业陪伴部负责人（执行层）",
    "TG-PERSON-000330": "女童军青年领袖（仅名无姓，信息不足）",
    "TG-PERSON-000256": "UBLT 名誉校长（荣誉职位，尼日利亚传统统治者，无实职）",
}.items():
    CULL[pid] = ("F_事务性/技术岗位", r)

# ── 汇总输出 ──
found = []
missing = []
for pid in CULL:
    if pid in by_id:
        found.append(pid)
    else:
        missing.append(pid)
cats = defaultdict(list)
for pid, (cat, reason) in CULL.items():
    if pid in by_id:
        cats[cat].append(pid)

plan = {
    "generated": "2026-11-17",
    "phase": "P4_person_trim_draft",
    "status": "DRAFT_PENDING_USER_CONFIRMATION",
    "principle": "用户指示：政治领袖高官、活跃政党/政治/军事人物优先保留；裁剪候选按 OSINT 增量价值评估（现势性×影响力×可核性）",
    "keep_principles": [
        "GOV/MIL 现任官员与指挥链全部保留（含 medium）",
        "PARTY 现任领导层全部保留（含发言人/司库等，活跃政党 OSINT 价值高）",
        "FIN/CORP/SOE/INTL 现任一把手（DG/行长/董事长）保留",
        "董事长层（ACAD 校长/NGO 主席/媒体台长现任）保留",
        "国际网络人物（Dangote、Koné Dossongui、琼多创始人等）保留——跨国外联情报价值"
    ],
    "trim_candidates": {
        cat: {"count": len(ids), "person_ids": ids}
        for cat, ids in sorted(cats.items())
    },
    "trim_total": len(found),
    "duplicate_merge_needed_before_P4": [
        {"ids": ["TG-PERSON-000331", "TG-PERSON-000337", "TG-PERSON-000340"],
         "person": "Tchakpelé Aklesso / Ali Esso Tchakpélé（恰克佩莱·阿克莱索）",
         "evidence": "MIL-001 报告明示新任总参谋长为原 ANR 局长；000337 name_en 含两个拼写",
         "action": "保留 000331（现任总参谋长），000337/000340 引用改指 000331"},
        {"ids": ["TG-PERSON-000335", "TG-PERSON-000342"],
         "person": "Massina（马西纳，宪兵总局长 2014-2021 / ANR 2012 前后）",
         "evidence": "ANR 批次记载马西纳'后调任宪兵'，任期衔接一致",
         "action": "待 P4 核验后合并（保留 000335）"},
        {"ids": ["TG-PERSON-000001", "TG-PERSON-000006"],
         "person": "Faure (Essozimna) Gnassingbé",
         "evidence": "000006 为 P2 骨架旧注册（同名、无 title、level=low），000001 为 P3 挂接主档",
         "action": "保留 000001，000006 引用改指"},
    ],
    "missing_ids_not_in_list": missing,
}
json.dump(plan, open(BASE + r"\_p4_trim_plan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"裁剪候选总数: {len(found)} / 342 ({round(len(found)/342*100)}%)，P4 保留 {342-len(found)} 人")
print("missing（清单中无此 ID）:", missing if missing else "无")
print()
for cat in sorted(cats):
    print(f"{cat}: {len(cats[cat])} 人")
    for pid in cats[cat]:
        p = by_id[pid]
        print(f"   {pid} | {p.get('importance_level','?'):<6} | {(p.get('name_zh') or p.get('name_en') or p.get('name',''))[:22]:<22} | {CULL[pid][1][:48]}")
print()
print("saved: _p4_trim_plan.json (DRAFT，未修改 person_list.json)")

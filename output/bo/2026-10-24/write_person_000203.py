# -*- coding: utf-8 -*-
"""Generate BO-PERSON-000203 person profile JSON (Sergio Soliz Gomez)."""
import json
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PERSONS_DIR = os.path.join(OUT_DIR, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

profile = {
    "person_id": "BO-PERSON-000203",
    "wikidata_qid": None,
    "name_zh": "塞尔希奥·索利斯·戈麦斯",
    "name": "Sergio Soliz Gómez",
    "name_en": "Sergio Soliz Gomez",
    "aliases": ["Sergio Soliz"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "contacts": [],
    "current_positions": [],
    "education": [
        {
            "institution": "玻利维亚天主教圣保罗大学 (Universidad Católica Boliviana San Pablo)",
            "degree": "bachelor",
            "field": "法学"
        }
    ],
    "work_experience": [
        {
            "start_date": "2026-03-10",
            "end_date": "2026-06",
            "organization": "玻利维亚国家锂业公司 (Yacimientos de Litio Bolivianos, YLB)",
            "org_id": "BO-SOE-006",
            "position": "执行总裁"
        },
        {
            "start_date": "2019",
            "end_date": "2024",
            "organization": "玻利维亚水泥公司 (Sociedad Boliviana de Cemento S.A., SOBOCE)",
            "org_id": "BO-CORP-005",
            "position": "全国法律经理"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000619",
            "person_name": "毛里西奥·梅迪纳塞利 (Mauricio Medinaceli)",
            "relationship_type": "superior",
            "description": "玻利维亚碳氢化合物与能源部部长，2026年3月10日主持索利斯出任YLB执行总裁的就任仪式，为其任命上司。"
        },
        {
            "person_id": None,
            "person_name": "巴勃罗·尼纳·特兰 (Pablo Nina Terán)",
            "relationship_type": "colleague",
            "description": "YLB前任执行总裁（2025年8月15日就任），索利斯于2026年3月10日接替其职务。"
        },
        {
            "person_id": None,
            "person_name": "吉列尔莫·特里戈·纳格尔 (Guillermo Trigo Nagel)",
            "relationship_type": "colleague",
            "description": "石油与天然气工程师，2026年6月初以临时执行总裁身份接替索利斯执掌YLB。"
        },
        {
            "person_id": "BO-PERSON-000481",
            "person_name": "萨穆埃尔·多利亚·梅迪纳 (Samuel Doria Medina)",
            "relationship_type": "associate",
            "description": "企业家、政府盟友。议员莉萨·克拉罗斯指控索利斯系多利亚·梅迪纳安插的人选，后者公开否认，并说明索利斯任职SOBOCE（2019-2024）是在其出售该公司多年之后，与其无雇佣或顾问关系。"
        },
        {
            "person_id": "BO-PERSON-000501",
            "person_name": "莉萨·克拉罗斯 (Lissa Claros)",
            "relationship_type": "other",
            "description": "自由联盟（Libre）波托西籍众议员，公开质疑索利斯律师出身缺乏技术背景、称任命系政治分肥，并要求将其罢免。"
        }
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Sergio Soliz-Gómez",
            "url": "https://bo.linkedin.com/in/sergio-soliz-g%C3%B3mez-8aa2484",
            "source": "LinkedIn检索结果，页面列有YLB执行总裁与SOBOCE法律负责人经历，与本人物信息一致"
        }
    ],
    "family_members": [],
    "political_stances": [
        {
            "date": "2026-05-15",
            "topic": "锂产业运营恢复与增产",
            "stance_content": "任内作为YLB执行总裁推动「运营恢复计划」：设定2026年生产3,600吨碳酸锂和87,696吨氯化钾的目标（高于上一管理年度），并预计蒸发盐产品销售收入约5.34亿玻利维亚诺；称上述目标与执行技术方案、优化工业厂房既有装机能力并保障更高运营效率相挂钩，强调运营恢复是强化蒸发盐资源工业化、巩固企业可持续性的战略优先事项。",
            "source": "YLB官网新闻稿（2026-05-15，ylb.gob.bo）"
        }
    ],
    "major_achievements": [
        {
            "date": "2026-03-10",
            "achievement": "经碳氢化合物与能源部部长毛里西奥·梅迪纳塞利主持就任，成为玻利维亚国家锂业公司（YLB）自2017年创立以来的第七任执行总裁，执掌负责乌尤尼盐湖蒸发盐资源开发与锂工业化的国家战略企业。",
            "organization": "玻利维亚国家锂业公司 (Yacimientos de Litio Bolivianos, YLB)"
        },
        {
            "date": "2026-05-15",
            "achievement": "任内主导发布YLB 2026年运营恢复计划，确立年产3,600吨碳酸锂、87,696吨氯化钾的增产目标及约5.34亿玻利维亚诺的收入预期。",
            "organization": "玻利维亚国家锂业公司 (Yacimientos de Litio Bolivianos, YLB)"
        },
        {
            "date": "2022",
            "achievement": "入选Legal 500 GC Powerlist玻利维亚2022榜单（建材与矿业类推荐企业法律顾问，时任SOBOCE全国法律副经理），并于2023年、2024年以全国法律经理身份连续入选该榜单。",
            "organization": "玻利维亚水泥公司 (Sociedad Boliviana de Cemento S.A., SOBOCE)"
        }
    ],
    "biography_summary": "塞尔希奥·索利斯·戈麦斯（Sergio Soliz Gómez），玻利维亚律师出身的企业高管，获玻利维亚天主教圣保罗大学（拉巴斯）法学学位，并拥有英国工商管理硕士（MBA）学位，在碳氢化合物、矿业与工业领域拥有逾25年职业经验，专长融合法律管理与战略管理。2019至2024年任玻利维亚私营水泥龙头企业SOBOCE法律负责人（2022年任全国法律副经理，2023-2024年升任全国法律经理并兼任合规负责人，连续入选Legal 500 GC Powerlist玻利维亚榜单）。2026年3月10日，他在能源部长梅迪纳塞利主持下就任国家锂业公司YLB第七任执行总裁，接替巴勃罗·尼纳·特兰，任内推动2026年运营恢复计划、设定碳酸锂与氯化钾增产目标；任命因律师背景遭波托西公民委员会（Comcipo）及自由联盟议员克拉罗斯批评为缺乏技术含量、政治分肥。2026年6月初，YLB宣布由工程师吉列尔莫·特里戈·纳格尔临时接任，索利斯卸任，公告未披露去职原因；截至2026年10月未查到其新的公开任职。",
    "birth_date_note": "公开来源（新闻检索、LinkedIn摘要）均未披露其出生日期。",
    "name_zh_note": "中文译名「塞尔希奥·索利斯·戈麦斯」取自项目 _name_index.json 既有条目；未检索到玻利维亚华文媒体的独立译名报道。",
    "position_note": "2026年6月2-3日YLB公告由Guillermo Trigo Nagel出任临时执行总裁、接替索利斯，未披露去职原因；截至2026-10-25未查到索利斯的新任职务，故current_positions留空。",
    "work_note": "YLB官方通报称其拥有碳氢化合物、矿业与工业领域逾25年经验并兼具法律与战略管理背景，但相关早年任职机构未见公开披露；已核实职位为SOBOCE法律负责人（2019-2024：Doria Medina公开声明佐证2019年起任职，Legal 500榜单佐证2022年任全国法律副经理、2023-2024年任全国法律经理，BBV与PCR信用评级报告佐证2023年9月及2024年6月全国法律经理（Gerencia Nacional Legal）由其执掌、并被指定为合规负责人Encargado de Cumplimiento）及YLB执行总裁（2026年3-6月）。",
    "education_note": "拥有英国工商管理硕士（MBA）学位，具体院校未公开（YLB官方通报，经Correo del Sur、ABI/Los Tiempos、Opinión等多家媒体转引），故未单列education条目。",
    "family_note": "公开来源未查到其配偶、子女等家庭成员信息。",
    "social_accounts_note": "六项社交平台扫描（facebook/x/instagram/tiktok/youtube/linkedin）：仅核实到LinkedIn个人资料页；其余平台检索命中的均为媒体账号或YLB官方账号，非本人实名账号。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": ["official_website", "news_search", "web_search", "social_media"],
        "quotes": [
            {
                "title": "Sergio Soliz asume como nuevo presidente ejecutivo de YLB - Correo del Sur (2026-03-10)",
                "url": "https://correodelsur.com/politica/20260310/sergio-soliz-asume-como-nuevo-presidente-ejecutivo-de-ylb.html"
            },
            {
                "title": "Sergio Soliz Gómez asume como presidente ejecutivo de YLB - Los Tiempos/ABI (2026-03-11)",
                "url": "https://www.lostiempos.com/actualidad/economia/20260311/sergio-soliz-gomez-asume-como-presidente-ejecutivo-ylb"
            },
            {
                "title": "Sergio Soliz Gómez es el nuevo Presidente Ejecutivo de YLB - Opinión/Oxígeno (2026-03-11)",
                "url": "https://www.opinion.com.bo/pais/sergio-soliz-gomez-es-nuevo-presidente-ejecutivo-ylb/20260311194818989932.html"
            },
            {
                "title": "YLB impulsa plan de reactivación para incrementar producción e ingresos en 2026 - YLB官网 (2026-05-15)",
                "url": "https://www.ylb.gob.bo/index.php/nota_prensa/20656/"
            },
            {
                "title": "En nueve años, YLB tuvo tres gerentes y siete presidentes ejecutivos - Visión 360 (2026-03-11)",
                "url": "https://www.vision360.bo/noticias/2026/03/11/41353-en-nueve-anos-ylb-tuvo-tres-gerentes-y-siete-presidentes-ejecutivos-quienes-ocuparon-el-cargo-entre-uno-y-dos-anos-y-algunos-solo-unos-meses"
            },
            {
                "title": "Gobierno posesiona a un abogado como presidente de YLB; diputada califica la designación como política - ANF/Fides (2026-03-11)",
                "url": "https://www.noticiasfides.com/economia/gobierno-posesiona-a-un-abogado-como-presidente-de-ylb-diputada-califica-la-designacion-como-politica"
            },
            {
                "title": "Sergio Soliz asume como presidente de YLB y Comcipo cuestiona designación - eju.tv/La Razón (2026-03-11)",
                "url": "https://eju.tv/2026/03/sergio-soliz-asume-como-presidente-de-ylb-y-comcipo-cuestiona-designacion/"
            },
            {
                "title": "Doria Medina niega vínculo con nuevo Presidente de YLB - El Día (2026-03-11)",
                "url": "https://eldia.com.bo/2026-03-11/politica/doria-medina-niega-vinculo-con-nuevo-presidente-de-ylb-y-pide-a-diputada-de-libre-leer-antes-de-hablar.html"
            },
            {
                "title": "Guillermo Trigo asume como nuevo presidente de Yacimientos de Litio Bolivianos - eju.tv (2026-06-02)",
                "url": "https://eju.tv/2026/06/guillermo-trigo-asume-como-nuevo-presidente-de-yacimientos-de-litio-bolivianos/"
            },
            {
                "title": "Sergio Soliz-Gómez – GC Powerlist Bolivia 2022 - Legal 500",
                "url": "https://www.legal500.com/gc-powerlist/bolivia-2022/sergio-soliz-gomez/"
            },
            {
                "title": "Cambios en YLB: Sergio Soliz es posesionado como presidente mientras crecen dudas sobre el litio - Bolivia.com (2026-03-12)",
                "url": "https://www.bolivia.com/actualidad/economia/sergio-soliz-asumio-la-presidencia-de-la-ylb-en-medio-de-senalamientos-por-el-litio-573339"
            },
            {
                "title": "Sergio Soliz-Gómez - LinkedIn",
                "url": "https://bo.linkedin.com/in/sergio-soliz-g%C3%B3mez-8aa2484"
            }
        ],
        "notes": "共精读10个独立全文来源（Correo del Sur、Los Tiempos/ABI、Opinión/Oxígeno、ANF/Fides、eju.tv/La Razón、El Día、Visión 360、eju.tv/Trigo接任、YLB官网、Bolivia.com），另经Legal 500、BBV/PCR评级报告及LinkedIn检索摘要交叉验证。核心事实均经两个以上独立来源确认：就任日期2026-03-10（Correo del Sur当日报道+ANF次日「ayer」表述+YLB官方FB帖）、UCB San Pablo法学学位与英国MBA（四源）、SOBOCE法律负责人2019-2024（Doria Medina公开声明+Legal 500榜单+评级报告）、2026年6月初去职（ABI/eju.tv/Los Tiempos三源）。关键发现与存疑：(1)任务背景所述「接替Calderón」与来源不符——Visión 360梳理的YLB历任名单显示直接前任为Pablo Nina Terán（2025-08-15就任），Karla Calderón Dávalos任期实为2023年8月至2024年8月，本档案按来源事实记录并在person_relationships中如实标注；(2)任内第7任总裁任期仅约3个月，去职原因未见公开披露；(3)出生日期、出生地、家庭信息未公开，均留空；(4)Wikidata无此人条目，wikidata_qid=null；(5)ABI官网、LinkedIn详情页、Instantáneas、Radio Pio XII、La Razón、Red Uno等站点直读时返回502/403或反爬拦截，相关事实改经可直读来源与检索摘要交叉确认；El Potosí 2026-03-16报道的「确认乌尤尼盐湖为世界最大锂储量」表态因原文页被Cloudflare拦截无法核验，依铁律未收录；(6)completeness_score未达85系客观信息上限所致：无出生/家庭公开资料、无个人联系方式、仅1个可核实社交账号、YLB任期仅3个月且早年履历机构未披露，依「禁止编造」铁律不再补条。"
    }
}

out_path = os.path.join(PERSONS_DIR, "BO-PERSON-000203.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE:", out_path)
print("bytes:", os.path.getsize(out_path))

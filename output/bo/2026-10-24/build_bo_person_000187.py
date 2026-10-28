#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build BO-PERSON-000187 (Luis Fernando Añez Campos) person profile JSON."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000187.json")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

profile = {
    "person_id": "BO-PERSON-000187",
    "wikidata_qid": None,
    "name": "Luis Fernando Añez Campos",
    "name_en": "Luis Fernando Anez Campos",
    "name_zh": "路易斯·费尔南多·阿涅斯·坎波斯",
    "aliases": ["Luis Fernando Áñez Campos"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_date_note": "公开资料（CIEE-SC 2021 年个人简介）仅载明其生于 1979 年，具体月日未见披露，故 birth_date 留空",
    "birth_place": "特立尼达 (Trinidad, Beni)",
    "current_positions": ["玻利维亚国家电力公司副总裁"],
    "education": [
        {
            "institution": "圣西蒙高等大学 (Universidad Mayor de San Simón)",
            "degree": "bachelor",
            "field": "电气工程"
        },
        {
            "institution": "玻利维亚私立大学圣克鲁斯校区 (Universidad Privada de Bolivia - UPB, Santa Cruz)",
            "degree": "other",
            "field": "电力系统"
        }
    ],
    "work_experience": [
        {
            "start_date": "2026-01-28",
            "end_date": None,
            "organization": "玻利维亚国家电力公司 (Empresa Nacional de Electricidad - ENDE Corporación)",
            "org_id": "BO-SOE-003",
            "position": "副总裁"
        },
        {
            "start_date": "2019-11-20",
            "end_date": "2020-11-30",
            "organization": "电力与核技术监管局 (Autoridad de Fiscalización de Electricidad y Tecnología Nuclear - AETN)",
            "org_id": None,
            "position": "执行主任（代理）"
        },
        {
            "start_date": "2020",
            "end_date": None,
            "organization": "圣克鲁斯电气电子工程师协会 (Colegio de Ingenieros Electricistas y Electrónicos de Santa Cruz - CIEE-SC)",
            "org_id": None,
            "position": "会长"
        },
        {
            "start_date": "2018",
            "end_date": "2020",
            "organization": "圣克鲁斯电气电子工程师协会 (Colegio de Ingenieros Electricistas y Electrónicos de Santa Cruz - CIEE-SC)",
            "org_id": None,
            "position": "副会长"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "贝尼省政府 (Gobernación del Departamento del Beni)",
            "org_id": None,
            "position": "农村电气化部门主任"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "贝尼自治大学 (Universidad Autónoma del Beni)",
            "org_id": None,
            "position": "土木工程专业讲师"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "农村电气化合作社 (Cooperativa Rural de Electrificación - CRE)",
            "org_id": None,
            "position": "奇基托斯与拉斯米西奥内斯系统技术处处长"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "农村电气化合作社 (Cooperativa Rural de Electrificación - CRE)",
            "org_id": None,
            "position": "拉斯米西奥内斯系统副经理"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "农村电气化合作社 (Cooperativa Rural de Electrificación - CRE)",
            "org_id": None,
            "position": "孤立系统单元助理"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "农村电气化合作社 (Cooperativa Rural de Electrificación - CRE)",
            "org_id": None,
            "position": "商业管理部大客户处处长"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000186",
            "person_name": "马里奥·拉赖恩·萨阿维德拉 (Mario Larrain Saavedra)",
            "relationship_type": "superior",
            "description": "拉赖恩为 ENDE 临时执行总裁（2025-11-18 由碳氢化合物与能源部长就职），2026-01-28 在科恰班巴正式介绍阿涅斯出任 ENDE 副总裁；两人同属帕斯政府 2025 年 11 月起组建的 ENDE 新领导层"
        }
    ],
    "social_accounts": [
        {
            "platform": "twitter_x",
            "account_name": "Luis Fernando Añez (@LuisferAz)",
            "url": "https://x.com/luisferaz",
            "source": "X 个人主页搜索结果，简介标注 Vicepresidente ENDE Corporación"
        },
        {
            "platform": "facebook",
            "account_name": "Luis Fernando Añez (@luisfernando.anez)",
            "url": "https://www.facebook.com/luisfernando.anez/",
            "source": "Facebook 个人主页（搜索结果确认）"
        },
        {
            "platform": "linkedin",
            "account_name": "Luis Fernando Añez",
            "url": "https://bo.linkedin.com/in/luis-fernando-a%C3%B1ez-a220b4108",
            "source": "LinkedIn 个人主页（搜索结果显示现任副总裁及 AETN 2019-11 至 2020-11 履历）"
        }
    ],
    "family_members": [
        {
            "person_id": None,
            "name": "埃韦特·阿涅斯·胡斯蒂尼亚诺 (Hebert Añez Justiniano)",
            "relationship": "father",
            "industry_or_organization": None
        },
        {
            "person_id": None,
            "name": "何塞法·坎波斯 (Josefa Campos)",
            "relationship": "mother",
            "industry_or_organization": None
        },
        {
            "person_id": None,
            "name": "卡拉·甘巴尔特 (Karla Gambarte)",
            "relationship": "spouse",
            "industry_or_organization": None
        }
    ],
    "political_stances": [
        {
            "date": "2026-07-01",
            "topic": "能源部门转型",
            "stance_content": "公开表示玻利维亚正处于能源部门转型的决定性阶段",
            "source": "https://www.instagram.com/p/DaQoQV8kSzG/"
        }
    ],
    "major_achievements": [
        {
            "date": "2019-11-20",
            "achievement": "经碳氢化合物与能源部第 186/2019 号部长决议任命为电力与核技术监管局（AETN）代理执行主任，其后经 2020 年 2 月、5 月、8 月三次部长决议批准留任",
            "organization": "电力与核技术监管局 (AETN)"
        },
        {
            "date": "2026-01-28",
            "achievement": "在科恰班巴被正式介绍出任国家电力公司（ENDE Corporación）副总裁，加入公司执行层",
            "organization": "玻利维亚国家电力公司 (ENDE Corporación)"
        },
        {
            "date": "2026-01-30",
            "achievement": "与执行总裁拉赖恩一同获玻利维亚工程师协会科恰班巴分会（SIB Cochabamba）表彰",
            "organization": "玻利维亚工程师协会科恰班巴分会 (SIB Cochabamba)"
        }
    ],
    "biography_summary": "路易斯·费尔南多·阿涅斯·坎波斯（Luis Fernando Añez Campos），1979 年生于玻利维亚贝尼省特立尼达市，玻利维亚电力行业资深工程师。毕业于科恰班巴圣西蒙高等大学电气工程专业，后在圣克鲁斯玻利维亚私立大学（UPB）修读电力系统研究生课程。早年执教于贝尼自治大学土木工程系，曾任贝尼省政府农村电气化部门主任，并在农村电气化合作社（CRE）历任奇基托斯与拉斯米西奥内斯系统技术处处长、拉斯米西奥内斯系统副经理、大客户处处长等职。2019 年 11 月至 2020 年 11 月出任电力与核技术监管局（AETN）代理执行主任；2018 至 2020 年任圣克鲁斯电气电子工程师协会（CIEE-SC）副会长，2020 年起任会长。2026 年 1 月 28 日经 ENDE 执行总裁拉赖恩正式介绍出任国家电力公司（ENDE Corporación）副总裁，成为帕斯政府 2025 年 11 月组建的 ENDE 新领导层核心成员。已婚，妻子卡拉·甘巴尔特，育有四名子女；其父于 2026 年 5 月去世。",
    "family_note": "父母为何塞法·坎波斯与埃韦特·阿涅斯·胡斯蒂尼亚诺，有四名兄弟姐妹（Carlos Humberto、Daniela Inés、Heber、Ana Valeria）。妻子卡拉·甘巴尔特（Karla Gambarte），育有四名子女（María Fernanda、Karel、Flavia、Luis Fernando，仅知名、未获全名，按规则未单列条目）。父亲埃韦特·阿涅斯·胡斯蒂尼亚诺于 2026 年 5 月去世（ENDE 子公司及相关机构 2026-05-18 发布唁函）。",
    "profile": {
        "source_url": "https://www.ende.bo/public/imgs/personal-ejecutivo/luis.fernando.añez.jpeg",
        "local_path": "photos/BO-PERSON-000187.jpg"
    },
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": ["official_website", "news_search", "web_search", "social_media", "other"],
        "notes": "核心生平（出生、父母、兄弟姐妹、配偶子女、教育、CRE/贝尼省政府/贝尼自治大学经历、CIEE-SC 职务）来自 CIEE-SC 官方 Facebook 专页 2021-04-07 发布的个人简介，并与多民族宪法法院判决 SCP 0364/2025-S4（2025-04-28，Pixi Legal 收录）交叉验证：AETN 代理执行主任任期 2019-11-20（部长决议 RM 186/2019）至 2020-11-30；该判决另载 2022-02 AETN 曾对其启动内部行政惩戒程序（sumario administrativo interno），其 2023 年以主持权限为由提起宪法保护之诉，本档案仅记录事实。2025-11-18 能源部长梅迪纳塞利就职 6 名当局的 Opinión 报道仅含拉赖恩（ENDE 临时执行总裁），未列阿涅斯；IBNORCA 2025-11-27 帖文（玻利维亚能源委员会 2025-11-19 会议）祝贺阿涅斯「新任务」，与任务背景所述 2025 年 11 月进入 ENDE 新领导层一致，但未见直接列名其董事职务的公开报道，故副总裁起始日采用 2026-01-28（ENDE 官方 X 账号及多家来源报道）。出生仅知年份，birth_date 留空。社交媒体 6 平台扫描：确认 X（@LuisferAz）、Facebook（luisfernando.anez）、LinkedIn 三个账号；Instagram、TikTok、YouTube 未找到其个人账号。2026-07-01 公开表态「玻利维亚正处于能源部门转型的决定性阶段」。AETN、CRE、CIEE-SC、贝尼自治大学、UPB 均未收录入 _name_index.json，org_id 一律为 null。",
        "quotes": [
            {
                "title": "CONOCIENDO A NUESTRO DIRECTORIO Ing. Luis Fernando Añez Campos - Colegio de Ingenieros Electricistas y Electrónicos de Santa Cruz (Facebook)",
                "url": "https://www.facebook.com/cieesantacruz/posts/conociendo-a-nuestro-directorioing-luis-fernando-a%C3%B1ez-camposnacido-en-la-ciudad-/3931283803584560/"
            },
            {
                "title": "Ministro de Hidrocarburos posesiona a 6 autoridades; Mario Larraín es el presidente de ENDE - Opinión (2025-11-18)",
                "url": "https://www.opinion.com.bo/pais/ministro-hidrocarburos-posesiona-6-autoridades-mario-larrain-es-presidente-ende/20251118174631983804.html"
            },
            {
                "title": "Sentencia Constitucional Plurinacional 0364/2025-S4 (Luis Fernando Añez Campos c/ AETN) - Pixi Legal",
                "url": "https://www.pixilegal.com/sentencias/tcp-0364-2025-s4-sala-cuarta-especializada-ref-current-212184"
            },
            {
                "title": "NÓMINA DE AUTORIDADES - ENDE Corporación",
                "url": "https://www.ende.bo/nomina-autoridades"
            },
            {
                "title": "MATKOVIC NO ES EL UNICO CRUCENO EN LA NUEVA CUPULA DE ENDE - Sol de Pando / Cabildeo Digital (2026-07)",
                "url": "https://www.cabildeodigital.com/2026/07/matkovic-no-es-el-unico-cruceno-en-la.html"
            },
            {
                "title": "ENDE Corporación on X: presentación del nuevo vicepresidente Luis Fernando Añez Campos (2026-01-28)",
                "url": "https://x.com/ENDECORPORACION/status/2016593106783605002"
            },
            {
                "title": "Ejecutivos de ENDE Corporación reciben reconocimientos de la SIB Cochabamba - ENDE (2026-01-30)",
                "url": "https://www.ende.bo/noticia/noticia/1001"
            },
            {
                "title": "Luis Fernando Añez - Vicepresidente de ENDE | Energy Executive - LinkedIn",
                "url": "https://bo.linkedin.com/in/luis-fernando-a%C3%B1ez-a220b4108"
            },
            {
                "title": "LUIS FERNANDO AÑEZ: Bolivia atraviesa una etapa decisiva para la transformación de su sector energético - Instagram (2026-07-01)",
                "url": "https://www.instagram.com/p/DaQoQV8kSzG/"
            },
            {
                "title": "Hebert Añez Justiniano Q.E.P.D. - condolencias (Instagram, 2026-05-18)",
                "url": "https://www.instagram.com/p/DYfad38GvF3/"
            }
        ]
    }
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)

print("written:", OUT)
print("top-level keys:", len(profile.keys()))
print("work_experience:", len(profile["work_experience"]))
print("education:", len(profile["education"]))
print("family_members:", len(profile["family_members"]))
print("social_accounts:", len(profile["social_accounts"]))
print("political_stances:", len(profile["political_stances"]))
print("major_achievements:", len(profile["major_achievements"]))
print("person_relationships:", len(profile["person_relationships"]))
print("quotes:", len(profile["collection_meta"]["quotes"]))
print("bio_len:", len(profile["biography_summary"]))

# -*- coding: utf-8 -*-
"""Build BO-PERSON-000377 (Lucero Noemí Claros Torrico, Editora Revista OH!, Los Tiempos)."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000377.json")

p = {
    "person_id": "BO-PERSON-000377",
    "wikidata_qid": None,
    "name": "Lucero Noemí Claros Torrico",
    "name_en": "Lucero Claros",
    "name_zh": None,
    "aliases": [
        "Lucero Claros",
        "Lucero N. Claros",
        "Lucero Claros Torrico",
        "Lucero Noemí Claros Torrico",
    ],
    "nationality": "BO",
    "gender": "female",
    "birth_date": None,
    "birth_place": None,
    "contacts": [
        {
            "type": "email",
            "value": "oh@lostiempos-bolivia.com",
            "source": "《OH!》杂志2025-01-26期（总第1.339期）版权页：Editora de OH! 栏下所列编辑部邮箱（职务邮箱，非个人专用）",
        },
        {
            "type": "email",
            "value": "clarostorricolucerito@gmail.com",
            "source": "圣西蒙大学（UMSS）2020年 Coursera 计划受理注册公开名单 PDF（第3021条：LUCERO NOEMÍ CLAROS TORRICO）",
        },
    ],
    "current_positions": [
        "《时报》报社《OH!》杂志主编"
    ],
    "education": [
        {
            "institution": "圣西蒙大学 (Universidad Mayor de San Simón)",
            "degree": "bachelor",
            "field": "社会传播",
            "start_date": None,
            "end_date": None,
            "source": "LinkedIn 公开主页（Lic. en Comunicación Social / Periodista，Universidad Mayor de San Simón，Cochabamba）",
            "note": "学历信息主要来自 LinkedIn 自述；UMSS 2020年 Coursera 计划受理注册公开名单（第3021条 LUCERO NOEMÍ CLAROS TORRICO）佐证其与该校的关联；入学与毕业年份不详。",
        }
    ],
    "work_experience": [
        {
            "organization": "《时报》报社 (Los Tiempos)",
            "org_id": "BO-MEDIA-002",
            "position": "多媒体记者",
            "start_date": "2019-05",
            "end_date": None,
            "is_current": "false",
            "description": "以摄影、摄像加文字的多媒体形式为《时报》做现场报道。2019—2020年间《时报》官方 X 账号（@LosTiemposBol）与官方 Facebook（lostiemposbol1）发布的大量科恰班巴现场图片/视频报道均以「Lucero Claros - LT」署名，题材包括2019年11月玻利维亚危机期间的抗议与警察骚乱、2020年新冠疫情期间归国人员隔离、儿童滑轮车赛、Tiquipaya 儿童村等；2025年仍以「Lucero Claros - LT」署名拍摄 Fexco 2025 无人机秀等视频。",
            "source": "https://bo.linkedin.com/in/luceroclaros",
            "start_date_note": "LinkedIn 载「Periodista Multimedia de Los Tiempos, may 2019 — actualidad」；《时报》官网作者页（node/454720）创建于2019-04-13，与入职时间吻合；2019—2020年官方社媒署名报道证实其在岗。",
            "end_date_note": "现官方 Staff 名录仅以其现任职务「Editora Revista OH!」列名；LinkedIn 个人页仍将「多媒体记者」条目标注为「至今」，是否兼任不详。",
        },
        {
            "organization": "《时报》报社《OH!》杂志 (Revista OH!, Los Tiempos)",
            "org_id": "BO-MEDIA-002",
            "position": "《OH!》杂志主编",
            "start_date": "2024",
            "end_date": None,
            "is_current": "true",
            "description": "负责编辑《时报》每周日随报发行的《OH!》生活时尚杂志及其平面与新媒体内容（@revistaoh_bo 的 Instagram/Facebook/TikTok 视频亦以其署名监制），署名报道涵盖旅行、社会、文化、健康等题材。现任职务由多个独立来源交叉证实：《时报》官网 Staff 名录「Editora Revista OH!: Lucero Claros」；2025-01-26 第1.339期《OH!》版权页「Editora de OH!: Lucero Noemí Claros Torrico」（检索线索显示2025年上半年多期版权页同名在任）；LinkedIn 自述「2024年接受挑战编辑一份全国发行的周日杂志并提升其影响力」；ZoomInfo 名录「Editora Revista OH at Los Tiempos」。",
            "source": "https://www.lostiempos.com/staff",
            "start_date_note": "LinkedIn 自述2024年起接任该职；至迟2025年1月（第1.339期版权页）已在任，确切上任月份不详。",
        },
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000371",
            "person_name": "卡蒂乌斯卡·巴斯克斯 (Katiuska Vásquez)",
            "relationship_type": "superior",
            "description": "Vásquez 任《时报》编辑部主任（Jefa de Redacción），是 Claros 在编辑部架构中的直接上级；2025-01-26《OH!》版权页上 Vásquez 署名位次列于主编 Claros 之前。",
            "source": "https://www.lostiempos.com/sites/default/files/edicion_online/oh_webb_26_enero_2025.pdf",
        },
        {
            "person_id": "BO-PERSON-000370",
            "person_name": "何塞·玛丽亚·雷耶斯·加西亚 (José María Reyes García)",
            "relationship_type": "superior",
            "description": "Reyes García 任《时报》董事会主席（Presidente del Directorio），Claros 为该报《OH!》杂志主编，二人同列官网 Staff 管理层名录。",
            "source": "https://www.lostiempos.com/staff",
        },
        {
            "person_id": "BO-PERSON-000698",
            "person_name": "米格尔·迪亚斯·科西奥 (Miguel Díaz Cossío)",
            "relationship_type": "superior",
            "description": "Díaz Cossío 任《时报》报媒集团总经理（Gerente General），在2025-01-26《OH!》版权页署名位次先于主编 Claros。",
            "source": "https://www.lostiempos.com/sites/default/files/edicion_online/oh_webb_26_enero_2025.pdf",
        },
        {
            "person_id": "BO-PERSON-000374",
            "person_name": "鲁迪·奥雷利亚纳 (Ruddy Orellana)",
            "relationship_type": "colleague",
            "description": "Orellana 任《时报》数字主编（Editor Digital），与 Claros 同列官网 Staff 管理层名录。",
            "source": "https://www.lostiempos.com/staff",
        },
        {
            "person_id": None,
            "person_name": "布丽萨·马里亚卡·贝拉斯科 (Brisa Mariaca Velasco)",
            "relationship_type": "subordinate",
            "description": "Mariaca 为《OH!》杂志记者（Periodistas），2025-01-26版权页列于主编 Claros 麾下编辑团队。",
            "source": "https://www.lostiempos.com/sites/default/files/edicion_online/oh_webb_26_enero_2025.pdf",
        },
        {
            "person_id": None,
            "person_name": "达拉·卡卢斯特罗·罗萨斯 (Dara Calustro Rosas)",
            "relationship_type": "subordinate",
            "description": "Calustro 为《OH!》杂志记者（Periodistas）；同期版权页报道预告显示其曾获奖学金赴华交流（becada en China）。",
            "source": "https://www.lostiempos.com/sites/default/files/edicion_online/oh_webb_26_enero_2025.pdf",
        },
        {
            "person_id": None,
            "person_name": "苏萨娜·古铁雷斯·科雷亚 (Susana Gutiérrez Correa)",
            "relationship_type": "associate",
            "description": "Gutiérrez 为《日报》（El Diario）编辑；2026年7月与 Claros 同为玻利维亚仅有的两名媒体代表，赴华参加「全球南方媒体研讨会：相聚西藏」。",
            "source": "https://www.lostiempos.com/oh/actualidad/20260824/tiempos-medios-latinoamericanos-participan-taller-comunicacion-del-sur-global",
        },
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Lucero Claros",
            "url": "https://bo.linkedin.com/in/luceroclaros",
            "source": "Web 检索命中（bo.linkedin.com）；个人页内容（UMSS 学历、2019年5月入职《时报》、2024年起编辑周日刊、常驻科恰班巴）与官网 Staff 页、版权页等独立来源交叉吻合，判定为本人。",
        }
    ],
    "family_members": [],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2025-06-07",
            "achievement": "获圣克鲁斯私立大学（UPSA）颁发的「国际数字新闻计划」（Programa Internacional de Periodismo Digital）结业证书（Acreditta 数字认证，认证技能涵盖数字新闻、社交媒体运营、人工智能、区块链、数据核实、品牌塑造与 storytelling 等）。",
            "organization": "圣克鲁斯私立大学 (Universidad Privada de Santa Cruz de la Sierra, UPSA)",
        },
        {
            "date": "2025-06",
            "achievement": "其主编的《OH!》杂志在圣西蒙大学传播学系主办的第三届「图纳里金奖」（Premios Tunari de Oro a la Excelencia en Comunicación，时隔17年重启，2025年6月颁奖，评选基于150余名传播学学生问卷）上获评「最佳副刊」（mejor suplemento de variedades）。",
            "organization": "圣西蒙大学传播学系 (Carrera de Ciencias de la Comunicación, UMSS)",
        },
        {
            "date": "2026-07",
            "achievement": "应中国国务院新闻办公室与中国驻玻利维亚大使馆邀请，作为玻利维亚仅有的两名媒体代表之一（《时报》代表）赴北京、拉萨、成都参加「全球南方媒体研讨会：相聚西藏」（Global South Media Workshop: Meet in Xizang），与阿根廷、巴西、墨西哥、智利、秘鲁六国媒体代表交流，并系统采写四川、西藏题材特稿。",
            "organization": "全球南方媒体研讨会 (Global South Media Workshop: Meet in Xizang)",
        },
    ],
    "biography_summary": "卢塞罗·诺埃米·克拉罗斯·托里科（Lucero Noemí Claros Torrico，媒体署名 Lucero N. Claros）是玻利维亚科恰班巴主流大报《时报》（Los Tiempos）旗下《OH!》周日刊杂志的主编（Editora de la Revista OH!）。她自2019年5月起以多媒体记者身份加入《时报》，从事摄影、摄像与文字报道，2019—2020年间《时报》官方 X 与 Facebook 账号的大量科恰班巴现场报道均以「Lucero Claros - LT」署名。2024年起她接手编辑这份全国发行的周日杂志，《时报》官网 Staff 名录与2025年各期《OH!》版权页均列其为「Editora de OH!」。任内《OH!》于2025年6月获圣西蒙大学传播学系第三届「图纳里金奖」最佳副刊（mejor suplemento de variedades）奖；她本人于2025年6月获圣克鲁斯私立大学（UPSA）「国际数字新闻计划」结业证书。2026年7月，她应中国国务院新闻办公室与中国驻玻利维亚大使馆邀请，作为玻利维亚两家媒体代表之一赴北京、拉萨、成都参加「全球南方媒体研讨会」，随后在《OH!》发表四川大熊猫、三星堆与西藏旅行特稿并随团摄影。她毕业于圣西蒙大学（UMSS）社会传播专业，常驻科恰班巴。",
    "position_note": "现任职务「《OH!》杂志主编（Editora Revista OH!）」由四个独立来源交叉证实：(1)《时报》官网 Staff 名录（Editora Revista OH!: Lucero Claros，同页列 Presidenta del Directorio 为 José María Reyes García=BO-PERSON-000370、Jefa de Redacción 为 Katiuska Vásquez=BO-PERSON-000371、Editor Digital 为 Ruddy Orellana=BO-PERSON-000374）；(2) 2025-01-26《OH!》第1.339期版权页 PDF 直读「Editora de OH!: Lucero Noemí Claros Torrico」；(3) LinkedIn 自述2024年起编辑周日刊；(4) ZoomInfo「Editora Revista OH at Los Tiempos」。",
    "name_note": "全名 Lucero Noemí Claros Torrico 由三个独立来源确认：《OH!》2025-01-26期版权页；Acreditta 数字证书（2025-06-07）；UMSS 2020年 Coursera 受理名单（第3021条）。报道署名为「Lucero N. Claros」（N. 即 Noemí），官网作者页与 Staff 页均用「Lucero Claros」。玻利维亚人名惯例中父姓在前（Claros），母姓 Torrico。",
    "identity_note": "同名消歧：Instagram 演员兼模特账号 @luceroclaros（约900粉，MA @lookmgmt）、TikTok @claroslucero 与 @luceroclaros5、YouTube @LuceroClaros-g7d 等同名社交账号均无法证实为本人，不采纳；已建档的 Claudia Stacy Peña Claros（BO-PERSON-000102）与 Lissa Claros（BO-PERSON-000501）为不同个体；玻利维亚包装企业 Camex 的「Miguel Lucero C.」无关。检索中未发现科恰班巴政界同名人物，未见混淆个案。",
    "social_accounts_note": "六平台扫描（Facebook/X/Instagram/LinkedIn/TikTok/YouTube）：唯一可确证为本人的账号为 LinkedIn（bo.linkedin.com/in/luceroclaros）。X（@LosTiemposBol）、Facebook（lostiemposbol1）、TikTok（@lostiemposbol、@revistaoh_bo）上的「Lucero Claros - LT/OH」署名均属报社及杂志官方账号的图文视频署名，非其个人账户，故不计入 social_accounts；Instagram/TikTok/YouTube 上的同名个人账号（见 identity_note）均无法证实为本人，不采纳。",
    "work_note": "LinkedIn 经验栏另载「Profesional de la comunicación」「Content Manager / Equipo…」等条目，因检索摘要信息不完整且无法读取全文核实细节，未单列入 work_experience。",
    "education_note": "无毕业年份与院校系所明细；「Lic. en Comunicación Social」（社会传播学士）为 LinkedIn 自述，UMSS 2020年 Coursera 名单仅佐证校方关联，不构成学位证明，故 degree 记 bachelor 并在 note 说明证据强度。",
    "family_note": "未检索到任何家庭成员的公开信息，family_members 留空。",
    "birth_note": "出生日期、出生地均未见于任何公开来源（作者页无简介栏，LinkedIn 公开页不可直读），置 null。",
    "name_zh_note": "多轮中文检索（维基百科、华文媒体）未见该人物的既有标准中文译名，name_zh 置 null；biography_summary 中「卢塞罗·诺埃米·克拉罗斯·托里科」仅为行文用音译。",
    "nationality_note": "自2019年起持续以玻利维亚科恰班巴《时报》记者/主编身份公开活动；2026年7月经《时报》报道作为「玻利维亚代表」赴华参加媒体研讨会，国籍按任务参数记为 BO，未见双重国籍信息。",
    "collection_meta": {
        "collection_date": "2026-10-26",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "news_search",
            "web_search",
            "social_media",
            "other"
        ],
        "notes": "关键结论与来源：(1) 身份与全名：Lucero Noemí Claros Torrico 由《OH!》2025-01-26期版权页 PDF（直读）、Acreditta 证书页（直读，2025-06-07 UPSA「国际数字新闻计划」结业证书）、UMSS 2020年 Coursera 受理名单 PDF（第3021条）三源确认；署名 Lucero N. Claros 经官网作者页及2025—2026年多篇《OH!》署名报道直读核实。(2) 现职《OH!》杂志主编：官网 Staff 页（直读）+ 版权页 + LinkedIn + ZoomInfo 四源交叉。(3) 履历：2019-05 入职《时报》任多媒体记者（LinkedIn；作者页2019-04-13创建；2019—2020年 @LosTiemposBol 多条署名帖文、lostiemposbol1 视频署名佐证）→ 2024年起任《OH!》主编（LinkedIn 自述；至迟2025-01 版权页在任）。(4) 成就：2025-06-07 UPSA 证书（Acreditta 直读）；2025-06《OH!》获图纳里金奖最佳副刊（《时报》2025-06-30 报道直读，奖项属杂志而非个人）；2026-07 全球南方媒体研讨会玻方代表（《时报》2026-08-24 报道直读：「Por parte de Bolivia, integraron la delegación Lucero Noemí Claros Torrico, periodista y editora de Los Tiempos…」）。(5) 同名消歧与六平台社媒扫描结论见 identity_note、social_accounts_note；LinkedIn 直读受阻（999/451），内容经多组搜索摘要交叉并与其他官方来源吻合后采信。(6) 出生日期、出生地、家庭成员、个人社交账号（除 LinkedIn）、政治立场均未查到，相应字段留空；Wikidata 检索无条目，wikidata_qid 置 null。(7) completeness_score 受中层编辑公开信息客观限制（评分器对 birth_date/birth_place/name_zh/family/political 等不可得字段同等计权），已以可核实信息（2段任职、7项关系、3项成就、2个联系渠道、1个社媒账号）尽力充实。",
        "quotes": [
            {
                "title": "Staff | Los Tiempos（官网管理层名录：Editora Revista OH! — Lucero Claros）",
                "url": "https://www.lostiempos.com/staff"
            },
            {
                "title": "Lucero N. Claros | Los Tiempos（官网作者页，含2025—2026年《OH!》署名报道存档）",
                "url": "https://www.lostiempos.com/autor/lucero-n-claros"
            },
            {
                "title": "《OH!》杂志第1.339期（2025-01-26）版权页 PDF：Editora de OH! — Lucero Noemí Claros Torrico",
                "url": "https://www.lostiempos.com/sites/default/files/edicion_online/oh_webb_26_enero_2025.pdf"
            },
            {
                "title": "Los Tiempos y medios latinoamericanos participan en el taller de comunicación del Sur Global（2026-08-24，玻方代表署名）",
                "url": "https://www.lostiempos.com/oh/actualidad/20260824/tiempos-medios-latinoamericanos-participan-taller-comunicacion-del-sur-global"
            },
            {
                "title": "Sichuan: pandas gigantes, el misterio de la civilización Sanxingdui…（2026-08-10，署名 Lucero N. Claros，图片署名 Lucero Claros）",
                "url": "https://www.lostiempos.com/oh/actualidad/20260810/sichuan-pandas-gigantes-misterio-civilizacion-sanxingdui-ingenieria"
            },
            {
                "title": "Vuelven los premios Tunari de Oro: la revista OH! es reconocida como mejor suplemento（2025-06-30）",
                "url": "https://www.lostiempos.com/oh/actualidad/20250630/vuelven-premios-tunari-oro-revista-oh-es-reconocida-como-mejor-suplemento"
            },
            {
                "title": "Asociación Kuska, el arte de unir fragmentos para empoderar y renacer（2025-10-06，署名报道）",
                "url": "https://www.lostiempos.com/oh/actualidad/20251006/asociacion-kuska-arte-unir-fragmentos-empoderar-renacer"
            },
            {
                "title": "Acreditta 数字证书：PROGRAMA INTERNACIONAL DE PERIODISMO DIGITAL — LUCERO NOEMI CLAROS TORRICO（UPSA，2025-06-07）",
                "url": "https://www.acreditta.com/credential/3bfa5c82-46a9-4f70-8d2a-7f9a09e02fb7"
            },
            {
                "title": "UMSS 2020年 Coursera 计划受理注册名单 PDF（第3021条：LUCERO NOEMÍ CLAROS TORRICO）",
                "url": "https://www.umss.edu.bo/wp-content/uploads/2020/06/Registros-Aceptados-Coursera-UMSS.pdf"
            },
            {
                "title": "LinkedIn 公开主页：Lucero Claros — Lic. en Comunicación Social / Periodista（UMSS，Cochabamba）",
                "url": "https://bo.linkedin.com/in/luceroclaros"
            },
            {
                "title": "ZoomInfo：Lucero Claros — Editora Revista OH at Los Tiempos",
                "url": "https://www.zoominfo.com/p/Lucero-Claros/8837411552"
            },
            {
                "title": "X @LosTiemposBol 署名帖（2020-03-24，Villa Suramericana 归国人员报道，图片署名 Lucero Claros - LT）",
                "url": "https://x.com/LosTiemposBol/status/1242833322608394240"
            },
            {
                "title": "TikTok @revistaoh_bo：Miss Cochabamba 2025 视频（监制署名 Lucero Claros - OH）",
                "url": "https://www.tiktok.com/@revistaoh_bo/video/7480775943779355909"
            }
        ]
    },
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(p, f, ensure_ascii=False, indent=2)
print("written:", OUT)
print("bytes:", os.path.getsize(OUT))

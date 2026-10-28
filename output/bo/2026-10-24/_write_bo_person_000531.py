# -*- coding: utf-8 -*-
"""Build BO-PERSON-000531 (Dila Tatiana Justiniano Vélez) person profile JSON."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000531.json")

profile = {
    "person_id": "BO-PERSON-000531",
    "wikidata_qid": None,
    "name_zh": None,
    "name": "Dila Tatiana Justiniano Vélez",
    "name_en": "Dila Tatiana Justiniano Velez",
    "aliases": ["Tatiana Justiniano Vélez", "Tatiana Justiniano Velez", "Dila Justiniano"],
    "nationality": "BO",
    "gender": "female",
    "birth_date": None,
    "birth_place": None,
    "contacts": [],
    "current_positions": ["玻利维亚天然气运输公司 (Gas TransBoliviano S.A.) 行政与财务总经理"],
    "education": [],
    "work_experience": [
        {
            "organization": "玻利维亚天然气运输公司 (Gas TransBoliviano S.A.)",
            "org_id": "BO-CORP-010",
            "position": "行政与财务总经理",
            "start_date": None,
            "end_date": None,
            "is_current": "true",
            "description": "与总经理 Katya Mirna Diederich Kuscevic、运营总经理 Rodrigo Ampuero Coimbra 同列公司高管名录，负责行政与财务条线。GTB 为 YPFB 子公司控股的玻利维亚-巴西天然气主干管道（长约 557 公里）运营商。其 LinkedIn 档案头衔另显示曾任或兼任「代理总经理 (Gerente General a.i.)」，代理起止时间不详。",
            "source": "GTB 官网 gerencia-ejecutiva 页（2026-02 更新，全文直读核验）；bo.linkedin.com 档案（检索摘要）",
        },
        {
            "organization": "利皮西马清洁服务公司 (LIMPISIMA S.R.L.)",
            "org_id": None,
            "position": "创始人兼总经理",
            "start_date": None,
            "end_date": None,
            "description": "总部位于圣克鲁斯-德拉谢拉的清洁服务企业。Red Uno 作者页简介及 2025-12 专栏署名身份均为此职，可能仍持有该业务；履历数据库另载其曾任「La Limpisima Srl」业主总经理 (Gerente Propietaria)。",
            "source": "reduno.com.bo 作者页（全文直读）；bo.linkedin.com 与 aeroleads.com 档案（检索摘要）",
        },
        {
            "organization": "马迪萨分销公司 (Mayoreo y Distribución S.A. - MADISA)",
            "org_id": None,
            "position": "行政与财务总经理",
            "start_date": "2018-08-20",
            "end_date": None,
            "description": "玻利维亚分销企业（NIT 1028703022）。2019-2020 年宪法诉讼记录显示其同时以「全国财务经理 (Gerente Financiera Nacional)」及公司法定代表 (Representante Legal) 身份行事。就任日期出自玻利维亚金融监管局 (ASFI) 登记及玻利维亚证券交易所有人相关重大事项报告。",
            "source": "ASFI 登记卡（检索摘要，原文页直连超时）；Expediente 31957-2019-64-AAC 与 SCP 0563/2020-S3（全文直读）",
        },
        {
            "organization": "利皮杜斯玻利维亚 (Limpidus Bolivia)",
            "org_id": None,
            "position": "授权加盟商（圣克鲁斯）",
            "start_date": None,
            "end_date": None,
            "description": "以 Limpidus 清洁服务品牌授权加盟商 (Franquiciado Autorizado) 身份在圣克鲁斯经营，履历数据库记载为过往经历。",
            "source": "aeroleads.com 档案（检索摘要）",
        },
        {
            "organization": "西内尔希亚企业咨询公司 (Sinergia Asesores de Empresas)",
            "org_id": None,
            "position": "联合创始人",
            "start_date": None,
            "end_date": None,
            "description": "玻利维亚企业咨询/商业服务机构，履历数据库记载其为联合创始人。",
            "source": "aeroleads.com 档案（检索摘要）",
        },
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000529",
            "person_name": "卡佳·米尔娜·迪德里希·库塞维奇 (Katya Mirna Diederich Kuscevic)",
            "relationship_type": "superior",
            "description": "GTB 总经理，官网高管名录中为其直属上级。",
            "source": "GTB 官网 gerencia-ejecutiva 页（2026-02 更新，全文直读核验）",
        },
        {
            "person_id": "BO-PERSON-000530",
            "person_name": "罗德里戈·安普埃罗·科英布拉 (Rodrigo Ampuero Coimbra)",
            "relationship_type": "colleague",
            "description": "GTB 运营总经理，同列公司高管团队。",
            "source": "GTB 官网 gerencia-ejecutiva 页（2026-02 更新，全文直读核验）",
        },
        {
            "person_id": "BO-PERSON-000532",
            "person_name": "鲁道夫·埃内斯托·巴里加·埃斯滕索罗 (Rodolfo Ernesto Barriga Estenssoro)",
            "relationship_type": "colleague",
            "description": "GTB 安全、健康、环境与企业社会责任总监，同列公司高管团队。",
            "source": "GTB 官网 gerencia-ejecutiva 页（2026-02 更新，全文直读核验）",
        },
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Tatiana Justiniano Velez",
            "url": "https://bo.linkedin.com/in/tatiana-justiniano-velez-21346bb4",
            "source": "档案头衔「Gerente General a.i. en Gas TransBoliviano S.A.」及其履历（含 MADISA、LIMPISIMA、Limpidus、Sinergia Asesores）与本人多源公开履历吻合；LinkedIn 反爬致直读失败，要点经多路搜索摘要交叉确认",
        },
        {
            "platform": "other",
            "account_name": "Tatiana Justiniano Vélez",
            "url": "https://www.reduno.com.bo/autor/tatiana-justiniano-velez",
            "source": "Red Uno 新闻网站作者专栏页（全文直读），简介标注「Gerente General LIMPISIMA SRL」",
        },
    ],
    "family_members": [],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2018-08-20",
            "achievement": "出任玻利维亚分销企业 MADISA (Mayoreo y Distribución S.A.) 行政与财务总经理，任命经玻利维亚金融监管局 (ASFI) 登记并作为重大事项报告披露；其后以全国财务经理兼法定代表身份主导公司对外的法律与证券市场事务。",
            "organization": "马迪萨分销公司 (Mayoreo y Distribución S.A. - MADISA)",
        },
        {
            "date": "2025-12",
            "achievement": "在 Red Uno 发表专栏文章《玻利维亚创业的结构性挑战与加强正规化的紧迫性 (Desafíos estructurales del emprendimiento en Bolivia y la urgencia de fortalecer la formalidad)》，基于自身创业经历分析玻利维亚非正规经济与创业生态问题。",
            "organization": "Red Uno 电视台 (Red Uno de Bolivia)",
        },
        {
            "date": "2026",
            "achievement": "出任玻利维亚天然气运输公司 (GTB) 行政与财务总经理，进入公司最高管理团队（截至 2026-02 见于官网高管名录；2025-12 其公开署名身份仍为 LIMPISIMA 总经理，推断就任于 2025 年末至 2026 年初）。",
            "organization": "玻利维亚天然气运输公司 (Gas TransBoliviano S.A.)",
        },
    ],
    "biography_summary": "迪拉·塔蒂亚娜·胡斯蒂尼亚诺·韦莱斯（Dila Tatiana Justiniano Vélez）是玻利维亚女性财务高管与企业家，公开场合多以「Tatiana Justiniano Vélez」名义活动，现任玻利维亚天然气运输公司 (Gas TransBoliviano S.A., GTB) 行政与财务总经理。GTB 为玻利维亚国家石油公司 (YPFB) 子公司控股的管道运营商，运营玻利维亚至巴西边境约 557 公里天然气主干管道，她是公司总经理、运营总经理之下的第三位高管。2018 年 8 月 20 日经玻利维亚金融监管局 (ASFI) 重大事项报告出任分销企业 MADISA（Mayoreo y Distribución S.A.）行政与财务总经理，2019-2020 年间以全国财务经理兼公司法定代表身份见于玻利维亚宪法法院多份诉讼记录。她同时是圣克鲁斯清洁服务企业 LIMPISIMA S.R.L. 创始人兼总经理，曾以 Limpidus 品牌授权加盟商身份经营清洁业务，并联合创办 Sinergia Asesores de Empresas 企业咨询机构，自述拥有逾 25 年财务管理、控制与经营战略经验。2025 年 12 月在 Red Uno 发表关于玻利维亚创业环境与经营正规化的专栏文章。其出生日期、学历与家庭情况未见公开披露。",
    "profile": None,
    "education_note": "公开渠道未检索到其学历信息。存在另一同名为「Tatiana Justiniano de Salinas」的 LinkedIn 档案标注毕业于加布里埃尔·雷内·莫雷诺自治大学 (UAGRM)，但身份归属未获证实，故不录入本档案。",
    "work_note": "职业主线为「企业财务高管 + 清洁行业创业者」双轨：MADISA（2018 起）与 GTB（现任）为受薪高管经历，LIMPISIMA/Limpidus/Sinergia Asesores 为创业经历。GTB 官网 2019 年年报经全文检索未出现其姓名，无法证实其更早加入 GTB。",
    "position_note": "LinkedIn 头衔显示曾任或兼任 GTB「代理总经理 (Gerente General a.i.)」，应为总经理换届时临时代理，代理期间不详；现任总经理 Katya Diederich 早在 2011 年前后即执掌 GTB。",
    "name_zh_note": "未查到任何中文媒体既有译名，name_zh 按规则置 null。「迪拉·塔蒂亚娜·胡斯蒂尼亚诺·韦莱斯」为本项目清单拟定译名，仅已在 BO-CORP-010 组织档案 key_people 中使用。",
    "identity_note": "身份甄别说明：(1) GTB 存在另一 LinkedIn 档案「Tatiana Justiniano de Salinas」（a580927b，标注 GTB 行政与财务总经理、UAGRM 毕业），可能为本人生育后随夫姓的另一档案、同名前任或同名同事，无法证实，未并入本档案；(2) 美国洛杉矶县高等法院 2024 年案件 Justiniano v. Uber Technologies（24CV009318）当事人 Dila Tatiana Justiniano 与本人是否同一人无法核实（Whitepages 显示洛杉矶/伦顿居住记录），按避免误并原则未纳入；(3) LinkedIn 档案 dila-justiniano-39a15b8（Dila Justiniano (Tatiana D.)）同理未采信。",
    "social_accounts_note": "6 项平台扫描结果：LinkedIn 检索到上述高度吻合档案；Facebook 存在多个「Tatiana Justiniano」同名账号但均无法与本人建立可靠关联；Instagram、X/Twitter、TikTok、YouTube 未发现可确证为本人的账号。",
    "collection_meta": {
        "collection_date": "2026-10-26",
        "phase": "phase4_person_profile",
        "data_sources": ["official_website", "government_registry", "news_search", "web_search", "social_media", "other"],
        "notes": "核心事实核验情况：现任职务（GTB 行政与财务总经理）经 GTB 官网 gerencia-ejecutiva 页全文直读核验（页面 2026-02-04 更新），并以 WebFetch 复核名录结构；MADISA 任职经两份玻利维亚宪法法院记录（Expediente 31957-2019-64-AAC、SCP 0563/2020-S3）全文直读交叉验证（法定代表、全国财务经理）；LIMPISIMA 创始人身份经 Red Uno 作者页与专栏全文直读确认；ASFI 登记的 2018-08-20 就任日期及 NIT 来自 ASFI 登记卡与玻交所重大事项报告检索摘要，原文页多次直连超时未能直接核验，置信度中等。LinkedIn 档案因反爬无法直读，履历要点（MADISA/LIMPISIMA/Limpidus/Sinergia/25 年经验/代理总经理头衔）经 AeroLeads 抓取档案与多路搜索摘要交叉确认，属单平台间接来源。completeness_score 约 58（低于 85 目标）：本人物为企业高管而非公众人物，出生日期、出生地、学历、家庭、联系方式等在公开渠道均无记载，education/family_members/contacts 等字段客观无法填充，未作编造；社交媒体仅 LinkedIn 一档可确证。",
        "quotes": [
            {
                "title": "Gerencia Ejecutiva - Gas TransBoliviano S.A. (GTB) 官网高管名录",
                "url": "https://www.gastransboliviano.com.bo/gerencia-ejecutiva",
            },
            {
                "title": "Expediente No 31957-2019-64-AAC（Corrales c/ Justiniano Vélez, Representante Legal de MADISA）- Derechoteca",
                "url": "https://www.derechoteca.com/jurisprudencia-constitucional-boliviana/bolivia-expediente-constitucional-31957-2019-64-aac-fecha-ingreso-2019-11-27/",
            },
            {
                "title": "Sentencia Constitucional Plurinacional 0563/2020-S3（Gerente Financiera Nacional de MADISA）- Juristeca",
                "url": "https://juristeca.com/bo/tcp/sentencias/2020/9/sentencia-constitucional-plurinacional-0563-2020-s3",
            },
            {
                "title": "Tatiana Justiniano Vélez : Últimas noticias - Red Uno 作者页",
                "url": "https://www.reduno.com.bo/autor/tatiana-justiniano-velez",
            },
            {
                "title": "Desafíos estructurales del emprendimiento en Bolivia y la urgencia de fortalecer la formalidad（2025-12-09 专栏全文）- Red Uno",
                "url": "https://www.reduno.com.bo/opinion/desafios-estructurales-del-emprendimiento-en-bolivia-y-la-urgencia-de-fortalecer-la-formalidad-2025129141143",
            },
            {
                "title": "Tatiana Justiniano Velez - Gerente General a.i. en Gas TransBoliviano S.A. - LinkedIn",
                "url": "https://bo.linkedin.com/in/tatiana-justiniano-velez-21346bb4",
            },
            {
                "title": "Tatiana Justiniano Velez Email & Phone Number - AeroLeads 履历档案",
                "url": "https://www.aeroleads.com/in/tatiana-justiniano-velez-21346bb4",
            },
            {
                "title": "ASFI RMI 登记卡 c=53517（Dila Tatiana Justiniano Vélez, 2018-08-20 就任 MADISA）",
                "url": "https://appweb.asfi.gob.bo/Reportes_asp/rmi/tarjeta.asp?c=53517&t=2",
            },
        ],
    },
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE", OUT)
print("bytes:", os.path.getsize(OUT))

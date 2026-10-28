# -*- coding: utf-8 -*-
"""Write person profile BO-PERSON-000273 (José Andrés Abraham Handal, CBN GM). v2"""
import json
import os

OUT_DIR = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24"
OUT_FILE = os.path.join(OUT_DIR, "persons", "BO-PERSON-000273.json")

CBN = "玻利维亚国家啤酒公司 (Cervecería Boliviana Nacional)"

profile = {
    "person_id": "BO-PERSON-000273",
    "wikidata_qid": None,
    "name": "José Andrés Abraham Handal",
    "name_en": "Jose Andres Abraham Handal",
    "name_zh": None,
    "aliases": ["Andrés Abraham", "José Andrés Abraham", "Jose Andres Abraham"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": "拉巴斯 (La Paz)",
    "birth_date_note": "未公开确切出生日期。2025年10月 Management Magazine 报道称其46岁，2026年7月 Trendsetter Bolivia 专访中自述「tengo 47 años」，据此推算约1978-1979年出生。",
    "contacts": [
        {
            "type": "website",
            "value": "http://www.cbn.com.bo/",
            "source": "任职机构官方网站（其执掌的 CBN 官网，作为机构联络渠道）",
        }
    ],
    "current_positions": ["玻利维亚国家啤酒公司总经理"],
    "education": [
        {
            "institution": "玻利维亚天主教大学 (Universidad Católica Boliviana)",
            "degree": "bachelor",
            "field": "经济学",
            "start_date": None,
            "end_date": None,
        },
        {
            "institution": "因斯珀商学院 (Insper)",
            "degree": "master",
            "field": "商务管理",
            "start_date": None,
            "end_date": None,
        },
    ],
    "work_experience": [
        {
            "start_date": "2004",
            "end_date": None,
            "organization": CBN,
            "org_id": "BO-CORP-001",
            "position": "贸易营销分析师",
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": CBN,
            "org_id": "BO-CORP-001",
            "position": "Paceña品牌总经理",
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": CBN,
            "org_id": "BO-CORP-001",
            "position": "全国销售总经理",
        },
        {
            "start_date": "2014",
            "end_date": None,
            "organization": "百威英博 (AB InBev)",
            "org_id": None,
            "position": "非酒精饮料总经理（负责玻利维亚和秘鲁）",
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "百威英博哥伦比亚 (AB InBev Colombia)",
            "org_id": None,
            "position": "商务总监",
        },
        {
            "start_date": "2020-01",
            "end_date": "2021-03",
            "organization": "塞尔韦帕啤酒公司 (Cervepar)",
            "org_id": None,
            "position": "全国销售总监",
        },
        {
            "start_date": "2021-04",
            "end_date": "2023-10",
            "organization": "塞尔韦帕啤酒公司 (Cervepar)",
            "org_id": None,
            "position": "国家负责人（总经理）",
        },
        {
            "start_date": "2023-10",
            "end_date": None,
            "organization": CBN,
            "org_id": "BO-CORP-001",
            "position": "总经理",
        },
    ],
    "person_relationships": [
        {
            "person_id": None,
            "person_name": "蒂亚戈·佩雷拉 (Tiago Pereira Da Costa De Menezes)",
            "relationship_type": "colleague",
            "description": "CBN 前任 Country Head Bolivia（总经理），2023年12月31日卸任；José Andrés Abraham Handal 自2024年1月1日起接任该职（ASFI 官方登记之重大事项公告）。",
        },
        {
            "person_id": None,
            "person_name": "米歇尔·杜克里斯 (Michel Doukeris)",
            "relationship_type": "superior",
            "description": "百威英博（AB InBev）全球首席执行官；CBN 为 AB InBev 玻利维亚子公司。2026年4月 CBN 成立140周年之际杜克里斯到访玻利维亚，与 Abraham Handal 会面并重申集团对玻利维亚的长期投资承诺。",
        },
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "José Andrés Abraham Handal",
            "url": "https://bo.linkedin.com/in/andr%C3%A9s-abraham-handal",
            "source": "LinkedIn 玻利维亚站点检索确认，个人主页显示 Gerente General Cervecería Boliviana Nacional",
        }
    ],
    "family_members": [],
    "political_stances": [
        {
            "date": "2023-11",
            "topic": "走私治理与产业政策",
            "stance_content": "多次公开指出走私是玻利维亚工业及 CBN 面临的最大问题之一：估计国家每年因啤酒走私少征税收约1.18亿美元，国内消费的啤酒中约每10瓶就有2瓶来自走私（主要经阿根廷和巴西边境入境）；主张加强治理以保护民族工业和就业。",
            "source": "El Deber 专访（2023-11-21、2023-12-19）",
        },
        {
            "date": "2026-07",
            "topic": "经济信心与投资环境",
            "stance_content": "认为拉巴斯当时面临的主要挑战是恢复和增强投资、创业的信心；强调企业应通过持续投资、创造就业、强化产业链来回应复杂的经济环境，并以长期视角应对多变的经济形势。",
            "source": "Trendsetter Bolivia 封面专访（2026-07-14）",
        },
    ],
    "major_achievements": [
        {
            "date": "2023-10",
            "achievement": "获任命为玻利维亚最大私营饮料企业 CBN 总经理（Country Head Bolivia），2024年1月1日正式就任，从巴拉圭子公司负责人回归祖国执掌其职业生涯起步的公司。",
            "organization": CBN,
        },
        {
            "date": "2026-05",
            "achievement": "在 MERCO（企业声誉监测机构）2025-2026 年度玻利维亚最佳声誉领导者排行榜中上升15位至第7名，首次进入前十（执掌 CBN 不到3年）；同期 CBN 连续第十年位居玻利维亚企业声誉排行榜（MERCO Empresas）第一。",
            "organization": CBN,
        },
        {
            "date": "2026",
            "achievement": "其执掌下 CBN 在公司成立140周年之际再度获评 Great Place to Work 玻利维亚第一（500人以上企业类别）；CBN 亦为玻利维亚纳税额最高的私营企业。",
            "organization": CBN,
        },
        {
            "date": "2026",
            "achievement": "任内持续推进数字化转型与渠道创新：截至2026年，B2B 电商平台 BEES 已连接约95%的直接客户并承载逾90%的销售额；TaDa 连锁零售特许经营体系持续扩张（加盟者中约52%为女性创业者）。",
            "organization": CBN,
        },
    ],
    "biography_summary": "José Andrés Abraham Handal，玻利维亚企业家，生于拉巴斯，现任玻利维亚最大饮料企业、百威英博（AB InBev）玻利维亚子公司国家啤酒公司（Cervecería Boliviana Nacional, CBN）总经理（Country Head Bolivia）。经济学专业出身，毕业于玻利维亚天主教大学（UCB），后赴巴西因斯珀商学院（Insper）修读商务管理研究生课程（MBA）。2004年加入CBN，从贸易营销分析师起步，历任媒体与消费者关系经理、Paceña品牌总经理、全国销售总经理等职；2014年任百威英博玻利维亚和秘鲁非酒精饮料品类负责人，随后外派哥伦比亚任商务总监，2020年1月调任巴拉圭Cervepar全国销售总监，2021年4月升任国家负责人（总经理）。2023年10月获任命回国执掌CBN，并于2024年1月1日正式就任，接替Tiago Pereira Da Costa de Menezes。任内推动B2B数字平台BEES（连接约95%直接客户、承载逾90%销售额）与TaDa零售连锁扩张，推出Golden、Corona Cero等新品；2026年CBN迎来140周年并连续十年蝉联MERCO企业声誉榜第一，其个人亦于2026年5月首次跻身MERCO玻利维亚最佳声誉领导者前十（第7位）。已婚逾十年，育有两名子女。2018年11月曾因AEMP（玻利维亚企业监管局）第RA/AEMP/DTDCDN/N°126/2018号决议与多名CBN高管一并被处以60日商事行为禁止，该处罚于2019年9月经行政程序最终确定（ASFI官方登记）。",
    "position_note": "就任时间两种口径并存：ASFI（玻利维亚金融监管局）证券市场官方登记显示其作为 CBN Gerente General 的入职日期为2024-01-01，重大事项公告载明自2024年1月1日起接替 Tiago Pereira Da Costa De Menezes 出任 Country Head Bolivia（Gerente General）；其 LinkedIn 主页及玻利维亚媒体报道则显示2023年10月获任（LinkedIn 记录 oct 2023 起任 Gerente General CBN）。本档案工作经历以2023-10为起点记录。",
    "identity_note": "Abraham/Handal 为玻利维亚圣克鲁斯巴勒斯坦裔常见姓氏，注意区分同名者：CBN 现任销售总经理 Juan Pablo Handall Tadic 为另一人（ASFI 登记），与本人物非同一人，现有公开资料亦未见二人亲属关系证据。",
    "family_note": "已婚逾十年（2023年11月接受 Negocios Press 专访时自述），育有两名子女；配偶及子女姓名未公开，故 family_members 不设条目。",
    "social_accounts_note": "社交媒体6项扫描结果：仅核实个人 LinkedIn 账号；未发现经核实的个人 Facebook/X/Instagram/TikTok/YouTube 账号，相关搜索命中均为媒体账号（Trendsetter Bolivia、Management Magazine Bolivia、Nueva Economía）或 CBN 企业账号（X: @CBN_Bolivia、TikTok: @cbnbolivia）。2025年12月曾作为讲者参加 TEDxUPDS Tarija（YouTube 官方频道发布演讲视频）。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "news_search",
            "web_search",
            "social_media",
            "government_registry",
            "official_website",
        ],
        "completeness_score": 68,
        "notes": "数据来源：精读6个独立来源全文（El Deber 2023-11-21 与 2023-12-19 两篇专访、Negocios Press 2023-11-23 专访含个人档案、Management Magazine 2025-10-02 人物报道、Trendsetter Bolivia 2026-07-14 封面专访、economy.com.bo 2026-06-23 报道），经网页直读核验 CBN 官网 2026-05-26 MERCO 新闻，并核验 ASFI 证券市场官方登记页（含2024-01-01就任之重大事项公告与2018年AEMP处罚记录）。关键事实（教育、职业轨迹、就任时间、MERCO排名）均有≥2独立来源。存疑与说明：(1) 出生日期未公开，仅有年龄自述推算1978-1979年生，birth_date置空；(2) name_zh 经中英文检索无既有中文译名，置null；(3) 早期职务表述来源间略有差异（Trade Marketing分析师/Media & CA Manager），已在biography中并列；(4) 就任时间2023-10（LinkedIn/媒体）与2024-01-01（ASFI官方）两说并存，详见position_note；(5) 2026年4月 Bolivian Business「玻利维亚19佳CEO第5位」仅单一来源，未录入major_achievements；(6) 2018年AEMP处罚为信息披露类程序性处罚，事实取自ASFI官方登记，处罚原因细节未见官方展开；(7) completeness_score=68（<85）：受公开信息客观限制——无中文译名、无Wikidata条目、出生日期与家属信息未公开、无个人公开联系方式、无可靠个人肖像图（Trendsetter页面为动态加载无法提取本人照片），故未达85，已达≥65标准。",
        "quotes": [
            {
                "title": "CBN aporta al desarrollo de la industria nacional - El Deber (2023-11-21)",
                "url": "https://eldeber.com.bo/te-puede-interesar/cbn-aporta-al-desarrollo-de-la-industria-nacional_347615/",
            },
            {
                "title": "José Andrés Abraham: «Estamos enfocados en crecer junto con nuestra cadena de valor» - Negocios Press (2023-11-23)",
                "url": "https://negociospress.com.bo/jose-andres-abraham-estamos-enfocados-en-crecer-junto-con-nuestra-cadena-de-valor/",
            },
            {
                "title": "José Andrés Abraham Handal: «La mayor fortaleza de CBN es su gente» - El Deber (2023-12-19)",
                "url": "https://eldeber.com.bo/te-puede-interesar/jose-andres-abraham-handal-la-mayor-fortaleza-de-cbn-es-su-gente_350915/",
            },
            {
                "title": "La Receta del Éxito: José Andrés Abraham Handal y el legado sostenible de CBN - Magazine Management (2025-10-02)",
                "url": "https://www.magazinemanagement.gm-bolivia.com/la-receta-del-exito-jose-andres-abraham-handal-y-el-legado-sostenible-de-cbn/",
            },
            {
                "title": "Andrés Abraham, Gerente General CBN - Trendsetter Bolivia TST Nº 46 (2026-07-14)",
                "url": "https://trendsetterbolivia.com/tst/andres-abraham",
            },
            {
                "title": "Diez años en la cima: CBN mantiene el primer lugar en reputación corporativa en Bolivia - Economy.com.bo (2026-06-23)",
                "url": "https://www.economy.com.bo/articulo/branding-y-rse/diez-anos-cima-cbn-mantiene-primer-lugar-reputacion-corporativa-bolivia/20260623162517022989.html",
            },
            {
                "title": "CBN no deja el trono: 1º en MERCO por diez años y celebrando su 140 aniversario - CBN 官网 (2026-05-26)",
                "url": "https://www.cbn.bo/noticias/cbn-no-deja-el-trono-1o-en-merco-por-diez-anos-y-celebrando-su-140-aniversario/",
            },
            {
                "title": "ASFI - Tarjeta de Registro Cervecería Boliviana Nacional S.A. (官方登记)",
                "url": "https://appweb.asfi.gob.bo/Reportes_asp/rmi/tarjeta.asp?tr=2&c=51818&t=2",
            },
            {
                "title": "José Andrés Abraham Handal - Gerente General Cervecería Boliviana Nacional | LinkedIn",
                "url": "https://bo.linkedin.com/in/andr%C3%A9s-abraham-handal",
            },
        ],
    },
}

os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)

print("WROTE:", OUT_FILE)
with open(OUT_FILE, encoding="utf-8") as f:
    check = json.load(f)
print("person_id:", check["person_id"])
print("name:", check["name"])
print("bio_len:", len(check["biography_summary"]))
print("work_experience:", len(check["work_experience"]))
print("education:", len(check["education"]))
print("achievements:", len(check["major_achievements"]))
print("stances:", len(check["political_stances"]))
print("relationships:", len(check["person_relationships"]))
print("quotes:", len(check["collection_meta"]["quotes"]))

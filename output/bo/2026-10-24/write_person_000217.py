# -*- coding: utf-8 -*-
"""BO-PERSON-000217 David Miranda Saigua 人物画像写入脚本（phase4_person_profile）"""
import json
import os

profile = {
    "person_id": "BO-PERSON-000217",
    "wikidata_qid": None,
    "name": "David Miranda Saigua",
    "name_en": "David Miranda Saigua",
    "name_zh": "达维德·米兰达·赛瓜",
    "aliases": ["David Miranda"],
    "nationality": "BO",
    "gender": "male",
    "contacts": [
        {
            "type": "email",
            "value": "g.tec.min@esm.gob.bo",
            "source": "ESM官网「透明度与人力资源」页面 (esm.gob.bo/transparencia.php)"
        }
    ],
    "current_positions": [
        "穆通钢铁公司矿山技术总经理"
    ],
    "work_experience": [
        {
            "organization": "穆通钢铁公司 (Empresa Siderúrgica del Mutún)",
            "org_id": "BO-SOE-009",
            "position": "矿山技术总经理 (Gerente Técnico de Mina)",
            "start_date": None,
            "end_date": None,
            "is_current": "true",
            "start_date_note": "个人任命日期未见公开报道，任职起始日留空；2026年官网名录及3月、5月公开活动中均以此职务出现",
            "description": "负责国营穆通钢铁公司矿山技术条线管理，代表公司参与产学研合作接待与跨机构技术协调",
            "source": "https://esm.gob.bo/transparencia.php"
        }
    ],
    "education": [
        {
            "institution": "加夫列尔·雷内·莫雷诺自治大学 (Universidad Autónoma Gabriel René Moreno)",
            "degree": "bachelor",
            "field": "土木工程 (Ingeniería Civil)",
            "start_date": None,
            "end_date": None,
            "country": "BO",
            "source": "Scribd工作文档署名「DAVID MIRANDA SAIGUA, INGENIERO CIVIL, UNIVERSIDAD AUTONOMA GABRIEL RENE MORENO」；其Facebook个人资料显示「Studied Civil…」「Works at UAGRM」，并在UAGRM工业电气中心小组以本名发帖，多源相互印证",
            "note": "入学与毕业年份未公开；玻利维亚土木工程师为5年制本科（licenciatura），按枚举取 bachelor"
        }
    ],
    "education_note": "学历经多源交叉印证为UAGRM土木工程专业，但毕业年份与学位证书细节未公开",
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000215",
            "person_name": "阿尔瓦罗·特赫里纳·奥利维拉 (Álvaro Tejerina Olivera)",
            "relationship_type": "superior",
            "description": "ESM执行总裁（临时/interino a.i.），2025年12月底经矿业与冶金部部长主持在拉巴斯宣誓就职，米兰达为其执掌的新一届管理团队成员（矿山技术总经理）"
        },
        {
            "person_id": "BO-PERSON-000216",
            "person_name": "玛丽亚·埃丝特·伊诺霍萨·加西亚 (María Esther Hinojosa García)",
            "relationship_type": "colleague",
            "description": "ESM规划总经理，同属特赫里纳执掌的公司高管团队（见ESM官网高管名录）"
        },
        {
            "person_id": "BO-PERSON-000218",
            "person_name": "法布里西奥·豪尔赫·阿道夫·博纳多纳·基罗加 (Fabricio Jorge Adolfo Bonadona Quiroga)",
            "relationship_type": "colleague",
            "description": "ESM行政财务总经理，同属公司高管团队（见ESM官网高管名录）"
        },
        {
            "person_id": "BO-PERSON-000220",
            "person_name": "加夫列拉·桑切斯·萨拉斯 (Gabriela Sánchez Salas)",
            "relationship_type": "colleague",
            "description": "ESM总稽查长（Fiscal General），同属公司高管团队（见ESM官网高管名录）"
        },
        {
            "person_id": "BO-PERSON-000219",
            "person_name": "罗森贝特·莱梅·马丁内斯 (Rossembert Laime Martínez)",
            "relationship_type": "colleague",
            "description": "ESM钢铁厂总经理（Gerente de Planta Siderúrgica），同属公司高管团队（见ESM官网高管名录）"
        }
    ],
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "David Miranda Saigua",
            "url": "https://www.facebook.com/david.mirandasaigua.1/",
            "source": "Facebook检索命中（姓名完全一致；资料显示居住圣克鲁斯-德拉谢拉、土木工程背景，与本人画像相符；未登录未能核实全部信息）"
        },
        {
            "platform": "youtube",
            "account_name": "David Miranda Saigua (@davidmirandasaigua3010)",
            "url": "https://www.youtube.com/channel/UCA2_nl-pWOPhtBLk8NbNxIA",
            "source": "YouTube频道，频道名与本人姓名完全一致（3个视频）；身份一致性未完全核实"
        }
    ],
    "family_members": [],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2026-03",
            "achievement": "2026年3月7日以矿山技术总经理身份代表ESM，与项目总稽查长、法律顾问共同接待加夫列尔·雷内·莫雷诺自治大学（UAGRM）农业科学学院院长、师生代表团参观穆通钢铁厂，该活动为两机构2026年2月18日签署的机构间合作协议框架下首项活动，旨在促进学生实习、技术支持与联合项目",
            "organization": "穆通钢铁公司 (Empresa Siderúrgica del Mutún)"
        },
        {
            "date": "2026-05",
            "achievement": "以「穆通矿山总经理」身份出席与玻利维亚军事地理研究所（IGM）波多黎各苏亚雷斯地理区（德属赫尔曼·布什省）的跨机构协调会议，就区域技术工作与未来工作协调交换技术意见，服务区域工业化与领土开发",
            "organization": "穆通钢铁公司 (Empresa Siderúrgica del Mutún)"
        }
    ],
    "biography_summary": "达维德·米兰达·赛瓜（David Miranda Saigua），玻利维亚工程师，现任国营企业穆通钢铁公司（Empresa Siderúrgica del Mutún，ESM）矿山技术总经理（Gerente Técnico de Mina），公务邮箱为 g.tec.min@esm.gob.bo。他毕业于圣克鲁斯的加夫列尔·雷内·莫雷诺自治大学（UAGRM）土木工程专业，据其社交与行业资料自述，长期从事工程技术管理、复杂项目的技术指导与行政管理工作。2025年12月底，前阿涅斯临时政府劳动部长阿尔瓦罗·特赫里纳·奥利维拉在罗德里戈·帕斯政府整顿国企矿业板块的背景下，经矿业与冶金部任命出任ESM临时执行总裁；米兰达作为新一届高管团队成员执掌矿山技术条线，与规划总经理伊诺霍萨、行政财务总经理博纳多纳、总稽查长桑切斯、钢铁厂总经理莱梅等同僚共事。2026年3月7日，他代表ESM接待UAGRM农业科学学院师生代表团参观钢厂，落实当年2月18日两校签署的机构间合作协议；2026年5月，又以穆通矿山总经理身份出席与玻利维亚军事地理研究所（IGM）波多黎各苏亚雷斯地理区的跨机构协调会议。其出生日期、籍贯及家庭情况均未见公开报道。",
    "profile": {
        "source_url": None,
        "local_path": None
    },
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "news_search",
            "web_search",
            "social_media"
        ],
        "notes": "数据确认情况：职务「矿山技术总经理 (Gerente Técnico de Mina)」与公务邮箱由ESM官网透明度页面（esm.gob.bo/transparencia.php）直接确认；eju.tv 2026-03-09报道与玻利维亚军事地理研究所（IGM）Instagram官方账号2026-05-21帖子两个独立来源交叉证实其职务及2026年公开活动。学历：Scribd工作文档署名「DAVID MIRANDA SAIGUA, INGENIERO CIVIL, UNIVERSIDAD AUTONOMA GABRIEL RENE MORENO」，与其Facebook资料（Studied Civil、Works at UAGRM）及UAGRM小组本名发帖相互印证，判为UAGRM土木工程背景（毕业年份未公开）。组织背景：ESM为国营钢铁企业（BO-SOE-009），穆通钢铁综合体位于圣克鲁斯省波多黎各苏亚雷斯，2025年2月投产；特赫里纳2025年12月底被任命为临时执行总裁（El Deber 2026-01-02）。存疑与留空：个人任命日期、出生日期、籍贯、家庭信息未公开，相应字段留空；political_stances未检索到任何公开政治表态；Wikidata无个人条目。另检索到玻利维亚工程课程讲师/「Consultora & Constructora DM&SM Srl」负责人「David Miranda Saigua」（结构专业，科恰班巴C.I. 8661474，课程广告中留有手机号），疑为同一人，因无法独立核实其与ESM职务的同一性，未计入正式字段（不采信其个人电话）。Facebook与YouTube账号按姓名精确匹配检索发现，身份一致性未完全核实（已在source字段注明）。name_zh沿用_name_index既有译名「达维德·米兰达·赛瓜」；组织中文译名「穆通钢铁公司」经中文媒体（中国钢铁新闻网、我的钢铁网等）印证。completeness_score说明：本人物为技术岗位高管，无Wikipedia/Wikidata条目，出生信息、家庭、政治立场客观不可得，评分机制中相应权重（education×4、political_stances×4、family_members×3、birth×2、wikidata×2）无法填充，已尽力在可核实范围内填充。",
        "quotes": [
            {
                "title": "Empresa Siderúrgica del Mutún | Transparencia y Recursos Humanos",
                "url": "https://esm.gob.bo/transparencia.php"
            },
            {
                "title": "La Empresa Siderúrgica del Mutún recibió la visita de la Facultad de Ciencias Agrícolas de la Universidad Autónoma Gabriel René Moreno (eju.tv, 2026-03-09)",
                "url": "https://eju.tv/2026/03/la-empresa-siderurgica-del-mutun-recibio-la-visita-de-la-facultad-de-ciencias-agricolas-de-la-universidad-autonoma-gabriel-rene-moreno/"
            },
            {
                "title": "COORDINACIÓN INTERINSTITUCIONAL EN EL MUTÚN — Instituto Geográfico Militar (Instagram, 2026-05-21)",
                "url": "https://www.instagram.com/p/DYnDtnSJUB_/"
            },
            {
                "title": "Posesionan a Álvaro Tejerina como presidente interino de la Siderúrgica Mutún (El Deber, 2026-01-02)",
                "url": "https://eldeber.com.bo/economia/posesionan-alvaro-tejerina-presidente-interino-siderurgica-mutun_1767396446"
            },
            {
                "title": "David Miranda Saigua - Facebook",
                "url": "https://www.facebook.com/david.mirandasaigua.1/"
            },
            {
                "title": "David Miranda Saigua - YouTube",
                "url": "https://www.youtube.com/channel/UCA2_nl-pWOPhtBLk8NbNxIA"
            },
            {
                "title": "Cálculo de Rendimiento de Personal y Mano de Obra (Scribd, 署名 DAVID MIRANDA SAIGUA - INGENIERO CIVIL - UAGRM)",
                "url": "https://es.scribd.com/document/653599522/Calculo-de-Rendimiento-Sde-Pesonal-y-Mano-de-Obra"
            }
        ]
    }
}

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "BO-PERSON-000217.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)

bio_len = len(profile["biography_summary"])
print("written:", out_path)
print("biography_summary length:", bio_len)

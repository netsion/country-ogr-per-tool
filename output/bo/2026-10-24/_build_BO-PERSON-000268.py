# -*- coding: utf-8 -*-
"""Build person profile BO-PERSON-000268 (Jorge Alberto Vargas Rios, BDP Gerente General)."""
import json
import os

OUT = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000268.json"

profile = {
    "person_id": "BO-PERSON-000268",
    "wikidata_qid": None,
    "name": "Jorge Alberto Vargas Rios",
    "name_en": "Jorge Alberto Vargas Rios",
    "name_zh": "豪尔赫·阿尔贝托·巴尔加斯·里奥斯",
    "aliases": ["Jorge Alberto Vargas Ríos", "Jorge Vargas Ríos", "Jorge Vargas"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "current_positions": ["玻利维亚生产发展银行总经理"],
    "contacts": [
        {
            "type": "website",
            "value": "https://www.bdp.com.bo",
            "source": "任职机构BDP官方网站（机构联系渠道，本人无公开个人联系方式）"
        }
    ],
    "education": [
        {
            "institution": "玻利维亚天主教大学 (Universidad Católica Boliviana)",
            "degree": "master",
            "field": "农业经济学"
        },
        {
            "institution": "美利坚大学 (The American University)",
            "degree": "bachelor",
            "field": "国际企业管理"
        }
    ],
    "work_experience": [
        {
            "start_date": "2026-04",
            "end_date": None,
            "organization": "玻利维亚生产发展银行 (Banco de Desarrollo Productivo)",
            "org_id": "BO-FIN-013",
            "position": "总经理"
        },
        {
            "start_date": "2020-10-01",
            "end_date": "2020-12-01",
            "organization": "玻利维亚金融体系监管局 (Autoridad de Supervisión del Sistema Financiero)",
            "org_id": "BO-FIN-002",
            "position": "代理执行总监"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚金融体系监管局 (Autoridad de Supervisión del Sistema Financiero)",
            "org_id": "BO-FIN-002",
            "position": "证券与金融集团受控公司监督总监"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000266",
            "person_name": "豪尔赫·马塞洛·贝拉斯科·图德拉 (Jorge Marcelo Velasco Tudela)",
            "relationship_type": "superior",
            "description": "2026年3月31日由帕斯政府经济与公共财政部任命为BDP董事长，是巴尔加斯·里奥斯的直接上级；其领导下董事会于4月9日批准巴尔加斯·里奥斯出任总经理，两人共同主导BDP「Creciendo Juntas」等项目发布。"
        },
        {
            "person_id": "BO-PERSON-000221",
            "person_name": "马里奥·瓦尔特·雷克纳·平托 (Mario Walter Requena Pinto)",
            "relationship_type": "colleague",
            "description": "雷克纳·平托于2025年11月出任玻利维亚金融体系监管局（ASFI）执行总监，是该行业的监管机构负责人；BDP须向ASFI报告重大人事与经营事项（如巴尔加斯·里奥斯2026年4月的任命即向ASFI通报），两人为监管与被监管机构负责人间的工作关系。"
        },
        {
            "person_id": None,
            "person_name": "阿列尔·埃尔温·萨瓦拉·达维德 (Ariel Erwin Zabala David)",
            "relationship_type": "colleague",
            "description": "萨瓦拉是巴尔加斯·里奥斯在BDP的总经理前任（至少自2024年4月至2025年12月在任，曾主导该行绿色债券发行），2026年4月由巴尔加斯·里奥斯接任。"
        }
    ],
    "political_stances": [
        {
            "date": "2026-04-29",
            "topic": "气候融资与绿色金融",
            "stance_content": "在圣克鲁斯「高水平对话：气候变化适应与减缓」论坛上强调必须将负责任投资与可持续生产相结合，主张BDP作为玻利维亚迈向「绿色与可持续玻利维亚」的执行机构，把国家气候优先事项与国际可持续融资机制对接，并展示该行减排逾15,849吨二氧化碳、年节能115,445兆瓦时等成果。",
            "source": "ABI通讯社报道及La Patria转载（https://lapatria.bo/enfoque-nacional/bdp-presenta-resultados-sobre-cambio-climatico-en-santa-cruz/）"
        },
        {
            "date": "2026-07-23",
            "topic": "女性金融普惠",
            "stance_content": "在「Creciendo Juntas BDP」计划发布时主张通过互助担保链（garantía encadenada）让3至5名女性小组凭集体互信获得融资，并简化审批、消除历史上限制妇女获得信贷的障碍；首期最高8万玻利维亚诺，还款记录良好并参加培训者可再融资至15万、期限延至24个月并获利率下调。",
            "source": "玻利维亚经济与公共财政部新闻稿（https://www.economiayfinanzas.gob.bo/node/22502）"
        },
        {
            "date": "2026-08",
            "topic": "农牧业生产性融资",
            "stance_content": "在AgroTech Bolivia 2026及玻利维亚农业商会（CAO）大会等场合表示，BDP寻求成为玻利维亚生产者的主要战略盟友，主张通过开发银行信贷支持农牧业生产，并与美洲农业合作研究所（IICA）合作推动农业科技数字目录。",
            "source": "CAO玻利维亚农业商会Instagram帖（https://www.instagram.com/p/DccKA-7lLnr/）及IICA Bolivia帖（https://www.instagram.com/p/DbYVS_aHN7q/）"
        },
        {
            "date": "2026-10",
            "topic": "畜牧业可持续融资与风险管理",
            "stance_content": "在「畜牧业金融风险：如何降低」专题小组讨论中分享BDP在拉丁美洲畜牧业可持续融资方面的经验，主张以可持续金融推动畜牧业的气候适应与转型。",
            "source": "Willay tv与Infobo BoliviaFacebook帖（https://www.facebook.com/100066536017927/photos/1469765995251254/）、BDP官方Facebook（https://www.facebook.com/BancoDeDesarrolloProductivo/posts/1534166375404406/）"
        }
    ],
    "major_achievements": [
        {
            "date": "2026-04",
            "achievement": "经BDP董事会2026年4月9日会议决议被任命为总经理（4月10日向ASFI通报备案，4月13日银行官方渠道宣布），在罗德里戈·帕斯政府2026年3月改组BDP领导层后出任这一国有开发银行最高管理职务，接替阿里埃尔·萨瓦拉。",
            "organization": "玻利维亚生产发展银行 (Banco de Desarrollo Productivo)"
        },
        {
            "date": "2026-04-29",
            "achievement": "在圣克鲁斯主办的「高水平对话：气候变化适应与减缓」论坛上代表BDP发布可持续金融成果：累计减排二氧化碳超15,849吨、年节能115,445兆瓦时、年节水460,743立方米、回收处置废弃物近500吨，并介绍2023年发行的玻利维亚证券市场史上首批绿色债券（1.029亿玻利维亚诺）。",
            "organization": "玻利维亚生产发展银行 (Banco de Desarrollo Productivo)"
        },
        {
            "date": "2026-07",
            "achievement": "与董事长贝拉斯科共同主导发布面向女性创业者的「Creciendo Juntas BDP」金融扶持计划，与加拿大Desjardins集团发展国际合作组织（DID）及加拿大全球事务部合作，引入互助担保链、技术援助与数字化转型辅导等创新机制。",
            "organization": "玻利维亚生产发展银行 (Banco de Desarrollo Productivo)"
        },
        {
            "date": "2026",
            "achievement": "以总经理身份担任BDP在绿色气候基金（GCF）的认证实体主要联络人（focal point）：BDP于2024年10月获GCF直接国家实体认证，为玻利维亚直接获取国际气候融资打通渠道；2026年其以「General Manager」身份列名GCF官网认证实体页面。",
            "organization": "玻利维亚生产发展银行 (Banco de Desarrollo Productivo)"
        }
    ],
    "biography_summary": "豪尔赫·阿尔贝托·巴尔加斯·里奥斯（Jorge Alberto Vargas Rios）是玻利维亚金融监管与开发银行体系出身的技术官僚，2026年4月起任国有开发银行玻利维亚生产发展银行（BDP）总经理。他毕业于美国华盛顿美利坚大学国际企业管理专业，并在玻利维亚天主教大学获农业经济学硕士学位。其职业生涯长期服务于玻利维亚金融体系监管局（ASFI），曾任证券与金融集团受控公司监督总监；2020年10月1日经阿涅斯过渡政府任命为ASFI代理执行总监，同年12月1日由雷纳尔多·尤赫拉接任。2025年11月罗德里戈·帕斯就任总统后改组国有机构领导层：2026年3月31日豪尔赫·贝拉斯科·图德拉出任BDP董事长，4月9日董事会批准巴尔加斯·里奥斯出任总经理，接替此前在任的阿里埃尔·萨瓦拉。任内他推动该行绿色金融与气候融资议程（BDP于2024年10月获绿色气候基金认证，他担任主要联络人）、发布面向女性创业者的「Creciendo Juntas BDP」普惠金融计划，并主张发展银行应成为玻利维亚生产者的主要战略盟友。",
    "collection_meta": {
        "phase": "phase4_person_profile",
        "collection_date": "2026-10-25",
        "data_sources": ["official_website", "government_registry", "news_search", "web_search", "social_media"],
        "completeness_score": 0,
        "quotes": [
            {
                "title": "Banco de Desarrollo Productivo - Sociedad Anónima Mixta | Green Climate Fund",
                "url": "https://www.greenclimate.fund/partners/accredited-entities/bdp-sam"
            },
            {
                "title": "BDP PRESENTA 'CRECIENDO JUNTAS' PARA IMPULSAR EL LIDERAZGO ECONÓMICO DE LAS MUJERES | MEFP",
                "url": "https://www.economiayfinanzas.gob.bo/node/22502"
            },
            {
                "title": "Posesionan a cuatro nuevas autoridades del Ministerio de Economía - El País (Tarija)",
                "url": "https://elpais.bo/nacional/20201001_posesionan-a-cuatro-nuevas-autoridades-del-ministerio-de-economia.html"
            },
            {
                "title": "Ministro de Economía y Finanzas Públicas posesiona a cuatro nuevas autoridades - CADECOCRUZ",
                "url": "https://www.cadecocruz.org.bo/index.php?op=200&gr=1&nw=5922"
            },
            {
                "title": "BDP presenta resultados sobre cambio climático en Santa Cruz - La Patria (fuente ABI)",
                "url": "https://lapatria.bo/enfoque-nacional/bdp-presenta-resultados-sobre-cambio-climatico-en-santa-cruz/"
            },
            {
                "title": "Tarjeta de Registro BDP S.A.M. - ASFI",
                "url": "https://appweb.asfi.gob.bo/Reportes_asp/rmi/tarjeta.asp?c=51830&t=2"
            },
            {
                "title": "Reporte Informativo ASFI al 14/04/2026 - Hecho Relevante (designación Gerente General)",
                "url": "https://appweb2.asfi.gob.bo/PaginasPublicas2/VistaHechosRelevantes/VisorDocumentos.aspx?variable1=5d2e5498-a12d-408f-b67c-9588f3c97a9e"
            },
            {
                "title": "#SomosBDPsam | Saludamos y damos la bienvenida a Jorge Alberto Vargas Ríos - BDP Facebook",
                "url": "https://www.facebook.com/BancoDeDesarrolloProductivo/posts/somosbdpsam-saludamos-y-damos-la-bienvenida-a-jorge-alberto-vargas-r%C3%ADos-quien-as/1361364246017954/"
            },
            {
                "title": "Banco de Desarrollo Productivo SAM - LinkedIn (bienvenida Gerencia General)",
                "url": "https://es.linkedin.com/posts/bancodesarrolloproductivo_somosbdpsam-activity-7449568092470501377-uEu9"
            },
            {
                "title": "Ficha NFB CAR - Banco de Desarrollo Productivo S.A.M. (EEFF al 30/09/2026, firma Gerente General)",
                "url": "https://www.bbv.com.bo/Media/Default/Archivos/Fichas/NFB_CAR.pdf"
            },
            {
                "title": "El BDP destaca avances en finanzas sostenibles en el Diálogo sobre Cambio Climático en Santa Cruz - ABI",
                "url": "https://abi.bo/el-bdp-destaca-avances-en-finanzas-sostenibles-en-el-dialogo-sobre-cambio-climatico-en-santa-cruz/"
            },
            {
                "title": "#CNCenAcción reunión con el Director General Ejecutivo a.i. de la ASFI Jorge Vargas Rios - CNC",
                "url": "https://www.facebook.com/cncbol/posts/3688266381226110/"
            },
            {
                "title": "Ivette Espinoza fue posesionada como directora de la ASFI - Red Uno (predecesor Yujra desde 01-12-2020)",
                "url": "https://www.reduno.com.bo/economia/ivette-espinoza-fue-posesionada-como-directora-de-la-asfi-202372117402"
            },
            {
                "title": "Jorge Marcelo Velasco, nuevo presidente del Directorio del BDP - Correo del Sur",
                "url": "https://correodelsur.com/economia/20260401/jorge-marcelo-velasco-nuevo-presidente-del-directorio-del-bdp.html"
            }
        ],
        "notes": "身份核验：多来源交叉确认「Jorge Alberto Vargas Rios」即2026年4月起任BDP总经理的同一人——ASFI登记卡与重大事项报告（2026-04-09董事会任命）、BDP官方Facebook/LinkedIn/Instagram欢迎帖（2026-04-13）、绿色气候基金官网focal point、BDP 2026年7月财务报表及BBV托管文件（2026-09-30）签名栏均一致；其2020年任ASFI代理执行总监的报道（El País/CADECOCRUZ/CNC）姓名与教育背景完全吻合，确认同一人。姓名拼写：监管登记文件（ASFI/GCF/财报）作「Vargas Rios」（无重音），BDP官方社媒及新闻作「Vargas Ríos」，name采用登记拼写并以aliases收录重音变体。name_zh「豪尔赫·阿尔贝托·巴尔加斯·里奥斯」沿用本项目_name_index既定标准音译，未查到玻利维亚华文媒体既有独立译名。ASFI任期截止日2020-12-01系依据Red Uno报道（继任者Yujra自2020-12-01在任）推断，开始日2020-10-01依据El País/CADECOCRUZ报道。2021-2025年经历公开信息缺失（无法确认空白期任职）；出生日期/地点、家庭、个人社交媒体（LinkedIn/Twitter/Facebook/Instagram/TikTok/YouTube六项扫描均无可靠个人账号，Facebook同名账号无法核实为本人）均未查证，相应字段留空。social_accounts为空系因仅能核实BDP机构账号而非其个人账号。completeness_score约67分，未达85：受限于公开披露有限（无出生信息、无个人社媒、2021-2025履历空白），已按规则以可核实信息填充全部可填字段。"
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("written:", OUT)
print("bio length:", len(profile["biography_summary"]))

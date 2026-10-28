# -*- coding: utf-8 -*-
"""Enrich BO-ACAD-013 Universidad Nur profile (phase3_enriched)."""
import json

path = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/orgs/BO-ACAD-013.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

data["basic_info"]["name_zh"] = "努尔大学"
data["basic_info"]["name_en"] = "Nur University"
data["basic_info"]["website"] = "https://www.nur.edu"

data["social_accounts"] = [
    {
        "platform": "facebook",
        "account_name": "UniversidadNURoficial",
        "url": "https://www.facebook.com/UniversidadNURoficial/",
        "source": "official_website (footer) + Facebook search",
    },
    {
        "platform": "instagram",
        "account_name": "universidadnur",
        "url": "https://www.instagram.com/universidadnur/",
        "source": "official_website (footer)",
    },
    {
        "platform": "youtube",
        "account_name": "Universidad NUR Bolivia (UCg7_S3COOpvKoMxnf7qKmBw)",
        "url": "https://www.youtube.com/channel/UCg7_S3COOpvKoMxnf7qKmBw",
        "source": "official_website (footer) + wikidata",
    },
    {
        "platform": "twitter_x",
        "account_name": "universidadnur",
        "url": "https://twitter.com/universidadnur",
        "source": "wikidata",
    },
    {
        "platform": "linkedin",
        "account_name": "Universidad Núr- Santa Cruz - Bolivia",
        "url": "https://bo.linkedin.com/company/universidad-n%C3%BAr-santa-cruz-bolivia",
        "source": "linkedin (search result)",
    },
]

data["digital_assets"] = [
    {
        "name": "Plataforma Virtual NUR",
        "url": "https://cvsc.nur.edu",
        "description": "在线学习管理平台（虚拟校园），支持面授与半面授课程教学。",
        "source": "official_website",
    },
    {
        "name": "Notas y Pagos en Línea",
        "url": "https://notas2.nur.edu",
        "description": "学生成绩查询与在线缴费门户，含教师端（notas2.nur.edu/Docentes/）。",
        "source": "official_website",
    },
    {
        "name": "Biblioteca NUR",
        "url": "https://biblio.nur.edu",
        "description": "大学数字图书馆门户。",
        "source": "official_website",
    },
    {
        "name": "Portal IICS-NUR",
        "url": "https://iics.nur.edu",
        "description": "科学与社会研究所（Instituto de Investigación Científica y Social）门户，发布学术期刊、征稿与NUR出版社信息。",
        "source": "official_website",
    },
    {
        "name": "UNIRSE 平台",
        "url": "https://unirse.nur.edu",
        "description": "大学社区服务计划（Universitarios al Servicio de la Comunidad）项目管理平台。",
        "source": "official_website",
    },
    {
        "name": "Internacionalización 门户",
        "url": "https://internacionalizacion.nur.edu",
        "description": "国际化办公室门户，发布国际交流与合作项目信息。",
        "source": "official_website",
    },
    {
        "name": "FESTINUR 门户",
        "url": "https://festinur.nur.edu",
        "description": "努尔短片节（Festival de Cortometrajes NUR）官方网站。",
        "source": "official_website",
    },
    {
        "name": "Fernandito Assistant",
        "url": "https://www.nur.edu",
        "description": "官网在线聊天机器人，提供招生与咨询问答。",
        "source": "official_website",
    },
]

data["key_people"] = [
    {
        "person_id": None,
        "name": "威廉·绍艾·贝克（William Shoaie Baker）",
        "title": "校长（Rector）",
        "title_description": "大学最高行政负责人，由托管委员会（Junta Fiduciaria）提名、创始人大会批准任命；文献中亦作 Willy Shoaie Baker，称谓 Mgr.（Magíster，硕士）。",
        "description": "至少自2010年起执掌努尔大学至今，领导玻利维亚首所依法设立的私立大学。近期活动：2025年8月率团出席南美中西部大学校长一体化委员会（CRISCOS）第26届大会；2025年12月出镜官方播客NURCAST首期，介绍2026年新培养方案；2026年1月在开学典礼致辞欢迎Gestión I/2026学年第II学期新生。",
    },
    {
        "person_id": None,
        "name": "古斯塔沃·奥尔特加（Gustavo Ortega）",
        "title": "学术副校长（Vicerrector Académico）",
        "title_description": "协助校长主管学术事务，与校长同属指导委员会（Consejo Directivo）。",
        "description": "现任努尔大学学术副校长，联系邮箱 vr_academico@nur.edu（官网权威页列示）。",
    },
    {
        "person_id": None,
        "name": "阿巴斯·礼萨尼（Abbas Rezvani）",
        "title": "财务副校长（Vicerrector Financiero）",
        "title_description": "主管大学财务与行政资源管理，为指导委员会成员。",
        "description": "现任努尔大学财务副校长（官网权威页列示）。",
    },
    {
        "person_id": None,
        "name": "奥古斯托·科斯塔斯·莫雷利（Augusto Costas Morelli）",
        "title": "拉巴斯分校主任（Director La Paz）",
        "title_description": "负责拉巴斯校区（Subsede La Paz）的运营与教学管理。",
        "description": "现任努尔大学拉巴斯分校主任（官网权威页列示）。",
    },
    {
        "person_id": None,
        "name": "萨桑·塞达加特（Sassan Sedaghat）",
        "title": "国际化办公室负责人（Responsable de Internacionalización）",
        "title_description": "主管大学国际化战略与国际学术合作事务。",
        "description": "2026年8月代表努尔大学出席在科恰班巴举行的CRISCOS 2026国际研究研讨会，强调区域科研合作与未来联合项目的前景。",
    },
]

data["departments"] = [
    {
        "name": "本科部（Pregrado）",
        "dept_id": None,
        "head": None,
        "description": "开设17个学士学位专业，覆盖工商管理、市场营销、商业工程、金融工程、系统工程、网络与电信、公共会计、法律、国际关系、公共关系、社会传播、心理学、心理教育学、营养学、理疗与康复、可持续发展旅游等；圣克鲁斯主校区与拉巴斯分校开课，实行面授与半面授并举的学期制。",
        "parent_dept_id": None,
    },
    {
        "name": "研究生院（Postgrado / Colegio de Postgrado）",
        "dept_id": None,
        "head": None,
        "description": "1986年创设，为玻利维亚首个研究生院。现设工商管理、国际贸易、公共卫生（卫生系统管理方向）、社会发展、金融管理、人力资源管理、审计、市场营销、会计与税务规划、大学教育、水与基础卫生项目管理等11个硕士项目，以及企业管理、高等教育、医院管理等领域的多类高级研修（diplomados）课程。",
        "parent_dept_id": None,
    },
    {
        "name": "国际语言中心（Centro Internacional de Idiomas Núr）",
        "dept_id": None,
        "head": None,
        "description": "面向校内外开设英语、葡萄牙语语言教学，为官网一级学术单位（Idiomas）。",
        "parent_dept_id": None,
    },
    {
        "name": "持续教育部（Educación Continua）",
        "dept_id": None,
        "head": None,
        "description": "面向在职人士与企业提供短期培训与高级研修课程，为官网列示的四大教学板块之一。",
        "parent_dept_id": None,
    },
    {
        "name": "科学与社会研究所（Instituto de Investigación Científica y Social, IICS-NUR）",
        "dept_id": None,
        "head": None,
        "description": "大学科研中枢（门户 iics.nur.edu），出版学术期刊（如Oikonomía）、组织学生研究种子项目（semilleros，含环境正义与气候变化方向），并与德国技术合作公司（GIZ）、国际科研网络等开展合作研究。",
        "parent_dept_id": None,
    },
    {
        "name": "NUR出版社（Editorial NUR）",
        "dept_id": None,
        "head": None,
        "description": "大学出版机构，2026年在圣克鲁斯国际书展（FILSC 2026）推出13部新出版物，并出版《NARRATIVAS GLOBALES》等刊物。",
        "parent_dept_id": None,
    },
    {
        "name": "大学社区服务计划（UNIRSE）",
        "dept_id": None,
        "head": None,
        "description": "要求本科学生完成至少120小时社区服务的管理机构；运营帕尔马索拉（Palmasola）监狱法学教学中心等社会延伸项目，与公私机构合作服务市政、民间组织与农村教师群体。",
        "parent_dept_id": None,
    },
]

data["recent_events"] = [
    {
        "date": "2026-10-19",
        "title": "与国际原住民权利组织IWGIA合作开展原住民领地能力建设",
        "description": "努尔大学与IWGIA联合实施项目，强化原住民组织在领地防御与管理方面的能力（此前亦与玻利维亚原住民女性领袖网络CNAMIB合作举办原住民领地领导力与治理培训）。",
        "impact": "巩固大学在原住民发展、可持续发展与社会责任领域的影响力，拓展国际合作网络。",
        "source": "https://www.nur.edu/direccion-santa-cruz/",
    },
    {
        "date": "2026-10-15",
        "title": "承办玻利维亚首届筹款与可持续发展全国会议",
        "description": "努尔大学首次在玻利维亚主办'Primer Encuentro de Fundraising y Sostenibilidad de Bolivia 2026'，约40家机构与会。",
        "impact": "确立大学作为社会部门能力建设与可持续发展议题召集者的地位，提升机构声誉与合作资源。",
        "source": "https://www.facebook.com/UniversidadNURoficial/posts/la-universidad-nur-fue-sede-del-primer-encuentro-de-fundraising-y-sostenibilidad/1550478543773866/",
    },
    {
        "date": "2026-10-13",
        "title": "推进师资博士化战略，与西班牙纳瓦拉公立大学（UPNA）合作",
        "description": "努尔大学实施教师队伍博士培养战略，与西班牙纳瓦拉公立大学合作开展师资博士训练，以提升高等教育质量与研究水平。",
        "impact": "提高教师博士学位比例与科研产出，推动学校向研究型、国际化方向转型。",
        "source": "https://www.instagram.com/p/DecOJ75jqWW/",
    },
    {
        "date": "2026-09-27",
        "title": "向圣克鲁斯市捐赠'El Jichi'民俗传说雕塑",
        "description": "在圣克鲁斯建城纪念月期间，努尔大学'民俗传说步道'（Paseo de Leyendas Costumbristas）扩容，揭幕玻利维亚艺术家创作的'El Jichi'雕塑并赠予城市。",
        "impact": "以城市文化公益提升大学公众可见度与社区联结。",
        "source": "https://periodistavirtual.com/2026/09/27/en-el-mes-de-santa-cruz-la-universidad-nur-le-hace-un-regalo-a-la-ciudad/",
    },
    {
        "date": "2026-08-26",
        "title": "首次参加CRISCOS 2026国际研究研讨会",
        "description": "8月26-28日在科恰班巴多明戈·萨维奥私立大学（UPDS）举行的CRISCOS 2026国际研究研讨会（主题'知识无国界：从南安第斯联结领土'，阿根廷、玻利维亚、智利、厄瓜多尔、巴拉圭、秘鲁六国高校参与），努尔大学师生首次以观察员身份参加校际工作组会议；校长已于2025年8月出席CRISCOS第26届大会。",
        "impact": "标志其研究国际化战略落地，为联合发表、合作项目与学术流动铺路。",
        "source": "https://www.nur.edu/la-universidad-nur-proyecta-su-investigacion-internacional-a-traves-de-la-red-criscos/",
    },
    {
        "date": "2026-02-28",
        "title": "与Instituto Técnico CEPESS签署战略合作框架协议",
        "description": "努尔大学与技术学院CEPESS签署宏观合作协议（convenio macro），共同推进玻利维亚教育发展。",
        "impact": "打通职业教育与高等教育衔接渠道，扩大生源与合作办学网络。",
        "source": "https://www.instagram.com/p/DVTlIsbDedU/",
    },
    {
        "date": "2025-12-03",
        "title": "官方播客NURCAST上线，首期聚焦2026年新培养方案",
        "description": "努尔大学推出播客'NURCAST - Entre Voces'第一季，首期邀请校长William Shoaie介绍2026年新教学计划。",
        "impact": "拓展数字传播渠道，对外公布2026年课程与培养方案更新。",
        "source": "https://www.youtube.com/watch?v=Bfi0bJVD-Po",
    },
]

data["related_entities"] = [
    {
        "org_id": "BO-GOV-008",
        "org_name": "Ministry of Education (Ministerio de Educación)",
        "org_type": "government_ministry",
        "org_description": "玻利维亚教育部，私立大学的主管部门（cabeza de sector）。",
        "relationship_type": "regulator",
    },
    {
        "org_id": "BO-ACAD-010",
        "org_name": "Universidad Privada de Santa Cruz de la Sierra (UPSA)",
        "org_type": "university",
        "org_description": "同城（圣克鲁斯）私立大学，同为CRISCOS等区域学术网络的参与方。",
        "relationship_type": "sibling",
    },
    {
        "org_id": None,
        "org_name": "Universidad Pública de Navarra (UPNA)",
        "org_type": "university",
        "org_description": "西班牙纳瓦拉公立大学，与努尔大学合作开展师资博士培养。",
        "relationship_type": "partner",
    },
    {
        "org_id": None,
        "org_name": "Red CRISCOS (Consejo de Rectores por la Integración de la Subregión Centro Oeste de Sudamérica)",
        "org_type": "university_network",
        "org_description": "南美中西部次区域大学校长一体化委员会，覆盖阿根廷、玻利维亚、智利、厄瓜多尔、巴拉圭、秘鲁六国高校，促进科研合作、学术交流与流动项目。",
        "relationship_type": "member_of",
    },
    {
        "org_id": None,
        "org_name": "IWGIA (International Work Group for Indigenous Affairs)",
        "org_type": "international_ngo",
        "org_description": "国际原住民事务工作组，与努尔大学合作开展原住民领地防御与管理能力建设。",
        "relationship_type": "partner",
    },
    {
        "org_id": None,
        "org_name": "Deutsche Gesellschaft für Internationale Zusammenarbeit (GIZ)",
        "org_type": "international_agency",
        "org_description": "德国技术合作公司，与努尔大学科学与社会研究所（IICS）合作学生研究种子项目。",
        "relationship_type": "partner",
    },
    {
        "org_id": None,
        "org_name": "Instituto Técnico CEPESS",
        "org_type": "technical_institute",
        "org_description": "玻利维亚技术学院，2026年2月与努尔大学签署宏观战略合作框架协议。",
        "relationship_type": "strategic_alliance",
    },
]

data["core_business"] = (
    "努尔大学（Universidad Núr）是玻利维亚首所依法设立的私立大学：1982年由多国人士发起创办申请，1984年8月28日经最高法令第20441号批准设立，1985年4月以97名学生开学，1986年创设玻利维亚首个研究生院，1994年开创该国远程教育先河，并是玻利维亚首家采用学期制的大学。主校区位于圣克鲁斯-德拉谢拉（Av. Cristo Redentor No. 100），在拉巴斯设分校。学校以'培养变革者'（Formamos Agentes de Cambio）为校训，通过ISO 9001质量认证，现有约4000余名学生，开设17个本科专业与11个硕士项目及多类高级研修课程，学科覆盖工商管理、金融、系统工程与网络电信、法律、国际关系、传播、心理与教育、营养与理疗、可持续旅游等领域。校内设国际语言中心、持续教育部、科学与社会研究所（IICS）与NUR出版社，运营虚拟校园平台，并通过UNIRSE社区服务计划要求学生完成至少120小时志愿服务，含在帕尔马索拉监狱设立法学教学中心等特色社会项目。"
)

data["profile"] = (
    "努尔大学是玻利维亚历史最悠久的私立大学之一，1985年在圣克鲁斯-德拉谢拉开学，以学期制、研究生教育和远程教育开创者著称。现任校长为威廉·绍艾·贝克（William Shoaie Baker）。学校定位应用型、双语化与国际化并重，近年持续推进师资博士化（与西班牙UPNA合作）、研究国际化（首次参与CRISCOS网络）与社会影响力建设（IWGIA原住民合作、首届筹款与可持续发展全国会议），同时通过 Editorial NUR、FESTINUR 短片节和 UNIRSE 社区服务计划拓展文化传播与社会服务职能。"
)

data["apec_stance"] = "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。努尔大学作为玻利维亚私立高校，无公开的APEC相关立场表态。"

data["collection_meta"] = {
    "collection_date": "2026-10-24",
    "phase": "phase3_enriched",
    "data_sources": [
        "wikidata",
        "wikipedia (es)",
        "official_website (nur.edu: 首页/autoridades-ejecutivas/CRISCOS新闻页)",
        "facebook (UniversidadNURoficial)",
        "instagram (@universidadnur)",
        "youtube (Universidad NUR Bolivia)",
        "linkedin",
        "news_media (periodistavirtual.com)",
        "search (mcp__search-read)",
    ],
    "completeness_score": 19,
    "notes": "Phase3 enrichment 2026-10-24: 校长William Shoaie Baker经2025-08 Instagram、2026-01 Facebook、官网autoridades页多源核实；领导层含学术副校长Gustavo Ortega、财务副校长Abbas Rezvani、拉巴斯主任Augusto Costas Morelli；近期事件7条（2025-12至2026-10）均带来源；社交账号与数字资产来自官网页脚/导航核实。",
    "quotes": [
        {
            "title": "Universidad Núr - Wikipedia, la enciclopedia libre",
            "url": "https://es.wikipedia.org/wiki/Universidad_N%C3%BAr",
        },
        {
            "title": "Autoridades Ejecutivas - Universidad Nur（Rector: William Shoaie）",
            "url": "https://www.nur.edu/autoridades-ejecutivas/",
        },
        {
            "title": "La Universidad NUR proyecta su investigación internacional a través de la Red CRISCOS（2026-09-01, Santa Cruz de la Sierra）",
            "url": "https://www.nur.edu/la-universidad-nur-proyecta-su-investigacion-internacional-a-traves-de-la-red-criscos/",
        },
        {
            "title": "Nuestro rector, Mgr. William Shoaie Baker, participó en la XXVI Asamblea del CRISCOS（2025-08-12）",
            "url": "https://www.instagram.com/p/DNRiOWXuK-b/",
        },
        {
            "title": "Bienvenidos a la Gestión I/2026 – Universidad NUR（2026-01-26）",
            "url": "https://www.facebook.com/UniversidadNURoficial/posts/-bienvenidos-a-la-gesti%C3%B3n-i2026-universidad-nuriniciamos-un-nuevo-a%C3%B1o-acad%C3%A9mico-/1322630083225381/",
        },
        {
            "title": "La Universidad NUR fue sede del Primer Encuentro de Fundraising y Sostenibilidad de Bolivia 2026（2026-10-15）",
            "url": "https://www.facebook.com/UniversidadNURoficial/posts/la-universidad-nur-fue-sede-del-primer-encuentro-de-fundraising-y-sostenibilidad/1550478543773866/",
        },
    ],
}

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK: enriched", path)

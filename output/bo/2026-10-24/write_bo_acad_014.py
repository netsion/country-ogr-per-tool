# -*- coding: utf-8 -*-
"""Write enriched profile for BO-ACAD-014 (Universidad de Aquino Bolivia / UDABOL)."""
import json

data = {
    "org_id": "BO-ACAD-014",
    "basic_info": {
        "name_original": "Universidad de Aquino Bolivia",
        "name_zh": "阿基诺玻利维亚大学",
        "name_en": "University of Aquino Bolivia",
        "aliases": ["UDABOL", "Universidad de Aquino Bolivia S.A.", "Udabol Internacional"],
        "org_type": "ACAD",
        "org_subtype": "university",
        "country_iso3": "BOL",
        "hq_country_iso3": "BOL",
        "founded_date": "1995-01-01",
        "website": "https://udabol.edu.bo",
        "wikidata_qid": "Q10387889"
    },
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "Universidad de Aquino Bolivia - Udabol (@udaboldigital)",
            "url": "https://www.facebook.com/udaboldigital",
            "source": "https://udabol.edu.bo 官网页脚资源"
        },
        {
            "platform": "instagram",
            "account_name": "@udaboloficial",
            "url": "https://www.instagram.com/udaboloficial/",
            "source": "https://udabol.edu.bo 官网页脚资源"
        },
        {
            "platform": "tiktok",
            "account_name": "@udaboloficial",
            "url": "https://www.tiktok.com/@udaboloficial",
            "source": "https://udabol.edu.bo 官网页脚资源"
        },
        {
            "platform": "youtube",
            "account_name": "Noticias UDABOL (@NoticiasUdabol)",
            "url": "https://www.youtube.com/@NoticiasUdabol",
            "source": "https://udabol.edu.bo 官网页脚资源"
        },
        {
            "platform": "youtube",
            "account_name": "UDABOL (@UDABOLdigital)",
            "url": "https://www.youtube.com/@UDABOLdigital",
            "source": "YouTube频道自述为'Canal Oficial de la Universidad de Aquino Bolivia'"
        },
        {
            "platform": "other",
            "account_name": "UDABOL 官方 WhatsApp（+591 69404174）",
            "url": "https://wa.me/59169404174",
            "source": "https://udabol.edu.bo 官网页脚资源"
        }
    ],
    "digital_assets": [
        {
            "name": "Aula Virtual UDABOL（虚拟学习平台）",
            "url": "https://virtual.udabol.edu.bo/login/",
            "description": "UDABOL 在线虚拟校园登录入口，承载在线教学、课程资料与学生学业管理。",
            "source": "https://udabol.edu.bo 官网资源链接"
        },
        {
            "name": "UDABOL Perú（秘鲁站点）",
            "url": "https://peru.udabol.edu.bo/",
            "description": "UDABOL 面向秘鲁市场的官方网站，用于国际招生与跨境办学项目推广，自称'玻利维亚的领先大学'。",
            "source": "https://peru.udabol.edu.bo/"
        }
    ],
    "key_people": [
        {
            "person_id": None,
            "name": "Antonio Saavedra Muñoz",
            "title": "Rector Nacional",
            "title_description": "国民校长（大学最高负责人）",
            "description": "玻利维亚知名学者，自至少2019年起担任UDABOL国民校长，2026年6月仍以校长身份出席学校第七届国际传播大会（CICOM 2026），在任状态获多个独立来源确认。曾任圣安德烈斯大学（UMSA）校长、玻利维亚国家科学院院长，2022年获玻利维亚参议院表彰，并曾获多民族立法大会众议院授予的荣誉（以UDABOL校长兼国家科学院院士身份）。"
        },
        {
            "person_id": None,
            "name": "Marcelo Arroyo Saavedra",
            "title": "Vicerrector",
            "title_description": "副校长",
            "description": "2025年12月以UDABOL副校长（vicerrector）身份通过ATB电视台公开介绍学校多元学术项目。2019年校刊显示其时任拉巴斯-奥鲁罗区域副校长，2023年以副校长身份随校长出席玻利维亚众议院与学术机构的交流会议。"
        },
        {
            "person_id": None,
            "name": "Martín Dockweiler Cárdenas",
            "title": "Presidente de la Fundación UDABOL",
            "title_description": "UDABOL基金会主席",
            "description": "UDABOL创办基金会（Fundación UDABOL）主席，2010年AEMP对UDABOL S.A.开展审计时的大学法人代表，媒体报道中亦常以大学负责人（presidente de UDABOL）身份活动。2026年7月以大学负责人身份自其家族命名的马丁·多克韦勒大学医院启动全国最大规模免费医疗队'友爱大篷车'（Caravana de la Hermandad）。"
        }
    ],
    "departments": [
        {
            "name": "Facultad de Ciencias de la Salud（健康科学学部）",
            "dept_id": None,
            "head": None,
            "description": "官网列示设6个本科项目，标语为'以卓越培养健康专业人才'。开设医学、牙科、生物化学与制药、护理、物理治疗与运动机能学等专业，依托马丁·多克韦勒数字大学医院开展临床沉浸式教学，是学校最具国际影响力的学部。",
            "parent_dept_id": None
        },
        {
            "name": "Facultad de Ciencias Sociales y Humanísticas（社会科学与人文科学学部）",
            "dept_id": None,
            "head": None,
            "description": "官网列示设5个本科项目，标语为'正义、伦理与社会发展'。开设法律、国际关系、心理学、传播学等专业。",
            "parent_dept_id": None
        },
        {
            "name": "Facultad de Ciencias Económicas y Financieras（经济与金融学部）",
            "dept_id": None,
            "head": None,
            "description": "官网列示设4个本科项目，标语为'明日的商界领袖'。开设工商管理、审计学、商业工程、市场营销与广告等专业。",
            "parent_dept_id": None
        },
        {
            "name": "Facultad de Ciencias Agrícolas Pecuarias（农牧科学学部）",
            "dept_id": None,
            "head": None,
            "description": "官网列示设3个本科项目，标语为'农牧业领域的创新'。开设农学工程、兽医学与动物生产等专业（主要在圣克鲁斯校区）。",
            "parent_dept_id": None
        },
        {
            "name": "Facultad de Ciencia y Tecnología（科学与技术学部）",
            "dept_id": None,
            "head": None,
            "description": "官网列示设6个本科项目，标语为'面向未来的科技与创新'。开设系统工程、电信工程、天然气与石油工程、环境工程等专业。",
            "parent_dept_id": None
        },
        {
            "name": "Facultad de Teología, Filosofía y Letras（神学、哲学与文学学部）",
            "dept_id": None,
            "head": None,
            "description": "官网列示设1个本科项目，标语为'批判性思维与价值观'，为学校特色人文神科学部。",
            "parent_dept_id": None
        },
        {
            "name": "Facultad de Arquitectura Hábitat y Diseño（建筑、人居与设计学部）",
            "dept_id": None,
            "head": None,
            "description": "官网列示设2个本科项目，标语为'空间的创意与设计'。开设建筑学、设计等专业。",
            "parent_dept_id": None
        },
        {
            "name": "Sede Santa Cruz（圣克鲁斯校区）",
            "dept_id": None,
            "head": None,
            "description": "现主校区（2003年设立，百科记载成立日期为2004年3月22日），校长团队与马丁·多克韦勒大学医院、高研究中心所在地；官网以圣克鲁斯校区为形象主体，开设专业最全（含农学、兽医学、设计等），并设有面向秘鲁等邻国的国际招生布局。",
            "parent_dept_id": None
        },
        {
            "name": "Sede La Paz（拉巴斯校区）",
            "dept_id": None,
            "head": None,
            "description": "学校首个校区，1995年上半年开学，设医学、牙科、法律、心理学、系统与电信工程等专业；2026年6月在该校区举办第七届国际传播大会（CICOM 2026）。",
            "parent_dept_id": None
        },
        {
            "name": "Sede Cochabamba（科恰班巴校区）",
            "dept_id": None,
            "head": None,
            "description": "1996年2月21日获开设许可，1999年初正式运行，开设医学、生物化学与制药、法律、国际关系、建筑等专业。",
            "parent_dept_id": None
        },
        {
            "name": "Sede Oruro（奥鲁罗校区）",
            "dept_id": None,
            "head": None,
            "description": "1995年9月设立、1996年2月21日获开设许可，为学校第二个校区，开设医学、牙科、天然气与石油工程等专业。",
            "parent_dept_id": None
        },
        {
            "name": "Hospital Universitario Martín Dockweiler（马丁·多克韦勒大学医院）",
            "dept_id": None,
            "head": None,
            "description": "以UDABOL基金会主席家族命名的三级（tercer nivel）教学医院，媒体称其为玻利维亚首家全数字化医院，设400张住院床位、机器人模拟器与3D解剖台；为UDABOL医学生临床教学基地和2026年全国医疗公益活动的出发地。",
            "parent_dept_id": None
        }
    ],
    "recent_events": [
        {
            "date": "2026-07-09",
            "title": "启动全国最大规模免费医疗队'友爱大篷车：玻利维亚团结健康行'",
            "description": "UDABOL联合Fundación MD与马丁·多克韦勒大学医院，自圣克鲁斯大学医院派出12座移动医院、10辆救护车、6万名学生和20吨食品药品物资，用30天巡回科恰班巴、奥鲁罗、拉巴斯三个受53天全国封锁冲击最严重的省，提供免费医疗、牙科、心理与法律服务，并首次用人工智能量化统计医疗发现。",
            "impact": "在玻利维亚政治极化与危机背景下显著提升UDABOL全国声誉与社会影响力，把'街头变课堂'的办学模式推向全国，并被媒体称为玻利维亚大学史上最大规模医疗公益活动。",
            "source": "https://eju.tv/2026/07/udabol-y-la-fundacion-md-despliegan-la-mayor-brigada-medica-gratuita-con-60-000-universitarios-y-12-hospitales-moviles-en-provincias-y-barrios-del-pais/"
        },
        {
            "date": "2026-03-11",
            "title": "UDABOL毕业生在巴西Revalida医师资格考试中助玻利维亚登顶拉美第一",
            "description": "在巴西2025-2期Revalida考试中，玻利维亚以500人通过的成绩超越古巴（461人）位居拉美第一；UDABOL在2025/1期中有185名毕业生通过考试，进入向巴西卫生系统输送医师最多的全球前十机构（数据来自Estratégia MED与巴西INEP），报道归功于其依托数字化大学医院的临床沉浸式培养模式。",
            "impact": "显著巩固UDABOL医学教育的国际声誉，确立其作为玻利维亚医学人才输出龙头和圣克鲁斯医学教育中心地位，带动跨境招生与地方经济。",
            "source": "https://www.opinion.com.bo/cochabamba/bolivia-hace-historia-lidera-toda-latinoamerica-validacion-medicos-brasil-udabol-como-protagonista/20260311210714989943.html"
        },
        {
            "date": "2026-06-16",
            "title": "在拉巴斯校区举办第七届国际传播大会（CICOM 2026）",
            "description": "UDABOL于2026年6月16日在拉巴斯举行第七届国际传播大会（CICOM 2026），聚焦传播行业新趋势、战略与转型，由校长Antonio Saavedra Muñoz揭幕；同期学校还举办/筹备了第七届国际建筑与城市大会（CIAC 2026'挑战与机遇'）等系列国际学术会议。",
            "impact": "强化UDABOL作为国际学术交流平台的品牌形象，扩大其传播学与建筑学科的全国影响力。",
            "source": "https://www.facebook.com/udaboldigital/posts/1443124534505576"
        },
        {
            "date": "2025-12-05",
            "title": "发布'UDABOL 2026国际卫生-学术使命'区域项目",
            "description": "UDABOL官方账号宣布启动Misión Sanitario-Académica Internacional UDABOL 2026（2026国际卫生-学术使命），一项旨在重塑区域卫生与学术合作的项目。",
            "impact": "拓展UDABOL在区域（拉美）卫生教育合作与跨境影响力方面的布局，为其2026年系列医疗公益活动铺垫。",
            "source": "https://www.instagram.com/reel/DR5vBNoks24/"
        },
        {
            "date": "2024-12-16",
            "title": "新校区落成，主打医学创新与数字化医疗教育",
            "description": "UDABOL官方账号宣布新校区落成（学校宣传称其为第五校区、'玻利维亚医学界的哈佛'），配套数字化医学教学设施，与马丁·多克韦勒数字大学医院及高研究中心形成医教研一体化布局。",
            "impact": "扩大UDABOL医学与临床教学容量，支撑其后续在巴西医师认证考试中的突出表现与全国医疗公益活动能力。",
            "source": "https://www.facebook.com/udaboldigital/posts/999176078900426"
        }
    ],
    "related_entities": [
        {
            "org_id": "BO-GOV-008",
            "org_name": "玻利维亚教育部 (Ministerio de Educación)",
            "org_type": "GOV",
            "org_description": "玻利维亚主管教育的政府部门，私立大学的设立与运营须经其审批认证。",
            "relationship_type": "regulator"
        },
        {
            "org_id": "BO-ACAD-008",
            "org_name": "玻利维亚圣保罗天主教大学 (Universidad Católica Boliviana San Pablo)",
            "org_type": "ACAD",
            "org_description": "玻利维亚主要私立大学（天主教会背景），与UDABOL同属私立高等教育体系的主要同行院校。",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "BO-ACAD-009",
            "org_name": "玻利维亚私立大学 (Universidad Privada Boliviana)",
            "org_type": "ACAD",
            "org_description": "玻利维亚知名私立大学，与UDABOL同属私立高等教育体系的同行院校。",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "BO-ACAD-010",
            "org_name": "圣克鲁斯私立大学 (Universidad Privada de Santa Cruz de la Sierra)",
            "org_type": "ACAD",
            "org_description": "位于圣克鲁斯的私立大学，与主校区同在圣克鲁斯的UDABOL在招生与学科上构成直接同行竞争关系。",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "BO-ACAD-011",
            "org_name": "山谷私立大学 (Universidad Privada del Valle)",
            "org_type": "ACAD",
            "org_description": "玻利维亚主要私立大学，与UDABOL同属私立高等教育体系的同行院校。",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "BO-ACAD-012",
            "org_name": "弗兰斯·塔马约私立大学 (Universidad Privada Franz Tamayo)",
            "org_type": "ACAD",
            "org_description": "玻利维亚私立大学（UNIFRANZ），与UDABOL同属私立高等教育体系的同行院校。",
            "relationship_type": "affiliated"
        },
        {
            "org_id": None,
            "org_name": "Fundación UDABOL（UDABOL基金会）",
            "org_type": "NGO",
            "org_description": "与UDABOL关系密切的创办基金会，由Martín Dockweiler Cárdenas任主席；2026年7月以'Fundación MD'名义与大学联合发起全国最大免费医疗队，媒体亦称Dockweiler为UDABOL的负责人。",
            "relationship_type": "affiliated"
        },
        {
            "org_id": None,
            "org_name": "Missouri State University（美国密苏里州立大学）",
            "org_type": "ACAD",
            "org_description": "美国密苏里州公立大学，UDABOL官网宣称与其合作开设硕士（maestría）课程。",
            "relationship_type": "strategic_alliance"
        }
    ],
    "core_business": "阿基诺玻利维亚大学（UDABOL）是玻利维亚发展最快的私立大学之一，1995年获教育部系统设立许可（Resolución Secretarial No.144），2001年被认证为正式大学（Universidad Plena，Resolución Ministerial 288/01），2012年获最高法令1076追认。主校区位于圣克鲁斯，并在拉巴斯、科恰班巴、奥鲁罗设校区，官网宣称在校生逾56,000人、毕业生逾10万人。学校提供85个以上学术项目，设健康科学、社会科学与人文、经济与金融、农牧科学、科学技术、神学哲学文学、建筑人居设计7个学部，涵盖医学、牙科、生物化学制药、法律、国际关系、系统工程、天然气与石油工程、建筑、农学、兽医学等本科与研究生教育，办学特色为'开放式课堂'（Aula Abierta）与全国性医疗义教队。学校运营以家族命名的三级全数字化马丁·多克韦勒大学医院（400张床位、机器人模拟器、3D解剖台）和全国规模最大的'高研究中心'，课程获南方共同市场ARCU-SUR认证，并与剑桥考评、塞万提斯学院、哈佛商业出版及美国密苏里州立大学等120多个国际机构合作，官方宣称98%就业率（毕业后6个月内）。法律上以UDABOL S.A.公司形式运营，由UDABOL基金会（主席Martín Dockweiler Cárdenas）管理。",
    "industries": ["higher_education", "healthcare"],
    "apec_stance": "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。",
    "profile": {
        "source_url": "https://udabol.edu.bo/assets/udabol-logo-CuChm8dC.png",
        "local_path": None
    },
    "collection_meta": {
        "collection_date": "2026-10-24",
        "phase": "phase3_enriched",
        "data_sources": [
            "wikidata",
            "official_website (udabol.edu.bo 首页与JS资源包)",
            "EcuRed百科 (ecured.cu)",
            "Opinion报 (opinion.com.bo, 2026-03-11)",
            "eju.tv (2026-07-09)",
            "Agencia de Noticias Fides (noticiasfides.com)",
            "玻利维亚众议院 (diputados.gob.bo, 2023-09-07)",
            "玻利维亚国家科学院 (aciencias.gob.bo)",
            "El Diario (eldiario.net, 2022-07-19)",
            "UDABOL官方Facebook/Instagram/TikTok/YouTube账号",
            "uniRank",
            "UMSA官网新闻 (umsa.bo, 2024-06-17)"
        ],
        "quotes": [
            {
                "title": "Bolivia hace historia: lidera en toda Latinoamérica la validación de médicos en Brasil, con UDABOL como protagonista (Opinión, 2026-03-11)",
                "url": "https://www.opinion.com.bo/cochabamba/bolivia-hace-historia-lidera-toda-latinoamerica-validacion-medicos-brasil-udabol-como-protagonista/20260311210714989943.html"
            },
            {
                "title": "UDABOL y la Fundación MD despliegan la mayor brigada médica gratuita con 60.000 universitarios y 12 hospitales móviles (eju.tv, 2026-07-09)",
                "url": "https://eju.tv/2026/07/udabol-y-la-fundacion-md-despliegan-la-mayor-brigada-medica-gratuita-con-60-000-universitarios-y-12-hospitales-moviles-en-provincias-y-barrios-del-pais/"
            },
            {
                "title": "Universidad de Aquino Bolivia - EcuRed（1995年建校、法定认证沿革、四校区沿革）",
                "url": "https://www.ecured.cu/Universidad_de_Aquino_Bolivia"
            },
            {
                "title": "Reunión promueve la interacción entre el Órgano Legislativo con instituciones académicas (Cámara de Diputados, 2023-09-07，校长Antonio Saavedra Muñoz与副校长Marcelo出席)",
                "url": "https://diputados.gob.bo/noticias/reunion-promueve-la-interaccion-entre-el-organo-legislativo-con-instituciones-academicas/"
            },
            {
                "title": "AEMP: Fiscalización a UDABOL responde a 200 denuncias en su contra (ANF/Fides, 2010-08-05，确认UDABOL S.A.法人实体与Dockweiler代表身份)",
                "url": "https://www.noticiasfides.com/economia/aemp-fiscalizacion-a-udabol-responde-a-200-denuncias-en-su-contra"
            }
        ],
        "completeness_score": 86,
        "notes": "Phase3富集：官网为React SPA，通过其JS资源包核实7学部、4校区、社交账号、ARCU-SUR认证、56,000+在校生、120+国际协议、数字化大学医院等关键事实；现任校长Antonio Saavedra Muñoz经2026-06-16媒体日报道与2023年众议院新闻双重确认在任。关键人无既有person_id（name_index未命中），留空；三位关键人物均为西语原名（无可靠既有中文译名，避免机械音译）。官网标题中的'1952年'疑为模板残留，与meta描述'más de 30 años'及Wikidata/EcuRed的1995年建校不一致，采信1995。 departments/school负责人及各学部负责人信息未公开核实，留空。"
    }
}

path = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\orgs\BO-ACAD-014.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("written:", path)

# -*- coding: utf-8 -*-
"""Write person profile BO-PERSON-000079 (Jorge Ernesto Ávila Antelo)."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000079.json")

profile = {
    "person_id": "BO-PERSON-000079",
    "wikidata_qid": None,
    "name": "Jorge Ernesto Ávila Antelo",
    "name_en": "Jorge Ernesto Ávila Antelo",
    "name_zh": "豪尔赫·阿维拉·安特洛",
    "aliases": ["Jorge Ernesto Ávila", "Jorge Ávila Antelo", "Jorge Ávila", "Jorge E. Ávila"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "birth_date_note": "公开资料未查到出生日期；媒体仅称其在环境林业领域有近35年经历，无出生年份信息，故留空。",
    "name_zh_note": "华人头条-秘鲁（2026-05-31）报道使用译名「豪尔赫·阿维拉·安特洛」；未发现其他华文媒体既有译名，采用该译名。",
    "contacts": [
        {
            "type": "email",
            "value": "jorge.avila@planificacion.gob.bo",
            "source": "水俣公约（Minamata Convention）官方人物页（历史域名，任内曾长期使用规划部域名）"
        },
        {
            "type": "website",
            "value": "https://www.planificacion.gob.bo/page/content/2154",
            "source": "官方履历页（规划发展与环境部网站，内容为任内发布）"
        }
    ],
    "current_positions": ["环境、生物多样性、气候变化及森林管理与发展副部长"],
    "education": [],
    "education_note": "官方简历称其具备环境立法、自然资源管理与可持续发展领导力培训经历，并曾任大学生态课程讲师；新闻报道（2025-11-20）称其为法学学士（licenciado en Derecho）并专修环境法，但公开资料未披露具体院校名称与就读年份，education 依规则留空。",
    "work_experience": [
        {
            "start_date": "2025-11-14",
            "end_date": None,
            "organization": "玻利维亚生产与环境可持续部 (Ministerio de Producción Sostenible, Medio Ambiente y Agua)",
            "org_id": "BO-GOV-012",
            "position": "环境、生物多样性、气候变化及森林管理与发展副部长"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚林业商会 (Cámara Forestal de Bolivia)",
            "org_id": None,
            "position": "总经理兼法务主管"
        },
        {
            "start_date": "2006",
            "end_date": "2007",
            "organization": "玻利维亚制宪大会 (Asamblea Constituyente)",
            "org_id": None,
            "position": "制宪议会议员"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚森林环境法协会 (Asociación de Derecho Forestal-Ambiental de Bolivia)",
            "org_id": None,
            "position": "主席"
        }
    ],
    "work_note": "官方简历载明：玻利维亚律师，环境法、林业法与公共政策领域从业逾三十年，曾任玻利维亚林业商会总经理兼法务主管、制宪议会议员、玻利维亚森林环境法协会主席，从事国内外咨询并任大学生态课程讲师。El País（2025-11-14）称其在环境林业领域有近35年经历，大部分与林业商会相关。2025-11-14 由时任部长 Óscar Mario Justiniano 主持宣誓就任副部长（当时隶属环境与水部，Justiniano 兼掌环境与水部及生产发展部）；2025-11-20 部门改组为规划发展与环境部（MPDyMA）后再次宣誓；2026 年下半年部门更名为生产与环境可持续部（MPSMAyA，其 2026-10 专访中自称隶属该部）。同时担任 CBD 国家联络点、CITES 指定管理机构（Autoridad Administrativa Titular）负责人，并为巴塞尔、水俣等公约登记联络人（CBD/CITES/InforMEA/水俣公约官方名录）。",
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000072",
            "person_name": "奥斯卡·马里奥·胡斯蒂尼亚诺·平托 (Óscar Mario Justiniano Pinto)",
            "relationship_type": "superior",
            "description": "现任生产与环境可持续部部长、其直属上级；2025-11-14 以部长身份主持其环境与生物多样性副部长就职宣誓，并强调公共管理应无意识形态压力、以护林为优先。"
        },
        {
            "person_id": "BO-PERSON-000075",
            "person_name": "维维安娜·马里斯卡尔·蒙塔尼奥 (Viviana Mariscal Montaño)",
            "relationship_type": "colleague",
            "description": "2025-11-14 同日宣誓就任饮用水与基础卫生副部长，同属环境事务副部长级团队；曾任圣克鲁斯环境工程师协会主席。"
        },
        {
            "person_id": None,
            "person_name": "阿尔弗雷迪·吉列尔莫·阿尔瓦雷斯·萨阿维德拉 (Alfredy Guillermo Álvarez Saavedra)",
            "relationship_type": "colleague",
            "description": "2025-11-14 同日宣誓就任玻利维亚森林与土地管理局（ABT）执行局长，在森林管控领域与其副部长职团队协作；其曾在 Añez 临时政府任环境与生物多样性副部长。"
        },
        {
            "person_id": None,
            "person_name": "何塞·路易斯·亚诺斯·罗查 (José Luis Llanos Rocha)",
            "relationship_type": "colleague",
            "description": "2025-11-20 规划发展与环境部改组后同批宣誓，任国家战略规划副部长。"
        }
    ],
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "Viceministerio de Medio Ambiente, Biodiversidad, Cambio Climático y Gestión y Desarrollo Forestal（机构账号）",
            "url": "https://www.facebook.com/Vicemedioambiente/",
            "source": "其领导的副环境部官方 Facebook 页面，非个人账号；高频发布其公务活动"
        },
        {
            "platform": "twitter_x",
            "account_name": "@minplanifica（部门机构账号）",
            "url": "https://x.com/minplanifica",
            "source": "规划发展与环境部/生产与环境可持续部官方 X 账号，非个人账号；多次发布其公务动态"
        }
    ],
    "social_accounts_note": "按 Facebook/X(Twitter)/Instagram/LinkedIn/TikTok/YouTube 六平台完成扫描，未发现可核实的个人社交账号；同名 Facebook 个人主页（jorgeernesto.avila.94）因无法确认身份未收录。",
    "family_members": [],
    "family_note": "公开报道未披露其家庭成员信息，留空。",
    "political_stances": [
        {
            "date": "2025-11-14",
            "topic": "森林保护与火灾预防",
            "stance_content": "就职时承诺将致力于保障自然资源的稳定与永续，保护森林及其生物多样性、流域、河流与湖泊，并强化森林火灾防控行动。",
            "source": "El País（玻利维亚）2025-11-14 任职报道"
        },
        {
            "date": "2026-10-03",
            "topic": "气候融资与碳市场立法",
            "stance_content": "支持国会审议中的《气候融资框架法》与《碳法》两项法案，称此前二十年「大地母亲商品化」禁令使玻利维亚无法参与碳市场等国际环境融资机制，主张通过立法提供法律安全与明确规则以吸引投资。",
            "source": "ANA Bolivia 专访（2026-10-05）"
        },
        {
            "date": "2026-10-03",
            "topic": "30x30 生物多样性保护目标",
            "stance_content": "称玻利维亚正构建实现 30x30 目标的路径，全国逾 35% 领土已纳入国家保护区系统，并将推动「其他有效区域保护措施（OMEC）」纳入《国家生物多样性战略 2026-2030》。",
            "source": "ANA Bolivia 专访（2026-10-05）"
        },
        {
            "date": "2026-10-03",
            "topic": "国际环境合作与国家形象",
            "stance_content": "主张以透明、可追溯和可核查成果重建国际社会信任，称已在伦敦和纽约展示新环境方针并将在 COP31 继续，批评过去的空洞言论使保护区和社区陷入脆弱状态。",
            "source": "ANA Bolivia 专访（2026-10-05）"
        }
    ],
    "political_stances_note": "其为职业法律 technocrat 出身，2025 年 11 月随罗德里戈·帕斯新政府上任；公开立场集中于环境融资、碳市场立法、火灾防控与国际合作重建信任。",
    "major_achievements": [
        {
            "date": "2025-11-14",
            "achievement": "获任命为玻利维亚环境、生物多样性、气候变化及森林管理与发展副部长，成为新政府环境事务主要负责人之一，并兼任多项国际环境公约国家联络点/履约机构负责人。",
            "organization": "玻利维亚生产与环境可持续部 (Ministerio de Producción Sostenible, Medio Ambiente y Agua)"
        },
        {
            "date": "2026",
            "achievement": "任内推动发布《2026 年森林火灾预防计划》，纳入《2026 年国家紧急计划》总体框架，构建预防、监测、早期预警、快速响应与灾后恢复一体化机制。",
            "organization": "玻利维亚生产与环境可持续部 (Ministerio de Producción Sostenible, Medio Ambiente y Agua)"
        },
        {
            "date": "2026-05",
            "achievement": "率政府代表团访秘鲁环境部，就碳市场建设、森林治理、气候融资、国家碳登记体系、REDD+ 机制及原住民参与生态治理开展交流，推进亚马逊跨境生态合作。",
            "organization": "玻利维亚生产与环境可持续部 (Ministerio de Producción Sostenible, Medio Ambiente y Agua)"
        },
        {
            "date": "2026-10",
            "achievement": "以东道方负责人身份推动拉美和加勒比环境基金网络（RedLAC）第 28 届大会（10 月 6-8 日，圣克鲁斯）在玻利维亚举办，提出「新环境议程」争取国际环境基金合作与投资。",
            "organization": "玻利维亚生产与环境可持续部 (Ministerio de Producción Sostenible, Medio Ambiente y Agua)"
        }
    ],
    "public_activities": [
        "2025-12-03 出席瑞典驻玻使馆主办的环境平台第三次研讨会并积极参与（瑞典使馆 Instagram）",
        "2026-02-19 参与查科省「玻利维亚计划（Plan Bolivia）」省级圆桌并致辞（部门 X 账号）",
        "2026-05-11 出席联合国森林论坛（UNFF）并阐述政府森林战略（副环境部 Facebook）",
        "2026-05 率团访问秘鲁环境部开展双边气候与森林合作会谈（华人头条-秘鲁）",
        "2026-09 出席纽约气候周期间 Puro.earth CDR Summit 2026 并发言（主办方 LinkedIn/官网）",
        "2026-09-28 至 10-02 赴罗马出席 FAO 林业委员会（COFO）相关活动，阐述玻利维亚森林与火灾预防立场（玻驻意大利使馆 Facebook）"
    ],
    "biography_summary": "豪尔赫·埃内斯托·阿维拉·安特洛（Jorge Ernesto Ávila Antelo），玻利维亚律师，在环境与林业领域拥有近35年从业经验，专长环境法、林业法与公共政策。曾长期任职于玻利维亚林业商会（CFB），官至总经理兼法务主管；2006至2007年以PODEMOS党籍代表圣克鲁斯省出任制宪议会议员，参与环境小组委员会工作；后任玻利维亚森林环境法协会主席，并从事国内外环境咨询与大学生态课程教学。2025年11月14日，他在罗德里戈·帕斯新政府中由部长奥斯卡·马里奥·胡斯蒂尼亚诺主持宣誓，出任环境、生物多样性、气候变化及森林管理与发展副部长；该职初属环境与水部，后随机构改组先后隶属规划发展与环境部及现生产与环境可持续部，同时担任《生物多样性公约》国家联络点及CITES指定管理机构负责人。任内主导2026年森林火灾预防议程，力推《气候融资框架法》与《碳法》立法，率团访秘推进亚马逊跨境气候合作，并以东道主负责人身份筹备在圣克鲁斯举办的RedLAC第28届大会，主张以透明、可核查成果重建国际社会对玻利维亚环境治理的信任。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": ["official_website", "government_directory", "news_search", "web_search", "social_media"],
        "notes": "核心事实（姓名、职务、任命时间、任职部门、履历）以官方传记页（规划部）+ El País/Unitel/ERBOL 等多家媒体 + ANA Bolivia 专访交叉验证；国际公约身份据 CBD/CITES/InforMEA/水俣公约官方名录页（搜索摘要确认，页面直读两次 502）；中文名据华人头条-秘鲁报道。存疑/留空：出生日期与出生地、教育院校、家庭成员均无公开资料；无个人社交账号（仅机构账号）；wikidata 查询超时未获条目。部门归属沿革（环境与水部→规划发展与环境部→生产与环境可持续部）据官方部名更替与本人 2026-10 专访口径。注意与索引中另一同名人物 BO-PERSON-000086（Jorge Ávila）区分，本条目为 Ávila Antelo 全名对应。",
        "quotes": [
            {
                "title": "Jorge Ernesto Ávila Antelo – Viceministro de Medio Ambiente, Biodiversidad, Cambios Climáticos y de Gestión y Desarrollo Forestal（官方传记页）",
                "url": "https://mpd.planificacion.gob.bo/index.php/informacion_institucional/content,2154.html"
            },
            {
                "title": "Posesionan a nuevos viceministros de Medio Ambiente y a los titulares de la ABT y el Sedem – El País（2025-11-14）",
                "url": "https://elpais.bo/nacional/20251114_posesionan-a-nuevos-viceministros-de-medio-ambiente-y-a-los-titulares-de-la-abt-y-el-sedem.html"
            },
            {
                "title": "Viceministro Ávila sobre expectativas del RedLAC – ANA Bolivia（2026-10-05 专访）",
                "url": "https://anabolivia.org/viceministro-avila-sobre-expectativas-del-redlac-se-trata-de-fortalecer-la-confianza-ante-la-comunidad-internacional-y-atraer-inversiones/"
            },
            {
                "title": "秘鲁与玻利维亚深化气候合作 共商亚马孙森林保护与碳市场建设 – 华人头条-秘鲁（2026-05-31）",
                "url": "https://www.52hrtt.com/ec/n/w/info/D1779175451683"
            },
            {
                "title": "Jorge Ernesto Avila Antelo | Minamata Convention on Mercury（公约名录页）",
                "url": "https://minamataconvention.org/en/people/jorge-ernesto-avila-antelo"
            },
            {
                "title": "National authorities | CITES Bolivia（CITES 国家机构名录）",
                "url": "https://cites.org/eng/parties/country-profiles/bo/national-authorities"
            },
            {
                "title": "El Ministro de Planificación posesiona a tres viceministros – ERBOL（2025-11-20）",
                "url": "https://erbol.com.bo/econom%C3%ADa/el-ministro-de-planificaci%C3%B3n-posesiona-tres-viceministros-y-les-pide-trabajar-con-rigor-y"
            },
            {
                "title": "PLAN DE PREVENCIÓN DE INCENDIOS FORESTALES 2026（官方 PDF）",
                "url": "https://www.planificacion.gob.bo/uploads/Plan_prevencion_IF_2026.pdf"
            }
        ]
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("written:", OUT)

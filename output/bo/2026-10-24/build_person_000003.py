# -*- coding: utf-8 -*-
"""Build BO-PERSON-000003 Fernando Hugo Aramayo Carrasco person profile JSON."""
import json
import os

OUT = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000003.json"

profile = {
    "person_id": "BO-PERSON-000003",
    "wikidata_qid": "Q136756222",
    "name": "Fernando Hugo Aramayo Carrasco",
    "name_en": "Fernando Hugo Aramayo Carrasco",
    "name_zh": "费尔南多·阿拉马约",
    "aliases": ["Fernando Aramayo", "费尔南多·胡戈·阿拉马约"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": "1974-02-19",
    "birth_place": "拉巴斯 (La Paz)",
    "contacts": [
        {
            "type": "website",
            "value": "https://presidencia.gob.bo/index.php/ministro-de-la-presidencia/",
            "source": "玻利维亚总统府部官网部长简历页"
        }
    ],
    "current_positions": ["玻利维亚总统府部部长"],
    "education": [
        {
            "institution": "玻利维亚圣保罗天主教大学 (Universidad Católica Boliviana San Pablo)",
            "degree": "bachelor",
            "field": "经济学",
            "start_date": None,
            "end_date": None
        },
        {
            "institution": "玻利维亚圣保罗天主教大学 (Universidad Católica Boliviana San Pablo)",
            "degree": "master",
            "field": "公共政策管理 (Gestión de Políticas Públicas)",
            "start_date": None,
            "end_date": None
        }
    ],
    "work_experience": [
        {
            "start_date": "2026-08-03",
            "end_date": None,
            "organization": "玻利维亚总统府部 (Ministerio de la Presidencia)",
            "org_id": "BO-GOV-006",
            "position": "总统府部部长"
        },
        {
            "start_date": "2025-11-09",
            "end_date": "2026-08-03",
            "organization": "玻利维亚外交部 (Ministerio de Relaciones Exteriores)",
            "org_id": "BO-GOV-002",
            "position": "外交部部长（Canciller）"
        },
        {
            "start_date": "2026-07-21",
            "end_date": "2026-08-03",
            "organization": "玻利维亚可持续文化旅游、民俗与美食部 (Ministerio de Turismo Sostenible, Culturas, Folklore y Gastronomía)",
            "org_id": "BO-GOV-011",
            "position": "部长（时任外长临时兼任）"
        },
        {
            "start_date": "2018",
            "end_date": None,
            "organization": "联合国开发计划署玻利维亚办事处 (PNUD Bolivia)",
            "org_id": None,
            "position": "经济政策、战略与创新负责人"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "联合国开发计划署玻利维亚办事处 (PNUD Bolivia)",
            "org_id": None,
            "position": "项目与机构管理协调员"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "联合国开发计划署拉丁美洲和加勒比区域办事处（美国纽约） (PNUD Oficina Regional para América Latina y el Caribe)",
            "org_id": None,
            "position": "民主与发展事务顾问"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "国际发展合作机构（德国国际合作机构GIZ、世界银行、美洲开发银行BID、瑞典国际开发合作署ASDI等）",
            "org_id": None,
            "position": "民主治理、和平建设、分权与公共政策顾问"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚国家统计局 (Instituto Nacional de Estadística de Bolivia)",
            "org_id": "BO-GOV-030",
            "position": "2001年全国人口与住房普查技术秘书"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚制宪大会 (Asamblea Constituyente de Bolivia)",
            "org_id": None,
            "position": "制宪大会技术协调员（2006年）"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000001",
            "person_name": "罗德里戈·帕斯·佩雷拉 (Rodrigo Paz Pereira)",
            "relationship_type": "superior",
            "description": "帕斯总统先后于2025-11-09任命其为外交部长、2026-08-03任命其为总统府部部长，视其为政府核心技术官僚骨干。"
        },
        {
            "person_id": "BO-PERSON-000025",
            "person_name": "埃克托·弗朗西斯科·万卡·古铁雷斯 (Héctor Francisco Huanca Gutiérrez)",
            "relationship_type": "subordinate",
            "description": "万卡原任外交部副部长，2026-08-03接替阿拉马约出任外交部长。"
        },
        {
            "person_id": "BO-PERSON-000094",
            "person_name": "何塞·路易斯·卢波·弗洛雷斯 (José Luis Lupo Flores)",
            "relationship_type": "colleague",
            "description": "阿拉马约于2026-08-03接替卢波出任总统府部部长；卢波随后获提名出任玻利维亚驻美洲国家组织（OEA）大使。"
        }
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Fernando Aramayo Carrasco",
            "url": "https://bo.linkedin.com/in/fernando-aramayo-carrasco-b9a80214",
            "source": "LinkedIn检索结果，职务显示为玻利维亚部长级官员"
        },
        {
            "platform": "twitter_x",
            "account_name": "FernandoAramayo (@Fer_Aramayo_C)",
            "url": "https://x.com/Fer_Aramayo_C",
            "source": "X账号简介自述「玻利维亚总统府部部长」；玻利维亚外交部、智利外长等多方官方账号@该账号"
        },
        {
            "platform": "instagram",
            "account_name": "fer_aramayo_c",
            "url": "https://www.instagram.com/fer_aramayo_c/",
            "source": "Instagram账号页（姓名Fernando Aramayo）；美众议员Diaz-Balart帖文以其外长身份@该账号"
        }
    ],
    "family_members": [],
    "political_stances": [
        {
            "date": "2025-11-11",
            "topic": "外交体制改革",
            "stance_content": "主张全面重组玻利维亚外交与外交政策体制架构：应「从地缘经济学和数字外交出发思考」，驻外使团「不应只承担政治职能，还应承担商业职能」，并快速定位市场、利用世界提供的竞争优势。",
            "source": "https://consulados.cancilleria.gob.bo/blog/embajadass_noticias/el-nuevo-canciller-fernando-aramayo-plantea-una-reestructuracion-integral-de-la-diplomacia-boliviana/"
        },
        {
            "date": "2025-11-11",
            "topic": "减贫与发展理念",
            "stance_content": "称「政府的目标不是管理危机，而是建设繁荣」「贫困不能靠给人们最低限度的期望来消除；我们的职责是创造条件，让每一个玻利维亚人都能选择自己的命运」。",
            "source": "https://consulados.cancilleria.gob.bo/blog/embajadass_noticias/el-nuevo-canciller-fernando-aramayo-plantea-una-reestructuracion-integral-de-la-diplomacia-boliviana/"
        },
        {
            "date": "2025-11",
            "topic": "玻利维亚—美国关系",
            "stance_content": "任外长前后推动玻美恢复大使级外交关系（时隔约17-18年）；2025-11-08就任外长前与美国副国务卿克里斯托弗·兰道会晤，宣布价值70万美元的抗艾药品与诊断设备捐赠，与2008年莫拉莱斯驱逐美大使的路线形成鲜明对比。",
            "source": "https://www.t13.cl/noticia/ex-ante/mundo/quien-fernando-aramayo-nuevo-canciller-bolivia-sus-desafios-chile-10-11-2025"
        },
        {
            "date": "2025-12",
            "topic": "对美经济合作与锂矿开放",
            "stance_content": "接受《华尔街日报》采访时表示，玻利维亚正向特朗普政府寻求金融支持，并将向外国投资者开放巨大的锂矿资源，以摆脱经济困境。",
            "source": "https://cn.wsj.com/articles/玻利维亚寄望借助锂矿和美国来摆脱经济困境-d8163237"
        },
        {
            "date": "2026-01",
            "topic": "国际引资与资源外交",
            "stance_content": "赴达沃斯世界经济论坛介绍引资政策与锂矿潜力，称玻利维亚锂资源极具吸引力，稀土等矿产与技术领域也引起外界浓厚兴趣。",
            "source": "https://www.br-cn.com/static/content/news/nm_news/2026-01-24/1464591341160896858.html"
        },
        {
            "date": "2026-08",
            "topic": "玻利维亚—智利关系",
            "stance_content": "其外长任内主要成果之一是推动玻利维亚与智利的外交接近。",
            "source": "https://eju.tv/2026/08/paz-posesiona-aramayo-y-huanca-como-ministros-de-la-presidencia-y-relaciones-exteriores/"
        },
        {
            "date": "2026-09",
            "topic": "金砖国家合作",
            "stance_content": "再次确认玻利维亚有意参加9月在印度举行的金砖国家峰会，称该国正努力「扩大融资和政治经济合作机制」。",
            "source": "https://bricscouncil.ru/zh/analytics/boliviya-i-briks-shag-vpered-dva-shaga-nazad"
        }
    ],
    "major_achievements": [
        {
            "date": "2001",
            "achievement": "担任2001年全国人口与住房普查技术秘书，负责这一国家重大统计进程的技术工作。",
            "organization": "玻利维亚国家统计局 (Instituto Nacional de Estadística de Bolivia)"
        },
        {
            "date": "2006",
            "achievement": "担任制宪大会技术协调员，深度参与2006年玻利维亚制宪大会进程。",
            "organization": "玻利维亚制宪大会 (Asamblea Constituyente de Bolivia)"
        },
        {
            "date": "2024",
            "achievement": "应邀出席智利「未来大会」（Congreso Futuro 2024），就人工智能时代的民主挑战发表演讲。",
            "organization": "智利未来大会 (Congreso Futuro)"
        },
        {
            "date": "2025-11-09",
            "achievement": "获总统罗德里戈·帕斯任命为外交部长；任内实现玻美关系时隔约17-18年恢复大使级外交关系，并推动玻智外交接近。",
            "organization": "玻利维亚外交部 (Ministerio de Relaciones Exteriores)"
        },
        {
            "date": "2026-08-03",
            "achievement": "转任总统府部部长，成为帕斯内阁中首位在任期内先后执掌三个部长职位的阁员，并配合推动内阁由14个部精简至12个部的机构改革。",
            "organization": "玻利维亚总统府部 (Ministerio de la Presidencia)"
        }
    ],
    "biography_summary": "费尔南多·乌戈·阿拉马约·卡拉斯科（Fernando Hugo Aramayo Carrasco，1974年2月19日生于拉巴斯）是玻利维亚经济学家、技术官僚型政治人物，现任总统府部部长。毕业于玻利维亚圣保罗天主教大学，持经济学学位及公共政策管理硕士学位，专长政治经济学、公共政策、冲突替代解决与国际合作管理。曾任联合国开发计划署（UNDP）玻利维亚办事处经济政策、战略与创新负责人及项目与机构管理协调员，并任UNDP拉美和加勒比区域办事处（纽约）民主与发展事务顾问，拥有25年以上国际合作经验，先后为德国国际合作机构（GIZ）、世界银行、美洲开发银行、瑞典国际开发合作署等工作，足迹遍及拉美、非洲与中东；曾任2001年全国人口与住房普查技术秘书、2006年制宪大会技术协调员。2025年11月9日被总统罗德里戈·帕斯任命为外交部长（接替塞琳达·索萨），任内推动玻美关系时隔约18年重启、玻智接近；2026年7月21日临时兼任可持续文化旅游部长；2026年8月3日转任总统府部部长（接替何塞·路易斯·卢波），被视为帕斯政府核心技术派阁员。",
    "profile": {
        "source_url": "https://upload.wikimedia.org/wikipedia/commons/0/02/Fernando_Aramayo_dic_2025.jpg",
        "local_path": None
    },
    "position_note": "任职序列：2025-11-09任外交部长→2026-07-21以DP 5659临时兼任可持续文化旅游、民俗与美食部部长→2026-08-03以DP 5668转任总统府部部长，外长职务由原副部长埃克托·万卡接任（DP 5669另任命万卡临时执掌旅游部）。任务背景所载外长任命法令DS 5486未在本次公开报道检索中直接核验到编号。",
    "education_note": "官方简历载其拥有公共政策管理硕士（Maestría en Gestión de Políticas Públicas）；据智利T13/ex-ante引述其简历，硕士亦毕业于玻利维亚圣保罗天主教大学，另曾在西班牙和墨西哥修读研究生文凭课程（diplomados），授予院校未披露。",
    "work_note": "另曾在多家非营利组织任职，长期从事冲突分析培训、对话调解（社会、政治与社会环境冲突）及社会经济领域研究（官方简历及T13报道）。注意区分同名者：玻利维亚另有农业经济学者Fernando Aramayo Arze及X账号@fernandoarama12（IICA协调员），均非本人。",
    "family_note": "据智利T13/ex-ante报道（2025-11-10），阿拉马约育有三名子女；配偶及子女姓名等详情未见于公开来源，故family_members留空。",
    "social_accounts_note": "六项平台扫描结果：确认LinkedIn、X（@Fer_Aramayo_C）、Instagram（@fer_aramayo_c）个人账号；未发现个人Facebook、TikTok、YouTube账号（Facebook上仅玻外交部与总统府部官方账号发布其活动信息）。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "wikipedia",
            "wikidata",
            "official_website",
            "news_search",
            "web_search",
            "social_media",
            "government_directory"
        ],
        "notes": "核心事实（出生日期1974-02-19拉巴斯、UCB经济学教育、PNUD任职、2025-11-09任外长、2026-07-21临时兼任旅游部长、2026-08-03任总统府部长）均有≥2独立来源交叉验证（西语/英语维基百科、总统府部官网简历、玻外交部官网、T13/ex-ante、eju.tv、Tarija Conecta、ABI）。中文名「费尔南多·阿拉马约」经中国外交部官网国家概况页确认沿用，新华网全名译作「费尔南多·胡戈·阿拉马约」已收入aliases。子女数仅单一来源（T13），家庭细节未核实。外长任命法令编号DS 5486未在公开报道中直接核验。2026-07-21兼任日期依据DP 5659签发日（周二）及任务参数，媒体报道多标注为7月22日。",
        "quotes": [
            {
                "title": "Fernando Aramayo - Wikipedia, la enciclopedia libre（西语维基百科）",
                "url": "https://es.wikipedia.org/wiki/Fernando_Aramayo"
            },
            {
                "title": "Fernando Aramayo - Wikipedia（英语维基百科）",
                "url": "https://en.wikipedia.org/wiki/Fernando_Aramayo"
            },
            {
                "title": "Ministro de la Presidencia - Presidencia del Estado Plurinacional de Bolivia（总统府部官网官方简历）",
                "url": "https://presidencia.gob.bo/index.php/ministro-de-la-presidencia/"
            },
            {
                "title": "El nuevo Canciller Fernando Aramayo plantea una reestructuración integral de la diplomacia boliviana - Cancillería de Bolivia（玻利维亚外交部官网）",
                "url": "https://consulados.cancilleria.gob.bo/blog/embajadass_noticias/el-nuevo-canciller-fernando-aramayo-plantea-una-reestructuracion-integral-de-la-diplomacia-boliviana/"
            },
            {
                "title": "Quién es Fernando Aramayo, el nuevo canciller de Bolivia (y sus desafíos con Chile) - T13/ex-ante（智利）",
                "url": "https://www.t13.cl/noticia/ex-ante/mundo/quien-fernando-aramayo-nuevo-canciller-bolivia-sus-desafios-chile-10-11-2025"
            },
            {
                "title": "Fernando Aramayo ocupa su tercer cargo en gabinete de Paz - eju.tv",
                "url": "https://eju.tv/2026/08/paz-posesiona-aramayo-y-huanca-como-ministros-de-la-presidencia-y-relaciones-exteriores/"
            },
            {
                "title": "¿Quién es Fernando Aramayo Carrasco? Ministro de Relaciones Exteriores - Tarija Conecta",
                "url": "https://tarijaconecta.bo/noticia/8150"
            },
            {
                "title": "玻利维亚寄望借助锂矿和美国来摆脱经济困境 - 华尔街日报中文网",
                "url": "https://cn.wsj.com/articles/玻利维亚寄望借助锂矿和美国来摆脱经济困境-d8163237"
            },
            {
                "title": "玻利维亚国家概况 - 中华人民共和国外交部（中文译名依据）",
                "url": "https://www.fmprc.gov.cn/web/gjhdq_676201/gj_676203/nmz_680924/1206_681022/1206x0_681024/"
            }
        ]
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("written:", OUT)

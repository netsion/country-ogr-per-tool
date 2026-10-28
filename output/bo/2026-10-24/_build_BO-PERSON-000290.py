# -*- coding: utf-8 -*-
"""Build person profile BO-PERSON-000290 (Julio Enrique Anglarill Serrate)."""
import json
import os

OUT = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000290.json"

profile = {
    "person_id": "BO-PERSON-000290",
    "wikidata_qid": None,
    "name": "Julio Enrique Anglarill Serrate",
    "name_en": "Julio Enrique Anglarill Serrate",
    "name_zh": "胡利奥·恩里克·安格拉里尔·塞拉特",
    "aliases": ["Julio Anglarill Serrate", "Julio Anglarill", "Dr. Julio Enrique Anglarill"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": "1970-07-01",
    "birth_place": None,
    "contacts": [],
    "current_positions": ["玻利维亚索菲亚食用油公司（索菲亚集团）总经理"],
    "education": [
        {
            "institution": "里约热内卢联邦乡村大学 (Universidade Federal Rural do Rio de Janeiro)",
            "degree": "professional",
            "field": "兽医学",
            "start_date": "1989",
            "end_date": "1994"
        },
        {
            "institution": "努尔大学 (Universidad Nur)",
            "degree": "master",
            "field": "工商管理",
            "start_date": "2003",
            "end_date": "2004"
        },
        {
            "institution": "康涅狄格大学 (University of Connecticut)",
            "degree": "other",
            "field": "禽类科学专科"
        },
        {
            "institution": "代文特动物卫生研究所 (Animal Health Institute Deventer)",
            "degree": "other",
            "field": "禽病理学专科"
        }
    ],
    "work_experience": [
        {
            "organization": "玻利维亚索菲亚食用油公司 (Granja Avícola Integral Sofía Ltda.)",
            "org_id": "BO-CORP-006",
            "position": "田间兽医",
            "start_date": "1994-07",
            "end_date": None
        },
        {
            "organization": "玻利维亚索菲亚食用油公司 (Granja Avícola Integral Sofía Ltda.)",
            "org_id": "BO-CORP-006",
            "position": "屠宰场生产经理",
            "start_date": None,
            "end_date": None
        },
        {
            "organization": "玻利维亚索菲亚食用油公司 (Granja Avícola Integral Sofía Ltda.)",
            "org_id": "BO-CORP-006",
            "position": "生产与运营经理",
            "start_date": None,
            "end_date": None
        },
        {
            "organization": "索菲亚食品公司（阿根廷萨尔塔） (Productos Alimenticios Sofía S.A.)",
            "org_id": None,
            "position": "总经理",
            "start_date": None,
            "end_date": "2014"
        },
        {
            "organization": "玻利维亚索菲亚食用油公司 (Granja Avícola Integral Sofía Ltda.)",
            "org_id": "BO-CORP-006",
            "position": "项目事业部总经理",
            "start_date": "2014",
            "end_date": "2023"
        },
        {
            "organization": "玻利维亚索菲亚食用油公司 (Granja Avícola Integral Sofía Ltda.)",
            "org_id": "BO-CORP-006",
            "position": "总经理",
            "start_date": "2023-03",
            "end_date": None
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000292",
            "person_name": "马里奥·伊格纳西奥·安格拉里尔·塞拉特 (Mario Ignacio Anglarill Serrate)",
            "relationship_type": "sibling",
            "description": "长兄（1968年生），2012年至2023年3月任索菲亚公司总经理，卸任后转任Anglarill集团主席"
        },
        {
            "person_id": "BO-PERSON-000291",
            "person_name": "奥斯卡·安格拉里尔·塞拉特 (Óscar Anglarill Serrate)",
            "relationship_type": "sibling",
            "description": "弟弟（1980年生），工业与系统工程师，2023年3月起出任公司新设副总经理（Subgerente General）"
        },
        {
            "person_id": "BO-PERSON-000293",
            "person_name": "胡安·卡洛斯·安格拉里尔·塞拉特 (Juan Carlos Anglarill Serrate)",
            "relationship_type": "sibling",
            "description": "弟弟（1973年生），农业经济学士，长期执掌畜牧事业部，分管禽类与生猪养殖屠宰板块"
        },
        {
            "person_id": None,
            "person_name": "里卡多·安格拉里尔·塞拉特 (Ricardo Anglarill Serrate)",
            "relationship_type": "sibling",
            "description": "弟弟（1977年生），企业管理学士，2015年起任公司创新与新业务事业部总经理，在CAINCO Leaders计划中代表索菲亚公司"
        },
        {
            "person_id": "BO-PERSON-000289",
            "person_name": "马里奥·安格拉里尔·萨尔瓦铁拉 (Mario Anglarill Salvatierra)",
            "relationship_type": "parent",
            "description": "父亲，1976年9月与妻子在圣克鲁斯共同创立索菲亚公司，2023年将公司管理权交给第二代"
        },
        {
            "person_id": None,
            "person_name": "迈达·塞拉特 (Maida Serrate de Anglarill)",
            "relationship_type": "parent",
            "description": "母亲，与丈夫共同创业；公司名「Sofía」取自父亲的母亲（胡利奥的祖母）之名"
        }
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Julio Enrique Anglarill",
            "url": "https://bo.linkedin.com/in/julio-enrique-anglarill-8854a69",
            "source": "LinkedIn搜索结果（MBA at Avicola Sofia, Bolivia）"
        }
    ],
    "family_members": [
        {
            "person_id": "BO-PERSON-000289",
            "name": "马里奥·安格拉里尔·萨尔瓦铁拉 (Mario Anglarill Salvatierra)",
            "relationship": "father",
            "industry_or_organization": "玻利维亚索菲亚食用油公司（创始人）"
        },
        {
            "person_id": None,
            "name": "迈达·塞拉特 (Maida Serrate de Anglarill)",
            "relationship": "mother",
            "industry_or_organization": "玻利维亚索菲亚食用油公司（联合创始人）"
        },
        {
            "person_id": None,
            "name": "帕特里夏·安德烈亚·马塔莫罗斯 (Patricia Andrea Matamoros de Anglarill)",
            "relationship": "spouse",
            "industry_or_organization": None
        },
        {
            "person_id": "BO-PERSON-000292",
            "name": "马里奥·伊格纳西奥·安格拉里尔·塞拉特 (Mario Ignacio Anglarill Serrate)",
            "relationship": "brother",
            "industry_or_organization": "Anglarill集团（主席）"
        },
        {
            "person_id": "BO-PERSON-000291",
            "name": "奥斯卡·安格拉里尔·塞拉特 (Óscar Anglarill Serrate)",
            "relationship": "brother",
            "industry_or_organization": "玻利维亚索菲亚食用油公司（副总经理）"
        },
        {
            "person_id": "BO-PERSON-000293",
            "name": "胡安·卡洛斯·安格拉里尔·塞拉特 (Juan Carlos Anglarill Serrate)",
            "relationship": "brother",
            "industry_or_organization": "玻利维亚索菲亚食用油公司（畜牧事业部总经理）"
        },
        {
            "person_id": None,
            "name": "里卡多·安格拉里尔·塞拉特 (Ricardo Anglarill Serrate)",
            "relationship": "brother",
            "industry_or_organization": "玻利维亚索菲亚食用油公司（创新与新业务事业部总经理）"
        }
    ],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2023-03",
            "achievement": "接替长兄马里奥·伊格纳西奥出任索菲亚公司总经理，完成家族企业向第二代的交接班",
            "organization": "玻利维亚索菲亚食用油公司 (Granja Avícola Integral Sofía Ltda.)"
        },
        {
            "date": "2023-03",
            "achievement": "就任后主导拓展宠物食品业务，宣布推出猫粮新品线Podium Cat及犬猫粮系列",
            "organization": "玻利维亚索菲亚食用油公司 (Granja Avícola Integral Sofía Ltda.)"
        },
        {
            "date": "2025-05-07",
            "achievement": "代表公司接受玻利维亚对外贸易协会（IBCE）表彰，表彰其近50年对国家粮食安全的贡献及行业领导地位",
            "organization": "玻利维亚对外贸易协会 (Instituto Boliviano de Comercio Exterior)"
        },
        {
            "date": "2026",
            "achievement": "主导公司创立50周年庆典系列活动（含Expocruz 2026「La Casa de Sofía」展馆），以家族第二代代表身份对外讲述企业史",
            "organization": "玻利维亚索菲亚食用油公司 (Granja Avícola Integral Sofía Ltda.)"
        }
    ],
    "biography_summary": "胡利奥·恩里克·安格拉里尔·塞拉特，玻利维亚最大食品企业之一索菲亚集团（Granja Avícola Integral Sofía Ltda.）总经理，创始人马里奥·安格拉里尔·萨尔瓦铁拉与迈达·塞拉特的五个子女中的次子。1989至1994年在巴西里约热内卢联邦乡村大学攻读兽医学，后于玻利维亚努尔大学获工商管理硕士（2003-2004），并在美国康涅狄格大学与荷兰代文特动物卫生研究所进修禽类科学及禽病理专科。1994年7月进入家族企业，从养鸡场田间兽医做起，历任屠宰场生产经理、生产与运营经理，后出任集团阿根廷萨尔塔姊妹公司Productos Alimenticios Sofía S.A.总经理，2014年起执掌项目事业部。2023年3月1日经兄弟间协商接替长兄马里奥·伊格纳西奥出任公司总经理，后者转任Anglarill集团主席。任内推动宠物食品等新品线扩张，2025年5月代表公司接受IBCE近50年粮食安全贡献表彰，2026年主导公司创立50周年庆典，并常以企业领袖身份出席Merco Bolivia等商界活动。",
    "birth_date_note": "阿根廷萨尔塔省官方公报（Boletín Oficial de Salta，2007-12-21刊， orden de publicación 41055）刊载的Productos Alimenticios Sofía S.A.公司登记文件载明「nacido el 01/7/1970」，按阿根廷DD/MM/YYYY日期惯例推定为1970年7月1日；该信息为单一官方公报来源，玻利维亚媒体未见出生日期报道",
    "name_zh_note": "未检索到中文媒体既有译名；「胡利奥·恩里克·安格拉里尔·塞拉特」为本项目人物清单拟定音译，与_name_index.json及BO-CORP-006组织档案一致",
    "spouse_note": "配偶Patricia Andrea Matamoros de Anglarill见2007年萨尔塔省官方公报公司登记文件（载明为首婚）；此后婚姻状况无公开更新信息",
    "education_note": "兽医（médico veterinario）学位与MBA来自其LinkedIn档案（Universidade Federal Rural do Rio de Janeiro兽医1989-1994；Universidad Nur MBA 2003-2004），并与El Deber专访中本人自述「我是兽医、持有企业管理硕士」互证；康涅狄格大学禽类专科与荷兰代文特动物卫生研究所禽病理专科来自本项目BO-CORP-006组织档案（原引公司公开资料），本次检索未能独立复核",
    "work_note": "职业路径综合本人El Deber专访（自述从养鸡场田间兽医起步、后管理屠宰场并开发新项目、曾任阿根廷萨尔塔公司总管理层、在公司任职20余年）与BO-CORP-006组织档案（1994年7月入职；2014-2023年任项目事业部总经理；阿根廷公司总经理任期约至2014年前）；2007年12月萨尔塔官方公报列其为阿根廷子公司候补董事（director suplente）并持840股",
    "family_note": "五兄弟排行与出生年份（Mario Ignacio 1968、Julio Enrique 1970、Juan Carlos 1973、Ricardo 1977、Óscar 1980）取自2007年萨尔塔省官方公报公司登记文件；母亲姓名部分媒体报道作Maida Serrate Arredondo（El Día）；注意区分兄弟角色，勿与父亲Mario Anglarill Salvatierra（创始人）及长兄Mario Ignacio（前任总经理）混淆",
    "position_note": "2023年3月1日正式就任总经理（El Deber专访），3月14-15日晚间仪式公开介绍（Economy.com.bo、Publiagro、Negocios Press）；其LinkedIn档案当前职位标注为「MBA at Avicola Sofia」",
    "social_accounts_note": "六平台扫描（LinkedIn/Facebook/Instagram/X/TikTok/YouTube）：仅核实个人LinkedIn档案；Facebook、Instagram、X、TikTok、YouTube未发现经核实的个人账号，涉及本人的帖文与视频均发布于公司账号（@sofia.bolivia）、商会（FEPSC、CAINCO）或媒体（Nueva Economía、Cedrovet、TuGuía、Bolivian Business）账号",
    "identity_note": "该公司总经理职位于2023年3月由兄长Mario Ignacio Anglarill Serrate（BO-PERSON-000292）交接而来；集团公司背景见BO-CORP-006（Industrias de Aceite Sofía）组织档案",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": ["news_search", "web_search", "social_media", "government_registry"],
        "notes": "总经理任命（2023-03-01就任）经El Deber、Economy.com.bo、Publiagro、Negocios Press及CAINCO/FEPSC商会账号等多渠道交叉证实；出生日期、配偶及五兄弟出生年份来自阿根廷萨尔塔省官方公报2007-12-21公司登记文件（单一定期官方出版物来源，玻媒未报道）；学历以LinkedIn档案为据并与本人专访互证，UConn与荷兰Deventer两专科仅见于组织档案、未能独立复核（已作标注）；未见Wikidata/Wikipedia条目，wikidata_qid为null；中文名无既有媒体译名，采用项目拟定音译；completeness_score约76，主要受限于无个人联系方式、无Wikidata/照片及无政治立场公开记录。玻利维亚公众人物公开信息以企业报道为主，客观难以达到85分以上。",
        "quotes": [
            {
                "title": "Julio Enrique Anglarill, gerente de Sofía: 「En el negocio de los alimentos nada es estático...」 — El Deber（2023-03-18专访，自述学历与职业路径）",
                "url": "https://eldeber.com.bo/edicion-impresa/julio-enrique-anglarill-gerente-de-sofia-en-el-negocio-de-los-alimentos-nada-es-estatico-y-hay-que-s_318118/"
            },
            {
                "title": "Julio Enrique Anglarill fue presentado como nuevo Gerente General de Sofía Ltda. — Economy.com.bo（2023-03-15，任命仪式及创始人交棒表态）",
                "url": "https://www.economy.com.bo/articulo/gerencia/julio-enrique-anglarill-fue-presentado-como-nuevo-gerente-general-sofia-ltda/20230315204427009537.html"
            },
            {
                "title": "Mario Ignacio y Julio Enrique Anglarill lideran la empresa Sofía con nuevos retos — Publiagro（2023-03-15，父母姓名及兄弟交接）",
                "url": "https://publiagro.com.bo/2023/03/mario-ignacio-y-julio-enrique-anglarill-lideran-la-empresa-sofia-con-nuevos-retos/"
            },
            {
                "title": "Boletín Oficial de Salta — Constitución de Productos Alimenticios Sofía S.A.（2007-12-21，官方公报：出生日期、配偶、五兄弟及股份登记）",
                "url": "https://boletinoficialsalta.gob.ar/Imprimir_doc.php?cXdlcnR5dGFibGE9QXw0MTA1NXF3ZXJ0eQ=="
            },
            {
                "title": "Mario Anglarill: 「En Bolivia se puede construir una empresa de clase mundial」 — El Deber（2026-09-08，创始人五十年访谈与家族传承）",
                "url": "https://eldeber.com.bo/dinero/mario-anglarill-bolivia-puede-construir-empresa-clase-mundial_1788828628"
            },
            {
                "title": "IBCE estrena Presidente: Luis Ernesto Castedo — IBCE（2025-05-08，IBCE表彰Sofía公司并由胡利奥·恩里克领奖）",
                "url": "https://ibce.org.bo/noticias-detalle.php?idNot=961"
            },
            {
                "title": "Julio Enrique Anglarill - MBA at Avicola Sofia — LinkedIn（个人档案：学历与现任职务）",
                "url": "https://bo.linkedin.com/in/julio-enrique-anglarill-8854a69"
            }
        ]
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("written:", OUT)

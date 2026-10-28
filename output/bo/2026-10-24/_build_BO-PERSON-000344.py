# -*- coding: utf-8 -*-
"""Build BO-PERSON-000344 Pamela Gil Dávila person profile."""
import json
import os

OUT = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons\BO-PERSON-000344.json"

profile = {
    "person_id": "BO-PERSON-000344",
    "wikidata_qid": None,
    "name": "Pamela Gil Dávila",
    "name_zh": "帕梅拉·希尔·达维拉",
    "name_en": "Pamela Gil Davila",
    "aliases": ["Pamela Gil Davila", "Pamela Gil"],
    "nationality": "BO",
    "gender": "female",
    "birth_date": None,
    "birth_place": None,
    "contacts": [],
    "current_positions": ["山谷私立大学圣克鲁斯校区学术副校长"],
    "education": [
        {
            "institution": "山谷私立大学 (Universidad Privada del Valle)",
            "degree": "bachelor",
            "field": "商业工程",
            "start_date": None,
            "end_date": None,
        }
    ],
    "work_experience": [
        {
            "start_date": "2025-12",
            "end_date": None,
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
            "org_id": "BO-ACAD-011",
            "position": "圣克鲁斯校区学术副校长",
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
            "org_id": "BO-ACAD-011",
            "position": "企业管理学院院长",
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "安第斯ProCredit银行 (Banco Los Andes ProCredit)",
            "org_id": None,
            "position": "管理职务",
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "商业银行 (Banco Mercantil)",
            "org_id": None,
            "position": "管理职务",
        },
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000339",
            "person_name": "贡萨洛·比森特·鲁伊斯·奥斯特里亚 (Gonzalo Vicente Ruiz Ostria)",
            "relationship_type": "superior",
            "description": "山谷私立大学校长，为其校级上级；2025年12月校方宣布任命其出任圣克鲁斯校区学术副校长，两人共同出席2026年9月Univalle NEXT+发布等活动",
        },
        {
            "person_id": "BO-PERSON-000341",
            "person_name": "迭戈·阿隆索·比列加斯·萨莫拉 (Diego Alonso Villegas Zamora)",
            "relationship_type": "colleague",
            "description": "同校学术副校长（Vicerrector Académico），同属Univalle校级领导团队",
        },
        {
            "person_id": "BO-PERSON-000342",
            "person_name": "桑德拉·马塞拉·鲁伊斯·奥斯特里亚 (Sandra Marcela Ruiz Ostria)",
            "relationship_type": "colleague",
            "description": "同校社会互动副校长，Univalle校级领导团队成员；系校长贡萨洛·鲁伊斯·奥斯特里亚之妹",
        },
        {
            "person_id": "BO-PERSON-000343",
            "person_name": "桑德罗·格雷罗·莫拉莱斯 (Sandro Guerrero Morales)",
            "relationship_type": "colleague",
            "description": "同校研究生副校长，Univalle校级领导团队成员",
        },
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Pamela Gil Davila",
            "url": "https://bo.linkedin.com/in/pamela-gil-davila-7888b114a",
            "source": "LinkedIn公开档案（Santa Cruz, Bolivia，500+联系人）；该账号发布过Agro Tech 2026学生表现祝贺等校园帖文",
        },
        {
            "platform": "instagram",
            "account_name": "@pamelagildavila",
            "url": "https://www.instagram.com/pamelagildavila/",
            "source": "Instagram公开档案（1.1K+粉丝，关注767，发帖86条）",
        },
    ],
    "family_members": [
        {
            "person_id": None,
            "name": "博里斯·乌格里诺维奇 (Boris Ugrinovic)",
            "relationship": "spouse",
            "industry_or_organization": None,
        },
        {
            "person_id": None,
            "name": "尼古拉斯 (Nicolás)",
            "relationship": "son",
            "industry_or_organization": None,
        },
        {
            "person_id": None,
            "name": "安德烈亚 (Andrea)",
            "relationship": "daughter",
            "industry_or_organization": None,
        },
    ],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2025-12",
            "achievement": "经山谷私立大学（Univalle）官方宣布出任圣克鲁斯校区学术副校长（Vicerrectora Sede Académica Santa Cruz），执掌该校近年最大投资项目——圣克鲁斯Eco-Smart生态智慧校区（一期约6万平方米，现有学生3000余人）",
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
        },
        {
            "date": "2026-03",
            "achievement": "获任2026年玻利维亚艾菲奖（Effie Awards Bolivia 2026）组委会专员（Comisario）",
            "organization": "玻利维亚艾菲奖 (Effie Awards Bolivia)",
        },
        {
            "date": "2026-06",
            "achievement": "在校区为获全国Abrapalabra 2026文学竞赛首奖的校友Laura Baldiviezo Orgaz举办致敬活动，并介绍Univalle毕业生追踪网络（Alumni Univalle Bolivia）",
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
        },
        {
            "date": "2026-09-22",
            "achievement": "参与校方与玻利维亚意大利工业商会（CBICI）在意大利设计日2026框架下的合作签署（含两个研究生项目的整合）",
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
        },
        {
            "date": "2026-09-28",
            "achievement": "代表学校领取智力功绩（mérito intelectual）表彰",
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
        },
    ],
    "biography_summary": (
        "帕梅拉·希尔·达维拉（Pamela Gil Dávila），玻利维亚学术管理者，现任山谷私立大学（Univalle）圣克鲁斯校区学术副校长，"
        "2025年12月经校方正式宣布就任，执掌该校近年最大投资项目——圣克鲁斯Eco-Smart生态智慧校区（一期约6万平方米，学生3000余人）的学术事务。"
        "她毕业于山谷私立大学商业工程（Ingeniería Comercial）专业，此前在安第斯ProCredit银行、商业银行等金融机构及保险业担任管理职务多年，"
        "后转入学术界，2025年8月已任Univalle企业管理学院院长，同年12月升任圣克鲁斯校区学术副校长。"
        "任内她推动校企联动、创新生态、国际化与学术卓越建设，倡导将可持续发展融入培养方案（2026年以校园方身份参与TrendTalks商业可持续发展领袖论坛），"
        "同年3月出任2026年玻利维亚艾菲奖组委会专员，9月参与校方与玻利维亚意大利工业商会的合作签署。"
        "她公开倡导女性领导力，指出Univalle学生与教师中女性占比超过50%，并支持年轻母亲完成学业。丈夫为Boris Ugrinovic，育有一子一女。"
    ),
    "birth_date_note": "El Deber 2026-04-22专访称其时年50岁（据此推算约1975-1976年出生）；未获精确出生日期，故birth_date留空。",
    "education_note": "本科学历为商业工程（Ingeniería Comercial），毕业于山谷私立大学（El Deber专访称其为「titulada de la Universidad Privada del Valle」）；项目组织档案BO-ACAD-011（源自Univalle官网当局页）列其头衔为Lic. M.Sc.，提示具有硕士学位，但硕士就读院校与专业未获可靠来源，故未单列学位条目。",
    "family_note": "据El Deber 2026-04-22专访：丈夫Boris Ugrinovic；一子Nicolás（时年29岁）、一女Andrea（时年25岁）；子女仅公开教名，姓氏未公开。",
    "name_zh_note": "未检索到中文媒体既有译名；「帕梅拉·希尔·达维拉」沿用本项目_name_index.json与BO-ACAD-011组织档案已注册译名（Gil按西语发音[xil]音译为「希尔」）。",
    "social_accounts_note": "已完成6平台扫描：LinkedIn与Instagram个人账号确认（见social_accounts）；存在同名个人Facebook账号（活跃于Boliviana de Aviación、univallesc等帖子评论区），但未获取稳定主页URL，未收录；未发现X/Twitter、TikTok、YouTube个人账号。JCI Bolivia（TikTok/YouTube）、Effie Awards Bolivia（Facebook）等机构账号多次致谢其支持。",
    "collection_meta": {
        "collection_date": "2026-10-27",
        "phase": "phase4_person_profile",
        "data_sources": ["web_search", "news_search", "social_media"],
        "notes": (
            "数据来源与确认：核心事实（职务、就任时间、教育背景、银行履历、家庭）经El Deber长篇专访（2026-04-22）、Univalle Santa Cruz官方Facebook/LinkedIn任命公告（2025-12-01）、"
            "economy.com.bo两篇报道（2026-06-02、2026-09-17）等多源交叉验证；姓名重音「Dávila」经economy.com.bo两处全文及Univalle官方帖确认。"
            "消歧：以「Univalle圣克鲁斯校区学术副校长」职务为锚，结合Univalle官方nombramiento公告与El Deber同名专访确认为同一人，排除玻利维亚其他Pamela Dávila/Gil同名者。"
            "存疑未采信：①2021年3月Unifranz研究生院生日帖提及同事「Pamela」，疑似其曾任职Unifranz，仅单一线索；②硕士学历仅有「Lic. M.Sc.」头衔佐证，院校专业不详；"
            "③Instagram 2020年一条评论疑似显示其更早担任副校长，但搜索快照混杂发帖与评论时间，证据不足。"
            "Univalle官网直接抓取多次失败（502/404），官网信息经项目组织档案BO-ACAD-011（源自官网当局页，含官方职务头衔Vicerrectora Sede Académica Santa Cruz及Lic. M.Sc.头衔）转引核证。"
            "completeness_score=67：校区副校长公开信息有限（无公开精确出生日期、联系方式、硕士院校信息，无政治立场表态），未达85分目标但高于45分可接受线，属客观上限。"
        ),
        "quotes": [
            {
                "title": "Pamela Gil promueve el liderazgo femenino - El Deber Para Ellas（2026-04-22专访：年龄、家庭、教育、银行履历）",
                "url": "https://eldeber.com.bo/para-ellas/pamela-gil-promueve-liderazgo-femenino_1776799276",
            },
            {
                "title": "Pamela Gil asume como Vicerrectora de la Sede Santa Cruz - Univalle Santa Cruz官方Facebook（2025-12-01任命公告）",
                "url": "https://www.facebook.com/univallesc/posts/pamela-gil-asume-como-vicerrectora-de-la-sede-santa-cruz-iniciando-una-etapa-mar/1307706121371002/",
            },
            {
                "title": "Univalle Santa Cruz LinkedIn官方nombramiento公告（2025-12-01）",
                "url": "https://es.linkedin.com/posts/univalle-santa-cruz_univalle-se-complace-en-informar-a-toda-la-activity-7401373811658477568-7GBp",
            },
            {
                "title": "Laura Baldiviezo Orgaz…mujeres palliris - Economy（2026-06-02：vicerrectora de la sede Santa Cruz，Pamela Gil Dávila致辞与Alumni网络）",
                "url": "https://www.economy.com.bo/articulo/life/laura-baldiviezo-orgaz-transforma-memoria-mujeres-palliris-obra-premiada-nivel-nacional/20260602170015022735.html",
            },
            {
                "title": "Convocan a creativos bolivianos…nueva marca turística - Economy（2026-09-17：玻利维亚国家旅游品牌Hub Creativo发布）",
                "url": "https://www.economy.com.bo/articulo/economia/convocan-creativos-bolivianos-construir-campana-nueva-marca-turistica-1/20260917163854024101.html",
            },
            {
                "title": "Trendsetter Bolivia LinkedIn帖（2026-06-20：TrendTalks可持续领导力论坛，其可持续教学融合表态）",
                "url": "https://es.linkedin.com/posts/trendsetter-bolivia_pamela-gil-davila-vicerrectora-univalle-activity-7474267818272776192-fwAj",
            },
            {
                "title": "Colegio de Ingenieros Comerciales & Ingenieros en Marketing y Publicidad祝贺nombramiento - Instagram（2025-11-21）",
                "url": "https://www.instagram.com/p/DRVEppDCYw5/",
            },
            {
                "title": "Pamela Gil asume el rol de Comisario de Effie Awards Bolivia 2026 - Effie Awards Bolivia Facebook（2026-03-18）",
                "url": "https://www.facebook.com/EffieAwardsBolivia/posts/pamela-gil-vicerrectora-de-univalle-santa-cruz-asume-el-rol-de-comisario-de-effi/122249304650293198/",
            },
            {
                "title": "Univalle Santa Cruz recibe reconocimiento por su mérito intelectual - Univalle Santa Cruz Facebook（2026-09-28）",
                "url": "https://www.facebook.com/univallesc/posts/univalle-santa-cruz-recibe-reconocimiento-por-su-m%C3%A9rito-intelectualla-universida/1564009082407370/",
            },
            {
                "title": "Pamela Gil, directora de la Facultad de Ciencias Empresariales de Univalle - SiempreLibres Facebook视频（2025-08-05）",
                "url": "https://www.facebook.com/SiempreLibres1825/videos/en-el-marco-del-bicentenario-de-bolivia-pamela-gil-directora-de-la-facultad-de-c/771675935541162/",
            },
            {
                "title": "Diseñar el futuro sin borrar el pasado: Italian Design Day 2026 - Nueva Economía（2026-10-15）",
                "url": "https://nuevaeconomia.com.bo/news/disear-el-futuro-sin-borrar-el-pasado-el-desafo-que-plante-el-italian-design-day-2026",
            },
        ],
    },
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE:", OUT)
print("bytes:", os.path.getsize(OUT))

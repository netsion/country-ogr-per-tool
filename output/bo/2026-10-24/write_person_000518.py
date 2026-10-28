# -*- coding: utf-8 -*-
"""Build BO-PERSON-000518 (Héctor Alejandro Alarcón Antezana) person profile JSON."""
import json
import os

OUT_DIR = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons"
OUT_PATH = os.path.join(OUT_DIR, "BO-PERSON-000518.json")

profile = {
    "person_id": "BO-PERSON-000518",
    "wikidata_qid": None,
    "name": "Héctor Alejandro Alarcón Antezana",
    "name_en": "Héctor Alejandro Alarcón Antezana",
    "name_zh": "埃克托·亚历杭德罗·阿拉尔孔·安特萨纳",
    "name_zh_note": "中文译名沿用本项目 _name_index.json 中同名既有条目（BO-PERSON-000514）的译名「埃克托·亚历杭德罗·阿拉尔孔·安特萨纳」；西语/英语/中文公开检索未发现其他权威华文媒体译名。",
    "aliases": [],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_date_note": "未找到可靠出生日期来源。2023年陆军司令部礼宾指南文档（Scribd 用户上传）中其姓名旁标注「02-AGO」，疑为生日8月2日，但无法核实，故 birth_date 留空。",
    "birth_place": None,
    "military_rank": "General de División (Gral. Div.)，2026-06 由 General de Brigada (Gral. Brig.) 晋升",
    "current_positions": ["玻利维亚陆军总司令"],
    "work_experience": [
        {
            "start_date": "2025-11-13",
            "end_date": None,
            "organization": "玻利维亚陆军 (Ejército de Bolivia)",
            "org_id": "BO-MIL-002",
            "position": "陆军总司令",
            "is_current": "true",
            "description": "2025年11月13日在拉巴斯克马多宫（Palacio Quemado）由总统罗德里戈·帕斯·佩雷拉主持宣誓就任，与武装部队总司令巴尔德拉马等同批组成帕斯政府新军事高层；2026年6月18日经第5632号最高法令（DS 5632）确认留任。",
            "source": "El Deber (2025-11-13, 2026-06-19)；Correo del Sur (2026-06-19)"
        }
    ],
    "education": [],
    "education_note": "公开来源未披露其军事院校教育与学历信息，无可核实来源，故留空。",
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000001",
            "person_name": "罗德里戈·帕斯·佩雷拉 (Rodrigo Paz Pereira)",
            "relationship_type": "superior",
            "description": "玻利维亚总统兼宪法意义上的武装部队大元帅（Capitán General）。2025年11月13日主持其陆军总司令就职宣誓，2026年6月18日以第5632号最高法令确认其留任。"
        },
        {
            "person_id": "BO-PERSON-000516",
            "person_name": "维克托·乌戈·巴尔德拉马·克萨达 (Víctor Hugo Balderrama Quezada)",
            "relationship_type": "superior",
            "description": "武装部队总司令（Comandante en Jefe de las Fuerzas Armadas），为其军事指挥链上的直接上级。两人于2025年11月13日同日就任，并同批获 DS 5632 留任。"
        },
        {
            "person_id": "BO-PERSON-000004",
            "person_name": "埃内斯托·阿米卡尔·胡斯蒂尼亚诺·乌尔塔多 (Ernesto Amilcar Justiniano Hurtado)",
            "relationship_type": "superior",
            "description": "国防部长，为其民事领导上级；2026年6月主持其晋升为师长（General de División），在维阿恰军营爆炸事件处理中与其立场一致（均支持执行警戒任务的阿尔瓦拉多上校）。"
        },
        {
            "person_id": "BO-PERSON-000515",
            "person_name": "何塞·威尔逊·桑切斯·贝拉斯克斯 (José Wilson Sánchez Velásquez)",
            "relationship_type": "subordinate",
            "description": "陆军参谋长（Jefe de Estado Mayor General del Ejército），为其在陆军司令部内的主要副手。"
        },
        {
            "person_id": "BO-PERSON-000517",
            "person_name": "贡萨洛·埃德温·鲁伊斯·西斯内罗斯 (Gonzalo Edwin Ruiz Cisneros)",
            "relationship_type": "colleague",
            "description": "武装力量总参谋长（Jefe de Estado Mayor del Comando en Jefe），同批于2025年11月就任并同获 DS 5632 留任。"
        },
        {
            "person_id": "BO-PERSON-000519",
            "person_name": "塞尔希奥·费尔南多·洛拉·阿劳奥斯 (Sergio Fernando Lora Araoz)",
            "relationship_type": "colleague",
            "description": "空军总司令，与其同批就任并同获 DS 5632 留任。"
        },
        {
            "person_id": "BO-PERSON-000520",
            "person_name": "埃内斯托·阿达利德·阿尔法罗·帕尔马 (Ernesto Adalid Alfaro Palma)",
            "relationship_type": "colleague",
            "description": "海军总司令，与其同批就任并同获 DS 5632 留任。"
        },
        {
            "person_id": None,
            "person_name": "埃德蒙多·诺维利奥·阿吉拉尔 (Edmundo Novillo Aguilar)",
            "relationship_type": "other",
            "description": "前国防部长（阿尔塞政府）。2026年9月11日阿拉尔孔代表陆军就9月4日维阿恰「玻利瓦尔」防空炮兵团爆炸事故，以涉嫌过失杀人（homicidio culposo）与渎职（incumplimiento de deberes）向检察院对其提起刑事控告（9月28日通报对控告材料进行补救后继续推进）。"
        }
    ],
    "social_accounts": [],
    "social_accounts_note": "对 facebook / x(twitter) / linkedin / instagram / tiktok / youtube 六项平台扫描未发现其个人社交账号；其公开活动影像由玻利维亚陆军官方账号发布（Facebook @ejercitodeboliviaforjadordelapatria、Instagram、TikTok @ejtobolivia），非本人账号，故不录入。",
    "family_members": [],
    "family_note": "公开来源未查到其配偶、子女等家庭成员信息。",
    "political_stances": [
        {
            "date": "2026-09-09",
            "topic": "维阿恰爆炸事件中的军民关系争议",
            "stance_content": "就副总统埃德曼·拉拉指控负责维阿恰军营警戒的罗纳德·阿尔瓦拉多·佩雷多上校「不服从」一事，阿拉尔孔公开支持该上校，称其「只是执行了被赋予的任务」，并称「错误的命令不应执行」；主张危险区出入限制应适用于包括官员在内的所有人，同时表示军方优先事项是搜寻爆炸中失踪的5名军人、陪伴其家属，避免卷入政治纷争。",
            "source": "Erbol 采访 (2026-09-09)"
        },
        {
            "date": "2026-04",
            "topic": "对智利军事合作与军队国际交流",
            "stance_content": "访智接受授勋时公开表态：代表玻利维亚陆军感谢智利陆军，称两国军事友谊与合作「始于亚松森美洲国家会议」，应继续通过交流巩固机构间合作，「始终以尊重、职业精神及对两国和平与发展的承诺为框架」；主张玻利维亚陆军与邻国军队建立稳定的信任关系。",
            "source": "Infodefensa (2026-04-12)；智利陆军官网 (2026-04-10)"
        }
    ],
    "major_achievements": [
        {
            "date": "2025-11-13",
            "achievement": "被总统罗德里戈·帕斯任命并宣誓就任玻利维亚陆军总司令，成为帕斯政府2025年11月组建的新一届军事高层（Alto Mando Militar）成员。",
            "organization": "玻利维亚陆军 (Ejército de Bolivia)"
        },
        {
            "date": "2026-04",
            "achievement": "正式访问智利期间，由智利陆军总司令佩德罗·瓦雷拉将军授予「胜利十字勋章」（Cruz de la Victoria）——智利陆军授予友好国家军队最高领导人的最高荣誉；期间参观智利战争学院与奥希金斯军事学校。",
            "organization": "智利陆军 (Ejército de Chile)"
        },
        {
            "date": "2026-06-15",
            "achievement": "由国防部长埃内斯托·胡斯蒂尼亚诺正式宣布由准将（General de Brigada）晋升为师长（General de División）。",
            "organization": "玻利维亚国防部 (Ministerio de Defensa)"
        },
        {
            "date": "2026-06-18",
            "achievement": "经第5632号最高法令（DS 5632）确认留任陆军总司令，随玻利维亚武装力量晋升整编后新指挥结构一道获官方正式化。",
            "organization": "玻利维亚总统 (Presidente de Bolivia)"
        }
    ],
    "public_activities": [
        "2026-04：访问智利圣地亚哥，参观智利战争学院与奥希金斯军事学校，接受智利陆军「胜利十字勋章」授勋。",
        "2026-06-29：视察陆军航空连（据玻利维亚陆军官方Facebook）。",
        "2026-09：维阿恰「玻利瓦尔」防空炮兵团9月4日连环爆炸事故后，多次向媒体通报搜救失踪军人进展，宣布军方保险承担受伤军人全部费用，并部署核查全国其他团级单位爆炸物储存状况。",
        "2026-09-11：代表陆军就维阿恰爆炸事故对前防长诺维利奥提起刑事控告；2026-09-28：通报控告材料经补救后继续推进，并公布院内信息汇总（sumarios）结果。"
    ],
    "biography_summary": "埃克托·亚历杭德罗·阿拉尔孔·安特萨纳（Héctor Alejandro Alarcón Antezana）是玻利维亚陆军将领、现任玻利维亚陆军总司令。2025年11月13日，他在拉巴斯克马多宫由新任总统罗德里戈·帕斯·佩雷拉主持宣誓就任陆军总司令，与武装部队总司令巴尔德拉马等同批组成帕斯政府新军事高层。就任时军衔为准将（General de Brigada），2026年6月15日由国防部长胡斯蒂尼亚诺宣布晋升为师长（General de División），6月18日第5632号最高法令将其留任正式化。任内重要事件包括：2026年4月正式访问智利并获智利陆军最高荣誉「胜利十字勋章」；2026年9月4日维阿恰军营爆炸事故后指挥搜救失踪军人、承诺军险承担伤员费用，并代表陆军于9月11日就事故对前防长诺维利奥提起过失杀人与渎职刑事控告；在副总统拉拉与警戒军官冲突中公开力挺下属，主张「错误的命令不应执行」。其出生日期、军事教育背景及家庭成员等个人信息暂无公开可靠来源。",
    "contacts": [
        {
            "type": "website",
            "value": "https://ejercito.mil.bo",
            "source": "其执掌的玻利维亚陆军总司令部官方网址（机构渠道，非个人联系方式）"
        }
    ],
    "profile": {
        "source_url": "https://www.ejercito.cl/resources/cache/4/3/8/e/3/438e324b47d7411f144c3a5a41d6b772abedc335.jpeg",
        "local_path": None
    },
    "profile_note": "照片为智利陆军官网2026年4月10日报道中「玻利维亚陆军总司令获授胜利十字勋章」配图（授勋仪式新闻照，非官方标准像）；本地下载被目标站反爬拦截（返回HTML），故 local_path 置空。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "wikipedia",
            "news_search",
            "web_search",
            "government_registry",
            "social_media"
        ],
        "completeness_score": 0,
        "notes": "数据来源：精读10个独立来源全文（El Deber 2025-11-13任命与2026-06-19留任报道、Correo del Sur DS 5632报道、玻利维亚陆军官网Autoridades Militares页、Erbol 2025-11-13任命与2026-09-09采访、Infodefensa 2026-04-12访智受勋报道、Opinion 2026-09-11控告报道、智利陆军官网2026-04-10授勋报道、西语Wikipedia Ejército de Bolivia条目），另以Gaceta Oficial DS 5632原文PDF与国防部Instagram等交叉核证。关键事实（任命日期、留任、军衔、控告事件）均有≥2独立来源。存疑/留空字段：出生日期（仅Scribd礼宾文档疑含「02-AGO」线索，未核实故留空）、出生地、教育经历、家庭成员均查无可靠来源；Wikidata无本人条目（wikidata_qid=null）；六平台扫描未发现个人社交账号。completeness_score偏低系军人个人信息客观不可得（评分项中education/social_accounts/family_members/birth等约30分无公开来源，禁止编造），实际可查证维度（职务、军衔、成就、关系、立场、生平摘要）均已填满。name_zh 沿用项目索引既有译名（BO-PERSON-000514同名条目）。军衔时间线：2025-11就任时为准将（智利陆军2026-04报道及陆军官方2026-02帖文均称Gral. Brig.），2026-06-15晋升师长、6-18 DS 5632正式化，故 military_rank 取 General de División。",
        "quotes": [
            {
                "title": "Rodrigo Paz posesiona al nuevo Alto Mando Militar y anuncia una nueva era - El Deber (2025-11-13)",
                "url": "https://eldeber.com.bo/pais/rodrigo-paz-posesiono-nuevo-alto-mando-militar_1763066658"
            },
            {
                "title": "En medio de la crisis en Bolivia, Rodrigo Paz ratifica al Alto Mando Militar - El Deber (2026-06-19)",
                "url": "https://eldeber.com.bo/pais/medio-crisis-bolivia-rodrigo-paz-ratifica-alto-mando-militar_1781869705"
            },
            {
                "title": "Presidente promulga decreto que oficializa nuevo alto mando militar tras ascensos - Correo del Sur (2026-06-19)",
                "url": "https://correodelsur.com/politica/20260619/presidente-promulga-decreto-que-oficializa-nuevo-alto-mando-militar-tras-ascensos.html"
            },
            {
                "title": "Autoridades Militares - Comandante General del Ejército - Ejército de Bolivia (官网)",
                "url": "https://ejercito.mil.bo/then3wpag/template_e_commerce/mando.php"
            },
            {
                "title": "Decreto Presidencial N° 5632 - Gaceta Oficial de Bolivia",
                "url": "http://www.gacetaoficialdebolivia.gob.bo/normas/descargarNrms/281244"
            },
            {
                "title": "El Ejército de Chile recibe la visita del general Alarcón del Ejército de Bolivia y le otorga la Cruz de la Victoria - Infodefensa (2026-04-12)",
                "url": "https://www.infodefensa.com/texto-diario/mostrar/5841300/ejercito-chile-recibe-visita-general-alarcon-ejercito-bolivia-otorga-cruz-victoria"
            },
            {
                "title": "「Órdenes mal dadas no se cumplen」: Comandante del Ejército responde a impase con Lara - Erbol (2026-09-09)",
                "url": "https://erbol.com.bo/seguridad/%E2%80%9C%C3%B3rdenes-mal-dadas-no-se-cumplen%E2%80%9D-comandante-del-ej%C3%A9rcito-responde-impase-con-lara"
            },
            {
                "title": "Ejército presenta querella contra exministro Novillo por explosiones en Viacha - Los Tiempos/Opinión (2026-09-11)",
                "url": "https://www.opinion.com.bo/pais/ejercito-presenta-querella/20260911215449996083.html"
            },
            {
                "title": "Ejército de Bolivia - Wikipedia (es)",
                "url": "https://es.wikipedia.org/wiki/Ej%C3%A9rcito_de_Bolivia"
            },
            {
                "title": "Comandante General del Ejército de Bolivia recibió condecoración 「Cruz de la Victoria」 - Ejército de Chile (2026-04-10)",
                "url": "https://www.ejercito.cl/prensa/visor/comandante-general-del-ejercito-de-bolivia-recibio-condecoracion-cruz-de-la-victoria"
            },
            {
                "title": "El ministro de Defensa, Ernesto Justiniano, oficializó el ascenso al grado de General de División: Héctor Alejandro Alarcón Antezana - Instagram (2026-06-15)",
                "url": "https://www.instagram.com/reel/DZmwF1qA3c7/"
            }
        ]
    }
}

os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE:", OUT_PATH)
print("bytes:", os.path.getsize(OUT_PATH))

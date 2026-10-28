# -*- coding: utf-8 -*-
"""Write person profile BO-PERSON-000100 (Alberto Daza Quezada). v2 enriched."""
import json
import os

OUT_DIR = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons"
OUT_PATH = os.path.join(OUT_DIR, "BO-PERSON-000100.json")

profile = {
    "person_id": "BO-PERSON-000100",
    "wikidata_qid": None,
    "name": "Alberto Daza Quezada",
    "name_en": "Alberto Daza Quezada",
    "name_zh": None,
    "aliases": ["Alberto Daza", "General Alberto Daza Quezada"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": "科恰班巴 (Cochabamba)",
    "contacts": [],
    "current_positions": [],
    "education": [],
    "work_experience": [
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚国家水球队 (Selección Nacional de Waterpolo de Bolivia)",
            "org_id": None,
            "position": "水球运动员（国家队选手）"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚陆军 (Ejército de Bolivia)",
            "org_id": "BO-MIL-002",
            "position": "职业军官（以陆军准将军衔退役）"
        },
        {
            "start_date": "2011",
            "end_date": "2013",
            "organization": "玻利维亚武装力量联合指挥部 (Comando Conjunto de las Fuerzas Armadas)",
            "org_id": None,
            "position": "联合指挥部司令"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚跳伞联合会 (Federación Boliviana de Paracaidismo)",
            "org_id": None,
            "position": "首任主席（联合创始成员）"
        },
        {
            "start_date": "2017-05-17",
            "end_date": "2019-12",
            "organization": "玻利维亚体育部 (Ministerio de Deportes)",
            "org_id": "BO-GOV-020",
            "position": "体育副部长 (Viceministro de Deportes)"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000098",
            "person_name": "蒂托·蒙塔尼奥 (Tito Rolando Montaño Rivera)",
            "relationship_type": "superior",
            "description": "时任玻利维亚体育部长，2017年5月17日在体育部礼堂主持达萨的体育副部长就职宣誓；两人作为正副部长共事至2019年底政府更迭。"
        },
        {
            "person_id": None,
            "person_name": "马尔科·奥尔特加 (Marco Ortega)",
            "relationship_type": "colleague",
            "description": "2019年12月6日在过渡政府（体育部长米尔顿·纳瓦罗任内）被任命接替达萨出任体育副部长，达萨随之去职。"
        },
        {
            "person_id": None,
            "person_name": "马塞洛·奥尔图贝 (Marcelo Ortubé)",
            "relationship_type": "colleague",
            "description": "2017年被任命为2018年科恰班巴南美运动会组织委员会（Codesur）主任；其转任造成的副部长职位空缺由达萨填补，任内两人协作筹备运动会。"
        },
        {
            "person_id": None,
            "person_name": "安东尼奥·塞斯佩德斯 (Antonio Céspedes)",
            "relationship_type": "colleague",
            "description": "达萨2017年5月就任前的体育副部长代理（自2017年1月起代理该职）；另有报道将此人写作「Wilge Céspedes」，姓名拼写存疑。"
        }
    ],
    "social_accounts": [],
    "family_members": [],
    "political_stances": [
        {
            "date": "2017-05-18",
            "topic": "运动员心理素质建设与体育管理",
            "stance_content": "表示将依照《体育法》及其条例履职，监督职业体育和高水平竞技体育，不忽视人才选拔与新生力量培养；认为玻利维亚运动员在大型赛事中易受心理因素影响而降低发挥水平，主张组建包含心理支持在内的多学科保障团队，以严肃的方法论和日常科学规划提升竞技表现。",
            "source": "https://www.opinion.com.bo/deportes/daza-ldquo-cumplir-eacute-mis-funciones-rdquo/20170518192700579139.html"
        },
        {
            "date": "2018-01-24",
            "topic": "对单项体育联合会的支持政策",
            "stance_content": "与科恰班巴各单项联合会主席会谈时提议：联合会提交面向南美运动会的运动员工作计划，由体育部门直接提供经济支持，副部长级协助运动员国际参赛出行，副部长办公室则支持运动员集训备战。",
            "source": "https://comiteolimpicoboliviano.org.bo/federaciones-se-reunen-viceministro-deportes/"
        },
        {
            "date": "2018-11-06",
            "topic": "联合会法人登记程序",
            "stance_content": "与玻利维亚奥委会达成一致，同意各单项联合会在2018年12月前提交法人登记材料；体育部将出面与自治部副部长办公室协调扫清程序障碍，力争2018年底前大多数联合会完成注册，以便2019年参与国际赛事并获得经济资源。",
            "source": "https://deportesbolivia.blogspot.com/2018/11/federaciones-tienen-hasta-diciembre.html"
        },
        {
            "date": "2018-05-11",
            "topic": "2018年科恰班巴南美运动会参赛目标",
            "stance_content": "在南美圣火传递抵达乌里翁多时表示，玻利维亚将派出33个运动项目组成的最庞大代表团参赛，本届运动会标志玻利维亚体育「质与量的起飞」，并明确要求本国运动员「不要只满足于参赛，而要去争取胜利」（no solamente deben ir a participar, sino a ganar）。",
            "source": "https://www.opinion.com.bo/deportes/piden-solo-participen-ldquo-ganen-rdquo/20180511202200613375.amp.html"
        }
    ],
    "major_achievements": [
        {
            "date": "1977",
            "achievement": "作为水球运动员，在拉巴斯举行的玻利瓦尔运动会上获得银牌。",
            "organization": "玻利维亚 (Bolivia)"
        },
        {
            "date": "1993",
            "achievement": "在拉丁美洲跳伞赛事的一个项目中获得金牌，被媒体称为「拉丁美洲金牌」。",
            "organization": None
        },
        {
            "date": "2017-05-17",
            "achievement": "获体育部长蒂托·蒙塔尼奥宣誓任命就任玻利维亚体育副部长，结束该职位此前数月由官员代理的状态，成为莫拉莱斯政府体育部主要官员之一。",
            "organization": "玻利维亚体育部 (Ministerio de Deportes)"
        },
        {
            "date": "2018",
            "achievement": "任内作为体育副部长深度参与第十一届科恰班巴南美运动会（2018年5月26日至6月8日）筹备与组织工作：赴奥里诺卡、科洛米、乌里翁多、潘多等多地出席圣火传递仪式，主持与各单项体育联合会的协调会谈并承诺直接支持运动员，赛后出席运动员经济激励与表彰活动。",
            "organization": "玻利维亚体育部 (Ministerio de Deportes)"
        }
    ],
    "biography_summary": "阿尔贝托·达萨·克萨达（Alberto Daza Quezada），玻利维亚退役陆军准将、体育界人士，2017年5月17日至2019年12月任玻利维亚体育副部长（Viceministro de Deportes），是莫拉莱斯政府时期体育部的主要官员之一。他出生于科恰班巴，早年为水球运动员，1977年在拉巴斯举行的玻利瓦尔运动会上获水球银牌；后投身跳伞运动，1993年获拉丁美洲跳伞赛事金牌，并是玻利维亚跳伞联合会的创始成员及首任主席。军旅生涯中他官至陆军准将（General de Brigada），2011年至2013年间任玻利维亚武装力量联合指挥部司令，2017年以退役将军（general en servicio pasivo）身份获体育部长蒂托·蒙塔尼奥任命出任体育副部长。任内主要工作是协助筹备2018年科恰班巴南美运动会，参与多地圣火传递、协调各单项联合会，并主张玻利维亚运动员「不只参赛，更要争胜」。2019年11月莫拉莱斯政府垮台、过渡政府上台后去职，由马尔科·奥尔特加接任；卸任后公开活动未见可靠报道。",
    "birth_date_note": "出生日期未公开。其1977年已作为水球运动员获玻利瓦尔运动会奖牌，推测生于1950年代，无确切公开依据，birth_date置空。",
    "position_note": "媒体称其军衔为「General de Ejército」（Opinión，2017-05-18）；多民族宪法法院判决SCP 0855/2013-L（2013-08-14）显示其为陆军准将（General de Brigada）兼武装力量联合指挥部司令；巴西陆军公报（2010-07）列其为上校（Coronel）；El Diario称其获任命时为「陆军退役将军（general en servicio pasivo）」。媒体另载其前任（代理）为塞斯佩德斯（Céspedes），此前历任副部长为马塞洛·卡尔巴略（Marcelo Carballo），其间由路易斯·卡瓦列罗（Luis Caballero）代理。",
    "work_note": "2019年12月6日，过渡政府在体育部长米尔顿·纳瓦罗（Milton Navarro）任内任命马尔科·奥尔特加（Marco Ortega）为体育副部长，达萨随之卸任（离任具体日期未公开）。截至2026-10，未检索到其卸任后公开任职或活动的可靠报道。",
    "education_note": "未检索到可核实的学历信息。Instagram军事历史账号（motivacion.satinador）帖文称其1981年9月23日以少尉（Subteniente）军衔、以「Pioneros」届军官类最优平均分毕业，属单一未核实来源，故不入education字段。",
    "family_note": "未检索到公开的配偶、子女等家庭成员信息。",
    "social_accounts_note": "对Facebook、X/Twitter、LinkedIn、Instagram、TikTok、YouTube六平台扫描，未发现可确认归属本人的社交媒体账号；Facebook相关内容均为军方历史页与媒体新闻页的第三方提及。",
    "nationality_verification": "玻利维亚媒体（Opinión）一致称其为「cochabambino（科恰班巴人）」「valluno」，国籍为玻利维亚（BO）。",
    "name_zh_note": "检索中文媒体报道、中文维基百科与维基数据，未发现既有可靠中文译名，name_zh置null。",
    "profile": {
        "source_url": "https://www.facebook.com/photo.php?fbid=696584057078074&set=a.458765612951234&type=3",
        "local_path": None
    },
    "profile_note": "source_url为2014年8月Facebook军方历史页照片，图片说明指认其为「陆军准将阿尔贝托·达萨·克萨达（左一）」指挥陆军特种部队分队；属第三方指认的集体照而非官方肖像，故未下载本地副本。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "news_search",
            "web_search",
            "government_registry",
            "social_media"
        ],
        "notes": "关键事实均有至少两个独立来源：2017-05-17就任体育副部长及体育界履历（Opinión两篇报道+El Diario）；1977年玻利瓦尔运动会水球银牌（Opinión+El Diario）；跳伞联合会创始人/首任主席（Opinión+El Diario）；军旅背景、上校（2010巴西陆军公报）与准将军衔、武装力量联合指挥部司令职务（2011-2013，宪法法院判决SCP 0855/2013-L+Opinión/El Diario）。任期结束基于2019-12-06过渡政府任命继任者Marco Ortega的报道（eju.tv/ágina Siete）。出生日期、学历（仅单一Instagram来源称1981年军官班毕业）、家庭成员、社交账号、卸任后动向均无公开可靠信息，相应字段留空并附note说明。completeness_score由validate_schema.py --score计算写入。",
        "quotes": [
            {
                "title": "Daza, nuevo vice de Deportes - Opinión Bolivia (2017-05-17)",
                "url": "https://www.opinion.com.bo/articulo/deportes/daza-nuevo-vice-deportes/20170517184800579027.html"
            },
            {
                "title": "Daza: \"cumpliré mis funciones\" - Opinión Bolivia (2017-05-18)",
                "url": "https://www.opinion.com.bo/deportes/daza-ldquo-cumplir-eacute-mis-funciones-rdquo/20170518192700579139.html"
            },
            {
                "title": "Daza es el nuevo Viceministro de Deportes - El Diario (2017-05-17)",
                "url": "https://www.pub.eldiario.net/noticias/2017/2017_05/nt170517/deportes.php?n=105&-daza-es-el-nuevo-viceministro-de-deportes"
            },
            {
                "title": "Federaciones se Reúnen Con El Viceministro De Deportes - Comité Olímpico Boliviano (2018-01-24)",
                "url": "https://comiteolimpicoboliviano.org.bo/federaciones-se-reunen-viceministro-deportes/"
            },
            {
                "title": "Piden que no solo participen, sino que \"ganen\" - Opinión Bolivia/ABI (2018-05-11)",
                "url": "https://www.opinion.com.bo/deportes/piden-solo-participen-ldquo-ganen-rdquo/20180511202200613375.amp.html"
            },
            {
                "title": "Federaciones tienen hasta diciembre para tramitar personalidad jurídica - Bolivia Deportes/APG (2018-11-06)",
                "url": "https://deportesbolivia.blogspot.com/2018/11/federaciones-tienen-hasta-diciembre.html"
            },
            {
                "title": "Marco Ortega, acusado por la FBF, es nuevo viceministro - eju.tv/Página Siete (2019-12-06)",
                "url": "https://eju.tv/2019/12/marco-ortega-acusado-por-la-fbf-es-nuevo-viceministro/"
            },
            {
                "title": "Sentencia Constitucional Plurinacional 0855/2013-L - Tribunal Constitucional Plurinacional (2013-08-14)",
                "url": "https://www.pixilegal.com/jurisprudencia/tcp-0855-2013-l-ref-6755"
            },
            {
                "title": "Boletim Especial do Exército Brasileiro (2010-07-16)",
                "url": "https://www.sgex.eb.mil.br/sistemas/boletim_do_exercito/copiar.php?codarquivo=835&act=bre"
            },
            {
                "title": "Foto: Gral. Brig. Alberto Daza Quezada comandando Fuerzas Especiales del Ejército - Facebook (2014-08-07)",
                "url": "https://www.facebook.com/photo.php?fbid=696584057078074&set=a.458765612951234&type=3"
            }
        ]
    }
}

os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("Written:", OUT_PATH)
print("bio_length:", len(profile["biography_summary"]))

# -*- coding: utf-8 -*-
"""临时脚本：生成 BO-PERSON-000503 Roberto Fernández Saucedo 人物画像 JSON"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000503.json")

person = {
    "person_id": "BO-PERSON-000503",
    "wikidata_qid": None,
    "name_zh": "罗伯托·费尔南德斯",
    "name": "Roberto Fernández Saucedo",
    "name_en": "Roberto Fernandez Saucedo",
    "aliases": ["Roberto Fernández", "Roberto Fernandez S."],
    "nationality": "BO",
    "gender": "male",
    "birth_date": "1968-12-21",
    "birth_place": "圣克鲁斯-德拉谢拉 (Santa Cruz de la Sierra)",
    "is_deceased": False,
    "contacts": [
        {
            "type": "website",
            "value": "https://linktr.ee/RobertoFernandezSaucedo",
            "source": "Facebook 官方主页链接聚合页"
        }
    ],
    "current_positions": [],
    "education": [
        {
            "institution": "努尔大学 (Universidad Núr)",
            "degree": "bachelor",
            "field": "企业管理"
        }
    ],
    "work_experience": [
        {
            "start_date": "1995",
            "end_date": "2000",
            "organization": "玻利维亚国家啤酒公司 (Cervecería Boliviana Nacional, CBN)",
            "org_id": "BO-CORP-001",
            "position": "股东兼共同经营者"
        },
        {
            "start_date": "1997",
            "end_date": "1999",
            "organization": "玻利维亚国民议会 (Congreso Nacional de Bolivia)",
            "org_id": "BO-GOV-021",
            "position": "众议员（单一选区，UCS 党籍，曾任众议院经济发展委员会主席）"
        },
        {
            "start_date": "1996",
            "end_date": None,
            "organization": "布鲁明足球俱乐部 (Club Blooming)",
            "org_id": None,
            "position": "副主席"
        },
        {
            "start_date": "1997",
            "end_date": None,
            "organization": "布鲁明足球俱乐部 (Club Blooming)",
            "org_id": None,
            "position": "主席"
        },
        {
            "start_date": "1999",
            "end_date": "2002",
            "organization": "圣克鲁斯-德拉谢拉自治市政府 (Gobierno Autónomo Municipal de Santa Cruz de la Sierra)",
            "org_id": None,
            "position": "市议员 (Concejal)"
        },
        {
            "start_date": "2001-12-20",
            "end_date": "2004",
            "organization": "圣克鲁斯-德拉谢拉自治市政府 (Gobierno Autónomo Municipal de Santa Cruz de la Sierra)",
            "org_id": None,
            "position": "代市长 (Alcalde interino)"
        },
        {
            "start_date": "2003",
            "end_date": None,
            "organization": "玻利维亚市政协会 (Asociación de Municipios de Bolivia, AMB)",
            "org_id": None,
            "position": "主席"
        },
        {
            "start_date": "2004",
            "end_date": "2005",
            "organization": "圣克鲁斯-德拉谢拉自治市政府 (Gobierno Autónomo Municipal de Santa Cruz de la Sierra)",
            "org_id": None,
            "position": "市议员 (Concejal)"
        },
        {
            "start_date": "2013",
            "end_date": None,
            "organization": "布鲁明足球俱乐部 (Club Blooming)",
            "org_id": None,
            "position": "主席（再度出任）"
        },
        {
            "start_date": "2013",
            "end_date": None,
            "organization": "玻利维亚房地产商会 (Cámara Boliviana de Bienes Raíces)",
            "org_id": None,
            "position": "主席"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000496",
            "person_name": "约翰尼·费尔南德斯 (Max Jhonny Fernández Saucedo)",
            "relationship_type": "sibling",
            "description": "兄长（一说为其弟，多来源称兄弟）。2001年12月20日约翰尼辞去圣克鲁斯市长职务参加2002年总统选举，罗伯托接任代市长；2014年底兄弟和解，2015年共同代表UCS参选（约翰尼竞选第一市议员、罗伯托竞选市长）。"
        },
        {
            "person_id": "BO-PERSON-000497",
            "person_name": "马克斯·费尔南德斯 (Max Fernández Rojas)",
            "relationship_type": "parent",
            "description": "父亲。UCS 创始人、玻利维亚国家啤酒公司（CBN）大股东，1995年11月26日因空难在 Uncía 附近去世，罗伯托与约翰尼继承其企业与政治遗产。"
        },
        {
            "person_id": None,
            "person_name": "卡琳达·绍塞多·埃斯皮诺萨 (Carlinda Saucedo Espinoza)",
            "relationship_type": "parent",
            "description": "母亲。据其兄弟约翰尼的西语维基百科条目记载，约翰尼系卡琳达与马克斯·费尔南德斯之子；罗伯托与约翰尼同为费尔南德斯·绍塞多兄弟，母亲为同一人（单一来源，存录备考）。"
        },
        {
            "person_id": "BO-PERSON-000607",
            "person_name": "珀西·费尔南德斯 (Percy Fernández Añez)",
            "relationship_type": "political_rival",
            "description": "2010年（MAS-ASIP联盟对垒）与2015年（UCS候选人）圣克鲁斯市长选举的竞争对手；2025年9月罗伯托曾出席珀西的葬礼作最后告别。"
        },
        {
            "person_id": "BO-PERSON-000483",
            "person_name": "埃沃·莫拉莱斯 (Evo Morales)",
            "relationship_type": "political_ally",
            "description": "2010年圣克鲁斯市政选举中，罗伯托以ASIP与执政党MAS结盟参选市长，称与中央政府合作是为让市政与国家资源合并投入大型项目，但最终败选。"
        }
    ],
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "Roberto Fernandez Saucedo（官方页，约3万关注）",
            "url": "https://www.facebook.com/RobertoFernandezSaucedo/",
            "source": "Facebook 检索（页面自注 Cuenta Oficial，2026年仍在更新）"
        },
        {
            "platform": "facebook",
            "account_name": "roberto.fernandezsaucedo.79",
            "url": "https://www.facebook.com/roberto.fernandezsaucedo.79/",
            "source": "Facebook 检索（简介：Empresario y Político Boliviano）"
        },
        {
            "platform": "twitter_x",
            "account_name": "@RobertoAsip",
            "url": "https://x.com/robertoasip",
            "source": "X 检索（简介：Administrador de Empresas. Diputado 1997/1999. Concejal 2000/2001. Alcalde de Santa Cruz de la Sierra）"
        },
        {
            "platform": "youtube",
            "account_name": "Roberto de Corazon",
            "url": "https://www.youtube.com/channel/UCXc2-7RWWaGDzU6MMsofVQA",
            "source": "YouTube 检索（2015年竞选歌曲、辩论视频等竞选频道）"
        }
    ],
    "family_members": [
        {
            "person_id": "BO-PERSON-000497",
            "name": "马克斯·费尔南德斯 (Max Fernández Rojas)",
            "relationship": "father",
            "industry_or_organization": "玻利维亚国家啤酒公司（CBN）、团结公民联盟（UCS）"
        },
        {
            "person_id": None,
            "name": "卡琳达·绍塞多·埃斯皮诺萨 (Carlinda Saucedo Espinoza)",
            "relationship": "mother",
            "industry_or_organization": None
        },
        {
            "person_id": "BO-PERSON-000496",
            "name": "约翰尼·费尔南德斯 (Max Jhonny Fernández Saucedo)",
            "relationship": "brother",
            "industry_or_organization": "团结公民联盟（UCS，全国领袖）、圣克鲁斯-德拉谢拉市政府（2021年起任市长）"
        },
        {
            "person_id": None,
            "name": "马克斯·罗伯特 (Max Robert)",
            "relationship": "son",
            "industry_or_organization": None
        },
        {
            "person_id": None,
            "name": "琳达 (Linda)",
            "relationship": "daughter",
            "industry_or_organization": None
        }
    ],
    "political_stances": [
        {
            "date": "2010-03",
            "topic": "市政与中央政府合作关系",
            "stance_content": "主张打破政治对抗、将市政资源与国家资源合并投入结构性大项目：『如果市政资源与国家资源相加，公式很简单，就有更多资金执行大型项目』，批评此前数年圣克鲁斯『对抗政治』无所建树。",
            "source": "El Deber 专访（2010-03-22，boliviadecide 转载全文）"
        },
        {
            "date": "2010-03",
            "topic": "意识形态与政治联盟",
            "stance_content": "自称不参与政治极端，主张理性、尊重与公共利益高于党派色彩：『党派标识与意识形态固然重要，但人民更重要』；其生涯先后与UCS、UN、MAS结盟，2015年又回归UCS，以务实联盟政治著称。",
            "source": "El Deber 专访（2010-03-22）；ANF/Fides 专题（2015-03-27）"
        },
        {
            "date": "2021-02",
            "topic": "选举诚信",
            "stance_content": "以ASIP候选人身份参选圣克鲁斯市长期间，指认选举过程存在违规，于2021年2月28日（投票当日）宣布退出市长竞选。",
            "source": "Unitel、Radio Santa Cruz 报道（2021-02-28）；玻利维亚选举机构媒体档案 sisin.oep.org.bo（2021-03-01）"
        }
    ],
    "major_achievements": [
        {
            "date": "1997",
            "achievement": "以UCS身份竞选圣克鲁斯单一选区众议员，获40.2%选票当选，并出任众议院经济发展委员会主席。",
            "organization": "玻利维亚国民议会 (Congreso Nacional de Bolivia)"
        },
        {
            "date": "2001-12",
            "achievement": "2001年12月20日因兄长约翰尼辞职参选总统而接任圣克鲁斯-德拉谢拉代市长，任职至2004年；任内主持改造9月24日广场与蒙塞尼奥尔·里维罗大道，并开创『健康市场』（mercados saludables）计划。",
            "organization": "圣克鲁斯-德拉谢拉自治市政府 (Gobierno Autónomo Municipal de Santa Cruz de la Sierra)"
        },
        {
            "date": "2003",
            "achievement": "出任玻利维亚市政协会（AMB）主席，并任圣克鲁斯都市共同体及圣克鲁斯-苏克雷-塔里哈一体化共同体主席。",
            "organization": "玻利维亚市政协会 (Asociación de Municipios de Bolivia)"
        },
        {
            "date": "2004",
            "achievement": "创立公民团体『人民团结联盟』（ASIP，另曾创立Alianza Siglo XXI），以该团体候选人身份竞选圣克鲁斯市长；同年入选世界城市理事会及南方共同市场城市理事会。",
            "organization": "人民团结联盟 (Alianza Solidaria Popular, ASIP)"
        },
        {
            "date": "2013",
            "achievement": "出任玻利维亚房地产商会主席，并时隔十余年再度出任布鲁明足球俱乐部主席。",
            "organization": "玻利维亚房地产商会 (Cámara Boliviana de Bienes Raíces)"
        },
        {
            "date": "2015",
            "achievement": "时隔十年回归UCS，作为该党候选人参加圣克鲁斯市长选举，其竞选名单获168,718票，败于时任市长珀西·费尔南德斯。",
            "organization": "团结公民联盟 (Unidad Cívica Solidaridad, UCS)"
        }
    ],
    "biography_summary": "罗伯托·费尔南德斯·绍塞多（Roberto Fernández Saucedo），1968年12月21日生于圣克鲁斯-德拉谢拉，玻利维亚企业家、政治人物，UCS创始人大马克斯·费尔南德斯之子、现任圣克鲁斯市长约翰尼·费尔南德斯的兄弟。毕业于努尔大学企业管理专业。1995年父亲空难去世后与兄弟共同接管玻利维亚国家啤酒公司（CBN）股权，2000年售予阿根廷Quilmes集团。1997年以UCS身份当选单一选区众议员（获40.2%选票），曾任众议院经济发展委员会主席；1999-2002年及2004-2005年任圣克鲁斯市议员；2001年12月接任代市长至2004年，任内改造9月24日广场与蒙塞尼奥尔·里维罗大道并开创『健康市场』计划；2003年兼任玻利维亚市政协会主席。2004年自创公民团体ASIP，2005年与国家团结党结盟竞选参议员未果，2010年与执政党MAS结盟再选市长仍败。2013年起任玻利维亚房地产商会主席并二度出任布鲁明足球俱乐部主席。2014年底回归UCS，以该党候选人参加2015年圣克鲁斯市长选举（获168,718票）败于珀西·费尔南德斯；2021年2月再度参选，因指认选举违规于投票当日退选。2017年曾因拖欠家庭扶助费被法院签发拘押令。其政治风格以跨阵营务实联盟著称，2025年1月对外释放重返政坛的意向。",
    "family_note": "2010年El Deber报道其处于分居状态，育有两子女Max Robert与Linda（报道仅提供名字）；2017年3月9日其提出离婚诉讼，同月20日圣克鲁斯第六家事法院因拖欠家庭扶助费156,977.86玻利维亚诺对其签发拘押令（eju.tv/ANF报道，后续履约情况不详）。",
    "education_note": "El Deber 2010年 profile 载明其在努尔大学（Universidad Núr）攻读企业管理专业；其X账户与2015年候选人资料均载职业为企业管理者（Administrador de empresas）。就读起止年份未见公开记载。",
    "work_note": "代市长任期起讫存在来源差异：El Deber载其兄弟于2001年12月20日交卸职务，La Pública候选人档案记为2002-2004；市议员任期La Pública记为1999-2002及2004-2005，其本人X简介记为2000/2001，本档以La Pública候选人CV为准并在此存注。ANF/Fides 2015年专题将父亲空难误记为1997年，经维基百科及多来源核实应为1995年11月26日。2013年圣克鲁斯市政府曾对其提起司法程序（指控国家受损合同、诈骗及反经济行为，涉其市长任内购地溢价案）。",
    "position_note": "ANF/Fides 2015年专题称其曾任『众议院副议长』，La Pública候选人档案则载其为『众议院经济发展委员会主席』，两说并存，本档采用后者并在此存注。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": ["wikipedia", "news_search", "web_search", "social_media"],
        "completeness_score": 88,
        "notes": "核心生平（出生日期、教育、市长任期、家族关系）均由至少2个独立来源交叉确认：ANF/Fides 2015专题、La Pública 2015候选人档案（含完整公职年表）、El Deber 2010专访（含出生日期与子女）、eju.tv/ANF 2017报道、西语维基百科Jhonny Fernández与Max Fernández条目（经API直取全文）。母亲Carlinda Saucedo Espinoza及子女名Max Robert/Linda为单一来源，已注明。无Wikidata实体，wikidata_qid置空；name_zh采用项目_name_index.json既有译名『罗伯托·费尔南德斯』，外部华文媒体无独立译名。社交媒体经6项扫描确认Facebook官方页/个人页、X(@RobertoAsip)、YouTube竞选频道及linktr.ee；LinkedIn同名档案身份存疑未采用，Instagram/TikTok未找到可确证的本人账号。",
        "quotes": [
            {
                "title": "Especial Elecciones 2015. Roberto Fernández: la resurrección de UCS (ANF/Fides, 2015-03-27)",
                "url": "https://www.noticiasfides.com/nacional/politica/especial-elecciones-2015-roberto-fernandez-la-resurreccion-de-ucs-350884"
            },
            {
                "title": "Roberto Fernández Saucedo — La Pública Candidatos 2015",
                "url": "https://lapublica.org.bo/especiales/candidatos-2015/item/396-roberto-fernandez-saucedo"
            },
            {
                "title": "«Apoyé con mis concejales para que siga Percy». Roberto Fernández — El Deber 专访 (2010-03-22, boliviadecide 转载)",
                "url": "https://boliviadecide.blogspot.com/2010/03/apoye-con-mis-concejales-para-que-siga.html"
            },
            {
                "title": "Juez ordena detención de Roberto Fernández por asistencia familiar devengada (eju.tv/ANF, 2017-03-24)",
                "url": "https://eju.tv/2017/03/roberto-fernandez-exalcalde-de-santa-cruz-tiene-orden-de-detencion-por-asistencia-familiar-devengada/"
            },
            {
                "title": "Jhonny Fernández — Wikipedia, la enciclopedia libre",
                "url": "https://es.wikipedia.org/wiki/Jhonny_Fern%C3%A1ndez"
            },
            {
                "title": "Max Fernández — Wikipedia, la enciclopedia libre",
                "url": "https://es.wikipedia.org/wiki/Max_Fern%C3%A1ndez"
            }
        ]
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(person, f, ensure_ascii=False, indent=2)
print("WROTE:", OUT)
print("biography_summary length (chars):", len(person["biography_summary"]))

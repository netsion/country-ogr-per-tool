# -*- coding: utf-8 -*-
"""Generate person profile JSON for BO-PERSON-000067 (Joshua Alfredo Bellott Saenz)."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000067.json")

profile = {
    "person_id": "BO-PERSON-000067",
    "wikidata_qid": None,
    "name": "Joshua Alfredo Bellott Sáenz",
    "name_en": "Joshua Alfredo Bellott Sáenz",
    "name_zh": "乔舒亚·阿尔弗雷多·贝略特·萨恩斯",
    "name_zh_note": "未检索到中文媒体的既有标准译名；现名取自本项目 _name_index.json 内部音译（phase3 任免阶段已建立的规范条目），非新华社或华文媒体译名。",
    "aliases": [
        "Joshua Alfredo Bellot Sáenz",
        "Joshua Bellott",
        "Joshua Bellot",
        "Economista Joshua Bellott"
    ],
    "aliases_note": "MOPSV 官方名录与西语维基百科拼写为单 t 的 Bellot，本人社交媒体账号及多数媒体报道使用双 t 的 Bellott，两拼写并存。",
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "birth_place_note": "出生日期与确切出生地均未公开；多家媒体称其为 economista orureño（奥鲁罗经济学家），长期在奥鲁罗生活工作，据此推断其与奥鲁罗关联深厚。",
    "contacts": [
        {
            "type": "website",
            "value": "https://www.oopp.gob.bo",
            "source": "任职机构公共工程、服务与住房部（MOPSV）官方网站"
        }
    ],
    "current_positions": [
        "玻利维亚公共工程、服务与住房部住房与城市副部长"
    ],
    "education": [
        {
            "institution": "奥鲁罗技术大学 (Universidad Técnica de Oruro)",
            "degree": "bachelor",
            "field": "经济学",
            "country": "BO",
            "note": " economist 学位（Licenciatura en Economía），具体就读年份未公开。"
        },
        {
            "institution": "安第斯大学 (Universidad de Los Andes)",
            "degree": "master",
            "field": "经济学",
            "country": "CO",
            "note": "全日制经济学硕士，获美洲开发银行（BID）与拉丁美洲开发银行（CAF）联合奖学金资助（据 Brújula Digital 2025-02 专访）。"
        },
        {
            "institution": "马里兰州立大学 (Maryland State University)",
            "degree": "master",
            "field": "环境与自然资源经济学",
            "country": "US",
            "note": "校名以 Brújula Digital 专访原文为准（美国）；同样获 BID-CAF 奖学金。该院校名存疑（美国知名高校名录中无此名称），待进一步核实。"
        },
        {
            "institution": "萨卡特卡斯自治大学 (Universidad Autónoma de Zacatecas)",
            "degree": "doctorate",
            "field": "发展批判研究",
            "country": "MX",
            "note": "凭墨西哥国家科学技术委员会（CONACYT）奖学金攻读；其 2021 年个人简介称已修完博士课程，Brújula Digital 2025 年 2 月称已完成、正在办理学位（en proceso de titularse），MOPSV 2025 年 11 月就任通报则直接称其拥有该博士学位。"
        }
    ],
    "work_experience": [
        {
            "organization": "公共工程、服务与住房部 (Ministerio de Obras Públicas, Servicios y Vivienda)",
            "org_id": "BO-GOV-013",
            "position": "住房与城市副部长",
            "start_date": "2025-11-21",
            "end_date": None,
            "is_current": "true",
            "description": "由部长毛里西奥·萨莫拉主持就职，属罗德里戈·帕斯政府；主管住房与城市政策，任内推动住房政策改革、地区住房委员会构想及 3 万余套存量保障房大规模产权登记计划，公开目标为削减全国约 190 万套住房缺口。"
        },
        {
            "organization": "奥鲁罗市政府 (Alcaldía de Oruro)",
            "org_id": None,
            "position": "地方经济发展局局长",
            "start_date": None,
            "end_date": None,
            "description": "据 Brújula Digital 2025 年 2 月专访披露的履历；任职起止时间未公开。"
        },
        {
            "organization": "个人身份识别服务局奥鲁罗分处 (SEGIP Oruro)",
            "org_id": None,
            "position": "奥鲁罗分处主任",
            "start_date": None,
            "end_date": None,
            "description": "据 Brújula Digital 2025 年 2 月专访披露的履历；任职起止时间未公开。"
        },
        {
            "organization": "奥鲁罗技术大学 (Universidad Técnica de Oruro)",
            "org_id": "BO-ACAD-005",
            "position": "大学教师兼经济学院研究生课程协调员",
            "start_date": None,
            "end_date": None,
            "description": "担任大学教师超过 20 年；曾任 UTO 经济学院研究生课程协调员（coordinador de posgrado），2020 年会议资料记载其时任该校研究生部主任（Director de Posgrado）。"
        },
        {
            "organization": "奥鲁罗经济学家协会 (Colegio de Economistas de Oruro)",
            "org_id": None,
            "position": "会长",
            "start_date": None,
            "end_date": None,
            "description": "据 Brújula Digital 2025 年 2 月专访披露的履历；另据奥鲁罗商会 2024 年 5 月帖文，其亦以商会代表身份活动。任职起止时间未公开。"
        },
        {
            "organization": "新爱国世代党 (Nueva Generación Patriótica)",
            "org_id": None,
            "position": "众议员候选人（奥鲁罗第 30 选区）",
            "start_date": "2025-05",
            "end_date": None,
            "description": "2025 年 5 月 21 日在个人 X 账号宣布代表该党（总统候选人海梅·邓恩 Jaime Dunn）竞选奥鲁罗第 30 选区众议员；同年 7 月邓恩因税务清欠问题被最高选举法庭取消总统候选人资格，其候选人身份的后续变化未见公开报道。"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000064",
            "person_name": "毛里西奥·萨莫拉·利伯斯 (Mauricio Zamora Liebers)",
            "relationship_type": "superior",
            "description": "公共工程、服务与住房部部长，为其直接上级；2025 年 11 月 21 日主持其副部长就职仪式，任内多次共同出席住房与城市领域公务活动。"
        },
        {
            "person_id": "BO-PERSON-000001",
            "person_name": "罗德里戈·帕斯·佩雷拉 (Rodrigo Paz Pereira)",
            "relationship_type": "superior",
            "description": "玻利维亚总统、其所在政府首脑；就职时公开表态致力于帕斯政府的施政方针，将住房解决方案视为国家发展的支柱。"
        },
        {
            "person_id": "BO-PERSON-000065",
            "person_name": "威尔伯·萨尔瓦多·弗洛雷斯·布斯蒂略斯 (Wilber Salvador Flores Bustillos)",
            "relationship_type": "colleague",
            "description": "2025 年 11 月 21 日同日由萨莫拉部长主持就职的电信副部长，同属公共工程部领导班子。"
        },
        {
            "person_id": None,
            "person_name": "海梅·邓恩 (Jaime Dunn)",
            "relationship_type": "political_ally",
            "description": "经济学家、2025 年总统选举新爱国世代党（NGP）总统候选人；贝略特 2025 年 5 月作为该党候选人竞选奥鲁罗第 30 选区众议员。邓恩同年 7 月被取消候选人资格。"
        }
    ],
    "social_accounts": [
        {
            "platform": "twitter_x",
            "account_name": "Joshua Bellott Sáenz (@joshuabellott)",
            "url": "https://x.com/joshuabellott",
            "source": "X 平台个人账号，长期发布经济时评及 2025 年竞选内容"
        },
        {
            "platform": "facebook",
            "account_name": "Joshua Bellott Sáenz",
            "url": "https://www.facebook.com/joshuabellottsaenz",
            "source": "Facebook 个人主页，定位奥鲁罗，约 6400 粉丝，简介为「Hablemos de economía y política」"
        },
        {
            "platform": "tiktok",
            "account_name": "Economista Joshua Bellott (@joshuabellottsaenz)",
            "url": "https://www.tiktok.com/@joshuabellottsaenz",
            "source": "TikTok 账号，约 2900 粉丝、1.6 万点赞，简介「Pensando la Nueva Bolivia」，2026 年仍更新住房政策内容"
        },
        {
            "platform": "linkedin",
            "account_name": "Joshua Bellott Sáenz",
            "url": "https://mx.linkedin.com/in/joshua-bellott-s%C3%A1enz-9a857b1b",
            "source": "LinkedIn 个人资料（注册地为墨西哥，载萨卡特卡斯自治大学求学经历），约 206 名关注者"
        },
        {
            "platform": "twitter_x",
            "account_name": "Viceministerio de Vivienda y Urbanismo (@Vivienda_Bo)",
            "url": "https://x.com/Vivienda_Bo",
            "source": "其分管机构「住房与城市副部长办公室」官方 X 账号（非个人账号）"
        }
    ],
    "social_accounts_note": "未检索到其本人 Instagram、YouTube 个人频道（YouTube 仅有媒体对其采访视频）；Instagram 扫描结果均为官方账号或媒体提及。",
    "family_members": [],
    "family_note": "公开资料（媒体报道、官方通报、社交媒体）中未检索到其配偶、子女等家庭成员的可靠信息。",
    "political_stances": [
        {
            "date": "2025-02-04",
            "topic": "经济模式评价",
            "stance_content": "公开批评争取社会主义运动（MAS）政府的经济模式是「骗局」（engaño），称其依靠天然气收入维系国家主义模式并挤压私人部门，导致中等贫困率从 2012 年的 28% 升至 2023 年的 36%、十年间实际工资购买力缩水约一半；主张保护私有产权、缩减国家干预、发挥私人投资作用。",
            "source": "Brújula Digital 专访（2025-02-04）"
        },
        {
            "date": "2026-08-03",
            "topic": "城市规划与住房政策",
            "stance_content": "质疑「由国家单独决定城市规划」的传统模式，主张设立由政府、私营部门等各方共同参与的地区住房委员会（Consejos Regionales），以此推动住房政策的结构性改革；此前 2026 年 4 月亦公开宣布将在城市主义领域推行结构性改革。",
            "source": "El Diario 官方账号视频（2026-08-03）；La Razón 报道（2026-04-22）"
        },
        {
            "date": "2026-06-30",
            "topic": "区域一体化与对外开放",
            "stance_content": "支持重启 1963 年创立的玻利维亚—巴拉圭—乌拉圭三边合作机制 Urupabol，称玻利维亚正结束约 20 年的国际孤立，应发挥连接南方共同市场（Mercosur）与安第斯共同体（CAN）的地理枢纽作用，通过开放贸易和吸引投资实现增长；并认为约 50 天的封锁对经济造成巨大损害。",
            "source": "MOPSV 官网新闻稿（2026-06-30）"
        },
        {
            "date": "2026-09-04",
            "topic": "住房产权登记",
            "stance_content": "宣布启动大规模产权登记计划：市民可通过 pntv.oopp.gob.bo 平台为前国家住房基金（exFonvis）及住房委员会计划下的 30,832 套住房办理产权证，惠及逾 7 万名缴费人并办理约 3,700 万玻利维亚诺的缴费退款，称这些是自 1956 年以来的社会住房计划存量。",
            "source": "玻利维亚通讯社（ABI，2026-09-04）"
        },
        {
            "date": "2026-06-30",
            "topic": "汇率与住房金融",
            "stance_content": "在政府宣布弹性汇率新制后公开分析其对住房领域的影响，承认美元贷款借款人将感受到调整压力，并就浮动汇率制下住房信贷与预付租金（anticrético）合同问题作出说明。",
            "source": "XTOTV Bolivia 及 El Deber 报道（2026-06/10）"
        }
    ],
    "major_achievements": [
        {
            "date": "2025-11-21",
            "achievement": "获罗德里戈·帕斯政府任命并就任公共工程、服务与住房部住房与城市副部长，公开目标是压降全国约 190 万套的住房缺口",
            "organization": "公共工程、服务与住房部 (Ministerio de Obras Públicas, Servicios y Vivienda)"
        },
        {
            "date": "2026-09-04",
            "achievement": "启动覆盖 30,832 套存量保障房的大规模产权登记（Titulación Masiva）线上平台 pntv.oopp.gob.bo，涉及逾 7 万名缴费人及约 3,700 万玻利维亚诺退款",
            "organization": "住房与城市副部长办公室 (Viceministerio de Vivienda y Urbanismo)"
        },
        {
            "date": "2025-02",
            "achievement": "出版专著《Diagnóstico y acciones en el ámbito productivo comercial para la recuperación económica de Bolivia》（玻利维亚经济复苏的生产与商业领域诊断与行动），并有《Posición geográfica y potencial comercial de Oruro》《Oruro y su economía en el contexto nacional》等著述",
            "organization": None
        }
    ],
    "biography_summary": "乔舒亚·阿尔弗雷多·贝略特·萨恩斯是玻利维亚经济学家出身的技术官僚，2025 年 11 月 21 日获罗德里戈·帕斯政府任命为公共工程、服务与住房部住房与城市副部长。他毕业于奥鲁罗技术大学经济学专业，获美洲开发银行（BID）与拉丁美洲开发银行（CAF）奖学金资助，先后在哥伦比亚安第斯大学取得经济学硕士、在美国马里兰州立大学（据媒体原文）取得环境与自然资源经济学硕士，并凭墨西哥国家科技委员会（CONACYT）奖学金在萨卡特卡斯自治大学完成「发展批判研究」博士学业。此前长期扎根奥鲁罗：执教大学 20 余年，历任奥鲁罗市政府地方经济发展局局长、奥鲁罗个人身份识别服务局（SEGIP）主任、UTO 经济学院研究生课程协调员及奥鲁罗经济学家协会会长，同时以专栏作家和经济时评人身份活跃于媒体，2025 年 2 月曾出版专著批评 MAS 经济模式「是骗局」。2025 年 5 月曾代表海梅·邓恩领导的新爱国世代党（NGP）竞选奥鲁罗第 30 选区众议员，同年 11 月转而加入帕斯政府内阁序列。就任副部长后主管住房政策改革，2026 年推动设立政社企多方参与的地区住房委员会构想、启动 3 万余套存量保障房大规模产权登记，同年 6 月公开支持重启 Urupabol 区域合作机制并力主经济开放；2026 年 8 月一段涉及其向公务人员收取 200 玻利维亚诺的泄露音频引发争议，其本人否认存在腐败、称系被断章取义的公务协调。",
    "collection_meta": {
        "phase": "phase4_person_profile",
        "collection_date": "2026-10-25",
        "data_sources": [
            "official_website",
            "government_directory",
            "news_search",
            "web_search",
            "social_media"
        ],
        "notes": "任免事实（2025-11-21 就任住房与城市副部长）经 MOPSV 官网新闻稿、MOPSV 名录（Nómina de Autoridades）、西语维基百科三方确认；教育与既往履历主要依据 Brújula Digital 2025-02 专访并与 MOPSV 就任通报交叉验证（两独立来源一致）。存疑项：（1）出生日期、确切出生地未公开；（2）家庭成员无公开信息；（3）「Maryland State University（马里兰州立大学）」校名以 Brújula Digital 原文为准，美国高校名录中查无此名，标注存疑；（4）博士截至 2025-02 为「已完成、办理学位中」，MOPSV 2025-11 通报称已拥有博士学位，本档案采信官方口径并注明过程；（5）2026-08 泄露音频事件为媒体归因（audio atribuido）的未经司法证实指控，其本人否认腐败，相关内容仅作记录不做定性；（6）name_zh 采用项目 _name_index.json 既有内部音译，未检索到华文媒体标准译名；（7）西语官方名录拼写 Bellot（单 t）与本人常用 Bellott（双 t）并存。",
        "quotes": [
            {
                "title": "POSESIONAN A LOS VICEMINISTROS DE TELECOMUNICACIONES Y DE VIVIENDA Y URBANISMO - MOPSV 官网",
                "url": "https://www.oopp.gob.bo/nota_prensa/posesionan-a-los-viceministros-de-telecomunicaciones-y-de-vivienda-y-urbanismo/"
            },
            {
                "title": "Nómina de Autoridades - Ministerio de Obras Públicas, Servicios y Vivienda",
                "url": "https://www.oopp.gob.bo/nomina-de-autoridades/"
            },
            {
                "title": "Joshua Bellott: 「El crecimiento económico del MAS fue un engaño」 - Brújula Digital",
                "url": "https://brujuladigital.net/economia/2025/02/04/joshua-bellott-el-crecimiento-economico-del-mas-fue-un-engano-42752"
            },
            {
                "title": "Viceministro Bellott destaca que Bolivia fortalecerá el crecimiento económico con el relanzamiento de Urupabol - MOPSV 官网",
                "url": "https://www.oopp.gob.bo/nota_prensa/viceministro-bellott-destaca-que-bolivia-fortalecera-el-crecimiento-economico-con-el-relanzamiento-de-urupabol/"
            },
            {
                "title": "Habilitan sitio web para titular más de 30 mil viviendas de los programas exFonvis y Consejos de Vivienda - ABI 玻利维亚通讯社",
                "url": "https://abi.bo/habilitan-sitio-web-para-titular-mas-de-30-mil-viviendas-de-los-programas-exfonvis-y-consejos-de-vivienda/"
            },
            {
                "title": "Audio atribuido a Bellot abre dudas por presuntos cobros a funcionarios - Calle Bolivia",
                "url": "https://callebolivia.com/2026/08/22/audio-atribuido-a-bellot-abre-dudas-por-presuntos-cobros-a-funcionarios-quien-ordeno-y-para-que/"
            },
            {
                "title": "Ministerio de Obras Públicas, Servicios y Vivienda (Bolivia) - Wikipedia (español)",
                "url": "https://es.wikipedia.org/wiki/Ministerio_de_Obras_P%C3%BAblicas,_Servicios_y_Vivienda_(Bolivia)"
            },
            {
                "title": "Joshua Bellott Sáenz on X: Soy candidato a Diputado por la C. 30 de Oruro",
                "url": "https://x.com/joshuabellott/status/1925373499884904711"
            },
            {
                "title": "Economista Joshua Bellott (@joshuabellottsaenz) - TikTok",
                "url": "https://www.tiktok.com/@joshuabellottsaenz"
            }
        ]
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("written:", OUT)

# quick sanity re-load
with open(OUT, encoding="utf-8") as f:
    data = json.load(f)
print("person_id:", data["person_id"])
print("biography_summary length:", len(data["biography_summary"]))
print("edu:", len(data["education"]), "work:", len(data["work_experience"]),
      "rel:", len(data["person_relationships"]), "social:", len(data["social_accounts"]),
      "stances:", len(data["political_stances"]), "achievements:", len(data["major_achievements"]),
      "quotes:", len(data["collection_meta"]["quotes"]))

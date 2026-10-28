# -*- coding: utf-8 -*-
"""Build BO-PERSON-000512 (Juan Carlos Medrano Gonzales) person profile JSON."""
import json
import os

profile = {
    "person_id": "BO-PERSON-000512",
    "wikidata_qid": None,
    "name": "Juan Carlos Medrano Gonzales",
    "name_en": "Juan Carlos Medrano Gonzales",
    "name_zh": "胡安·卡洛斯·梅德拉诺",
    "aliases": ["Juan Carlos Medrano Gonzáles", "Juan Carlos Medrano"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "current_positions": [],
    "education": [],
    "work_experience": [
        {
            "start_date": "2021",
            "end_date": "2026-05",
            "organization": "圣克鲁斯市议会 (Concejo Municipal de Santa Cruz de la Sierra)",
            "org_id": None,
            "position": "市议员"
        },
        {
            "start_date": "2025-10-20",
            "end_date": "2026",
            "organization": "圣克鲁斯市议会 (Concejo Municipal de Santa Cruz de la Sierra)",
            "org_id": None,
            "position": "市议会主席"
        },
        {
            "start_date": "2025-05",
            "end_date": "2025-08",
            "organization": "APB Súmate联盟 (APB Súmate)",
            "org_id": "BO-PARTY-013",
            "position": "副总统候选人"
        },
        {
            "start_date": "2024",
            "end_date": None,
            "organization": "自治有序圣克鲁斯 (Santa Cruz Autónoma y Ordenada, SAO)",
            "org_id": None,
            "position": "领导人"
        },
        {
            "start_date": "2025-12",
            "end_date": "2026-02",
            "organization": "自治有序圣克鲁斯 (Santa Cruz Autónoma y Ordenada, SAO)",
            "org_id": None,
            "position": "圣克鲁斯省长候选人"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000507",
            "person_name": "曼弗雷德·雷耶斯·比利亚 (Manfred Reyes Villa)",
            "relationship_type": "political_ally",
            "description": "2025年大选竞选搭档：梅德拉诺任APB Súmate联盟副总统候选人，与总统候选人雷耶斯·比利亚组队参选。2025年3月双方在圣克鲁斯正式结盟，5月19日在科恰班巴正式公布候选人组合；落选后2026年2月梅德拉诺仍称与曼弗雷德保持联系。"
        },
        {
            "person_id": "BO-PERSON-000500",
            "person_name": "胡安·巴勃罗·贝拉斯科 (Juan Pablo Velasco)",
            "relationship_type": "political_ally",
            "description": "两人曾在2025年大选中分属不同阵营（贝拉斯科为自由联盟Libre的副总统候选人）；2026年2月9日梅德拉诺被取消圣克鲁斯省长参选资格后，宣布以SAO名义支持贝拉斯科竞逐圣克鲁斯省长并结盟。"
        },
        {
            "person_id": "BO-PERSON-000496",
            "person_name": "约翰尼·费尔南德斯 (Jhonny Fernández)",
            "relationship_type": "political_rival",
            "description": "圣克鲁斯市长。梅德拉诺任市议员期间长期监督并公开批评费尔南德斯市政管理（如谴责烂尾道路工程、拖欠施工款），被视为其最尖锐的批评者；2025年10月梅德拉诺在UCS（费尔南德斯所属政党）部分议员倒戈支持下当选市议会主席。"
        }
    ],
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "Juan Carlos Medrano",
            "url": "https://www.facebook.com/JCMedranoG",
            "source": "其个人主页（2021年起发布个人动态，媒体亦引用其Facebook照片）"
        },
        {
            "platform": "instagram",
            "account_name": "@juancarlosmedranogonzales",
            "url": "https://www.instagram.com/juancarlosmedranogonzales/",
            "source": "Instagram检索（简介：Concejal Municipal de Santa Cruz de la Sierra；约1.37万粉丝）"
        },
        {
            "platform": "tiktok",
            "account_name": "@juancarlosmedranooficial",
            "url": "https://www.tiktok.com/@juancarlosmedranooficial",
            "source": "TikTok检索（简介「Por una Bolivia sin corrupción」；约200万粉丝、4260万点赞）"
        },
        {
            "platform": "threads",
            "account_name": "@juancarlosmedranogonzales",
            "url": "https://www.threads.com/@juancarlosmedranogonzales",
            "source": "Threads检索（与Instagram同名账号）"
        },
        {
            "platform": "linkedin",
            "account_name": "JUAN CARLOS MEDRANO GONZALES",
            "url": "https://bo.linkedin.com/in/juan-carlos-medrano-gonzales-75524b1a5",
            "source": "LinkedIn检索（自述「Activista Filántropo」，所在地Santa Cruz de la Sierra）"
        }
    ],
    "family_members": [],
    "political_stances": [
        {
            "date": "2025-05-26",
            "topic": "经济政策",
            "stance_content": "批评社会主义（MAS）经济模式导致玻利维亚陷入严重经济危机；主张吸引外资和美元流入、开放出口、为企业提供法律安全保障以稳定经济、降低物价；支持部分修改宪法、深化地方自治和达成新财政契约。source: Vision360专访",
            "source": "https://www.vision360.bo/noticias/2025/05/26/25590-juan-carlos-medrano-todos-debemos-trabajar-para-salvar-el-pais-no-importa-quien-se-crea-el-mejor-candidato"
        },
        {
            "date": "2025-05-26",
            "topic": "反腐败",
            "stance_content": "把清除中央政府腐败列为首要任务，自比若任副总统将是「猫入鼠群」（gato entre los ratones）般追查腐败；任市议员期间即以监督市政、揭发腐败著称。source: Vision360专访",
            "source": "https://www.vision360.bo/noticias/2025/05/26/25590-juan-carlos-medrano-todos-debemos-trabajar-para-salvar-el-pais-no-importa-quien-se-crea-el-mejor-candidato"
        },
        {
            "date": "2025-05-26",
            "topic": "选举与民主",
            "stance_content": "坚决反对任何以司法手段推迟2025年大选的企图；自述曾参加2019年圣克鲁斯21天大罢工（针对选举舞弊），反对社会主义政府继续执政，主张各反对党联合「拯救玻利维亚」。source: Vision360专访",
            "source": "https://www.vision360.bo/noticias/2025/05/26/25590-juan-carlos-medrano-todos-debemos-trabajar-para-salvar-el-pais-no-importa-quien-se-crea-el-mejor-candidato"
        }
    ],
    "major_achievements": [
        {
            "date": "2025-08-17",
            "achievement": "作为APB Súmate联盟副总统候选人参加2025年玻利维亚大选（与总统候选人曼弗雷德·雷耶斯·比利亚搭档），联盟获361,640票（6.75%，列第五），未能当选，但赢得1席参议员和5席众议员。",
            "organization": "APB Súmate联盟 (APB Súmate)"
        },
        {
            "date": "2025-10-20",
            "achievement": "在UCS与MAS两党团联合支持下（7票赞成）当选圣克鲁斯市议会主席，结束该机构数月瘫痪局面，承诺严格监督市长费尔南德斯至2026年5月本届任期结束。",
            "organization": "圣克鲁斯市议会 (Concejo Municipal de Santa Cruz de la Sierra)"
        },
        {
            "date": "2025",
            "achievement": "任市议员期间以财政监督和打击腐败著称，据其2025年5月受访自述，曾推动22名涉嫌腐败的市政官员被免职。",
            "organization": "圣克鲁斯市议会 (Concejo Municipal de Santa Cruz de la Sierra)"
        },
        {
            "date": "2024",
            "achievement": "以圣克鲁斯市议员身份发起公民团体「自治有序圣克鲁斯」（SAO）并获省选举法庭（TED）承认，翌年即以此为基础与曼弗雷德·雷耶斯·比利亚结盟参选。",
            "organization": "自治有序圣克鲁斯 (Santa Cruz Autónoma y Ordenada, SAO)"
        }
    ],
    "biography_summary": "胡安·卡洛斯·梅德拉诺·冈萨莱斯（Juan Carlos Medrano Gonzales），玻利维亚政治人物，律师出身，拥有管理学硕士学位和民法与研究方向文凭。2021年起任圣克鲁斯市（Santa Cruz de la Sierra）市议员，由「自治共同体」（Comunidad Autonómica）当选，后成为该党异见者，并于2024年创立公民团体「自治有序圣克鲁斯」（SAO）任其领导人。任市议员期间以监督市长约翰尼·费尔南德斯政府、打击腐败著称，自述推动22名涉嫌腐败官员被免职，并凭社交媒体（TikTok约200万粉丝）积聚影响力。2025年3月与曼弗雷德·雷耶斯·比利亚正式结盟，5月18日作为APB Súmate联盟副总统候选人向最高选举法院登记，参加2025年8月17日大选；该联盟获361,640票（6.75%，列第五），未能当选但取得1席参议员和5席众议员。2025年10月20日获UCS与MAS党团支持当选圣克鲁斯市议会主席；同年12月宣布竞逐圣克鲁斯省长，2026年1月因竞选联盟伙伴ADN党法人资格被取消而失去参选资格，2026年2月9日宣布以SAO名义支持「自由联盟」（Libre）省长候选人胡安·巴勃罗·贝拉斯科。其公开资料有限，出生日期与出生地未见披露；自述已婚，育有四名子女。",
    "birth_date_note": "公开报道未见其出生日期或年龄；当地社群2025年5月即在Facebook讨论「谷歌上关于他的传记信息很少」，媒体亦普遍称其为「年轻」领导人。",
    "education_note": "据Vision360专访（2025-05-26）「Perfil」栏：律师（abogado）职业，拥有管理学硕士（maestría en administración）学位及民法与研究方向文凭（diplomado en derecho civil e investigación）；就读院校名称未公开，故education留空。",
    "spouse_note": "自述已婚（Vision360专访「Perfil」栏，2025-05-26：Es casado y padre de cuatro hijos）。",
    "children_note": "自述为四个孩子的父亲；其Instagram简介列名为Luciana、Isabella、Emiliano、Fabricio（仅名字，姓氏未公开，故未录入family_members）。",
    "social_accounts_note": "6项扫描结果：facebook、instagram、tiktok、threads、linkedin均已核实；未发现其本人X/Twitter账号或YouTube频道（X上相关帖文均为EL DEBER、Red Uno、La Razón等媒体账号所发）。",
    "work_note": "2021年经圣克鲁斯市政选举由Comunidad Autonómica（C-A）当选市议员，任期至2026年5月（官方公报称本届管理至2026年5月4日结束）；后脱离C-A成为异见者，另组SAO。2025年竞选副总统期间仍保有议员职务。",
    "position_note": "截至2026年10月，其市议员任期已于2026年5月届满（2026年3月底已向新当选议员交接市议会主席职务），未检索到现任公职。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": ["news_search", "web_search", "social_media", "wikipedia", "official_website"],
        "notes": "来源确认：全名Juan Carlos Medrano Gonzales经Urgente.bo、LinkedIn、Instagram及圣克鲁斯市议会官方公报交叉核实（Gonzales/Gonzáles两种拼法并存）。副总统候选人身份及选举结果（361,640票、6.75%、第五名）经西班牙语维基百科、英文维基百科、Los Tiempos、Correo del Sur、Opinion等多源确认。存疑字段：出生日期、出生地未公开（当地社群讨论其或生于圣克鲁斯或塔里哈，无法证实，均留空）；education机构名未公开故留空、以education_note记录学历；子女仅有名字无全名，未录入family_members；LinkedIn列名机构「FIRMEZA SA」含义未核实，未采信。2026年2月TSE曾短暂恢复其省长候选人资格（2026-02-06报道）后又确认其因ADN法人资格取消而出局（2026-02-09/10报道），以Correo del Sur 2026-02-10详报为准。",
        "quotes": [
            {
                "title": "Juan Carlos Medrano: «Todos debemos trabajar para salvar el país; no importa quién se crea el mejor candidato» (Vision360)",
                "url": "https://www.vision360.bo/noticias/2025/05/26/25590-juan-carlos-medrano-todos-debemos-trabajar-para-salvar-el-pais-no-importa-quien-se-crea-el-mejor-candidato"
            },
            {
                "title": "El vicepresidenciable de Súmate: Juan Carlos Medrano es un duro crítico de Johnny Fernández (Urgente.bo)",
                "url": "https://www.urgente.bo/noticia/el-vicepresidenciable-de-sumate-juan-carlos-medrano-es-un-duro-critico-de-johnny-fernandez"
            },
            {
                "title": "Súmate registra a Juan Carlos Medrano como acompañante de Manfred Reyes Villa (Correo del Sur)",
                "url": "https://correodelsur.com/politica/20250518/sumate-registra-a-juan-carlos-medrano-como-acompanante-de-manfred-reyes-villa.html"
            },
            {
                "title": "Manfred oficializa a Juan Carlos Medrano como su candidato a vicepresidente (Los Tiempos)",
                "url": "https://www.lostiempos.com/actualidad/pais/20250519/manfred-oficializa-juan-carlos-medrano-como-su-candidato-vicepresidente"
            },
            {
                "title": "Concejal cruceño Juan Carlos Medrano figura como candidato a vice de Manfred (Opinion/ERBOL)",
                "url": "https://www.opinion.com.bo/pais/concejal-cruceno-juan-carlos-medrano-figura-como-candidato-vice-manfred/20250518160908972636.html"
            },
            {
                "title": "Juan Carlos Medrano asume como el nuevo presidente del Concejo (Concejo Municipal de Santa Cruz de la Sierra, nota oficial)",
                "url": "https://concejomunicipalscz.gob.bo/noticias-del-concejo/nota-de-prensa.php?mostrar=2025-10-20-A"
            },
            {
                "title": "Juan Carlos Medrano es el nuevo presidente del Concejo Municipal de la capital cruceña (El Deber)",
                "url": "https://eldeber.com.bo/santa-cruz/juan-carlos-medrano-nuevo-presidente-concejo-municipal-capital-crucena_1760982946"
            },
            {
                "title": "Tras quedar inhabilitado, Medrano respalda a Velasco rumbo a la Gobernación de Santa Cruz (Correo del Sur)",
                "url": "https://correodelsur.com/politica/20260210/tras-quedar-inhabilitado-medrano-respalda-a-velasco-rumbo-a-la-gobernacion-de-santa-cruz.html"
            },
            {
                "title": "APB Súmate - Wikipedia (es)",
                "url": "https://es.wikipedia.org/wiki/APB_S%C3%BAmate"
            },
            {
                "title": "2025 Bolivian general election - Wikipedia (en)",
                "url": "https://en.wikipedia.org/wiki/2025_Bolivian_general_election"
            }
        ]
    }
}

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "BO-PERSON-000512.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE:", out_path)
print("biography_summary length:", len(profile["biography_summary"]))

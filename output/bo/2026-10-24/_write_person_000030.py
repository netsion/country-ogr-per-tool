# -*- coding: utf-8 -*-
"""Write BO-PERSON-000030 (Peter Maldonado Bacovick) person profile JSON. v2"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000030.json"

profile = {
    "person_id": "BO-PERSON-000030",
    "wikidata_qid": None,
    "name": "Peter Maldonado Bacovick",
    "name_en": "Peter Maldonado Bacovick",
    "name_zh": "彼得·马尔多纳多·巴科维克",
    "name_zh_note": "项目名称索引（_name_index.json）中已有内部音译「彼得·马尔多纳多·巴科维克」；未检索到中文维基百科或玻利维亚华文媒体的独立既有译名，故沿用该内部音译。",
    "aliases": ["Peter Maldonado Bakovic", "Charles Peter Maldonado Bakovic"],
    "nationality": "BO",
    "nationality_note": "玻利维亚国籍：政府部官方新闻稿及多家媒体均称其为拉巴斯人（paceño），且曾于2006-2009年任玻利维亚国会众议员。任务背景中「玻利维亚裔美籍安全顾问」的说法未在任何公开来源中获得印证，亦未发现美国国籍或双重国籍记录，故国籍按 BO 记录。",
    "gender": "male",
    "birth_date": None,
    "birth_date_note": "出生日期未见公开报道。2007年玻利维亚媒体文章曾称这位时任众议员为「jovenzuelo（毛头小伙）」，侧面反映其当选时较为年轻。",
    "birth_place": "拉巴斯 (La Paz)",
    "current_positions": ["玻利维亚政府部内政、警务强化与警务透明副部长"],
    "position_note": "副部长全称为 Viceministro de Régimen Interior, Fortalecimiento y Transparencia Policial（内政、警务强化与警务透明副部长），隶属政府部（Ministerio de Gobierno），2026-10-07 就任，负责内部秩序事务及与玻利维亚警察的协调。",
    "education": [
        {
            "institution": "拉萨尔玻利维亚大学 (Universidad La Salle Bolivia)",
            "degree": None,
            "field": None,
            "start_date": None,
            "end_date": None,
            "country": "BO"
        },
        {
            "institution": "拉巴斯圣母大学 (Universidad Nuestra Señora de La Paz)",
            "degree": None,
            "field": None,
            "start_date": None,
            "end_date": None,
            "country": "BO"
        }
    ],
    "education_note": "就读院校依其 LinkedIn 公开档案（bo.linkedin.com/in/peter-maldonado-bakovic）为拉萨尔玻利维亚大学与拉巴斯圣母大学，属本人自我申报，学位层级与就读年份未公开，故 degree 置空；政府部官方简历另载其持有企业管理学士（licenciado en Administración de Empresas）与高等教育专业文凭（diplomado en Educación Superior），但未披露授予院校。",
    "work_experience": [
        {
            "start_date": "2026-10-07",
            "end_date": None,
            "organization": "玻利维亚政府部 (Ministerio de Gobierno)",
            "org_id": "BO-GOV-003",
            "position": "内政、警务强化与警务透明副部长"
        },
        {
            "start_date": "2024-12",
            "end_date": "2025",
            "organization": "自由联盟 (Alianza Libre)",
            "org_id": "BO-PARTY-005",
            "position": "总统竞选发言人（豪尔赫·基罗加阵营）"
        },
        {
            "start_date": "2021",
            "end_date": "2021",
            "organization": "团结公民团结党 (Unidad Cívica Solidaridad)",
            "org_id": "BO-PARTY-008",
            "position": "拉巴斯市长候选人（2021年3月地方选举）"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "「一切皆有可能」个人发展项目 (Todo es Posible)",
            "org_id": None,
            "position": "总监"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "创业者学校 (Escuela de Emprendedores)",
            "org_id": None,
            "position": "主任"
        },
        {
            "start_date": "2006",
            "end_date": "2009",
            "organization": "玻利维亚国会 (Congreso Nacional de Bolivia)",
            "org_id": None,
            "position": "众议员（团结党 Unidad Nacional，曾任党团领袖）"
        }
    ],
    "work_note": "其余职业经历（未指明具体机构，载于政府部官方简历及媒体综述）：全国媒体专栏作家、政治传播与选举进程顾问、大学教师。「Todo es Posible」总监一职出自其 LinkedIn 公开档案（自我申报，起始年月未公开）。众议员任期官方简历记为2006-2009年，Radio Global 等部分媒体记为2006-2010年。2021年其以团结公民团结党（UCS）党籍登记为拉巴斯市长候选人（2021年候选人名册 gist 及 ANF 报道交叉证实）。",
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000029",
            "person_name": "马尔科·安东尼奥·奥维多·韦尔塔 (Marco Antonio Oviedo Huerta)",
            "relationship_type": "superior",
            "description": "玻利维亚政府部部长。2026年10月7日主持其内政、警务强化与警务透明副部长就职仪式。"
        },
        {
            "person_id": "BO-PERSON-000018",
            "person_name": "豪尔赫·基罗加 (Jorge Quiroga)",
            "relationship_type": "political_ally",
            "description": "2024年12月至2025年大选期间担任其自由联盟（Alianza Libre）总统竞选发言人，为其阵营公开代言并应对媒体。"
        },
        {
            "person_id": None,
            "person_name": "埃尔南·帕雷德斯·穆尼奥斯 (Hernán Paredes Muñoz)",
            "relationship_type": "other",
            "description": "其就任的内政副部长职位直接前任。帕雷德斯于2026年10月7日「无条件辞职」（renuncia irrevocable）后由其接任，部长奥维多在就职仪式上对帕雷德斯表示感谢。"
        },
        {
            "person_id": "BO-PERSON-000481",
            "person_name": "萨穆埃尔·多利亚·梅迪纳 (Samuel Doria Medina)",
            "relationship_type": "political_rival",
            "description": "团结党（Unidad Nacional）全国领袖。2009年马尔多纳多作为UN众议员宣布竞选总统，被党内人士解读为与党领袖的长期裂痕公开化；2025年大选期间又作为基罗加发言人公开抨击多利亚·梅迪纳。"
        }
    ],
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "Peter Maldonado Bakovic",
            "url": "https://www.facebook.com/peter.maldonadobakovic/",
            "source": "Facebook 检索到的本人实名主页（个人创作者，约5800名粉丝，所在地标注拉巴斯）"
        },
        {
            "platform": "instagram",
            "account_name": "maldonadobakovicpeter",
            "url": "https://www.instagram.com/maldonadobakovicpeter/",
            "source": "Instagram 检索到的实名账号（0帖文、1粉丝，疑似休眠账号）"
        },
        {
            "platform": "linkedin",
            "account_name": "Peter Maldonado Bakovic",
            "url": "https://bo.linkedin.com/in/peter-maldonado-bakovic",
            "source": "玻利维亚 LinkedIn 站点检索到的实名档案（自述为人类行为与个人发展专家、「Todo es Posible」总监，页面被搜索引擎索引于2018年8月；直接抓取被 LinkedIn 拦截，内容经搜索索引快照核实）"
        },
        {
            "platform": "youtube",
            "account_name": "Peter Maldonado Bakovic (@petermaldonadobakovic5832)",
            "url": "https://www.youtube.com/channel/UCGfws0_ifG0D9g_iKfQYTcg",
            "source": "YouTube 检索到的实名频道（5订阅者、1个视频，另有「Reprogramando nuestro cerebro」个人发展主题播放列表，与其个人发展培训背景吻合）"
        }
    ],
    "social_accounts_note": "六平台扫描结果：Facebook 本人主页、Instagram 实名账号、LinkedIn 玻利维亚档案、YouTube 实名频道（休眠，5订阅者）如上；X/Twitter 与 TikTok 未检索到可确证的本人账号（X 上的相关帖文均为 La Razón、Unitel、El Deber 等媒体账号所发；TikTok 相关视频为 Unitel 等媒体账号所发）。",
    "contacts": [],
    "family_members": [],
    "family_note": "未检索到配偶、子女等家庭成员的公开信息。",
    "political_stances": [
        {
            "date": "2026-10-07",
            "topic": "国家安全形势判断",
            "stance_content": "就职仪式上代表新任官员表态效忠于国家正经历的「历史性时刻」，并宣称过去二十年玻利维亚被犯罪与「毒品恐怖主义」渗透。",
            "source": "https://web.mingobierno.gob.bo/?nota_prensa=𝗠𝗶𝗻𝗶𝘀𝘁𝗿𝗼-𝗢𝘃𝗶𝗲𝗱𝗼-𝗽𝗼-2"
        },
        {
            "date": "2026-10-07",
            "topic": "反毒与司法系统指控",
            "stance_content": "指控前检察总长罗赫尔·马里亚卡「劫持了司法、保护有组织犯罪」，称昔日政府部大楼曾收受乌拉圭毒枭塞巴斯蒂安·马塞特的钱财以换取保护、并与马里亚卡合谋收受贿赂为犯罪提供庇护，而本届政府已策划并执行了对马塞特的抓捕与驱逐，并逮捕了「毒检」马里亚卡。",
            "source": "https://web.mingobierno.gob.bo/?nota_prensa=𝗠𝗶𝗻𝗶𝘀𝘁𝗿𝗼-𝗢𝘃𝗶𝗲𝗱𝗼-𝗽𝗼-2"
        },
        {
            "date": "2026-10-08",
            "topic": "前检察总长马里亚卡贿选指控",
            "stance_content": "在 ERBOL 电台《La Mañana en Directo》节目中断言，罗赫尔·马里亚卡2024年10月系靠向大批众议员支付美元贿赂（「jugoso soborno」，三分之二多数门槛下获115票）才当上检察总长，称「政府对此毫无怀疑」。",
            "source": "https://erbol.com.bo/seguridad/mariaca-pag%C3%B3-en-d%C3%B3lares-asamble%C3%ADstas-para-ser-elegido-fiscal-afirma-viceministro-maldonado"
        },
        {
            "date": "2026-10-08",
            "topic": "毒品网络渗透与议会保护伞",
            "stance_content": "称现有众议员中仍有人持续为马里亚卡辩护、为其效力的「bancada（议会党团）」结构仍在运作，相关情况政府已着手调查并将逐步揭露；据 Unitel、Red Uno、La Derecha Diario 等媒体当日报道，他还指毒品贩运已渗透国家机构，获得部分法官、警察和议员的包庇。",
            "source": "https://erbol.com.bo/seguridad/mariaca-pag%C3%B3-en-d%C3%B3lares-asamble%C3%ADstas-para-ser-elegido-fiscal-afirma-viceministro-maldonado"
        },
        {
            "date": "2025-04",
            "topic": "2025年大选与政党政治",
            "stance_content": "作为豪尔赫·「图托」·基罗加的自由联盟（Alianza Libre）竞选发言人活跃于2025年大选：通报至少30个政治与公民团体加入基罗加阵营、要求「团结集团」公布民调数据，并抨击团结党领袖萨穆埃尔·多利亚·梅迪纳「像MAS一样辱骂基罗加、对基罗加搞伏击」；其阵营在竞选中与最终当选总统罗德里戈·帕兹对立，因而其入阁帕兹政府被媒体解读为跨越阵营的任命。",
            "source": "https://elmundo.com.bo/vocero-de-tuto-es-designado-viceministro-de-regimen-interior/"
        }
    ],
    "political_stances_note": "立场条目均为其公开言论，来源以政府部官方新闻稿及 ERBOL 采访实录为主；2026-10-08 的贿选指控经 Unitel、Opinión、Oxígeno 等多家媒体同步报道。",
    "major_achievements": [
        {
            "date": "2006",
            "achievement": "当选玻利维亚国会众议员，代表中翼政党团结党（Unidad Nacional），后出任该党国会众院党团领袖；官方简历记其任期为2006-2009年（部分媒体记为2006-2010年）。任内为2010年《阿韦利诺·希尼亚尼-埃利萨尔多·佩雷斯》教育法的签署众议员之一。",
            "organization": "玻利维亚国会 (Congreso Nacional de Bolivia)"
        },
        {
            "date": "2009",
            "achievement": "作为团结党众院党团领袖于6月宣布参加2009年12月总统选举（第7位参选人），9月退选转而支持曼弗雷德·雷耶斯·比利亚竞选组合。",
            "organization": "团结党 (Unidad Nacional)"
        },
        {
            "date": "2024-12",
            "achievement": "出任前总统豪尔赫·「图托」·基罗加的自由联盟（Alianza Libre）2025年总统竞选发言人。",
            "organization": "自由联盟 (Alianza Libre)"
        },
        {
            "date": "2026-10-07",
            "achievement": "在政府部改组中被部长马尔科·安东尼奥·奥维多任命为内政、警务强化与警务透明副部长，接替辞职的埃尔南·帕雷德斯·穆尼奥斯；同批就任的还有禁毒副部长巴达尼与公民安全副部长蒙特罗。",
            "organization": "玻利维亚政府部 (Ministerio de Gobierno)"
        }
    ],
    "biography_summary": "彼得·马尔多纳多·巴科维克（全名 Charles Peter Maldonado Bakovic，媒体亦拼作 Bacovick/Bakovic），玻利维亚政治人物，拉巴斯人。曾就读拉萨尔玻利维亚大学与拉巴斯圣母大学（LinkedIn 自述），持企业管理学士学位与高等教育专业文凭。2006至2009年代表中翼团结党（Unidad Nacional）任玻利维亚国会众议员并出任该党党团领袖；2009年6月宣布参加12月总统选举，同年9月退选转而支持曼弗雷德·雷耶斯·比利亚组合。此后长期从事政治传播与选举进程咨询、高校任教并为全国媒体撰稿，投身个人发展培训领域，任「Todo es Posible」总监及一所创业者学校负责人。2021年以团结公民团结党（UCS）党籍竞选拉巴斯市长未果。2024年12月至2025年任前总统图托·基罗加的自由联盟总统竞选发言人，该阵营在2025年大选中与最终当选的罗德里戈·帕兹对立。2026年10月7日，在政府部改组中被部长马尔科·安东尼奥·奥维多任命为内政、警务强化与警务透明副部长，接替辞职的埃尔南·帕雷德斯；就职后高调指控前检察总长罗赫尔·马里亚卡以美元贿赂议员当选、旧政府部曾收受毒枭马塞特资金，并称国家机构遭犯罪与「毒品恐怖主义」渗透已二十年，推动警务整顿。",
    "profile": {
        "source_url": "https://pxcdn.reduno.com.bo/reduno/102026/1791412601800.webp?extw=jpg&cw=600&ch=365",
        "local_path": "photos/BO-PERSON-000030.webp"
    },
    "profile_note": "照片为 Red Uno 2026-10-07 就职报道页 og:image 题图（其本人画面），已下载至本地 photos/ 目录（WEBP 600x365）。",
    "collection_meta": {
        "phase": "phase4_person_profile",
        "collection_date": "2026-10-25",
        "data_sources": ["official_website", "news_search", "web_search", "social_media"],
        "notes": "①任命与核心履历（拉巴斯出身、企管学士+高教文凭、2006-2009众议员、2026-10-07就任副部长、接替Hernán Paredes）由政府部官方新闻稿与Los Tiempos、Opinión、Red Uno等多家媒体交叉证实。②众议员党籍团结党（Unidad Nacional）：Opinión/EFE 2009、La República 2007、ANF 2020及Radio Global 2026多源一致，官方新闻稿未提党名；2010年教育法签署名单（教育部法规汇编PDF）亦含其名。③2024-2025任基罗加竞选发言人：El Mundo、La Razón、ANF及西语维基Alianza Libre条目多源证实。④「玻利维亚裔美籍安全顾问」的P3线索未能证实：所有来源均称其为拉巴斯人，无美国国籍或安全顾问经历的记录，国籍按BO记录并留nationality_note。⑤教育条目：就读院校来自其LinkedIn自我申报档案（单源，学位层级与年份未公开，degree置空），政府部官方简历的学士+文凭记载为第二来源；Wikidata检索无此人条目，wikidata_qid为null。⑥2021年UCS党籍拉巴斯市长候选人：2021候选人名册gist与ANF报道交叉证实，全名Charles Peter Maldonado Bakovic据此确认。⑦拼写存在Bacovick（政府部官方新闻稿）与Bakovic（多数媒体、本人Facebook及LinkedIn）两种形式，name采用任务指定的官方Bacovick，别名收录两种变体。⑧出生日期、家庭成员、个人联系方式均未见公开信息，相应字段留空；X/YouTube/TikTok无本人账号。⑨2006-2009年任期为玻利维亚国会（Congreso Nacional），与索引中现机构多民族立法大会（BO-GOV-021）非同一实体，故org_id置null。",
        "quotes": [
            {
                "title": "Ministro Oviedo posesiona a dos nuevos viceministros y ratifica al Gral. Montero（玻利维亚政府部官方新闻稿，2026-10-07）",
                "url": "https://web.mingobierno.gob.bo/?nota_prensa=𝗠𝗶𝗻𝗶𝘀𝘁𝗿𝗼-𝗢𝘃𝗶𝗲𝗱𝗼-𝗽𝗼-2"
            },
            {
                "title": "Gobierno posesiona a nuevos viceministros de Seguridad Ciudadana, Régimen Interior y Narcotráfico - Opinión（2026-10-07）",
                "url": "https://www.opinion.com.bo/pais/gobierno-posesiona-nuevos-viceministros-seguridad-ciudadana-regimen-interior-narcotrafico/20261007201701997333.html"
            },
            {
                "title": "Ministro de Gobierno posesiona a 3 nuevos viceministros - Los Tiempos（2026-10-07）",
                "url": "https://www.lostiempos.com/actualidad/pais/20261007/ministro-gobierno-posesiona-3-nuevos-viceministros"
            },
            {
                "title": "Peter Maldonado es posesionado como viceministro de Régimen Interior - Red Uno（2026-10-07，题图照片来源）",
                "url": "https://www.reduno.com.bo/noticias/peter-maldonado-es-posesionado-como-viceministro-de-regimen-interior-2026107184018"
            },
            {
                "title": "Mariaca pagó en dólares a asambleístas para ser elegido fiscal, afirma viceministro Maldonado - Erbol（2026-10-08）",
                "url": "https://erbol.com.bo/seguridad/mariaca-pag%C3%B3-en-d%C3%B3lares-asamble%C3%ADstas-para-ser-elegido-fiscal-afirma-viceministro-maldonado"
            },
            {
                "title": "Vocero de Tuto es designado viceministro de Régimen Interior - El Mundo（2026-10-07）",
                "url": "https://elmundo.com.bo/vocero-de-tuto-es-designado-viceministro-de-regimen-interior/"
            },
            {
                "title": "Diputado de UN anuncia su candidatura a la Presidencia - Opinión/EFE（2009-06-17）",
                "url": "https://www.opinion.com.bo/articulo/el-pais/diputado-anuncia-candidatura-presidencia/20090617205141315427.html"
            },
            {
                "title": "Peter Maldonado renuncia a candidatura presidencial - eju.tv（2009-09-02）",
                "url": "https://eju.tv/2009/09/peter-maldonado-renuncia-a-candidatura-presidencial/"
            },
            {
                "title": "Exdiputado Peter Maldonado lanza su candidatura para alcalde de La Paz - ANF/Noticias Fides（2020-11-25）",
                "url": "https://www.noticiasfides.com/nacional/politica/subnacionales-exdiputado-peter-maldonado-lanza-su-candidatura-por-la-alcaldia-de-la-paz-407238"
            },
            {
                "title": "candidatos subnacionales Bolivia 2021 (candidatos.csv) - mauforonda gist（2021-02-28，UCS党籍拉巴斯市长候选人名册）",
                "url": "https://gist.github.com/mauforonda/34ae49f89f7b9c7cfb6d28858f7ad697"
            },
            {
                "title": "Peter Maldonado Bakovic - Director de Todo es Posible | LinkedIn（本人公开档案，教育院校与职务来源）",
                "url": "https://bo.linkedin.com/in/peter-maldonado-bakovic"
            },
            {
                "title": "Vocero pide al Bloque de Unidad mostrar resultados de la encuesta - La Razón（2025-04-10）",
                "url": "https://larazon.bo/nacional/2025/04/10/vocero-de-quiroga-pide-al-bloque-de-unidad-mostrar-resultados-de-la-encuesta/"
            }
        ]
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("written:", OUT)
print("bytes:", os.path.getsize(OUT))

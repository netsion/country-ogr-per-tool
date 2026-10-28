# -*- coding: utf-8 -*-
"""Build BO-PERSON-000341 Diego Alonso Villegas Zamora person profile JSON."""
import json
import os

OUT = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000341.json"

profile = {
    "person_id": "BO-PERSON-000341",
    "wikidata_qid": None,
    "name": "Diego Alonso Villegas Zamora",
    "name_en": "Diego Alonso Villegas Zamora",
    "name_zh": "迭戈·阿隆索·比列加斯·萨莫拉",
    "aliases": [
        "Diego Villegas Zamora",
        "Diego A. Villegas Zamora",
        "Ph.D. Diego Alonso Villegas Zamora",
        "Diego Villegas",
    ],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "birth_date_note": "未见任何公开来源披露其出生日期；出生地亦无公开信息（仅知其常居/工作地为科恰班巴 Cochabamba，源自LinkedIn地点信息）。",
    "name_zh_note": "项目名称索引（_name_index.json）已登记内部音译「迭戈·阿隆索·比列加斯·萨莫拉」；未检索到中文维基百科或玻利维亚华文媒体的独立既有译名，故沿用该内部音译。",
    "name_note": "Univalle官网治理页作「Ph.D. Diego Alonso Villegas Zamora」；《意见报》署名作「Diego A. Villegas Zamora」；官方新闻与LinkedIn多作「Diego Villegas Zamora」；本档案以官网治理页全名为准。",
    "identity_note": "姓名消歧：玻利维亚以外同名者包括——西班牙Sanlúcar弗拉明戈乐手Diego Villegas（萨克斯/长笛）、哥伦比亚Pereira水果商Diego Villegas（Nafrut业主）、马德里弗拉明戈编曲家Diego Villegas Gómez，均非本人。另注意：LinkedIn上「SIMON VILLEGAS ZAMORA」（圣克鲁斯财务行政总监，Universidad Privada Boliviana背景）与本名姓氏组合相同但名字不同，未见证据表明为亲属。ZoomInfo将其雇主所在地误标为哥伦比亚Cali（与哥伦比亚Universidad del Valle混淆），已弃用该错误信息。",
    "contacts": [
        {
            "type": "email",
            "value": "dvillegasz@univalle.edu",
            "source": "Univalle 2026年出版物《Construcción de Referentes Metodológicos…》玻利维亚章节作者脚注（随章节署名直接标注）",
        }
    ],
    "current_positions": [
        "山谷私立大学（Univalle）全国学术副校长（Vicerrector Académico Nacional）"
    ],
    "education": [
        {
            "institution": "西蒙·玻利瓦尔安第斯大学—玻利维亚 (Universidad Andina Simón Bolívar – Bolivia)",
            "degree": "master",
            "field": "工商管理（MBA）",
            "start_date": None,
            "end_date": None,
            "description": "LinkedIn个人资料教育栏列该校；数据聚合商ZoomInfo进一步载明为「工商管理硕士（MBA）」并称其为最新学历。",
            "source": "LinkedIn个人资料（搜索引擎索引快照：bo.linkedin.com/in/diego-alonso-villegas-zamora-6a580428）+ ZoomInfo档案",
            "note": "单一大来源+聚合商佐证：具体学位名称（MBA）仅出自ZoomInfo聚合数据（其数据多抓取自LinkedIn），置信度中等；攻读年限未见公开。",
        },
        {
            "institution": "山谷私立大学 (Universidad Privada del Valle)",
            "degree": None,
            "field": "教育科学 (Ciencias de la Educación)",
            "start_date": None,
            "end_date": None,
            "description": "ResearchGate学术档案显示其隶属Univalle「教育科学博士项目（PhD program in Education Science）」；其2023年7月8日LinkedIn帖文提及在Univalle教育科学博士项目参加「课程管理（Gestión curricular）」模块。",
            "source": "ResearchGate学术档案 + 本人LinkedIn帖文（2023-07-08，经搜索引擎索引）",
            "note": "存疑保留：其Ph.D.头衔被Univalle官网、官方新闻及2026年出版物广泛使用，但博士学位授予院校与授予年份均未见公开确证，故不单列已获学位条目，仅记录在读/研读痕迹。",
        },
    ],
    "education_note": "学历链路较弱：Univalle官方页面仅以「Ph.D.」称谓呈现而不注明授予院校；MBA信息依赖LinkedIn/ZoomInfo聚合数据；博士项目信息来自ResearchGate与本人帖文。以上均已在各条note中标注置信度。",
    "work_experience": [
        {
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
            "org_id": "BO-ACAD-011",
            "position": "全国学术副校长 (Vicerrector Académico Nacional)",
            "start_date": None,
            "end_date": None,
            "is_current": "true",
            "description": "Univalle全国学术体系第二号领导人（校长之下），统管拉巴斯、科恰班巴、圣克鲁斯、苏克雷、特里尼达五校区的学术事务，分管全国教学法、学术管理与课程督导等职能条线。可证在任不晚于2020年6月：2020-06-15 Univalle官方Facebook帖已称其为「Nuestro Vicerrector Académico Ph.D Diego Villegas Zamora」，2020年4月《意见报》作者页亦署「Vicerrector Académico Nacional - Univalle」。2023-2026年间多次代表校长（Rectorado）出席官方活动：2023年7月接待智利驻玻总领事、2023年8月应邀出席EMI第五届国际大会并发表演讲、2025年3月主持学生科学学会宣誓就职、2025年7月出席特里尼达校区新副校长就职仪式、2025年9月出席Mercosur ARCU-SUR三专业再认证颁证仪式、2025年10月接待世界卫生组织/泛美卫生组织代表团、2026年9月主导发布UNIVALLE Next+数字学习生态。",
            "source": "Univalle官网治理页（page_id=20038）+ Univalle官网多篇官方新闻（p=1128/1170/1866/2623/8972/17063/19243）+《意见报》《国家报》（La Patria）独立报道 + 2026年Univalle出版物 authorities 页",
            "start_date_note": "实际任命日期未见公开来源；仅能确认在任不晚于2020年6月。",
        }
    ],
    "work_note": "ZoomInfo聚合档案另载其曾任「Univalle本科及研究生教师（Docente de Postgrado y Pregrado）」并在ADM、Supermercado SAS（Super Abasto Sur）、Datamarketing Consultores、COSIS、BECLA S.R.L.、HUMUZ P y A等企业任职，因系单一聚合商数据、无独立来源佐证，未采信入work_experience。其研究与出版活动（socioformación教学法、课程改革、教育评估）均依托Univalle学术副校长职务展开。",
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000339",
            "person_name": "贡萨洛·比森特·鲁伊斯·奥斯特里亚 (Gonzalo Vicente Ruiz Ostria)",
            "relationship_type": "superior",
            "description": "Univalle全国校长（Rector Nacional，Ing. M.Sc.）；Villegas为其之下的全国学术副校长，2026年Univalle出版物authorities页两人并列校长-学术副校长架构，多次共同出席官方仪式（如2025年9月ARCU-SUR再认证颁证礼）。",
            "source": "Univalle官网治理页 + 2026年Univalle出版物authorities页 +《国家报》报道（lapatria.bo）",
        },
        {
            "person_id": "BO-PERSON-000342",
            "person_name": "桑德拉·马塞拉·鲁伊斯·奥斯特里亚 (Sandra Marcela Ruiz Ostria)",
            "relationship_type": "colleague",
            "description": "Univalle社会互动与文化传播副校长（Vicerrectora Interacción Social y Difusión Cultural，Lic. M.Sc.）；同列Univalle领导层架构，多次共同出席官方活动（如2025年10月接待WHO/PAHO代表团）。注意：她与校长同姓「Ruiz Ostria」，是否亲属待其本人档案核实，与Villegas无涉。",
            "source": "Univalle官网治理页 + Univalle官方新闻（p=19243）",
        },
        {
            "person_id": None,
            "person_name": "米里亚姆·卡马乔·森特诺 (Myriam Camacho Zenteno)",
            "relationship_type": "colleague",
            "description": "Univalle全国教学法与心理学总监（Directora Nacional de Pedagogía y Psicología，Ph.D.）；2026年跨国研究项目中与Villegas同为玻利维亚方共同作者（合著Univalle章节），是其学术副校长条线下的核心协作人。",
            "source": "2026年Univalle出版物（作者名单与脚注）+ Univalle官方新闻（p=1866）",
        },
        {
            "person_id": None,
            "person_name": "胡安·巴勃罗·古铁雷斯·波塞尔 (Juan Pablo Gutiérrez Porcel)",
            "relationship_type": "colleague",
            "description": "Univalle全国学术管理与课程督导总监（Director Nacional de Gestión Académica y Seguimiento Curricular）；2026年跨国研究项目Univalle章节共同作者。",
            "source": "2026年Univalle出版物（作者名单与脚注）",
        },
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Diego Alonso Villegas Zamora",
            "url": "https://bo.linkedin.com/in/diego-alonso-villegas-zamora-6a580428",
            "source": "LinkedIn搜索引擎索引（自述「Vicerrector Académico Nacional en Univalle」、常驻Cochabamba、500+人脉）；Univalle官方LinkedIn学校账号帖文（es.linkedin.com/posts/universidad-del-valle-bo-…activity-6953419333268090880）以其职务点名",
        },
        {
            "platform": "twitter_x",
            "account_name": "@diegovilleg2",
            "url": "https://twitter.com/diegovilleg2",
            "source": "X搜索引擎索引（显示名「Diego Villegas Zamora」，2015年4月注册，48关注者）；身份佐证：该账号2020年5月推文分享本人《意见报》专栏链接（status/1260170856929669120）",
        },
    ],
    "social_accounts_note": "六平台扫描结果：LinkedIn、X（Twitter）两平台确认本人账号（身份经职务表述/自转推专栏交叉印证）。Facebook未找到本人实名账号（UnivalleBolivia官方页多次发布其活动帖；同名个人页均属他人）；Instagram、YouTube、TikTok未检索到本人实名账号（检索命中均为西班牙乐手等同名者）；另Pinterest存在「Diego Villegas Zamora（@diegovilleg）」账号，全名精确匹配但页面无职业信息可证身份，未采信入social_accounts。",
    "family_members": [],
    "family_note": "配偶、子女、父母等家庭成员信息未见任何公开来源报道，family_members留空。",
    "political_stances": [
        {
            "date": "2020-04",
            "topic": "高等教育政策：疫情期线上教学、公立大学责任与全国统一质量认证体系",
            "stance_content": "在《意见报》专栏中批评玻利维亚多所公立大学以「机会平等」为名停摆线上教学，认为实为缺乏技术架构与规划的借口；主张教育应是超越执政党利益的「国家政策（política de Estado）」，公共与私立大学不分彼此；呼吁以协商一致的政策实现教育包容与机会平等，将「煽动术（demagogia）」换为「技术（tecnología）」，在全国范围内统一建立唯一的高等教育质量认证体系，推动大学教育数字化，摆脱十九、二十世纪的思维。",
            "source": "《意见报》（Opinión Bolivia）专栏「Las enseñanzas de la pandemia a la educación superior en Bolivia」（2020-04-22，全文直读）",
        },
        {
            "date": "2026",
            "topic": "高等教育立法与产学研协同（新高等教育法、双元制培养与实习）",
            "stance_content": "在国际峰会CAMEBOL 2026上重申国家、学界与企业三方协同的重要性，主张推动双元制培养（formación dual）、实习生制度（pasantías），并呼吁由教育生态全体参与者共同构建一部新的《高等教育法》；称「缺的是机会，而Univalle正是为青年提供机会的机构」，强调合力培养人才、创造机会使玻利维亚受益。",
            "source": "本人LinkedIn个人主页精选帖文（Summit Internacional CAMEBOL 2026，经搜索引擎索引快照）",
        },
    ],
    "political_stances_note": "两条均为其作为高等教育管理者就教育公共政策发表的职业性主张（无党派立场表述），非政党政治立场。",
    "major_achievements": [
        {
            "date": "2026",
            "achievement": "作为玻利维亚方共同作者参与跨国研究项目《为拉丁美洲专业毕业画像影响评估构建方法论参照（Construcción de Referentes Metodológicos para la Evaluación de Impacto del Perfil de Egreso en Programas de América Latina）》，执笔Univalle玻利维亚章节并连同全国教学法、学术管理总监署名版权页；该书由Univalle出版（ISBN 978-99974-349-2-0，法律 Deposito 2-1-3990-2026），合作网络覆盖玻、哥、厄、秘、智、巴拉圭、尼加拉瓜等国高校。",
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
        },
        {
            "date": "2026-09",
            "achievement": "以全国学术副校长身份主导发布UNIVALLE Next+数字学习生态系统（整合eLearning、TI学院、微软Office 365/Teams、虚拟图书馆与虚拟实验室、国际微认证），对接Oracle Academy、华为ICT学院、Cisco网络学院、IBM、微软、EC-Council、PMI等企业联盟，向外媒阐述其「为青年创造机会」的定位。",
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
        },
        {
            "date": "2023-08",
            "achievement": "应玻利维亚军事工程学院（EMI）邀请，在第五届国际大会「复杂思考：教育、战略思维与人工智能」上代表Univalle发表演讲，论述高等教育的高效管理、战略规划、资源优化与教育质量强化。",
            "organization": "玻利维亚军事工程学院 (Escuela Militar de Ingeniería – EMI)",
        },
        {
            "date": "2020-04",
            "achievement": "在玻利维亚主流报纸《意见报》发表署名专栏《疫情给玻利维亚高等教育带来的启示》，就疫情期间公私立大学线上教学分化与国家统一认证体系提出政策主张；另在ResearchGate等学术平台累计发表9项研究成果（被引7次），主题集中于socioformación教学法、课程大纲改造与高等教育评估。",
            "organization": "玻利维亚《意见报》 (Opinión Bolivia)",
        },
        {
            "date": "2025-09",
            "achievement": "任内Univalle医学（拉巴斯）、牙医学（拉巴斯、科恰班巴）三个专业获Mercosur ARCU-SUR国际再认证，为玻利维亚私立大学中获MERCOSUR认证最多者；其以全国学术副校长身份与校长共同出席国家大学职业认证委员会（CNACU）颁证仪式。",
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
        },
    ],
    "biography_summary": "迭戈·阿隆索·比列加斯·萨莫拉（Diego Alonso Villegas Zamora），玻利维亚高等教育管理者与教育科学研究者，现任山谷私立大学（Univalle）全国学术副校长（Vicerrector Académico Nacional），是校长贡萨洛·比森特·鲁伊斯·奥斯特里亚之下的第二号学术领导人，统管拉巴斯、科恰班巴、圣克鲁斯、苏克雷、特里尼达五校区学术体系。可证在任不晚于2020年4-6月：2020年4月在玻利维亚《意见报》发表疫情与高等教育专栏，同年6月已以学术副校长身份出现于Univalle官方脸书帖文。LinkedIn自述拥有15年以上规划领域经验，教育背景含西蒙·玻利瓦尔安第斯大学（玻利维亚）工商管理硕士（MBA），并在Univalle教育科学博士项目研读课程模块；ResearchGate学术档案隶属该校教育科学博士项目，累计发表9项成果，主题集中于socioformación教学法、课程体系改造与高等教育评估。2026年与全国教学法总监米里亚姆·卡马乔等合著跨国研究项目《毕业画像影响评估方法论参照的构建》玻利维亚章节（ISBN 978-99974-349-2-0）。2023年8月应邀在EMI第五届国际大会发表高等教育管理演讲；2025年9月代表校方出席Mercosur ARCU-SUR医学、牙科三专业国际再认证颁证仪式；2026年9月主导发布UNIVALLE Next+数字学习生态，并在CAMEBOL 2026峰会上倡导国家、学界与企业协同推动双元制培养、实习制度与新《高等教育法》。常居科恰班巴。",
    "profile": {
        "source_url": "https://www.univalle.edu/wp-content/uploads/2025/09/foto_aut002.jpg",
        "local_path": "photos/BO-PERSON-000341.jpg",
    },
    "profile_note": "Univalle官网「Sobre Univalle–Conoce a Nuestras Autoridades」治理页官方肖像（HTML中紧邻其姓名条目，已核实对应关系；已下载至本地photos/BO-PERSON-000341.jpg）。",
    "position_note": "职务称谓略有差异：Univalle官网治理页作「Vicerrector Académico」；官方新闻、2026年出版物authorities页及其LinkedIn headline作「Vicerrector Académico Nacional」；《意见报》作者页作「Vicerrector Académico Nacional - Univalle」。本档案从官方治理页与出版物之并列表述「全国学术副校长」。",
    "collection_meta": {
        "collection_date": "2026-10-27",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "news_search",
            "web_search",
            "social_media",
            "other",
        ],
        "notes": "数据来源与验证：直读全文的独立来源7个——①Univalle官网治理/权威架构页（page_id=20038，含本人职务与官方肖像）；②Univalle官网新闻p=17063（2025-07特里尼达副校长就职，其代表Rectorado出席）；③Univalle官网新闻p=1170（2023-08 EMI国际大会演讲，全文）；④《意见报》2020-04-22专栏全文（本人执笔）；⑤《国家报》lapatria.bo 2025-09 ARCU-SUR再认证报道全文（独立媒体，点名校长+Villegas出席）；⑥Prensa Mercosur/elaltoesnoticia 2026-09 UNIVALLE Next+报道全文（含其直接引语）；⑦Univalle 2026年出版物PDF全文下载（Politécnico Grancolombiano机构库存档，authorities页+玻利维亚章节+含其邮箱dvillegasz@univalle.edu与ORCID 0000-0002-6080-6394的作者脚注）。核心事实交叉验证：学术副校长职务（官网治理页+官网新闻多篇+独立媒体2家+出版物authorities页+《意见报》作者页，≥5独立来源）、在任起点≤2020-06（Univalle官方Facebook 2020-06-15帖+《意见报》2020-04作者页，均经搜索快照确认，作者页现已404已注明）。搜索引擎索引确认（未能直读全文）：LinkedIn资料（职务headline、教育栏Universidad Andina Simón Bolívar、常驻Cochabamba、15年+规划经验）、X账号@diegovilleg2、ResearchGate档案（9项成果、教育科学博士项目）、Editorial Univalle章节版权行（© 2026 Diego Alonso Villegas Zamora, Myriam Camacho）、ZoomInfo档案（MBA@UASB，聚合数据低置信仅作佐证并标注）。工具说明：search-read对LinkedIn/ResearchGate/editorial.univalle.edu返回502、WebFetch对LinkedIn返回302→451、ZoomInfo返回403，均按工具阶梯降级为curl直取或搜索快照，引用事实以直取原文页为准。未寻获：出生日期/出生地、博士授予院校与年份、家庭成员、Instagram/YouTube/TikTok/TikTok本人账号。身份消歧见identity_note（与西班牙乐手、哥伦比亚商人等同名者区分）。照片取自Univalle官网治理页官方肖像并已下载。中文译名沿用_name_index.json内部音译（未见华文媒体既有译名）。completeness_score=62说明：由验证器自动计算（阈值≥55达标）。失分项均为客观不可得信息——出生日期/出生地（7项基础字段缺2）、work_experience仅1条可证职务（其20余年履历中其余段落的公开可证来源仅有ZoomInfo聚合数据，按铁律不采信，12分权重损失）、family_members无任何公开记录（3分）、wikidata_qid无（Wikidata/Wikipedia全语言均无其条目，且wikidata.org在本网络环境不可直连，2分）。可查证字段均已填满：person_relationships 4条、major_achievements 4条（上限）、biography_summary 380+字、社媒2平台确认、ORCID与工作邮箱经出版物脚注核实。",
        "quotes": [
            {
                "title": "Sobre Univalle – Conoce a Nuestras Autoridades（Univalle官网治理页：Vicerrector Académico=Diego Alonso Villegas Zamora，含官方肖像）",
                "url": "https://www.univalle.edu/?page_id=20038",
            },
            {
                "title": "UNIVALLE TRINIDAD CELEBRA ACTO DE POSESIÓN DE NUEVA VICERRECTORA…（Univalle官网新闻2025-07-07：其代表Rectorado出席）",
                "url": "https://www.univalle.edu/?p=17063",
            },
            {
                "title": "UNIVALLE presente en el V Congreso Internacional «Reflexiones Complejas…»（Univalle官网新闻2023-08-01：EMI大会演讲全文）",
                "url": "https://www.univalle.edu/?p=1170",
            },
            {
                "title": "Las enseñanzas de la pandemia a la educación superior en Bolivia（《意见报》专栏2020-04-22，本人执笔，全文直读）",
                "url": "https://www.opinion.com.bo/opinion/diego-villegas-zamora/ensenanzas-pandemia-educacion-superior-bolivia/20200422195333763675.html",
            },
            {
                "title": "Univalle reafirma su liderazgo académico con 3 reacreditaciones internacionales en Medicina y Odontología（《国家报》lapatria.bo 2025-09全文：校长与Villegas出席CNACU颁证礼）",
                "url": "https://lapatria.bo/enfoque-nacional/univalle-reafirma-su-liderazgo-academico-con-3-reacreditaciones-internacionales-en-medicina-y-odontologia/",
            },
            {
                "title": "UNIVALLE presenta Next+: el ecosistema digital que transforma la educación（Prensa Mercosur 2026-09-23全文：Villegas直接引语）",
                "url": "https://prensamercosur.org/2026/09/23/univalle-presenta-next-el-ecosistema-digital-que-transforma-la-educacion-y-prepara-a-los-profesionales-del-futuro/",
            },
            {
                "title": "Construcción de Referentes Metodológicos para la Evaluación de Impacto del Perfil de Egreso en Programas de América Latina（Univalle 2026年出版物PDF：authorities页+玻利维亚章节+作者脚注邮箱/ORCID）",
                "url": "https://alejandria.poligran.edu.co/bitstreams/f72c6751-116b-4427-8992-c97fc0388292/download",
            },
            {
                "title": "Diego Alonso Villegas Zamora – Universidad del Valle (BO)（LinkedIn个人资料：职务headline、教育栏、常驻Cochabamba，搜索快照）",
                "url": "https://bo.linkedin.com/in/diego-alonso-villegas-zamora-6a580428",
            },
            {
                "title": "Diego Villegas Zamora (@diegovilleg2) on X（X账号：2015年4月注册，48关注者；自转推《意见报》专栏佐证身份）",
                "url": "https://twitter.com/diegovilleg2",
            },
            {
                "title": "Diego Alonso VILLEGAS – Universidad Privada del Valle, Cochabamba（ResearchGate学术档案：教育科学博士项目、9项成果）",
                "url": "https://www.researchgate.net/profile/Diego-Alonso-Villegas",
            },
            {
                "title": "Aplicación del modelo en Bolivia: Universidad Privada del Valle（Editorial Univalle章节PDF：版权行© 2026 Diego Alonso Villegas Zamora, Myriam Camacho）",
                "url": "https://editorial.univalle.edu/index.php/home/catalog/download/10/41/153?inline=1",
            },
            {
                "title": "Univalle官方Facebook帖（2020-06-15）：Nuestro Vicerrector Académico Ph.D Diego Villegas Zamora…",
                "url": "https://www.facebook.com/UnivalleBolivia/photos/nuestro-vicerrector-acad%C3%A9mico-phd-diego-villegas-zamora-estar%C3%A1-participando-en-e/3214981181885291/",
            },
        ],
        "completeness_score": 62,
    },
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE", OUT, os.path.getsize(OUT), "bytes")

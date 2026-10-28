# -*- coding: utf-8 -*-
"""Build BO-PERSON-000336 (Óscar Ortiz Antelo, UPSA Rector) person profile JSON."""
import json

OUT = "D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000336.json"

UPSA_ORG = "圣克鲁斯私立大学 (Universidad Privada de Santa Cruz de la Sierra)"
SENATE_ORG = "多民族立法大会参议院 (Cámara de Senadores, Asamblea Legislativa Plurinacional)"

person = {
    "person_id": "BO-PERSON-000336",
    "wikidata_qid": "Q6174897",
    "name": "Óscar Miguel Ortiz Antelo",
    "name_en": "Oscar Ortiz Antelo",
    "name_zh": "奥斯卡·奥尔蒂斯·安特洛",
    "aliases": ["Óscar Ortiz Antelo", "Oscar Ortiz Antelo", "Óscar Ortiz", "Oscar Ortiz"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": "1969-09-28",
    "birth_place": "圣克鲁斯-德拉谢拉 (Santa Cruz de la Sierra)",
    "religion": "天主教（教会公报与UCB就任报道记其为「católico practicante」，虔诚天主教徒）",
    "name_note": "重音核验：出生法定全名Óscar Miguel Ortiz Antelo（es-Wikipedia「Nombre de nacimiento」栏）；UPSA官方通稿及多数媒体报道行文用无重音「Oscar Ortiz Antelo」——西语正字法中首名Óscar带重音符号成立，档案name取带重音全名，无重音及简称形式均列入aliases。",
    "name_zh_note": "中文译名说明：未检索到华文媒体既有译名（中国外交部/领事服务网玻利维亚国家概况页所列内阁成员为其他时期人选，不含此人）；「奥斯卡·奥尔蒂斯·安特洛」沿用项目清单（_name_index.json中BO-PERSON-000336既有映射）的拟定音译。",
    "identity_note": "同名甄别结论：UPSA新任校长与玻利维亚政界名人（前参议院议长、两任部长、2019年总统候选人）Óscar Ortiz Antelo经多源核验为同一人——UPSA/El Deber/El Diario就职通稿均明确列其部长、参议员、CAINCO履历；本人为UPSA校友（企业管理学士+商法硕士）；其X账号@OscarOrtizA自署生日9月28日与es-Wikipedia出生日期1969-09-28一致；es-Wikipedia信息框（Wikidata Q6174897）已将「UPSA校长（2026-09-01起）」列为现任职务。需与玻利维亚其他同名者（如艺人Oscar Ortiz等）区分。另注：其2021-2026年任UCB圣克鲁斯校区校长（BO-ACAD-008），与任务背景所述库内UCB相关建档人物（BO-PERSON-000325）分属不同职务层面，无冲突；治理层职务属BO-PERSON-000337（Juan Federico Stelzer Castedo，UPSA基金会董事会主席），勿与本档案人物混淆。",
    "contacts": [
        {
            "type": "website",
            "value": "https://oscarortiz.com.bo",
            "source": "X账号@OscarOrtizA自署网址 + es-Wikipedia外链"
        }
    ],
    "current_positions": [
        "圣克鲁斯私立大学（UPSA）校长（Rector）",
        "新民主基金会（Fundación Nueva Democracia）主席"
    ],
    "education": [
        {
            "institution": UPSA_ORG,
            "degree": "bachelor",
            "field": "企业管理（Administración de Empresas）",
            "description": "本科毕业于UPSA企业管理专业；2026年以校友身份回归母校出任校长，基金会董事会主席Stelzer在就职典礼上称「Oscar回归他的母校（vuelve a su alma mater）」。",
            "source": "UPSA就职通稿（El Deber全文转载）+ es-Wikipedia + eju.tv 2021-11背景资料（三源一致）"
        },
        {
            "institution": UPSA_ORG,
            "degree": "master",
            "field": "商法（Derecho Empresarial）",
            "description": "获UPSA商法硕士学位。",
            "source": "UPSA就职通稿（El Deber全文转载）+ es-Wikipedia + eju.tv 2021-11背景资料（三源一致）"
        },
        {
            "institution": "南方大学IAE商学院 (IAE Business School, Universidad Austral)",
            "degree": "professional",
            "field": "高级管理（Programa de Alta Dirección）",
            "country": "AR",
            "note": "高管培训项目；仅见eju.tv 2021-11就任背景资料单一来源，置信度中等。",
            "source": "eju.tv 2021-11（「Realizó el programa de Alta Dirección IAE Business School de la Universidad Austral de Argentina」）"
        },
        {
            "institution": "马里斯塔学校 (Colegio Marista)",
            "degree": "high_school",
            "field": None,
            "location": "圣克鲁斯-德拉谢拉",
            "note": "中学就读于圣克鲁斯Colegio Marista；仅es-Wikipedia单一来源提及。",
            "source": "es-Wikipedia"
        }
    ],
    "work_experience": [
        {
            "organization": UPSA_ORG,
            "org_id": "BO-ACAD-010",
            "position": "校长 (Rector)",
            "start_date": "2026-09",
            "end_date": None,
            "is_current": "true",
            "start_date_note": "任职时间双口径：es-Wikipedia信息框记任命自2026-09-01起生效；正式授职仪式于2026-09-17在UPSA会议中心举行（UPSA官方通稿及El Diario、El Deber、Red Uno、InfoRSE等多源一致）。start_date取月份粒度。",
            "description": "经UPSA基金会董事会决议任命，接替执掌22年的前校长Lauren Müller de Pacheco。就职演说回顾CAINCO于1984年创校的历史，提出以「2034地平线（Horizonte 2034）」战略规划治校，治校重点包括扎根区域需求的研究、与生产部门的联动、与毕业生的长期关系、国际化及伦理人格培养。",
            "source": "UPSA官方通稿（经El Deber/InfoRSE全文转载核对；官网原文页反爬）+ El Diario 2026-10-05 + es-Wikipedia信息框"
        },
        {
            "organization": "玻利维亚天主教大学圣巴勃罗 (Universidad Católica Boliviana San Pablo)",
            "org_id": "BO-ACAD-008",
            "position": "圣克鲁斯校区校长 (Rector de Sede Santa Cruz)",
            "start_date": "2021-11",
            "end_date": "2026-09",
            "start_date_note": "2021年11月15日前后经UCB公告就任（eju.tv、El Deber、Unitel、notibol等2021-11报道；UCB官网新闻页存档）。",
            "end_date_note": "2026年9月转任UPSA校长后卸任（es-Wikipedia记「hasta septiembre de 2026」）；其X账号简介在此前仍署「Rector de la @UCatolicaSC」。",
            "description": "由UCB聘任主持圣克鲁斯校区，完成从政界向大学管理岗位的转型；UCB官网新闻称「Oscar Ortiz ha tomado posesión como rector de sede Santa Cruz」。",
            "source": "eju.tv 2021-11 + El Deber 2021-11 + UCB官网新闻（搜索摘要印证）+ es-Wikipedia"
        },
        {
            "organization": "经济与公共财政部 (Ministerio de Economía y Finanzas Públicas)",
            "org_id": "BO-GOV-005",
            "position": "部长 (Ministro)",
            "start_date": "2020-07-07",
            "end_date": "2020-09-28",
            "description": "在阿涅斯（Jeanine Áñez）临时政府改任经济与公共财政部长（前任José Luis Parada，继任Branko Marinković）；2020-07-16曾因感染新冠入重症监护（其妻Ojdana Salvatierra向媒体证实），2020-09-28以与内阁部分成员存在内部分歧为由去职。",
            "source": "es-Wikipedia信息框与正文 + Correo del Sur 2020-07-16 + Erbol报道（经Wikipedia引用）"
        },
        {
            "organization": "生产发展与多元经济部 (Ministerio de Desarrollo Productivo y Economía Plural)",
            "org_id": "BO-GOV-012",
            "position": "部长 (Ministro)",
            "start_date": "2020-05-08",
            "end_date": "2020-07-07",
            "description": "获临时总统阿涅斯任命出任该职，使命是在新冠（COVID-19）卫生紧急状态下推动经济重启与保就业。",
            "source": "es-Wikipedia信息框与正文"
        },
        {
            "organization": SENATE_ORG,
            "org_id": "BO-GOV-021",
            "org_id_note": "org_id取索引登记的上一级机构多民族立法大会（BO-GOV-021）；参议院为其组成机构。",
            "position": "参议员 (Senador por Santa Cruz)",
            "start_date": "2015-01-22",
            "end_date": "2020-05-08",
            "description": "代表圣克鲁斯省由团结民主联盟（Unidad Demócrata, UD）当选；任宪法、人权、立法与选举制度委员会委员。信息框所载任期止于2020-05-08（就任部长当日）。同期曾参与2019年11-12月议会对话桌，促成和平与宪法过渡协议。",
            "source": "es-Wikipedia信息框与正文"
        },
        {
            "organization": SENATE_ORG,
            "org_id": "BO-GOV-021",
            "org_id_note": "org_id取索引登记的上一级机构多民族立法大会（BO-GOV-021）。",
            "position": "参议员 (Senador por Santa Cruz)",
            "start_date": "2006-01-22",
            "end_date": "2010-01-22",
            "description": "2005年投身政坛，代表圣克鲁斯省由社会民主力量党（PODEMOS）首次当选参议员；2008年与PODEMOS决裂，创立公民团体Consenso Popular（后与Samuel Doria Medina阵营结盟）。",
            "source": "es-Wikipedia信息框与正文"
        },
        {
            "organization": SENATE_ORG,
            "org_id": "BO-GOV-021",
            "org_id_note": "org_id取索引登记的上一级机构多民族立法大会（BO-GOV-021）。",
            "position": "参议院议长 (Presidente de la Cámara de Senadores)",
            "start_date": "2008-01-22",
            "end_date": "2010-01-22",
            "description": "主持参议院（多民族宪法前的国会时期）。eju.tv就任背景资料记为「参议院主席2008-2009」，es-Wikipedia信息框记2008-01-22至2010-01-22，取后者。",
            "source": "es-Wikipedia信息框 + eju.tv 2021-11背景资料"
        },
        {
            "organization": "圣克鲁斯省政府 (Gobierno Autónomo Departamental de Santa Cruz)",
            "org_id": None,
            "position": "机构协调秘书长 (Secretario Departamental de Coordinación Institucional)",
            "start_date": "2010",
            "end_date": "2014",
            "description": "应新当选省长Rubén Costas之邀出任，为省府内阁成员。",
            "source": "es-Wikipedia正文 + El Deber/UPSA就职通稿"
        },
        {
            "organization": "圣克鲁斯工业、商业、服务与旅游商会 (Cámara de Industria, Comercio, Servicios y Turismo de Santa Cruz, CAINCO)",
            "org_id": None,
            "position": "总经理 (Gerente General)，此前历任外贸顾问、研究与项目部主任、规划与发展经理",
            "start_date": "1991",
            "end_date": "2006",
            "note": "任职年限双口径：es-Wikipedia记其在CAINCO整体任职1991-2005；UPSA就职通稿（El Deber/El Diario转载）记1999-2006任总经理、1991年起即在商会任职。end_date取2006（2006年1月就任参议员）。",
            "description": "在商会系统工作15年以上并官至总经理，职业起点为外贸领域。",
            "source": "El Deber/UPSA就职通稿 + es-Wikipedia + eju.tv 2021-11背景资料"
        },
        {
            "organization": "房屋与基本服务部 (Ministerio de Vivienda y Servicios Básicos)",
            "org_id": None,
            "position": "总顾问 (Asesor General)",
            "start_date": None,
            "end_date": None,
            "description": "早年公职经历之一；具体年份未公开。",
            "source": "es-Wikipedia正文（单一来源）"
        },
        {
            "organization": "外贸与投资部 (Ministerio de Comercio Exterior e Inversión)",
            "org_id": None,
            "position": "首席顾问 (Asesor Principal)",
            "start_date": None,
            "end_date": None,
            "description": "早年公职经历之一；具体年份未公开。",
            "source": "es-Wikipedia正文（单一来源）"
        },
        {
            "organization": UPSA_ORG,
            "org_id": "BO-ACAD-010",
            "position": "研究生层次领导力课程教授 (Profesor de Liderazgo, Posgrado)",
            "start_date": None,
            "end_date": None,
            "note": "任教时段未公开（至迟2021年11月UCB就任前）。",
            "description": "曾在UPSA研究生层次教授领导力课程。",
            "source": "eju.tv 2021-11就任背景资料"
        },
        {
            "organization": "新民主基金会 (Fundación Nueva Democracia)",
            "org_id": None,
            "position": "主席 (Presidente)",
            "start_date": None,
            "end_date": None,
            "is_current": "true",
            "description": "该非营利机构推动民主价值、公共政策研究与公民及政治领导力培养；es-Wikipedia以「Actualmente（目前）」记述。",
            "source": "es-Wikipedia"
        },
        {
            "organization": "「与奥斯卡·奥尔蒂斯面对面」数字节目 (De Frente con Oscar Ortiz)",
            "org_id": None,
            "position": "主持人兼总监",
            "start_date": None,
            "end_date": None,
            "is_current": "true",
            "description": "分析经济、政治与国际时事的个人数字评论节目，以播客形式发行于Spotify、Apple Podcasts等平台。",
            "source": "Spotify/Apple Podcasts节目页 + es-Wikipedia"
        },
        {
            "organization": "Publico.bo 门户 (Publico.bo)",
            "org_id": None,
            "position": "总监",
            "start_date": None,
            "end_date": None,
            "is_current": "true",
            "description": "倡导公共辩论与玻利维亚现代化的数字媒体门户。",
            "source": "es-Wikipedia"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000337",
            "person_name": "胡安·费德里科·施泰泽·卡斯特多 (Juan Federico Stelzer Castedo)",
            "relationship_type": "superior",
            "description": "UPSA基金会（Fundación UPSA）董事会主席，为其校长职位的任命上级：2026-09-17就职典礼上由基金会副董事长宣读董事会任命决议，Stelzer亲自为其披校长袍、授校长勋章，并致辞要求其依「2034地平线」战略与基础设施总规划引领大学。（person_id对应同期待建档任务BO-PERSON-000337。）",
            "source": "El Deber（UPSA官方通稿全文）+ El Diario 2026-10-05"
        },
        {
            "person_id": "BO-PERSON-000338",
            "person_name": "劳伦·米勒·德·帕切科 (Lauren Müller de Pacheco)",
            "relationship_type": "other",
            "description": "UPSA校长职位直接前任：在UPSA服务40年、任校长22年，2026年9月卸任；Ortiz在就职演说中向其及前总经理Tihana Vranjican（任职30余年）致谢。（person_id对应同期待建档任务BO-PERSON-000338。）",
            "source": "El Diario 2026-10-05 + El Deber（UPSA官方通稿全文）"
        },
        {
            "person_id": "BO-PERSON-000549",
            "person_name": "珍妮娜·阿涅斯 (Jeanine Áñez)",
            "relationship_type": "superior",
            "description": "2020年玻利维亚临时总统，先后任命Ortiz为生产发展与多元经济部长（2020-05-08）和经济与公共财政部长（2020-07-07）。",
            "source": "es-Wikipedia信息框与正文"
        },
        {
            "person_id": "BO-PERSON-000504",
            "person_name": "鲁文·科斯塔斯 (Rubén Costas)",
            "relationship_type": "political_ally",
            "description": "2010年当选圣克鲁斯省省长后，邀请Ortiz出任省政府机构协调秘书长（2010-2014）。",
            "source": "es-Wikipedia正文"
        },
        {
            "person_id": "BO-PERSON-000481",
            "person_name": "萨穆埃尔·多利亚·梅迪纳 (Samuel Doria Medina)",
            "relationship_type": "political_ally",
            "description": "Ortiz 2008年脱离PODEMOS创立公民团体Consenso Popular后，与Doria Medina领导的力量结盟（UN-CP联盟时期）共同参与选举政治。",
            "source": "es-Wikipedia正文"
        },
        {
            "person_id": None,
            "person_name": "塞尔希奥·达加·梅里达 (Sergio Daga Mérida)",
            "relationship_type": "colleague",
            "description": "UPSA现任副校长（Vicerrector）兼学术委员会主席；2026-09-17校长就职典礼由其开场致词。",
            "source": "El Deber（UPSA官方通稿全文）+ El Diario 2026-10-05"
        }
    ],
    "social_accounts": [
        {
            "platform": "twitter_x",
            "account_name": "@OscarOrtizA",
            "url": "https://x.com/OscarOrtizA",
            "source": "X站内检索确认（简介自署「oscarortiz.com.bo」、出生日期September 28，与es-Wikipedia一致）"
        },
        {
            "platform": "facebook",
            "account_name": "Oscar Ortiz (@oscar.ortiz.antelo)",
            "url": "https://www.facebook.com/oscar.ortiz.antelo/",
            "source": "Facebook站内检索确认（认证公共主页，简介已更新为「Rector Universidad Privada de Santa Cruz de la Sierra (UPSA)」，约13.5万赞）"
        },
        {
            "platform": "linkedin",
            "account_name": "Oscar Ortiz Antelo",
            "url": "https://www.linkedin.com/in/oscar-ortiz-antelo-rectoruca/",
            "source": "LinkedIn站内检索确认（显示Universidad Privada de Santa Cruz de la Sierra任职及UPSA就职帖文）"
        },
        {
            "platform": "other",
            "account_name": "De Frente con Oscar Ortiz（Spotify播客）",
            "url": "https://open.spotify.com/show/6SaDje7Z5QoWF8PkVIW5Y3",
            "source": "Spotify节目页检索确认（另见Apple Podcasts id1556726459）"
        }
    ],
    "social_accounts_note": "六平台扫描结果：X（@OscarOrtizA）、Facebook（oscar.ortiz.antelo）、LinkedIn（oscar-ortiz-antelo-rectoruca）三个个人账号均经站内检索确认；Instagram、TikTok、YouTube未发现本人账号——Instagram相关内容均为UPSA官方账号@upsabolivia发帖，TikTok同名账号均为他人，其评论节目以Spotify/Apple Podcasts播客形式发行（记入other平台）。",
    "family_members": [
        {
            "person_id": None,
            "name": "奥达娜·萨尔瓦铁拉 (Ojdana Salvatierra)",
            "relationship": "spouse",
            "industry_or_organization": None,
            "description": "妻子；2019年大选期间曾公开撰文为丈夫辩护（Los Tiempos/Fides报道），2020年其夫感染新冠入ICU期间向媒体证实病情（Correo del Sur）。",
            "source": "es-Wikipedia信息框 + Los Tiempos 2019-10-15 + Correo del Sur 2020-07-16 + ASC教会公报（多源一致）"
        }
    ],
    "family_note": "育有三名子女，姓名未公开，按规范不入条目（ASC教会公报与es-Wikipedia双源证实「padre de tres hijos」）。",
    "children_note": "有三名子女（姓名未公开；来源：campanas.iglesiasantacruz.org 2021-11 + es-Wikipedia）。",
    "political_stances": [
        {
            "date": "2016",
            "topic": "21F修宪公投与连任限制",
            "stance_content": "作为主要反对派领导人之一，捍卫2016年2月21日修宪公投结果、反对取消连任限制；并代表反对派领袖向美洲国家间人权委员会（CIDH）提交申诉，要求尊重公投结果、防止宪法秩序断裂。",
            "source": "https://es.wikipedia.org/wiki/%C3%93scar_Ortiz_Antelo"
        },
        {
            "date": "2016",
            "topic": "议会监督与反腐败",
            "stance_content": "任参议员期间以议会监督见长，提交逾20份监督报告，系统揭露原住民基金（Fondo Indígena）腐败、CAMC合同、Gabriela Zapata影响力案、中国驳船租赁、YPFB钻机采购及MAS政府直接委托采购等事件。",
            "source": "https://es.wikipedia.org/wiki/%C3%93scar_Ortiz_Antelo"
        },
        {
            "date": "2019-04",
            "topic": "委内瑞拉危机",
            "stance_content": "以参议员暨总统候选人身份公开声援委内瑞拉临时总统瓜伊多（Juan Guaidó），呼吁委内瑞拉军队避免暴力、服务于人民。",
            "source": "https://x.com/oscarortiza/status/1123270881709572097"
        },
        {
            "date": "2019-11",
            "topic": "2019年选举危机与宪法过渡",
            "stance_content": "2019年10月大选因舞弊争议被废止引发政治危机后，作为反对派领导人参与多民族立法议会对话桌，促成和平协议与宪法过渡（阿涅斯接任临时总统）；2020-12-21以抗议党内「专断作风」为由退出自己参与创立的Demócratas党，淡出党派政治。",
            "source": "https://es.wikipedia.org/wiki/%C3%93scar_Ortiz_Antelo（含Erbol报道链接）"
        }
    ],
    "political_stances_note": "上述立场均为其2016-2020年从政期间公开表态；2021年转入大学管理岗位后未发现新党派政治表态，就任UPSA校长后的公开言论集中于高等教育质量、AI时代人才培养与地区发展。",
    "major_achievements": [
        {
            "date": "2008",
            "achievement": "当选并出任玻利维亚参议院议长（2008-01-22至2010-01-22）。",
            "organization": SENATE_ORG
        },
        {
            "date": "2017",
            "achievement": "出版《Crónica de una Traición》（背叛编年史），系统调查原住民基金（Fondo Indígena）腐败案；另发布CAMC合同、UPRE「玻利维亚在变」计划、Montero-Bulo Bulo铁路等多份参议院监督报告。",
            "organization": None
        },
        {
            "date": "2019",
            "achievement": "获「玻利维亚说不」联盟推举为总统候选人，参加2019年10月20日大选（竞选搭档为科恰班巴参议员Shirley Franco）；该次选举后因舞弊争议被废止。",
            "organization": "玻利维亚说不联盟 (Alianza Bolivia Dice No)"
        },
        {
            "date": "2021-11",
            "achievement": "出任玻利维亚天主教大学圣巴勃罗（UCB）圣克鲁斯校区校长，完成从政界向大学管理岗位的转型。",
            "organization": "玻利维亚天主教大学圣巴勃罗 (Universidad Católica Boliviana San Pablo)"
        },
        {
            "date": "2026-09",
            "achievement": "经UPSA基金会董事会决议出任圣克鲁斯私立大学（UPSA）校长（2026-09-17正式就职），以校友身份回归母校执掌玻利维亚声誉领先的私立大学。",
            "organization": UPSA_ORG
        },
        {
            "date": "2026-10",
            "achievement": "获玻利维亚空军授予「杰出服务」勋章（Medalla Servicios Distinguidos）。",
            "organization": "玻利维亚空军 (Fuerza Aérea Boliviana)"
        }
    ],
    "honors": "2026年10月获玻利维亚空军「杰出服务」勋章（Medalla Servicios Distinguidos）（UPSA官方Instagram 2026-10-10帖文）。",
    "public_activities": [
        "2026-09-17：在UPSA会议中心出席就职授职典礼并发表就职演说，省长Juan Pablo Velasco、市长Manuel Saavedra及CAINCO、司法、学界、企业界代表出席。",
        "2026-10-10：接受玻利维亚空军授予的「杰出服务」勋章（UPSA官方Instagram帖文）。",
        "2026-10-12：在UPSA活动中就人才培养表态，称主要挑战是培养兼具技术能力与判断力的专业人才（UPSA官方Instagram帖文）。"
    ],
    "biography_summary": "奥斯卡·奥尔蒂斯·安特洛（Óscar Miguel Ortiz Antelo），1969年9月28日生于玻利维亚圣克鲁斯-德拉谢拉，企业管理者、前政界要员，2026年9月起任母校圣克鲁斯私立大学（UPSA）校长。他毕业于UPSA企业管理专业并获该校商法硕士学位，曾在阿根廷南方大学IAE商学院修读高级管理课程；1991年起在圣克鲁斯工业、商业、服务与旅游商会（CAINCO）任职至总经理（1999-2006）。2005年投身政坛，代表PODEMOS当选参议员（2006-2010）并出任参议院议长（2008-2010），2010-2014年任圣克鲁斯省政府机构协调秘书长，2015-2020年再度当选参议员，2019年以「玻利维亚说不」联盟候选人身份竞选总统；2020年在阿涅斯临时政府中先后出任生产发展与多元经济部长和经济与公共财政部长，同年12月退出政党政治。2021年11月出任玻利维亚天主教大学圣克鲁斯校区校长。2026年9月17日经UPSA基金会董事会决议正式就任UPSA校长，提出以「2034地平线」战略规划、科研与产业联结、毕业生长期关系和国际化为治校重点。他兼任新民主基金会主席，主持数字评论节目「De Frente con Oscar Ortiz」并掌Publico.bo门户；已婚，育有三名子女。",
    "profile": {
        "source_url": "https://commons.wikimedia.org/wiki/File:Oscar_Miguel_Ortiz_Antelo_(51906320667).jpg",
        "local_path": "photos/BO-PERSON-000336.jpg"
    },
    "profile_note": "肖像取自Wikimedia Commons（2019年摄影，es-Wikipedia词条信息框用图），经本地代理下载至photos/BO-PERSON-000336.jpg（1366x2048 JPEG）。",
    "position_note": "UPSA校长任职时间双口径：任命决议生效日es-Wikipedia记2026-09-01，正式就职仪式2026-09-17（UPSA通稿及多家媒体），档案start_date取「2026-09」。UCB圣克鲁斯校区校长任期2021-11至2026-09（转任UPSA）。",
    "work_note": "CAINCO任职年限双口径：es-Wikipedia记整体任职1991-2005，UPSA就职通稿记1999-2006任总经理、1991年起即在商会任职，end_date取2006（2006年1月就任参议员）。另曾任基金会UPSA、圣克鲁斯私人企业家联合会（FEPC）、全国工业协会（CNI）、全国商会（CNC）、玻利维亚外贸协会（IBCE）、圣克鲁斯博览会（FEXPOCRUZ）、圣克鲁斯青年企业家协会（AJE）、FUNDES Bolivia董事；曾任拉美政党联盟（UPLA）主席与国际民主联盟（IDU）副主席（年份未公开，es-Wikipedia）；亦为国际天主教立法者网络（ICLN）成员（ASC教会公报）。房屋与基本服务部总顾问、外贸与投资部首席顾问两段早年公职年份未公开。",
    "education_note": "企业管理学士与商法硕士均由UPSA授予（es-Wikipedia、eju.tv就任背景资料、UPSA就职通稿三源一致）；IAE商学院高级管理课程仅见eju.tv背景资料单一来源；中学就读圣克鲁斯Colegio Marista仅见es-Wikipedia，均已在条目note中标注置信度。",
    "collection_meta": {
        "collection_date": "2026-10-27",
        "phase": "phase4_person_profile",
        "data_sources": ["wikipedia", "news_search", "social_media", "web_search"],
        "notes": "数据来源与验证：全文精读4个独立来源——El Diario 2026-10-05就职报道（WebFetch直取）、es-Wikipedia词条（read_url直取，含信息框与履历正文）、El Deber就任报道（read_url直取，为UPSA官方通稿全文）、eju.tv 2021-11 UCB就任报道（read_url直取，含官方背景资料）；另以UPSA官网/UCB官网/Unitel/Red Uno/InfoRSE/ANF/Los Tiempos/Fides/Correo del Sur/ASC教会公报搜索摘要交叉印证（UPSA官网原文页307反爬，其通稿内容经El Deber/InfoRSE转载核对）。核心事实（UPSA校长身份与就职日期、UCB校区校长任期、两任部长、参议员与议长任期、出生日期地点、配偶与子女数、学历）均有≥2独立来源。同名甄别为本次重点：确认UPSA校长与前参议员/经济部长Óscar Ortiz Antelo为同一人（详见identity_note）。社交媒体六平台扫描完成（X/Facebook/LinkedIn确认，Instagram/TikTok/YouTube无本人账号）。存疑与差异：CAINCO任期2005/2006双口径；UPSA任命生效日2026-09-01与就职仪式日2026-09-17双口径；IAE高管课程、中学、两段早年部委任期为单一来源——均已在相应note字段标注。",
        "quotes": [
            {
                "title": "Oscar Ortiz Antelo asume como Rector de la UPSA（UPSA官方新闻）",
                "url": "https://www.upsa.edu.bo/oscar-ortiz-antelo-asume-como-rector-de-la-upsa"
            },
            {
                "title": "Óscar Ortiz, nuevo Rector de la UPSA（El Diario, 2026-10-05）",
                "url": "https://www.eldiario.net/portal/2026/10/05/oscar-ortiz-nuevo-rector-de-la-upsa/"
            },
            {
                "title": "Oscar Ortiz Antelo asume como rector de la UPSA（El Deber，UPSA官方通稿全文）",
                "url": "https://eldeber.com.bo/te-puede-interesar/oscar-ortiz-antelo-asume-rector-upsa_1789840740"
            },
            {
                "title": "Óscar Ortiz asume como rector de la Universidad Católica en Santa Cruz（eju.tv, 2021-11）",
                "url": "https://eju.tv/2021/11/oscar-ortiz-asume-como-rector-de-la-universidad-catolica-en-santa-cruz/"
            },
            {
                "title": "Óscar Ortiz Antelo — Wikipedia en español",
                "url": "https://es.wikipedia.org/wiki/%C3%93scar_Ortiz_Antelo"
            },
            {
                "title": "Mgr. Oscar Ortiz fue Posesionado como nuevo Rector de la UCB de sede Santa Cruz（ASC Campanas教会公报, 2021-11）",
                "url": "https://campanas.iglesiasantacruz.org/mgr-oscar-ortiz-fue-posesionado-como-nuevo-rector-de-la-ucb-de-sede-santa-cruz/"
            }
        ]
    }
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(person, f, ensure_ascii=False, indent=2)

# quick self-checks
data = json.load(open(OUT, encoding="utf-8"))
bio_len = len(data["biography_summary"])
assert bio_len >= 200, f"biography too short: {bio_len}"
assert data["nationality"] == "BO"
assert data["gender"] == "male"
print("WROTE", OUT, "| bio_chars =", bio_len, "| work =", len(data["work_experience"]),
      "| edu =", len(data["education"]), "| rel =", len(data["person_relationships"]),
      "| social =", len(data["social_accounts"]), "| stances =", len(data["political_stances"]),
      "| achievements =", len(data["major_achievements"]), "| quotes =", len(data["collection_meta"]["quotes"]))

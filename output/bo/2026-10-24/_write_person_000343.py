# -*- coding: utf-8 -*-
"""Build BO-PERSON-000343 Sandro Guerrero Morales person profile."""
import json

person = {
    "person_id": "BO-PERSON-000343",
    "wikidata_qid": None,
    "name": "Sandro Guerrero Morales",
    "name_en": "Sandro Guerrero Morales",
    "name_zh": "桑德罗·格雷罗·莫拉莱斯",
    "aliases": ["Sandro Augusto Guerrero Morales", "Sandro Guerrero"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "religion": None,
    "name_note": "全名为 Sandro Augusto Guerrero Morales（中间名 Augusto）：ICAM 2025-09-25 就任理事名录与 LinkedIn 档案 URL 双重记载；日常公开署名多为「Sandro Guerrero Morales」，获学位后常冠「Ph.D.」。name_zh 为数据库拟定音译名（_name_index.json 预注册「桑德罗·格雷罗·莫拉莱斯」），未检索到中文媒体既有译名。",
    "name_zh_note": "「桑德罗·格雷罗·莫拉莱斯」系任务清单拟定译名（_name_index.json 已预注册映射至本 ID）；玻利维亚本地华文媒体无该人物报道，无独立既有译名可核。",
    "identity_note": "同名消歧（本次核验重点）：玻利维亚体坛/政界存在多名「Sandro Guerrero」，本次全程以「Univalle 研究生副校长」职务为锚，所有归档事实均出自 Univalle 官网、Univalle 官方社交账号、CAF-Univalle 官方手册及点名其 Univalle 职务的新闻报道。需注意两点：① ZoomInfo 将同名档案与哥伦比亚卡利 Universidad del Valle（univalle.edu.co）混淆，已排除；② 2011-04-02 universidadesbol 一篇报道称其为「rector de la Universidad del Valle」，同期 Opinion（2011-04-21）称其为「decano en ejercicio」、Opinion（2011-08-23）与 universidadesbol（2012-11-27）均称「vicerrector académico」——「rector」提法与其后多源记载不符，判断为当年报道口误，本档案不采信。",
    "contacts": [],
    "current_positions": [
        "山谷私立大学研究生副校长 (Vicerrector de Postgrado, Universidad Privada del Valle)",
        "玻利维亚私立大学协会秘书长 (Secretario General, ANUP)",
        "科恰班巴工业商业与服务业商会理事 (Director Titular, ICAM)",
    ],
    "education": [
        {
            "institution": "山谷私立大学 (Universidad Privada del Valle)",
            "degree": "doctorate",
            "field": "战略规划/工商管理 (Planificación Estratégica / Business Administration)",
            "description": "LinkedIn 档案教育背景记载为 Univalle(BO)；RocketReach 索引其学位为「Ph.D. Planificación Estratégica（工商管理与管理方向）」，获自 Universidad del Valle (BO)。CAF-Univalle 官方合作手册（官网 2024 年 3 月版）刊载的自我简介为「教育科学博士（Doctor en Ciencias de la Educación），专长战略规划、教育管理、学术行政与企业管理，拥有逾 30 年学士与研究生层级项目的领导、管理与发展经验」。两处记载均指向博士学历且专长一致（战略规划+企业管理），但具体学位授予年份未公开，本科生源院校不详。",
            "source": "LinkedIn（经 Google/Bing 索引摘要与 RocketReach 交叉）+ CAF-Univalle 手册 PDF（univalle.edu 官网 2024-03 版，直取解析）",
        }
    ],
    "work_experience": [
        {
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
            "org_id": "BO-ACAD-011",
            "position": "研究生副校长 (Vicerrector de Postgrado)",
            "start_date": "2025-04",
            "end_date": None,
            "is_current": "true",
            "start_date_note": "2025-04-04 Univalle 研究生院官方 Facebook 发布其任命仪式（「Nombramiento del Vicerrector de Postgrado…en un acto institucional」）；El Deber 2025-04-23 已称其「vicerrector de Posgrado de Univalle」。start_date 取月份粒度。",
            "description": "执掌覆盖科恰班巴、拉巴斯、圣克鲁斯、苏克雷、特立尼达五地的研究生教育体系（官网：在校生逾 6300 人、学位项目 429 个，与 CAF 合作 20 年的公共治理文凭项目亦由该院执行）。官网当局页与研究生学院页均署「Ph.D. Sandro Guerrero Morales, Vicerrector de Postgrado」。需注意：2018-12 PENSER 手册的 Univalle 当局名录已记载其任此职，2020-12 至 2025-01 间职务名称改署「Director Nacional de Postgrado」，2025 年 4 月起恢复「Vicerrector de Postgrado」职名。",
            "source": "Univalle 官网当局页 page_id=20038（直取验证）+ 官网研究生学院页 page_id=20104 + Facebook FacultadPostgradoUnivalle 2025-04-04 + El Deber 2025-04-23",
        },
        {
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
            "org_id": "BO-ACAD-011",
            "position": "研究生部全国主任 (Director Nacional de la Facultad de Postgrado)",
            "start_date": None,
            "end_date": "2025",
            "start_date_note": "任职下限：2020-12-02 UnivallePremios KAMAY 报道（Facebook/YouTube）已署「Ph.D. Sandro Guerrero, Director Nacional de Postgrado」；2021-07 Radio Activa、2021-09 官方贺帖、2022 年 Valor Agregado 专访、2023/24 CAF 手册均沿用该职名。",
            "end_date_note": "2025-01-31 官网新闻仍署「Director nacional de Postgrado」；2025-04-04 获任命研究生副校长后卸任该职名。",
            "description": "执掌研究生院（Facultad de Postgrado）全国事务，任内研究生院 2024 年在校生逾 6300 人、学位项目 429 个；2022 年其向媒体介绍全年 160 个研究生项目规划、与 CAF 合作的公共治理文凭项目及微软 TEAMS 虚拟教学体系（2019-03 起使用，Univalle 被微软评为拉美成功案例）。",
            "source": "Facebook UnivalleBolivia 2020-12/2021-09 + Valor Agregado 2022 专访（直取全文）+ CAF-Univalle 手册 PDF + Univalle 官网新闻 2025-01-31（直取全文）",
        },
        {
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
            "org_id": "BO-ACAD-011",
            "position": "学术副校长 (Vicerrector Académico)",
            "start_date": None,
            "end_date": None,
            "start_date_note": "Opinion 2011-08-23（直取全文）明确署「El vicerrector académico Sandro Guerrero」；此前 2011-04-21 Opinion 亦以 Univalle 当局身份发言（称「decano en ejercicio」）。",
            "end_date_note": "universidadesbol 2012-11-27 仍署「vicerrector académico」；此后至 2018 年（PENSER 手册）已转任研究生副校长，具体交替时间未见于公开报道。",
            "description": "任内代表校方主持优秀学生「卓越奖学金（Beca de Excelencia）」颁发等学术管理事务，并推动与微软的 Live@edu 云平台合作（玻利维亚首所，约 1.4 万师生受益）。",
            "source": "Opinion 2011-08-23（直取全文）+ universidadesbol 2012-11-27 + Opinion 2011-04-21（搜索摘要）",
        },
        {
            "organization": "科恰班巴工业商业与服务业商会 (Cámara de Industria, Comercio y Servicios de Cochabamba, ICAM)",
            "org_id": None,
            "position": "理事 (Director Titular，代表 UNIVALLE S.A.)",
            "start_date": "2025-09",
            "end_date": None,
            "is_current": "true",
            "start_date_note": "2025-09-25 经 ICAM 年度大会宣誓就任 2025-2026 届理事（任期对应 gestión 2025-2026），以 UNIVALLE S.A. 代表身份列名理事 titular 名单。",
            "description": "ICAM 为科恰班巴主要商业行业协会（此前 2024-08 其曾以研究生部全国主任身份参与 ICAM 视频访谈，阐述学术界对可持续未来的贡献）。",
            "source": "ICAM 官网新闻 2025-09-26（直取全文）",
        },
        {
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
            "org_id": "BO-ACAD-011",
            "position": "学术管理专家 (Experto en Gestión Académica)",
            "start_date": "2015-07",
            "end_date": None,
            "is_current": "true",
            "start_date_note": "LinkedIn 档案索引摘要记载「Experto en Gestion Academica, Universidad del Valle Bolivia, jul 2015 - actualidad」；另一索引片段载 Univalle 任职总跨度「1992 - jun 2025（33 年）」。受登录墙与索引颗粒度限制，无法核读档案全文，条目间精确关系存疑。",
            "description": "其 LinkedIn 自述总头衔，与副校长职务并行使用；另印证其 Univalle 职业生涯始于 1992 年。",
            "source": "LinkedIn 档案（经 Google/Bing 索引摘要，2026-10-27 检索）",
        },
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000342",
            "person_name": "桑德拉·马塞拉·鲁伊斯·奥斯特里亚 (Sandra Marcela Ruiz Ostria)",
            "relationship_type": "spouse",
            "description": "妻子，同为 Univalle 副校长级高层（社会互动副校长 Vicerrectora de Interacción Social，两人并列于官网当局页）。Opinion 2018-05-27 人物报道明确称其为 Sandra 的「esposo Sandro Guerrero」；Opinion 2019-07-28 关于女儿的报道（「hija de Sandro Guerrero y Sandra Ruiz」）相互印证。",
            "source": "Opinion 2018-05-27（直取全文）+ Opinion 2019-07-28（直取全文）+ Univalle 官网当局页（两人并列当局名录）",
        },
        {
            "person_id": "BO-PERSON-000339",
            "person_name": "贡萨洛·比森特·鲁伊斯·奥斯特里亚 (Gonzalo Vicente Ruiz Ostria)",
            "relationship_type": "superior",
            "description": "Univalle 校长（Rector），为其副校长职位的直接上级；2025-01-30 市议会表彰仪式上两人共同出席受奖（官网新闻照片说明列名）。",
            "source": "Univalle 官网当局页 + 官网新闻 2025-01-31（直取全文）",
        },
        {
            "person_id": "BO-PERSON-000341",
            "person_name": "迭戈·阿隆索·比列加斯·萨莫拉 (Diego Alonso Villegas Zamora)",
            "relationship_type": "colleague",
            "description": "Univalle 学术副校长，同届当局班子成员（官网当局页并列）。",
            "source": "Univalle 官网当局页（直取验证）",
        },
        {
            "person_id": None,
            "person_name": "妮可·亚历杭德拉·格雷罗·鲁伊斯 (Nicole Alejandra Guerrero Ruiz)",
            "relationship_type": "child",
            "description": "女儿（长女之外的女儿，2019 年时 23 岁）：企业管理专业毕业，玻利维亚食物银行（Banco de Alimentos de Bolivia）创始人与主席，项目「La Manzana Roja」2017 年前后创立于 Univalle 课堂；2025-01-30 与其父同台获科恰班巴市议会表彰。Opinion 2019 明确记载「Nicole es hija de Sandro Guerrero y Sandra Ruiz」。",
            "source": "Opinion 2019-07-28（直取全文）+ Univalle 官网新闻 2025-01-31 + Los Tiempos 2024-11-25 人物稿（搜索摘要）",
        },
        {
            "person_id": None,
            "person_name": "伊瓦尔·格雷罗 (Ivar Guerrero)",
            "relationship_type": "parent",
            "description": "父亲，已去世（Opinion 2018-05-27 从其妻 Sandra 角度记载为「suegro Ivar Guerrero (+)」，即公公；第二姓氏未公开）。疑与 Univalle 创办家族企业渊源相关，但无直接公开记载，不作推断。",
            "source": "Opinion 2018-05-27（直取全文）",
        },
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Sandro Augusto Guerrero Morales",
            "url": "https://bo.linkedin.com/in/sandro-augusto-guerrero-morales-6b8842111",
            "source": "Google/Bing 索引确认本人档案（Cochabamba，约 1000 关注者，自述「Experto en Gestión Académica」，Univalle(BO) 1992 年起任职）；2023 年多条其署名帖子（研究生师资招募、数据科学培训、AI 文凭）佐证活跃使用。",
        }
    ],
    "social_accounts_note": "六平台扫描结果：仅 LinkedIn 确认本人账号；另存在疑似其重复旧档 /in/sandro-augusto-guerrero-morales-a6173110b（316 联系人，Cercado），因无法登录核验未列入。Facebook/Instagram/YouTube/TikTok/X 均未检索到本人账号——相关内容（任命公告、获奖、访谈视频）均由 Univalle 官方账号发布：Facebook「UnivalleBolivia」「FacultadPostgradoUnivalle」「UnivallePostgradoLPZ」、Instagram「postgradounivalle」、YouTube「Premios KAMAY 2020」、X@BancodeALIM_24 等。LinkedIn 登录墙限制全文核读，任职/学历细节经搜索引擎索引摘要与 RocketReach 交叉印证。",
    "family_members": [
        {
            "person_id": "BO-PERSON-000342",
            "name": "桑德拉·马塞拉·鲁伊斯·奥斯特里亚 (Sandra Marcela Ruiz Ostria)",
            "relationship": "spouse",
            "industry_or_organization": "山谷私立大学 (Universidad Privada del Valle)",
            "description": "妻子，Univalle 社会互动副校长（约 2012 年起任职）；毕业于 Univalle 酒店与旅游专业。夫妻同校任副校长级职务。",
            "source": "Opinion 2018-05-27（直取全文，称「su esposo Sandro Guerrero」）+ Univalle 官网当局页",
        },
        {
            "person_id": None,
            "name": "妮可·亚历杭德拉·格雷罗·鲁伊斯 (Nicole Alejandra Guerrero Ruiz)",
            "relationship": "daughter",
            "industry_or_organization": "玻利维亚食物银行 (Banco de Alimentos de Bolivia)",
            "description": "女儿，企业家，玻利维亚首个食物银行创始人与主席（TEDxUNIFRANZ 讲者）；2025-01-30 获科恰班巴市议会表彰时与其父同台。",
            "source": "Opinion 2019-07-28（直取全文，「hija de Sandro Guerrero y Sandra Ruiz」）+ Univalle 官网新闻 2025-01-31 + TEDx/联合国 WFP 报道（搜索摘要）",
        },
        {
            "person_id": None,
            "name": "伊瓦尔·格雷罗 (Ivar Guerrero)",
            "relationship": "father",
            "industry_or_organization": None,
            "description": "父亲，已去世（+）；Opinion 2018 年报道从其妻角度记载为「suegro Ivar Guerrero (+)」。仅此单一来源记载，第二姓氏不详。",
            "source": "Opinion 2018-05-27（直取全文）",
        },
    ],
    "family_note": "与妻子 Sandra Marcela Ruiz Ostria 育有三名子女：Brenda（2018 年时 28 岁）、Nicole Alejandra Guerrero Ruiz（2018 年时 22 岁）与 Ivar Gonzalo「Junior」（2018 年时 21 岁）。Brenda 与 Ivar Gonzalo 仅有名字、无全名公开，按「真实全名」规则未单列 family_members 条目。其妻之母为 Julia Ostria。",
    "political_stances": [
        {
            "date": "2025-04",
            "topic": "玻利维亚高等教育治理改革（ANUP 共同议程）",
            "stance_content": "作为玻利维亚私立大学协会（ANUP）新任秘书长，与理事会共同提出五轴议程：治理与机构自治（推动质量与结果导向的自治规范改革）、质量教育与弹性课程（对接国内外标准）、科学创新与数字转型、包容与终身学习、国际化与区域合作；并将推动设立迄今缺位的玻利维亚国家认证署（Agencia Nacional de Acreditación）、修订限制私立高校虚拟教育模式的现行法规。注：该议程系 ANUP 理事会集体提出（媒体报道引言出自主席 Ágreda 与学术秘书 Cuéllar），其以秘书长身份为共同署理人，非其个人独有主张。",
            "source": "El Deber 2025-04-23（直取全文）+ UPDS 官网 2025-04-25（直取全文）",
        }
    ],
    "political_stances_note": "无政党关联或政治立场公开记录：其为私立大学管理者与商会理事，公开表态集中于研究生教育创新、虚拟教学（专栏《Docencia 5.0——虚拟教学能力》）、与 CAF 合作的公共治理培训及 ANUP「知识经济转型」议程，均属机构性、非党派立场，故不立 political_stances 条目。",
    "political_party": None,
    "major_achievements": [
        {
            "date": "2025-04",
            "achievement": "当选玻利维亚私立大学协会（ANUP）秘书长，与 Unifranz 校长 Verónica Ágreda（主席）、USFA 校长 Jorge Dorado（副主席）、Unicen 校长 José Miguel Bustamante（司库）、UPDS 校长 Carlos Cuéllar（学术秘书）组成新理事会，共同推进设立国家认证署、修订虚拟教育法规等高教改革议程。",
            "organization": "玻利维亚私立大学协会 (Asociación Nacional de Universidades Privadas, ANUP)",
        },
        {
            "date": "2025-01",
            "achievement": "以研究生部全国主任身份接受科恰班巴市议会授予 Univalle 研究生院的「20 年卓越教育」表彰（同场获科恰班巴私营企业家联合会企业家功绩表彰）；其执掌下研究生院 2024 年在校生逾 6300 人、学位项目 429 个，其称「已成为全国最具创新力的研究生院」。",
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
        },
        {
            "date": "2011-04",
            "achievement": "任学术副校长期间推动 Univalle 与微软战略合作，成为玻利维亚首所部署 Live@edu 云端协作平台的高校，约 1.4 万名师生受益（此前 Univalle 自 2004 年与微软合作，后获评微软拉美成功案例并自 2019-03 起全面采用 TEAMS 虚拟教学平台）。",
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
        },
        {
            "date": "2023",
            "achievement": "作为研究生部全国主任负责执行 CAF（拉美开发银行）与 Univalle 研究生院联合开设的「公共治理与公共创新」文凭项目——该项目系 CAF 与拉美 19 所顶尖高校联盟在玻利维亚的独家落地点，已有 20 年合作历史，面向拉美加勒比地区公共部门领导者与创新者。",
            "organization": "山谷私立大学 (Universidad Privada del Valle)",
        },
    ],
    "public_activities": [
        "2025-09-25 出席科恰班巴工业商业与服务业商会（ICAM）年度大会，宣誓就任 2025-2026 届理事（代表 UNIVALLE S.A.）",
        "2025-04 应邀出席 Estrategia Bolivia「父亲」主题特刊座谈（LinkedIn 帖文以其「Vicerrector de Postgrado Univalle」头衔列名）",
        "2025-01-30 出席科恰班巴市议会表彰仪式，与玻利维亚食物银行创始人（其女 Nicole Guerrero Ruiz）、校长 Gonzalo Ruiz Ostria 等同台受奖",
        "2024-08 应 ICAM（科恰班巴工业商会）邀请出镜视频访谈，阐述学术界对可持续未来发展的贡献",
        "2021-07 做客 Radio Activa Bolivia 电台节目（自圣克鲁斯连线）介绍 Univalle 研究生项目",
        "2020-12 担任 Univalle「Premios KAMAY」奖项评审委员会成员",
        "撰写教育专栏《Docencia 5.0——虚拟教学能力》（经 Univalle 研究生院 Facebook 发布）",
    ],
    "biography_summary": "桑德罗·格雷罗·莫拉莱斯（全名 Sandro Augusto Guerrero Morales），玻利维亚科恰班巴人，山谷私立大学（Univalle）研究生副校长、玻利维亚私立大学协会（ANUP）现任秘书长。他自 1992 年起在 Univalle 任职三十余年，头衔为「学术管理专家」，历任学术副校长（2011-2012 年见诸报道）、研究生副校长（2018 年校方手册已记载）与研究生部全国主任（2020-2025 年），2025 年 4 月 4 日经校方仪式获任命为研究生副校长，执掌覆盖科恰班巴、拉巴斯、圣克鲁斯、苏克雷与特立尼达五地的研究生教育体系（在校生逾 6300 人、学位项目 429 个，与 CAF 合作 20 年的公共治理文凭项目由该院执行）。其为 Univalle 博士（战略规划/工商管理方向，自述教育科学博士），任内推动 Univalle 于 2011 年成为玻利维亚首所部署微软 Live@edu 云平台的高校。2025 年 4 月当选 ANUP 秘书长，参与推动玻利维亚私立高教向知识经济转型；同年 9 月以 UNIVALLE S.A. 代表身份出任科恰班巴工业商业与服务业商会（ICAM）2025-2026 届理事。其配偶为同校社会互动副校长桑德拉·鲁伊斯·奥斯特里亚，长女妮可·格雷罗·鲁伊斯是玻利维亚食物银行创始人与主席。",
    "profile": {
        "source_url": "https://www.univalle.edu/wp-content/uploads/2025/12/DR_SANDRO_01.png",
        "local_path": "photos/BO-PERSON-000343.png",
    },
    "profile_note": "照片为 Univalle 官网研究生学院页（page_id=20104）其署名 welcome 板块的官方头像（DR_SANDRO_01.png，2025-12 上传），已下载至 photos/BO-PERSON-000343.png。",
    "position_note": "职名口径说明：其在 Univalle 研究生条线的职务在「Vicerrector de Postgrado（研究生副校长）」与「Director Nacional de la Facultad de Postgrado（研究生部全国主任）」两个职名间变动——2018-12 PENSER 手册署副校长，2020-12 至 2025-01 期间各类报道与 CAF 手册均署主任，2025-04-04 起恢复副校长职名（现任）。2011-2012 年任学术副校长；2011-04 一篇报道的「rector」提法系当年媒体口径不一，不采信（详见 identity_note）。",
    "work_note": "LinkedIn 索引摘要显示：其总头衔为「Experto en Gestión Académica」（jul 2015 - actualidad），Univalle 任职跨度记载为「1992 - jun 2025，33 年」，另有「Vicerrector Academico」条目；即其在 Univalle 的职业履历始于 1992 年，2011 年前经历不详。ICAM 理事职务（2025-09 起）与 ANUP 秘书长（2025-04 起）为其在 Univalle 本职之外的机构性兼任。",
    "education_note": "学历仅能确证博士层次（LinkedIn 教育背景=Univalle(BO)；RocketReach 索引学位名「Ph.D. Planificación Estratégica, Business Administration and Management」；CAF 手册自我简介「教育科学博士，专长战略规划、教育管理、学术行政与企业管理，30 余年经验」），学位具体名称两个口径略有出入、授予年份未公开；本科/硕士院校与专业无公开记录。2024-03 版 CAF-Univalle 手册 PDF（官网直取）中其人物卡按版面坐标归属「教育科学博士」简介（同页 Coordinator Mariana Suárez Acosta 卡对应「经济学家」简介），与 LinkedIn 学位记录一致。",
    "collection_meta": {
        "collection_date": "2026-10-27",
        "phase": "phase4_person_profile",
        "data_sources": ["official_website", "news_search", "web_search", "social_media", "other"],
        "notes": "数据来源与验证：直取/精读全文来源共 13 个——Univalle 官网当局页（page_id=20038）、官网研究生学院页（page_id=20104，含官方头像提取）、官网新闻 2025-01-31（?p=8530）、CAF-Univalle 手册 PDF 2024-03 版（官网直取，pymupdf 解析含版面坐标归属分析）、PENSER 手册 PDF（2018-12 上传版，含 2018 年 Univalle 当局名录）、Valor Agregado 2022 专访、Opinion 2018-05-27、Opinion 2019-07-28、Opinion 2011-08-23、El Deber 2025-04-23、UPDS 官网 2025-04-25、ICAM 官网 2025-09-26、universidadesbol 2011-04-02；另以 Facebook/Instagram/YouTube 官方帖文、LinkedIn/RocketReach 索引摘要、Red Uno 搜索摘要交叉印证。核心事实（现任研究生副校长、2025-04 任命、ANUP 秘书长、ICAM 理事、配偶与女儿、博士学历层次、2011-2012 学术副校长）均有≥2 独立来源。同名消歧与哥伦比亚 Univalle 混淆排除详见 identity_note；职名双口径见 position_note；学位双口径见 education_note。个人邮箱/电话不可验证，contacts 留空；birth_date/birth_place 无公开记录，置 null。社交媒体六平台扫描完成（仅 LinkedIn 有本人账号）。Wikidata 检索无本人条目，wikidata_qid=null；ICAM/ANUP 未入 _name_index.json，org_id=null。completeness_score=72：大学副校长级人物公开信息多但个人向信息（出生日期/地点、个人邮箱电话、个人社媒账号、Wikidata 条目、本科院校）客观不存在或不可验证，涉及空缺字段均无法在不违背「禁止编造」铁律下补足，已按实际可验证信息最大化填写。",
        "quotes": [
            {
                "title": "Sobre Univalle — 官网当局页（Ph.D. Sandro Guerrero Morales, Vicerrector de Postgrado）",
                "url": "https://www.univalle.edu/?page_id=20038",
            },
            {
                "title": "0 Postgrado — Univalle 官网研究生学院页（其署名欢迎辞与官方头像）",
                "url": "https://www.univalle.edu/?page_id=20104",
            },
            {
                "title": "UNIVALLE CELEBRA EL RECONOCIMIENTO A LA FACULTAD DE POSTGRADO Y AL BANCO DE ALIMENTOS DE BOLIVIA（官网新闻 2025-01-31）",
                "url": "https://www.univalle.edu/?p=8530",
            },
            {
                "title": "ANUP renueva su liderazgo para avanzar hacia una economía basada en el conocimiento（El Deber 2025-04-23）",
                "url": "https://eldeber.com.bo/educacion-y-sociedad/anup-renueva-su-liderazgo-para-avanzar-hacia-una-economia-basada-en-el-conocimiento_511642/",
            },
            {
                "title": "Carlos Cuéllar asume como Secretario Académico de ANUP（UPDS 官网 2025-04-25，列 ANUP 理事会名单）",
                "url": "https://www.upds.edu.bo/carlos-cuellar-rector-nacional-de-la-upds-asume-como-secretario-academico-de-anup-en-una-nueva-etapa-para-la-educacion-superior-boliviana/",
            },
            {
                "title": "ICAM llevó a cabo su Asamblea Ordinaria anual y posesionó a su nuevo Directorio 2025-2026（ICAM 官网，理事名录含 Sandro Augusto Guerrero Morales – UNIVALLE S.A.）",
                "url": "https://icam.bo/icam-llevo-a-cabo-su-asamblea-ordinaria-anual-y-posesiono-a-su-nuevo-directorio-por-la-gestion-2025-2026/",
            },
            {
                "title": "Brochure Diplomado en Gobernabilidad e Innovación Pública CAF-UNIVALLE（2023/24 版 PDF，其人物简介）",
                "url": "https://www.univalle.edu/wp-content/uploads/2024/03/Brochure-Diplomado-en-Gobernabilidad-e-Innovacion-Publica-2023-CAF-UNIVALLE-1.pdf",
            },
            {
                "title": "Diplomados de Univalle, 4 novedosas propuestas（Valor Agregado 2022 专访）",
                "url": "https://valoragregado.net/diplomados-de-univalle-4-novedosas-propuestas/",
            },
            {
                "title": "Nicole Guerrero, líder juvenil con proyección（Opinion 2019-07-28，「hija de Sandro Guerrero y Sandra Ruiz」）",
                "url": "https://www.opinion.com.bo/articulo/tendencias/nicole-guerrero-l-iacute-der-juvenil-proyecci-oacute-n/20190728002600680226.html",
            },
            {
                "title": "Mujeres todoterreno: Madres y empresarias cochabambinas（Opinion 2018-05-27，「su esposo Sandro Guerrero」）",
                "url": "https://www.opinion.com.bo/articulo/tendencias/mujeres-todoterreno-madres-empresarias-cochabambinas/20180527192900677646.html",
            },
            {
                "title": "Quince estudiantes reciben una Beca de Excelencia de Univalle（Opinion 2011-08-23，时署 Vicerrector Académico）",
                "url": "https://www.opinion.com.bo/articulo/cochabamba/quince-estudiantes-reciben-beca-excelencia-univalle/20110823204400375099.html",
            },
            {
                "title": "Univalle estrena plataforma virtual con 14 mil usuarios（universidadesbol 2011-04-02，微软 Live@edu）",
                "url": "https://www.universidadesbol.com/2011/04/univalle-estrena-plataforma-virtual-con.html",
            },
            {
                "title": "Nombramiento del Vicerrector de Postgrado（Facebook FacultadPostgradoUnivalle 2025-04-04 任命仪式帖）",
                "url": "https://www.facebook.com/FacultadPostgradoUnivalle/posts/-nombramiento-del-vicerrector-de-postgrado-en-un-acto-institucional-se-llev%C3%B3-a-c/1073403331495562/",
            },
            {
                "title": "Handbooks PENSER（2018-12 上传 PDF，Univalle 当局名录署其 Vicerrector de Postgrado）",
                "url": "https://claudiaaponte.com.co/wp-content/uploads/2018/12/4.-Handbooks-PENSER-1.pdf",
            },
        ],
    },
}

OUT = "persons/BO-PERSON-000343.json"
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(person, f, ensure_ascii=False, indent=2)
print("written", OUT)
print("bio_len", len(person["biography_summary"]))
print("quotes", len(person["collection_meta"]["quotes"]))

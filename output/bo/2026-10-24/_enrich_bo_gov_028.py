# -*- coding: utf-8 -*-
"""Phase 3 enrichment for BO-GOV-028 (Defensoría del Pueblo de Bolivia)."""
import json

FILE = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/orgs/BO-GOV-028.json"

with open(FILE, encoding="utf-8") as f:
    data = json.load(f)

# ---------- basic_info ----------
data["basic_info"]["aliases"] = ["Defensoría del Pueblo de Bolivia", "DPB", "玻利维亚人民监察署"]
data["basic_info"]["website"] = "https://www.defensoria.gob.bo"

# ---------- social_accounts (official site footer, fetched 2026-10-24) ----------
data["social_accounts"] = [
    {
        "platform": "twitter_x",
        "account_name": "@DPBoliviaOf",
        "url": "https://twitter.com/DPBoliviaOf",
        "source": "https://www.defensoria.gob.bo/（官网页脚官方社交媒体链接）",
    },
    {
        "platform": "facebook",
        "account_name": "Defensoría del Pueblo Bolivia",
        "url": "https://www.facebook.com/Defensor%C3%ADa-del-Pueblo-Bolivia-1420825398141777/",
        "source": "https://www.defensoria.gob.bo/（官网页脚官方社交媒体链接）",
    },
    {
        "platform": "instagram",
        "account_name": "@dpboliviaof",
        "url": "https://www.instagram.com/dpboliviaof/",
        "source": "https://www.defensoria.gob.bo/（官网页脚官方社交媒体链接）",
    },
    {
        "platform": "youtube",
        "account_name": "Defensoría del Pueblo Bolivia (频道 UCR5jjUzRigFaB0Pr7z4aGRA)",
        "url": "https://www.youtube.com/channel/UCR5jjUzRigFaB0Pr7z4aGRA",
        "source": "https://www.defensoria.gob.bo/（官网页脚官方社交媒体链接）",
    },
]

# ---------- digital_assets (official site links, fetched 2026-10-24) ----------
data["digital_assets"] = [
    {
        "name": "SIDENIB（监察员办公室国家信息系统）",
        "url": "https://sidenib.defensoria.gob.bo/#/",
        "description": "监察员办公室官方在线信息系统（SIDENIB），提供公民投诉受理与机构信息查询服务",
        "source": "https://www.defensoria.gob.bo/（首页服务入口）",
    },
    {
        "name": "Aula Virtual（人权教育虚拟课堂）",
        "url": "https://academico.defensoria.gob.bo",
        "description": "监察员办公室学术平台，提供人权教育在线课程（程序教育/教育项目板块）",
        "source": "https://www.defensoria.gob.bo/（首页 EDUCACIÓN EN DERECHOS HUMANOS 板块）",
    },
    {
        "name": "Defensoras y Defensores Estudiantiles（学生监察员平台）",
        "url": "https://estudiantil.defensoria.gob.bo",
        "description": "学生监察员计划官方平台，面向学校社群推广人权文化",
        "source": "https://www.defensoria.gob.bo/（首页专题入口）",
    },
    {
        "name": "Boletín Informativo（机构公报）",
        "url": "https://www.defensoria.gob.bo/boletin",
        "description": "监察员办公室定期新闻公报（另提供 Atom 订阅源 https://www.defensoria.gob.bo/atom）",
        "source": "https://www.defensoria.gob.bo/（首页通讯入口）",
    },
    {
        "name": "Monitoreo Defensorial del Estado de Excepción（紧急状态人权监测专栏）",
        "url": "https://www.defensoria.gob.bo/contenido/monitoreo-defensorial-del-estado-de-excepcion",
        "description": "2026年紧急状态期间设立的专项监测页面，跟踪封锁、军队部署等措施中的人权状况；另设社会冲突行为监测（Diálogos y Gestión de Paz）与司法检察监察观察站等专栏",
        "source": "https://www.defensoria.gob.bo/（首页专题横幅）",
    },
]

# ---------- key_people ----------
data["key_people"] = [
    {
        "person_id": None,
        "name": "佩德罗·弗朗西斯科·卡利萨亚·阿罗 (Pedro Francisco Callisaya Aro)",
        "title": "玻利维亚监察专员 (Defensor del Pueblo de Bolivia)",
        "title_description": (
            "第6任监察专员；2022年9月23日经多民族立法大会（ALP）选举产生，同年9月27日宣誓就任"
            "（官网历史页记载：elegido el 23/09/2022, posesionado el 27/09/2022），任期至2028年前后；"
            "2025年11月罗德里戈·帕斯政府更替后留任，2026年10月仍在任并在积极履职"
        ),
        "description": (
            "1966年生，玻利维亚人，讲西班牙语和艾马拉语。圣安德烈斯大学（UMSA）法学学士，"
            "安第斯西蒙·玻利瓦尔大学宪法与宪法诉讼法硕士，瑞典隆德大学Raúl Wallenberg研究所人权专业进修，"
            "UMSA与瓦伦西亚大学联合培养宪法与行政法博士候选人。2001年入职监察员办公室，曾任全国公民服务处"
            "（Unidad Nacional de Servicio a la Ciudadanía）主任；2016-2017年任联合国人权事务高级专员办公室"
            "人权专家；2021年任拉巴斯司法部门民事第一审判庭庭长。曾被多方描述为MAS阵营候选人（ANF报道），"
            "就任后与2025年上台的中间派帕斯政府保持机构独立并多次就人权问题发声"
        ),
    },
    {
        "person_id": None,
        "name": "纳迪娅·亚历杭德拉·克鲁斯·塔里法 (Nadia Alejandra Cruz Tarifa)",
        "title": "代理监察专员 (Defensora del Pueblo interina, 前任)",
        "title_description": "2019年1月30日至2022年9月23日以代理身份主持监察员办公室工作（前任专员辞职后立法大会长期未能选出继任者）",
        "description": "1982年生；时任监察专员副手（Defensora Adjunta），2019年1月Tezanos Pinto辞职后依法代理专员职务约3年7个月（西语维基记载2019-01-30至2022-09-23）",
    },
    {
        "person_id": None,
        "name": "戴维·阿隆索·特萨诺斯·平托·莱德斯马 (David Alonzo Tezanos Pinto Ledezma)",
        "title": "监察专员 (Defensor del Pueblo, 前任)",
        "title_description": "2016年5月13日至2019年1月24日在任（后辞职）",
        "description": "1976年生；法学士、刑事科学研究生，曾任多民族公设辩护服务局全国主任（2014-2016）及司法与基本权利总司长（2011-2014）",
    },
    {
        "person_id": None,
        "name": "罗兰多·比列纳·比列加斯 (Rolando Villena Villegas)",
        "title": "监察专员 (Defensor del Pueblo, 前任)",
        "title_description": "2010年5月13日至2016年5月13日在任（两届6年）",
        "description": "1947年生于波托西，2021年去世；神学家、玻利维亚卫理公会主教，2006-2009年任职于玻利维亚常设人权大会（APDHB）",
    },
    {
        "person_id": None,
        "name": "安娜·玛丽亚·罗梅罗·德·坎佩罗 (Ana María Romero de Campero)",
        "title": "首任监察专员 (Primera Defensora del Pueblo, 前任)",
        "title_description": "1998年5月13日至2003年3月31日在任，为该机构首任监察专员",
        "description": "1941-2010；玻利维亚著名记者、专栏作家，新闻基金会（Fundación UNIR）创始人；任内奠定了该机构的社会公信力",
    },
]

# ---------- departments (official /oficinas page, fetched 2026-10-24) ----------
HQ = "BO-GOV-028-DEPT-001"
offices = [
    ("拉巴斯国家总部 (Oficina Nacional – La Paz)", HQ,
     "机构总部，位于拉巴斯圣佩德罗区哥伦比亚街440号（Calle Colombia N°440, Zona San Pedro），电话2113600/2112600，免费热线800 10 8004；统筹全国各代表处与边境办事处工作"),
    ("拉巴斯代表处 (Oficina La Paz)", "BO-GOV-028-DEPT-002", "拉巴斯省省会城市代表处"),
    ("埃尔阿尔托代表处 (Oficina El Alto)", "BO-GOV-028-DEPT-003", "拉巴斯省埃尔阿尔托市代表处，服务于该市庞大的艾马拉族城市人口"),
    ("永加斯-卡拉纳维代表处 (Oficina Yungas - Caranavi)", "BO-GOV-028-DEPT-004", "拉巴斯省永加斯与卡拉纳维古柯种植区代表处"),
    ("科恰班巴代表处 (Oficina Cochabamba)", "BO-GOV-028-DEPT-005", "科恰班巴省代表处"),
    ("查帕雷代表处 (Oficina Chapare)", "BO-GOV-028-DEPT-006", "科恰班巴省查帕雷（古柯种植核心区）代表处"),
    ("圣克鲁斯代表处 (Oficina Santa Cruz)", "BO-GOV-028-DEPT-007", "圣克鲁斯省代表处，位于玻利维亚经济中心城市圣克鲁斯-德 la 谢拉"),
    ("苏亚雷斯港代表处 (Oficina Puerto Suárez)", "BO-GOV-028-DEPT-008", "圣克鲁斯省苏亚雷斯港，邻近巴西边境的矿业与贸易城市代表处"),
    ("利亚利亚瓜代表处 (Oficina Llallagua)", "BO-GOV-028-DEPT-009", "波托西省利亚利亚瓜（北部矿业城镇）代表处"),
    ("波托西代表处 (Oficina Potosí)", "BO-GOV-028-DEPT-010", "波托西省代表处"),
    ("比利亚松代表处 (Oficina Villazón)", "BO-GOV-028-DEPT-011", "波托西省比利亚松，阿根廷边境口岸代表处"),
    ("奥鲁罗代表处 (Oficina Oruro)", "BO-GOV-028-DEPT-012", "奥鲁罗省代表处"),
    ("皮西加代表处 (Oficina Pisiga)", "BO-GOV-028-DEPT-013", "奥鲁罗省皮西加，智利边境口岸代表处"),
    ("丘基萨卡-苏克雷代表处 (Oficina Chuquisaca - Sucre)", "BO-GOV-028-DEPT-014", "丘基萨卡省（首府苏克雷，宪法首都）代表处"),
    ("蒙特阿古多代表处 (Oficina Monteagudo)", "BO-GOV-028-DEPT-015", "丘基萨卡省蒙特阿古多地区代表处"),
    ("塔里哈代表处 (Oficina Tarija)", "BO-GOV-028-DEPT-016", "塔里哈省代表处"),
    ("亚奎瓦代表处 (Oficina Yacuiba)", "BO-GOV-028-DEPT-017", "塔里哈省亚奎瓦，阿根廷边境城市代表处"),
    ("贝尔梅霍代表处 (Oficina Bermejo)", "BO-GOV-028-DEPT-018", "塔里哈省贝尔梅霍，阿根廷边境口岸代表处"),
    ("贝尼代表处 (Oficina Beni)", "BO-GOV-028-DEPT-019", "贝尼省（首府特立尼达）代表处"),
    ("里韦拉尔塔代表处 (Oficina Riberalta)", "BO-GOV-028-DEPT-020", "贝尼省里韦拉尔塔（亚马逊北部地区）代表处"),
    ("潘多代表处 (Oficina Pando)", "BO-GOV-028-DEPT-021", "潘多省（首府科维哈，巴西亚马逊边境）代表处"),
    ("德萨瓜德罗代表处 (Oficina Desaguadero)", "BO-GOV-028-DEPT-022", "拉巴斯省德萨瓜德罗，秘鲁边境口岸代表处"),
]
data["departments"] = [
    {"name": n, "dept_id": d, "head": None, "description": desc,
     "parent_dept_id": (None if d == HQ else HQ)}
    for n, d, desc in offices
]

# ---------- recent_events ----------
data["recent_events"] = [
    {
        "date": "2026-10-22",
        "title": "监察专员发布2026年第三季度社会冲突报告：登记109起已爆发冲突，紧急状态背景下介入42%",
        "description": (
            "监察专员卡利萨亚在政府实施紧急状态的背景下发布《玻利维亚冲突监测报告》2026年第三期：全国共登记168起事件，"
            "其中109起为已爆发的冲突、59起为预告，社会紧张集中于国家中部轴线，诉求集中在食品、柴油与就业；"
            "监察员办公室及时介入了42%的已登记冲突，充当国家与民间之间的对话促进机构"
        ),
        "impact": "量化呈现2025年政权更替后经济危机引发的社会压力规模；巩固机构作为危机调解人的公共角色",
        "source": "https://www.defensoria.gob.bo/noticias/defensor-del-pueblo-informa-de-109-conflictos-con-demandas-de-alimentacion,-diesel-y-empleo-durante-tercer-trimestre-de-2026",
    },
    {
        "date": "2026-10-22",
        "title": "发布甘蔗与巴西栗收获季强迫劳动研究报告，揭露债役与童工迹象",
        "description": (
            "监察专员卡利萨亚发布研究报告《玻利维亚甘蔗与巴西栗收获季的强迫劳动、债役与最恶劣形式童工》"
            "（Trabajo forzoso, servidumbre por deudas y peores formas de trabajo infantil en la zafra de la caña y castaña），"
            "警示收获季工人中存在债役与劳工剥削迹象，敦促国家机关出台保护收获季工人及其家庭的公共政策"
        ),
        "impact": "将农业季节性劳工（zafra）权利问题推上公共政策议程，构成对劳动与反贩卖政策的直接督促",
        "source": "https://www.defensoria.gob.bo/noticias/defensor-del-pueblo-alerta-sobre-indicios-de-servidumbre-por-deudas-y-explotacion-laboral-en-las-zafras-de-canya-y-castanya",
    },
    {
        "date": "2026-09-17",
        "title": "紧急状态获90天延长；监察员办公室警告新冲突风险并持续人权监测",
        "description": (
            "6月20日生效的紧急状态（6月20日至9月18日期间全国公路封锁点由42处降至0处）到期之际，帕斯政府以仍有公共威胁和"
            "新封锁预告为由批准将紧急状态延长90天；监察员办公室同期警告尽管紧急状态延长，新冲突仍将出现，并持续发布封锁、"
            "军队部署等措施的人权监测信息"
        ),
        "impact": "机构在扩权措施延续的情况下保持批评性监督立场，平衡安全措施与人权保障",
        "source": "https://abi.bo/estado-de-excepcion-se-amplia-por-90-dias-que-implica-la-medida-y-hasta-cuando-regira/ ；https://www.instantaneas.org.bo/2026/09/26/corrupcion-transparencia-bolivia/estado-excepcion-bolivia-defensoria-conflictos",
    },
    {
        "date": "2026-06-20",
        "title": "帕斯总统签署第5636号最高法令，以内部骚乱（conmoción interna）为由在全国实施紧急状态；监察员办公室当日发表机构声明",
        "description": (
            "在农民等群体持续近一个月的公路封锁（峰值超过60处）并要求总统辞职的背景下，罗德里戈·帕斯总统于签署和平协定"
            "数小时后颁布第5636号最高法令（DS 5636），以内部骚乱（conmoción interna）为由在全国实施30天紧急状态并授权军队"
            "清障；监察员办公室同日就紧急状态颁布发布机构声明，宣布将持续监测人权状况"
        ),
        "impact": "2025年政权更替后首次全国紧急状态；监察员办公室成为紧急状态期间官方人权监测的核心机构",
        "source": "https://elpais.com/america/2026-06-20/paz-decreta-el-estado-de-excepcion-en-bolivia-horas-despues-de-firmar-el-acuerdo-de-pacificacion.html ；https://www.pixilegal.com/normativa/decreto-5636-2026-06-20 ；https://www.defensoria.gob.bo/noticias/defensor-del-pueblo-reporta-reduccion-de-bloqueos-y-monitorea-el-respeto-de-derechos-humanos-durante-el-estado-de-excepcion",
    },
    {
        "date": "2026-06-09",
        "title": "《紧急状态法》生效；监察员办公室通报抗议冲突已致至少10人死亡、37人受伤",
        "description": (
            "国会此前取消了总统宣布紧急状态须经议会批准的限制，《紧急状态法》于6月上旬生效；梵蒂冈新闻援引监察员办公室报告称，"
            "自抗议开始以来至少10人死亡、37人受伤；机构此前还通报因道路封锁延误就医致4人死亡"
        ),
        "impact": "机构伤亡统计成为国际媒体（RFI/Vatican News等）报道玻利维亚危机的关键人权数据来源",
        "source": "https://www.vaticannews.va/es/mundo/news/2026-06/bolivia-entra-en-vigor-la-ley-de-estados-de-excepcion.html ；https://radio.uchile.cl/2026/05/29/pedro-callisaya-defensor-del-pueblo-de-bolivia-un-estado-de-excepcion-no-va-a-solucionar-los-problemas-estructurales-del-pais/",
    },
    {
        "date": "2026-05-29",
        "title": "监察专员卡利萨亚对媒体表示紧急状态解决不了国家的结构性问题",
        "description": (
            "接受RFI采访时，卡利萨亚指出食品短缺与物价飞涨正在民众中制造绝望与对立情绪，警告社会内部分裂对抗的风险，"
            "并明确表示紧急状态作为应对手段结果难以预料，无法解决玻利维亚经济、社会与政治层面的结构性危机；"
            "6月2日他又呼吁各动员群体将抗议方式人道化并坚持对话解决（ABI报道）"
        ),
        "impact": "确立机构在政府与街头运动之间的独立调解立场，与帕斯政府的强力清障路线形成公开张力",
        "source": "https://radio.uchile.cl/2026/05/29/pedro-callisaya-defensor-del-pueblo-de-bolivia-un-estado-de-excepcion-no-va-a-solucionar-los-problemas-estructurales-del-pais/ ；https://abi.bo/defensor-del-pueblo-urge-a-humanizar-las-medidas-de-protesta-e-insiste-en-el-dialogo/",
    },
]

# ---------- related_entities ----------
data["related_entities"] = [
    {
        "org_id": "BO-GOV-021",
        "org_name": "多民族立法大会 (Asamblea Legislativa Plurinacional)",
        "org_type": "GOV",
        "org_description": "玻利维亚两院制立法机关；依据宪法与第870号法律负责选举产生监察专员（2022年9月23日选举卡利萨亚就任现职）",
        "relationship_type": "partner",
    },
    {
        "org_id": "BO-GOV-003",
        "org_name": "玻利维亚政府部 (Ministerio de Gobierno)",
        "org_type": "GOV",
        "org_description": "主管内政、公民安全与国家警察的内阁部门；与监察员办公室在紧急状态人权监测、社会冲突治理等事务上形成监督与协作关系（西语维基将其列为参见机构 véase también）",
        "relationship_type": "partner",
    },
    {
        "org_id": None,
        "org_name": "全球国家人权机构联盟 (GANHRI)",
        "org_type": "INTL",
        "org_description": "全球国家人权机构资格认证体系；监察员办公室持有其最高等级A级（status A）认证（官网明示），据此保持国际人权机构网络成员地位",
        "relationship_type": "member_of",
    },
    {
        "org_id": "BO-INTL-001",
        "org_name": "联合国 (Organización de las Naciones Unidas)",
        "org_type": "INTL",
        "org_description": "监察员办公室长期对接联合国人权体系：现任专员2016-2017年曾任人权高专办（OHCHR）专家；机构与联合国儿童基金会（UNICEF）、联合国妇女署（UN Women）、国际移民组织（IOM）等保持合作链接",
        "relationship_type": "partner",
    },
    {
        "org_id": "BO-NGO-005",
        "org_name": "玻利维亚常设人权大会 (Asamblea Permanente de Derechos Humanos de Bolivia)",
        "org_type": "NGO",
        "org_description": "玻利维亚历史最久的民间人权组织之一；与监察员办公室同属人权保护领域机构（第3任监察专员罗兰多·比列纳曾任该会领导职务），形成官民人权网络互补",
        "relationship_type": "partner",
    },
    {
        "org_id": None,
        "org_name": "圣克鲁斯克雷尼奥人监察署 (Defensoría de las Cruceñas y los Cruceños)",
        "org_type": "GOV",
        "org_description": "2026年10月16日依圣克鲁斯省第429号省法设立的省级监察机构（落实自治条例第118条）；国家监察员办公室发表声明对其成立予以肯定，二者构成职能相近的上下层级人权申诉体系",
        "relationship_type": "affiliated",
    },
]

# ---------- core_business ----------
data["core_business"] = (
    "玻利维亚监察员办公室（Defensoría del Pueblo）是依据《多民族宪法政治》设立、由2016年12月13日第870号"
    "《监察专员法》规范的独立国家人权机构，具有职能、财政与行政自主权，不受国家任何机关指令约束，仅受审计监督。"
    "核心职能包括：受理并跟进公民对公共服务及公共权力行为的投诉申诉；捍卫与促进人权，特别是原住民农民社群"
    "（NPIOC）、城市社区、非裔玻利维亚人社群及海外侨民的权益；作为国家预防酷刑机制对拘留场所开展巡视；"
    "对女性、儿童青少年、老年人、残疾人、LGBTQI+、被剥夺自由者、移民等脆弱群体实施特别保护；依据第348号"
    "《对女性免受暴力综合保障法》开展专门工作；监测社会冲突并在政府与动员群体之间促成对话（如2026年紧急状态"
    "期间介入42%的已登记冲突）；发布人权、冲突、司法检察观察等专题报告；开展人权教育与传播（虚拟课堂、学生"
    "监察员计划、专业图书馆等）。机构持有全球国家人权机构联盟（GANHRI）A级认证并通过ISO 9001质量体系认证，"
    "总部设于拉巴斯，在全国九个省设有21个代表处及边境办事处。"
)

# ---------- apec_stance ----------
data["apec_stance"] = (
    "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入），该机构与APEC机制无直接关联。"
    "其国际合作主要面向国家人权机构体系：持有全球国家人权机构联盟（GANHRI）A级认证（官网明示），"
    "并与联合国体系（联合国人权高专办、UNICEF、UN Women、国际移民组织IOM等）保持合作，"
    "而非环太平洋经贸合作框架。"
)

# ---------- industries 补充 ----------
data["industries"] = ["public_administration", "civil_service", "social_services"]

# ---------- collection_meta ----------
data["collection_meta"] = {
    "collection_date": "2026-10-25",
    "phase": "phase3_enriched",
    "data_sources": [
        "official_website",
        "wikipedia",
        "wikidata",
        "news_search",
        "web_search",
        "social_media",
    ],
    "completeness_score": 90,
    "quotes": [
        {
            "title": "Defensoría del Pueblo (Bolivia) — Wikipedia (español)",
            "url": "https://es.wikipedia.org/wiki/Defensor%C3%ADa_del_Pueblo_(Bolivia)",
        },
        {
            "title": "AUTORIDADES — Defensoría del Pueblo (sitio oficial, 明确记载 Callisaya 2022-09-23当选、09-27就任)",
            "url": "https://www.defensoria.gob.bo/contenido/autoridades",
        },
        {
            "title": "Nuestras Oficinas — Defensoría del Pueblo (sitio oficial, 全国22处办公点名录)",
            "url": "https://www.defensoria.gob.bo/oficinas",
        },
        {
            "title": "Paz decreta el estado de excepción en Bolivia horas después de firmar el acuerdo de pacificación — El País (2026-06-20)",
            "url": "https://elpais.com/america/2026-06-20/paz-decreta-el-estado-de-excepcion-en-bolivia-horas-despues-de-firmar-el-acuerdo-de-pacificacion.html",
        },
        {
            "title": "Pedro Callisaya, Defensor del Pueblo de Bolivia: \"Un estado de excepción no va a solucionar los problemas estructurales del país\" — Radio Universidad de Chile/RFI (2026-05-29)",
            "url": "https://radio.uchile.cl/2026/05/29/pedro-callisaya-defensor-del-pueblo-de-bolivia-un-estado-de-excepcion-no-va-a-solucionar-los-problemas-estructurales-del-pais/",
        },
        {
            "title": "Bolivia: Entra en vigor la ley de Estados de excepción (援引监察员办公室伤亡统计) — Vatican News (2026-06-09)",
            "url": "https://www.vaticannews.va/es/mundo/news/2026-06/bolivia-entra-en-vigor-la-ley-de-estados-de-excepcion.html",
        },
    ],
    "notes": (
        "Phase 3 富化（2026-10-24执行）：现任监察专员 Pedro Francisco Callisaya Aro 经官网 autoridades 页、"
        "官网新闻（2026-10-22/24署名报道）、西语维基及2026年5-6月国际媒体（RFI/Vatican News/El País）交叉确认"
        "2025年11月帕斯政府更替后仍留任并积极履职。地区办事处22处（含总部）取自官网 /oficinas 页。"
        "key_people 含现任专员及4位近前任专员（官网历史页+西语维基双源）；其 person_id 因 _name_index.json "
        "无对应人名条目而留空；departments 的 dept_id 采用本项目既有局部编号约定（参照 BO-GOV-003-DEPT-001 先例），"
        "非注册表ID。founded_date 沿用骨架 Wikidata 值（1994年宪法改革创设监察专员职位），"
        "官网/维基记载机构经1997年12月立法规范、首任专员1998年5月就任。"
    ),
}

with open(FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK: wrote", FILE)

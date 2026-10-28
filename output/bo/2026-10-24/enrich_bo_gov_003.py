# -*- coding: utf-8 -*-
"""Enrich BO-GOV-003 (Ministerio de Gobierno de Bolivia) - phase3_enriched."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orgs", "BO-GOV-003.json")

with open(OUT, encoding="utf-8") as f:
    data = json.load(f)

data["basic_info"]["name_original"] = "Ministerio de Gobierno"
data["basic_info"]["name_zh"] = "玻利维亚政府部"
data["basic_info"]["name_en"] = "Ministry of Government"
data["basic_info"]["aliases"] = [
    "MinGob",
    "MINGOB",
    "Ministerio de Gobierno de Bolivia",
    "Ministerio del Interior（旧称）",
    "Ministry of Government of Bolivia",
]
data["basic_info"]["website"] = "https://web.mingobierno.gob.bo/"

data["industries"] = ["public_administration", "internal_security"]

data["social_accounts"] = [
    {
        "platform": "facebook",
        "account_name": "Ministerio de Gobierno Bolivia (@MindeGobierno)",
        "url": "https://www.facebook.com/MindeGobierno/",
        "source": "Facebook 官方主页，2026年10月仍在发布官方新闻稿（如安全边境2.0计划）",
    },
    {
        "platform": "twitter_x",
        "account_name": "Ministerio de Gobierno Bolivia (@mindegobol)",
        "url": "https://x.com/mindegobol",
        "source": "X（Twitter）官方账号，发布官方公告（comunicados）",
    },
    {
        "platform": "twitter_x",
        "account_name": "Ministerio De Gobierno Bolivia (@MindeGobierno)",
        "url": "https://x.com/MindeGobierno",
        "source": "X（Twitter）旧官方账号（阿尔塞政府时期使用，现为历史存档）",
    },
    {
        "platform": "instagram",
        "account_name": "MinGob (@mingobierno)",
        "url": "https://www.instagram.com/mingobierno/",
        "source": "Instagram 官方账号，简介为玻利维亚多民族国政府部",
    },
    {
        "platform": "threads",
        "account_name": "@mingobierno",
        "url": "https://www.threads.com/@mingobierno",
        "source": "Threads 官方账号（与 Instagram 同名）",
    },
]

data["digital_assets"] = [
    {
        "name": "官方门户网站（web.mingobierno.gob.bo）",
        "url": "https://web.mingobierno.gob.bo/",
        "description": "政府部官方网站：发布新闻稿（Notas de Prensa）、官方公告（Comunicados）、政务公开与公众服务入口",
        "source": "官方网站首页",
    },
    {
        "name": "Estado Digital 在线政务平台（ED1-ED9）",
        "url": "https://web.mingobierno.gob.bo/?post_type=tramite",
        "description": "提供警察无犯罪证明（ED1）、出入境流量（ED2）、车窗贴膜许可（ED3）、在押人员信息查询（ED4）、私人安保企业注册（ED5）、管制化学品登记（ED6）、数字身份证与驾照（ED7）、警校报考（ED8）、移民手续（ED9）等在线服务",
        "source": "官方网站政务栏目",
    },
    {
        "name": "官方公告栏目（Comunicados）",
        "url": "https://web.mingobierno.gob.bo/?post_type=comunicados",
        "description": "政府部及移民总局、监狱管理总局、管制物质总局等下属机构公告发布平台",
        "source": "官方网站公告栏目",
    },
]

data["key_people"] = [
    {
        "person_id": None,
        "name": "马尔科·安东尼奥·奥维多·韦尔塔（Marco Antonio Oviedo Huerta）",
        "title": "Ministro de Gobierno（政府部长）",
        "title_description": "主管国家内政、公民安全、警务、移民、监狱与禁毒政策的内阁部长（相当于内政部长）",
        "description": "1956年6月13日生于拉巴斯，律师（圣安德烈斯大学UMSA），早年属左翼革命运动（MIR），1989-1993年任帕斯·萨莫拉政府内政与警察事务副部长；2025年11月9日经总统罗德里戈·帕斯任命就任政府部长（前任Roberto Ríos Sanjinés），2026年10月仍在任",
    },
    {
        "person_id": None,
        "name": "彼得·马尔多纳多·巴科维克（Peter Maldonado Bacovick）",
        "title": "Viceministro de Régimen Interior, Fortalecimiento y Transparencia Policial（内政、警务强化与警务透明副部长）",
        "title_description": "主管内政事务、警察体系强化与警务反腐廉政建设",
        "description": "拉巴斯人，企业管理学士，2006-2009年曾任国会议员，兼任媒体专栏作者、政治传播与选举进程顾问、大学教师；2026年10月7日就任（接替埃尔南·帕雷德斯·穆尼奥兹）",
    },
    {
        "person_id": None,
        "name": "安东尼奥·蒙泰罗·托里科斯（Antonio Montero Torricos）",
        "title": "Viceministro de Seguridad Ciudadana y Prevención del Delito（公民安全与犯罪预防副部长）",
        "title_description": "主管公民安全政策与犯罪预防（含国家公民安全计划、消防救援等）",
        "description": "波托西人，警察将军，曾任玻利维亚国家警察总司令及警察国家通讯、交通、总监察等部门领导；2026年10月7日获部长留任该职（部分媒体称其为 Rodolfo Montero）",
    },
    {
        "person_id": None,
        "name": "多里安·费尔南多·巴达尼·比列加斯（Dorian Fernando Badani Villegas）",
        "title": "Viceministro de Lucha Integral contra el Narcotráfico（综合治理禁毒副部长）",
        "title_description": "主管全国禁毒政策的统筹执行（缉毒、管制物质与禁毒资产查扣管理）",
        "description": "企业管理学士，拥有25年以上公共管理与国际合作经验，人力资源管理硕士；2026年10月7日就任新设立的综合治理禁毒副部长",
    },
]

data["departments"] = [
    {
        "dept_id": "BO-GOV-003-DEPT-001",
        "name": "Viceministerio de Régimen Interior, Fortalecimiento y Transparencia Policial",
        "head": "Peter Maldonado Bacovick",
        "description": "内政、警务强化与警务透明副部长：主管内政（régimen interior）事务与国家警察体系的强化、监督和廉政透明化建设；由原内政与警察事务副部长（Viceministerio de Régimen Interior y Policía）改组而来",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-GOV-003-DEPT-002",
        "name": "Viceministerio de Seguridad Ciudadana y Prevención del Delito",
        "head": "Antonio Montero Torricos",
        "description": "公民安全与犯罪预防副部长：统筹国家公民安全计划、犯罪预防政策，协调警察与地方政府的治安工作及消防救援事务",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-GOV-003-DEPT-003",
        "name": "Viceministerio de Lucha Integral contra el Narcotráfico",
        "head": "Dorian Fernando Badani Villegas",
        "description": "综合治理禁毒副部长：统筹缉毒执法、禁毒政策（2026-2030年国家禁毒政策）与禁毒资产查扣管理；2026年10月7日设立，承接原社会防卫与管制物质副部长（Viceministerio de Defensa Social y Sustancias Controladas）职能",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-GOV-003-DEPT-004",
        "name": "Dirección General de Migración（玻利维亚移民总局）",
        "head": None,
        "description": "移民总局：负责出入境管理、外国人停留与居留许可、护照签发及打击人口贩运；提供ED2出入境流量、ED9移民手续等在线服务",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-GOV-003-DEPT-005",
        "name": "Dirección General de Régimen Penitenciario（监狱管理总局）",
        "head": None,
        "description": "监狱（刑罚执行）管理总局：负责全国监狱系统管理与在押人员权益，提供在押人员信息实时查询（ED4）服务，并推动囚犯改造与社会重新融入",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-GOV-003-DEPT-006",
        "name": "Dirección General de Sustancias Controladas（管制物质总局）",
        "head": None,
        "description": "管制物质总局：负责受管制化学品与物质的登记、审批与监管（ED6管制化学品管理系统），防范前体化学品流入非法制毒渠道",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-GOV-003-DEPT-007",
        "name": "Servicio General de Identificación Personal（SEGIP，个人身份识别总局）",
        "head": None,
        "description": "个人身份识别总局：负责全国身份证件（cédula de identidad）与数字身份、驾照等签发；2026年推行SEGIP数字化身份与全国办理点（ brigadas）建设",
        "parent_dept_id": None,
    },
]

data["recent_events"] = [
    {
        "date": "2025-11-09",
        "title": "马尔科·奥维多就任帕斯新政府政府部长",
        "description": "2025年11月8日罗德里戈·帕斯就任总统并大幅精简内阁（由17个部减至13个），11月9日总统帕斯任命并宣誓马尔科·安东尼奥·奥维多为政府部长，接替上届政府部长罗贝托·里奥斯·桑希内斯（Roberto Ríos Sanjinés），负责国家内政、警务与公共安全事务",
        "impact": "玻利维亚内政与安全政策随政权更迭转向：恢复与美国全面外交与安全合作，警务廉政与禁毒成为优先议程",
        "source": "https://es.wikipedia.org/wiki/Marco_Antonio_Oviedo",
    },
    {
        "date": "2026-09-17",
        "title": "国会以100票赞成通过戒严状态延长90天",
        "description": "针对2026年8月起持续53天的大规模道路封锁与抗议，部长奥维多于9月13日宣布将提请延长紧急状态（estado de excepción），9月17日多民族立法大会以158票中100票赞成通过延长90天；部长亲赴国会作技术陈述并提交12份官方报告佐证",
        "impact": "政府在戒严框架下获得更大执法权限以恢复战略通道与经济秩序；官方称封锁期间警方行动未致死亡、55名警员受重伤，并指认古查坦巴（Trópico de Cochabamba）等地资金资助封锁",
        "source": "https://www.noticiasfides.com/nacional/politica/asamblea-legislativa-aprueba-la-ampliacion-por-90-dias-del-estado-de-excepcion",
    },
    {
        "date": "2026-10-01",
        "title": "警方逮捕总检察长罗赫尔·马里亚卡，端掉检察院内部犯罪保护网",
        "description": "10月1日凌晨（苏克雷），在部长奥维多指挥下警方与检方联合行动逮捕总检察长罗赫尔·马里亚卡（Roger Mariaca）及至少13名涉案人员，指其领导盘踞在检察院的犯罪组织（非法收费、勒索、保护毒品犯罪）；此前9月29日美国以涉毒为由吊销其签证",
        "impact": "玻利维亚司法系统重大震动：政府借此整肃司法保护网并宣示反毒反腐立场；检察长办公室则指逮捕非法，引发府院对峙与人事争议",
        "source": "https://www.bbc.com/mundo/articles/cwlyky680kg8o",
    },
    {
        "date": "2026-10-07",
        "title": "部长改组副部级班子：新设综合治理禁毒副部长并留任公民安全副部长",
        "description": "10月7日部长奥维多宣誓彼得·马尔多纳多·巴科维克为内政、警务强化与警务透明副部长，多里安·巴达尼·比列加斯为新设的综合治理禁毒副部长，并留任（前警察总司令）安东尼奥·蒙泰罗·托里科斯为公民安全与犯罪预防副部长；原内政副部长埃尔南·帕雷德斯离任",
        "impact": "部门机构重组：将禁毒提升为专门副部级职能、强化警务廉政建设，配合全国范围打击毒品犯罪与有组织犯罪的攻势",
        "source": "https://web.mingobierno.gob.bo/?nota_prensa=%f0%9d%97%a0%f0%9d%97%b6%f0%9d%97%bb%f0%9d%97%b6%f0%9d%98%80%f0%9d%98%81%f0%9d%97%bf%f0%9d%97%bc-%f0%9d%97%a2%f0%9d%98%83%f0%9d%97%b6%f0%9d%97%b2%f0%9d%97%b1%f0%9d%97%bc-%f0%9d%97%bd%f0%9d%97%bc-2",
    },
    {
        "date": "2026-10-21",
        "title": "启动安全边境2.0计划，并与美国合作筹建两支超精锐警察部队",
        "description": "10月21日政府在圣克鲁斯启动安全边境2.0（Plan Fronteras Seguras 2.0）计划，向圣克鲁斯增派230名专业警力；部长奥维多同时宣布正与美国合作（含美国缉毒局DEA）在圣克鲁斯（圣伊格纳西奥-圣马蒂亚斯一带）与贝尼（圣安娜）筹建两支打击毒品恐怖主义的超精锐警察部队，教官来自美、哥、阿、智等国",
        "impact": "强化玻利维亚与巴西、秘鲁边境的缉毒与打击跨国犯罪能力；标志2025年11月DEA获准重返玻利维亚后美玻安全合作进一步机制化",
        "source": "https://abi.bo/gobierno-anuncia-la-creacion-de-dos-unidades-policiales-de-super-elite-en-santa-cruz-y-beni-para-combatir-el-narcoterrorismo/",
    },
]

data["related_entities"] = [
    {
        "org_id": "BO-MIL-005",
        "org_name": "玻利维亚国家警察 (Policía Nacional de Bolivia)",
        "org_type": "MIL",
        "org_description": "玻利维亚国家警察：负责国内公共安全、交通、缉毒（缉毒特种部队FELCN）、消防救援等；政府部为其上级主管与政策制定部门，2026年警察总司令为阿德里安·阿尔瓦雷斯（Adrián Álvarez）上校",
        "relationship_type": "subsidiary",
    },
    {
        "org_id": "BO-GOV-001",
        "org_name": "玻利维亚总统 (Presidente de Bolivia)",
        "org_type": "GOV",
        "org_description": "国家元首兼行政首脑：政府部长由总统罗德里戈·帕斯任命并向其负责，政府部隶属国家行政机关（órgano ejecutivo）",
        "relationship_type": "parent_org",
    },
    {
        "org_id": "BO-INTL-002",
        "org_name": "美洲国家组织 (Organización de los Estados Americanos)",
        "org_type": "INTL",
        "org_description": "美洲区域性组织：2026年部长奥维多推动美洲国家组织派公民安全文职使团访玻，在53天封锁事件后加强公民安全与和平共处领域的合作",
        "relationship_type": "partner",
    },
    {
        "org_id": "BO-INTL-001",
        "org_name": "联合国 (Organización de las Naciones Unidas)",
        "org_type": "INTL",
        "org_description": "通过联合国毒品和犯罪问题办公室（UNODC）与玻政府部及国际机构合作，启动2026-2030年国家禁毒政策部门间协调机制（Mesa Sectorial），并在边境缉毒、反腐培训等领域提供支持",
        "relationship_type": "partner",
    },
]

data["core_business"] = (
    "玻利维亚政府部（Ministerio de Gobierno，旧称内政部）是多民族国行政机关中主管内政事务的核心部门，1826年设立，驻地拉巴斯（Belisario Salinas大街2409号）。"
    "其职能依据第3351号《行政机关组织法》（经第29894号最高法令公布）及各届政府组织条例，涵盖：公民安全与犯罪预防政策（国家公民安全计划）；国家警察事务（警务指挥协调、警务强化与廉政透明改革）；"
    "移民与出入境管理（移民总局）；监狱与刑罚执行管理（监狱管理总局）；禁毒与管制物质管理（缉毒政策、前体化学品管制、古柯超额种植治理及禁毒资产查扣保管）；个人身份识别（SEGIP身份证件签发）；"
    "私人安保企业监管；以及社会冲突处置与危机状态（戒严状态）的实施并向国会作技术论证。2026年以来该部主导安全边境2.0边境安全计划、2026-2030年国家禁毒政策，并统筹对美国DEA、UNODC、欧盟、美洲国家组织及智利、巴西等国的安全合作事务。"
)

data["apec_stance"] = (
    "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。玻利维亚政府部实际参与的国际安全与禁毒合作包括：2025年11月玻美恢复全面外交关系后，美国缉毒局（DEA）在时隔18年后获准重返玻利维亚（重点关注查帕雷古柯种植区）；"
    "2026年10月21日部长奥维多宣布在美国合作下于圣克鲁斯和贝尼筹建两支打击毒品恐怖主义的超精锐警察部队；与联合国毒罪办（UNODC）等国际机构共同启动2026-2030年国家禁毒政策部门间协调机制，并获欧盟资助开展缉毒警反腐培训；"
    "推动美洲国家组织（OEA）公民安全文职使团访玻；2026年10月16日与智利签署深化边境安全、移民和打击有组织犯罪合作的协议；另与巴西开展联合边境安全行动。"
)

data["profile"] = {
    "source_url": "https://upload.wikimedia.org/wikipedia/commons/5/5b/Ministerio_de_Gobierno.png",
    "local_path": None,
}

data["collection_meta"] = {
    "collection_date": "2026-10-24",
    "phase": "phase3_enriched",
    "data_sources": [
        "official_website",
        "wikipedia",
        "news_search",
        "web_search",
        "social_media",
    ],
    "completeness_score": 0,
    "notes": "2026-10 深度画像：核实帕斯新政府（2025-11-08就任）现任部长Marco Antonio Oviedo（2025-11-09就任，2026-10仍任）及2026-10-07改组后的三位副部长；下属机构含移民总局、监狱管理总局、管制物质总局、SEGIP；近期事件含戒严延长、总检察长被捕、安全边境2.0与美玻精锐部队合作。未确认字段（移民/监狱/管制物质/SEGIP负责人姓名）留空",
    "quotes": [
        {
            "title": "Ministerio de Gobierno (Bolivia) - Wikipedia (es)",
            "url": "https://es.wikipedia.org/wiki/Ministerio_de_Gobierno_(Bolivia)",
        },
        {
            "title": "Marco Antonio Oviedo - Wikipedia (es)",
            "url": "https://es.wikipedia.org/wiki/Marco_Antonio_Oviedo",
        },
        {
            "title": "Ministro Oviedo posesiona a dos nuevos viceministros y ratifica al Gral. Montero (MinGob, 2026-10-07)",
            "url": "https://web.mingobierno.gob.bo/?nota_prensa=%f0%9d%97%a0%f0%9d%97%b6%f0%9d%97%bb%f0%9d%97%b6%f0%9d%98%80%f0%9d%98%81%f0%9d%97%bf%f0%9d%97%bc-%f0%9d%97%a2%f0%9d%98%83%f0%9d%97%b6%f0%9d%97%b2%f0%9d%97%b1%f0%9d%97%bc-%f0%9d%97%bd%f0%9d%97%bc-2",
        },
        {
            "title": "Asamblea Legislativa aprueba la ampliación por 90 días del estado de excepción (Agencia Fides)",
            "url": "https://www.noticiasfides.com/nacional/politica/asamblea-legislativa-aprueba-la-ampliacion-por-90-dias-del-estado-de-excepcion",
        },
        {
            "title": "Por qué arrestaron al fiscal general en Bolivia (BBC Mundo, 2026-10-01)",
            "url": "https://www.bbc.com/mundo/articles/cwlyky680kg8o",
        },
        {
            "title": "Gobierno anuncia la creación de dos unidades policiales de súper élite en Santa Cruz y Beni (ABI, 2026-10-21)",
            "url": "https://abi.bo/gobierno-anuncia-la-creacion-de-dos-unidades-policiales-de-super-elite-en-santa-cruz-y-beni-para-combatir-el-narcoterrorismo/",
        },
        {
            "title": "Oviedo anuncia decreto para ampliar el estado de excepción por 90 días (La Razón, 2026-09-13)",
            "url": "https://larazon.bo/nacional/2026/09/13/oviedo-anuncia-decreto-para-ampliar-el-estado-de-excepcion-por-90-dias/",
        },
        {
            "title": "Santa Cruz: Gobierno despliega 230 policías especializados (Red Uno, 2026-10-22)",
            "url": "https://www.reduno.com.bo/noticias/santa-cruz-gobierno-despliega-230-policias-especializados-para-combatir-el-crimen-organizado-2026102253930",
        },
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("WROTE", OUT)
core = data["core_business"]
print("core_business chars:", len(core))
print("apec chars:", len(data["apec_stance"]))

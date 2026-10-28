# -*- coding: utf-8 -*-
"""Build BO-PERSON-000190 Jorge Arturo Iporre Salguero person profile."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000190.json")

ENDE = "玻利维亚国家电力公司 (Empresa Nacional de Electricidad - ENDE)"

bio = (
    "豪尔赫·阿图罗·伊波雷·萨尔盖罗是玻利维亚资深电力工程师与国企管理者，现任国家电力公司（ENDE）"
    "项目执行部总经理，系2025年11月18日罗德里戈·帕斯政府改组后ENDE新管理团队成员。他毕业于布拉迪斯拉发"
    "斯洛伐克技术大学，获电气能源工程师学位（发电、配电与输电专业方向），另持工商管理硕士（MBA）学位，"
    "在电力行业拥有逾25年经验。2010至2012年任区域电力一体化委员会玻利维亚委员会（CIER玻利维亚委员会）"
    "执行秘书，曾任国家负荷调度委员会（CNDC）主席及ENDE协调部经理。2013年5月2日经埃沃·莫拉莱斯总统"
    "第9650号最高决议任命为ENDE临时总经理（5月6日就职），任内于2014年11月代表ENDE接收西班牙Red "
    "Eléctrica Internacional交还的国家输电公司（TDE）股权，使国家控制全国逾80%的电力输送，并推动对阿根廷、"
    "巴西等邻国的电力互联与出口规划。2015年9月至2017年9月任ENDE Transmisión国际市场部总经理，其后据其"
    "个人资料显示在AUDING LATAM任合伙人董事。2025年11月重返ENDE领导层。"
)
assert len(bio) >= 200, "biography_summary must be at least 200 chars: %d" % len(bio)

data = {
    "person_id": "BO-PERSON-000190",
    "name": "Jorge Arturo Iporre Salguero",
    "name_en": "Jorge Arturo Iporre Salguero",
    "name_zh": "豪尔赫·阿图罗·伊波雷·萨尔盖罗",
    "aliases": ["Arturo Iporre", "Jorge Iporre"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "current_positions": ["玻利维亚国家电力公司（ENDE）项目执行部总经理"],
    "education": [
        {
            "institution": "布拉迪斯拉发斯洛伐克技术大学 (Slovenská technická univerzita v Bratislave)",
            "degree": "master",
            "field": "电气能源工程（发电、配电与输电方向）",
            "description": "获电气能源工程师（Ingeniero Electroenergético）学位；斯洛伐克高校Ing.（inžinier）学位属硕士层次，故归入master",
            "country": "斯洛伐克",
            "source": "eju.tv/Los Tiempos 2013-05-07 就任报道（引官方信息）",
        }
    ],
    "work_experience": [
        {
            "organization": ENDE,
            "org_id": "BO-SOE-003",
            "position": "项目执行部总经理",
            "start_date": "2025-11",
            "end_date": None,
            "is_current": "true",
            "description": "2025年11月18日帕斯政府改组ENDE管理层（马里奥·拉赖恩·萨阿维德拉任临时执行总裁）后进入新领导班子，现主管项目执行",
            "start_date_note": "ENDE官网管理机构名录现任列名；与新董事会同步就任，确切就任日期未单独见于报道",
            "source": "https://www.ende.bo/nomina-autoridades",
        },
        {
            "organization": "国家输电公司 (ENDE Transmisión S.A.)",
            "org_id": None,
            "position": "国际市场部总经理",
            "start_date": "2015-09-17",
            "end_date": "2017-09-11",
            "description": "2015年9月17日获任国际市场部总经理（ENDE子公司）；2017年9月11日提交不可撤销辞呈，9月12日经ASFI重大事项公告披露",
            "source": "玻利维亚证券交易所有关公告及ASFI登记记录；2017年拉美能源峰会讲者名单",
        },
        {
            "organization": "奥丁工程拉美公司 (AUDING LATAM)",
            "org_id": None,
            "position": "合伙人董事",
            "start_date": None,
            "end_date": None,
            "description": "据其LinkedIn资料及RocketReach聚合信息（全名Arturo Iporre Salguero、所在地玻利维亚）显示曾任/现任合伙人董事，该资料可能更新于其重返ENDE之前；任职时间不详（约在2017年离开ENDE Transmisión之后），未经第二独立来源证实",
        },
        {
            "organization": ENDE,
            "org_id": "BO-SOE-003",
            "position": "临时执行总裁（临时总经理）",
            "start_date": "2013-05-02",
            "end_date": "2014-12-22",
            "description": "经埃沃·莫拉莱斯总统第9650号最高决议（2013年5月2日）任命为临时总经理，5月6日由碳氢化合物与能源部长胡安·何塞·索萨主持就职，接替雨果·比利亚罗埃尔·森萨诺；2014年12月22日卸任",
            "source": "ENDE官网历届负责人栏、第9650号最高决议及Los Tiempos等媒体就任报道",
        },
        {
            "organization": ENDE,
            "org_id": "BO-SOE-003",
            "position": "协调部经理",
            "start_date": None,
            "end_date": None,
            "description": "据ENDE官网简历，出任临时总裁前曾任公司协调部经理，具体起止时间不详（2013年之前）",
            "source": "https://www.ende.bo/prerfil-presidente/7",
        },
        {
            "organization": "国家负荷调度委员会 (Comité Nacional de Despacho de Carga - CNDC)",
            "org_id": None,
            "position": "主席",
            "start_date": None,
            "end_date": None,
            "description": "据ENDE官网简历曾任玻利维亚电力系统国家负荷调度委员会主席，具体起止时间不详",
            "source": "https://www.ende.bo/prerfil-presidente/7",
        },
        {
            "organization": "区域电力一体化委员会玻利维亚委员会 (Comisión de Integración Eléctrica Regional - CIER Comité Boliviano)",
            "org_id": None,
            "position": "执行秘书",
            "start_date": "2010",
            "end_date": "2012",
            "description": "2010至2012年任区域电力一体化委员会玻利维亚委员会（CIER玻利维亚委员会）执行秘书",
            "source": "https://www.ende.bo/prerfil-presidente/7",
        },
        {
            "organization": "巴列埃尔莫索电力公司 (Empresa Eléctrica Valle Hermoso S.A.)",
            "org_id": None,
            "position": "董事",
            "start_date": None,
            "end_date": None,
            "description": "玻利维亚证券交易所有关公告及ASFI登记记录显示其曾任该公司董事，后被免职并由Eduardo Paz Castro接任，具体任免日期未能核实",
        },
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000186",
            "person_name": "马里奥·拉赖恩·萨阿维德拉 (Mario Larrain Saavedra)",
            "relationship_type": "superior",
            "description": "拉赖恩于2025年11月18日就任ENDE临时执行总裁（帕斯政府新管理层），伊波雷任其下项目执行部总经理，同属新领导班子",
            "source": "ERBOL/Opinión 2025-11-18至19报道、ENDE官网",
        },
        {
            "person_id": None,
            "person_name": "雨果·比利亚罗埃尔·森萨诺 (Hugo Villarroel Senzano)",
            "relationship_type": "colleague",
            "description": "伊波雷任ENDE临时总经理时的前任：比利亚罗埃尔2012年3月至2013年5月任ENDE执行总裁，2013年5月由伊波雷接任",
            "source": "eju.tv/Los Tiempos 2013-05-07报道、ENDE官网历届负责人栏",
        },
        {
            "person_id": "BO-PERSON-000483",
            "person_name": "埃沃·莫拉莱斯 (Evo Morales)",
            "relationship_type": "associate",
            "description": "2013年时任玻利维亚总统，通过第9650号最高决议（2013年5月2日）任命伊波雷为ENDE临时总经理",
            "source": "第9650号最高决议（2013-05-02）、eju.tv/Los Tiempos报道",
        },
        {
            "person_id": None,
            "person_name": "胡安·何塞·索萨 (Juan José Sosa)",
            "relationship_type": "superior",
            "description": "2013至2014年任碳氢化合物与能源部长，系伊波雷2013年5月6日ENDE就职仪式的主持者与任期内上级部长",
            "source": "eju.tv/Los Tiempos 2013-05-07报道、El Diario 2014-11-14报道",
        },
    ],
    "social_accounts": [],
    "family_members": [],
    "political_stances": [
        {
            "date": "2014-09-29",
            "topic": "电力出口与区域能源一体化",
            "stance_content": "任ENDE总经理期间表示，因输电线路建设需时约一年，玻利维亚预计2015年起可向阿根廷出口电力；出口电价应由两国商定并反映国际市场行情，并强调扩大出口须先建设联通两国互联系统的输电线路",
            "source": "Hoy Bolivia 2014-09-29；La Razón 2014-05-06",
        },
        {
            "date": "2014-11-14",
            "topic": "输电国有化与国家能源主权",
            "stance_content": "在TDE国有化争议解决仪式上代表ENDE接收西班牙Red Eléctrica Internacional交还的股权凭证，并声明国家由此控制全国逾80%的电力输送",
            "source": "El Diario 2014-11-14；IBCE 2014-11-14",
        },
    ],
    "major_achievements": [
        {
            "date": "2014-11-13",
            "organization": ENDE,
            "achievement": "作为ENDE临时总裁代表公司接收西班牙Red Eléctrica Internacional（REI）交还的国家输电公司（TDE）股权凭证，标志TDE国有化仲裁争议以6500万美元和解正式了结，国家获得对全国逾80%电力输运的控制",
        },
        {
            "date": "2014-09",
            "organization": ENDE,
            "achievement": "任内推动玻利维亚与巴西、阿根廷、智利、秘鲁四国电力互联评估，并在2014年8月玻阿签署电力互换谅解备忘录后规划自2015年起向阿根廷出口电力",
        },
    ],
    "biography_summary": bio,
    "profile": {
        "source_url": "https://www.ende.bo/public/imgs/personal-ejecutivo/arturo.iporre.salguero.jpg",
        "local_path": None,
    },
    "social_accounts_note": "6项平台扫描（facebook/twitter-x/linkedin/instagram/tiktok/youtube）未发现可确证为本人的账号。LinkedIn候选：bo.linkedin.com/in/jorgeiporre（电信与诺基亚背景，判定为同名不同人）；bo.linkedin.com/in/arturo-iporre-salguero-0a1a1223（AUDING LATAM合伙人，全名匹配但未获独立佐证）；Facebook存在多个同名个人档案均无法确认身份。保守起见均不收录。",
    "education_note": "另据ENDE官网简历，其持有工商管理硕士（MBA）学位，授予院校不详，故未单列条目。",
    "collection_meta": {
        "phase": "phase4_person_profile",
        "collection_date": "2026-10-25",
        "data_sources": ["official_website", "news_search", "web_search", "government_registry"],
        "notes": "信息核实说明：(1) 现任职务及2025-11-18新领导层背景以ENDE官网名录与ERBOL、Opinión任命报道为准；(2) 2013-2014总裁任期及2015-2017 ENDE Transmisión任期有官方决议、交易所公告及两个以上独立媒体来源；(3) 出生日期、出生地、家庭成员无公开记录，相关字段留空；(4) LinkedIn存在同名候选档案但身份无法核实，social_accounts留空；(5) AUDING LATAM履历仅见于LinkedIn自述及RocketReach聚合，未经独立来源证实，已在条目内注明；(6) MBA授予院校不详；(7) name_zh沿用库内既有译名。",
        "quotes": [
            {"title": "NÓMINA DE AUTORIDADES | ENDE Corporación（官网现任管理机构名录）", "url": "https://www.ende.bo/nomina-autoridades"},
            {"title": "Jorge Arturo Iporre - ENDE Corporación（官网简历）", "url": "https://www.ende.bo/prerfil-presidente/7"},
            {"title": "Panel de Presidentes | ENDE Corporación（历届负责人）", "url": "https://www.ende.bo/galeria-de-presidentes"},
            {"title": "Cambian gerente en ENDE; asume Arturo Iporre（Los Tiempos/eju.tv，2013-05-07）", "url": "https://eju.tv/2013/05/cambian-gerente-en-ende-asume-arturo-iporre/"},
            {"title": "Resolución Suprema No 09650 del 02 de mayo de 2013（第9650号最高决议）", "url": "https://www.derechoteca.com/gacetabolivia/resolucion-suprema-no-09650-del-02-de-mayo-de-2013/"},
            {"title": "El Ministro de Hidrocarburos posesiona a nuevos viceministros y autoridades del área energética（ERBOL，2025-11-18）", "url": "https://erbol.com.bo/econom%C3%ADa/el-ministro-de-hidrocarburos-posesiona-nuevos-viceministros-y-autoridades-del-%C3%A1rea"},
            {"title": "Nuevos funcionarios: Boa, ENDE y Gestora estrenan jefes（Opinión，2025-11-19）", "url": "https://www.opinion.com.bo/pais/nuevos-funcionarios-boa-ende-gestora-estrenan-jefes-continuan-posesiones/20251119000012983861.html"},
            {"title": "Estado controla transporte de electricidad（El Diario，2014-11-14）", "url": "https://www.pub.eldiario.net/noticias/2014/2014_11/nt141114/economia.php?n=4&-estado-controla-transporte-de-electricidad"},
            {"title": "El Estado consolida la nacionalización de TDE（IBCE，2014-11-14）", "url": "https://ibce.org.bo/principales-noticias-bolivia/noticias-nacionales-detalle.php?id=48332&idPeriodico=34&fecha=2014-11-14"},
            {"title": "Ende prevé exportar electricidad a Argentina desde 2015（Hoy Bolivia，2014-09-29）", "url": "https://hoybolivia.com/Noticia.php?IdNoticia=122250"},
            {"title": "ENDE analiza interconexión eléctrica con Brasil, Argentina, Chile y Perú（IBCE，2014-09-10）", "url": "https://ibce.org.bo/principales-noticias-bolivia/noticias-nacionales-detalle.php?id=46186&idPeriodico=34&fecha=2014-09-10"},
            {"title": "ENDE Transmisión S.A. hecho relevante: designación Gerente de Mercados Internacionales（玻利维亚证券交易所，2015-09-18）", "url": "https://www.bbv.com.bo/Publicacionv3/View_Publicacion/Detalle_HR1.aspx?Publicacion=98278"},
            {"title": "Reporte Hecho Relevante ASFI - ENDE Transmisión S.A.（2017-09-12，辞呈公告）", "url": "https://appweb2.asfi.gob.bo/PaginasPublicas2/VistaHechosRelevantes/VisorDocumentos.aspx?variable1=96410776-b550-4ec4-b7e4-6ae004d60c85"},
            {"title": "Medrano explicó Plan Estratégico de Hidrocarburos en Congreso Internacional（ANH，2014-08-21）", "url": "https://www.anh.gob.bo/w2026/contenido.php?s=5&O=578"},
            {"title": "Latin America Energy Summit 2017 Speakers（2017年讲者名单：ENDE Transmisión国际市场部总经理）", "url": "https://www.latamenergysummit.com/latin-america-energy-event-speakers"},
        ],
    },
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("WROTE", OUT)
print("biography_summary length:", len(bio))
print("work_experience entries:", len(data["work_experience"]))
print("person_relationships entries:", len(data["person_relationships"]))
print("education entries:", len(data["education"]))
print("political_stances entries:", len(data["political_stances"]))
print("major_achievements entries:", len(data["major_achievements"]))
print("quotes:", len(data["collection_meta"]["quotes"]))

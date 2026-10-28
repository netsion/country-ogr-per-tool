# -*- coding: utf-8 -*-
"""Enrich BO-FIN-005 (Banco Mercantil Santa Cruz S.A.) phase3 profile."""
import json
import os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orgs", "BO-FIN-005.json")

with open(PATH, encoding="utf-8") as f:
    data = json.load(f)

data["basic_info"]["name_zh"] = "圣克鲁斯商业银行"
data["basic_info"]["aliases"] = [
    "Banco Mercantil",
    "Banco Mercantil Santa Cruz S.A.",
    "BMSC",
    "Mercantil Santa Cruz",
]

data["social_accounts"] = [
    {
        "platform": "facebook",
        "account_name": "BancoMercantilSantaCruz",
        "url": "https://www.facebook.com/BancoMercantilSantaCruz/",
        "source": "Facebook 官方主页（2026-10 核实，约62万关注者，页标注'本机构受ASFI监管'）",
    },
    {
        "platform": "twitter_x",
        "account_name": "@MercantilSCZ",
        "url": "https://twitter.com/MercantilSCZ",
        "source": "X 官方账号（2026-10 核实；Wikidata 中旧账号 BancoMSC 已失效）",
    },
    {
        "platform": "instagram",
        "account_name": "@bancomercantil",
        "url": "https://www.instagram.com/bancomercantil/",
        "source": "Instagram 官方账号（2026-10 核实，约3.6万关注者）",
    },
    {
        "platform": "youtube",
        "account_name": "Banco Mercantil Santa Cruz S.A.",
        "url": "https://www.youtube.com/c/BancoMercantilSantaCruzSA",
        "source": "YouTube 官方频道（2026-10 核实）",
    },
    {
        "platform": "linkedin",
        "account_name": "Banco Mercantil Santa Cruz S.A.",
        "url": "https://bo.linkedin.com/company/bancomercantilsantacruz",
        "source": "LinkedIn 官方公司主页（2026-10 核实）",
    },
    {
        "platform": "tiktok",
        "account_name": "@soybmsc",
        "url": "https://www.tiktok.com/@soybmsc",
        "source": "BMSC 官方推广内容中标注的 TikTok 账号（2026-10，未单独二次核实）",
    },
]

data["digital_assets"] = [
    {
        "name": "KOIN e-wallet（数字资产钱包平台）",
        "url": "https://www.bmsc.com.bo/Koin",
        "description": "BMSC 于2026年7月推出的数字资产电子钱包，支持通过二维码购买 USDC 稳定币、用户间转账、接收兼容钱包的 USDC/USDT，并配套 Visa 卡在全球商户消费；平台基于 Ethereum 与 Polygon 网络（ERC-20），由 Koibanx 提供区块链基础设施、ATC 提供发卡处理，BMSC 为拉美首批以 USDC 通过 Visa 进行稳定币清算的银行之一。",
        "source": "BMSC 官网 KOIN 专区；Latam Fintech（2026-07-23）",
    },
    {
        "name": "KOIN App（Android）",
        "url": "https://play.google.com/store/apps/details?id=com.bmsc.koin",
        "description": "KOIN 数字钱包安卓应用，支持 KYC 数字开户、二维码购买 USDC、实时余额查询与交易记录管理。",
        "source": "Google Play 应用商店",
    },
    {
        "name": "BMSC Banca por Internet / Banca Móvil（网上银行与手机银行）",
        "url": "https://www.bmsc.com.bo",
        "description": "官网首页提供的 24/7 数字银行渠道：网上银行（Banca por internet）与手机银行 App（Banca Móvil，官网首页提供下载入口），支持在线开户、在线申请贷款及主要交易操作。",
        "source": "BMSC 官网首页（2026-10 抓取）",
    },
]

data["key_people"] = [
    {
        "person_id": None,
        "name": "Darko Zuazo Batchelder",
        "title": "Presidente del Directorio（董事长）",
        "title_description": "主持银行董事会，是银行最高治理机构负责人；同时为集团创始家族（Zuazo 家族）第二代核心成员。",
        "description": "2015年2月5日董事会会议即以董事长身份获任命（ASFI 债券招募书存档）；2026年8月仍以'Presidente del Directorio del Banco Mercantil Santa Cruz'身份出席 Urubó 分行开业仪式并发表讲话；D&B 企业名录列为 Key Principal。1973年其家族在前辈 Javier Zuazo 率领下收购银行股份，开启家族主导时期。",
    },
    {
        "person_id": None,
        "name": "Alberto Valdés Andreatta",
        "title": "Vicepresidente Ejecutivo（执行副总裁）",
        "title_description": "银行最高行政负责人（首席执行官层级），统管全行业务经营。",
        "description": "ASFI 债券招募书'主要高管'名单列其职务为执行副总裁；2025年2月接受媒体采访（ATB、Trendsetter Bolivia）时仍以'BMSC 执行副总裁'身份代表银行发言，任职延续至2025-2026年。1966年生于拉巴斯，在 BMSC 任职多年，曾获玻利维亚最佳CEO类报道关注。",
    },
    {
        "person_id": None,
        "name": "Maribel Fabiola Cerveró Ardaya",
        "title": "Vicepresidente de Tecnología（技术副总裁）",
        "title_description": "主管银行信息技术与数字化转型，含核心银行系统升级与 KOIN 数字资产平台。",
        "description": "ASFI 债券招募书列名 Maribel F. Cervero Ardaya 为技术副总裁；2026年7月以'Fabiola Cerveró，BMSC 技术副总裁'身份主导 KOIN 电子钱包发布，称其为 BMSC 数字金融生态战略的开端。",
    },
]

data["departments"] = [
    {
        "dept_id": "BO-FIN-005-DEPT-001",
        "name": "执行管理层 (Vicepresidencia Ejecutiva)",
        "head": "Alberto Valdés Andreatta",
        "description": "银行最高行政管理层，负责全行战略执行与日常经营，对董事会负责。",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-FIN-005-DEPT-002",
        "name": "个人与中小企业银行部 (Vicepresidencia de Banca Personas y Pymes)",
        "head": None,
        "description": "负责个人客户（储蓄、房贷、信用卡、消费信贷）与中小企业（Pyme）金融产品和服务。",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-FIN-005-DEPT-003",
        "name": "企业与公司银行部 (Vicepresidencia de Banca Corporativa Empresas)",
        "head": None,
        "description": "负责大企业与公司客户融资、贸易金融与现金管理业务；2025年该板块贷款增长35.06%，为全行增长主力。",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-FIN-005-DEPT-004",
        "name": "技术部 (Vicepresidencia de Tecnología)",
        "head": "Maribel Fabiola Cerveró Ardaya",
        "description": "负责核心银行系统（2025-2026年新核心系统投产与稳定）、数字渠道及 KOIN 数字资产平台建设。",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-FIN-005-DEPT-005",
        "name": "财务与国际事务部 (Vicepresidencia de Finanzas y Asuntos Internacionales)",
        "head": None,
        "description": "负责资产负债管理、财务报告、国际业务与同业往来（SWIFT: MERBBOLXX）。",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-FIN-005-DEPT-006",
        "name": "风险与运营支持条线 (Vicepresidencia de Riesgos / Operaciones y Administración / Recursos Humanos)",
        "head": None,
        "description": "涵盖风险管理（VP de Riesgos）、运营与行政（VP de Operaciones y Administración）、人力资源（VP de Recursos Humanos）及法律事务（Gerencia de Asuntos Legales），构成中后台支持体系；集团层面设有全面风险管理（GIR）委员会。",
        "parent_dept_id": None,
    },
]

data["recent_events"] = [
    {
        "date": "2026-07-23",
        "title": "BMSC 发布 KOIN 数字资产电子钱包，成为拉美首批稳定币清算银行之一",
        "description": "BMSC 推出 KOIN——玻利维亚首个由银行创设并背书的数字资产钱包：支持 KYC 数字开户、二维码购买 USDC、钱包间转账及配套 Visa 卡全球消费；平台基于 Ethereum/Polygon 网络，与 Koibanx（区块链基础设施）、Visa（支付网络与稳定币清算）、ATC（发卡处理）合作，并通过 Visa 稳定币清算能力实现每周7天结算。",
        "impact": "标志该行从传统商业银行向数字金融生态转型，成为拉美及加勒比地区首批以 USDC 通过 Visa 清算的银行之一，有望提升其数字获客与跨境支付能力。",
        "source": "https://www.latamfintech.co/articles/banco-mercantil-santa-cruz-lanza-koin-una-e-wallet-para-acceder-a-activos-digitales-en-bolivia",
    },
    {
        "date": "2026-08-14",
        "title": "Urubó 新分行开业：波龙戈市首个银行网点，年内已连开四家分行",
        "description": "BMSC 在圣克鲁斯都市区波龙戈市（Porongo）Urubó 地区开业新分行（建筑面积574平方米、配备电动车充电桩、虚拟助理ATM与24小时 autobanco），系该市首个银行网点；2026年内该行还开设了 El Cristo（圣克鲁斯）、Tupiza（波托西）、Achumani（拉巴斯）分行，全国服务网点超过120个。",
        "impact": "延续全国扩张战略，强化在圣克鲁斯增长最快的住宅与商业新区的布局，巩固其'玻利维亚最大私营银行'地位。",
        "source": "https://eldeber.com.bo/te-puede-interesar/bmsc-estrena-moderna-amplia-agencia-urubo-primera-municipio-porongo_1786638567",
    },
    {
        "date": "2026-03-19",
        "title": "穆迪地方（Moody's Local Bolivia）确认 BMSC 本币发行人 AAA.bo 评级，展望负面",
        "description": "评级机构于2026年3月17日开会、19日发布报告：确认 BMSC 本币发行人及本币中长期存款评级 AAA.bo（短期 A-1.bo），外币中长期存款 A.bo，展望维持负面。2025年全行净利润 4.13 亿玻利维亚诺（同比+38.94%），总贷款组合同比+2.21%（企业贷款+35.06%、中小企业+12.50%、住房按揭占比54.59%）；报告同时披露新核心银行系统已投产、处于稳定化阶段，并指出外汇提款限制与流动性指标下降等风险。",
        "impact": "最高本币评级获确认有助于其债券融资，但负面展望反映玻利维亚宏观经济（通胀、外汇短缺）对银行业的持续压力。",
        "source": "https://moodyslocal.com.bo/wp-content/uploads/2026/03/MLBO_Informe-Final-BMSC_19.03.2026.pdf",
    },
    {
        "date": "2025-02-03",
        "title": "BMSC 迎来120周年，盘点年度业绩与国际奖项，'Puedes Creer'基金会受益者超5.8万人",
        "description": "BMSC 以'迈向120年领导地位'为主题庆祝成立120周年并总结上一年度业绩与多项国际荣誉；执行副总裁 Alberto Valdés 表示全行聚焦金融科技投资。旗下社会责任机构 Fundación Mercantil Santa Cruz 'Puedes Creer'通过教育、卫生与体育项目累计惠及超过5.8万名玻利维亚人。",
        "impact": "强化其'玻利维亚历史最悠久、规模最大私营银行'的品牌形象，并凸显企业社会责任投入。",
        "source": "https://www.atb.com.bo/2025/02/03/bmsc-rumbo-a-los-120-anos-de-liderazgo-en-bolivia-celebra-un-ano-de-logros-e-importantes-reconocimientos/",
    },
]

data["related_entities"] = [
    {
        "org_id": "BO-FIN-002",
        "org_name": "Autoridad de Supervisión del Sistema Financiero (ASFI)",
        "org_type": "FIN",
        "org_description": "玻利维亚金融系统监管局，负责对银行等金融机构的审慎监管；BMSC 官方渠道明示'本机构受 ASFI 监管'。",
        "relationship_type": "regulated_by",
    },
    {
        "org_id": "BO-FIN-001",
        "org_name": "Banco Central de Bolivia (BCB)",
        "org_type": "FIN",
        "org_description": "玻利维亚中央银行，国家货币当局，负责货币政策与支付清算体系，是商业银行开展准备金与清算业务的政策对手方。",
        "relationship_type": "regulator",
    },
    {
        "org_id": None,
        "org_name": "Grupo Financiero Mercantil Santa Cruz (Sociedad Controladora Mercantil Santa Cruz S.A.)",
        "org_type": "FIN",
        "org_description": "BMSC 的控股母公司/金融集团（主股东），玻利维亚最重要的金融集团之一，旗下涵盖银行、证券、保险、基金管理等子公司。",
        "relationship_type": "controlling_shareholder",
    },
    {
        "org_id": None,
        "org_name": "Mercantil Santa Cruz Agencia de Bolsa S.A.",
        "org_type": "FIN",
        "org_description": "集团旗下证券经纪公司（Agencia de Bolsa），办公地址设于 BMSC 拉巴斯总部二楼，从事证券经纪与债券发行结构化业务（官网 mscbolsa.com.bo）。",
        "relationship_type": "subsidiary",
    },
    {
        "org_id": None,
        "org_name": "Universal Brokers S.A.",
        "org_type": "FIN",
        "org_description": "集团旗下证券经纪/交易商公司，属 Grupo Mercantil Santa Cruz 成员企业。",
        "relationship_type": "subsidiary",
    },
    {
        "org_id": None,
        "org_name": "SAFI Mercantil Santa Cruz S.A.",
        "org_type": "FIN",
        "org_description": "集团旗下基金管理公司（SAFI），负责共同基金的投资管理业务。",
        "relationship_type": "subsidiary",
    },
    {
        "org_id": None,
        "org_name": "Mercantil Santa Cruz Seguros y Reaseguros Generales S.A.",
        "org_type": "FIN",
        "org_description": "集团旗下一般保险与再保险公司，属 Grupo Mercantil Santa Cruz 成员企业。",
        "relationship_type": "subsidiary",
    },
    {
        "org_id": None,
        "org_name": "Fundación Mercantil Santa Cruz 'Puedes Creer'",
        "org_type": "NGO",
        "org_description": "BMSC 发起的社会责任基金会，通过教育、卫生与体育项目服务弱势社区，2025年成立十周年、累计受益超过5.8万人。",
        "relationship_type": "affiliated",
    },
    {
        "org_id": "BO-ACAD-003",
        "org_name": "Universidad Autónoma Gabriel René Moreno (UAGRM)",
        "org_type": "ACAD",
        "org_description": "圣克鲁斯最主要的公立大学，与 BMSC 结为合作伙伴（'Pacto Verde'合作计划），开展校企合作。",
        "relationship_type": "partner",
    },
    {
        "org_id": None,
        "org_name": "Visa Inc.",
        "org_type": "CORP",
        "org_description": "全球支付网络；为 KOIN 钱包配套 Visa 卡发卡与稳定币（USDC）清算能力，双方在拉美稳定币结算领域战略合作。",
        "relationship_type": "strategic_alliance",
    },
    {
        "org_id": None,
        "org_name": "Koibanx",
        "org_type": "CORP",
        "org_description": "拉美区块链基础设施公司，为 KOIN 平台提供区块链底层与金融生态集成技术。",
        "relationship_type": "supplier",
    },
]

data["core_business"] = (
    "Banco Mercantil Santa Cruz（BMSC）是玻利维亚最大的私营商业银行，总部位于拉巴斯（Calle Ayacucho No 277），"
    "由 Simón I. Patiño 于1905年12月11日创立的 Banco Mercantil 与1966年创立的 Banco Santa Cruz 于2006年合并而成，2016-2017年"
    "相继整合 Mutual La Paz 与 Banco PyME Los Andes ProCredit，2023年在中国人民银行式干预中承接了问题银行 Banco Fassil 的部分资产与负债。"
    "银行持有 ASFI 颁发的多功能银行（banca múltiple）牌照，提供全能银行服务：个人银行（储蓄、定期存款、按揭贷款、消费信贷、信用卡）、"
    "企业与公司银行（营运资金与项目融资、贸易金融）、中小企业信贷、外汇与国际贸易融资、保险经纪、证券化及财富管理。截至2026年，"
    "集团口径总资产逾59.7亿美元、存款逾49.3亿美元、贷款组合逾40.3亿美元、活跃客户超120万，拥有120余个营业网点和470余台ATM；"
    "按揭贷款占贷款组合约54.59%（2025年末），2025年新增投放以企业与中小企业贷款为主。渠道方面除实体网点外，提供网上银行、"
    "手机银行、借记/信用卡'plaTa'与积分权益体系（B de BMSC），并于2026年7月推出玻利维亚首个银行系数字资产钱包 KOIN（USDC 稳定币"
    "买卖与 Visa 卡消费）。母公司 Grupo Financiero Mercantil Santa Cruz 旗下还设有证券经纪（MSC Agencia de Bolsa、Universal Brokers）、"
    "基金管理（SAFI MSC）及一般保险（MSC Seguros）子公司，形成银行主导的综合金融集团。穆迪地方（2026-03）确认其本币发行人评级为"
    "玻利维亚国内最高档 AAA.bo，AESA 与惠誉地方亦分别给予 AAA 本币/AA 外币评级（展望负面）。"
)

data["apec_stance"] = "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。"

data["industries"] = ["banking", "financial_services", "payment_services"]

data["profile"] = {
    "source_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Banco_Mercantil_Santa_Cruz_Logo.svg/250px-Banco_Mercantil_Santa_Cruz_Logo.svg.png",
    "local_path": None,
}

data["collection_meta"] = {
    "collection_date": "2026-10-24",
    "phase": "phase3_enriched",
    "data_sources": [
        "wikidata",
        "wikipedia",
        "official_website",
        "moodyslocal_bolivia_issuer_report_2026-03-19",
        "asfi_bond_prospectus_bmsc_emision2",
        "eldeber",
        "negociospress",
        "latamfintech",
        "atb_com_bo",
        "trendsetterbolivia",
        "dnb_business_directory",
        "google_play",
        "facebook_official_page",
        "x_twitter_official",
        "instagram_official",
        "linkedin_official",
    ],
    "quotes": [
        {
            "title": "Moody's Local Bolivia — Informe Final Banco Mercantil Santa Cruz S.A. (19.03.2026)",
            "url": "https://moodyslocal.com.bo/wp-content/uploads/2026/03/MLBO_Informe-Final-BMSC_19.03.2026.pdf",
        },
        {
            "title": "Latam Fintech — Banco Mercantil Santa Cruz lanza KOIN, una e-wallet para acceder a activos digitales en Bolivia",
            "url": "https://www.latamfintech.co/articles/banco-mercantil-santa-cruz-lanza-koin-una-e-wallet-para-acceder-a-activos-digitales-en-bolivia",
        },
        {
            "title": "El Deber — BMSC estrena moderna y amplia agencia en el Urubó, la primera en el municipio de Porongo",
            "url": "https://eldeber.com.bo/te-puede-interesar/bmsc-estrena-moderna-amplia-agencia-urubo-primera-municipio-porongo_1786638567",
        },
        {
            "title": "ATB — BMSC, rumbo a los 120 años de liderazgo en Bolivia, celebra un año de logros e importantes reconocimientos",
            "url": "https://www.atb.com.bo/2025/02/03/bmsc-rumbo-a-los-120-anos-de-liderazgo-en-bolivia-celebra-un-ano-de-logros-e-importantes-reconocimientos/",
        },
        {
            "title": "BMSC 官网 AboutUs（集团沿革、经营规模、信用评级）",
            "url": "https://www.bmsc.com.bo/AboutUs",
        },
        {
            "title": "ASFI — Bonos Banco Mercantil Santa Cruz Emisión 2（主要高管名单存档）",
            "url": "https://www.asfi.gob.bo/sites/default/files/2025-08/Bonos%20BANCO%20MERCANTIL%20SANTA%20CRUZ%20-%20Emisi%C3%B3n%202.pdf",
        },
    ],
    "completeness_score": data.get("collection_meta", {}).get("completeness_score", 16),
    "notes": "Phase3 富化：官网、穆迪地方2026年3月发行人报告（PDF全文提取）、ASFI债券招募书、2025-2026年媒体报道多源交叉核实；董事长 Darko Zuazo Batchelder 与执行副总裁 Alberto Valdés 任职经2025-2026年来源确认；KOIN 于2026-07-23发布（多源）。玻利维亚非APEC成员。",
}

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("WROTE", PATH)

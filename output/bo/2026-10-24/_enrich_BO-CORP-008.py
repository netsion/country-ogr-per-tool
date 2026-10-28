#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enrich BO-CORP-008 (Tigo Bolivia) — phase3_enriched. Temporary writer script."""
import json

FP = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/orgs/BO-CORP-008.json"

with open(FP, encoding="utf-8") as f:
    data = json.load(f)

data["basic_info"].update({
    "name_zh": "Tigo玻利维亚电信公司",
    "name_en": "Tigo Bolivia",
    "aliases": [
        "Telecel",
        "Telefónica Celular de Bolivia S.A.",
        "Tigo Star Bolivia（2014-2019年付费电视品牌）",
        "Bolivia Telecel S.A.",
    ],
    "website": "https://www.tigo.com.bo",
})

data["industries"] = ["telecommunications", "mobile_telecommunications", "financial_services", "payment_services"]

data["social_accounts"] = [
    {
        "platform": "facebook",
        "account_name": "Tigo Bolivia",
        "url": "https://www.facebook.com/BoliviaTigo",
        "source": "tigo.com.bo页脚社交图标及官方帖子链接（facebook.com/BoliviaTigo）",
    },
    {
        "platform": "instagram",
        "account_name": "@tigobolivia",
        "url": "https://www.instagram.com/tigobolivia/",
        "source": "Instagram官方主页（Tigo Bolivia @tigobolivia）",
    },
    {
        "platform": "twitter_x",
        "account_name": "@Tigo_Bolivia",
        "url": "https://twitter.com/Tigo_Bolivia",
        "source": "tigo.com.bo页脚twitter:site元标签",
    },
    {
        "platform": "youtube",
        "account_name": "Tigo Bolivia (@BoliviaTigo)",
        "url": "https://www.youtube.com/@BoliviaTigo",
        "source": "YouTube官方频道（2026年9月以@BoliviaTigo进行官方直播）",
    },
]

data["digital_assets"] = [
    {
        "name": "Tigo Money",
        "url": "https://play.google.com/store/apps/details?id=bo.tigo.mfsapp",
        "description": "玻利维亚首个移动钱包/数字金融服务（2013年推出），由子公司E-FECTIVO S.A.运营，支持转账、缴费、二维码支付等；2014年起向竞争对手Entel与Viva的用户开放，另有网页版入口。",
        "source": "Wikipedia（Tigo (Bolivia)）、Google Play应用商店",
    },
    {
        "name": "Mi Tigo",
        "url": "https://www.tigo.com.bo",
        "description": "自助服务门户与应用，用户可查询账单、管理套餐与充值。",
        "source": "tigo.com.bo官网导航（Servicios: Mi Tigo）",
    },
    {
        "name": "Tigo Sports",
        "url": None,
        "description": "体育频道及应用，由子公司Producciones Digitales de Bolivia S.R.L.制作，转播玻利维亚足球甲级联赛，通过Tigo Hogar付费电视专属频道（700/717/718 HD）及App播出。",
        "source": "Wikipedia（Tigo (Bolivia)、Tigo Sports条目）",
    },
    {
        "name": "Tigo ONE tv",
        "url": None,
        "description": "基于App的互联网电视（OTT）服务，可在多种联网设备上安装观看。",
        "source": "Wikipedia（Tigo (Bolivia)）",
    },
    {
        "name": "EducaTigo",
        "url": None,
        "description": "面向儿童与青少年学习的教育频道。",
        "source": "Wikipedia（Tigo (Bolivia)）",
    },
]

data["key_people"] = [
    {
        "person_id": None,
        "name": "迭戈·古铁雷斯（Diego Gutiérrez）",
        "title": "首席执行官（Gerente General / CEO）",
        "title_description": "总经理兼首席执行官",
        "description": "玻利维亚籍高管，2026年1月15日获Telecel S.A.董事会批准、1月19日正式就任Tigo玻利维亚CEO。此前自2017年起任Vodacom（沃达丰集团）国际市场CEO，负责坦桑尼亚、刚果（金）、莫桑比克、莱索托等市场，管理超1.1亿客户基础，并参与建设非洲最大金融科技平台之一；更早曾任职于母公司Millicom。拥有玻利维亚天主教大学ePC商学院MBA。上任重点为加速公司数字化转型、升级网络基础设施并扩张Tigo Money金融科技业务。",
    },
    {
        "person_id": None,
        "name": "巴勃罗·瓜迪亚（Pablo Guardia）",
        "title": "董事会成员（前任CEO）",
        "title_description": "董事；2011-2024年任总经理",
        "description": "2011年起担任Tigo玻利维亚总经理（CEO）长达13年，2024年4月卸任；据2026年1月报道，其继续以董事会成员身份为公司提供战略支持，并于2026年1月向迭戈·古铁雷斯完成交接。",
    },
]

data["departments"] = [
    {
        "name": "移动通信业务",
        "dept_id": None,
        "head": None,
        "description": "核心业务板块：提供2G/3G/4G移动服务（4G已全国覆盖）并推进5G准备；为玻利维亚首家提供3.5G与eSIM服务的运营商，另以字冠17提供国内国际长途。",
        "parent_dept_id": None,
    },
    {
        "name": "家庭业务（固网、宽带与电视）",
        "dept_id": None,
        "head": None,
        "description": "提供有线宽带（含WiMAX）、付费电视（有线电视与卫星电视）及固话服务；2013年收购有线运营商Multivisión（2000万美元），2014年推出Tigo Star卫星电视品牌并于2019年前后完成品牌整合。",
        "parent_dept_id": None,
    },
    {
        "name": "Tigo Money数字金融业务",
        "dept_id": None,
        "head": None,
        "description": "运营玻利维亚首个移动钱包Tigo Money（2013年上线），经子公司E-FECTIVO S.A.开展，2014年起向Entel与Viva用户开放，是公司金融科技与普惠金融战略的核心。",
        "parent_dept_id": None,
    },
    {
        "name": "媒体与内容业务",
        "dept_id": None,
        "head": None,
        "description": "通过子公司Producciones Digitales de Bolivia S.R.L.制作Tigo Sports体育频道（转播玻利维亚足球甲级联赛），并运营Tigo ONE tv、EducaTigo教育频道，套餐中分销Amazon Prime Video、HBO Max、Paramount+、Universal+等流媒体。",
        "parent_dept_id": None,
    },
    {
        "name": "企业客户业务（Tigo Business）",
        "dept_id": None,
        "head": None,
        "description": "面向政企客户提供企业连接与数字化转型解决方案，定期举办面向企业的网络研讨会等活动。",
        "parent_dept_id": None,
    },
]

data["recent_events"] = [
    {
        "date": "2025-11-12",
        "title": "玻利维亚ATT批准4G频谱招标时间表，Tigo将以私营运营商身份参与竞标",
        "description": "玻利维亚电信监管机构ATT批准2026年初新4G频谱（1710-1770 MHz与2110-2170 MHz频段）招标日程：2025年12月15日公布招标条件，2026年1月19-20日提交技术与经济标书。国营Entel（市场份额约58%）获预留子频段且此前已获5G频段直接分配；私营运营商Tigo与Viva（份额各约25%-32%）须通过竞标获得频谱。",
        "impact": "频谱政策直接影响Tigo未来4G/5G网络扩容成本与竞争格局；与国营Entel相比处于制度性劣势地位。",
        "source": "https://www.telesemana.com/blog/2025/11/12/bolivia-licitara-espectro-para-4g-a-principios-de-2026/",
    },
    {
        "date": "2026-01-19",
        "title": "迭戈·古铁雷斯出任Tigo玻利维亚CEO",
        "description": "2026年1月15日获Telecel S.A.董事会批准、1月19日正式就任，接替掌舵13年的巴勃罗·瓜迪亚（转任董事会成员）。古铁雷斯曾任Vodacom集团国际市场CEO（主管坦桑尼亚、刚果（金）、莫桑比克、莱索托，服务超1.1亿用户），并曾任职于Millicom；公司表示其非洲金融科技经验将重点赋能Tigo Money扩张，推动公司由电信运营商向综合数字服务商转型。",
        "impact": "领导层更替：新CEO拥有新兴市场与金融科技背景，预计加速数字化转型与Tigo Money金融业务扩张。",
        "source": "https://www.teleinfopress.com/post/diego-gutiérrez-se-convierte-en-el-nuevo-ceo-de-tigo-bolivia",
    },
    {
        "date": "2026-03-12",
        "title": "Tigo玻利维亚宣布投资超1000万美元加强拉巴斯移动网络",
        "description": "对拉巴斯271个无线基站进行扩容，重点覆盖Huyustus集市、总公墓区、批发商业走廊、Villa Fátima市场及Minasa省际客运站等高流量商业与交通区域，属于全国网络现代化计划的一部分；CEO古铁雷斯称此举旨在改善通话清晰度、上网速度与数字交易流畅度。",
        "impact": "显著提升玻利维亚行政首都所在地拉巴斯高密度商业区的移动网络容量与服务质量。",
        "source": "https://www.urgente.bo/noticia/tigo-refuerza-su-red-movil-en-la-paz-con-una-inversion-de-mas-de-10-millones-de-dolares",
    },
    {
        "date": "2026-05-26",
        "title": "Tigo玻利维亚位列2026年建设性资本指数（ICC）榜首",
        "description": "在米利尼奥基金会（Fundación Milenio）编制的2026年建设性资本指数（Índice de Capital Constructivo）中，Tigo玻利维亚在45家受评企业中排名第一，获AAA+评级（97.2/100），反映其对国家发展的企业贡献；公司官方账号于5月26日发布致谢。",
        "impact": "巩固公司声誉与企业公民形象，为品牌与监管沟通提供加分项。",
        "source": "https://www.facebook.com/BoliviaTigo/posts/estamos-entre-las-empresas-con-mejor-reputaci%C3%B3n-de-boliviaagradecemos-profundame/1475216277982263/",
    },
    {
        "date": "2026-07-15",
        "title": "MERCO ESG玻利维亚2025-2026榜单：Tigo蝉联电信业最负责任企业",
        "description": "在MERCO责任ESG玻利维亚2025-2026排名（7月中旬发布）中，Tigo玻利维亚位列全国第七、电信行业第一，并在社会维度排名第四，继续保持国内ESG表现最佳的电信企业地位。",
        "impact": "强化公司在环境、社会与治理（ESG）领域的行业标杆形象。",
        "source": "https://rcbolivia.com/tigo-fortalece-su-liderazgo-esg-y-se-mantiene-como-la-empresa-de-telecomunicaciones-mas-responsable-del-pais/",
    },
]

data["related_entities"] = [
    {
        "org_id": None,
        "org_name": "Millicom International Cellular S.A.（Millicom集团）",
        "org_type": "CORP",
        "org_description": "总部位于卢森堡、聚焦拉美的上市电信集团（Tigo品牌所有者）；通过Millicom International IV NV（50.98%）与Millicom International Enterprise AB（49.01%）合计持有Tigo玻利维亚近100%股权。",
        "relationship_type": "parent_org",
    },
    {
        "org_id": "BO-GOV-032",
        "org_name": "Autoridad de Regulación y Fiscalización de Telecomunicaciones y Transportes（ATT，玻利维亚电信与交通运输监管审计局）",
        "org_type": "GOV",
        "org_description": "玻利维亚电信行业监管机构；Tigo官网明确标注公司受ATT监管与审计（Empresa regulada y fiscalizada por la ATT），频谱分配、资费与服务合规均受其管辖。",
        "relationship_type": "regulator",
    },
    {
        "org_id": None,
        "org_name": "E-FECTIVO S.A.（Tigo Money）",
        "org_type": "CORP",
        "org_description": "Tigo玻利维亚子公司，负责运营Tigo Money移动钱包与数字支付业务。",
        "relationship_type": "subsidiary",
    },
    {
        "org_id": None,
        "org_name": "Producciones Digitales de Bolivia S.R.L.",
        "org_type": "CORP",
        "org_description": "Tigo玻利维亚子公司，负责制作Tigo Sports体育频道内容并转播玻利维亚足球甲级联赛。",
        "relationship_type": "subsidiary",
    },
]

data["core_business"] = (
    "Tigo玻利维亚是卢森堡Millicom集团在玻利维亚的电信子公司（法律实体为Telefónica Celular de Bolivia S.A.，"
    "早期以Telecel品牌经营），总部位于圣克鲁斯-德拉谢拉，1990年11月在玻利维亚率先提供移动电话服务，并首创预付费电话卡销售。"
    "公司长期为玻利维亚主要移动运营商之一（西语维基百科称其为第二大移动运营商；近年监管数据更新不足，Tigo与Viva市场份额均约25%-32%，"
    "与占约58%的国营Entel（BO-SOE-004）三足鼎立，Viva（BO-CORP-009）为另一竞争者）。核心业务涵盖：移动通信"
    "（2G/3G/4G全国覆盖并推进5G准备，率先推出3.5G与eSIM服务）；固定宽带与WiMAX上网；付费电视（有线电视与卫星电视，"
    "曾整合Multivisión并运营Tigo Star品牌）；流媒体与内容（Tigo Sports、Tigo ONE tv、EducaTigo，并分销Amazon Prime Video、"
    "HBO Max、Paramount+、Universal+）；以字冠17提供国内国际长途；以及2013年推出的玻利维亚首个移动钱包Tigo Money"
    "（经子公司E-FECTIVO S.A.运营，2014年起向Entel、Viva用户开放）。公司目前正从传统电信运营商向融合连接与数字金融的"
    "综合数字服务商转型。2016年营收5.67亿美元、总资产7.53亿美元；2025年员工约1926人。"
)

data["apec_stance"] = "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。"

data["profile"] = {
    "source_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Logo_Tigo.svg/250px-Logo_Tigo.svg.png",
    "local_path": None,
}

data["collection_meta"] = {
    "collection_date": "2026-10-24",
    "phase": "phase3_enriched",
    "data_sources": [
        "es.wikipedia.org（Tigo (Bolivia)、Tigo Sports、Millicom条目）",
        "tigo.com.bo（官网首页、页脚社交链接、sala de prensa）",
        "teleinfopress.com",
        "nuevaeconomia.com.bo",
        "urgente.bo",
        "telesemana.com",
        "rcbolivia.com",
        "facebook.com/BoliviaTigo（公司官方账号）",
        "instagram.com/tigobolivia",
        "twitter.com/Tigo_Bolivia（官网元标签核实）",
        "play.google.com（Tigo Money应用）",
    ],
    "quotes": [
        {
            "title": "Diego Gutiérrez se convierte en el nuevo CEO de Tigo Bolivia（TeleinfoPress, 2026-01-26）",
            "url": "https://www.teleinfopress.com/post/diego-gutiérrez-se-convierte-en-el-nuevo-ceo-de-tigo-bolivia",
        },
        {
            "title": "Tigo refuerza su red móvil en La Paz con una inversión de más de 10 millones de dólares（Urgente.bo, 2026-03-12）",
            "url": "https://www.urgente.bo/noticia/tigo-refuerza-su-red-movil-en-la-paz-con-una-inversion-de-mas-de-10-millones-de-dolares",
        },
        {
            "title": "Bolivia licitará espectro para 4G a principios de 2026（TeleSemana.com, 2025-11-12）",
            "url": "https://www.telesemana.com/blog/2025/11/12/bolivia-licitara-espectro-para-4g-a-principios-de-2026/",
        },
        {
            "title": "Tigo fortalece su liderazgo ESG y se mantiene como la empresa de telecomunicaciones más responsable del país（Tigo sala de prensa / RC Bolivia, 2026-07）",
            "url": "https://www.tigo.com.bo/sala-de-prensa/tigo-se-mantiene-como-la-empresa-de-telecomunicaciones-mas-responsable-del-pais",
        },
        {
            "title": "Tigo (Bolivia) - Wikipedia（公司历史、股权结构与子公司）",
            "url": "https://es.wikipedia.org/wiki/Tigo_(Bolivia)",
        },
        {
            "title": "Diego Gutiérrez asume como CEO de Tigo Bolivia tras casi dos décadas de liderazgo en África（NuevaEconomía, 2026-01-16）",
            "url": "https://nuevaeconomia.com.bo/news/diego-gutirrez-asume-como-ceo-de-tigo-bolivia-tras-casi-dcadas-de-liderazgo-en-frica",
        },
    ],
    "completeness_score": 11,
    "notes": (
        "竞争关系说明：主要竞争对手Entel（BO-SOE-004，国营）与Viva（BO-CORP-009）因schema关系类型枚举不含competitor类型，"
        "未列入related_entities，已在core_business与recent_events中描述。CEO更替（2026-01）经TeleinfoPress与NuevaEconomia双源核实；"
        "MERCO ESG与ICC 2026排名经官网、RC Bolivia及公司官方社媒多源核实；2025-11频谱招标经TeleSemana报道核实。"
        "官网为JS单页应用，页脚及导航信息经web_reader提取；5G尚未商用（全国5G频谱未完成向私营运营商分配）。"
    ),
}

with open(FP, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("written:", FP)

# -*- coding: utf-8 -*-
"""Write enriched profile for BO-SOE-008 (Emapa). v2"""
import json

PATH = "D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/orgs/BO-SOE-008.json"

with open(PATH, encoding="utf-8") as f:
    data = json.load(f)

data["basic_info"]["name_zh"] = "食品生产支持公司（Emapa）"
data["basic_info"]["name_en"] = "Food Production Support Company (EMAPA)"
data["basic_info"]["aliases"] = ["EMAPA", "Emapa", "EMAPA Bolivia", "Emapa Bolivia"]
data["basic_info"]["founded_date"] = "2007-08-15"
data["basic_info"]["website"] = "https://emapa.gob.bo"
data["basic_info"]["wikidata_qid"] = None
data["basic_info"]["hq_city"] = "La Paz（拉巴斯）"
data["basic_info"]["hq_address"] = "Av. Mariscal Santa Cruz, Edif. Centro de Comunicaciones, La Paz, Bolivia"

data["profile"] = {
    "source_url": "https://emapa.gob.bo/wp-content/uploads/2026/05/emapa-azul.png",
    "local_path": None,
}

data["social_accounts"] = [
    {
        "platform": "facebook",
        "account_name": "EMAPA Bolivia",
        "url": "https://www.facebook.com/EmapaBolivia",
        "source": "Emapa官方帖子公布的官方账号清单及官网页脚（约12.9万粉丝，2026年核实）",
    },
    {
        "platform": "instagram",
        "account_name": "emapa.bolivia.oficial",
        "url": "https://www.instagram.com/emapa.bolivia.oficial",
        "source": "Emapa官方帖子公布的官方账号清单（2026-05核实）",
    },
]

data["digital_assets"] = [
    {
        "name": "Emapa官方网站",
        "url": "https://emapa.gob.bo",
        "description": "官方网站（WordPress/WooCommerce平台），含机构介绍、组织架构（组织图、负责人名册、薪酬表）、透明度与审计、年度运营计划、供应商招标、举报与信息公开表单，并提供全国门店查询入口",
        "source": "https://emapa.gob.bo",
    },
    {
        "name": "新闻发布页（Notas de Prensa）",
        "url": "https://emapa.gob.bo/comunicacion/noticias/notas-prensa",
        "description": "官方新闻稿栏目，发布粮食收购、工业厂区重启、展会与平价销售等动态",
        "source": "https://emapa.gob.bo/comunicacion/noticias/notas-prensa",
    },
    {
        "name": "玻利维亚政府门户网站Emapa页面",
        "url": "https://www.gob.bo/entidades/empresa-de-apoyo-a-la-produccion-de-alimentos",
        "description": "国家政府门户网站中的Emapa机构页，说明其为国家战略类公共企业（Empresa Pública Nacional Estratégica）",
        "source": "https://www.gob.bo/entidades/empresa-de-apoyo-a-la-produccion-de-alimentos",
    },
    {
        "name": "客户服务渠道（官方）",
        "url": "https://emapa.gob.bo",
        "description": "客服邮箱 atencion.cliente@emapa.gob.bo，免费热线 800-10-1230",
        "source": "https://emapa.gob.bo",
    },
]

data["key_people"] = [
    {
        "person_id": None,
        "name": "塞尔希奥·西莱斯·桑切斯（Sergio Siles Sánchez）",
        "title": "Gerente General (a.i.)",
        "title_description": "总经理（临时任命，以代理身份主持工作）",
        "description": "2025年12月9日被政府任命为Emapa临时总经理，接替Richard Wilmer Rojas Ramos；截至2026年10月仍以总经理（代理）身份主持工作。任内启动内部反腐审计、宣布关闭20余家亏损门店、将公司预算削减45%并推进10个新项目以摆脱亏损（2026年2月至10月多家媒体持续以「总经理」身份报道其活动）。",
    },
    {
        "person_id": None,
        "name": "理查德·威尔默·罗哈斯·拉莫斯（Richard Wilmer Rojas Ramos）",
        "title": "Ex Gerente General",
        "title_description": "前任总经理（2025年9月-12月，已离任）",
        "description": "2025年9月2日接替Franklin Flores出任Emapa总经理，帕斯政府2025年11月上台后短暂留任（11月中旬再次出席就任活动），同年12月9日因公司审计发现前任管理层涉嫌巨额损失等问题被Sergio Siles接替；其本人为当选众议员。",
    },
    {
        "person_id": None,
        "name": "富兰克林·理查德·弗洛雷斯·科尔多瓦（Franklin Richard Flores Córdova）",
        "title": "Ex Gerente General",
        "title_description": "前总经理（2021年5月-2025年9月，已离任，现涉司法调查）",
        "description": "MAS籍政客，2021年5月26日由生产发展与多元经济部长Néstor Huanca任命为总经理，任职至2025年9月2日。2026年1月2日在拉巴斯被逮捕，随后被判处5个月预防性拘留，面临至少5项司法调查（包括涉嫌非法致富——其向国家审计署申报资产达283.6万玻利维亚诺），多起案件涉及其执掌Emapa期间的经营管理。",
    },
]

data["departments"] = [
    {
        "name": "总经理办公室（Gerencia General）",
        "dept_id": None,
        "head": "塞尔希奥·西莱斯·桑切斯（Sergio Siles Sánchez）",
        "description": "公司最高管理机构，负责整体经营、审计整改与新管理模式推进",
        "parent_dept_id": None,
    },
    {
        "name": "商业销售部（Gerencia de Comercialización）",
        "dept_id": None,
        "head": None,
        "description": "负责全国门店与销售网络、食品平价销售（如「Emapa来到你的社区」流动销售）及内外贸销售",
        "parent_dept_id": None,
    },
    {
        "name": "收购与加工部（Gerencia de Acopio y Transformación）",
        "dept_id": None,
        "head": None,
        "description": "负责小麦、大米、玉米等粮食的基准价收购（acopio）与加工转化，下辖各工业加工厂（Nuestras Plantas）",
        "parent_dept_id": None,
    },
    {
        "name": "生产部（Gerencia de Producción）",
        "dept_id": None,
        "head": None,
        "description": "负责自有生产项目与农牧业生产支持",
        "parent_dept_id": None,
    },
    {
        "name": "行政财务部（Gerencia Administrativa Financiera）",
        "dept_id": None,
        "head": None,
        "description": "负责行政、财务与预算管理；2026年主导将公司预算由44亿玻利维亚诺压缩至24亿玻利维亚诺的重组",
        "parent_dept_id": None,
    },
    {
        "name": "全国分公司网络（Sucursales / Tiendas Emapa）",
        "dept_id": None,
        "head": None,
        "description": "零售网络：2024年7月全国共有101家门店（其中拉巴斯省46家），覆盖全国九个省府城市，含Súper Emapa与Express等业态；2026年2月起陆续关闭约20-25家亏损门店并重组商业网络",
        "parent_dept_id": None,
    },
    {
        "name": "工业加工厂（Plantas Industriales）",
        "dept_id": None,
        "head": None,
        "description": "包括圣克鲁斯省Chane-Piray粮食收购仓储厂、San Julián大米加工厂、埃尔阿尔托奶制品厂及平衡饲料厂等；贝尼省San Borja屠宰冷冻联合厂（Matadero Frigorífico）项目投资逾1.536亿玻利维亚诺，2026年年中土建进度约84%、财务执行约63%",
        "parent_dept_id": None,
    },
]

data["recent_events"] = [
    {
        "date": "2025-12-09",
        "title": "塞尔希奥·西莱斯被任命为Emapa临时总经理",
        "description": "政府在审计发现Emapa前任管理层涉嫌造成巨额损失（presunto daño millonario）后，任命Sergio Siles Sánchez为临时总经理，接替仅任职约三个月的Richard Wilmer Rojas Ramos，并启动内部审计。",
        "impact": "领导层更迭叠加反腐审计，公司进入整改与重组期；后续2026年2月总经理公开表示过往管理层腐败造成重大损失。",
        "source": "https://www.opinion.com.bo/pais/sergio-siles-es-designado-como-gerente-interino-emapa/20251209183413985095.html",
    },
    {
        "date": "2026-01-02",
        "title": "前总经理Franklin Flores被逮捕",
        "description": "Emapa前总经理（2021-2025年任职）Franklin Richard Flores Córdova在拉巴斯被逮捕，随后被判处5个月预防性拘留；其面临至少5项司法调查，包括涉嫌非法致富（向国家审计署申报资产283.6万玻利维亚诺），多起案件涉及其执掌Emapa期间。",
        "impact": "印证公司历史上管理腐败问题的严重性，为帕斯政府对公司开展反腐整改提供背景。",
        "source": "https://eldeber.com.bo/pais/justicia-dicta-cinco-meses-detencion-preventiva-franklin-flores-exgerente-emapa_1767469189",
    },
    {
        "date": "2026-02-25",
        "title": "Emapa宣布关闭20家亏损门店",
        "description": "总经理Sergio Siles宣布关闭城市和农村地区20家亏损、被认定非必要的门店，作为压缩运营成本、扭转亏损的举措。",
        "impact": "全国零售网络明显收缩，公司由规模扩张转向成本控制。",
        "source": "https://unitel.bo/noticias/economia/son-deficitarias-emapa-anuncia-el-cierre-de-20-tiendas-en-areas-urbanas-y-rurales-LD19389604",
    },
    {
        "date": "2026-03-17",
        "title": "启动关闭「非盈利」分公司并重组商业网络",
        "description": "Emapa开始正式关闭「非盈利」分支机构并重新布局商业网络，同时计划开设新门店并扩大产品供应。",
        "impact": "零售网络重组持续推进，门店布局向盈利区域集中。",
        "source": "https://correodelsur.com/economia/20260317/emapa-inicia-cierre-de-sucursales-no-rentables-y-reubica-su-red-comercial.html",
    },
    {
        "date": "2026-06-25",
        "title": "全国封锁周期间向逾41.9万人销售鸡肉",
        "description": "在全国道路封锁引发食品供应紧张期间，Emapa通过其销售网络在一周内向超过41.9万人售出鸡肉，发挥国有食品企业平抑市场、保障基本供给的作用。",
        "impact": "凸显Emapa在危机时期作为国家食品供应稳定器的职能。",
        "source": "https://emapa.gob.bo/comunicacion/noticias/notas-prensa",
    },
    {
        "date": "2026-07-28",
        "title": "重启工业加工厂、推行新管理模式",
        "description": "Emapa宣布激活旗下工业加工厂，新管理模式优先利用闲置产能扩大食品生产；8月初又与丘基萨卡省小麦生产者达成协议，支持其小麦商业化销售。",
        "impact": "产能利用率提升，收购模式转向与生产者组织直接合作。",
        "source": "https://emapa.gob.bo/comunicacion/noticias/notas-prensa",
    },
    {
        "date": "2026-09-06",
        "title": "预算削减45%，退出十大最亏损国企名单",
        "description": "Emapa将年度运营预算从44亿玻利维亚诺削减至24亿玻利维亚诺（削减约20亿玻利维亚诺、幅度45%），退出国有十大亏损企业名单；总经理同时承认公司仍背负约6亿玻利维亚诺的遗留负债与债务。",
        "impact": "财务重组初见成效，但历史债务负担仍制约经营。",
        "source": "https://abi.bo/emapa-reduce-bs-2-000-millones-de-su-presupuesto-y-sale-del-grupo-de-las-10-empresas-estatales-mas-deficitarias/",
    },
    {
        "date": "2026-09-29",
        "title": "推进10个新项目谋求摆脱亏损、否认关停",
        "description": "总经理Sergio Siles Sánchez表示Emapa正推进10个新项目以维持运营、摆脱「亏损企业」标签；此前国内舆论曾讨论关停或彻底重组Emapa（「关停还是转型」之争），管理层明确否认关停。",
        "impact": "公司战略方向确定为转型存续而非清算关闭。",
        "source": "https://larazon.bo/economia-y-empresa/2026/09/29/emapa-apunta-a-mantenerse-en-operaciones-con-10-nuevos-proyectos/",
    },
    {
        "date": "2026-10-19",
        "title": "门店关闭累计推进至25家，与面包行业达成面粉协议",
        "description": "总经理Sergio Siles通报全国门店关闭累计推进至25家；同期Emapa与独立及联合会面包师达成协议并延长注册期限，就7.4万袋（quintales）面粉的返还达成「实物+现金」各半、最长30个工作日的处理方案，以维持面包价格稳定（Emapa通讯稿2026年10月19日及多家媒体报道）。",
        "impact": "零售网络进一步精简，同时通过面包行业合作强化主食价格稳定职能。",
        "source": "https://www.facebook.com/canalpalenquetv/posts/el-gerente-general-de-emapa-sergio-siles-inform%C3%B3-que-se-ampli%C3%B3-el-plazo-de-regis/1518662590308569/",
    },
]

data["related_entities"] = [
    {
        "org_id": "BO-GOV-012",
        "org_name": "生产发展与多元经济部（Ministerio de Desarrollo Productivo y Economía Plural）",
        "org_type": "GOV",
        "org_description": "玻利维亚主管生产发展与多元经济的政府部门，是Emapa的上级主管部门（tuición）；Emapa官网页眉并列使用该部标识，历任总经理由该部部长主持任命。其前身「生产发展、农村与水利部」2007年签署创建Emapa的第29230号最高法令。",
        "relationship_type": "parent_org",
    },
    {
        "org_id": "BO-GOV-018",
        "org_name": "农村发展与土地部（Ministerio de Desarrollo Rural y Tierras）",
        "org_type": "GOV",
        "org_description": "主管农牧业生产与土地政策的政府部门，与Emapa在粮食收购（小麦、玉米、大米）、农资支持等业务上密切协作。",
        "relationship_type": "partner",
    },
    {
        "org_id": "BO-SOE-009",
        "org_name": "穆通钢铁公司（Siderúrgica del Mutún）",
        "org_type": "SOE",
        "org_description": "玻利维亚国家级公共战略企业，负责圣克鲁斯省穆通铁矿的钢铁工业项目，与Emapa同属国家公共企业体系的姊妹国有企业。",
        "relationship_type": "sibling",
    },
    {
        "org_id": None,
        "org_name": "玻利维亚面包师联合会（Confederación de Panificadores de Bolivia）",
        "org_type": "NGO",
        "org_description": "全国面包师行业组织。2025-2026年间与Emapa围绕补贴面粉供应多次对话并达成合作（2026年10月就7.4万袋面粉返还达成「实物+现金」各半、最长30个工作日的方案），是Emapa平价面粉-面包供应链上的关键伙伴。",
        "relationship_type": "partner",
    },
]

data["core_business"] = (
    "Emapa是玻利维亚的国家战略类公共企业，2007年8月15日依据第29230号最高法令（DS Nº 29230）创建，总部设于拉巴斯。"
    "核心职能是支持农业食品产业链、保障国家粮食主权（soberanía alimentaria）：一是以政府确定的基准价收购小麦、大米、玉米等主粮，"
    "为中小农牧生产者提供收购保障、良种农资与技术融资支持；二是通过自有工业加工厂（粮食仓储烘干厂、大米加工厂、奶制品厂、平衡饲料厂，"
    "并在贝尼省San Borja建设屠宰冷冻联合厂）将初级农产品加工为食品；三是运营全国零售网络（2024年约101家门店、覆盖九个省府城市），"
    "以平价直接销售鸡肉、鸡蛋、面粉、糖等基本食品，在市场投机涨价、运输封锁等情形下发挥平抑物价、稳定供给的政策工具作用；"
    "四是开展内外贸销售以调节国内市场供求。2025年11月帕斯政府上台后，公司经历领导层更迭、反腐审计、关停20-25家亏损门店、"
    "预算削减45%等深度重组，当前定位转向压缩亏损、激活闲置产能的「转型存续」。"
)

data["industries"] = ["agriculture_food", "food_beverage", "retail", "logistics_warehousing"]

data["apec_stance"] = (
    "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。APEC现有成员为中国、美国、日本、韩国、俄罗斯、澳大利亚、"
    "加拿大、墨西哥、智利、秘鲁、新西兰、新加坡、马来西亚、泰国、菲律宾、印度尼西亚、越南、文莱、巴布亚新几内亚以及中国香港、"
    "中国台北等21个环太平洋经济体；玻利维亚从未加入APEC，因此Emapa作为玻利维亚国有企业不存在APEC成员资格或相关官方立场问题，"
    "其对外经贸合作主要面向安第斯共同体、南方共同市场等区域机制。"
)

data["collection_meta"] = {
    "collection_date": "2026-10-25",
    "phase": "phase3_enriched",
    "data_sources": [
        "web_search",
        "https://emapa.gob.bo（官方网站：机构介绍、组织架构、新闻、页眉MDPyEP标识与Logo）",
        "https://www.gob.bo/entidades/empresa-de-apoyo-a-la-produccion-de-alimentos（政府门户机构页）",
        "https://faolex.fao.org/docs/pdf/bol73462.pdf（创建法令DS Nº 29230全文）",
        "La Razón、ABI、Unitel、Correo del Sur、Opinión、El Deber、El Mundo、Urgente.bo、Vision360等玻利维亚媒体报道（2025-11至2026-10）",
        "Emapa官方Facebook/Instagram账号",
        "玻利维亚生产部SIIP系统Emapa资料页",
    ],
    "completeness_score": 0,
    "notes": "Wikidata无条目，画像完全由Web搜索构建。现任总经理为临时任命（a.i.）身份并经2026年9-10月多来源核实；历任总经理沿革（Flores 2021-05至2025-09、Rojas 2025-09至2025-12、Siles 2025-12至今）经多个独立来源交叉验证。部分细节（如各工业厂准确投产年份、各Gerencia现任负责人姓名、Emapa官方X/YouTube账号是否存在）未获可靠来源，相应字段留空。",
    "quotes": [
        {
            "title": "EMAPA - Empresa de Apoyo a la Producción de Alimentos（官方网站：Trabajando por la soberanía alimentaria de Bolivia）",
            "url": "https://emapa.gob.bo/",
        },
        {
            "title": "CREA LA EMPRESA DE APOYO A LA PRODUCCION DE ALIMENTOS - EMAPA, Decreto Supremo Nº 29230 de 15 de agosto de 2007（FAOLEX）",
            "url": "https://faolex.fao.org/docs/pdf/bol73462.pdf",
        },
        {
            "title": "Emapa apunta a mantenerse en operaciones con 10 nuevos proyectos（La Razón, 2026-09-29）",
            "url": "https://larazon.bo/economia-y-empresa/2026/09/29/emapa-apunta-a-mantenerse-en-operaciones-con-10-nuevos-proyectos/",
        },
        {
            "title": "Emapa: Designan a Sergio Siles como gerente interino（Opinión, 2025-12-09）",
            "url": "https://www.opinion.com.bo/pais/sergio-siles-es-designado-como-gerente-interino-emapa/20251209183413985095.html",
        },
        {
            "title": "Emapa reduce Bs 2.000 millones de su presupuesto y sale del grupo de las 10 empresas estatales más deficitarias（ABI, 2026-09-06）",
            "url": "https://abi.bo/emapa-reduce-bs-2-000-millones-de-su-presupuesto-y-sale-del-grupo-de-las-10-empresas-estatales-mas-deficitarias/",
        },
        {
            "title": "Emapa inicia cierre de sucursales 「no rentables」 y reubica su red comercial（Correo del Sur, 2026-03-17）",
            "url": "https://correodelsur.com/economia/20260317/emapa-inicia-cierre-de-sucursales-no-rentables-y-reubica-su-red-comercial.html",
        },
        {
            "title": "Justicia dicta cinco meses de detención preventiva para Franklin Flores, exgerente de Emapa（El Deber, 2026-01）",
            "url": "https://eldeber.com.bo/pais/justicia-dicta-cinco-meses-detencion-preventiva-franklin-flores-exgerente-emapa_1767469189",
        },
        {
            "title": "Franklin Flores: de dirigente universitario y concejal a exgerente de Emapa investigado por corrupción（Vision360, 2026-02-24）",
            "url": "https://www.vision360.bo/noticias/2026/02/24/40493-franklin-flores-de-dirigente-universitario-y-concejal-a-exgerente-de-emapa-investigado-por-corrupcion",
        },
    ],
}

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Written:", PATH)
print("org_id:", data["org_id"])
print("key_people:", len(data["key_people"]), "| departments:", len(data["departments"]),
      "| recent_events:", len(data["recent_events"]), "| related:", len(data["related_entities"]))

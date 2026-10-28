# -*- coding: utf-8 -*-
"""Phase3 enrichment for BO-NGO-001 (Central Obrera Boliviana). Temp script - safe to delete."""
import json, os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orgs", "BO-NGO-001.json")

with open(PATH, encoding="utf-8") as f:
    data = json.load(f)

# ---------- basic_info ----------
data["basic_info"]["name_original"] = "Central Obrera Boliviana"
data["basic_info"]["name_zh"] = "玻利维亚工人中央工会"
data["basic_info"]["name_en"] = "Bolivian Workers' Center"
data["basic_info"]["aliases"] = ["Central Obrera Boliviana", "COB", "玻利维亚总工会", "玻利维亚工人中心"]
data["basic_info"]["founded_date"] = "1952-04-17"
data["basic_info"]["website"] = "http://cob.org.bo/"
data["basic_info"]["wikidata_qid"] = "Q1053929"

# ---------- social_accounts ----------
data["social_accounts"] = [
    {
        "platform": "facebook",
        "account_name": "COB Central Obrera Boliviana (Oficial)",
        "url": "https://www.facebook.com/CentralObreraBolivianaOficial/",
        "source": "Facebook平台检索；该账号持续发布COB全国扩大会及执行秘书Mario Argollo官方活动信息",
    },
    {
        "platform": "facebook",
        "account_name": "Central Obrera Boliviana",
        "url": "https://www.facebook.com/centralobreraboliviana/",
        "source": "Facebook平台检索；页面自述为聚合各行业劳动者的工人最高组织",
    },
    {
        "platform": "tiktok",
        "account_name": "@cob.bolivia.oficial",
        "url": "https://www.tiktok.com/@cob.bolivia.oficial",
        "source": "TikTok平台检索；账号简介自述'Organización matriz de los trabajadores'（工人最高组织）并发布Mario Argollo活动视频",
    },
]

# ---------- digital_assets ----------
data["digital_assets"] = [
    {
        "name": "COB官方网站",
        "url": "http://cob.org.bo/",
        "description": "注册官方网站（另曾使用cobolivia.com域名），自2022年底起基本停止更新且当前无法访问；COB信息发布已转向Facebook、TikTok等社交媒体。",
        "source": "Wayback Machine（官网最后快照2022-11-30，2015-2022年共36次抓取）",
    },
    {
        "name": "COB官方网站历史快照（Internet Archive）",
        "url": "https://web.archive.org/web/20221130093054/http://cob.org.bo/",
        "description": "互联网档案馆保存的COB官网历史抓取记录，可查询其历史公告与组织结构信息。",
        "source": "web.archive.org",
    },
]

# ---------- key_people ----------
data["key_people"] = [
    {
        "person_id": None,
        "name": "马里奥·阿戈略（Mario Argollo）",
        "title": "执行秘书（Secretario Ejecutivo）",
        "title_description": "COB最高领导人，主持全国执行委员会，统筹罢工动员、与政府谈判及对外表态",
        "description": "2025年10月10日在潘多省科维哈（Cobija）举行的COB第十八次普通代表大会上以79票对41票击败Colquiri矿工代表Joaquín Mamani当选，接替任职近8年的Juan Carlos Huarachi；出身奥鲁罗Huanuni国营矿业公司矿工工会（前矿工领袖）。上任后强调'恢复工会独立性'，2026年领导反对取消燃油补贴（DS 5503）和要求最低工资上调20%的无限期总罢工；其6月19日与政府签署停火协议遭亲莫拉莱斯农民派系斥为'背叛'，当选程序亦被部分基层工会质疑。中文译名另见'阿戈约'（南美侨报网用法）。",
    },
    {
        "person_id": None,
        "name": "Juan Carlos Huarachi",
        "title": "前执行秘书（2018-2025）",
        "title_description": "2018年2月至2025年10月执掌COB，是MAS执政时期COB的主要政治面孔",
        "description": "出身奥鲁罗Huanuni矿工工会；2018年2月25日当选COB执行秘书，虽章程规定任期两年仍任职近八年；任内先后支持Evo Morales、Jeanine Áñez过渡政府及Luis Arce政府。2019年选举危机中曾号召支持莫拉莱斯、后又建议其'必要时辞职'。2025年4月在FSTMB等矿工系统压力下宣布卸任，10月代表大会上其管理报告被否决，正式交权。",
    },
    {
        "person_id": None,
        "name": "Andrés Paye Rodríguez",
        "title": "加盟工会FSTMB执行秘书",
        "title_description": "玻利维亚矿工工会联合会（FSTMB，COB历史最具影响力的加盟联合会）最高负责人",
        "description": "2025年4月上任的FSTMB执行秘书，矿工系统领袖；FSTMB系推动2025年10月COB领导层换届的主要力量。2026年5-6月罢工封锁期间代表矿工参与COB动员与政府复谈（6月19日与会），并多次公开批评政府部长及矿业政策；10月表示矿工暂不参加新一轮动员。",
    },
    {
        "person_id": None,
        "name": "David Quispe Machaca",
        "title": "加盟工会CSUTCB执行秘书（派系争议中）",
        "title_description": "玻利维亚农民统一工会联合会（CSUTCB，COB主要农民加盟组织）最高负责人",
        "description": "2026年7月3日CSUTCB全国扩大会确认其接替被罢免的Víctor Hugo Roca出任执行秘书；立场亲MAS，2026年5-6月参与支持封锁的农民动员，7月17日因冲突相关指控被捕、后获居家监禁。其领导地位面临Feliciano Vegamonte派系（自立执行秘书）挑战，CSUTCB处于分裂状态。",
    },
]

# ---------- departments ----------
data["departments"] = [
    {
        "dept_id": "BO-NGO-001-DEPT-001",
        "name": "玻利维亚矿工工会联合会（Federación Sindical de Trabajadores Mineros de Bolivia, FSTMB）",
        "head": "Andrés Paye Rodríguez",
        "description": "COB历史最悠久、最具战斗性的加盟联合会，代表国营与私营矿区矿工；COB前五任标志性领导人均出身该会（Juan Lechín、Simón Reyes、Víctor López、Edgar Ramírez、Óscar Salas Moya），矿工系统长期主导COB执行秘书职位（Huanuni矿工工会连续产生四任执行秘书）。2025年4月以违反任期章程为由施压Huarachi提前交权，是COB换届的主要推手。",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-NGO-001-DEPT-002",
        "name": "玻利维亚农民统一工会联合会（Confederación Sindical Única de Trabajadores Campesinos de Bolivia, CSUTCB）",
        "head": "David Quispe Machaca（2026年7月全国扩大会确认；Feliciano Vegamonte派系另有自立领导层）",
        "description": "全国农民及原住民（艾马拉、克丘亚、图皮-瓜拉尼等）劳动者的最大工会组织，1979年成立，COB最重要的农民加盟成员；2026年5-6月冲突中与COB同属动员方，7月起陷入Quispe Machaca与Vegamonte两个执行秘书的领导权分裂。",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-NGO-001-DEPT-003",
        "name": "全国原住民农民工妇联合会“巴托利娜·西萨”（Confederación Nacional de Mujeres Campesinas Indígenas Originarias de Bolivia - Bartolina Sisa, CNMCIOB-BS）",
        "head": None,
        "description": "以18世纪艾马拉起义女英雄Bartolina Sisa命名的全国原住民农民工妇组织，COB加盟成员，代表农民工妇在COB及'团结公约'（Pacto de Unidad）框架内的声音。",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-NGO-001-DEPT-004",
        "name": "玻利维亚行会工匠、小商贩劳动者联合会（Confederación de Trabajadores Gremiales, Artesanos, Comerciantes Minoristas y Vivanderos de Bolivia）",
        "head": None,
        "description": "1955年3月15日成立，代表行会工匠、小商贩、摊贩等城市非正规经济部门劳动者，隶属COB（中央全国层级），国际层面关联世界工会联合会。",
        "parent_dept_id": None,
    },
    {
        "dept_id": "BO-NGO-001-DEPT-005",
        "name": "省级工人中央工会网络（Centrales Obreras Departamentales, CODes）",
        "head": None,
        "description": "COB在玻利维亚九个省设立的省级联合工会架构，与区域工人中央（CORes）共同构成地方组织网络；COB共有60余个加盟组织。拉巴斯、奥鲁罗、科恰班巴等省工人中央（COD）是2025年五一封锁和2026年5-6月罢工封锁的主要地方动员力量。",
        "parent_dept_id": None,
    },
]

# ---------- recent_events ----------
data["recent_events"] = [
    {
        "date": "2025-10-10",
        "title": "COB第十八次全国代表大会选举Mario Argollo为新任执行秘书",
        "description": "在潘多省科维哈（Cobija）举行的第十八次普通代表大会闭幕日，Huanuni矿工代表Mario Argollo以79票对41票击败Colquiri矿工代表Joaquín Mamani当选执行秘书，接替任职近八年（章程规定仅两年）的Juan Carlos Huarachi；大会否决Huarachi的管理报告，FSTMB等矿工系统以'恢复工会独立、巩固工人阶级团结'为口号推动换届。",
        "impact": "结束与MAS关系密切的Huarachi时代、矿工系统重掌COB，为2026年COB与帕斯政府的全面对抗奠定领导层基础。",
        "source": "https://correodelsur.com/politica/20251010/mario-argollo-asume-la-secretaria-ejecutiva-de-la-cob-tras-ocho-anos-de-gestion-de-juan-carlos-huarachi.html",
    },
    {
        "date": "2025-12-23",
        "title": "COB强烈反对取消燃油补贴的第5503号最高法令并宣布全国抗议",
        "description": "帕斯政府12月颁布取消燃油补贴的DS 5503（汽油上涨86%至6.96玻利维亚诺/升、柴油上涨163%至9.8玻利维亚诺/升），执行秘书Mario Argollo称法令'武断'、'毁了许多家庭的圣诞节'，宣布在全国开展和平维权抗议，要求政府重新审议并评估社会经济影响。",
        "impact": "拉开COB与帕斯政府公开对抗的序幕；1月初COB动员的封锁蔓延多省。",
        "source": "https://www.br-cn.com/static/content/news/nm_news/2025-12-23/1453115428637285626.html",
    },
    {
        "date": "2026-01-11",
        "title": "COB与政府在埃尔阿尔托签署协议：废止DS 5503但保留取消补贴核心内容",
        "description": "政府与COB及农民组织在埃尔阿尔托签署协议，同意'全面废止'DS 5503并成立委员会重拟综合燃油政策法令（后以DS 5516延续取消补贴与油价调整），同时涉及信贷重组与工资措施；COB随即宣布解除1月初以来的封锁与施压行动。",
        "impact": "取消燃油补贴的政策实质得以延续，COB被基层支持者批评让步；政府-工会进入短暂缓和期（政府并据此于1月上调最低工资20%）。",
        "source": "https://www.noticiasfides.com/nacional/politica/gobierno-y-cob-acuerdan-un-nuevo-decreto-y-mantienen-la-eliminacion-de-la-subvencion-a-los-carburantes",
    },
    {
        "date": "2026-05-01",
        "title": "COB在埃尔阿尔托宣布无限期总罢工，要求最低工资再涨20%",
        "description": "因谈判无果，COB在埃尔阿尔托露天大会宣布自当日起无限期动员式总罢工，核心诉求包括：最低工资上调20%（政府1月已上调20%，COB指通胀侵蚀购买力）、废除针对小商户的税制改革、提高养老金、削减高官薪酬、反对关闭国企、废除改变小农土地制度的第1720号法律、限制粮食出口并稳定汇率；Argollo放话'若政府不理会人民要求就下台'，总统帕斯拒绝并称经济'已被上届政府搞破产'。",
        "impact": "引爆全国54天罢工封锁冲突（高峰期约90-103个封锁点），14人死亡、365人被捕，经济损失估计超27亿美元，拉巴斯出现燃料食品短缺。",
        "source": "https://www.dw.com/es/principal-sindicato-de-bolivia-se-declara-en-paro-indefinido/a-77016291",
    },
    {
        "date": "2026-06-19",
        "title": "COB与政府签署全国和平协议，宣布解除全部封锁",
        "description": "冲突第50天，政府与COB签署'国家和平协议'，商定设立部门工作委员会（mesas sectoriales）并设90天履行期；执行秘书Argollo宣布在全国范围内解除压力措施并呼吁 affiliated 组织回岗。数小时后政府以'打击narco恐怖主义'为由颁布DS 5636宣布全国紧急状态90天（议会两 thirds 批准），禁止道路封锁、限制集会；六联合会等亲莫拉莱斯组织指Argollo'背叛'并拒绝承认COB领导层、短暂继续封锁。",
        "impact": "54天冲突落幕、道路全面恢复通行，但COB与农民激进派系公开分裂，组织权威受损，转入紧急状态压制下的守势。",
        "source": "https://erbol.com.bo/nacional/cob-firma-acuerdo-con-el-gobierno-y-anuncia-que-se-levantan-medidas-de-presi%C3%B3n",
    },
    {
        "date": "2026-09-16",
        "title": "Argollo代表COB公开反对延长全国紧急状态",
        "description": "Argollo公开现身并谴责政府延长紧急状态'不负责任'，称国内局势平静、延长措施缺乏法律依据；同时要求政府停止针对工会领导层的'迫害'。",
        "impact": "COB以法律与舆论手段持续对抗政府安全措施，但避免重启大规模动员。",
        "source": "https://www.noticiasfides.com/nacional/politica/el-dirigente-de-la-cob-argollo-reaparece-y-expresa-su-total-rechazo-a-la-ampliacion-del-estado-de-excepcion",
    },
    {
        "date": "2026-10-15",
        "title": "COB科恰班巴全国扩大会宣布组织进入紧急状态、抵制政府法令",
        "description": "全国扩大会（ampliado nacional）在科恰班巴举行，宣布COB因国家政治经济局势进入'紧急状态'，拒绝政府涉及柴油涨价、基本服务费率上调等'损害最贫困阶层'的法令，要求停止'迫害'工会领导人；Argollo强调运动属'维权性质'而非党派斗争、COB不寻求与政府'共治'，将'从街头和社会组织'发挥反对派作用，但未宣布具体施压措施；大会背书现任领导层并派代表赴九省巩固团结。",
        "impact": "确立COB对帕斯政府的街头反对立场与'阶级独立'路线，为2027年工资谈判（要求补足至12月31日的购买力损失）预设斗争框架；但动员能力较5-6月明显受限。",
        "source": "https://www.lostiempos.com/actualidad/pais/20261016/cob-declara-emergencia-rechaza-decretos-no-apoyara-acciones-politicas",
    },
]

# ---------- related_entities ----------
data["related_entities"] = [
    {
        "org_id": "BO-GOV-010",
        "org_name": "Ministry of Work, Employment, and Social Security (Ministerio de Trabajo, Empleo y Previsión Social)",
        "org_type": "GOV",
        "org_description": "玻利维亚劳动、就业与社会保障部：工会登记与劳工监管主管部门，COB在最低工资、养老金与劳动立法议题上的核心政府对话部门。",
        "relationship_type": "regulated_by",
    },
    {
        "org_id": "BO-GOV-001",
        "org_name": "President of Bolivia (Presidencia del Estado Plurinacional de Bolivia)",
        "org_type": "GOV",
        "org_description": "罗德里戈·帕斯（Rodrigo Paz，2025年11月就职）领导的中右翼政府：2025年12月颁布取消燃油补贴的DS 5503、2026年6月宣布全国紧急状态，均为COB激烈反对的对象；2026年1月11日与6月19日两次与COB签署缓和协议。",
        "relationship_type": "partner",
    },
    {
        "org_id": "BO-PARTY-001",
        "org_name": "Movimiento al Socialismo (MAS)",
        "org_type": "PARTY",
        "org_description": "争取社会主义运动党：2006-2019年Evo Morales执政期间COB最重要的政治盟友，Huarachi时代（2018-2025）延续结盟；2019年选举危机中COB一度要求莫拉莱斯辞职，2025年Argollo上任后重申'阶级政治独立'、与政党划清界限，但COB内亲MAS派系（农民联合会、六联合会）仍势力强大。",
        "relationship_type": "affiliated",
    },
    {
        "org_id": "BO-NGO-002",
        "org_name": "Confederación de Empresarios Privados de Bolivia (CEPB)",
        "org_type": "NGO",
        "org_description": "玻利维亚私营企业家联合会：雇主方最高代表机构，与COB分别构成玻利维亚社会劳资对话中的劳工方与资方两端。",
        "relationship_type": "partner",
    },
    {
        "org_id": None,
        "org_name": "Federación Sindical Mundial (WFTU, 世界工会联合会)",
        "org_type": "NGO",
        "org_description": "世界工会联合会：COB的国际工会隶属组织，COB对外工会合作主要通过该框架开展。",
        "relationship_type": "member_of",
    },
]

# ---------- core_business ----------
data["core_business"] = (
    "玻利维亚工人中央工会（COB）是玻利维亚全国性的总工会联合组织，1952年4月17日全国革命胜利后成立，"
    "总部设于拉巴斯，代表约200万各行业劳动者，下辖60余个加盟组织，按'行业工会-省级联合会-全国联合会'的"
    "层级整合矿工、农民、工厂工人、教师、建筑、银行、行会小贩等行业联合会及九省工人中央（COD）。其核心职能包括："
    "代表工人与政府和雇主方（CEPB）进行集体谈判与社会对话；组织总罢工、游行、道路封锁等施压行动；就最低工资、"
    "养老金与社保改革、燃油及基本物资价格、劳动立法等议题向政府提交诉求清单并游说立法；协调各加盟工会的联合行动。"
    "COB历史上推动了矿山与天然气国有化诉求、2005年梅萨总统辞职、2010年养老金改革、2011年全国大罢工等重大事件，"
    "长期是玻利维亚政治中最具街头动员力的社会力量；2018-2025年Huarachi领导时期与MAS政府关系密切，2025年10月"
    "换届后重申工会独立，2026年因政府取消燃油补贴、最低工资争议发起大规模罢工封锁并遭紧急状态压制。COB为世界"
    "工会联合会（WFTU）成员，意识形态以工团主义为主，历史上融合卡塔里主义与原住民主义思潮。"
)

# ---------- apec_stance ----------
data["apec_stance"] = (
    "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入），COB作为玻利维亚国内工会联合组织"
    "从未就APEC合作进程发表过官方立场。其对外交往集中于拉美区域（世界工会联合会WFTU框架及地区工会联络），"
    "与亚太经合组织事务无直接关联。"
)

# ---------- profile ----------
data["profile"] = {
    "source_url": "https://es.wikipedia.org/wiki/Central_Obrera_Boliviana",
    "local_path": None,
}

# ---------- collection_meta ----------
data["collection_meta"] = {
    "collection_date": "2026-10-25",
    "phase": "phase3_enriched",
    "data_sources": [
        "wikidata",
        "wikipedia_es",
        "wayback_machine",
        "facebook",
        "tiktok",
        "correodelsur.com",
        "instantaneas.org.bo",
        "dw.com",
        "noticiasfides.com",
        "erbol.com.bo",
        "lostiempos.com",
        "br-cn.com (南美侨报网)",
        "larazon.bo",
        "eju.tv",
    ],
    "quotes": [
        {
            "title": "Mario Argollo asume la Secretaría Ejecutiva de la COB tras ocho años de gestión de Juan Carlos Huarachi — Correo del Sur (2025-10-10)",
            "url": "https://correodelsur.com/politica/20251010/mario-argollo-asume-la-secretaria-ejecutiva-de-la-cob-tras-ocho-anos-de-gestion-de-juan-carlos-huarachi.html",
        },
        {
            "title": "Principal sindicato de Bolivia se declara en paro indefinido — DW (2026-05-02)",
            "url": "https://www.dw.com/es/principal-sindicato-de-bolivia-se-declara-en-paro-indefinido/a-77016291",
        },
        {
            "title": "Gobierno y COB acuerdan un nuevo decreto y mantienen la eliminación de la subvención a los carburantes — Noticias Fides (2026-01-11)",
            "url": "https://www.noticiasfides.com/nacional/politica/gobierno-y-cob-acuerdan-un-nuevo-decreto-y-mantienen-la-eliminacion-de-la-subvencion-a-los-carburantes",
        },
        {
            "title": "COB firma acuerdo con el Gobierno y anuncia que se levantan medidas de presión — ERBOL (2026-06-19)",
            "url": "https://erbol.com.bo/nacional/cob-firma-acuerdo-con-el-gobierno-y-anuncia-que-se-levantan-medidas-de-presi%C3%B3n",
        },
        {
            "title": "La COB declara emergencia y rechaza decretos; no apoyará acciones políticas — Los Tiempos (2026-10-16)",
            "url": "https://www.lostiempos.com/actualidad/pais/20261016/cob-declara-emergencia-rechaza-decretos-no-apoyara-acciones-politicas",
        },
        {
            "title": "争议声中 玻利维亚新法令艰难推行 — 南美侨报网 (2025-12-23)",
            "url": "https://www.br-cn.com/static/content/news/nm_news/2025-12-23/1453115428637285626.html",
        },
    ],
    "completeness_score": 0,
    "notes": "Phase3 enrichment (2026-10): leadership verified via Bolivian press (XVIII Congress, Cobija, 2025-10-10) and cross-checked with ES Wikipedia; 2026 strike cycle (fuel subsidy DS 5503, indefinite general strike, June 19 accord, state of exception, Oct 15 ampliado) sourced from DW/Fides/ERBOL/Los Tiempos/infobae. Official website defunct since ~2022 (Wayback last capture 2022-11-30); COB communicates via Facebook/TikTok. Caveats: Argollo's election legitimacy contested by some grassroots sectors; CSUTCB leadership disputed (Quispe Machaca vs Vegamonte). key_people person_id null (no entries in _name_index.json).",
}

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("WROTE", PATH)
print("key_people:", len(data["key_people"]), "| events:", len(data["recent_events"]),
      "| social:", len(data["social_accounts"]), "| depts:", len(data["departments"]),
      "| related:", len(data["related_entities"]), "| digital:", len(data["digital_assets"]))

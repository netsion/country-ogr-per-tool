# -*- coding: utf-8 -*-
"""Enrich BO-MEDIA-012 (Bolivia TV) org profile — phase3_enriched."""
import json

path = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/orgs/BO-MEDIA-012.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

# ---------- basic_info ----------
data["basic_info"]["website"] = "https://www.boliviatv.bo"
data["basic_info"]["founded_date"] = "1969-08-30"  # first official broadcast of Televisión Boliviana (Canal 7), per es.wikipedia
data["basic_info"]["aliases"] = ["Canal 7", "BTv", "Bolivia Televisión"]

# ---------- social_accounts ----------
data["social_accounts"] = [
    {"platform": "facebook", "account_name": "BTVCanalOficial", "url": "https://www.facebook.com/BTVCanalOficial", "source": "official_website_footer"},
    {"platform": "twitter_x", "account_name": "Canal_BoliviaTV", "url": "https://twitter.com/Canal_BoliviaTV", "source": "official_website_footer"},
    {"platform": "instagram", "account_name": "boliviatv_oficial", "url": "https://www.instagram.com/boliviatv_oficial/", "source": "official_website_footer"},
    {"platform": "youtube", "account_name": "Bolivia TV", "url": "https://www.youtube.com/channel/UCKadCx-t_VmwzfWczlWE98w", "source": "official_website_footer"},
    {"platform": "tiktok", "account_name": "boliviatv", "url": "https://www.tiktok.com/@boliviatv", "source": "official_website_footer"},
    {"platform": "other", "account_name": "Bolivia TV WhatsApp Channel", "url": "https://whatsapp.com/channel/0029Vb7c7J3HLHQPe45t5a3a", "source": "official_website_footer"},
]

# ---------- digital_assets ----------
data["digital_assets"] = [
    {"name": "Bolivia TV 官方网站", "url": "https://www.boliviatv.bo", "description": "官方网站，发布新闻稿件、栏目信息、领导名录与联系方式，并提供两路网络直播入口", "source": "official_website"},
    {"name": "Bolivia TV en vivo 7.1", "url": "https://www.boliviatv.bo/vivo71.php", "description": "7.1主频道（高清）24小时网络直播页面", "source": "official_website"},
    {"name": "Bolivia TV en vivo 7.2", "url": "https://www.boliviatv.bo/vivo72.php", "description": "7.2第二信号（原体育取向，现为综合内容）网络直播页面", "source": "official_website"},
    {"name": "Bolivia TV YouTube 官方频道", "url": "https://www.youtube.com/channel/UCKadCx-t_VmwzfWczlWE98w", "description": "官方YouTube频道，提供新闻与栏目直播及点播", "source": "official_website_footer"},
]

# ---------- key_people ----------
data["key_people"] = [
    {"person_id": None, "name": "Luis Carlos Villazón Martínez（Carlos Villazón）", "title": "Gerente General（总经理）",
     "title_description": "Bolivia TV最高负责人，主持全台台务；依据创立法令及2026年最高法令5566号由总统最高决议任命",
     "description": "记者出身的媒体管理者，2026年1月7日帕斯新政府上台后获任命出任总经理，接掌国家电视台；官方Facebook及多家媒体当日报道其就任。据其公开资料，此前曾任职于私营电视台Red ATB。"},
    {"person_id": None, "name": "Álvaro Irusta Bernal", "title": "Gerente de Informaciones（新闻信息部总经理）",
     "title_description": "主管全台新闻采编与播报体系",
     "description": "官网现任领导名录列名，负责新闻信息条线，下辖国家新闻总监与多媒体岗位。"},
    {"person_id": None, "name": "Eddy Ariel Peñaloza Rada", "title": "Director Nacional de Noticias（国家新闻总监）",
     "title_description": "负责全国新闻内容的统筹编排",
     "description": "官网现任领导名录列名，隶属新闻信息部，统筹全国新闻编排。"},
    {"person_id": None, "name": "Leticia Azeñas Soria Galvarro", "title": "Gerente de Producción（制作部总经理）",
     "title_description": "主管节目制作、体育与创意内容",
     "description": "官网现任领导名录列名，负责制作条线，下辖体育与创意、节目制作与运营岗位。"},
    {"person_id": None, "name": "Rafael Martín Porcel De La Barra", "title": "Gerente Administrativo y Financiero（行政与财务总经理）",
     "title_description": "主管行政、财务、人力资源与采购",
     "description": "官网现任领导名录列名，负责行政财务条线。"},
    {"person_id": None, "name": "Grace Caterine Del Castillo Aiaga", "title": "Gerente Técnico a.i.（技术部代总经理）",
     "title_description": "主管技术传输与工程保障（代理）",
     "description": "官网现任领导名录列名，以代理身份主持技术部工作。"},
    {"person_id": None, "name": "Erika Lizet Arteaga Miranda", "title": "Gerente de Marketing y Ventas（市场营销与销售总经理）",
     "title_description": "主管广告销售与商业合作",
     "description": "官网现任领导名录列名，负责市场营销条线。"},
    {"person_id": None, "name": "Reynaldo Vega Gareca", "title": "Director de Programación y Promoción（节目与推广总监）",
     "title_description": "主管节目编排与频道推广",
     "description": "官网现任领导名录列名，隶属总经理办公室条线。"},
    {"person_id": None, "name": "Ricardo Armando Molina Cadima", "title": "Director Jurídico Nacional（国家法律主任）",
     "title_description": "主管全台法律事务",
     "description": "官网现任领导名录列名，负责法律事务条线。"},
]

# ---------- departments ----------
data["departments"] = [
    {"name": "Gerencia General（总经理办公室）", "dept_id": None, "head": "Luis Carlos Villazón Martínez",
     "description": "全台中枢，统筹战略管理与对外代表；下设国家法律主任、节目与推广主任、规划与项目主管、内部审计主管及总协调人等职能岗位", "parent_dept_id": None},
    {"name": "Gerencia de Informaciones（新闻信息部）", "dept_id": None, "head": "Álvaro Irusta Bernal",
     "description": "负责新闻采编、播报与多媒体内容，下设国家新闻总监岗位", "parent_dept_id": None},
    {"name": "Gerencia de Producción（制作部）", "dept_id": None, "head": "Leticia Azeñas Soria Galvarro",
     "description": "负责节目制作与运营，下设体育与创意主管、制作主管、运营主管岗位", "parent_dept_id": None},
    {"name": "Gerencia Técnica（技术部）", "dept_id": None, "head": "Grace Caterine Del Castillo Aiaga（代理）",
     "description": "负责信号传输、播控设备与工程技术保障", "parent_dept_id": None},
    {"name": "Gerencia Administrativa Financiera（行政财务部）", "dept_id": None, "head": "Rafael Martín Porcel De La Barra",
     "description": "负责行政、财务、人力资源、采购合同与一站式服务窗口", "parent_dept_id": None},
    {"name": "Gerencia de Marketing（市场营销与销售部）", "dept_id": None, "head": "Erika Lizet Arteaga Miranda",
     "description": "负责广告销售、商业合作与商业编辑", "parent_dept_id": None},
]

# ---------- recent_events ----------
data["recent_events"] = [
    {"date": "2025-11-08", "title": "罗德里戈·帕斯就任总统，国家媒体整体转归新政府管理",
     "description": "2025年10月总统选举第二轮投票中罗德里戈·帕斯（Rodrigo Paz Pereira）胜出，11月8日宣誓就职，终结争取社会主义运动（MAS）自2006年以来对国家媒体体系的长期主导；Bolivia TV作为国家电视旗舰随之转由新政府主导，管理层面临整体更替。",
     "impact": "编辑方针与人事随执政当局更替调整；国家媒体从MAS时代的宣传定位进入政策转向期。",
     "source": "https://statemediamonitor.com/bolivia/"},
    {"date": "2026-01-07", "title": "卡洛斯·比亚松出任Bolivia TV总经理",
     "description": "新政府任命媒体从业者卡洛斯·比亚松（Luis Carlos Villazón Martínez）为Bolivia TV总经理，官方账号及多家媒体当日发布其就任消息，称其将强化频道管理；官网现任领导名录与其就任后信息一致。",
     "impact": "新政府完成国家电视台管理层换血，为随后的节目与形象更新铺路。",
     "source": "https://x.com/popularbolivia/status/2008957917639401905"},
    {"date": "2026-03-02", "title": "最高法令5566号改组国家传播体系，Bolivia TV人事权上收总统层级",
     "description": "帕斯政府颁布最高法令5566号，创设直属总统府部的'多民族国战略传播局'（Unidad de Comunicación Estratégica），将ABI、Red Patria Nueva、报纸《Ahora El Pueblo》及原住民电台网RPO纳入其管理；Bolivia TV在同一法令中单独处理：重新界定其由六位部长组成的董事会，并将总经理任命方式改为总统最高决议任命。",
     "impact": "行政对国家媒体的控制进一步集中化；Bolivia TV最高人事权上收至总统层级，编辑独立保障仍然缺失。",
     "source": "https://www.vision360.bo/noticias/2026/03/04/40920-gobierno-de-paz-crea-una-unidad-estrategica-para-centralizar-la-politica-comunicacional-del-ejecutivo-tiene-22-funciones"},
    {"date": "2026-08-30", "title": "Bolivia TV迎来开播57周年，管理层强调全国公共电视定位与更新转型",
     "description": "总经理卡洛斯·比亚松在57周年致辞中回顾频道自1969年8月30日开播以来的历程，强调其向全国各地区输送信息、文化、娱乐与地方故事的公共职能，并提出频道更新（renovación）方向；国家通讯社ABI亦刊发专题报道。",
     "impact": "强化公共电视品牌叙事，为10月节目改版与台庆后的'新阶段'造势。",
     "source": "https://abi.bo/bolivia-tv-cumple-57-anos-de-historia-llevando-informacion-y-entretenimiento-a-las-familias-bolivianas/"},
    {"date": "2026-10-08", "title": "举办'Screening 2026'节目推介会，宣布开启节目编排新阶段",
     "description": "Bolivia TV在拉巴斯举办'Screening 2026'推介会，邀请政府官员、企业界与特邀嘉宾，通过互动视频、频道历史回顾等方式发布年度主要新栏目，官方称频道将开启'传播提案的新阶段'；另据当地媒体2026年7-10月披露，政府约3000万玻利维亚诺的国家广告预算中约一半（约1500万诺）投向Bolivia TV，引发对国家媒体资金依赖与收视偏低的批评讨论。",
     "impact": "政府更替后频道内容与品牌现代化的标志性动作；高额国家广告集中投放亦凸显其财政依附性与舆论争议。",
     "source": "https://www.youtube.com/watch?v=s7Msi5I7K1U"},
]

# ---------- related_entities ----------
data["related_entities"] = [
    {"org_id": "BO-GOV-006", "org_name": "玻利维亚总统府部（Ministerio de la Presidencia）", "org_type": "GOV",
     "org_description": "Bolivia TV的主管部会：依据创立法令第0078号（2009年），董事会由总统府部、发展规划部、经济与公共财政部、公共工程服务与住房部、教育部、文化部六位部长组成，总统府部部长任主席；总经理原由部长决议任命，2026年最高法令5566号后改为总统最高决议任命。",
     "relationship_type": "parent_org"},
    {"org_id": "BO-GOV-032", "org_name": "玻利维亚电信与交通运输监管审计局（ATT）", "org_type": "GOV",
     "org_description": "玻利维亚电信与交通运输监管机构，对包括Bolivia TV在内的广播电视频率、信号传输与电信事务实施监管。",
     "relationship_type": "regulator"},
    {"org_id": "BO-MEDIA-017", "org_name": "玻利维亚国家通讯社（Agencia Boliviana de Información, ABI）", "org_type": "MEDIA",
     "org_description": "国家通讯社，与Bolivia TV同属国家媒体体系；2025年11月政府改组期间曾短期停运，2026年恢复运作并被纳入国家战略传播局管理。",
     "relationship_type": "sibling"},
    {"org_id": "BO-MEDIA-016", "org_name": "祖国新电台网（Red Patria Nueva – Radio Illimani）", "org_type": "MEDIA",
     "org_description": "国家广播电台网，与Bolivia TV同属国家媒体体系，2026年3月最高法令5566号后被纳入国家战略传播局管理。",
     "relationship_type": "sibling"},
    {"org_id": None, "org_name": "玻利维亚国家电视公司（Empresa Nacional de Televisión Boliviana, ENTB）", "org_type": "MEDIA",
     "org_description": "Bolivia TV的法律前身：1968年6月19日依最高法令8395号设立，因巨额债务于2009年4月15日经最高法令0074号宣告破产清算，资产与约200名员工转入新组建的国家电视公司EET-Bolivia TV。",
     "relationship_type": "predecessor"},
]

# ---------- core_business ----------
data["core_business"] = (
    "Bolivia TV（玻利维亚电视台）是玻利维亚的全国性公共电视台，由国有公共企业'国家电视公司'（Empresa Estatal de Televisión, EET）运营，"
    "2009年4月15日依据最高法令0078号在清算原国家电视公司ENTB的基础上组建，隶属总统府部管理，历史可追溯至1969年8月30日正式开播的'玻利维亚电视'（Canal 7）。"
    "频道实行以新闻、教育、文化、体育和娱乐为主的综合编排，通过72座地面发射机、276座转播台和11个地方制作点实现全国覆盖，并以卫星、数字地面电视（7.1高清主信号、7.2副信号）、"
    "有线电视及官网网络直播（vivo 7.1/7.2）向境内外传输，24小时播出。经费高度依赖国家：2026年机构预算约9000万玻利维亚诺，2024年预算约7840万诺（执行约5720万诺），"
    "收入主要来自政府广告与财政拨款（2021年国家资金占比约92%）；据当地媒体2026年报道，政府约3000万诺国家广告预算中约一半投向该台。频道缺乏编辑独立的制度保障，"
    "学术研究、欧盟观察团与媒体监测机构均指出其报道倾向随执政政府更替，属典型的政府控制型国家媒体。"
)

# ---------- apec_stance ----------
data["apec_stance"] = "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。"

# ---------- collection_meta ----------
meta = data.get("collection_meta", {})
meta["phase"] = "phase3_enriched"
meta["collection_date"] = "2026-10-24"
meta["data_sources"] = [
    "wikipedia_es",
    "official_website",
    "state_media_monitor",
    "abi.bo",
    "vision360.bo",
    "x.com_popularbolivia",
    "facebook.com_BTVCanalOficial",
    "youtube.com",
]
meta["quotes"] = [
    {"title": "Bolivia TV (Empresa Estatal de Televisión) — State Media Monitor", "url": "https://statemediamonitor.com/2026/07/bolivia-tv-empresa-estatal-de-television/"},
    {"title": "Bolivia Televisión — Wikipedia (español)", "url": "https://es.wikipedia.org/wiki/Bolivia_Televisi%C3%B3n"},
    {"title": "Gobierno de Paz crea una unidad estratégica para centralizar la política comunicacional del Ejecutivo — Vision360", "url": "https://www.vision360.bo/noticias/2026/03/04/40920-gobierno-de-paz-crea-una-unidad-estrategica-para-centralizar-la-politica-comunicacional-del-ejecutivo-tiene-22-funciones"},
    {"title": "Bolivia TV cumple 57 años de historia — ABI", "url": "https://abi.bo/bolivia-tv-cumple-57-anos-de-historia-llevando-informacion-y-entretenimiento-a-las-familias-bolivianas/"},
    {"title": "Contactos — Bolivia TV（官网现任领导名录）", "url": "https://www.boliviatv.bo/principal/contactos.php"},
]
meta["notes"] = "Phase3 enrichment: leadership (GM Carlos Villazón since 2026-01-07), six gerencias from official contacts page, post-Nov-2025 government transition events (DS 5566 of 2026-03-02), verified social accounts from official footer. key_people person_id null: no registry matches in _name_index."
data["collection_meta"] = meta

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("written:", path)

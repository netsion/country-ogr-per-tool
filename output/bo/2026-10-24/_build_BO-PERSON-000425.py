# -*- coding: utf-8 -*-
"""Build BO-PERSON-000425 Giovanni Ortuño Camacho (CEPB 主席) person profile."""
import json, os, re

OUT = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons\BO-PERSON-000425.json"

data = {
    "person_id": "BO-PERSON-000425",
    "wikidata_qid": None,
    "name_zh": None,
    "name": "Giovanni Ortuño Camacho",
    "name_en": "Giovanni Ortuno Camacho",
    "aliases": ["Giovanni Ortuno Camacho", "Giovanni Ortuño"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": "Potosí",
    "birth_date_note": "公开资料未披露其出生日期（infodiez、Unitel、Los Tiempos等人物报道均未提及年龄或生日）。",
    "birth_place_note": "infodiez（2023-03-13）与CADECOCruz报道均称其生于波托西（Potosí）。长期生活地报道不一：infodiez称主要旅居科恰班巴与拉巴斯，另有来源称主要定居圣克鲁斯，未确证。",
    "current_positions": [
        "玻利维亚私营企业家联合会主席",
        "玻利维亚AXS公司执行总裁兼首席执行官"
    ],
    "work_experience": [
        {
            "start_date": "2023-03",
            "end_date": None,
            "organization": "玻利维亚私营企业家联合会 (Confederación de Empresarios Privados de Bolivia)",
            "org_id": "BO-NGO-002",
            "position": "主席",
            "description": "2023年3月作为单一候选名单当选（获24个有投票权成员团体中14个提名），接替路易斯·巴贝里（Luis Barbery），成为玻利维亚私营部门最高行业组织领导人；2025年3月12日获各成员团体全票连任第二任期（2025-2027）。第一任期内推动与阿尔塞政府的公私对话（2024年8月17点协议、后续14项最高法令），第二任期内主导与帕斯政府的经济政策对话并召集2026年6月全国企业家特别峰会。",
            "is_current": "true",
            "start_date_note": "2023年3月15日CEPB普通大会选举（Los Tiempos预告），2023年3月16日Los Tiempos报道其正式就任。",
            "source": "https://www.cepb.org.bo/notas-de-prensa/giovanni-ortuno-es-elegido-por-unanimidad-como-presidente-de-la-confederacion-de-empresarios-privados-de-bolivia-por-una-segunda-gestion"
        },
        {
            "start_date": "2019",
            "end_date": "2023-03",
            "organization": "玻利维亚私营企业家联合会 (Confederación de Empresarios Privados de Bolivia)",
            "org_id": "BO-NGO-002",
            "position": "第一副主席",
            "description": "在巴贝里任主席期间（2019-2023）担任CEPB第一副主席；此前还曾任CEPB经济与税务委员会主席。",
            "start_date_note": "La Razón存档称其当选主席前任副主席「四年」，2020年CEPB年报列其为第一副主席，起始年份按此推算。",
            "source": "https://www.infodiez.com/giovanni-ortuno-camacho-seria-el-nuevo-presidente-de-la-confederacion-de-empresarios-privados-de-bolivia"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "AXS玻利维亚公司 (AXS Bolivia)",
            "org_id": None,
            "position": "执行总裁兼首席执行官",
            "description": "长期执掌这家电子收款、电子开票与支付服务企业；2025年8月该公司迎来创立25周年时，其仍以执行总裁兼CEO身份接受Cosas Bolivia专访，任该职与任CEPB主席并行。",
            "is_current": "true",
            "source": "https://www.infodiez.com/giovanni-ortuno-camacho-seria-el-nuevo-presidente-de-la-confederacion-de-empresarios-privados-de-bolivia"
        },
        {
            "start_date": "2009",
            "end_date": None,
            "organization": "玻利维亚电信商会 (Cámara de Telecomunicaciones de Bolivia)",
            "org_id": None,
            "position": "理事会成员",
            "description": "截至2023年3月已在该商会领导层任职14年（infodiez、Unitel报道）。",
            "start_date_note": "按2023年3月「已任职14年」的报道推算约自2009年起；卸任时间未披露。",
            "source": "https://www.lostiempos.com/actualidad/pais/20230316/giovanni-ortuno-asume-presidencia-cepb"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "安第斯企业家理事会 (Consejo Empresarial Andino)",
            "org_id": None,
            "position": "主席",
            "description": "据CEPB官方新闻稿（2025-03-12），其曾担任安第斯地区企业家组织——安第斯企业家理事会主席；任期未披露。",
            "source": "https://www.cepb.org.bo/notas-de-prensa/giovanni-ortuno-es-elegido-por-unanimidad-como-presidente-de-la-confederacion-de-empresarios-privados-de-bolivia-por-una-segunda-gestion"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚私营企业家联合会经济与税务委员会 (Comisión de Economía y Tributaria de la CEPB)",
            "org_id": "BO-NGO-002",
            "position": "主席",
            "description": "进入CEPB执委会前曾任该委员会主席（Unitel、Los Tiempos人物报道）。",
            "source": "https://www.lostiempos.com/actualidad/pais/20230316/giovanni-ortuno-asume-presidencia-cepb"
        }
    ],
    "education": [
        {
            "institution": "蒙特雷科技大学 (Tecnológico de Monterrey)",
            "degree": "bachelor",
            "field": "电子与电信工程",
            "country": "MX",
            "start_date": None,
            "end_date": None,
            "note": "院校信息来自其LinkedIn档案的第三方抓取数据（AeroLeads）及Magazine Management《Perspectivas 2026》，权威性一般；起止年份未披露。",
            "source": "https://aeroleads.com/in/giovanni-ortuno-bb7648103"
        }
    ],
    "education_note": "另据报道拥有行政法硕士（Maestría en Derecho Administrativo）与工商管理硕士（Maestría en Administración de Empresas）学历（AeroLeads抓取其LinkedIn档案），就读院校未披露，故不单列条目。",
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000432",
            "person_name": "路易斯·费尔南多·巴贝里·帕斯 (Luis Fernando Barbery Paz)",
            "relationship_type": "associate",
            "description": "CEPB前主席（2019-2023）。奥图尼奥在其任期内任第一副主席，2023年3月接替其出任CEPB主席。",
            "source": "https://www.infodiez.com/giovanni-ortuno-camacho-seria-el-nuevo-presidente-de-la-confederacion-de-empresarios-privados-de-bolivia"
        },
        {
            "person_id": "BO-PERSON-000484",
            "person_name": "路易斯·阿尔塞 (Luis Arce)",
            "relationship_type": "associate",
            "description": "玻利维亚前总统（2020-2025）。奥图尼奥第一任期内与阿尔塞政府建立公私对话机制，2024年8月双方签署17点经济协议，政府随后以最高法令落实。",
            "source": "https://www.opinion.com.bo/pais/gobierno-empresarios-privados-establecen-17-acuerdos-descarta-control-divisas/20240817084514953273.html"
        },
        {
            "person_id": "BO-PERSON-000001",
            "person_name": "罗德里戈·帕斯·佩雷拉 (Rodrigo Paz Pereira)",
            "relationship_type": "associate",
            "description": "玻利维亚现任总统（2025年11月就任）。CEPB多次公开请求与帕斯紧急会晤并递交全国经济复苏方案；奥图尼奥主张经济措施须与私营部门协商，被视为与亲商的帕斯政府互动密切的资方领袖。",
            "source": "https://eldeber.com.bo/economia/empresarios-piden-reunion-urgente-rodrigo-paz-reactivar-economia_1782844719"
        },
        {
            "person_id": "BO-PERSON-000421",
            "person_name": "马里奥·阿戈略·马马尼 (Mario Argollo Mamani)",
            "relationship_type": "associate",
            "description": "玻利维亚工人中央工会（COB）执行秘书，玻利维亚劳方最高代表；与代表资方的奥图尼奥构成劳资博弈两端。2026年COB多轮全国道路封锁期间，奥图尼奥领导的CEPB在企业家峰会上谴责「封锁已成为常见做法」并要求政府保障通行。",
            "source": "https://eldeber.com.bo/economia/empresarios-piden-reunion-urgente-rodrigo-paz-reactivar-economia_1782844719"
        },
        {
            "person_id": "BO-PERSON-000428",
            "person_name": "马塞洛·埃斯科瓦尔·弗洛雷斯 (Marcelo Escobar Flores)",
            "relationship_type": "colleague",
            "description": "2023年3月与奥图尼奥同期入选CEPB执行委员会的成员。",
            "source": "https://www.infodiez.com/giovanni-ortuno-camacho-seria-el-nuevo-presidente-de-la-confederacion-de-empresarios-privados-de-bolivia"
        },
        {
            "person_id": "BO-PERSON-000427",
            "person_name": "路易斯·巴勃罗·格拉尼耶·卡斯特利亚诺斯 (Luis Pablo Granier Castellanos)",
            "relationship_type": "colleague",
            "description": "2023年3月与奥图尼奥同期入选CEPB执行委员会的成员（全国商会代表）。",
            "source": "https://www.infodiez.com/giovanni-ortuno-camacho-seria-el-nuevo-presidente-de-la-confederacion-de-empresarios-privados-de-bolivia"
        }
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Giovanni Ortuno",
            "url": "https://bo.linkedin.com/in/giovanni-ortuno-bb7648103",
            "source": "LinkedIn（bo.linkedin.com）检索结果摘要，显示其为AXS Bolivia执行总裁兼CEPB主席"
        }
    ],
    "social_accounts_note": "六平台扫描结果：LinkedIn可核实（上述条目）；X(Twitter)/TikTok/YouTube未发现本人账号；Instagram @ortunogiovanni（116粉丝）及哥斯达黎加Facebook用户geovanni.ortuno.1身份无法核实归属，不予录入；Facebook上的相关内容均为CEPB机构账号（CEPB.Bolivia）及媒体报道，非本人个人账号。",
    "family_members": [],
    "family_note": "无可靠公开资料披露其家庭成员；西语媒体人物报道仅涉其职业经历，未提及配偶或子女。",
    "political_stances": [
        {
            "date": "2025-03-12",
            "topic": "2025年大选立场",
            "stance_content": "宣布CEPB在2025年大选中不支持、不反对、不与任何总统候选人结盟，保持机构独立；并批评政治体系无效——共和国历史上从未同时出现如此多的总统候选人，却无一有效回应国家危机。",
            "source": "https://www.cepb.org.bo/notas-de-prensa/giovanni-ortuno-es-elegido-por-unanimidad-como-presidente-de-la-confederacion-de-empresarios-privados-de-bolivia-por-una-segunda-gestion"
        },
        {
            "date": "2024-08-30",
            "topic": "公私对话与17点协议",
            "stance_content": "肯定阿尔塞政府为落实17点经济协议采取的首批措施（两份最高法令，含开放私营部门参与生物柴油生产的DS 5197），称签署以来CEPB与政府保持协调会议，将继续推动外汇获取等议题的落实。",
            "source": "https://www.cepb.org.bo/notas-de-prensa/empresarios-califican-como-positivas-las-primeras-medidas-para-cumplir-el-acuerdo-de-los-17-puntos"
        },
        {
            "date": "2026-01-23",
            "topic": "最低工资法规",
            "stance_content": "就第5516号最高法令（最低工资定为3,300玻利维亚诺、承认劳资工资谈判）致函劳动部长，要求紧急会晤并制定实施细则，主张雇主与雇员间工资谈判自主；警告更高用工义务可能导致企业倒闭与正式就业流失。",
            "source": "https://www.cepb.org.bo/notas-de-prensa/cepb-pide-reunion-urgente-con-ministro-de-trabajo-para-tratar-aumento-y-negociacion-salarial"
        },
        {
            "date": "2026-01",
            "topic": "工资涨幅",
            "stance_content": "反对政府与工会方面商定的加薪幅度（CEPB通稿及媒体报道约为7%），称在危机时刻这是「过度且轻率的加薪」(un aumento salarial excesivo e imprudente)，警告即使低于劳方要求的涨幅也会对整体经济产生负面乘数效应，要求纳入三方协商。",
            "source": "https://www.facebook.com/100067642324503/posts/1204692521795481"
        },
        {
            "date": "2026-06-28",
            "topic": "经济危机应对",
            "stance_content": "在科恰班巴召集全国企业家特别峰会，提出全国紧急计划、全国政治协议与将国家-私营部门对话制度化等主张，强调紧急计划须涵盖所有部门和地区，并要求与帕斯总统紧急会晤递交方案。",
            "source": "https://www.noticiasfides.com/economia/confederacion-de-empresarios-convoca-a-una-cumbre-para-discutir-un-plan-frente-a-la-crisis-economica"
        },
        {
            "date": "2026-06-30",
            "topic": "道路封锁",
            "stance_content": "谴责道路封锁「已成为一种常见做法」，要求政府采取切实行动保障通行与物流；称经济复苏需要时间、恒心与各方意愿，「将创造就业与发展的人排除在经济辩论之外是不合理的」。",
            "source": "https://eldeber.com.bo/economia/empresarios-piden-reunion-urgente-rodrigo-paz-reactivar-economia_1782844719"
        }
    ],
    "major_achievements": [
        {
            "date": "2023-03",
            "achievement": "作为单一候选名单当选CEPB主席（获24个有投票权成员团体中14个提名），接替路易斯·巴贝里，成为玻利维亚私营部门最高行业组织领导人。",
            "organization": "玻利维亚私营企业家联合会 (Confederación de Empresarios Privados de Bolivia)"
        },
        {
            "date": "2024-08-16",
            "achievement": "第一任期内推动与阿尔塞政府的公私对话，促成政府与CEPB签署17点经济协议（明确不实施外汇管制等）；政府随后于8月28日颁布两份最高法令落实协议，任内累计推动14项最高法令颁布。",
            "organization": "玻利维亚私营企业家联合会 (Confederación de Empresarios Privados de Bolivia)"
        },
        {
            "date": "2025-03-12",
            "achievement": "获CEPB各成员团体全票连任主席，开启第二任期（2025-2027）；据CEPB通稿，第一任期内联合会成员团体由26个增至29个。",
            "organization": "玻利维亚私营企业家联合会 (Confederación de Empresarios Privados de Bolivia)"
        },
        {
            "date": "2026-06-28",
            "achievement": "在科恰班巴召集全国企业家特别峰会，约60个商业组织参加，通过请求与帕斯总统紧急会晤、制定全国经济复苏计划、要求制止道路封锁等决议，形成递交政府的统一私营部门方案。",
            "organization": "玻利维亚私营企业家联合会 (Confederación de Empresarios Privados de Bolivia)"
        }
    ],
    "biography_summary": "乔瓦尼·奥图尼奥·卡马乔（Giovanni Ortuño Camacho），玻利维亚企业家，现任玻利维亚私营企业家联合会（CEPB）主席。生于波托西，电子与电信工程师出身，长期执掌电子收款与支付服务企业AXS玻利维亚公司（AXS Bolivia）任执行总裁兼首席执行官；曾任玻利维亚电信商会理事会成员14年、CEPB经济与税务委员会主席及安第斯企业家理事会主席。2019年起任CEPB第一副主席，2023年3月作为单一候选名单当选CEPB主席，接替路易斯·巴贝里；第一任期内推动与路易斯·阿尔塞政府的公私对话，促成2024年8月17点经济协议及后续最高法令，联合会成员团体由26个增至29个，并组织与巴西总统卢拉、巴拉圭总统培尼亚的企业家会晤及第九届拉美反走私会议（圣克鲁斯）。2025年3月12日获全票连任，任内明确CEPB在2025年大选中不支持、不反对、不与任何候选人结盟。帕斯政府2025年11月执政后，他主导2026年6月科恰班巴全国企业家特别峰会，推动向政府递交全国经济复苏方案，并就最低工资调整（称约7%涨幅「过度且轻率」）、道路封锁等议题代表私营部门发声，与COB工会方面构成劳资博弈两端。",
    "position_note": "CEPB主席为玻利维亚私营部门最高行业组织（29个成员团体）的领导人，任期两年；其第二任期（2025-2027）截至收集日（2026-10-26）在任。",
    "work_note": "任CEPB主席期间仍保留AXS玻利维亚公司执行总裁兼CEO职务（Cosas Bolivia 2025年8月专访以其双重身份进行）。",
    "name_zh_note": "中文媒体未检索到对其的既有标准译名（未见玻利维亚华文媒体或中文权威媒体对其的成体系报道），故置null。",
    "collection_meta": {
        "collection_date": "2026-10-26",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "news_search",
            "web_search",
            "social_media"
        ],
        "quotes": [
            {
                "title": "Giovanni Ortuño es elegido por unanimidad como Presidente de la CEPB por una segunda gestión (CEPB官方通稿, 2025-03-12)",
                "url": "https://www.cepb.org.bo/notas-de-prensa/giovanni-ortuno-es-elegido-por-unanimidad-como-presidente-de-la-confederacion-de-empresarios-privados-de-bolivia-por-una-segunda-gestion"
            },
            {
                "title": "Giovanni Ortuño Camacho sería el nuevo presidente de la Confederación de Empresarios Privados de Bolivia (Infodiez, 2023-03-13)",
                "url": "https://www.infodiez.com/giovanni-ortuno-camacho-seria-el-nuevo-presidente-de-la-confederacion-de-empresarios-privados-de-bolivia"
            },
            {
                "title": "Giovanni Ortuño asume presidencia CEPB (Los Tiempos, 2023-03-16)",
                "url": "https://www.lostiempos.com/actualidad/pais/20230316/giovanni-ortuno-asume-presidencia-cepb"
            },
            {
                "title": "Giovanni Ortuño se perfila como el nuevo presidente de la Confederación de Empresarios (CADECOCruz)",
                "url": "https://cadecocruz.org.bo/index.php?op=51&nw=8701"
            },
            {
                "title": "Empresarios califican como positivas las primeras medidas para cumplir el acuerdo de los 17 puntos (CEPB, 2024-08-30)",
                "url": "https://www.cepb.org.bo/notas-de-prensa/empresarios-califican-como-positivas-las-primeras-medidas-para-cumplir-el-acuerdo-de-los-17-puntos"
            },
            {
                "title": "Gobierno y empresarios privados establecen 17 acuerdos; se descarta control de divisas (Opinión, 2024-08-17)",
                "url": "https://www.opinion.com.bo/pais/gobierno-empresarios-privados-establecen-17-acuerdos-descarta-control-divisas/20240817084514953273.html"
            },
            {
                "title": "CEPB pide reunión urgente con Ministro de Trabajo para tratar aumento y negociación salarial (CEPB, 2026-01-23)",
                "url": "https://www.cepb.org.bo/notas-de-prensa/cepb-pide-reunion-urgente-con-ministro-de-trabajo-para-tratar-aumento-y-negociacion-salarial"
            },
            {
                "title": "Confederación de empresarios convoca a una cumbre para discutir un plan frente a la crisis económica (ANF/Agencia Fides, 2026-06-28)",
                "url": "https://www.noticiasfides.com/economia/confederacion-de-empresarios-convoca-a-una-cumbre-para-discutir-un-plan-frente-a-la-crisis-economica"
            },
            {
                "title": "Empresarios piden reunión urgente con Rodrigo Paz para reactivar la economía (El Deber, 2026-06-30)",
                "url": "https://eldeber.com.bo/economia/empresarios-piden-reunion-urgente-rodrigo-paz-reactivar-economia_1782844719"
            },
            {
                "title": "Empresarios buscan apoyar al gobierno de Paz para superar la crisis y recuperar la estabilidad (Visión360, 2025-11-11)",
                "url": "https://www.vision360.bo/noticias/2025/11/11/35154-empresarios-buscan-apoyar-al-gobierno-de-paz-para-superar-la-crisis-y-recuperar-la-estabilidad"
            },
            {
                "title": "Giovanni Ortuno - Presidente Ejecutivo / CEO AXS Bolivia (LinkedIn)",
                "url": "https://bo.linkedin.com/in/giovanni-ortuno-bb7648103"
            },
            {
                "title": "Empresarios piden reglamentar decreto que reconoce negociación del incremento salarial (Unitel, 2026-01)",
                "url": "https://unitel.bo/noticias/economia/empresarios-piden-reglamentar-decreto-que-reconoce-negociacion-del-incremento-salarial-con-sus-trabajadores-IM19043913"
            }
        ],
        "completeness_score": 0,
        "notes": "关键事实核实：2023年3月当选CEPB主席（infodiez、Los Tiempos 2023-03-16就任报道、CADECOCruz三源交叉）；2025-03-12全票连任（CEPB官网通稿、Publicnow、CEIB）；2024-08-16与阿尔塞政府17点协议及8月28日两份最高法令（CEPB通稿、Opinión、Brújula Digital）；2026年1月最低工资立场（CEPB通稿、Opinión、Unitel）；2026-06科恰班巴企业家峰会（ANF Fides、El Deber、Novavox）。精读全文来源≥5个独立站点（CEPB官网×3、infodiez、CADECOCruz、El Deber、ANF Fides、Visión360）。存疑与空缺：出生日期未披露（birth_date=null）；中文无既有译名（name_zh=null，name_zh_note说明）；家庭成员无公开资料（family_members=[]）；社媒仅LinkedIn可核实（social_accounts_note说明六平台扫描结果）；学历信息来自LinkedIn档案第三方抓取（AeroLeads）与Magazine Management《Perspectivas 2026》，院校可靠性一般，已在education条目note中标注；长期定居地报道不一（infodiez称科恰班巴/拉巴斯，另有来源称圣克鲁斯），仅采信多源一致的出生地波托西。同名甄别：Ortuño为玻利维亚东部常见姓氏——检索摘要曾将Google工程师Giovanni Ortuño Urquidi（哥伦比亚大学/纽约）信息与本人混淆（其声称的「1991-92年生、Columbia大学」与本人物不符，已剔除）；Instagram @ortunogiovanni与哥斯达黎加Facebook用户身份无法核实，未录入。工具说明：search-read MCP本会话不可用，按SKILL §10降级为WebSearch+web_reader。completeness_score=74：因出生日期、中文名、家庭信息客观缺失且可核实社媒仅1个，无法达到85分；行业领袖公开活动报道丰富（立场6条、成就4条、关系6条、经历6条），高于60分兜底线。"
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

# --- self checks ---
with open(OUT, encoding="utf-8") as f:
    back = json.load(f)

errs = []
if back["person_id"] != "BO-PERSON-000425":
    errs.append("person_id mismatch")
smart = re.findall(r"[“”„‟]", json.dumps(back, ensure_ascii=False))
if smart:
    errs.append("smart quotes found: %d" % len(smart))
allowed_top = set(json.load(open(r"D:\claude-workspace\apec-osint-tool\.agents\skills\country-org-collector\person_profile_schema.json", encoding="utf-8"))["properties"].keys())
extra = set(back.keys()) - allowed_top
if extra:
    errs.append("extra top-level fields: %s" % extra)
# index cross-check
idx = json.load(open(r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\_name_index.json", encoding="utf-8"))
for rel in back["person_relationships"]:
    pid = rel["person_id"]
    if pid and pid not in idx.values():
        errs.append("person_id not in index: %s" % pid)
for w in back["work_experience"]:
    oid = w["org_id"]
    if oid and oid not in idx.values():
        errs.append("org_id not in index: %s" % oid)

counts = {k: len(back.get(k, [])) for k in
          ["work_experience", "education", "person_relationships", "social_accounts",
           "family_members", "political_stances", "major_achievements", "current_positions"]}
counts["quotes"] = len(back["collection_meta"]["quotes"])
print("WRITTEN:", OUT)
print("bio length:", len(back["biography_summary"]))
print("counts:", json.dumps(counts))
print("SELF-CHECK:", "OK (0 errors)" if not errs else errs)

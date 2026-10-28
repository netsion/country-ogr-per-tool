# -*- coding: utf-8 -*-
"""Enrich BO-GOV-015 (Ministerio de Hidrocarburos y Energias) org profile. Phase 3."""
import json

PATH = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\orgs\BO-GOV-015.json"

data = {
    "org_id": "BO-GOV-015",
    "wikidata_qid": "Q52536720",
    "basic_info": {
        "name_original": "Ministerio de Hidrocarburos y Energías",
        "name_zh": "玻利维亚碳氢化合物与能源部",
        "name_en": "Ministry of Hydrocarbons and Energies",
        "aliases": [
            "Ministerio de Hidrocarburos y Energía",
            "Min-HE",
            "MHE",
            "Ministry of Hydrocarbons and Energy",
            "Ministerio de Hidrocarburos"
        ],
        "org_type": "GOV",
        "org_subtype": "ministry",
        "country_iso3": "BOL",
        "hq_country_iso3": "BOL",
        "founded_date": None,
        "website": "https://www.mhe.gob.bo/"
    },
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "Ministerio de Hidrocarburos y Energías",
            "url": "https://www.facebook.com/profile.php?id=61582062099927",
            "source": "https://www.mhe.gob.bo/（官网页脚链接）"
        },
        {
            "platform": "twitter_x",
            "account_name": "@Bolivia_MHE",
            "url": "https://x.com/Bolivia_MHE",
            "source": "https://www.mhe.gob.bo/（官网页脚链接）"
        },
        {
            "platform": "instagram",
            "account_name": "@bolivia_mhe",
            "url": "https://www.instagram.com/bolivia_mhe/",
            "source": "https://www.mhe.gob.bo/（官网页脚链接）"
        },
        {
            "platform": "youtube",
            "account_name": "Ministerio de Hidrocarburos y Energías (canal UCXudQJyOKCqjCckLlbyu-dA)",
            "url": "https://www.youtube.com/channel/UCXudQJyOKCqjCckLlbyu-dA",
            "source": "https://www.mhe.gob.bo/（官网页脚链接）"
        },
        {
            "platform": "tiktok",
            "account_name": "@mhebolivia",
            "url": "https://www.tiktok.com/@mhebolivia",
            "source": "https://www.mhe.gob.bo/（官网页脚链接）"
        }
    ],
    "digital_assets": [
        {
            "name": "MHE 机构门户网站",
            "url": "https://www.mhe.gob.bo/",
            "description": "玻利维亚碳氢化合物与能源部官方网站，发布部长动态、副部长机构设置、新闻（燃料供应管控、乙醇掺混、双边能源合作等）及各副部长单位页面（如 /vmeer/ 电力与可再生能源）。",
            "source": "https://www.mhe.gob.bo/"
        },
        {
            "name": "旧版门户网站（www3.hidrocarburos.gob.bo，已停用）",
            "url": "https://www3.hidrocarburos.gob.bo/",
            "description": "该部旧官网域名，西班牙语维基百科标注为失效链接（enlace roto），内容仅可通过 Internet Archive 历史快照访问；现官网已迁移至 mhe.gob.bo。",
            "source": "https://es.wikipedia.org/wiki/Ministerio_de_Hidrocarburos_(Bolivia)"
        }
    ],
    "key_people": [
        {
            "person_id": None,
            "name": "Marcelo Blanco Quintanilla",
            "title": "Ministro de Hidrocarburos y Energías",
            "title_description": "碳氢化合物与能源部部长（部长会议成员）",
            "description": "2026年4月22日由总统罗德里戈·帕斯·佩雷拉（Rodrigo Paz Pereira）宣誓就任部长，接替毛里西奥·梅迪纳塞利（Mauricio Medinaceli），就任时正值燃料质量争议及YPFB总裁辞职的危机背景。能源领域从业30余年，此前（2025年11月起）任该部电力与可再生能源副部长。"
        },
        {
            "person_id": None,
            "name": "Tatiana Genucio Pazzi",
            "title": "Viceministra de Hidrocarburos",
            "title_description": "碳氢化合物副部长",
            "description": "2026年9月1日由部长布兰科宣誓就任，任命依据为2026年8月26日第32438号最高决议（Resolución Suprema 32438），由总统帕斯签署。"
        },
        {
            "person_id": None,
            "name": "José Eduardo Germán Ustariz Márquez",
            "title": "Viceministro de Planificación y Desarrollo Energético",
            "title_description": "能源规划与发展副部长",
            "description": "2026年9月1日就任，任命依据为2026年8月第32439号最高决议（Resolución Suprema 32439），分管能源规划与开发政策。"
        },
        {
            "person_id": None,
            "name": "Luis Eduardo Osorio Calderón",
            "title": "Viceministro de Recursos Evaporíticos y Tecnologías Energéticas Emergentes",
            "title_description": "蒸发岩资源与新兴能源技术副部长",
            "description": "2026年9月1日就任，任命依据为2026年8月26日第32440号最高决议（Resolución Suprema 32440），分管盐湖蒸发岩资源与新兴能源技术。"
        },
        {
            "person_id": None,
            "name": "Rudy Alberto Peredo Flores",
            "title": "Viceministro de Electricidad y Energías Renovables",
            "title_description": "电力与可再生能源副部长",
            "description": "2026年5月4日宣誓就任；机械电气工程师，拥有30余年行业经验。其前任马塞洛·布兰科·金塔尼利亚于2026年4月升任部长。"
        }
    ],
    "departments": [
        {
            "name": "Viceministerio de Hidrocarburos（碳氢化合物副部长单位）",
            "dept_id": None,
            "head": "Tatiana Genucio Pazzi",
            "description": "主管碳氢化合物行业政策，涵盖勘探开发、工业化、商业化、运输与储存等环节，并牵头燃料供应与价格管控事务（如ANH介入整顿、燃料走私查缉）。",
            "parent_dept_id": "BO-GOV-015"
        },
        {
            "name": "Viceministerio de Planificación y Desarrollo Energético（能源规划与发展副部长单位）",
            "dept_id": None,
            "head": "José Eduardo Germán Ustariz Márquez",
            "description": "负责国家能源发展规划与能源开发政策，统筹天然气产量下滑背景下的勘探开发投资规划。",
            "parent_dept_id": "BO-GOV-015"
        },
        {
            "name": "Viceministerio de Recursos Evaporíticos y Tecnologías Energéticas Emergentes（蒸发岩资源与新兴能源技术副部长单位）",
            "dept_id": None,
            "head": "Luis Eduardo Osorio Calderón",
            "description": "负责蒸发岩资源（盐湖锂、钾盐等）与新兴能源技术相关政策，为帕斯政府新设机构设置。",
            "parent_dept_id": "BO-GOV-015"
        },
        {
            "name": "Viceministerio de Electricidad y Energías Renovables（电力与可再生能源副部长单位）",
            "dept_id": None,
            "head": "Rudy Alberto Peredo Flores",
            "description": "主管电力部门与可再生能源政策及监管，推动电力矩阵转型与区域能源互联（与智利电网互联评估等）。",
            "parent_dept_id": "BO-GOV-015"
        }
    ],
    "recent_events": [
        {
            "date": "2025-12-17",
            "title": "政府颁布第5503号最高法令取消燃料补贴并宣布经济社会紧急状态",
            "description": "总统帕斯于12月17日夜间颁布包含121条条款的第5503号最高法令（DS 5503），终结实施约20年的燃料补贴：特殊汽油升至6.96玻利维亚诺/升（约1美元）、高级汽油11玻利维亚诺/升、柴油9.80玻利维亚诺/升，并宣布经济社会紧急状态。该法令由碳氢化合物与能源部配合执行，引发运输等行业抗议（12月22日矿工、古柯农等举行示威）。",
            "impact": "重大政策转折：结束长期燃料补贴以遏制财政失血与燃料长期短缺，但推高通胀与生活成本，引发持续社会抗议，成为该部及帕斯政府执政初期的核心争议议题。",
            "source": "https://www.bbc.com/mundo/articles/c0je2pljl84o"
        },
        {
            "date": "2026-04-22",
            "title": "马塞洛·布兰科·金塔尼利亚接任碳氢化合物与能源部部长",
            "description": "总统帕斯宣誓马塞洛·布兰科·金塔尼利亚为新任部长，接替上任仅约半年的毛里西奥·梅迪纳塞利（Mauricio Medinaceli）。布兰科此前任该部电力与可再生能源副部长，能源行业经验逾30年，就任时正值燃料质量争议发酵、YPFB总裁辞职。",
            "impact": "帕斯政府首次更换该部部长，反映燃料短缺与质量危机下的问责压力；布兰科随后主导ANH介入整顿、乙醇掺混协议与对智利能源一体化谈判等系列措施。",
            "source": "https://www.reuters.com/world/americas/bolivia-nominates-marcelo-blanco-new-minister-energy-hydrocarbons-2026-04-23/"
        },
        {
            "date": "2026-09-03",
            "title": "政府依据第5699号最高法令对国家碳氢化合物局（ANH）实施介入整顿",
            "description": "部长布兰科主持宣布对行业监管机构ANH实施介入整顿（intervención），以第5699号最高法令（DS 5699）刊宪，事由为该机构履职存在缺陷，背景是柴油等燃料持续短缺。9月1日部长还先行宣誓了三位新任副部长（碳氢化合物、能源规划与发展、蒸发岩资源）。",
            "impact": "该部对核心监管机构实施直接接管，强化燃料进口、分销与价格管控；随后每月公布查缉成果，成为该部恢复燃料供应秩序的主要手段。",
            "source": "https://www.infobae.com/america/agencias/2026/09/03/intervienen-el-ente-regulador-de-hidrocarburos-en-bolivia-por-deficiencias-en-su-labor/"
        },
        {
            "date": "2026-10-16",
            "title": "玻利维亚与智利签署能源一体化等五份合作文件（卡斯特访拉巴斯）",
            "description": "智利总统卡斯特对玻利维亚进行71年来首次正式访问，两国总统签署涵盖贸易、矿业、能源一体化与数字互联互通的五份文件：推进双边电网互联评估，碳氢化合物方面突出Sica Sica–Arica输油管反输（OSSA II）将增强玻方燃料供应安全。部长布兰科表示与智利的能源一体化将推动玻利维亚成为区域连接中心。",
            "impact": "两国关系历史性突破，为玻利维亚打开经智利港口的燃料供应通道并推进电力出口互联，直接改变该部区域能源一体化议程的外部环境。",
            "source": "https://cancilleria.gob.bo/mre/2026/10/17/26515/"
        },
        {
            "date": "2026-10-19",
            "title": "政府与蔗糖乙醇企业及蔗农达成协议：汽油乙醇掺混比例升至15%",
            "description": "政府、YPFB、蔗糖乙醇企业（ingenios sucroalcoholeros）与蔗农部门签署协议，自2026年11月1日起将汽油中乙醇掺混比例提高至15%，并自2027年4月1日起自动提高至18%。10月23日该部回应质疑时称掺混比例调整以科学研究为基础，并呼吁反对部门对话。",
            "impact": "通过生物燃料掺混部分替代进口汽油、节省外汇并支撑蔗糖产业，是该部在燃料补贴取消后推进能源主权与燃料多元化的标志性政策。",
            "source": "https://www.lostiempos.com/actualidad/economia/20261020/ypfb-caneros-acuerdan-elevar-mezcla-etanol-gasolina-15-partir-noviembre"
        },
        {
            "date": "2026-10-21",
            "title": "ANH介入整顿月度成果：查扣逾1.4万升汽油、封锁万余车牌",
            "description": "部长布兰科公布ANH介入整顿10月成果：查扣14,097升汽油与659罐液化石油气（GLP）、因重复超额加油封锁10,781块车牌、签发57项新的燃料进口许可，另有9人被捕、3辆车被扣；10月22日部长赴拉巴斯核查4.3万罐GLP供应。此前10月2日公布的首月数据显示封锁6,700块车牌、查扣1,700万升燃料、逮捕31人。",
            "impact": "显示该部借助介入整顿与B-SISA系统数据打击燃料走私与套利、稳定拉巴斯等地GLP供应，是应对燃料危机的直接治理成果。",
            "source": "https://www.reduno.com.bo/noticias/controles-dejan-14-097-litros-de-gasolina-decomisados-y-10-789-placas-bloqueadas-20261021112430"
        }
    ],
    "related_entities": [
        {
            "org_id": "BO-SOE-001",
            "org_name": "YPFB（Yacimientos Petrolíferos Fiscales Bolivianos，玻利维亚国家石油矿藏公司）",
            "org_type": "SOE",
            "org_description": "玻利维亚国家石油公司，负责碳氢化合物勘探、开采、炼化、运输与销售，下属YPFB Andina、YPFB Chaco、YPFB Refinación、YPFB Transporte及与Petrobras合资的Gas TransBoliviano等子公司；2025-2026年燃料短缺与乙醇掺混协议中的核心执行企业。",
            "relationship_type": "subsidiary"
        },
        {
            "org_id": "BO-GOV-038",
            "org_name": "ANH（Agencia Nacional de Hidrocarburos，国家碳氢化合物局）",
            "org_type": "GOV",
            "org_description": "碳氢化合物行业监管与的技术行政机构，负责油气合同、计量与燃料市场管控；2026年9月因履职缺陷被该部依据DS 5699介入整顿。",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "BO-SOE-003",
            "org_name": "ENDE（Empresa Nacional de Electricidad，国家电力公司）",
            "org_type": "SOE",
            "org_description": "国家电力 Corporación，业务覆盖发电、输电与配电，下属ELFEC、ENDE Corani、ENDE Guaracachi、ENDE Transmisión等子公司，是该部电力政策的国有企业执行主体。",
            "relationship_type": "subsidiary"
        },
        {
            "org_id": "BO-SOE-006",
            "org_name": "YLB（Yacimientos de Litio Bolivianos，玻利维亚锂矿藏公司）",
            "org_type": "SOE",
            "org_description": "负责乌尤尼等盐湖锂资源工业化开发的国有企业；蒸发岩资源事项与该部新设的蒸发岩资源与新兴能源技术副部长单位对口。",
            "relationship_type": "subsidiary"
        },
        {
            "org_id": None,
            "org_name": "ABEN（Agencia Boliviana de Energía Nuclear，玻利维亚核能局）",
            "org_type": "GOV",
            "org_description": "主管核能开发与核技术应用的附属机构，隶属该部管辖（据西班牙语维基百科该部隶属机构清单）。",
            "relationship_type": "affiliated"
        },
        {
            "org_id": None,
            "org_name": "AETN（Autoridad de Fiscalización de Electricidad y Tecnología Nuclear，电力与核技术监督局）",
            "org_type": "GOV",
            "org_description": "电力行业与核技术监督机构，隶属该部管辖（据西班牙语维基百科该部隶属机构清单）。",
            "relationship_type": "affiliated"
        },
        {
            "org_id": None,
            "org_name": "EBIH（Empresa Boliviana de Industrialización de Hidrocarburos，玻利维亚碳氢化合物工业化公司）",
            "org_type": "SOE",
            "org_description": "专注碳氢化合物工业化（炼化与石化）的国有企业，隶属该部管辖（据西班牙语维基百科该部隶属机构清单）。",
            "relationship_type": "subsidiary"
        }
    ],
    "core_business": "玻利维亚碳氢化合物与能源部（Min-HE）是多民族国政府主管能源与碳氢化合物行业的内阁部委，总部位于拉巴斯（Av. Mariscal Santa Cruz esq. Calle Oruro，Centro de Comunicaciones 大楼12层）。其核心职能是提出、制定并执行国家碳氢化合物与能源发展政策，覆盖油气勘探与开采、工业化、商业化、运输与储存全链条，以及电力、可再生能源、蒸发岩资源（盐湖锂钾）与新兴能源技术等领域；下设碳氢化合物、能源规划与发展、蒸发岩资源与新兴能源技术、电力与可再生能源四个副部长单位。该部对国家石油公司YPFB、国家碳氢化合物局ANH、国家电力公司ENDE、锂业公司YLB、核能局ABEN、电力与核技术监督局AETN及碳氢化合物工业化公司EBIH等机构行使主管部门职权。2025年底以来，其工作重心转向应对天然气产量与出口持续下滑引发的燃料危机：执行取消燃料补贴的第5503号最高法令、整顿监管机构ANH（DS 5699）、打击燃料走私、提高汽油乙醇掺混比例，并推进与智利的能源一体化（输油管反输与电网互联），以保障燃料供应安全、重塑能源主权并推动玻利维亚成为南美区域能源连接枢纽。",
    "industries": [
        "public_administration",
        "energy_oil_gas",
        "electricity_gas",
        "energy_renewable",
        "regulatory"
    ],
    "apec_stance": "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。该国能源对外合作重心在南美区域一体化：2026年10月16日与智利签署能源一体化等合作文件（含Sica Sica–Arica输油管反输项目与双边电网互联评估），部长布兰科称目标是使玻利维亚成为区域能源连接中心；此前玻利维亚长期通过管道向巴西、阿根廷出口天然气，但因产量下滑，对阿根廷供应合同已结束，导致其陷入民主化时代最严重的经济危机，能源出口重心正转向区域电力互联与生物燃料掺混。",
    "profile": {
        "source_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Ministerio_de_Hidrocarburos_y_Energias.png/330px-Ministerio_de_Hidrocarburos_y_Energias.png",
        "local_path": None
    },
    "collection_meta": {
        "collection_date": "2026-10-24",
        "phase": "phase3_enriched",
        "data_sources": [
            "wikidata",
            "es.wikipedia.org",
            "www.mhe.gob.bo（官方网站首页及/vmeer/机构页）",
            "www.reuters.com",
            "abi.bo（玻利维亚通讯社，经vision360.bo转载核实）",
            "www.bbc.com/mundo",
            "elpais.com",
            "www.infobae.com",
            "www.lostiempos.com",
            "www.reduno.com.bo",
            "www.opinion.com.bo",
            "cancilleria.gob.bo",
            "www.vision360.bo",
            "lexivox.org / bolivia.vlex.com（DS 29894）"
        ],
        "quotes": [
            {
                "title": "Bolivia nominates Marcelo Blanco as new minister of energy and hydrocarbons (Reuters, 2026-04-23)",
                "url": "https://www.reuters.com/world/americas/bolivia-nominates-marcelo-blanco-new-minister-energy-hydrocarbons-2026-04-23/"
            },
            {
                "title": "Intervienen el ente regulador de hidrocarburos en Bolivia por deficiencias en su labor (Infobae, 2026-09-03, DS 5699)",
                "url": "https://www.infobae.com/america/agencias/2026/09/03/intervienen-el-ente-regulador-de-hidrocarburos-en-bolivia-por-deficiencias-en-su-labor/"
            },
            {
                "title": "Bolivia y Chile sellan acuerdos de integración económica y energética (Cancillería de Bolivia, 2026-10-17)",
                "url": "https://cancilleria.gob.bo/mre/2026/10/17/26515/"
            },
            {
                "title": "YPFB y cañeros acuerdan elevar la mezcla de etanol en la gasolina al 15% a partir de noviembre (Los Tiempos, 2026-10-20)",
                "url": "https://www.lostiempos.com/actualidad/economia/20261020/ypfb-caneros-acuerdan-elevar-mezcla-etanol-gasolina-15-partir-noviembre"
            },
            {
                "title": "Marcelo Blanco posesiona a tres nuevos viceministros en el Ministerio de Hidrocarburos (Visión 360/ABI, 2026-09-01)",
                "url": "https://www.vision360.bo/noticias/2026/09/01/65593-marcelo-blanco-posesiona-a-tres-nuevos-viceministros-en-el-ministerio-de-hidrocarburos"
            }
        ],
        "completeness_score": 9,
        "notes": "Phase3 enrichment (2026-10-24). 现任部长Marcelo Blanco Quintanilla（2026-04-22就任，Reuters/ABI/Los Tiempos/Red Uno多源核实）；四位现任副部长经ABI（2026-09-01、2026-05-04）及官网/vmeer/页核实。founded_date留空：现行'碳氢化合物与能源部'架构由DS 29894（2009-02-07）确立，此前历经Ministerio de Hidrocarburos（2003-2005）与Ministerio de Energías等多次改组，确切创部日期无一致来源，故不填。旧官网www3.hidrocarburos.gob.bo已失效（Wikipedia标注），现官网为mhe.gob.bo。官网页脚另有LinkedIn入口但未获URL，未收录。总部地址：Av. Mariscal Santa Cruz esq. C/Oruro, Edif. Centro de Comunicaciones, Piso 12, La Paz（Wikipedia信息框）。ABEN/AETN/EBIH未入ID索引，org_id置null。"
    }
}

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("WROTE", PATH)
# quick self-check
with open(PATH, encoding="utf-8") as f:
    d = json.load(f)
print("keys:", list(d.keys()))
print("kp:", len(d["key_people"]), "| events:", len(d["recent_events"]),
      "| related:", len(d["related_entities"]), "| depts:", len(d["departments"]),
      "| social:", len(d["social_accounts"]), "| digital:", len(d["digital_assets"]))
cb = d["core_business"]
print("core_business length:", len(cb))
print("apec_stance length:", len(d["apec_stance"]))

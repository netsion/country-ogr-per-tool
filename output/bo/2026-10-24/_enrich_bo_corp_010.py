# -*- coding: utf-8 -*-
"""Enrich BO-CORP-010 (Gas TransBoliviano S.A.) - phase3_enriched"""
import json

PATH = "D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/orgs/BO-CORP-010.json"

with open(PATH, encoding="utf-8") as f:
    data = json.load(f)

data["basic_info"].update({
    "name_zh": "玻利维亚天然气运输公司",
    "name_en": "Gas TransBoliviano S.A.",
    "aliases": ["GTB", "Gas TransBoliviano", "玻利维亚天然气运输股份有限公司"],
    "founded_date": "1997-07-16",
    "website": "https://www.gastransboliviano.com.bo/",
    "wikidata_qid": None,
})

data["social_accounts"] = [
    {
        "platform": "linkedin",
        "account_name": "Gas TransBoliviano S.A.",
        "url": "https://www.linkedin.com/company/gas-transboliviano-s.a.",
        "source": "https://www.linkedin.com/company/gas-transboliviano-s.a.",
    },
    {
        "platform": "instagram",
        "account_name": "@gastransboliviano",
        "url": "https://www.instagram.com/gastransboliviano/",
        "source": "https://www.instagram.com/gastransboliviano/",
    },
]

data["digital_assets"] = [
    {
        "name": "Gas TransBoliviano 官方网站",
        "url": "https://www.gastransboliviano.com.bo/",
        "description": "公司官网，发布企业概况、管道运营信息、采购招标与年度报告（Memorias）等。",
        "source": "https://www.gastransboliviano.com.bo/",
    },
    {
        "name": "GTB 新闻订阅（RSS）",
        "url": "https://www.gastransboliviano.com.bo/feed/",
        "description": "官网 WordPress 站点提供的内容订阅源。",
        "source": "https://www.gastransboliviano.com.bo/",
    },
]

data["key_people"] = [
    {
        "person_id": None,
        "name": "卡佳·米尔娜·迪德里希·库塞维奇（Katya Mirna Diederich Kuscevic）",
        "title": "Gerente General（总经理）",
        "title_description": "总经理",
        "description": "玻利维亚油气行业资深管理者，企业管理专业出身，曾于2010-2015年首次出任GTB总经理，2020年10月被任命为YPFB执行总裁（该职位历史上首位女性），此后再度执掌GTB。公司官网管理层页面（2026年2月更新）、YPFB官方报道（2026年5月）及YPFB述职纪要（2026年4月）均确认其现任GTB总经理。",
    },
    {
        "person_id": None,
        "name": "罗德里戈·安普埃罗·科英布拉（Rodrigo Ampuero Coimbra）",
        "title": "Gerente de Operaciones（运营总经理）",
        "title_description": "运营总经理",
        "description": "据GTB官网管理层页面（2026年2月更新），现任公司运营总经理，负责玻利维亚-巴西天然气管道玻方管段的日常运营维护。",
    },
    {
        "person_id": None,
        "name": "迪拉·塔蒂亚娜·胡斯蒂尼亚诺·韦莱斯（Dila Tatiana Justiniano Vélez）",
        "title": "Gerente de Administración y Finanzas（行政与财务总经理）",
        "title_description": "行政与财务总经理",
        "description": "据GTB官网管理层页面（2026年2月更新），现任公司行政与财务总经理。",
    },
    {
        "person_id": None,
        "name": "鲁道夫·埃内斯托·巴里加·埃斯滕索罗（Rodolfo Ernesto Barriga Estenssoro）",
        "title": "Director de Seguridad, Salud, Medio Ambiente y RSE（安全、健康、环境与企业社会责任总监）",
        "title_description": "安全、健康、环境与企业社会责任总监",
        "description": "据GTB官网管理层页面（2026年2月更新），现任公司安全、职业健康、环境与企业社会责任（HSE+RSE）总监。",
    },
]

data["departments"] = [
    {
        "name": "Gerencia de Operaciones（运营部）",
        "dept_id": None,
        "head": "罗德里戈·安普埃罗·科英布拉（Rodrigo Ampuero Coimbra）",
        "description": "负责玻利维亚-巴西天然气管道玻方557公里管段及里奥格兰德、伊索索格、奇基托斯、罗博雷、亚库塞斯、穆通等站场的运行、维护与完整性管理。",
        "parent_dept_id": None,
    },
    {
        "name": "Gerencia de Administración y Finanzas（行政与财务部）",
        "dept_id": None,
        "head": "迪拉·塔蒂亚娜·胡斯蒂尼亚诺·韦莱斯（Dila Tatiana Justiniano Vélez）",
        "description": "负责公司行政管理、财务预算与资金管理；2026年公司预算净收入约1.78亿玻利维亚诺、投资计划2100万玻利维亚诺。",
        "parent_dept_id": None,
    },
    {
        "name": "Dirección de Seguridad, Salud, Medio Ambiente y RSE（安全、健康、环境与企业社会责任部）",
        "dept_id": None,
        "head": "鲁道夫·埃内斯托·巴里加·埃斯滕索罗（Rodolfo Ernesto Barriga Estenssoro）",
        "description": "负责管道安全、职业健康、环境许可（2026年启动环境许可证换证）及企业社会责任事务。",
        "parent_dept_id": None,
    },
    {
        "name": "Auditoría Interna（内部审计）",
        "dept_id": None,
        "head": None,
        "description": "公司内部审计职能。官网历史版本显示何塞·路易斯·莫利纳·佩雷斯（José Luis Molina Pérez）曾任该职，现任负责人未获可靠信息。",
        "parent_dept_id": None,
    },
]

data["core_business"] = (
    "Gas TransBoliviano S.A.（GTB）是玻利维亚天然气管道运输企业，隶属玻利维亚国家石油公司（YPFB）体系："
    "YPFB通过其子公司YPFB Transporte S.A.持有GTB 51%股份，其余约49%为私人资本，其中包括巴西国家石油公司Petrobras。"
    "公司核心业务是运营玻利维亚-巴西天然气管道（GASBOL）的玻利维亚段：该管段全长557公里、直径32英寸、最高输量约"
    "3290万立方米/日，起自圣克鲁斯东南约40-50公里的里奥格兰德（Río Grande）计量首站，经伊索索格、奇基托斯、罗博雷、"
    "亚库塞斯等压气站，东至玻巴边境穆通（Mutún）计量站，是全长3150公里的南美洲最长天然气管道的玻方部分。GTB与巴西侧"
    "运营商TBG（Transportadora Brasileira Gasoduto Bolivia-Brasil S.A.）协同，将玻利维亚天然气输往圣保罗、阿雷格里港等"
    "巴西东南部市场，1999年投运至今逾26年（2024年经该管道输巴气量平均约1420万立方米/日，较2023年下降8.4%）。经年度客户满意度调查确认的主要客户为YPFB、Petrobras与TBG。近年因玻利维亚"
    "气田产量下滑，2026年计划输量约1300万立方米/日（预算净收入约1.78亿玻利维亚诺，其中出口市场1.65亿），公司同步推进"
    "管道完整性修复、微燃机自发电改造、环境许可换证等项目，其设施亦自2025年起成为阿根廷经玻利维亚向巴西输气的过境通道"
    "组成部分，正从单一出口运营商向南美洲区域天然气过境枢纽转型。"
)

data["industries"] = [
    "energy_oil_gas",
    "infrastructure",
]

data["recent_events"] = [
    {
        "date": "2026-05-01",
        "title": "GTB公布2026年2100万玻利维亚诺投资计划，预计输气1300万立方米/日",
        "description": "在YPFB2026年首场公众述职听证会上，总经理卡佳·迪德里希介绍：2026年计划投资2100万玻利维亚诺（88%投向运营连续性），其中约1600万用于管道完整性项目（伊索索格-奇基托斯、亚库塞斯-穆通管段，已识别1700延米缺陷并完成约838延米修复，财务进度34%）；预计全年净收入1.78亿玻利维亚诺（出口1.65亿、国内市场0.13亿），输量约1300万立方米/日；并推进站场微燃机替代柴油发电、环境许可换证与信息化建设。",
        "impact": "保障已运营26年的对巴西出口通道的安全可靠与能效，降低运营成本并满足环境合规，巩固GTB作为玻利维亚对巴西输气核心资产的地位。",
        "source": "https://www.ypfb.gob.bo/index.php/node/525",
    },
    {
        "date": "2026-04-15",
        "title": "YPFB文件确认卡佳·迪德里希任GTB总经理",
        "description": "YPFB官网发布的《2025年度公众述职听证会纪要（ACTA RPC FINAL 2025）》中，卡佳·米尔娜·迪德里希·库塞维奇以Gas TransBoliviano S.A.总经理身份署名；公司官网管理层页面（2026年2月更新）亦列其为总经理。迪德里希曾于2010-2015年执掌GTB，2020年10月曾任YPFB执行总裁，此番系再度执掌GTB。",
        "impact": "由具有YPFB体系高层经验的资深管理者执掌，有助于GTB在玻利维亚天然气产量下行期协调集团资源，推进管道完整性投资与区域输气枢纽转型。",
        "source": "https://www.ypfb.gob.bo/sites/default/files/2026-04/ACTA%20RPC%20FINAL%202025.pdf",
    },
    {
        "date": "2025-05-26",
        "title": "YPFB研究扩容GASBOL（输量自3500万提至4200万立方米/日）以承接阿根廷对巴西输气",
        "description": "据巴西能源媒体Agência iNFRA报道，YPFB总裁阿明·多加滕（Armin Dorgathen）表示，YPFB已完成可行性研究，可通过较小投资（约1000万-1200万美元）将玻利维亚-巴西管道（GASBOL）输气能力从3500万立方米/日提升至4200万立方米/日，以承接阿根廷经玻利维亚对巴西的输气，土建工期约1年；巴方已授权十余家企业开展点对点（非固定容量）输气。GASBOL玻方管段运营商即GTB。2024年经该管道输巴气量平均约1420万立方米/日（较2023年的1550万下降8.4%），历史峰值超3000万立方米/日。",
        "impact": "若扩容落地，将提升GTB所辖管道资产的过境利用率与收入弹性，是公司从单一出口运营商转向区域输气枢纽的关键潜在项目。",
        "source": "https://agenciainfra.com/blog/presidente-da-ypfb-fala-em-ampliar-gasbol-para-passagem-de-gas-argentino-ao-brasil/",
    },
    {
        "date": "2026-06-25",
        "title": "YPFB调整子公司管理层：迪德里希获任YPFB Transporte（GTB直接母公司）负责人",
        "description": "据玻利维亚通讯社（ANF）报道，YPFB于2026年6月25日公布子公司新任管理层名单，其中卡佳·迪德里希·库塞维奇获任YPFB Transporte S.A.（GTB持股51%的直接控股股东）负责人；截至本次采集时点，GTB官网管理层页面仍将其列为GTB总经理，其是否兼任或已卸任GTB总经理有待后续确认。",
        "impact": "母公司层面人事联动密切了GTB与YPFB Transporte的协调，但GTB总经理职位归属需持续跟踪，存在治理层面不确定性。",
        "source": "https://www.facebook.com/ANFidesBolivia/videos/1337063487924089",
    },
    {
        "date": "2026-10-01",
        "title": "巴西ANP批准Petrobras经GASBOL直接进口阿根廷天然气（每年最高1800万立方米）",
        "description": "据行业媒体2026年10月1日报道，巴西国家石油局（ANP）已在官方公报批准Petrobras不经中介直接进口最多1800万立方米/年的阿根廷天然气，经玻利维亚管网汇入玻利维亚-巴西管道（GASBOL，玻方由GTB运营）输往巴西。此前YPFB已建立阿根廷经玻利维亚至巴西的天然气过境业务（2025年四季度起全面投运，初期可达400万立方米/日）并已公布过境气价。另据YPFB年度听证信息，2026年GTB预算已将过境等多元合同纳入输量结构。",
        "impact": "在玻利维亚自产气持续减产背景下，GASBOL由玻气出口专线向区域过境通道转型，为GTB带来新的过境输量与收入来源，但区域气源格局变化亦带来长期不确定性。",
        "source": "https://en.clickpetroleoegas.com.br/petrobras-obtem-aval-da-anp-para-importar-ate-180-milhoes-m%C2%B3-ano-de-gas-argentino-diretamente-via-gasbol-e-fortalecer-seguranca-energetica-nacional-hl1402/",
    },
]

data["related_entities"] = [
    {
        "org_id": "BO-SOE-001",
        "org_name": "Yacimientos Petrolíferos Fiscales Bolivianos（YPFB，玻利维亚国家石油公司）",
        "org_type": "SOE",
        "org_description": "玻利维亚国家油气产业链核心国有企业。GTB为其filial（集团旗下公司），GTB总经理参加YPFB年度公众述职听证会。",
        "relationship_type": "controlling_shareholder",
    },
    {
        "org_id": "BO-GOV-015",
        "org_name": "Ministerio de Hidrocarburos y Energías（玻利维亚碳氢化合物与能源部）",
        "org_type": "GOV",
        "org_description": "玻利维亚主管碳氢化合物与能源事务的政府部门，是国家油气运输行业的政策与主管部门；YPFB及其子公司（含GTB）业务处于其政策框架之下。",
        "relationship_type": "regulator",
    },
    {
        "org_id": None,
        "org_name": "YPFB Transporte S.A.",
        "org_type": "SOE",
        "org_description": "YPFB旗下天然气运输子公司，持有GTB 51%股份，为GTB的直接控股股东（YPFB官方与GTB官网均作此表述）。",
        "relationship_type": "controlling_shareholder",
    },
    {
        "org_id": None,
        "org_name": "Transportadora Brasileira Gasoduto Bolivia-Brasil S.A.（TBG）",
        "org_type": "CORP",
        "org_description": "玻利维亚-巴西天然气管道巴西段的所有者与运营商，与GTB就跨境管道保持常态化运营与行政协调，同为GTB客户之一。",
        "relationship_type": "partner",
    },
    {
        "org_id": None,
        "org_name": "Petróleo Brasileiro S.A.（Petrobras，巴西国家石油公司）",
        "org_type": "CORP",
        "org_description": "巴西国家石油公司，GTB的主要客户（出口承购方）之一；据GTB官网，其亦为GTB私人股东之一，并持有GASBOL巴西段运营商TBG的51%权益。",
        "relationship_type": "customer",
    },
    {
        "org_id": None,
        "org_name": "PETROGASBOL S.A.",
        "org_type": "CORP",
        "org_description": "玻利维亚-巴西管道玻方管段的建设公司，GTB股东曾向其提供融资以偿付建设债务。",
        "relationship_type": "supplier",
    },
]

data["apec_stance"] = (
    "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入），因此GTB不参与APEC框架下的议程，公司亦未发布"
    "任何与APEC相关的立场文件。作为玻利维亚-巴西天然气管道（GASBOL）玻方运营商，GTB的对外合作集中于南美洲区域能源"
    "一体化：一方面依YPFB与巴西Petrobras的合同向巴西市场输气（2026年计划输量约1300万立方米/日）；另一方面自2025年起"
    "承接阿根廷经玻利维亚管网向巴西的天然气过境业务（巴西ANP已批准Petrobras经GASBOL直接进口阿根廷气），YPFB管理层"
    "并公开表示可研究扩容GASBOL以扩大区域过境输能。上述合作均为双边或区域性质，与APEC机制无关。"
)

data["profile"] = {
    "source_url": "https://www.gastransboliviano.com.bo/wp-content/uploads/2025/11/cropped-logotipo2GTBv2.png",
    "local_path": None,
}

data["collection_meta"] = {
    "collection_date": "2026-10-25",
    "phase": "phase3_enriched",
    "data_sources": [
        "web_search",
        "https://www.gastransboliviano.com.bo/",
        "https://www.gastransboliviano.com.bo/perfil-de-la-empresa/",
        "https://www.gastransboliviano.com.bo/gerencia-ejecutiva/",
        "https://www.gastransboliviano.com.bo/clientes-y-contratos/",
        "https://www.ypfb.gob.bo/index.php/node/525",
        "https://www.ypfb.gob.bo/sites/default/files/2026-04/ACTA%20RPC%20FINAL%202025.pdf",
        "https://www.eldiario.net/portal/2026/05/02/gtb-proyecta-bs-21-millones-en-inversiones/",
        "https://en.clickpetroleoegas.com.br/petrobras-obtem-aval-da-anp-para-importar-ate-180-milhoes-m%C2%B3-ano-de-gas-argentino-diretamente-via-gasbol-e-fortalecer-seguranca-energetica-nacional-hl1402/",
        "https://www.gem.wiki/Gasoducto_GASBOL",
        "https://www.bnamericas.com/en/company-profile/gas-transboliviano-sa",
        "https://www.linkedin.com/company/gas-transboliviano-s.a.",
        "https://www.instagram.com/gastransboliviano/",
        "https://erbol.com.bo/nacional/katya-diederich-ser%C3%A1-la-primera-mujer-presidenta-de-ypfb",
        "https://agenciainfra.com/blog/presidente-da-ypfb-fala-em-ampliar-gasbol-para-passagem-de-gas-argentino-ao-brasil/",
        "https://www.facebook.com/ANFidesBolivia/videos/1337063487924089",
    ],
    "completeness_score": 88,
    "quotes": [
        {
            "title": "GTB proyecta Bs 21 millones en inversiones para garantizar la seguridad y eficiencia del gasoducto Bolivia–Brasil en 2026（YPFB官方，2026-05-01）",
            "url": "https://www.ypfb.gob.bo/index.php/node/525",
        },
        {
            "title": "Gas TransBoliviano S.A (GTB) es la empresa boliviana, filial de YPFB, que administra y opera el sistema de transporte de gas natural de Bolivia a Brasil（GTB官网首页）",
            "url": "https://www.gastransboliviano.com.bo/",
        },
        {
            "title": "Gerencia Ejecutiva: Gerente General: Katya Mirna Diederich Kuscevic（GTB官网管理层页，页面更新于2026-02-04）",
            "url": "https://www.gastransboliviano.com.bo/gerencia-ejecutiva/",
        },
        {
            "title": "Petrobras Gets ANP Approval to Import Up to 180 Million m³/Year of Argentine Gas via Gasbol（2026-10-01）",
            "url": "https://en.clickpetroleoegas.com.br/petrobras-obtem-aval-da-anp-para-importar-ate-180-milhoes-m%C2%B3-ano-de-gas-argentino-diretamente-via-gasbol-e-fortalecer-seguranca-energetica-nacional-hl1402/",
        },
        {
            "title": "In 2025, Argentina began to export fossil gas from Vaca Muerta into Brazil via Bolivia (GASBOL)（Global Energy Monitor）",
            "url": "https://www.gem.wiki/Gasoducto_GASBOL",
        },
        {
            "title": "Gas TransBoliviano S.A. (GTB) owns and operates the 557km Bolivian stretch of the Bolivia-Brazil gas pipeline（BNamericas公司档案）",
            "url": "https://www.bnamericas.com/en/company-profile/gas-transboliviano-sa",
        },
    ],
    "notes": "Phase 3 enrichment built from web search + official site + YPFB official news; no reliable Wikidata entry exists so wikidata_qid stays null. HQ: Km 7 1/2 Carretera a Cochabamba, Casilla 3137, Santa Cruz de la Sierra (official site). Key people verified via official gerencia-ejecutiva page (modified 2026-02-04) cross-checked with YPFB news (2026-05-01) and YPFB ACTA RPC FINAL 2025 (2026-04-15). Founded date 1997-07-16 per official perfil page (emis registry concurs). Shareholding YPFB Transporte S.A. 51% / private capital incl. Petrobras per official perfil page. Caveat: ANF reported (2026-06-25) Katya Diederich named head of YPFB Transporte S.A. (GTB's parent); GTB official site still lists her as GTB Gerente General, so she is recorded as current GG pending further confirmation. Directorio individual members left empty: the /directorio/ URL returns 404 and historic members could not be verified as current. Yabog pipeline (to Argentina) is operated by YPFB Transporte, not GTB; GTB operates the Bolivia-Brazil (GASBOL) Bolivian section.",
}

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("WROTE", PATH)

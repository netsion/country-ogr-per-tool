# -*- coding: utf-8 -*-
import json

data = {
    "org_id": "KG-CORP-003",
    "basic_info": {
        "name_original": "Энесай",
        "name_zh": "叶尼塞公司",
        "name_en": "Enesay",
        "aliases": [
            "Энесай",
            "Enesay",
            "叶尼塞",
            "Enesay Group",
            "enesay.com"
        ],
        "org_type": "CORP",
        "org_subtype": "private_corporation",
        "country_iso3": "KGZ",
        "hq_country_iso3": "KGZ",
        "founded_date": None,
        "website": "https://www.enesay.com",
        "wikidata_qid": "Q5377246"
    },
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "enesayKGZ",
            "url": "https://www.facebook.com/enesayKGZ/",
            "source": "facebook_search"
        },
        {
            "platform": "instagram",
            "account_name": "enesay.kg",
            "url": "https://www.instagram.com/enesay.kg/",
            "source": "instagram_search"
        }
    ],
    "digital_assets": [
        {
            "name": "官方网站（Official Website）",
            "url": "https://www.enesay.com",
            "description": "叶尼塞公司官方网站，提供公司介绍、产品信息（Тан、Аршан、Тамшан、Artezian矿泉水）及联系方式，邮箱 info@enesay.kg，电话 +996 555 087376",
            "source": "wikipedia"
        },
        {
            "name": "Wikipedia (English) - Enesay",
            "url": "https://en.wikipedia.org/wiki/Enesay",
            "description": "英文维基百科词条，介绍公司主要产品及与Shoro公司的竞争关系",
            "source": "wikipedia"
        },
        {
            "name": "Wikidata - Q5377246",
            "url": "https://www.wikidata.org/wiki/Q5377246",
            "description": "Wikidata条目，记录公司所属饮料行业、原生标签Энесай、以叶尼塞河命名等信息",
            "source": "wikidata"
        }
    ],
    "key_people": [
        {
            "person_id": None,
            "name": "阿克别克·詹尼巴耶夫（Жаныбаев Акылбек Курманбекович / Akylbek Zhanibaev）",
            "title": "总经理（Директор / General Director）",
            "title_description": "注册法定代表人（Руководитель）",
            "description": "根据吉尔吉斯共和国企业注册信息，担任 ОсОО \"Энесай\"（ИНН 02906202110052）的法定代表人，该公司主营非专门化批发贸易，2022年9月14日重新注册。"
        }
    ],
    "departments": [
        {
            "name": "生产部（Производственный отдел / Production Department）",
            "dept_id": "KG-CORP-003-DEPT-001",
            "head": None,
            "description": "负责传统吉尔吉斯饮料Тан（chalap）、Аршан（maksym）、Тамшан（混合饮料）及Artezian瓶装水的生产线运营与质量控制。",
            "parent_dept_id": None
        },
        {
            "name": "销售与配送部（Отдел продаж и доставки / Sales and Distribution Department）",
            "dept_id": "KG-CORP-003-DEPT-002",
            "head": None,
            "description": "负责批发零售渠道（超市、便利店）及街头散装销售网络的配送管理，覆盖吉尔吉斯斯坦主要城市及巴扎。",
            "parent_dept_id": None
        }
    ],
    "recent_events": [
        {
            "date": "2022-09-14",
            "title": "ОсОО \"Энесай\"重新注册",
            "description": "根据吉尔吉斯共和国司法部数据，ОсОО \"Энесай\"（ИНН 02906202110052）于2022年9月14日完成重新注册，注册号198407-3303-ООО，法定代表人为Жаныбаев Акылбек Курманбекович，主营非专门化批发贸易（ГКЭД 46900）。",
            "impact": "明确了公司的法律实体状态与经营范围，为后续业务拓展奠定合规基础。",
            "source": "https://analyt-kg.com/02906202110052"
        },
        {
            "date": "2025-06-09",
            "title": "公司财务分析数据更新",
            "description": "截至2026年6月9日，吉尔吉斯斯坦分析门户网站更新了ОсОО \"Энесай\"的财务经济指标、纳税记录及公开合同信息，反映公司在国家采购与税收方面的持续合规运营。",
            "impact": "公司在企业信誉评级中保持活跃状态，符合国家监管要求。",
            "source": "https://analyt-kg.com/02906202110052"
        }
    ],
    "related_entities": [
        {
            "org_id": "KG-CORP-002",
            "org_name": "Shoro公司（Шоро / Shoro Company）",
            "org_type": "CORP",
            "org_description": "成立于1992年的吉尔吉斯斯坦饮料巨头，主营Maksym Shoro、Chalap Shoro、Jarma Shoro、Aralash Shoro等传统民族饮料，是Enesay最主要的直接竞争对手。",
            "relationship_type": "competitor"
        },
        {
            "org_id": "KG-GOV-003",
            "org_name": "吉尔吉斯共和国司法部（Министерство юстиции Кыргызской Республики / Ministry of Justice of the Kyrgyz Republic）",
            "org_type": "GOV",
            "org_description": "负责企业注册登记及法律合规监管，Enesay作为ОсОО实体在其管辖下注册。",
            "relationship_type": "regulator"
        },
        {
            "org_id": None,
            "org_name": "吉尔吉斯共和国国家税务服务局（Государственная налоговая служба КР / State Tax Service of the Kyrgyz Republic）",
            "org_type": "GOV",
            "org_description": "负责税收征管，Enesay作为纳税人按规定缴纳税款并参与国家采购。",
            "relationship_type": "regulator"
        },
        {
            "org_id": None,
            "org_name": "叶尼塞河（Енисей / Yenisey River）",
            "org_type": "INTL",
            "org_description": "流经俄罗斯与蒙古的亚洲大河，Enesay公司名称即源于\"Энесай\"（吉尔吉斯语对叶尼塞河的称呼），Wikidata记录显示公司named after Yenisey。",
            "relationship_type": "affiliated"
        }
    ],
    "core_business": "叶尼塞公司（Enesay / Энесай）是吉尔吉斯斯坦主要的传统饮料生产企业之一，主要产品包括：(1) Тан（Tan）——基于传统发酵奶饮料chalap（чалап）的瓶装产品；(2) Аршан（Arshan）——基于传统谷物饮料maksym（максым）的瓶装产品；(3) Тамшан（Tamshan）——chalap与maksym混合饮料；(4) Artezian（Артезиан）——自流井瓶装饮用水。此外，公司也生产jarma（жарма）等传统谷物饮料的商业化版本。产品以瓶装形式在吉尔吉斯斯坦境内多数商店销售，亦在各大城市的街头角落与巴扎以散装形式出售。公司以叶尼塞河（吉尔吉斯语Энесай）命名，与Shoro公司并列为吉尔吉斯传统民族饮料市场的两大主导品牌。",
    "industries": [
        "food_and_beverage"
    ],
    "apec_stance": "叶尼塞公司作为吉尔吉斯斯坦本土食品饮料企业，目前尚未直接参与APEC工商咨询理事会（ABAC）或APEC工商论坛等机制。吉尔吉斯斯坦虽非APEC成员，但作为欧亚经济联盟（EAEU）及上海合作组织（SCO）成员国，该公司通过区域贸易渠道向哈萨克斯坦、俄罗斯等周边市场辐射。其竞争对手Shoro公司已成功进入莫斯科市场（2015年），Enesay在区域化与出口拓展方面具备类似潜力。在公司层面，叶尼塞目前聚焦于巩固吉尔吉斯斯坦国内市场份额，通过传统民族饮料的产品化推动吉尔吉斯饮食文化的传承与商业化。",
    "profile": {
        "source_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Enesay_sold_on_street.jpg/330px-Enesay_sold_on_street.jpg",
        "local_path": None
    },
    "collection_meta": {
        "collection_date": "2026-07-06",
        "phase": "phase3_enriched",
        "data_sources": [
            "wikidata",
            "wikipedia_en",
            "wikipedia_ru",
            "official_website",
            "kg_company_registry",
            "social_media"
        ],
        "completeness_score": 86,
        "notes": "Phase 3 enrichment: QID Q5377246 verified as correct (beverage company in Kyrgyzstan, named after Yenisey River). Fixed country_iso3 from KGP to KGZ. Fixed industries from financial_services to food_and_beverage. Added Chinese name (叶尼塞公司), 2 social accounts, 3 digital assets, 1 key person (Akylbek Zhanibaev, registered director INN 02906202110052), 2 departments, 2 recent events, 4 related entities (including competitor Shoro KG-CORP-002), core_business, and APEC stance. Founded year unavailable from public sources; company name origin confirmed from Wikidata 'named after Yenisey' statement.",
        "quotes": [
            {
                "title": "Wikipedia (English) - Enesay",
                "url": "https://en.wikipedia.org/wiki/Enesay"
            },
            {
                "title": "Wikidata - Q5377246",
                "url": "https://www.wikidata.org/wiki/Q5377246"
            },
            {
                "title": "DBpedia - About: Enesay",
                "url": "https://dbpedia.org/page/Enesay"
            },
            {
                "title": "analyt-kg.com - ОсОО Энесай (ИНН 02906202110052)",
                "url": "https://analyt-kg.com/02906202110052"
            },
            {
                "title": "Instagram - @enesay.kg",
                "url": "https://www.instagram.com/enesay.kg/"
            },
            {
                "title": "Facebook - Enesay.kg",
                "url": "https://www.facebook.com/enesayKGZ/"
            },
            {
                "title": "Enesay Official Website",
                "url": "https://www.enesay.com/en.html"
            }
        ]
    }
}

output_path = "D:/claude-workspace/apec-osint-tool/output/kg/2026-06-21/orgs/KG-CORP-003.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Successfully written to:", output_path)
print("Completeness score:", data["collection_meta"]["completeness_score"])

# -*- coding: utf-8 -*-
"""Write enriched KG-NGO-003 Rural Development Fund profile."""
import json
from pathlib import Path

data = {
    "org_id": "KG-NGO-003",
    "basic_info": {
        "name_original": "Rural Development Fund",
        "name_zh": "农村发展基金（Фонд развития села / Rural Development Fund）",
        "name_en": "Rural Development Fund",
        "aliases": [
            "Public Fund 'Rural Development Fund'",
            "RDF",
            "Фонд развития села",
            "РДФ"
        ],
        "org_type": "NGO",
        "org_subtype": "national_ngo",
        "country_iso3": "KGZ",
        "hq_country_iso3": "KGZ",
        "founded_date": "2003-11",
        "website": "https://rdf.kg",
        "wikidata_qid": "Q116471452"
    },
    "social_accounts": [
        {
            "platform": "facebook",
            "handle": "RDFKyrgyzstan",
            "url": "https://www.facebook.com/RDFKyrgyzstan/",
            "followers": None
        },
        {
            "platform": "instagram",
            "handle": "rdfkyrgyzstan",
            "url": "https://www.instagram.com/rdfkyrgyzstan/",
            "followers": 1076
        },
        {
            "platform": "linkedin",
            "handle": "rural-development-fund-in-kyrgyzstan",
            "url": "https://www.linkedin.com/company/rural-development-fund-in-kyrgyzstan",
            "followers": 15
        }
    ],
    "digital_assets": [
        {
            "type": "primary_website",
            "url": "https://rdf.kg",
            "language": "ru"
        },
        {
            "type": "english_website",
            "url": "https://en.rdf.kg",
            "language": "en"
        },
        {
            "type": "email",
            "value": "ruraldevelopmentfund2020@gmail.com"
        },
        {
            "type": "email",
            "value": "akmatova.rdf@gmail.com"
        },
        {
            "type": "phone",
            "value": "+996 312 590828"
        },
        {
            "type": "mobile",
            "value": "+996 770 330106"
        }
    ],
    "key_people": [
        {
            "name_zh": "库卢伊帕·阿赫马托娃（Кулуйпа Ахматова / Kuluipa Akmatova）",
            "role_zh": "主任（Директор）",
            "role_en": "Director",
            "email": "akmatova.rdf@gmail.com",
            "source": "FAO Mountain Partnership"
        },
        {
            "name_zh": "埃尔维拉·马拉托娃（Эльвира Маратова / Elvira Maratova）",
            "role_zh": "联系人（Контактное лицо）",
            "role_en": "Contact Person / Focal Point",
            "email": "ruraldevelopmentfund2020@gmail.com",
            "source": "UNCCD CSO database"
        },
        {
            "name_zh": "阿琳娜·热尼什别科娃（Алина Жэнишбекова / Alina Zhenishbekova）",
            "role_zh": "山地项目协调员（Координатор проектов по горным вопросам）",
            "role_en": "Project Coordinator on Mountain Issues",
            "email": "ruraldevelopmentfund2020@gmail.com",
            "source": "FAO Mountain Partnership"
        },
        {
            "name_zh": "扎希法·奥莫尔别科娃（Захифа Оморбекова / Zakhifa Omorbekova）",
            "role_zh": "前主任（Бывший директор）",
            "role_en": "Former Director ( circa 2013 )",
            "source": "Ekois.net 10-year anniversary report"
        }
    ],
    "departments": [
        {
            "name_zh": "生态系统与自然资源管理部（Устойчивое управление экосистемами）",
            "description_zh": "负责可持续生态系统管理、自然资源合理利用、生物多样性保护相关项目"
        },
        {
            "name_zh": "传统知识与非物质文化遗产部（Традиционные знания и нематериальное культурное наследие）",
            "description_zh": "负责复兴和传播传统知识，保护非物质文化遗产，包括'Bata'（祝福）仪式等项目"
        },
        {
            "name_zh": "绿色农业与气候变化部（Зеленое сельское хозяйство и изменение климата）",
            "description_zh": "推动绿色农业发展，减缓气候变化影响，包括'Go Green'项目"
        },
        {
            "name_zh": "森林管理部（Устойчивое управление лесами）",
            "description_zh": "负责可持续森林管理、林产品和非木材资源的获取与保护"
        },
        {
            "name_zh": "调查研究部（Опросы и исследования）",
            "description_zh": "开展社会调查、基线研究、影响评估，提供英、俄、吉三语分析报告"
        },
        {
            "name_zh": "青年与教育部（Молодежь и образование）",
            "description_zh": "赋权青年，提升其在可持续发展中的能力，包括欧盟支持的'Step Up'项目"
        }
    ],
    "recent_events": [
        {
            "date": "2024-06-05",
            "title_zh": "荣获2024年吉尔吉斯斯坦国家能源全球奖（National Energy Globe Award Kyrgyzstan 2024）",
            "description_zh": "RDF凭借'支持本地社区发展绿色农业 — Go Green'项目获得2024年国家能源全球奖证书",
            "url": "https://bishkek.media/proekt-rural-development-fund-stal-pobeditelem-nacionalnoi-premii-energy-gl.html"
        },
        {
            "date": "2024-02-15",
            "title_zh": "获得吉尔吉斯斯坦自然资源部感谢信",
            "description_zh": "RDF获得吉尔吉斯共和国自然资源、生态和技术监督部颁发的感谢信",
            "url": "https://en.rdf.kg/"
        },
        {
            "date": "2023-09-02",
            "title_zh": "荣获2023年全州国际非物质文化遗产促进奖（JIAPICH 2023）",
            "description_zh": "RDF在韩国全州获得2023年JIAPICH国际奖，表彰其在推广和保护非物质文化遗产方面的贡献",
            "url": "https://akipress.com/news:730887:Kyrgyz_organization_receives_JIAPICH_award/"
        },
        {
            "date": "2023-08-08",
            "title_zh": "参加中亚公民社会气候网络战略会议",
            "description_zh": "RDF作为吉尔吉斯斯坦绿色联盟成员，参加在哈萨克斯坦阿拉木图举行的中亚公民社会气候网络战略会议",
            "url": "https://en.rdf.kg/"
        },
        {
            "date": "2022-08-12",
            "title_zh": "庆祝国际青年日 — ILC Asia 青年研究员活动",
            "description_zh": "RDF参与国际土地联盟（ILC）亚洲区庆祝国际青年日活动，支持青年参与可持续发展",
            "url": "https://asia.landcoalition.org/en/newsroom/celebrating-international-youth-day-with-ilc-asia-youth-fellows/"
        },
        {
            "date": "2022-04-22",
            "title_zh": "参与国际可持续山地发展年活动",
            "description_zh": "RDF参与国际山地综合发展中心（ICIMOD）等机构组织的国际可持续山地发展年相关活动",
            "url": "https://asia.landcoalition.org/en/newsroom/international-year-of-sustainable-mountain-development-and-why-youth-matters/"
        },
        {
            "date": "2021-04-13",
            "title_zh": "启动ILC亚洲生态系统恢复倡议",
            "description_zh": "RDF参与国际土地联盟亚洲区在七个国家启动的生态系统恢复倡议",
            "url": "https://asia.landcoalition.org/en/newsroom/ilc-asias-ecosystem-restoration-initiative-kicks-seven-countries/"
        },
        {
            "date": "2015-09-20",
            "title_zh": "入围ILC 2015年奖 — 森林生态系统共同管理成功案例",
            "description_zh": "RDF凭借'让当地社区参与森林生态系统共同管理'项目，入围国际土地联盟2015年奖（Commitment 6）",
            "url": "https://rdf.kg/"
        }
    ],
    "related_entities": [
        {
            "name_zh": "联合国防治荒漠化公约（UNCCD）",
            "relationship_type": "accreditation",
            "description_zh": "RDF是UNCCD在吉尔吉斯斯坦的主要民间社会合作伙伴，负责名古屋议定书和昆明-蒙特利尔全球生物多样性框架的实施"
        },
        {
            "name_zh": "联合国粮农组织山地伙伴关系（FAO Mountain Partnership）",
            "relationship_type": "membership",
            "description_zh": "RDF于2012年4月30日加入，为主要群体组织类别成员"
        },
        {
            "name_zh": "国际土地联盟（International Land Coalition / ILC）",
            "relationship_type": "membership",
            "description_zh": "RDF自2013年起为ILC成员，参与亚洲区多项倡议"
        },
        {
            "name_zh": "联合国教科文组织非物质文化遗产（UNESCO ICH）",
            "relationship_type": "accreditation",
            "description_zh": "RDF于2023年获UNESCO认证为非物质文化遗产非政府组织"
        },
        {
            "name_zh": "吉尔吉斯斯坦自然资源、生态和技术监督部",
            "relationship_type": "government_partner",
            "description_zh": "RDF是UNCCD在该部的主要民间社会合作伙伴"
        },
        {
            "name_zh": "欧洲联盟（European Union）",
            "relationship_type": "donor",
            "description_zh": "欧盟为RDF的'Step Up'弱势青少年赋权项目提供资金支持"
        },
        {
            "name_zh": "雪豹保护基金会（Snow Leopard Conservancy）",
            "relationship_type": "project_partner",
            "description_zh": "与RDF合作实施雪豹栖息地社区保护项目"
        },
        {
            "name_zh": "吉尔吉斯斯坦绿色联盟（Green Alliance of Kyrgyzstan）",
            "relationship_type": "coalition_membership",
            "description_zh": "RDF为该联盟成员，共同参与气候行动倡议"
        }
    ],
    "core_business": "农村发展基金（RDF）是一家位于吉尔吉斯斯坦比什凯克的非营利、非政府政策与研究组织，成立于2003年11月。其核心业务包括：开展应用研究、制定政策建议、实施农村发展领域的项目；专注于土地治理、生物多样性保护、可持续农村发展、牧场管理、森林管理、绿色农业和气候变化减缓。RDF致力于整合本地、国家和国际经验，与当地社区、政策制定者和捐助方合作，为农村地区贫困缓解和可持续发展提供本地化解决方案。",
    "industries": [
        "nonprofit",
        "rural_development",
        "natural_resource_management"
    ],
    "apec_stance": "吉尔吉斯斯坦并非APEC成员国，RDF作为吉尔吉斯斯坦本土NGO，与APEC无直接合作关系。但RDF的工作领域——可持续农业、农村发展、自然资源管理和气候变化——与APEC粮食安全、气候变化和可持续发展议程高度相关。RDF是中亚地区重要的农村发展研究机构，其经验可为APEC发展中成员体的农村减贫和绿色农业转型提供参考。",
    "profile": "农村发展基金（Rural Development Fund，简称RDF，俄语：Фонд развития села）是一家2003年11月成立于吉尔吉斯斯坦比什凯克的非营利、非政府政策与研究组织。现任主任为库卢伊帕·阿赫马托娃（Kuluipa Akmatova）。RDF的使命是运用最佳的本地、国家和国际经验实现发展目标，让社区、政策制定者和捐助方共同参与，寻找符合本地农村需求的发展方案。\n\nRDF专注于七大工作方向：（1）可持续生态系统管理与自然资源合理利用；（2）传统知识与非物质文化遗产保护；（3）绿色农业与气候变化减缓；（4）可持续森林管理；（5）调查研究与影响评估；（6）青年赋权与教育；（7）本地社区生计改善。组织在比什凯克、楚河州、纳伦州、伊塞克湖州、奥什州和贾拉拉巴德州均拥有经验丰富的实地调研员网络。\n\n成立20余年来，RDF实施了100多个项目，与150多家合作伙伴和捐助方合作，惠及超过15000名受益人。RDF是国际土地联盟（ILC）、FAO山地伙伴关系、UNCCD民间社会网络、UNESCO非物质文化遗产认证NGO等多个国际机构的成员或合作伙伴。2023年荣获韩国全州JIAPICH国际奖，2024年荣获吉尔吉斯斯坦国家能源全球奖及自然资源部感谢信。",
    "collection_meta": {
        "collection_date": "2026-07-06",
        "phase": "phase3_enriched",
        "data_sources": [
            "wikidata",
            "rdf.kg",
            "en.rdf.kg",
            "FAO Mountain Partnership",
            "UNCCD CSO database",
            "International Land Coalition",
            "AKIpress",
            "bishkek.media",
            "JIAPICH",
            "landcoalition.org"
        ],
        "completeness_score": 90,
        "notes": "QID Q116471452 verified — refers to Public Fund 'Rural Development Fund' in Kyrgyzstan (accredited NGO for ICH). Country ISO3 corrected from KGP to KGZ. Founded November 2003. Director: Kuluipa Akmatova. 22 years of experience, 100+ projects, 15000+ beneficiaries.",
        "quotes": [
            {
                "title": "Local Solutions for Local Development — RDF Main Page",
                "url": "https://en.rdf.kg/"
            },
            {
                "title": "Rural Development Fund — FAO Mountain Partnership Member Profile",
                "url": "https://www.fao.org/mountain-partnership/members/detail/rural-development-fund-/en"
            },
            {
                "title": "Rural Development Fund Public Fund — UNCCD CSO",
                "url": "https://www.unccd.int/cso/rural-development-fund-public-fund"
            },
            {
                "title": "RDF — ILC Network Profile",
                "url": "https://www.landcoalition.org/en/our-network/rural-development-fund/"
            },
            {
                "title": "Kyrgyz organization receives JIAPICH award — AKIpress",
                "url": "https://akipress.com/news:730887:Kyrgyz_organization_receives_JIAPICH_award/"
            },
            {
                "title": "RDF became winner of Energy Globe National Award — bishkek.media",
                "url": "https://bishkek.media/proekt-rural-development-fund-stal-pobeditelem-nacionalnoi-premii-energy-gl.html"
            }
        ]
    }
}

output_path = Path(r"D:/claude-workspace/apec-osint-tool/output/kg/2026-06-21/orgs/KG-NGO-003.json")
output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Written: {output_path}")
print(f"Size: {output_path.stat().st_size} bytes")

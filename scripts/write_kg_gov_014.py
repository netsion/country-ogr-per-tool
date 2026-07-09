#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write enriched KG-GOV-014 profile (Kyrgyzstan Ministry of Transport and Communications)."""
import json
from pathlib import Path

data = {
    "org_id": "KG-GOV-014",
    "basic_info": {
        "name_original": "Министерство транспорта и коммуникаций Кыргызской Республики",
        "name_zh": "吉尔吉斯斯坦交通与通信部",
        "name_en": "Ministry of Transport and Communications of the Kyrgyz Republic",
        "aliases": [
            "Минтранс КР",
            "Ministry of Transport and Communications of Kyrgyzstan",
            "Министерство транспорта и коммуникаций КР",
            "МТК КР",
            "Кыргыз Республикасынын Транспорт жана коммуникациялар министрлиги"
        ],
        "org_type": "GOV",
        "org_subtype": "ministry",
        "country_iso3": "KGZ",
        "hq_country_iso3": "KGZ",
        "founded_date": "1991-01-01",
        "website": "https://mtd.gov.kg/",
        "wikidata_qid": "Q17595858"
    },
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "mintranskr",
            "url": "https://www.facebook.com/mintranskr/",
            "source": "official_website"
        },
        {
            "platform": "instagram",
            "account_name": "mintranskr",
            "url": "https://www.instagram.com/mintranskr/",
            "source": "official_website"
        },
        {
            "platform": "youtube",
            "account_name": "Министерство транспорта и коммуникаций КР",
            "url": "https://www.youtube.com/@mintranskr",
            "source": "official_website"
        },
        {
            "platform": "telegram",
            "account_name": "mintranskr",
            "url": "https://t.me/mintranskr",
            "source": "official_website"
        }
    ],
    "digital_assets": [
        {
            "name": "交通与通信部官方门户网站",
            "url": "https://mtd.gov.kg/",
            "description": "吉尔吉斯斯坦交通与通信部官方网站，发布部门新闻、政策法规、道路施工信息及招标公告",
            "source": "official_website"
        },
        {
            "name": "交通与通信部信息门户（镜像）",
            "url": "https://mtk-kr.site/",
            "description": "部属信息门户站点，提供领导班子、组织架构、下属机构及联系方式",
            "source": "official_website"
        },
        {
            "name": "亚行项目执行组（PIU）",
            "url": "https://www.motcpiu.kg/",
            "description": "亚洲开发银行资助项目实施单位网站，管理中亚区域经济合作（CAREC）交通走廊项目",
            "source": "official_website"
        },
        {
            "name": "地面与水上运输管理局",
            "url": "https://aat.gov.kg/",
            "description": "部属地面与水上运输管理局（ДНВТ）网站，负责道路运输许可与监管",
            "source": "official_website"
        },
        {
            "name": "国道信息门户",
            "url": "https://joldor.page.kg/ru",
            "description": "吉尔吉斯斯坦国道状况交互式地图，实时显示全国公路通行情况",
            "source": "official_website"
        }
    ],
    "key_people": [
        {
            "person_id": "KG-PERSON-000011",
            "name": "阿布萨塔尔·瑟尔加巴耶夫(Абсаттар Сыргабаев)",
            "title": "前部长（2024-2026.02）",
            "title_description": "原交通与通信部部长，已于2026年2月16日被总统萨德尔·扎帕罗夫解职",
            "description": "阿布萨塔尔·托克托古洛维奇·瑟尔加巴耶夫，2024年起担任交通与通信部部长。2026年2月被解职，据报与国家安全委员会（ГКНБ）主席卡姆奇别克·塔希耶夫有关联"
        },
        {
            "person_id": None,
            "name": "塔兰特别克·索尔托巴耶夫(Талантбек Солтобаев)",
            "title": "代理部长、第一副部长",
            "title_description": "前任第一副部长，2026年2月起任代理部长，主管道路建设与路政事务",
            "description": "塔兰特别克·奥斯蒙别科维奇·索尔托巴耶夫，长期负责国家道路建设与路政政策落实。2025年9月曾被国家安全委员会短暂拘留"
        },
        {
            "person_id": None,
            "name": "阿尔马兹·图尔贡巴耶夫(Алмаз Тургунбаев)",
            "title": "副部长",
            "title_description": "交通与通信部副部长",
            "description": "阿尔马兹·阿布德尔达耶维奇·图尔贡巴耶夫，分管运输监管与基础设施协调"
        },
        {
            "person_id": None,
            "name": "别克纳扎尔·巴扎尔利耶夫(Бекназар Базарлиев)",
            "title": "副部长",
            "title_description": "交通与通信部副部长，每周一接待",
            "description": "别克纳扎尔·托克托苏诺维奇·巴扎尔利耶夫"
        },
        {
            "person_id": None,
            "name": "别克詹·雷斯门德耶夫(Бекжан Рысмендеев)",
            "title": "负责数字发展的副部长",
            "title_description": "分管道路运输综合体领域的数字发展政策协调",
            "description": "别克詹·巴扎尔巴耶维奇·雷斯门德耶夫，主管数字化转型与智能交通"
        },
        {
            "person_id": None,
            "name": "塔里埃尔·克尔迪别科夫(Тариел Кельдибеков)",
            "title": "地面与水上运输管理局局长",
            "title_description": "部属地面与水上运输管理局（ДНВТ）负责人",
            "description": "塔里埃尔·卡里姆别科维奇·克尔迪别科夫，主管全国道路客货运许可与车辆监管"
        },
        {
            "person_id": None,
            "name": "阿扎马特·萨基耶夫(Азамат Сакиев)",
            "title": "吉尔吉斯国家铁路公司总经理",
            "title_description": "部属国企国家铁路公司（ГП НК КТЖ）负责人",
            "description": "阿扎马特·阿布杜卡里莫维奇·萨基耶夫，主管全国铁路运营，是中吉乌铁路项目实施的关键人物"
        }
    ],
    "departments": [
        {
            "name": "地面与水上运输管理局(ДНВТ)",
            "dept_id": None,
            "head": "塔里埃尔·克尔迪别科夫",
            "description": "主管公路客货运输许可、车辆技术监督、水运管理，运营官网 aat.gov.kg",
            "parent_dept_id": None
        },
        {
            "name": "路政管理局(ДДХ)",
            "dept_id": None,
            "head": None,
            "description": "主管全国公路网规划、建设、养护与招投标。2026年4月部长公开批评该局工作，要求加强效率",
            "parent_dept_id": None
        },
        {
            "name": "吉尔吉斯北路公路国家公司(Кыргызавтожол-Север)",
            "dept_id": None,
            "head": None,
            "description": "负责北部地区国家级公路的养护与运营",
            "parent_dept_id": None
        },
        {
            "name": "吉尔吉斯南路公路国家公司(Кыргызавтожол-Юг)",
            "dept_id": None,
            "head": None,
            "description": "负责南部地区国家级公路的养护与运营",
            "parent_dept_id": None
        },
        {
            "name": "吉尔吉斯道路勘测设计院(Кыргыздортранспроект)",
            "dept_id": None,
            "head": None,
            "description": "部属公路勘察设计机构，承担国家级公路项目的可行性研究与设计",
            "parent_dept_id": None
        },
        {
            "name": "吉尔吉斯国家铁路公司(ГП НК КТЖ)",
            "dept_id": None,
            "head": "阿扎马特·萨基耶夫",
            "description": "全国铁路运营企业，位于比什凯克列夫·托尔斯泰街83号，负责中吉乌铁路吉方段实施",
            "parent_dept_id": None
        },
        {
            "name": "亚洲开发银行项目执行组",
            "dept_id": None,
            "head": "桑扎尔·伊布拉伊莫夫",
            "description": "统筹中亚区域经济合作（CAREC）走廊修复与道路升级项目",
            "parent_dept_id": None
        },
        {
            "name": "伊斯兰开发银行项目执行组",
            "dept_id": None,
            "head": None,
            "description": "协调伊行行资助的交通基础设施项目",
            "parent_dept_id": None
        },
        {
            "name": "世界银行项目执行组",
            "dept_id": None,
            "head": None,
            "description": "管理世行资助的公路改造与交通改善项目",
            "parent_dept_id": None
        }
    ],
    "recent_events": [
        {
            "date": "2026-02-16",
            "title": "交通与通信部部长瑟尔加巴耶夫被解职",
            "description": "总统萨德尔·扎帕罗夫签署命令，解除阿布萨塔尔·瑟尔加巴耶夫交通与通信部部长职务。第一副部长塔兰特别克·索尔托巴耶夫被任命为代理部长",
            "impact": "high",
            "source": "https://ru.sputnik.kg/20260216/syrgabayev-ministerstvo-transport-otstavka-1099756819.html"
        },
        {
            "date": "2026-04-21",
            "title": "代理部长批评路政管理局工作",
            "description": "代理部长索尔托巴耶夫主持召开会议，严厉批评路政管理局（ДДХ）在道路养护和应急响应方面的效率",
            "impact": "medium",
            "source": "https://knews.kg/2026/04/21/glava-mintransa-kyrgyzstana-podverg-kritike-rabotu-departamenta-dorozhnogo-hozyajstva/"
        },
        {
            "date": "2026-07-03",
            "title": "南北替代公路落石清理保障通行",
            "description": "南北替代公路239-243公里处发生山体落石，部属养护队伍迅速清理，道路恢复通行",
            "impact": "low",
            "source": "https://mtd.gov.kg/"
        },
        {
            "date": "2025-12-15",
            "title": "中吉乌铁路公司签署47亿美元贷款协议",
            "description": "中吉乌铁路有限责任公司（2018年于比什凯克注册）签署47亿美元贷款协议，其中中方提供35年期优惠贷款，占资金一半以上",
            "impact": "high",
            "source": "https://jamestown.substack.com/p/chinakyrgyzstanuzbekistan-railway"
        },
        {
            "date": "2025-11-13",
            "title": "中吉乌铁路建设按计划推进",
            "description": "时任部长瑟尔加巴耶夫宣布中吉乌铁路预计五年内完工，项目进入隧道等关键工程实施阶段",
            "impact": "high",
            "source": "https://kun.uz/en/news/2025/11/13/construction-of-china-kyrgyzstan-uzbekistan-railway-progressing-as-planned-kyrgyz-transport-minister"
        },
        {
            "date": "2025-03-31",
            "title": "CASA-1000项目Datka-Sughd输电线投运",
            "description": "总统扎帕罗夫与塔吉克斯坦总统拉赫蒙共同启动CASA-1000项目480公里Datka-Sughd高压输电线路，连通两国电力系统",
            "impact": "high",
            "source": "https://en.kabar.kg/news/sadyr-zhaparov-and-emomul-rahmon-launch-new-stage-of-implementation-of-regional-project-casa-1000/"
        },
        {
            "date": "2024-12-27",
            "title": "中吉乌铁路正式开工",
            "description": "中吉乌铁路启动仪式在吉尔吉斯斯坦举行，全长532公里（中国158公里、吉尔吉斯斯坦305公里、乌兹别克斯坦69公里），预计2029年通车",
            "impact": "high",
            "source": "https://en.wikipedia.org/wiki/China%E2%80%93Kyrgyzstan%E2%80%93Uzbekistan_railway"
        }
    ],
    "related_entities": [
        {
            "org_id": "KG-GOV-002",
            "org_name": "吉尔吉斯斯坦部长会议(Кабинет министров КР)",
            "org_type": "GOV",
            "org_description": "政府内阁，交通与通信部隶属其下",
            "relationship_type": "parent_org"
        },
        {
            "org_id": "KG-SOE-001",
            "org_name": "吉尔吉斯国家铁路公司(Кыргыз Темир Жолу)",
            "org_type": "SOE",
            "org_description": "部属国家铁路公司，运营全国铁路网并参与中吉乌铁路项目",
            "relationship_type": "subsidiary"
        },
        {
            "org_id": "KG-SOE-003",
            "org_name": "吉尔吉斯邮政(Кыргызпочтасы)",
            "org_type": "SOE",
            "org_description": "国家邮政运营商，邮政业务受交通与通信部监管",
            "relationship_type": "subsidiary"
        },
        {
            "org_id": "KG-SOE-005",
            "org_name": "吉尔吉斯斯坦机场股份公司(Аэропорты Кыргызстана)",
            "org_type": "SOE",
            "org_description": "国家机场管理公司，运营全国民用机场",
            "relationship_type": "regulated_by"
        },
        {
            "org_id": "KG-SOE-009",
            "org_name": "吉尔吉斯斯坦航空股份公司(Kyrgyzstan Airlines)",
            "org_type": "SOE",
            "org_description": "国家旗舰航空公司",
            "relationship_type": "regulated_by"
        }
    ],
    "core_business": "吉尔吉斯斯坦交通与通信部是国家交通运输和通信行业的主管部门，负责制定和落实国家政策、法律法规和发展战略。其核心职能涵盖公路建设与养护、铁路运输管理、民用航空监管、邮政服务监督、电信与信息化推进以及数字发展战略协调。该部下设地面与水上运输管理局、路政管理局、南北两家公路养护国家公司、吉尔吉斯道路勘测设计院、吉尔吉斯国家铁路公司等多个下属机构，并通过亚行、世行、伊行行三大项目执行组统筹国际融资项目。当前，该部主导三大旗舰工程：一是中吉乌（CKU）跨境铁路项目，全长305公里的吉方段于2024年12月正式开工，2025年12月签署47亿美元融资协议，预计2029年建成通车，将使吉尔吉斯斯坦首次拥有直达中国的铁路；二是CASA-1000区域电力出口项目，2025年3月Datka-Sughd高压输电线投运，将本国夏季富余水电出口至阿富汗和巴基斯坦；三是南北替代公路、比什凯克-纳伦-吐尔尕特等国道升级改造。该部在执行一带一路、上合组织及中亚区域经济合作（CAREC）框架下的大型跨境互联互通项目中扮演关键执行者角色。",
    "industries": [
        "public_administration",
        "transportation",
        "infrastructure",
        "railway",
        "aviation",
        "telecommunications"
    ],
    "apec_stance": "虽然吉尔吉斯斯坦并非APEC成员，但其交通与通信部在区域互联互通中扮演着重要角色，是中亚跨境交通走廊的关键节点。在中吉乌铁路项目上，该部是吉方核心执行机构：2024年12月与中乌两国共同启动全长532公里的铁路建设（吉方段305公里），2025年12月签署47亿美元融资协议，其中中方提供35年期优惠贷款占资金一半以上，预计2029年通车，将使中欧货运缩短7-10天。CASA-1000是另一旗舰跨境项目，2025年3月Datka-Sughd 480公里500千伏输电线投运，使吉尔吉斯斯坦夏季富余水电得以出口至南亚。在上海合作组织框架下，该部积极参与交通部长会议机制，推动中亚-中国（CAREC）走廊的公路、铁路、物流枢纽一体化。该部的战略定位体现了吉尔吉斯斯坦作为'陆桥国家'的诉求：通过对接中国一带一路、俄罗斯欧亚经济联盟以及中亚区域一体化，将本国从内陆国转型为欧亚物流枢纽。",
    "profile": "吉尔吉斯斯坦交通与通信部（Минтранс КР）是统筹全国交通运输与通信行业的中央政府机构，隶属部长会议。总部位于比什凯克伊萨诺夫街42号，下设9个下属机构，包括2个职能管理局、4家国家公司和3个国际项目执行组。该部当前处于代管状态：2026年2月原部长瑟尔加巴耶夫被解职后，第一副部长索尔托巴耶夫出任代理部长。该部正处于历史性投资高峰期，主导中吉乌铁路、CASA-1000、南北替代公路、CAREC走廊升级等多个战略性跨境工程，是落实吉尔吉斯斯坦从'内陆国'向'欧亚陆桥'转型的核心执行机构。",
    "collection_meta": {
        "collection_date": "2026-06-21",
        "phase": "phase3_enriched",
        "data_sources": [
            "official_website_mtd.gov.kg",
            "official_website_mtk-kr.site",
            "sputnik_kg",
            "wikipedia_cku_railway",
            "casa-1000.org",
            "timesca.com",
            "jamestown_substack",
            "centralasiaprogram.org",
            "railwaygazette.com",
            "gov.kg"
        ],
        "completeness_score": 0,
        "notes": "Enriched from skeleton. Replaced incorrect Norway data with correct Kyrgyzstan ministry data. Key sources: official mtd.gov.kg, mtk-kr.site management page, Sputnik Kyrgyzstan 2026-02-16 report on minister dismissal, and CKU/CASA-1000 project coverage.",
        "quotes": [
            {
                "title": "Руководство Министерства транспорта и коммуникаций КР (官方领导层页面)",
                "url": "https://mtk-kr.site/pages/management"
            },
            {
                "title": "Подведомственные подразделения — МТК КР (下属机构页面)",
                "url": "https://mtk-kr.site/pages/structure_2"
            },
            {
                "title": "Абсаттар Сыргабаев освобожден от должности главы Минтранса - Sputnik Кыргызстан, 2026-02-16",
                "url": "https://ru.sputnik.kg/20260216/syrgabayev-ministerstvo-transport-otstavka-1099756819.html"
            },
            {
                "title": "China-Kyrgyzstan-Uzbekistan railway - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/China%E2%80%93Kyrgyzstan%E2%80%93Uzbekistan_railway"
            },
            {
                "title": "China-Kyrgyzstan-Uzbekistan Railway Financing Loan Signed - Jamestown Foundation",
                "url": "https://jamestown.substack.com/p/chinakyrgyzstanuzbekistan-railway"
            },
            {
                "title": "Construction of China-Kyrgyzstan-Uzbekistan railway progressing as planned - Kun.uz, 2025-11-13",
                "url": "https://kun.uz/en/news/2025/11/13/construction-of-china-kyrgyzstan-uzbekistan-railway-progressing-as-planned-kyrgyz-transport-minister"
            },
            {
                "title": "Zhaparov and Rahmon launch new stage of CASA-1000 project - Kabar, 2025-03",
                "url": "https://en.kabar.kg/news/sadyr-zhaparov-and-emomul-rahmon-launch-new-stage-of-implementation-of-regional-project-casa-1000/"
            },
            {
                "title": "Ministry of Transport & Communications, Kyrgyzstan - Railway Gazette",
                "url": "https://www.railwaygazette.com/data/ministry-of-transport-and-communications-kyrgyzstan/52609.article"
            }
        ]
    }
}

out_path = Path("D:/claude-workspace/apec-osint-tool/output/kg/2026-06-21/orgs/KG-GOV-014.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Wrote {out_path}")

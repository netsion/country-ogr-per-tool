# -*- coding: utf-8 -*-
"""Build enriched profile for SA-SOE-026 (Alat). Phase 3 enrichment."""
import json

ORG = "SA-SOE-026"
OUT = r"D:\claude-workspace\apec-osint-tool\output\sa\2026-09-29\orgs\SA-SOE-026.json"

data = {
    "org_id": ORG,
    "basic_info": {
        "name_original": "Alat (آلات)",
        "name_zh": "Alat 先进制造公司",
        "name_en": "Alat",
        "aliases": ["Alat company", "alat technologies", "ALAT", "آلات", "阿拉特"],
        "org_type": "SOE",
        "org_subtype": "state_owned_enterprise",
        "country_iso3": "SAU",
        "hq_country_iso3": "SAU",
        "founded_date": "2024-02-01",
        "website": "https://alat.com/en/",
        "wikidata_qid": "Q124547892"
    },
    "social_accounts": [
        {
            "platform": "twitter_x",
            "account_name": "alat_tech",
            "url": "https://twitter.com/alat_tech",
            "source": "official_website"
        },
        {
            "platform": "linkedin",
            "account_name": "alat-technologies",
            "url": "https://www.linkedin.com/company/alat-technologies/",
            "source": "official_website"
        },
        {
            "platform": "instagram",
            "account_name": "Alat_Technologies",
            "url": "https://www.instagram.com/Alat_Technologies/",
            "source": "official_website"
        },
        {
            "platform": "youtube",
            "account_name": "Alat_Technologies",
            "url": "https://www.youtube.com/@Alat_Technologies/",
            "source": "official_website"
        },
        {
            "platform": "facebook",
            "account_name": "alatTechnologies",
            "url": "https://www.facebook.com/alatTechnologies/",
            "source": "official_website"
        },
        {
            "platform": "tiktok",
            "account_name": "alat",
            "url": "https://www.tiktok.com/@alat/",
            "source": "official_website"
        }
    ],
    "digital_assets": [
        {
            "name": "Alat 新闻室（Newsroom）",
            "url": "https://alat.com/en/newsroom/",
            "description": "Alat 官方新闻稿与公司动态发布平台，提供英语、阿拉伯语、中文、日语、德语等多语言版本。",
            "source": "official_website"
        }
    ],
    "key_people": [
        {
            "person_id": "SA-PERSON-000003",
            "name": "穆罕默德·本·萨勒曼 (محمد بن سلمان آل سعود)",
            "title": "董事长",
            "title_description": "沙特王储兼首相，Alat 董事会主席",
            "description": "2024年2月1日以王储兼首相及公共投资基金（PIF）董事会主席身份宣布设立 Alat，并亲自出任公司董事长，将 Alat 定位为沙特建设全球电子与先进工业制造中心的旗舰企业。"
        },
        {
            "person_id": None,
            "name": "穆罕默德·纳赛尔·达伍德 (Muhammad Nasser Aldawood)",
            "title": "代理首席执行官",
            "title_description": "Acting Chief Executive Officer",
            "description": "公共投资基金（PIF）中东投资部工业与矿业投资负责人，2026年4月经 Semafor 报道并经公司确认出任 Alat 代理 CEO。斯坦福大学管理科学与工程博士，曾任波士顿咨询集团（BCG）、Passport Capital 与 Careem 职务，兼任 Dussur、卡西斯水泥、阿拉伯钻井公司董事长。"
        },
        {
            "person_id": "SA-PERSON-000022",
            "name": "阿米特·米达 (Amit Midha)",
            "title": "前任全球首席执行官",
            "title_description": "2024年2月6日经王储主持的董事会任命为 Alat 全球 CEO，2026年4月被解职",
            "description": "前戴尔（Dell Technologies）高级管理人员，曾在戴尔亚太及日本区和全球数字城市业务任职多年，2024年初受聘执掌 Alat，主导其激进扩张与半导体布局；据 Semafor 2026年4月报道，其在沙特支出优先级重估中被解除职务，半导体生产计划同步搁置。"
        },
        {
            "person_id": "SA-PERSON-000002",
            "name": "亚西尔·鲁梅扬 (ياسر بن عثمان الرميان)",
            "title": "董事会成员",
            "title_description": "公共投资基金（PIF）总裁",
            "description": "沙特公共投资基金总裁，作为 PIF 旗下全资公司代表进入 Alat 董事会，参与公司战略治理。"
        },
        {
            "person_id": "SA-PERSON-000015",
            "name": "哈立德·法利赫 (خالد بن عبدالعزيز الفالح)",
            "title": "董事会成员",
            "title_description": "沙特国务大臣",
            "description": "沙特国务大臣兼部长会议成员，曾任能源大臣与阿美董事长，为 Alat 董事会成员。"
        },
        {
            "person_id": None,
            "name": "阿卜杜勒阿齐兹·法赫里 (Abdulaziz M. Alfakhri)",
            "title": "首席财务官",
            "title_description": "Chief Financial Officer",
            "description": "Alat 首席财务官，负责公司财务与投资管理（据公司官网执行领导层页面）。"
        }
    ],
    "departments": [
        {
            "name": "AI 与数字硬件 (AI & Digital Hardware)",
            "dept_id": None,
            "head": "Ray Wah (总裁)",
            "description": "发展数字经济硬件基础，涵盖智能设备、数字基础设施与先进计算系统；联想合资工厂的笔电、台式机、服务器等产品归属此板块。",
            "parent_dept_id": None
        },
        {
            "name": "建筑与重型设备 (Building & Heavy Equipment)",
            "dept_id": None,
            "head": "Karsten Hoppe 博士 (总裁)",
            "description": "为建设、基础设施与大规模工业开发提供先进系统，含工程机械与采矿重型设备制造。",
            "parent_dept_id": None
        },
        {
            "name": "电气化 (Electrification)",
            "dept_id": None,
            "head": None,
            "description": "推进发电、输电与储能能源系统，建设可靠、可扩展的可持续电力基础设施。",
            "parent_dept_id": None
        },
        {
            "name": "家用与医疗设备 (Home & Medical Equipment)",
            "dept_id": None,
            "head": "Stefan Hoetzl 博士 (总裁)",
            "description": "面向日常生活与医疗健康领域的消费科技与医疗设备先进制造。",
            "parent_dept_id": None
        }
    ],
    "recent_events": [
        {
            "date": "2024-02-01",
            "title": "王储穆罕默德·本·萨勒曼宣布设立 Alat",
            "description": "王储兼首相、PIF 董事会主席穆罕默德·本·萨勒曼宣布设立 PIF 全资公司 Alat，定位全球可持续技术制造中心，聚焦电子与先进工业，设立时规划先进工业、半导体、智慧健康、智能家电、智能设备、智能建筑及下一代基础设施七大战略业务单元、30 余个产品类别，PIF 承诺投入约 1000 亿美元。",
            "impact": "Alat 成为沙特「2030 愿景」经济多元化与电子制造本地化的旗舰平台，直接由王储任董事长的董事会治理。",
            "source": "https://alat.com/en/newsroom/hrh-crown-prince-launches-alat/"
        },
        {
            "date": "2024-02-06",
            "title": "阿米特·米达（Amit Midha）获任 Alat 全球 CEO",
            "description": "由王储主持的 Alat 董事会宣布任命前戴尔高管阿米特·米达为公司全球首席执行官，其在正式设立前即已受聘筹建公司。",
            "impact": "国际化高管团队到位，加速与国际科技大厂的合作谈判与运营体系搭建。",
            "source": "https://www.spa.gov.sa/en/N2042609"
        },
        {
            "date": "2024-02-20",
            "title": "Alat 与软银、开利、大华、Tahakom 达成四项全球合作",
            "description": "Alat 宣布与软银集团（SoftBank Group）、开利公司（Carrier）、大华股份（Dahua Technology）与沙特综合安防技术公司（Tahakom）建立四项全球合作伙伴关系；其中与大华将共同投资 2 亿美元成立合资公司 Alat AIVisio Technology，建设大华首个海外制造中心。",
            "impact": "为沙特本地机器人、暖通空调、视觉物联（AIoT）安防等产品制造落地与供应链建设奠定基础。",
            "source": "https://alat.com/en/newsroom/alat-announces-four-global-technology-partnerships/"
        },
        {
            "date": "2024-05-29",
            "title": "联想与 Alat 宣布 20 亿美元战略合作框架",
            "description": "联想集团与 Alat 签署战略合作框架协议及债券认购协议，Alat 认购联想 20 亿美元三年期零息可换股债券，双方在中东与非洲市场开展战略合作并在沙特设立制造基地。",
            "impact": "开创 PIF「以投资换产能」模式：Alat 入股联想，换取其在沙特建厂并带动区域业务扩张。",
            "source": "https://news.lenovo.com/pressroom/press-releases/lenovo-enters-strategic-collaboration-with-alat/"
        },
        {
            "date": "2025-01-08",
            "title": "联想与 Alat 完成 20 亿美元投资并签署战略合作协议",
            "description": "经股东与监管机构批准，联想与 Alat 宣布完成 20 亿美元零息可换股债券投资（换股价调整为 10.02 港元，对应约 15.59 亿股），并正式达成战略合作协议。",
            "impact": "Alat 成为联想重要股东，制造合作由协议进入执行阶段。",
            "source": "https://investor.lenovo.com/en/ir/corp_actions/nl250108.pdf"
        },
        {
            "date": "2025-02-09",
            "title": "Alat 与联想利雅得制造基地动工",
            "description": "在 LEAP 2025 科技大会期间，Alat 与联想为位于利雅得综合特别物流区（Riyadh Integrated / SILZ）的新制造基地举行动工仪式，工厂占地 20 万平方米，将生产「沙特制造」笔记本电脑、台式机与服务器，预计创造最多 1.5 万个直接就业岗位及 4.5 万个间接岗位。",
            "impact": "该厂为联想在中国以外最大制造基地之一，是沙特建设区域科技制造中心的核心项目。",
            "source": "https://www.spa.gov.sa/en/N2258189"
        },
        {
            "date": "2026-04-09",
            "title": "Semafor 报道 Alat 解除 CEO 米达职务并放弃半导体计划",
            "description": "据 Semafor 报道，PIF 解除阿米特·米达的 Alat CEO 职务，公司放弃进入半导体制造的计划并重组芯片团队，任命 PIF 工业与矿业负责人穆罕默德·纳赛尔·达伍德为代理 CEO；Alat 发言人确认任命「符合公司治理框架与长期战略规划」，公司战略重心转向数据中心枢纽等方向。",
            "impact": "标志沙特高科技制造雄心在财政纪律与支出重估背景下的收缩与转向，半导体自产目标搁置。",
            "source": "https://www.semafor.com/article/04/09/2026/saudis-alat-removes-head-drops-chip-ambitions"
        },
        {
            "date": "2026-08-31",
            "title": "Alat 与联想发布首台沙特制造的联想笔记本电脑",
            "description": "在 LEAP 2026 大会上，Alat 与联想发布首台在沙特制造的联想笔记本电脑；批量生产预计 2026 年底在利雅得工厂启动，产品组合包括笔记本电脑、台式机、摩托罗拉智能手机与服务器，首批沙特工程师已在联想全球制造基地完成专项培训。",
            "impact": "「沙特制造」电子产品实现标志性落地，推进知识转移与高技能岗位创造，支撑 2030 愿景先进制造目标。",
            "source": "https://alat.com/en/newsroom/alat-lenovo-first-saudi-manufactured-laptop/"
        }
    ],
    "related_entities": [
        {
            "org_id": "SA-FIN-001",
            "org_name": "公共投资基金 (Public Investment Fund)",
            "org_type": "sovereign_wealth_fund",
            "org_description": "沙特主权财富基金，Alat 为其全资子公司，承诺向 Alat 投入约 1000 亿美元。",
            "relationship_type": "controlling_shareholder"
        },
        {
            "org_id": None,
            "org_name": "联想集团 (Lenovo Group)",
            "org_type": "private_company",
            "org_description": "全球个人电脑与服务器制造商；与 Alat 完成 20 亿美元可换股债券投资与战略合作，共建利雅得 20 万平方米制造基地（2026 年底量产）。",
            "relationship_type": "strategic_alliance"
        },
        {
            "org_id": None,
            "org_name": "大华股份 (Dahua Technology)",
            "org_type": "private_company",
            "org_description": "以视频为核心的 AIoT 解决方案提供商；2024年2月与 Alat 宣布共同投资 2 亿美元成立合资公司 Alat AIVisio Technology，在大华首个海外制造中心生产视觉物联产品。",
            "relationship_type": "partner"
        },
        {
            "org_id": None,
            "org_name": "开利公司 (Carrier Global)",
            "org_type": "private_company",
            "org_description": "全球暖通空调与制冷巨头；2024年2月与 Alat 建立战略合作，在沙特本地化制造先进 HVAC 相关产品。",
            "relationship_type": "strategic_alliance"
        },
        {
            "org_id": None,
            "org_name": "软银集团 (SoftBank Group)",
            "org_type": "private_company",
            "org_description": "日本跨国科技投资集团；2024年2月与 Alat 达成合作，拟在沙特本地化制造先进机器人等产品。",
            "relationship_type": "strategic_alliance"
        },
        {
            "org_id": None,
            "org_name": "沙特综合安防技术公司 (Tahakom)",
            "org_type": "state_owned_enterprise",
            "org_description": "沙特技术与安全综合控制公司；2024年2月与 Alat 建立战略合作，推动安防与监控技术本地制造。",
            "relationship_type": "strategic_alliance"
        }
    ],
    "core_business": "Alat（آلات，品牌写作 ALAT）是沙特公共投资基金（PIF）全资拥有的先进制造与科技公司，2024年2月1日由王储穆罕默德·本·萨勒曼宣布设立，总部位于利雅得，PIF 承诺投入约 1000 亿美元。公司定位是依托沙特低成本的太阳能、风能等清洁能源，打造面向电子与先进工业的全球可持续技术制造中心，倡导「零碳工厂」与工业 4.0 制造理念，并服务于沙特到 2060 年实现碳中和的目标。设立之初规划先进工业、半导体、智慧健康、智能家电、智能设备、智能建筑与下一代基础设施七大战略业务单元，覆盖半导体、机器人系统、通信系统、先进计算机、数字娱乐、医疗系统与建筑采矿重型机械等 30 余个产品类别；目前官网显示四大业务板块：AI 与数字硬件、建筑与重型设备、电气化、家用与医疗设备。公司目标到 2030 年创造 3.9 万个直接就业岗位、为非石油 GDP 贡献 93 亿美元，支撑「2030 愿景」经济多元化。运营模式上，Alat 通过对国际大厂投资入股换取其在沙特设厂与本地化生产（如 20 亿美元投资联想并共建利雅得制造基地），并与大华股份（AIVisio 合资）、开利、软银集团、Tahakom 等建立制造合作。据 Semafor 2026年4月报道，公司已放弃半导体制造计划，战略转向数据中心等方向，反映沙特大型项目支出重估的影响。",
    "industries": [
        "investment"
    ],
    "apec_stance": None,
    "profile": {
        "source_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7f/Alat_Logo.svg/330px-Alat_Logo.svg.png?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail",
        "local_path": None
    },
    "collection_meta": {
        "collection_date": "2026-09-29",
        "phase": "phase3_enriched",
        "data_sources": [
            "wikidata",
            "wikipedia",
            "official_website",
            "spa_saudi_press_agency",
            "lenovo_press_release",
            "dahua_press_release",
            "prnewswire",
            "semafor",
            "reuters",
            "news_search"
        ],
        "quotes": [
            {
                "title": "HRH Crown Prince launches 'Alat' to Make Saudi Arabia a Global Center for Electronics and Advanced Industrials",
                "url": "https://alat.com/en/newsroom/hrh-crown-prince-launches-alat/"
            },
            {
                "title": "Saudi's Alat removes head, drops chip ambitions",
                "url": "https://www.semafor.com/article/04/09/2026/saudis-alat-removes-head-drops-chip-ambitions"
            },
            {
                "title": "Alat and Lenovo Break Ground on Major New Manufacturing Facility in the Kingdom of Saudi Arabia (SPA)",
                "url": "https://www.spa.gov.sa/en/N2258189"
            },
            {
                "title": "Lenovo and Alat Complete US$2 Billion Investment and Reach Strategic Collaboration Agreements",
                "url": "https://news.lenovo.com/pressroom/press-releases/lenovo-and-alat-complete-us2-billion-investment-and-reach-strategic-collaboration-agreements/"
            },
            {
                "title": "Alat announces four partnerships with leading global companies to rapidly progress technology manufacturing in Saudi Arabia",
                "url": "https://www.prnewswire.com/news-releases/alat-announces-four-partnerships-with-leading-global-companies-to-rapidly-progress-technology-manufacturing-in-saudi-arabia-302066110.html"
            },
            {
                "title": "Alat and Lenovo Mark Milestone with First Saudi-Manufactured Laptop",
                "url": "https://alat.com/en/newsroom/alat-lenovo-first-saudi-manufactured-laptop/"
            },
            {
                "title": "Amit Midha Appointed as Global CEO of Alat (SPA)",
                "url": "https://www.spa.gov.sa/en/N2042609"
            }
        ],
        "completeness_score": 85,
        "notes": "Phase3 丰富完成：Wikipedia（英语，含 Q124547892）+ 官网（董事会/高管/业务板块/页脚社交账号）+ SPA/联想/大华/Semafor/路透等新闻交叉验证。要点：2024-02-01 设立、PIF 约 1000 亿美元支持、王储任董事长；Amit Midha 2024-02-06 任 CEO、2026-04 被解职（Semafor 报道），穆罕默德·纳赛尔·达伍德任代理 CEO；半导体计划放弃。沙特非 APEC 成员，apec_stance 保持 null。"
    }
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("written", OUT)

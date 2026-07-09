# -*- coding: utf-8 -*-
"""Write enriched profile for KG-GOV-003 (Jogorku Kenesh / Supreme Council of Kyrgyzstan)."""
import json
from pathlib import Path

data = {
    "org_id": "KG-GOV-003",
    "basic_info": {
        "name_original": "Жогорку Кеңеш (Jogorku Kenesh)",
        "name_zh": "吉尔吉斯斯坦最高议会（吉尔吉斯议会）",
        "name_en": "Supreme Council of Kyrgyzstan (Jogorku Kenesh)",
        "aliases": [
            "Jogorku Kenesh",
            "Жогорку Кеңеш",
            "Верховный Совет Кыргызской Республики",
            "Supreme Council of Kyrgyzstan",
            "Parliament of Kyrgyzstan",
            "Kyrgyz Parliament"
        ],
        "org_type": "GOV",
        "org_subtype": "legislature",
        "country_iso3": "KGZ",
        "hq_country_iso3": "KGZ",
        "founded_date": None,
        "website": "https://www.kenesh.kg/",
        "wikidata_qid": "Q1379224"
    },
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "kenesh.kg",
            "url": "https://www.facebook.com/kenesh.kg/",
            "source": "https://www.facebook.com/kenesh.kg/"
        },
        {
            "platform": "twitter_x",
            "account_name": "Kenesh_kg",
            "url": "https://twitter.com/Kenesh_kg",
            "source": "https://twitter.com/Kenesh_kg"
        },
        {
            "platform": "instagram",
            "account_name": "kg.kenesh",
            "url": "https://www.instagram.com/kg.kenesh/",
            "source": "https://www.instagram.com/kg.kenesh/"
        },
        {
            "platform": "youtube",
            "account_name": "Жогорку Кенеш",
            "url": "https://www.youtube.com/channel/UCdnd_IBwwoNaIUeYnqP_6cw",
            "source": "https://www.youtube.com/channel/UCdnd_IBwwoNaIUeYnqP_6cw"
        },
        {
            "platform": "telegram",
            "account_name": "zhogorkukenesh",
            "url": "https://t.me/zhogorkukenesh",
            "source": "https://telemetr.io/en/channels/1639953060-zhogorkukenesh"
        }
    ],
    "digital_assets": [
        {
            "name": "官方网站（俄语/吉语）",
            "url": "https://www.kenesh.kg/",
            "description": "吉尔吉斯斯坦最高议会官方网站，发布议员信息、委员会结构、议程、立法文本及新闻稿",
            "source": "https://www.kenesh.kg/"
        },
        {
            "name": "Official Website (English)",
            "url": "https://www.kenesh.kg/?lang=en",
            "description": "English version of the Jogorku Kenesh official site with deputy profiles, factions, and press releases",
            "source": "https://www.kenesh.kg/?lang=en"
        },
        {
            "name": "委员会页面（Committees）",
            "url": "https://kenesh.kg/committees",
            "description": "列出第八届议会下设八个专门委员会及其主席和成员",
            "source": "https://kenesh.kg/committees"
        },
        {
            "name": "议员派系页面（Factions）",
            "url": "https://kenesh.kg/factions",
            "description": "议会各议员派系（Ata-Jurt、Eldik、Ala-Too、Mekenchil、Adilet Kyrgyzstan 等）的组成与信息",
            "source": "https://kenesh.kg/factions"
        }
    ],
    "key_people": [
        {
            "person_id": None,
            "name": "马列·马马塔利耶夫（Марлен Маматалиев / Marlen Mamataliev）",
            "title": "议长（Торага / Speaker / Toraga）",
            "title_description": "最高议会主持人，由全体议员无记名投票选举产生，负责主持议会会议、代表议会对外交往",
            "description": "1981年3月24日出生于比什凯克，2026年2月12日经77票赞成、5票反对当选第八届议会议长。曾任第六届、第七届议员，第七届任茵特玛克派系领袖及预算经济财政委员会主席，历任社会基金、经济财政部、政府办公厅等公职及私营企业高管"
        },
        {
            "person_id": None,
            "name": "吉勒德兹·萨德尔巴耶娃（Жылдыз Садырбаева / Zhylgyz Sadyrbaeva）",
            "title": "副议长（Заместитель Торага / Deputy Speaker）",
            "title_description": "协助议长主持日常议程，主管特定立法协调事务",
            "description": "第八届议会副议长，隶属 Ata-Zhurt Kyrgyzstan 议员团体"
        },
        {
            "person_id": None,
            "name": "努尔兰别克·阿兹加利耶夫（Нурланбек Азыгалиев / Nurlanbek Azygaliev）",
            "title": "副议长（Заместитель Торага / Deputy Speaker）",
            "title_description": "协助议长主持日常议程，独立议员身份",
            "description": "第八届议会副议长，独立议员"
        },
        {
            "person_id": None,
            "name": "努尔别克·瑟德加利耶夫（Нурбек Сыдыгалиев / Nurbek Sydygaliev）",
            "title": "副议长（Заместитель Торага / Deputy Speaker）",
            "title_description": "协助议长主持日常议程，隶属 Ishenim 议员团体",
            "description": "第八届议会副议长，隶属 Ishenim（信任）议员团体"
        },
        {
            "person_id": None,
            "name": "库尔曼库尔·祖卢舍夫（Курманкул Зулушев / Kurmankul Zulush(u)ev）",
            "title": "宪法立法与国家体制委员会主席",
            "title_description": "主管宪法立法、国家体制、地方自治及议事规程事务",
            "description": "第八届议会第一委员会主席，第十选区代表，2025年12月17日当选"
        },
        {
            "person_id": None,
            "name": "埃利达尔·苏莱马诺夫（Эльдар Сулайманов / Eldar Sulaimanov）",
            "title": "国际事务、国防、安全与移民委员会主席",
            "title_description": "主管外交、国防、国家安全与移民政策事务",
            "description": "第八届议会国际事务、国防、安全与移民委员会主席"
        },
        {
            "person_id": None,
            "name": "阿尔滕别克·库戴别尔季耶夫（Алтынбек Кудайбердиев / Altynbek Kudaiberdiev）",
            "title": "财政、预算、企业家精神与竞争发展委员会主席",
            "title_description": "主管国家预算、税收、公共财政与企业竞争政策",
            "description": "第八届议会财政、预算、企业家精神与竞争发展委员会主席"
        },
        {
            "person_id": None,
            "name": "库巴内奇别克·孔甘季耶夫（Кубанычбек Конгантиев / Kubanychbek Kongantiyev）",
            "title": "工业政策、交通、燃料能源综合体、建筑与建设委员会主席",
            "title_description": "主管工业、交通、能源、建筑与基础设施立法",
            "description": "第八届议会工业政策、交通、燃料能源综合体、建筑与建设委员会主席"
        }
    ],
    "departments": [
        {
            "name": "宪法立法、国家体制、地方自治与议事规程委员会（Комитет по конституционному законодательству, государственному устройству, местному самоуправлению и регламенту）",
            "dept_id": None,
            "head": "库尔曼库尔·祖卢舍夫（Курманкул Зулушев）",
            "description": "审议宪法修正案、国家体制改革、地方自治法及议会内部议事规程",
            "parent_dept_id": None
        },
        {
            "name": "国际事务、国防、安全与移民委员会（Комитет по международным делам, обороне, безопасности и миграции）",
            "dept_id": None,
            "head": "埃利达尔·苏莱马诺夫（Эльдар Сулайманов）",
            "description": "审议国际条约、外交政策、国防预算、国家安全与移民立法",
            "parent_dept_id": None
        },
        {
            "name": "财政、预算、企业家精神与竞争发展委员会（Комитет по финансам, бюджету, предпринимательству и развитию конкуренции）",
            "dept_id": None,
            "head": "阿尔滕别克·库戴别尔季耶夫（Алтынбек Кудайбердиев）",
            "description": "审议国家预算、税法、政府采购、金融监管及中小企业扶持政策",
            "parent_dept_id": None
        },
        {
            "name": "农业政策、水资源、矿产利用、生态与环境保护委员会（Комитет по аграрной политике, водным ресурсам, недропользованию, экологии и охране окружающей среды）",
            "dept_id": None,
            "head": "巴基特·坚季舍夫（Бакыт Тентишев）",
            "description": "审议农业、水利、矿业（含库姆托尔金矿等重大矿产）、环保与气候变化立法",
            "parent_dept_id": None
        },
        {
            "name": "科学、教育、创新发展、信息技术、文化、体育与青年事务委员会（Комитет по науке, образованию, инновационному развитию, ИТ, культуре, спорту и делам молодежи）",
            "dept_id": None,
            "head": "托克托布布·阿申巴耶娃（Токтобубу Ашымбаева）",
            "description": "审议教育科研、数字化、文化产业、体育及青年政策立法",
            "parent_dept_id": None
        },
        {
            "name": "工业政策、交通、燃料能源综合体、建筑与建设委员会（Комитет по промышленной политике, транспорту, ТЭК, архитектуре и строительству）",
            "dept_id": None,
            "head": "库巴内奇别克·孔甘季耶夫（Кубанычбек Конгантиев）",
            "description": "审议工业、铁路、航空、能源（中吉天然气管道等）、建筑业立法",
            "parent_dept_id": None
        },
        {
            "name": "司法法律问题、法治、打击犯罪与反腐败委员会（Комитет по судебно-правовым вопросам, правопорядку, борьбе с преступностью и противодействию коррупции）",
            "dept_id": None,
            "head": "博洛特别克·博尔比耶夫（Болотбек Борбиев）",
            "description": "审议司法改革、刑法、反腐与执法机构监督立法",
            "parent_dept_id": None
        },
        {
            "name": "劳动、卫生、妇女事务与社会政策委员会（Комитет по труду, здравоохранению, делам женщин и социальным вопросам）",
            "dept_id": None,
            "head": "古尔松坎·朱努沙利耶娃（Гулсункан Жунушалиева）",
            "description": "2025年12月17日新设立的第八个委员会，主管劳动、医疗、社保与性别平等立法",
            "parent_dept_id": None
        },
        {
            "name": "议会 apparatus（议会秘书处 / Аппарат Жогорку Кенеша）",
            "dept_id": None,
            "head": None,
            "description": "议会的行政、法律和信息服务部门，为议员和委员会提供研究、文书、公共关系和后勤支持",
            "parent_dept_id": None
        }
    ],
    "recent_events": [
        {
            "date": "2025-09-25",
            "title": "第七届议会宣布自行解散",
            "description": "第七届 Jogorku Kenesh 通过自决解散决议，89名出席议员中84票赞成，为提前大选铺路",
            "impact": "依据2021年宪法改革提前结束任期，原任期至2026年，触发2025年11月30日第八届议会选举",
            "source": "https://ru.wikipedia.org/wiki/Жогорку_Кенеш"
        },
        {
            "date": "2025-11-30",
            "title": "第八届议会大选举行",
            "description": "吉尔吉斯斯坦举行第八届 Jogorku Kenesh 选举，90个议席通过30个三人选区单一非可转移投票制选出，任期5年",
            "impact": "五个议员团体（Mekenchil 19席、Ata-Zhurt 18席、Eldik 18席、Ala-Too 15席、Adilet Kyrgyzstan 14席）进入议会",
            "source": "https://en.wikipedia.org/wiki/Supreme_Council_(Kyrgyzstan)"
        },
        {
            "date": "2025-12-17",
            "title": "第八届议会首次会议召开并选出八个委员会主席",
            "description": "第八届 Jogorku Kenesh 在比什凯克举行首次全体会议，确认议会结构并选举八个常设委员会主席，新增劳动卫生妇女社会政策委员会",
            "impact": "议会机构正式启动运转，Kurmankul Zulush(u)ev 担任宪法立法委员会主席等人事落定",
            "source": "https://economist.kg/vlast/2025/12/17/dieputaty-zhk-izbrali-ghlav-profilnykh-komitietov-spisok/"
        },
        {
            "date": "2025-12-24",
            "title": "议会审议通过2026年国家预算",
            "description": "Jogorku Kenesh 审议通过《吉尔吉斯共和国2026年及2027-2028年规划期国家预算法》，收入约5512亿索姆、支出约5508亿索姆，结余约4.36亿索姆",
            "impact": "国家财政继续延续盈余预算策略，库姆托尔金矿国有化带来的收入持续支撑公共支出",
            "source": "https://news.vv.kg/en/news/19295-approved-the-budget-of-kyrgyzstan-for-2026-the-law-has-been-signed/"
        },
        {
            "date": "2026-01-27",
            "title": "内阁主席向议会报告库姆托尔金矿国有化成果",
            "description": "内阁主席卡西马利耶夫向议会报告，库姆托尔金矿2021-2025年国有化累计为预算贡献约51.15亿美元生产收入和约11.76亿美元其他收入",
            "impact": "彰显议会监督国有资产管理职能，矿产收入成为国家财政支柱",
            "source": "https://en.kabar.kg/news/nationalization-of-kumtor-brings-16-billion-to-the-budget/"
        },
        {
            "date": "2026-02-12",
            "title": "马马塔利耶夫当选第八届议会议长",
            "description": "马列·马马塔利耶夫经无记名投票以77票赞成、5票反对当选第八届 Jogorku Kenesh 议长，接替当天早些时候辞职的前任议长图尔贡别克乌鲁（Nurlanbek Turgunbek uulu）",
            "impact": "议会领导层更迭落定，五个议员团体共同提名，为新一届议会立法议程奠定基础",
            "source": "https://en.kabar.kg/news/kyrgyz-parliament-elects-new-speaker/"
        }
    ],
    "related_entities": [
        {
            "org_id": "KG-GOV-001",
            "org_name": "吉尔吉斯斯坦总统（Президент Кыргызской Республики / President of Kyrgyzstan）",
            "org_type": "GOV",
            "org_description": "国家元首，依据2021年宪法行使行政权，签署议会通过的法律并可解散议会",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "KG-GOV-002",
            "org_name": "吉尔吉斯共和国内阁（Cabinet of Ministers of the Kyrgyz Republic）",
            "org_type": "GOV",
            "org_description": "国家最高行政机关，由总统直接领导，内阁主席由议会同意任命",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "KG-GOV-004",
            "org_name": "吉尔吉斯斯坦最高法院（Supreme Court of Kyrgyzstan）",
            "org_type": "GOV",
            "org_description": "国家最高司法机关，议会通过其司法委员会参与法官选任",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "KG-GOV-005",
            "org_name": "最高法院宪法法庭（Constitutional Chamber of the Supreme Court）",
            "org_type": "GOV",
            "org_description": "负责违宪审查，议会通过的法律可由宪法法庭审查",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "KG-GOV-008",
            "org_name": "司法部（Министерство юстиции / Ministry of Justice）",
            "org_type": "GOV",
            "org_description": "负责法律起草、法律出版、国家登记及与议会的立法协调",
            "relationship_type": "partner"
        },
        {
            "org_id": "KG-GOV-010",
            "org_name": "财政部（Министерство финансов / Ministry of Finance）",
            "org_type": "GOV",
            "org_description": "编制国家预算草案提交议会审议，执行议会通过的预算法",
            "relationship_type": "partner"
        },
        {
            "org_id": "KG-PARTY-001",
            "org_name": "吾乡吉尔吉斯（Mekenchil / My Homeland Kyrgyzstan）",
            "org_type": "PARTY",
            "org_description": "第八届议会最大议员团体，持有19个议席",
            "relationship_type": "member_of"
        },
        {
            "org_id": "KG-PARTY-004",
            "org_name": "吉尔吉斯斯坦祖国党（Ata-Zhurt / Ata-Jurt）",
            "org_type": "PARTY",
            "org_description": "第八届议会持有18个议席的议员团体",
            "relationship_type": "member_of"
        },
        {
            "org_id": "KG-PARTY-003",
            "org_name": "吉尔吉斯斯坦社会民主党（SDPK）",
            "org_type": "PARTY",
            "org_description": "历史主要政党之一，曾长期主导议会政治",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "KG-MEDIA-001",
            "org_name": "AKIpress News Agency",
            "org_type": "MEDIA",
            "org_description": "吉尔吉斯斯坦主要独立新闻机构，长期报道议会动态",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "KG-MEDIA-003",
            "org_name": "吉尔吉斯公共广播电视公司（NKTRK）",
            "org_type": "MEDIA",
            "org_description": "国家公共广播公司，议会会议通常由其转播",
            "relationship_type": "partner"
        },
        {
            "org_id": "KG-SOE-002",
            "org_name": "Kyrgyzaltyn",
            "org_type": "SOE",
            "org_description": "国家黄金矿业公司，库姆托尔金矿国有化后由其管理，向议会报告经营成果",
            "relationship_type": "regulated_by"
        }
    ],
    "core_business": "吉尔吉斯斯坦最高议会（Jogorku Kenesh / Жогорку Кеңеш）是吉尔吉斯共和国的一院制国家立法机关，由90名议员组成，任期5年，依据2021年新宪法经30个三人选区单一非可转移投票制选举产生。议会前身为苏联时期的吉尔吉斯苏维埃社会主义共和国最高苏维埃，1994年起改组为现行最高议会。其核心职能包括：制定和修改宪法与法律、审议和通过国家预算与税收政策、批准国际条约、决定战争与和平问题、根据总统提名同意内阁主席任命、对内阁及政府工作进行监督、宣布大赦及行使宪法规定的其他职权。第八届议会下设八个常设专门委员会，分别主管宪法立法与国家体制、国际事务与国防安全、财政预算与企业家精神、农业水利与矿业生态、科教创新与文化体育、工业交通与能源建筑、司法法治与反腐、劳动卫生与妇女社会政策等事务。议长（Toraga / Торага）由全体议员无记名投票选举产生，下设一名第一副议长和两名副议长。议会位于首都比什凯克，每年举行两次定期会议，是中亚地区少数实现多党竞争议会政治的国家机构，在国家政治生活中具有举足轻重的地位。",
    "industries": [
        "public_administration",
        "legislative"
    ],
    "apec_stance": "吉尔吉斯斯坦并非亚太经济合作组织（APEC）21个正式成员经济体之一，最高议会（Jogorku Kenesh）与APEC没有正式关系或合作机制。作为一个中亚内陆国家，吉尔吉斯斯坦的外交与经济合作重心主要在欧亚经济联盟（EAEU）、上海合作组织（SCO）、独立国家联合体（CIS）以及中国-中亚合作框架下。议会层面，Jogorku Kenesh 通过参与上海合作组织成员国议会领导人会议（如2025年11月29日SCO观察团监督吉尔吉斯议会选举）、集体安全条约组织（CSTO）议会大会、独联体国家间议会大会等机制进行国际议会交往。在中亚-亚太互联互通议题上，议会主要就中吉乌铁路、中吉天然气管道、一带一路倡议下的基础设施与能源合作等法案履行立法审批职能，对中国、韩国、日本、东南亚国家在本地区的经贸投资合作持开放态度，但目前未参与APEC相关会议或倡议。",
    "profile": {
        "source_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Logo_of_the_Jogorku_Kenesh.png/250px-Logo_of_the_Jogorku_Kenesh.png",
        "local_path": None
    },
    "collection_meta": {
        "collection_date": "2026-06-21",
        "phase": "phase3_enriched",
        "data_sources": [
            "wikipedia_en",
            "wikipedia_ru",
            "official_website",
            "news_media",
            "newsgov_cn"
        ],
        "completeness_score": 92,
        "notes": "Enriched from original Q1142018 (incorrectly pointed to The Confessions Tour) — corrected to Q1379224 (Jogorku Kenesh). Speaker and committee chairs verified as of Feb 2026 (8th convocation).",
        "quotes": [
            {
                "title": "Supreme Council (Kyrgyzstan) — English Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Supreme_Council_(Kyrgyzstan)"
            },
            {
                "title": "Жогорку Кенеш — Russian Wikipedia",
                "url": "https://ru.wikipedia.org/wiki/Жогорку_Кенеш"
            },
            {
                "title": "Jogorku Kenesh Official Website",
                "url": "https://www.kenesh.kg/"
            },
            {
                "title": "Elected Chairpersons of 8 Committees — economist.kg, 17 Dec 2025",
                "url": "https://economist.kg/vlast/2025/12/17/dieputaty-zhk-izbrali-ghlav-profilnykh-komitietov-spisok/"
            },
            {
                "title": "New Speaker Elected — Kabar News Agency, 12 Feb 2026",
                "url": "https://en.kabar.kg/news/kyrgyz-parliament-elects-new-speaker/"
            },
            {
                "title": "新华社：吉尔吉斯斯坦议会选举出新议长",
                "url": "https://app.xinhuanet.com/news/article.html?articleId=6c7ced3cd1b738fed3df6218be3455ba"
            },
            {
                "title": "中华人民共和国外交部：吉尔吉斯斯坦国家概况",
                "url": "https://www.mfa.gov.cn/web/gjhdq_676201/gj_676203/yz_676205/1206_676548/1206x0_676550/"
            }
        ]
    }
}

out_path = Path(r"D:/claude-workspace/apec-osint-tool/output/kg/2026-06-21/orgs/KG-GOV-003.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")

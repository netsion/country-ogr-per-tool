# -*- coding: utf-8 -*-
"""Generate enriched profile for KG-GOV-013 (Ministry of Health of Kyrgyzstan)."""
import json

null = None

data = {
    "org_id": "KG-GOV-013",
    "basic_info": {
        "name_original": "Кыргыз Республикасынын Саламаттык Сактоо Министрлиги",
        "name_zh": "卫生部",
        "name_en": "Ministry of Health of the Kyrgyz Republic",
        "aliases": [
            "Министерство здравоохранения Кыргызской Республики",
            "Минздрав КР",
            "Ministry of Health of Kyrgyzstan",
            "КР ССМ",
            "Кыргыз Республикасынын Саламаттык Сактоо Министрлили"
        ],
        "org_type": "GOV",
        "org_subtype": "ministry",
        "country_iso3": "KGZ",
        "hq_country_iso3": "KGZ",
        "founded_date": null,
        "website": "https://med.kg/",
        "wikidata_qid": "Q33130027"
    },
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "MinzdravKG",
            "url": "https://www.facebook.com/MinzdravKG/",
            "source": "https://med.kg/"
        },
        {
            "platform": "instagram",
            "account_name": "minzdravkg_official",
            "url": "https://www.instagram.com/minzdravkg_official/",
            "source": "https://med.kg/"
        },
        {
            "platform": "telegram",
            "account_name": "minzdravKR",
            "url": "https://t.me/minzdravKR",
            "source": "https://med.kg/"
        },
        {
            "platform": "youtube",
            "account_name": "Ministerstvo Zdravoohraneniya KR",
            "url": "https://www.youtube.com/@minzdravKR",
            "source": "https://t.me/minzdravKR"
        }
    ],
    "digital_assets": [
        {
            "name": "官方网站 (med.kg)",
            "url": "https://med.kg/",
            "description": "吉尔吉斯斯坦卫生部官方网站，发布新闻、政策法规、招标公告与公众健康信息",
            "source": "https://med.kg/"
        },
        {
            "name": "药品与医疗器械局 (DLSMI)",
            "url": "https://dlsmi.kg/",
            "description": "卫生部下属药品与医疗器械管理局，负责药品注册、监管与essential medicines list",
            "source": "https://dlsmi.kg/"
        },
        {
            "name": "强制性医疗保险基金 (FOMS)",
            "url": "http://foms.kg/",
            "description": "卫生部下属强制性医疗保险基金，作为全国统一公共支付方，统筹公立医院与基层医疗的资金",
            "source": "https://med.kg/"
        },
        {
            "name": "电子医疗门户 (e-license)",
            "url": "https://elicense.gov.kg/widget/iframe?activities=&views=&agencies=19&page=1&limit=15&lang=Ru",
            "description": "卫生部医疗执业许可证与授权文件在线查询系统",
            "source": "https://med.kg/"
        }
    ],
    "key_people": [
        {
            "person_id": null,
            "name": "达米尔别克·奥斯莫诺夫 (Damirbek Osmonov)",
            "title": "卫生部长 (Minister of Health)",
            "title_description": "吉国内阁成员，主管全国医疗卫生政策制定与执行的最高官员",
            "description": "心脏病学家，1982年1月12日生于奥什，土耳其哈西德佩大学医学院毕业，曾在伊斯坦布尔Siyami Ersek胸心血管外科培训医院任职；曾任BIKARD私人诊所创始人兼首席医师、比什凯克国际医科大学心脏病学系主任；欧洲心脏病学会Fellow (FESC)、美国心脏病学会会员；2026年2月24日任代部长，2月26日正式就任卫生部长"
        },
        {
            "person_id": "KG-PERSON-000010",
            "name": "埃尔金·切切巴耶夫 (Erkin Checheybayev)",
            "title": "前卫生部长 (Former Minister of Health, 2025年2月–12月)",
            "title_description": "前卫生部长，现任职务待定",
            "description": "曾任卫生部长（2025年2月5日至12月），任内与俄罗斯卫生部长穆拉什科签署2025-2026年吉俄卫生合作行动计划；内阁改组后去职"
        },
        {
            "person_id": null,
            "name": "马纳斯·托克托穆拉托夫 (Manas Toktomuratov)",
            "title": "第一副部长 (First Deputy Minister of Health)",
            "title_description": "卫生部常务副部长，协助部长统筹日常行政与政策执行",
            "description": "2025年2月14日起任第一副部长，Kasymaliev内阁"
        },
        {
            "person_id": null,
            "name": "卡尔曼别克·拜达夫列托夫 (Kaarmanbek Baydavletov)",
            "title": "副部长 (Deputy Minister of Health)",
            "title_description": "分管医疗事务的副部长",
            "description": "2024年9月起任副部长，Kasymaliev内阁"
        },
        {
            "person_id": null,
            "name": "布布詹·阿雷克巴耶娃 (Bubujan Arykbaeva)",
            "title": "副部长 (Deputy Minister of Health)",
            "title_description": "分管公共卫生与妇女儿童健康事务的副部长",
            "description": "2022年6月起任副部长，Kasymaliev内阁"
        },
        {
            "person_id": null,
            "name": "努尔古尔·阿德纳耶娃 (Nurgul Adnayeva)",
            "title": "副部长 (Deputy Minister of Health)",
            "title_description": "副部长，分管医疗教育与科学事务",
            "description": "2025年4月起任副部长，Kasymaliev内阁"
        }
    ],
    "departments": [
        {
            "name": "疾病预防与国家卫生防疫监督局",
            "dept_id": "KG-GOV-013-DEPT-001",
            "head": null,
            "description": "负责组织落实传染病、寄生虫病及重点非传染性疾病的预防与防疫措施，与电子医疗中心共同开发iEPID公共卫生事件监测信息系统",
            "parent_dept_id": null
        },
        {
            "name": "药品与医疗器械局",
            "dept_id": "KG-GOV-013-DEPT-002",
            "head": null,
            "description": "卫生部下属独立执行机构，负责国家药品与医疗器械注册、监管、Essential Medicines List制定与药品进口许可",
            "parent_dept_id": null
        },
        {
            "name": "强制性医疗保险基金",
            "dept_id": "KG-GOV-013-DEPT-003",
            "head": null,
            "description": "卫生部下属执行机构，作为单一公共支付方统筹公立医院与基层医疗机构的资金，承担国家保障福利计划 (SGBP) 的支付",
            "parent_dept_id": null
        },
        {
            "name": "卫生政策与战略司",
            "dept_id": "KG-GOV-013-DEPT-004",
            "head": null,
            "description": "制定国家卫生政策、起草卫生法规与部门战略，推动'健康人—繁荣国家'(Healthy Person - Prosperous Country) 2019-2030卫生部门战略",
            "parent_dept_id": null
        },
        {
            "name": "医政与医疗机构管理司",
            "dept_id": "KG-GOV-013-DEPT-005",
            "head": null,
            "description": "负责医疗机构执业许可、医疗质量监管、专科医疗服务体系建设，协调国家科学研究所以及国立医学院",
            "parent_dept_id": null
        },
        {
            "name": "公共卫生与非传染性疾病预防司",
            "dept_id": "KG-GOV-013-DEPT-006",
            "head": null,
            "description": "推进'健康心脏'等国家级慢病防控项目，承担免疫规划、健康促进与非传染性疾病预防政策落地",
            "parent_dept_id": null
        },
        {
            "name": "人力资源与医学教育司",
            "dept_id": "KG-GOV-013-DEPT-007",
            "head": null,
            "description": "负责卫生人力配置、住院医培训、继续医学教育及与外国医学院校合作项目的协调",
            "parent_dept_id": null
        },
        {
            "name": "国际合作司",
            "dept_id": "KG-GOV-013-DEPT-008",
            "head": null,
            "description": "负责与世界卫生组织 (WHO)、上合组织 (SCO)、欧盟、土耳其、韩国、俄罗斯等国际伙伴的双多边卫生合作",
            "parent_dept_id": null
        }
    ],
    "recent_events": [
        {
            "date": "2026-04-20",
            "title": "第九次上合组织成员国卫生部长会议在比什凯克举行",
            "description": "吉尔吉斯斯坦以轮值主席国身份主办第九次上合组织卫生部长会议，主题为'共同加强卫生体系，建设上合国家健康未来'；卫生部长Osmonov主持会议，强调数字技术与创新方案在医疗中的作用",
            "impact": "会议通过议定书，各方支持吉方提出的建立上合卫生管理能力对话平台倡议，确立吉国在中亚区域卫生合作中的领导地位",
            "source": "https://eng.sectsco.org/20260421/2267733.html"
        },
        {
            "date": "2026-04-07",
            "title": "与土耳其讨论扩大医疗合作",
            "description": "卫生部长Damir Osmonov会见土耳其驻吉尔吉斯斯坦大使Mekin Mustafa Kemal Okema，讨论吉土卫生合作议题，包括150名吉公民在土耳其医院按配额免费治疗",
            "impact": "巩固吉土卫生伙伴关系，扩大土耳其对吉医疗援助配额与专科医生交流",
            "source": "https://www.akchabar.kg/en/news/150-kirgizstantsev-smogut-besplatno-lechitsya-v-bolnitsakh-turtsii-po-kvotam-lnbqgpqjughtdiva"
        },
        {
            "date": "2026-03-16",
            "title": "与韩国讨论扩大卫生合作",
            "description": "卫生部长Damir Osmonov会见韩国驻吉尔吉斯斯坦大使Kwang-jae Kim，就双边医疗卫生合作进行洽谈",
            "impact": "推动韩国在数字化医疗、医院管理与医学培训方面对吉支持",
            "source": "https://www.akchabar.kg/en/news/v-minzdrave-obsudili-rasshirenie-sotrudnichestva-s-koreej-v-sfere-zdravookhraneniya-mukzyllhqvncbiip"
        },
        {
            "date": "2026-02-26",
            "title": "达米尔别克·奥斯莫诺夫正式就任卫生部长",
            "description": "总统扎帕罗夫签署命令，正式任命Osmonov为卫生部长；此前自2月24日起任代部长，接替自2025年12月起任职的Dosmambetov",
            "impact": "吉卫生部高层在新一轮内阁改组后稳定，专业派医生出身的部长有望推动医疗现代化议程",
            "source": "https://en.kabar.kg/news/damirbek-osmonov-appointed-kyrgyz-minister-of-health/"
        },
        {
            "date": "2026-02-06",
            "title": "Archaly将建设残疾儿童康复中心",
            "description": "卫生部计划在现有Maksat康复中心基础上，设计并建设集教育、科研方法学功能于一体的现代化儿童康复中心",
            "impact": "扩大儿科康复服务可及性，提升残疾儿童专项医疗服务能力",
            "source": "https://www.akchabar.kg/en/news/v-archali-postroyat-reabilitatsionnij-gorodok-dlya-detej-s-ovz-ionohghyjxirjjbt"
        },
        {
            "date": "2025-12-26",
            "title": "与联合国系统组织讨论药品可及与透明采购合作",
            "description": "卫生部与联合国系统组织举行会谈，重点讨论药品可及性、采购透明度、免疫规划与慢病预防等优先合作领域",
            "impact": "强化与UNICEF、UNFPA、WHO等联合国机构在药品、疫苗与公共卫生领域的合作框架",
            "source": "https://med.kg/?locale=ru"
        },
        {
            "date": "2025-12-01",
            "title": "Kanybek Dosmambetov任代卫生部长",
            "description": "总统任命Kanybek Dosmambetov为代卫生部长，接替2月被解职的Beishenaliev；12月23日议会劳动、卫生、妇女与社会事务委员会通过其提名",
            "impact": "2025年吉卫生部第二次换帅，反映总统对卫生改革进展的不满与新阶段的期待",
            "source": "https://en.kabar.kg/news/kyrgyz-parliament-approves-kanybek-dosmambetov-for-post-of-minister-of-health/"
        },
        {
            "date": "2025-08-15",
            "title": "吉俄签署2025-2026年卫生合作行动计划",
            "description": "在欧亚政府间理事会会议期间，卫生部长Chechebaev与俄罗斯卫生部长Murashko签署吉俄卫生合作2025-2026行动计划，内容涵盖设立吉俄友谊多功能医院可行性研究、吉医生赴俄培训（含移植、肿瘤、遗传学）、放射药物与肿瘤治疗合作",
            "impact": "深化吉俄在专科医疗、医学教育与药品监管领域的双边合作",
            "source": "https://www.akchabar.kg/en/news/minzdravi-kirgizstana-i-rossii-podpisali-plan-sovmestnikh-dejstvij-v-sfere-zdravookhraneniya-na-20252026-godi-vmtbyghrbbhybxzf"
        },
        {
            "date": "2025-03-12",
            "title": "WHO发布吉医院融资改革政策文件",
            "description": "WHO欧洲区发布政策文件，探讨吉尔吉斯斯坦医疗改革中DRGs（诊断相关组）的发展与演变，作为按病例付费住院支付体系的基础",
            "impact": "为吉国25年来医院病例付费体系改革提供独立评估与政策建议",
            "source": "https://www.who.int/europe/news/item/12-03-2025-hospital-financing-reforms-key-to-delivering-improved-health-services-in-kyrgyzstan"
        },
        {
            "date": "2025-02-03",
            "title": "卫生部长Beishenaliev被解职",
            "description": "总统扎帕罗夫签署命令，解除Alymkadyr Beishenaliev的卫生部长职务；由卫生部副部长Erkin Checheybayev任代部长，2月5日转正",
            "impact": "吉国卫生系统进入新一轮改革周期，新领导层优先推动药品可及与卫生体系现代化",
            "source": "https://en.wikipedia.org/wiki/Ministry_of_Health_(Kyrgyzstan)"
        }
    ],
    "related_entities": [
        {
            "org_id": "KG-GOV-002",
            "org_name": "内阁 (Cabinet of Ministers of the Kyrgyz Republic)",
            "org_type": "GOV",
            "org_description": "吉尔吉斯共和国最高行政权力机关",
            "relationship_type": "parent_org"
        },
        {
            "org_id": "KG-GOV-003",
            "org_name": "最高议会 (Supreme Council / Jogorku Kenesh)",
            "org_type": "GOV",
            "org_description": "吉尔吉斯共和国一院制议会，负责审议卫生部长任命与卫生立法",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "KG-ACAD-007",
            "org_name": "吉尔吉斯国立医学院 (Kyrgyz State Medical Academy)",
            "org_type": "ACAD",
            "org_description": "吉尔吉斯斯坦最古老的医学高等教育机构",
            "relationship_type": "affiliated"
        },
        {
            "org_id": "KG-INTL-001",
            "org_name": "联合国儿童基金会驻吉尔吉斯斯坦办事处 (UNICEF Kyrgyzstan)",
            "org_type": "INTL",
            "org_description": "联合国儿童基金会在吉尔吉斯斯坦的 Country Office",
            "relationship_type": "strategic_alliance"
        }
    ],
    "core_business": "吉尔吉斯斯坦卫生部是主管全国医疗卫生、公共卫生、医学科学与药品监管的中央执行机构。其核心职能包括：制定与落实国家卫生政策与法规、确保医疗服务的可及性与质量、统筹传染病与非传染性疾病防控、推进免疫规划、监管药品与医疗器械市场、管理强制性医疗保险基金、协调国家医学科研院所与吉尔吉斯国立医学院。卫生部还承担国家卫生战略——'健康人—繁荣国家'(2019-2030) 的执行，重点从治疗转向预防，推动数字医疗、基层医疗与医院融资 (DRGs) 改革。在国际合作方面，卫生部与WHO、UNICEF、上合组织、欧亚经济联盟成员国以及土耳其、韩国、中国等伙伴在医疗援助、专家培训、药品供应、疫苗采购等领域开展广泛合作，并主导推动上合组织卫生部长级对话平台。",
    "industries": [
        "public_administration",
        "healthcare"
    ],
    "apec_stance": "吉尔吉斯斯坦虽非APEC成员（2025年成为APECGuest身份），但卫生部积极参与亚太与欧亚区域卫生多边合作。在WHO框架下，吉国于2024年签署《WHO国家合作战略2024-2030》，与WHO欧洲区办公室、欧洲卫生观察站共同推进卫生体系评估、融资改革与初级卫生保健（PHC）升级。2025-2026年吉国担任上海合作组织轮值主席国，于2026年4月在比什凯克主办第九次上合组织卫生部长会议，倡议建立上合卫生管理能力对话平台，强调数字医疗与创新方案。与俄罗斯签署2025-2026年卫生合作行动计划，探讨共建吉俄友谊医院；与土耳其、韩国分别就医疗配额、数字化医疗开展合作；并依托欧盟、德国GIZ、阿迦汗基金会等发展伙伴推进基层医疗与公共卫生项目。吉国支持区域传染病联防联控、卫生人才培养跨国协作以及药品可及性合作。",
    "profile": "吉尔吉斯斯坦卫生部是吉内阁下设的卫生主管机关，总部位于比什凯克莫斯科大街148号。作为前苏联卫生体系的继承者，吉国实行强制性医疗保险制度，由卫生部下属强制性医疗保险基金 (MHIF/FOMS) 作为统一公共支付方统筹公立医院与基层医疗机构资金。卫生部下设疾病预防与国家卫生防疫监督局、药品与医疗器械局 (DLSMI)、强制性医疗保险基金等执行机构，以及卫生政策、医政管理、公共卫生、医学教育、国际合作等职能司。2025-2026年吉国卫生系统经历深度改革期：从'健康人—繁荣国家'战略下的DRGs病例付费改革、基层医疗 (PHC) 强化，到与WHO、俄罗斯、土耳其、韩国等的密集合作，再到高层频繁换帅——卫生部长三度易人（Beishenaliev→Checheybayev→Dosmambetov→Osmonov）。2026年2月心脏病学家Damirbek Osmonov就任部长后，卫生部将工作重心放在慢病预防（'健康心脏'国家级项目）、药品可及性、数字医疗与卫生人才培养国际化上，同时在上合组织框架下推动区域卫生合作对话。",
    "collection_meta": {
        "collection_date": "2026-06-21",
        "phase": "phase3_enriched",
        "quotes": [
            {
                "title": "Ministry of Health (Kyrgyzstan) - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Ministry_of_Health_(Kyrgyzstan)"
            },
            {
                "title": "Damirbek Osmonov appointed Kyrgyz Minister of Health - Kabar",
                "url": "https://en.kabar.kg/news/damirbek-osmonov-appointed-kyrgyz-minister-of-health/"
            },
            {
                "title": "9th Meeting of SCO Member States' Health Ministers in Bishkek",
                "url": "https://eng.sectsco.org/20260421/2267733.html"
            },
            {
                "title": "WHO: Hospital financing reforms in Kyrgyzstan (12 March 2025)",
                "url": "https://www.who.int/europe/news/item/12-03-2025-hospital-financing-reforms-key-to-delivering-improved-health-services-in-kyrgyzstan"
            },
            {
                "title": "Kyrgyz-Russian Health Cooperation Action Plan 2025-2026 - Akchabar",
                "url": "https://www.akchabar.kg/en/news/minzdravi-kirgizstana-i-rossii-podpisali-plan-sovmestnikh-dejstvij-v-sfere-zdravookhraneniya-na-20252026-godi-vmtbyghrbbhybxzf"
            },
            {
                "title": "Ministry of Health of Kyrgyzstan official website (med.kg)",
                "url": "https://med.kg/?locale=ru"
            }
        ],
        "data_sources": [
            "https://en.wikipedia.org/wiki/Ministry_of_Health_(Kyrgyzstan)",
            "https://med.kg/",
            "https://med.kg/?locale=ru",
            "https://dlsmi.kg/",
            "https://t.me/minzdravKR",
            "https://www.facebook.com/MinzdravKG/",
            "https://www.instagram.com/minzdravkg_official/",
            "https://en.kabar.kg/news/damirbek-osmonov-appointed-kyrgyz-minister-of-health/",
            "https://24.kg/english/363417_Damirbek_Osmonov_appointed_acting_Minister_of_Health_of_Kyrgyzstan/",
            "https://gazeta.kg/en/social/zdorove/173811-chto-izvestno-o-novom-glave-minzdrava-damirbeke-osmonove.html",
            "https://24.kg/english/363673___President_appoints_Erlist_Akunbekov_and_Damirbek_Osmonov_as_ministers/",
            "https://www.akchabar.kg/en/news/minzdravi-kirgizstana-i-rossii-podpisali-plan-sovmestnikh-dejstvij-v-sfere-zdravookhraneniya-na-20252026-godi-vmtbyghrbbhybxzf",
            "https://www.akchabar.kg/en/news/150-kirgizstantsev-smogut-besplatno-lechitsya-v-bolnitsakh-turtsii-po-kvotam-lnbqgpqjughtdiva",
            "https://www.akchabar.kg/en/news/v-minzdrave-obsudili-rasshirenie-sotrudnichestva-s-koreej-v-sfere-zdravookhraneniya-mukzyllhqvncbiip",
            "https://eng.sectsco.org/20260421/2267733.html",
            "https://www.who.int/europe/news/item/12-03-2025-hospital-financing-reforms-key-to-delivering-improved-health-services-in-kyrgyzstan",
            "https://www.who.int/publications/i/item/WHO-EURO-2025-9497-49269-73611",
            "https://en.kabar.kg/news/kyrgyz-parliament-approves-kanybek-dosmambetov-for-post-of-minister-of-health/",
            "https://en.kabar.kg/news/sco-summit-kyrgyzstan-outlines-strategic-priorities-for-2026/",
            "https://eurohealthobservatory.who.int/publications/i/health-systems-in-action-kyrgyzstan-2024",
            "https://lca.logcluster.org/12-kyrgyzstan-regulatory-departments",
            "https://24.kg/english/265077_Health_Ministry_develops_system_for_epidemiological_situation_monitoring/",
            "https://open.kg/en/news/local-news/66551-v-minzdrave-kr-podveli-itogi-2025-goda-i-zaplanirovali-zadachi-na-2026-j.html"
        ],
        "completeness_score": 90,
        "notes": "Phase3 enrichment complete. 4 social accounts, 4 digital assets, 6 key people (current minister + 5 senior leadership including 4 deputy ministers and former minister), 8 departments, 10 recent events spanning 2025-2026, 4 related entities. Minister updated to Damirbek Osmonov (appointed 2026-02-26); country_iso3 corrected from KGP to KGZ. Manas Toktomuratov (First Deputy), Kaarmanbek Baydavletov, Bubujan Arykbaeva, Nurgul Adnayeva (Deputies) are NOT in name_index - person_id set to null per ID rules."
    }
}

with open("D:/claude-workspace/apec-osint-tool/output/kg/2026-06-21/orgs/KG-GOV-013.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK - written")

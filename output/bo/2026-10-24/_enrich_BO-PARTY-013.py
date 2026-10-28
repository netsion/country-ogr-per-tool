# -*- coding: utf-8 -*-
"""Phase3 enrichment for BO-PARTY-013 (APB Súmate). One-off write script."""
import json

PATH = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/orgs/BO-PARTY-013.json"

data = {
    "org_id": "BO-PARTY-013",
    "basic_info": {
        "name_original": "Autonomía Para Bolivia Súmate (APB Súmate)",
        "name_zh": "玻利维亚自治-加入党",
        "name_en": "Autonomy for Bolivia - Súmate",
        "aliases": ["APB Súmate", "APB-Súmate", "Súmate"],
        "org_type": "PARTY",
        "org_subtype": "opposition_party",
        "country_iso3": "BOL",
        "hq_country_iso3": "BOL",
        "founded_date": "2024-12-13",
        "website": None,
        "wikidata_qid": "Q131629757"
    },
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "Súmate Bolivia (APB Súmate)",
            "url": "https://www.facebook.com/APBSumateBolivia/",
            "source": "Facebook官方党页（搜索核实，2026-10在用，主页定位科恰班巴，发布党与曼弗雷德·雷耶斯·比利亚动态）"
        },
        {
            "platform": "facebook",
            "account_name": "APB Súmate Sacaba（萨卡瓦地方支部页）",
            "url": "https://www.facebook.com/p/APB-S%C3%BAmate-Sacaba-61573153681530/",
            "source": "Facebook（搜索核实，APB Súmate萨卡瓦[科恰班巴省]地方组织页，公示联系电话+591 71445871）"
        }
    ],
    "digital_assets": [
        {
            "name": "OEP政党信息页（APB-SÚMATE）",
            "url": "https://web.oep.org.bo/organizaciones_politicas/apb-sumate/",
            "description": "玻利维亚多民族选举机构（OEP）官网APB Súmate政党专栏，载有法人资格授予决议（TSE-RSP-ADM N° 0453/2024）及政党基本信息。",
            "source": "OEP官网（搜索核实）"
        },
        {
            "name": "党章（Estatuto Orgánico APB Súmate，PDF）",
            "url": "https://web.oep.org.bo/wp-content/uploads/2024/12/ESTATUTO_ORGANICO_-APB_SUMATE.pdf",
            "description": "党章程官方文件，明确其为玻利维亚公民组成的全国性政党（partido político de alcance nacional），参与各级民主选举。",
            "source": "OEP官网文件库（搜索核实）"
        },
        {
            "name": "党徽图像文件（Wikimedia）",
            "url": "https://upload.wikimedia.org/wikipedia/en/9/92/Logo_of_the_APB_S%C3%BAmate.png",
            "description": "英文Wikipedia条目使用的APB Súmate党徽（logo）图像文件，浅紫-红-白配色。",
            "source": "Wikimedia/en.wikipedia（源自骨架profile.source_url）"
        }
    ],
    "key_people": [
        {
            "person_id": None,
            "name": "曼弗雷德·雷耶斯·比利亚 (Manfred Reyes Villa)",
            "title": "政治领袖 (Líder político)、建党领导人",
            "title_description": "党的创始人与最高政治领袖，现任科恰班巴市长；2025年以APB Súmate党魁身份竞选总统。",
            "description": "玻利维亚中右翼政治人物，1995年创立新共和力量党（NFR），曾长期担任科恰班巴市长并曾任科恰班巴州长。2021年以'Súmate'联盟当选科恰班巴市长（55.63%）；2024年12月推动其政治运动与公民团体Autonomía Para Bolivia合并组建全国性政党APB Súmate并任政治领袖。2025年大选获361,640票（6.75%，第五），2026-03-22以约47%得票（Sirepre口径）连任科恰班巴市长。"
        },
        {
            "person_id": None,
            "name": "亨利·帕雷德斯 (Henry Paredes)",
            "title": "党主席/全国总负责人 (Presidente / Jefe nacional)",
            "title_description": "据西语Wikipedia党信息框任党主席，正文称其为全国总负责人（jefe nacional）。",
            "description": "党内全国组织事务负责人；公开资料有限（信息主要来自西语Wikipedia单源），需以该党官方公告进一步核实。"
        },
        {
            "person_id": None,
            "name": "迭戈·布拉涅斯 (Diego Brañez)",
            "title": "众议院党团负责人 (Jefe de bancada en Diputados)",
            "title_description": "该党众议员，2026年立法年度代表党团就众议院领导层改选等事务发声。",
            "description": "APB Súmate籍众议员、众议院党团负责人。ERBOL（2026-10-19）与Brújula Digital（2026-08）报道均称其为'Diego Brañez'；西语Wikipedia党条目议员名单中同名议员记作'Andrés Brañez'，两源姓名拼写存在差异，此处以新闻来源为准。2026-10就新一届众议院指导层选举代表党团表态，称未收受争议'馈赠'并要求审议领导层开支报告。"
        },
        {
            "person_id": None,
            "name": "弗雷迪·卡马乔 (Freddy Camacho)",
            "title": "众议员、党团主要发言人",
            "title_description": "科恰班巴籍众议员（2025-11-03就任），党团对外表态的主要声音之一。",
            "description": "2026年10月宣布其党团将要求在新一届众议院指导层中获得职位，并争取主持一个议会委员会；此前亦多次代表党团就立法与政府相关议题公开表态。"
        },
        {
            "person_id": None,
            "name": "克劳迪娅·马永 (Claudia Mallón)",
            "title": "参议员（该党在参议院唯一席位）",
            "title_description": "科恰班巴籍参议员，2025-11-03就任，系该党在36席参议院中的唯一议员。",
            "description": "作为该党唯一参议员参与多民族立法大会立法事务，曾就该党法人资格授予决议日期相关的选举程序议题公开表态。"
        },
        {
            "person_id": None,
            "name": "胡安·卡洛斯·梅德拉诺 (Juan Carlos Medrano)",
            "title": "2025年副总统候选人",
            "title_description": "2025年大选中与曼弗雷德·雷耶斯·比利亚搭档竞选副总统。",
            "description": "代表APB Súmate参加2025-08-17大选，组合得票361,640票（6.75%，第五），未能进入决选。"
        }
    ],
    "departments": [
        {
            "name": "全国领导机构 (Dirección Nacional)",
            "dept_id": None,
            "head": "亨利·帕雷德斯 (Henry Paredes)",
            "description": "党的全国领导与执行机构：党主席（全国总负责人）亨利·帕雷德斯，政治领袖曼弗雷德·雷耶斯·比利亚。党部地址据西语Wikipedia信息框位于科恰班巴（C/ Antezana esq. Av. Salamanca），同一条目正文另称全国总负责人驻圣克鲁斯德拉谢拉，两处记载不一致。",
            "parent_dept_id": None
        },
        {
            "name": "众议院党团 (Bancada de Diputados)",
            "dept_id": None,
            "head": "迭戈·布拉涅斯 (Diego Brañez)",
            "description": "该党在多民族立法大会众议院的5席党团（2025-11-03就任）。据西语Wikipedia，成员包括弗雷迪·卡马乔（科恰班巴）、玛丽亚·埃斯特·贡戈拉（拉巴斯）、利内特·罗德里格斯、大卫·蒙塔尼奥（圣克鲁斯）及布拉涅斯。",
            "parent_dept_id": None
        },
        {
            "name": "参议院党团 (Bancada de Senadores)",
            "dept_id": None,
            "head": "克劳迪娅·马永 (Claudia Mallón)",
            "description": "该党在参议院的唯一席位党团（科恰班巴籍，2025-11-03就任）。",
            "parent_dept_id": None
        }
    ],
    "recent_events": [
        {
            "date": "2024-12-05",
            "title": "获TSE授予法人资格，正式注册为全国性政党",
            "description": "多民族选举机构最高选举法庭全体会议决议（Res. TSE-RSP-ADM N° 0453/2024，2024-12-05）授予Autonomía Para Bolivia Súmate（APB Súmate）政党法人资格；2024-12-13完成注册，由公民团体转为全国性政党（此前2024-11已提交逾106,000份签名）。",
            "impact": "取得参加全国选举的合法资格，为2025年大选铺路。",
            "source": "OEP官网 https://web.oep.org.bo/organizaciones_politicas/apb-sumate/；La Razón（2024-11-23）https://hemeroteca.larazon.bo/nacional/2024/11/23/reyes-villa-sumate-ya-supero-las-106-000-firmas-para-convertirse-en-un-frente-de-alcance-nacional/"
        },
        {
            "date": "2025-01-14",
            "title": "与公民团体Nueva Opción Social（NOS）签署政治联盟",
            "description": "APB Súmate与公民团体NOS（Nueva Opción Social）签署政治联盟，并将所组建的团结阵营命名为'Juntucha'。",
            "impact": "扩大2025年大选的联盟与动员基础。",
            "source": "ANF/Noticias Fides（2025-01-14）https://www.noticiasfides.com/nacional/politica/sumate-de-reyes-villa-firma-alianza-con-agrupacion-nos-y-llaman-juntucha-al-bloque-de-unidad"
        },
        {
            "date": "2025-05-15",
            "title": "率先注册2025年大选候选人，成为首个完成候选人注册的政党",
            "description": "APB Súmate成为2025年大选中第一个向选举机构启动候选人注册的政党。",
            "impact": "展示组织动员能力（据西语Wikipedia，2025年登记党员约110,878人）。",
            "source": "La Razón（2025-05-15）https://larazon.bo/nacional/2025/05/15/apb-sumate-es-el-primer-partido-en-inscribir-sus-candidaturas-para-las-elecciones/"
        },
        {
            "date": "2025-08-17",
            "title": "2025年大选首轮：雷耶斯·比利亚获6.75%（第五），党获5众议员+1参议员",
            "description": "雷耶斯·比利亚-梅德拉诺组合得票361,640票（6.75%），列第五，未能进入决选；该党在立法选举中赢得5个众议员席位和1个参议员席位。",
            "impact": "首次进入多民族立法大会，形成全国性议会党团。",
            "source": "西语Wikipedia（APB Súmate条目）https://es.wikipedia.org/wiki/APB_S%C3%BAmate；OEP结果公报PDF https://web.oep.org.bo/wp-content/uploads/2025/08/30-08-2025-Separata-resultados-EG2025.pdf"
        },
        {
            "date": "2025-08-21",
            "title": "宣布决选不站队：不支持帕斯亦不支持基罗加，党员投票自由",
            "description": "该党宣布在2025-10-19总统决选中不表态支持罗德里戈·帕斯或豪尔赫·基罗加任何一方，党员投票自由，并将重心转向2026年地方选举的重组。",
            "impact": "与随后执政的帕斯阵营保持距离，巩固科恰班巴基本盘与独立定位。",
            "source": "Opinion.com.bo（2025-08-21）https://www.opinion.com.bo/pais/apb-sumate-decide-que-apoyara-paz-ni-tuto-segunda-vuelta/20250821175038978644.html"
        },
        {
            "date": "2026-03-22",
            "title": "地方选举：雷耶斯·比利亚以约47%连任科恰班巴市长，全国获6市长",
            "description": "2026年地方选举初步计票（Sirepre）显示，雷耶斯·比利亚以46.8%-47.7%大幅领先连任科恰班巴市长；该党全国共赢得6个市长职位、9个省级议会议席，但未获任何州长职位。",
            "impact": "巩固该党最重要的市级执政地盘（科恰班巴），维持全国存在感。",
            "source": "Correo del Sur（2026-03-22）https://correodelsur.com/politica/20260322/manfred-reyes-villa-es-reelecto-como-alcalde-de-cochabamba-segun-datos-del-sirepre.html；Opinion.com.bo https://www.opinion.com.bo/cochabamba/resultados-preliminares-manfred-es-reelegido-alcalde-zavaleta-sorprende-como-segundo/20260322235154990475.html；Noticias Fides https://www.noticiasfides.com/nacional/politica/manfred-reyes-villa-es-reelecto-como-alcalde-de-cochabamba"
        },
        {
            "date": "2026-10-19",
            "title": "党团要求在新一届众议院指导层获职位并主持委员会",
            "description": "在2026-11-08开始的新立法年度前，该党众议院党团（负责人迭戈·布拉涅斯、众议员弗雷迪·卡马乔）表示将要求在众议院指导层中获得职位并主持一个议会委员会，并批评现任众议院领导层（PDC的罗伯托·卡斯特罗）存在行政争议；党团同时评估联盟角色与下一步选举定位。",
            "impact": "以5+1席争取立法机构话语权，在执政联盟与反对派之间保持要价能力。",
            "source": "Opinion.com.bo/ERBOL（2026-10-19）https://www.opinion.com.bo/pais/viene-eleccion-directiva-diputados-medio-denuncias-dadivas-reelegir-presidente/20261019094654997821.html；El Diario（2026-10-21）https://www.eldiario.net/portal/2026/10/21/diputados-perfilan-nueva-directiva-entre-divisiones/"
        }
    ],
    "related_entities": [
        {
            "org_id": None,
            "org_name": "Nueva Opción Social (NOS)",
            "org_type": "PARTY",
            "org_description": "玻利维亚公民政治团体（Agrupación Ciudadana Nueva Opción Social）。",
            "relationship_type": "strategic_alliance"
        },
        {
            "org_id": None,
            "org_name": "Fuerza Republicana Democrática Nacional (Súmate)",
            "org_type": "PARTY",
            "org_description": "2021年雷耶斯·比利亚为科恰班巴市选举组建的政治联盟（含ADN、RETO等，简称'Súmate'，赢得2021年科恰班巴市长选举）；2024年12月并入并改组为全国性政党APB Súmate。",
            "relationship_type": "predecessor"
        },
        {
            "org_id": None,
            "org_name": "Autonomía Para Bolivia (APB)",
            "org_type": "PARTY",
            "org_description": "2005年成立的公民团体，曾参与2009年'Plan Progreso para Bolivia-Convergencia Nacional'联盟；2024年以其注册名义向TSE申请转为全国性政党，即今日的APB Súmate。",
            "relationship_type": "predecessor"
        },
        {
            "org_id": None,
            "org_name": "Nueva Fuerza Republicana (NFR)",
            "org_type": "PARTY",
            "org_description": "曼弗雷德·雷耶斯·比利亚1995年创立的政党（已消亡），曾为全国主要中右翼力量之一；APB Súmate继承其政治传统与党色（浅紫、红、白），系该党的历史渊源组织。",
            "relationship_type": "predecessor"
        }
    ],
    "core_business": "APB Súmate（Autonomía Para Bolivia Súmate，玻利维亚自治-加入党）是2024年12月在玻利维亚多民族选举机构注册的全国性中右翼政党，由科恰班巴市长曼弗雷德·雷耶斯·比利亚创建并任政治领袖。意识形态上主张自由保守主义、混合经济、地方主义、联邦制与自治主义，党色为浅紫、红、白，据西语Wikipedia其2025年登记党员约110,878人。核心活动是组织并参加选举：2025年8月大选中推出雷耶斯·比利亚-梅德拉诺总统组合（得票6.75%，列第五），赢得5个众议员席位与1个参议员席位（2025-11-03就任）；2026年3月地方选举赢得6个市长职位（含科恰班巴市连任）但未获州长职位。在国会以党团形式参与立法与监督，2026年立法年度要求进入众议院指导层并主持委员会。组织上设全国领导机构与众、参两院党团；据西语Wikipedia信息框党部位于科恰班巴（C/ Antezana esq. Av. Salamanca），另有记载称全国总负责人驻圣克鲁斯德拉谢拉。对外沟通以Facebook主页为主，无独立官网。",
    "industries": ["public_administration"],
    "apec_stance": "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。玻利维亚的对外经贸与区域一体化参与集中在拉美区域机制（如安第斯共同体成员、南方共同市场联系国），未参与APEC框架下的亚太经贸合作议程，因此APB Súmate作为玻利维亚政党不存在公开的APEC相关立场文件；该党对外经贸主张以地区自治、吸引投资为主。",
    "profile": {
        "source_url": "https://upload.wikimedia.org/wikipedia/en/9/92/Logo_of_the_APB_S%C3%BAmate.png?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail_unscaled",
        "local_path": None
    },
    "collection_meta": {
        "collection_date": "2026-10-24",
        "phase": "phase3_enriched",
        "data_sources": [
            "wikidata",
            "wikipedia",
            "es.wikipedia.org",
            "web.oep.org.bo",
            "opinion.com.bo",
            "noticiasfides.com (ANF)",
            "larazon.bo",
            "correodelsur.com",
            "eldiario.net",
            "facebook.com"
        ],
        "quotes": [
            {
                "title": "APB Súmate - Wikipedia, la enciclopedia libre（建党日期、领袖、议席、选举结果）",
                "url": "https://es.wikipedia.org/wiki/APB_S%C3%BAmate"
            },
            {
                "title": "APB-SÚMATE | Órgano Electoral Plurinacional（法人资格授予决议）",
                "url": "https://web.oep.org.bo/organizaciones_politicas/apb-sumate/"
            },
            {
                "title": "Súmate de Reyes Villa firma alianza con agrupación NOS y llaman Juntucha al bloque de unidad（ANF，2025-01-14）",
                "url": "https://www.noticiasfides.com/nacional/politica/sumate-de-reyes-villa-firma-alianza-con-agrupacion-nos-y-llaman-juntucha-al-bloque-de-unidad"
            },
            {
                "title": "APB Súmate decide que no apoyará a Paz ni a Tuto en segunda vuelta（Opinion.com.bo，2025-08-21）",
                "url": "https://www.opinion.com.bo/pais/apb-sumate-decide-que-apoyara-paz-ni-tuto-segunda-vuelta/20250821175038978644.html"
            },
            {
                "title": "Manfred Reyes Villa es reelecto como alcalde de Cochabamba，según datos del Sirepre（Correo del Sur，2026-03-22）",
                "url": "https://correodelsur.com/politica/20260322/manfred-reyes-villa-es-reelecto-como-alcalde-de-cochabamba-segun-datos-del-sirepre.html"
            },
            {
                "title": "APB-Súmate es el primer partido en inscribir sus candidaturas para las elecciones（La Razón，2025-05-15）",
                "url": "https://larazon.bo/nacional/2025/05/15/apb-sumate-es-el-primer-partido-en-inscribir-sus-candidaturas-para-las-elecciones/"
            },
            {
                "title": "Se viene elección de directiva de Diputados en medio de denuncias de dádivas（Opinion/ERBOL，2026-10-19，含APB Súmate党团负责人表态）",
                "url": "https://www.opinion.com.bo/pais/viene-eleccion-directiva-diputados-medio-denuncias-dadivas-reelegir-presidente/20261019094654997821.html"
            }
        ],
        "completeness_score": 9,
        "notes": "由phase2骨架升级为phase3画像（2026-10搜索核实）。重要更正：任务简报称该党由前圣克鲁斯省长Rubén Costas创立，与2025-2026年多来源（西/英Wikipedia、OEP、主流媒体）不符——该党由曼弗雷德·雷耶斯·比利亚于2024-12创建并任政治领袖，未发现Rubén Costas与其的可靠关联。无独立官网；亨利·帕雷德斯任职信息为西语Wikipedia单源；党部所在地两处记载不一致；众议员Brañez姓名在Wikipedia（Andrés）与新闻（Diego）间存在拼写差异。上述不确定项均在字段中注明。全部人员均未命中_name_index，person_id置null；related_entities中NOS及两个前身组织未命中索引，org_id置null。"
    }
}

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("written:", PATH)

# -*- coding: utf-8 -*-
"""Build BO-PERSON-000466 Sergio Criales Aguirre (WWF Bolivia Director de País)."""
import json
import os

OUT = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons\BO-PERSON-000466.json"

WWF_ORG = "世界自然基金会玻利维亚办公室 (WWF-Bolivia)"

person = {
    "person_id": "BO-PERSON-000466",
    "wikidata_qid": None,
    "name_zh": None,
    "name": "Sergio Criales Aguirre",
    "name_en": "Sergio Criales Aguirre",
    "aliases": ["Sergio Criales"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "contacts": [
        {
            "type": "website",
            "value": "https://www.wwf.org.bo",
            "source": "WWF玻利维亚官网（其任职工机构的公开联系渠道，非个人主页）"
        },
        {
            "type": "phone",
            "value": "+591-3-4624969",
            "source": "WWF玻利维亚官网联系页（圣克鲁斯机构办公电话，非个人直线）"
        }
    ],
    "current_positions": [
        "世界自然基金会玻利维亚办公室国家主任"
    ],
    "education": [],
    "work_experience": [
        {
            "start_date": "2025",
            "end_date": None,
            "organization": WWF_ORG,
            "org_id": "BO-NGO-011",
            "position": "国家主任",
            "is_current": "true",
            "source": "https://www.wwf.org.bo/sobre_nosotros/nuestro_equipo/; https://web.archive.org/web/20251109153600/https://www.wwf.org.bo/sobre_nosotros/nuestro_equipo/",
            "start_date_note": "精确任命日期未公开。2025-03-31 WWF官方新闻稿中该机构仍由Alfonso Llobet以代理国家代表（Representante País a.i.）身份主持；2025-11-09官网团队页Wayback存档已列其为Director de País，据此推定2025年内（约4—11月间）就任。org_id按_name_index.json映射取WWF Bolivia=BO-NGO-011。",
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000467",
            "person_name": "豪尔迪·苏尔金·贝内里亚 (Jordi Surkin Beneria)",
            "relationship_type": "colleague",
            "description": "同在WWF玻利维亚办公室领导层：Criales任国家主任，Surkin任保护高级总监（Director Senior de Conservación），两人并列见于官网「Nuestro equipo」团队页。勿混淆两人。",
            "source": "https://www.wwf.org.bo/sobre_nosotros/nuestro_equipo/",
        },
        {
            "person_id": "BO-PERSON-000469",
            "person_name": "萨穆埃尔·桑圭萨·帕尔多 (Samuel Sangüeza Pardo)",
            "relationship_type": "colleague",
            "description": "WWF玻利维亚办公室「永久融资计划」（Programa de Financiamiento para la Permanencia, PFP）项目总监，与Criales同列官网团队页领导层。",
            "source": "https://www.wwf.org.bo/sobre_nosotros/nuestro_equipo/"
        },
        {
            "person_id": "BO-PERSON-000468",
            "person_name": "阿方索·洛贝特·克雷哈苏 (Alfonso Llobet Querejazu)",
            "relationship_type": "associate",
            "description": "2025年3月WWF官方新闻稿中仍以代理国家代表（Representante País a.i.）身份代表WWF玻利维亚公开表态；其后Criales以国家主任身份出现，洛贝特为其前任（代理）。",
            "source": "https://www.wwf.org.bo/?394270/Bolivia-se-ilumina-en-la-Hora-del-Planeta-2025-con-un-llamado-urgente-a-proteger-el-agua"
        },
        {
            "person_id": "BO-PERSON-000072",
            "person_name": "奥斯卡·马里奥·胡斯蒂尼亚诺·平托 (Óscar Mario Justiniano Pinto)",
            "relationship_type": "associate",
            "description": "玻利维亚生产可持续、环境与水务部长。2026年10月纽约气候周期间与Criales率领的WWF玻利维亚团队举行双边会晤，部长表态支持PFP并同意推进WWF与政府间谅解备忘录。",
            "source": "https://www.wwf.org.bo/?401771/WWF-Bolivia-fortalece-alianzas-para-impulsar-la-conservacion-y-el-financiamiento-climatico-en-Bolivia-desde-Nueva-York"
        },
        {
            "person_id": None,
            "person_name": "印第安娜·阿斯卡伦斯 (Indiana Ascarrunz)",
            "relationship_type": "associate",
            "description": "圣克鲁斯省教育厅自然环境局（DIRENA）局长。2026年10月在野生动物救助中心（CAD）设备交接活动中与Criales共同出席，分别代表省方与WWF玻利维亚表态。",
            "source": "https://www.wwf.org.bo/?402010/Fauna-Silvestre-se-fortalece-al-Centro-de-Atencion-y-Derivacion-de-Fauna-Silvestre-de-Santa-Cruz-para-el-rescate-ante-posibles-incendios"
        },
    ],
    "social_accounts": [],
    "family_members": [],
    "political_stances": [
        {
            "date": "2026-03-25",
            "topic": "保护区保护（2026年「地球一小时」玻利维亚主题）",
            "stance_content": "为2026年「地球一小时」玻利维亚活动（主题「保护区时刻」）表态：保护区是「我们自然的心脏，是子孙后代的生命保障。今天我们比以往任何时候都更需要联合力量保护它们。「地球一小时」是一次从反思走向行动的邀请，证明只要共同行动，我们就能带来改变」。报道同时指出玻利维亚保护区仍保持良好保护状态，但面临毁林、森林火灾及改变生态系统的活动扩张等日益增大的压力。",
            "source": "https://eldia.com.bo/2026-03-25/pais/hora-del-planeta-2026-una-hora-por-nuestras-areas-protegidas.html",
        },
        {
            "date": "2026-10-05",
            "topic": "保护区长效融资机制（永久融资计划PFP）",
            "stance_content": "在纽约气候周及联合国大会期间代表WWF玻利维亚与玻政府及国际组织会晤，称「这些空间使我们得以加强与玻利维亚政府及与国家长期保护愿景一致的组织间的对话。WWF玻利维亚正推动永久融资计划（PFP）等机制，为全国及恰瓜瓜·伊扬巴埃（Charagua Iyambae）原住民保护区创造长期融资条件」。会后玻政府表态支持PFP，并同意推进WWF与政府间谅解备忘录。",
            "source": "https://www.wwf.org.bo/?401771/WWF-Bolivia-fortalece-alianzas-para-impulsar-la-conservacion-y-el-financiamiento-climatico-en-Bolivia-desde-Nueva-York",
        },
        {
            "date": "2026-10-05",
            "topic": "全球热带森林融资（TFFF热带森林永久基金）",
            "stance_content": "参加WWF与联合国开发计划署（PNUD）共同主办的「热带森林永久基金」（Tropical Forests Forever Facility, TFFF）活动，支持玻利维亚接入TFFF等承认热带国家森林保护努力的融资机制；其间玻生产可持续、环境与水务部长 Óscar Mario Justiniano 强调玻利维亚应能获取该基金。此系其气候融资立场的组成部分。",
            "source": "https://www.wwf.org.bo/?401771/WWF-Bolivia-fortalece-alianzas-para-impulsar-la-conservacion-y-el-financiamiento-climatico-en-Bolivia-desde-Nueva-York",
        },
        {
            "date": "2025-11",
            "topic": "环境与国家繁荣的关系",
            "stance_content": "在官网团队页阐述其领导理念：「激励我的是领导WWF玻利维亚的优秀团队，创造让所有人都能与自然和谐共处的持久解决方案——我坚信，国家的繁荣未来与环境健康密不可分」。",
            "source": "https://web.archive.org/web/20251109153600/https://www.wwf.org.bo/sobre_nosotros/nuestro_equipo/"
        },
        {
            "date": "2026-10-23",
            "topic": "野生动物救助与机构协作（火灾应急）",
            "stance_content": "在圣克鲁斯野生动物救助与转运中心（CAD）设备交接活动（隶属WWF意大利资助的「玻利维亚亚马逊——森林火灾紧急项目」）上，强调支持一线野生动物救助团队、维持机构间协作：「CAD的工作对于应对威胁我们野生动物的局面至关重要。每一次救助背后都有训练有素、尽职尽责的人员，他们需要合适的工具来安全地开展工作」。",
            "source": "https://www.wwf.org.bo/?402010/Fauna-Silvestre-se-fortalece-al-Centro-de-Atencion-y-Derivacion-de-Fauna-Silvestre-de-Santa-Cruz-para-el-rescate-ante-posibles-incendios"
        },
    ],
    "major_achievements": [
        {
            "date": "2025",
            "achievement": "出任世界自然基金会玻利维亚办公室（WWF-Bolivia）国家主任（Director de País），接替此前以代理身份主持机构的Alfonso Llobet，成为该环保组织在玻利维亚的最高负责人。",
            "organization": WWF_ORG,
        },
        {
            "date": "2026-03-28",
            "achievement": "领导2026年「地球一小时」玻利维亚活动，以「保护区时刻」为主题，全国九个省份（拉巴斯、圣克鲁斯、科恰班巴、波托西、埃尔阿尔托、潘多等）联动举办保护区参观、集市、座谈等活动，推动公众关注保护区面临的毁林与火灾压力。",
            "organization": WWF_ORG,
        },
        {
            "date": "2026-10-05",
            "achievement": "率WWF玻利维亚团队参加纽约气候周，与玻利维亚政府及国际组织举行双边会晤，推动「永久融资计划」（PFP）设计进入最后阶段：玻利维亚政府表态支持PFP为国家战略选项，并同意推进WWF与政府间谅解备忘录签署。",
            "organization": WWF_ORG,
        },
        {
            "date": "2026-10-23",
            "achievement": "代表WWF玻利维亚向圣克鲁斯野生动物救助与转运中心（CAD）交付救助装备与防护物资，强化火灾季一线野生动物救助能力；项目由WWF意大利资助，系上一年度同类支持的延续。",
            "organization": WWF_ORG,
        },
    ],
    "biography_summary": "塞尔希奥·克里亚莱斯·阿吉雷（Sergio Criales Aguirre）是环境保护组织世界自然基金会玻利维亚办公室（WWF-Bolivia）现任国家主任（Director de País）。2025年3月该机构仍由阿方索·洛贝特以代理国家代表身份主持，2025年11月官网团队页存档已列克里亚莱斯为国家主任，据此推定其于2025年内接任。就任后他频繁代表机构就保护区与气候融资议题公开表态：2026年3月主导以「保护区时刻」为主题的地球一小时活动，称保护区是「自然的心脏、子孙后代的生命保障」；2026年10月率团出席纽约气候周，与玻利维亚生产可持续、环境与水务部长奥斯卡·马里奥·胡斯蒂尼亚诺会晤，推动「永久融资计划」（PFP）与热带森林永久基金（TFFF）等长效资金机制，政府同意推进与WWF的谅解备忘录。其团队页自述信条为「国家的繁荣未来与环境健康密不可分」。注意：克里亚莱斯为圣克鲁斯常见姓氏，玻利维亚另有同名者塞尔希奥·阿尔贝托·克里亚莱斯·阿吉雷（本库BO-PERSON-000792），须加以区分；其出生日期、出生地、学历及就任WWF前的履历均未见公开报道。",
    "profile": None,
    "position_note": "西班牙语职称 Director de País / Director País（两种拼法均见于报道），对应机构最高负责人，等同于国家代表（Representante País）职位。",
    "work_note": "就任WWF前的职业履历未见公开报道，work_experience仅含现职。2025-03-31官方新闻稿（Hora del Planeta 2025）中Alfonso Llobet头衔为「Representante País a.i.」（代理国家代表）；2025-11-09团队页存档中Criales已是「Director de País」，任命窗口据此推定。",
    "social_accounts_note": "已按要求扫描X/Twitter、LinkedIn、Facebook、Instagram、YouTube、TikTok六平台：未发现可归属本人的个人账号（本环境搜索引擎受限：Google 429、Bing软拦截、DDG/Brave/Yandex/Ecosia均拦截）。X/Instagram/Facebook/YouTube上仅存在WWF玻利维亚机构账号（@wwf_bolivia、@wwfbolivia、boliviawwf等），已记录于组织档案BO-NGO-011，非个人账号。",
    "identity_note": "存在同名异人：本库另有BO-PERSON-000792「Sergio Alberto Criales Aguirre」（含中间名Alberto），与本条目BO-PERSON-000466为不同个体；媒体报道中的「Sergio Criales（WWF玻利维亚国家主任）」均指本条目对象。Wikidata检索命中的Q82266266「Sergio Criales」为阿根廷研究者，非同一人，故wikidata_qid置null。",
    "collection_meta": {
        "collection_date": "2026-10-26",
        "phase": "phase4_person_profile",
        "data_sources": ["official_website", "news_search", "web_search"],
        "notes": "收集环境受限：WebSearch配额耗尽、主流搜索引擎（Google/Bing/DDG/Brave/Yandex/Ecosia/Mojeek，含Bing RSS输出）均拦截或返回缓存垃圾结果，改用Google News RSS+官网直取+Wayback Machine CDX定位来源并精读全文。已精读全文来源：(1)WWF玻利维亚官网团队页及其2025-11-09存档；(2)El Día 2026-03-25地球一小时报道；(3)La Voz de Tarija 2026-03-28报道；(4)WWF官网2026-10-05纽约气候周新闻稿；(5)WWF官网2026-10-23野生动物救助中心（CAD）新闻稿；(6)WWF官网2025-03-31地球一小时2025新闻稿（佐证前任代理身份）；另有El Potosí、ABI、Bolivia.com等至少4家媒体转载同一新闻稿佐证。关键事实（现任国家主任、保护区表态、PFP推动、火灾应急表态）均有≥2独立来源。存疑/留空项：出生日期、出生地、学历、家庭、就任WWF前履历均未见公开资料，留空；精确任命日期未公开（2025-04至2025-11区间推定），见start_date_note；个人社交媒体六平台扫描未获可验证账号，social_accounts留空。completeness_score客观上限说明：无Wikidata条目、无个人社媒账号、无公开出生/学历信息，分值受缺项限制，非收集疏漏。",
        "quotes": [
            {
                "title": "Nuestro equipo - WWF Bolivia（官网团队页：SERGIO CRIALES - Director de País）",
                "url": "https://www.wwf.org.bo/sobre_nosotros/nuestro_equipo/"
            },
            {
                "title": "Hora del Planeta 2026: una hora por nuestras Áreas Protegidas - EL DÍA",
                "url": "https://eldia.com.bo/2026-03-25/pais/hora-del-planeta-2026-una-hora-por-nuestras-areas-protegidas.html"
            },
            {
                "title": "Hora del Planeta 2026: Conozca las actividades que se desarrollarán en los nueve departamentos - La Voz de Tarija",
                "url": "https://lavozdetarija.com/2026/03/28/hora-del-planeta-2026-conozca-las-actividades-que-se-desarrollaran-en-los-nueve-departamentos/"
            },
            {
                "title": "WWF-Bolivia fortalece alianzas para impulsar la conservación y el financiamiento climático en Bolivia desde Nueva York | WWF",
                "url": "https://www.wwf.org.bo/?401771/WWF-Bolivia-fortalece-alianzas-para-impulsar-la-conservacion-y-el-financiamiento-climatico-en-Bolivia-desde-Nueva-York"
            },
            {
                "title": "Bolivia se ilumina en la Hora del Planeta 2025 con un llamado urgente a proteger el agua | WWF（佐证Alfonso Llobet时任代理国家代表）",
                "url": "https://www.wwf.org.bo/?394270/Bolivia-se-ilumina-en-la-Hora-del-Planeta-2025-con-un-llamado-urgente-a-proteger-el-agua"
            },
            {
                "title": "Nuestro equipo - WWF Bolivia（Wayback Machine 2025-11-09存档，佐证任命窗口）",
                "url": "https://web.archive.org/web/20251109153600/https://www.wwf.org.bo/sobre_nosotros/nuestro_equipo/"
            },
            {
                "title": "Fauna Silvestre: se fortalece al Centro de Atención y Derivación de Fauna Silvestre de Santa Cruz para el rescate ante posibles incendios | WWF",
                "url": "https://www.wwf.org.bo/?402010/Fauna-Silvestre-se-fortalece-al-Centro-de-Atencion-y-Derivacion-de-Fauna-Silvestre-de-Santa-Cruz-para-el-rescate-ante-posibles-incendios"
            }
        ]
    },
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(person, f, ensure_ascii=False, indent=2)
print("written:", OUT)
print("bytes:", os.path.getsize(OUT))

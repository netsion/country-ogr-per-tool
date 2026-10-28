# -*- coding: utf-8 -*-
"""Build BO-PERSON-000400 Eddy Ariel Peñaloza Rada person profile JSON."""
import json
import os

OUT = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000400.json"

person = {
    "person_id": "BO-PERSON-000400",
    "wikidata_qid": None,
    "name": "Eddy Ariel Peñaloza Rada",
    "name_en": "Eddy Ariel Penaloza Rada",
    "name_zh": None,
    "aliases": ["Eddy Peñaloza", "Eddy Peñaloza Rada"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_date_note": "未检索到任何公开的出生日期或年龄信息，birth_date 置 null。",
    "birth_place": None,
    "name_zh_note": "检索中文维基百科、华文媒体均未发现其既有标准中文译名，按规则 name_zh 置 null；传记内「埃迪·阿里埃尔·佩尼亚洛萨·拉达」仅为内部参考音译。",
    "contacts": [
        {
            "type": "email",
            "value": "eddy.penaloza@boliviatv.bo",
            "source": "Bolivia TV 官网 Contactos 页现任领导名录（2026-10-27 直读）：Director Nacional de Noticias Eddy Ariel Peñaloza Rada, Correo: eddy.penaloza@boliviatv.bo"
        }
    ],
    "current_positions": [
        "玻利维亚国家电视台国家新闻总监"
    ],
    "position_note": "现任职务三源确认：(1) Bolivia TV 官网 Contactos 页现任领导名录（2026-10-27 直读，列于新闻信息部条线）；(2) 其 LinkedIn（搜索摘要）自述 Director Nacional de Noticias, Bolivia TV, 2025年12月起；(3) Bolivia Verifica 2026-10-07 报道称其为「Eddy Peñaloza, director nacional de Noticias de Bolivia TV」。隶属新闻信息部，直接上级为新闻信息部总经理 Álvaro Irusta（BO-PERSON-000399），台最高负责人为总经理 Carlos Villazón（BO-PERSON-000398），三人职务已严格区分。",
    "work_experience": [
        {
            "start_date": "2025-12",
            "end_date": None,
            "organization": "玻利维亚国家电视台 (Bolivia TV)",
            "org_id": "BO-MEDIA-012",
            "position": "国家新闻总监",
            "location": "拉巴斯 (La Paz)",
            "is_current": "true",
            "source": "https://bo.linkedin.com/in/eddy-ariel-pe%C3%B1aloza-rada-7a08b1300",
            "description": "2025年12月（罗德里戈·帕斯新政府上台约一个月后）进入 Bolivia TV 新闻领导层，统筹全国新闻内容编排，隶属新闻信息部。2025-12-10 Notiviral（Facebook 页，援引 BlockNoticias）报道其入职时头衔为「jefatura de prensa（新闻主管）」，同期新闻信息部总经理为 Álvaro Irusta、总经理为 Daniel Castellón；现职头衔「Director Nacional de Noticias（国家新闻总监）」见官网现任名录、其 LinkedIn 及 Bolivia Verifica 2026-10-07 报道。晋升为总监的具体日期未查明。",
            "note": "LinkedIn 标注该职起始为 2025年12月（dic 2025）；官网名录同时列出其工作邮箱 eddy.penaloza@boliviatv.bo（2026-10-27 直读）。"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚第一台 (Red Uno)",
            "org_id": "BO-MEDIA-010",
            "position": "记者",
            "location": "拉巴斯 (La Paz)",
            "is_current": "false",
            "source": "https://vocesdelsurunidas.org/incidentes/productores-de-coca-golpean-a-periodistas-de-tv-red-uno",
            "description": "任 Red Uno《Notivisión》节目记者。2022-08-09 晚与摄像师在拉巴斯比利亚法蒂玛区（Villa Fátima）采访 Yungas 古柯农（Adepcoca）扣留一名女警的对峙事件时遭袭击：其面部中拳、摄像机落地，当时正进行现场直播（ANP 通稿，经 ANP/Voces del Sur 报道）。2023-05 与同事 Elvis Torres 以揭露埃尔阿尔托地下留宿场所乱象的调查报道系列《Alojamientos Clandestinos》获 Unifranz 首届「弗朗茨·塔马约调查新闻奖」电视类金奖。入职与离任 Red Uno 的具体年份未查明（2025-12 已入职 Bolivia TV，故离任不晚于2025年）。",
            "note": "《Notivisión》节目归属见 Voces del Sur 报道原文「Un periodista del programa Notivisión del canal privado de televisión Red Uno de Bolivia」；获奖见 Unifranz 官方博客（2023-05-16）。"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚ATB电视台 (Red ATB)",
            "org_id": "BO-MEDIA-011",
            "position": "记者",
            "location": "玻利维亚 (Bolivia)",
            "is_current": "false",
            "source": "https://boliviaverifica.bo/este-titular-atribuido-a-la-red-atb-fue-editado",
            "description": "任 Red ATB 电视台记者。2020-03-06 早间新闻就埃尔阿尔托「Juntos」联盟竞选总部（calle 6 与 av. 6 de Marzo 交叉口）前夜被毁事件进行 07:03 现场连线，字幕条题为「Destrozos en la casa de campaña de Juntos」；就网传第二张截图，其向 Bolivia Verifica 证实系伪造：「el generador de la segunda imagen que está circulando es falsa. Han alterado el generador de canal」（网传第二图的字幕生成器是伪造的，有人篡改了台标生成器）。任职起止年份未查明。",
            "note": "Bolivia Verifica 事实核查报道（2020-03-06 刊发）直接称其为 Red ATB 记者并引述其原话；2022 年已在 Red Uno 任职，故 ATB 任期应早于2022年。"
        }
    ],
    "education": [
        {
            "institution": "山谷大学 (Universidad del Valle)",
            "degree": None,
            "field": None,
            "start_date": None,
            "end_date": None,
            "source": "https://bo.linkedin.com/in/eddy-ariel-pe%C3%B1aloza-rada-7a08b1300",
            "note": "仅据其 LinkedIn 个人资料搜索摘要（其两个 LinkedIn 账号均显示「Educated at Universidad del Valle (Bolivia)」）；LinkedIn authwall 拦截未能直读原文，学位、专业与起止年份均未知。"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000399",
            "person_name": "阿尔瓦罗·伊鲁斯塔·贝尔纳尔 (Álvaro Irusta Bernal)",
            "relationship_type": "superior",
            "description": "Álvaro Irusta 任 Bolivia TV 新闻信息部总经理（Gerente de Informaciones），为国家新闻总监的直接上级；2025-12-10 Notiviral（援引 BlockNoticias）报道两人同批加入该台新领导层（Irusta 掌新闻信息部、Peñaloza 任新闻主管）。官网现任名录将两人同列于新闻条线。",
            "source": "https://www.boliviatv.bo/principal/contactos.php"
        },
        {
            "person_id": "BO-PERSON-000398",
            "person_name": "路易斯·卡洛斯·比利亚松·马丁内斯 (Luis Carlos Villazón Martínez)",
            "relationship_type": "superior",
            "description": "Carlos Villazón 于 2026-01-07 获帕斯政府任命出任 Bolivia TV 总经理（Gerente General），为 Peñaloza 在台内的最高上级；官网现任名录列其为台第一负责人。",
            "source": "https://www.boliviatv.bo/principal/contactos.php"
        },
        {
            "person_id": None,
            "person_name": "埃尔维斯·托雷斯 (Elvis Torres)",
            "relationship_type": "colleague",
            "description": "Red Uno 时期的记者同事；2023年5月两人共同以《Alojamientos Clandestinos》系列调查报道获 Unifranz 首届「弗朗茨·塔马约调查新闻奖」电视类金奖。",
            "source": "https://unifranz.edu.bo/blog/periodismoinvestigacion"
        }
    ],
    "social_accounts": [
        {
            "platform": "twitter_x",
            "account_name": "@eddypenaloza",
            "url": "https://x.com/eddypenaloza",
            "source": "搜索摘要（2026-10-27）：显示名「Eddy Peñaloza Rada」与本人全名完全一致，2012年5月注册，发布拉巴斯市政新闻类内容（如市长与比利亚圣安东尼奥居民辩论）；X 登录墙拦截未能直读原文，身份匹配基于全名一致+内容领域吻合。"
        },
        {
            "platform": "twitter_x",
            "account_name": "@epenalozarada",
            "url": "https://x.com/epenalozarada",
            "source": "搜索摘要：显示名「Eddy Peñaloza Rada」与本人全名完全一致，2016年推文涉及玻利维亚诈骗事件新闻；仅见单条旧推文摘要，是否为其本人现用账号待核。"
        },
        {
            "platform": "linkedin",
            "account_name": "Eddy Ariel Peñaloza Rada",
            "url": "https://bo.linkedin.com/in/eddy-ariel-pe%C3%B1aloza-rada-7a08b1300",
            "source": "搜索摘要（2026-10-27）：自述「Periodista y Productor de Noticias」，Director Nacional de Noticias, Bolivia TV, 2025年12月起，常驻拉巴斯，母校 Universidad del Valle；authwall 拦截未能直读原文。全名与现任职务均与官网名录互证。"
        },
        {
            "platform": "linkedin",
            "account_name": "Eddy Ariel Peñaloza Rada",
            "url": "https://bo.linkedin.com/in/eddy-ariel-pe%C3%B1aloza-rada-b81417142",
            "source": "搜索摘要：显示「Periodista en Red Uno de Bolivia」、同校 Universidad del Valle（BO）、23 位关注者；与其现任账号同名同校，疑为同一人早期账号（对应其 Red Uno 任职期），两账号归属同一性待核。"
        }
    ],
    "social_accounts_note": "6 平台扫描已完成（X、Facebook、LinkedIn、Instagram、TikTok、YouTube）。X 两个账号与 LinkedIn 两个账号均依搜索摘要收录（显示名与本人全名完全一致/职务互证），并逐一注明核实状态与限制；Facebook、Instagram（@eddypenalozapolar、@eddy55927）、TikTok（@eddypenaloza0）、YouTube（@eddypenaloza7526、@eddypenaloza5256）仅见同名账号且无任何职业身份佐证，无法确认属本人，均不收录。",
    "family_members": [],
    "family_note": "未检索到任何关于其家庭成员（配偶、子女等）的公开信息，family_members 留空。",
    "political_stances": [],
    "political_stances_note": "未检索到其个人政治立场表态。其 2020 年在 ATB 期间向 Bolivia Verifica 证实网传截图伪造、2022 年 Red Uno 期间采访 Adepcoca 古柯农与警方冲突，均属职务新闻报道行为，不计入个人政治立场。",
    "major_achievements": [
        {
            "date": "2023-05",
            "achievement": "与 Red Uno 同事 Elvis Torres 凭揭露埃尔阿尔托（El Alto）地下留宿场所乱象（涉及性工作者及未成年人性剥削问题）的调查报道系列《Alojamientos Clandestinos》，获 Unifranz 首届「弗朗茨·塔马约调查新闻奖」（Reconocimiento Franz Tamayo al Periodismo de Investigación）电视类金奖；评审团由美洲西班牙语新闻出版大会（纽约）指定并经美洲新闻协会（SIP，迈阿密）背书",
            "organization": "弗朗茨·塔马约大学 (Universidad Franz Tamayo, Unifranz)"
        },
        {
            "date": "2025-12",
            "achievement": "帕斯新政府上台后获任进入玻利维亚国家电视台（Bolivia TV）新闻领导层（先以新闻主管/jefe de prensa 身份入职，现任国家新闻总监），执掌国家台全国新闻条线",
            "organization": "玻利维亚国家电视台 (Bolivia TV)"
        }
    ],
    "biography_summary": "埃迪·阿里埃尔·佩尼亚洛萨·拉达（Eddy Ariel Peñaloza Rada）是玻利维亚资深电视新闻记者兼新闻制作人，现任国有玻利维亚国家电视台（Bolivia TV，Canal 7）国家新闻总监。他早年供职于私营玻利维亚ATB电视台（Red ATB）任记者，2020年3月曾就埃尔阿尔托「Juntos」联盟竞选总部被毁事件进行早间现场连线，并向事实核查机构 Bolivia Verifica 证实网传现场截图系伪造。其后转入玻利维亚第一台（Red Uno）任《Notivisión》节目记者：2022年8月与摄像师在拉巴斯比利亚法蒂玛区采访古柯农扣留女警的对峙事件时遭袭击、面部中拳；2023年5月与同事埃尔维斯·托雷斯凭揭露地下留宿场所乱象的调查报道系列《Alojamientos Clandestinos》获弗朗茨·塔马约大学（Unifranz）首届调查新闻奖电视类金奖。2025年12月，即罗德里戈·帕斯新政府上台约一个月后，他进入国家电视台新闻领导层，先以新闻主管身份入职，现任国家新闻总监，在新闻信息部总经理阿尔瓦罗·伊鲁斯塔麾下统筹全国新闻编排，常驻拉巴斯。据其领英自述，他就读于山谷大学（Universidad del Valle）。",
    "status_note": "截至收集日（2026-10-27）确认在职：Bolivia TV 官网现任领导名录当日直读仍列其为国家新闻总监（含工作邮箱）；Bolivia Verifica 2026-10-07 报道亦以其国家新闻总监头衔称谓并尝试联络其核实信源。",
    "work_note": "职业轨迹（依可靠时间锚点）：Red ATB 记者（至少2020-03在职）→ Red Uno《Notivisión》记者（2022-08遇袭、2023-05获奖时在职）→ Bolivia TV（2025-12入职，先任新闻主管，现任国家新闻总监）。各段任职的确切起止年份均未查明。",
    "profile": None,
    "profile_note": "未找到可确认归属的本人照片（官网名录页无头像，Unifranz 报道页无配图，X/LinkedIn 头像因登录墙无法获取），profile 置 null。",
    "collection_meta": {
        "collection_date": "2026-10-27",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "news_search",
            "web_search",
            "social_media"
        ],
        "notes": "核心事实均≥2独立来源：现任国家新闻总监（官网 Contactos 页 2026-10-27 直读列出全名与邮箱 eddy.penaloza@boliviatv.bo + LinkedIn 搜索摘要自述 2025年12月起 + Bolivia Verifica 2026-10-07 报道称谓）；2025-12 入职 Bolivia TV（LinkedIn「dic 2025」+ Notiviral 2025-12-10 帖援引 BlockNoticias）；Red Uno 时期（Voces del Sur/ANP 2022-08-10 遇袭报道 + Unifranz 官方博客 2023-05-16 获奖报道）；ATB 时期（Bolivia Verifica 2020-03-06，其本人向该机构证实网传截图伪造）。全文直读来源6个：官网 Contactos 页、Unifranz 博客、Voces del Sur、Bolivia Verifica 两篇（2020-03/2026-10）、Notiviral Facebook 帖。关键核验：(1) 入职时头衔为「jefe de prensa（新闻主管）」（Notiviral 2025-12-10，时总经理 Daniel Castellón），2026-01-07 Carlos Villazón（BO-PERSON-000398）接任总经理，现头衔「国家新闻总监」为官网/LinkedIn/媒体2026年口径，晋升具体日期未查明；(2) 三人职务已严格区分：Villazón=总经理、Irusta（BO-PERSON-000399）=新闻信息部总经理（其直接上级）、Peñaloza=国家新闻总监；(3) 同名者已排除：Eddy Peñaloza Salazar（2015年任警察纪律法庭名誉主席）、Eddy Peñaloza Tapia（X 账号 @EddyPenalozaT）、Adriana Peñaloza Villavicencio（官网体育创意部主管，同姓氏非本人）；(4) AI 生成站点 memoria-salud-bolivia...chatgpt.site 声称其「由部长 Javier Torres Goitia 任命」，来源不可靠，未采信；(5) X/LinkedIn 账号依搜索摘要收录并注明核实状态（登录墙/authwall 拦截未能直读），两个 LinkedIn 账号同名同校疑为同一人先后账号；(6) 无公开出生日期/出生地/家庭信息、无 Wikidata 条目、无既有标准中文译名（name_zh 置 null）。completeness_score 约58：受限于公开生平资料稀缺（birth_date/birth_place/家庭/政治立场均无信息，客观不可补），已达任务规定的 ≥50 达标线。",
        "quotes": [
            {
                "title": "Contactos — Bolivia TV 官网现任领导名录（2026-10-27 直读）",
                "url": "https://www.boliviatv.bo/principal/contactos.php"
            },
            {
                "title": "Unifranz destaca la labor de periodistas en la Primera Versión del Reconocimiento Franz Tamayo al Periodismo de Investigación (2023-05-16)",
                "url": "https://unifranz.edu.bo/blog/periodismoinvestigacion"
            },
            {
                "title": "Productores de coca golpean a periodistas de Tv Red Uno — Voces del Sur (ANP, 2022-08-10)",
                "url": "https://vocesdelsurunidas.org/incidentes/productores-de-coca-golpean-a-periodistas-de-tv-red-uno"
            },
            {
                "title": "Este titular atribuido a la Red ATB fue editado — Bolivia Verifica (2020-03-06)",
                "url": "https://boliviaverifica.bo/este-titular-atribuido-a-la-red-atb-fue-editado"
            },
            {
                "title": "El edecán del exfiscal Roger Mariaca no fue aprehendido el 1 de octubre — Bolivia Verifica (2026-10-07)",
                "url": "https://boliviaverifica.bo/el-edecan-del-exfiscal-roger-mariaca-no-fue-aprehendido-el-1-de-octubre"
            },
            {
                "title": "Trabajadores de Bolivia TV Denuncian maltrato de los nuevos directivos del canal estatal — Notiviral (Facebook, 2025-12-10, 援引 BlockNoticias)",
                "url": "https://www.facebook.com/Notiviral2024/posts/trabajadores-de-bolivia-tv-denuncian-maltrato-de-los-nuevos-directivos-del-canal/1434544738673957"
            },
            {
                "title": "Eddy Ariel Peñaloza Rada — Periodista y Productor de Noticias / Director Nacional de Noticias Bolivia TV — LinkedIn（搜索摘要）",
                "url": "https://bo.linkedin.com/in/eddy-ariel-pe%C3%B1aloza-rada-7a08b1300"
            },
            {
                "title": "Eddy Peñaloza Rada (@eddypenaloza) / X（搜索摘要）",
                "url": "https://x.com/eddypenaloza"
            }
        ]
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(person, f, ensure_ascii=False, indent=2)

print("written:", OUT)
print("bytes:", os.path.getsize(OUT))
print("bio_len:", len(person["biography_summary"]))

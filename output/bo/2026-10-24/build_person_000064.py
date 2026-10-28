# -*- coding: utf-8 -*-
"""Build person profile BO-PERSON-000064 (Mauricio Zamora Liebers)."""
import json
import os

profile = {
    "person_id": "BO-PERSON-000064",
    "wikidata_qid": None,
    "name": "Mauricio Zamora Liebers",
    "name_en": "Mauricio Zamora Liebers",
    "name_zh": "毛里西奥·萨莫拉·利伯斯",
    "aliases": ["Mauricio Zamora"],
    "nationality": "BO",
    "gender": "male",
    "profile": {
        "source_url": "https://lavozdetarija.com/wp-content/uploads/2025/10/Mauricio-Zamora-e1761146085663.jpg",
        "local_path": None,
    },
    "birth_date": None,
    "birth_date_note": "出生日期与出生年份均未见公开报道，无法确认。",
    "birth_place": "塔里哈 (Tarija)",
    "birth_place_note": "多来源（MOPSV官网、Correo del Sur、Tarija Conecta）称其为「塔里哈人（tarijeño）」，现居圣克鲁斯；未明确具体出生城市与日期。",
    "contacts": [
        {
            "type": "website",
            "value": "https://www.oopp.gob.bo/",
            "source": "其执掌的公共工程、服务与住房部（MOPSV）官方网站",
        },
    ],
    "current_positions": [
        "公共工程、服务与住房部长",
        "玻利维亚国家航空（BoA）董事会主席",
    ],
    "education": [],
    "education_note": "公开来源（MOPSV官网、Correo del Sur、Tarija Conecta、eju.tv、英文维基百科）均未披露其学历与院校信息，故留空。",
    "work_experience": [
        {
            "start_date": "2025-11-09",
            "end_date": None,
            "organization": "公共工程、服务与住房部 (Ministerio de Obras Públicas, Servicios y Vivienda)",
            "org_id": "BO-GOV-013",
            "position": "部长",
        },
        {
            "start_date": "2026-02-03",
            "end_date": "2026-02-08",
            "organization": "经济与公共财政部 (Ministerio de Economía y Finanzas Públicas)",
            "org_id": "BO-GOV-005",
            "position": "临时部长（第5540号最高法令，时任部长埃斯皮诺萨外访期间代职）",
        },
        {
            "start_date": "2026-10-10",
            "end_date": "2026-10-18",
            "organization": "可持续生产、环境与水部 (Ministerio de Producción Sostenible, Medio Ambiente y Agua)",
            "org_id": "BO-GOV-012",
            "position": "临时部长（第5743号最高法令，时任部长胡斯蒂尼亚诺赴罗马与会期间代职）",
        },
        {
            "start_date": "2025-10",
            "end_date": "2025-11",
            "organization": "政府过渡委员会 (Comisión de Transición Gubernamental)",
            "org_id": None,
            "position": "总协调员",
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚航空 (Boliviana de Aviación, BoA)",
            "org_id": "BO-SOE-005",
            "position": "董事会主席",
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "Tinto 餐厅 (Tinto)",
            "org_id": None,
            "position": "所有者（拉巴斯与圣克鲁斯）",
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "La Morada 餐厅 (La Morada)",
            "org_id": None,
            "position": "所有者（圣克鲁斯）",
        },
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000001",
            "person_name": "罗德里戈·帕斯·佩雷拉 (Rodrigo Paz Pereira)",
            "relationship_type": "superior",
            "description": "玻利维亚总统、直接上级。2025年10月决选后任命其为政府过渡委员会总协调员，2025年11月9日任命其为公共工程部长。据 El País（塔里哈）2026年7月分析报道，萨莫拉属帕斯核心圈层，其兄为帕斯少年时代挚友。",
        },
        {
            "person_id": None,
            "person_name": "阿德里安·萨莫拉·利伯斯 (Adrián Zamora Liebers)",
            "relationship_type": "sibling",
            "description": "兄长。据 El País（塔里哈）2026年7月报道，其为总统帕斯·佩雷拉的少年好友，其妻为玛丽亚·埃莱娜·乌尔基迪（「Bibi」）的姐妹之一。（单源意见专栏，谨慎采信）",
        },
        {
            "person_id": "BO-PERSON-000534",
            "person_name": "玛丽亚·埃莱娜·乌尔基迪·巴贝里 (María Elena Urquidi Barbery)",
            "relationship_type": "in_law",
            "description": "姻亲。据 El País（塔里哈）2026年7月报道，其兄阿德里安的妻子为乌尔基迪的姐妹之一；乌尔基迪被称为「Bibi」，被舆论视为对政府颇有影响力的总统圈层人物。（单源意见专栏，谨慎采信）",
        },
        {
            "person_id": "BO-PERSON-000156",
            "person_name": "何塞·加布里埃尔·埃斯皮诺萨·亚涅斯 (José Gabriel Espinoza Yáñez)",
            "relationship_type": "colleague",
            "description": "内阁同僚。埃斯皮诺萨2025年11月起任经济与公共财政部长，2026年2月3日至8日外访期间由萨莫拉临时代理其职务（DS 5540）；2026年8月21日埃斯皮诺萨被议会弹劾去职。",
        },
    ],
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "Mauricio Zamora",
            "url": "https://www.facebook.com/zamoraliebers/",
            "source": "Facebook 个人主页（约1.2万粉丝，简介为公共工程、服务与住房部长）",
        },
    ],
    "social_accounts_note": "六平台扫描结果：仅检出 Facebook 个人主页（facebook.com/zamoraliebers）；Instagram、X/Twitter、LinkedIn、TikTok、YouTube 未检出其个人账号（相关内容均为媒体与 MOPSV 机构账号发布）。",
    "family_members": [],
    "family_note": "据 Correo del Sur 与 Tarija Conecta（2025-11，转引《任务报》El Deber）：已婚21年（约2004-2005年成婚），育有四名子女，其中一名出生两日后夭折。El País（塔里哈）2025-11-16 专栏称其配偶为 María Teresa Justiniano Arce（该信息仅见于该意见专栏单源，且其 2023 年接受《Moscatel》杂志专访时提及的内兄 Renán Justiniano 姓氏与之吻合，但全名未获第二独立来源确认，故 family_members 留空）。其弟（兄）Adrián Zamora Liebers 为 Tinto 餐厅合伙创始人之一（Moscatel 专访自述），亦是总统帕斯的少年好友。",
    "political_stances": [
        {
            "date": "2025-10-22",
            "topic": "加入过渡政府与对 MAS 政府司法迫害的控诉",
            "stance_content": "在社交媒体发表声明称「在经历 MAS 政府和私人利益推动的多年司法迫害之后，我今天向前迈出一步，去陪伴一场历史性的过渡」，宣布以政府过渡委员会总协调员身份辅佐帕斯；当时还表示「我不会当部长」，两周后（11月9日）接受公共工程部长任命。",
            "source": "La Voz de Tarija https://lavozdetarija.com/2025/10/22/mauricio-zamora-no-voy-a-ser-ministro-ayudo-a-rodrigo-paz-en-esta-etapa-de-transicion/",
        },
        {
            "date": "2026-05-16",
            "topic": "奇莫雷机场被占事件与对埃沃·莫拉莱斯支持者行动的立场",
            "stance_content": "谴责埃沃·莫拉莱斯支持者「非法占领」奇莫雷机场，称「占领公共机场是非法的。玻利维亚不需要更多暴力、威胁和危及民众生命的言论，国家需要对话、和平、体制和真正的解决方案」，并宣布对该机场建设项目进行审计以维护国家资源透明。",
            "source": "MOPSV官网新闻稿 https://www.oopp.gob.bo/nota_prensa/ministro-zamora-denuncia-la-toma-ilegal-del-aeropuerto-de-chimore/",
        },
        {
            "date": "2026-10",
            "topic": "玻利维亚航空（BoA）危机与私有化问题",
            "stance_content": "在 BoA 工人宣布紧急状态、质疑运营安全后明确表态「BoA 不会被私有化」，称运营安全无风险；同时表示愿听取任何有意投资 BoA 的企业家的意见，将问题归因于多年补贴政策和票价未更新等决策，并宣布通过与工会、飞行员组成混合委员会以对话解决问题；其领导的董事会已批准采购发动机与备件。",
            "source": "FM Bolivia https://fmbolivia.com.bo/economia/ministro-zamora-boa-no-va-a-ser-privatizada-y-el-gobierno-escuchara-a-empresarios-interesados-en-invertir-21506",
        },
        {
            "date": "2026-10-21",
            "topic": "塞尔梅多录音风波（涉抓捕埃沃·莫拉莱斯行动）",
            "stance_content": "针对外流的其与前总统顾问费尔南多·塞尔梅多（Fernando Cerimedo）的电话录音（内容涉以700-800万玻利维亚诺协调抓捕莫拉莱斯的行动）予以否认，斥之为「胡闹（chacota）」。Bolivia Verifica 鉴定该录音99%概率为真人语音、仅2%与AI生成音频吻合，但鉴定不构成对完整性与剪辑的最终认证。",
            "source": "ANF/Fides https://www.noticiasfides.com/nacional/politica/verificadora-concluye-que-el-audio-de-conversacion-entre-cerimedo-y-el-ministro-zamora-no-es-artificial-en-un-99",
        },
        {
            "date": "2026-07-12",
            "topic": "自身政治定位",
            "stance_content": "自称「我是内阁中最不像政治家的人」（Soy el menos político del gabinete）；而 El País（塔里哈）分析专栏则认为他已是帕斯总统的「圈内人」，正借「解决问题者」角色积累政治声望。",
            "source": "El País (Tarija) https://elpais.bo/la-mano-del-moto/20260712_mauricio-zamora-el-elegido.html",
        },
    ],
    "major_achievements": [
        {
            "date": "1994",
            "achievement": "被评为玻利维亚最佳篮球运动员，同年玻利维亚国家队晋级在美国举办的世界锦标赛。",
            "organization": "玻利维亚国家篮球队 (Selección Nacional de Baloncesto de Bolivia)",
        },
        {
            "date": "2025-10",
            "achievement": "在10月19日决选后获当选总统罗德里戈·帕斯任命为政府过渡委员会总协调员，主持政权交接工作。",
            "organization": "政府过渡委员会 (Comisión de Transición Gubernamental)",
        },
        {
            "date": "2025-11-09",
            "achievement": "在帕斯总统首届内阁中就任公共工程、服务与住房部长，统管住房与城市规划、电信与交通副部及全部下属实体。",
            "organization": "公共工程、服务与住房部 (Ministerio de Obras Públicas, Servicios y Vivienda)",
        },
        {
            "date": "2025-11",
            "achievement": "上任伊始即主持电信交通领域人事重组：11月18日就任 BoA、NAABOL、DGAC 新领导层，11月21日就任 ATT、ABC、AEVivienda、Mi Teleférico、Vías Bolivia 新负责人，11月25日以国家多数股东代表身份参与指定 Entel 新董事会。",
            "organization": "公共工程、服务与住房部 (Ministerio de Obras Públicas, Servicios y Vivienda)",
        },
    ],
    "biography_summary": "毛里西奥·萨莫拉·利伯斯是玻利维亚企业家出身的政治人物，现任公共工程、服务与住房部长（2025年11月9日就任）。他出身塔里哈、定居圣克鲁斯，长期经营餐饮与葡萄酒行业，拥有知名餐厅 Tinto（拉巴斯与圣克鲁斯）和 La Morada（圣克鲁斯），早年曾向塔里哈市政府供应小型物资。1994年曾被评为玻利维亚最佳篮球运动员，时值国家队晋级美国世锦赛。其性格内敛，以纪律与低调著称，自称「内阁中最不像政治家的人」，并自述曾遭 MAS 政府多年司法迫害。2025年10月决选后他声明「不会当部长」、仅出任政府过渡委员会总协调员辅佐帕斯，两周后接受任命进入首届内阁，并成为总统核心圈层成员。任内以公共工程部长身份兼任玻利维亚航空（BoA）董事会主席，主导 Entel、Mi Teleférico、ABC、ATT 等国企与监管机构人事重组，并两度临时代掌其他部委：2026年2月3日至8日（第5540号最高法令）临时执掌经济与公共财政部，2026年10月10日至18日（第5743号最高法令）临时执掌可持续生产、环境与水部。2026年8月19日曾因 BoA 管理问题受国会质询；同年10月，其与前总统顾问塞尔梅多涉抓捕前总统莫拉莱斯行动的录音外流引发争议，他斥之为「胡闹」，法医鉴定显示录音99%为真人语音。在 BoA 危机中他坚持「BoA 不会被私有化」，同时对企业投资持开放态度。",
    "position_note": "职务时间线：2025-10 政府过渡委员会总协调员；2025-11-09 公共工程、服务与住房部长（第5486号最高法令内阁名单）；2026-02-03至02-08 临时经济与公共财政部长（DS 5540，媒体多源报道）；2026-10-10至10-18 临时可持续生产、环境与水部长（DS 5743，宪报刊载）。任务背景所称「临时兼任生产发展部长」未在法令或主流报道中得到证实，故未收录。",
    "work_note": "国企兼任情况：以公共工程部长身份兼任 BoA 董事会主席（2026年7-10月经 El Diario、ANF、La Patria、FM Bolivia 等多源确认）。Entel：2025-11-25 新董事会由 Álvaro Bazán Auza 任董事长，Zamora 仅以国家多数股东代表身份参与指定，未见其任 Entel 董事会主席的报道；Mi Teleférico 董事会主席职务亦未获来源证实（2025-11-21 其仅以部长身份就任该司新任执行总经理 Christian Rojas 等负责人）。任务背景中「兼任 Entel 与 Mi Teleférico 董事长」的说法无法核实，未收录。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "wikipedia",
            "wikidata",
            "news_search",
            "web_search",
            "social_media",
            "government_registry",
        ],
        "quotes": [
            {
                "title": "MAURICIO ZAMORA, NUEVO MINISTRO DE OBRAS PÚBLICAS, SERVICIOS Y VIVIENDA - MOPSV（官方新闻稿）",
                "url": "https://www.oopp.gob.bo/nota_prensa/mauricio-zamora-nuevo-ministro-de-obras-publicas-servicios-y-vivienda/",
            },
            {
                "title": "Mauricio Zamora Liebers asume como titular de Obras Públicas - Correo del Sur",
                "url": "https://correodelsur.com/politica/20251109/mauricio-zamora-liebers-asume-como-titular-de-obras-publicas.html",
            },
            {
                "title": "¿Quién es Mauricio Zamora? Ministro de Obras Públicas - Tarija Conecta",
                "url": "https://tarijaconecta.bo/noticia/8162",
            },
            {
                "title": "Conozca quién es quién en el flamante gabinete de ministros de Rodrigo Paz - eju.tv",
                "url": "https://eju.tv/2025/11/conozca-quien-es-quien-en-el-flamante-gabinete-de-ministros-de-rodrigo-paz/",
            },
            {
                "title": "Mauricio Zamora, el elegido - El País (Tarija)",
                "url": "https://elpais.bo/la-mano-del-moto/20260712_mauricio-zamora-el-elegido.html",
            },
            {
                "title": "Cuatro ministerios interinos serán absorbidos en la nueva estructura del Ejecutivo - ANF/Fides",
                "url": "https://www.noticiasfides.com/nacional/politica/cuatro-ministerios-interinos-seran-absorbidos-en-la-nueva-estructura-del-ejecutivo",
            },
            {
                "title": "Decreto Presidencial N° 5743（2026-10-10，临时部长任命）- Pixi Legal / Gaceta Oficial",
                "url": "https://www.pixilegal.com/normativa/decreto-5743-2026-10-10",
            },
            {
                "title": "Ministro Zamora denuncia la toma ilegal del aeropuerto de Chimoré - MOPSV",
                "url": "https://www.oopp.gob.bo/nota_prensa/ministro-zamora-denuncia-la-toma-ilegal-del-aeropuerto-de-chimore/",
            },
            {
                "title": "Ministro Zamora asiste a la interpelación del Legislativo - ABI",
                "url": "https://abi.bo/ministro-zamora-asiste-a-la-interpelacion-del-legislativo/",
            },
            {
                "title": "Cerimedo y Zamora habrían coordinado detener a Evo Morales con un operativo de Bs 8 millones, según nuevo audio - ANF/Fides",
                "url": "https://www.noticiasfides.com/nacional/politica/cerimedo-y-zamora-habrian-coordinado-detener-a-evo-morales-con-un-operativo-de-bs-8-millones-segun-nuevo-audio",
            },
            {
                "title": "Verificadora concluye que el audio de conversación entre Cerimedo y el ministro Zamora no es artificial en un 99% - ANF/Fides",
                "url": "https://www.noticiasfides.com/nacional/politica/verificadora-concluye-que-el-audio-de-conversacion-entre-cerimedo-y-el-ministro-zamora-no-es-artificial-en-un-99",
            },
            {
                "title": "Ministro Zamora: \"BoA no va a ser privatizada\" y el Gobierno escuchará a empresarios interesados en invertir - FM Bolivia",
                "url": "https://fmbolivia.com.bo/economia/ministro-zamora-boa-no-va-a-ser-privatizada-y-el-gobierno-escuchara-a-empresarios-interesados-en-invertir-21506",
            },
            {
                "title": "NUEVO DIRECTORIO DE ENTEL S.A. ABRE UN NUEVO RUMBO ESTRATÉGICO - MOPSV",
                "url": "https://www.oopp.gob.bo/nota_prensa/nuevo-directorio-de-entel-s-a-abre-un-nuevo-rumbo-estrategico/",
            },
            {
                "title": "MINISTRO POSESIONA A NUEVAS AUTORIDADES DE LA ATT, ABC, AEVIVIENDA, MI TELEFÉRICO Y VÍAS BOLIVIA - MOPSV",
                "url": "https://www.oopp.gob.bo/nota_prensa/ministro-posesiona-a-nuevas-autoridades-de-la-att-abc-aevivienda-mi-teleferico-y-vias-bolivia/",
            },
            {
                "title": "Mauricio Zamora - Wikipedia (English)",
                "url": "https://en.wikipedia.org/wiki/Mauricio_Zamora",
            },
            {
                "title": "Mauricio Zamora - Facebook 个人主页",
                "url": "https://www.facebook.com/zamoraliebers/",
            },
            {
                "title": "Mediante DS 5540, Rodrigo Paz designa a Mauricio Zamora como Ministro Interino de Economía（2026-02-03）- La Página de Sucre",
                "url": "https://www.facebook.com/LaPaginadeSucre/posts/mediante-ds-5540-rodrigo-paz-designa-a-mauricio-zamora-como-ministro-interino-de/1309251544582556/",
            },
            {
                "title": "Mauricio Zamora: 「si lo haces con el corazón siempre ganas」 - Revista Moscatel（2023-04 专访）",
                "url": "https://revistamoscatel.com.bo/mauricio-zamora-si-lo-haces-con-el-corazon-siempre-ganas/",
            },
            {
                "title": "Los amigos chapacos del presidente - El País (Tarija)（2025-11-16）",
                "url": "https://elpais.bo/la-mano-del-moto/20251116_los-amigos-chapacos-del-presidente.html",
            },
            {
                "title": "Mauricio Zamora: No voy a ser ministro, ayudo a Rodrigo Paz en esta etapa de transición - La Voz de Tarija（2025-10-22）",
                "url": "https://lavozdetarija.com/2025/10/22/mauricio-zamora-no-voy-a-ser-ministro-ayudo-a-rodrigo-paz-en-esta-etapa-de-transicion/",
            },
        ],
        "notes": "数据来源与核验情况：生平核心信息（塔里哈出身、定居圣克鲁斯、Tinto/La Morada 餐厅业主、1994年最佳篮球运动员、已婚21年育四子女、过渡委员会总协调员）由 Correo del Sur、Tarija Conecta、eju.tv（均转引 El Deber）及 MOPSV 官网交叉验证；2023年《Moscatel》杂志专访补充了 Tinto 创业细节（约2021年开拉巴斯店、与弟 Adrián 及内兄 Renán Justiniano 等合伙、代理 Riedel 酒具并进口阿根廷酒庄葡萄酒）；部长任命与初始内阁由 Fides/ANF（DS 5486名单）、MOPSV 官网、英文维基百科确认；两次临时部长任命分别依据 DS 5540（2026-02-03，任期为媒体报道的2月3-8日）与 DS 5743（2026-10-10，宪报全文，10-18日代职）；BoA 董事会主席身份经 El Diario、ANF、La Patria、FM Bolivia、Aviacionline 等多源确认。存疑与留空项：出生日期、学历、个人 X/Instagram/LinkedIn/TikTok/YouTube 账号均未查获，相关字段留空；配偶全名 María Teresa Justiniano Arce 仅见于 El País 单一意见专栏（与专访中内兄姓氏吻合但未获第二独立来源确认），故 family_members 留空并记入 family_note；任务背景所称「临时兼任生产发展部长」「兼任 Entel 与 Mi Teleférico 董事长」均未能从法令与主流报道中证实，已在 position_note/work_note 说明；兄长、姻亲及总统圈层关系主要来自 El País「La Mano del Moto」意见专栏，已标注谨慎采信；name_zh 沿用项目既有译名「毛里西奥·萨莫拉·利伯斯」（_name_index.json 收录）。Wikidata 无该人物条目，wikidata_qid 为 null。",
    },
}

out_dir = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "BO-PERSON-000064.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE", out_path)

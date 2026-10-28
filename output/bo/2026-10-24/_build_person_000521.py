# -*- coding: utf-8 -*-
"""Build BO-PERSON-000521 Ernesto Justiniano Urenda person profile."""
import json
import os

OUT_DIR = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24"
PERSONS_DIR = os.path.join(OUT_DIR, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

data = {
    "person_id": "BO-PERSON-000521",
    "wikidata_qid": None,
    "name_zh": "埃内斯托·胡斯蒂尼亚诺·乌伦达",
    "name": "Ernesto Justiniano Urenda",
    "name_en": "Ernesto Justiniano Urenda",
    "aliases": ["Ernesto Justiniano"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": "1969-04-15",
    "birth_place": "圣克鲁斯-德拉谢拉 (Santa Cruz de la Sierra)",
    "contacts": [
        {
            "type": "website",
            "value": "https://www.mindef.gob.bo",
            "source": "玻利维亚国防部官方网站 (Ministerio de Defensa)"
        }
    ],
    "current_positions": ["玻利维亚国防部长"],
    "education": [
        {
            "institution": "圣克鲁斯私立大学 (Universidad Privada de Santa Cruz de la Sierra)",
            "degree": "master",
            "field": "工商管理",
            "start_date": "1997",
            "end_date": "1999",
            "location": "圣克鲁斯-德拉谢拉，玻利维亚",
            "source": "个人竞选网站 (ERNESTOJUSTINIANO.ORG 存档)；Urgente.bo；Infobae；Mindef.gob.bo"
        },
        {
            "institution": "贝尔格拉诺大学 (Universidad de Belgrano)",
            "degree": "bachelor",
            "field": "机电工程（电气方向）",
            "start_date": "1988",
            "end_date": "1994",
            "location": "布宜诺斯艾利斯，阿根廷",
            "source": "个人竞选网站 (ERNESTOJUSTINIANO.ORG 存档)；Infodefensa.com；Mindef.gob.bo"
        }
    ],
    "work_experience": [
        {
            "organization": "玻利维亚国防部 (Ministerio de Defensa)",
            "org_id": "BO-GOV-004",
            "position": "国防部长",
            "start_date": "2026-06-03",
            "end_date": None,
            "is_current": "true",
            "description": "由总统罗德里戈·帕斯 (Rodrigo Paz Pereira) 在拉巴斯主持就职，接替 2026-06-02 辞职的劳尔·马塞洛·萨利纳斯·加马拉 (Raúl Marcelo Salinas Gamarra)。任内正值全国性道路封锁危机，负责协调武装力量与警察恢复秩序、疏通运输通道，并推动对美安全与禁毒合作、军队表彰与追责前官员等事务。",
            "start_date_note": "2026-06-03 正式宣誓就职；西语维基百科《Ministerio de Defensa (Bolivia)》任期表同日记载。",
            "source": "Infodefensa.com；Infobae；es.wikipedia.org；新华网"
        },
        {
            "organization": "玻利维亚政府部 (Ministerio de Gobierno)",
            "org_id": "BO-GOV-003",
            "position": "社会防御与受管制物质副部长",
            "start_date": "2025-11-11",
            "end_date": "2026-06",
            "is_current": "false",
            "description": "时隔约23年重返该职位（2002-2003 年曾任职），由政府部长马尔科·安东尼奥·奥维多 (Marco Antonio Oviedo) 主持就职。主导禁毒行动，推动美国缉毒局 (DEA) 重返玻利维亚，被视为抓获大毒枭塞巴斯蒂安·马塞特 (Sebastián Marset) 行动的策略制定者之一；2026年5月中旬曾赴美国会见 DEA。",
            "end_date_note": "2026-06-03 就任国防部长前一日仍任该职（Infobae），卸任月份记为 2026-06。",
            "source": "Urgente.bo；Infobae；Red Uno；es.wikipedia.org"
        },
        {
            "organization": "玻利维亚社会防御副部 (Viceministerio de Defensa Social)",
            "org_id": None,
            "position": "社会防御副部长（缉毒事务负责人）",
            "start_date": "2002-08-23",
            "end_date": "2003",
            "is_current": "false",
            "description": "由总统贡萨洛·桑切斯·德洛萨达 (Gonzalo Sánchez de Lozada) 任命，媒体称其为「缉毒沙皇 (zar antidrogas)」。",
            "end_date_note": "确切卸任月份未单独确认：西语维基《玻利维亚政府部长列表》该行并列记载 Ernesto Justiniano Urenda 与 Alberto Gasser Vargas，任期止于 2003-10-21。",
            "source": "es.wikipedia.org (Anexo:Ministros de Gobierno)；Urgente.bo；个人竞选网站存档"
        },
        {
            "organization": "玻利维亚众议院 (Honorable Cámara de Diputados de Bolivia)",
            "org_id": "BO-GOV-021",
            "position": "全国单名制众议员（C-51 选区）",
            "start_date": "2006",
            "end_date": "2010",
            "is_current": "false",
            "description": "以已解散政党「社会民主力量 (Poder Democrático Social, Podemos)」（胡斯托·「图托」·基罗加领导）身份当选。",
            "source": "个人竞选网站存档；Urgente.bo；Infodefensa.com；Infobae"
        },
        {
            "organization": "Meridian SRL",
            "org_id": None,
            "position": "所有者兼总经理",
            "start_date": "1995",
            "end_date": "2002",
            "location": "圣克鲁斯-德拉谢拉，玻利维亚",
            "source": "个人竞选网站 (ERNESTOJUSTINIANO.ORG 存档)"
        },
        {
            "organization": "Socinter SRL",
            "org_id": None,
            "position": "总经理",
            "start_date": "1994",
            "end_date": "1995",
            "location": "圣克鲁斯-德拉谢拉，玻利维亚",
            "source": "个人竞选网站 (ERNESTOJUSTINIANO.ORG 存档)"
        },
        {
            "organization": "Management Development Group Overseas",
            "org_id": None,
            "position": "创始人、企业咨询顾问（合伙人）",
            "start_date": "1992",
            "end_date": "1994",
            "location": "布宜诺斯艾利斯，阿根廷",
            "source": "个人竞选网站 (ERNESTOJUSTINIANO.ORG 存档)"
        },
        {
            "organization": "SC Cables",
            "org_id": None,
            "position": "生产经理",
            "start_date": "1989",
            "end_date": "1992",
            "location": "布宜诺斯艾利斯，阿根廷",
            "description": "负责为 Longvie、Volcán、Whirlpool 等品牌白色家电配套电气系统的制造与组装。",
            "source": "个人竞选网站 (ERNESTOJUSTINIANO.ORG 存档)"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000001",
            "person_name": "罗德里戈·帕斯·佩雷拉 (Rodrigo Paz Pereira)",
            "relationship_type": "superior",
            "description": "现任玻利维亚总统。2025-11 任命其为社会防御与受管制物质副部长，2026-06-03 任命其为国防部长。",
            "source": "Infodefensa.com；Urgente.bo"
        },
        {
            "person_id": "BO-PERSON-000029",
            "person_name": "马尔科·安东尼奥·奥维多·韦尔塔 (Marco Antonio Oviedo Huerta)",
            "relationship_type": "superior",
            "description": "政府部长。2025-11-11 由其主持 Justiniano 的社会防御与受管制物质副部长就职。",
            "source": "Urgente.bo"
        },
        {
            "person_id": None,
            "person_name": "劳尔·马塞洛·萨利纳斯·加马拉 (Raúl Marcelo Salinas Gamarra)",
            "relationship_type": "other",
            "description": "前任国防部长（2025-11-09 至 2026-06-02 在任），2026-06-02 于内阁会议中辞职，其职位由 Justiniano 接任。",
            "source": "Infodefensa.com；es.wikipedia.org；新华网"
        },
        {
            "person_id": "BO-PERSON-000003",
            "person_name": "费尔南多·乌戈·阿拉马约·卡拉斯科 (Fernando Hugo Aramayo Carrasco)",
            "relationship_type": "colleague",
            "description": "总统府部长。2026-09 两人一同赴华盛顿与美国国务院等机构举行会晤。",
            "source": "eju.tv, 2026-09-09"
        },
        {
            "person_id": "BO-PERSON-000018",
            "person_name": "豪尔赫·基罗加 (Jorge Quiroga)",
            "relationship_type": "political_ally",
            "description": "前总统。2006-2010 年 Justiniano 以其领导的 Podemos 党身份当选众议员。",
            "source": "Urgente.bo；个人竞选网站存档"
        },
        {
            "person_id": "BO-PERSON-000481",
            "person_name": "萨穆埃尔·多利亚·梅迪纳 (Samuel Doria Medina)",
            "relationship_type": "associate",
            "description": "民族团结党 (Unidad Nacional) 领袖。2014 年 Justiniano 以该党身份再度竞选圣克鲁斯-德拉谢拉市长。",
            "source": "Urgente.bo；Mindef.gob.bo"
        },
        {
            "person_id": None,
            "person_name": "贡萨洛·桑切斯·德洛萨达 (Gonzalo Sánchez de Lozada)",
            "relationship_type": "superior",
            "description": "前总统。2002 年任命 Justiniano 为社会防御副部长（缉毒沙皇）。",
            "source": "Urgente.bo；Mindef.gob.bo"
        }
    ],
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "Ernesto Justiniano Urenda",
            "url": "https://www.facebook.com/ernesto.justiniano.urenda/",
            "source": "页面简介标注「Ministro de Defensa」及禁毒政策主张"
        },
        {
            "platform": "twitter_x",
            "account_name": "@E_J_U",
            "url": "https://x.com/E_J_U",
            "source": "X 个人账号，账号名 Ernesto Justiniano Urenda，2015年3月注册，530 帖"
        },
        {
            "platform": "instagram",
            "account_name": "ernesto.justiniano.u",
            "url": "https://www.instagram.com/ernesto.justiniano.u/",
            "source": "同名 Instagram 账号（955 关注者）；另存在低活跃同名账号 ernesto.justiniano.urenda，账号主体身份未能逐一人工核实"
        },
        {
            "platform": "tiktok",
            "account_name": "@ernestojustinianourenda",
            "url": "https://www.tiktok.com/@ernestojustinianourenda",
            "source": "TikTok 搜索结果同名账号（187 关注者）"
        }
    ],
    "family_members": [],
    "political_stances": [
        {
            "date": "2025-11-11",
            "topic": "禁毒政策",
            "stance_content": "就任缉毒事务副部长时表示：「我们想要一个始终在法律框架内运转的国家。合法产品将是我们的盟友，敌人是毒品贩运。今天的玻利维亚需要的不是空谈，而是成果。」",
            "source": "Urgente.bo, 2025-11-11"
        },
        {
            "date": "2026-05",
            "topic": "美玻禁毒合作与 DEA 重返玻利维亚",
            "stance_content": "支持美国缉毒局 (DEA) 恢复在玻利维亚运作，2026年5月中旬赴美与 DEA 会晤，为打击贩毒和有组织犯罪争取美方技术与后勤支持，并曾在白宫录制宣布相关消息的视频。",
            "source": "Infobae, 2026-06-03"
        },
        {
            "date": "2026-06-03",
            "topic": "危机应对与恢复秩序",
            "stance_content": "就任国防部长时承诺：「玻利维亚依靠协调、坚定、平衡与对宪法的忠诚自持。我怀着这一信念来到新的岗位，从制度上支持我们的武装力量，帮助国家恢复和平、秩序与民主共处。」",
            "source": "Infodefensa.com, 2026-06-04"
        },
        {
            "date": "2026-06-09",
            "topic": "暴力与法治",
            "stance_content": "在海军表彰仪式上发表强硬声明：国家将以合法和坚定的方式应对暴力行为。",
            "source": "YouTube 新闻报道 (dq2Qr-wTss8), 2026-06-09"
        },
        {
            "date": "2026-09-28",
            "topic": "对前总统莫拉莱斯阵营最后通牒的回应",
            "stance_content": "针对与前总统埃沃·莫拉莱斯关系密切的派系发出的最后通牒，警告将以法律手段回应，强调国家机构不会屈服于胁迫。",
            "source": "Red Uno (YouTube, I5sq-Vh1fZ0), 2026-09-28"
        },
        {
            "date": "2026-10-15",
            "topic": "追责前政府官员",
            "stance_content": "以「损害国家经济」罪名向检察院对前政府官员提起刑事控告 (querella por daño económico al Estado)。",
            "source": "玻利维亚国防部 Facebook；Visión360 (X), 2026-10-15"
        }
    ],
    "major_achievements": [
        {
            "date": "2025",
            "achievement": "作为缉毒事务负责人之一，被视为抓获大毒枭塞巴斯蒂安·马塞特 (Sebastián Marset) 行动的策略制定者之一。",
            "organization": "玻利维亚政府部 (Ministerio de Gobierno)"
        },
        {
            "date": "2026-05",
            "achievement": "推动美国缉毒局 (DEA) 重返玻利维亚恢复运作，并为国家禁毒行动争取美方技术与后勤支持。",
            "organization": "玻利维亚政府部 (Ministerio de Gobierno)"
        },
        {
            "date": "2026-06",
            "achievement": "就任防长后主导恢复因全国道路封锁瘫痪的交通，确认重新开通拉巴斯三条战略路线并推进全国疏通行动。",
            "organization": "玻利维亚国防部 (Ministerio de Defensa)"
        }
    ],
    "biography_summary": "埃内斯托·胡斯蒂尼亚诺·乌伦达，1969年4月15日生于圣克鲁斯-德拉谢拉，玻利维亚工程师、企业家和政治家，现任国防部长（2026年6月3日就任）。毕业于阿根廷贝尔格拉诺大学机电工程（电气方向）专业（1988-1994），后获圣克鲁斯私立大学工商管理硕士（1997-1999），通晓英语、德语和葡萄牙语。早年在阿根廷从事企业管理，1994年回国创办并经营企业。2002年被总统桑切斯·德洛萨达任命为社会防御副部长（「缉毒沙皇」）；2004年代表 MIR 竞选圣克鲁斯市长未果；2006-2010年以 Podemos 党身份任 C-51 选区众议员；2014年再以民族团结党身份竞选市长。2025年11月在罗德里戈·帕斯政府中出任社会防御与受管制物质副部长，主导禁毒行动、推动美国 DEA 重返玻利维亚，是抓获大毒枭马塞特行动的策略制定者之一。2026年6月3日接替辞职的马塞洛·萨利纳斯出任国防部长，任内应对全国道路封锁危机、推动恢复秩序、深化对美安全合作并追责前官员。已婚，据单一媒体来源报道育有子女。",
    "profile": {
        "source_url": "https://www.mindef.gob.bo/wp-content/uploads/2026/06/WhatsApp-Image-2026-06-03-at-14.34.33-2.jpeg",
        "local_path": None
    },
    "languages": "西班牙语（母语）；英语、德语、葡萄牙语（其个人竞选网站自述）",
    "military_rank": None,
    "political_party": "历史上先后隶属革命左翼运动 MIR（2002-2005）、社会民主力量 Podemos（2006-2010）、民族团结 UN（2014年竞选）；现为罗德里戈·帕斯政府阁员，当前党籍未见明确公开报道",
    "honors": "2026-06 获玻利维亚海军表彰（Armada Boliviana 表彰仪式并授勋；具体勋章名称未能从现有来源确认）",
    "family_note": "据 tunota.com（2026-06-03）报道已婚，妻子名为 Lorena Villalobos，育有四名子女；该信息仅此单一来源，且其本人早年竞选网站称育有三名子女，故 family_members 留空仅作备注。",
    "education_note": "另曾于贝尔格拉诺大学修读神经语言程序学 (PNL) 沟通课程（1991-1993），于 Kepner Tregoe 国际公司（布宜诺斯艾利斯）修读管理问题分析与决策课程（1992-1994），均见其个人竞选网站自述。",
    "work_note": "2002-2003 年任社会防御副部长的确切卸任日期未单独确认：西语维基《玻利维亚政府部长列表》该行并列记载 Ernesto Justiniano Urenda 与 Alberto Gasser Vargas，任期止于 2003-10-21。",
    "position_note": "2026-06-03 由总统罗德里戈·帕斯在拉巴斯行政首都主持就职；其前任劳尔·马塞洛·萨利纳斯·加马拉于 2026-06-02 辞职（任务背景中所述「前任为 Ignacio Zabala」与全部独立来源不符，已按来源核实修正）。",
    "name_zh_note": "新华社/人民网用「埃内斯托·胡斯蒂尼亚诺」，俄罗斯卫星通讯社中文站与 MiGFlug 中文页用全名音译「埃内斯托·胡斯蒂尼亚诺·乌伦达」，本档案取全名音译。",
    "birth_date_note": "1969-04-15：其个人竞选网站与 tunota.com 一致记载；Infodefensa、Urgente.bo、Infobae、新华网仅称 1969 年生。",
    "social_accounts_note": "LinkedIn 与 YouTube 未发现其个人官方账号（LinkedIn/YouTube 相关结果均为他人或媒体账号提及他）。Instagram 存在两个同名账号（ernesto.justiniano.u 与 ernesto.justiniano.urenda），账号主体身份未能逐一人工核实。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "wikipedia",
            "news_search",
            "web_search",
            "social_media",
            "government_directory"
        ],
        "notes": "关键事实均经 ≥2 独立来源交叉验证：出生（1969-04-15，圣克鲁斯-德拉谢拉）、教育（贝尔格拉诺大学机电工程、UPSA 工商管理硕士）、2002-2003 副部长、2006-2010 Podemos 众议员、2025-11-11 副部长（缉毒）、2026-06-03 就任防长。⚠️ 任务背景称前任防长为 Ignacio Zabala，但 Infodefensa、Infobae、tunota、西语维基百科、新华社等多源一致确认前任为 Raúl Marcelo Salinas Gamarra（2025-11-09 至 2026-06-02 在任，2026-06-02 辞职），「Ignacio Zabala」未见于任何玻利维亚防长相关来源，疑为背景信息错误。注意与 BO-PERSON-000004（Ernesto Amilcar Justiniano Hurtado）系同姓不同人，已排除混淆。无 Wikidata 个人条目（wikidata_qid 置 null）。家庭信息（配偶 Lorena Villalobos、子女数）仅单一来源且互相矛盾（tunota 称4名子女，本人旧竞选网站称3名），故 family_members 留空。 Instagram 双账号及 Facebook/TikTok/X 账号主体身份基于姓名与简介匹配，未逐一登录核实。",
        "quotes": [
            {
                "title": "Ernesto Justiniano jura el cargo de ministro de Defensa de Bolivia en plena crisis nacional (Infodefensa.com)",
                "url": "https://www.infodefensa.com/texto-diario/mostrar/5906530/ernesto-justiniano-asume-cartera-defensa-bolivia-medio-grave-crisis-sufre-pais-andino"
            },
            {
                "title": "Ernesto Justiniano retorna como zar antidrogas tras más de dos décadas (Urgente.bo)",
                "url": "https://www.urgente.bo/noticia/ernesto-justiniano-retorna-como-zar-antidrogas-tras-mas-de-dos-decadas"
            },
            {
                "title": "Quién es Ernesto Justiniano, el nuevo ministro de Defensa que asumió en Bolivia (Infobae)",
                "url": "https://www.infobae.com/america/america-latina/2026/06/03/quien-es-ernesto-justiniano-el-nuevo-ministro-de-defensa-que-asumio-en-bolivia-en-medio-de-una-ola-de-conflictos/"
            },
            {
                "title": "Ernesto Justiniano quién es: Biografía, Wikipedia, edad y vida personal (Tunota.com)",
                "url": "https://www.tunota.com/entretenimiento/ernesto-justiniano-quien-es-biografia-wikipedia-edad-y-vida-personal-2026-06-03"
            },
            {
                "title": "Recorrido profesional del Ministro de Defensa, Ernesto Justiniano Urenda (Ministerio de Defensa de Bolivia)",
                "url": "https://www.mindef.gob.bo/index.php/nota_prensa/ministro-de-defensa-ernesto-justiniano-urenda/"
            },
            {
                "title": "Ministerio de Defensa (Bolivia) - Wikipedia (es)",
                "url": "https://es.wikipedia.org/wiki/Ministerio_de_Defensa_(Bolivia)"
            },
            {
                "title": "Ernesto Justiniano > Acerca de Ernesto (ERNESTOJUSTINIANO.ORG 存档, eju.tv)",
                "url": "https://cd1.eju.tv/index_files/acercadeernesto.htm"
            },
            {
                "title": "玻利维亚新防长上任强调恢复秩序 (新华网)",
                "url": "https://www.news.cn/world/20260604/41738547fa774ac58a53595e022a4f45/c.html"
            },
            {
                "title": "Ernesto Justiniano y Fernando Aramayo están en Washington para reuniones con el Departamento de Estado de EEUU (eju.tv)",
                "url": "https://eju.tv/2026/09/ernesto-justiniano-y-fernando-aramayo-estan-en-washington-para-reuniones-con-el-departamento-de-estado-de-eeuu/"
            }
        ]
    }
}

# Try downloading the official photo
photo_path = os.path.join(OUT_DIR, "photos", "BO-PERSON-000521.jpg")
photo_url = data["profile"]["source_url"]
try:
    import urllib.request
    req = urllib.request.Request(photo_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        content = resp.read()
    if len(content) > 5000 and content[:2] in (b"\xff\xd8", b"\x89P"):
        os.makedirs(os.path.dirname(photo_path), exist_ok=True)
        with open(photo_path, "wb") as f:
            f.write(content)
        data["profile"]["local_path"] = "photos/BO-PERSON-000521.jpg"
        print("PHOTO OK:", len(content), "bytes")
    else:
        print("PHOTO SKIP: invalid content", len(content))
except Exception as e:
    print("PHOTO FAIL:", e)

out_path = os.path.join(PERSONS_DIR, "BO-PERSON-000521.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("WROTE:", out_path)

# quick self-checks
s = json.dumps(data, ensure_ascii=False)
print("bio_summary length:", len(data["biography_summary"]))
print("quotes:", len(data["collection_meta"]["quotes"]))

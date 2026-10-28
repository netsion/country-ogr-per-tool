# -*- coding: utf-8 -*-
"""Build BO-PERSON-000454 (Nicolas Joray, Fondation Patiño Directeur général)."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "persons", "BO-PERSON-000454.json")

data = {
    "person_id": "BO-PERSON-000454",
    "wikidata_qid": None,
    "name": "Nicolas Joray",
    "name_en": "Nicolas Joray",
    "name_zh": None,
    "aliases": [],
    "nationality": "CH",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "contacts": [
        {
            "type": "phone",
            "value": "+41 22 347 02 11",
            "source": "Fondation Patiño 官网 Contact 页（日内瓦总部总机，总干事公务联络渠道，非个人直线）"
        },
        {
            "type": "email",
            "value": "info@patino.org",
            "source": "Fondation Patiño 官网 Contact 页及 2025 年度报告（基金会官方邮箱，非个人邮箱）"
        },
        {
            "type": "website",
            "value": "https://patino.org",
            "source": "Fondation Patiño 官网（其任职机构官网，2025 年度报告版权页）"
        }
    ],
    "current_positions": [
        "帕蒂尼奥基金会总干事"
    ],
    "education": [],
    "work_experience": [
        {
            "start_date": None,
            "end_date": None,
            "organization": "帕蒂尼奥基金会 (Fondation Simón I. Patiño)",
            "org_id": "BO-NGO-007",
            "position": "总干事 (Directeur général)",
            "is_current": "true",
            "location": "日内瓦 (Genève)",
            "description": (
                "常驻日内瓦总部（Rue Giovanni-Gambini 8, 1206 Genève），主持基金会全球事务。"
                "官网「Nos forces vives」名单中，日内瓦总部仅列总干事及其下设的财务负责人"
                "（Benoit Lécorché）、大学奖学金与文化活动负责人（Arnaud Dubouchet）、办公室主任"
                "（Valérie Gautier）三人，玻利维亚各中心运营则由常驻科恰班巴的总经理"
                "罗德里戈·达萨·门迪萨瓦尔（Rodrigo Daza Mendizábal）负责，形成日内瓦—玻利维亚双总部治理结构。"
                "日内瓦分部（1958年设立）主管面向玻利维亚学生的瑞士/比利时硕士奖学金管理与欧洲文化活动。"
            ),
            "start_date_note": (
                "确切就任日期未公开：覆盖至2023-12-31、2024-12-31的2023与2024两份年度报告均列前任 Frédéric Debray "
                "为总干事，覆盖至2025-12-31的2025年度报告已列 Joray，且官网于2025年11月上传其官方肖像，"
                "可判断就任发生在2025年内。"
            ),
            "source": "https://patino.org/notre-engagement-fondateur/"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000455",
            "person_name": "罗德里戈·达萨·门迪萨瓦尔 (Rodrigo Daza Mendizábal)",
            "relationship_type": "colleague",
            "description": (
                "帕蒂尼奥基金会玻利维亚总经理（Gerente General；官网法文版作 Directeur exécutif），"
                "常驻科恰班巴统筹玻利维亚各中心运营；与 Joray 分掌基金会日内瓦/玻利维亚双总部的全球治理分工。"
            ),
            "source": "https://patino.org/notre-engagement-fondateur/"
        },
        {
            "person_id": None,
            "person_name": "伯努瓦·梅尔特 (Benoît Merkt)",
            "relationship_type": "superior",
            "description": (
                "帕蒂尼奥基金会理事会主席（Président du Conseil de Fondation，2025年度报告截至2025-12-31在任，"
                "并与副主席、秘书等组成理事会 Bureau）；总干事 Joray 向理事会负责。"
            ),
            "source": "https://patino.org/wp-content/uploads/2026/06/Fondation-Patino_Rapport-activites-2025.pdf"
        },
        {
            "person_id": None,
            "person_name": "弗雷德里克·德布雷 (Frédéric Debray)",
            "relationship_type": "other",
            "description": (
                "Joray 的总干事职位前任：覆盖至2023-12-31与2024-12-31的2023、2024两份年度报告均列 Debray 为总干事，"
                "2025年度报告（截至2025-12-31）改列 Joray，两人为前后任交接关系。"
            ),
            "source": "https://patino.org/wp-content/uploads/2025/09/Fondation-Patino-Rapport-dactivite-2024.pdf"
        },
        {
            "person_id": None,
            "person_name": "贝努瓦·莱科尔谢 (Benoit Lécorché)",
            "relationship_type": "subordinate",
            "description": "官网「Nos forces vives」日内瓦总部名单列其为财务负责人（Responsable des finances），在总干事 Joray 主管的日内瓦团队之下。",
            "source": "https://patino.org/notre-engagement-fondateur/"
        },
        {
            "person_id": None,
            "person_name": "阿尔诺·迪布歇 (Arnaud Dubouchet)",
            "relationship_type": "subordinate",
            "description": "官网日内瓦总部名单列其为大学奖学金与文化活动负责人（Responsable des Bourses universitaires et des Activités culturelles），在总干事 Joray 主管的日内瓦团队之下。",
            "source": "https://patino.org/notre-engagement-fondateur/"
        },
        {
            "person_id": None,
            "person_name": "瓦莱丽·戈蒂耶 (Valérie Gautier)",
            "relationship_type": "subordinate",
            "description": "官网日内瓦总部名单列其为办公室主任（Office Manager / Responsable de oficina），在总干事 Joray 主管的日内瓦团队之下。",
            "source": "https://patino.org/notre-engagement-fondateur/"
        }
    ],
    "social_accounts": [],
    "family_members": [],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2025",
            "achievement": (
                "出任帕蒂尼奥基金会（Fondation Simón I. Patiño，1931年由玻利维亚「锡王」西蒙·伊图里·帕蒂尼奥创立的"
                "私立文化慈善基金会）总干事（Directeur général），接替 Frédéric Debray，"
                "常驻日内瓦主持基金会国际奖学金、儿科健康、农业生态与文化四大板块的全球事务。"
            ),
            "organization": "帕蒂尼奥基金会 (Fondation Simón I. Patiño)"
        }
    ],
    "biography_summary": (
        "尼古拉·若拉（Nicolas Joray），瑞士法语区人士，现任帕蒂尼奥基金会（Fondation Simón I. Patiño，"
        "西语作 Fundación Patiño）总干事（Directeur général），常驻瑞士日内瓦总部"
        "（Rue Giovanni-Gambini 8, 1206 Genève）。该基金会由玻利维亚「锡王」西蒙·伊图里·帕蒂尼奥于1931年创立，"
        "是玻利维亚历史最悠久、影响力最大的私立文化慈善基金会之一，1958年起在日内瓦设分部，"
        "在玻利维亚运营十余个中心，治理呈日内瓦—科恰班巴双总部结构。若拉作为总干事主持基金会全球事务，"
        "日内瓦团队下设财务、大学奖学金与文化活动及办公室职能，其中日内瓦分部具体负责面向玻利维亚学生的"
        "瑞士/比利时硕士奖学金管理与欧洲文化活动；玻利维亚业务的日常运营由常驻科恰班巴的总经理"
        "罗德里戈·达萨·门迪萨瓦尔负责，两人分掌双端并向理事会主席伯努瓦·梅尔特领衔的理事会负责。"
        "其就任路径可由官方文件交叉印证：覆盖至2024年12月31日的2024年度报告列前任弗雷德里克·德布雷"
        "（Frédéric Debray）为总干事，而覆盖至2025年12月31日的2025年度报告已列若拉，"
        "官网亦于2025年11月上传其官方肖像，可推断其于2025年内接任。除基金会官网与年报外，"
        "其个人公开活动记录极少：媒体检索未发现其以基金会职务出席公开活动的报道，"
        "出生日期、学历、家庭与社交账号信息均无公开可靠来源；瑞士媒体存在同名的汝拉州文艺界人士，"
        "与本人无法证实为同一人，相关报道未予采信。"
    ),
    "profile": {
        "source_url": "https://patino.org/wp-content/uploads/2025/11/Nicolas-Joray-800x0-c-default.jpeg",
        "local_path": "photos/BO-PERSON-000454.jpg"
    },
    "nationality_note": (
        "瑞士国籍归属无公开文件直接证实（瑞士商业登记与基金会名录不公开个人国籍信息）；"
        "依据其常驻日内瓦、任瑞士注册基金会（Fondation Simón I. Patiño，注册地 Genève）总干事、"
        "瑞士法语区姓氏 Joray 及官网将其列于「Genève | Suisse」名下，暂按常驻国记 CH，待核实。"
    ),
    "position_note": (
        "官网西语版作「Director General」，官网法文版与2025年度报告作「Directeur général」；"
        "官网「Nos forces vives / Nuestro compromiso fundacional」页在日内瓦总部（Genève | Suisse）栏位列出。"
    ),
    "work_note": (
        "就任时间推断依据：2024年度报告（覆盖至2024-12-31，2025年9月发布）列前任 Frédéric Debray 为总干事；"
        "2025年度报告（覆盖至2025-12-31，2026年6月发布）改列 Joray；官网肖像上传于2025年11月。"
        "既往任职记录无法核实：LinkedIn 个人页（ch.linkedin.com/in/nicolas-joray 等候选地址）均返回登录墙，"
        "phase3 组织建档时曾记录「长期任职基金会、瑞士会计师教育背景」的 LinkedIn 线索，本次未能复核，故不写入。"
    ),
    "education_note": "无公开可靠来源；LinkedIn 个人页受登录墙阻隔无法核实，搜索引擎配额受限亦无法定位其档案，留空。",
    "social_accounts_note": (
        "已完成 6 平台扫描（LinkedIn/X/Facebook/Instagram/YouTube/TikTok）：LinkedIn 个人页两处候选地址"
        "（ch.linkedin.com/in/nicolas-joray、/in/nicolasjoray）均返回登录墙；其余平台未检索到可确证为本人的账号。"
        "检索受限说明：WebSearch 与 web_reader MCP 配额耗尽，Bing 返回去引号的通用结果，DuckDuckGo/Brave/SearX/Mojeek/Ecosia/Yandex 均反爬拦截，"
        "仅 Google News RSS 可用（检索「Nicolas Joray」及「Joray Patiño」组合，后者无结果）。"
        "基金会机构账号（LinkedIn/Instagram/X/Facebook/YouTube）已收录于 BO-NGO-007 组织档案，非个人账号。"
    ),
    "name_zh_note": (
        "未检索到中文媒体既有译名（WebSearch 配额受限，Google News 与官网双语文告均无中文名），"
        "name_zh 置 null；本档案叙述按法语发音暂译「尼古拉·若拉」，不作为正式译名。"
    ),
    "collection_meta": {
        "collection_date": "2026-10-26",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "annual_report",
            "news_search",
            "web_search"
        ],
        "completeness_score": 0,
        "notes": (
            "总干事职务由官网法文版「Notre engagement fondateur」（Nos forces vives 名单：Genève|Suisse 栏首位列 "
            "Nicolas Joray, Directeur général）、官网西语版「Nuestro compromiso fundacional」（Director General）"
            "及2025年度报告（截至2025-12-31：Directeur général Nicolas Joray；并列出理事会主席 Benoît Merkt 等9名理事）"
            "三个官方载体交叉确认，满足「重要信息≥2独立来源」铁律。任命路径：2024年度报告（覆盖至2024-12-31）"
            "列前任 Frédéric Debray，2025年度报告改列 Joray，官网2025年11月上传其肖像，判断2025年内接任，"
            "与玻利维亚总经理 Daza（BO-PERSON-000455）的双总部分工亦经官网双语文告核实。"
            "国籍、出生日期、学历、家庭、个人社交账号均无公开可靠来源，相应字段留空并附 note。"
            "身份甄别：Google News RSS 显示瑞士汝拉州文艺界存在同名「Nicolas Joray」（RFJ、Le Quotidien Jurassien 等"
            "2017-2025年戏剧/音乐报道），无法证实与本人为同一人，相关内容未采信。"
            "检索环境受限：WebSearch/web_reader 配额耗尽、主流搜索引擎反爬，改为官网直取+年报PDF解析+Google News RSS。"
            "completeness_score 由 validate_schema.py --score 计算。经评估公开信息客观稀缺：本人可核实的公共记录仅限"
            "基金会官网双语文告与年度报告中的职务列示（无独立媒体报道、无维基数据条目、无个人主页），"
            "出生/学历/家庭/个人社交账号均无来源，political_stances/family 等数组依「查不到留空、禁止编造」铁律留空，"
            "Wikidata 检索命中的 Q23061220（Swiss cinematographer and photographer）为同名他人，未采用；"
            "故得分低于 50 属客观上限，未以推测性条目刷分。"
            "contacts 三项均为任职机构的公务联络渠道（总机/官方邮箱/官网），已按本数据集既有惯例标注来源并注明非个人直线。"
        ),
        "quotes": [
            {
                "title": "Notre engagement fondateur — Fondation Patiño（官网法文版·「Nos forces vives」领导名单，Genève 栏列 Nicolas Joray, Directeur général）",
                "url": "https://patino.org/notre-engagement-fondateur/"
            },
            {
                "title": "Nuestro compromiso fundacional — Fundación Patiño（官网西语版·领导名单，列 Director General Nicolas Joray 及日内瓦/玻利维亚团队）",
                "url": "https://patino.org/es/nuestro-compromiso-fundacional/"
            },
            {
                "title": "Fondation Simón I. Patiño — Rapport d'activités 2025（2025年度报告：截至2025-12-31理事会名单与总干事 Nicolas Joray）",
                "url": "https://patino.org/wp-content/uploads/2026/06/Fondation-Patino_Rapport-activites-2025.pdf"
            },
            {
                "title": "Fondation Simón I. Patiño — Rapport d'activités 2024（2024年度报告：理事会名单与前任总干事 Frédéric Debray）",
                "url": "https://patino.org/wp-content/uploads/2025/09/Fondation-Patino-Rapport-dactivite-2024.pdf"
            },
            {
                "title": "Fondation Patiño — Rapport d'activités 2023（2023年度报告：确认2023年末总干事仍为 Frédéric Debray）",
                "url": "https://patino.org/wp-content/uploads/2024/12/Rapport-dactivite-2023_compressed.pdf"
            },
            {
                "title": "Contact — Fondation Patiño（日内瓦总部 Rue Giovanni-Gambini 8, 1206 Genève 地址与电话）",
                "url": "https://patino.org/contact/"
            }
        ]
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("size:", os.path.getsize(OUT))

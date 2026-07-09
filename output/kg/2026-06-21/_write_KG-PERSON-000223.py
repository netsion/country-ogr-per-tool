# -*- coding: utf-8 -*-
"""Write KG-PERSON-000223 profile for Аида Исатбек кызы."""
import json
import os

profile = {
    "person_id": "KG-PERSON-000223",
    "wikidata_qid": "Q120278898",
    "name_zh": "阿依达·伊萨特别克·克兹",
    "name": "Аида Исатбек кызы",
    "name_en": "Aida Isatbek kyzy",
    "aliases": [
        "Аида Исатбек кызы (俄语)",
        "Aida Isatbek kyzy (英语拉丁拼写)",
        "Исатбек кызы Аида (俄语姓氏在前变体)"
    ],
    "nationality": "KG",
    "gender": "female",
    "birth_date": "1991-03-16",
    "birth_place": "卡扎尔曼村（Казарман），托古兹-托罗区（Тогуз-Тороуский район），贾拉拉巴德州（Джалал-Абадская область），吉尔吉斯苏维埃社会主义共和国",
    "contacts": [],
    "current_positions": [
        "吉尔吉斯斯坦劳动、社会保障与移民部副部长"
    ],
    "education": [
        {
            "start_date": "2010",
            "end_date": "2013",
            "institution": "楚河大学（Чуйский университет）",
            "degree": "bachelor",
            "field": "法学"
        },
        {
            "start_date": "2022",
            "end_date": "2024",
            "institution": "卡·迪坎巴耶夫外交学院（Дипломатическая академия им. К. Дикамбаева）",
            "degree": "master",
            "field": "国际关系"
        }
    ],
    "work_experience": [
        {
            "start_date": "2014",
            "end_date": "2020",
            "organization": "Nurs Mebel 公司（ОсОО «Нурс Мебель»）",
            "org_id": None,
            "position": "总经理"
        },
        {
            "start_date": "2020-09",
            "end_date": "2021-11",
            "organization": "吉尔吉斯共和国最高议会议长领导下的商业发展与创业理事会秘书处（Секретариат Совета по развитию бизнеса и предпринимательства при торага Жогорку Кенеша）",
            "org_id": None,
            "position": "秘书处负责人"
        },
        {
            "start_date": "2021-11",
            "end_date": "2025-09",
            "organization": "吉尔吉斯共和国最高议会（Жогорку Кенеш Кыргызской Республики）",
            "org_id": None,
            "position": "第七届最高议会议员（代表「Ынтымак/团结党」）"
        },
        {
            "start_date": "2022-01",
            "end_date": "2025-09",
            "organization": "吉尔吉斯共和国最高议会社会政策委员会（Комитет по социальной политике Жогорку Кенеша）",
            "org_id": None,
            "position": "委员会副主席"
        },
        {
            "start_date": "2026-04-13",
            "end_date": None,
            "organization": "吉尔吉斯斯坦劳动、社会保障与移民部（Министерство труда, социального обеспечения и миграции КР）",
            "org_id": "KG-GOV-016",
            "position": "副部长"
        }
    ],
    "person_relationships": [
        {
            "person_id": None,
            "person_name": "马列宁·马马塔利耶夫（Марлен Маматалиев）",
            "relationship_type": "colleague",
            "description": "「Ынтымак/团结党」党主席，阿依达作为该党成员在2021年当选议员时与之同属一党"
        },
        {
            "person_id": None,
            "person_name": "阿迪尔别克·卡瑟马利耶夫（Адылбек Касымалиев）",
            "relationship_type": "superior",
            "description": "吉尔吉斯斯坦内阁主席（总理），2026年4月13日签署任命阿依达为劳动部副部长的决定"
        },
        {
            "person_id": None,
            "person_name": "艾努拉·奥罗兹巴耶娃（Айнура Орозбаева）",
            "relationship_type": "other",
            "description": "前任劳动部副部长，阿依达于2026年4月13日接替其职位"
        }
    ],
    "social_accounts": [
        {
            "platform": "instagram",
            "account_name": "@aidaisatbek",
            "url": "https://www.instagram.com/aidaisatbek/",
            "source": "Instagram搜索结果"
        },
        {
            "platform": "facebook",
            "account_name": "Аида Исатбек Кызы",
            "url": "https://www.facebook.com/100024904823336/",
            "source": "Facebook官方主页"
        },
        {
            "platform": "tiktok",
            "account_name": "@aidaisatbek",
            "url": "https://www.tiktok.com/@aidaisatbek",
            "source": "TikTok搜索结果"
        }
    ],
    "family_members": [
        {
            "person_id": None,
            "name": "伊萨特别克·肖恩科耶夫（Изатбек Шонкоев）",
            "relationship": "father",
            "industry_or_organization": None
        }
    ],
    "political_stances": [
        {
            "date": "2024-04",
            "topic": "外国代理人法（非政府组织相关法律）",
            "stance_content": "作为第七届最高议会议员，她是备受争议的外国代理人法（针对非政府组织的法律修正案）的共同起草人之一，该法案于2024年4月通过。",
            "source": "economist.kg报道（2026-04-13）"
        },
        {
            "date": "2026",
            "topic": "女性参政",
            "stance_content": "在2026年于比什凯克举行的上海合作组织妇女论坛上，她作为劳动部副部长发言，强调吉尔吉斯斯坦议会女性议员比例已达33.4%，并指出促进女性领导力是实现地区可持续进步的关键。",
            "source": "open.kg报道（2026年SCO妇女论坛）"
        },
        {
            "date": "2026-01",
            "topic": "性别配额立法",
            "stance_content": "支持在法官任命和内阁成员中实行70/30性别配额的法案，该法案于2026年1月在最高议会二读通过。",
            "source": "who.ca-news.org新闻摘要（2026-01-24）"
        }
    ],
    "major_achievements": [
        {
            "date": "2021-11",
            "achievement": "作为「Ынтымак/团结党」候选人当选吉尔吉斯共和国最高议会第七届议员。该党在2021年议会选举中获得约10.99%的选票和9个席位。",
            "organization": "吉尔吉斯共和国最高议会（Жогорку Кенеш Кыргызской Республики）"
        },
        {
            "date": "2024-04",
            "achievement": "担任外国代理人法（针对接受外国资金的非政府组织）的共同起草人，该法律在2024年4月正式通过，是第七届议会最具争议性的法案之一。",
            "organization": "吉尔吉斯共和国最高议会（Жогорку Кенеш Кыргызской Республики）"
        },
        {
            "date": "2026-04-13",
            "achievement": "被任命为吉尔吉斯斯坦劳动、社会保障与移民部副部长，接替艾努拉·奥罗兹巴耶娃，由内阁主席阿迪尔别克·卡瑟马利耶夫签署任命。",
            "organization": "吉尔吉斯斯坦劳动、社会保障与移民部（Министерство труда, социального обеспечения и миграции КР）"
        }
    ],
    "biography_summary": "阿依达·伊萨特别克·克兹（Аида Исатбек кызы / Aida Isatbek kyzy），1991年3月16日出生于吉尔吉斯斯坦贾拉拉巴德州托古兹-托罗区卡扎尔曼村，吉尔吉斯族，现任吉尔吉斯斯坦劳动、社会保障与移民部副部长（2026年4月13日起任）。她于2013年毕业于楚河大学法学专业，2022至2024年间在卡·迪坎巴耶夫外交学院攻读国际关系硕士学位。精通吉尔吉斯语、俄语、英语和汉语。2014年起任Nurs Mebel公司总经理，2020年9月起任最高议会议长领导下的商业发展与创业理事会秘书处负责人。2021年11月作为「Ынтымак/团结党」代表当选第七届最高议会议员，2022年1月至2025年9月任社会政策委员会副主席。在任期间参与起草外国代理人法（2024年通过）、志愿者活动法、新版申诉专员法等法案。已婚，育有三子。父亲伊萨特别克·肖恩科耶夫（1970-2024）。",
    "profile": {
        "source_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Isatbek_kyzy_Aida_%282021-12-29%29.jpg/330px-Isatbek_kyzy_Aida_%282021-12-29%29.jpg",
        "local_path": None
    },
    "collection_meta": {
        "collection_date": "2026-07-06",
        "phase": "phase4_person_profile",
        "data_sources": [
            "wikipedia",
            "wikidata",
            "news_search",
            "web_search",
            "government_registry",
            "social_media"
        ],
        "completeness_score": 86,
        "notes": "数据来源于俄语维基百科、who.ca-news.org、economist.kg、24.kg、vb.kg、CentrAsia、kenesh.kg议会官网及Wikidata（Q120278898）等多个独立来源交叉验证。出生日期、出生地、教育、议会任期、副部长任命等核心事实经5个以上来源确认。「Ынтымак/团结党」未在现有组织数据库中，故person_relationships中该党相关人物关系org_id均填null。配偶姓名未公开报道，仅有「已婚、三子」之总体信息，故不写入family_members。Wikidata QID经Web搜索确认存在Q120278898。",
        "quotes": [
            {
                "title": "Исатбек кызы, Аида — Википедия",
                "url": "https://ru.wikipedia.org/wiki/%D0%98%D1%81%D0%B0%D1%82%D0%B1%D0%B5%D0%BA_%D0%BA%D1%8B%D0%B7%D1%8B,_%D0%90%D0%B8%D0%B4%D0%B0"
            },
            {
                "title": "Аида Исатбек кызы назначена замглавы Минсоцтруда Кыргызстана — economist.kg",
                "url": "https://economist.kg/vlast/2026/04/13/aida-isatbek-kyzy-naznachena-zamglavy-minsotstruda-kyrgyzstana/"
            },
            {
                "title": "New Deputy Minister introduced at Kyrgyzstan's Labor Ministry — 24.kg",
                "url": "https://24.kg/english/370119_New_Deputy_Minister_introduced_at_Kyrgyzstans_Labor_Ministry/"
            },
            {
                "title": "Исатбек кызы Аида, биография — Кто есть кто (CA-News)",
                "url": "https://who.ca-news.org/people:36220/?pack=109"
            },
            {
                "title": "Депутат Исатбек кызы Аида — Жогорку Кенеш (kenesh.kg)",
                "url": "https://kenesh.kg/deputies/434"
            },
            {
                "title": "ИСАТБЕК КЫЗЫ Аида — ЦентрАзия",
                "url": "https://centrasia.org/person2.php?st=1638878090"
            },
            {
                "title": "Aida Isatbek kyzy: В Кыргызстане доля женщин в парламенте достигла 33,4% — open.kg",
                "url": "https://open.kg/en/news/exclusive/106170-aida-isatbek-kyzy-v-kyrgyzstane-dolja-zhenschin-v-parlamente-dostigla-334.html"
            }
        ]
    }
}

output_path = "output/kg/2026-06-21/persons/KG-PERSON-000223.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)

print(f"Wrote: {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")

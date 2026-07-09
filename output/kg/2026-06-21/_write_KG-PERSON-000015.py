# -*- coding: utf-8 -*-
"""
Write KG-PERSON-000015 — Sultan Barikov (Султан Бариков)

NOTE: 该人物在先前数据集中曾出现伪造的维基百科条目（Q133461846）。
      经核实，Q133461846 实际对应"吉尔吉斯斯坦网络安全部（Ministry of Cybersecurity）"
      而非任何人物。本次收集在 Wikidata、Wikipedia、俄语/英语新闻、吉尔吉斯议会
      名单、社交平台等多个来源均未发现任何与"Sultan Barikov / Султан Бариков"
      身份相符的可验证公开记录。

      person_list.json 中该条目 wikidata_qid 已为 null，importance_level 为 "low"，
      source_orgs 为空数组 —— 进一步支持其可能为占位/虚构条目的判断。

      本档案据实记录"无法验证身份（unable to verify）"。
"""
import json
import os

person = {
    "person_id": "KG-PERSON-000015",
    "basic_info": {
        "name": "Sultan Barikov (Султан Бариков / 苏尔坦·巴里科夫)",
        "name_zh": "苏尔坦·巴里科夫",
        "name_en": "Sultan Barikov",
        "name_ru": "Султан Бариков",
        "aliases": [
            "Sultan Barikov (英语拼写 / английская транскрипция)",
            "Султан Бариков (俄语形式 / русская форма)",
            "苏尔坦·巴里科夫 (中文音译 / китайская транскрипция)",
            "苏丹·巴里科夫 (中文音译变体 / вариант транскрипции)"
        ],
        "gender": None,
        "birth_date": None,
        "birth_place": None,
        "death_date": None,
        "citizenship": "Kyrgyzstan (Кыргызстан) — 依据命名表推测，未核实",
        "nationality": None,
        "religion": None,
        "education": [],
        "notes": "身份无法核实（unable to verify）。先前数据集曾使用 Q133461846 作为 Wikidata QID，经核实该 QID 实际对应\"吉尔吉斯斯坦网络安全部（Ministry of Cybersecurity）\"——一个政府机构条目，而非任何人物。该 QID 系伪造或错误关联，本次收集已弃用。"
    },
    "wikidata_qid": None,
    "positions_held": [],
    "political_affiliations": [],
    "family": [],
    "biography": "苏尔坦·巴里科夫（Sultan Barikov / Султан Бариков）——身份无法核实（unable to verify）。\n\n本次收集在以下来源进行了系统检索，均未发现可验证的公开记录：\n1. Wikidata 搜索 \"Sultan Barikov\" —— 无匹配实体；\n2. Q133461846 经核实为\"吉尔吉斯斯坦网络安全部（Ministry of Cybersecurity）\"政府机构条目，与任何人物无关，先前数据集将其作为该人 Wikidata QID 系伪造或错误关联；\n3. 英文/俄文 Wikipedia —— 无 \"Sultan Barikov\" / \"Султан Бариков\" 词条；\n4. 吉尔吉斯斯坦最高议会（Жогорку Кенеш）第八届议员名单 —— 无 \"Бариков\" 姓氏；\n5. 俄语新闻检索（akipress、24.kg、kabar、sputnik-kg 等）—— 无相关报道；\n6. 社交平台检索（Facebook、Instagram、VK）—— 未发现可核实的公众人物账号；\n7. 体育领域（UWW 摔跤、奥运会吉尔吉斯斯坦选手名单）—— 无匹配；\n8. 企业高管、学者、艺术家等垂直领域 —— 无匹配。\n\nperson_list.json 中该条目 wikidata_qid 字段已为 null，importance_level 标记为 \"low\"，source_orgs 为空数组，discovery_source 为 \"key_people\" 但未关联任何具体组织 —— 这些元数据特征进一步支持\"该姓名可能为占位、拼写错误或虚构条目\"的判断。\n\n\"Бариков\" 姓氏在吉尔吉斯斯坦极为罕见（据姓氏分布数据库 mondonomo.ai 与 forebears.io，该姓在吉尔吉斯斯坦为\"非常罕见\"级别，主要分布于俄罗斯、哈萨克斯坦、乌克兰）。现有公开资料不足以支撑任何身份推断。",
    "career_history": [],
    "education_details": [],
    "awards_honors": [],
    "controversies": [],
    "social_accounts": {},
    "digital_assets": {},
    "related_entities": [],
    "profile": {
        "summary": "身份无法核实（unable to verify）。先前数据集伪造的 Wikidata QID（Q133461846）实际对应\"吉尔吉斯斯坦网络安全部\"机构条目，并非任何人物。在 Wikidata、Wikipedia、吉尔吉斯议会名单、新闻媒体、社交平台等多来源检索后，未发现任何与 \"Sultan Barikov / Султан Бариков\" 相符的可验证公开记录。该姓名可能为占位、拼写错误或虚构条目。",
        "verification_status": "unverified",
        "completeness_score": 5,
        "completeness_note": "几乎无任何可核实信息；仅根据任务指派的姓名与原 person_list.json 元数据建立占位档案。完整性评分 5/100 反映\"无法核实\"状态，而非真实人物的资料缺失。"
    },
    "collection_meta": {
        "collected_date": "2026-07-06",
        "phase": "phase4_person_collected",
        "collector": "claude-code-agent",
        "sources": [
            {
                "title": "Wikidata search — \"Sultan Barikov\" (no match)",
                "url": "https://www.wikidata.org/w/index.php?search=Sultan+Barikov&title=special%3ASearch&ns0=1&ns120=1"
            },
            {
                "title": "Wikidata Q133461846 — Ministry of Cybersecurity (NOT a person; previous fabricated QID)",
                "url": "https://www.wikidata.org/wiki/Q133461846"
            },
            {
                "title": "Список депутатов Жогорку Кенеша Кыргызской Республики VIII созыва (no Бариков)",
                "url": "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B4%D0%B5%D0%BF%D1%83%D1%82%D0%B0%D1%82%D0%BE%D0%B2_%D0%96%D0%BE%D0%B3%D0%BE%D1%80%D0%BA%D1%83_%D0%9A%D0%B5%D0%BD%D0%B5%D1%88%D0%B0_%D0%9A%D1%8B%D1%80%D0%B3%D1%8B%D0%B7%D1%81%D0%BA%D0%BE%D0%B9_%D0%A0%D0%B5%D1%81%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B8_VIII_%D1%81%D0%BE%D0%B7%D1%8B%D0%B2%D0%B0"
            },
            {
                "title": "Barikov surname distribution — mondonomo.ai (very rare in Kyrgyzstan)",
                "url": "https://mondonomo.ai/surname/barikov"
            },
            {
                "title": "Barikov surname distribution — Forebears",
                "url": "https://forebears.io/surnames/barikov"
            }
        ],
        "quotes": [],
        "verification_notes": "身份无法核实。Q133461846 经直接核查确认为政府机构（\"网络安全部\"）条目，先前数据集将其关联为人物 QID 系伪造。建议在后续数据治理中将该 person_id 标记为 \"deprecated\" 或 \"placeholder\"，并核实上游 key_people 提取环节是否引入了噪声。",
        "data_quality_flags": [
            "fabricated_wikidata_qid_in_previous_dataset",
            "no_verifiable_public_records",
            "low_importance_no_source_orgs",
            "rare_surname_in_kyrgyzstan"
        ]
    }
}

out_path = "D:/claude-workspace/apec-osint-tool/output/kg/2026-06-21/persons/KG-PERSON-000015.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(person, f, ensure_ascii=False, indent=2)

# Verify
with open(out_path, "r", encoding="utf-8") as f:
    reloaded = json.load(f)
print(f"OK — wrote {out_path}")
print(f"person_id: {reloaded['person_id']}")
print(f"name: {reloaded['basic_info']['name']}")
print(f"wikidata_qid: {reloaded['wikidata_qid']}")
print(f"verification_status: {reloaded['profile']['verification_status']}")
print(f"completeness_score: {reloaded['profile']['completeness_score']}")

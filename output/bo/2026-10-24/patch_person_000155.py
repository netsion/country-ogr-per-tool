# -*- coding: utf-8 -*-
"""Patch BO-PERSON-000155.json: add 5th work entry, 4th stance, 4th relationship, profile photo."""
import json

path = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons\BO-PERSON-000155.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 1) 5th work_experience: international consultant roles (SIN official bio + Red Uno)
data["work_experience"].append({
    "start_date": None,
    "end_date": None,
    "organization": "联合国开发计划署等国际机构 (PNUD, CIAT, BID, CESO, JICA)",
    "org_id": None,
    "position": "税务专家/国际顾问",
    "description": "以税务专家（especialista tributario）身份在联合国开发计划署（PNUD）、美洲税收管理中心（CIAT）、美洲开发银行（BID）、加拿大行政服务机构（CESO）、日本国际协力机构（JICA）等机构从事财政政策、治理与税收征管效率相关项目；并作为技术援助顾问服务于玻利维亚、秘鲁、日本政府。",
    "source": "https://www.impuestos.gob.bo/index.php/nota_prensa/el-ministro-de-economia-posesiona-a-jorge-leonardo-zogbi-como-presidente-del-sin/",
    "note": "多项并行咨询业务，具体起止年份未公开。SIN官方新闻稿与Red Uno报道双源确认。"
})

# 2) 4th political_stance: 2026-06-11 deregulation/simplification
data["political_stances"].append({
    "date": "2026-06-11",
    "topic": "简化企业监管程序",
    "stance_content": "作为税收减免与简化合规议程的一部分，宣布企业将不再需要取得生产监管机构的事先授权，以降低企业经营的行政合规成本。",
    "source": "https://x.com/ContBolivia/status/2065182272341389761"
})

# 3) 4th person_relationship: Alberto Soto (colleague, sworn in same day)
data["person_relationships"].append({
    "person_id": None,
    "person_name": "阿尔贝托·索托 (Alberto Soto)",
    "relationship_type": "colleague",
    "description": "2025-11-25与索格比在拉巴斯经济部同日宣誓，分别就任国家海关署（ANB）执行总裁与国家税务局（SIN）执行局长，为帕斯政府税务海关整顿组合的平行同僚。"
})

# 4) profile photo
data["profile"] = {
    "source_url": "https://www.impuestos.gob.bo/wp-content/uploads/2025/11/designacion.jpeg",
    "local_path": "photos/BO-PERSON-000155.jpg"
}

# 5) update collection_meta.notes to reflect additions
data["collection_meta"]["notes"] = "来源构成：SIN与海关署官网一手公告2篇全文精读；Red Uno、ANF/Noticias Fides、Bolivianos Destacados博客3篇全文精读；经济部/SIN/CNC等机构社媒吊唁与活动帖、LinkedIn快照、Sputnik/El Deber/eju.tv报道交叉引用。多语言检索（西语为主，英语/中文辅）共执行13轮搜索。Wikidata检索无此人条目；官方新闻稿照片已本地化存档（photos/BO-PERSON-000155.jpg）。completeness_score受name_zh（无既有译名）、birth_date/birth_place（无公开来源）、wikidata_qid（无条目）四项客观缺失限制。"

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("PATCHED:", path)
print("work_experience:", len(data["work_experience"]))
print("political_stances:", len(data["political_stances"]))
print("person_relationships:", len(data["person_relationships"]))
print("profile:", data["profile"])

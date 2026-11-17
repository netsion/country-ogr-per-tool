# -*- coding: utf-8 -*-
"""修复 TG-GOV-003 的错误 QID 污染（Q866730 是维基媒体"多哥总统列表"条目，非总统府机构）
1. _target_orgs.json: TG-GOV-003 wikidata_qid -> null
2. orgs/TG-GOV-003.json: 修正 basic_info 三处名称，清除 QID 与 thumb 图片 URL，notes 记录原因
3. 删除 _cache/Q866730.json（列表条目缓存，防止后续工具重新关联）
"""
import json
import os
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r"D:\ai-workspace\apec-osint-tool\output\tg\2026-11-16"

# 1) target
tp = os.path.join(BASE, "_target_orgs.json")
t = json.load(open(tp, encoding="utf-8"))
for o in t["organizations"]:
    if o["id"] == "TG-GOV-003":
        o["wikidata_qid"] = None
        o["verification_status"] = "partial"
with open(tp, "w", encoding="utf-8") as f:
    json.dump(t, f, ensure_ascii=False, indent=2)

# 2) skeleton
sp = os.path.join(BASE, "orgs", "TG-GOV-003.json")
d = json.load(open(sp, encoding="utf-8"))
bi = d["basic_info"]
bi["name_original"] = "Présidence de la République togolaise"
bi["name_zh"] = "多哥总统府"
bi["name_en"] = "Presidency of the Republic of Togo"
bi["aliases"] = ["Presidency of the Republic", "Présidence du Togo"]
bi["wikidata_qid"] = None
d["profile"] = {"source_url": None, "local_path": None}
cm = d.get("collection_meta") or {}
cm["notes"] = ("Skeleton from cached Wikidata + Wikipedia data; "
               "wikidata_qid cleared 2026-11-16: Q866730 was a Wikimedia list article "
               "('list of presidents of Togo'), not the presidency institution. "
               "P3 to re-source via official website/news.")
cm["data_sources"] = ["wikipedia"]
d["collection_meta"] = cm
with open(sp, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

# 3) cache 删除
cp = os.path.join(BASE, "_cache", "Q866730.json")
removed = False
if os.path.exists(cp):
    os.remove(cp)
    removed = True

# 验证
chk = json.load(open(sp, encoding="utf-8"))
assert chk["basic_info"]["wikidata_qid"] is None
assert chk["basic_info"]["name_en"] == "Presidency of the Republic of Togo"
assert chk["key_people"] and chk["key_people"][0]["person_id"] == "TG-PERSON-000004"
tchk = json.load(open(tp, encoding="utf-8"))
g3 = next(x for x in tchk["organizations"] if x["id"] == "TG-GOV-003")
assert g3["wikidata_qid"] is None
print("cache Q866730.json removed:", removed)
print("TG-GOV-003 fixed: qid=null, names corrected, key_people intact")

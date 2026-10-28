# -*- coding: utf-8 -*-
"""Agent D task 1: fix _zh_violations (org_no_cjk / rel_name_no_cjk)."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
PERSONS = os.path.join(BASE, "persons")

# (pid, kind, idx, expected_current, new_value)
FIXES = [
    ("BO-PERSON-000060", "org", 7, "Bolivian Foods S.A. (Bolivian Foods S.A.)",
     "玻利维亚食品公司（Bolivian Foods S.A.）"),
    ("BO-PERSON-000087", "org", 2, "Bioconstruc S.R.L.",
     "比奥建造公司（Bioconstruc S.R.L.）"),
    ("BO-PERSON-000192", "org", 2, "Leader Global Solutions LLC",
     "领航全球解决方案公司（Leader Global Solutions LLC）"),
    ("BO-PERSON-000227", "rel", 0, "Mario Alberto Patiño Serrate",
     "马里奥·阿尔贝托·帕蒂尼奥·塞拉特（Mario Alberto Patiño Serrate）"),
    ("BO-PERSON-000328", "org", 12, "NAFIBO ST (NAFIBO ST)",
     "纳菲沃公司（NAFIBO ST）"),
    ("BO-PERSON-000355", "org", 2, "HELP GLOBAL SRL (HG)",
     "援助环球咨询公司（HELP GLOBAL SRL）"),
    ("BO-PERSON-000355", "org", 3, "AGEBOL SRL",
     "阿赫博尔报关公司（AGEBOL SRL）"),
    ("BO-PERSON-000396", "org", 3, "AAM (AAM)",
     "AAM公司（AAM）"),
    ("BO-PERSON-000500", "org", 0, "Netcomidas (Netcomidas)",
     "网络订餐公司（Netcomidas）"),
    ("BO-PERSON-000500", "org", 1, "Yango Bolivia (Yango Bolivia)",
     "扬戈玻利维亚公司（Yango Bolivia）"),
    ("BO-PERSON-000500", "org", 2, "MOBI Latam (MOBI Latam)",
     "莫比拉美公司（MOBI Latam）"),
    ("BO-PERSON-000508", "org", 6, "APB Súmate (Autonomía Para Bolivia Súmate)",
     "玻利维亚自治-加入党（Autonomía Para Bolivia Súmate）"),
    ("BO-PERSON-000521", "org", 4, "Meridian SRL",
     "梅里迪安有限公司（Meridian SRL）"),
    ("BO-PERSON-000521", "org", 5, "Socinter SRL",
     "索辛特有限公司（Socinter SRL）"),
    ("BO-PERSON-000521", "org", 6, "Management Development Group Overseas",
     "海外管理发展集团（Management Development Group Overseas）"),
    ("BO-PERSON-000521", "org", 7, "SC Cables",
     "SC电缆公司（SC Cables）"),
]

cache = {}
changed = 0
for pid, kind, idx, old, new in FIXES:
    if pid not in cache:
        path = os.path.join(PERSONS, pid + ".json")
        with open(path, encoding="utf-8") as f:
            cache[pid] = (path, json.load(f))
    path, data = cache[pid]
    if kind == "org":
        entry = data["work_experience"][idx]
        field = "organization"
    else:
        entry = data["person_relationships"][idx]
        field = "person_name"
    cur = entry.get(field)
    if cur != old:
        raise SystemExit("MISMATCH %s %s[%d] field=%s current=%r expected=%r"
                         % (pid, kind, idx, field, cur, old))
    entry[field] = new
    changed += 1
    print("OK %s %s[%d].%s: %r -> %r" % (pid, kind, idx, field, old, new))

for path, data in cache.values():
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
print("Changed %d entries across %d files" % (changed, len(cache)))

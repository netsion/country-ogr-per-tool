# -*- coding: utf-8 -*-
"""P4 language fixes: add Chinese to zero-CN person/institution names."""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = "output/ci/2026-10-06/persons"

# verified Chinese renderings (standard transliterations)
NAME_ZH = {
    "Michel Zunon-Kipré": "米歇尔·祖农-基普雷",
    "GONNIN Gilbert": "吉尔贝·戈宁",
    "Djely Lamine Brahima Coulibaly": "杰利·拉米内·布拉希马·库利巴利",
    "Laurent Dona-Fologo": "洛朗·多纳-福洛戈",
    "Patricia Barabas": "帕特里夏·巴拉巴斯",
    "Eleanor Linda Jordan": "埃莉诺·琳达·乔丹",
    "Duncan Israel": "邓肯·伊斯雷尔",
    "Maijory Chitupa Mung'omba": "玛乔莉·奇图帕·蒙贡巴",
    "Fhara Gutierrez": "法拉·古铁雷斯",
}
INST_ZH = {
    "INSEAD": "欧洲工商管理学院 (INSEAD)",
    "CAS-UEMOA": "西非经货联盟会计税务进修中心 (CAS-UEMOA)",
}

def fmt(name, zh):
    return f"{zh} ({name})" if "(" not in name else f"{zh} {name}"

fixed = 0
for fn in sorted(os.listdir(BASE)):
    if not fn.endswith(".json") or fn == "_index.json":
        continue
    fp = os.path.join(BASE, fn)
    d = json.load(open(fp, encoding="utf-8"))
    pid = d.get("person_id", fn[:-5])
    changed = False
    for r in d.get("person_relationships", []) or []:
        nm = r.get("person_name") or ""
        if nm in NAME_ZH:
            r["person_name"] = fmt(nm, NAME_ZH[nm]); changed = True
    for r in d.get("family_members", []) or []:
        nm = r.get("name") or ""
        if nm in NAME_ZH:
            r["name"] = fmt(nm, NAME_ZH[nm]); changed = True
    for e in d.get("education", []) or []:
        t = e.get("institution") or ""
        if t in INST_ZH:
            e["institution"] = INST_ZH[t]; changed = True
    if changed:
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        fixed += 1
        print("fixed:", pid)
print("total files fixed:", fixed)

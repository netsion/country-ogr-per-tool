# -*- coding: utf-8 -*-
"""Audit-fix patch: GOV-001 rename, GOV-020 L1 upgrade, name backfills."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ORGS = os.path.join(BASE, "orgs")


def load(fn):
    with open(os.path.join(ORGS, fn), encoding="utf-8") as f:
        return json.load(f)


def save(fn, d):
    with open(os.path.join(ORGS, fn), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def set_name(d, name_en, name_original, name_zh):
    bi = d["basic_info"]
    bi["name_en"] = name_en
    bi["name_original"] = name_original
    if name_zh:
        bi["name_zh"] = name_zh


# registry canonical zh names
reg = json.load(open(os.path.join(BASE, "id_registry.json"), encoding="utf-8"))
reg_name = {r["org_id"]: r.get("name") for r in reg["registry"]}


def zh_from_registry(oid):
    n = reg_name.get(oid) or ""
    return n.split(" (")[0] if " (" in n else (n or None)


# 1. KW-GOV-001: list-page name -> office name (enwiki title "Emir of Kuwait", Q246932)
d = load("KW-GOV-001.json")
set_name(d, "Emir of Kuwait", "أمير دولة الكويت", "科威特埃米尔")
d["collection_meta"]["notes"] = "Head-of-state office per JO/BN/KG dataset precedent; enwiki 'Emir of Kuwait' anchors Q246932 (WD en label is stale list-page name)."
save("KW-GOV-001.json", d)
reg_name["KW-GOV-001"] = "科威特埃米尔 (Emir of Kuwait)"

# 2. KW-GOV-020: L3 -> L1 with Q115925879
d = load("KW-GOV-020.json")
set_name(d, "The Kuwait Municipality", "بلدية الكويت", "科威特市政厅")
d["basic_info"]["wikidata_qid"] = "Q115925879"
d["collection_meta"]["data_sources"] = ["wikidata", "wikipedia"]
d["collection_meta"]["notes"] = "L3->L1 during P2 audit: enwiki 'The Kuwait Municipality' -> Q115925879 (P31=Q43229)."
save("KW-GOV-020.json", d)
reg_name["KW-GOV-020"] = "科威特市政厅 (The Kuwait Municipality)"

# 3. name backfills (Arabic originals from P1 target-list aliases / WD labels)
backfill = {
    "KW-GOV-021.json": ("State Audit Bureau", "ديوان المحاسبة", zh_from_registry("KW-GOV-021")),
    "KW-SOE-001.json": ("Kuwait Petroleum Corporation", "المؤسسة العامة للبترول", zh_from_registry("KW-SOE-001")),
    "KW-SOE-004.json": ("Kuwait Petroleum International", "بترول الكويت الدولية", zh_from_registry("KW-SOE-004")),
    "KW-SOE-006.json": ("Oil Sector Services Company", "شركة خدمات القطاع النفطي", zh_from_registry("KW-SOE-006")),
}
for fn, (en, orig, zh) in backfill.items():
    d = load(fn)
    set_name(d, en, orig, zh)
    save(fn, d)

# 4. sync registry names + QID for GOV-020
for r in reg["registry"]:
    r["name"] = reg_name.get(r["org_id"], r.get("name"))
    if r["org_id"] == "KW-GOV-020":
        r["wikidata_qid"] = "Q115925879"
with open(os.path.join(BASE, "id_registry.json"), "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)

print("patched: KW-GOV-001 rename, KW-GOV-020 L1, 4x name backfill, registry synced")
print("GOV-021 zh:", zh_from_registry("KW-GOV-021"), "| SOE-004 zh:", zh_from_registry("KW-SOE-004"), "| SOE-006 zh:", zh_from_registry("KW-SOE-006"))

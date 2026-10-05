# -*- coding: utf-8 -*-
"""Repair: 1) restore wrongly-trimmed KW-CORP-008 (KNCC) 2) trim KW-CORP-013 (United Networks) 3) fix ISO3 KWP->KWT."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ORGS = os.path.join(BASE, "orgs")

# ---------- load cache for KNCC ----------
cache = json.load(open(os.path.join(BASE, "_cache", "Q6448856.json"), encoding="utf-8"))
org_block = cache.get("org", {})
wd = cache.get("wikidata", {})
claims = wd.get("claims", {})
labels = wd.get("labels", {})


def dv_time(pid):
    # org founded_date is strict YYYY-MM-DD; Wikidata year/month precision -> 01-01 / MM-01 per skill §10
    for c in claims.get(pid, []):
        t = c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("time", "")
        if t:
            y, m, d = t[1:5], t[6:8], t[9:11]
            return f"{y}-{m if m != '00' else '01'}-{d if d != '00' else '01'}"
    return None


name_en = org_block.get("name") or wd.get("labels", {}).get("en", {}).get("value") or "Kuwait National Cinema Company"
name_orig = wd.get("labels", {}).get("ar", {}).get("value") or (org_block.get("aliases") or [None])[0]

# registry zh name
reg = json.load(open(os.path.join(BASE, "id_registry.json"), encoding="utf-8"))
reg_map = {r["org_id"]: r for r in reg["registry"]}
rn = reg_map["KW-CORP-008"].get("name") or ""
name_zh = rn.split(" (")[0] if " (" in rn else None

skeleton = {
    "org_id": "KW-CORP-008",
    "basic_info": {
        "name_original": name_orig,
        "name_zh": name_zh,
        "name_en": name_en,
        "aliases": [],
        "org_type": "CORP",
        "org_subtype": "publicly_listed",
        "country_iso3": "KWT",
        "hq_country_iso3": "KWT",
        "founded_date": dv_time("P571"),
        "website": org_block.get("website"),
        "wikidata_qid": "Q6448856",
    },
    "social_accounts": [],
    "digital_assets": [],
    "key_people": [],
    "departments": [],
    "recent_events": [],
    "related_entities": [],
    "core_business": None,
    "industries": [],
    "apec_stance": None,
    "profile": None,
    "collection_meta": {
        "collection_date": "2026-10-03",
        "phase": "phase2_skeleton",
        "data_sources": ["wikidata", "wikipedia"],
        "completeness_score": 10,
        "notes": "Restored from cache Q6448856 after trim-ID mixup (was wrongly trimmed as CORP-008 on 2026-10-03; trim target was CORP-013 United Networks).",
    },
}
with open(os.path.join(ORGS, "KW-CORP-008.json"), "w", encoding="utf-8") as f:
    json.dump(skeleton, f, ensure_ascii=False, indent=2)
print("restored KW-CORP-008:", name_en, "| orig:", name_orig, "| zh:", name_zh, "| founded:", skeleton["basic_info"]["founded_date"], "| website:", skeleton["basic_info"]["website"])

# ---------- trim CORP-013 United Networks ----------
d13 = json.load(open(os.path.join(ORGS, "KW-CORP-013.json"), encoding="utf-8"))
assert d13["basic_info"]["name_en"] == "United Networks" and d13["basic_info"]["wikidata_qid"] == "Q7888986", "unexpected CORP-013 content, abort"
os.remove(os.path.join(ORGS, "KW-CORP-013.json"))

reg_map["KW-CORP-008"].update({"status": "profiled", "notes": None})
reg_map["KW-CORP-013"].update({
    "status": "trimmed",
    "notes": "insignificance: KIPCO holding platform, no enwiki, 4 claims, no independent activity; telecom covered by Zain/Ooredoo/Fast",
})
with open(os.path.join(BASE, "id_registry.json"), "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)
print("registry: CORP-008 profiled / CORP-013 trimmed")

# ---------- _target_orgs: re-add KNCC, remove United Networks ----------
t_path = os.path.join(BASE, "_target_orgs.json")
t = json.load(open(t_path, encoding="utf-8"))
tl = t["organizations"] if isinstance(t, dict) else t
tl[:] = [o for o in tl if o["id"] != "KW-CORP-013"]
if not any(o["id"] == "KW-CORP-008" for o in tl):
    tl.append({
        "id": "KW-CORP-008",
        "wikidata_qid": "Q6448856",
        "name": name_en,
        "aliases": org_block.get("aliases") or [],
        "category": "CORP",
        "subcategory": "Entertainment",
        "description": org_block.get("description"),
        "headquarters": org_block.get("headquarters") or "Kuwait City",
        "country": "KW",
        "website": org_block.get("website"),
        "key_people": [],
        "relationships": [],
        "sources": [{"type": "wikidata", "url": "https://www.wikidata.org/wiki/Q6448856"}],
        "verification_status": "verified",
    })
with open(t_path, "w", encoding="utf-8") as f:
    json.dump(t, f, ensure_ascii=False, indent=2)
print(f"_target_orgs now: {len(tl)}")

# ---------- ISO3 fix: KWP -> KWT everywhere ----------
fixed = 0
for fn in os.listdir(ORGS):
    if not fn.endswith(".json") or not fn.startswith("KW-"):
        continue
    p = os.path.join(ORGS, fn)
    d = json.load(open(p, encoding="utf-8"))
    bi = d["basic_info"]
    ch = False
    if bi.get("country_iso3") == "KWP":
        bi["country_iso3"] = "KWT"; ch = True
    if bi.get("hq_country_iso3") == "KWP":
        bi["hq_country_iso3"] = "KWT"; ch = True
    if ch:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        fixed += 1
print(f"ISO3 fixed in {fixed} files")

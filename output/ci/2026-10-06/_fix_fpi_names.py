import json

BASE = "output/ci/2026-10-06"

# FPI (CI-PARTY-003): fix name fields contaminated by wrong Wikidata label "RHDP"
with open(f"{BASE}/orgs/CI-PARTY-003.json", encoding="utf-8") as f:
    d = json.load(f)
bi = d["basic_info"]
assert bi["wikidata_qid"] == "Q1422092"
bi["name_en"] = "Ivorian Popular Front"
bi["name_original"] = "Front populaire ivoirien"
with open(f"{BASE}/orgs/CI-PARTY-003.json", "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("FPI profile: name_en/name_original fixed")

# RHDP (CI-PARTY-001): traditional -> simplified Chinese
with open(f"{BASE}/orgs/CI-PARTY-001.json", encoding="utf-8") as f:
    d = json.load(f)
bi = d["basic_info"]
if bi.get("name_zh") == "烏弗埃民主和平聯盟":
    bi["name_zh"] = "乌弗埃民主和平联盟"
    with open(f"{BASE}/orgs/CI-PARTY-001.json", "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("RHDP profile: name_zh simplified")

# update target list names for the 2 dropped-QID orgs note + verify all reloaded
for p in [f"{BASE}/orgs/CI-PARTY-003.json", f"{BASE}/orgs/CI-PARTY-001.json",
          f"{BASE}/orgs/CI-GOV-011.json", f"{BASE}/orgs/CI-GOV-012.json",
          f"{BASE}/orgs/CI-GOV-020.json", f"{BASE}/orgs/CI-CORP-004.json",
          f"{BASE}/orgs/CI-CORP-006.json", f"{BASE}/orgs/CI-FIN-009.json"]:
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    bi = d["basic_info"]
    print(f"  {d['org_id']}: qid={bi.get('wikidata_qid')} | {bi.get('name_en')} | {bi.get('name_original')}")

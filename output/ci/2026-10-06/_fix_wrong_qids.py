"""Fix the 6 wrongly-QID'd orgs + FPI profile check + registry status."""
import json
import os

BASE = "output/ci/2026-10-06"

# --- 1. target list fixes ---
tpath = f"{BASE}/_target_orgs.json"
with open(tpath, encoding="utf-8") as f:
    targets = json.load(f)

# restore original correct QID (script "fix" was a regression)
RESTORE = {
    "CI-CORP-004": "Q3488399",    # SIFCA groupe industriel ivoirien
    "CI-CORP-006": "Q3361548",    # Palmci
    "CI-GOV-020": "Q112863189",   # Min. Environment CI
}
# wrong QID, no verified replacement -> L3 (no QID)
DROP = ["CI-GOV-011", "CI-GOV-012", "CI-FIN-009"]

WRONG_CACHE_QIDS = ["Q140635280", "Q125608468", "Q111998898", "Q65128150", "Q3315297", "Q134283275"]
RESTORED_ORGS = ["CI-CORP-004", "CI-CORP-006", "CI-GOV-020"]
DROPPED_ORGS = ["CI-GOV-011", "CI-GOV-012", "CI-FIN-009"]

for t in targets:
    if t["id"] in RESTORE:
        t.pop("qid", None)
        t["wikidata_qid"] = RESTORE[t["id"]]
        t["verification_status"] = "verified"
    elif t["id"] in DROP:
        removed = t.pop("qid", None)
        t.pop("wikidata_qid", None)
        t["verification_status"] = "partial"

with open(tpath, "w", encoding="utf-8") as f:
    json.dump(targets, f, ensure_ascii=False, indent=2)
print(f"1. target list: restored {list(RESTORE)}, dropped QID from {DROP}")

# --- 2. delete wrong caches and wrong profiles ---
for q in WRONG_CACHE_QIDS:
    p = f"{BASE}/_cache/{q}.json"
    if os.path.exists(p):
        os.remove(p)
print("2. deleted 6 wrong cache files")

for oid in RESTORED_ORGS + DROPPED_ORGS:
    p = f"{BASE}/orgs/{oid}.json"
    if os.path.exists(p):
        os.remove(p)
print("2. deleted 6 wrong profiles (will regenerate)")

# --- 3. registry: CI-MEDIA-006 status revert ---
rpath = f"{BASE}/id_registry.json"
with open(rpath, encoding="utf-8") as f:
    reg = json.load(f)
for r in reg.get("registry", []):
    if r.get("org_id") == "CI-MEDIA-006":
        r["status"] = "listed"
        print("3. registry: CI-MEDIA-006 status profiled -> listed")
with open(rpath, "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)

# --- 4. inspect FPI (CI-PARTY-003) and RHDP (CI-PARTY-001) profiles ---
for oid in ["CI-PARTY-001", "CI-PARTY-003"]:
    with open(f"{BASE}/orgs/{oid}.json", encoding="utf-8") as f:
        d = json.load(f)
    bi = d["basic_info"]
    print(f"4. {oid}: qid={bi.get('wikidata_qid')} | name_en={bi.get('name_en')} | "
          f"name_zh={bi.get('name_zh')} | name_original={bi.get('name_original')}")
    for kp in (d.get("key_people") or [])[:6]:
        print(f"     kp: {kp.get('name')} | {kp.get('title')}")

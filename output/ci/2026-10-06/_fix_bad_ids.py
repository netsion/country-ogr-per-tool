"""Fix non-standard org IDs: renumber to standard enum-based IDs, update files + registry + counters."""
import json
import glob
import re
import os

BASE = "output/ci/2026-10-06"
ORGS = f"{BASE}/orgs"

# canonical mapping: bad id -> (new_id, new_org_type_enum)
FIXES = {
    "CI-company-001": ("CI-CORP-014", "CORP"),      # China Nat'l Geological & Mining (foreign CORP per skill rule: assign by main activity country CI context)
    "CI-CORP-023": ("CI-CORP-015", "CORP"),          # Abidjan Terminal
    "CI-CORP-024": ("CI-CORP-016", "CORP"),          # Sitarail
    "CI-association-001": ("CI-INTL-011", "INTL"),   # AGPAOC (HQ Abidjan, international association)
    "CI-association-002": ("CI-INTL-012", "INTL"),   # AIVP
}
# orgs to register as new: CIT (currently null in SOE-005)
NEW = {"科特迪瓦码头": ("CI-CORP-017", "CORP")}

# 1. update referencing org files
for fp in glob.glob(f"{ORGS}/*.json"):
    with open(fp, encoding="utf-8") as f:
        d = json.load(f)
    changed = False
    for rel in d.get("related_entities", []) or []:
        oid = rel.get("org_id")
        if oid in FIXES:
            rel["org_id"], rel["org_type"] = FIXES[oid]
            changed = True
        elif oid is None and rel.get("org_name", "").startswith("科特迪瓦码头"):
            rel["org_id"], rel["org_type"] = NEW["科特迪瓦码头"]
            changed = True
    if changed:
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"updated {d['org_id']}")

# 2. registry: drop bad entries, add corrected ones
rpath = f"{BASE}/id_registry.json"
reg = json.load(open(rpath, encoding="utf-8"))
new_entries = [r for r in reg["registry"] if r.get("org_id") not in FIXES]
have = {r.get("org_id") for r in new_entries}
for old, (new, typ) in FIXES.items():
    if new not in have:
        new_entries.append({"org_id": new, "name": old, "org_type": typ, "org_subtype": None,
                            "wikidata_qid": None, "status": "listed", "notes": "renamed from non-standard id (audit fix)"})
for nm, (new, typ) in NEW.items():
    if new not in have:
        new_entries.append({"org_id": new, "name": nm, "org_type": typ, "org_subtype": None,
                            "wikidata_qid": None, "status": "listed", "notes": "registered from related_entity (audit fix)"})
reg["registry"] = new_entries

# 3. recompute counters as true max seq per type from registry + files
files = {os.path.basename(p)[:-5] for p in glob.glob(f"{ORGS}/*.json")}
counters = {}
for oid in set(files) | {r.get("org_id") for r in new_entries}:
    m = re.match(r"^CI-([A-Z]+)-(\d{3})$", oid or "")
    if m:
        counters[m.group(1)] = max(counters.get(m.group(1), 0), int(m.group(2)))
reg["counters"] = {"CI": counters}
with open(rpath, "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)

# verify
ids = [r["org_id"] for r in new_entries]
bad = [i for i in ids if not re.match(r"^CI-(GOV|SOE|CORP|NGO|ACAD|MEDIA|FIN|INTL|PARTY|MIL)-\d{3}$", i)]
dupe = [i for i in set(ids) if ids.count(i) > 1]
print(f"registry size={len(ids)}, bad={bad}, dupes={dupe}, counters={counters}")

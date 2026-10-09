"""Second bad-ID fix: rename 6 non-standard registry IDs to standard enum-based IDs."""
import json
import glob
import re
import os

BASE = "output/ci/2026-10-06"
ORGS = f"{BASE}/orgs"

FIXES = {
    "CI-international_organization-001": ("CI-INTL-013", "INTL"),  # IFRC
    "CI-international_organization-002": ("CI-INTL-014", "INTL"),  # ICRC
    "CI-international_organization-003": ("CI-INTL-015", "INTL"),  # Socialist International
    "CI-hospital-001": ("CI-GOV-039", "GOV"),                       # Mère-Enfant hospital (public)
    "CI-REBEL_GROUP-001": ("CI-PARTY-012", "PARTY"),                # MPIGO (political-military movement)
    "CI-REBEL_GROUP-002": ("CI-PARTY-013", "PARTY"),                # MJP (political-military movement)
}

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
    if changed:
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"updated {d['org_id']}")

# 2. registry: rename entries
rpath = f"{BASE}/id_registry.json"
reg = json.load(open(rpath, encoding="utf-8"))
have = {r.get("org_id") for r in reg["registry"]}
kept = []
for r in reg["registry"]:
    oid = r.get("org_id")
    if oid in FIXES:
        new, typ = FIXES[oid]
        r["org_id"] = new
        r["org_type"] = typ
        if new in have:
            continue  # collision safety
        have.add(new)
    kept.append(r)
reg["registry"] = kept

# 3. recompute counters
files = {os.path.basename(p)[:-5] for p in glob.glob(f"{ORGS}/*.json")}
counters = {}
for oid in set(files) | {r.get("org_id") for r in kept}:
    mm = re.match(r"^CI-([A-Z]+)-(\d{3})$", oid or "")
    if mm:
        counters[mm.group(1)] = max(counters.get(mm.group(1), 0), int(mm.group(2)))
reg["counters"] = {"CI": counters}
with open(rpath, "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)

ids = [r["org_id"] for r in kept]
bad = [i for i in ids if not re.match(r"^CI-(GOV|SOE|CORP|NGO|ACAD|MEDIA|FIN|INTL|PARTY|MIL)-\d{3}$", i)]
dupe = [i for i in set(ids) if ids.count(i) > 1]
print(f"registry size={len(ids)}, bad={bad}, dupes={dupe}")

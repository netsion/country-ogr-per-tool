"""Consolidate wrongly-allocated IDs back to target-list IDs; dedupe registry."""
import json
import glob
import os
from collections import defaultdict

BASE = "output/ci/2026-10-06"
ORGS = f"{BASE}/orgs"

# new_id -> target_id (content provenance verified earlier)
RENAME = {
    "CI-CORP-014": "CI-CORP-004",   # SIFCA (Q3488399)
    "CI-CORP-015": "CI-CORP-006",   # Palmci (Q3361548)
    "CI-GOV-028": "CI-GOV-011",     # Min Economie et Finances (no qid)
    "CI-GOV-029": "CI-GOV-012",     # Min Justice (no qid)
    "CI-GOV-030": "CI-GOV-020",     # Min Environnement (Q112863189)
    "CI-FIN-012": "CI-FIN-009",     # Bridge Bank Group CI (no qid)
    "CI-MEDIA-009": "CI-MEDIA-006", # L'Inter
}
DELETE = ["CI-MEDIA-010"]  # duplicate L'Inter

with open(f"{BASE}/id_registry.json", encoding="utf-8") as f:
    reg = json.load(f)

# 1. rename profile files + fix internal org_id
for new_id, target_id in RENAME.items():
    src = f"{ORGS}/{new_id}.json"
    dst = f"{ORGS}/{target_id}.json"
    with open(src, encoding="utf-8") as f:
        d = json.load(f)
    d["org_id"] = target_id
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    os.remove(src)
    print(f"1. {new_id} -> {target_id} (content: {d['basic_info'].get('name_en')})")

# restore correct qids inside renamed profiles
RESTORED_QID = {"CI-CORP-004": "Q3488399", "CI-CORP-006": "Q3361548", "CI-GOV-020": "Q112863189"}
for oid, qid in RESTORED_QID.items():
    p = f"{ORGS}/{oid}.json"
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    d["basic_info"]["wikidata_qid"] = qid
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
print("1b. restored wikidata_qid in 3 profiles")

# 2. delete duplicate L'Inter profile
for oid in DELETE:
    p = f"{ORGS}/{oid}.json"
    if os.path.exists(p):
        os.remove(p)
        print(f"2. deleted duplicate profile {oid}")

# 3. registry cleanup
entries = reg["registry"]
new_entries = []
seen_ids = set()
for r in entries:
    oid = r.get("org_id")
    if oid in DELETE or oid in RENAME:
        continue  # drop old/dup entries; target-ID entries already exist below
    new_entries.append(r)
# ensure every target ID has exactly one registry entry, status profiled
target_ids = set()
with open(f"{BASE}/_target_orgs.json", encoding="utf-8") as f:
    for t in json.load(f):
        target_ids.add(t["id"])
existing_by_id = {r["org_id"]: r for r in new_entries}
for tid in target_ids:
    if tid not in existing_by_id:
        # registry entry lost -> rebuild minimal from target list
        t = next(t for t in json.load(open(f"{BASE}/_target_orgs.json", encoding="utf-8")) if t["id"] == tid)
        existing_by_id[tid] = {
            "org_id": tid,
            "name": t.get("name", ""),
            "org_type": t.get("category"),
            "org_subtype": t.get("subcategory"),
            "wikidata_qid": t.get("qid") or t.get("wikidata_qid"),
            "status": "profiled" if os.path.exists(f"{ORGS}/{tid}.json") else "listed",
            "notes": "rebuilt_by_audit",
        }
        new_entries.append(existing_by_id[tid])
# fix status/qid for the consolidated ones
for r in new_entries:
    if r["org_id"] in RESTORED_QID:
        r["wikidata_qid"] = RESTORED_QID[r["org_id"]]
    if r["org_id"] == "CI-MEDIA-006":
        r["status"] = "profiled"
reg["registry"] = new_entries

# 4. recount org files vs registry; rebuild counters from disk max seq
files = {os.path.basename(p)[:-5] for p in glob.glob(f"{ORGS}/*.json")}
counters = defaultdict(int)
for oid in files:
    parts = oid.split("-")
    counters[parts[1]] = max(counters[parts[1]], int(parts[2]))
reg["counters"] = {"CI": dict(counters)}
with open(f"{BASE}/id_registry.json", "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)

print(f"4. files={len(files)}, registry entries={len(new_entries)}, counters={dict(counters)}")
print(f"   file-vs-target diff: missing={sorted(target_ids - files)}, extra={sorted(files - target_ids)}")
reg_ids = [r["org_id"] for r in new_entries]
dupes = [i for i in set(reg_ids) if reg_ids.count(i) > 1]
print(f"   registry dupes: {dupes}, registry-not-in-files: {sorted(set(reg_ids) - files)}")

# -*- coding: utf-8 -*-
"""Set EG-GOV-037 wikidata_qid to null (was a Wikimedia disambiguation page)."""
import json, glob, sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import load_json, save_json

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
OID = "EG-GOV-037"
BAD = "Q133404956"

n = 0
# target file
t = load_json(f"{BASE}/_target_orgs.json")
for o in t["organizations"]:
    if o["id"] == OID:
        assert o.get("wikidata_qid") == BAD, o.get("wikidata_qid")
        o["wikidata_qid"] = None
        o["notes"] = (o.get("notes") or "") + " | audit 2026-11-17: QID was a Wikimedia disambiguation page, set null; resolve via Arabic name in P3"
        n += 1
save_json(f"{BASE}/_target_orgs.json", t)

# skeleton
p = f"{BASE}/orgs/{OID}.json"
d = load_json(p)
if d["basic_info"].get("wikidata_qid") == BAD:
    d["basic_info"]["wikidata_qid"] = None
    d["collection_meta"]["notes"] = (d["collection_meta"].get("notes") or "") + "; audit: disambiguation-page QID nulled"
    save_json(p, d)
    n += 1

# registry
r = load_json(f"{BASE}/id_registry.json")
for e in r["registry"]:
    if e["org_id"] == OID and e.get("wikidata_qid") == BAD:
        e["wikidata_qid"] = None
        save_json(f"{BASE}/id_registry.json", r)
        n += 1

print(f"patched {n} locations")

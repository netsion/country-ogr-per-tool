# -*- coding: utf-8 -*-
"""Re-mark 3 mistakenly-enriched excluded orgs: registry status excluded_enriched, profiles noted."""
import json, sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import load_json, save_json

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
IDS = ["EG-CORP-013", "EG-CORP-016", "EG-CORP-017"]

reg = load_json(f"{BASE}/id_registry.json")
for e in reg["registry"]:
    if e["org_id"] in IDS:
        e["status"] = "excluded_enriched"
        e["notes"] = (e.get("notes") or "") + " | P3 dispatch error: enriched despite trim; keep data, excluded from P5 scope count"
save_json(f"{BASE}/id_registry.json", reg)

for oid in IDS:
    p = f"{BASE}/orgs/{oid}.json"
    d = load_json(p)
    d["collection_meta"]["phase"] = "phase3_enriched_out_of_scope"
    d["collection_meta"]["notes"] = (d["collection_meta"].get("notes") or "") + "; out-of-scope: enriched by dispatch error, excluded from P5 statistics (OSINT trim 2026-11-17)"
    save_json(p, d)

prog = load_json(f"{BASE}/_phase_progress.json")
prog["out_of_scope_enriched"] = IDS
prog["in_scope_completed_actual"] = len([c for c in prog["completed"] if c not in IDS])
save_json(f"{BASE}/_phase_progress.json", prog)
print("re-marked:", IDS)
print("in-scope completed:", prog["in_scope_completed_actual"], "| remaining:", len(prog["remaining"]))

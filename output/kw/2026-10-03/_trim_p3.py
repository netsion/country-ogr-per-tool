# -*- coding: utf-8 -*-
"""P3 trim: remove 3 low-significance orgs per audit decision."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ORGS = os.path.join(BASE, "orgs")

TRIM = {
    "KW-NGO-009": ("Kuwait Society For Relief", "insignificance: no enwiki, new Q136096413 item w/o description, 5 claims; charity sector covered by stronger NGOs"),
    "KW-NGO-010": ("Kuwait Society for Humanitarian Work", "insignificance: no enwiki, new Q136094714 item w/o description, 4 claims; humanitarian sector covered"),
    "KW-CORP-008": ("United Networks", "insignificance: KIPCO holding platform, no enwiki, 4 claims, no independent activity; telecom covered by Zain/Ooredoo/Fast"),
}

# 1. delete org files
deleted = []
for oid in TRIM:
    p = os.path.join(ORGS, f"{oid}.json")
    if os.path.exists(p):
        os.remove(p)
        deleted.append(oid)
print("deleted org files:", deleted)

# 2. registry: mark trimmed (keep for audit trail, IDs never reused)
reg_path = os.path.join(BASE, "id_registry.json")
reg = json.load(open(reg_path, encoding="utf-8"))
for r in reg["registry"]:
    if r["org_id"] in TRIM:
        r["status"] = "trimmed"
        r["notes"] = TRIM[r["org_id"]][1]
with open(reg_path, "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)
active = sum(1 for r in reg["registry"] if r["status"] == "profiled")
print(f"registry: {active} profiled / {sum(1 for r in reg['registry'] if r['status']=='trimmed')} trimmed")

# 3. remove from _target_orgs.json (operative P2/P3 input list)
t_path = os.path.join(BASE, "_target_orgs.json")
t = json.load(open(t_path, encoding="utf-8"))
orgs = t["organizations"] if isinstance(t, dict) else t
before = len(orgs)
orgs[:] = [o for o in orgs if o["id"] not in TRIM]
with open(t_path, "w", encoding="utf-8") as f:
    json.dump(t, f, ensure_ascii=False, indent=2)
print(f"_target_orgs: {before} -> {len(orgs)}")

# 4. dangling reference check (related_entities / key_people / person refs)
import glob
leftover = []
for fp in glob.glob(os.path.join(ORGS, "KW-*.json")):
    d = json.load(open(fp, encoding="utf-8"))
    for re_ in d.get("related_entities") or []:
        if re_.get("org_id") in TRIM:
            leftover.append((d["org_id"], "related_entities", re_.get("org_id")))
for fp in glob.glob(os.path.join(BASE, "persons", "*.json")):
    d = json.load(open(fp, encoding="utf-8"))
    if d.get("org_id") in TRIM:
        leftover.append((d.get("person_id"), "person.org_id", d.get("org_id")))
print("dangling refs:", leftover if leftover else "none")

# -*- coding: utf-8 -*-
"""Merge duplicate: keep EG-PERSON-000063 (canonical, fuller Arabic name), retire 000110."""
import json, glob, sys
BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
CANON = "EG-PERSON-000063"
DUP = "EG-PERSON-000110"
CANON_NAME = "艾哈迈德·法特希·哈利法（音译） (أحمد فتحي إبراهيم خليفة)"

# 1. registry: update canonical name, remove dup entry
reg = json.load(open(f"{BASE}/id_registry.json", encoding="utf-8"))
plist = reg["person_registry"]
for e in plist:
    if e.get("person_id") == CANON:
        e["name_en"] = CANON_NAME
        e.setdefault("source_orgs", [])
        for o in ["EG-GOV-006", "EG-MIL-001", "EG-MIL-002"]:
            if o not in e["source_orgs"]:
                e["source_orgs"].append(o)
        e["dedupe_note"] = "merged duplicate EG-PERSON-000110 (same chief-of-staff, name variant) 2026-11-17"
reg["person_registry"] = [e for e in plist if e.get("person_id") != DUP]
json.dump(reg, open(f"{BASE}/id_registry.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# 2. update referencing profiles
changed = 0
for p in sorted(glob.glob(f"{BASE}/orgs/*.json")):
    d = json.load(open(p, encoding="utf-8"))
    dirty = False
    for kp in d.get("key_people", []) or []:
        if kp.get("person_id") == DUP:
            kp["person_id"] = CANON
            kp["name"] = CANON_NAME
            dirty = True
        elif kp.get("person_id") == CANON and kp.get("name") != CANON_NAME:
            kp["name"] = CANON_NAME
            dirty = True
    if dirty:
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        changed += 1
        print("updated:", d["org_id"])

with open(f"{BASE}/_tmp/khalifa_merge_log.txt", "w", encoding="utf-8") as f:
    f.write(f"merged {DUP} into {CANON}, {changed} profiles updated\n")
print("profiles updated:", changed)

# -*- coding: utf-8 -*-
"""P5: mark registry persons without profile files as status='trimmed'."""
import json
import os

BASE = "output/ci/2026-10-06"
REG = os.path.join(BASE, "id_registry.json")
PERSONS = os.path.join(BASE, "persons")

with open(REG, encoding="utf-8") as f:
    reg = json.load(f)

files = {fn[:-5] for fn in os.listdir(PERSONS) if fn.endswith(".json")}
changed = 0
for entry in reg.get("person_registry", []):
    pid = entry.get("person_id")
    if not pid or pid in files:
        continue
    if entry.get("status") != "trimmed":
        entry["status"] = "trimmed"
        changed += 1

with open(REG, "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)
print(f"marked {changed} registry persons as trimmed")

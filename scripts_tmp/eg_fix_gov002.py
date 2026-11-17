# -*- coding: utf-8 -*-
"""Fix EG-GOV-002 key_people: Ghaffar title was his old Higher-Ed post; verified Health Minister (GOV-010, 5 sources)."""
import sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import load_json, save_json

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
d = load_json(f"{BASE}/orgs/EG-GOV-002.json")
changed = 0
for kp in d.get("key_people", []):
    if kp.get("person_id") == "EG-PERSON-000011":
        print("BEFORE:", kp.get("name"), "|", kp.get("title"), "|", kp.get("title_description"))
        if "高等教育" in (kp.get("title") or ""):
            kp["title"] = "卫生和人口部长 (وزير الصحة والسكان)"
            kp["title_description"] = "主管全国卫生与人口事务，2024-07起兼任人力发展副总理，2026-02改组卸任副总理兼职（GOV-010画像五源核实）"
            changed += 1
        print("AFTER:", kp.get("name"), "|", kp.get("title"))
if changed:
    save_json(f"{BASE}/orgs/EG-GOV-002.json", d)
print("fixed:", changed)

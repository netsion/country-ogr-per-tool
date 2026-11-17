# -*- coding: utf-8 -*-
"""Add cross-profile conflict note: NRC profile claims Muawwad acting ASRT chair; ASRT profile (multi-source) says Gina El-Feky. Flag for P5."""
import sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import load_json, save_json
BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
d = load_json(f"{BASE}/orgs/EG-ACAD-018.json")
changed = 0
for kp in d.get("key_people", []):
    if "穆阿瓦德" in (kp.get("name") or ""):
        kp["title_description"] = (kp.get("title_description") or "") + "【P5复核】其「兼任ASRT代理主席」表述与EG-ACAD-020画像冲突（ASRT侧多源指向代理院长吉娜·法基，2025-12续任），两说并存待核"
        changed += 1
if changed:
    d["collection_meta"]["notes"] = (d["collection_meta"].get("notes") or "") + "; P5复核项: 穆阿瓦德兼任ASRT代理主席与ACAD-020画像冲突（法基vs穆阿瓦德）"
    save_json(f"{BASE}/orgs/EG-ACAD-018.json", d)
print("notes added:", changed)

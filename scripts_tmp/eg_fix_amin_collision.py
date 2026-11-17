# -*- coding: utf-8 -*-
"""Fix name collision: journalist Mustafa Amin (Akhbar El-Yom founder, d.1997) wrongly bound to EG-PERSON-000121 (NSPO ex-director). Set null + flag."""
import sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import load_json, save_json
BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
d = load_json(f"{BASE}/orgs/EG-MEDIA-003.json")
fixed = 0
for kp in d.get("key_people", []):
    if kp.get("person_id") == "EG-PERSON-000121":
        kp["person_id"] = None
        kp["description"] = (kp.get("description") or "") + "【修正2026-11-17】原误绑 EG-PERSON-000121（NSPO前总干事，当代军方人物）；创始人记者穆斯塔法·阿明(1914-1997)与该人物同名不同人，person_id置null"
        fixed += 1
if fixed:
    d["collection_meta"]["notes"] = (d["collection_meta"].get("notes") or "") + "; ID修正: 创始人穆斯塔法·阿明与EG-PERSON-000121(NSPO)同名不同人，已置null"
    save_json(f"{BASE}/orgs/EG-MEDIA-003.json", d)
print("fixed:", fixed)

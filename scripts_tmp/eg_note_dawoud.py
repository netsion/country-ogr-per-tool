# -*- coding: utf-8 -*-
"""Flag Dawoud cross-org ID (000267: Al-Azhar Univ president + former NARSS chair) for P5 verification."""
import sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import load_json, save_json
BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
for oid, kw in [("EG-ACAD-002", "达乌德"), ("EG-ACAD-021", "达乌德")]:
    d = load_json(f"{BASE}/orgs/{oid}.json")
    hit = False
    for kp in d.get("key_people", []):
        if kw in (kp.get("name") or "") and kp.get("person_id") == "EG-PERSON-000267":
            kp["description"] = (kp.get("description") or "") + "【P5复核】EG-PERSON-000267 同时关联 EG-ACAD-002（爱资哈尔大学校长）与 EG-ACAD-021（NARSS前主席），同名同人判定依据通信工程教授履历，建议P5二次确认非同名不同人"
            hit = True
    if hit:
        d["collection_meta"]["notes"] = (d["collection_meta"].get("notes") or "") + "; P5复核项: 达乌德(000267)跨机构双职判定需确认"
        save_json(f"{BASE}/orgs/{oid}.json", d)
        print("flagged:", oid)

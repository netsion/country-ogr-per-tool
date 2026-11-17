# -*- coding: utf-8 -*-
"""Dedupe check: Khalifa chief-of-staff 000063 vs 000110."""
import json, glob, sys

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
out = []
reg = json.load(open(f"{BASE}/id_registry.json", encoding="utf-8"))
plist = reg.get("person_registry", [])
out.append(f"person_registry entry keys sample: {list(plist[0].keys())}")
for e in plist:
    pid = str(e.get("person_id") or e.get("id") or "")
    if "000063" in pid or "000110" in pid:
        out.append(f"REG {pid}: {json.dumps(e, ensure_ascii=False)[:200]}")

idx = json.load(open(f"{BASE}/_name_index.json", encoding="utf-8"))
blob = json.dumps(idx, ensure_ascii=False)
for pid in ["EG-PERSON-000063", "EG-PERSON-000110"]:
    cnt = blob.count(pid)
    out.append(f"INDEX occurrences of {pid}: {cnt}")

for p in sorted(glob.glob(f"{BASE}/orgs/*.json")):
    d = json.load(open(p, encoding="utf-8"))
    for kp in d.get("key_people", []) or []:
        pid = kp.get("person_id")
        if pid in ("EG-PERSON-000063", "EG-PERSON-000110"):
            out.append(f"REF {d['org_id']}: {pid} | name={kp.get('name')} | title={kp.get('title')}")

with open(f"{BASE}/_tmp/khalifa_dedupe_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("written", len(out), "lines")

# -*- coding: utf-8 -*-
"""Clean GOV-031 notes: remove wrong GAFI CEO claim (Hiba El-Sibaie name confusion, verified by GOV-047)."""
import sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import load_json, save_json

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
d = load_json(f"{BASE}/orgs/EG-GOV-031.json")
meta = d.get("collection_meta", {})
notes = meta.get("notes") or ""
print("BEFORE notes:", notes[:400])
if "GAFI" in notes and ("希巴" in notes or "Sibaie" in notes or "西拜伊" in notes):
    # replace wrong claim with verified chain
    fixed = notes
    for wrong in ["GAFI 前 CEO 希巴 2026-01 卸任已两源确认，继任者未经多源核实，按铁律留空",
                  "GAFI前CEO希巴2026-01卸任已两源确认，继任者未经多源核实，按铁律留空"]:
        fixed = fixed.replace(wrong, "GAFI CEO沿革经GOV-047核实：海巴(2022-2025)→吉奥斯基(2026短任)→阿瓦德(2026-04现任总理令1301/2026)")
    meta["notes"] = fixed
    save_json(f"{BASE}/orgs/EG-GOV-031.json", d)
    print("AFTER notes:", meta["notes"][:400])
else:
    print("no wrong claim found in notes")

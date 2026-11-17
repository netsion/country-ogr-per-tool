# -*- coding: utf-8 -*-
"""Fix GOV-046 events: add verified source URLs, remove 2 unverifiable events (宁缺毋滥)."""
import sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import load_json, save_json
BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
SOURCES = {
    "612/2026": "https://edaegypt.gov.eg/media/vicni4az/612-2026_ar.pdf",
    "480/2026": "https://www.eastlaws.com/legislation-full-text/ar/egypt/egyptian-drug-authority-president-decision/23-09-2026/no-480?type=1&id=5671172",
    "eCTD": "https://www.linkedin.com/posts/egyptian-drug-authority_egyptiandrugauthority-egyptiandrugauthoritymediacenter-activity-7500873346088280065-OfRg",
    "47/2025": "https://edaegypt.gov.eg/media/je0jyocs/قرار-رقم-47-لسنة-2025.pdf",
}
d = load_json(f"{BASE}/orgs/EG-GOV-046.json")
keep = []
for ev in d.get("recent_events", []):
    t = ev.get("title", "")
    if "612" in t:
        ev["source"] = SOURCES["612/2026"]; keep.append(ev)
    elif "480" in t:
        ev["source"] = SOURCES["480/2026"]; keep.append(ev)
    elif "eCTD" in t:
        ev["source"] = SOURCES["eCTD"]; keep.append(ev)
    elif "47/2025" in t:
        ev["source"] = SOURCES["47/2025"]; keep.append(ev)
    else:
        print("REMOVED (unverifiable):", t[:50])
d["recent_events"] = keep
d["collection_meta"]["notes"] = (d["collection_meta"].get("notes") or "") + "; P3收尾修复: 2条无法溯源事件按宁缺毋滥移除, 余4条补官方PDF/全文库/官方LinkedIn来源 (主会话2026-11-17)"
save_json(f"{BASE}/orgs/EG-GOV-046.json", d)
print("kept:", len(keep), "events")

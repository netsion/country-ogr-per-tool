# -*- coding: utf-8 -*-
import json, time, urllib.request, urllib.parse, sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import setup_proxy, load_json, save_json
setup_proxy()

# 1) verify the two uncertain candidates with full labels
url = ("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q16120918|Q20419500|Q68171436"
       "&props=labels|descriptions|claims&languages=en|ar&format=json")
req = urllib.request.Request(url, headers={"User-Agent": "ApecOsintTool/1.0"})
with urllib.request.urlopen(req, timeout=30) as r:
    ents = json.loads(r.read().decode())["entities"]
lines = []
for q, e in ents.items():
    lab = e.get("labels", {})
    desc = e.get("descriptions", {}).get("en", {}).get("value", "")
    lines.append(f"{q}: en={lab.get('en',{}).get('value')} | ar={lab.get('ar',{}).get('value')} | desc={desc} | claims={len(e.get('claims',{}))}")
time.sleep(2)

# 2) apply fixes
BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
targets = load_json(f"{BASE}/_target_orgs.json")
fixes = {
    "EG-CORP-018": "Q68171436",
    "EG-MIL-006":  "Q16120918",
    "EG-SOE-011":  "Q253927",
    "EG-FIN-013":  "Q20419500",
}
n = 0
for o in targets["organizations"]:
    if o["id"] in fixes:
        old = o.get("wikidata_qid")
        o["wikidata_qid"] = fixes[o["id"]]
        lines.append(f"APPLY {o['id']}: {old} -> {fixes[o['id']]} ({o['name']})")
        n += 1
save_json(f"{BASE}/_target_orgs.json", targets)
lines.append(f"saved, {n} fixes applied")
with open(f"{BASE}/_tmp/qid_fix_log.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("\n".join(lines))

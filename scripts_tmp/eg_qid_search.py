# -*- coding: utf-8 -*-
import json, time, urllib.request, urllib.parse, sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import setup_proxy
setup_proxy()

names = [
    "Al Ahram Beverages",
    "National Authority for Military Production",
    "Egyptian National Railways",
    "Misr Insurance",
    "Misr Insurance Company",
]
out = []
for n in names:
    url = ("https://www.wikidata.org/w/api.php?action=wbsearchentities&search="
           + urllib.parse.quote(n) + "&language=en&format=json&limit=5")
    req = urllib.request.Request(url, headers={"User-Agent": "ApecOsintTool/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
    for hit in data.get("search", []):
        out.append(f"query={n} | {hit.get('id')} | {hit.get('label')} | {hit.get('description','')}")
    time.sleep(2)

with open(r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16\_tmp\qid_search.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"{len(out)} hits written")

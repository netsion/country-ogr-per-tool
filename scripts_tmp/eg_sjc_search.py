# -*- coding: utf-8 -*-
"""Find correct QID for Supreme Judicial Council of Egypt."""
import json, time, urllib.request, urllib.parse, sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import setup_proxy
setup_proxy()

out = []
for q in ["Supreme Judicial Council Egypt", "Supreme Judicial Council",
          "Higher Judicial Council Egypt"]:
    url = ("https://www.wikidata.org/w/api.php?action=wbsearchentities&search="
           + urllib.parse.quote(q) + "&language=en&format=json&limit=8")
    req = urllib.request.Request(url, headers={"User-Agent": "ApecOsintTool/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
    for h in data.get("search", []):
        out.append(f"{q} | {h.get('id')} | {h.get('label')} | {h.get('description','')}")
    time.sleep(2)

import io, sys as _s
_s.stdout = io.TextIOWrapper(_s.stdout.buffer, encoding="utf-8")
print("\n".join(out) or "no hits")

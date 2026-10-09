import json
import subprocess
import time
import urllib.parse

PROXY = "http://127.0.0.1:7890"


def api_get(url):
    cmd = ["curl", "-sL", "--proxy", PROXY, "--max-time", "30", url]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8").stdout
    return json.loads(r)


# 1. Q1422092 sitelinks: which wikipedia article does it belong to?
d = api_get("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q1422092&props=sitelinks&format=json")
sl = d["entities"]["Q1422092"].get("sitelinks", {})
print("Q1422092 sitelinks:", {k: v.get("title") for k, v in list(sl.items())[:8]})
time.sleep(2)

# 2. RHDP real item
d = api_get("https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&limit=4&language=en&search="
            + urllib.parse.quote("Rassemblement des Houphouetistes pour la Democratie et la Paix"))
print("\nRHDP search:")
for r in d.get("search", []):
    print(f"  {r['id']}: {r.get('label')} — {(r.get('description') or '')[:60]}")
time.sleep(2)

# 3. remaining entries in English
for q in ["Ministry of Economy and Finance Ivory Coast",
          "Ministry of Justice Ivory Coast",
          "Bridge Bank Group Ivory Coast"]:
    d = api_get("https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&limit=4&language=en&search="
                + urllib.parse.quote(q))
    print(f"\n[{q}]")
    for r in d.get("search", []):
        print(f"  {r['id']}: {r.get('label')} — {(r.get('description') or '')[:60]}")
    time.sleep(2)

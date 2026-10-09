import json
import subprocess
import time
import urllib.parse

PATH = "output/ci/2026-10-06/_target_orgs.json"
PROXY = "http://127.0.0.1:7890"

with open(PATH, encoding="utf-8") as f:
    orgs = json.load(f)

missing = [o for o in orgs if not (o.get("qid") or o.get("wikidata_qid"))]
print(f"{len(missing)} entries missing QID")


def search(name, lang):
    url = (
        "https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json"
        f"&limit=5&language={lang}&search={urllib.parse.quote(name)}"
    )
    cmd = ["curl", "-sL", "--proxy", PROXY, "--max-time", "30", url]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8").stdout
    try:
        return json.loads(out).get("search", [])
    except Exception:
        return []


candidates = []
for o in missing:
    name = o.get("name", "")
    hits = search(name, "fr")
    time.sleep(1)
    if not hits:
        # strip parenthetical and retry in English
        base = name.split("(")[0].strip()
        hits = search(base, "en")
        time.sleep(1)
    if hits:
        top = hits[0]
        candidates.append((o["id"], name[:50], top.get("id"), top.get("label", ""), (top.get("description") or "")[:60]))
    else:
        candidates.append((o["id"], name[:50], None, "", "NO HIT"))

for c in candidates:
    print(c)

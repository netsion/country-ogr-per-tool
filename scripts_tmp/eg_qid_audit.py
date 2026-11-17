# -*- coding: utf-8 -*-
"""EG QID audit: batch-fetch labels for all wikidata_qid, compare with org names."""
import json, sys, time, urllib.request, urllib.parse
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import setup_proxy

setup_proxy()
BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"

with open(f"{BASE}/_target_orgs.json", encoding="utf-8") as f:
    targets = json.load(f)["organizations"]

qids = {}
for o in targets:
    q = o.get("wikidata_qid") or o.get("qid")
    if q:
        qids.setdefault(q, []).append(o["id"])

def fetch_batch(qid_list):
    url = ("https://www.wikidata.org/w/api.php?action=wbgetentities&ids="
           + urllib.parse.quote("|".join(qid_list))
           + "&props=labels|descriptions&languages=en|ar&format=json")
    req = urllib.request.Request(url, headers={"User-Agent": "ApecOsintTool/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

all_ids = sorted(qids)
result = {}
for i in range(0, len(all_ids), 50):
    batch = all_ids[i:i+50]
    try:
        data = fetch_batch(batch)
        for qid, ent in data.get("entities", {}).items():
            label = ent.get("labels", {}).get("en", {}).get("value")
            ar = ent.get("labels", {}).get("ar", {}).get("value")
            desc = ent.get("descriptions", {}).get("en", {}).get("value")
            if label is None and "missing" in ent:
                result[qid] = {"missing": True}
            else:
                result[qid] = {"en": label, "ar": ar, "desc": desc}
    except Exception as e:
        print(f"batch {i//50} error: {e}")
        for q in batch:
            result[q] = {"error": str(e)}
    time.sleep(2)

with open(f"{BASE}/_tmp/qid_labels.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print(f"fetched {len(result)} entities, saved to _tmp/qid_labels.json")
missing = [q for q, v in result.items() if v.get("missing")]
errs = [q for q, v in result.items() if v.get("error")]
print(f"missing: {len(missing)} {missing}")
print(f"errors: {len(errs)} {errs}")

"""Resolve the 7 problematic entries: check old QIDs, Q1422092 identity, search correct QIDs."""
import json
import subprocess
import time
import urllib.parse

PROXY = "http://127.0.0.1:7890"


def api_get(url):
    cmd = ["curl", "-sL", "--proxy", PROXY, "--max-time", "30", url]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8").stdout
    return json.loads(r)


def labels_of(qids):
    url = ("https://www.wikidata.org/w/api.php?action=wbgetentities&ids="
           + "|".join(qids) + "&props=labels|descriptions|claims&languages=en|fr&format=json")
    d = api_get(url)
    out = {}
    for qid, ent in d.get("entities", {}).items():
        labs = ent.get("labels", {})
        desc = (ent.get("descriptions", {}).get("en") or ent.get("descriptions", {}).get("fr") or {}).get("value", "")
        inc = ""
        for cl in ent.get("claims", {}).get("P571", []):  # inception
            inc = cl["mainsnak"]["datavalue"]["value"]["time"]
        out[qid] = (labs.get("en", {}).get("value") or labs.get("fr", {}).get("value"), desc, inc)
    return out


def search(q, lang="en", limit=4):
    url = ("https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json"
           f"&limit={limit}&language={lang}&search={urllib.parse.quote(q)}")
    d = api_get(url)
    return [(r["id"], r.get("label", ""), (r.get("description") or "")[:60]) for r in d.get("search", [])]


print("=== 1. old wikidata_qid values (candidates to restore) ===")
for q, lab in labels_of(["Q3488399", "Q3361548", "Q112863189"]).items():
    print(f"  {q}: {lab}")
time.sleep(2)

print("\n=== 2. Q1422092 identity (RHDP label, claimed FPI) ===")
print(" ", labels_of(["Q1422092"]))
time.sleep(2)

print("\n=== 3. search correct QIDs ===")
queries = [
    ("SIFCA group Cote d'Ivoire", "en"),
    ("Palmci", "en"),
    ("FPI Front populaire ivoirien", "fr"),
    ("Ministère Économie Finances Côte d'Ivoire", "fr"),
    ("Ministère Justice Côte d'Ivoire", "fr"),
    ("Ministère Environnement Côte d'Ivoire", "fr"),
    ("Bridge Bank Côte d'Ivoire", "en"),
]
for q, lang in queries:
    print(f"  [{q}]")
    for hit in search(q, lang):
        print(f"    {hit[0]}: {hit[1]} — {hit[2]}")
    time.sleep(2)

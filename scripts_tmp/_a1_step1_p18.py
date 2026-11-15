import json, os, subprocess, urllib.parse, sys

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

TARGETS = {
    "NG-PERSON-000017": "Q25753711",
    "NG-PERSON-000130": "Q139666510",
    "NG-PERSON-000140": "Q35496974",
    "NG-PERSON-000159": "Q123361810",
    "NG-PERSON-000167": "Q108704107",
    "NG-PERSON-000168": "Q29514826",
    "NG-PERSON-000173": "Q117112512",
    "NG-PERSON-000174": "Q123362161",
    "NG-PERSON-000201": "Q123003396",
    "NG-PERSON-000212": "Q130220299",
    "NG-PERSON-000226": "Q5984649",
    "NG-PERSON-000233": "Q124049613",
    "NG-PERSON-000237": "Q123367928",
    "NG-PERSON-000273": "Q136457095",
    "NG-PERSON-000293": "Q123110548",
}

def curl_json(url):
    r = subprocess.run(
        ["curl", "-s", "-x", PROXY, "-A", UA, "--max-time", "40", url],
        capture_output=True, text=True)
    return r.stdout

results = {}
for pid, qid in TARGETS.items():
    url = "https://www.wikidata.org/wiki/Special:EntityData/%s.json" % qid
    raw = curl_json(url)
    try:
        d = json.loads(raw)
        ent = d["entities"][qid]
        p18 = ent.get("claims", {}).get("P18", [])
        names = []
        for c in p18:
            v = c.get("mainsnak", {}).get("datavalue", {}).get("value", {})
            if isinstance(v, dict):
                names.append(v.get("time", "") and v or v)
        # simpler: grab the text value
        names = []
        for c in p18:
            dv = c.get("mainsnak", {}).get("datavalue", {})
            val = dv.get("value")
            if isinstance(val, str):
                names.append(val)
        results[pid] = {"qid": qid, "p18": names}
        print(pid, qid, "->", names)
    except Exception as e:
        results[pid] = {"qid": qid, "error": str(e), "raw_head": raw[:200]}
        print(pid, qid, "ERROR", str(e), raw[:120])

with open(os.path.join(BASE, "scripts_tmp", "_a1_p18_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)

import json, os, subprocess, urllib.parse, time

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "AvatarBackfillBot/1.0 (contact: research@example.com)"

QUERIES = {
    "NG-PERSON-000281": "Nasir Abdulsalam",
    "NG-PERSON-000293": "Tola Odeyemi",
    "NG-PERSON-000311": "Olakunle Alake",
    "NG-PERSON-000312": "Devakumar Edwin",
    "NG-PERSON-000174": "Uba Ahmadu",
    "NG-PERSON-000201": "Adeniyi customs",
    "NG-PERSON-000273": "Adighije",
}

def curl_json(url):
    r = subprocess.run(
        ["curl", "-s", "-x", PROXY, "-A", UA, "--max-time", "40", url],
        capture_output=True)
    return r.stdout.decode("utf-8", "replace")

results = {}
for pid, q in QUERIES.items():
    time.sleep(5)
    url = ("https://commons.wikimedia.org/w/api.php?action=query&list=search"
           "&srsearch=%s&srnamespace=6&srlimit=8&format=json" % urllib.parse.quote(q))
    raw = curl_json(url)
    try:
        d = json.loads(raw)
        hits = [h["title"] for h in d["query"]["search"]]
    except Exception:
        hits = ["ERROR: " + raw[:100]]
    results[pid] = hits
    print(pid, q, "=>", len(hits), flush=True)

# also get direct URL for Joseph Tegbe images
time.sleep(3)
for title in ["File:Joseph Tegbe.jpg", "File:Joseph Tegbe at Main one-Business Day Broadband summit.jpg"]:
    time.sleep(3)
    url = ("https://commons.wikimedia.org/w/api.php?action=query&titles=%s"
           "&prop=imageinfo&iiprop=url|size|mime&format=json" % urllib.parse.quote(title))
    raw = curl_json(url)
    results[title] = raw
    print(title, "=>", raw[:400], flush=True)

with open(os.path.join(BASE, "scripts_tmp", "_a1_commons_c.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("done")

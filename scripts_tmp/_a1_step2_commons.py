import json, os, subprocess, urllib.parse

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

QUERIES = {
    "NG-PERSON-000017": "Abubakar Kyari",
    "NG-PERSON-000130": "Joseph Tegbe",
    "NG-PERSON-000140": "Yusuf Abdullahi Ata",
    "NG-PERSON-000159": "Joseph Utsev",
    "NG-PERSON-000167": "Maigari Dingyadi",
    "NG-PERSON-000168": "Nkeiruka Onyejeocha",
    "NG-PERSON-000172": "Nneka Anibeze",
    "NG-PERSON-000173": "Abubakar Momoh",
    "NG-PERSON-000174": "Uba Maigari Ahmadu",
    "NG-PERSON-000183": "Mariya Bunkure",
    "NG-PERSON-000185": "Richard Yunana Dauda",
    "NG-PERSON-000201": "Bashir Adewale Adeniyi",
    "NG-PERSON-000212": "Aminu Maida",
    "NG-PERSON-000226": "Ibrahim Ida Katsina",
    "NG-PERSON-000233": "Jamila Bio Ibrahim",
    "NG-PERSON-000237": "Ayodele Olawande",
    "NG-PERSON-000268": "Sule Ahmed Abdulaziz",
    "NG-PERSON-000273": "Jennifer Adighije",
    "NG-PERSON-000281": "Nasir Abdulsalam Ajaokuta",
    "NG-PERSON-000293": "Tola Odeyemi",
    "NG-PERSON-000311": "Olakunle Alake",
    "NG-PERSON-000312": "Devakumar Edwin",
}

def curl_json(url):
    r = subprocess.run(
        ["curl", "-s", "-x", PROXY, "-A", UA, "--max-time", "40", url],
        capture_output=True, text=True)
    return r.stdout

results = {}
for pid, q in QUERIES.items():
    url = ("https://commons.wikimedia.org/w/api.php?action=query&list=search"
           "&srsearch=%s&srnamespace=6&srlimit=10&format=json" % urllib.parse.quote(q))
    raw = curl_json(url)
    try:
        d = json.loads(raw)
        hits = [(h["title"], h.get("snippet", "")[:120]) for h in d["query"]["search"]]
    except Exception as e:
        hits = [("ERROR", raw[:150])]
    results[pid] = hits
    print(pid, q, "=>", len(hits))
    for t, s in hits[:10]:
        print("   ", t, "|", s)

with open(os.path.join(BASE, "scripts_tmp", "_a1_commons_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)

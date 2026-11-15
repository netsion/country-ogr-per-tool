import json, os, subprocess, urllib.parse, time

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

TITLES = {
    "NG-PERSON-000017": "Abubakar Kyari",
    "NG-PERSON-000140": "Yusuf Abdullahi Ata",
    "NG-PERSON-000159": "Joseph Utsev",
    "NG-PERSON-000167": "Mohammed Maigari Dingyadi",
    "NG-PERSON-000168": "Nkeiruka Onyejeocha",
    "NG-PERSON-000173": "Abubakar Eshiokpekha Momoh",
    "NG-PERSON-000174": "Uba Maigari Ahmadu",
    "NG-PERSON-000201": "Bashir Adewale Adeniyi",
    "NG-PERSON-000212": "Aminu Maida",
    "NG-PERSON-000226": "Ibrahim M. Ida",
    "NG-PERSON-000233": "Jamila Bio Ibrahim",
    "NG-PERSON-000237": "Ayodele Olawande",
    "NG-PERSON-000273": "Jennifer Adighije",
    "NG-PERSON-000293": "Tola Odeyemi",
    "NG-PERSON-000130": "Joseph Tegbe",
    "NG-PERSON-000268": "Sule Ahmed Abdulaziz",
    "NG-PERSON-000281": "Nasir Naeem Abdulsalam",
    "NG-PERSON-000311": "Olakunle Alake",
    "NG-PERSON-000312": "Devakumar Edwin",
    "NG-PERSON-000163": "Busayo Fakinlede",
    "NG-PERSON-000172": "Nneka Anibeze",
    "NG-PERSON-000183": "Mariya Mahmoud Bunkure",
    "NG-PERSON-000185": "Richard Yunana Dauda",
}

def curl_json(url):
    r = subprocess.run(
        ["curl", "-s", "-x", PROXY, "-A", UA, "--max-time", "40", url],
        capture_output=True)
    return r.stdout.decode("utf-8", "replace")

results = {}
# batch query in groups of 10
items = list(TITLES.items())
for i in range(0, len(items), 10):
    group = items[i:i+10]
    titles = "|".join(t for _, t in group)
    url = ("https://en.wikipedia.org/w/api.php?action=query&prop=pageimages"
           "&piprop=original|name&format=json&redirects=1&titles=%s" % urllib.parse.quote(titles))
    raw = curl_json(url)
    try:
        d = json.loads(raw)
        pages = d.get("query", {}).get("pages", {})
        for pid_, pg in pages.items():
            img = pg.get("original", {}).get("source")
            # map back by title
            t = pg.get("title", "")
            for pid, name in group:
                if name.lower() == t.lower():
                    results[pid] = {"title": t, "image": img}
    except Exception as e:
        print("batch error:", e)
    time.sleep(2)

for pid in TITLES:
    r = results.get(pid)
    print(pid, TITLES[pid], "=>", (r or {}).get("image", "NO IMAGE"))

with open(os.path.join(BASE, "scripts_tmp", "_a1_wiki_images.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)

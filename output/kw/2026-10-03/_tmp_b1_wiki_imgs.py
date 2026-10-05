# -*- coding: utf-8 -*-
"""Batch 1 helper: query en/ar Wikipedia search+pageimages for person portraits."""
import json, time, urllib.parse, subprocess

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 OsintResearch/1.0"

# pid, query_en, query_ar
PEOPLE = [
    ("000004", "Imad Al-Atiqi Kuwait", "عماد العتيقي"),
    ("000005", "Badah Al-Mutairi Kuwait", "عبدالرحمن بدر المطيري"),
    ("000007", "Bandar Al-Khairan", "بندر الخيران"),
    ("000009", "Mohammad Al-Olaim Kuwait", "محمد العليم"),
    ("000010", "Khaled Sultan bin Essa", "خالد سلطان بن عيسى"),
    ("000013", "Bader Al-Dahoum", "بدر الداهوم"),
    ("000014", "Ahmad Al-Deyain Kuwait", "أحمد الديين"),
    ("000015", "Bader Nasser Al-Kharafi", "بدر ناصر الخرافي"),
    ("000018", "Mubarak Faisal Al-Sabah", "مبارك الفيصل السعود الصباح"),
    ("000019", "Abdulaziz Mishal Al-Sabah Amiri Diwan", "عبدالعزيز مشعل مبارك الصباح"),
    ("000020", "Jamal Al-Dhiyab Kuwait", "جمال محمد الذياب"),
    ("000021", "Shereeda Al-Mousherji", "شريدة المعوشرجي"),
    ("000023", "Abdullah Ali Abdullah Al-Sabah", "عبدالله علي عبدالله السالم الصباح"),
    ("000024", "Yaqoub Al-Rifai Kuwait finance", "يعقوب الرفاعي"),
    ("000025", "Tarek Al-Roumi", "طارق الرومي"),
    ("000027", "Khaled Al-Bouslaib", "خالد بوصليب"),
    ("000028", "Abdulwahab Al-Wuhaib", "عبدالوهاب الوهيب"),
    ("000030", "Nasser Al-Sumait", "ناصر السميط"),
    ("000031", "Awatif Al-Sanad", "عواطف السند"),
    ("000032", "Abdullah Mishal Al-Sabah", "عبدالله مشعل مبارك الصباح"),
    ("000033", "Bandar Al-Muzayen", "بندر المزين"),
    ("000034", "Sabah Jaber Al-Ahmad Al-Sabah", "صباح جابر الأحمد الصباح"),
    ("000035", "Wael Al-Sabah defence", "وائل ناصر حمود الصباح"),
    ("000036", "Anoud Al-Turaiman", "عنود الطريمان"),
    ("000037", "Aseel Al-Munaifi", "أسيل المنيفي"),
]

def api(host, params):
    url = "https://%s/w/api.php?%s" % (host, urllib.parse.urlencode(params))
    try:
        out = subprocess.run(
            ["curl", "-s", "-m", "25", "-x", PROXY, "-A", UA, url],
            capture_output=True, text=True, timeout=40).stdout
        return json.loads(out)
    except Exception as e:
        return {"_err": str(e)}

for pid, qen, qar in PEOPLE:
    row = {"pid": pid}
    for lang, q in (("en", qen), ("ar", qar)):
        d = api(lang + ".wikipedia.org", {
            "action": "query", "format": "json",
            "generator": "search", "gsrsearch": q, "gsrlimit": "2",
            "gsrnamespace": "0",
            "prop": "pageimages", "piprop": "original", "pilicense": "any"})
        hits = []
        for p in (d.get("query", {}) or {}).get("pages", {}).values():
            img = (p.get("original") or {}).get("source", "")
            hits.append([p.get("title"), img])
        row[lang] = hits
        time.sleep(1.5)
    print(json.dumps(row, ensure_ascii=False))

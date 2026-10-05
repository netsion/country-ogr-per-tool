# -*- coding: utf-8 -*-
"""Batch 1 helper: search Commons File namespace for person photos."""
import json, time, urllib.parse, subprocess

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 OsintResearch/1.0"

PEOPLE = [
    ("000004", "عماد العتيقي", "Imad Al-Atiqi"),
    ("000005", "بدر المطيري الكويت", "Badah Al-Mutairi"),
    ("000007", "بندر الخيران", "Bandar Al-Khairan"),
    ("000009", "محمد العليم الكويت", "Mohammad Al-Olaim"),
    ("000010", "خالد سلطان بن عيسى", "Khaled Sultan bin Essa"),
    ("000013", "بدر الداهوم", "Bader Al-Dahoum"),
    ("000014", "أحمد الديين", "Ahmad Al-Deyain"),
    ("000018", "مبارك الفيصل الصباح", "Mubarak Faisal Al-Sabah"),
    ("000019", "عبدالعزيز مشعل الصباح", "Abdulaziz Mishal Al-Sabah"),
    ("000020", "جمال الذياب", "Jamal Al-Dhiyab"),
    ("000021", "شريدة المعوشرجي", "Shereeda Al-Mousherji"),
    ("000023", "عبدالله علي الصباح وزير الدفاع", "Abdullah Ali Al-Sabah Kuwait"),
    ("000024", "يعقوب الرفاعي الكويت", "Yaqoub Al-Rifai"),
    ("000025", "طارق الرومي الكويت", "Tarek Al-Roumi"),
    ("000027", "خالد بوصليب", "Khaled Al-Bouslaib"),
    ("000028", "عبدالوهاب الوهيب", "Abdulwahab Al-Wuhaib"),
    ("000030", "ناصر السميط", "Nasser Al-Sumait"),
    ("000031", "عواطف السند", "Awatif Al-Sanad"),
    ("000032", "عبدالله مشعل الصباح", "Abdullah Mishal Al-Sabah"),
    ("000033", "بندر المزين", "Bandar Al-Muzayen"),
    ("000034", "صباح جابر الأحمد الصباح", "Sabah Jaber Al-Ahmad Al-Sabah"),
    ("000035", "وائل الصباح الدفاع", "Wael Nasser Al-Sabah"),
    ("000036", "عنود الطريمان", "Anoud Al-Turaiman"),
    ("000037", "أسيل المنيفي", "Aseel Al-Munaifi"),
]

def api(params):
    url = "https://commons.wikimedia.org/w/api.php?%s" % urllib.parse.urlencode(params)
    try:
        out = subprocess.run(
            ["curl", "-s", "-m", "25", "-x", PROXY, "-A", UA, url],
            capture_output=True, text=True, timeout=40).stdout
        return json.loads(out)
    except Exception as e:
        return {"_err": str(e)}

for pid, qar, qen in PEOPLE:
    row = {"pid": pid}
    for tag, q in (("ar", qar), ("en", qen)):
        d = api({
            "action": "query", "format": "json",
            "generator": "search", "gsrsearch": q, "gsrlimit": "4",
            "gsrnamespace": "6",
            "prop": "imageinfo", "iiprop": "url", "iiurlwidth": "400"})
        hits = []
        for p in (d.get("query", {}) or {}).get("pages", {}).values():
            ii = (p.get("imageinfo") or [{}])[0]
            hits.append([p.get("title"), ii.get("thumburl", "")])
        row[tag] = hits
        time.sleep(1.5)
    print(json.dumps(row, ensure_ascii=False))

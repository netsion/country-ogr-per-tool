# -*- coding: utf-8 -*-
import io, json, sys, time
import urllib.request, urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PROXY = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
opener = urllib.request.build_opener(urllib.request.ProxyHandler(PROXY))
opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) osint-research/1.0")]

TITLES = {
    "KW-PERSON-000056": "أحمد عبد الوهاب العوضي",
    "KW-PERSON-000059": "جلال عبدالمحسن الطبطبائي",
    "KW-PERSON-000051": "محمد إبراهيم الوسمي",
    "KW-PERSON-000049": "أمثال الحويلة",
}

for pid, t in TITLES.items():
    ok = False
    for attempt in range(3):
        try:
            url = "https://ar.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
                "action": "query", "titles": t, "prop": "pageimages",
                "piprop": "thumbnail|original", "pithumbsize": "400",
                "format": "json", "redirects": "1",
            })
            with opener.open(url, timeout=30) as r:
                d = json.loads(r.read().decode("utf-8"))
            for _, pg in d["query"]["pages"].items():
                th = (pg.get("thumbnail") or {}).get("source")
                og = (pg.get("original") or {}).get("source") if pg.get("original") else None
                print(pid, "|", pg.get("title"), "| thumb:", th, "| orig:", og)
            ok = True
            break
        except Exception as e:
            print(pid, "attempt", attempt + 1, "err:", e)
            time.sleep(12)
    if not ok:
        print(pid, "FAILED")
    time.sleep(4)

# -*- coding: utf-8 -*-
"""B2 batch: check pageimages for arwiki/enwiki titles + social/wiki metadata."""
import io, json, sys, time
import urllib.request, urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PROXY = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
opener = urllib.request.build_opener(urllib.request.ProxyHandler(PROXY))
opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) osint-research/1.0")]


def get(url, params=None):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    with opener.open(url, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


AR_TITLES = {
    "KW-PERSON-000045": "حمد روح الدين",
    "KW-PERSON-000051": "محمد إبراهيم الوسمي",
    "KW-PERSON-000054": "فهد العفاسي",
    "KW-PERSON-000056": "أحمد عبد الوهاب العوضي",
    "KW-PERSON-000059": "جلال عبدالمحسن الطبطبائي",
    "KW-PERSON-000066": "عبد اللطيف المشاري",
    "KW-PERSON-000038": "عبدالعزيز ناصر المرزوق",
    "KW-PERSON-000042": "عمر سعود العمر",
    "KW-PERSON-000041": "علي الخليفة العذبي الصباح",
}
EN_TITLES = {
    "KW-PERSON-000041": "Ali Al-Khalifa Al-Sabah",
    "KW-PERSON-000056": "Ahmad Abdulwahab Al-Awadhi",
}

results = {}

def fetch_batch(api, titles, tag):
    # one request per title, with retry/backoff to survive 429
    out = {}
    for t in titles:
        d = None
        for attempt in range(4):
            try:
                d = get(api, {
                    "action": "query", "titles": t,
                    "prop": "pageimages", "piprop": "thumbnail|original",
                    "pithumbsize": "400", "format": "json", "redirects": "1",
                })
                break
            except Exception as e:
                print(f"{tag} '{t}' attempt{attempt+1} error: {e}")
                time.sleep(15 * (attempt + 1))
        if d is None:
            out[t] = "FAILED"
            continue
        for pid, pg in d["query"]["pages"].items():
            if "missing" in pg:
                out[t] = None
            else:
                out[t] = {
                    "thumb": (pg.get("thumbnail") or {}).get("source"),
                    "original": pg.get("original", {}).get("source") if pg.get("original") else None,
                }
        time.sleep(4)
    return out

ar_res = fetch_batch("https://ar.wikipedia.org/w/api.php", list(AR_TITLES.values()), "arwiki")
time.sleep(10)
en_res = fetch_batch("https://en.wikipedia.org/w/api.php", list(EN_TITLES.values()), "enwiki")

print("=== arwiki ===")
for pid, t in AR_TITLES.items():
    r = ar_res.get(t, "TITLE_NOT_IN_RESPONSE")
    print(pid, "|", t, "|", json.dumps(r, ensure_ascii=False) if r else r)
print("=== enwiki ===")
for pid, t in EN_TITLES.items():
    r = en_res.get(t, "TITLE_NOT_IN_RESPONSE")
    print(pid, "|", t, "|", json.dumps(r, ensure_ascii=False) if r else r)

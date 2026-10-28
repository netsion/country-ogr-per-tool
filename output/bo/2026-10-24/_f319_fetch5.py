# -*- coding: utf-8 -*-
"""Round 5: full reads of La Patria articles (appointment, anniversary, fair, necrologicas)."""
import re
import gzip
import io
import urllib.request

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def fetch(url, timeout=45):
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    opener.addheaders = [("User-Agent", UA), ("Accept-Language", "es,en;q=0.8")]
    try:
        resp = opener.open(url, timeout=timeout)
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
        return raw.decode("utf-8", "replace")
    except Exception as e:
        return "FETCH_ERROR: %s" % e


def totext(html):
    if html.startswith("FETCH_ERROR"):
        return html
    html = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"<[^>]+>", " ", html)
    for a, b in [("&nbsp;", " "), ("&amp;", "&"), ("&quot;", '"'), ("&#8220;", '"'),
                 ("&#8221;", '"'), ("&#8216;", "'"), ("&#8217;", "'"), ("&laquo;", "«"),
                 ("&raquo;", "»"), ("&#8211;", "-"), ("&#8212;", "-"), ("&#8230;", "...")]:
        text = text.replace(a, b)
    return re.sub(r"\s+", " ", text)


URLS = [
    ("appt", "https://lapatria.bo/actualidad/carlos-flores-se-convierte-en-nuevo-decano-de-la-fni/", r"[Ff]lores"),
    ("aniv", "https://lapatria.bo/enfoque-nacional/regiones/ingenieros-oruro-fni-reafirma-liderazgo/", r"[Ff]lores"),
    ("fair", "https://lapatria.bo/enfoque-nacional/gestion/inauguran-fimem-ficon-fegac-campo-ferial-julio/", r"[Ff]lores"),
    ("necro1", "https://lapatria.bo/avisos/necrologicos/condolencia-m-sc-ing-hugo-edmundo-zavaleta-loayza-q-e-p-d-2/", r"[Ff]lores"),
    ("necro2", "https://lapatria.bo/avisos/necrologicos/condolencia-ing-alvaro-rolando-bellota-cespedes-q-e-p-d/", r"[Ff]lores"),
]

for tag, url, pat in URLS:
    html = fetch(url)
    name = "_f319_lapatria_%s.html" % tag
    if not html.startswith("FETCH_ERROR"):
        with open(name, "w", encoding="utf-8") as f:
            f.write(html)
    text = totext(html)
    print("=====", tag, url)
    if text.startswith("FETCH_ERROR"):
        print(text)
        continue
    print("LEN:", len(text))
    # article body: find date marker
    idxs = [m.start() for m in re.finditer(pat, text)]
    if idxs:
        # print around each occurrence, first 6
        shown = set()
        for i in idxs[:6]:
            s = max(0, i - 700)
            e = min(len(text), i + 700)
            key = s // 500
            if key in shown:
                continue
            shown.add(key)
            print("  [CTX]...", text[s:e], "...")
    else:
        print("  NO MATCH; head:", text[:1500])

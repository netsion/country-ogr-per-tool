# -*- coding: utf-8 -*-
"""Round 4: La Patria article URLs + fetch articles; Wayback CDX for FNI authorities."""
import re
import gzip
import io
import json
import urllib.request
import urllib.parse

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


# 1. La Patria search page: extract article links with titles
html = fetch('https://lapatria.bo/?s=%22Flores+Castillo%22')
items = re.findall(r'<a[^>]+href="(https://lapatria\.bo/[^"]+)"[^>]*>([^<]{5,120})</a>', html)
seen = set()
print("=== La Patria search links ===")
for u, t in items:
    t = t.strip()
    if u not in seen and u.count("/") >= 3 and not any(x in u for x in ["categoria", "tag", "author", "page", "#", "autor", "seccion"]):
        seen.add(u)
        print(t[:80], "|", u)

# 2. Wayback CDX: UTO FNI pages over time
print()
print("=== Wayback CDX: uto.edu.bo FNI pages ===")
for q in ["uto.edu.bo/*facultad-nacional-de-ingenieria*", "uto.edu.bo/facultad-nacional-de-ingenieria/*"]:
    u = "http://web.archive.org/cdx/search/cdx?url=%s&output=json&fl=timestamp,original,statuscode&collapse=digest&limit=60" % urllib.parse.quote(q, safe="")
    r = fetch(u)
    print("Q:", q)
    if r.startswith("FETCH_ERROR"):
        print(" ", r)
        continue
    try:
        rows = json.loads(r)
        for row in rows[1:]:
            print(" ", row)
    except Exception as e:
        print("  parse fail:", r[:300])

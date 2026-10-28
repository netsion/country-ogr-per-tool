# -*- coding: utf-8 -*-
"""Round 7: portrait download; Wayback snapshots; old-site search; social scan."""
import re
import gzip
import io
import json
import urllib.request
import urllib.parse

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def fetch_bytes(url, timeout=60):
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    opener.addheaders = [("User-Agent", UA)]
    try:
        resp = opener.open(url, timeout=timeout)
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
        return raw
    except Exception as e:
        return b"FETCH_ERROR: %s" % str(e).encode()


def fetch(url, timeout=60):
    r = fetch_bytes(url, timeout)
    if r.startswith(b"FETCH_ERROR"):
        return r.decode("utf-8", "replace")
    return r.decode("utf-8", "replace")


# 1. Portrait download
img = fetch_bytes("https://www.uto.edu.bo/wp-content/uploads/2026/09/M.Sc_.-Ing.-Carlos-Antonio-Flores-Castillo.jpg")
if img.startswith(b"FETCH_ERROR"):
    print("IMG ERROR:", img[:200])
else:
    with open("photos/BO-PERSON-000319.jpg", "wb") as f:
        f.write(img)
    print("IMG saved:", len(img), "bytes, magic:", img[:4].hex())

# 2. Wayback snapshot 2026-04-23 of FNI page
h = fetch("https://web.archive.org/web/20260423235117/https://www.uto.edu.bo/facultad-nacional-de-ingenieria/")
print()
print("=== Wayback 2026-04-23 FNI page ===")
if h.startswith("FETCH_ERROR"):
    print(h)
else:
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t)
    i = t.find("AUTORIDADES")
    print(t[i:i + 400] if i > 0 else "no AUTORIDADES block; len=%d" % len(t))
    j = t.find("DECANO")
    print("DECANO ctx:", t[max(0, j - 100):j + 300] if j > 0 else "none")

# 3. CDX old site pages with 'ingenieria' in URL (2020-2025)
print()
print("=== CDX domain filter ingenieria (2020-2025) ===")
u = ("http://web.archive.org/cdx/search/cdx?url=uto.edu.bo&matchType=domain"
     "&filter=original:.*[Ii]ngenieria.*&filter=statuscode:200&collapse=urlkey"
     "&fl=timestamp,original&from=2020&to=2026&limit=80&output=json")
r = fetch(u)
if r.startswith("FETCH_ERROR"):
    print(r)
else:
    try:
        rows = json.loads(r)
        for row in rows[1:]:
            print(" ", row)
    except Exception:
        print("parse fail:", r[:300])

# 4. Social scan via Bing
print()
print("=== Social scan (Bing) ===")
QUERIES = [
    '"Carlos Antonio Flores Castillo" site:facebook.com',
    '"Carlos Antonio Flores Castillo" OR "Carlos Flores Castillo" UTO site:linkedin.com',
    '"Carlos Antonio Flores Castillo" site:instagram.com',
    '"Carlos Antonio Flores Castillo" site:tiktok.com',
    '"Carlos Antonio Flores Castillo" (site:twitter.com OR site:x.com)',
    '"Carlos Antonio Flores Castillo" site:youtube.com',
]
for q in QUERIES:
    u = "https://www.bing.com/search?q=" + urllib.parse.quote(q) + "&setlang=es"
    r = fetch(u)
    print("Q:", q)
    if r.startswith("FETCH_ERROR"):
        print("  ", r)
        continue
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", r)
    # extract result links
    links = re.findall(r'<h2><a href="(http[^"]+)"[^>]*>(.*?)</a></h2>', t)
    if not links:
        t2 = re.sub(r"<[^>]+>", " ", t)
        t2 = re.sub(r"\s+", " ", t2)
        print("   no h2 links; page head:", t2[t2.find("results"):t2.find("results") + 300] if "results" in t2 else t2[:300])
    for link, title in links[:6]:
        title = re.sub(r"<[^>]+>", "", title)
        print("   -", title[:90], "|", link[:120])

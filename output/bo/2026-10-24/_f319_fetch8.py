# -*- coding: utf-8 -*-
"""Round 8: FNI old-site Wayback timeline; May snapshot; better social extraction."""
import re
import gzip
import io
import json
import urllib.request
import urllib.parse

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def fetch(url, timeout=60):
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


def clean(html):
    html = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
    t = re.sub(r"<[^>]+>", " ", html)
    for a, b in [("&nbsp;", " "), ("&amp;", "&"), ("&quot;", '"'), ("&#8220;", '"'),
                 ("&#8221;", '"'), ("&#8217;", "'"), ("&#8211;", "-"), ("&#225;", "á"),
                 ("&#233;", "é"), ("&#237;", "í"), ("&#243;", "ó"), ("&#250;", "ú"),
                 ("&#241;", "ñ")]:
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)


# 1. CDX for fni.uto.edu.bo homepage snapshots
print("=== CDX fni.uto.edu.bo homepage ===")
u = ("http://web.archive.org/cdx/search/cdx?url=fni.uto.edu.bo/&output=json"
     "&fl=timestamp,original,statuscode&collapse=timestamp:6&limit=40")
r = fetch(u)
snaps = []
if not r.startswith("FETCH_ERROR"):
    try:
        rows = json.loads(r)
        for row in rows[1:]:
            print(" ", row)
            snaps.append(row[0])
    except Exception:
        print("parse fail", r[:300])
else:
    print(r)

# 2. Grep decano in a few key snapshots of fni.uto.edu.bo
for ts in snaps:
    if ts[:4] in ("2021", "2022", "2023", "2024", "2025"):
        h = fetch("https://web.archive.org/web/%s/http://www.fni.uto.edu.bo/" % ts)
        print("--- snapshot", ts)
        if h.startswith("FETCH_ERROR"):
            print("   ", h)
            continue
        t = clean(h)
        for pat in [r"[Dd]ecano[^.]{0,160}", r"[Ff]lores [Cc]astillo[^.]{0,120}", r"[Aa]liendre[^.]{0,120}"]:
            hits = re.findall(pat, t)
            uniq = []
            for x in hits:
                if x not in uniq:
                    uniq.append(x)
            for x in uniq[:4]:
                print("   [%s] %s" % (pat[:8], x.strip()[:150]))

# 3. Wayback 2026-05-13 snapshot of new FNI page (confirm update to Flores)
print()
print("=== Wayback 2026-05-13 FNI page ===")
h = fetch("https://web.archive.org/web/20260513162939/https://www.uto.edu.bo/facultad-nacional-de-ingenieria/")
if h.startswith("FETCH_ERROR"):
    print(h)
else:
    t = clean(h)
    i = t.find("AUTORIDADES")
    print(t[i:i + 260] if i > 0 else "no block")

# 4. Social scan with better extraction (Bing b_algo links)
print()
print("=== Social scan v2 (Bing) ===")
QUERIES = [
    '"Carlos Antonio Flores Castillo" facebook',
    '"Carlos Flores Castillo" UTO linkedin',
    '"Carlos Antonio Flores Castillo" instagram',
    '"Carlos Antonio Flores Castillo" tiktok',
    '"Carlos Antonio Flores Castillo" twitter',
    '"Carlos Antonio Flores Castillo" youtube',
    '"Carlos Antonio Flores Castillo"',
]
for q in QUERIES:
    u = "https://www.bing.com/search?q=" + urllib.parse.quote(q) + "&setlang=es&count=20"
    r = fetch(u)
    print("Q:", q)
    if r.startswith("FETCH_ERROR"):
        print("   ", r)
        continue
    # b_algo blocks
    blocks = re.findall(r'<li class="b_algo".*?</li>', r, re.S)
    if not blocks:
        t = clean(r)
        i = t.lower().find("resultados")
        print("   no b_algo; text sample:", t[max(0, i - 50):i + 400])
    for b in blocks[:7]:
        m = re.search(r'href="(http[^"]+)"', b)
        t = clean(b)
        if m:
            print("   -", t[:110], "||", m.group(1)[:130])

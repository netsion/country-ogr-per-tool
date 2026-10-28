# -*- coding: utf-8 -*-
"""Round 9: La Patria election-history queries; GN RSS variants; Mojeek/DDG-lite social scan."""
import re
import gzip
import io
import time
import urllib.request
import urllib.parse

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def fetch(url, timeout=50):
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
                 ("&#8221;", '"'), ("&#8217;", "'"), ("&laquo;", "«"), ("&raquo;", "»"),
                 ("&#8211;", "-"), ("&#8230;", "...")]:
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)


# 1. La Patria queries on decano history
for q in ["FNI+elecciones+decano", "Aliendre+decano", "nuevo+decano+de+la+FNI", "Flores+decano+ingenieria+2021"]:
    u = "https://lapatria.bo/?s=" + q
    h = fetch(u)
    print("=== LA PATRIA [%s] ===" % q)
    if h.startswith("FETCH_ERROR"):
        print("  ", h)
        continue
    items = re.findall(r'<a[^>]+href="(https://lapatria\.bo/[^"]+)"[^>]*>([^<]{5,120})</a>', h)
    seen = set()
    for link, title in items:
        title = title.strip()
        if link not in seen and link.count("/") >= 3 and not any(x in link for x in ["categoria", "tag", "author", "page/", "autor", "seccion", "#"]):
            seen.add(link)
            # only print items whose title looks relevant
            if any(k in (title + link).lower() for k in ["fni", "decano", "flores", "aliendre", "ingenier"]):
                print("  *", title[:90], "|", link)
    time.sleep(1)

# 2. Google News RSS variants
print()
for q in ["decano Facultad Nacional de Ingeniería Oruro", "FNI UTO decano",
          "Aliendre García FNI", '"Facultad Nacional de Ingeniería" UTO']:
    u = "https://news.google.com/rss/search?q=" + urllib.parse.quote(q) + "&hl=es-419&gl=BO&ceid=BO:es-419"
    xml = fetch(u)
    print("GN-RSS [%s]:" % q)
    if xml.startswith("FETCH_ERROR"):
        print("  ", xml)
        continue
    items = re.findall(r"<item><title>(.*?)</title><link>(.*?)</link>.*?<pubDate>(.*?)</pubDate>", xml, re.S)
    for title, link, date in items[:6]:
        print("  *", date, "|", title)
    time.sleep(1)

# 3. Social scan via Mojeek and DDG lite
print()
for engine, base in [("MOJEEK", "https://www.mojeek.com/search?q="), ("DDGLITE", "https://lite.duckduckgo.com/lite/?q=")]:
    for q in ['"Carlos Antonio Flores Castillo"',
              '"Carlos Flores Castillo" UTO ingeniería',
              '"Carlos Antonio Flores Castillo" facebook OR linkedin OR instagram OR tiktok OR twitter OR youtube']:
        u = base + urllib.parse.quote(q)
        h = fetch(u)
        print("=== %s [%s] ===" % (engine, q))
        if h.startswith("FETCH_ERROR"):
            print("  ", h)
            continue
        if engine == "MOJEEK":
            results = re.findall(r'<a class="title[^"]*" href="(http[^"]+)"[^>]*>(.*?)</a>', h, re.S)
            if not results:
                results = re.findall(r'<h2><a href="(http[^"]+)"[^>]*>(.*?)</a>', h, re.S)
            if not results:
                t = clean(h)
                print("   raw sample:", t[:400])
            for link, title in results[:8]:
                print("   -", re.sub(r"<[^>]+>", "", title)[:90], "|", link[:120])
        else:
            t = clean(h)
            links = re.findall(r'href="(http[^"]+)"[^>]*>', h)
            links = [l for l in links if "duckduckgo" not in l][:8]
            if links:
                for l in links:
                    print("   -", l[:130])
            else:
                print("   raw sample:", t[:400])
        time.sleep(1)

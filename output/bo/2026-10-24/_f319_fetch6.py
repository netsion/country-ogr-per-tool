# -*- coding: utf-8 -*-
"""Round 6: FNI page photo/contacts; Wayback old-site FNI; Wikidata; social scan prep."""
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


# 1. FNI page: save, look for images and contact info
html = fetch("https://www.uto.edu.bo/facultad-nacional-de-ingenieria/")
if not html.startswith("FETCH_ERROR"):
    with open("_f319_fni_page.html", "w", encoding="utf-8") as f:
        f.write(html)
    # images with alt/src
    print("=== FNI page images ===")
    for m in re.finditer(r'<img[^>]+>', html, re.I):
        tag = m.group(0)
        alt = re.search(r'alt="([^"]*)"', tag, re.I)
        src = re.search(r'src="([^"]*)"', tag, re.I)
        if alt and src and ("decano" in (alt.group(1) or "").lower() or "flores" in (alt.group(1) or "").lower()
                            or "autoridad" in (alt.group(1) or "").lower() or "ing" in (alt.group(1) or "").lower()):
            print("  ALT:", alt.group(1), "| SRC:", src.group(1))
    text = totext(html)
    i = text.find("AUTORIDADES")
    if i > 0:
        print("=== AUTORIDADES block ===")
        print(text[i:i + 900])
    j = text.find("Contactos")
    if j > 0:
        print("=== Contactos block ===")
        print(text[j:j + 700])
    # phone/email regex on raw html
    print("=== phones/emails ===")
    print(sorted(set(re.findall(r'[\w.+-]+@[\w.-]+\.\w+', html)))[:20])
    print(sorted(set(re.findall(r'\(591\)[^A-Za-z<]{5,25}', html)))[:20])
else:
    print("FNI page fetch error:", html)

# 2. Wayback CDX old UTO site FNI pages
print()
print("=== Wayback CDX old site ===")
for q in ["www.uto.edu.bo/index.php/facultad-nacional-de-ingenieria",
          "www.uto.edu.bo/facultad-nacional-de-ingenieria"]:
    u = "http://web.archive.org/cdx/search/cdx?url=%s&output=json&fl=timestamp,original,statuscode&collapse=digest&limit=40" % urllib.parse.quote(q, safe="")
    r = fetch(u)
    print("Q:", q, "->", (r[:600] if not r.startswith("FETCH_ERROR") else r))

# 3. Wikidata search
print()
print("=== Wikidata ===")
for q in ["Carlos Antonio Flores Castillo", "Carlos Flores Castillo"]:
    u = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=%s&language=es&format=json&limit=5" % urllib.parse.quote(q)
    r = fetch(u)
    if r.startswith("FETCH_ERROR"):
        print(q, r)
        continue
    try:
        d = json.loads(r)
        hits = [(x["id"], x.get("label"), x.get("description")) for x in d.get("search", [])]
        print(q, "->", hits if hits else "no results")
    except Exception:
        print(q, "parse fail", r[:200])

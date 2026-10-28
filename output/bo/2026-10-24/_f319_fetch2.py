# -*- coding: utf-8 -*-
"""Round 2: extract URLs from UTO search page; fetch FNI site (no SSL verify); more searches."""
import re
import ssl
import gzip
import io
import urllib.request

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
NOSSL = ssl._create_unverified_context()


def fetch(url, timeout=45, noverify=False):
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    if noverify:
        opener.add_handler(urllib.request.HTTPSHandler(context=NOSSL))
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
                 ("&raquo;", "»"), ("&#8211;", "-"), ("&aacute;", "á"), ("&eacute;", "é"),
                 ("&iacute;", "í"), ("&oacute;", "ó"), ("&uacute;", "ú"), ("&ntilde;", "ñ")]:
        text = text.replace(a, b)
    return re.sub(r"\s+", " ", text)


# 1. Extract article links from UTO search results
html = fetch("https://www.uto.edu.bo/?s=%22Flores+Castillo%22")
links = re.findall(r'href="(https://www\.uto\.edu\.bo/[^"]+)"[^>]*>', html)
seen = set()
print("=== UTO search-page article links ===")
for u in links:
    if u not in seen and not any(x in u for x in ["wp-content", "wp-json", "#", "feed", "xmlrpc", "?s="]):
        seen.add(u)
        print(u)

print()
print("=== UTO search: Carlos Antonio Flores ===")
html2 = fetch("https://www.uto.edu.bo/?s=%22Carlos+Antonio+Flores%22")
links2 = re.findall(r'href="(https://www\.uto\.edu\.bo/[^"]+)"[^>]*>', html2)
seen2 = set()
for u in links2:
    if u not in seen2 and not any(x in u for x in ["wp-content", "wp-json", "#", "feed", "xmlrpc", "?s="]):
        seen2.add(u)
        print(u)
text2 = totext(html2)
m = re.search(r"Resultados de búsqueda para(.*?)Comentarios|Entradas recientes", text2)
if m:
    print("SEARCH TEXT:", text2[m.start():m.start() + 3500])

print()
print("=== FNI site (noverify) ===")
t = totext(fetch("https://fni.uto.edu.bo/", noverify=True))
print(t[:3000])

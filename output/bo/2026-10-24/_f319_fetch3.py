# -*- coding: utf-8 -*-
"""Round 3: full reads of UTO FNI articles + La Patria + Google News RSS + fni.uto.edu.bo http."""
import re
import gzip
import io
import urllib.request
import urllib.parse

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def fetch(url, timeout=45, use_proxy=True):
    handlers = []
    if use_proxy:
        handlers.append(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    opener = urllib.request.build_opener(*handlers)
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


def article(url, save=None, anchor=None):
    html = fetch(url)
    if save and not html.startswith("FETCH_ERROR"):
        with open(save, "w", encoding="utf-8") as f:
            f.write(html)
    text = totext(html)
    print("URL:", url)
    if text.startswith("FETCH_ERROR"):
        print(text)
        return
    # print main content: from title marker to comments/footer
    idx = text.find("UNIVERSIDAD TECNICA DE ORURO")
    seg = text[idx:idx + 6000] if idx >= 0 else text[:6000]
    if anchor:
        for m in re.finditer(anchor, text, re.I):
            s = max(0, m.start() - 400)
            print("  [CTX]...", text[s:m.end() + 400], "...")
    print(seg[:5500])
    print("-" * 100)


# 1. ARCU-SUR MERCOSUR accreditation article (2026-05-22)
article("https://www.uto.edu.bo/siete-carreras-de-la-fni-recibiran-su-certificacion-homologada-de-acreditacion-internacional-al-mercosur-en-el-congreso-de-universidades/",
        save="_f319_mercosur.html")
# 2. FNI CXX aniversario article
article("https://www.uto.edu.bo/con-la-solemne-iza-de-las-banderas-y-un-acto-academico-la-fni-conmemora-su-cxx-aniversario-de-gloria-y-excelencia/",
        save="_f319_cxx.html")
# 3. La Patria search
t = totext(fetch("https://lapatria.bo/?s=%22Flores+Castillo%22"))
print("LA PATRIA SEARCH:", t[:3000])
print("-" * 100)
# 4. Google News RSS
for q in ['"Carlos Flores Castillo" UTO', '"Carlos Antonio Flores Castillo"',
          'Flores Castillo decano FNI Oruro', '"Flores Castillo" Ingeniería Oruro']:
    u = "https://news.google.com/rss/search?q=" + urllib.parse.quote(q) + "&hl=es-419&gl=BO&ceid=BO:es-419"
    xml = fetch(u)
    print("GN-RSS [%s]:" % q)
    if xml.startswith("FETCH_ERROR"):
        print(" ", xml)
    else:
        items = re.findall(r"<item><title>(.*?)</title><link>(.*?)</link>.*?<pubDate>(.*?)</pubDate>", xml, re.S)
        if not items:
            print("  (no items)", xml[:200])
        for title, link, date in items[:8]:
            print("  *", date, "|", title)
    print("-" * 60)
# 5. fni.uto.edu.bo plain http
t = totext(fetch("http://fni.uto.edu.bo/"))
print("FNI HTTP:", t[:2000])

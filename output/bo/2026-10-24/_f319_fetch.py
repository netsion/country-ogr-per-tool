# -*- coding: utf-8 -*-
"""Fetch helper for BO-PERSON-000319 (Carlos Flores Castillo, Decano FNI UTO)."""
import re
import sys
import gzip
import io
import urllib.request
import urllib.error

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def fetch(url, timeout=45, use_proxy=True, referer=None):
    handlers = []
    if use_proxy:
        handlers.append(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    opener = urllib.request.build_opener(*handlers)
    headers = [("User-Agent", UA), ("Accept-Language", "es,en;q=0.8")]
    if referer:
        headers.append(("Referer", referer))
    opener.addheaders = headers
    try:
        resp = opener.open(url, timeout=timeout)
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
        charset = "utf-8"
        ct = resp.headers.get("Content-Type", "")
        m = re.search(r"charset=([\w-]+)", ct)
        if m:
            charset = m.group(1)
        return raw.decode(charset, "replace")
    except Exception as e:
        return "FETCH_ERROR: %s" % e


def totext(html):
    if html.startswith("FETCH_ERROR"):
        return html
    html = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&#8220;|&#8221;", '"', text)
    text = re.sub(r"&#8216;|&#8217;", "'", text)
    text = re.sub(r"\s+", " ", text)
    return text


def show(url, patterns=None, maxchars=4000, ctx=300):
    html = fetch(url)
    print("URL:", url)
    if html.startswith("FETCH_ERROR"):
        print(html)
        return
    text = totext(html)
    print("LEN:", len(text))
    if patterns:
        for pat in patterns:
            found = False
            for m in re.finditer(pat, text, re.I):
                found = True
                s = max(0, m.start() - ctx)
                e = min(len(text), m.end() + ctx)
                print("  [CTX %s] ...%s..." % (pat, text[s:e]))
            if not found:
                print("  [MISS %s]" % pat)
    else:
        print(text[:maxchars])


if __name__ == "__main__":
    # 1. UTO site search for Flores Castillo
    show("https://www.uto.edu.bo/?s=%22Flores+Castillo%22", patterns=[r"[Ff]lores\s+[Cc]astillo"], maxchars=3000)
    print("=" * 100)
    # 2. UTO FNI category / faculty page
    show("https://www.uto.edu.bo/facultad-nacional-de-ingenieria/", patterns=[r"[Dd]ecano", r"[Ff]lores"], maxchars=2500)
    print("=" * 100)
    # 3. FNI own website guess
    show("https://fni.uto.edu.bo/", patterns=[r"[Dd]ecano", r"[Ff]lores"], maxchars=2500)

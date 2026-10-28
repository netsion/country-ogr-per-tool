# -*- coding: utf-8 -*-
"""Bing SERP fetch + extract helper for Sergio Criales research."""
import re
import html
import sys
import urllib.parse
import subprocess

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def fetch(url, out):
    subprocess.run(
        ["curl", "-s", "-L", "-m", "50", "-x", PROXY, "-A", UA, url, "-o", out],
        check=False,
    )
    try:
        with open(out, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def extract(html_text, max_n=15):
    results = []
    # Bing organic results live in <li class="b_algo"> blocks
    blocks = re.findall(r'<li class="b_algo".*?</li>', html_text, re.S)
    for b in blocks[:max_n * 2]:
        m = re.search(r'<h2[^>]*><a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', b, re.S)
        if not m:
            continue
        url = html.unescape(m.group(1))
        title = re.sub(r"<[^>]+>", "", m.group(2))
        # snippet
        sn = re.search(r'<p[^>]*>(.*?)</p>', b, re.S)
        snippet = ""
        if sn:
            snippet = re.sub(r"<[^>]+>", "", sn.group(1))
        results.append((html.unescape(title), url, html.unescape(snippet)))
        if len(results) >= max_n:
            break
    return results


def bing_search(query, out, max_n=15):
    q = urllib.parse.quote(query)
    url = ("https://www.bing.com/search?q=" + q +
           "&setmkt=en-US&count=20&setlang=es")
    t = fetch(url, out)
    res = extract(t, max_n)
    print("QUERY:", query)
    if not res:
        txt = re.sub(r"<[^>]+>", " ", t)
        txt = html.unescape(re.sub(r"\s+", " ", txt))
        print("  NO-PARSED-RESULTS. page head:", txt[:200])
    for ti, u, sn in res:
        print(" -", ti[:110])
        print("   ", u[:180])
        if sn:
            print("   >", sn[:180])
    print()
    return res


if __name__ == "__main__":
    queries = sys.argv[1:] or ['"Sergio Criales" WWF Bolivia']
    for i, q in enumerate(queries, 1):
        bing_search(q, "_serp_bing_%d.html" % i)

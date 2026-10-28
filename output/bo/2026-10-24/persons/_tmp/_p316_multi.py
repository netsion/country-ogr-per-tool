# -*- coding: utf-8 -*-
"""Multi-engine SERP fetch + extract for BO-PERSON-000316 research."""
import html
import re
import subprocess
import sys
import urllib.parse

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
OUT = "D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/_tmp/"


def fetch(url, out):
    subprocess.run(["curl", "-s", "-L", "-m", "50", "-x", PROXY, "-A", UA,
                    "-H", "Accept-Language: es-ES,es;q=0.9,en;q=0.7", url, "-o", OUT + out],
                   check=False)
    try:
        with open(OUT + out, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def parse_bing(t, max_n=12):
    res = []
    for b in re.findall(r'<li class="b_algo".*?</li>', t, re.S):
        m = re.search(r'<h2[^>]*><a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', b, re.S)
        if not m:
            continue
        u = html.unescape(m.group(1))
        ti = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        sn = re.search(r'<p[^>]*>(.*?)</p>', b, re.S)
        snip = html.unescape(re.sub(r"<[^>]+>", "", sn.group(1))) if sn else ""
        res.append((ti, u, snip))
        if len(res) >= max_n:
            break
    return res


def parse_brave(t, max_n=12):
    res = []
    for b in re.findall(r'<div class="snippet[^"]*"[^>]*>.*?(?=<div class="snippet|<div id="side"|</main>)', t, re.S):
        m = re.search(r'<a[^>]+href="(http[^"]+)"', b, re.S)
        if not m:
            continue
        u = html.unescape(m.group(1))
        ti = re.search(r'class="title[^"]*"[^>]*>(.*?)</div>', b, re.S)
        title = html.unescape(re.sub(r"<[^>]+>", "", ti.group(1))) if ti else u
        sn = re.search(r'class="snippet-description[^"]*"[^>]*>(.*?)</div>', b, re.S)
        snip = html.unescape(re.sub(r"<[^>]+>", "", sn.group(1))) if sn else ""
        res.append((title, u, snip))
        if len(res) >= max_n:
            break
    return res


def parse_mojeek(t, max_n=12):
    res = []
    for b in re.findall(r'<li>(.*?)</li>', t, re.S):
        m = re.search(r'<h2><a[^>]+href="(http[^"]+)"[^>]*>(.*?)</a></h2>', b, re.S)
        if not m:
            continue
        u = html.unescape(m.group(1))
        ti = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        p = re.search(r'<p class="s">(.*?)</p>', b, re.S)
        snip = html.unescape(re.sub(r"<[^>]+>", "", p.group(1))) if p else ""
        res.append((ti, u, snip))
        if len(res) >= max_n:
            break
    return res


def show(label, res):
    print("### " + label + " : %d results" % len(res))
    for ti, u, sn in res:
        print(" -", ti[:120])
        print("   URL:", u[:170])
        if sn:
            print("   SNIP:", sn[:260])


if __name__ == "__main__":
    engine, query, name = sys.argv[1], sys.argv[2], sys.argv[3]
    q = urllib.parse.quote(query)
    if engine == "bing":
        t = fetch("https://www.bing.com/search?q=" + q + "&setmkt=en-US&count=20&setlang=es", name)
        show("BING " + query, parse_bing(t))
    elif engine == "brave":
        t = fetch("https://search.brave.com/search?q=" + q, name)
        show("BRAVE " + query, parse_brave(t))
        if not parse_brave(t):
            txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))
            print("  raw head:", txt[:300])
    elif engine == "mojeek":
        t = fetch("https://www.mojeek.com/search?q=" + q, name)
        show("MOJEEK " + query, parse_mojeek(t))
        if not parse_mojeek(t):
            txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))
            print("  raw head:", txt[:300])
    elif engine == "ddghtml":
        t = fetch("https://html.duckduckgo.com/html/?q=" + q, name)
        res = []
        for m in re.finditer(r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.*?)</a>', t, re.S):
            u = html.unescape(m.group(1))
            ti = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
            res.append((ti, u, ""))
            if len(res) >= 12:
                break
        show("DDGHTML " + query, res)
        if not res:
            txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))
            print("  raw head:", txt[:300])

# -*- coding: utf-8 -*-
"""DDG html POST search helper + batch queries."""
import subprocess
import re
import html
import urllib.parse
import sys
import time
import json
import os

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
BASE = os.path.dirname(os.path.abspath(__file__))


def ddg(q, fn):
    r = subprocess.run(
        ["curl", "-s", "--max-time", "30", "-x", PROXY, "-A", UA,
         "-e", "https://html.duckduckgo.com/",
         "--data-urlencode", "q=" + q,
         "--data-urlencode", "b=",
         "--data-urlencode", "kl=es-es",
         "https://html.duckduckgo.com/html/"],
        capture_output=True, text=True, encoding="utf-8", errors="ignore")
    c = r.stdout
    with open(os.path.join(BASE, fn), "w", encoding="utf-8") as f:
        f.write(c)
    items = re.findall(
        r'<div class="result results_links.*?(?=<div class="result results_links|<div class="nav-link)',
        c, re.S)
    out = []
    for it in items:
        mu = re.search(r'class="result__a"[^>]*href="([^"]+)"', it)
        mt = re.search(r'class="result__a"[^>]*>(.*?)</a>', it, re.S)
        ms = re.search(r'class="result__snippet"[^>]*>(.*?)</a>', it, re.S)
        url = html.unescape(mu.group(1)) if mu else ""
        if "uddg=" in url:
            qq = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            url = qq.get("uddg", [url])[0]
        t = html.unescape(re.sub(r"<[^>]+>", "", mt.group(1))).strip() if mt else ""
        s = html.unescape(re.sub(r"<[^>]+>", " ", ms.group(1))).strip() if ms else ""
        out.append({"title": t, "url": url, "snippet": s})
    return out


QUERIES = [
    ("Alberto Mosquera World Vision Bolivia retiro sucesor 2022", "q_retiro.html"),
    ("Juan Carlos Ramirez World Vision Bolivia nuevo director nacional", "q_jcr.html"),
    ("Peter Fenoy World Vision Bolivia director nacional", "q_fenoy.html"),
    ("Alberto Mosquera ecuatoriano Vision Mundial Bolivia", "q_ecu.html"),
    ("Alberto Mosquera World Vision Ecuador director nacional", "q_wvecu.html"),
    ("\"Alberto Mosquera\" \"World Vision\" 2021 OR 2022 Bolivia", "q_2122.html"),
]

if __name__ == "__main__":
    for q, fn in QUERIES:
        res = ddg(q, fn)
        print("#" * 12, "QUERY:", q, "-> results:", len(res))
        for r in res[:9]:
            print("-", r["title"][:120])
            print(" ", r["url"][:160])
            if r["snippet"]:
                print("  S:", r["snippet"][:230])
        print()
        time.sleep(2)

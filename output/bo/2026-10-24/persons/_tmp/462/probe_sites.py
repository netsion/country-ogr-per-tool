# -*- coding: utf-8 -*-
"""Probe search endpoints of reachable Bolivian news sites."""
import subprocess
import re
import html
import urllib.parse

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def get(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "30", "-x", PROXY, "-A", UA,
                        "-H", "Accept-Language: es,en;q=0.8",
                        "-w", "\n===HTTP:%{http_code}", url],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return r.stdout


def head(c):
    m = re.search(r"<title>(.*?)</title>", c, re.S)
    return html.unescape(m.group(1)).strip()[:150] if m else "n/a"


def forms(c):
    out = []
    for f in re.findall(r"<form[^>]*>", c)[:6]:
        out.append(f[:200])
    return out


for site in ["https://www.noticiasfides.com", "https://www.reduno.com.bo",
             "https://www.atb.com.bo", "https://larazon.bo",
             "https://www.lapatriaenlinea.com"]:
    c = get(site)
    print("=" * 20, site)
    print("title:", head(c))
    for f in forms(c):
        print("FORM:", f)
    # common WP search test
    q = urllib.parse.quote_plus("Mosquera Vision Mundial")
    c2 = get(site + "/?s=" + q)
    print("WP ?s= title:", head(c2), "| mosquera hits:", c2.lower().count("mosquera"),
          "| bytes:", len(c2))
    print()

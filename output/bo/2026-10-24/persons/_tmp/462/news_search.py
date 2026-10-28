# -*- coding: utf-8 -*-
"""Site searches on reachable Bolivian news sites + wvi.org."""
import subprocess
import re
import html
import urllib.parse
import json

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def get(url, referer=None):
    cmd = ["curl", "-sL", "--max-time", "30", "-x", PROXY, "-A", UA,
           "-H", "Accept-Language: es,en;q=0.8",
           "-w", "\n===HTTP:%{http_code}"]
    if referer:
        cmd += ["-e", referer]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return r.stdout


def links_from(html_text, base_pat):
    """Extract (title, url) pairs from anchor tags."""
    out = []
    for m in re.finditer(r'<a[^>]+href="(' + base_pat + r')[^"]*"[^>]*>(.*?)</a>', html_text, re.S):
        u, t = m.group(1), re.sub(r"<[^>]+>", " ", m.group(2))
        t = html.unescape(re.sub(r"\s+", " ", t)).strip()
        if t and len(t) > 10:
            out.append((t, u))
    return out


def show(title, hits, limit=20):
    print("###", title, "-> hits:", len(hits))
    seen = set()
    n = 0
    for t, u in hits:
        if u in seen:
            continue
        seen.add(u)
        print("-", t[:130])
        print(" ", u[:160])
        n += 1
        if n >= limit:
            break
    print()


Q1 = urllib.parse.quote_plus('"Alberto Mosquera" "World Vision"')
Q2 = urllib.parse.quote_plus('Mosquera Vision Mundial')
Q3 = urllib.parse.quote_plus('Mosquera Visión Mundial')

# opinion.com.bo (WordPress?)
c = get("https://www.opinion.com.bo/?s=" + Q2)
print("opinion.com.bo http:", c[-20:])
mm = re.search(r"<title>(.*?)</title>", c, re.S)
print("opinion title:", html.unescape(mm.group(1))[:150] if mm else "n/a")
print("Mosquera mentions:", c.lower().count("mosquera"))
show("opinion.com.bo ?s=Mosquera Vision Mundial",
     links_from(c, r"https://www\.opinion\.com\.bo/[a-z0-9/\-]+"))

# erbol.com.bo
c = get("https://www.erbol.com.bo/noticia/buscar?texto=" + Q3)
print("erbol http:", c[-20:])
mm = re.search(r"<title>(.*?)</title>", c, re.S)
print("erbol title:", html.unescape(mm.group(1))[:150] if mm else "n/a")
print("Mosquera mentions:", c.lower().count("mosquera"))
show("erbol search", links_from(c, r"https?://www\.erbol\.com\.bo/\S+"))

# eldeber (301 follow)
c = get("https://eldeber.com.bo/busqueda?q=" + Q2)
print("eldeber http:", c[-20:])
mm = re.search(r"<title>(.*?)</title>", c, re.S)
print("eldeber title:", html.unescape(mm.group(1))[:150] if mm else "n/a")
print("Mosquera mentions:", c.lower().count("mosquera"))

# correodelsur (301 follow)
c = get("https://www.correodelsur.com/busqueda?q=" + Q3)
print("correodelsur http:", c[-20:])
mm = re.search(r"<title>(.*?)</title>", c, re.S)
print("correodelsur title:", html.unescape(mm.group(1))[:150] if mm else "n/a")
print("Mosquera mentions:", c.lower().count("mosquera"))

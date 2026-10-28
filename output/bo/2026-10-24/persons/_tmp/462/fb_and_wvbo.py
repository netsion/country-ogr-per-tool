# -*- coding: utf-8 -*-
"""Fetch FB pages (save to disk), extract dates; worldvision.bo site search."""
import subprocess
import re
import html
import os
import urllib.parse

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
BASE = os.path.dirname(os.path.abspath(__file__))


def get(url, mobile=False):
    ua = ("Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36" if mobile else UA)
    cmd = ["curl", "-sL", "--max-time", "40", "-x", PROXY, "-A", ua,
           "-H", "Accept-Language: es,en;q=0.8"]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return r.stdout


def fb_dates(c):
    pats = {
        "datePublished": r'"datePublished":"([^"]+)"',
        "uploadDate": r'"uploadDate":"([^"]+)"',
        "creation_time": r'"creation_time":(\d{9,11})',
        "publish_time": r'"publish_time":(\d{9,11})',
        "iso": r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{4})',
        "created": r'"created_time":"([^"]+)"',
        "publish": r'"publish":"(\d+)"',
        "date_posted": r'datePosted["\s:]+(\d{4}-\d{2}-\d{2})',
    }
    out = {}
    for k, p in pats.items():
        ms = re.findall(p, c)
        if ms:
            out[k] = ms[:4]
    return out


def save(name, c):
    with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
        f.write(c)


# 1. FB retirement interview — desktop + mobile versions
print("### FB puntovida desktop")
c = get("https://www.facebook.com/puntovidascc/videos/entrevista-con-alberto-mosquera-director-nacional-world-vision-bolivia/1069618153686471/")
save("fb_puntovida.html", c)
print("bytes:", len(c), "dates:", fb_dates(c))

print("### FB puntovida mobile")
c = get("https://mbasic.facebook.com/puntovidascc/videos/1069618153686471/", mobile=True)
save("fb_puntovida_mbasic.html", c)
print("bytes:", len(c))
mm = re.search(r"<title>(.*?)</title>", c, re.S)
print("title:", html.unescape(mm.group(1)).strip()[:200] if mm else "n/a")
for m in re.finditer(r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})', c):
    print("DATE:", m.group(1))
    break

print("### FB condecoracion Camiri")
c = get("https://www.facebook.com/WorldVisionBO/videos/world-vision-bolivia-representado-por-su-director-nacional-alberto-mosquerarecib/562736575376663/")
save("fb_condecoracion.html", c)
print("bytes:", len(c), "dates:", fb_dates(c))
mt = re.search(r'property="og:description" content="([^"]*)"', c)
if mt:
    print("og:desc:", html.unescape(mt.group(1))[:400])

# 2. worldvision.bo site search for Mosquera
for q in ["Mosquera", "Alberto Mosquera", "nuevo director", "Juan Carlo"]:
    u = "https://www.worldvision.bo/?s=" + urllib.parse.quote_plus(q)
    c = get(u)
    save("wvbo_s_%s.html" % q.replace(" ", "_"), c)
    n = c.lower().count("mosquera")
    t = re.search(r"<title>(.*?)</title>", c, re.S)
    print("### worldvision.bo ?s=%s bytes=%d mosquera=%d title=%s" % (
        q, len(c), n, html.unescape(t.group(1)).strip()[:80] if t else ""))
    links = re.findall(r'href="(https://www\.worldvision\.bo/[^"]+)"[^>]*>([^<]{10,200})<', c)
    seen = set()
    for l, tt in links:
        if l in seen or "/wp-content" in l or "#" in l:
            continue
        tt2 = html.unescape(tt).strip()
        if re.search(r"(mosquera|director|mundial|visi)", tt2, re.I):
            seen.add(l)
            print("  -", tt2[:120], "|", l[:130])

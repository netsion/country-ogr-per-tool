# -*- coding: utf-8 -*-
"""Fetch and extract text from key source pages."""
import subprocess
import re
import html
import os

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
BASE = os.path.dirname(os.path.abspath(__file__))


def get(url, extra=None):
    cmd = ["curl", "-sL", "--max-time", "35", "-x", PROXY, "-A", UA,
           "-H", "Accept-Language: es,en;q=0.8",
           "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"]
    if extra:
        cmd += extra
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return r.stdout


def meta_tags(c):
    out = {}
    for m in re.finditer(r'<meta[^>]+(?:property|name)="(og:title|og:description|og:url|description|article:published_time|og:type)"[^>]+content="([^"]*)"', c):
        out[m.group(1)] = html.unescape(m.group(2))
    for m in re.finditer(r'content="([^"]*)"[^>]+(?:property|name)="(og:title|og:description|article:published_time)"', c):
        if m.group(2) not in out:
            out[m.group(2)] = html.unescape(m.group(1))
    t = re.search(r"<title>(.*?)</title>", c, re.S)
    out["__title"] = html.unescape(t.group(1)).strip() if t else ""
    return out


def body_text(c, limit=4000):
    m = re.search(r"<article.*?</article>", c, re.S)
    body = m.group(0) if m else c
    text = re.sub(r"<script.*?</script>", " ", body, flags=re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    return text[:limit]


TARGETS = [
    ("linkedin_ec", "https://ec.linkedin.com/in/alberto-mosquera-aa210523b"),
    ("inforse", "https://www.inforse.com.bo/2020/12/19/world-vision-bolivia/"),
    ("worldvision_bo", "https://www.worldvision.bo/"),
    ("wvbo_equipo", "https://www.worldvision.bo/nuestro-equipo"),
    ("agendaminera", "https://www.agendaminera.com/actualidad/%F0%9D%90%96%F0%9D%90%A8%F0%9D%90%AB%F0%9D%90%A5%F0%9D%90%9D-%F0%9D%90%95%F0%9D%90%A2%F0%9D%90%AC%F0%9D%90%A2%F0%9D%90%A8%F0%9D%90%A7-%F0%9D%90%81%F0%9D%90%A8%F0%9D%90%A5%F0%9D%90%A2%F0%9D%90%AF%F0%9D%90%9A-%F0%9D%90%9C%F0%9D%90%AE%F0%9D%90%A6%F0%9D%90%A9%F0%9D%90%9A%F0%9D%90%9A%F0%9D%90%9A"),
    ("fb_puntovida", "https://www.facebook.com/puntovidascc/videos/entrevista-con-alberto-mosquera-director-nacional-world-vision-bolivia/1069618153686471/"),
    ("fb_condecoracion", "https://www.facebook.com/WorldVisionBO/videos/world-vision-bolivia-representado-por-su-director-nacional-alberto-mosquerarecib/562736575376663/"),
    ("wv_alc_sanitaria", "https://worldvisionamericalatina.org/world-vision-bolivia-fortalece-la-respuesta-sanitaria-durante-la-contingencia-nacional/"),
]

if __name__ == "__main__":
    for name, url in TARGETS:
        c = get(url)
        print("=" * 25, name, "bytes:", len(c))
        mt = meta_tags(c)
        for k in ("__title", "og:title", "og:description", "article:published_time", "description"):
            if mt.get(k):
                print("%s: %s" % (k, mt[k][:300]))
        print()

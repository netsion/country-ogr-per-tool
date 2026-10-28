# -*- coding: utf-8 -*-
"""Last probes: sedes page for La Paz web/contacts; Economy Huawei 2024 article; El Diario googlebot."""
import json
import re
import urllib.request

BASE = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24"
PROXY = "http://127.0.0.1:7890"


def make_opener(ua):
    op = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    op.addheaders = [("User-Agent", ua), ("Accept-Language", "es-419,es;q=0.9,en;q=0.7")]
    return op


UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def fetch(url, opener, timeout=45):
    try:
        resp = opener.open(url, timeout=timeout)
        return resp.read().decode("utf-8", "replace")
    except Exception as e:
        return f"__ERR__ {e}"


op = make_opener(UA)

# 1. sedes academicas page
print("== sedes page ==")
h = fetch("https://www.ucb.edu.bo/sedes-academicas-de-la-ucb/", op)
if not h.startswith("__ERR__"):
    h2 = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<style.*?</style>", " ", h2, flags=re.S | re.I)))
    i = txt.find("Sede La Paz")
    print(txt[max(0, i - 50): i + 900])
    for m in re.finditer(r'href="(https?://[^"]*(?:paz|lapaz)[^"]*)"', h2, re.I):
        print("  LINK:", m.group(1)[:150])
else:
    print("ERR", h[:100])

# 2. Economy Huawei Semillas 2024 — search wp-json
print("\n== economy.com.bo search ==")
for q in ["Huawei Semillas", "Semillas para el Futuro 2024"]:
    u = "https://www.economy.com.bo/buscador?query=" + urllib.parse.quote(q)
    r = fetch(u, op)
    if r.startswith("__ERR__"):
        print("search ERR", r[:80])
        break
    hits = re.findall(r'href="(https://www\.economy\.com\.bo/articulo/[^"]+)"', r)
    uniq = list(dict.fromkeys(hits))
    print(q, "->", len(uniq))
    for x in uniq[:6]:
        print("   ", x[:170])

# fallback: try wp-json
r = fetch("https://www.economy.com.bo/wp-json/wp/v2/posts?search=" + urllib.parse.quote("Huawei Semillas Futuro"), op)
if not r.startswith("__ERR__"):
    try:
        posts = json.loads(r)
        if isinstance(posts, list):
            for p in posts[:5]:
                print("  wp:", p.get("link", "")[:170])
    except Exception:
        print("  wp-json nonjson")

# 3. El Diario with googlebot UA
print("\n== El Diario googlebot ==")
gb = make_opener("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
r = fetch("https://www.eldiario.net/portal/2024/01/08/nace-la-carrera-de-medicina-en-la-ucb/", gb)
print("googlebot:", r[:100])
if r.startswith("__ERR__"):
    r2 = fetch("http://www.eldiario.net/portal/2024/01/08/nace-la-carrera-de-medicina-en-la-ucb/", op)
    print("http:", r2[:100])

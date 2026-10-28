# -*- coding: utf-8 -*-
"""Fetch appointment post + CEB articles; parse Bing SERP links."""
import json
import re
import urllib.request

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener.addheaders = [("User-Agent", UA), ("Accept-Language", "es-ES,es;q=0.9,en;q=0.7")]


def fetch(url, timeout=50):
    try:
        resp = opener.open(url, timeout=timeout)
        return resp.read().decode("utf-8", "replace")
    except Exception as e:
        return f"__ERR__ {e}"


def strip_html(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    for a, b in [("&nbsp;", " "), ("&amp;", "&"), ("&#8220;", '"'), ("&#8221;", '"'), ("&#8217;", "'"),
                 ("&quot;", '"'), ("&#8211;", "-"), ("&#8216;", "'"), ("&laquo;", "«"), ("&raquo;", "»"),
                 ("&#8226;", "-"), ("&#8230;", "...")]:
        h = h.replace(a, b)
    return re.sub(r"\s+", " ", h).strip()


# 1. appointment post full text + featured image
raw = fetch("https://www.ucb.edu.bo/wp-json/wp/v2/posts?slug=la-sede-la-paz-de-la-u-c-b-tiene-una-nueva-rectora&_embed")
try:
    p = json.loads(raw)[0]
    print("=" * 90)
    print("APPOINTMENT POST:", p.get("date"), "|", p.get("link"))
    print(strip_html(p.get("content", {}).get("rendered", ""))[:4000])
    for m in p.get("_embedded", {}).get("wp:featuredmedia", []):
        print("\nFEATURED IMG:", m.get("source_url"))
except Exception as e:
    print("appt ERR", e)

# 2. CEB articles
for url in [
    "https://ceb.bo/2025/11/encuentro-sinodal-de-universidades-catolicas/",
    "https://ceb.bo/2026/04/la-universidad-catolica-boliviana-recibe-distinciones-internacionales-por-la-fundacion-carlos-iii/",
]:
    h = fetch(url)
    if h.startswith("__ERR__"):
        print(url, "ERR", h[:100])
        continue
    h2 = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h2 = re.sub(r"<style.*?</style>", " ", h2, flags=re.S | re.I)
    # isolate article body
    mbody = re.search(r"<article.*?</article>", h2, re.S) or re.search(r"<main.*?</main>", h2, re.S)
    body = mbody.group(0) if mbody else h2
    txt = strip_html(body)
    print("=" * 90)
    print("CEB:", url)
    print(txt[:3000])
    with open(url.split("/")[-1][:40] + "_ceb.txt", "w", encoding="utf-8") as f:
        f.write(txt)

# 3. parse Bing SERP files
import html as hm
import os
os.chdir(r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24")
for key in ["li", "fb", "ig", "x", "tt", "senado", "gen1", "gen2", "yt"]:
    fn = f"_xpa_bing_{key}.html"
    h = open(fn, encoding="utf-8", errors="ignore").read()
    h2 = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h2 = re.sub(r"<style.*?</style>", " ", h2, flags=re.S | re.I)
    seen = set()
    print("=" * 90)
    print(f"== SERP {key} ==")
    for m in re.finditer(r'<h2><a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', h2, re.S):
        u = m.group(1)
        t = strip_html(m.group(2))
        if u in seen or "bing.com" in u:
            continue
        seen.add(u)
        print("  -", u[:180], "||", t[:110])
    # also snippet text mentioning Peres
    plain = strip_html(h2)
    for mm in re.finditer(r"[Pp]eres Arenas", plain):
        s = max(0, mm.start() - 200)
        print("  SNIP:", plain[s:mm.end() + 200].strip()[:380])

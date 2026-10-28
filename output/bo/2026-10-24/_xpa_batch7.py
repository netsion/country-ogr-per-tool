# -*- coding: utf-8 -*-
"""Mojeek searches + YouTube oEmbed check."""
import json
import re
import urllib.parse
import urllib.request

BASE = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24"
PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener.addheaders = [("User-Agent", UA), ("Accept-Language", "es-419,es;q=0.9,en;q=0.7")]


def fetch(url, timeout=45):
    try:
        resp = opener.open(url, timeout=timeout)
        return resp.read().decode("utf-8", "replace")
    except Exception as e:
        return f"__ERR__ {e}"


def clean(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = urllib.parse.unquote(t)
    return re.sub(r"\s+", " ", t).strip()


QUERIES = {
    "gen": '"Ximena Peres Arenas"',
    "li": '"Ximena Peres Arenas" linkedin',
    "li2": '"Ximena Peres" UCB linkedin',
    "fb": '"Ximena Peres Arenas" facebook',
    "ig": '"Ximena Peres Arenas" instagram',
    "x": '"Ximena Peres Arenas" twitter OR x.com',
    "tt": '"Ximena Peres Arenas" tiktok',
    "sen": '"Ximena Peres" senado distincion',
    "yt": '"Ximena Peres Arenas" youtube',
    "med": '"Ximena Peres" UCB -site:ucb.edu.bo',
}
for key, q in QUERIES.items():
    url = "https://www.mojeek.com/search?q=" + urllib.parse.quote(q)
    h = fetch(url)
    fn = rf"{BASE}\_xpa_mjk_{key}.html"
    with open(fn, "w", encoding="utf-8", errors="ignore") as f:
        f.write(h)
    if h.startswith("__ERR__"):
        print(key, "ERR", h[:90])
        continue
    h2 = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    print(f"===== mojeek {key} =====")
    seen = set()
    for m in re.finditer(r'<a[^>]+class="title[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', h2, re.S):
        u, t = m.group(1), clean(m.group(2))
        if u in seen:
            continue
        seen.add(u)
        print("  -", u[:170], "||", t[:100])
    plain = clean(h2)
    for mm in list(re.finditer(r"Peres", plain))[:3]:
        s = max(0, mm.start() - 150)
        print("   SNIP:", plain[s:mm.end() + 250][:380])

# YouTube oEmbed
print("\n== YouTube oEmbed ==")
r = fetch("https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=3rdpCa18BmE&format=json")
try:
    j = json.loads(r)
    print(json.dumps(j, ensure_ascii=False, indent=1)[:800])
except Exception:
    print("raw:", r[:300])

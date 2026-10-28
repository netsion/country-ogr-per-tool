# -*- coding: utf-8 -*-
"""Grep Bing SERP files for social URLs and Peres mentions; grep CEB txts."""
import re

BASE = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24"
import html as hm


def clean(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = hm.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


for key in ["li", "fb", "ig", "x", "tt", "senado", "gen1", "gen2", "yt"]:
    h = open(rf"{BASE}\_xpa_bing_{key}.html", encoding="utf-8", errors="ignore").read()
    h2 = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h2 = re.sub(r"<style.*?</style>", " ", h2, flags=re.S | re.I)
    print(f"===== {key} =====")
    urls = set()
    for m in re.finditer(r'href="(https?://(?!www\.bing|go\.micro|cn\.bing|support\.micro|microsoft)[^"]+)"', h2):
        u = hm.unescape(m.group(1))
        if any(s in u for s in ["linkedin.com", "facebook.com", "instagram.com", "tiktok.com", "x.com", "twitter.com", "youtube.com", "senado", "eldiario", "urgentebo", "eju", "celam", "elecciones", "opinion"]):
            if u not in urls:
                urls.add(u)
                print("  URL:", u[:200])
    plain = clean(h2)
    n = 0
    for mm in re.finditer(r"Peres", plain):
        s = max(0, mm.start() - 160)
        seg = plain[s:mm.end() + 240].strip()
        if "Búsqueda" in seg or "resultados" in seg:
            continue
        n += 1
        if n <= 4:
            print("  SNIP:", seg[:360])
    if not urls and n == 0:
        print("  (no relevant organic hits)")

print()
print("===== CEB sinodal txt: Peres/Ximena mentions =====")
try:
    t = open(rf"{BASE}\encuentro-sinodal-de-universidades-c_ceb.txt", encoding="utf-8").read()
    for mm in re.finditer(r"Peres|Ximena", t):
        s = max(0, mm.start() - 250)
        print("  >>>", t[s:mm.end() + 300].strip()[:550])
        print()
except FileNotFoundError:
    print("  file not found")

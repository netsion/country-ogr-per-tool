# -*- coding: utf-8 -*-
"""Grep bing SERPs for raw social URLs; verify CEB txts; archive.org El Diario; eju.tv search."""
import glob
import json
import re
import urllib.parse
import urllib.request

BASE = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24"
PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener.addheaders = [("User-Agent", UA), ("Accept-Language", "es-419,es;q=0.9,en;q=0.7")]


def fetch(url, timeout=50):
    try:
        resp = opener.open(url, timeout=timeout)
        return resp.read().decode("utf-8", "replace")
    except Exception as e:
        return f"__ERR__ {e}"


# 1. grep bing SERPs for raw URLs
for key in ["li", "fb", "ig", "x", "tt", "senado", "gen1", "gen2", "yt"]:
    h = open(rf"{BASE}\_xpa_bing_{key}.html", encoding="utf-8", errors="ignore").read()
    found = set()
    for m in re.finditer(r'https?://(?!www\.bing|go\.micro|cn\.bing|support|account|microsoft|choice)[a-zA-Z0-9./_%?=&;-]+', urllib.parse.unquote(h)):
        u = m.group(0)
        for dom in ["linkedin.com/in", "facebook.com/", "instagram.com/", "tiktok.com/@", "x.com/", "twitter.com/", "youtube.com/", "senado"]:
            if dom in u and "bing" not in u:
                u2 = u.split("&")[0].split('"')[0]
                if len(u2) > 25:
                    found.add(u2)
    if found:
        print(f"== {key} ==")
        for u in list(found)[:12]:
            print("  ", u[:190])

# 2. CEB txts
print("\n== CEB txts ==")
for fn in glob.glob(BASE + r"\*_ceb.txt"):
    t = open(fn, encoding="utf-8").read()
    print("--", fn.split("\\")[-1], len(t))
    for mm in re.finditer(r"Peres|Ximena", t):
        s = max(0, mm.start() - 280)
        print("   >>>", t[s:mm.end() + 280].strip()[:560])
        print()

# 3. archive.org El Diario
print("== archive.org El Diario ==")
av = fetch("https://archive.org/wayback/available?url=eldiario.net/portal/2024/01/08/nace-la-carrera-de-medicina-en-la-ucb/")
try:
    j = json.loads(av)
    print(json.dumps(j, ensure_ascii=False)[:400])
    snap = j.get("archived_snapshots", {}).get("closest", {}).get("url")
    if snap:
        h = fetch(snap)
        if not h.startswith("__ERR__"):
            h2 = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
            h2 = re.sub(r"<style.*?</style>", " ", h2, flags=re.S | re.I)
            h2 = re.sub(r"<[^>]+>", " ", h2)
            h2 = re.sub(r"\s+", " ", h2)
            i = h2.find("Medicina")
            print(h2[max(0, i - 100): i + 2600])
            open(rf"{BASE}\_xpa_eldiario.txt", "w", encoding="utf-8").write(h2)
except Exception as e:
    print("ERR", e)

# 4. eju.tv search Huawei
print("\n== eju.tv wp-json 'Huawei educación' ==")
r = fetch("https://eju.tv/wp-json/wp/v2/posts?search=" + urllib.parse.quote("Huawei redobla apuesta educación") + "&per_page=5")
if not r.startswith("__ERR__"):
    try:
        posts = json.loads(r)
        for p in posts if isinstance(posts, list) else []:
            print("  -", p.get("link", ""), "|", re.sub("<[^>]+>", "", p.get("title", {}).get("rendered", ""))[:100])
            if "huawei" in p.get("link", "").lower() or "huawei" in p.get("title", {}).get("rendered", "").lower():
                body = re.sub(r"<[^>]+>", " ", p.get("content", {}).get("rendered", ""))
                body = re.sub(r"\s+", " ", body)
                for mm in re.finditer(r"Peres|Ximena", body):
                    s = max(0, mm.start() - 250)
                    print("    >>>", body[s:mm.end() + 300].strip()[:520])
    except Exception as e:
        print("  ERR", e, r[:120])
else:
    print("  ", r[:100])

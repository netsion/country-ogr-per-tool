# -*- coding: utf-8 -*-
"""Fetch UCB wp-json posts mentioning Peres/Arenas + resolve Google News redirects."""
import json
import re
import sys
import urllib.parse
import urllib.request

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener.addheaders = [("User-Agent", UA), ("Accept-Language", "es-ES,es;q=0.9,en;q=0.7")]


def fetch(url, timeout=50, data=None):
    try:
        req = url if data is None else urllib.request.Request(url, data=data.encode("utf-8"))
        resp = opener.open(req, timeout=timeout)
        return resp.read().decode("utf-8", "replace")
    except Exception as e:
        return f"__ERR__ {e}"


# --- 1. UCB wp-json search ---
for q in ["Peres Arenas", "Peres", "rectora sede la paz"]:
    url = "https://www.ucb.edu.bo/wp-json/wp/v2/posts?search=" + urllib.parse.quote(q) + "&per_page=20"
    raw = fetch(url)
    if raw.startswith("__ERR__"):
        print(f"UCB search '{q}' ERROR:", raw[:150])
        continue
    try:
        posts = json.loads(raw)
    except Exception:
        print(f"UCB search '{q}': non-JSON response len={len(raw)}", raw[:200])
        continue
    if isinstance(posts, dict):
        print(f"UCB search '{q}':", json.dumps(posts, ensure_ascii=False)[:300])
        continue
    print(f"== UCB wp-json '{q}': {len(posts)} posts ==")
    for p in posts:
        print("  -", p.get("date", ""), "|", p.get("link", ""), "|", re.sub("<[^>]+>", "", p.get("title", {}).get("rendered", ""))[:120])

# --- 2. Resolve Google News redirects ---
INNER = (
    '[["garturlreq",[["en-US","US",["FINANCE_TOP_INDICES","WEB_TEST_1_0_0"],null,null,1,1,"US:en",null,180,null,null,null,null,null,0,null,null,[1608992183,723341000]],"en-US","US",1,[2,3,4,8],1,0,"655000234",0,0,null,0],"{ID}",0,"en-US"]'
)


def resolve(gn_id):
    inner = INNER.replace("{ID}", gn_id)
    freq = json.dumps([["Fbv4je", inner, None, "generic"]])
    body = "f.req=" + urllib.parse.quote(freq)
    r = urllib.request.Request(
        "https://news.google.com/_/DotsSplashUi/data/batchexecute",
        data=body.encode("utf-8"),
        headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"},
    )
    op = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    with op.open(r, timeout=40) as resp:
        text = resp.read().decode("utf-8", "replace")
    m = re.search(r'https?://[^"\\\s]+', text)
    if not m:
        raise ValueError("no url: " + text[:150])
    return m.group(0)


with open(r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\_xpa_rss1.json", encoding="utf-8") as f:
    rss = json.load(f)

targets = {}
for key in ["gn_ximena_peres_arenas", "gn_ximena_peres_ucb", "gn_peres_arenas"]:
    for it in rss.get(key, {}).get("items", []):
        link = it["link"]
        if "/articles/" in link:
            targets[link] = it["title"]

print("\n== Resolving", len(targets), "gnews links ==")
resolved = {}
for link, title in targets.items():
    gn_id = link.split("/articles/")[1].split("?")[0]
    try:
        u = resolve(gn_id)
        print("OK ", u[:180], "||", title[:80])
        resolved[link] = {"url": u, "title": title}
    except Exception as e:
        print("ERR", repr(e)[:120], "||", title[:80])
    import time
    time.sleep(1)

with open(r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\_xpa_gnews_resolved.json", "w", encoding="utf-8") as f:
    json.dump(resolved, f, ensure_ascii=False, indent=1)

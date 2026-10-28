# -*- coding: utf-8 -*-
"""Search Ximena Peres Arenas via Google News RSS / Bing News RSS / Bing SERP (WebSearch quota exhausted)."""
import json
import re
import sys
import urllib.parse
import urllib.request

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener.addheaders = [("User-Agent", UA), ("Accept-Language", "es-ES,es;q=0.9,en;q=0.7")]


def fetch(url, timeout=45):
    try:
        resp = opener.open(url, timeout=timeout)
        return resp.read().decode("utf-8", "replace")
    except Exception as e:
        return f"__ERR__ {e}"


def parse_rss_titles(xml, tag_prefix=""):
    out = []
    for m in re.finditer(r"<item>(.*?)</item>", xml, re.S):
        it = m.group(1)
        t = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", it, re.S)
        l = re.search(r"<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>", it, re.S)
        d = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
        out.append({
            "title": t.group(1).strip() if t else "",
            "link": l.group(1).strip() if l else "",
            "date": d.group(1).strip() if d else "",
        })
    return out


QUERIES = {
    "gn_ximena_peres_arenas": "https://news.google.com/rss/search?q=%22Ximena%20Peres%20Arenas%22&hl=es-419&gl=BO&ceid=BO:es-419",
    "gn_ximena_peres_ucb": "https://news.google.com/rss/search?q=%22Ximena%20Peres%22%20UCB&hl=es-419&gl=BO&ceid=BO:es-419",
    "gn_peres_arenas": "https://news.google.com/rss/search?q=%22Peres%20Arenas%22&hl=es-419&gl=BO&ceid=BO:es-419",
    "bn_ximena_peres": "https://www.bing.com/news/search?q=%22Ximena+Peres%22&setmkt=es-BO&setlang=es&format=rss",
    "bn_peres_arenas_ucb": "https://www.bing.com/news/search?q=%22Peres+Arenas%22+UCB&setmkt=es-BO&setlang=es&format=rss",
}

results = {}
for key, url in QUERIES.items():
    xml = fetch(url)
    if xml.startswith("__ERR__"):
        results[key] = {"error": xml}
        continue
    items = parse_rss_titles(xml)
    results[key] = {"count": len(items), "items": items[:25]}

with open(r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\_xpa_rss1.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)

for k, v in results.items():
    if "error" in v:
        print(k, "ERROR:", v["error"][:120])
    else:
        print(f"== {k}: {v['count']} ==")
        for it in v["items"]:
            print("  -", it["date"][:16], "|", it["title"][:140])
            print("    ", it["link"][:200])

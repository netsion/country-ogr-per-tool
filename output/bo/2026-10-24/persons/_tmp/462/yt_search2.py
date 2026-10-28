# -*- coding: utf-8 -*-
"""YouTube search with dates + snippets; multiple queries."""
import json
import subprocess
import re
import sys
import urllib.parse

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def search(q):
    url = ("https://www.youtube.com/results?search_query=" +
           urllib.parse.quote_plus(q) + "&hl=es")
    r = subprocess.run(["curl", "-s", "--max-time", "40", "-x", PROXY, "-A", UA,
                        "-H", "Accept-Language: es,en;q=0.8", url],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    c = r.stdout
    m = re.search(r"ytInitialData = (\{.*?\});</script>", c, re.S)
    if not m:
        print("### FAIL:", q)
        return
    d = json.loads(m.group(1))
    out = []

    def walk(o):
        if isinstance(o, dict):
            if "videoRenderer" in o:
                v = o["videoRenderer"]
                t = "".join(r.get("text", "") for r in v.get("title", {}).get("runs", []))
                ch = "".join(r.get("text", "") for r in v.get("ownerText", {}).get("runs", []))
                pub = v.get("publishedTimeText", {}).get("simpleText", "")
                sn = "".join(r.get("text", "") for r in
                             v.get("detailedMetadataSnippets", [{}])[0].get("snippetText", {}).get("runs", []))
                out.append({"title": t, "channel": ch, "id": v.get("videoId", ""),
                            "published": pub, "snippet": sn})
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(d)
    print("### SEARCH:", q, "-> videos:", len(out))
    for v in out[:14]:
        print("- TITLE:", v["title"][:120])
        print("  CH:", v["channel"], "| ID:", v["id"], "| PUBLISHED:", v["published"])
        if v["snippet"]:
            print("  SNIP:", v["snippet"][:200])
    print()


QUERIES = [
    "Mosquera Vision Mundial Bolivia",
    "Vision Mundial Bolivia director nacional",
    "Juan Carlos Ramirez Vision Mundial Bolivia",
    "Alberto Mosquera Lopez Bolivia",
]
for q in QUERIES:
    search(q)

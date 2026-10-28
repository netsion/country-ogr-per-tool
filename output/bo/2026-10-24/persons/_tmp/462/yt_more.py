# -*- coding: utf-8 -*-
"""YouTube innertube WEB client + more searches."""
import json
import subprocess
import re
import sys

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def curl(url, post=None, extra_headers=None):
    cmd = ["curl", "-s", "--max-time", "40", "-x", PROXY, "-A", UA,
           "-H", "Accept-Language: es,en;q=0.8",
           "-b", "CONSENT=YES+cb.20220101-01-p0.en+FX+678; SOCS=CAISNQgQEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjMwODI5LjA3X3AxGgJlbiACGgYIgLC_pwY",
           "--compressed"]
    if post:
        cmd += ["-X", "POST", "-H", "Content-Type: application/json", "-d", post]
    if extra_headers:
        for h in extra_headers:
            cmd += ["-H", h]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return r.stdout


def player(vid):
    body = json.dumps({
        "context": {"client": {"clientName": "WEB", "clientVersion": "2.20240401.00.00",
                               "hl": "es", "gl": "BO"}},
        "videoId": vid,
    })
    o = curl("https://www.youtube.com/youtubei/v1/player", post=body)
    try:
        d = json.loads(o)
    except Exception:
        print(vid, "innertube parse fail", o[:200])
        return
    vd = d.get("videoDetails", {})
    mf = d.get("microformat", {}).get("playerMicroformatRenderer", {})
    print("=" * 25, vid, "=" * 25)
    print("title:", vd.get("title"))
    print("channel:", vd.get("author"), "| channelId:", vd.get("channelId"))
    print("publishDate:", mf.get("publishDate"), "| uploadDate:", mf.get("uploadDate"))
    print("views:", vd.get("viewCount"))
    desc = vd.get("shortDescription") or ""
    print("DESC:", desc[:1800].replace("\n", " | "))
    print()


def search(q):
    o = curl("https://www.youtube.com/results?search_query=" + q + "&hl=es")
    m = re.search(r"ytInitialData = (\{.*?\});</script>", o, re.S)
    if not m:
        print("search fail for", q)
        return
    d = json.loads(m.group(1))
    out = []

    def walk(o):
        if isinstance(o, dict):
            if "videoRenderer" in o:
                v = o["videoRenderer"]
                t = "".join(r.get("text", "") for r in v.get("title", {}).get("runs", []))
                ch = "".join(r.get("text", "") for r in v.get("ownerText", {}).get("runs", []))
                out.append((t, ch, v.get("videoId", "")))
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(d)
    print("### SEARCH:", q, "-> videos:", len(out))
    for t, ch, vid in out[:15]:
        print("-", t[:110], "|", ch, "|", vid)
    print()


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "player":
        for v in sys.argv[2:]:
            player(v)
    else:
        for q in sys.argv[2:]:
            search(q)

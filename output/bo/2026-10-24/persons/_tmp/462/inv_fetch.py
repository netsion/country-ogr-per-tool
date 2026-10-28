# -*- coding: utf-8 -*-
"""Fetch video metadata via Invidious/Piped public instances."""
import json
import subprocess
import sys

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

INVIDIOUS = [
    "https://inv.nadeko.net",
    "https://invidious.nerdvpn.de",
    "https://yewtu.be",
    "https://invidious.f5.si",
    "https://iv.melmac.space",
]
PIPED = [
    "https://pipedapi.kavin.rocks",
    "https://api.piped.private.coffee",
    "https://pipedapi.reallyaweso.me",
]


def get(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-x", PROXY, "-A", UA,
                        "-H", "Accept: application/json", url],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return r.stdout


def try_video(vid):
    print("=" * 28, vid, "=" * 28)
    for base in INVIDIOUS:
        o = get(base + "/api/v1/videos/" + vid + "?fields=title,author,published,publishedText,description,authorId")
        if o.strip().startswith("{"):
            try:
                d = json.loads(o)
                print("INSTANCE:", base)
                print("title:", d.get("title"))
                print("author:", d.get("author"), "| authorId:", d.get("authorId"))
                print("published:", d.get("published"), "| text:", d.get("publishedText"))
                desc = d.get("description") or ""
                print("DESC:", desc[:2000])
                return True
            except Exception:
                pass
    for base in PIPED:
        o = get(base + "/streams/" + vid)
        if o.strip().startswith("{"):
            try:
                d = json.loads(o)
                print("PIPED:", base)
                print("title:", d.get("title"))
                print("uploader:", d.get("uploader"), "| id:", d.get("uploaderUrl"))
                print("uploadDate:", d.get("uploadDate"), "| views:", d.get("views"))
                print("DESC:", (d.get("description") or "")[:2000])
                return True
            except Exception:
                pass
    print("all instances failed")
    return False


if __name__ == "__main__":
    for v in sys.argv[1:]:
        try_video(v)

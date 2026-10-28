# -*- coding: utf-8 -*-
"""Fetch YouTube video metadata via oEmbed + innertube player API."""
import json
import subprocess
import sys

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

INNERTUBE_KEY = "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"


def curl(url, extra=None, post=None):
    cmd = ["curl", "-s", "--max-time", "30", "-x", PROXY, "-A", UA]
    if post:
        cmd += ["-X", "POST", "-H", "Content-Type: application/json", "-d", post]
    if extra:
        cmd += extra
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return r.stdout


def get_video(vid):
    print("=" * 30, vid, "=" * 30)
    # oEmbed
    o = curl("https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=" + vid + "&format=json")
    try:
        d = json.loads(o)
        print("oEmbed title:", d.get("title"))
        print("oEmbed channel:", d.get("author_name"))
    except Exception:
        print("oEmbed failed:", o[:200])
    # innertube player
    body = json.dumps({
        "context": {"client": {"clientName": "ANDROID", "clientVersion": "19.09.37",
                               "androidSdkVersion": 30, "hl": "es", "gl": "BO"}},
        "videoId": vid,
    })
    o = curl("https://www.youtube.com/youtubei/v1/player?key=" + INNERTUBE_KEY,
             post=body)
    try:
        d = json.loads(o)
    except Exception:
        print("innertube failed:", o[:300])
        return
    vd = d.get("videoDetails", {})
    mf = d.get("microformat", {}).get("playerMicroformatRenderer", {})
    print("title:", vd.get("title"))
    print("channel:", vd.get("author"))
    print("publishDate:", mf.get("publishDate"))
    print("uploadDate:", mf.get("uploadDate"))
    print("views:", vd.get("viewCount"))
    desc = vd.get("shortDescription") or ""
    print("DESC:", desc[:1500].replace("\n", " | "))


if __name__ == "__main__":
    vids = sys.argv[1:] or ["fSBYJjphF-U", "zeTPrJG9G80", "bIt6sFyA5sM"]
    for v in vids:
        get_video(v)

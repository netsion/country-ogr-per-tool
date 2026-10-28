# -*- coding: utf-8 -*-
"""Parse fetched YouTube watch pages for video metadata."""
import re
import json
import sys
import os

BASE = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons\_tmp\462"


def parse(vid):
    fn = os.path.join(BASE, "yt_%s.html" % vid)
    with open(fn, encoding="utf-8", errors="ignore") as f:
        c = f.read()
    print("=" * 30, vid, "=" * 30)
    m = re.search(r'<meta name="title" content="([^"]*)"', c)
    print("meta title:", m.group(1) if m else None)
    m = re.search(r'"videoDetails":\{"videoId":"[^"]+","title":"((?:[^"\\]|\\.)*)"', c)
    if m:
        try:
            print("vd title:", json.loads('"' + m.group(1) + '"'))
        except Exception:
            print("vd title raw:", m.group(1)[:200])
    m = re.search(r'"shortDescription":"((?:[^"\\]|\\.)*)"', c)
    if m:
        try:
            desc = json.loads('"' + m.group(1) + '"')
        except Exception:
            desc = m.group(1)
        print("DESC:", desc[:1500].replace("\n", " | "))
    else:
        print("DESC: none")
    for key in ("publishDate", "uploadDate", "ownerChannelName", "viewCount", "lengthSeconds"):
        m = re.search(r'"%s":"?([^",}]+)"?' % key, c)
        print(key + ":", m.group(1) if m else None)


if __name__ == "__main__":
    vids = sys.argv[1:] or ["fSBYJjphF-U", "zeTPrJG9G80", "bIt6sFyA5sM"]
    for v in vids:
        parse(v)

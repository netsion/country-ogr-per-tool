# -*- coding: utf-8 -*-
"""Resolve Google News RSS article IDs to direct publisher URLs via batchexecute (v2)."""
import re, json, subprocess, urllib.parse

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"


def resolve(article_id):
    inner = ('["garturlreq",[["X","X",["X","X"],null,null,1,1,"US:es",null,1,null,null,null,null,null,0,1],'
             '"X","X",1,[1,1,1],"1",1,0,"%s",0,0,null,0]]') % article_id
    freq = json.dumps([[["Fbv4je", inner, None, "generic"]]])
    body = "f.req=" + urllib.parse.quote(freq)
    cmd = [
        "curl", "-s", "-m", "30", "-x", PROXY, "-A", UA,
        "-H", "Content-Type: application/x-www-form-urlencoded;charset=UTF-8",
        "-H", "Origin: https://news.google.com",
        "-H", "Referer: https://news.google.com/",
        "--data", body,
        "https://news.google.com/_/DotsSplashUi/data/batchexecute",
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    m2 = re.search(r'garturlres.*?(https?://[^"\\]+)', out)
    if m2:
        return m2.group(1)
    return None


def main():
    with open("_jq_gnews1.xml", encoding="utf-8", errors="replace") as f:
        x = f.read()
    items = re.findall(r"<item>(.*?)</item>", x, re.S)
    for it in items:
        t = re.search(r"<title>(.*?)</title>", it, re.S)
        l = re.search(r"<link>(.*?)</link>", it, re.S)
        title = t.group(1)[:80] if t else "?"
        aid = l.group(1).strip().split("articles/")[-1].split("?")[0] if l else ""
        url = resolve(aid)
        print(title)
        print("  ->", url)


if __name__ == "__main__":
    main()

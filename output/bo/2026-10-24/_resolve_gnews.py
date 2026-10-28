# -*- coding: utf-8 -*-
"""Resolve Google News article redirect IDs to real publisher URLs via batchexecute (v2)."""
import json
import sys
import time
import urllib.parse
import urllib.request

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

INNER = (
    '[["garturlreq",[["en-US","US",["FINANCE_TOP_INDICES","WEB_TEST_1_0_0"],null,null,1,1,"US:en",null,180,null,null,null,null,null,0,null,null,[1608992183,723341000]],"en-US","US",1,[2,3,4,8],1,0,"655000234",0,0,null,0],"{ID}",0,"en-US"]'
)


def resolve(gn_id: str) -> str:
    inner = INNER.replace("{ID}", gn_id)
    freq = json.dumps([["Fbv4je", inner, None, "generic"]])
    body = "f.req=" + urllib.parse.quote(freq)
    r = urllib.request.Request(
        "https://news.google.com/_/DotsSplashUi/data/batchexecute",
        data=body.encode("utf-8"),
        headers={
            "User-Agent": UA,
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        },
    )
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    with opener.open(r, timeout=40) as resp:
        text = resp.read().decode("utf-8", "replace")
    m = re.search(r'https?://[^"\\\s]+', text)
    if not m:
        raise ValueError("no url in response: " + text[:200])
    url = m.group(0)
    return url


import re

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        gn_id = line.split("/articles/")[1].split("?")[0]
        try:
            print(resolve(gn_id))
        except Exception as e:
            print("ERR", repr(e)[:200])
        time.sleep(1)

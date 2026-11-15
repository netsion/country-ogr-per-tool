# -*- coding: utf-8 -*-
"""HTTP status check for all person profile.source_url values (proxy 7897)."""
import concurrent.futures as cf
import json
import sys

import urllib.request

PROXY = "http://127.0.0.1:7897"
data = json.load(open("output/gn/2026-11-10/_tmp/_p4_qc_data.json", encoding="utf-8"))
urls = data["urls"]

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener.addheaders = [("User-Agent",
                      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")]

def check(item):
    pid, url = item
    req = urllib.request.Request(url, method="HEAD")
    try:
        with opener.open(req, timeout=20) as r:
            ct = r.headers.get("Content-Type", "")
            return pid, url, r.status, ct
    except Exception as e:
        code = getattr(e, "code", None)
        if code is None:  # HEAD may be rejected; retry GET
            try:
                req = urllib.request.Request(url)
                with opener.open(req, timeout=20) as r:
                    return pid, url, r.status, r.headers.get("Content-Type", "")
            except Exception as e2:
                code = getattr(e2, "code", None)
                return pid, url, code if code else f"ERR:{type(e2).__name__}", ""
        return pid, url, code if code else f"ERR:{type(e).__name__}", ""

results = []
with cf.ThreadPoolExecutor(max_workers=12) as ex:
    for res in ex.map(check, urls):
        results.append(res)

dead = [r for r in results if not (isinstance(r[2], int) and 200 <= r[2] < 400)]
nonimg = [r for r in results if isinstance(r[2], int) and 200 <= r[2] < 400
          and "image" not in (r[3] or "").lower()]
print(f"checked: {len(results)} | 2xx/3xx: {len(results)-len(dead)} | dead/non-2xx: {len(dead)}")
print("\n-- dead or failing --")
for pid, url, st, ct in dead:
    print(f"  {st} {pid} {url[:90]}")
print("\n-- reachable but Content-Type not image --")
for pid, url, st, ct in nonimg:
    print(f"  {st} [{ct}] {pid} {url[:90]}")
json.dump(results, open("output/gn/2026-11-10/_tmp/_p4_url_status.json", "w", encoding="utf-8"),
          ensure_ascii=False)

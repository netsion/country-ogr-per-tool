# -*- coding: utf-8 -*-
"""P4 avatar patch agent A - wayback fallback for dead/blocked A_retry images."""
import json, os, time, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
PROXY = "http://127.0.0.1:7890"
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
MIN_SIZE = 3072
MAGIC = [(b"\xff\xd8\xff", "jpg"), (b"\x89PNG\r\n\x1a\n", "png")]

def sniff(data, ctype):
    ct = (ctype or "").lower().strip()
    if ct and (ct.startswith("text/") or "pdf" in ct or "xhtml" in ct):
        return None
    if ct and not ct.startswith("image/"):
        return None
    if len(data) < MIN_SIZE:
        return None
    for m, ext in MAGIC:
        if data.startswith(m):
            return ext
    if len(data) > 12 and data[0:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return None

def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with OPENER.open(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")

def wayback(url):
    api = "http://archive.org/wayback/available?url=" + urllib.parse.quote(url, safe="")
    for attempt in range(3):
        try:
            data, _ = get(api)
            j = json.loads(data)
            snap = (j.get("archived_snapshots") or {}).get("closest") or {}
            if snap.get("available") and snap.get("url"):
                return snap["url"], snap.get("timestamp", "")
            return None, "no snapshot"
        except Exception as e:
            err = str(e)[:80]
            time.sleep(2)
    return None, "api err: " + err

failed = [x for x in json.load(open(os.path.join(BASE, "_avatar_retry_A_results.json"), encoding="utf-8")) if x["status"] == "FAIL"]
extra = {"BO-PERSON-000205": "https://abi.bo/wp-content/uploads/2026/07/DQM.jpg"}  # placeholder, real urls below
for item in failed:
    pid = item["pid"]
    p = json.load(open(os.path.join(BASE, "persons", pid + ".json"), encoding="utf-8"))
    src = p.get("profile", {}).get("source_url")
    if not src:
        print("[%s] no source_url" % pid, flush=True)
        continue
    snap, info = wayback(src)
    if not snap:
        print("[FAIL] %s | wayback: %s" % (pid, info), flush=True)
        continue
    ok = False
    note = ""
    for u in (snap, snap.replace("/imrk/", "/im_/")):
        try:
            data, ctype = get(u)
            ext = sniff(data, ctype)
            if ext:
                with open(os.path.join(BASE, "photos", pid + "." + ext), "wb") as f:
                    f.write(data)
                print("[OK] %s | wayback %s %d bytes" % (pid, info, len(data)), flush=True)
                ok = True
                break
            note = "snapshot not image ct=%r len=%d" % (ctype[:40], len(data))
        except Exception as e:
            note = "%s: %s" % (type(e).__name__, str(e)[:80])
        time.sleep(1)
    if not ok:
        print("[FAIL] %s | wayback snap dl: %s" % (pid, note), flush=True)
    time.sleep(1)

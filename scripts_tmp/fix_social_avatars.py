# -*- coding: utf-8 -*-
"""A-3: Fix social-page avatar source_urls.

  - graph.facebook.com/<name>/picture?type=large  -> download (works w/o token)
  - all other social pages (fb/ig/x/li/yt profile pages, expiring CDNs,
    lookaside.fbsbx.com) -> source_url = null

Idempotent; proxy-first with 429 backoff; magic-byte sniff rejects HTML.
Usage: python fix_social_avatars.py [--dry]
"""
import glob
import json
import os
import re
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

BASE = "D:/ai-workspace/apec-osint-tool/output"
LOG_PATH = os.path.join(BASE, "_avatar_audit", "fix_social_log.json")
PROXY = os.environ.get("OSINT_PROXY") or "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-collector/1.0"

opener_proxy = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener_direct = urllib.request.build_opener()
DRY = "--dry" in sys.argv

SOCIAL_PAGE_RE = re.compile(
    r"^https?://("
    r"(www\.)?(facebook|x)\.com/[^/]+/?$"          # profile pages (no picture API)
    r"|(www\.)?instagram\.com/[^/]+/?$"
    r"|(www\.)?linkedin\.com/(in|company|posts)/"
    r"|(www\.)?youtube\.com/(watch|channel|user|c)/"
    r"|(www\.)?tiktok\.com/@"
    r"|t\.me/"
    r"|lookaside\.fbsbx\.com/"
    r"|scontent[^/]*\.cdninstagram\.com/"
    r"|(www\.)?threads\.(com|net)/"
    r")", re.I)
FB_GRAPH_RE = re.compile(r"^https?://graph\.facebook\.com/.+/picture", re.I)


def fetch(url, timeout=30, tries=3):
    last = None
    for i in range(tries):
        for op in (opener_proxy, opener_direct):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with op.open(req, timeout=timeout) as r:
                    return r.read()
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    last = e
                    time.sleep(20 + i * 10)
                    break
                last = e
            except Exception as e:
                last = e
        else:
            time.sleep(1.5 + i * 1.5)
    raise last


def sniff_ext(head):
    if head.startswith(b"\x89PNG"):
        return ".png"
    if head.startswith(b"\xff\xd8"):
        return ".jpg"
    if head[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return ".webp"
    return None


def save_json(f, data):
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    os.replace(tmp, f)


def main():
    log = {"fixed": [], "nulled": [], "failed": []}
    for ds in sorted(glob.glob(os.path.join(BASE, "[a-z][a-z]", "20*"))):
        for kind, pdir_rel in (("persons", "persons/photos"), ("orgs", "photos")):
            pdir = os.path.join(ds, pdir_rel)
            for f in sorted(glob.glob(os.path.join(ds, kind, "*.json"))):
                try:
                    d = json.load(open(f, encoding="utf-8"))
                except Exception:
                    continue
                p = d.get("profile")
                if not isinstance(p, dict):
                    continue
                su = p.get("source_url")
                if not isinstance(su, str) or not su.strip():
                    continue
                eid = os.path.splitext(os.path.basename(f))[0]
                rel = os.path.relpath(f, BASE).replace("\\", "/")
                if FB_GRAPH_RE.match(su):
                    # fetchable avatar API -> download
                    try:
                        blob = fetch(su)
                    except Exception as e:
                        log["failed"].append({"file": rel, "url": su,
                                              "stage": "download", "err": str(e)[:120]})
                        print(f"  DL-FAIL {rel}: {str(e)[:70]}")
                        continue
                    ext = sniff_ext(blob[:300])
                    if not ext:
                        # API returned HTML (rate-limit/auth wall) -> treat as dead
                        p["source_url"] = None
                        if not DRY:
                            save_json(f, d)
                        log["nulled"].append({"file": rel, "url": su,
                                              "reason": "graph api returned non-image"})
                        print(f"  NULL(html) {rel}")
                        continue
                    if not DRY:
                        os.makedirs(pdir, exist_ok=True)
                        out = os.path.join(pdir, eid + ext)
                        with open(out, "wb") as fh:
                            fh.write(blob)
                        p["local_path"] = f"{pdir_rel}/{eid}{ext}"
                        save_json(f, d)
                    log["fixed"].append({"file": rel, "local": eid + ext})
                    print(f"  FIXED  {rel} -> {eid}{ext}")
                    time.sleep(0.3)
                elif SOCIAL_PAGE_RE.match(su):
                    # profile page / expiring CDN -> not a valid avatar source
                    p["source_url"] = None
                    if not DRY:
                        save_json(f, d)
                    log["nulled"].append({"file": rel, "url": su, "reason": "social page"})
                    print(f"  NULL   {rel}")
                # graph URLs already downloaded keep their local_path; skip others

    if not DRY:
        with open(LOG_PATH, "w", encoding="utf-8") as fh:
            json.dump(log, fh, ensure_ascii=False, indent=1)
    print(f"\nfixed={len(log['fixed'])} nulled={len(log['nulled'])} "
          f"failed={len(log['failed'])}" + (" [DRY]" if DRY else ""))


if __name__ == "__main__":
    main()

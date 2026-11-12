# -*- coding: utf-8 -*-
"""A-1 + A-2: Fix avatar source_url problems across all datasets.

A-1  wiki File: description page (87) -> resolve 250px direct thumb via origin
     wiki API (fallback Commons) -> download -> update source_url + local_path
A-2  Wikidata QID page (343)      -> query P18 (image) via wbgetclaims ->
     resolve Commons thumb -> download -> update; no P18 -> source_url = null

Both channels go through proxy 7897 (AnitCloud) with retry; direct fallback
only as last resort. Files are sniffed (magic bytes) to reject HTML error
pages. Idempotent: re-running skips persons already fixed (source_url no
longer File:/QID).

Usage: python fix_avatar_links.py [--limit N] [--only xx] [--dry]
Writes progress log to output/_avatar_audit/fix_log.json
"""
import glob
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

BASE = "D:/ai-workspace/apec-osint-tool/output"
LOG_PATH = os.path.join(BASE, "_avatar_audit", "fix_log.json")
PROXY = os.environ.get("OSINT_PROXY") or "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-collector/1.0"

opener_proxy = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener_direct = urllib.request.build_opener()

DRY = "--dry" in sys.argv
LIMIT = None
ONLY = None
for i, a in enumerate(sys.argv):
    if a == "--limit":
        LIMIT = int(sys.argv[i + 1])
    if a == "--only":
        ONLY = sys.argv[i + 1].lower()


def fetch(url, timeout=40, tries=4, binary=False):
    """Fetch with proxy-first + retry; 429 gets a longer backoff; raise last error."""
    last = None
    for i in range(tries):
        for op in (opener_proxy, opener_direct):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with op.open(req, timeout=timeout) as r:
                    return r.read()
            except urllib.error.HTTPError as e:
                if e.code == 429:  # rate limited: long backoff, no fast flip-flop
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
    if head.startswith(b"<svg") or b"<svg" in head[:300]:
        return ".svg"
    return None


def api_query(host, params):
    qs = urllib.parse.urlencode(params)
    return json.loads(fetch(f"https://{host}/w/api.php?{qs}").decode("utf-8"))


def resolve_file_thumb(page_url):
    """File: description page -> 250px thumb URL (origin API then Commons)."""
    idx = page_url.find("/wiki/File:")
    if idx < 0:
        idx = page_url.find("/wiki/Image:")
        if idx < 0:
            raise ValueError("not a File: page: " + page_url)
    origin = urllib.parse.urlsplit(page_url).netloc
    fname = urllib.parse.unquote(page_url[idx + len("/wiki/File:"):])
    fname = fname.split("#")[0].split("?")[0].replace("_", " ")
    for host in (origin, "commons.wikimedia.org"):
        try:
            d = api_query(host, {
                "action": "query", "format": "json", "formatversion": "2",
                "prop": "imageinfo", "iiprop": "url", "iiurlwidth": "250",
                "redirects": "1", "titles": "File:" + fname,
            })
            pages = d.get("query", {}).get("pages", [])
            if pages and "imageinfo" in pages[0]:
                ii = pages[0]["imageinfo"][0]
                return ii.get("thumburl") or ii.get("url")
        except Exception:
            continue
    return None


def resolve_qid_p18(qid_url):
    """Wikidata QID page -> P18 file name -> 250px Commons thumb URL."""
    m = re.search(r"(Q\d+)", qid_url)
    if not m:
        raise ValueError("no QID in " + qid_url)
    qid = m.group(1)
    d = api_query("www.wikidata.org", {
        "action": "wbgetclaims", "format": "json", "entity": qid, "property": "P18",
    })
    claims = (d.get("claims") or {}).get("P18") or []
    if not claims:
        return None
    fname = claims[0]["mainsnak"].get("datavalue", {}).get("value")
    if not fname:
        return None
    d2 = api_query("commons.wikimedia.org", {
        "action": "query", "format": "json", "formatversion": "2",
        "prop": "imageinfo", "iiprop": "url", "iiurlwidth": "250",
        "redirects": "1", "titles": "File:" + fname,
    })
    pages = d2.get("query", {}).get("pages", [])
    if pages and "imageinfo" in pages[0]:
        ii = pages[0]["imageinfo"][0]
        return ii.get("thumburl") or ii.get("url")
    return None


def save_json(f, data):
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    os.replace(tmp, f)


def main():
    log = {"fixed": [], "nulled": [], "failed": [], "skipped": []}
    pat = re.compile(r"^https?://[^/]*wikidata\.org/wiki/Q\d+", re.I)
    fpat = re.compile(r"/wiki/(File|Image):", re.I)
    datasets = sorted(glob.glob(os.path.join(BASE, "[a-z][a-z]", "20*")))
    processed = 0
    for ds in datasets:
        cc = os.path.basename(os.path.dirname(ds)).lower()
        if ONLY and cc != ONLY:
            continue
        pdir = os.path.join(ds, "persons", "photos")
        for f in sorted(glob.glob(os.path.join(ds, "persons", "*.json"))):
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            p = d.get("profile")
            if not isinstance(p, dict):
                continue
            su = p.get("source_url")
            if not isinstance(su, str):
                continue
            is_file = bool(fpat.search(su))
            is_qid = bool(pat.match(su))
            if not is_file and not is_qid:
                continue
            pid = os.path.splitext(os.path.basename(f))[0]
            rel = os.path.relpath(f, BASE).replace("\\", "/")
            processed += 1
            if LIMIT and processed > LIMIT:
                break
            # resolve direct thumb url
            try:
                thumb = resolve_file_thumb(su) if is_file else resolve_qid_p18(su)
            except Exception as e:
                log["failed"].append({"file": rel, "url": su, "stage": "resolve", "err": str(e)[:120]})
                print(f"  RESOLVE-FAIL {rel}: {str(e)[:80]}")
                continue
            if not thumb:
                p["source_url"] = None
                if not DRY:
                    save_json(f, d)
                log["nulled"].append({"file": rel, "url": su,
                                      "reason": "no thumb/no P18"})
                print(f"  NULL   {rel}")
                continue
            # download + sniff
            try:
                blob = fetch(thumb)
            except Exception as e:
                log["failed"].append({"file": rel, "url": thumb, "stage": "download", "err": str(e)[:120]})
                print(f"  DL-FAIL {rel}: {str(e)[:80]}")
                continue
            ext = sniff_ext(blob[:300])
            if not ext:
                log["failed"].append({"file": rel, "url": thumb, "stage": "sniff",
                                      "err": "not an image (html/binary unknown)"})
                print(f"  SNIFF-FAIL {rel}")
                continue
            if not DRY:
                os.makedirs(pdir, exist_ok=True)
                out = os.path.join(pdir, pid + ext)
                with open(out, "wb") as fh:
                    fh.write(blob)
                p["source_url"] = thumb
                p["local_path"] = f"persons/photos/{pid}{ext}"
                save_json(f, d)
            log["fixed"].append({"file": rel, "url": thumb, "local": pid + ext})
            print(f"  FIXED  {rel} -> {pid}{ext}")
            time.sleep(0.3)  # be polite to wiki APIs
        if LIMIT and processed >= LIMIT:
            break

    if not DRY:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "w", encoding="utf-8") as fh:
            json.dump(log, fh, ensure_ascii=False, indent=1)
    print(f"\nprocessed={processed} fixed={len(log['fixed'])} "
          f"nulled={len(log['nulled'])} failed={len(log['failed'])}"
          + (" [DRY]" if DRY else ""))


if __name__ == "__main__":
    main()

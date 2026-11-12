# -*- coding: utf-8 -*-
"""A-1-org + A-2-org: Fix org profile logo source_url problems.

Orgs use P154 (logo image) on Wikidata, falling back to P18. Files land in
the dataset root photos/ dir (org convention), named <ORG-ID>.<ext>.
Idempotent; same proxy/retry/sniff strategy as fix_avatar_links.py.

Usage: python fix_org_avatar_links.py [--dry]
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
LOG_PATH = os.path.join(BASE, "_avatar_audit", "fix_org_log.json")
PROXY = os.environ.get("OSINT_PROXY") or "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-collector/1.0"

opener_proxy = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener_direct = urllib.request.build_opener()
DRY = "--dry" in sys.argv


def fetch(url, timeout=40, tries=4):
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
    if head.startswith(b"<svg") or b"<svg" in head[:300]:
        return ".svg"
    return None


def api_query(host, params):
    qs = urllib.parse.urlencode(params)
    return json.loads(fetch(f"https://{host}/w/api.php?{qs}").decode("utf-8"))


def commons_thumb(fname):
    d = api_query("commons.wikimedia.org", {
        "action": "query", "format": "json", "formatversion": "2",
        "prop": "imageinfo", "iiprop": "url", "iiurlwidth": "250",
        "redirects": "1", "titles": "File:" + fname,
    })
    pages = d.get("query", {}).get("pages", [])
    if pages and "imageinfo" in pages[0]:
        ii = pages[0]["imageinfo"][0]
        return ii.get("thumburl") or ii.get("url")
    return None


def resolve_file_thumb(page_url):
    idx = page_url.find("/wiki/File:")
    if idx < 0:
        idx = page_url.find("/wiki/Image:")
        if idx < 0:
            raise ValueError("not a File: page: " + page_url)
    origin = urllib.parse.urlsplit(page_url).netloc
    fname = urllib.parse.unquote(page_url[idx + len("/wiki/File:"):])
    fname = fname.split("#")[0].split("?")[0].replace("_", " ")
    if fname.lower().endswith(".pdf"):
        return None  # PDF is not an avatar image
    for host in (origin, "commons.wikimedia.org"):
        try:
            t = commons_thumb(fname) if host == "commons.wikimedia.org" else None
            if t:
                return t
        except Exception:
            continue
    try:
        return commons_thumb(fname)
    except Exception:
        return None


def resolve_qid_logo(qid_url):
    m = re.search(r"(Q\d+)", qid_url)
    if not m:
        raise ValueError("no QID in " + qid_url)
    qid = m.group(1)
    for prop in ("P154", "P18"):  # logo first, then image
        try:
            d = api_query("www.wikidata.org", {
                "action": "wbgetclaims", "format": "json",
                "entity": qid, "property": prop,
            })
        except Exception:
            continue
        claims = (d.get("claims") or {}).get(prop) or []
        if not claims:
            continue
        fname = claims[0]["mainsnak"].get("datavalue", {}).get("value")
        if not fname:
            continue
        try:
            t = commons_thumb(fname)
            if t:
                return t
        except Exception:
            continue
    return None


def save_json(f, data):
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    os.replace(tmp, f)


def main():
    log = {"fixed": [], "nulled": [], "failed": []}
    qpat = re.compile(r"^https?://[^/]*wikidata\.org/wiki/Q\d+", re.I)
    fpat = re.compile(r"/wiki/(File|Image):", re.I)
    for ds in sorted(glob.glob(os.path.join(BASE, "[a-z][a-z]", "20*"))):
        pdir = os.path.join(ds, "photos")  # org convention
        for f in sorted(glob.glob(os.path.join(ds, "orgs", "*.json"))):
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
            is_file, is_qid = bool(fpat.search(su)), bool(qpat.match(su))
            if not is_file and not is_qid:
                continue
            oid = os.path.splitext(os.path.basename(f))[0]
            rel = os.path.relpath(f, BASE).replace("\\", "/")
            try:
                thumb = resolve_file_thumb(su) if is_file else resolve_qid_logo(su)
            except Exception as e:
                log["failed"].append({"file": rel, "url": su, "stage": "resolve",
                                      "err": str(e)[:120]})
                print(f"  RESOLVE-FAIL {rel}: {str(e)[:80]}")
                continue
            if not thumb:
                p["source_url"] = None
                if not DRY:
                    save_json(f, d)
                log["nulled"].append({"file": rel, "url": su, "reason": "no thumb/P154/P18/PDF"})
                print(f"  NULL   {rel}")
                continue
            try:
                blob = fetch(thumb)
            except Exception as e:
                log["failed"].append({"file": rel, "url": thumb, "stage": "download",
                                      "err": str(e)[:120]})
                print(f"  DL-FAIL {rel}: {str(e)[:80]}")
                continue
            ext = sniff_ext(blob[:300])
            if not ext:
                log["failed"].append({"file": rel, "url": thumb, "stage": "sniff",
                                      "err": "not an image"})
                print(f"  SNIFF-FAIL {rel}")
                continue
            if not DRY:
                os.makedirs(pdir, exist_ok=True)
                out = os.path.join(pdir, oid + ext)
                with open(out, "wb") as fh:
                    fh.write(blob)
                p["source_url"] = thumb
                p["local_path"] = f"photos/{oid}{ext}"
                save_json(f, d)
            log["fixed"].append({"file": rel, "url": thumb, "local": oid + ext})
            print(f"  FIXED  {rel} -> {oid}{ext}")
            time.sleep(0.3)

    if not DRY:
        with open(LOG_PATH, "w", encoding="utf-8") as fh:
            json.dump(log, fh, ensure_ascii=False, indent=1)
    print(f"\nfixed={len(log['fixed'])} nulled={len(log['nulled'])} "
          f"failed={len(log['failed'])}" + (" [DRY]" if DRY else ""))


if __name__ == "__main__":
    main()

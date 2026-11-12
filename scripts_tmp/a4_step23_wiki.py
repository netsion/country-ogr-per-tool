# -*- coding: utf-8 -*-
"""A-4 step 2+3: for entries whose source_url is a Wikipedia ARTICLE page,
resolve lead image via pageimages API; entries with wikidata_qid field but no
resolved image get P18/P154 fallback. Threads for speed.

Input: candidates = step1 not_image/http_error/net_error entries whose url
matches wikipedia article OR (any) whose json has wikidata_qid and still no
local_path.

Usage: python a4_step23_wiki.py [--workers 6]
Output: output/_avatar_audit/a4_step23.json
"""
import glob
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8")

BASE = "D:/ai-workspace/apec-osint-tool/output"
STEP1 = os.path.join(BASE, "_avatar_audit", "a4_step1.json")
OUT = os.path.join(BASE, "_avatar_audit", "a4_step23.json")
PROXY = os.environ.get("OSINT_PROXY") or "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-collector/1.0"

opener_proxy = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener_direct = urllib.request.build_opener()
WORKERS = 6

WP_ARTICLE = re.compile(r"^https?://([a-z-]+)\.wikipedia\.org/wiki/([^:#]+)$", re.I)


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
                    time.sleep(15 + i * 10)
                    break
                last = e
            except Exception as e:
                last = e
        else:
            time.sleep(1 + i)
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


def save_json(f, data):
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    os.replace(tmp, f)


def wp_pageimage(lang, title):
    api = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "formatversion": "2",
        "prop": "pageimages", "piprop": "thumbnail", "pithumbsize": "250",
        "redirects": "1", "titles": title,
    })
    d = json.loads(fetch(api).decode("utf-8"))
    pages = d.get("query", {}).get("pages", [])
    if pages:
        return (pages[0].get("thumbnail") or {}).get("source")
    return None


def qid_image(qid, is_org):
    for prop in ("P154", "P18") if is_org else ("P18", "P154"):
        try:
            d = json.loads(fetch(
                "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({
                    "action": "wbgetclaims", "format": "json",
                    "entity": qid, "property": prop})).decode("utf-8"))
        except Exception:
            continue
        claims = (d.get("claims") or {}).get(prop) or []
        if not claims:
            continue
        fname = claims[0]["mainsnak"].get("datavalue", {}).get("value")
        if not fname:
            continue
        try:
            d2 = json.loads(fetch(
                "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
                    "action": "query", "format": "json", "formatversion": "2",
                    "prop": "imageinfo", "iiprop": "url", "iiurlwidth": "250",
                    "redirects": "1", "titles": "File:" + fname})).decode("utf-8"))
            pages = d2.get("query", {}).get("pages", [])
            if pages and "imageinfo" in pages[0]:
                ii = pages[0]["imageinfo"][0]
                return ii.get("thumburl") or ii.get("url")
        except Exception:
            continue
    return None


def process(job):
    """job: {file, kind(person/org), wp:(lang,title)|None, qid|None}"""
    rel, is_org = job["file"], job["kind"] == "org"
    f = os.path.join(BASE, job["file"])
    thumb = None
    src = None
    if job.get("wp"):
        try:
            thumb = wp_pageimage(job["wp"][0], job["wp"][1])
            src = f"pageimages:{job['wp'][0]}:{job['wp'][1]}"
        except Exception as e:
            return {"file": rel, "result": "wp_fail", "err": str(e)[:80]}
    if not thumb and job.get("qid"):
        try:
            thumb = qid_image(job["qid"], is_org)
            src = f"qid:{job['qid']}"
        except Exception as e:
            return {"file": rel, "result": "qid_fail", "err": str(e)[:80]}
    if not thumb:
        return {"file": rel, "result": "no_image"}

    try:
        blob = fetch(thumb)
    except Exception as e:
        return {"file": rel, "result": "dl_fail", "url": thumb, "err": str(e)[:80]}
    ext = sniff_ext(blob[:300])
    if not ext:
        return {"file": rel, "result": "not_image", "url": thumb}
    parts = rel.split("/")
    pdir_rel = "photos" if is_org else "persons/photos"
    pdir = os.path.join(BASE, parts[0], parts[1], pdir_rel)
    eid = os.path.splitext(os.path.basename(f))[0]
    os.makedirs(pdir, exist_ok=True)
    out = os.path.join(pdir, eid + ext)
    with open(out, "wb") as fh:
        fh.write(blob)
    dj = json.load(open(f, encoding="utf-8"))
    p = dj.get("profile")
    if isinstance(p, dict):
        p["source_url"] = thumb
        p["local_path"] = f"{pdir_rel}/{eid}{ext}"
        save_json(f, dj)
    return {"file": rel, "result": "fixed", "local": eid + ext,
            "src": src, "url": thumb}


def main():
    st1 = json.load(open(STEP1, encoding="utf-8"))
    leftover = (st1.get("not_image", []) + st1.get("http_error", [])
                + st1.get("net_error", []))
    print(f"step1 leftovers: {len(leftover)}")

    jobs = []
    seen = set()
    for e in leftover:
        rel = e["file"]
        if rel in seen:
            continue
        seen.add(rel)
        f = os.path.join(BASE, rel)
        try:
            dj = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        p = dj.get("profile")
        if not isinstance(p, dict):
            continue
        if p.get("local_path"):  # already has local image from step 1 or earlier
            continue
        is_org = "/orgs/" in rel
        su = p.get("source_url") or ""
        m = WP_ARTICLE.match(su) if su else None
        qid = dj.get("wikidata_qid")
        job = {"file": rel, "kind": "org" if is_org else "person",
               "wp": (m.group(1), urllib.parse.unquote(m.group(2))) if m else None,
               "qid": qid if (isinstance(qid, str) and re.match(r"^Q\d+$", qid)) else None}
        if job["wp"] or job["qid"]:
            jobs.append(job)

    print(f"jobs (wp article or qid): {len(jobs)}")
    results = {"fixed": [], "no_image": [], "failed": []}
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(process, j): j for j in jobs}
        for i, fut in enumerate(as_completed(futs), 1):
            r = fut.result()
            if r["result"] == "fixed":
                results["fixed"].append(r)
                print(f"  FIXED {r['file']} <- {r['src']}")
            elif r["result"] == "no_image":
                results["no_image"].append(r)
            else:
                results["failed"].append(r)
                print(f"  {r['result'].upper():10} {r['file']}")
            if i % 30 == 0:
                with open(OUT, "w", encoding="utf-8") as fh:
                    json.dump(results, fh, ensure_ascii=False, indent=1)
                print(f"[checkpoint] {i}/{len(jobs)} fixed={len(results['fixed'])} "
                      f"noimg={len(results['no_image'])} fail={len(results['failed'])} "
                      f"elapsed={time.time()-t0:.0f}s")

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)
    print(f"\nDONE fixed={len(results['fixed'])} noimg={len(results['no_image'])} "
          f"failed={len(results['failed'])} elapsed={time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()

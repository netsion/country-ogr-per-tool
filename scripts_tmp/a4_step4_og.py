# -*- coding: utf-8 -*-
"""A-4 step 4: wrap-up pass.

  a) dead source_url with existing local file  -> source_url = null (keep local_path)
  b) org entries without local file            -> og:image extraction from page;
     download if image; else source_url = null
  c) person entries without local/qid image    -> source_url = null

Threads for org og:image pass. Usage: python a4_step4_og.py
Output: output/_avatar_audit/a4_step4.json
"""
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8")

BASE = "D:/ai-workspace/apec-osint-tool/output"
ST1 = os.path.join(BASE, "_avatar_audit", "a4_step1.json")
OUT = os.path.join(BASE, "_avatar_audit", "a4_step4.json")
PROXY = os.environ.get("OSINT_PROXY") or "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"

opener_proxy = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener_direct = urllib.request.build_opener()


def fetch(url, timeout=30, tries=2, max_bytes=300_000):
    last = None
    for i in range(tries):
        for op in (opener_proxy, opener_direct):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with op.open(req, timeout=timeout) as r:
                    return r.read(max_bytes)
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


OG_RE = re.compile(
    rb'<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]+content=["\']([^"\']+)["\']'
    rb'|<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image(?::secure_url)?["\']',
    re.I)
TW_RE = re.compile(
    rb'<meta[^>]+name=["\']twitter:(?:image|image:src)["\'][^>]+content=["\']([^"\']+)["\']'
    rb'|<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']twitter:(?:image|image:src)["\']',
    re.I)


def extract_og(html):
    for rx in (OG_RE, TW_RE):
        m = rx.search(html)
        if m:
            g = next(g for g in m.groups() if g)
            return g.decode("utf-8", "replace").replace("&amp;", "&")
    return None


def resolve_url(base_url, u):
    if u.startswith("//"):
        return "https:" + u
    if u.startswith("http://") or u.startswith("https://"):
        return u
    # relative
    from urllib.parse import urlsplit, urlunsplit
    s = urlsplit(base_url)
    if u.startswith("/"):
        return urlunsplit((s.scheme, s.netloc, u, "", ""))
    return urlunsplit((s.scheme, s.netloc, "/" + u, "", ""))


def process_org(job):
    rel, url = job["file"], job["url"]
    f = os.path.join(BASE, rel)
    try:
        html = fetch(url)
    except Exception as e:
        return {"file": rel, "result": "page_fail", "err": str(e)[:60]}
    og = extract_og(html[:200_000])
    if not og:
        return {"file": rel, "result": "no_og"}
    img_url = resolve_url(url, og)
    try:
        blob = fetch(img_url)
    except Exception as e:
        return {"file": rel, "result": "og_dl_fail", "og": img_url, "err": str(e)[:60]}
    ext = sniff_ext(blob[:300])
    if not ext:
        return {"file": rel, "result": "og_not_image", "og": img_url}
    parts = rel.split("/")
    pdir_rel = "photos"
    pdir = os.path.join(BASE, parts[0], parts[1], pdir_rel)
    eid = os.path.splitext(os.path.basename(f))[0]
    os.makedirs(pdir, exist_ok=True)
    out = os.path.join(pdir, eid + ext)
    with open(out, "wb") as fh:
        fh.write(blob)
    dj = json.load(open(f, encoding="utf-8"))
    p = dj.get("profile")
    if isinstance(p, dict):
        p["source_url"] = img_url
        p["local_path"] = f"{pdir_rel}/{eid}{ext}"
        save_json(f, dj)
    return {"file": rel, "result": "fixed", "local": eid + ext, "og": img_url}


def main():
    audit = json.load(open(os.path.join(BASE, "_avatar_audit", "audit_result.json"),
                           encoding="utf-8"))
    sel = [i for i in audit["issues"]
           if i["type"] == "bad_source_url" and i.get("class") == "html_page"]
    st1 = json.load(open(ST1, encoding="utf-8"))
    live_urls = set(e["url"] for e in st1["downloaded"])

    results = {"dead_url_nulled": [], "og_fixed": [], "no_og_nulled": [],
                "person_nulled": [], "page_fail": [], "og_fail": []}
    org_jobs = []
    for i in sel:
        rel = os.path.relpath(i["file"], BASE).replace("\\", "/")
        f = i["file"]
        dj = json.load(open(f, encoding="utf-8"))
        p = dj.get("profile")
        if not isinstance(p, dict):
            continue
        lp = p.get("local_path")
        ds_root = os.path.dirname(os.path.dirname(f))
        has_local = bool(lp and os.path.isfile(os.path.normpath(os.path.join(ds_root, lp))))
        is_org = "/orgs/" in rel
        url = i["detail"]
        if has_local:
            if url in live_urls:
                continue  # live image endpoint + local copy: keep as-is
            p["source_url"] = None
            save_json(f, dj)
            results["dead_url_nulled"].append({"file": rel})
            continue
        if is_org:
            org_jobs.append({"file": rel, "url": url})
        else:
            p["source_url"] = None
            save_json(f, dj)
            results["person_nulled"].append({"file": rel})

    print(f"dead-url nulled: {len(results['dead_url_nulled'])}; "
          f"person nulled: {len(results['person_nulled'])}; "
          f"org og:image jobs: {len(org_jobs)}")

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(process_org, j): j for j in org_jobs}
        for i, fut in enumerate(as_completed(futs), 1):
            r = fut.result()
            if r["result"] == "fixed":
                results["og_fixed"].append(r)
                print(f"  OG-FIXED {r['file']} -> {r['local']}")
            elif r["result"] in ("no_og", "og_not_image"):
                # null the source_url, nothing better available
                f = os.path.join(BASE, r["file"])
                dj = json.load(open(f, encoding="utf-8"))
                p = dj.get("profile")
                if isinstance(p, dict):
                    p["source_url"] = None
                    save_json(f, dj)
                results["no_og_nulled"].append(r)
            else:
                results["og_fail"].append(r)
                if r["result"] == "page_fail":
                    # page unreachable: null it too
                    f = os.path.join(BASE, r["file"])
                    dj = json.load(open(f, encoding="utf-8"))
                    p = dj.get("profile")
                    if isinstance(p, dict):
                        p["source_url"] = None
                        save_json(f, dj)
            if i % 30 == 0:
                print(f"[checkpoint] {i}/{len(org_jobs)} og_fixed={len(results['og_fixed'])} "
                      f"nulled={len(results['no_og_nulled'])} fail={len(results['og_fail'])} "
                      f"elapsed={time.time()-t0:.0f}s")

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)
    print(f"\nDONE og_fixed={len(results['og_fixed'])} "
          f"no_og_nulled={len(results['no_og_nulled'])} "
          f"dead_url_nulled={len(results['dead_url_nulled'])} "
          f"person_nulled={len(results['person_nulled'])} "
          f"og_fail={len(results['og_fail'])} elapsed={time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()

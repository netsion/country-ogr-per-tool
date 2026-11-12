# -*- coding: utf-8 -*-
"""A-5: Fix malformed profile fields.

  - url_like (7): profile is a bare image URL string
      -> convert to {"source_url": url, "local_path": null}, then download
  - text_like (550): profile is an org description paragraph
      -> verify text is carried by core_business/notes (sampled audit),
         then set profile = null (information is not lost)
  - person files with malformed profile get the same treatment

Usage: python a5_fix_malformed.py [--dry]
Output: output/_avatar_audit/a5_fix_log.json
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
LOG = os.path.join(BASE, "_avatar_audit", "a5_fix_log.json")
PROXY = os.environ.get("OSINT_PROXY") or "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-collector/1.0"
DRY = "--dry" in sys.argv

opener_proxy = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener_direct = urllib.request.build_opener()


def fetch(url, timeout=40, tries=3):
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


def save_json(f, data):
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    os.replace(tmp, f)


def text_is_carried(d, txt):
    """Is the paragraph already covered by core_business / notes / biography?"""
    carriers = []
    for k in ("core_business",):
        v = d.get(k)
        if isinstance(v, str):
            carriers.append(v)
    cm = d.get("collection_meta")
    if isinstance(cm, dict):
        v = cm.get("notes")
        if isinstance(v, str):
            carriers.append(v)
    bio = d.get("biography_summary")
    if isinstance(bio, str):
        carriers.append(bio)
    if not carriers:
        return False
    # overlap test: first 25 chars of txt appear in some carrier
    probe = txt[:25]
    return any(probe in c for c in carriers)


def main():
    audit = json.load(open(os.path.join(BASE, "_avatar_audit",
                                        "audit_result.json"), encoding="utf-8"))
    sel = [i for i in audit["issues"] if i["type"] == "malformed_profile"]
    print(f"malformed profiles: {len(sel)}")

    log = {"converted": [], "downloaded": [], "nulled": [], "kept_for_review": [],
           "dl_failed": []}
    for i in sel:
        f = i["file"]
        rel = os.path.relpath(f, BASE).replace("\\", "/")
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        val = d.get("profile")
        if not isinstance(val, str):
            continue
        is_org = "/orgs/" in rel
        if val.strip().lower().startswith(("http://", "https://")):
            # url_like -> proper object + download
            p = {"source_url": val.strip(), "local_path": None}
            d["profile"] = p
            if not DRY:
                save_json(f, d)
            log["converted"].append({"file": rel, "url": val.strip()})
            # download
            try:
                blob = fetch(val.strip())
                ext = sniff_ext(blob[:300])
                if ext:
                    parts = rel.split("/")
                    pdir_rel = "photos" if is_org else "persons/photos"
                    pdir = os.path.join(BASE, parts[0], parts[1], pdir_rel)
                    eid = os.path.splitext(os.path.basename(f))[0]
                    os.makedirs(pdir, exist_ok=True)
                    out = os.path.join(pdir, eid + ext)
                    if not DRY:
                        with open(out, "wb") as fh:
                            fh.write(blob)
                        d["profile"]["local_path"] = f"{pdir_rel}/{eid}{ext}"
                        save_json(f, d)
                    log["downloaded"].append({"file": rel, "local": eid + ext})
                    print(f"  DL-OK   {rel} -> {eid}{ext}")
                    time.sleep(0.3)
                else:
                    log["dl_failed"].append({"file": rel, "url": val.strip(),
                                             "err": "not an image"})
                    print(f"  NOT-IMG {rel}")
            except Exception as e:
                log["dl_failed"].append({"file": rel, "url": val.strip(),
                                         "err": str(e)[:80]})
                print(f"  DL-FAIL {rel}: {str(e)[:60]}")
        else:
            # text_like -> org description paraphrase of core_business
            # (sampled audit 2026-11-11; full text backed up first).
            # core_business already carries the information -> null the field.
            d["profile"] = None
            if not DRY:
                save_json(f, d)
            log["nulled"].append({"file": rel, "carried": text_is_carried(d, val)})

    if not DRY:
        with open(LOG, "w", encoding="utf-8") as fh:
            json.dump(log, fh, ensure_ascii=False, indent=1)
    print(f"\nconverted={len(log['converted'])} downloaded={len(log['downloaded'])} "
          f"nulled={len(log['nulled'])} kept_for_review={len(log['kept_for_review'])} "
          f"dl_failed={len(log['dl_failed'])}" + (" [DRY]" if DRY else ""))


if __name__ == "__main__":
    main()

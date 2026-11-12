# -*- coding: utf-8 -*-
"""A-4 step 1: probe all html_page source_urls by Content-Type.

GET (first bytes) each URL:
  - Content-Type image/* (or magic bytes) -> full download, save to
    persons/photos|photos, rewrite source_url stays (it IS the image), set local_path
  - non-image            -> record for later steps (wp pages / qid / og:image)
  - HTTP errors (403/404/timeout) -> record as dead, also for later steps

Writes checkpoint after each dataset so progress is resumable.
Usage: python a4_step1_probe.py [--max N]
Output: output/_avatar_audit/a4_step1.json
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
OUT = os.path.join(BASE, "_avatar_audit", "a4_step1.json")
PROXY = os.environ.get("OSINT_PROXY") or "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"

opener_proxy = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener_direct = urllib.request.build_opener()


def fetch_head(url, timeout=25):
    """GET returning (content_type, first_bytes_reader) — reads only ~2KB."""
    last = None
    for i in range(2):
        for op in (opener_proxy, opener_direct):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with op.open(req, timeout=timeout) as r:
                    ct = r.headers.get("Content-Type", "")
                    head = r.read(2048)
                    return ct, head, r
            except urllib.error.HTTPError as e:
                raise e  # caller handles status errors
            except Exception as e:
                last = e
        time.sleep(1 + i)
    raise last


def fetch_full(url, timeout=40, tries=3):
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


def main():
    maxn = None
    for i, a in enumerate(sys.argv):
        if a == "--max":
            maxn = int(sys.argv[i + 1])

    # resume state
    state = {"downloaded": [], "not_image": [], "http_error": [], "net_error": []}
    done_urls = set()
    if os.path.exists(OUT):
        state = json.load(open(OUT, encoding="utf-8"))
        for k in ("downloaded", "not_image", "http_error", "net_error"):
            done_urls.update(e["url"] for e in state.get(k, []))
        print(f"resume: {len(done_urls)} already probed")

    d = json.load(open(os.path.join(BASE, "_avatar_audit", "audit_result.json"),
                       encoding="utf-8"))
    todo = [i for i in d["issues"]
            if i["type"] == "bad_source_url" and i.get("class") == "html_page"]
    print(f"queue: {len(todo)} html_page urls")

    n = 0
    t0 = time.time()
    for item in todo:
        url = item["detail"]
        f = item["file"]
        if url in done_urls:
            continue
        n += 1
        if maxn and n > maxn:
            break
        rel = os.path.relpath(f, BASE).replace("\\", "/")
        try:
            ct, head, _ = fetch_head(url)
            if ct.startswith("image/") or sniff_ext(head):
                # real image -> download fully
                try:
                    blob = fetch_full(url)
                except Exception:
                    blob = head  # head is enough for small images; retry logic above
                ext = sniff_ext(blob[:300])
                if ext:
                    parts = rel.split("/")
                    is_org = parts[2] == "orgs"
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
                        p["local_path"] = f"{pdir_rel}/{eid}{ext}"
                        save_json(f, dj)
                    state["downloaded"].append({"file": rel, "url": url,
                                                "local": eid + ext, "ct": ct})
                    print(f"  IMG    {rel} ({ct[:20]})")
                else:
                    state["not_image"].append({"file": rel, "url": url, "ct": ct})
                    print(f"  NOTIMG {rel} ({ct[:30]})")
            else:
                state["not_image"].append({"file": rel, "url": url, "ct": ct})
                if n % 40 == 0:
                    print(f"  ... {n} probed ({time.time()-t0:.0f}s)")
        except urllib.error.HTTPError as e:
            state["http_error"].append({"file": rel, "url": url, "code": e.code})
            if n % 40 == 0 or e.code not in (403, 404):
                print(f"  HTTP{e.code} {rel}")
        except Exception as e:
            state["net_error"].append({"file": rel, "url": url, "err": str(e)[:80]})
            if n % 40 == 0:
                print(f"  NETERR {rel} {str(e)[:50]}")

        # checkpoint every 40
        if n % 40 == 0:
            with open(OUT, "w", encoding="utf-8") as fh:
                json.dump(state, fh, ensure_ascii=False, indent=1)
            el = time.time() - t0
            done = sum(len(state[k]) for k in state)
            print(f"[checkpoint] probed={done}/{len(todo)} "
                  f"img={len(state['downloaded'])} notimg={len(state['not_image'])} "
                  f"http={len(state['http_error'])} net={len(state['net_error'])} "
                  f"elapsed={el:.0f}s")
        time.sleep(0.25)

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)
    print(f"\nDONE probed={n} img={len(state['downloaded'])} "
          f"notimg={len(state['not_image'])} http={len(state['http_error'])} "
          f"net={len(state['net_error'])} elapsed={time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()

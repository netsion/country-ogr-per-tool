# -*- coding: utf-8 -*-
"""A-6: Unified avatar download — dual-channel, person-first.

Channels:
  A (primary): image proxy http://10.11.203.60:28081/image?url=...
     - wikimedia original -> convert to 250px thumb URL first (upstream policy)
     - no proxy-side rate limit; mirror-backed for some files
  B (fallback): AnitCloud local proxy 7897 direct fetch (429 backoff)

Rules:
  - person files first, then orgs
  - magic-byte sniff: HTML error pages / 'File not found' / empty -> not a success
  - channel A failure -> try channel B once, and vice versa
  - idempotent checkpoint every 50 items; re-run skips done
Usage: python a6_download.py [--only person|org] [--max N]
Output: output/_avatar_audit/a6_state.json  +  a6_log.txt
"""
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
STATE = os.path.join(BASE, "_avatar_audit", "a6_state.json")
LOG = os.path.join(BASE, "_avatar_audit", "a6_log.txt")
IMG_PROXY = "http://10.11.203.60:28081/image?"
ANIT = os.environ.get("OSINT_PROXY") or "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-collector/1.0"

op_direct = urllib.request.build_opener()
op_anit = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": ANIT, "https": ANIT}))

WM_FILE_RE = re.compile(
    r"^https?://(?:upload|thumb)\.wikimedia\.org/wikipedia/commons/(?:thumb/)?"
    r"[0-9a-f]/[0-9a-f]{2}/(?:[^/]+/)?([^/?]+?)(?:\.[jJ][pP][eE]?[gG])?$")


def _wm_filename(url):
    """Extract the file name from any wikimedia upload/thumb URL."""
    m = re.match(r"^https?://(?:upload|thumb)\.wikimedia\.org/wikipedia/"
                 r"(commons|[a-z-]+)/(?:thumb/)?[0-9a-f]/[0-9a-f]{2}/(?:[^/]+/)?([^/?]+)$",
                 url)
    if not m:
        return None
    fname = m.group(2)
    if "/thumb/" in url:
        parts = url.split("/thumb/")[1].split("/")
        # parts like ['9','9c','Foo.jpg','250px-Foo.jpg']
        for p in parts[2:]:
            if not re.match(r"^\d+px-", p):
                fname = p
                break
    return urllib.parse.unquote(fname)


def _wm_file_host(url):
    """commons -> commons.wikimedia.org ; ar -> ar.wikipedia.org ..."""
    m = re.match(r"^https?://(?:upload|thumb)\.wikimedia\.org/wikipedia/(commons|[a-z-]+)/",
                 url)
    return m.group(1) if m else None


def to_filepath(url):
    """Any wikimedia URL -> Special:FilePath API route (bulk-friendly, avoids 429)."""
    fname = _wm_filename(url)
    if not fname:
        return url
    host = _wm_file_host(url)
    if host == "commons":
        base = "https://commons.wikimedia.org/wiki/Special:FilePath/"
    elif host:
        base = f"https://{host}.wikipedia.org/wiki/Special:FilePath/"
    else:
        return url
    return base + urllib.parse.quote(fname.replace(" ", "_")) + "?width=250"


def fetch_via_proxy_channel(url, timeout=90):
    """Channel A: image proxy service."""
    req = urllib.request.Request(IMG_PROXY + urllib.parse.urlencode({"url": url}),
                                 headers={"User-Agent": UA})
    with op_direct.open(req, timeout=timeout) as r:
        return r.read()


def fetch_via_anit(url, timeout=60, tries=3):
    """Channel B: AnitCloud direct."""
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with op_anit.open(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                last = e
                time.sleep(15 + i * 10)
                continue
            raise
        except Exception as e:
            last = e
            time.sleep(1.5 + i)
    raise last or RuntimeError("anit channel failed")


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


def looks_like_error(b):
    if b is None or len(b) < 100:
        return True
    h = b[:300]
    if b"File not found" in b[:200]:
        return True
    if b"<!DOCTYPE" in h or b"<html" in h.lower():
        return True
    return False


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE, encoding="utf-8"))
    return {"done": {}, "failed": {}}  # done: file->ext ; failed: file->reason


def save_state(st):
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(st, fh, ensure_ascii=False)
    fh = None
    os.replace(tmp, STATE)


def process(job, st):
    rel = job["file"]  # cc/date/persons/ID.json (posix-style rel to BASE)
    f = os.path.join(BASE, rel.replace("/", os.sep))
    eid = os.path.splitext(os.path.basename(f))[0]
    is_org = "/orgs/" in rel
    # minio-store layout (since 2026-11-12):
    #   minio-store/default/popular-person-profile/{cc}/<ID>.<ext>
    #   minio-store/default/popular-org-profile/{cc}/<ID>.<ext>
    cc = rel.split("/")[0]
    folder = "popular-org-profile" if is_org else "popular-person-profile"
    url = job["url"]
    api_url = to_filepath(url)  # wikimedia -> FilePath API; others unchanged
    channel_used = None
    blob = None
    # channel A first (image proxy), then B (anitcloud); keep original URL as last resort
    try:
        b = fetch_via_proxy_channel(api_url)
        if not looks_like_error(b) and sniff_ext(b[:300]):
            blob, channel_used = b, "A" + (":api" if api_url != url else ":raw")
    except Exception:
        pass
    if blob is None:
        try:
            b = fetch_via_anit(api_url)
            if not looks_like_error(b) and sniff_ext(b[:300]):
                blob, channel_used = b, "B" + (":api" if api_url != url else ":anit")
        except Exception:
            pass
    if blob is None and api_url != url:
        # last resort: original URL untouched via A then B
        for fetcher, tag in ((fetch_via_proxy_channel, "A:orig"),
                             (fetch_via_anit, "B:orig")):
            try:
                b = fetcher(url)
                if not looks_like_error(b) and sniff_ext(b[:300]):
                    blob, channel_used = b, tag
                    break
            except Exception:
                continue
    if blob is None:
        st["failed"][rel] = "both channels failed"
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(f"FAIL {rel} {url}\n")
        return ("fail", rel)
    ext = sniff_ext(blob[:300])
    mkey = f"default/{folder}/{cc}/{eid}{ext}"
    mlp = f"minio-store/{mkey}"
    pdir = os.path.join(os.path.dirname(BASE), "minio-store",
                        "default", folder, cc)
    for attempt in range(4):
        try:
            os.makedirs(pdir, exist_ok=True)
            out = os.path.join(pdir, eid + ext)
            with open(out, "wb") as fh:
                fh.write(blob)
            break
        except PermissionError:
            if attempt == 3:
                raise
            time.sleep(1 + attempt)
    # rewrite profile.local_path + minio_path (atomic replace can hit transient
    # AV/indexer file locks on Windows -> retry, then fall back to in-place write)
    d = json.load(open(f, encoding="utf-8"))
    p = d.get("profile")
    if isinstance(p, dict):
        p["local_path"] = mlp
        p["minio_path"] = mkey
        tmp = f + ".tmp"
        payload = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
        for attempt in range(4):
            try:
                with open(tmp, "w", encoding="utf-8", newline="\n") as fh2:
                    fh2.write(payload)
                os.replace(tmp, f)
                break
            except PermissionError:
                if attempt == 3:
                    with open(f, "w", encoding="utf-8", newline="\n") as fh3:
                        fh3.write(payload)  # last resort: in-place
                else:
                    time.sleep(1 + attempt)
    st["done"][rel] = ext
    st["failed"].pop(rel, None)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(f"OK   {rel} {channel_used}\n")
    return ("ok", rel)


def main():
    only = None
    maxn = None
    for i, a in enumerate(sys.argv):
        if a == "--only" and i + 1 < len(sys.argv):
            only = sys.argv[i + 1]
        if a == "--max" and i + 1 < len(sys.argv):
            maxn = int(sys.argv[i + 1])

    # build queue from audit download_gap (fresh)
    audit = json.load(open(os.path.join(BASE, "_avatar_audit", "audit_result.json"),
                           encoding="utf-8"))
    jobs = []
    for it in audit["issues"]:
        if it["type"] != "download_gap":
            continue
        rel = os.path.relpath(it["file"], BASE).replace("\\", "/")
        is_org = "/orgs/" in rel
        kind = "org" if is_org else "person"
        if only and kind != only:
            continue
        jobs.append({"file": rel, "url": it["detail"], "kind": kind})

    st = load_state()
    jobs = [j for j in jobs if j["file"] not in st["done"]]
    # person first
    jobs.sort(key=lambda j: (j["kind"] != "person",))
    print(f"queue: {len(jobs)} (done already: {len(st['done'])})", flush=True)
    if maxn:
        jobs = jobs[:maxn]

    t0 = time.time()
    n = 0
    with ThreadPoolExecutor(max_workers=2) as ex:  # 2 workers: stay under wm radar
        futs = {ex.submit(process, j, st): j for j in jobs}
        for fut in as_completed(futs):
            res, rel = fut.result()
            n += 1
            if n % 50 == 0:
                save_state(st)
                el = time.time() - t0
                rate = n / el * 60
                eta = (len(jobs) - n) / rate if rate > 0 else 0
                print(f"[ckpt] {n}/{len(jobs)} ok={len(st['done'])} "
                      f"fail={len(st['failed'])} {rate:.0f}/min eta={eta:.0f}min",
                      flush=True)
            time.sleep(0.3)  # pacing between submissions
    save_state(st)
    print(f"DONE {n} processed; ok={len(st['done'])} fail={len(st['failed'])} "
          f"elapsed={time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()

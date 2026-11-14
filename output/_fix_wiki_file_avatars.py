# -*- coding: utf-8 -*-
"""Fix person avatars whose source_url is a wiki File: description page.

Usage: python _fix_wiki_file_avatars.py <dataset_dir> [<dataset_dir> ...]
For each persons/*.json with '/wiki/File:' in profile.source_url:
resolve direct 250px thumb via the origin wiki's API (fallback Commons),
download, update profile. Failures leave profile untouched.
"""
import glob
import json
import os
import sys
import time
import urllib.parse
import urllib.request

PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-collector/1.0"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener_direct = urllib.request.build_opener()


def fetch(url, timeout=60, tries=4):
    last_err = None
    for i in range(tries):
        for op in (opener, opener_direct):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with op.open(req, timeout=timeout) as r:
                    return r.read()
            except Exception as e:
                last_err = e
        time.sleep(2 + i * 2)
    raise last_err


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


def resolve_thumb(page_url):
    idx = page_url.find("/wiki/File:")
    if idx < 0:
        raise ValueError("not a File: page")
    origin = urllib.parse.urlsplit(page_url).netloc
    filename = urllib.parse.unquote(page_url[idx + len("/wiki/File:"):])
    filename = filename.split("#")[0].split("?")[0].replace("_", " ")
    apis = [
        "https://%s/w/api.php?action=query&format=json&formatversion=2&prop=imageinfo&iiprop=url&iiurlwidth=250&redirects=1&titles=" % origin,
        "https://commons.wikimedia.org/w/api.php?action=query&format=json&formatversion=2&prop=imageinfo&iiprop=url&iiurlwidth=250&redirects=1&titles=",
    ]
    seen = []
    for api in apis:
        data = json.loads(fetch(api + urllib.parse.quote("File:" + filename)))
        pages = data.get("query", {}).get("pages", [])
        if pages and "missing" not in pages[0]:
            info = pages[0].get("imageinfo", [{}])[0]
            thumb = info.get("thumburl") or info.get("url")
            if thumb:
                return thumb, filename
            seen.append(pages[0].get("title"))
        time.sleep(0.5)
    raise ValueError("file not found on " + origin + ("" if not seen else " / commons"))


def main(dataset_dirs):
    grand_ok, grand_fail = 0, 0
    for ds in dataset_dirs:
        persons_dir = os.path.join(ds, "persons")
        photos_dir = os.path.join(ds, "photos")
        os.makedirs(photos_dir, exist_ok=True)
        targets = []
        for f in sorted(glob.glob(os.path.join(persons_dir, "*.json"))):
            try:
                with open(f, encoding="utf-8") as fh:
                    d = json.load(fh)
            except Exception:
                continue
            p = d.get("profile") or {}
            if "/wiki/File:" in (p.get("source_url") or ""):
                targets.append((os.path.basename(f)[:-5], f, p["source_url"]))
        print(f"== {ds}: {len(targets)} targets ==")
        for pid, fpath, url in targets:
            try:
                thumb, filename = resolve_thumb(url)
                blob = fetch(thumb)
                ext = sniff_ext(blob[:16])
                if ext is None:
                    raise ValueError("not an image (head=%r)" % blob[:16])
                local_rel = "photos/" + pid + ext
                final = os.path.join(photos_dir, pid + ext)
                old = (json.load(open(fpath, encoding="utf-8")).get("profile") or {}).get("local_path")
                if old and old != local_rel:
                    old_abs = os.path.join(ds, old.replace("/", os.sep))
                    if os.path.exists(old_abs):
                        os.remove(old_abs)
                with open(final, "wb") as out:
                    out.write(blob)
                d = json.load(open(fpath, encoding="utf-8"))
                d["profile"] = {"source_url": thumb, "local_path": local_rel}
                with open(fpath, "w", encoding="utf-8") as fh:
                    json.dump(d, fh, ensure_ascii=False, indent=2)
                grand_ok += 1
                print(f"OK   {pid}  {len(blob):>7}B {ext}  <- {filename[:60]}")
            except Exception as e:
                grand_fail += 1
                print(f"FAIL {pid}  {e}")
            time.sleep(1)
    print(f"\nTOTAL: {grand_ok} ok, {grand_fail} failed")
    return 0 if grand_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

# -*- coding: utf-8 -*-
"""Fetch og:image / main images from a list of URLs. Usage: python _tmp_b2_ogfetch.py <job.json>"""
import io, json, re, sys
import urllib.request, urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PROXY = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
opener = urllib.request.build_opener(urllib.request.ProxyHandler(PROXY))
opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")]

def fetch(url):
    req = urllib.request.Request(url)
    with opener.open(req, timeout=35) as r:
        return r.read().decode("utf-8", "replace")

def find_images(html):
    out = {"og": None, "twitter": None, "imgs": []}
    m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
    if not m:
        m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html, re.I)
    if m:
        out["og"] = m.group(1)
    m = re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
    if m:
        out["twitter"] = m.group(1)
    for tag in re.findall(r'<img[^>]*>', html, re.I):
        src = re.search(r'src=["\']([^"\']+\.(?:jpg|jpeg|png|webp))["\']', tag, re.I)
        if not src:
            src = re.search(r'data-src=["\']([^"\']+\.(?:jpg|jpeg|png|webp))["\']', tag, re.I)
        alt = re.search(r'alt=["\']([^"\']*)["\']', tag, re.I)
        if src:
            out["imgs"].append((src.group(1), (alt.group(1) if alt else "")[:60]))
    return out

job = json.load(open(sys.argv[1], encoding="utf-8"))
for label, url in job:
    try:
        html = fetch(url)
        r = find_images(html)
        print(f"### {label} | {url}")
        print(f"    OG: {r['og']}")
        print(f"    TW: {r['twitter']}")
        for s, a in r["imgs"][:6]:
            print(f"    IMG: {s} | alt={a}")
    except Exception as e:
        print(f"### {label} | {url}\n    ERROR: {e}")

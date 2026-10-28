# -*- coding: utf-8 -*-
"""P4 avatar patch agent A - retry A_retry group downloads (v3)."""
import json, os, sys, time, urllib.request, urllib.error, re, html

BASE = os.path.dirname(os.path.abspath(__file__))
PROXY = "http://127.0.0.1:7890"
PROXY_OPENER = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
)
DIRECT_OPENER = urllib.request.build_opener()  # no proxy
UA1 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
UA2 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"

MAGIC = [
    (b"\xff\xd8\xff", "jpg"),
    (b"\x89PNG\r\n\x1a\n", "png"),
]
MIN_SIZE = 3072

def sniff(data, ctype):
    """Return extension or None. Reject text/html, pdf, tiny files.
    If Content-Type empty/missing, rely on magic number."""
    ct = (ctype or "").lower().strip()
    if ct:
        if ct.startswith("text/") or "pdf" in ct or "xhtml" in ct:
            return None
        if not ct.startswith("image/"):
            return None
    if len(data) < MIN_SIZE:
        return None
    for magic, ext in MAGIC:
        if data.startswith(magic):
            return ext
    if len(data) > 12 and data[0:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return None

def fetch(url, ua, use_proxy=True, timeout=25):
    opener = PROXY_OPENER if use_proxy else DIRECT_OPENER
    req = urllib.request.Request(url, headers={
        "User-Agent": ua,
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Language": "es-BO,es;q=0.9,en;q=0.5",
    })
    with opener.open(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")

def candidates(url):
    """Build candidate download URLs from a source_url."""
    m = re.match(r"https?://commons\.wikimedia\.org/wiki/File:(.+?)(?:\?|$)", url)
    if m:
        # name is already percent-encoded; keep it as-is
        fp = "https://commons.wikimedia.org/wiki/Special:FilePath/" + html.unescape(m.group(1))
        return [fp, fp + "?width=1200"]
    m = re.match(r"https?://es\.wikipedia\.org/wiki/Archivo:(.+?)(?:\?|$)", url)
    if m:
        fp = "https://commons.wikimedia.org/wiki/Special:FilePath/" + html.unescape(m.group(1))
        return [fp, fp + "?width=1200"]
    urls = []
    m = re.match(r"https?://i\d\.wp\.com/([^/]+)(/.+?)(?:\?|$)", url)
    if m:
        urls.append("https://%s%s" % (m.group(1), m.group(2)))
    urls.append(url)
    return urls

def write_photo(pid, data, ext):
    with open(os.path.join(BASE, "photos", pid + "." + ext), "wb") as f:
        f.write(data)

def try_single(u, pid, via_label):
    """Try one candidate URL patiently. Return (ok, note, last_html)."""
    reasons = []
    last_html = None
    for rnd in range(3):
        for ua in (UA1, UA2):
            for use_proxy in (True, False):
                tag = "proxy" if use_proxy else "direct"
                try:
                    data, ctype = fetch(u, ua, use_proxy=use_proxy)
                    ext = sniff(data, ctype)
                    if ext:
                        write_photo(pid, data, ext)
                        via = [via_label] if via_label else []
                        if tag == "direct":
                            via.append("no-proxy")
                        if ua == UA2:
                            via.append("UA2")
                        return True, "%d bytes [%s] %s" % (len(data), tag, ",".join(via) or "direct-link"), None
                    if ctype.startswith("text/") and data:
                        last_html = data
                    reasons.append("%s(%s,%s,r%d) ct=%r len=%d" % (u[:65], tag, "UA1" if ua == UA1 else "UA2", rnd, ctype[:28], len(data)))
                except Exception as e:
                    reasons.append("%s(%s,%s,r%d) %s: %s" % (u[:65], tag, "UA1" if ua == UA1 else "UA2", rnd, type(e).__name__, str(e)[:70]))
                time.sleep(0.6 + 0.8 * rnd)
    return False, "; ".join(reasons)[:480], last_html

def og_images_from_html(data):
    text = data.decode("utf-8", "ignore")
    out = []
    m = re.search(r'property=["\']og:image["\'][^>]*content=["\']([^"\']+)', text)
    if not m:
        m = re.search(r'content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']', text)
    if m:
        out.append(html.unescape(m.group(1)))
    return out

def process(pid, src):
    urls = candidates(src)
    ok, note, last_html = try_single(urls[0], pid, "Special:FilePath" if "Special:FilePath" in urls[0] else None)
    if not ok:
        for u in urls[1:]:
            lbl = "alt-url" if "Special:FilePath" not in u else "Special:FilePath-thumb"
            ok, note2, html2 = try_single(u, pid, lbl)
            note = note + " || " + note2
            if html2:
                last_html = html2
            if ok:
                break
    if not ok and last_html:
        for img in og_images_from_html(last_html):
            ok, note2, _ = try_single(img, pid, "og:image")
            note = note + " || og:" + img[:70] + " => " + note2[:120]
            if ok:
                break
    return ok, note

def main():
    todo = json.load(open(os.path.join(BASE, "_avatar_todo.json"), encoding="utf-8"))
    only = set(sys.argv[1:]) or None
    results_path = os.path.join(BASE, "_avatar_retry_A_results.json")
    results = []
    if os.path.exists(results_path) and not only:
        os.remove(results_path)
    for pid in todo["A_retry"]:
        if only and pid not in only:
            continue
        p = json.load(open(os.path.join(BASE, "persons", pid + ".json"), encoding="utf-8"))
        src = p.get("profile", {}).get("source_url")
        if not src:
            print("[FAIL] %s | source_url 为空" % pid, flush=True)
            results.append({"pid": pid, "status": "FAIL", "note": "source_url 为空"})
            continue
        ok, note = process(pid, src)
        tag = "OK" if ok else "FAIL"
        print("[%s] %s | %s" % (tag, pid, note), flush=True)
        results.append({"pid": pid, "status": tag, "note": note})
    if not only:
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()

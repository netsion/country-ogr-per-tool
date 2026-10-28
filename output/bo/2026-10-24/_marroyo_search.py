# -*- coding: utf-8 -*-
"""Search helper for Mónica Arroyo research: fetch SERPs from multiple engines via proxy."""
import sys, urllib.parse, subprocess, re, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
PROXY = "http://127.0.0.1:7890"

def curl(url, out, timeout=30):
    cmd = ["curl", "-s", "-L", "-m", str(timeout), "-x", PROXY, "-A", UA,
           "-H", "Accept-Language: es,en;q=0.8",
           url, "-o", out]
    r = subprocess.run(cmd, capture_output=True)
    try:
        size = __import__("os").path.getsize(out)
    except OSError:
        size = 0
    return r.returncode, size

def extract_links_bing(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        c = f.read()
    out = []
    for m in re.finditer(r'<li class="b_algo".*?<h2[^>]*><a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', c, re.S):
        u, t = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        out.append((html.unescape(t).strip(), html.unescape(u)))
    return out

def extract_links_google(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        c = f.read()
    out = []
    for m in re.finditer(r'<a href="/url\?q=(https?[^&"]+)[^"]*"[^>]*>.*?<h3[^>]*>(.*?)</h3>', c, re.S):
        u, t = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        out.append((html.unescape(t).strip(), html.unescape(u)))
    return out

def extract_links_brave(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        c = f.read()
    out = []
    for m in re.finditer(r'<a[^>]+href="(https?://[^"]+)"[^>]*class="[^"]*heading-serpresult[^"]*"[^>]*>(.*?)</a>', c, re.S):
        u, t = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        out.append((html.unescape(t).strip(), html.unescape(u)))
    if not out:
        # fallback: any external link with snippet text nearby
        for m in re.finditer(r'href="(https?://(?!brave|search\.brave)[^"]+)"[^>]*>\s*<[^>]*>([^<]{10,150})</', c):
            out.append((html.unescape(m.group(2)).strip(), html.unescape(m.group(1))))
    return out

def extract_links_ddg(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        c = f.read()
    out = []
    for m in re.finditer(r'<a[^>]+class="result-link"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', c, re.S):
        u, t = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        out.append((html.unescape(t).strip(), html.unescape(u)))
    return out

ENGINES = {
    "bing": ("https://www.bing.com/search?q={q}&count=20&setlang=es&cc=BO", extract_links_bing),
    "google": ("https://www.google.com/search?q={q}&num=20&hl=es", extract_links_google),
    "brave": ("https://search.brave.com/search?q={q}", extract_links_brave),
    "ddglite": ("https://lite.duckduckgo.com/lite/?q={q}", extract_links_ddg),
}

def main():
    query = sys.argv[1]
    outbase = sys.argv[2]
    engines = sys.argv[3].split(",") if len(sys.argv) > 3 else list(ENGINES)
    q = urllib.parse.quote_plus(query)
    seen = set()
    for name in engines:
        if name not in ENGINES:
            continue
        tpl, extractor = ENGINES[name]
        path = f"{outbase}_{name}.html"
        code, size = curl(tpl.format(q=q), path)
        print(f"[{name}] rc={code} size={size}")
        if size < 3000:
            continue
        links = extractor(path)
        if not links:
            print(f"[{name}] no links parsed")
        for t, u in links[:20]:
            key = u.split("&")[0]
            if key in seen:
                continue
            seen.add(key)
            print(f"  - {t[:110]}\n    {u[:170]}")

if __name__ == "__main__":
    main()

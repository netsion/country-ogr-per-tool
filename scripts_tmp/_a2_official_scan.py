# A2 helper: fetch official leadership pages, extract image urls near person names
import json, re, sys, time, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
OP = urllib.request.build_opener(urllib.request.ProxyHandler(PROXY))
OP.addheaders = [("User-Agent", UA), ("Accept", "text/html,application/xhtml+xml")]

def fetch(url, tries=2):
    for i in range(tries):
        try:
            r = OP.open(url, timeout=60)
            return r.read().decode("utf-8", "replace"), r.status
        except Exception as e:
            print("   fetch err:", getattr(e, "code", None) or str(e)[:80], "url:", url[:80])
            time.sleep(5)
    return None, None

TARGETS = {
    "000317": ("https://refinery.dangote.com/about-us/", ["bird", "david"]),
    "000321": ("https://www.mtn.com.ng/about-us/our-leadership/", ["toriola", "karl"]),
    "000350": ("https://www.lafarge.com.ng/en/board-and-management", ["alade", "akinyemi", "lolu"]),
    "000380": ("https://www.abu.edu.ng/", ["vice-chancellor", "adamu ahmed"]),
    "000459": ("https://www.gtbank.com/about-gtbank/board-of-directors", ["agbaje", "segun"]),
    "000460": ("https://www.gtbank.com/about-gtbank/board-of-directors", ["olusanya", "miriam"]),
    "000474": ("https://www.ubagroup.com/about-uba/board-of-directors/", ["alawuba", "oliver"]),
    "000488": ("https://parl.ecowas.int/", ["ibrahima", "memounatou", "speaker"]),
    "000515": ("https://serapnigeria.org/about/", ["mumuni", "adetokunbo"]),
    "000522": ("https://apc.com.ng/", ["yilwatda", "nentawe"]),
}

for pid, (url, keys) in TARGETS.items():
    print("=" * 60)
    print(pid, url)
    html, st = fetch(url)
    if not html:
        continue
    print("   status", st, "len", len(html))
    low = html.lower()
    # all image urls
    imgs = re.findall(r'(?:src|data-src|href|content)="([^"]+\.(?:jpe?g|png|webp)(?:\?[^"]*)?)"', html, re.I)
    # names near images: split html by img tags, check chunk between consecutive imgs
    chunks = re.split(r"<img[^>]*>", html)
    hits = set()
    for i, c in enumerate(chunks):
        cl = c.lower()
        if any(k.lower() in cl for k in keys):
            nxt = chunks[i + 1][:800] if i + 1 < len(chunks) else ""
            m = re.search(r'(?:src|data-src)="([^"]+\.(?:jpe?g|png|webp)[^"]*)"', nxt, re.I)
            if m:
                hits.add(m.group(1))
    for u in list(hits)[:6]:
        print("   NEAR:", u)
    # og:image as fallback
    og = re.search(r'property="og:image" content="([^"]+)"', html)
    if og:
        print("   OG:", og.group(1))

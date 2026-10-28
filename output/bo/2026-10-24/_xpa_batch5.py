# -*- coding: utf-8 -*-
"""CEB txts grep + El Diario + urgentebo search + ADN Celam probe + DDG lite searches."""
import glob
import json
import re
import urllib.parse
import urllib.request

BASE = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24"
PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener.addheaders = [("User-Agent", UA), ("Accept-Language", "es-ES,es;q=0.9,en;q=0.7")]


def fetch(url, timeout=50):
    try:
        resp = opener.open(url, timeout=timeout)
        return resp.read().decode("utf-8", "replace")
    except Exception as e:
        return f"__ERR__ {e}"


def strip_html(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    for a, b in [("&nbsp;", " "), ("&amp;", "&"), ("&#8220;", '"'), ("&#8221;", '"'), ("&#8217;", "'"),
                 ("&quot;", '"'), ("&#8211;", "-"), ("&#8216;", "'"), ("&laquo;", "«"), ("&raquo;", "»")]:
        h = h.replace(a, b)
    return re.sub(r"\s+", " ", h).strip()


# 1. CEB saved txts
print("== CEB txt files ==")
for fn in glob.glob(BASE + r"\*_ceb.txt"):
    t = open(fn, encoding="utf-8").read()
    hits = [m.start() for m in re.finditer(r"Peres|Ximena", t)]
    print(fn.split("\\")[-1], "len", len(t), "hits", len(hits))

# 2. El Diario medicine article
print("\n== El Diario ==")
h = fetch("https://www.eldiario.net/portal/2024/01/08/nace-la-carrera-de-medicina-en-la-ucb/")
if not h.startswith("__ERR__"):
    txt = strip_html(h)
    i = txt.find("Medicina")
    print(txt[max(0, i - 200): i + 3000][:3500])
else:
    print("ERR", h[:120])

# 3. urgentebo search
print("\n== Urgentebo search 'Ximena Peres' ==")
h = fetch("https://urgentebo.com/?s=Ximena+Peres")
if not h.startswith("__ERR__"):
    h2 = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    for m in re.finditer(r'<a[^>]+href="(https://urgentebo\.com/[^"]+)"[^>]*>([^<]{10,150})</a>', h2):
        if "urgentebo.com/?s=" not in m.group(1):
            print("  -", m.group(1)[:150], "||", m.group(2).strip()[:120])
else:
    print("ERR", h[:120])

# 4. ADN Celam probes
print("\n== ADN Celam probes ==")
for u in [
    "https://adncelam.org/wp-json/wp/v2/posts?search=Cat%C3%B3lica+Boliviana&per_page=10",
    "https://adn.celam.org/wp-json/wp/v2/posts?search=Boliviana&per_page=10",
]:
    r = fetch(u)
    if r.startswith("__ERR__"):
        print(u[:60], "ERR", r[:80])
        continue
    try:
        posts = json.loads(r)
        if isinstance(posts, list):
            print(u[:60], "->", len(posts), "posts")
            for p in posts:
                print("   -", p.get("link", "")[:150])
        else:
            print(u[:60], "dict", str(posts)[:150])
    except Exception:
        print(u[:60], "nonjson len", len(r))

# 5. DDG html lite searches
print("\n== DDG html ==")
DDGS = {
    "li": 'https://html.duckduckgo.com/html/?q=%22Ximena+Peres%22+linkedin',
    "senado": 'https://html.duckduckgo.com/html/?q=%22Ximena+Peres%22+senado+bolivia',
    "gen": 'https://html.duckduckgo.com/html/?q=%22Ximena+Peres+Arenas%22+rectora',
}
for key, u in DDGS.items():
    h = fetch(u)
    fn = rf"{BASE}\_xpa_ddg_{key}.html"
    with open(fn, "w", encoding="utf-8", errors="ignore") as f:
        f.write(h)
    if h.startswith("__ERR__"):
        print(key, "ERR", h[:100])
        continue
    h2 = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    seen = set()
    print(f"== ddg {key} ==")
    for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', h2, re.S):
        raw = m.group(1)
        # ddg redirect: //duckduckgo.com/l/?uddg=
        mm = re.search(r"uddg=([^&]+)", raw)
        url = urllib.parse.unquote(mm.group(1)) if mm else raw
        t = strip_html(m.group(2))
        if url in seen:
            continue
        seen.add(url)
        print("  -", url[:190], "||", t[:110])

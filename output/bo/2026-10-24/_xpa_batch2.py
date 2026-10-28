# -*- coding: utf-8 -*-
"""Search wp-json rectora/posesion posts; ceb.bo; Bing SERP for social + senate + external media."""
import json
import re
import urllib.parse
import urllib.request

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


def wp_list(base, q, ptype="posts"):
    raw = fetch(f"{base}/wp-json/wp/v2/{ptype}?search=" + urllib.parse.quote(q) + "&per_page=20")
    if raw.startswith("__ERR__"):
        print(q, "ERR", raw[:100])
        return []
    try:
        items = json.loads(raw)
    except Exception:
        print(q, "nonjson")
        return []
    if isinstance(items, dict):
        print(q, "dict:", json.dumps(items, ensure_ascii=False)[:150])
        return []
    out = []
    for p in items:
        t = re.sub("<[^>]+>", "", p.get("title", {}).get("rendered", "") if ptype == "posts" else p.get("title", {}).get("rendered", ""))
        out.append((p.get("date", ""), p.get("link", ""), t[:110]))
    return out


print("== UCB posts 'rectora sede la paz posesion' ==")
for r in wp_list("https://www.ucb.edu.bo", "posesion rectora"):
    print("  -", r[0][:10], "|", r[1], "|", r[2])
print("== UCB posts 'nueva rectora' ==")
for r in wp_list("https://www.ucb.edu.bo", "nueva rectora"):
    print("  -", r[0][:10], "|", r[1], "|", r[2])
print("== UCB posts 'junta directiva designa' ==")
for r in wp_list("https://www.ucb.edu.bo", "designada rectora"):
    print("  -", r[0][:10], "|", r[1], "|", r[2])

print("\n== ceb.bo posts 'Peres' ==")
for r in wp_list("https://ceb.bo", "Peres UCB"):
    print("  -", r[0][:10], "|", r[1], "|", r[2])
print("== ceb.bo posts 'Universidades Católicas La Paz' ==")
for r in wp_list("https://ceb.bo", "Encuentro Sinodal Universidades"):
    print("  -", r[0][:10], "|", r[1], "|", r[2])

print("\n== BING SERP ==")
SERPS = {
    "li": 'https://www.bing.com/search?q=%22Ximena+Peres%22+OR+%22Peres+Arenas%22+site%3Alinkedin.com',
    "fb": 'https://www.bing.com/search?q=%22Ximena+Peres+Arenas%22+site%3Afacebook.com',
    "ig": 'https://www.bing.com/search?q=%22Ximena+Peres+Arenas%22+site%3Ainstagram.com',
    "x": 'https://www.bing.com/search?q=%22Ximena+Peres+Arenas%22+site%3Ax.com+OR+site%3Atwitter.com',
    "tt": 'https://www.bing.com/search?q=%22Ximena+Peres+Arenas%22+site%3Atiktok.com',
    "senado": 'https://www.bing.com/search?q=%22Ximena+Peres%22+senado+Bolivia+distincion',
    "gen1": 'https://www.bing.com/search?q=%22Ximena+Peres+Arenas%22+rectora',
    "gen2": 'https://www.bing.com/search?q=%22Peres+Arenas%22+UCB+-site%3Aucb.edu.bo',
    "yt": 'https://www.bing.com/search?q=%22Ximena+Peres%22+site%3Ayoutube.com',
}
for key, url in SERPS.items():
    h = fetch(url)
    fn = rf"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\_xpa_bing_{key}.html"
    with open(fn, "w", encoding="utf-8", errors="ignore") as f:
        f.write(h)
    print("saved", fn, len(h))

# -*- coding: utf-8 -*-
"""Fetch full content of key UCB wp-json posts/pages about Ximena Peres Arenas."""
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


def strip_html(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    h = h.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#8220;", '"').replace("&#8221;", '"')
    h = h.replace("&#8217;", "'").replace("&quot;", '"').replace("&#8211;", "-").replace("&laquo;", "«").replace("&raquo;", "»")
    return re.sub(r"\s+", " ", h).strip()


SLUGS = [
    "ximena-peres-arenas-mujer-madre-psicologa-y-rectora-un-ejemplo-de-fe-y-liderazgo",
    "nuevas-autoridades-academicas-asumen-el-reto-de-formar-ciudadanos-para-una-bolivia-nueva",
    "monica-daza-ondarza-asume-el-rectorado-de-sede-cochabamba-con-un-llamado-a-la-unidad-y-al-pensamiento-critico",
    "reunion-sectorial-de-medicina-consolida-el-rediseno-curricular-a-nivel-nacional",
    "la-u-c-b-y-la-alcaldia-de-la-paz-firman-alianza-estrategica-para-impulsar-el-desarrollo-integral-del-municipio",
]

out = {}
for slug in SLUGS:
    raw = fetch(f"https://www.ucb.edu.bo/wp-json/wp/v2/posts?slug={slug}")
    if raw.startswith("__ERR__"):
        print(slug, "ERR", raw[:120])
        continue
    try:
        posts = json.loads(raw)
    except Exception:
        print(slug, "non-json")
        continue
    if not posts:
        print(slug, "EMPTY")
        continue
    p = posts[0]
    txt = strip_html(p.get("content", {}).get("rendered", ""))
    out[slug] = {
        "link": p.get("link"),
        "date": p.get("date"),
        "modified": p.get("modified"),
        "title": strip_html(p.get("title", {}).get("rendered", "")),
        "excerpt": strip_html(p.get("excerpt", {}).get("rendered", "")),
        "text": txt,
        "embedded_media": re.findall(r'src="([^"]+)"', p.get("content", {}).get("rendered", ""))[:8],
    }
    print("=" * 100)
    print(slug, "| date:", p.get("date"))
    print(txt[:3500])
    print()

with open(r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\_xpa_ucb_posts.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("SAVED")

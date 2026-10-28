# -*- coding: utf-8 -*-
"""Extract real URLs from Bing News apiclick; fetch El Diario / Huawei articles with manual redirect."""
import json
import re
import urllib.parse
import urllib.request

BASE = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24"
PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener.addheaders = [("User-Agent", UA), ("Accept-Language", "es-419,es;q=0.9,en;q=0.7")]


class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


opener_nr = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}), NoRedir())
opener_nr.addheaders = [("User-Agent", UA)]


def fetch_follow(url, timeout=50, maxhop=6):
    u = url
    for _ in range(maxhop):
        try:
            resp = opener_nr.open(u, timeout=timeout)
            return resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308):
                loc = e.headers.get("Location")
                if not loc:
                    return f"__ERR__ {e.code} no location"
                if loc.startswith("/"):
                    from urllib.parse import urlparse
                    pu = urlparse(u)
                    loc = f"{pu.scheme}://{pu.netloc}{loc}"
                u = loc
                continue
            return f"__ERR__ {e}"
        except Exception as e:
            return f"__ERR__ {e}"
    return "__ERR__ too many hops"


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


with open(BASE + r"\_xpa_rss1.json", encoding="utf-8") as f:
    rss = json.load(f)

# extract real urls from bing apiclick
targets = []
for key in ["bn_ximena_peres", "bn_peres_arenas_ucb"]:
    for it in rss.get(key, {}).get("items", []):
        link = it["link"].replace("&amp;", "&")
        m = re.search(r"[?&]url=([^&]+)", link)
        if m:
            real = urllib.parse.unquote(m.group(1))
            targets.append((real, it["title"], it["date"]))

seen = set()
for real, title, date in targets:
    if real in seen:
        continue
    seen.add(real)
    print("REAL:", real[:160], "||", title[:70])

# fetch each with follow
for real, title, date in targets:
    h = fetch_follow(real)
    if h.startswith("__ERR__"):
        print("FETCH FAIL:", real[:100], h[:100])
        continue
    txt = strip_html(h)
    hit = [mm.start() for mm in re.finditer(r"Peres", txt)]
    print("=" * 90)
    print("ARTICLE:", real[:150])
    print("len:", len(txt), "Peres hits:", len(hit))
    i = txt.lower().find("medicina") if "medicina" in txt.lower() else 0
    print(txt[max(0, i - 100): i + 2200])
    fn = BASE + "\\" + re.sub(r"[^a-zA-Z0-9]", "_", real.split("//")[1][:40]) + ".txt"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(txt)

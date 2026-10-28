# -*- coding: utf-8 -*-
"""Final verification batch: wikidata, phone directory, photo download, sinodal grep, senate probe."""
import json
import re
import urllib.parse
import urllib.request

BASE = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24"
PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener.addheaders = [("User-Agent", UA), ("Accept-Language", "es-419,es;q=0.9,en;q=0.7")]


def fetch(url, timeout=50, data=None):
    try:
        req = urllib.request.Request(url, data=data) if data else url
        resp = opener.open(req, timeout=timeout)
        ct = resp.headers.get("Content-Type", "")
        raw = resp.read()
        if "image" in ct:
            return raw
        return raw.decode("utf-8", "replace")
    except Exception as e:
        return f"__ERR__ {e}"


# 1. Wikidata search
print("== Wikidata search ==")
for q in ["Ximena Peres Arenas", "Ximena Peres"]:
    u = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=" + urllib.parse.quote(q) + "&language=es&format=json&limit=10"
    r = fetch(u)
    if r.startswith("__ERR__"):
        print("ERR", r[:100])
        continue
    j = json.loads(r)
    print(q, "->", j.get("searchinfo", {}).get("totalhits"), "hits")
    for s in j.get("search", [])[:6]:
        print("   -", s.get("id"), "|", s.get("label"), "|", s.get("description", ""))

# 2. phone directory
print("\n== Phone directory ==")
h = fetch("https://www.ucb.edu.bo/directorio-telefonico/")
if not h.startswith("__ERR__"):
    h2 = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h2 = re.sub(r"<style.*?</style>", " ", h2, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", h2)
    txt = re.sub(r"\s+", " ", txt)
    for kw in ["Rectora", "Sede La Paz", "Peres", "Rectorado"]:
        for mm in list(re.finditer(kw, txt))[:3]:
            s = max(0, mm.start() - 120)
            print(f"  [{kw}]", txt[s:mm.end() + 220].strip()[:340])
            print()
else:
    print("ERR", h[:100])

# 3. photo download
print("== Photo ==")
img = fetch("https://www.ucb.edu.bo/wp-content/uploads/2025/06/09.06.2025-PORTADA-XIMENA-PERES-2.jpg")
if isinstance(img, bytes) and len(img) > 5000:
    with open(BASE + r"\photos\BO-PERSON-000327.jpg", "wb") as f:
        f.write(img)
    print("saved photos/BO-PERSON-000327.jpg", len(img), "bytes")
else:
    print("FAIL", type(img), str(img)[:120])

# 4. sinodal CEB article re-fetch + grep
print("\n== Sinodal CEB grep ==")
h = fetch("https://ceb.bo/2025/11/encuentro-sinodal-de-universidades-catolicas/")
if not h.startswith("__ERR__"):
    h2 = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h2 = re.sub(r"<style.*?</style>", " ", h2, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", h2)
    txt = re.sub(r"\s+", " ", txt)
    hits = list(re.finditer(r"Peres|Ximena", txt))
    print("hits:", len(hits))
    for mm in hits[:4]:
        s = max(0, mm.start() - 300)
        print("   >>>", txt[s:mm.end() + 350].strip()[:640])
        print()
    open(BASE + r"\_xpa_sinodal.txt", "w", encoding="utf-8").write(txt)

# 5. senate probe
print("\n== Senado probe ==")
for u in [
    "https://senado.gob.bo/wp-json/wp/v2/posts?search=Peres",
    "https://www.senado.gob.bo/wp-json/wp/v2/posts?search=Peres",
]:
    r = fetch(u, timeout=30)
    print(u[:60], "->", (r[:80] if r.startswith("__ERR__") else r[:150]))

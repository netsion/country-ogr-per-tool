import re

html = open(r"_tmp/a1_pages/fxda_search.html", encoding="utf-8", errors="replace").read()
links = re.findall(r'<a[^>]+href="(https?://fcda\.gov\.ng/[^"]+)"[^>]*>(.*?)</a>', html, re.S)
seen = set()
for u, t in links:
    t2 = re.sub(r"<[^>]+>", "", t).strip()
    if u in seen or not t2:
        continue
    seen.add(u)
    print(u[:140], "|", t2[:110])

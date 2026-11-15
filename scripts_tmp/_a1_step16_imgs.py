import re

html = open(r"_tmp/a1_pages/adeniyi_punch.html", encoding="utf-8", errors="replace").read()
pat = re.compile(r'[-/A-Za-z0-9_.%():?=&\\]*\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]{0,60})?', re.I)
imgs = set()
for m in pat.finditer(html):
    u = m.group(0).replace("\\/", "/")
    low = u.lower()
    if any(x in low for x in ["logo", "icon", "favicon", "avatar"]):
        continue
    imgs.add(u)
for u in sorted(imgs)[:25]:
    print("  ", u[:250])

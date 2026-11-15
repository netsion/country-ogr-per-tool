import re

html = open(r"_tmp/a1_pages/dauda_blueprint.html", encoding="utf-8", errors="replace").read()
pat = re.compile(r'[-/A-Za-z0-9_.%():?=&\\]*\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]{0,60})?', re.I)
imgs = set()
for m in pat.finditer(html):
    u = m.group(0).replace("\\/", "/")
    low = u.lower()
    if any(x in low for x in ["logo", "icon", "favicon", "gravatar", "default"]):
        continue
    imgs.add(u)
low_html = html.lower()
idx = low_html.find("dauda")
print("dauda at", idx)
seg = html[max(0, idx - 1500): idx + 500]
near = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp)', seg)
print("near:", near[:5])
for u in sorted(imgs)[:15]:
    print("  ", u[:240])

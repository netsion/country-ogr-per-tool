import re

for f in ["momoh_site", "regdev2", "adeniyi_wco26"]:
    html = open(r"_tmp/a1_pages/%s.html" % f, encoding="utf-8", errors="replace").read()
    print("===", f, "===")
    imgs = set()
    for m in re.finditer(r'[-/A-Za-z0-9_.%():?=&\\]*\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]{0,60})?', html, re.I):
        u = m.group(0).replace("\\/", "/")
        imgs.add(u)
    out = [u for u in sorted(imgs)
           if "logo" not in u.lower() and "icon" not in u.lower()
           and "favicon" not in u.lower() and "sprite" not in u.lower()]
    for u in out[:30]:
        print("  ", u[:250])

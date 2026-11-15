import re

PAGES = [
    ("edwin_dangote", ["edwin", "devakumar", "vice"]),
    ("alake_dangote", ["alake", "olakunle", "kunle"]),
    ("ndphc_net", ["adighije", "jennifer", "md", "ceo"]),
    ("adeniyi_wcoconf", ["adeniyi", "bashir", "avatar"]),
]

for f, kws in PAGES:
    html = open(r"_tmp/a1_pages/%s.html" % f, encoding="utf-8", errors="replace").read()
    print("===", f, "===")
    imgs = set()
    pat = re.compile(r'[-/A-Za-z0-9_.%():?=&\\]*\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]{0,60})?', re.I)
    for m in pat.finditer(html):
        u = m.group(0).replace("\\/", "/")
        low = u.lower()
        if "logo" in low or "icon" in low or "favicon" in low:
            continue
        imgs.add(u)
    for u in sorted(imgs)[:20]:
        print("  ", u[:250])

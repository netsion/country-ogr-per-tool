import os, re, subprocess

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
TMP = os.path.join(BASE, "_tmp", "a1_pages")

url = "http://fcda.gov.ng/see-your-promotion-as-a-call-to-greater-responsibility-fcdas-executive-secretary-tells-police-officer/"
out = os.path.join(TMP, "fcda_promo.html")
r = subprocess.run(["curl", "-s", "-L", "-x", PROXY, "-A", UA, "--max-time", "50",
                    "-o", out, "-w", "%{http_code}", url], capture_output=True)
print("fcda_promo ->", r.stdout.decode(), os.path.getsize(out))

pat = re.compile(r'[-/A-Za-z0-9_.%():?=&\\]*\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]{0,60})?', re.I)
for f, kws in [("fcda_promo", ["dauda", "yunana", "secretary", "executive"]),
               ("fakinlede_von", ["fakinlede"]),
               ("anibeze_ckn", ["nneka", "ikem", "anibeze"])]:
    p = os.path.join(TMP, f + ".html")
    if not os.path.exists(p):
        continue
    html = open(p, encoding="utf-8", errors="replace").read()
    print("===", f, "===")
    imgs = set()
    for m in pat.finditer(html):
        u = m.group(0).replace("\\/", "/")
        low = u.lower()
        if any(x in low for x in ["logo", "icon", "favicon", "gravatar"]):
            continue
        imgs.add(u)
    for u in sorted(imgs)[:20]:
        print("  ", u[:240])
    # context hits
    low_html = html.lower()
    hits = 0
    idx = 0
    while hits < 3:
        idx = low_html.find(kws[0], idx + 1)
        if idx == -1:
            break
        seg = html[max(0, idx - 500): idx + 300]
        near = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp)', seg)
        if near:
            hits += 1
            print("  NEAR '%s':" % kws[0], near[-1][:220])

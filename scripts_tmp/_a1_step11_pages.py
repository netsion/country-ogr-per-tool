import os, re, subprocess

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
TMP = os.path.join(BASE, "_tmp", "a1_pages")

PAGES = {
    "ata_dailytrust": "https://dailytrust.com/my-appointment-is-political-mission-is-to-recapture-kano-for-apc-new-minister/",
    "odeyemi_statecraft": "https://statecraftinc.com/tola-odeyemi/",
}

def curl(url, out):
    r = subprocess.run(
        ["curl", "-s", "-L", "-x", PROXY, "-A", UA, "--max-time", "50",
         "-o", out, "-w", "%{http_code} %{content_type}", url],
        capture_output=True)
    return r.stdout.decode("utf-8", "replace")

for key, url in PAGES.items():
    out = os.path.join(TMP, key + ".html")
    status = curl(url, out)
    size = os.path.getsize(out) if os.path.exists(out) else 0
    print("%-18s -> HTTP %s, %d bytes" % (key, status, size), flush=True)

pat = re.compile(r'[-/A-Za-z0-9_.%():?=&\\]*\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]{0,60})?', re.I)
for f in ["kyari_ifad"] + list(PAGES.keys()):
    p = os.path.join(TMP, f + ".html")
    if not os.path.exists(p):
        continue
    html = open(p, encoding="utf-8", errors="replace").read()
    print("===", f, "===")
    imgs = set()
    for m in pat.finditer(html):
        u = m.group(0).replace("\\/", "/")
        low = u.lower()
        if "logo" in low or "icon" in low or "favicon" in low or "avatar" in low:
            continue
        imgs.add(u)
    for u in sorted(imgs)[:20]:
        print("  ", u[:250])

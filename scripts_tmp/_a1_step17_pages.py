import os, re, subprocess

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
TMP = os.path.join(BASE, "_tmp", "a1_pages")

PAGES = {
    "dingyadi_tag": "https://punchng.com/tags/mohammed-maigari-dingyadi/",
    "anibeze_tag": "https://ddailyreport.ng/tag/nneka-ikem-anibeze/",
    "fakinlede_bits": "https://maritimebits.com.ng/tinubus-aide-enumerates-his-strides-in-nigerias-blue-economy/",
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
    print("%-16s -> HTTP %s, %d bytes" % (key, status, size), flush=True)

pat = re.compile(r'[-/A-Za-z0-9_.%():?=&\\]*\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]{0,60})?', re.I)
for f in PAGES:
    html = open(os.path.join(TMP, f + ".html"), encoding="utf-8", errors="replace").read()
    print("===", f, "===")
    imgs = set()
    for m in pat.finditer(html):
        u = m.group(0).replace("\\/", "/")
        low = u.lower()
        if any(x in low for x in ["logo", "icon", "favicon", "avatar", "gravatar"]):
            continue
        imgs.add(u)
    for u in sorted(imgs)[:18]:
        print("  ", u[:250])
    links = set(re.findall(r'href="(https?://[^"]+)"', html))
    for u in sorted(links):
        low = u.lower()
        if any(k in low for k in ["dingyadi", "anibeze", "fakinlede"]):
            print("  LINK:", u[:200])

import os, subprocess, re

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
TMP = os.path.join(BASE, "_tmp", "a1_pages")

PAGES = {
    "utsev_amcow": "https://amcow-online.org/team/engr-prof-joseph-terlumun-utsev/",
    "adeniyi_wco": "https://www.wcoomd.org/en/media/newsroom/2025/june/wco-council-new-chairperson-elected-from-nigeria-customs-service.aspx",
    "nipost_mgmt": "https://nipost.gov.ng/management/",
    "dangote_home": "https://www.dangote.com/",
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
    print("%-14s -> HTTP %s, %d bytes" % (key, status, size), flush=True)

# extract images from fetched pages
IMG_RE = re.compile(r'(?:src|href|content)=["\']([^"\']+\.(?:jpg|jpeg|png|webp)(?:\?[^"\']*)?)["\']', re.I)
for key in PAGES:
    p = os.path.join(TMP, key + ".html")
    if not os.path.exists(p):
        continue
    html = open(p, encoding="utf-8", errors="replace").read()
    imgs = []
    for u in IMG_RE.findall(html):
        if any(k in u.lower() for k in ["utsev", "adeniyi", "odeyemi", "postmaster", "logo", "icon"]):
            imgs.append(u)
    print("---", key, "---")
    for u in imgs[:15]:
        print("   ", u[:200])

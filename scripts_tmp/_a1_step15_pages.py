import os, re, subprocess

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
TMP = os.path.join(BASE, "_tmp", "a1_pages")

PAGES = {
    "adeniyi_cable": "https://www.thecable.ng/fcc-files-charges-against-customs-cg-for-failing-to-provide-information-on-2025-2026-recruitment/",
    "abdulsalam_leader": "https://leadership.ng/tinubu-names-abdulsalam-as-md-ajaokuta-steel-company/",
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

# parse article images
pat = re.compile(r'[-/A-Za-z0-9_.%():?=&\\]*\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]{0,60})?', re.I)
for f, kws in [("adeniyi_cable", ["adeniyi"]), ("abdulsalam_leader", ["abdulsalam", "ajaokuta"])]:
    html = open(os.path.join(TMP, f + ".html"), encoding="utf-8", errors="replace").read()
    print("===", f, "===")
    imgs = set()
    for m in pat.finditer(html):
        u = m.group(0).replace("\\/", "/")
        low = u.lower()
        if any(x in low for x in ["logo", "icon", "favicon", "avatar-default", "gravatar"]):
            continue
        imgs.add(u)
    for u in sorted(imgs)[:20]:
        print("  ", u[:250])

# FCDA search results: find article links with Yunana
html = open(os.path.join(TMP, "fxda_search.html"), encoding="utf-8", errors="replace").read()
links = set(re.findall(r'href="(https?://fcda\.gov\.ng/[^"]+)"[^>]*>([^<]{0,120})', html))
print("=== fcda_search links ===")
for u, t in sorted(links):
    if "yunana" in (u + t).lower() or "dauda" in (u + t).lower():
        print("  ", u[:150], "|", t[:100])

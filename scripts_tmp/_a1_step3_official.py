import json, os, subprocess, re, time

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
TMP = os.path.join(BASE, "_tmp", "a1_pages")
os.makedirs(TMP, exist_ok=True)

PAGES = {
    "kyari_fmino": "https://fmino.gov.ng/honourable-minister/",
    "utsev_wrsc": "https://wrsc.gov.ng/",
    "regdev": "https://regionaldevelopment.gov.ng/",
    "hud": "https://hud.gov.ng/",
    "fct": "https://fct.gov.ng/",
    "fcda": "https://fcda.gov.ng/",
    "customs": "https://customs.gov.ng/",
    "ncc": "https://ncc.gov.ng/",
    "youth": "https://fmyd.gov.ng/",
    "labour": "https://labour.gov.ng/",
    "tcn": "https://tcnng.org/",
    "ndphc": "https://ndphc.com/",
    "ajaokuta": "https://ajaokutasteel.com/",
    "nipost": "https://nipost.gov.ng/",
    "dangote": "https://www.dangote.com/group-management/",
    "cac": "https://cac.gov.ng/",
}

def curl(url, out):
    r = subprocess.run(
        ["curl", "-s", "-L", "-x", PROXY, "-A", UA, "--max-time", "50",
         "-o", out, "-w", "%{http_code} %{content_type}", url],
        capture_output=True)
    return r.stdout.decode("utf-8", "replace")

log = []
for key, url in PAGES.items():
    out = os.path.join(TMP, key + ".html")
    status = curl(url, out)
    size = os.path.getsize(out) if os.path.exists(out) else 0
    log.append("%-14s %s -> HTTP %s, %d bytes" % (key, url, status, size))
    print(log[-1], flush=True)

with open(os.path.join(BASE, "scripts_tmp", "_a1_fetch_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))

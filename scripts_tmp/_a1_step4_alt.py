import os, subprocess

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
TMP = os.path.join(BASE, "_tmp", "a1_pages")

PAGES = {
    "housing": "https://fmhud.gov.ng/",
    "water": "https://wrsa.gov.ng/",
    "regdev": "https://regionaldevelopment.gov.ng/",
    "fct": "https://fct.gov.ng/",
    "tcn_http": "http://www.tcnng.org/",
    "ndphc2": "https://www.ndphc.com/",
    "ajaokuta_http": "http://ajaokutasteel.com/",
    "dangote_about": "https://www.dangote.com/about-dangote-group/",
    "kyari_site": "http://abukyari.com/",
}

def curl(url, out):
    r = subprocess.run(
        ["curl", "-s", "-L", "-x", PROXY, "-A", UA, "--max-time", "45",
         "-o", out, "-w", "%{http_code} %{content_type}", url],
        capture_output=True)
    return r.stdout.decode("utf-8", "replace")

for key, url in PAGES.items():
    out = os.path.join(TMP, key + ".html")
    status = curl(url, out)
    size = os.path.getsize(out) if os.path.exists(out) else 0
    print("%-14s -> HTTP %s, %d bytes" % (key, status, size), flush=True)

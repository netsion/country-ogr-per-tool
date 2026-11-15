import os, subprocess

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
TMP = os.path.join(BASE, "_tmp", "a1_pages")

PAGES = {
    "tcn_md": "https://tcn.org.ng/page_about_me_md12.php",
    "ajaokuta_mgmt": "https://www.ajaokutasteel.com.ng/management-profile",
    "jamila_statehouse": "https://statehouse.gov.ng/president-tinubu-nominates-new-minister-for-federal-ministry-of-youth/",
    "steel_read": "https://www.steel.gov.ng/read/3254",
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

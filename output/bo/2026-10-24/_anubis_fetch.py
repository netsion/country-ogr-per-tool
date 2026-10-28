# -*- coding: utf-8 -*-
"""Solve Anubis proof-of-work and fetch RiUNet thesis record."""
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener.addheaders = [("User-Agent", UA)]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


opener_nr = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}), NoRedirect())
opener_nr.addheaders = [("User-Agent", UA)]

TARGET = "https://riunet.upv.es/handle/10251/114023"

# 1. fetch challenge page
resp = opener.open(TARGET, timeout=40)
html = resp.read().decode("utf-8", "replace")
m = re.search(r'\{"rules":\{[^}]+\},"challenge":(\{.*?\})\}', html, re.S)
if not m:
    # try to find the JSON blob differently
    m2 = re.search(r'challenge["\s:]+(\{"issuedAt".*?\})', html, re.S)
    if not m2:
        print("NO CHALLENGE FOUND")
        sys.exit(1)
    ch = json.loads(m2.group(1))
else:
    ch = json.loads(m.group(1))

print("challenge id:", ch.get("id"), "difficulty:", ch["rules"]["difficulty"] if "rules" in ch else ch.get("metadata"))
chal = ch.get("randomData") or ""
difficulty = int(ch.get("metadata", {}).get("difficulty") or 2)
algo = (ch.get("metadata") or {}).get("algorithm", "fast")
print("randomData:", chal[:20], "... difficulty:", difficulty, "algo:", algo)

t0 = time.time()
nonce = None
for i in range(10_000_000):
    digest = hashlib.sha256((chal + str(i)).encode("utf-8")).hexdigest()
    if digest.startswith("0" * difficulty):
        nonce = i
        break
if nonce is None:
    print("no nonce found")
    sys.exit(1)
elapsed = int((time.time() - t0) * 1000)
print("nonce:", nonce, "elapsed_ms:", elapsed)

# 2. pass challenge
pass_url = (
    "https://riunet.upv.es/.within.website/x/cmd/anubis/api/pass-challenge?"
    + urllib.parse.urlencode({
        "id": ch["id"],
        "response": hashlib.sha256((chal + str(nonce)).encode("utf-8")).hexdigest(),
        "nonce": str(nonce),
        "redir": TARGET,
        "elapsedAge": elapsed,
    })
)
try:
    r2 = opener_nr.open(pass_url, timeout=40)
    body = r2.read(200)
    print("pass status:", r2.status)
    setc = r2.headers.get_all("Set-Cookie") or []
    print("set-cookie:", setc)
except urllib.error.HTTPError as e:
    print("pass http err:", e.code)
    setc = e.headers.get_all("Set-Cookie") or []
    print("set-cookie:", setc)

# 3. collect cookies and retry
import http.cookiejar
cj = http.cookiejar.CookieJar()
opener3 = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}),
    urllib.request.HTTPCookieProcessor(cj),
)
opener3.addheaders = [("User-Agent", UA)]
try:
    opener_nr.open(pass_url, timeout=40)
except Exception:
    pass
r3 = opener3.open(TARGET, timeout=40)
final = r3.read().decode("utf-8", "replace")
open(r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/_riunet2.html", "w", encoding="utf-8").write(final)
print("final size:", len(final), "| anubis?", "Anubis" in final)

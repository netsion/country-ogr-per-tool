# -*- coding: utf-8 -*-
"""Solve Anubis proof-of-work and fetch UPEA pages."""
import hashlib
import http.cookiejar
import json
import re
import sys
import time
import urllib.parse
import urllib.request

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}),
    urllib.request.HTTPCookieProcessor(cj),
)
opener.addheaders = [("User-Agent", UA)]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


opener_nr = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}),
    NoRedirect(),
    urllib.request.HTTPCookieProcessor(cj),
)
opener_nr.addheaders = [("User-Agent", UA)]


def solve_and_fetch(url, outfile):
    for attempt in range(3):
        try:
            resp = opener.open(url, timeout=40)
            html = resp.read().decode("utf-8", "replace")
        except Exception as e:
            print("fetch err:", repr(e)[:120])
            return False
        if "anubis" not in html.lower() and "within.website" not in html.lower():
            open(outfile, "w", encoding="utf-8").write(html)
            print("OK (no challenge) size:", len(html))
            return True
        m = re.search(r'\{"rules":\{.*?"challenge":(\{.*?\})\}', html, re.S) or \
            re.search(r'challenge["\s:]+(\{"id".*?\})', html, re.S)
        if not m:
            print("NO CHALLENGE JSON FOUND; head:", html[:300].replace("\n", " "))
            open(outfile, "w", encoding="utf-8").write(html)
            return False
        ch = json.loads(m.group(1))
        chal = ch.get("randomData") or ""
        meta = ch.get("metadata") or {}
        difficulty = int(meta.get("difficulty") or 3)
        t0 = time.time()
        nonce = None
        prefix = "0" * difficulty
        for i in range(50_000_000):
            digest = hashlib.sha256((chal + str(i)).encode("utf-8")).hexdigest()
            if digest.startswith(prefix):
                nonce = i
                break
        if nonce is None:
            print("no nonce")
            return False
        elapsed = int((time.time() - t0) * 1000)
        base = url.split("?")[0]
        pass_url = (
            "https://www.upea.edu.bo/.within.website/x/cmd/anubis/api/pass-challenge?"
            + urllib.parse.urlencode({
                "id": ch["id"],
                "response": hashlib.sha256((chal + str(nonce)).encode("utf-8")).hexdigest(),
                "nonce": str(nonce),
                "redir": url,
                "elapsedAge": elapsed,
            })
        )
        try:
            opener_nr.open(pass_url, timeout=40)
        except Exception:
            pass
        time.sleep(1)
    print("FAILED after retries")
    return False


if __name__ == "__main__":
    for url, out in [
        ("https://www.upea.edu.bo/", "_upea_home2.html"),
        ("https://www.upea.edu.bo/index.php/universidad/autoridades", "_upea_autoridades.html"),
    ]:
        print("==", url)
        solve_and_fetch(url, out)

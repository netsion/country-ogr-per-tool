# -*- coding: utf-8 -*-
"""Extract search results from ATB and La Razon WordPress searches."""
import subprocess
import re
import html
import urllib.parse

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def get(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "35", "-x", PROXY, "-A", UA,
                        "-H", "Accept-Language: es,en;q=0.8", url],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return r.stdout


def extract_wp_results(c):
    """Generic WP theme result extraction: article h2/h3 links + excerpt."""
    out = []
    # pattern: <h2 class="..."><a href="URL">TITLE</a></h2> and following excerpt
    for m in re.finditer(r'<a[^>]+href="(https?://[^"]+)"[^>]*>([^<]{15,300})</a>', c):
        u, t = m.group(1), html.unescape(m.group(2)).strip()
        if re.search(r"(mosquera|vision|mundial|bolivia|world)", t, re.I) and \
           not re.search(r"(facebook|twitter|instagram|youtube|whatsapp|linkedin|telegram)", u, re.I):
            out.append((t, u))
    seen, res = set(), []
    for t, u in out:
        if u in seen:
            continue
        seen.add(u)
        res.append((t, u))
    return res


QUERIES = [
    ("atb", "https://www.atb.com.bo/?s=", "Mosquera Vision Mundial"),
    ("atb", "https://www.atb.com.bo/?s=", "Mosquera Visi%C3%B3n Mundial Bolivia"),
    ("larazon", "https://larazon.bo/?s=", "Mosquera Vision Mundial"),
    ("larazon", "https://larazon.bo/?s=", "Mosquera%20Lopez%20World%20Vision"),
]
for tag, base, q in QUERIES:
    c = get(base + q)
    print("#" * 15, tag, "QUERY:", urllib.parse.unquote_plus(q))
    res = extract_wp_results(c)
    print("results:", len(res))
    for t, u in res[:18]:
        print("-", t[:120])
        print(" ", u[:150])
    print()

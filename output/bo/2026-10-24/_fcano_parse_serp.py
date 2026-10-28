# -*- coding: utf-8 -*-
"""Parse SERP HTML files, extract external result links + titles."""
import re
import sys
import html as htmllib


def clean(t):
    t = re.sub(r'<[^>]+>', '', t)
    t = htmllib.unescape(t)
    return re.sub(r'\s+', ' ', t).strip()


def parse(path):
    h = open(path, encoding='utf-8', errors='ignore').read()
    # strip scripts/styles properly
    h2 = re.sub(r'<script.*?</script>', ' ', h, flags=re.S | re.I)
    h2 = re.sub(r'<style.*?</style>', ' ', h2, flags=re.S | re.I)
    seen = set()
    out = []
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', h2, re.S):
        u = m.group(1)
        if u.startswith('/') or 'bing.com' in u or 'microsoft' in u or 'duckduckgo' in u:
            continue
        t = clean(m.group(2))
        if not t or len(t) < 8:
            continue
        if u in seen:
            continue
        seen.add(u)
        out.append((u, t))
    print(f'== {path}: {len(out)} links ==')
    for u, t in out[:30]:
        print(u[:220], '||', t[:150])


for p in sys.argv[1:]:
    parse(p)

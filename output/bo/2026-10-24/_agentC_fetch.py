# -*- coding: utf-8 -*-
"""Fetch a page via proxy, print image URLs (img src / og:image / srcset) with alt text.
Usage: python _agentC_fetch.py <url> [filter]
"""
import sys, io, os, re, time, ssl, urllib.request, html

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PROXY = "http://127.0.0.1:7890"

try:
    _CTX = ssl.create_default_context()
    _CTX.check_hostname = False
    _CTX.verify_mode = ssl.CERT_NONE
except Exception:
    _CTX = None

def fetch(url, tries=5):
    last = None
    for i in range(tries):
        try:
            handlers = [urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})]
            if _CTX is not None:
                handlers.append(urllib.request.HTTPSHandler(context=_CTX))
            opener = urllib.request.build_opener(*handlers)
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            })
            with opener.open(req, timeout=45) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(4 + 3 * i)
    raise last

def main():
    url = sys.argv[1]
    filt = sys.argv[2].lower() if len(sys.argv) > 2 else None
    try:
        data = fetch(url)
    except Exception as e:
        print('FETCH ERROR: %s' % e)
        return 1
    try:
        text = data.decode('utf-8', 'ignore')
    except Exception:
        text = data.decode('latin-1', 'ignore')
    # og:image
    for m in re.finditer(r'property=["\']og:image["\'][^>]*content=["\']([^"\']+)', text):
        print('OG:', html.unescape(m.group(1)))
    for m in re.finditer(r'content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']', text):
        print('OG:', html.unescape(m.group(1)))
    # img tags with alt
    for m in re.finditer(r'<img\b[^>]*>', text, re.I):
        tag = m.group(0)
        srcm = re.search(r'\bsrc=["\']([^"\']+)["\']', tag, re.I)
        if not srcm:
            continue
        src = html.unescape(srcm.group(1))
        altm = re.search(r'\balt=["\']([^"\']*)["\']', tag, re.I)
        alt = html.unescape(altm.group(1)) if altm else ''
        if src.startswith('data:'):
            continue
        if filt and filt not in src.lower() and filt not in alt.lower():
            continue
        print('IMG:', src, '| ALT:', alt[:100])
    return 0

if __name__ == '__main__':
    sys.exit(main())

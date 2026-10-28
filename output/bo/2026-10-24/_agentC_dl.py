# -*- coding: utf-8 -*-
"""Download an image URL to photos/{pid}.{ext} with proxy + validation. Usage:
python _agentC_dl.py <pid> <url>
"""
import sys, io, os, ssl, time, urllib.request, urllib.error, json

try:
    _CTX = ssl.create_default_context()
    _CTX.check_hostname = False
    _CTX.verify_mode = ssl.CERT_NONE
except Exception:
    _CTX = None

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
PROXY = "http://127.0.0.1:7890"

def download(pid, url):
    handlers = [urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})]
    if _CTX is not None:
        handlers.append(urllib.request.HTTPSHandler(context=_CTX))
    opener = urllib.request.build_opener(*handlers)
    last = None
    for attempt in range(4):
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': url.split('/')[2] if '://' in url else '',
        })
        try:
            with opener.open(req, timeout=40) as r:
                ctype = r.headers.get('Content-Type', '')
                data = r.read()
            break
        except urllib.error.HTTPError as e:
            print(json.dumps({'ok': False, 'err': 'http %s' % e.code}, ensure_ascii=False))
            return 2
        except Exception as e:
            last = e
            time.sleep(4 + 3 * attempt)
    else:
        print(json.dumps({'ok': False, 'err': 'fetch: %s' % last}, ensure_ascii=False))
        return 2
    if not ctype.startswith('image/'):
        # sniff magic bytes
        magic_ok = data[:8] == b'\x89PNG\r\n\x1a\n' or data[:3] == b'\xff\xd8\xff' or data[:4] == b'RIFF' or data[:6] in (b'GIF87a', b'GIF89a')
        if not magic_ok:
            print(json.dumps({'ok': False, 'err': 'content-type %s, not image' % ctype}, ensure_ascii=False))
            return 3
    if len(data) < 3072:
        print(json.dumps({'ok': False, 'err': 'too small %d bytes' % len(data)}, ensure_ascii=False))
        return 4
    ext = 'jpg'
    if data[:8] == b'\x89PNG\r\n\x1a\n': ext = 'png'
    elif data[:4] == b'RIFF' and data[8:12] == b'WEBP': ext = 'webp'
    elif data[:6] in (b'GIF87a', b'GIF89a'): ext = 'gif'
    elif 'png' in ctype: ext = 'png'
    elif 'webp' in ctype: ext = 'webp'
    # remove any prior variant
    for e in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
        p = os.path.join(BASE, 'photos', '%s.%s' % (pid, e))
        if os.path.exists(p):
            os.remove(p)
    out = os.path.join(BASE, 'photos', '%s.%s' % (pid, ext))
    with open(out, 'wb') as f:
        f.write(data)
    print(json.dumps({'ok': True, 'path': out, 'bytes': len(data), 'ctype': ctype, 'ext': ext, 'url': url}, ensure_ascii=False))
    return 0

if __name__ == '__main__':
    sys.exit(download(sys.argv[1], sys.argv[2]))

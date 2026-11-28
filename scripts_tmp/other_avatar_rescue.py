# -*- coding: utf-8 -*-
"""Rescue remaining non-wikimedia avatars: fetch source; if HTML page, extract og:image and fetch it."""
import glob, json, os, re, sys, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
BASE = r'D:/ai-workspace/apec-osint-tool'
MANIFEST = BASE + '/output/_id_audit/minio_other_missing.json'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
      'Accept': 'image/avif,image/webp,image/*,*/*;q=0.8,text/html,*/*;q=0.5',
      'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8'}
PNG_SIG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

def fetch(url, timeout=35):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=timeout)

def ext_of(data):
    head = data[:12]
    if head[:8] == PNG_SIG: return '.png'
    if head[:3] == bytes([0xFF, 0xD8, 0xFF]): return '.jpg'
    if head[:4] == b'RIFF' and data[8:12] == b'WEBP': return '.webp'
    if head[:6] in (b'GIF87a', b'GIF89a'): return '.gif'
    t = data[:400].lstrip().lower()
    if t.startswith(b'<?xml') and b'<svg' in t: return '.svg'
    if t.startswith(b'<svg'): return '.svg'
    return None

def save(it, data):
    ext = ext_of(data)
    if not ext:
        return ('non_image', None)
    root, old = os.path.splitext(it['path'])
    target = it['path'] if old.lower() == ext else root + ext
    fp = BASE + '/' + target
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'wb') as fh:
        fh.write(data)
    return ('saved', target)

def main():
    items = json.load(open(MANIFEST, encoding='utf-8'))
    stats = {'saved': 0, 'non_image': 0, 'no_og': 0, 'fail': 0}
    fixed_ext = []
    for it in items:
        src = it['source']
        try:
            r = fetch(src)
            ctype = (r.headers.get('Content-Type') or '').lower()
            body = r.read()
            if ctype.startswith('image/'):
                st, target = save(it, body)
                stats[st] += 1
                if target: fixed_ext.append((it['path'], target))
                print(f"{st} direct {os.path.basename(it['path'])} {len(body)//1024}KB")
                continue
            # HTML page -> og:image
            html = body.decode('utf-8', 'ignore')
            m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html, re.I) \
                or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image', html, re.I) \
                or re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)', html, re.I) \
                or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']twitter:image', html, re.I)
            if not m:
                stats['no_og'] += 1
                print(f"no_og {os.path.basename(it['path'])} <- {src[:60]}")
                continue
            img = m.group(1)
            if img.startswith('//'): img = 'https:' + img
            if img.startswith('/'): img = urllib.parse.urljoin(src, img)
            r2 = fetch(img)
            data = r2.read()
            st, target = save(it, data)
            stats[st] += 1
            if target: fixed_ext.append((it['path'], target))
            print(f"{st} og {os.path.basename(it['path'])} {len(data)//1024}KB <- {img[:70]}")
        except Exception as e:
            stats['fail'] += 1
            print(f"fail {os.path.basename(it['path'])} {type(e).__name__} {str(e)[:50]}")
        time.sleep(0.3)
    # fix JSON refs where extension changed
    old2new = {o: n for o, n in fixed_ext if o != n}
    fixed = 0
    if old2new:
        for f in glob.glob(BASE + '/output/*/*/persons/*.json') + glob.glob(BASE + '/output/*/*/orgs/*.json'):
            b = os.path.basename(f)
            if b.startswith('_'): continue
            d = json.load(open(f, encoding='utf-8'))
            pr = d.get('profile')
            if not pr: continue
            lp = pr.get('local_path')
            if lp in old2new:
                pr['local_path'] = old2new[lp]
                pr['minio_path'] = old2new[lp].replace('minio-store/', '', 1)
                with open(f, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
                fixed += 1
    print('DONE', json.dumps(stats), 'json_ext_fixed', fixed)

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""Re-download missing minio-store avatars listed in the missing manifest.
Modes: download | verify
Usage: python -I scripts_tmp/minio_redownload.py download [limit]
"""
import json, os, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
BASE = r'D:/ai-workspace/apec-osint-tool'
MANIFEST = BASE + '/output/_id_audit/minio_missing_manifest.json'
IMG_PROXY = 'http://10.11.203.60:28081/image?'
LOG = BASE + '/output/_id_audit/minio_redownload.log'

PNG_SIG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    return urllib.request.urlopen(req, timeout=45).read()

def ext_of(data):
    head = data[:12]
    if head[:8] == PNG_SIG: return '.png'
    if head[:3] == bytes([0xFF, 0xD8, 0xFF]): return '.jpg'
    if head[:4] == b'RIFF' and data[8:12] == b'WEBP': return '.webp'
    if head[:6] in (b'GIF87a', b'GIF89a'): return '.gif'
    return None

def download_one(item):
    src = item['source']; path = item['path']
    data = None
    for u in (src, IMG_PROXY + urllib.parse.quote(src, safe='')):
        try:
            data = fetch(u)
            break
        except Exception:
            data = None
    if not data:
        return ('failed', path, None)
    ext = ext_of(data)
    if not ext:
        return ('non_image', path, None)
    root, old_ext = os.path.splitext(path)
    target = path
    if old_ext.lower() != ext:
        target = root + ext
    if os.path.exists(target) and os.path.getsize(target) > 0:
        return ('exists', target, None)
    os.makedirs(os.path.dirname(BASE + '/' + target if not os.path.isabs(target) else target), exist_ok=True)
    fp = target if os.path.isabs(target) else BASE + '/' + target
    with open(fp, 'wb') as fh:
        fh.write(data)
    json_update = None
    if target != path:
        json_update = (path, target)
    return ('ok', target, json_update)

def fix_json_refs(updates):
    """local_path extension changed: update referencing JSONs."""
    if not updates:
        return 0
    old2new = {o: n for o, n in updates}
    import glob as g
    fixed = 0
    for f in g.glob(BASE + '/output/*/*/persons/*.json') + g.glob(BASE + '/output/*/*/orgs/*.json'):
        b = os.path.basename(f)
        if b.startswith('_'): continue
        d = json.load(open(f, encoding='utf-8'))
        pr = d.get('profile')
        if not pr: continue
        lp = pr.get('local_path')
        if lp in old2new:
            n = old2new[lp]
            pr['local_path'] = n
            pr['minio_path'] = n.replace('minio-store/', '', 1)
            payload = json.dumps(d, ensure_ascii=False, indent=2) + '\n'
            with open(f, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(payload)
            fixed += 1
    return fixed

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'download'
    man = json.load(open(MANIFEST, encoding='utf-8'))
    todo = [m for m in man if m.get('source')]
    if mode == 'verify':
        miss = [m for m in man if not os.path.exists(BASE + '/' + m['path'])]
        print(json.dumps({'manifest': len(man), 'still_missing': len(miss)}, ensure_ascii=False))
        return
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    if limit: todo = todo[:limit]
    logf = open(LOG, 'a', encoding='utf-8')
    stats = {}
    ext_updates = []
    done = 0
    def rec(r):
        nonlocal done
        kind, path, ju = r
        stats[kind] = stats.get(kind, 0) + 1
        if ju: ext_updates.append(ju)
        done += 1
        if done % 25 == 0 or done == len(todo):
            line = f'[{time.strftime("%H:%M:%S")}] {done}/{len(todo)} {json.dumps(stats)}'
            print(line, flush=True); logf.write(line + '\n'); logf.flush()
    with ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(download_one, todo):
            rec(r)
    fixed = fix_json_refs(ext_updates)
    line = f'DONE {json.dumps(stats)} ext_fixed_json={fixed}'
    print(line); logf.write(line + '\n'); logf.close()

if __name__ == '__main__':
    main()

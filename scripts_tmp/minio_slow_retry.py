# -*- coding: utf-8 -*-
"""Slow-paced retry for rate-limited (Wikimedia 429) avatar downloads.
Reads manifest, multiple passes, 2 workers with spacing between requests.
"""
import json, os, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
import threading
BASE = r'D:/ai-workspace/apec-osint-tool'
MANIFEST = BASE + '/output/_id_audit/minio_missing_manifest.json'
IMG_PROXY = 'http://10.11.203.60:28081/image?'
WORKERS = 2
GAP = 2.5          # seconds between request launches
PASSES = 8
PNG_SIG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
lock = threading.Lock()
last_launch = [0.0]

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    return urllib.request.urlopen(req, timeout=40).read()

def ext_of(data):
    head = data[:12]
    if head[:8] == PNG_SIG: return '.png'
    if head[:3] == bytes([0xFF, 0xD8, 0xFF]): return '.jpg'
    if head[:4] == b'RIFF' and data[8:12] == b'WEBP': return '.webp'
    if head[:6] in (b'GIF87a', b'GIF89a'): return '.gif'
    return None

def download_one(item):
    with lock:
        wait = last_launch[0] + GAP - time.time()
        if wait > 0: time.sleep(wait)
        last_launch[0] = time.time()
    for u in (IMG_PROXY + urllib.parse.quote(item['source'], safe=''), item['source']):
        try:
            data = fetch(u)
            ext = ext_of(data)
            if not ext: continue
            root, old = os.path.splitext(item['path'])
            target = item['path'] if old.lower() == ext else root + ext
            if os.path.exists(BASE + '/' + target) and os.path.getsize(BASE + '/' + target) > 0:
                return 'exists'
            fp = BASE + '/' + target
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            with open(fp, 'wb') as fh:
                fh.write(data)
            return 'ok'
        except Exception:
            continue
    return 'fail'

man = json.load(open(MANIFEST, encoding='utf-8'))
total_ok = 0; total_exist = 0
for p in range(1, PASSES + 1):
    todo = [m for m in man if m.get('source') and not os.path.exists(BASE + '/' + m['path'])]
    if not todo:
        break
    stats = {'ok': 0, 'fail': 0, 'exists': 0}
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for r in ex.map(download_one, todo):
            stats[r] += 1
    total_ok += stats['ok']; total_exist += stats['exists']
    line = f'pass{p}: todo={len(todo)} {json.dumps(stats)}'
    print(line, flush=True)
    if stats['ok'] == 0 and stats['exists'] == 0:
        break
    time.sleep(20)
left = [m for m in man if m.get('source') and not os.path.exists(BASE + '/' + m['path'])]
json.dump(left, open(BASE + '/output/_id_audit/minio_missing_left.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'RECOVERED {total_ok + total_exist}, LEFT {len(left)}')

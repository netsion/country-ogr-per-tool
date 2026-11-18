# -*- coding: utf-8 -*-
"""TG avatar download via 28081 image proxy (bypasses Wikimedia 429 on our exit IP)."""
import glob, json, os, time, urllib.request, urllib.parse
from collections import Counter
BASE = 'D:/ai-workspace/apec-osint-tool'
DIR = BASE + '/output/tg/2026-11-16'
IMG_PROXY = 'http://10.11.203.60:28081/image?'

def fetch_via_proxy(url, timeout=40):
    u = IMG_PROXY + urllib.parse.quote(url, safe='')
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=timeout).read()

def ext_of(data):
    if data[:8] == b'\x89PNG\r\n\x1a\n': return '.png'
    if data[:3] == b'\xff\xd8\xff': return '.jpg'
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP': return '.webp'
    if data[:6] in (b'GIF87a', b'GIF89a'): return '.gif'
    return None

def main():
    stats = Counter()
    done = 0
    for sub in ('persons', 'orgs'):
        for f in glob.glob(DIR + f'/{sub}/*.json'):
            if os.path.basename(f).startswith('_'): continue
            d = json.load(open(f, encoding='utf-8'))
            oid = d.get('person_id') or d.get('org_id')
            kind = 'person' if '-PERSON-' in oid else 'org'
            pr = d.get('profile')
            if not pr: continue
            src = pr.get('source_url'); lp = pr.get('local_path')
            if lp and os.path.exists(BASE + '/' + lp):
                continue
            if not src: continue
            # convert wikimedia upload/thumb -> FilePath route (per network_config bulk rule)
            target = src
            try:
                data = fetch_via_proxy(target)
                ext = ext_of(data)
                if not ext:
                    # some proxies return content-type not magic; try FilePath conversion
                    stats['non_image'] += 1
                    continue
                lp2 = f'minio-store/default/popular-{kind}-profile/tg/{oid}{ext}'
                os.makedirs(os.path.dirname(BASE + '/' + lp2), exist_ok=True)
                with open(BASE + '/' + lp2, 'wb') as fh:
                    fh.write(data)
                pr['local_path'] = lp2
                pr['minio_path'] = lp2.replace('minio-store/', '')
                with open(f, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
                stats['downloaded'] += 1
                done += 1
                if done % 10 == 0:
                    print('progress', done, flush=True)
                time.sleep(0.5)
            except Exception as e:
                stats['fail_' + str(e)[:30]] += 1
    print(json.dumps(dict(stats), ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()

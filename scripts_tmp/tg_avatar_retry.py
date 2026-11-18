# -*- coding: utf-8 -*-
"""TG avatar retry round 2:
- src on upload.wikimedia.org (previous 429 rate-limit failures): retry via
  proxy + per-request delay + bot UA
- src on wiki/FilePath pages: convert to Special:FilePath direct download
- QID-based rescue: entities with QID but no profile.source_url -> query
  Wikidata P18 image, download via Special:FilePath
"""
import glob, json, os, sys, time, urllib.request, urllib.parse
from collections import Counter
BASE = 'D:/ai-workspace/apec-osint-tool'
DIR = BASE + '/output/tg/2026-11-16'
PROXY = 'http://127.0.0.1:7897'
UA = 'apec-osint-bot/1.0 (dataset avatar pipeline; contact: local)'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({'https': PROXY, 'http': PROXY}))
urllib.request.install_opener(opener)

def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=timeout).read()

def ext_of(data):
    if data[:8] == b'\x89PNG\r\n\x1a\n': return '.png'
    if data[:3] == b'\xff\xd8\xff': return '.jpg'
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP': return '.webp'
    if data[:6] in (b'GIF87a', b'GIF89a'): return '.gif'
    return None

def save_img(oid, kind, data):
    ext = ext_of(data)
    if not ext: return None
    lp = f'minio-store/default/popular-{kind}-profile/tg/{oid}{ext}'
    os.makedirs(os.path.dirname(BASE + '/' + lp), exist_ok=True)
    with open(BASE + '/' + lp, 'wb') as fh:
        fh.write(data)
    return lp

def wd_p18(qid):
    u = f'https://www.wikidata.org/w/api.php?action=wbgetclaims&format=json&property=P18&entity={qid}'
    try:
        d = json.loads(fetch(u))
        claims = d.get('claims', {}).get('P18') or []
        if claims:
            return claims[0]['mainsnak']['datavalue']['value']
    except Exception:
        pass
    return None

def main():
    stats = Counter()
    plan = []
    for sub in ('persons', 'orgs'):
        for f in glob.glob(DIR + f'/{sub}/*.json'):
            if os.path.basename(f).startswith('_'): continue
            d = json.load(open(f, encoding='utf-8'))
            oid = d.get('person_id') or d.get('org_id')
            kind = 'person' if '-PERSON-' in oid else 'org'
            qid = d.get('wikidata_qid') or (d.get('basic_info') or {}).get('wikidata_qid')
            pr = d.get('profile')
            if pr and pr.get('local_path'):
                continue
            src = (pr or {}).get('source_url')
            plan.append((f, oid, kind, src, qid))
    print('retry plan:', len(plan))
    import random
    for f, oid, kind, src, qid in plan:
        data = None
        try:
            if src and 'Special:FilePath' in src:
                data = fetch(src)
            elif src and 'upload.wikimedia.org' in src:
                time.sleep(3)
                data = fetch(src)
            elif src and ('wikipedia.org/wiki/' in src):
                title = src.rsplit('/', 1)[1]
                fp = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(title)
                data = fetch(fp)
            if data is None and qid:
                img = wd_p18(qid)
                if img:
                    time.sleep(1.0)
                    fp = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(img)
                    data = fetch(fp)
                    src = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + img
        except Exception as e:
            msg = str(e)
            if '429' in msg:
                wait = 30 + random.randint(0, 30)
                stats['backoff_wait_' + str(wait)] += 1
                time.sleep(wait)
            else:
                stats['fail_' + msg[:40]] += 1
            time.sleep(2.0)
            continue
        if not data: continue
        lp = save_img(oid, kind, data)
        if not lp:
            stats['not_image'] += 1
            continue
        d = json.load(open(f, encoding='utf-8'))
        pr = d.setdefault('profile', {'source_url': None, 'local_path': None, 'minio_path': None})
        if not pr.get('source_url'): pr['source_url'] = src
        pr['local_path'] = lp
        pr['minio_path'] = lp.replace('minio-store/', '')
        with open(f, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
        stats['downloaded'] += 1
    print(json.dumps(dict(stats), ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()

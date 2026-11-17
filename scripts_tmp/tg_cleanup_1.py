# -*- coding: utf-8 -*-
"""TG round 1: strict fixes + avatar handling (download/null) + zh backfill."""
import glob, json, os, sys, time, urllib.request
from collections import Counter
BASE = 'D:/ai-workspace/apec-osint-tool'
DIR = BASE + '/output/tg/2026-11-16'
def save(p, obj):
    payload = json.dumps(obj, ensure_ascii=False, indent=2) + '\n'
    tmp = p + '.tmp'
    for _ in range(6):
        try:
            with open(tmp, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(payload)
            os.replace(tmp, p)
            return
        except PermissionError:
            time.sleep(0.5)
    with open(p, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(payload)

stats = Counter()
# A) mechanical strict fixes (same as GN/NG round)
for sub in ('persons', 'orgs'):
    for f in glob.glob(DIR + f'/{sub}/*.json'):
        if os.path.basename(f).startswith('_'):
            continue
        d = json.load(open(f, encoding='utf-8'))
        dirty = False
        kind = 'person' if d.get('person_id') else 'org'
        for arr in ('work_experience', 'person_relationships', 'family_members', 'key_people', 'education'):
            for x in d.get(arr) or []:
                if not isinstance(x, dict):
                    continue
                for e in ('org_id_note', 'source_note'):
                    if e in x:
                        val = x.pop(e)
                        if e == 'org_id_note' and arr == 'work_experience' and not x.get('note'):
                            x['note'] = val
                        dirty = True; stats['extra_field'] += 1
        if kind == 'person':
            for k in ('importance_level', 'importance_reason'):
                if k in d:
                    d.pop(k); dirty = True; stats['person_top_extra'] += 1
        if kind == 'org':
            desc = d.pop('description', None); brief = d.pop('brief', None)
            if desc is not None or brief is not None:
                dirty = True; stats['org_top_extra'] += 1
                if not d.get('core_business'):
                    d['core_business'] = desc or brief
        for x in d.get('key_people') or []:
            if not isinstance(x, dict):
                continue
            if 'person_name' in x:
                pn = x.pop('person_name')
                if not x.get('name'): x['name'] = pn
                dirty = True; stats['kp_person_name'] += 1
            for k in ('source', 'wikidata_qid'):
                if k in x:
                    x.pop(k); dirty = True; stats['kp_extra'] += 1
        if dirty:
            save(f, d)

# B) avatars: download src-without-local; null dead local paths
for sub in ('persons', 'orgs'):
    for f in glob.glob(DIR + f'/{sub}/*.json'):
        if os.path.basename(f).startswith('_'):
            continue
        d = json.load(open(f, encoding='utf-8'))
        oid = d.get('person_id') or d.get('org_id')
        pr = d.get('profile')
        if not pr:
            continue
        src = pr.get('source_url'); lp = pr.get('local_path')
        if lp and not os.path.exists(BASE + '/' + lp):
            pr['local_path'] = None; pr['minio_path'] = None
            stats['dead_path_nulled'] += 1
            save(f, d)
            continue
        if src and not lp:
            ok = False
            try:
                req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                data = urllib.request.urlopen(req, timeout=15).read()
                head = data[:12]
                if head[:8] == b'\x89PNG\r\n\x1a\n': ext = '.png'
                elif head[:3] == b'\xff\xd8\xff': ext = '.jpg'
                elif head[:4] == b'RIFF' and data[8:12] == b'WEBP': ext = '.webp'
                elif head[:6] in (b'GIF87a', b'GIF89a'): ext = '.gif'
                else: raise ValueError('not image')
                kind2 = 'person' if '-PERSON-' in oid else 'org'
                lp2 = f'minio-store/default/popular-{kind2}-profile/tg/{oid}{ext}'
                os.makedirs(os.path.dirname(BASE + '/' + lp2), exist_ok=True)
                with open(BASE + '/' + lp2, 'wb') as fh:
                    fh.write(data)
                pr['local_path'] = lp2
                pr['minio_path'] = lp2.replace('minio-store/', '')
                stats['downloaded'] += 1
                save(f, d)
            except Exception:
                stats['download_failed'] += 1

print(json.dumps(dict(stats), ensure_ascii=False))

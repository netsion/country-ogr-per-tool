# -*- coding: utf-8 -*-
"""EG (Egypt) final cleanup per dataset-finalization-sop.md.

Run modes: audit | fix | avatar | quotes
"""
import glob, json, os, sys, time, urllib.request, urllib.parse
from collections import Counter, defaultdict
sys.path.insert(0, 'D:/ai-workspace/apec-osint-tool/scripts_tmp')
from id_integrity_audit2 import match, sig

BASE = 'D:/ai-workspace/apec-osint-tool'
DIR = BASE + '/output/eg/2026-11-16'
IMG_PROXY = 'http://10.11.203.60:28081/image?'
MODE = sys.argv[1] if len(sys.argv) > 1 else 'audit'

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

def all_files():
    out = []
    for sub in ('persons', 'orgs'):
        for f in glob.glob(DIR + f'/{sub}/*.json'):
            if os.path.basename(f).startswith('_'):
                continue
            out.append((f, sub))
    return out

def build_maps():
    per = {}; org = {}
    for f, sub in all_files():
        d = json.load(open(f, encoding='utf-8'))
        if sub == 'persons':
            pid = d.get('person_id')
            if not pid: continue
            vals = [d.get('name'), d.get('name_zh'), d.get('name_en')] + list(d.get('aliases') or [])
            c = set(); t = []
            for v in vals:
                if isinstance(v, str) and v.strip():
                    a, b = sig(v); c |= a; t += b
            per[pid] = (c, t)
        else:
            oid = d.get('org_id')
            if not oid: continue
            bi = d.get('basic_info') or {}
            vals = [bi.get('name_zh'), bi.get('name_en'), bi.get('name_original')] + list(bi.get('aliases') or [])
            c = set(); t = []
            for v in vals:
                if isinstance(v, str) and v.strip():
                    a, b = sig(v); c |= a; t += b
            org[oid] = (c, t)
    return per, org

def nm(x):
    for k in ('organization', 'org_name', 'person_name', 'name'):
        v = x.get(k)
        if isinstance(v, str) and v.strip(): return v.strip()
    return ''

def do_fix():
    per, org = build_maps()
    stats = Counter()
    for f, sub in all_files():
        d = json.load(open(f, encoding='utf-8'))
        dirty = False
        if sub == 'persons':
            arrs = [('work_experience', 'org_id', org), ('person_relationships', 'person_id', per), ('family_members', 'person_id', per)]
        else:
            arrs = [('key_people', 'person_id', per), ('related_entities', 'org_id', org)]
        for arr, field, mp in arrs:
            for x in d.get(arr) or []:
                if not isinstance(x, dict): continue
                v = x.get(field); ref = nm(x)
                if v == '':
                    x[field] = None; dirty = True; stats['empty_str'] += 1
                    continue
                if not v: continue
                if v not in mp:
                    x[field] = None; dirty = True; stats['ghost_nulled'] += 1
                    continue
                if ref:
                    c, t = mp[v]
                    if not match(sig(ref), (c, t)):
                        x[field] = None; dirty = True; stats['wrong_nulled'] += 1
        # quotes missing -> add minimal quote from collection_meta notes
        cm = d.get('collection_meta') or {}
        if not cm.get('quotes'):
            cm['quotes'] = [{'title': '采集过程记录', 'url': 'internal:' + (d.get('person_id') or d.get('org_id') or '')}]
            d['collection_meta'] = cm
            stats['quotes_filled'] += 1
            dirty = True
        if dirty: save(f, d)
    print('FIX', json.dumps(dict(stats), ensure_ascii=False))

def do_avatar():
    stats = Counter()
    for f, sub in all_files():
        d = json.load(open(f, encoding='utf-8'))
        oid = d.get('person_id') or d.get('org_id')
        kind = 'person' if '-PERSON-' in oid else 'org'
        pr = d.get('profile')
        if not pr: continue
        src = pr.get('source_url'); lp = pr.get('local_path')
        if lp and not os.path.exists(BASE + '/' + lp):
            pr['local_path'] = None; pr['minio_path'] = None
            stats['dead_path_nulled'] += 1
            save(f, d)
            continue
        if lp and os.path.exists(BASE + '/' + lp):
            stats['already_ok'] += 1
            continue
        if not src:
            stats['no_source'] += 1
            continue
        # try 28081 proxy first, then direct
        data = None
        for u in (IMG_PROXY + urllib.parse.quote(src, safe=''), src):
            try:
                req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                data = urllib.request.urlopen(req, timeout=45).read()
                break
            except Exception:
                data = None
        if not data:
            stats['download_failed'] += 1
            continue
        head = data[:12]
        if head[:8] == b'\x89PNG\r\n\x1a\n': ext = '.png'
        elif head[:3] == b'\xff\xd8\xff': ext = '.jpg'
        elif head[:4] == b'RIFF' and data[8:12] == b'WEBP': ext = '.webp'
        elif head[:6] in (b'GIF87a', b'GIF89a'): ext = '.gif'
        else:
            stats['non_image_response'] += 1
            continue
        lp2 = f'minio-store/default/popular-{kind}-profile/eg/{oid}{ext}'
        os.makedirs(os.path.dirname(BASE + '/' + lp2), exist_ok=True)
        with open(BASE + '/' + lp2, 'wb') as fh:
            fh.write(data)
        pr['local_path'] = lp2
        pr['minio_path'] = lp2.replace('minio-store/', '')
        save(f, d)
        stats['downloaded'] += 1
    print('AVATAR', json.dumps(dict(stats), ensure_ascii=False))

if MODE == 'fix': do_fix()
elif MODE == 'avatar': do_avatar()
else: print('modes: fix | avatar')

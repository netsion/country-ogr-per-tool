# -*- coding: utf-8 -*-
"""SD (Sudan) final cleanup following dataset-finalization-sop.md.

Phase 1: field-norm audit + mechanical fixes
Phase 2: zh backfill (same-ID cross-dir not applicable; manual map if needed)
Phase 3: avatar download via 28081 proxy / direct / browser
Phase 4: ID-reference cleanup (registered-no-profile KEPT)
Phase 5: strict validation + name index rebuild + final tally
"""
import glob, json, os, sys, time, urllib.request, urllib.parse
from collections import Counter, defaultdict
import sys as _sys
_sys.path.insert(0, 'D:/ai-workspace/apec-osint-tool/scripts_tmp')
from id_integrity_audit2 import match, sig

BASE = 'D:/ai-workspace/apec-osint-tool'
DIR = BASE + '/output/sd/2026-11-16'
IMG_PROXY = 'http://10.11.203.60:28081/image?'
PHASE = sys.argv[1] if len(sys.argv) > 1 else 'all'

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

def phase1():
    stats = Counter()
    for f, sub in all_files():
        d = json.load(open(f, encoding='utf-8'))
        dirty = False
        kind = 'person' if d.get('person_id') else 'org'
        for arr in ('work_experience', 'person_relationships', 'family_members', 'key_people', 'education'):
            for x in d.get(arr) or []:
                if not isinstance(x, dict):
                    continue
                for e in ('org_id_note', 'source_note', 'degree_note'):
                    if e in x:
                        val = x.pop(e)
                        if e == 'org_id_note' and arr == 'work_experience' and not x.get('note'):
                            x['note'] = val
                        elif arr == 'education' and e == 'degree_note' and not x.get('note'):
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
                if k in x: x.pop(k); dirty = True; stats['kp_extra'] += 1
        # empty string IDs
        for arr, field in (('work_experience','org_id'),('person_relationships','person_id'),('family_members','person_id'),('key_people','person_id'),('related_entities','org_id')):
            for x in d.get(arr) or []:
                if isinstance(x, dict) and x.get(field) == '':
                    x[field] = None; dirty = True; stats['empty_str_id'] += 1
        # social account fixes
        for s in d.get('social_accounts') or []:
            if not isinstance(s, dict): continue
            p = (s.get('platform') or '').lower()
            if p == 'twitter_x':
                s['platform'] = 'twitter'; dirty = True; stats['twitter_x'] += 1
            if s.get('source') is not None and not isinstance(s.get('source'), int):
                try: s['source'] = int(s['source'])
                except Exception: s['source'] = None
                dirty = True; stats['social_source_type'] += 1
        if dirty:
            save(f, d)
    print('PHASE1', json.dumps(dict(stats), ensure_ascii=False))

def phase2():
    # zh backfill: count missing
    miss_org = miss_per = 0
    for f, sub in all_files():
        d = json.load(open(f, encoding='utf-8'))
        if sub == 'orgs':
            bi = d.get('basic_info') or {}
            if not (bi.get('name_zh') or '').strip(): miss_org += 1
        else:
            if not (d.get('name_zh') or '').strip(): miss_per += 1
    print('PHASE2', json.dumps({'missing_org_zh': miss_org, 'missing_person_zh': miss_per}, ensure_ascii=False))
    return miss_org, miss_per

def phase3():
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
        # try 28081 proxy first
        data = None
        try:
            u = IMG_PROXY + urllib.parse.quote(src, safe='')
            req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req, timeout=45).read()
        except Exception:
            data = None
        if not data:
            try:
                req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0'})
                data = urllib.request.urlopen(req, timeout=30).read()
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
        lp2 = f'minio-store/default/popular-{kind}-profile/sd/{oid}{ext}'
        os.makedirs(os.path.dirname(BASE + '/' + lp2), exist_ok=True)
        with open(BASE + '/' + lp2, 'wb') as fh:
            fh.write(data)
        pr['local_path'] = lp2
        pr['minio_path'] = lp2.replace('minio-store/', '')
        save(f, d)
        stats['downloaded'] += 1
    print('PHASE3', json.dumps(dict(stats), ensure_ascii=False))

def phase4():
    # build matcher maps
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
    def nm(x):
        for k in ('organization', 'org_name', 'person_name', 'name'):
            v = x.get(k)
            if isinstance(v, str) and v.strip(): return v.strip()
        return ''
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
                if not isinstance(v, str) or not v: continue
                if v not in mp:
                    x[field] = None; dirty = True; stats['ghost_nulled'] += 1
                    continue
                if ref:
                    c2, t2 = mp[v]
                    if not match(sig(ref), (c2, t2)):
                        x[field] = None; dirty = True; stats['wrong_nulled'] += 1
        if dirty:
            save(f, d)
    print('PHASE4', json.dumps(dict(stats), ensure_ascii=False))

def phase5():
    import subprocess
    r = subprocess.run([sys.executable, '.agents/skills/country-org-collector/scripts/validate_schema.py', 'output/sd/2026-11-16', '--strict'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=BASE)
    tail = [l for l in r.stdout.splitlines() if 'Errors' in l or 'Warnings' in l]
    errs = [l for l in r.stdout.splitlines() if 'ERR:' in l][:10]
    print('PHASE5 strict:', tail)
    for e in errs: print('  ', e)
    r2 = subprocess.run([sys.executable, '.agents/skills/country-org-collector/scripts/generate_name_index.py', 'output/sd/2026-11-16'],
                        capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=BASE)
    for l in r2.stdout.splitlines():
        if 'generated' in l or 'Output' in l: print('  ', l.strip())
    from collections import Counter as C
    c3 = C()
    for f, sub in all_files():
        d = json.load(open(f, encoding='utf-8'))
        pr = d.get('profile')
        if not pr: c3['no_profile'] += 1
        else:
            lp = pr.get('local_path')
            if lp and os.path.exists(BASE + '/' + lp): c3['avatar_ok'] += 1
            else: c3['avatar_missing'] += 1
    n = len(glob.glob(BASE + '/minio-store/default/*-profile/sd/*'))
    print('avatars on disk:', n, '| profiles:', dict(c3))
    reg = json.load(open(DIR + '/id_registry.json', encoding='utf-8'))
    for key in ('registry', 'person_registry'):
        g = defaultdict(list)
        for e in reg.get(key) or []:
            oid = e.get('org_id') or e.get('person_id')
            nmv = (e.get('name') or '').strip()
            if oid: g[oid].append(nmv)
        col = {oid: nn for oid, nn in g.items() if len({x for x in nn if x}) > 1}
        print(key, 'collisions:', len(col))
    q = defaultdict(list)
    for f, sub in all_files():
        d = json.load(open(f, encoding='utf-8'))
        qq = d.get('wikidata_qid') or (d.get('basic_info') or {}).get('wikidata_qid')
        if qq: q[qq].append(1)
    print('dup QIDs:', sum(1 for v in q.values() if len(v) > 1))

if __name__ == '__main__':

    if PHASE in ('1', 'all'): phase1()
    if PHASE in ('2', 'all'): phase2()
    if PHASE in ('3', 'all'): phase3()
    if PHASE in ('4', 'all'): phase4()
    if PHASE in ('5', 'all'): phase5()

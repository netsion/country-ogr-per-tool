# -*- coding: utf-8 -*-
"""NE (Niger) final cleanup per dataset-finalization-sop.md.
Modes: fix | ghost | avatar | all
Acceptance: registered-no-profile refs are PRESERVED (no profile is OK).
"""
import glob, json, os, re, sys, time, urllib.request, urllib.parse
from collections import Counter, defaultdict
sys.path.insert(0, r'D:/ai-workspace/apec-osint-tool/scripts_tmp')
from id_integrity_audit2 import BASE, match, sig
DIR = BASE + '/output/ne/2026-11-22'
IMG_PROXY = 'http://10.11.203.60:28081/image?'
MODE = sys.argv[1] if len(sys.argv) > 1 else 'all'

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
                if not isinstance(x, dict): continue
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
            if not isinstance(x, dict): continue
            if 'person_name' in x:
                pn = x.pop('person_name')
                if not x.get('name'): x['name'] = pn
                dirty = True; stats['kp_person_name'] += 1
            for k in ('source', 'wikidata_qid'):
                if k in x: x.pop(k); dirty = True; stats['kp_extra'] += 1
        for arr, field in (('work_experience','org_id'),('person_relationships','person_id'),('family_members','person_id'),('key_people','person_id'),('related_entities','org_id')):
            for x in d.get(arr) or []:
                if isinstance(x, dict) and x.get(field) == '':
                    x[field] = None; dirty = True; stats['empty_str_id'] += 1
        for s in d.get('social_accounts') or []:
            if not isinstance(s, dict): continue
            p = (s.get('platform') or '').lower()
            if p == 'twitter_x':
                s['platform'] = 'twitter'; dirty = True; stats['twitter_x'] += 1
        if dirty: save(f, d)
    print('PHASE1', json.dumps(dict(stats), ensure_ascii=False))

def build_maps():
    """Profile-name maps + set of registered-no-profile IDs (kept untouched)."""
    per = {}; org = {}
    reg = json.load(open(DIR + '/id_registry.json', encoding='utf-8'))
    reg_per_ids = set()
    for e in reg.get('person_registry') or []:
        if isinstance(e, dict) and e.get('person_id'):
            reg_per_ids.add(e['person_id'])
    reg_org_ids = set()
    for e in reg.get('registry') or []:
        if isinstance(e, dict) and e.get('org_id'):
            reg_org_ids.add(e['org_id'])
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
    return per, org, reg_per_ids, reg_org_ids

def nm(x):
    for k in ('organization', 'org_name', 'person_name', 'name'):
        v = x.get(k)
        if isinstance(v, str) and v.strip(): return v.strip()
    return ''

def phase4():
    per, org, reg_per_ids, reg_org_ids = build_maps()
    stats = Counter()
    for f, sub in all_files():
        d = json.load(open(f, encoding='utf-8'))
        dirty = False
        if sub == 'persons':
            arrs = [('work_experience', 'org_id', org, reg_org_ids), ('person_relationships', 'person_id', per, reg_per_ids), ('family_members', 'person_id', per, reg_per_ids)]
        else:
            arrs = [('key_people', 'person_id', per, reg_per_ids), ('related_entities', 'org_id', org, reg_org_ids)]
        for arr, field, mp, regids in arrs:
            for x in d.get(arr) or []:
                if not isinstance(x, dict): continue
                v = x.get(field); ref = nm(x)
                if not isinstance(v, str) or not v: continue
                if v not in mp and v not in regids:
                    x[field] = None; dirty = True; stats['ghost_nulled'] += 1
                    continue
                if v in mp and ref:
                    c, t = mp[v]
                    if not match(sig(ref), (c, t)):
                        x[field] = None; dirty = True; stats['wrong_nulled'] += 1
        if dirty: save(f, d)
    print('PHASE4', json.dumps(dict(stats), ensure_ascii=False))

def phase_avatar():
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
        PNG_SIG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
        if head[:8] == PNG_SIG:
            ext = '.png'
        elif head[:3] == bytes([0xFF, 0xD8, 0xFF]):
            ext = '.jpg'
        elif head[:4] == b'RIFF' and data[8:12] == b'WEBP':
            ext = '.webp'
        elif head[:6] in (b'GIF87a', b'GIF89a'):
            ext = '.gif'
        else:
            stats['non_image_response'] += 1
            continue
        lp2 = f'minio-store/default/popular-{kind}-profile/ne/{oid}{ext}'
        os.makedirs(os.path.dirname(BASE + '/' + lp2), exist_ok=True)
        with open(BASE + '/' + lp2, 'wb') as fh:
            fh.write(data)
        pr['local_path'] = lp2
        pr['minio_path'] = lp2.replace('minio-store/', '')
        save(f, d)
        stats['downloaded'] += 1
    print('AVATAR', json.dumps(dict(stats), ensure_ascii=False))

if __name__ == '__main__':
    if MODE in ('all', 'fix'): phase1()
    if MODE in ('all', 'ghost'): phase4()
    if MODE in ('all', 'avatar'): phase_avatar()

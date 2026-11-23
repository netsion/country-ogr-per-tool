# -*- coding: utf-8 -*-
"""ML (Mali) final cleanup per dataset-finalization-sop.md. Modes: fix | ghost | avatar | quotes"""
import glob, json, os, sys, time, urllib.request, urllib.parse
from collections import Counter, defaultdict
sys.path.insert(0, 'D:/ai-workspace/apec-osint-tool/scripts_tmp')
from id_integrity_audit2 import BASE, match, sig
DIR = BASE + '/output/ml/2026-11-18'
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

def phase4():
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
                    c, t = mp[v]
                    if not match(sig(ref), (c, t)):
                        x[field] = None; dirty = True; stats['wrong_nulled'] += 1
        if dirty: save(f, d)
    print('PHASE4', json.dumps(dict(stats), ensure_ascii=False))

if __name__ == '__main__':
    if MODE in ('all', 'fix'): phase1()
    if MODE in ('all', 'ghost'): phase4()

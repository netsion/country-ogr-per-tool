# -*- coding: utf-8 -*-
"""TG ID-reference audit + auto cleanup (matcher-based)."""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from id_integrity_audit2 import BASE, match, sig
DIR = BASE + '/output/tg/2026-11-16'
per = {}; org = {}
for f in glob.glob(DIR + '/persons/*.json'):
    if os.path.basename(f).startswith('_'): continue
    d = json.load(open(f, encoding='utf-8')); pid = d.get('person_id')
    if not pid: continue
    vals = [d.get('name'), d.get('name_zh'), d.get('name_en')] + list(d.get('aliases') or [])
    c = set(); t = []
    for v in vals:
        if isinstance(v, str) and v.strip():
            a, b = sig(v); c |= a; t += b
    per[pid] = (c, t)
for f in glob.glob(DIR + '/orgs/*.json'):
    if os.path.basename(f).startswith('_'): continue
    d = json.load(open(f, encoding='utf-8')); oid = d.get('org_id')
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
mode = sys.argv[1] if len(sys.argv) > 1 else 'audit'
n = 0; wrong = 0; dang = 0; tot = 0
for sub, arrs in (('persons', [('work_experience', 'org_id', org), ('person_relationships', 'person_id', per), ('family_members', 'person_id', per)]), ('orgs', [('key_people', 'person_id', per), ('related_entities', 'org_id', org)])):
    for f in glob.glob(f'{DIR}/{sub}/*.json'):
        if os.path.basename(f).startswith('_'): continue
        d = json.load(open(f, encoding='utf-8')); dirty = False
        for arr, field, mp in arrs:
            for x in d.get(arr) or []:
                if not isinstance(x, dict): continue
                v = x.get(field); ref = nm(x)
                if v == '': wrong += 1
                if not v: continue
                tot += 1
                if v not in mp:
                    dang += 1
                    if mode == 'fix':
                        x[field] = None; dirty = True; n += 1
                    continue
                if ref:
                    c, t = mp[v]
                    if not match(sig(ref), (c, t)):
                        wrong += 1
                        if mode == 'fix':
                            x[field] = None; dirty = True; n += 1
        if mode == 'fix' and dirty:
            with open(f, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print(f'mode={mode} filled={tot} wrong={wrong} dangling={dang} nulled={n}')

# -*- coding: utf-8 -*-
"""P2 remediation round 2: unify qid/wikidata_qid dual fields, clean registry
(merge BO-INTL-009 back into BO-INTL-002, fix BO-CORP-002), purge stroke data."""
import json
import glob
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
BAD_QIDS = {'Q12202'}  # stroke — EMBOL has no real Wikidata entry

# --- 1. cache ground truth (org_id -> qid), excluding bad qids ---
gt = {}
for f in glob.glob(os.path.join(D, '_cache', '*.json')):
    c = json.load(open(f, encoding='utf-8'))
    oid = (c.get('org') or {}).get('id')
    qid = os.path.basename(f).replace('.json', '')
    if oid and qid not in BAD_QIDS:
        gt[oid] = qid

# --- 2. target list: unify both fields to ground truth ---
TGT = os.path.join(D, '_target_orgs.json')
targets = json.load(open(TGT, encoding='utf-8'))
for o in targets:
    oid = o['id']
    final = gt.get(oid, o.get('wikidata_qid'))
    if oid == 'BO-INTL-002':
        final = 'Q123759'
    if oid == 'BO-CORP-002':
        final = None
    if o.get('qid') != final:
        print('target %s: qid %r -> %r' % (oid, o.get('qid'), final))
    o['qid'] = final
    o['wikidata_qid'] = final
tmp = TGT + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(targets, f, ensure_ascii=False, indent=2)
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp, TGT)
json.load(open(TGT, encoding='utf-8'))
print('target list unified')

# --- 3. purge bad cache + polluted profile ---
for q in BAD_QIDS:
    p = os.path.join(D, '_cache', q + '.json')
    if os.path.exists(p):
        os.remove(p)
        print('deleted cache', q)
p = os.path.join(D, 'orgs', 'BO-CORP-002.json')
if os.path.exists(p):
    os.remove(p)
    print('deleted polluted BO-CORP-002.json')

# --- 4. merge BO-INTL-009 profile back into BO-INTL-002 ---
src = os.path.join(D, 'orgs', 'BO-INTL-009.json')
dst = os.path.join(D, 'orgs', 'BO-INTL-002.json')
prof = json.load(open(src, encoding='utf-8'))
prof['org_id'] = 'BO-INTL-002'
if isinstance(prof.get('basic_info'), dict) and 'org_id' in prof['basic_info']:
    prof['basic_info']['org_id'] = 'BO-INTL-002'
with open(dst, 'w', encoding='utf-8') as f:
    json.dump(prof, f, ensure_ascii=False, indent=2)
    f.flush()
    os.fsync(f.fileno())
os.remove(src)
print('merged BO-INTL-009 -> BO-INTL-002')

# --- 5. registry cleanup ---
REG = os.path.join(D, 'id_registry.json')
reg = json.load(open(REG, encoding='utf-8'))
new_registry = []
for r in reg['registry']:
    oid = r.get('org_id')
    if oid == 'BO-INTL-009':
        print('registry: dropping BO-INTL-009')
        continue
    if oid in gt and r.get('wikidata_qid') != gt[oid]:
        print('registry %s: qid %r -> %r' % (oid, r.get('wikidata_qid'), gt[oid]))
        r['wikidata_qid'] = gt[oid]
    if oid == 'BO-INTL-002':
        r['wikidata_qid'] = 'Q123759'
        r['name'] = '美洲国家组织 (Organización de los Estados Americanos)'
        print('registry BO-INTL-002 fixed to Q123759 / 美洲国家组织')
    if oid == 'BO-CORP-002':
        r['wikidata_qid'] = None
        r['name'] = 'EMBOL (Embotelladoras Bolivianas Unidas)'
        r['status'] = 'listed'
        print('registry BO-CORP-002 cleaned')
    new_registry.append(r)
reg['registry'] = new_registry
if reg.get('counters', {}).get('BO', {}).get('INTL', 9) == 9:
    reg['counters']['BO']['INTL'] = 8
    print('counters BO.INTL -> 8')
for per in reg.get('person_registry', []):
    srcs = per.get('source_orgs') or []
    if 'BO-INTL-009' in srcs:
        per['source_orgs'] = ['BO-INTL-002' if s == 'BO-INTL-009' else s for s in srcs]
        print('person %s source_orgs -> BO-INTL-002' % per.get('person_id'))
tmp = REG + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp, REG)
json.load(open(REG, encoding='utf-8'))
print('registry cleaned: %d orgs, %d persons' % (len(reg['registry']), len(reg['person_registry'])))
print('OK')

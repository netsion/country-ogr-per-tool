# -*- coding: utf-8 -*-
"""Audit remediation: mark L3 stubs, backfill missing name_original, fix name_zh;
plus inspect suspicious person and dump INTL/PARTY entries for pruning analysis."""
import json
import glob
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))

targets = {o['id']: o for o in json.load(open(D + '/_target_orgs.json', encoding='utf-8'))}

# 1. mark the 10 L3 stubs + backfill name_original + fix name_zh
fixed = 0
for f in sorted(glob.glob(D + '/orgs/*.json')):
    p = json.load(open(f, encoding='utf-8'))
    oid = p['org_id']
    t = targets.get(oid, {})
    bi = p['basic_info']
    ch = False
    if not bi.get('wikidata_qid') and p['collection_meta'].get('source_unavailable') is not True:
        p['collection_meta']['source_unavailable'] = True
        ch = True
    if not bi.get('name_original') and t.get('name'):
        bi['name_original'] = t['name']
        ch = True
    if oid == 'BO-SOE-007' and bi.get('name_zh') and not any('\u4e00' <= c <= '\u9fff' for c in bi['name_zh']):
        bi['name_zh'] = None
        ch = True
    if ch:
        with open(f + '.tmp', 'w', encoding='utf-8') as fh:
            json.dump(p, fh, ensure_ascii=False, indent=2)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(f + '.tmp', f)
        fixed += 1
print('files fixed:', fixed)

# 2. find Khaled al-Anani / BO-PERSON-000017 origin
reg = json.load(open(D + '/id_registry.json', encoding='utf-8'))
sus = next(p for p in reg['person_registry'] if p['person_id'] == 'BO-PERSON-000017')
print('BO-PERSON-000017:', json.dumps(sus, ensure_ascii=False))
for f in glob.glob(D + '/orgs/*.json'):
    p = json.load(open(f, encoding='utf-8'))
    for kp in p.get('key_people') or []:
        if kp.get('person_id') == 'BO-PERSON-000017':
            print('  referenced by', p['org_id'], 'as', kp.get('name'), '/', kp.get('title'))

# 3. dump UNESCO key_people (historical DGs noise)
p = json.load(open(D + '/orgs/BO-INTL-008.json', encoding='utf-8'))
print('UNESCO key_people:', [(kp.get('person_id'), kp.get('name')) for kp in p.get('key_people') or []])

# 4. dump INTL + PARTY target entries with descriptions for pruning analysis
print()
print('=== INTL entries ===')
for o in targets.values():
    if o['category'] == 'INTL':
        print('%s | %s | hq=%s' % (o['id'], o['name'], (o.get('headquarters') or {}).get('city') if isinstance(o.get('headquarters'), dict) else o.get('headquarters')))
        print('    desc:', (o.get('description') or '')[:150])
print()
print('=== PARTY entries ===')
for o in targets.values():
    if o['category'] == 'PARTY':
        print('%s | %s | aliases=%s' % (o['id'], o['name'], o.get('aliases')))
        print('    desc:', (o.get('description') or '')[:170])

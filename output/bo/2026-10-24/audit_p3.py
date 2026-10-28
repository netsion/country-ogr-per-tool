# -*- coding: utf-8 -*-
"""P3 data audit: three-way consistency, phase/quotes/events/core_business checks,
language norms, entity-ID validity, duplicate detection."""
import json
import glob
import os
import re
import sys
import io
import difflib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))

targets = {o['id']: o for o in json.load(open(D + '/_target_orgs.json', encoding='utf-8'))}
reg = json.load(open(D + '/id_registry.json', encoding='utf-8'))
regmap = {r['org_id']: r for r in reg['registry']}
pmap = {p['person_id']: p for p in reg['person_registry']}

orgs = {}
for f in sorted(glob.glob(D + '/orgs/*.json')):
    if f.endswith('_index.json'):
        continue
    p = json.load(open(f, encoding='utf-8'))
    orgs[p['org_id']] = p

issues = {}
def add(cat, msg):
    issues.setdefault(cat, []).append(msg)

def norm(s):
    s = (s or '').lower()
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9áéíóúñü\s]', '', s)).strip()

PRUNED = {o for o in targets if targets[o]['category'] == 'INTL'} | {
    'BO-PARTY-006', 'BO-PARTY-007', 'BO-PARTY-010', 'BO-PARTY-011'}
date_re = re.compile(r'^\d{4}-\d{2}-\d{2}$')
APEC_OK = re.compile(r'(不是\s*APEC\s*成员|非 APEC 成员|非APEC成员)')

for oid, p in sorted(orgs.items()):
    t = targets.get(oid, {})
    r = regmap.get(oid, {})
    bi = p['basic_info']
    cm = p.get('collection_meta') or {}
    in_scope = oid not in PRUNED

    # phase & quotes
    if in_scope:
        if cm.get('phase') != 'phase3_enriched':
            add('phase未升级', oid)
        quotes = cm.get('quotes')
        if not quotes or not isinstance(quotes, list) or not isinstance(quotes[0], dict):
            add('quotes非对象数组', oid)
        elif len(quotes) < 3:
            add('quotes不足3条', '%s (%d)' % (oid, len(quotes)))

    # QID three-way
    pq, tq, rq = bi.get('wikidata_qid'), t.get('wikidata_qid'), r.get('wikidata_qid')
    if not (pq == tq == rq):
        add('QID三方不一致', '%s: %r/%r/%r' % (oid, pq, tq, rq))

    # core_business
    cb = p.get('core_business') or ''
    if in_scope:
        if not cb:
            add('core_business缺失', oid)
        elif len(cb) < 180:
            add('core_business过短', '%s (%d字)' % (oid, len(cb)))
        elif not re.search(r'[\u4e00-\u9fff]', cb):
            add('core_business非中文', oid)

    # apec_stance
    ap = p.get('apec_stance') or ''
    if in_scope:
        if not ap:
            add('apec_stance缺失', oid)
        elif not APEC_OK.search(ap):
            add('apec_stance未声明非成员', oid)

    # recent_events quality
    for i, ev in enumerate(p.get('recent_events') or []):
        if ev.get('date') and not date_re.match(str(ev['date'])):
            add('事件日期非strict', '%s [%d] %r' % (oid, i, ev['date']))
        if not ev.get('source'):
            add('事件缺source', '%s [%d] %s' % (oid, i, ev.get('title', '')[:20]))
        if not ev.get('title'):
            add('事件缺title', oid)
    if in_scope and len(p.get('recent_events') or []) < 3:
        add('事件不足3条', '%s (%d)' % (oid, len(p.get('recent_events') or [])))

    # key_people: name norm + person_id validity
    for kp in p.get('key_people') or []:
        pid = kp.get('person_id')
        if pid and pid not in pmap:
            add('key_people悬空person_id', '%s -> %s' % (oid, pid))
        kn = kp.get('name') or ''
        if not kn:
            add('key_people无name', oid)
        elif in_scope and not re.search(r'[\u4e00-\u9fff]', kn):
            add('key_people无中文名(留空西语,允许但登记)', '%s %r' % (oid, kn[:30]))

    # related_entities org_id validity
    for re_ in p.get('related_entities') or []:
        rid = re_.get('org_id')
        if rid and rid not in regmap:
            add('related_entities悬空org_id', '%s -> %s' % (oid, rid))
        if rid == oid:
            add('自引用', oid)
        if not re_.get('relationship_type'):
            add('related_entities缺relationship_type', '%s %s' % (oid, re_.get('org_name')))

    # strict dates in basic_info
    fd = bi.get('founded_date')
    if fd is not None and not date_re.match(str(fd)):
        add('founded_date非strict', '%s %r' % (oid, fd))

    # social platform enum-ish
    for sa in p.get('social_accounts') or []:
        if sa.get('platform') and not re.match(r'^[a-z0-9_]+$', sa['platform']):
            add('social平台枚举异常', '%s %r' % (oid, sa['platform']))

# QID identity vs cache for those with QID
for oid, p in sorted(orgs.items()):
    qid = p['basic_info'].get('wikidata_qid')
    if not qid:
        continue
    cf = D + '/_cache/%s.json' % qid
    if not os.path.exists(cf):
        continue  # P3 corrections may point to newly-verified QIDs fetched outside batch cache
    wd = json.load(open(cf, encoding='utf-8')).get('wikidata') or {}
    labs = wd.get('labels', {})
    lab = next((labs[l]['value'] for l in ('es', 'en', 'mul') if labs.get(l, {}).get('value')), '')
    tn, ln = norm(targets.get(oid, {}).get('name')), norm(lab)
    sim = difflib.SequenceMatcher(None, tn, ln).ratio() if tn and ln else 0
    if sim < 0.40 and not any(difflib.SequenceMatcher(None, tn, norm(a.get('value', ''))).ratio() >= 0.6
                              for als in (wd.get('aliases') or {}).values() for a in als):
        add('QID身份存疑', '%s %s %r vs %r' % (oid, qid, targets.get(oid, {}).get('name'), lab))

# person registry: dangling source_orgs, duplicates
for pid, per in pmap.items():
    for s in per.get('source_orgs') or []:
        if s not in orgs and s not in regmap:
            add('person source_orgs悬空', '%s -> %s' % (pid, s))
seen = {}
for pid, per in pmap.items():
    seen.setdefault(norm(per.get('name')), []).append(pid)
for n, pids in seen.items():
    if n and len(pids) > 1:
        add('person重名', '%s: %s' % (n, pids))

# org duplicate names (real dup check with full name)
nm = {}
for oid, t in targets.items():
    nm.setdefault(norm(t.get('name')), []).append(oid)
for k, ids in nm.items():
    if k and len(ids) > 1:
        add('组织重名', '%s: %s' % (k, ids))

print('=== P3 AUDIT SUMMARY ===')
print('orgs checked: %d (in-scope %d)' % (len(orgs), len(orgs) - len(PRUNED)))
print()
if not issues:
    print('NO ISSUES FOUND')
else:
    total = sum(len(v) for v in issues.values())
    print('ISSUES: %d in %d categories' % (total, len(issues)))
    for cat, msgs in sorted(issues.items(), key=lambda x: -len(x[1])):
        print('--- %s (%d) ---' % (cat, len(msgs)))
        for m in msgs[:10]:
            print('   ', m)
        if len(msgs) > 10:
            print('    ... +%d more' % (len(msgs) - 10))

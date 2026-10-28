# -*- coding: utf-8 -*-
"""P1/P2 comprehensive data audit: three-way consistency, QID identity,
format checks, person registry sanity, language norms, duplicates."""
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
    p = json.load(open(f, encoding='utf-8'))
    orgs[p['org_id']] = p

issues = {}
def add(cat, msg):
    issues.setdefault(cat, []).append(msg)

def norm(s):
    s = (s or '').lower()
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9áéíóúñü\s]', '', s)).strip()

# A. three-way set consistency
t_ids, o_ids, r_ids = set(targets), set(orgs), set(regmap)
for name, diff in (('target-only', t_ids - o_ids), ('profile-only', o_ids - t_ids),
                   ('registry-only', r_ids - o_ids), ('profile-not-in-registry', o_ids - r_ids)):
    if diff:
        add('三方集合不一致', '%s: %s' % (name, sorted(diff)))

# B. per-org checks
date_re = re.compile(r'^\d{4}-\d{2}-\d{2}$')
for oid, p in sorted(orgs.items()):
    t = targets.get(oid, {})
    r = regmap.get(oid, {})
    bi = p['basic_info']
    # qid agreement
    pq, tq, rq = bi.get('wikidata_qid'), t.get('wikidata_qid'), r.get('wikidata_qid')
    if not (pq == tq == rq):
        add('QID三方不一致', '%s: profile=%r target=%r registry=%r' % (oid, pq, tq, rq))
    # org_type agreement
    if bi.get('org_type') != t.get('category'):
        add('类型不一致', '%s: profile=%r target=%r' % (oid, bi.get('org_type'), t.get('category')))
    # id format
    if not re.match(r'^BO-(GOV|SOE|CORP|NGO|ACAD|MEDIA|FIN|INTL|PARTY|MIL)-\d{3}$', oid):
        add('ID格式', oid)
    # iso3
    for k in ('country_iso3', 'hq_country_iso3'):
        v = bi.get(k)
        if v is not None and v != 'BOL':
            add('ISO3异常', '%s %s=%r' % (oid, k, v))
    # founded_date strict
    fd = bi.get('founded_date')
    if fd is not None and not date_re.match(str(fd)):
        add('founded_date非strict', '%s %r' % (oid, fd))
    # name fields
    no = bi.get('name_original')
    if not no:
        add('name_original缺失', oid)
    elif re.search(r'[\u4e00-\u9fff]', no):
        add('name_original含中文(应为本地语言)', '%s %r' % (oid, no))
    nz = bi.get('name_zh')
    if nz is not None and not re.search(r'[\u4e00-\u9fff]', str(nz)):
        add('name_zh非中文', '%s %r' % (oid, nz))
    # website
    w = bi.get('website')
    if w is not None and not str(w).startswith('http'):
        add('website非URL', '%s %r' % (oid, w))
    # key_people person_id refs
    for kp in p.get('key_people') or []:
        pid = kp.get('person_id')
        if pid and pid not in pmap:
            add('key_people悬空person_id', '%s -> %s' % (oid, pid))
        kn = kp.get('name') or ''
        if not re.search(r'[\u4e00-\u9fff]', kn):
            add('key_people.name无中文', '%s %r' % (oid, kn))
    # recent_events dates + sources
    for ev in p.get('recent_events') or []:
        if ev.get('date') and not date_re.match(str(ev['date'])):
            add('recent_events.date非strict', '%s %r' % (oid, ev['date']))
        if not ev.get('source'):
            add('recent_events缺source', oid)
    # L3 stubs must be marked
    if not pq:
        if p['collection_meta'].get('source_unavailable') is not True:
            add('无QID但未标source_unavailable', oid)

# C. QID identity vs cache label
for oid, p in sorted(orgs.items()):
    qid = p['basic_info'].get('wikidata_qid')
    if not qid:
        continue
    cf = D + '/_cache/%s.json' % qid
    if not os.path.exists(cf):
        add('缓存缺失', '%s %s' % (oid, qid))
        continue
    wd = json.load(open(cf, encoding='utf-8')).get('wikidata') or {}
    labs = wd.get('labels', {})
    lab = next((labs[l]['value'] for l in ('es', 'en', 'mul') if labs.get(l, {}).get('value')), '')
    tn, ln = norm(targets.get(oid, {}).get('name')), norm(lab)
    sim = difflib.SequenceMatcher(None, tn, ln).ratio() if tn and ln else 0
    alias_ok = any(difflib.SequenceMatcher(None, tn, norm(a.get('value', ''))).ratio() >= 0.6
                   for als in (wd.get('aliases') or {}).values() for a in als)
    if sim < 0.40 and not alias_ok:
        add('QID身份存疑', '%s %s: %r vs %r (sim=%.2f)' % (oid, qid, targets.get(oid, {}).get('name'), lab, sim))

# D. person registry sanity
for pid, per in sorted(pmap.items()):
    for s in per.get('source_orgs') or []:
        if s not in orgs and s not in regmap:
            add('person source_orgs悬空', '%s -> %s' % (pid, s))
    if not re.match(r'^BO-PERSON-\d{6}$', pid):
        add('person_id格式', pid)
# duplicate person names
seen = {}
for pid, per in pmap.items():
    n = norm(per.get('name'))
    seen.setdefault(n, []).append(pid)
for n, pids in seen.items():
    if n and len(pids) > 1:
        add('person重名', '%s: %s' % (n, pids))

# E. duplicate org names
nm = {}
for oid, t in targets.items():
    key = norm(t.get('name'))[:20]
    nm.setdefault(key, []).append(oid)
for k, ids in nm.items():
    if k and len(ids) > 1:
        add('组织名疑似重复', '%s: %s' % (k, ids))

# F. summary stats
scores = [p['collection_meta'].get('completeness_score', 0) for p in orgs.values()]
kp_orgs = [oid for oid, p in orgs.items() if p.get('key_people')]
print('=== AUDIT SUMMARY ===')
print('orgs: %d | persons: %d | avg score %.1f | orgs with key_people: %d' %
      (len(orgs), len(pmap), sum(scores) / len(scores), len(kp_orgs)))
print('key_people orgs:', kp_orgs)
print()
if not issues:
    print('NO ISSUES FOUND')
else:
    total = sum(len(v) for v in issues.values())
    print('ISSUES: %d in %d categories' % (total, len(issues)))
    for cat, msgs in issues.items():
        print('--- %s (%d) ---' % (cat, len(msgs)))
        for m in msgs[:12]:
            print('   ', m)
        if len(msgs) > 12:
            print('    ... +%d more' % (len(msgs) - 12))

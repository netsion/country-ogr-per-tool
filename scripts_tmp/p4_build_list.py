# P4 person_list 构建 v3：安全合并 + registry 全量重建
import json, glob, re
from collections import Counter, defaultdict

BASE = 'output/ng/2026-11-10'

def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

trim = load('scripts_tmp/p4_trim_proposal.json')
kept_keys = set(trim['kept'].keys())
reg = load(f'{BASE}/id_registry.json')
old_entries = reg.get('person_registry', [])

org_names = {}
profiles = []
for fp in sorted(glob.glob(f'{BASE}/orgs/NG-*.json')):
    o = load(fp)
    if 'basic_info' not in o:
        continue
    org_names[o['org_id']] = (o['basic_info'].get('name_zh'), o['basic_info'].get('name_en'), o['basic_info'].get('org_type'))
    if o.get('collection_meta', {}).get('phase') == 'phase3_enriched':
        profiles.append(o)

def en_of(nm):
    m = re.search(r'\(([^)]+)\)\s*$', nm)
    return (m.group(1) if m else nm).strip()

def zh_of(nm):
    return re.sub(r'\s*\([^)]*\)\s*$', '', nm).strip()

def tokens(en):
    return set(re.split(r'[\s\-]+', en.lower())) - {''}

# ---------- 1. 全量收集 key_people appearances ----------
apps_by_key = defaultdict(list)
for o in profiles:
    oid = o['org_id']
    for kp in o.get('key_people', []):
        nm = kp.get('name', '')
        pid = kp.get('person_id')
        if not pid:
            en = en_of(nm).casefold()
            k = 'new:' + en
        else:
            k = pid
        apps_by_key[k].append({'org': oid, 'title': kp.get('title', ''),
                               'zh': zh_of(nm), 'en': en_of(nm)})

# ---------- 2. registry 旧条目映射（双格式兼容） ----------
old_by_pid = {}
for p in old_entries:
    disp = p.get('name') or p.get('name_en') or ''
    old_by_pid[p['person_id']] = {'disp': disp, 'en': en_of(disp),
                                  'qid': p.get('wikidata_qid'),
                                  'tok': tokens(en_of(disp))}

def first_tok(en):
    parts = re.split(r'[\s\-]+', en.strip())
    return parts[0].lower() if parts else ''

def safe_merge(a_toks, b_toks, a_first=None, b_first=None):
    if not a_toks or not b_toks:
        return False
    inter = a_toks & b_toks
    if len(inter) < 2:
        return False
    if a_first and b_first and a_first != b_first:
        return False  # 首名不同 = 不同人（如 Atiku Abubakar vs Abubakar Atiku Bagudu）
    return a_toks <= b_toks or b_toks <= a_toks

def disp_of_key(k):
    if k in apps_by_key:
        best = max(apps_by_key[k], key=lambda a: len(a['zh'] or ''))
        return f"{best['zh']} ({best['en']})" if best['zh'] else best['en']
    return old_by_pid.get(k, {}).get('disp', k)

# ---------- 3. 分组 ----------
groups = {k: {k} for k in apps_by_key}
new_keys = [k for k in groups if k.startswith('new:')]

def rep_en_str(rep):
    if rep in apps_by_key:
        return apps_by_key[rep][0]['en']
    return old_by_pid.get(rep, {}).get('en', '')

def rep_tokens(rep):
    if rep in apps_by_key:
        en = apps_by_key[rep][0]['en'].lower()
        return tokens(en)
    return old_by_pid.get(rep, {}).get('tok', set())

changed = True
while changed:
    changed = False
    # 3a. new: 键并入安全匹配的组（优先精确 en 匹配旧 registry）
    for nk in new_keys:
        if nk not in groups: continue
        en = nk[4:]
        ta = tokens(en)
        hit = None
        # 精确匹配 registry 名
        for pidk, info in old_by_pid.items():
            if info['en'].casefold() == en:
                hit = pidk; break
        if hit is None:
            for rk in list(groups.keys()):
                if rk == nk: continue
                if safe_merge(ta, rep_tokens(rk), first_tok(en), first_tok(rep_en_str(rk))):
                    hit = rk; break
        if hit is not None and hit != nk:
            if hit not in groups:
                groups[hit] = set()
            groups[hit] |= groups.pop(nk)
            changed = True
    # 3b. 组间代表名安全合并
    reps = list(groups.keys())
    for i, a in enumerate(reps):
        if a not in groups: continue
        ta = rep_tokens(a)
        for b in reps[i+1:]:
            if b not in groups or b == a: continue
            if safe_merge(ta, rep_tokens(b), first_tok(rep_en_str(a)), first_tok(rep_en_str(b))):
                groups[a] |= groups.pop(b)
                changed = True
                break
        if changed: break

print(f'分组完成: {len(groups)} 组（原 keys {len(apps_by_key)}）')

# ---------- 4. 分配 person_id ----------
max_id = max((int(m.group(1)) for pid in old_by_pid if (m := re.match(r'NG-PERSON-(\d+)', pid))), default=0)
pid_keys = [k for k in old_by_pid]

def reg_name_match(en):
    ta = tokens(en); fa = first_tok(en)
    for pidk, info in old_by_pid.items():
        if safe_merge(ta, info['tok'], fa, first_tok(info['en'])):
            return pidk
    return None

person_records = []
seen_pid = set()
for rep, members in groups.items():
    apps = []
    for k in members:
        apps.extend(apps_by_key[k])
    disp = disp_of_key(rep)
    zh, en = zh_of(disp), en_of(disp)
    qid = old_by_pid.get(rep, {}).get('qid')
    pid = rep if rep.startswith('NG-PERSON-') else None
    if pid is None:
        for k in members:
            if k.startswith('NG-PERSON-'):
                pid = k; break
    if pid is None:
        pid = reg_name_match(en)
    if pid is None:
        max_id += 1
        pid = f'NG-PERSON-{max_id:06d}'
    if pid in seen_pid:
        max_id += 1
        pid = f'NG-PERSON-{max_id:06d}'
    seen_pid.add(pid)
    person_records.append({'pid': pid, 'disp': disp, 'zh': zh or None, 'en': en,
                           'qid': qid, 'apps': apps, 'members': members})
print(f'person_id 分配完成（max={max_id}）')

# ---------- 5. importance ----------
def importance(apps):
    for a in apps:
        t = a['title'] or ''
        if re.search(r'总统|副总统|州长|首席大法官|参谋长', t):
            return 'high', '国家最高层/军种首长'
        if a['org'].startswith('NG-MIL') and re.search(r'督察长|总监察长|总队长|局长|总干事', t):
            return 'high', '安全情报机构首长'
        if a['org'].startswith('NG-PARTY') and re.search(r'全国主席|全国领袖', t) and not re.search(r'前|former', t):
            return 'high', '政党全国主席'
        if a['org'].startswith('NG-GOV') and re.search(r'执行主席|主席|行长|关长|署长|局长|总干事|注册官', t) and not re.search(r'Deputy|副', t):
            return 'high', '联邦独立机构首长'
    for a in apps:
        t = a['title'] or ''
        if re.search(r'部长|首席执行官|CEO|董事总经理|总经理|总裁|GMD|出版人|总编辑|副校长|执行总监|执行主任|执行董事|创始人|董事长|全球总监|院长|议长|主任', t):
            return 'medium', '部长级/机构首长/核心管理层'
    return 'low', '一般成员/专业人员'

# ---------- 6. registry 重建 ----------
new_preg = []
for r in person_records:
    kept_flag = any(mk in kept_keys for mk in r['members'])
    new_preg.append({
        'person_id': r['pid'],
        'name': r['disp'],
        'name_en': r['en'],
        'wikidata_qid': r['qid'],
        'status': 'listed' if kept_flag else 'trimmed',
        'source_orgs': sorted({a['org'] for a in r['apps']}),
    })
reg['person_registry'] = new_preg
reg['person_counters'] = {'NG': max_id}
json.dump(reg, open(f'{BASE}/id_registry.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
st = Counter(p['status'] for p in new_preg)
print(f'registry 重建: {len(new_preg)} 人 | {dict(st)} | counter={max_id}')

# ---------- 7. person_list ----------
plist = []
for r in person_records:
    if not any(mk in kept_keys for mk in r['members']):
        continue
    imp, imp_reason = importance(r['apps'])
    src_orgs = []
    seen = set()
    for a in r['apps']:
        if a['org'] in seen: continue
        seen.add(a['org'])
        zn, en_, ot = org_names.get(a['org'], (None, None, None))
        src_orgs.append({'org_id': a['org'],
                         'org_name': f"{zn} ({en_})" if zn and en_ else (en_ or a['org']),
                         'position_title': a['title'] or None})
    plist.append({'person_id': r['pid'], 'wikidata_qid': r['qid'], 'name': r['disp'],
                  'name_zh': r['zh'], 'name_en': r['en'], 'importance_level': imp,
                  'importance_reason': imp_reason, 'source_orgs': src_orgs,
                  'discovery_source': 'key_people', 'nationality': 'NG', 'notes': None})
rank = {'high': 0, 'medium': 1, 'low': 2}
plist.sort(key=lambda x: (rank[x['importance_level']], x['person_id']))
imp = Counter(p['importance_level'] for p in plist)
print(f'person_list（P4 收集范围）: {len(plist)} 人 | {dict(imp)}')

out = {'metadata': {'country': 'Nigeria', 'country_iso': 'NG', 'collection_date': '2026-11-14',
                    'phase': 'phase4_person_list', 'source_org_count': len(profiles), 'total_persons': len(plist)},
       'persons': plist,
       'summary': {'by_importance_level': dict(imp),
                   'by_discovery_source': {'key_people': len(plist), 'web_search': 0, 'wikidata': 0, 'wikipedia': 0, 'other': 0},
                   'data_quality': {'with_person_id': len(plist),
                                    'with_wikidata_qid': sum(1 for p in plist if p['wikidata_qid']),
                                    'without_person_id': 0}}}
json.dump(out, open(f'{BASE}/person_list.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# ---------- 8. P4 进度 + 派发表 ----------
remaining = [p['person_id'] for p in plist]
json.dump({'phase': 'P4_person_enrichment', 'started_at': '2026-11-14T00:00:00',
           'last_updated': '2026-11-14T00:00:00', 'concurrency': 4,
           'completed': [], 'remaining': remaining, 'current': [], 'failed': []},
          open(f'{BASE}/_p4_progress.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
disp = [{'person_id': p['person_id'], 'name_zh': p['name_zh'], 'name_en': p['name_en'],
         'importance': p['importance_level'], 'imp_reason': p['importance_reason'],
         'source_orgs': [{'org_id': s['org_id'], 'title': s['position_title']} for s in p['source_orgs']]}
        for p in plist]
json.dump(disp, open('scripts_tmp/_p4_dispatch.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'_p4_progress.json: remaining={len(remaining)} | 派发表 scripts_tmp/_p4_dispatch.json')
for p in plist[:8]:
    print(f"  {p['person_id']} | {p['importance_level']} | {p['name'][:44]}")

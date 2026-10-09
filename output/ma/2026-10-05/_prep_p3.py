# 修复 + P3 准备：GOV-019 移除、P1 官名回填、改名、派发表与进度文件
import json, os, datetime

D = 'output/ma/2026-10-05'
now = datetime.datetime.now().isoformat(timespec='seconds')

# ---- 1. remove MA-GOV-019 (historical 2016-2021 ministry entity, duplicate of MA-GOV-016) ----
oid = 'MA-GOV-019'
if os.path.exists(f'{D}/orgs/{oid}.json'):
    os.remove(f'{D}/orgs/{oid}.json')
reg = json.load(open(f'{D}/id_registry.json', encoding='utf-8'))
reg['registry'] = [r for r in reg['registry'] if r['org_id'] != oid]
json.dump(reg, open(f'{D}/id_registry.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
targets = json.load(open(f'{D}/_target_orgs.json', encoding='utf-8'))
targets = [t for t in targets if t['id'] != oid]
json.dump(targets, open(f'{D}/_target_orgs.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
audit = json.load(open(f'{D}/_excluded_orgs.json', encoding='utf-8'))
if not any(e['org_id'] == oid for e in audit['excluded']):
    audit['excluded'].append({'org_id': oid, 'reason': 'Historical 2016-2021 cabinet entity of the ministry; current institution is MA-GOV-016 (Q26459282, mjcc.gov.ma). User-confirmed removal.'})
json.dump(audit, open(f'{D}/_excluded_orgs.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('MA-GOV-019 removed')

tmap = {t['id']: t for t in targets}

# ---- 2. name/alias repairs ----
def patch(fname, fn):
    p = f'{D}/orgs/{fname}'
    o = json.load(open(p, encoding='utf-8'))
    fn(o['basic_info'], o)
    json.dump(o, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# 2a. bulk: merge P1 official name + aliases into profile aliases; upgrade name_en when P1 more specific
upgrades = alias_added = 0
for f in sorted(os.listdir(f'{D}/orgs')):
    if not f.endswith('.json') or f.startswith('_'):
        continue
    oid = f[:-5]
    t = tmap.get(oid)
    if not t:
        continue
    def fn(bi, o, t=t):
        global upgrades, alias_added
        al = bi.get('aliases') or []
        low = {a.strip().lower() for a in al}
        p1_name = (t.get('name') or '').strip()
        new = []
        for cand in [p1_name] + list(t.get('aliases') or []):
            c = (cand or '').strip()
            if c and c.lower() not in low and c.lower() != (bi.get('name_en') or '').strip().lower():
                new.append(c); low.add(c.lower())
        if new:
            al += new; alias_added += len(new)
        nen = (bi.get('name_en') or '').strip()
        if p1_name and nen and nen.lower() in p1_name.lower() and p1_name.lower() != nen.lower():
            al = [a for a in al if a.lower() != nen.lower()] + [nen]
            bi['name_en'] = p1_name
            upgrades += 1
        bi['aliases'] = al
    patch(f, fn)
print(f'alias merge done: +{alias_added} aliases, {upgrades} name_en upgraded to P1 official name')

# 2b. point fixes
def fix_soe004(bi, o):
    bi['name_en'] = 'Phosboucraa'
    bi['name_original'] = 'فوسبوكرة'
patch('MA-SOE-004.json', fix_soe004)

def fix_mil001(bi, o):
    if bi.get('founded_date') == '1088-01-01':
        bi['founded_date'] = None
patch('MA-MIL-001.json', fix_mil001)

def fix_fin012(bi, o):
    bi['name_en'] = 'Sanlam Maroc'
    al = bi.get('aliases') or []
    for c in ['Saham Assurance', 'SanlamAllianz Maroc']:
        if c not in al:
            al.append(c)
    bi['aliases'] = al
patch('MA-FIN-012.json', fix_fin012)

def fix_fin009(bi, o):
    bi['name_en'] = 'BMCI'
    al = bi.get('aliases') or []
    for c in ["Banque Marocaine du Commerce et de l'Industrie", 'Banque Commerciale du Maroc', 'BNP Paribas Maroc']:
        if c not in al:
            al.append(c)
    bi['aliases'] = al
patch('MA-FIN-009.json', fix_fin009)

def fix_corp008(bi, o):
    if bi.get('name_en') == 'cosumar':
        bi['name_en'] = 'Cosumar'
patch('MA-CORP-008.json', fix_corp008)
print('point fixes done (SOE-004 names, MIL-001 date null, FIN-012 Sanlam, FIN-009 BMCI, CORP-008 Cosumar)')

# ---- 3. dispatch table in category priority order ----
ORDER = ['GOV', 'SOE', 'CORP', 'FIN', 'ACAD', 'MEDIA', 'PARTY', 'NGO', 'MIL', 'INTL']
params = {}
for f in sorted(os.listdir(f'{D}/orgs')):
    if f.endswith('.json') and not f.startswith('_'):
        o = json.load(open(f'{D}/orgs/{f}', encoding='utf-8'))
        bi = o['basic_info']
        params[o['org_id']] = {
            'name_en': bi.get('name_en'), 'name_zh': bi.get('name_zh'),
            'name_local': bi.get('name_original'), 'website': bi.get('website'),
            'category': bi['org_type'], 'filepath': f'{D}/orgs/{o["org_id"]}.json',
        }
queue = sorted(params, key=lambda x: (ORDER.index(params[x]['category']), x))
json.dump(params, open(f'{D}/_org_params.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

progress = {
    'phase': 'P3_org_enrichment',
    'started_at': now, 'last_updated': now,
    'completed': [], 'remaining': queue, 'current': [], 'failed': [],
}
json.dump(progress, open(f'{D}/_phase_progress.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('queue:', len(queue), '| first 5:', queue[:5])

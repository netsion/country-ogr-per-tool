"""Fix HK person schema errors: birth_date format, family/platform enums, malformed person_relationships."""
import json, glob, os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PERSONS_DIR = 'output/hk/2026-07-24/persons'
FAMILY = {'spouse','father','mother','son','daughter','brother','sister','grandfather','grandmother','uncle','aunt','cousin','father_in_law','mother_in_law','brother_in_law','sister_in_law','son_in_law','daughter_in_law','other'}
PLAT = {'twitter_x','facebook','linkedin','youtube','instagram','telegram','tiktok','threads','mastodon','wechat','weibo','github','gitlab','medium','substack','other'}
PRT = {'spouse','parent','child','sibling','grandparent','grandchild','uncle_aunt','cousin','in_law','mentor','mentee','ally','rival','colleague','superior','subordinate','business_partner','political_ally','political_rival','associate','other'}
STRICT = re.compile(r'^\d{4}-\d{2}-\d{2}$')
FLEX = re.compile(r'^\d{4}(-\d{2})?$')
YEAR_IN_TEXT = re.compile(r'(19|20)\d{2}')

def fam_infer(rel, desc, name):
    text = f'{rel or ""} {desc or ""} {name or ""}'
    if re.search(r'父亲|父親|家父|其父', text): return 'father'
    if re.search(r'母亲|母親|其母', text): return 'mother'
    if re.search(r'长子|長子|儿子|兒子|幼子|次子|其子|一子', text): return 'son'
    if re.search(r'女儿|女兒|长女|長女|幼女|其女', text): return 'daughter'
    if re.search(r'配偶|妻子|丈夫|夫人|夫', text): return 'spouse'
    if rel == '舅父': return 'uncle'
    if re.search(r'弟|兄|兄弟', text): return 'brother'
    if re.search(r'姐|妹|姐妹', text): return 'sister'
    if re.search(r'祖父|爺爺', text): return 'grandfather'
    if re.search(r'祖母|奶奶', text): return 'grandmother'
    return 'other'

def norm_birth(v):
    """Return (new_value, note_or_None)."""
    if STRICT.match(v): return v, None
    if FLEX.match(v): return v + '-01' * (2 - v.count('-')), None
    m = re.match(r'^约?(\d{4})年', v)
    if not m:
        m = YEAR_IN_TEXT.search(v)
    if m:
        y = m.group(0) if m.re is YEAR_IN_TEXT else m.group(1)
        y = m.group(0) if YEAR_IN_TEXT.fullmatch(m.group(0)) else y
        y = re.search(r'(19|20)\d{2}', m.group(0)).group(0)
        return f'{y}-01-01', f'birth_date 原始值为「{v}」，按年份归一化'
    return None, f'birth_date 无法解析: {v}'

changed = {}
for f in sorted(glob.glob(os.path.join(PERSONS_DIR, '*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    pid = d.get('person_id', os.path.basename(f))
    fixes = []
    notes = []

    bd = d.get('birth_date')
    if isinstance(bd, str):
        nb, note = norm_birth(bd)
        if nb != bd:
            d['birth_date'] = nb
            fixes.append(f'birth_date: {bd!r} -> {nb!r}')
            if note: notes.append(note)

    for i, fm in enumerate(d.get('family_members') or []):
        rel = fm.get('relationship')
        if rel in FAMILY: continue
        new = fam_infer(rel, fm.get('industry_or_organization'), fm.get('name'))
        fm['relationship'] = new
        fixes.append(f'family[{i}].relationship: {rel!r} -> {new!r}')

    for i, sa in enumerate(d.get('social_accounts') or []):
        p = sa.get('platform')
        if p == 'twitter':
            sa['platform'] = 'twitter_x'; fixes.append(f'platform[{i}]: twitter -> twitter_x')
        elif p not in PLAT:
            sa['platform'] = 'other'; fixes.append(f'platform[{i}]: {p!r} -> other')

    prs = d.get('person_relationships') or []
    keep = []
    for i, pr in enumerate(prs):
        t = pr.get('relationship_type')
        if t == 'mentor_of':
            pr['relationship_type'] = 'mentor'; fixes.append(f'rel_type[{i}]: mentor_of -> mentor'); keep.append(pr)
        elif t in PRT:
            keep.append(pr)
        elif 'person_name' in pr and 'relationship_type' in pr:
            keep.append(pr)
        else:
            fixes.append(f'removed malformed person_relationships[{i}]: {json.dumps(pr, ensure_ascii=False)[:80]}')
            notes.append(f'移除畸形 person_relationships 条目（org 形对象误入，角色已在 work_experience 覆盖）: {pr.get("org_name")}')
    d['person_relationships'] = keep

    for i, we in enumerate(d.get('work_experience') or []):
        sd = we.get('start_date')
        if sd == '2010年代':
            we['start_date'] = '2010'; fixes.append(f'we[{i}].start_date: 2010年代 -> 2010')
        elif isinstance(sd, str) and not FLEX.match(sd) and not STRICT.match(sd):
            m = YEAR_IN_TEXT.search(sd)
            if m:
                we['start_date'] = m.group(0); fixes.append(f'we[{i}].start_date: {sd!r} -> {m.group(0)}')

    if fixes:
        cm = d.setdefault('collection_meta', {})
        if notes:
            cm['notes'] = ((cm.get('notes') or '') + ' | ' + '；'.join(notes)).strip(' |')
        tmp = f + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as out:
            json.dump(d, out, ensure_ascii=False, indent=2)
        os.replace(tmp, f)
        changed[pid] = fixes

print(f'Changed {len(changed)} files')
for pid, fixes in changed.items():
    print(f'\n{pid}:')
    for x in fixes: print(f'  {x}')

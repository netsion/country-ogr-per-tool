"""Normalize nonstandard field shapes in ID P4 new person files (000425-000770) to schema."""
import json, glob, os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PERSONS = 'output/id/2026-07-27/persons'
REL_ENUM = {'spouse','parent','child','sibling','grandparent','grandchild','uncle_aunt','cousin',
            'in_law','mentor','mentee','ally','rival','colleague','superior','subordinate',
            'business_partner','political_ally','political_rival','associate','other'}

def map_rel(rel):
    if not rel: return 'other'
    r = str(rel).strip()
    if r in REL_ENUM: return r
    if any(k in r for k in ('夫','妻','配偶','husband','wife','spouse')): return 'spouse'
    if any(k in r for k in ('父','母','双亲','father','mother','parent')): return 'parent'
    if any(k in r for k in ('兄','弟','姐','妹','sibling','brother','sister')): return 'sibling'
    if any(k in r for k in ('祖父','祖母','外祖','grandparent')): return 'grandparent'
    if r in ('子','女','儿子','女儿','son','daughter'): return 'child'
    if any(k in r for k in ('孙','grandchild')): return 'grandchild'
    if any(k in r for k in ('叔','伯','舅','姑','姨','uncle','aunt')): return 'uncle_aunt'
    if any(k in r for k in ('堂','表','cousin')): return 'cousin'
    if any(k in r for k in ('姻','in-law','in_law')): return 'in_law'
    if any(k in r for k in ('导师','mentor')): return 'mentor'
    if any(k in r for k in ('商业伙伴','business partner')): return 'business_partner'
    if any(k in r for k in ('政治盟友','political ally')): return 'political_ally'
    if any(k in r for k in ('政治对手','political rival')): return 'political_rival'
    if any(k in r for k in ('同事','colleague')): return 'colleague'
    if any(k in r for k in ('上司','上级','superior','boss')): return 'superior'
    if any(k in r for k in ('下属','部下','subordinate')): return 'subordinate'
    if any(k in r for k in ('盟友','ally')): return 'ally'
    if any(k in r for k in ('对手','rival')): return 'rival'
    return 'other'

def fix_str(s):
    return s.replace('“','"').replace('”','"').replace('‘',"'").replace('’',"'")

def deep_fix_quotes(o):
    if isinstance(o, str): return fix_str(o)
    if isinstance(o, list): return [deep_fix_quotes(x) for x in o]
    if isinstance(o, dict): return {k: deep_fix_quotes(v) for k, v in o.items()}
    return o

stats = dict(wx_title=0, rel_dropped=0, rel_fixed=0, edu_school=0, edu_dropped=0,
             ach_converted=0, ach_noyear=0, files=0)

for f in sorted(glob.glob(os.path.join(PERSONS, 'ID-PERSON-*.json'))):
    num = int(os.path.basename(f).split('-')[-1].split('.')[0])
    if num < 425: continue
    d = json.load(open(f, encoding='utf-8'))
    changed = False

    # work_experience: title -> position
    for w in d.get('work_experience') or []:
        pos = (w.get('position') or '').strip()
        title = (w.get('title') or '').strip()
        if not pos and title:
            w['position'] = title
            stats['wx_title'] += 1
            changed = True
        if 'title' in w:
            w.pop('title')
            changed = True

    # person_relationships: normalize to {person_id, person_name, relationship_type, description}
    new_rels = []
    for r in d.get('person_relationships') or []:
        pname = (r.get('person_name') or '').strip()
        if not pname:
            pname = (r.get('related_person_name') or '').strip()
        if not pname:
            stats['rel_dropped'] += 1
            changed = True
            continue
        pid = r.get('person_id') or r.get('related_person_id') or None
        rel = r.get('relationship_type') or r.get('relationship') or r.get('relation') or r.get('relation_type')
        desc = r.get('description') or r.get('notes') or None
        extra = []
        if r.get('title'): extra.append(r['title'])
        if r.get('org_name'): extra.append(r['org_name'])
        if r.get('source'): extra.append('source: ' + str(r['source']))
        if extra and desc: desc = desc + '（' + '；'.join(extra) + '）'
        elif extra: desc = '；'.join(extra)
        new_rels.append({'person_id': pid, 'person_name': pname,
                         'relationship_type': map_rel(rel), 'description': desc})
        changed = True
        stats['rel_fixed'] += 1
    if d.get('person_relationships') != new_rels:
        d['person_relationships'] = new_rels

    # education: school -> institution; drop institution-less entries
    new_edu = []
    for e in d.get('education') or []:
        inst = (e.get('institution') or '').strip()
        if not inst:
            inst = (e.get('school') or '').strip()
            if inst:
                e['institution'] = inst
                stats['edu_school'] += 1
                changed = True
        if not (e.get('institution') or '').strip():
            stats['edu_dropped'] += 1
            changed = True
            continue
        new_edu.append(e)
    if d.get('education') != new_edu:
        d['education'] = new_edu

    # major_achievements: string -> object
    new_ach = []
    for a in d.get('major_achievements') or []:
        if isinstance(a, str):
            m = re.search(r'(19|20)\d{2}', a)
            if m:
                new_ach.append({'date': m.group(0), 'achievement': a, 'organization': None})
                stats['ach_converted'] += 1
            else:
                new_ach.append({'date': 'unknown', 'achievement': a, 'organization': None})
                stats['ach_noyear'] += 1
            changed = True
        else:
            new_ach.append(a)
    if d.get('major_achievements') != new_ach:
        d['major_achievements'] = new_ach

    d2 = deep_fix_quotes(d)
    if d2 != d:
        d = d2
        changed = True

    if changed:
        tmp = f + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as o:
            json.dump(d, o, ensure_ascii=False, indent=2)
        os.replace(tmp, f)
        stats['files'] += 1

print(stats)

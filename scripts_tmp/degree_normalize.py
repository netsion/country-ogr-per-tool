# -*- coding: utf-8 -*-
"""Normalize all non-standard education.degree values to the 8-value enum.

Rules (documented in docs/degree-enum.md):
  - literal 'null' string -> field set to None
  - everything else mapped via rule(); unmatchable -> 'other'
  - original value preserved in degree_note (appended) if degree_note absent
"""
import glob, json, os, re, sys, time
from collections import Counter

BASE = 'D:/ai-workspace/apec-osint-tool'
STANDARD = {'primary','high_school','associate','bachelor','master','doctorate','professional','other'}

def rule(v):
    s = v.strip(); low = s.lower()
    if low in ('phd','ph.d','dphil','doctor','doctorate','doctor of philosophy','doctorate degree','doctor of business administration (dba)','dba','doctor of law'):
        return 'doctorate'
    if low in ('mba','emba','master of public administration (mpa)','master of healthcare administration','master of law','master of arts in law and diplomacy (maid)','corporate master in business administration','master','硕士','硕士学位','msc','ma'):
        return 'master'
    if low.startswith('bachelor') or low in ('ba','bsc','llb','b.a.','b.s.','ll.b. (hons)','bba','mbbs (bachelor of medicine, bachelor of surgery)','ijazah sarjana muda pengurusan perniagaan','法学学位','法律学位','学士'):
        return 'bachelor'
    if low in ('associate','副学士','专科','大专','associate degree'):
        return 'associate'
    if low in ('secondary','middle_school','中学','中学教育','初中','高中','form_six','a-level','gcse（o level）及 gce a level','matrikulasi','大学先修班','大学先修班（中六）','中五毕业','spm','sijil rendah pelajaran (srp)'):
        return 'high_school'
    if low in ('primary','primary school','小学'):
        return 'primary'
    if low in ('foundation',):
        return 'high_school'
    if low in ('certificate','diploma','training','professional certification','vocational','btec national diploma','diploma in public administration','diploma in management (executive)','律师资格','特许会计师 (chartered accountant)','大律师资格（barrister-at-law）','executive_program','高级政治理论（cao cấp）','伊斯兰宗教研究','examination in accounting, financial statement analysis and asset valuation'):
        return 'professional'
    if '荣誉博士' in s or 'honorary' in low: return 'doctorate'
    if re.search(r'\b(phd|ph\.d|dphil|jd|juris doctor)\b', low): return 'doctorate'
    if re.search(r'\bmba\b', low): return 'master'
    if re.search(r'\b(llm|mphil|msc|mpa|m\.a\.|m\.s\.|master)\b', low): return 'master'
    if re.search(r'\b(llb|bsc|ba\b|b\.a\.|b\.s\.|beng|btech|bba|bachelor)\b', low): return 'bachelor'
    if low in ('specialist','specialty','residency','medical'): return 'professional'
    if low in ('candidate','candidate_of_sciences'): return 'doctorate'
    if low == 'law': return 'bachelor'
    if low in ('postgraduate',) or '研究生' in s: return 'master'
    if '博士后' in s: return 'doctorate'
    if '工程师' in s or '研究员' in s: return 'professional'
    if '荣誉' in s and '博士' in s: return 'doctorate'
    if '硕士' in s: return 'master'
    if '博士' in s: return 'doctorate'
    if '学士' in s: return 'bachelor'
    if any(k in s for k in ('小学','elementary')): return 'primary'
    if any(k in s for k in ('中学','高中','初中','secondary')): return 'high_school'
    if any(k in s for k in ('研修','培训','进修','结业','课程','certificate','training','diploma','文凭','证书','干部','党校','资格')): return 'professional'
    if '专科' in s or '大专' in s: return 'associate'
    return None  # literal 'null' or unmatchable

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

def main():
    apply = '--apply' in sys.argv
    stats = Counter(); changes = []
    for f in sorted(glob.glob(BASE + '/output/[a-z][a-z]/20*/persons/*.json')):
        if os.path.basename(f).startswith('_'):
            continue
        d = json.load(open(f, encoding='utf-8'))
        dirty = False
        for e in d.get('education') or []:
            if not isinstance(e, dict):
                continue
            v = e.get('degree')
            if not isinstance(v, str):
                continue
            s = v.strip()
            if not s or s in STANDARD:
                continue
            if s.lower() == 'null':
                e['degree'] = None
                stats['literal_null_cleared'] += 1
                dirty = True
                changes.append({'file': os.path.relpath(f, BASE).replace(os.sep,'/'),
                                'person_id': d.get('person_id'), 'old': v, 'new': None})
                continue
            r = rule(s) or 'other'
            note = f'原 degree 值「{s}」已归一为 {r}'
            if not e.get('degree_note'):
                e['degree_note'] = note
            else:
                e['degree_note'] = e['degree_note'] + '；' + note
            e['degree'] = r
            stats['fixed'] += 1
            stats['to_' + r] += 1
            dirty = True
            changes.append({'file': os.path.relpath(f, BASE).replace(os.sep,'/'),
                            'person_id': d.get('person_id'), 'old': v, 'new': r})
        if apply and dirty:
            save(f, d)
    summary = {'apply': apply, **dict(stats)}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    tag = 'apply' if apply else 'dry'
    json.dump({'summary': summary, 'changes': changes},
              open(BASE + f'/output/_id_audit/degree_normalize_{tag}.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('->', BASE + f'/output/_id_audit/degree_normalize_{tag}.json')

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""P2 batch 7 plan: fill null IDs where an existing profile matches by name.

Respects the user's acceptance rule: no-profile / no-registry refs are fine;
only fill when a profile already exists and the ref name matches strictly.
"""
import csv, glob, json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from id_integrity_audit2 import BASE, OUT, load_datasets
from p2_plan_strict import strict_match, clean, core

ALLOWED = {'CORP','FIN','SOE','ACAD','MEDIA','NGO','INTL'}

def get_name(x, cat):
    keys={'work_org':('organization','org_name','organization_en'),'person_rel':('person_name','name'),'family':('name','person_name')}[cat]
    for k in keys:
        v=x.get(k)
        if isinstance(v,str) and v.strip(): return v.strip()
    return ''

def main():
    latest,_=load_datasets()
    plan=json.load(open(os.path.join(OUT,'repair_plan.json'),encoding='utf-8'))['null_fill']
    org={}; per={}
    for cc,(date,folder) in latest.items():
        for f in glob.glob(os.path.join(folder,'orgs','*.json')):
            if os.path.basename(f).startswith('_'): continue
            d=json.load(open(f,encoding='utf-8')); oid=d.get('org_id'); bi=d.get('basic_info') or {}
            if oid: org[oid]={'names':[v for v in [bi.get('name_zh'),bi.get('name_en'),bi.get('name_original')] if isinstance(v,str) and v.strip()],'type':bi.get('org_type')}
        for f in glob.glob(os.path.join(folder,'persons','*.json')):
            if os.path.basename(f).startswith('_'): continue
            d=json.load(open(f,encoding='utf-8')); pid=d.get('person_id'); bi=d.get('basic_info') or {}
            if pid: per[pid]={'names':[v for v in [d.get('name'),d.get('name_en'),d.get('name_zh'),d.get('name_original'),bi.get('name_zh'),bi.get('name_en'),bi.get('name_original')] if isinstance(v,str) and v.strip()]}
    rows=[]; skipped=Counter()
    for r in plan:
        cat=r.get('cat'); cc=r.get('cc'); ref=r.get('ref_name'); t=r.get('suggested')
        if cat=='work_org':
            m=org.get(t)
            if not m: skipped['target_missing']+=1; continue
            kind=strict_match(ref,m['names'])
            if not kind: skipped['strict_no']+=1; continue
            same=t[:2].lower()==cc
            if not same:
                if m.get('type') not in ALLOWED:
                    skipped['cross_type_excluded']+=1; continue
                if any(ch.isalpha() and ord(ch)<128 for ch in ref):
                    if kind not in ('full_exact','latin_exact'):
                        skipped['cross_latin_mismatch']+=1; continue
                elif len(core(ref))<4:
                    skipped['cross_short']+=1; continue
            fld='org_id'
        else:
            m=per.get(t)
            if not m: skipped['target_missing']+=1; continue
            kind=strict_match(ref,m['names'])
            if not kind: skipped['strict_no']+=1; continue
            if t[:2].lower()!=cc:
                skipped['person_cross']+=1; continue
            fld='person_id'
        folder=latest.get(cc,(None,None))[1]
        if not folder: skipped['no_dataset']+=1; continue
        src_id=r.get('person_id') if cat in ('work_org','person_rel','family') else None
        sub='persons'
        arr={'work_org':'work_experience','person_rel':'person_relationships','family':'family_members'}[cat]
        sf=os.path.join(folder,sub,str(src_id)+'.json')
        if not os.path.exists(sf): skipped['source_missing']+=1; continue
        d=json.load(open(sf,encoding='utf-8'))
        found=0
        for i,x in enumerate(d.get(arr) or []):
            if not isinstance(x,dict): continue
            if x.get(fld) not in (None,''): continue
            if get_name(x,cat)!=ref: continue
            found+=1
            rows.append({'cat':cat,'cc':cc,'file':os.path.relpath(sf,BASE).replace(os.sep,'/'),'array':arr,'index':i,'source_id':src_id,'ref_name':ref,'current_id':x.get(fld),'target_id':t,'target_name':(m['names'][0] if m['names'] else ''),'match_kind':kind,'scope':'same_cc' if t[:2].lower()==cc else 'cross'})
        if not found: skipped['position_not_found']+=1
    seen=set(); uniq=[]
    for r in rows:
        k=(r['file'],r['array'],r['index'])
        if k in seen: continue
        seen.add(k); uniq.append(r)
    rows=uniq
    sample=[]
    for cat in ('work_org','person_rel','family'): sample += [r for r in rows if r['cat']==cat][:40]
    sample=sample[:100]
    p=os.path.join(OUT,'p2_nullfill_plan.csv')
    with open(p,'w',encoding='utf-8-sig',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    sp=os.path.join(OUT,'p2_nullfill_sample.csv')
    with open(sp,'w',encoding='utf-8-sig',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(sample)
    summary={'rows':len(rows),'by_cat':dict(Counter(r['cat'] for r in rows)),'by_scope':dict(Counter(r['scope'] for r in rows)),'skipped':dict(skipped),'sample':len(sample)}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    json.dump({'summary':summary,'rows':rows,'sample':sample},open(os.path.join(OUT,'p2_nullfill_plan.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('plan ->',p); print('sample ->',sp)

if __name__=='__main__': main()

# -*- coding: utf-8 -*-
"""P2 batch 6: null empty / invalid-format IDs that resolve nowhere.

Only IDs that do NOT match the expected org/person ID pattern and are absent
from every registry/profile are touched. Valid-format dangling IDs are kept.
"""
import glob, json, os, re, sys, time
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from id_integrity_audit2 import BASE, OUT, load_datasets

ORG_RE = re.compile(r'^[A-Z]{2}-[A-Z]+-[0-9]{3}$')
PERSON_RE = re.compile(r'^[A-Z]{2}-PERSON-[0-9]{6}$')

def save_json(path,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=path+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,path); return
        except PermissionError: time.sleep(.5)
    open(path,'w',encoding='utf-8',newline='\n').write(payload)

def main():
    apply='--apply' in sys.argv
    latest,_=load_datasets()
    allids=set()
    for f in glob.glob(os.path.join(BASE,'output/[a-z][a-z]/20*/id_registry.json')):
        d=json.load(open(f,encoding='utf-8'))
        for k in ['registry','person_registry','deprecated_registry','deprecated_person_registry']:
            for e in d.get(k) or []:
                v=e.get('org_id') or e.get('person_id')
                if v: allids.add(v)
    for f in glob.glob(os.path.join(BASE,'output/[a-z][a-z]/20*/orgs/*.json'))+glob.glob(os.path.join(BASE,'output/[a-z][a-z]/20*/persons/*.json')):
        if os.path.basename(f).startswith('_'): continue
        d=json.load(open(f,encoding='utf-8')); v=d.get('org_id') or d.get('person_id')
        if v: allids.add(v)
    changes=[]; stats=Counter()
    for cc,(date,folder) in sorted(latest.items()):
        for sub,arrs in [('persons',[('work_experience','org_id','org'),('person_relationships','person_id','person'),('family_members','person_id','person')]),('orgs',[('key_people','person_id','person'),('related_entities','org_id','org')])]:
            for f in glob.glob(os.path.join(folder,sub,'*.json')):
                if os.path.basename(f).startswith('_'): continue
                d=json.load(open(f,encoding='utf-8')); dirty=False
                for arr,field,kind in arrs:
                    pat=ORG_RE if kind=='org' else PERSON_RE
                    for i,x in enumerate(d.get(arr) or []):
                        if not isinstance(x,dict): continue
                        v=x.get(field)
                        if v is None: continue
                        if not isinstance(v,str):
                            continue
                        if v=='' or (v not in allids and not pat.match(v)):
                            changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':arr,'index':i,'field':field,'old':v,'new':None,
                                            'reason':'empty' if not v else 'invalid_format',
                                            'ref_name':x.get('organization') or x.get('org_name') or x.get('person_name') or x.get('name') or ''})
                            x[field]=None; dirty=True
                            stats['empty' if not v else 'invalid_format']+=1; stats[arr]+=1
                if apply and dirty: save_json(f,d)
    summary={'apply':apply,'refs_nulled':sum(stats[k] for k in ('empty','invalid_format')),
             'by_reason':{k:stats[k] for k in ('empty','invalid_format')},
             'by_array':{k:v for k,v in stats.items() if k not in ('empty','invalid_format')}}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        p=os.path.join(OUT,'p2_batch6_invalid_ids_undo.json')
        json.dump({'summary':summary,'changes':changes},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print('undo ->',p)
    else: print('DRY')
if __name__=='__main__': main()

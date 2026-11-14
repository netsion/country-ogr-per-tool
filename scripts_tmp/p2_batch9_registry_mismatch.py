# -*- coding: utf-8 -*-
"""P2 batch 9: null refs pointing to a registered ID whose names do not match.

Only when the current ID has NO profile and at least one active registry name;
if the ref name matches any registry name, keep it. This is the
'registry_wrong_name' class: the ID is a registered but wrong identity.
"""
import glob, json, os, sys, time
from collections import Counter, defaultdict
sys.path.insert(0,os.path.dirname(__file__))
from id_integrity_audit2 import BASE, OUT, load_datasets, match, sig
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def name_of(x,cat):
    keys={'work_org':('organization','org_name','organization_en'),'related_org':('org_name','name','organization'),'person_rel':('person_name','name'),'family':('name','person_name'),'key_people':('name','name_en','person_name')}[cat]
    for k in keys:
        v=x.get(k)
        if isinstance(v,str) and v.strip(): return v.strip()
    return ''
def main():
    apply='--apply' in sys.argv
    latest,_=load_datasets()
    reg=defaultdict(list); prof=set()
    for cc,(date,folder) in latest.items():
        rp=os.path.join(folder,'id_registry.json')
        if os.path.exists(rp):
            d=json.load(open(rp,encoding='utf-8'))
            for e in d.get('registry') or []:
                oid=e.get('org_id')
                if oid and e.get('name'): reg[oid].append(e['name'])
            for e in d.get('person_registry') or []:
                pid=e.get('person_id')
                if pid and e.get('name'): reg[pid].append(e['name'])
        for sub in ('orgs','persons'):
            for f in glob.glob(os.path.join(folder,sub,'*.json')):
                if os.path.basename(f).startswith('_'): continue
                d=json.load(open(f,encoding='utf-8')); v=d.get('org_id') or d.get('person_id')
                if v: prof.add(v)
    changes=[]; stats=Counter()
    for cc,(date,folder) in sorted(latest.items()):
        for sub,arrs in [('persons',[('work_experience','org_id','work_org'),('person_relationships','person_id','person_rel'),('family_members','person_id','family')]),('orgs',[('key_people','person_id','key_people'),('related_entities','org_id','related_org')])]:
            for f in glob.glob(os.path.join(folder,sub,'*.json')):
                if os.path.basename(f).startswith('_'): continue
                d=json.load(open(f,encoding='utf-8')); dirty=False
                for arr,field,cat in arrs:
                    for i,x in enumerate(d.get(arr) or []):
                        if not isinstance(x,dict): continue
                        v=x.get(field); nm=name_of(x,cat)
                        if not isinstance(v,str) or not nm or v in prof or v not in reg: continue
                        if any(match(sig(nm),(sig(n)[0],[])) for n in reg[v]): continue
                        changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':arr,'index':i,'field':field,'old':v,'new':None,'ref_name':nm,'reg_names':reg[v][:5],'cat':cat})
                        x[field]=None; dirty=True; stats[cat]+=1
                if apply and dirty: save(f,d)
    summary={'apply':apply,'refs_nulled':sum(stats.values()),'by_cat':dict(stats)}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        p=os.path.join(OUT,'p2_batch9_registry_mismatch_undo.json'); json.dump({'summary':summary,'changes':changes},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('undo ->',p)
    else:
        p=os.path.join(OUT,'p2_batch9_registry_mismatch_dry.json'); json.dump({'summary':summary,'changes':changes},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('dry ->',p); print('DRY')
if __name__=='__main__': main()

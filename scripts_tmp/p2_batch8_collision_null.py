# -*- coding: utf-8 -*-
"""P2 batch 8: null references that point at a collision shadow identity.

Uses the live collision report: for each current ID with multiple identities,
if the ref name matches a shadow name and not the owner profile name, the ID is
an incorrect link. Null it (text remains), which is acceptable under the new
acceptance rule.
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
    cr=json.load(open(os.path.join(OUT,'collision_report.json'),encoding='utf-8'))['collisions']
    maps={'org':{},'person':{}}
    for kind in ('org','person'):
        for cc,ids in (cr.get(kind) or {}).items():
            for oid,info in ids.items():
                owner=info.get('profile_name') or ''
                shadows=info.get('shadow_names') or []
                maps[kind][oid]=(owner,[sig(x) for x in shadows if x])
    changes=[]; stats=Counter()
    for cc,(date,folder) in sorted(latest.items()):
        for sub,arrs in [('persons',[('work_experience','org_id','org','work_org'),('person_relationships','person_id','person','person_rel'),('family_members','person_id','person','family')]),('orgs',[('key_people','person_id','person','key_people'),('related_entities','org_id','org','related_org')])]:
            for f in glob.glob(os.path.join(folder,sub,'*.json')):
                if os.path.basename(f).startswith('_'): continue
                d=json.load(open(f,encoding='utf-8')); dirty=False
                for arr,field,kind,cat in arrs:
                    for i,x in enumerate(d.get(arr) or []):
                        if not isinstance(x,dict): continue
                        v=x.get(field); nm=name_of(x,cat)
                        if not isinstance(v,str) or not nm or v not in maps[kind]: continue
                        owner,shadows=maps[kind][v]
                        if owner and match(sig(nm),(sig(owner)[0],[])): continue
                        if any(match(sig(nm),(s[0],[])) for s in shadows):
                            changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':arr,'index':i,'field':field,'old':v,'new':None,'ref_name':nm,'owner':owner,'cat':cat})
                            x[field]=None; dirty=True; stats[cat]+=1
                if apply and dirty: save(f,d)
    summary={'apply':apply,'refs_nulled':sum(stats.values()),'by_cat':dict(stats)}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        p=os.path.join(OUT,'p2_batch8_collision_undo.json'); json.dump({'summary':summary,'changes':changes},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('undo ->',p)
    else:
        p=os.path.join(OUT,'p2_batch8_collision_dry.json'); json.dump({'summary':summary,'changes':changes},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('dry ->',p); print('DRY')
if __name__=='__main__': main()

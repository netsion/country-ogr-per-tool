# -*- coding: utf-8 -*-
"""P3: generic person registry collision cleanup for SG/UZ/TH/KR/MX/ID/PG/VN.

Same logic as RU script: refs pointing at a collision ID are matched against
each registry shadow name; if the shadow name resolves uniquely to another
profile -> relink; else null. Then archive all non-owner registry entries.
"""
import glob,json,os,sys,time
from collections import Counter,defaultdict
sys.path.insert(0,os.path.dirname(__file__))
from id_integrity_audit2 import BASE,OUT,load_datasets,match,sig
CCS=['sg','uz','th','kr','mx','id','pg','vn']
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def nm(x):
    for k in ('person_name','name'):
        v=x.get(k)
        if isinstance(v,str) and v.strip(): return v.strip()
    return ''
def main():
    apply='--apply' in sys.argv
    cr=json.load(open(BASE+'/output/_id_audit/collision_report.json',encoding='utf-8'))
    latest,_=load_datasets()
    undo={'registry':[],'refs':[]}; stats=Counter()
    for cc in CCS:
        col=cr['collisions']['person'].get(cc) or {}
        if not col: continue
        folder=latest[cc][1]
        name2pid=defaultdict(set); profiles=set()
        for f in glob.glob(os.path.join(folder,'persons','*.json')):
            d=json.load(open(f,encoding='utf-8')); pid=d.get('person_id')
            if pid: profiles.add(pid)
            vals=[d.get('name'),d.get('name_zh'),d.get('name_en')]+list(d.get('aliases') or [])
            for v in vals:
                if isinstance(v,str) and v.strip(): name2pid[v.strip()].add(pid)
        for oid,info in col.items():
            has_profile=oid in profiles
            owner=info.get('profile_name'); owner_toks=set((owner or '').split())
            for sh in (info.get('shadow_names') or []):
                cands={p for p in (name2pid.get(sh) or set()) if p!=oid}
                target=next(iter(cands)) if len(cands)==1 else None
                for f in glob.glob(os.path.join(folder,'persons','*.json')):
                    d=json.load(open(f,encoding='utf-8')); dirty=False
                    for arr in ('person_relationships','family_members'):
                        for i,x in enumerate(d.get(arr) or []):
                            if not isinstance(x,dict): continue
                            if x.get('person_id')!=oid: continue
                            nmv=nm(x)
                            if not nmv or not match(sig(nmv),(sig(sh)[0],[])): continue
                            undo['refs'].append({'cc':cc,'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':arr,'index':i,'old':oid,'new':target,'ref_name':nmv,'shadow':sh})
                            x['person_id']=target; dirty=True
                            stats['relink' if target else 'null']+=1
                    if apply and dirty: save(f,d)
            # archive registry
            rp=os.path.join(folder,'id_registry.json')
            reg=json.load(open(rp,encoding='utf-8'))
            pre=reg.get('person_registry') or []; dep=reg.setdefault('deprecated_person_registry',[])
            keep=[]; removed=0
            for e in pre:
                if e.get('person_id')==oid:
                    nm_e=(e.get('name') or '').strip()
                    et=set(nm_e.split()) if nm_e else set()
                    is_owner=bool(has_profile and owner and (et & owner_toks))
                    if is_owner: keep.append(e); continue
                    e2=dict(e); e2['status']='collision_split'
                    e2['deprecated_reason']='P3 registry collision cleanup: shadow identity split from collision ID'
                    dep.append(e2); undo['registry'].append({'cc':cc,'id':oid,'name':nm_e}); removed+=1
                else: keep.append(e)
            if removed:
                reg['person_registry']=keep
                if apply: save(rp,reg)
                stats['archived']+=removed
    summary={'apply':apply,**{k:stats[k] for k in ('relink','null','archived')}}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        json.dump({'summary':summary,'undo':undo},open(OUT+'/p3_person_collisions_generic_undo.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print('undo ->',OUT+'/p3_person_collisions_generic_undo.json')
    else:
        json.dump({'summary':summary,'undo':undo},open(OUT+'/p3_person_collisions_generic_dry.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print('DRY')
if __name__=='__main__': main()

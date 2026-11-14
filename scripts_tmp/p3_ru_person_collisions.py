# -*- coding: utf-8 -*-
"""P3: RU person registry collision cleanup.

Classes:
  A) collision ID has an owner profile + registry shadow names:
     - redirect refs whose ref_name matches a shadow name to the shadow's own
       profile if one exists (matched by name across ru persons); else null
     - archive the shadow registry entry (status=merged/removed -> deprecated)
  B) collision ID has NO profile and only multiple registry names:
     - refs: null by name-match per shadow (no profiles exist)
     - archive ALL registry entries for this ID into deprecated as
       collision_split; keep id_registry active list clean (remove entries)
Never touches owner profiles' own names/refs.
"""
import glob,json,os,sys,time
from collections import Counter,defaultdict
sys.path.insert(0,os.path.dirname(__file__))
from id_integrity_audit2 import BASE,OUT,load_datasets,match,sig
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
    ru=cr['collisions']['person'].get('ru') or {}
    folder=BASE+'/output/ru/2026-05-26'
    # name -> pid (own profile)
    name2pid=defaultdict(set)
    profiles={}
    for f in glob.glob(folder+'/persons/*.json'):
        d=json.load(open(f,encoding='utf-8')); pid=d.get('person_id')
        profiles[pid]=d
        vals=[d.get('name'),d.get('name_zh'),d.get('name_en')]+list(d.get('aliases') or [])
        for v in vals:
            if isinstance(v,str) and v.strip(): name2pid[v.strip()].add(pid)
    reg=json.load(open(folder+'/id_registry.json',encoding='utf-8'))
    pre=reg.get('person_registry') or []
    dep=reg.setdefault('deprecated_person_registry',[])
    undo={'registry':[],'refs':[]}; stats=Counter()
    # classify collisions
    for oid,info in ru.items():
        shadows=info.get('shadow_names') or []
        owner=info.get('profile_name')
        has_profile=oid in profiles
        # for each shadow, find target profile by exact/alias name
        for sh in shadows:
            cands=name2pid.get(sh) or set()
            cands={p for p in cands if p!=oid}
            target=None
            if len(cands)==1: target=next(iter(cands))
            # redirect refs matching this shadow
            for f in glob.glob(folder+'/persons/*.json'):
                d=json.load(open(f,encoding='utf-8'))
                dirty=False
                for arr in ('person_relationships','family_members'):
                    for i,x in enumerate(d.get(arr) or []):
                        if not isinstance(x,dict): continue
                        if x.get('person_id')!=oid: continue
                        nmv=nm(x)
                        if not nmv or not match(sig(nmv),(sig(sh)[0],[])): continue
                        if target:
                            undo['refs'].append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':arr,'index':i,'old':oid,'new':target,'ref_name':nmv,'shadow':sh})
                            x['person_id']=target; dirty=True; stats['relink']+=1
                        else:
                            undo['refs'].append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':arr,'index':i,'old':oid,'new':None,'ref_name':nmv,'shadow':sh})
                            x['person_id']=None; dirty=True; stats['null']+=1
                if apply and dirty: save(f,d)
        # archive registry entries for this oid EXCEPT the owner entry
        keep=[]; removed=0
        for e in pre:
            if e.get('person_id')==oid:
                nm_e=(e.get('name') or '').strip()
                owner_toks=set((owner or '').split())
                entry_toks=set(nm_e.split()) if nm_e else set()
                is_owner = bool(has_profile and owner and (entry_toks & owner_toks))
                if has_profile and is_owner:
                    keep.append(e); continue
                e2=dict(e); e2['status']='collision_split'
                e2['deprecated_reason']='P3 registry collision cleanup: shadow identity split from collision ID'
                dep.append(e2)
                undo['registry'].append({'id':oid,'name':nm_e,'was_owner':bool(is_owner)})
                removed+=1
            else:
                keep.append(e)
        if removed:
            pre=keep; stats['archived']+=removed
    reg['person_registry']=pre
    reg['deprecated_person_registry']=dep
    summary={'apply':apply,'relink':stats['relink'],'null':stats['null'],'archived':stats['archived']}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        save(folder+'/id_registry.json',reg)
        json.dump({'summary':summary,'undo':undo},open(OUT+'/p3_ru_person_collisions_undo.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print('undo ->',OUT+'/p3_ru_person_collisions_undo.json')
    else:
        json.dump({'summary':summary,'undo':undo},open(OUT+'/p3_ru_person_collisions_dry.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print('DRY')
if __name__=='__main__': main()

# -*- coding: utf-8 -*-
"""P3: org registry collision cleanup (all remaining countries).

For each collision org ID: archive non-owner registry entries (shadow
identities). Refs to shadows were already nulled in P2 (auto pass). Owner
entry detection: token overlap with owner profile name OR oid has profile.
"""
import glob,json,os,sys,time
from collections import Counter
sys.path.insert(0,os.path.dirname(__file__))
from id_integrity_audit2 import BASE,OUT,load_datasets
CC_EX={'gn','ng'}
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def main():
    apply='--apply' in sys.argv
    cr=json.load(open(BASE+'/output/_id_audit/collision_report.json',encoding='utf-8'))
    latest,_=load_datasets()
    undo=[]; stats=Counter()
    for cc,col in (cr['collisions']['org'] or {}).items():
        if cc in CC_EX or not col: continue
        folder=latest[cc][1]
        profiles=set()
        for f in glob.glob(os.path.join(folder,'orgs','*.json')):
            if os.path.basename(f).startswith('_'): continue
            d=json.load(open(f,encoding='utf-8')); oid=d.get('org_id')
            if oid: profiles.add(oid)
        rp=os.path.join(folder,'id_registry.json')
        reg=json.load(open(rp,encoding='utf-8'))
        pre=reg.get('registry') or []; dep=reg.setdefault('deprecated_registry',[])
        keep=[]; removed=0
        for e in pre:
            oid=e.get('org_id')
            if oid not in col: keep.append(e); continue
            nm_e=(e.get('name') or '').strip()
            owner=(col[oid] or {}).get('profile_name')
            et=set(nm_e.split()) if nm_e else set()
            ot=set((owner or '').split())
            is_owner=bool(oid in profiles and owner and (et & ot))
            if is_owner: keep.append(e); continue
            e2=dict(e); e2['status']='collision_split'
            e2['deprecated_reason']='P3 registry collision cleanup: shadow identity split from collision ID'
            dep.append(e2); undo.append({'cc':cc,'id':oid,'name':nm_e,'owner':owner}); removed+=1
        if removed:
            reg['registry']=keep
            if apply: save(rp,reg)
            stats['archived']+=removed
    summary={'apply':apply,'archived':stats['archived']}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        json.dump({'summary':summary,'undo':undo},open(OUT+'/p3_org_collisions_undo.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print('undo ->',OUT+'/p3_org_collisions_undo.json')
    else: print('DRY')
if __name__=='__main__': main()

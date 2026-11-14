# -*- coding: utf-8 -*-
"""P2 batch 15: null wrong key_people in KZ/MY/TH/JP/RU (GN/NG excluded)."""
import glob,json,os,sys,time
from collections import Counter
sys.path.insert(0,os.path.dirname(__file__))
from id_integrity_audit2 import BASE,OUT,load_datasets,match,sig
EX={'gn','ng'}; TARGET_CC={'kz','my','th','jp','ru'}
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def main():
    apply='--apply' in sys.argv
    latest,_=load_datasets(); per={}
    for cc,(date,folder) in latest.items():
        if cc in EX: continue
        for f in glob.glob(os.path.join(folder,'persons','*.json')):
            if os.path.basename(f).startswith('_'): continue
            d=json.load(open(f,encoding='utf-8')); pid=d.get('person_id'); bi=d.get('basic_info') or {}
            if not pid: continue
            vals=[d.get('name'),d.get('name_en'),d.get('name_zh'),d.get('name_original'),bi.get('name_zh'),bi.get('name_en'),bi.get('name_original')]+list(d.get('aliases') or []); c=set();t=[]
            for v in vals:
                if isinstance(v,str) and v.strip(): a,b=sig(v);c|=a;t+=b
            per[pid]=(c,t,d.get('name_zh') or d.get('name_en') or pid)
    changes=[]; stats=Counter()
    for cc,(date,folder) in latest.items():
        if cc not in TARGET_CC: continue
        for f in glob.glob(os.path.join(folder,'orgs','*.json')):
            if os.path.basename(f).startswith('_'): continue
            d=json.load(open(f,encoding='utf-8')); dirty=False
            for i,x in enumerate(d.get('key_people') or []):
                if not isinstance(x,dict): continue
                v=x.get('person_id'); ref=x.get('name') or x.get('name_en') or x.get('person_name') or ''
                if not isinstance(v,str) or not ref or v not in per: continue
                c,t,cur=per[v]
                if match(sig(ref),(c,t)): continue
                changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':'key_people','index':i,'field':'person_id','old':v,'new':None,'ref_name':ref,'current_profile':cur,'cc':cc})
                x['person_id']=None; dirty=True; stats[cc]+=1
            if apply and dirty: save(f,d)
    summary={'apply':apply,'refs_nulled':sum(stats.values()),'by_cc':dict(stats)}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        p=os.path.join(OUT,'p2_batch15_keypeople_undo.json'); json.dump({'summary':summary,'changes':changes},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('undo ->',p)
    else: print('DRY')
if __name__=='__main__': main()

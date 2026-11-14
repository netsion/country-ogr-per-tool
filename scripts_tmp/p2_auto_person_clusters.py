# -*- coding: utf-8 -*-
"""Rolling person_relationships cluster cleanup (GN/NG excluded).

Auto-criteria per cluster (current person profile vs ref name):
  - keep if names match (audit matcher) or first-token translit overlap only
  - null otherwise, but keep rows where ref shares surname AND no better rule?
No: these clusters are all same-surname different-person; batch auto-nulls
every ref whose name does not strictly match, EXCEPT refs sharing the full
given-name token with different surname are still wrong -> null.
"""
import glob,json,os,sys,time,re
from collections import Counter
sys.path.insert(0,os.path.dirname(__file__))
from id_integrity_audit2 import BASE,OUT,load_datasets,match,sig
EX={'gn','ng'}
MIN_KEEP=1
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
        if cc in EX: continue
        for f in glob.glob(os.path.join(folder,'persons','*.json')):
            if os.path.basename(f).startswith('_'): continue
            d=json.load(open(f,encoding='utf-8')); dirty=False
            for i,x in enumerate(d.get('person_relationships') or []):
                if not isinstance(x,dict): continue
                v=x.get('person_id'); ref=x.get('person_name') or x.get('name') or ''
                if not isinstance(v,str) or not ref or v not in per: continue
                c,t,cur=per[v]
                if match(sig(ref),(c,t)): continue
                changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':'person_relationships','index':i,'field':'person_id','old':v,'new':None,'ref_name':ref})
                x['person_id']=None; dirty=True; stats['null']+=1
            if apply and dirty: save(f,d)
    summary={'apply':apply,'null':stats['null']}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    tag='apply' if apply else 'dry'
    json.dump({'summary':summary,'changes':changes},open(os.path.join(OUT,f'p2_auto_person_{tag}.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('->',os.path.join(OUT,f'p2_auto_person_{tag}.json'))
if __name__=='__main__': main()

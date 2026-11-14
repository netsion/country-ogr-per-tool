# -*- coding: utf-8 -*-
"""Rolling related_entities cluster cleanup (GN/NG excluded).

Null every related_entities org_id whose ref name does not match the current
org profile by the audit matcher. Keeps valid aliases/renames automatically.
"""
import glob,json,os,sys,time
from collections import Counter
sys.path.insert(0,os.path.dirname(__file__))
from id_integrity_audit2 import BASE,OUT,load_datasets,match,sig
EX={'gn','ng'}
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def nm(x):
    for k in ('org_name','name','organization'):
        v=x.get(k)
        if isinstance(v,str) and v.strip(): return v.strip()
    return ''
def main():
    apply='--apply' in sys.argv
    latest,_=load_datasets(); org={}
    for cc,(date,folder) in latest.items():
        if cc in EX: continue
        for f in glob.glob(os.path.join(folder,'orgs','*.json')):
            if os.path.basename(f).startswith('_'): continue
            d=json.load(open(f,encoding='utf-8')); oid=d.get('org_id'); bi=d.get('basic_info') or {}
            if not oid: continue
            vals=[bi.get('name_zh'),bi.get('name_en'),bi.get('name_original')]+list(bi.get('aliases') or []); c=set();t=[]
            for v in vals:
                if isinstance(v,str) and v.strip(): a,b=sig(v);c|=a;t+=b
            org[oid]=(c,t,d.get('basic_info') or {})
    changes=[]; stats=Counter()
    for cc,(date,folder) in latest.items():
        if cc in EX: continue
        for f in glob.glob(os.path.join(folder,'orgs','*.json')):
            if os.path.basename(f).startswith('_'): continue
            d=json.load(open(f,encoding='utf-8')); dirty=False
            for i,x in enumerate(d.get('related_entities') or []):
                if not isinstance(x,dict): continue
                v=x.get('org_id'); ref=nm(x)
                if not isinstance(v,str) or not ref or v not in org: continue
                c,t,curbi=org[v]
                if match(sig(ref),(c,t)): continue
                changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':'related_entities','index':i,'field':'org_id','old':v,'new':None,'ref_name':ref})
                x['org_id']=None; dirty=True; stats['null']+=1
            if apply and dirty: save(f,d)
    summary={'apply':apply,'null':stats['null']}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    tag='apply' if apply else 'dry'
    json.dump({'summary':summary,'changes':changes},open(os.path.join(OUT,f'p2_auto_related_{tag}.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('->',os.path.join(OUT,f'p2_auto_related_{tag}.json'))
if __name__=='__main__': main()

# -*- coding: utf-8 -*-
"""Generate next wrong-reference review sample, excluding GN/NG and prior reviewed positions."""
import csv,glob,json,os,sys
from collections import Counter
sys.path.insert(0,'scripts_tmp')
from id_integrity_audit2 import load_datasets,match,sig
BASE='D:/ai-workspace/apec-osint-tool'; OUT=os.path.join(BASE,'output/_id_audit')
EXCLUDE_CC={'gn','ng'}
latest,_=load_datasets()
org={}; per={}
for cc,(date,folder) in latest.items():
    if cc in EXCLUDE_CC: continue
    for f in glob.glob(os.path.join(folder,'orgs','*.json')):
        if os.path.basename(f).startswith('_'): continue
        d=json.load(open(f,encoding='utf-8')); oid=d.get('org_id'); bi=d.get('basic_info') or {}
        if oid:
            vals=[bi.get('name_zh'),bi.get('name_en'),bi.get('name_original')]+list(bi.get('aliases') or [])
            c=set(); t=[]
            for v in vals:
                if isinstance(v,str) and v.strip(): a,b=sig(v); c|=a; t+=b
            org[oid]=(c,t,bi.get('name_zh') or bi.get('name_en') or oid)
    for f in glob.glob(os.path.join(folder,'persons','*.json')):
        if os.path.basename(f).startswith('_'): continue
        d=json.load(open(f,encoding='utf-8')); pid=d.get('person_id'); bi=d.get('basic_info') or {}
        if pid:
            vals=[d.get('name'),d.get('name_en'),d.get('name_zh'),d.get('name_original'),bi.get('name_zh'),bi.get('name_en'),bi.get('name_original')]+list(d.get('aliases') or [])
            c=set(); t=[]
            for v in vals:
                if isinstance(v,str) and v.strip(): a,b=sig(v); c|=a; t+=b
            per[pid]=(c,t,d.get('name_zh') or d.get('name_en') or pid)
def nm(x,cat):
    keys={'work_org':('organization','org_name','organization_en'),'related_org':('org_name','name','organization'),'person_rel':('person_name','name'),'family':('name','person_name'),'key_people':('name','name_en','person_name')}[cat]
    for k in keys:
        v=x.get(k)
        if isinstance(v,str) and v.strip(): return v.strip()
    return ''
excluded=set()
p=os.path.join(OUT,'p2_wrong_review_200_decisions.csv')
if os.path.exists(p):
    for r in csv.DictReader(open(p,encoding='utf-8-sig')):
        excluded.add((r['file'],r['array'],r['index']))
rows=[]
for cc,(date,folder) in latest.items():
    if cc in EXCLUDE_CC: continue
    for sub,arrs in [('persons',[('work_experience','org_id','org','work_org'),('person_relationships','person_id','person','person_rel'),('family_members','person_id','person','family')]),('orgs',[('key_people','person_id','person','key_people'),('related_entities','org_id','org','related_org')])]:
        for f in glob.glob(os.path.join(folder,sub,'*.json')):
            if os.path.basename(f).startswith('_'): continue
            d=json.load(open(f,encoding='utf-8')); rel=os.path.relpath(f,BASE).replace(os.sep,'/')
            for arr,field,kind,cat in arrs:
                mp=org if kind=='org' else per
                for i,x in enumerate(d.get(arr) or []):
                    if not isinstance(x,dict): continue
                    if (rel,arr,str(i)) in excluded: continue
                    v=x.get(field); ref=nm(x,cat)
                    if not isinstance(v,str) or not ref or v not in mp: continue
                    c,t,cur=mp[v]
                    if match(sig(ref),(c,t)): continue
                    rows.append({'cat':cat,'cc':cc,'file':rel,'array':arr,'index':i,'ref_name':ref,'current_id':v,'current_profile':cur})
sample=[]
for cat in ('work_org','related_org','person_rel','key_people','family'):
    sample += [r for r in rows if r['cat']==cat][:40]
sample=sample[:200]
out=os.path.join(OUT,'p2_wrong_review_b.csv')
with open(out,'w',encoding='utf-8-sig',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(sample)
print('candidates',len(rows),Counter(r['cat'] for r in rows)); print('sample',len(sample),out)

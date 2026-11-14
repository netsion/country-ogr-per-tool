# -*- coding: utf-8 -*-
"""Scan current wrong refs by current ID, excluding GN/NG."""
import glob,json,os,sys
from collections import Counter,defaultdict
sys.path.insert(0,'scripts_tmp')
from id_integrity_audit2 import load_datasets,match,sig
BASE='D:/ai-workspace/apec-osint-tool'; OUT=os.path.join(BASE,'output/_id_audit'); EX={'gn','ng'}
latest,_=load_datasets()
org={}; per={}
for cc,(date,folder) in latest.items():
    if cc in EX: continue
    for f in glob.glob(os.path.join(folder,'orgs','*.json')):
        if os.path.basename(f).startswith('_'): continue
        d=json.load(open(f,encoding='utf-8')); oid=d.get('org_id'); bi=d.get('basic_info') or {}
        if oid:
            vals=[bi.get('name_zh'),bi.get('name_en'),bi.get('name_original')]+list(bi.get('aliases') or []); c=set();t=[]
            for v in vals:
                if isinstance(v,str) and v.strip(): a,b=sig(v);c|=a;t+=b
            org[oid]=(c,t,bi.get('name_zh') or bi.get('name_en') or oid)
    for f in glob.glob(os.path.join(folder,'persons','*.json')):
        if os.path.basename(f).startswith('_'): continue
        d=json.load(open(f,encoding='utf-8')); pid=d.get('person_id'); bi=d.get('basic_info') or {}
        if pid:
            vals=[d.get('name'),d.get('name_en'),d.get('name_zh'),d.get('name_original'),bi.get('name_zh'),bi.get('name_en'),bi.get('name_original')]+list(d.get('aliases') or []); c=set();t=[]
            for v in vals:
                if isinstance(v,str) and v.strip(): a,b=sig(v);c|=a;t+=b
            per[pid]=(c,t,d.get('name_zh') or d.get('name_en') or pid)
def nm(x,cat):
    keys={'work_org':('organization','org_name','organization_en'),'related_org':('org_name','name','organization'),'person_rel':('person_name','name'),'family':('name','person_name'),'key_people':('name','name_en','person_name')}[cat]
    for k in keys:
        v=x.get(k)
        if isinstance(v,str) and v.strip(): return v.strip()
    return ''
groups=defaultdict(list)
for cc,(date,folder) in latest.items():
    if cc in EX: continue
    for sub,arrs in [('persons',[('work_experience','org_id','work_org'),('person_relationships','person_id','person_rel'),('family_members','person_id','family')]),('orgs',[('key_people','person_id','key_people'),('related_entities','org_id','related_org')])]:
        for f in glob.glob(os.path.join(folder,sub,'*.json')):
            if os.path.basename(f).startswith('_'): continue
            d=json.load(open(f,encoding='utf-8')); rel=os.path.relpath(f,BASE).replace(os.sep,'/')
            for arr,field,cat in arrs:
                mp=org if cat in ('work_org','related_org') else per
                for i,x in enumerate(d.get(arr) or []):
                    if not isinstance(x,dict): continue
                    v=x.get(field); ref=nm(x,cat)
                    if not isinstance(v,str) or not ref or v not in mp: continue
                    c,t,cur=mp[v]
                    if match(sig(ref),(c,t)): continue
                    groups[v].append({'cat':cat,'file':rel,'array':arr,'index':i,'ref':ref,'cur':cur})
out=[]
for oid,rows in sorted(groups.items(),key=lambda kv:-len(kv[1])):
    out.append({'id':oid,'count':len(rows),'current':rows[0]['cur'],'cats':dict(Counter(r['cat'] for r in rows)),'top_names':Counter(r['ref'] for r in rows).most_common(10)})
json.dump(out,open(os.path.join(OUT,'p2_clusters_next.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('wrong',sum(x['count'] for x in out),'clusters',len(out))
for x in out[:30]: print(x['count'],x['id'],x['current'],x['cats'],x['top_names'][:4])

# -*- coding: utf-8 -*-
"""NG-2026-11-10 key_people linking:
1. match by exact name against existing person files (incl. aliases) -> set person_id
2. for unmatched: create skeleton person profiles (status listed) + registry entries,
   assign NG-PERSON next numbers; backfill person_id.
Names without any content beyond name => skeleton with name/name_zh/en parse from "zh (en)".
"""
import glob,json,os,re,sys,time
from collections import Counter,defaultdict
BASE='D:/ai-workspace/apec-osint-tool'
DIR=BASE+'/output/ng/2026-11-10'
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def parse_name(s):
    zh=en=None
    m=re.match(r'^(.*?)\s*[（(](.*)[）)]\s*$',s or '')
    if m: zh,en=m.group(1).strip(),m.group(2).strip()
    else:
        if re.search(r'[\u4e00-\u9fff]',s or ''): zh=s.strip()
        else: en=s.strip()
    return zh,en
def main():
    # name map from existing files
    name2pid=defaultdict(set)
    for f in glob.glob(DIR+'/persons/*.json'):
        if os.path.basename(f).startswith('_'): continue
        d=json.load(open(f,encoding='utf-8')); pid=d.get('person_id')
        vals=[d.get('name'),d.get('name_zh'),d.get('name_en')]+list(d.get('aliases') or [])
        for v in vals:
            if isinstance(v,str) and v.strip(): name2pid[v.strip()].add(pid)
    reg=json.load(open(DIR+'/id_registry.json',encoding='utf-8'))
    pre=reg.setdefault('person_registry',[])
    used=set()
    for e in pre:
        if e.get('person_id'): used.add(e['person_id'])
    mx=0
    for u in used:
        m=re.match(r'NG-PERSON-(\d+)',u)
        if m: mx=max(mx,int(m.group(1)))
    nextn=mx+1
    created=[]; linked=0
    for f in glob.glob(DIR+'/orgs/*.json'):
        if os.path.basename(f).startswith('_'): continue
        d=json.load(open(f,encoding='utf-8')); dirty=False
        for x in d.get('key_people') or []:
            if not isinstance(x,dict) or (x.get('person_id') or '').strip(): continue
            nm=(x.get('name') or x.get('name_en') or '').strip()
            if not nm: continue
            cands={p for p in name2pid.get(nm,set())}
            zh,en=parse_name(nm)
            if not cands and zh: cands={p for p in name2pid.get(zh,set())}
            if not cands and en: cands={p for p in name2pid.get(en,set())}
            if len(cands)==1:
                x['person_id']=next(iter(cands)); linked+=1; dirty=True
                continue
            if len(cands)>1:
                continue
            # create skeleton
            pid=f'NG-PERSON-{nextn:06d}'; nextn+=1
            prof={
              'person_id':pid,
              'name':en or zh or nm,
              'name_zh':zh or None,
              'name_en':en or nm,
              'name_original':None,
              'aliases':[],
              'gender':None,'birth_date':None,'birth_place':None,
              'nationality':'NG',
              'biography_summary':None,
              'current_positions':[x.get('title') or None],
              'work_experience':[{'organization':d.get('basic_info',{}).get('name_zh') or d.get('basic_info',{}).get('name_en'),'org_id':d.get('org_id'),'position':x.get('title') or None}],
              'education':[],'political_stances':[],'person_relationships':[],
              'major_achievements':[],'family_members':[],'social_accounts':[],'contacts':[],
              'profile':None,
              'collection_meta':{'collection_date':'2026-11-15','phase':'phase4_person_profile','data_sources':['org_key_people'],'completeness_score':35,'notes':'从组织 key_people 生成的骨架画像；待后续补全','quotes':[{'title':'来自组织 key_people','url':f'internal:{d.get("org_id")}'}]},
            }
            save(DIR+f'/persons/{pid}.json',prof)
            created.append(pid)
            name2pid[nm].add(pid)
            if zh: name2pid[zh].add(pid)
            x['person_id']=pid; dirty=True; linked+=1
        if dirty: save(f,d)
    # registry entries for created
    for pid in created:
        f=DIR+f'/persons/{pid}.json'
        d=json.load(open(f,encoding='utf-8'))
        pre.append({'person_id':pid,'name':d.get('name') or '','name_en':d.get('name_en'),'status':'listed','source':'org key_people skeleton'})
    reg['person_registry']=pre
    save(DIR+'/id_registry.json',reg)
    print(json.dumps({'linked_to_existing':linked-len(created),'created':len(created)},ensure_ascii=False))
    json.dump({'created':created},open(BASE+'/output/_id_audit/ng_keypeople_link_undo.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
if __name__=='__main__': main()

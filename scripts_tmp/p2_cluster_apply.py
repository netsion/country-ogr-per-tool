# -*- coding: utf-8 -*-
"""P2 cluster batch: for selected current IDs, keep matches, relink one known
case, null the rest. Excludes GN/NG."""
import glob, json, os, sys, time
from collections import Counter, defaultdict
sys.path.insert(0,os.path.dirname(__file__))
from id_integrity_audit2 import BASE, OUT, load_datasets
from p2_plan_strict import strict_match

EXCLUDE_CC={'gn','ng'}
# current_id -> (mode, target_id, keep_keywords)
CLUSTERS={
 'KR-GOV-016':('relink_kr','KR-GOV-015',['大法院','最高法院','高等法院','地方法院','法院行政处','法院','Supreme Court','High Court','District Court','법원']),
 'PH-CORP-015':('null',None,['国际集装箱码头服务','ICTSI','International Container Terminal']),
 'MX-ACAD-001':('null',None,['墨西哥国立自治大学','UNAM','Universidad Nacional Autónoma de México']),
 'CL-SOE-007':('null',None,['圣地亚哥地铁','Metro S.A.','Metro de Santiago']),
 'MX-ACAD-006':('null',None,['国家人文科学技术委员会','CONAHCYT','Consejo Nacional de Humanidades']),
 'PE-SOE-006':('null',None,['秘鲁矿业资产公司','Activos Mineros']),
 'JP-CORP-019':('null',None,['东京电力','東京電力','TEPCO','Tokyo Electric']),
 'UZ-SOE-005':('null',None,['乌兹别克斯坦铁路','Oʻzbekiston Temir Yoʻllari','Uzbekistan Railways']),
 'KR-GOV-001':('null',None,['国务会议','State Council']),
}
def names_of(p):
    bi=p.get('basic_info') or {}
    vals=[bi.get('name_zh'),bi.get('name_en'),bi.get('name_original')]+list(bi.get('aliases') or [])
    return [v.strip() for v in vals if isinstance(v,str) and v.strip()]
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def nm(x,cat):
    keys={'work_org':('organization','org_name','organization_en'),'related_org':('org_name','name','organization'),'person_rel':('person_name','name'),'family':('name','person_name'),'key_people':('name','name_en','person_name')}[cat]
    for k in keys:
        v=x.get(k)
        if isinstance(v,str) and v.strip(): return v.strip()
    return ''
def main():
    apply='--apply' in sys.argv
    latest,_=load_datasets()
    names={}
    for cc,(date,folder) in latest.items():
        if cc in EXCLUDE_CC: continue
        for sub in ('orgs','persons'):
            for f in glob.glob(os.path.join(folder,sub,'*.json')):
                if os.path.basename(f).startswith('_'): continue
                d=json.load(open(f,encoding='utf-8')); oid=d.get('org_id') or d.get('person_id')
                if oid: names[oid]=names_of(d)
    for oid in CLUSTERS:
        mode,t,kw=CLUSTERS[oid]
        if t and t not in names: print('WARN target missing',t)
    changes=[]; stats=Counter()
    for cc,(date,folder) in latest.items():
        if cc in EXCLUDE_CC: continue
        for sub,arrs in [('persons',[('work_experience','org_id','work_org'),('person_relationships','person_id','person_rel'),('family_members','person_id','family')]),('orgs',[('key_people','person_id','key_people'),('related_entities','org_id','related_org')])]:
            for f in glob.glob(os.path.join(folder,sub,'*.json')):
                if os.path.basename(f).startswith('_'): continue
                d=json.load(open(f,encoding='utf-8')); dirty=False
                for arr,field,cat in arrs:
                    for i,x in enumerate(d.get(arr) or []):
                        if not isinstance(x,dict): continue
                        v=x.get(field)
                        if v not in CLUSTERS: continue
                        ref=nm(x,cat); mode,target,keep_kw=CLUSTERS[v]
                        if not ref: continue
                        low=ref.lower()
                        if any(k.lower() in low for k in keep_kw):
                            stats['keep']+=1; continue
                        cur_match=strict_match(ref,names.get(v,[]))
                        if cur_match:
                            stats['keep']+=1; continue
                        if mode=='relink_kr' and target and strict_match(ref,names.get(target,[])):
                            changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':arr,'index':i,'field':field,'old':v,'new':target,'ref_name':ref,'cat':cat,'action':'relink'})
                            x[field]=target; dirty=True; stats['relink']+=1
                        else:
                            changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':arr,'index':i,'field':field,'old':v,'new':None,'ref_name':ref,'cat':cat,'action':'null'})
                            x[field]=None; dirty=True; stats['null']+=1
                if apply and dirty: save(f,d)
    summary={'apply':apply,'keep':stats['keep'],'relink':stats['relink'],'null':stats['null']}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        p=os.path.join(OUT,'p2_cluster_apply_undo.json'); json.dump({'summary':summary,'changes':changes},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('undo ->',p)
    else:
        p=os.path.join(OUT,'p2_cluster_apply_dry.json'); json.dump({'summary':summary,'changes':changes},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('dry ->',p); print('DRY')
if __name__=='__main__': main()

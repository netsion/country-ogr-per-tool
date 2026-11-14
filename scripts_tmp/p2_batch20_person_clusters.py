# -*- coding: utf-8 -*-
"""P2 batch 17: null wrong person_relationships in top person clusters."""
import glob,json,os,sys,time
from collections import Counter
sys.path.insert(0,os.path.dirname(__file__))
from id_integrity_audit2 import BASE,OUT,load_datasets
from p2_plan_strict import strict_match
EX={'gn','ng'}
IDS={
 'RU-PERSON-000115',
 'RU-PERSON-000107',
 'RU-PERSON-000364',
 'TH-PERSON-000101',
 'JO-PERSON-000055',
 'JO-PERSON-000152',
 'JO-PERSON-000142',
 'JO-PERSON-000148',
 'JO-PERSON-000081',
 'JO-PERSON-000023',
 'JO-PERSON-000049',
 'MX-PERSON-000004',
 'MX-PERSON-000285',
 'MX-PERSON-000008',
 'MX-PERSON-000167',
 'MX-PERSON-000122',
 'MX-PERSON-000050',
 'MX-PERSON-000005',
 'PG-PERSON-000319',
 'PH-PERSON-000042',
 'PH-PERSON-000118',
 'PH-PERSON-000068',
 'PH-PERSON-000682',
 'PH-PERSON-000134',
 'PH-PERSON-000129',
 'PH-PERSON-000064',
 'PH-PERSON-000104',
 'PH-PERSON-000045',
 'PH-PERSON-000369',
 'PH-PERSON-000296',
}
def names_of(p):
    bi=p.get('basic_info') or {}
    vals=[p.get('name'),p.get('name_en'),p.get('name_zh'),p.get('name_original'),bi.get('name_zh'),bi.get('name_en'),bi.get('name_original')]+list(p.get('aliases') or [])
    return [v.strip() for v in vals if isinstance(v,str) and v.strip()]
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def main():
    apply='--apply' in sys.argv
    latest,_=load_datasets(); names={}
    for cc,(date,folder) in latest.items():
        if cc in EX: continue
        for f in glob.glob(os.path.join(folder,'persons','*.json')):
            if os.path.basename(f).startswith('_'): continue
            d=json.load(open(f,encoding='utf-8')); pid=d.get('person_id')
            if pid: names[pid]=names_of(d)
    changes=[]; stats=Counter()
    for cc,(date,folder) in latest.items():
        if cc in EX: continue
        for f in glob.glob(os.path.join(folder,'persons','*.json')):
            if os.path.basename(f).startswith('_'): continue
            d=json.load(open(f,encoding='utf-8')); dirty=False
            for i,x in enumerate(d.get('person_relationships') or []):
                if not isinstance(x,dict): continue
                v=x.get('person_id'); ref=x.get('person_name') or x.get('name') or ''
                if v not in IDS or not ref: continue
                if strict_match(ref,names.get(v,[])): stats['keep']+=1; continue
                changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':'person_relationships','index':i,'field':'person_id','old':v,'new':None,'ref_name':ref})
                x['person_id']=None; dirty=True; stats['null']+=1
            if apply and dirty: save(f,d)
    summary={'apply':apply,'keep':stats['keep'],'null':stats['null']}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        p=os.path.join(OUT,'p2_batch20_person_clusters_undo.json'); json.dump({'summary':summary,'changes':changes},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('undo ->',p)
    else: print('DRY')
if __name__=='__main__': main()

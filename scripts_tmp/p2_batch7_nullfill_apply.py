# -*- coding: utf-8 -*-
"""P2 batch 7: fill null work_experience org IDs from existing-profile matches.

Only work_org rows from p2_nullfill_plan.csv are applied. person_rel/family
rows are deferred because Sr/Jr/generation variants need manual review.
"""
import csv, json, os, sys, time
from collections import Counter, defaultdict
BASE='D:/ai-workspace/apec-osint-tool'; OUT=os.path.join(BASE,'output/_id_audit')
PLAN=os.path.join(OUT,'p2_nullfill_plan.csv')
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def nm(x):
    for k in ('organization','org_name','organization_en'):
        v=x.get(k)
        if isinstance(v,str) and v.strip(): return v.strip()
    return ''
def main():
    apply='--apply' in sys.argv
    rows=[r for r in csv.DictReader(open(PLAN,encoding='utf-8-sig')) if r['cat']=='work_org']
    by=defaultdict(list)
    for r in rows: by[r['file']].append(r)
    undo=[]; stats=Counter()
    for rel,items in by.items():
        fp=os.path.join(BASE,rel); d=json.load(open(fp,encoding='utf-8')); dirty=False
        for r in items:
            arr=d.get(r['array']) or []; i=int(r['index'])
            if i>=len(arr) or not isinstance(arr[i],dict): stats['position_missing']+=1; continue
            x=arr[i]
            if x.get('org_id') not in (None,'') or nm(x)!=r['ref_name']:
                stats['position_changed']+=1; continue
            undo.append({'file':rel,'array':r['array'],'index':i,'field':'org_id','old':x.get('org_id'),'new':r['target_id'],'ref_name':r['ref_name'],'target_name':r['target_name']})
            x['org_id']=r['target_id']; dirty=True; stats['filled']+=1
        if apply and dirty: save(fp,d)
    summary={'apply':apply,'candidates':len(rows),'filled':stats['filled'],'position_missing':stats['position_missing'],'position_changed':stats['position_changed']}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        p=os.path.join(OUT,'p2_batch7_nullfill_undo.json'); json.dump({'summary':summary,'changes':undo},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('undo ->',p)
    else: print('DRY')
if __name__=='__main__': main()

# -*- coding: utf-8 -*-
"""P2 batch 11: reviewed sample B (GN/NG excluded)."""
import csv,json,os,sys,time
from collections import Counter,defaultdict
BASE='D:/ai-workspace/apec-osint-tool'; OUT=os.path.join(BASE,'output/_id_audit')
SRC=os.path.join(OUT,'p2_wrong_review_b.csv')
KEEP={4,5,46,47,48,49,53,55,56,63,70,73}
DEFER={7,10,11,30,35,36,75}
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
    rows=list(csv.DictReader(open(SRC,encoding='utf-8-sig')))
    decisions=[]
    for i,r in enumerate(rows):
        if i in KEEP: d,reason='keep','same entity/variant'
        elif i in DEFER: d,reason='defer','parent-subsidiary/ambiguous'
        else: d,reason='null','current profile unrelated'
        rr=dict(r); rr['decision']=d; rr['reason']=reason; decisions.append(rr)
    dp=os.path.join(OUT,'p2_wrong_review_b_decisions.csv')
    with open(dp,'w',encoding='utf-8-sig',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(decisions[0].keys())); w.writeheader(); w.writerows(decisions)
    by=defaultdict(list)
    for r in decisions:
        if r['decision']=='null': by[r['file']].append(r)
    undo=[]; stats=Counter()
    for rel,items in by.items():
        fp=os.path.join(BASE,rel); d=json.load(open(fp,encoding='utf-8')); dirty=False
        for r in items:
            arr=d.get(r['array']) or []; i=int(r['index'])
            if i>=len(arr) or not isinstance(arr[i],dict): stats['position_missing']+=1; continue
            x=arr[i]
            field={'work_org':'org_id','related_org':'org_id','person_rel':'person_id','family':'person_id','key_people':'person_id'}[r['cat']]
            if x.get(field)!=r['current_id'] or nm(x,r['cat'])!=r['ref_name']:
                stats['position_changed']+=1; continue
            undo.append({'file':rel,'array':r['array'],'index':i,'field':field,'old':x.get(field),'new':None,'ref_name':r['ref_name'],'cat':r['cat']})
            x[field]=None; dirty=True; stats[r['cat']]+=1
        if apply and dirty: save(fp,d)
    summary={'apply':apply,'rows':len(rows),'keep':len(KEEP),'defer':len(DEFER),'null_decisions':len(rows)-len(KEEP)-len(DEFER),'nulled':sum(stats.values()),'by_cat':dict(stats)}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        p=os.path.join(OUT,'p2_batch11_review_sample_b_undo.json'); json.dump({'summary':summary,'changes':undo},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('undo ->',p); print('decisions ->',dp)
    else: print('DRY')
if __name__=='__main__': main()

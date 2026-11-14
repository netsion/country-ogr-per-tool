# -*- coding: utf-8 -*-
"""P2 batch 5: null placeholder IDs and self links in person/family arrays."""
import glob, json, os, re, sys, time
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from id_integrity_audit2 import BASE, OUT, load_datasets

PLACE = re.compile(r'UNKNOWN|^unknown$|REL-|EXT-|000000|^N/?A$', re.I)

def save_json(path, obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=path+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,path); return
        except PermissionError: time.sleep(.5)
    open(path,'w',encoding='utf-8',newline='\n').write(payload)

def main():
    apply='--apply' in sys.argv
    latest,_=load_datasets(); changes=[]; stats=Counter()
    for cc,(date,folder) in sorted(latest.items()):
        for sub,arrs in (
            ('persons',[('work_experience','org_id','placeholder'),('person_relationships','person_id','both'),('family_members','person_id','both')]),
            ('orgs',[('key_people','person_id','placeholder'),('related_entities','org_id','placeholder')]),
        ):
            for f in glob.glob(os.path.join(folder,sub,'*.json')):
                if os.path.basename(f).startswith('_'): continue
                d=json.load(open(f,encoding='utf-8')); src=d.get('org_id') or d.get('person_id'); dirty=False
                for arr,field,mode in arrs:
                    for i,x in enumerate(d.get(arr) or []):
                        if not isinstance(x,dict): continue
                        v=x.get(field)
                        if not isinstance(v,str): continue
                        reason=None
                        if PLACE.search(v): reason='placeholder'
                        elif mode=='both' and v==src: reason='self'
                        if not reason: continue
                        changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':arr,'index':i,'field':field,'old':v,'new':None,'reason':reason,
                                        'ref_name':x.get('organization') or x.get('org_name') or x.get('person_name') or x.get('name') or ''})
                        x[field]=None; dirty=True; stats[reason]+=1; stats[arr]+=1
                if apply and dirty: save_json(f,d)
    summary={'apply':apply,'refs_nulled':sum(stats[k] for k in ('placeholder','self')),
             'by_reason':{k:stats[k] for k in ('placeholder','self')},
             'by_array':{k:v for k,v in stats.items() if k not in ('placeholder','self')}}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        p=os.path.join(OUT,'p2_batch5_placeholder_undo.json')
        json.dump({'summary':summary,'changes':changes},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print('undo ->',p)
    else: print('DRY')
if __name__=='__main__': main()

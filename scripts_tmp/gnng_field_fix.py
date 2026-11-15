# -*- coding: utf-8 -*-
"""GN/NG strict-error mechanical fixes (round 1).

1. strip non-schema extra fields: work_experience org_id_note/source_note,
   person_relationships source_note (keep the info in a valid 'note'/'source'
   field only if the target allows; here we just drop to satisfy strict).
   -> org_id_note content is merged into nothing; org_id_note is usually
      explanation of why org_id is null. Move to 'note' if WORK allows 'note'
      (WORK_FIELDS has 'note'/'notes'); else drop.
2. NG-2026-07-29: remove person top-level importance_level/importance_reason
   (info preserved? -> importance_level moves to nothing; registry keeps it),
   org top-level description/brief -> merge description into core_business if
   empty? description is long text; move to 'core_business' if empty else drop.
3. NG-2026-07-29 key_people extra fields person_name/source/wikidata_qid:
   map person_name->name if name empty else drop; drop source/wikidata_qid.
4. basic_info.name_zh empty: leave (needs real translation, next round).
"""
import glob, json, os, sys, time
BASE='D:/ai-workspace/apec-osint-tool'
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def fix_file(f, cc, dirn):
    d=json.load(open(f,encoding='utf-8')); dirty=False; n=0
    kind='person' if d.get('person_id') else 'org'
    # 1. strip work/rel extra fields
    for arr, extras in (('work_experience',['org_id_note','source_note']), ('person_relationships',['source_note']), ('family_members',['source_note']), ('key_people',['source_note']), ('education',['source_note'])):
        for x in d.get(arr) or []:
            if not isinstance(x,dict): continue
            for e in extras:
                if e in x:
                    val=x.pop(e)
                    # keep text: work->note if absent; others drop
                    if e=='org_id_note' and arr=='work_experience' and not x.get('note'):
                        x['note']=val
                    n+=1; dirty=True
    # 2. person top-level extras (NG 0729)
    if kind=='person':
        for k in ('importance_level','importance_reason'):
            if k in d:
                d.pop(k); n+=1; dirty=True
    # 3. org top-level description/brief
    if kind=='org':
        desc=d.pop('description',None); brief=d.pop('brief',None)
        if desc is not None or brief is not None:
            n+=1; dirty=True
            if not d.get('core_business'):
                d['core_business']=desc or brief
    # 4. key_people person_name/source/wikidata_qid (NG 0729)
    for x in d.get('key_people') or []:
        if not isinstance(x,dict): continue
        if 'person_name' in x:
            pn=x.pop('person_name')
            if not x.get('name'): x['name']=pn
            n+=1; dirty=True
        for k in ('source','wikidata_qid'):
            if k in x: x.pop(k); n+=1; dirty=True
    if dirty and True:  # apply always for this mechanical fix
        save(f,d)
    return n,dirty
def main():
    total=0; files=0
    for cc,dirn in [('gn','2026-11-10'),('ng','2026-11-10'),('ng','2026-07-29')]:
        for sub in ('persons','orgs'):
            for f in glob.glob(f'{BASE}/output/{cc}/{dirn}/{sub}/*.json'):
                if os.path.basename(f).startswith('_'): continue
                n,dirty=fix_file(f,cc,dirn)
                if dirty: total+=n; files+=1
    print(json.dumps({'files':files,'fixes':total},ensure_ascii=False))
if __name__=='__main__': main()

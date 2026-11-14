# -*- coding: utf-8 -*-
"""P3: dedupe duplicate QIDs.

Same-name groups:
  - cross-country (and any pair): the QID stays only on the richer keep copy.
    The drop copy keeps its profile but its wikidata_qid is cleared to null
    (merging whole profiles across country datasets is a bigger operation and
    is NOT done here — cross-country profiles are legitimate mirrors).
  - same-country: same treatment; profile kept, dup QID cleared.
Different-name groups (31): NOT touched here (need per-group review).
Org mirror groups (UN/WTO/...): keep richest, clear the rest — these are
per-country mirror profiles of the same international org; clearing the dup
QID is safe and non-destructive.
"""
import glob,json,os,sys,time
from collections import Counter
BASE='D:/ai-workspace/apec-osint-tool'; OUT=BASE+'/output/_id_audit'
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def find(oid):
    for f in glob.glob(f'{BASE}/output/[a-z][a-z]/20*/persons/{oid}.json')+glob.glob(f'{BASE}/output/[a-z][a-z]/20*/orgs/{oid}.json'):
        return f
def clear_qid(path):
    d=json.load(open(path,encoding='utf-8'))
    old=None
    if d.get('wikidata_qid'): old=d['wikidata_qid']; d['wikidata_qid']=None
    bi=d.get('basic_info') or {}
    if bi.get('wikidata_qid'): old=bi['wikidata_qid']; bi['wikidata_qid']=None
    return d,old
def main():
    apply='--apply' in sys.argv
    plan=json.load(open(OUT+'/p3_qid_merge_plan.json',encoding='utf-8'))
    changes=[]; stats=Counter()
    for grp in plan:
        qid=grp['qid']; keep=grp['keep']
        for oid in grp['drop'].split('|'):
            f=find(oid)
            if not f: stats['missing']+=1; continue
            d=json.load(open(f,encoding='utf-8'))
            cur=d.get('wikidata_qid') or (d.get('basic_info') or {}).get('wikidata_qid')
            if cur!=qid:
                stats['qid_mismatch']+=1; continue
            before=d
            d2,old=clear_qid(f)
            changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'id':oid,'qid':qid,'keep':keep,'old':old})
            stats['cleared']+=1
            if apply: save(f,d2)
    summary={'apply':apply,'cleared':stats['cleared'],'missing':stats['missing'],'qid_mismatch':stats['qid_mismatch']}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        json.dump({'summary':summary,'changes':changes},open(OUT+'/p3_qid_merge_undo.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print('undo ->',OUT+'/p3_qid_merge_undo.json')
    else: print('DRY')
if __name__=='__main__': main()

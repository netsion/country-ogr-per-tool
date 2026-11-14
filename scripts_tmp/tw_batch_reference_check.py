"""Inspect the 25 researched TW profiles' actual ID targets without resolving IDs."""
import json,pathlib,re,unicodedata,sys
import zhconv
ROOT=pathlib.Path(__file__).resolve().parents[1];BASE=ROOT/'output/tw/2026-07-27'
sys.stdout.reconfigure(encoding='utf-8')
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def norm(t):
 t=unicodedata.normalize('NFKD',t)
 t=''.join(c for c in t if not unicodedata.combining(c))
 return re.sub(r'[^\w\u4e00-\u9fff]','',zhconv.convert(t,'zh-cn').casefold())
def variants(t):return {norm(t)}|{norm(s) for s in re.split('[()（）]',t) if s.strip()}
first=load(BASE/'_supplement_progress.json')['completed'];second=load(BASE/'_batch2_progress.json')['completed']
rows=[]
for pid in first+second:
 data=load(BASE/'persons'/(pid+'.json'))
 for arr,key,nkey,folder in [('work_experience','org_id','organization','orgs'),('person_relationships','person_id','person_name','persons'),('family_members','person_id','name','persons')]:
  for i,ref in enumerate(data.get(arr,[])):
   rid=ref.get(key)
   if not rid:continue
   candidates=sorted((ROOT/'output').glob(f'[a-z][a-z]/20*/{folder}/{rid}.json'))
   row={'source_id':pid,'field':f'{arr}[{i}].{key}','target_id':rid,'reference_name':ref.get(nkey),'target_files':[str(p.relative_to(ROOT)) for p in candidates]}
   if not candidates:row['status']='missing_target'
   else:
    target=load(candidates[-1]);bi=target.get('basic_info',{}) if folder=='orgs' else target
    names=[bi[k] for k in ['name','name_original','name_zh','name_en'] if bi.get(k)]
    row['target_names']=names
    nv={v for name in names for v in variants(name)}
    row['status']='primary_name_match' if variants(ref.get(nkey) or '')&nv else 'needs_name_review'
    if rid==pid:row['status']='self_reference'
    if target.get('org_id' if folder=='orgs' else 'person_id')!=rid:row['status']='target_identity_mismatch'
   rows.append(row)
report={'reviewed_people':len(first+second),'references':rows}
(ROOT/'tmp/tw_batch_reference_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
from collections import Counter
print('People',len(first+second),'references',len(rows),'statuses',dict(Counter(x['status'] for x in rows)))
for row in rows:
 if row['status']!='primary_name_match':print(json.dumps(row,ensure_ascii=False))

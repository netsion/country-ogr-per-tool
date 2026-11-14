"""Read-only current evidence for second 80-ID review; include both reference kinds."""
import csv,hashlib,json,pathlib,re,sys
from collections import defaultdict
from id_integrity_audit2 import sig,match
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'output/_id_audit'
sys.stdout.reconfigure(encoding='utf-8');manifest={}
def read(p):
 raw=p.read_bytes();manifest[p.relative_to(ROOT).as_posix()]=hashlib.sha256(raw).hexdigest()
 return json.loads(raw.decode('utf-8-sig'))
def csvread(p):
 manifest[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 return list(csv.DictReader(p.open(encoding='utf-8-sig')))
rows=csvread(OUT/'registry_newid_sample_80_next.csv');plans=csvread(OUT/'registry_newid_plan_v3.csv')
latest=[]
for cc in (ROOT/'output').iterdir():
 if cc.is_dir() and re.fullmatch('[a-z]{2}',cc.name):
  ds=[d for d in cc.iterdir() if d.is_dir() and re.fullmatch(r'20\d\d-\d\d-\d\d',d.name)]
  if ds:latest.append(max(ds,key=lambda d:d.name))
profiles={};regs=defaultdict(list);refs=defaultdict(list);regnames=[]
for base in latest:
 rp=base/'id_registry.json'
 if rp.exists():
  data=read(rp)
  for arr,idfield in [('registry','org_id'),('deprecated_registry','org_id'),('person_registry','person_id'),('deprecated_person_registry','person_id')]:
   for e in data.get(arr) or []:
    if e.get(idfield):regs[e[idfield]].append({'file':rp.relative_to(ROOT).as_posix(),'array':arr,'entry':e})
    nm=e.get('name')
    if nm:regnames.append((sig(nm),{'file':rp.relative_to(ROOT).as_posix(),'array':arr,'entry':e}))
 for folder in ['orgs','persons']:
  for p in (base/folder).glob('*.json'):
   if p.name.startswith('_'):continue
   d=read(p);b=d.get('basic_info') or {};isorg=folder=='orgs';eid=d.get('org_id') if isorg else d.get('person_id')
   vals=([b.get(k) for k in ['name_original','name_zh','name_en']] if isorg else [d.get(k) for k in ['name','name_zh','name_en']])+(b.get('aliases') or [] if isorg else d.get('aliases') or [])
   s=set()
   for nm in vals:
    if isinstance(nm,str):s|=sig(nm)[0]
   if eid:profiles[eid]={'file':p.relative_to(ROOT).as_posix(),'kind':'org' if isorg else 'person','basic_info':b if isorg else {k:d.get(k) for k in ['name','name_zh','name_en','nationality']},'sig':s}
   owner=b.get('name_zh') or b.get('name_en') if isorg else d.get('name_zh') or d.get('name')
   for arr,field,kind in [('work_experience','org_id','org'),('related_entities','org_id','org'),('key_people','person_id','person'),('person_relationships','person_id','person'),('family_members','person_id','person')]:
    for j,e in enumerate(d.get(arr) or []):
     if not isinstance(e,dict) or not e.get(field):continue
     name=e.get('organization') or e.get('org_name') or e.get('person_name') or e.get('name') or ''
     refs[e[field]].append({'file':p.relative_to(ROOT).as_posix(),'pointer':f'{arr}[{j}].{field}','kind':kind,'owner':owner,'entry':e,'ref_name':name})
result=[]
for i,r in enumerate(rows,1):
 cid=r['冲突ID'];ss=sig(r['影子名称']);hits=[]
 for eid,p in profiles.items():
  if match(ss,(p['sig'],[])):hits.append({k:v for k,v in p.items() if k!='sig'}|{'id':eid})
 rr=[]
 for q in refs[cid]:rr.append(q|{'matches_shadow_heuristic':bool(q['ref_name'] and match(sig(q['ref_name']),ss))})
 registered=[q for rs,q in regnames if match(ss,rs)]
 plan=[q for q in plans if q['collision_id']==cid and q['shadow']==r['影子名称']]
 result.append({'review_row':i,'row':r,'plan':plan,'current_collision_profile':{k:v for k,v in profiles.get(cid,{}).items() if k!='sig'},'collision_registry':regs.get(cid,[]),'proposed_id_history':regs.get(r['建议新ID'],[]),'existing_profile_candidates':hits,'matching_registry_candidates':registered,'all_current_collision_references':rr})
 print(i,r['影子名称'],'CAND',[(h['id'],h['basic_info'].get('name_en') or h['basic_info'].get('name')) for h in hits], 'REF',[(q['kind'],q['ref_name']) for q in rr if q['matches_shadow_heuristic']][:4],flush=True)
(OUT/'registry_newid_next80_context.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'registry_newid_next80_read_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

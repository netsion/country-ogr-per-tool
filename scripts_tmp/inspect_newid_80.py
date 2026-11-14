"""Read-only evidence snapshot for the 80 shadow-ID samples."""
import csv,hashlib,json,pathlib,re,sys
from collections import defaultdict
from id_integrity_audit2 import sig,match
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'output/_id_audit'
sys.stdout.reconfigure(encoding='utf-8')
manifest={}
def read(p):
 raw=p.read_bytes();manifest[str(p.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest()
 return json.loads(raw.decode('utf-8-sig'))
sample=OUT/'registry_newid_sample_80.csv'
manifest[str(sample.relative_to(ROOT))]=hashlib.sha256(sample.read_bytes()).hexdigest()
rows=list(csv.DictReader(sample.open(encoding='utf-8-sig')))
plans=list(csv.DictReader((OUT/'registry_dedupe_plan_v2.csv').open(encoding='utf-8-sig')))
manifest['output/_id_audit/registry_dedupe_plan_v2.csv']=hashlib.sha256((OUT/'registry_dedupe_plan_v2.csv').read_bytes()).hexdigest()
latest=[]
for cc in (ROOT/'output').iterdir():
 if cc.is_dir() and re.fullmatch('[a-z]{2}',cc.name):
  ds=[d for d in cc.iterdir() if d.is_dir() and re.fullmatch(r'20\d\d-\d\d-\d\d',d.name)]
  if ds:latest.append(max(ds,key=lambda d:d.name))
profiles={};sources=[];registries=[]
for base in latest:
 rp=base/'id_registry.json'
 if rp.exists():registries.append((rp,read(rp)))
 for folder in ['orgs','persons']:
  for p in (base/folder).glob('*.json'):
   if p.name.startswith('_'):continue
   d=read(p);sources.append((p,d))
   if folder=='orgs':
    b=d.get('basic_info') or {};vals=[b.get(k) for k in ['name_zh','name_en','name_original']]+(b.get('aliases') or [])
    joined=set()
    for n in vals:
     if isinstance(n,str):joined|=sig(n)[0]
    profiles[d.get('org_id')]={'file':str(p.relative_to(ROOT)),'basic_info':b,'signature':joined}
result=[]
for i,r in enumerate(rows,1):
 cid=r['冲突ID'];ss=sig(r['影子名称']);hits=[]
 for oid,p in profiles.items():
  if oid and match(ss,(p['signature'],[])):
   hits.append({'id':oid,'file':p['file'],'basic_info':p['basic_info']})
 regs=[]
 for rp,d in registries:
  for e in d.get('registry') or []:
   if e.get('org_id') in [cid,r['建议新ID']] or (e.get('name') and match(ss,sig(e['name']))):
    regs.append({'file':str(rp.relative_to(ROOT)),'entry':e})
 refs=[]
 for p,d in sources:
  for arr,field in [('work_experience','org_id'),('related_entities','org_id')]:
   for j,e in enumerate(d.get(arr) or []):
    if not isinstance(e,dict) or e.get(field)!=cid:continue
    name=e.get('organization') or e.get('org_name') or e.get('name') or ''
    refs.append({'file':str(p.relative_to(ROOT)),'pointer':f'{arr}[{j}].{field}',
      'owner':d.get('name_zh') or d.get('name') or (d.get('basic_info') or {}).get('name_zh'),
      'entry':e,'matches_shadow_heuristic':bool(name and match(sig(name),ss))})
 plan=[p for p in plans if p['collision_id']==cid and p['shadow']==r['影子名称']]
 result.append({'review_row':i,'row':r,'plan':plan,'existing_profile_candidates':hits,'registry_candidates':regs,'all_current_collision_references':refs})
(OUT/'registry_newid_80_context.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'registry_newid_80_read_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
for x in result:
 print(x['review_row'],x['row']['影子名称'],'PLAN',[(p['action'],p['target']) for p in x['plan']],
  'CAND',[(p['id'],p['basic_info'].get('name_en')) for p in x['existing_profile_candidates']],
  'REF',sum(r['matches_shadow_heuristic'] for r in x['all_current_collision_references']))

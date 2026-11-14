"""Read-only indexed evidence collection for all 826 proposed identities."""
import csv,hashlib,json,pathlib,re,sys,unicodedata
from collections import defaultdict
from id_integrity_audit2 import sig,match
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'output/_id_audit'
sys.stdout.reconfigure(encoding='utf-8');manifest={}
def read(p):
 raw=p.read_bytes();manifest[p.relative_to(ROOT).as_posix()]=hashlib.sha256(raw).hexdigest()
 return json.loads(raw.decode('utf-8-sig'))
def fragments(name):
 return [s.strip() for s in re.split(r'[()（）/|]',name or '') if len(s.strip())>=3]
def norm(s):
 return ''.join(c.lower() for c in unicodedata.normalize('NFKD',s or '') if c.isalnum() and not unicodedata.combining(c))
source=OUT/'registry_newid_pending826_review.csv';raw=source.read_bytes();manifest[source.relative_to(ROOT).as_posix()]=hashlib.sha256(raw).hexdigest()
rows=list(csv.DictReader(source.open(encoding='utf-8-sig')));assert len(rows)==826
xp=OUT/'registry_newid_pending826_review.xlsx';manifest[xp.relative_to(ROOT).as_posix()]=hashlib.sha256(xp.read_bytes()).hexdigest()
profiles={};pidx=defaultdict(set);regs={};ridx=defaultdict(set);refs=defaultdict(list);used=defaultdict(list);latest=[]
for cc in (ROOT/'output').iterdir():
 if cc.is_dir() and re.fullmatch('[a-z]{2}',cc.name):
  ds=[d for d in cc.iterdir() if d.is_dir() and re.fullmatch(r'20\d\d-\d\d-\d\d',d.name)]
  if ds:latest.append(max(ds,key=lambda d:d.name))
for base in latest:
 rp=base/'id_registry.json'
 if rp.exists():
  data=read(rp)
  for arr,idkey in [('registry','org_id'),('person_registry','person_id'),('deprecated_registry','org_id'),('deprecated_person_registry','person_id')]:
   for j,e in enumerate(data.get(arr) or []):
    key=f'{rp.relative_to(ROOT).as_posix()}#{arr}[{j}]';rs=sig(e.get('name') or '');regs[key]={'file':rp.relative_to(ROOT).as_posix(),'array':arr,'entry':e,'sig':rs[0]}
    for token in rs[0]:ridx[token].add(key)
    for token in fragments(e.get('name') or ''):ridx['E:'+norm(token)].add(key)
    if e.get(idkey):used[e[idkey]].append(key)
 for folder in ['orgs','persons']:
  for p in (base/folder).glob('*.json'):
   if p.name.startswith('_'):continue
   d=read(p);b=d.get('basic_info') or {};isorg=folder=='orgs';eid=d.get('org_id') if isorg else d.get('person_id')
   values=([b.get(k) for k in ['name_original','name_zh','name_en']] if isorg else [d.get(k) for k in ['name','name_zh','name_en']])+(b.get('aliases') or [] if isorg else d.get('aliases') or [])
   tokens=set();exact=set()
   for n in values:
    if isinstance(n,str):tokens|=sig(n)[0];exact.add(norm(n));exact.update(norm(x) for x in fragments(n))
   if eid:
    profiles[eid]={'file':p.relative_to(ROOT).as_posix(),'kind':'org' if isorg else 'person','basic_info':b if isorg else {k:d.get(k) for k in ['name','name_zh','name_en','nationality','wikidata_qid']},'sig':tokens,'exact':exact}
    for t in tokens:pidx[t].add(eid)
    for t in exact:pidx['E:'+t].add(eid)
    used[eid].append(p.relative_to(ROOT).as_posix())
   for arr,field,kind in [('work_experience','org_id','org'),('related_entities','org_id','org'),('key_people','person_id','person'),('person_relationships','person_id','person'),('family_members','person_id','person')]:
    for j,e in enumerate(d.get(arr) or []):
     if not isinstance(e,dict) or not e.get(field):continue
     name=e.get('organization') or e.get('org_name') or e.get('person_name') or e.get('name') or ''
     q={'file':p.relative_to(ROOT).as_posix(),'pointer':f'{arr}[{j}].{field}','kind':kind,'entry':e,'ref_name':name}
     refs[e[field]].append(q);used[e[field]].append(q['file']+'#'+q['pointer'])
   for eid2 in d.get('org_ids') or []:
    if isinstance(eid2,str):used[eid2].append(p.relative_to(ROOT).as_posix()+'#org_ids')
print('indexed',len(profiles),len(regs),flush=True)
result=[]
for i,r in enumerate(rows,1):
 cid=r['冲突ID'];ss=sig(r['影子名称']);ex={norm(r['影子名称'])}|{norm(t) for t in fragments(r['影子名称'])};pcs=set();rcs=set()
 for t in ss[0]:pcs|=pidx[t];rcs|=ridx[t]
 for t in ex:pcs|=pidx['E:'+t];rcs|=ridx['E:'+t]
 hits=[]
 for eid in sorted(pcs):
  p=profiles[eid];exact=bool(ex & p['exact'])
  if exact or match(ss,(p['sig'],[])):hits.append({k:v for k,v in p.items() if k not in ['sig','exact']}|{'id':eid,'exact_fragment_match':exact})
 reghits=[]
 for key in sorted(rcs):
  v=regs[key]
  if match(ss,(v['sig'],[])):reghits.append({k:x for k,x in v.items() if k!='sig'})
 rr=[q|{'matches_shadow_heuristic':bool(q['ref_name'] and match(sig(q['ref_name']),ss))} for q in refs[cid]]
 result.append({'review_row':i,'row':r,'collision_profile':{k:v for k,v in profiles.get(cid,{}).items() if k not in ['sig','exact']},'collision_registry':[{k:v for k,v in regs[key].items() if k!='sig'} for key in used[cid] if key in regs],
 'existing_profile_candidates':hits,'matching_registry_candidates':reghits,'all_current_collision_references':rr,'candidate_id_used':used.get(r['候选新ID'],[])})
 if i%100==0:print('row',i,flush=True)
(OUT/'registry_pending826_context.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'registry_pending826_read_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('DONE',len(result),'occupied candidates',sum(bool(x['candidate_id_used']) for x in result),flush=True)

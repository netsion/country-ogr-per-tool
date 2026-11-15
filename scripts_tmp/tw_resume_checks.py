"""Scoped baseline and final checks for seven resumed Taiwan profiles."""
import pathlib,json,sys,hashlib,collections
import jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27'
O=R/'tmp/tw_resume_20261114';O.mkdir(exist_ok=True)
ids=['TW-PERSON-'+i for i in ['000184','000148','000533','000041','000141','000039','000163']]
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def snapshot():
 return {p.relative_to(R).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'profile':load(p).get('profile'),'id':load(p).get('person_id') or load(p).get('org_id')} for folder in ['persons','orgs'] for p in (B/folder).glob('TW-*.json')}
if sys.argv[1]=='baseline':
 assert not (O/'baseline.json').exists(),'Do not replace baseline'
 (O/'baseline.json').write_text(json.dumps(snapshot(),ensure_ascii=False,indent=2),encoding='utf-8')
 print('Baseline saved',len(snapshot()))
else:
 old=load(O/'baseline.json');new=snapshot();assert old.keys()==new.keys(),'Unexpected new/deleted profiles'
 changes=[p for p in old if old[p]['sha256']!=new[p]['sha256']]
 assert all(pathlib.Path(p).stem in ids for p in changes),changes
 assert all(old[p]['profile']==new[p]['profile'] and old[p]['id']==new[p]['id'] for p in old),'ID/avatar changed'
 schema=load(R/'.agents/skills/country-org-collector/person_profile_schema.json');v=jsonschema.Draft7Validator(schema)
 errors=[];links=[];summary=[]
 for pid in ids:
  x=load(B/'persons'/f'{pid}.json');errors += [f'{pid}: {e.message}' for e in v.iter_errors(x)]
  for key,field,folder in [('work_experience','org_id','orgs'),('person_relationships','person_id','persons'),('family_members','person_id','persons')]:
   for row in x.get(key,[]):
    rid=row.get(field);assert rid!=''
    if rid:
     files=list((R/'output').glob(f'[a-z][a-z]/20*/{folder}/{rid}.json'));assert files,(pid,key,rid)
     target=load(files[-1]);links.append({'source':pid,'field':key,'reference':row,'target_name':target.get('name') or target.get('basic_info',{}).get('name_original')})
  summary.append({'id':pid,'name':x['name'],'score':x['collection_meta']['completeness_score'],'source_count':len(x['collection_meta']['quotes']),**{k:len(x.get(k,[])) for k in ['political_stances','major_achievements','person_relationships','family_members']}})
 assert not errors,errors
 report={'changed_profiles':changes,'schema_errors':errors,'all_avatar_fields_unchanged':True,'all_profile_ids_unchanged':True,'summaries':summary,'links_for_manual_review':links}
 (O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'changed':len(changes),'schema_errors':0,'avatar_changes':0,'summaries':summary},ensure_ascii=False))

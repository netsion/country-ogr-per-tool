"""Register selected missing identities after whole-output historical ID scan."""
import pathlib,sys,json,re,subprocess,shutil,collections
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch6_20261115';O.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'.agents/skills/country-org-collector/scripts'))
from atomic_write import load_json,save_json
plan=load_json(str(R/'tmp/tw_batch6_selection.json'));reg=load_json(str(B/'id_registry.json'));lst=load_json(str(B/'person_list.json'))
for name in ['id_registry.json','person_list.json']:
 target=O/('pre_registration_'+name);assert not target.exists(),'Do not register twice';shutil.copy2(B/name,target)
scan=subprocess.run(['rg','--no-ignore','--hidden','--no-filename','-o','TW-PERSON-[0-9]{6}','output','-g','*.json','-g','*.csv','-g','*.md'],cwd=R,capture_output=True,text=True,encoding='utf-8');assert scan.returncode in [0,1],scan.stderr
used=set(re.findall(r'TW-PERSON-\d{6}',scan.stdout));maximum=max([int(i.rsplit('-',1)[1]) for i in used]+[reg['person_counters']['TW-PERSON'],reg['counters'].get('TW-PERSON',0)])
created=[]
for entry in plan['persons']:
 if entry['person_id']:continue
 names={entry['name'],entry['name_zh']}
 candidates=[]
 for f in (B/'persons').glob('TW-*.json'):
  d=load_json(str(f))
  if names.intersection({d.get('name'),d.get('name_zh'),*d.get('aliases',[])}):candidates.append(f.stem)
 assert not candidates,('Existing profile must be reused',entry['name'],candidates)
 rm=[e for e in reg['person_registry'] if names.intersection({e.get('name'),e.get('name_zh')})];assert not rm,('Existing registry requires identity review',rm)
 maximum+=1;assert maximum<1000000;pid=f'TW-PERSON-{maximum:06d}';assert pid not in used
 entry.update(person_id=pid,name_en='',status='registered_pending_research')
 reg['person_registry'].append({'person_id':pid,'name':entry['name'],'name_zh':entry['name_zh'],'name_en':'','wikidata_qid':None,'status':'registered'})
 reg['person_counters']['TW-PERSON']=maximum;reg['counters']['TW-PERSON']=maximum
 save_json(str(B/'id_registry.json'),reg)
 skeleton={'person_id':pid,'name':entry['name'],'name_en':'','name_zh':entry['name_zh'],'nationality':'TW','gender':'unknown','wikidata_qid':None,'aliases':[],'profile':None,'current_positions':[],'education':[],'work_experience':[],'political_stances':[],'major_achievements':[],'person_relationships':[],'family_members':[],'social_accounts':[],'collection_meta':{'collection_date':'2026-11-15','phase':'phase4_person_profile','data_sources':['web_search'],'quotes':[{'title':'选人身份线索；待人物研究核读原文','url':entry.get('official_url') or entry['independent_source_url']}],'notes':'仅注册姓名身份骨架，英文名及现职等均待深采；不代表研究完成。'}}
 save_json(str(B/'persons'/f'{pid}.json'),skeleton)
 lst['persons'].append({'person_id':pid,'name':entry['name'],'name_en':'','name_zh':entry['name_zh'],'nationality':'TW','wikidata_qid':None,'importance_level':'high','importance_reason':entry['selection_reason'],'source_orgs':[],'discovery_source':'web_search','notes':'第六批待研究身份骨架。'})
 created.append({'person_id':pid,'name':entry['name'],'official_url':entry['official_url']})
lst['metadata']['total_persons']=len(lst['persons'])
for key,field in [('by_importance_level','importance_level'),('by_discovery_source','discovery_source')]:lst['summary'][key]=dict(collections.Counter(e.get(field,'other') for e in lst['persons']))
lst['summary']['data_quality']={'with_person_id':sum(bool(e.get('person_id')) for e in lst['persons']),'with_wikidata_qid':sum(bool(e.get('wikidata_qid')) for e in lst['persons']),'without_person_id':sum(not e.get('person_id') for e in lst['persons'])}
save_json(str(B/'person_list.json'),lst);save_json(str(R/'tmp/tw_batch6_selection.json'),plan);save_json(str(O/'new_id_registration.json'),{'ever_used_count':len(used),'historical_max':max(int(i.rsplit('-',1)[1]) for i in used),'created':created})
print(json.dumps(created,ensure_ascii=False))

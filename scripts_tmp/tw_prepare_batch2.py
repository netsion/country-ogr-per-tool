"""Register missing selected candidates and persist the next serial research queue."""
import json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.agents/skills/country-org-collector/scripts'))
from atomic_write import load_json,save_json
BASE=ROOT/'output/tw/2026-07-27'
plan=load_json(str(ROOT/'tmp/tw_batch2_selection.json'))
reg=load_json(str(BASE/'id_registry.json'))
lst=load_json(str(BASE/'person_list.json'))
index=load_json(str(BASE/'_name_index.json'))
maximum=max([reg['counters'].get('TW-PERSON',0),reg['person_counters'].get('TW-PERSON',0)]+[int(f.stem.rsplit('-',1)[1]) for f in (BASE/'persons').glob('TW-*.json')])
for entry in plan['persons']:
 if entry['person_id']:continue
 matches={index[n] for n in [entry['name'],entry['name_zh'],entry['name_en']] if n in index and index[n].startswith('TW-PERSON-')}
 assert len(matches)<=1,(entry['name'],matches)
 if matches:
  entry['person_id']=matches.pop();continue
 maximum+=1;pid=f'TW-PERSON-{maximum:06d}';entry['person_id']=pid
 reg['counters']['TW-PERSON']=maximum;reg['person_counters']['TW-PERSON']=maximum
 reg['person_registry'].append({'person_id':pid,'name':entry['name'],'name_zh':entry['name_zh'],'name_en':entry['name_en'],'wikidata_qid':None,'status':'registered'})
 save_json(str(BASE/'id_registry.json'),reg)
 skeleton={'person_id':pid,'name':entry['name'],'name_zh':entry['name_zh'],'name_en':entry['name_en'],'wikidata_qid':None,'nationality':'TW','gender':'unknown','aliases':[],
  'current_positions':[],'education':[],'work_experience':[],'political_stances':[],'major_achievements':[],'person_relationships':[],'family_members':[],'social_accounts':[],
  'collection_meta':{'collection_date':'2026-11-13','phase':'phase4_person_profile','data_sources':['web_search'],'quotes':[{'title':'候选来源（待逐人深采复核）','url':s['url']} for s in entry['sources']],
   'notes':'仅为下一批候选建立身份骨架，尚未执行深采；现职、英文名及其他事实均须逐人核实。'}}
 save_json(str(BASE/'persons'/(pid+'.json')),skeleton)
 lst['persons'].append({'person_id':pid,'name':entry['name'],'name_zh':entry['name_zh'],'name_en':entry['name_en'],'wikidata_qid':None,'importance_level':'high','importance_reason':entry['selection_reason'],'source_orgs':[],'discovery_source':'web_search','nationality':'TW','notes':'下一批候选；尚未深采，现职与来源需逐人复核。'})
lst['metadata']['total_persons']=len(lst['persons'])
from collections import Counter
lst['summary']['by_importance_level']=dict(Counter(x['importance_level'] for x in lst['persons']))
lst['summary']['by_discovery_source']=dict(Counter(x.get('discovery_source','other') for x in lst['persons']))
lst['summary']['data_quality']={'with_person_id':len(lst['persons']),'with_wikidata_qid':sum(bool(x.get('wikidata_qid')) for x in lst['persons']),'without_person_id':0}
save_json(str(BASE/'person_list.json'),lst)
save_json(str(ROOT/'tmp/tw_batch2_selection.json'),plan)
save_json(str(BASE/'_batch2_progress.json'),{'phase':'P4_batch2_deep_research','completed':[],'remaining':[x['person_id'] for x in plan['persons']],'current':None,'failed':[]})
print([(x['person_id'],x['name_zh']) for x in plan['persons']])

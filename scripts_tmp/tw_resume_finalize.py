"""Refresh only researched person entries; never use global automatic relinking."""
import pathlib,sys,collections,json,shutil
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27'
sys.path.insert(0,str(R/'.agents/skills/country-org-collector/scripts'))
from atomic_write import load_json,save_json,decompose_name
p=load_json(str(B/'_batch2_progress.json'));assert not p['remaining'] and len(p['completed'])==15
backup=R/'tmp/tw_resume_20261114/index_before';backup.mkdir(parents=True,exist_ok=True)
for source in [B/'persons/_index.json',B/'_name_index.json']:
 target=backup/('persons_index.json' if source.parent.name=='persons' else source.name)
 if not target.exists():shutil.copy2(source,target)
index=load_json(str(B/'persons/_index.json'));entries={x['person_id']:x for x in index['profiles']}
lst=load_json(str(B/'person_list.json'));li={x['person_id']:x for x in lst['persons']}
ni=load_json(str(B/'_name_index.json'));conflicts=[]
researched=list(dict.fromkeys(load_json(str(B/'_supplement_progress.json'))['completed']+p['completed']))
for pid in researched:
 x=load_json(str(B/'persons'/f'{pid}.json'))
 e=entries.setdefault(pid,{'person_id':pid,'file':f'{pid}.json'})
 e.update(wikidata_qid=x.get('wikidata_qid'),name_en=x.get('name_en'),name_zh=x.get('name_zh'),gender=x.get('gender'),importance_level=li[pid]['importance_level'],current_title=next(iter(x.get('current_positions',[])),None),completeness_score=x['collection_meta'].get('completeness_score'))
 for name in [x.get('name'),x.get('name_zh'),x.get('name_en'),*x.get('aliases',[])]:
  if not name:continue
  if ni.get(name) not in [None,pid]:conflicts.append({'name':name,'existing':ni[name],'expected':pid});continue
  ni[name]=pid
index['profiles']=sorted(entries.values(),key=lambda x:x['person_id']);index['metadata']['total_profiles']=len(entries)
scores=[e['completeness_score'] for e in entries.values() if e.get('completeness_score') is not None]
index['completeness_summary']={'avg_score':round(sum(scores)/len(scores)),'high_completeness_gt80':sum(s>80 for s in scores),'medium_completeness_50_80':sum(50<=s<=80 for s in scores),'low_completeness_lt50':sum(s<50 for s in scores)}
index['by_importance_level']=dict(collections.Counter(e['importance_level'] for e in entries.values()))
save_json(str(B/'persons/_index.json'),index);save_json(str(B/'_name_index.json'),ni)
p.update(status='complete',current=None,completed_at='2026-11-14');save_json(str(B/'_batch2_progress.json'),p)
(R/'tmp/tw_resume_20261114/index_conflicts.json').write_text(json.dumps(conflicts,ensure_ascii=False,indent=2),encoding='utf-8')
print('Refreshed',len(researched),'researched entries; total',len(entries),'name conflicts',len(conflicts))

"""Add only full primary names from completed TW research, without rebuilding indexes."""
import pathlib,json,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];BASE=ROOT/'output/tw/2026-07-27'
sys.path.insert(0,str(ROOT/'.agents/skills/country-org-collector/scripts'))
from atomic_write import load_json,save_json
idxpath=BASE/'_name_index.json';index=load_json(str(idxpath))
ids=load_json(str(BASE/'_supplement_progress.json'))['completed']+load_json(str(BASE/'_batch2_progress.json'))['completed']
changes=[];conflicts=[]
for pid in ids:
 data=load_json(str(BASE/'persons'/(pid+'.json')))
 for field in ['name','name_zh','name_en']:
  name=data.get(field)
  if not isinstance(name,str) or not name.strip():continue
  name=name.strip();existing=index.get(name)
  if existing is None:
   index[name]=pid;changes.append({'name':name,'person_id':pid,'field':field})
  elif existing!=pid:
   conflicts.append({'name':name,'existing_id':existing,'researched_id':pid,'field':field})
backup=ROOT/'tmp/tw_verified_name_index_before.json'
if not backup.exists():save_json(str(backup),load_json(str(idxpath)))
save_json(str(idxpath),index)
save_json(str(ROOT/'tmp/tw_verified_name_key_audit.json'),{'added':changes,'conflicts_not_overwritten':conflicts,'researched_people':len(ids),'method':'full primary names only; no aliases, fragments, fuzzy resolution, or registry-derived keys'})
print(json.dumps({'added_keys':len(changes),'conflicts_not_overwritten':len(conflicts),'people':len(ids)}))

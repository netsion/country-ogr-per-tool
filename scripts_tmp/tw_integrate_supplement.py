"""Install incremental, sourced research for the reviewed TW first batch."""
import pathlib
import json
import sys
import shutil
import jsonschema
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/'output/tw/2026-07-27'
SC=ROOT/'.agents/skills/country-org-collector'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):
    t=p.with_suffix('.json.tmp');t.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');t.replace(p)
pid=sys.argv[1]
batch=read(BASE/'_phase_progress.json')['completed']
assert pid in batch
src=ROOT/'tmp/tw_supplement'/(pid+'.json');dst=BASE/'persons'/(pid+'.json')
old=read(dst);new=read(src)
assert new['person_id']==old['person_id'] and new.get('wikidata_qid')==old.get('wikidata_qid')
jsonschema.Draft7Validator(read(SC/'person_profile_schema.json')).validate(new)
for field in ['education','work_experience','social_accounts','profile']:
    assert old.get(field)==new.get(field),f'Unexpected change to {field}'
backup=ROOT/'tmp/tw_supplement_before';backup.mkdir(exist_ok=True)
if not (backup/dst.name).exists():shutil.copy2(dst,backup/dst.name)
write(dst,new)
pp=BASE/'_supplement_progress.json'
progress=read(pp) if pp.exists() else {'phase':'P4_batch1_supplement','completed':[],'remaining':batch[:],'failed':[]}
if pid not in progress['completed']:progress['completed'].append(pid)
progress['remaining']=[v for v in progress['remaining'] if v!=pid]
write(pp,progress)
print(pid,{k:(len(old.get(k,[])),len(new.get(k,[]))) for k in ['political_stances','major_achievements','person_relationships','family_members']})

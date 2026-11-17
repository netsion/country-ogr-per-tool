"""Fill four explicitly sourced preexisting null references after the new identities are profiled."""
import pathlib,json,hashlib,copy,sys
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch7_20261116'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
log=O/'known_reference_backfills.json';assert not log.exists();progress=load(B/'_batch7_progress.json');assert len(progress['completed'])==15
baseline=load(O/'baseline.json');records=[];back=O/'reference_backfill_before';back.mkdir(exist_ok=True)
mapping=[('TW-PERSON-000558','TW-PERSON-000569','賴瑞隆','赖瑞隆'),('TW-PERSON-000559','TW-PERSON-000570','郭國文','郭国文'),('TW-PERSON-000566','TW-PERSON-000580','吳宗憲','吴宗宪'),('TW-PERSON-000568','TW-PERSON-000580','吳宗憲','吴宗宪')]
sys.path.insert(0,str(R/'.agents/skills/country-org-collector/scripts'));from atomic_write import save_json
for source,target,native,zh in mapping:
 t=load(B/'persons'/f'{target}.json');assert t['name']==native and t.get('name_zh')==zh
 assert target in progress['completed']
 if target=='TW-PERSON-000580':assert any('立法委' in s or '立委' in s for s in t['current_positions'])
 p=B/'persons'/f'{source}.json';key=p.relative_to(R).as_posix();old=load(p);new=copy.deepcopy(old);row=new['person_relationships'][0]
 assert digest(p)==baseline[key]['sha256'];assert row.get('person_id') is None and (native in row['person_name'] or zh in row['person_name'])
 if target=='TW-PERSON-000580':assert '立委' in row['description'] or '国会职权' in row['description']
 prior=copy.deepcopy(row);row['person_id']=target;before=digest(p)
 save_json(str(back/p.name),old);save_json(str(p),new)
 assert new.get('profile')==old.get('profile') and new['social_accounts']==old['social_accounts']
 records.append({'path':key,'index':0,'target_id':target,'expected_row':prior,'before_sha256':before,'after_sha256':digest(p)})
save_json(str(log),records);print('Filled four explicitly reviewed old null references')

"""Validate and install one independently researched second-batch profile."""
import json,pathlib,shutil,sys
import jsonschema
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/'output/tw/2026-07-27';SC=ROOT/'.agents/skills/country-org-collector'
sys.path.insert(0,str(SC/'scripts'))
from atomic_write import load_json,save_json
pid=sys.argv[1];pp=BASE/'_batch2_progress.json';progress=load_json(str(pp))
assert pid in progress['remaining']+progress['completed']
target=BASE/'persons'/(pid+'.json');old=load_json(str(target));new=load_json(str(ROOT/'tmp/tw_batch2_enriched'/(pid+'.json')))
if pid in progress['completed']:
    assert new == old, 'Completed profile differs from staged copy; use a reviewed incremental update, never overwrite newer corrections'
    print('Already installed without changes:',pid)
    raise SystemExit(0)
assert new['person_id']==old['person_id']==pid
if old.get('wikidata_qid'):assert new.get('wikidata_qid')==old['wikidata_qid'],'Existing QID changed; review identity before install'
jsonschema.Draft7Validator(load_json(str(SC/'person_profile_schema.json'))).validate(new)
assert len(new.get('biography_summary',''))>=200
assert len(new.get('work_experience',[]))>=2
assert len(new['collection_meta'].get('quotes',[]))>=3
old_ids={str(x['user_id']) for x in old.get('social_accounts',[]) if x.get('user_id')}
new_ids={str(x['user_id']) for x in new.get('social_accounts',[]) if x.get('user_id')}
assert not old_ids-new_ids,'Existing social platform IDs were lost'
if old.get('profile'):
    assert new.get('profile') == old['profile'], 'Existing avatar fields changed; retain them and record verification limits in notes'
# Newly assigned identities must not duplicate another existing profile.
if not old.get('wikidata_qid') and new.get('wikidata_qid'):
    for other in (BASE/'persons').glob('TW-*.json'):
        if other.stem != pid:
            assert load_json(str(other)).get('wikidata_qid') != new['wikidata_qid'], f'Duplicate QID in {other.name}'
# A registry/name-index hit alone is insufficient: every non-null new link must
# resolve to an actual profile of the expected entity kind. Names require
# evidence review by the researcher; this guard rejects missing or cross-kind IDs.
for array, field, folder, idkey in [('work_experience','org_id','orgs','org_id'),
                                  ('person_relationships','person_id','persons','person_id'),
                                  ('family_members','person_id','persons','person_id')]:
    for entry in new.get(array,[]):
        linked=entry.get(field)
        if not linked:
            continue
        assert ('-PERSON-' in linked) == (folder == 'persons'), f'Wrong reference kind: {linked}'
        matches=list((ROOT/'output').glob(f'[a-z][a-z]/20*/{folder}/{linked}.json'))
        assert matches, f'No actual {folder} profile for {linked}; keep unknown IDs null'
        assert all(load_json(str(match)).get(idkey)==linked for match in matches), f'Profile identity mismatch for {linked}'
backup=ROOT/'tmp/tw_batch2_before';backup.mkdir(exist_ok=True)
if not (backup/target.name).exists():shutil.copy2(target,backup/target.name)
save_json(str(target),new)
registry=load_json(str(BASE/'id_registry.json'))
for entry in registry['person_registry']:
 if entry['person_id']==pid:entry.update(name=new['name'],name_zh=new.get('name_zh'),name_en=new['name_en'],wikidata_qid=new.get('wikidata_qid'),status='profiled')
save_json(str(BASE/'id_registry.json'),registry)
lst=load_json(str(BASE/'person_list.json'))
for entry in lst['persons']:
 if entry['person_id']==pid:entry.update(name=new['name'],name_zh=new.get('name_zh'),name_en=new['name_en'],wikidata_qid=new.get('wikidata_qid'),importance_level='high',notes='已执行第二批公开资料深采；来源边界、空字段原因和冲突见人物collection_meta.notes。')
from collections import Counter
lst['metadata']['total_persons']=len(lst['persons'])
lst['summary']['by_importance_level']=dict(Counter(entry['importance_level'] for entry in lst['persons']))
lst['summary']['by_discovery_source']=dict(Counter(entry.get('discovery_source','other') for entry in lst['persons']))
lst['summary']['data_quality']={'with_person_id':sum(bool(entry.get('person_id')) for entry in lst['persons']),
                                'with_wikidata_qid':sum(bool(entry.get('wikidata_qid')) for entry in lst['persons']),
                                'without_person_id':sum(not entry.get('person_id') for entry in lst['persons'])}
save_json(str(BASE/'person_list.json'),lst)
if pid not in progress['completed']:progress['completed'].append(pid)
progress['remaining']=[x for x in progress['remaining'] if x!=pid];progress['current']=None
progress['last_updated']='2026-11-14'
progress['status']='complete' if not progress['remaining'] else 'running'
save_json(str(pp),progress)
print('Installed',pid,'batch2',len(progress['completed']),'/15')

"""Validate that selection stays inside the original profile set before snapshotting."""
import pathlib,json,shutil
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch9_20261117';P=R/'tmp/tw_batch9_selection.json'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
d=load(P);assert 'selected' in d and 'persons' not in d
shutil.copy2(P,O/'selection_discovery_original.json')
people=d.pop('selected');assert len(people)==15 and len({x['person_id'] for x in people})==15
done=set()
for name in ['_supplement_progress.json',*[f'_batch{i}_progress.json' for i in range(2,9)]]:done.update(load(B/name)['completed'])
assert len(done)==115 and not done.intersection(x['person_id'] for x in people)
for x in people:
 p=B/'persons'/f"{x['person_id']}.json";old=load(p)
 assert old['person_id']==x['person_id'] and x['name'] in [old['name'],old.get('name_zh'),*old.get('aliases',[])]
 x['existing_profile']=p.relative_to(R).as_posix();x['requires_recent_activity_verification']=True
d['persons']=people;d['research_gate']='每人P4必须核可读2026政治/公共活动原文；初筛摘要不得当事实，无证可在原库内更换，不新增ID。'
P.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Validated 15 existing IDs, excluded all previous 115; no registrations')

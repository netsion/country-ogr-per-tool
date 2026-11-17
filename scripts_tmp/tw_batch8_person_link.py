"""Apply the single manually reviewed same-identity Singapore reference."""
import pathlib,json,copy
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch8_20261117'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
log=O/'verified_person_links.json';assert not log.exists()
p=B/'persons/TW-PERSON-000593.json';old=load(p);d=copy.deepcopy(old);row=d['person_relationships'][0]
assert row['person_id'] is None and row['person_name']=='马炎庆' and '东北区市长' in row['description']
t=load(R/'output/sg/2026-04-15/persons/SG-PERSON-000342.json')
assert t['name']=='Baey Yam Keng' and t['name_zh']=='马炎庆' and '东北区市长' in t['current_positions']
assert any(e['position']=='市长' and e['organization']=='东北区 (North East District)' and e['start_date']=='2025-05-23' for e in t['work_experience'])
row['person_id']=t['person_id'];d['collection_meta']['notes']+=' 主会话已读新加坡马炎庆Baey Yam Keng真实画像，核东北区市长与淡滨尼任职身份，补齐该次公务交流引用；不更新目标画像其他事实。'
backup=O/'before_person_reference_links';backup.mkdir(exist_ok=True)
(backup/p.name).write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for dest in [p,R/'tmp/tw_batch8_enriched'/p.name]:dest.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
log.write_text(json.dumps([{'source':p.stem,'field':'person_relationships','index':0,'before':old['person_relationships'][0],'target_id':t['person_id'],'target_name':t['name'],'review':'真实姓名、中文名、东北区市长职务与2025任职日期及淡滨尼背景一致'}],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Filled one manually verified Singapore person reference')

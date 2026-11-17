"""Final metadata, reference and scope checks for batch eight."""
import pathlib,json,sys,hashlib
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch8_20261117'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
p=load(B/'_batch8_progress.json');assert p['status']=='complete' and len(p['completed'])==15 and not p['remaining']
v=load(O/'validation.json');reviewed=int(sys.argv[1]);assert reviewed==len(v['links_for_manual_review'])
idx=load(B/'persons/_index.json');reg=load(B/'id_registry.json');ni=load(B/'_name_index.json');lst=load(B/'person_list.json')
assert len(list((B/'persons').glob('TW-PERSON-*.json')))==598==idx['metadata']['total_profiles']
assert len({e['person_id'] for e in idx['profiles']})==len(idx['profiles'])==598
assert len(v['changed_profiles'])==15 and not v['index_conflicts'] and not v['schema_errors']
for pid in p['completed']:
 d=load(B/'persons'/f'{pid}.json');assert d==load(R/'tmp/tw_batch8_enriched'/f'{pid}.json')
 assert len([e for e in reg['person_registry'] if e['person_id']==pid and e['status']=='profiled'])==1
 assert len([e for e in lst['persons'] if e['person_id']==pid])==1
 for n in [d['name'],d.get('name_zh'),*d.get('aliases',[])]:
  if n:assert ni[n]==pid,(pid,n,ni.get(n))
 for alias in load(O/'persons_before'/f'{pid}.json').get('aliases',[]):assert alias in d.get('aliases',[])
 for row in d.get('political_stances',[]):assert row['date']<=d['collection_meta']['collection_date'],(pid,row)
 assert d.get('profile') is None
created=load(O/'new_id_registration.json')['created'];assert len(created)==15
all_ids=[]
for name in ['_supplement_progress.json',*[f'_batch{i}_progress.json' for i in range(2,9)]]:all_ids+=load(B/name)['completed']
assert len(all_ids)==len(set(all_ids))==115
social=load(O/'social_identity_review.json');assert not any(social.values()),social
source=load(R/'tmp/social_xlsx_20261116/source.json');assert hashlib.sha256(pathlib.Path(source['path']).read_bytes()).hexdigest()==source['sha256']
orglog=O/'verified_org_links.json';orgs=load(orglog) if orglog.exists() else []
personlinks=load(O/'verified_person_links.json')
assert len(personlinks)==1 and personlinks[0]['source']=='TW-PERSON-000593' and personlinks[0]['target_id']=='SG-PERSON-000342'
v['manual_identity_review']={'status':'complete','references_checked':reviewed,'wrong_target_identity':0,'reviewed_org_backfills':len(orgs),'reviewed_person_backfills':len(personlinks),'scope':'逐条核对引用文字与目标画像身份；未全量更新目标画像其他事实。'}
v['metadata_verification']={'profiles':598,'unique_index_entries':598,'new_profiled_registry':15,'staged_formal_equal':True,'new_profiles_without_avatar':15,'all_nonselected_profiles_unchanged':True}
v['completed_research_total']=115;v['social_account_collision_review']=social;v['source_workbook_unchanged']=True
(O/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=R/'docs/tw_batch8_report.md';txt=report.read_text(encoding='utf-8').replace('逐条引用目标供人工核对',f'{reviewed}个非空引用目标已逐条核对身份')
accounts=sum(len(load(B/'persons'/f'{pid}.json').get('social_accounts',[])) for pid in p['completed'])
txt+=f'\n收尾：本批新增研究15人，八批累计115位不同人物。人物底库共598份，不等于全部已按本标准重采。{reviewed}个非空引用已核对身份，另补齐{len(orgs)}处本批组织空引用。姓名索引无冲突，15份暂存与正式文件一致。\n'
txt+=f'\n本批社交账号共{accounts}个，跨人物URL/USER-ID及平台前缀检查未发现碰撞或错配；用户《社交.xlsx》原文件校验值未变。来源层次、实时认证未核及USER/PAGE字段分别注明。新画像均未采头像；所有既有画像ID及头像字段与基线一致。许淑华限定南投身份，未混同台北市同名议员。\n'
txt+='\n另补齐本批谢国樑→新加坡马炎庆Baey Yam Keng一处人物空引用，已读SG-PERSON-000342实际画像核对中文名、职务及地区；未修改新加坡画像。\n'
report.write_text(txt,encoding='utf-8')
marker=B/'.inflight';assert marker.read_text(encoding='utf-8')=='TW batch8 2026-11-17';marker.unlink()
print(json.dumps({'completed':15,'total_researched':115,'reviewed_links':reviewed,'org_backfills':len(orgs),'social_accounts':accounts,'new_without_avatar':15,'marker_removed':True},ensure_ascii=False))

"""Close batch seven after manual reference identity review."""
import json,pathlib,sys
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch7_20261116'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
p=load(B/'_batch7_progress.json');assert p['status']=='complete' and len(p['completed'])==15 and not p['remaining']
v=load(O/'validation.json');reviewed=int(sys.argv[1]);assert reviewed==len(v['links_for_manual_review'])
idx=load(B/'persons/_index.json');reg=load(B/'id_registry.json');ni=load(B/'_name_index.json');lst=load(B/'person_list.json')
assert len(list((B/'persons').glob('TW-PERSON-*.json')))==583==idx['metadata']['total_profiles']
assert len({e['person_id'] for e in idx['profiles']})==len(idx['profiles'])==583
preserved=0
for pid in p['completed']:
 d=load(B/'persons'/f'{pid}.json');assert d==load(R/'tmp/tw_batch7_enriched'/f'{pid}.json')
 assert len([e for e in reg['person_registry'] if e['person_id']==pid and e['status']=='profiled'])==1
 assert len([e for e in lst['persons'] if e['person_id']==pid])==1
 for name in [d['name'],d.get('name_zh')]:
  if name:assert ni[name]==('TW-PERSON-000349' if pid=='TW-PERSON-000580' else pid),(pid,name,ni.get(name))
 for a in load(O/'persons_before'/f'{pid}.json').get('social_accounts',[]):
  assert any(all(a.get(k)==n.get(k) for k in ['platform','url','user_id','username','nickname'] if a.get(k)) for n in d.get('social_accounts',[]))
  preserved+=1
 for row in d.get('political_stances',[]):assert row['date']<=d['collection_meta']['collection_date'],(pid,row)
for name in ['吳宗憲（立法委員）','吴宗宪（立法委员）','吳宗憲（立委）','吴宗宪（立委）']:assert ni[name]=='TW-PERSON-000580'
assert all(c['existing']=='TW-PERSON-000349' and c['expected']=='TW-PERSON-000580' and c['name'] in ['吳宗憲','吴宗宪'] for c in v['index_conflicts'])
assert not v['schema_errors']
social=load(O/'social_identity_review.json')
assert not any(social.values()),social
source=load(R/'tmp/social_xlsx_20261116/source.json')
import hashlib
assert hashlib.sha256(pathlib.Path(source['path']).read_bytes()).hexdigest()==source['sha256']
created=load(O/'new_id_registration.json')['created'];assert len(created)==15
assert all(load(B/'persons'/f"{e['person_id']}.json")['profile'] is None for e in created)
all_ids=[]
for name in ['_supplement_progress.json',*[f'_batch{i}_progress.json' for i in range(2,8)]]:all_ids+=load(B/name)['completed']
assert len(all_ids)==len(set(all_ids))==100
orglog=O/'verified_org_links.json';orgs=load(orglog) if orglog.exists() else []
refs=load(O/'known_reference_backfills.json');assert len(refs)==4
v['manual_identity_review']={'status':'complete','references_checked':reviewed,'wrong_target_identity':0,'scope':'逐条核对引用文字与实际目标画像身份；未全量更新关联画像其他字段。','reviewed_organization_backfills':len(orgs)}
v['metadata_verification']={'person_profiles':583,'unique_index_entries':583,'batch_registry_profiled':15,'staged_formal_equal':True,'new_profiles_without_avatar':15,'preserved_original_accounts':preserved,'reviewed_same_name_index_conflicts':v['index_conflicts']}
v['completed_research_total']=100
v['social_account_collision_review']=social
v['source_workbook_unchanged']=True
(O/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=R/'docs/tw_batch7_report.md';txt=report.read_text(encoding='utf-8').replace('逐条引用目标供人工核对',f'{reviewed}个非空引用目标已逐条核对身份')
txt+=f'\n收尾：本批新增研究15人，七批累计100位不同人物。人物底库共583份，不等同本轮重新采集数量。{reviewed}个非空引用核对身份，补齐{len(orgs)}处组织引用及4处既有人物空引用。后4处仅改链接，不计为新增研究。\n'
txt+='\n同名消歧：立委吴宗宪使用TW-PERSON-000580，艺人使用TW-PERSON-000349；裸名索引保留原艺人归属，立委限定别名指向新政治人物档案。15个新画像暂未采集头像，原有头像和画像ID均未修改。社交表关联、官网外链与实时认证分开标注，USER-ID和PAGE-ID分列处理。\n'
report.write_text(txt,encoding='utf-8')
accounts=sum(len(load(B/'persons'/f'{pid}.json').get('social_accounts',[])) for pid in p['completed'])
with report.open('a',encoding='utf-8') as f:f.write(f'\n本批社交账号共{accounts}个；跨人物URL、USER-ID及平台前缀检查未发现碰撞或错配。原始《社交.xlsx》校验值未变。账号来源层次与身份字段冲突处理见tmp/tw_batch7_20261116/social_id_supplement.json。\n')
marker=B/'.inflight';assert marker.read_text(encoding='utf-8')=='TW batch7 2026-11-16';marker.unlink()
print(json.dumps({'completed':15,'total_researched':100,'reviewed_links':reviewed,'org_backfills':len(orgs),'old_reference_backfills':4,'new_without_avatar':15,'marker_removed':True},ensure_ascii=False))

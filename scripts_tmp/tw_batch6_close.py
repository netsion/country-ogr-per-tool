"""Verify final metadata after explicit manual reference-identity review."""
import json,pathlib,sys
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch6_20261115'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
p=load(B/'_batch6_progress.json');assert p['status']=='complete' and len(p['completed'])==15 and not p['remaining']
ids=p['completed'];v=load(O/'validation.json');reviewed=int(sys.argv[1]);assert reviewed==len(v['links_for_manual_review'])
idx=load(B/'persons/_index.json');reg=load(B/'id_registry.json');ni=load(B/'_name_index.json');lst=load(B/'person_list.json')
profiles=list((B/'persons').glob('TW-PERSON-*.json'));assert len(profiles)==568==idx['metadata']['total_profiles']
assert len({e['person_id'] for e in idx['profiles']})==len(idx['profiles'])==568
preserved_accounts=0
for pid in ids:
 d=load(B/'persons'/f'{pid}.json');assert d==load(R/'tmp/tw_batch6_enriched'/f'{pid}.json')
 assert len([e for e in reg['person_registry'] if e['person_id']==pid and e['status']=='profiled'])==1
 assert len([e for e in lst['persons'] if e['person_id']==pid])==1
 for name in [d['name'],d.get('name_zh')]:
  if name:assert ni[name]==pid,(name,ni.get(name),pid)
 old=load(O/'persons_before'/f'{pid}.json')
 for a in old.get('social_accounts',[]):
  if not a.get('user_id'):continue
  assert any(all(a.get(k)==n.get(k) for k in ['platform','url','user_id']) for n in d.get('social_accounts',[]))
  preserved_accounts+=1
 for row in d.get('political_stances',[]):assert row['date']<=d['collection_meta']['collection_date'],(pid,row)
registered=load(O/'new_id_registration.json')['created'];assert len(registered)==13
assert all(load(B/'persons'/f"{x['person_id']}.json")['profile'] is None for x in registered)
assert not v['index_conflicts'] and not v['schema_errors']
org_changes=load(O/'verified_org_links.json')
v['manual_identity_review']={'status':'complete','references_checked':reviewed,'wrong_target_identity':0,'scope':'逐条核对引用文字及真实目标画像身份；未对目标画像其他字段开展全量更新。','reviewed_organization_backfills':len(org_changes)}
v['metadata_verification']={'person_profiles':568,'unique_index_entries':568,'batch_registry_profiled':15,'primary_name_index_conflicts':0,'staged_formal_equal':True,'new_profiles_without_avatar':13,'preserved_original_platform_url_user_id_pairs':preserved_accounts}
all_ids=[]
for name in ['_supplement_progress.json','_batch2_progress.json','_batch3_progress.json','_batch4_progress.json','_batch5_progress.json','_batch6_progress.json']:all_ids+=load(B/name)['completed']
assert len(all_ids)==len(set(all_ids))==85
v['completed_research_total']=85
(O/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=R/'docs/tw_batch6_report.md';text=report.read_text(encoding='utf-8').replace('逐条引用目标供人工核对',f'{reviewed}个非空引用目标已逐条核对身份')
text+=f'\n复核收尾：{reviewed}个非空引用目标身份匹配，{len(org_changes)}处组织空引用补齐；姓名索引无冲突，人物索引568份且ID唯一。六批累计完成85位不同人物，本批均为政治人物。选人文件仅初筛线索，最终近期活跃及原文读取限制以各档quotes/notes为准。\n'
text+='\n重点边界：沈伯洋台大学位来源冲突，暂未填写该学位；许智杰未将博士候选人写成已取得博士；王世坚历史YouTube账号官方归属待核，保留原URL及ID并在账号source_note警示；陈清龙健保相关修法只记录三读，注明未实施。\n'
report.write_text(text,encoding='utf-8')
marker=B/'.inflight';assert marker.read_text(encoding='utf-8')=='TW batch6 2026-11-15';marker.unlink()
print(json.dumps({'completed':15,'total_researched':85,'schema_errors':0,'reviewed_links':reviewed,'org_backfills':len(org_changes),'original_account_pairs_preserved':preserved_accounts,'new_without_avatar':13,'marker_removed':True},ensure_ascii=False))

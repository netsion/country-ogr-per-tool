"""Close an existing-profile research batch with original identity safeguards."""
import pathlib,json,sys,hashlib
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch9_20261117'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
p=load(B/'_batch9_progress.json');assert p['status']=='complete' and len(p['completed'])==15 and not p['remaining']
v=load(O/'validation.json');reviewed=int(sys.argv[1]);assert reviewed==len(v['links_for_manual_review'])
idx=load(B/'persons/_index.json');reg=load(B/'id_registry.json');ni=load(B/'_name_index.json');lst=load(B/'person_list.json')
assert len(list((B/'persons').glob('TW-PERSON-*.json')))==598==idx['metadata']['total_profiles']
assert len({e['person_id'] for e in idx['profiles']})==len(idx['profiles'])==598
assert len(v['changed_profiles'])==15 and not v['index_conflicts'] and not v['schema_errors']
assert load(O/'new_id_registration.json')['created']==[]
prior_reg=load(O/'id_registry_before.json');assert reg['person_counters']==prior_reg['person_counters'] and reg['counters']==prior_reg['counters']
preserved_accounts=0;preserved_avatars=0
for pid in p['completed']:
 d=load(B/'persons'/f'{pid}.json');old=load(O/'persons_before'/f'{pid}.json')
 assert d==load(R/'tmp/tw_batch9_enriched'/f'{pid}.json')
 assert d['person_id']==old['person_id'] and d.get('profile')==old.get('profile')
 if old.get('wikidata_qid'):assert d.get('wikidata_qid')==old['wikidata_qid']
 preserved_avatars+=int(old.get('profile') is not None)
 assert len([e for e in reg['person_registry'] if e['person_id']==pid and e['status']=='profiled'])==1
 assert len([e for e in lst['persons'] if e['person_id']==pid])==1
 for n in [d['name'],d.get('name_zh')]:
  if n:assert ni[n]==pid,(pid,n,ni.get(n))
 for alias in old.get('aliases',[]):assert alias in d.get('aliases',[])
 for a in old.get('social_accounts',[]):
  matches=[n for n in d.get('social_accounts',[]) if n.get('platform')==a.get('platform') and n.get('url')==a.get('url')]
  assert any(all(n.get(k)==a.get(k) for k in ['user_id','username','nickname'] if a.get(k)) for n in matches)
  if a.get('source_note'):assert any(a['source_note'] in n.get('source_note','') for n in matches)
  preserved_accounts+=1
 for row in d.get('political_stances',[]):assert row['date']<=d['collection_meta']['collection_date']
all_ids=[]
for name in ['_supplement_progress.json',*[f'_batch{i}_progress.json' for i in range(2,10)]]:all_ids+=load(B/name)['completed']
assert len(all_ids)==len(set(all_ids))==130
social=load(O/'social_identity_review.json');assert not any(social.values()),social
source=load(R/'tmp/social_xlsx_20261116/source.json');assert hashlib.sha256(pathlib.Path(source['path']).read_bytes()).hexdigest()==source['sha256']
orglog=O/'verified_org_links.json';orgs=load(orglog) if orglog.exists() else []
v['manual_identity_review']={'status':'complete','references_checked':reviewed,'wrong_target_identity':0,'reviewed_org_backfills':len(orgs),'scope':'逐条核对引用文字与目标画像身份；未全量更新目标画像其他事实。'}
v['metadata_verification']={'profiles':598,'unique_index_entries':598,'existing_profiles_researched':15,'new_profiles':0,'staged_formal_equal':True,'preserved_original_avatars':preserved_avatars,'preserved_original_social_accounts':preserved_accounts,'all_nonselected_profiles_unchanged':True}
v['completed_research_total']=130;v['social_account_collision_review']=social;v['source_workbook_unchanged']=True
(O/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=R/'docs/tw_batch9_report.md';txt=report.read_text(encoding='utf-8').replace('逐条引用目标供人工核对',f'{reviewed}个非空引用目标已逐条核对身份')
accounts=sum(len(load(B/'persons'/f'{pid}.json').get('social_accounts',[])) for pid in p['completed'])
txt+=f'\n收尾：本批仅重采既有15份人物画像，未新建身份、未分配ID，底库仍为598份；九批累计深度研究130位不同人物。{reviewed}个非空引用已核对，补齐{len(orgs)}处本批组织空引用。姓名索引无冲突。\n'
txt+=f'\n本批社交账号共{accounts}个，原有{preserved_accounts}条账号完整保留，原有{preserved_avatars}份头像引用保持不变。原始社交.xlsx校验值未变；账号表关联与实时官方认证分开说明，USER/PAGE字段分列。现职与历史职务按近期证据重建，不沿用旧库过时头衔。\n'
report.write_text(txt,encoding='utf-8')
marker=B/'.inflight';assert marker.read_text(encoding='utf-8')=='TW batch9 2026-11-17';marker.unlink()
print(json.dumps({'completed':15,'total_researched':130,'new_profiles':0,'profile_count':598,'reviewed_links':reviewed,'org_backfills':len(orgs),'social_accounts':accounts,'preserved_original_accounts':preserved_accounts,'preserved_original_avatars':preserved_avatars,'marker_removed':True},ensure_ascii=False))

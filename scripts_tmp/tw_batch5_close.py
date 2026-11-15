"""Verify final metadata and record completed manual identity checks."""
import json,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch5_20261115'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
p=load(B/'_batch5_progress.json');assert p['status']=='complete' and len(p['completed'])==15 and not p['remaining']
ids=p['completed'];idx=load(B/'persons/_index.json');reg=load(B/'id_registry.json');ni=load(B/'_name_index.json');lst=load(B/'person_list.json')
profiles=list((B/'persons').glob('TW-PERSON-*.json'));assert len(profiles)==555==idx['metadata']['total_profiles']
assert len({e['person_id'] for e in idx['profiles']})==len(idx['profiles'])==555
for pid in ids:
 d=load(B/'persons'/f'{pid}.json');assert d==load(R/'tmp/tw_batch5_enriched'/f'{pid}.json')
 assert len([e for e in reg['person_registry'] if e['person_id']==pid and e['status']=='profiled'])==1
 assert len([e for e in lst['persons'] if e['person_id']==pid])==1
 for name in [d['name'],d.get('name_zh'),d['name_en']]:
  if name:assert ni[name]==pid,(name,ni.get(name),pid)
registered=load(O/'new_id_registration.json')['created'];assert len(registered)==14
assert all(load(B/'persons'/f"{x['person_id']}.json")['profile'] is None for x in registered)
v=load(O/'validation.json');assert len(v['links_for_manual_review'])==42 and not v['index_conflicts'] and not v['schema_errors']
v['manual_identity_review']={'status':'complete','references_checked':42,'wrong_target_identity':0,'scope':'逐条核对引用文字与实际目标画像身份；未对目标画像其他字段开展全量更新。','reviewed_organization_backfills':14}
v['metadata_verification']={'person_profiles':555,'unique_index_entries':555,'batch_profiles_registered_as_profiled':15,'primary_name_index_conflicts':0,'staged_formal_equal':True,'new_profiles_without_avatar':14}
all_ids=[]
for name in ['_supplement_progress.json','_batch2_progress.json','_batch3_progress.json','_batch4_progress.json','_batch5_progress.json']:all_ids+=load(B/name)['completed']
assert len(all_ids)==len(set(all_ids))==70
v['completed_research_total']=70
(O/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=R/'docs/tw_batch5_report.md';text=report.read_text(encoding='utf-8').replace('逐条引用目标供人工核对','42个非空引用目标已逐条核对身份').replace('近期活跃证据保存在selection.json及各画像quotes/notes','选人初始线索保存在selection.json；最终近期活跃证据及读取限制以各画像quotes/notes为准')
text+='\n复核收尾：42个非空引用目标身份匹配，14处组织空引用补齐；姓名索引无冲突，人物索引555份且ID唯一，新增14份均无头像。五批累计完成70位不同人物。目标画像的其他历史字段未作全库更新。\n'
report.write_text(text,encoding='utf-8')
marker=B/'.inflight';assert marker.read_text(encoding='utf-8')=='TW batch5 2026-11-15';marker.unlink()
print(json.dumps({'completed':15,'total_researched':70,'schema_errors':0,'reviewed_links':42,'new_org_links':14,'primary_name_conflicts':0,'new_without_avatar':14,'marker_removed':True},ensure_ascii=False))

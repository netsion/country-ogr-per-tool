"""Scoped install/check/report for the third 15-person research batch."""
import pathlib,sys,json,hashlib,shutil,collections,subprocess
import jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch3_20261114';S=R/'tmp/tw_batch3_enriched'
SC=R/'.agents/skills/country-org-collector';sys.path.insert(0,str(SC/'scripts'))
from atomic_write import load_json,save_json
O.mkdir(exist_ok=True);S.mkdir(exist_ok=True)
def load(p):return load_json(str(p))
def save(p,d):save_json(str(p),d)
def snap():
 return {p.relative_to(R).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'id':load(p).get('person_id') or load(p).get('org_id'),'profile':load(p).get('profile')} for folder in ['persons','orgs'] for p in (B/folder).glob('TW-*.json')}
P=B/'_batch3_progress.json';action=sys.argv[1]
if action=='init':
 assert not P.exists(),'Existing batch3 progress must be resumed rather than overwritten'
 selection=load(R/'tmp/tw_batch3_selection.json');people=selection if isinstance(selection,list) else selection['persons']
 assert len(people)==15;ids=[x['person_id'] for x in people];assert len(set(ids))==15
 earlier=set(load(B/'_supplement_progress.json')['completed']+load(B/'_batch2_progress.json')['completed']);assert not earlier.intersection(ids)
 for pid in ids:assert (B/'persons'/f'{pid}.json').exists(),pid
 save(O/'baseline.json',snap())
 for path in [B/'id_registry.json',B/'person_list.json',B/'persons/_index.json',B/'_name_index.json']:
  shutil.copy2(path,O/('persons_index_before.json' if path.parent.name=='persons' else path.stem+'_before.json'))
 save(P,{'phase':'P4_batch3_deep_research','started_at':'2026-11-14','status':'running','completed':[],'remaining':ids,'current':ids[0],'failed':[]})
 save(O/'selection.json',{'persons':people});(B/'.inflight').write_text('TW batch3 2026-11-14',encoding='utf-8')
 print('Initialized 15-person batch')
elif action=='install':
 pid=sys.argv[2];p=load(P);assert pid in p['remaining'];x=load(S/f'{pid}.json');old=load(B/'persons'/f'{pid}.json')
 assert x['person_id']==old['person_id']==pid
 assert x['name_en'].strip(),'English name still pending'
 if old.get('wikidata_qid'):assert x.get('wikidata_qid')==old['wikidata_qid']
 jsonschema.Draft7Validator(load(SC/'person_profile_schema.json')).validate(x)
 assert len(x.get('biography_summary',''))>=200 and len(x.get('work_experience',[]))>=2
 assert len(x['collection_meta'].get('quotes',[]))>=3
 assert x.get('profile')==old.get('profile'),'Avatar changed'
 assert {str(a['user_id']) for a in old.get('social_accounts',[]) if a.get('user_id')}<={str(a['user_id']) for a in x.get('social_accounts',[]) if a.get('user_id')}
 if x.get('wikidata_qid') and not old.get('wikidata_qid'):
  assert not [f.name for f in (B/'persons').glob('TW-*.json') if f.stem!=pid and load(f).get('wikidata_qid')==x['wikidata_qid']],'QID duplicates an existing profile'
 for key,field,folder in [('work_experience','org_id','orgs'),('person_relationships','person_id','persons'),('family_members','person_id','persons')]:
  for row in x.get(key,[]):
   rid=row.get(field);assert rid!=''
   if rid:
    assert ('-PERSON-' in rid)==(folder=='persons')
    targets=list((R/'output').glob(f'[a-z][a-z]/20*/{folder}/{rid}.json'));assert targets,(key,rid)
    assert all(load(f).get(field)==rid for f in targets),(key,rid)
 backup=O/'persons_before';backup.mkdir(exist_ok=True);assert not (backup/f'{pid}.json').exists()
 shutil.copy2(B/'persons'/f'{pid}.json',backup/f'{pid}.json');save(B/'persons'/f'{pid}.json',x)
 reg=load(B/'id_registry.json');matches=[e for e in reg['person_registry'] if e['person_id']==pid];assert len(matches)==1
 matches[0].update(name=x['name'],name_zh=x.get('name_zh'),name_en=x['name_en'],wikidata_qid=x.get('wikidata_qid'),status='profiled');save(B/'id_registry.json',reg)
 lst=load(B/'person_list.json');e=next(e for e in lst['persons'] if e['person_id']==pid)
 e.update(name=x['name'],name_zh=x.get('name_zh'),name_en=x['name_en'],wikidata_qid=x.get('wikidata_qid'),importance_level='high',notes='第三批公开资料研究已执行；证据截止时间、缺项和单源边界见人物collection_meta.notes。')
 lst['summary']['by_importance_level']=dict(collections.Counter(e['importance_level'] for e in lst['persons']));save(B/'person_list.json',lst)
 p['completed'].append(pid);p['remaining'].remove(pid);p['current']=p['remaining'][0] if p['remaining'] else None;p.update(last_updated='2026-11-14',status='running' if p['remaining'] else 'validating');save(P,p)
 print('Installed',pid,len(p['completed']),'/15')
elif action=='finalize':
 p=load(P);assert not p['remaining'] and len(p['completed'])==15
 before=load(O/'baseline.json');after=snap();assert before.keys()==after.keys()
 changed=[k for k in before if before[k]['sha256']!=after[k]['sha256']]
 assert all(pathlib.Path(k).stem in p['completed'] for k in changed)
 assert all(before[k]['id']==after[k]['id'] and before[k]['profile']==after[k]['profile'] for k in before)
 errors=[];links=[];summaries=[];strict=[];v=jsonschema.Draft7Validator(load(SC/'person_profile_schema.json'))
 idx=load(B/'persons/_index.json');entries={e['person_id']:e for e in idx['profiles']};ni=load(B/'_name_index.json');conflicts=[]
 for pid in p['completed']:
  x=load(B/'persons'/f'{pid}.json');errors += [f'{pid}: {e.message}' for e in v.iter_errors(x)]
  result=subprocess.run([sys.executable,str(SC/'scripts/validate_schema.py'),str(B),'--file',f'persons/{pid}.json','--strict'],capture_output=True,text=True,encoding='utf-8');assert 'Errors: 0' in result.stdout,(pid,result.stdout,result.stderr)
  strict.append({'person_id':pid,'stdout':result.stdout})
  for key,field,folder in [('work_experience','org_id','orgs'),('person_relationships','person_id','persons'),('family_members','person_id','persons')]:
   for row in x.get(key,[]):
    rid=row.get(field);assert rid!=''
    if rid:
     targets=list((R/'output').glob(f'[a-z][a-z]/20*/{folder}/{rid}.json'));assert targets
     t=load(targets[-1]);links.append({'person_id':pid,'field':key,'reference':row,'target_name':t.get('name') or t.get('basic_info',{}).get('name_original')})
  summaries.append({'person_id':pid,'name':x.get('name_zh',x['name']),'score':x['collection_meta']['completeness_score'],'sources':len(x['collection_meta']['quotes']),**{key:len(x.get(key,[])) for key in ['political_stances','major_achievements','person_relationships','family_members']}})
  e=entries.setdefault(pid,{'person_id':pid,'file':f'{pid}.json'});e.update(name_en=x['name_en'],name_zh=x.get('name_zh'),gender=x.get('gender'),current_title=next(iter(x.get('current_positions',[])),None),completeness_score=x['collection_meta']['completeness_score'],importance_level='high',wikidata_qid=x.get('wikidata_qid'))
  for name in [x['name'],x.get('name_zh'),x['name_en'],*x.get('aliases',[])]:
   if not name:continue
   if ni.get(name) not in [None,pid]:conflicts.append({'name':name,'existing':ni[name],'expected':pid});continue
   ni[name]=pid
 assert not errors,errors
 idx['profiles']=sorted(entries.values(),key=lambda x:x['person_id']);idx['metadata']['total_profiles']=len(entries)
 scores=[e['completeness_score'] for e in entries.values() if e.get('completeness_score') is not None]
 idx['completeness_summary']={'avg_score':round(sum(scores)/len(scores)),'high_completeness_gt80':sum(s>80 for s in scores),'medium_completeness_50_80':sum(50<=s<=80 for s in scores),'low_completeness_lt50':sum(s<50 for s in scores)};idx['by_importance_level']=dict(collections.Counter(e['importance_level'] for e in entries.values()))
 save(B/'persons/_index.json',idx);save(B/'_name_index.json',ni)
 lst=load(B/'person_list.json');lst['summary']['data_quality']={'with_person_id':sum(bool(e.get('person_id')) for e in lst['persons']),'with_wikidata_qid':sum(bool(e.get('wikidata_qid')) for e in lst['persons']),'without_person_id':sum(not e.get('person_id') for e in lst['persons'])};save(B/'person_list.json',lst)
 save(O/'validation.json',{'changed_profiles':changed,'schema_errors':errors,'avatar_changes':0,'profile_id_changes':0,'summaries':summaries,'links_for_manual_review':links,'index_conflicts':conflicts});save(O/'strict_validation.json',strict)
 lines=['# 台湾地区第三批15人研究（2026-11-14）','','已执行15/15。完成指公开资料研究、写入和校验结束，不等同所有事实多源核验或完整度达到85分。','','|人物|ID|政策|成就|人物关系|家庭|来源链接|完整度|','|---|---|---:|---:|---:|---:|---:|---:|']
 for s in summaries:lines.append('|'+s['name']+'|['+s['person_id']+']('+ (B/'persons'/f"{s['person_id']}.json").as_posix()+')|'+'|'.join(str(s[k]) for k in ['political_stances','major_achievements','person_relationships','family_members','sources','score'])+'|')
 lines+=['','仅记录可追溯公开事实；空字段及单源、不可读来源、现职截止时间逐档记录。成就区分团队贡献、计划与已实施成果；家庭仅公开实名与必要关系，不采私人财产或地址。所有原头像字段、画像ID和平台user_id保留。','','本轮15份真实JSON Schema及严格检查0错误；警告详情见复核记录。非本轮人物及组织画像与基线快照保持一致。未执行全库自动补链。逐条引用目标供人工核对，原文来源见各档collection_meta.quotes。','','备份与校验：tmp/tw_batch3_20261114/；候选依据：同目录selection.json。']
 lines+=['','本轮复用11份原有画像，另为杨金龙、庄翠云、陈世凯、林宜敬统一注册4个新身份（TW-PERSON-000534至000537）。注册前扫描全部output历史JSON/CSV/MD中的人物ID，未重用历史或业务引用编号；未给新人物下载头像，profile保持null。']
 lines+=['','本批合计政策主张44条、成就21条、人物关系5条、公开家庭关系8条。完整度52—74分；未达到85分的字段覆盖目标，未知日期、缺少证据的关系、账号等未为评分而补造。来源列为URL数量，不等同独立来源数量；同一原始发布者的多处转载只算一个来源。','','4位新增官员的主要任职组织尚无对应画像，组织ID保持null，保留机构名称供后续补建。谢龙介配偶李佳芬与韩国瑜配偶同名不同人，不得自动合并或按姓名补链。杨金龙没有个人社群账号的澄清来源已收录，不使用同名商人或冒名账号。','','严格检查保留15条TW中文姓名提示，此为规则误报警告；不修改正确中文姓名，不将其列为Schema错误。具体立法贡献、官方自陈及单源历史日期的局限见每份画像notes，未把竞选承诺或本人自述当独立绩效验证。']
 if conflicts:lines+=['','名称索引有同名冲突，保留既有映射，未自动覆盖：'+json.dumps(conflicts,ensure_ascii=False)]
 (R/'docs/tw_batch3_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 p.update(status='complete',current=None,completed_at='2026-11-14');save(P,p)
 print(json.dumps({'completed':15,'schema_errors':0,'changed_profiles':len(changed),'links_to_review':len(links),'name_conflicts':len(conflicts),'totals':{k:sum(s[k] for s in summaries) for k in ['political_stances','major_achievements','person_relationships','family_members']}},ensure_ascii=False))

"""Scoped install/check/report for the sixth 15-person research batch."""
import pathlib,sys,json,hashlib,shutil,collections,subprocess
import jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch6_20261115';S=R/'tmp/tw_batch6_enriched'
SC=R/'.agents/skills/country-org-collector';sys.path.insert(0,str(SC/'scripts'))
from atomic_write import load_json,save_json
O.mkdir(exist_ok=True);S.mkdir(exist_ok=True)
def load(p):return load_json(str(p))
def save(p,d):save_json(str(p),d)
def snap():
 return {p.relative_to(R).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'id':load(p).get('person_id') or load(p).get('org_id'),'profile':load(p).get('profile')} for folder in ['persons','orgs'] for p in (B/folder).glob('TW-*.json')}
P=B/'_batch6_progress.json';action=sys.argv[1]
if action=='init':
 assert not P.exists(),'Existing batch6 progress must be resumed rather than overwritten'
 selection=load(R/'tmp/tw_batch6_selection.json');people=selection if isinstance(selection,list) else selection['persons']
 assert len(people)==15;ids=[x['person_id'] for x in people];assert len(set(ids))==15
 earlier=set(load(B/'_supplement_progress.json')['completed']+load(B/'_batch2_progress.json')['completed']+load(B/'_batch3_progress.json')['completed']+load(B/'_batch4_progress.json')['completed']+load(B/'_batch5_progress.json')['completed']);assert not earlier.intersection(ids)
 for pid in ids:assert (B/'persons'/f'{pid}.json').exists(),pid
 save(O/'baseline.json',snap())
 for path in [B/'id_registry.json',B/'person_list.json',B/'persons/_index.json',B/'_name_index.json']:
  shutil.copy2(path,O/('persons_index_before.json' if path.parent.name=='persons' else path.stem+'_before.json'))
 save(P,{'phase':'P4_batch6_deep_research','started_at':'2026-11-15','status':'running','completed':[],'remaining':ids,'current':ids[0],'failed':[]})
 save(O/'selection.json',{'persons':people});(B/'.inflight').write_text('TW batch6 2026-11-15',encoding='utf-8')
 print('Initialized 15-person batch')
elif action=='install':
 pid=sys.argv[2];p=load(P);assert pid in p['remaining'];x=load(S/f'{pid}.json');old=load(B/'persons'/f'{pid}.json')
 assert x['person_id']==old['person_id']==pid
 if not x['name_en'].strip():assert '英文' in x['collection_meta'].get('notes',''),'Unknown English name needs explicit evidence-limit note'
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
 e.update(name=x['name'],name_zh=x.get('name_zh'),name_en=x['name_en'],wikidata_qid=x.get('wikidata_qid'),importance_level='high',notes='第六批公开资料研究已执行；证据截止时间、缺项和单源边界见人物collection_meta.notes。')
 lst['summary']['by_importance_level']=dict(collections.Counter(e['importance_level'] for e in lst['persons']));save(B/'person_list.json',lst)
 p['completed'].append(pid);p['remaining'].remove(pid);p['current']=p['remaining'][0] if p['remaining'] else None;p.update(last_updated='2026-11-16',status='running' if p['remaining'] else 'validating');save(P,p)
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
  result=subprocess.run([sys.executable,str(SC/'scripts/validate_schema.py'),str(B),'--file',f'persons/{pid}.json','--strict'],capture_output=True,text=True,encoding='utf-8')
  tool_errors=[line.strip() for line in result.stdout.splitlines() if line.strip().startswith('ERR:')]
  known_blank_english=not x['name_en'].strip() and '英文' in x['collection_meta'].get('notes','')
  exceptions=tool_errors if known_blank_english and tool_errors==['ERR: missing required field: name_en'] else []
  assert not [e for e in tool_errors if e not in exceptions],(pid,result.stdout,result.stderr)
  assert 'Files checked: 1' in result.stdout,(pid,result.stdout,result.stderr)
  strict.append({'person_id':pid,'stdout':result.stdout,'documented_exceptions':exceptions})
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
 lines=['# 台湾地区第六批15人研究（2026-11-15至2026-11-16）','','已执行15/15。完成指公开资料研究、写入和校验结束，不等同所有事实多源核验或完整度达到85分。各档采集日期及跨日补核说明见collection_meta。','','|人物|ID|政策|成就|人物关系|家庭|来源链接|完整度|','|---|---|---:|---:|---:|---:|---:|---:|']
 for s in summaries:lines.append('|'+s['name']+'|['+s['person_id']+']('+ (B/'persons'/f"{s['person_id']}.json").as_posix()+')|'+'|'.join(str(s[k]) for k in ['political_stances','major_achievements','person_relationships','family_members','sources','score'])+'|')
 lines+=['','仅记录可追溯公开事实；空字段及单源、不可读来源、现职截止时间逐档记录。成就区分团队贡献、计划与已实施成果；家庭仅公开实名与必要关系，不采私人财产或地址。所有原头像字段、画像ID和平台user_id保留。','','本轮15份真实JSON Schema及严格检查0错误；警告详情见复核记录。非本轮人物及组织画像与基线快照保持一致。未执行全库自动补链。逐条引用目标供人工核对，原文来源见各档collection_meta.quotes。','','备份与校验：tmp/tw_batch6_20261115/；候选依据：同目录selection.json。']
 totals={k:sum(t[k] for t in summaries) for k in ['political_stances','major_achievements','person_relationships','family_members']}
 registration=load(O/'new_id_registration.json') if (O/'new_id_registration.json').exists() else {'created':[]}
 created=registration['created']
 lines+=['',f'本批合计政策主张{totals["political_stances"]}条、成就{totals["major_achievements"]}条、人物关系{totals["person_relationships"]}条、公开家庭关系{totals["family_members"]}条。',f'复用{15-len(created)}份已有画像，新注册{len(created)}份人物身份；新增者头像保持null。新ID清单：'+', '.join(e['person_id']+' '+e['name'] for e in created),'来源列是链接数量，不等同独立来源数量；同源转载不重复算独立核实。未知关系ID保持null，未按姓名自动补链。','本批严格检查中文姓名提示详见strict_validation.json；不修改正确中文姓名。完整度是字段覆盖指标，尚有缺项及单源边界，不等同全部事实已核实。']
 lines=[line.replace('本轮15份真实JSON Schema及严格检查0错误','本轮15份真实JSON Schema均通过，严格工具结果及已知限制见下文') for line in lines]
 exception_count=sum(bool(e['documented_exceptions']) for e in strict)
 if exception_count:lines += ['',f'严格工具有{exception_count}份档案仅因未核英文名留空而报必填错误；真实JSON Schema允许空字符串，已逐档注明证据限制，未编造译名。除此之外严格工具错误为0；逐项输出保留在strict_validation.json。']
 else:lines += ['','15份档案严格工具检查0错误；中文姓名等提示保留在strict_validation.json，未为消除提示修改正确姓名。']
 lines += [f'完整度范围为{min(s["score"] for s in summaries)}—{max(s["score"] for s in summaries)}分；未以猜测补足85分目标。部分政策、成果、家庭及人物关系仍有缺项。']
 if conflicts:lines+=['','名称索引有同名冲突，保留既有映射，未自动覆盖：'+json.dumps(conflicts,ensure_ascii=False)]
 (R/'docs/tw_batch6_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 p.update(status='complete',current=None,completed_at='2026-11-16');save(P,p)
 print(json.dumps({'completed':15,'schema_errors':0,'changed_profiles':len(changed),'links_to_review':len(links),'name_conflicts':len(conflicts),'totals':{k:sum(s[k] for s in summaries) for k in ['political_stances','major_achievements','person_relationships','family_members']}},ensure_ascii=False))

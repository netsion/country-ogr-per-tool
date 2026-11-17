"""Apply pre-reviewed account changes with rollback, schema-delta and scope guards."""
from social_xlsx_common import *
import hashlib,copy,shutil,jsonschema
plan=load(O/'execution_plan.json');source=load(O/'source.json')
assert hashlib.sha256(pathlib.Path(source['path']).read_bytes()).hexdigest()==source['sha256']
audit=O/'applied.json';assert not audit.exists(),'Do not apply twice'
SC=R/'.agents/skills/country-org-collector';schema=load(SC/'person_profile_schema.json');validator=jsonschema.Draft7Validator(schema)
accountv=jsonschema.Draft7Validator({'$defs':schema['$defs'],**schema['$defs']['social_account']})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def errors(d):return sorted((str(list(e.absolute_path)),e.message) for e in validator.iter_errors(d))
paths=list((B/'persons').glob('TW-PERSON-*.json'))+list((B/'orgs').glob('TW-*.json'))+[B/n for n in ['id_registry.json','_name_index.json','person_list.json','persons/_index.json']]
baseline={str(p.relative_to(R)):sha(p) for p in paths};before={};preexisting=[]
for pid,c in plan['profiles'].items():
 p=B/'persons'/f'{pid}.json';assert sha(p)==c['before_sha256'],pid
 old=load(p);new=c['after'];before[pid]=old
 assert {k:v for k,v in old.items() if k!='social_accounts'}=={k:v for k,v in new.items() if k!='social_accounts'}
 assert new['person_id']==pid and new.get('profile')==old.get('profile')
 olderrors=errors(old);newerrors=errors(new);assert not set(newerrors)-set(olderrors),(pid,newerrors)
 if olderrors:preexisting.append({'person_id':pid,'errors_unchanged':olderrors})
 for i,a in enumerate(new.get('social_accounts',[])):
  if i>=len(old.get('social_accounts',[])) or a!=old['social_accounts'][i]:accountv.validate(a)
 for i,a in enumerate(old.get('social_accounts',[])):
  n=new['social_accounts'][i]
  for k,v in a.items():
   if k in ['source_note'] or not v:continue
   assert n.get(k)==v,(pid,i,k)
# A previously unowned ID must not become shared across two identities.
def owner_map(updated):
 result=collections.defaultdict(set)
 for p in (B/'persons').glob('TW-PERSON-*.json'):
  d=updated.get(p.stem) or load(p)
  for a in d.get('social_accounts',[]):
   if a.get('user_id'):result[(a.get('platform'),bare(a['user_id']))].add(d['person_id'])
 return result
oldowners=owner_map({});newowners=owner_map({pid:c['after'] for pid,c in plan['profiles'].items()})
assert not [k for k,v in newowners.items() if len(v)>1 and v!=oldowners.get(k,set())],'New cross-person user ID collision'
backup=O/'persons_before';backup.mkdir(exist_ok=True)
for pid,c in plan['profiles'].items():
 p=B/'persons'/f'{pid}.json';assert not (backup/p.name).exists();shutil.copy2(p,backup/p.name)
sys.path.insert(0,str(SC/'scripts'));from atomic_write import save_json
for pid,c in plan['profiles'].items():save_json(str(B/'persons'/f'{pid}.json'),c['after'])
changed=[]
for path,digest in baseline.items():
 p=R/path
 if sha(p)!=digest:changed.append(path);assert p.parent==B/'persons' and p.stem in plan['profiles']
assert len(changed)==len(plan['profiles'])
for pid,c in plan['profiles'].items():assert load(B/'persons'/f'{pid}.json')==c['after']
assert hashlib.sha256(pathlib.Path(source['path']).read_bytes()).hexdigest()==source['sha256']
result={'changed_people':len(changed),'actions':dict(collections.Counter(x['action'] for x in plan['actions'])),'fields_filled':plan['fields_filled'],'deferred':len(plan['deferred']),'id_conflicts':len(plan['conflicts']),'new_schema_errors':0,'changed_social_accounts_schema_errors':0,'profile_id_changes':0,'avatar_changes':0,'existing_nonempty_fields_overwritten':0,'workbook_unchanged':True,'other_profiles_and_metadata_unchanged':True,'preexisting_profile_schema_issues':preexisting,'changed_files':changed}
audit.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
report=R/'docs/tw-social-xlsx-supplement-20261116.md'
lines=['# 台湾人物社交账号补充（2026-11-16）','',f"已分析用户提供的29个工作表，与现有568份台湾人物画像对照。本次修改{len(changed)}人，新增32个账号，给24条既有账号补齐空字段（USER-ID 24处、用户名23处）。",'', '仅修改social_accounts。原人物ID、头像、原非空账号字段均保留；组织画像、注册表、索引和原Excel未修改。完整度分数未重算，避免更改本次范围以外字段。','', '新增依据分为可读公开外链交叉确认，以及来源表实名与既有本人账号用户名一致；不将后者称为逐平台认证，也不保证历史账号当前仍存续。逐条依据和源表行号写入source_note。', '', '同名艺人吴宗宪、陈信宏未按姓名强行补入；基金会、纪念账号、空YouTube链接、照片页不直接作为人物账号。Facebook PAGE-ID未混入USER-ID；15处ID差异不覆盖现值。', '', '曹兴诚Threads经节目说明明确外链确认；X未获得相同证明，暂缓。王世坚既有YouTube归属警示保留。', '', '## 本次修改', '', '|人物|ID|新增账号|补空账号|','|---|---|---:|---:|']
for pid,c in plan['profiles'].items():
 acts=[x for x in plan['actions'] if x['person_id']==pid];d=c['after'];lines.append(f"|{d.get('name_zh',d['name'])}|{pid}|{sum(x['action']=='add_account' for x in acts)}|{sum(x['action']=='fill_missing_fields' for x in acts)}|")
lines+=['','## 新增账号及依据','','|人物|平台|账号|依据|','|---|---|---|---|']
for x in plan['actions']:
 if x['action']=='add_account':lines.append(f"|{x['name']}|{x['platform']}|{x['url']}|{x['source']}；{x['locations']}|")
lines+=['','## 待核项','','下列89项暂未写入，不代表确定错误。仅姓名对应、同平台其他账号、同名人物等情况需要进一步原文核验。','','|人物|账号|原因|来源位置|','|---|---|---|---|']
for x in plan['deferred']:lines.append(f"|{x['name']}|{x['url']}|{x['reason']}|{x['locations']}|")
lines+=['','## ID差异','','|人物ID|账号|类型|保留说明|','|---|---|---|---|']
for x in plan['conflicts']:lines.append(f"|{x['person_id']}|{x['url']}|{x['reason']}|{json.dumps({k:v for k,v in x.items() if k not in ['person_id','url','reason']},ensure_ascii=False).replace('|','/')}|")
lines+=['','变更子项Schema检查通过，未引入新的全档Schema错误；旧画像已有问题仅记录未修复。备份、执行清单、源表提取及校验位于tmp/social_xlsx_20261116/。']
report.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['preexisting_profile_schema_issues','changed_files']},ensure_ascii=False))

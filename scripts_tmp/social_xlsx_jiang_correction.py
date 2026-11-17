"""Correct the over-conservative deferral of five explicitly named Chiang accounts."""
from social_xlsx_common import *
import copy,hashlib,shutil,jsonschema
pid='TW-PERSON-000526';p=B/'persons'/f'{pid}.json';old=load(p);assert old['name'] in ['蔣萬安','蒋万安'] and old.get('social_accounts',[])==[]
source=load(O/'source.json');assert hashlib.sha256(pathlib.Path(source['path']).read_bytes()).hexdigest()==source['sha256']
rows=next(s for s in load(O/'workbook_raw.json') if s['sheet']=='2026-03-16')['rows'];groups=collections.defaultdict(list)
for row in rows:
 c={x['col']:x['value'] for x in row['cells']}
 if c.get(2)=='蒋万安':groups[{'x':'twitter'}.get(c[3],c[3])].append((row['row'],c))
assert set(groups)=={'facebook','instagram','threads','youtube','twitter'} and sum(map(len,groups.values()))==10
new=copy.deepcopy(old);accounts=[]
for plat,entries in groups.items():
 urls={urlkey(c[4]) for _,c in entries};ids={c[5] for _,c in entries};assert len(urls)==len(ids)==1
 r,c=entries[0];u=uidval(plat,next(iter(ids)));assert u
 href=c[4];key=urlkey(href);external='https://ja.wikipedia.org/wiki/蔣万安#外部リンク' if plat=='twitter' else 'https://zh.wikipedia.org/wiki/蔣萬安#外部連結'
 note='用户提供社交.xlsx，2026-03-16：'+','.join(str(i) for i,_ in entries)+'行。实名、链接及USER-ID在重复行一致；外链交叉：'+external+'。平台正文受限，未声称实时登录认证。'
 if plat=='facebook':note+='原表USER-ID='+c[5]+'；PAGE-ID='+c[6]+'，百科Facebook外链为该PAGE-ID，未将PAGE-ID写入user_id。'
 a={'platform':plat,'account_name':'蒋万安','url':href,'user_id':u,'source':codes[plat],'source_note':note}
 if not key[1].startswith('id:'):a['username']=key[1].lstrip('@')
 accounts.append(a)
new['social_accounts']=accounts
schema=load(R/'.agents/skills/country-org-collector/person_profile_schema.json');v=jsonschema.Draft7Validator(schema);av=jsonschema.Draft7Validator({'$defs':schema['$defs'],**schema['$defs']['social_account']})
for a in accounts:av.validate(a)
err=lambda d:{(str(list(e.absolute_path)),e.message) for e in v.iter_errors(d)}
assert not err(new)-err(old)
assert {k:x for k,x in old.items() if k!='social_accounts'}=={k:x for k,x in new.items() if k!='social_accounts'}
for f in (B/'persons').glob('TW-PERSON-*.json'):
 if f.stem==pid:continue
 for a in load(f).get('social_accounts',[]):
  assert not any(a.get('platform')==n['platform'] and a.get('user_id') and bare(a['user_id'])==bare(n['user_id']) for n in accounts),'ID owned by another person'
paths=list((B/'persons').glob('TW-PERSON-*.json'))+list((B/'orgs').glob('TW-*.json'))+[B/n for n in ['id_registry.json','_name_index.json','person_list.json','persons/_index.json']]
snapshot={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths}
backup=O/'jiang_correction_before.json';assert not backup.exists();shutil.copy2(p,backup)
sys.path.insert(0,str(R/'.agents/skills/country-org-collector/scripts'));from atomic_write import save_json
save_json(str(p),new)
assert load(p)==new
assert [k for k,h in snapshot.items() if hashlib.sha256(pathlib.Path(k).read_bytes()).hexdigest()!=h]==[str(p)]
assert hashlib.sha256(pathlib.Path(source['path']).read_bytes()).hexdigest()==source['sha256']
review=load(O/'execution_plan.json');resolved=[d for d in review['deferred'] if d['person_id']==pid];assert len(resolved)==5
correction={'person_id':pid,'accounts_added':accounts,'resolved_deferred':resolved,'reason':'原表已明确列出本人及ID，上轮因无既有社交锚点而停在待核；本轮补读外链后完成','schema_new_errors':0,'only_person_file_changed':True,'avatar_changes':0,'profile_id_changes':0,'source_workbook_unchanged':True}
(O/'jiang_correction_applied.json').write_text(json.dumps(correction,ensure_ascii=False,indent=2),encoding='utf-8')
cumulative={'changed_people':35,'new_accounts':37,'existing_accounts_filled':24,'user_ids_filled':24,'usernames_filled':23,'remaining_review_items':84,'id_differences':15,'history':['applied.json','jiang_correction_applied.json']}
(O/'cumulative.json').write_text(json.dumps(cumulative,ensure_ascii=False,indent=2),encoding='utf-8')
report=R/'docs/tw-social-xlsx-supplement-20261116.md';s=report.read_text(encoding='utf-8');s='\n'.join(line for line in s.splitlines() if not line.startswith('|蒋万安|'))+'\n'
s=s.replace('本次修改34人，新增32个账号','本次修改35人，新增37个账号').replace('下列89项暂未写入','下列84项暂未写入')
s=s.replace('\n## 新增账号及依据','\n|蒋万安|TW-PERSON-000526|5|0|\n\n## 新增账号及依据')
extra='\n'.join(f"|蒋万安|{a['platform']}|{a['url']}|2026-03-16实名及ID；{a['source_note'].split('外链交叉：')[1].split('。')[0]}|" for a in accounts)
s=s.replace('\n## 待核项','\n'+extra+'\n\n## 待核项')
s+='\n蒋万安补核更正：2026-03-16中有10行、去重后5个平台，上轮全部暂缓并非表内缺失。已补入Facebook、Instagram、Threads、YouTube和X；原初轮执行记录保留，本次补充见jiang_correction_applied.json，最新合计见cumulative.json。\n'
report.write_text(s,encoding='utf-8')
print(json.dumps(cumulative,ensure_ascii=False))

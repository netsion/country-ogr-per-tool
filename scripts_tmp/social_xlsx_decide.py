"""Conservative review: preserve existing identities; separate account and ID uncertainty."""
from social_xlsx_common import *
import copy,hashlib
P=load(O/'proposals.json');profiles={p.stem:load(p) for p in (B/'persons').glob('TW-PERSON-*.json')}
verified={}
def seed(pid,urls,source):
 for u in urls:verified[(pid,urlkey(u))]=source
seed('TW-PERSON-000527',['https://www.facebook.com/pumashen','https://www.instagram.com/pumashen/','https://www.youtube.com/@PumaShen','https://x.com/pumashen'],'https://hypelink.app/@pumashen')
seed('TW-PERSON-000561',['https://www.facebook.com/jackylone','https://www.instagram.com/jackylone0329/'],'https://jackylone.com.tw/【青年節-】/')
seed('TW-PERSON-000564',['https://www.facebook.com/seanliao76/','https://www.instagram.com/seanliao.24/'],'https://zh.wikipedia.org/wiki/廖偉翔#外部連結')
seed('TW-PERSON-000566',['https://www.facebook.com/allenihelp'],'https://zh.wikipedia.org/wiki/張智倫#外部連結')
seed('TW-PERSON-000565',['https://www.facebook.com/CCCHsinchu/'],'https://news.ttv.com.tw/news/11301060002500W/amp')
seed('TW-PERSON-000551',['https://www.facebook.com/HsuChiaoHsin/','https://www.instagram.com/chiaohsinhsu/','https://www.threads.com/@chiaohsinhsu'],'https://zh.wikipedia.org/wiki/徐巧芯#外部連結')
seed('TW-PERSON-000290',['https://www.threads.net/@babujushi'],'https://podcasts.apple.com/us/podcast/知定講堂-曹興誠/id1709466312')
groups=collections.defaultdict(list)
for r in P:groups[(r['person_id'],tuple(r['key']))].append(r)
actions=[];deferred=[];conflicts=[];after={};fields=collections.Counter()
uidowners=collections.defaultdict(set)
for pid,d in profiles.items():
 for a in d.get('social_accounts',[]):
  if a.get('user_id'):uidowners[(a.get('platform'),bare(a['user_id']))].add(pid)
def uidchoice(rs,plat,pid):
 values=set();wrong=[]
 for r in rs:
  u=r.get('raw_user_id')
  if not u:continue
  if '#' in u and not u.startswith('fb#RHINO#' if plat=='facebook' else plat+'#'):wrong.append(u);continue
  values.add(bare(u))
 if len(values)>1 or wrong:
  conflicts.append({'person_id':pid,'platform':plat,'url':rs[0]['url'],'reason':'source_id_conflict_or_platform_mismatch','ids':sorted(values),'wrong_platform_ids':wrong,'locations':[(r['sheet'],r['row']) for r in rs]});return None
 if not values:return None
 value=next(iter(values))
 if uidowners.get((plat,value),set())-{pid}:
  conflicts.append({'person_id':pid,'platform':plat,'url':rs[0]['url'],'reason':'id_already_owned_by_other_person','other_people':sorted(uidowners[(plat,value)]-{pid})});return None
 return uidval(plat,value)
def locs(rs):return '；'.join(f"{r['sheet']}!第{r['row']}行" for r in sorted(rs,key=lambda x:(x['sheet'],x['row']))[-4:])
for (pid,key),rs in groups.items():
 old=profiles[pid];r=rs[0];plat=r['platform'];inds=sorted({i for x in rs for i in x['existing_indices']});source=verified.get((pid,key));reason=None
 if pid in ['TW-PERSON-000349','TW-PERSON-000460']:
  deferred.append({'person_id':pid,'name':r['person_name'],'url':r['url'],'reason':'同名艺人画像，表中账号未证明属于该人','locations':locs(rs)});continue
 if len(inds)>1:
  deferred.append({'person_id':pid,'name':r['person_name'],'url':r['url'],'reason':'命中多条既有账号，需人工消歧','locations':locs(rs)});continue
 if not inds:
  if any(t in r['url'].casefold() for t in ['ma19_foundation','drdemocracy']):reason='基金会或纪念账号，不作为人物个人账号直接加入'
  elif plat=='twitter' and not source:reason='新增X账号未取得本人明确外链，不仅凭跨平台同用户名认定'
  elif pid=='TW-PERSON-000290' and plat=='threads' and not source:reason='本人公开唯一账号清单未列此平台，官方归属待核'
  elif source:reason=None
  elif any(a.get('platform')==plat for a in old.get('social_accounts',[])):reason='同平台已有其他账号，尚未确认别名、改名或新增账号关系'
  else:
   handles={urlkey(a.get('url',''))[1].lstrip('@') for a in old.get('social_accounts',[]) if urlkey(a.get('url','')) and not urlkey(a.get('url',''))[1].startswith('id:') and not re.search('待核|归属.*疑',a.get('source_note',''))}
   has_named=any(x.get('name') and norm(x['name']) in {norm(old.get('name','')),norm(old.get('name_zh',''))} for x in rs)
   if not (has_named and key[1].lstrip('@') in handles):reason='仅姓名对应，缺少已核外链或既有账号用户名交叉佐证'
  if reason:
   deferred.append({'person_id':pid,'name':r['person_name'],'platform':plat,'url':r['url'],'reason':reason,'locations':locs(rs)});continue
 d=after.setdefault(pid,copy.deepcopy(old));note='用户提供社交.xlsx：'+locs(rs)+'。'
 pages=sorted({x['raw_page_id'] for x in rs if x.get('raw_page_id')})
 if pages:note+='原表PAGE-ID='+','.join(pages)+'，未作为USER-ID。'
 if source:note+='归属交叉来源：'+source+'；平台实时认证及存续状态未保证。'
 elif not inds:note+='表内实名与既有本人账号用户名一致；未逐平台实时认证。'
 else:note+='与既有账号URL或ID匹配，仅补空字段。'
 u=uidchoice(rs,plat,pid)
 if inds:
  idx=inds[0];a=d['social_accounts'][idx]
  if re.search('待核|归属.*疑|官方性存在疑',a.get('source_note','')):
   deferred.append({'person_id':pid,'name':r['person_name'],'url':r['url'],'reason':'原账号官方归属已标疑，未以来源表覆盖','locations':locs(rs)});continue
  changed=[]
  if u and a.get('user_id') and bare(u)!=bare(a['user_id']):conflicts.append({'person_id':pid,'url':r['url'],'reason':'existing_user_id_preserved','existing':a['user_id'],'source_id':u})
  if u and not a.get('user_id'):a['user_id']=u;changed.append('user_id')
  if not a.get('username') and not key[1].startswith('id:') and '/' not in key[1]:a['username']=key[1].lstrip('@');changed.append('username')
  if not changed:continue
  a['source_note']=(a.get('source_note','')+' '+note).strip();fields.update(changed)
  actions.append({'person_id':pid,'name':r['person_name'],'action':'fill_missing_fields','index':idx,'url':a['url'],'fields':changed,'locations':locs(rs)})
 else:
  # Keep source URL; strip tracking for new accounts only.
  q=urllib.parse.urlsplit(r['url']);url=urllib.parse.urlunsplit(('https',q.netloc,q.path,q.query if q.path.endswith('profile.php') else '', ''))
  a={'platform':plat,'account_name':r['person_name'],'url':url,'source':codes[plat],'source_note':note}
  if u:a['user_id']=u
  if not key[1].startswith('id:') and '/' not in key[1]:a['username']=key[1].lstrip('@')
  d.setdefault('social_accounts',[]).append(a);actions.append({'person_id':pid,'name':r['person_name'],'action':'add_account','platform':plat,'url':url,'source':source or '用户表与既有账号用户名交叉','locations':locs(rs)})
changed={pid:d for pid,d in after.items() if d!=profiles[pid]}
for pid,d in changed.items():
 old=profiles[pid]
 assert old.get('profile')==d.get('profile') and old['person_id']==d['person_id']
 assert {k:v for k,v in old.items() if k!='social_accounts'}=={k:v for k,v in d.items() if k!='social_accounts'}
 for i,a in enumerate(old.get('social_accounts',[])):
  b=d['social_accounts'][i]
  assert all(a.get(k)==b.get(k) for k in ['url','platform','user_id'] if a.get(k))
plan={'source':'C:/Users/R4314/Desktop/社交.xlsx','date':'2026-11-16','actions':actions,'deferred':deferred,'conflicts':conflicts,'fields_filled':dict(fields),'profiles':{pid:{'before_sha256':hashlib.sha256((B/'persons'/f'{pid}.json').read_bytes()).hexdigest(),'after':d} for pid,d in changed.items()}}
(O/'execution_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'changed_people':len(changed),'actions':dict(collections.Counter(x['action'] for x in actions)),'fields_filled':dict(fields),'deferred_accounts':len(deferred),'id_conflicts':len(conflicts),'new_accounts':[{'name':x['name'],'url':x['url']} for x in actions if x['action']=='add_account']},ensure_ascii=False))

"""Supplement only blank identity metadata of already collected accounts, from exact source URLs."""
import pathlib,json,copy,hashlib,collections,sys
import social_xlsx_common as soc
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch8_20261117'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
progress=load(B/'_batch8_progress.json');assert len(progress['completed'])==15 and not progress['remaining']
log=O/'social_id_supplement.json';assert not log.exists()
records=load(R/'tmp/social_xlsx_20261116/records.json');changes=[];conflicts=[];files={};owners=collections.defaultdict(set)
for p in (B/'persons').glob('TW-PERSON-*.json'):
 for a in load(p).get('social_accounts',[]):
  if a.get('user_id'):owners[(a.get('platform'),soc.bare(a['user_id']))].add(p.stem)
for pid in progress['completed']:
 p=B/'persons'/f'{pid}.json';old=load(p);new=copy.deepcopy(old);original=load(O/'persons_before'/f'{pid}.json')
 for i,a in enumerate(new.get('social_accounts',[])):
  key=soc.urlkey(a.get('url',''))
  if not key:continue
  hits=[r for r in records if tuple(r['key'])==key or (key[1].startswith('id:') and r['platform']==key[0] and r.get('raw_user_id') and soc.bare(r['raw_user_id'])==key[1][3:])]
  values=set();invalid=[]
  for h in hits:
   u=h.get('raw_user_id')
   if not u:continue
   prefix='fb#RHINO#' if key[0]=='facebook' else key[0]+'#'
   if '#' in u and not u.startswith(prefix):invalid.append(u)
   else:values.add(soc.bare(u))
  if len(values)>1 or invalid:
   conflicts.append({'person_id':pid,'index':i,'url':a['url'],'source_ids':sorted(values),'wrong_platform_prefix':invalid});continue
  if not values:continue
  u=next(iter(values));other=owners.get((key[0],u),set())-{pid}
  if other:conflicts.append({'person_id':pid,'index':i,'url':a['url'],'reason':'ID already belongs to other profile','other':sorted(other)});continue
  prior=a.get('user_id')
  if prior and soc.bare(prior)==u:continue
  if prior:
   protected=any(b.get('platform')==a.get('platform') and b.get('url')==a.get('url') and b.get('user_id') for b in original.get('social_accounts',[]))
   pages={soc.bare(h['raw_page_id']) for h in hits if h.get('raw_page_id')}
   if protected or soc.bare(prior) not in pages:
    conflicts.append({'person_id':pid,'index':i,'url':a['url'],'existing':prior,'source_id':u});continue
  a['user_id']=soc.uidval(key[0],u)
  locations=sorted({f"{h['sheet']}!第{h['row']}行" for h in hits})
  a['source_note']=(a.get('source_note','')+' 用户提供社交.xlsx同一账号URL/频道ID匹配，USER-ID来源：'+'；'.join(locations[-4:])+'；历史来源值，不代表实时平台认证，未用PAGE-ID替代。').strip()
  if prior:a['source_note']+=' 主会话确认本批草稿将PAGE-ID混入USER-ID，已据明确原列纠正；未修改批次开始前的既有账号ID。'
  changes.append({'person_id':pid,'index':i,'url':a['url'],'old_id':prior,'new_id':a['user_id'],'source_locations':locations})
  owners[(key[0],u)].add(pid)
 if new!=old:files[pid]=(old,new)
sys.path.insert(0,str(R/'.agents/skills/country-org-collector/scripts'));from atomic_write import save_json
backup=O/'before_social_id_supplement';backup.mkdir(exist_ok=True)
for pid,(old,new) in files.items():
 assert old.get('profile')==new.get('profile') and old['person_id']==new['person_id']
 assert {k:v for k,v in old.items() if k!='social_accounts'}=={k:v for k,v in new.items() if k!='social_accounts'}
 save_json(str(backup/f'{pid}.json'),old);save_json(str(B/'persons'/f'{pid}.json'),new);save_json(str(R/'tmp/tw_batch8_enriched'/f'{pid}.json'),new)
save_json(str(log),{'changes':changes,'conflicts':conflicts})
print(json.dumps({'filled_user_ids':sum(c['old_id'] is None for c in changes),'corrected_new_draft_page_ids':sum(c['old_id'] is not None for c in changes),'profiles':len(files),'conflicts_held':len(conflicts)},ensure_ascii=False))

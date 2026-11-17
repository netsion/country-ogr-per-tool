"""Read-only cross-person account collision recall for batch seven."""
import pathlib,json,collections
import social_xlsx_common as soc
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch8_20261117'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
selected=set(load(B/'_batch8_progress.json')['completed']);urls=collections.defaultdict(list);uids=collections.defaultdict(list);wrong=[]
for p in (B/'persons').glob('TW-PERSON-*.json'):
 for i,a in enumerate(load(p).get('social_accounts',[])):
  item={'person_id':p.stem,'index':i,'url':a.get('url'),'user_id':a.get('user_id')}
  key=soc.urlkey(a.get('url',''))
  if key:urls[key].append(item)
  if a.get('user_id'):
   u=str(a['user_id']);uids[(a['platform'],soc.bare(u))].append(item)
   prefix='fb#RHINO#' if a['platform']=='facebook' else a['platform']+'#'
   if p.stem in selected and '#' in u and not u.startswith(prefix):wrong.append(item)
out={'url_collisions':[v for v in urls.values() if len({x['person_id'] for x in v})>1 and any(x['person_id'] in selected for x in v)],'user_id_collisions':[v for v in uids.values() if len({x['person_id'] for x in v})>1 and any(x['person_id'] in selected for x in v)],'wrong_platform_prefix':wrong}
(O/'social_identity_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))

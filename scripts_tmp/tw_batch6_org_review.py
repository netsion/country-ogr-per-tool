"""Read-only recall of same-dataset exact primary-name org profiles for null links."""
import pathlib,json,re,unicodedata,collections
import zhconv
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch6_20261115'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def norm(s):return re.sub(r'\s+','',zhconv.convert(unicodedata.normalize('NFKC',s),'zh-cn')).lower()
index=collections.defaultdict(dict)
for f in (B/'orgs').glob('TW-*.json'):
 d=load(f);bi=d['basic_info']
 for n in {bi.get('name_original'),bi.get('name_zh'),bi.get('name_en')}:
  if n:index[norm(n)][d['org_id']]={'id':d['org_id'],'info':bi}
out=[]
for pid in load(B/'_batch6_progress.json')['completed']:
 for i,row in enumerate(load(B/'persons'/f'{pid}.json').get('work_experience',[])):
  if row.get('org_id'):continue
  parts=[p.strip() for p in re.split('[()（）]',row['organization']) if p.strip()]
  hits={k:v for part in parts for k,v in index.get(norm(part),{}).items()}
  if hits:out.append({'person_id':pid,'index':i,'reference':row,'candidates':list(hits.values())})
(O/'null_org_candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'person_id':x['person_id'],'index':x['index'],'organization':x['reference']['organization'],'candidates':[{'id':c['id'],'name':c['info'].get('name_original'),'hq':c['info'].get('hq_country_iso3')} for c in x['candidates']]} for x in out],ensure_ascii=False))

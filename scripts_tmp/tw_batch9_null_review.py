"""Read-only exact-name recall for unknown people links; never autolink."""
import pathlib,json,re,collections
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
index=collections.defaultdict(list)
for f in (B/'persons').glob('TW-*.json'):
 d=load(f)
 for n in {d.get('name'),d.get('name_zh'),d.get('name_en'),*d.get('aliases',[])}:
  if n:index[n].append({'id':d['person_id'],'name':d['name'],'positions':d.get('current_positions',[])})
out=[]
for pid in load(B/'_batch9_progress.json')['completed']:
 d=load(B/'persons'/f'{pid}.json')
 for field,key in [('person_relationships','person_name'),('family_members','name')]:
  for row in d.get(field,[]):
   if row.get('person_id'):continue
   name=row[key];parts=[p.strip() for p in re.split(r'[()（）]',name) if p.strip()]
   hits={x['id']:x for p in parts for x in index.get(p,[]) if x['id']!=pid}
   if hits:out.append({'source':pid,'field':field,'reference':row,'candidates':list(hits.values())})
(R/'tmp/tw_batch9_20261117/null_person_candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))

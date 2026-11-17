"""Retain evidence limits using the permitted nested-field contract."""
import pathlib,json
p=pathlib.Path(__file__).resolve().parents[1]/'tmp/tw_batch9_enriched/TW-PERSON-000145.json'
d=json.loads(p.read_text(encoding='utf-8'));known={q['url'] for q in d['collection_meta']['quotes']}
for r in d['person_relationships']:
 if r.get('source'):
  u=r.pop('source');assert u in known;r['description']+=' 来源：'+u
for e in d['education']:
 if e.get('note'):
  n=e.pop('note');d['collection_meta']['notes']+=' 学历限制：'+n
  e['field']='教育（本人称学分、时数未符台湾教育部采认标准）'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

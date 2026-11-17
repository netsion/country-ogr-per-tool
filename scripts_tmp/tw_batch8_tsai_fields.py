"""Keep family provenance in quotes/notes using the collection field contract."""
import pathlib,json
p=pathlib.Path(__file__).resolve().parents[1]/'tmp/tw_batch8_enriched/TW-PERSON-000598.json'
d=json.loads(p.read_text(encoding='utf-8'));f=d['family_members'][0]
assert f['name']=='黃玉廷'
if 'source' in f:
 urls=f.pop('source');assert all(u in {q['url'] for q in d['collection_meta']['quotes']} for u in urls.split('；'))
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

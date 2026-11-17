from pathlib import Path
import json,collections
R=Path(__file__).resolve().parents[1];p=R/'tmp/tw_batch7_selection.json';d=json.loads(p.read_text(encoding='utf-8'))
assert len(d['persons'])==15
for e in d['persons']:
 assert e.get('official_url') or e.get('independent_source_url'),e['name']
 if e['name']=='吳宗憲':assert e.get('distinct_identity_from')==['TW-PERSON-000349']
d['registry_encoding_review']='主会话UTF-8解析及Unicode转义核验通过；先前疑似乱码为终端编码显示问题，不据此认定底表损坏。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'name':e['name'],'id':e['person_id']} for e in d['persons']],ensure_ascii=False))

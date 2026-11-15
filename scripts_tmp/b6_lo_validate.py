import json,pathlib,jsonschema
r=pathlib.Path('.');p=r/'tmp/tw_batch6_enriched/TW-PERSON-000563.json';d=json.loads(p.read_text(encoding='utf-8'))
for e in d['education']:
 if e.get('degree') is None: e.pop('degree')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');jsonschema.validate(d,json.loads((r/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8-sig')));print('PASS')

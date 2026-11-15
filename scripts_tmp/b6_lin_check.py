import json,jsonschema,pathlib
p=pathlib.Path('tmp/tw_batch6_enriched/TW-PERSON-000560.json');d=json.loads(p.read_text(encoding='utf-8'));d['education'][0].pop('degree');p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');jsonschema.validate(d,json.load(open('.agents/skills/country-org-collector/person_profile_schema.json',encoding='utf-8-sig')));print('jsonschema PASS')

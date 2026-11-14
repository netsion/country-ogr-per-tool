import json,pathlib,jsonschema
r=pathlib.Path(__file__).resolve().parents[1];p=r/'tmp/tw_batch2_enriched/TW-PERSON-000532.json';x=json.loads(p.read_text(encoding='utf-8'))
for a in x['major_achievements']:a['achievement']+=' 此为2025全年统计，包含其2025年9月1日上任前期间，不能等同本人任内新增或个人贡献。'
x['collection_meta']['notes']+=' 2025年终报告公开检索时间早于采集日，正文取2025已发生数据而非未来预测；年度数据含上任前期间，归因限于在任部长公开说明部门成果。'
jsonschema.Draft7Validator(json.loads((r/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

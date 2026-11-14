import json,pathlib,jsonschema
r=pathlib.Path(__file__).resolve().parents[1];p=r/'tmp/tw_batch2_enriched/TW-PERSON-000199.json';x=json.loads(p.read_text(encoding='utf-8'))
x['family_members']=[]
x['collection_meta']['notes']+=' 复核更正：TVBS与联合报open虽返回页面，但正文在本次抓取内容中不可检索到配偶姓名/登记内容，检索引擎返回的全文样文本不当作成功直读双源；故撤回家庭结构化条目，骆武昌仅作为待复核公开线索。以上较早关于配偶已完成双原文确认的表述以本更正为准。'
jsonschema.Draft7Validator(json.loads((r/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

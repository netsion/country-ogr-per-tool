import json,pathlib,jsonschema
r=pathlib.Path('D:/ai-workspace/apec-osint-tool');f=r/'tmp/tw_batch5_enriched/TW-PERSON-000545.json';p=json.loads(f.read_text(encoding='utf8'))
u='https://www.businesstoday.com.tw/article/category/80392/post/200804170025/'
p['political_stances']=[{'date':'2008-04-17','topic':'国会公费助理薪资透明','stance_content':'在今周刊署名文章《国会要阳光，先让助理薪资透明化》中，主张推动国会改革应先公开立委亲友助理的薪资，让纳税人了解立委公费用途；以此预防人头助理及不当利益输送。此为当时署名评论主张，非已实施成果。','source':u}]
p['collection_meta']['quotes'].append({'title':'陳東豪署名：國會要陽光，先讓助理薪資透明化','url':u})
p['collection_meta']['notes']=p['collection_meta']['notes'].replace('未发现足以填写的明确具体公共政策主张，政治内幕预测与对个人批评不作政策。','补读2008-04-17今周刊本人署名全文，确认国会助理薪资透明化主张1项；其余国防预算检索多为民调解读，未作政策。寰宇2020-11-20报道全文仅讨论媒体与政党关系值得思考，缺具体制度主张未纳入。宝岛当前介绍页无文章发布日期，仅页脚2026，不将页脚视为活动日期。政治内幕预测与对个人批评不作政策。')
jsonschema.validate(p,json.loads((r/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8-sig')))
f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

import json,pathlib,jsonschema
p=pathlib.Path('tmp/tw_batch6_enriched/TW-PERSON-000561.json');d=json.loads(p.read_text(encoding='utf-8'))
d['collection_meta']['quotes'] += [{'title':'藍白合在台中 盧秀燕、黃國昌、江啟臣為白營站台','url':'https://www.cna.com.tw/news/aipl/202610040141.aspx'},{'title':'民眾黨通過第二波議員提名 候任立委陳清龍推太太接棒','url':'https://www.taisounds.com/news/content/71/224868'}]
n=d['collection_meta']['notes'];n=n.replace('家庭连小华据中国之春评论正文单源，其他新闻页面不可读，缺独立正文交叉。','家庭连小华夫妻关系已补中央社2026-10-04及太报2025-11-12新闻正文交叉确认；仅记录公开配偶及参选身份，无预写选举结果。');d['collection_meta']['notes']=n
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');jsonschema.validate(d,json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')));print('jsonschema PASS; social_accounts=',d['social_accounts'])

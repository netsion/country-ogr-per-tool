import json,pathlib,jsonschema
f=pathlib.Path('tmp/tw_batch7_enriched/TW-PERSON-000578.json');p=json.loads(f.read_text(encoding='utf-8'))
p['person_relationships']=[dict(person_id='TW-PERSON-000549',person_name='苏巧慧',relationship_type='colleague',description='2026年9月9日中央社引述苏巧慧说明，在蔡英文任内曾与吴琪铭共同争取前瞻预算补助新北轨道建设；仅指此项预算争取合作，不推定私人或长期盟友。')]
p['family_members']=[dict(person_id=None,name='吴昇翰',relationship='son',industry_or_organization='吴琪铭立法委员服务处（曾任主任）；2026年争取民进党新北市议员提名')]
p['collection_meta']['notes']+=' 补充：已读TW-PERSON-000549实际画像确认为苏巧慧，填入具体轨道预算合作关系；儿子吴昇翰依据TVBS2026-01-29明确父子报道收录，家庭仅单源，未独立双源核实。前述暂不结构化说明以此补充为准。'
jsonschema.validate(p,json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')));f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')

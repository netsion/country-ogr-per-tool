import json,pathlib
p=pathlib.Path('output/tw/2026-07-27/persons/TW-PERSON-000012.json');x=json.loads(p.read_text(encoding='utf-8-sig'))
s=json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))
x={k:v for k,v in x.items() if k in s['properties']}
x.update(name='蕭美琴',name_zh='萧美琴',aliases=['萧美琴'],birth_place='日本神户',current_positions=['台湾地区副领导人'],person_relationships=[])
x['education']=[dict(institution='欧柏林学院（Oberlin College）',degree='bachelor',field='东亚研究',start_date=None,end_date='1993'),dict(institution='哥伦比亚大学（Columbia University）',degree='master',field='政治学',start_date=None,end_date=None)]
def w(a,b,o,t,i=None):return dict(start_date=a,end_date=b,organization=o,position=t,org_id=i)
x['work_experience']=[w('1995','1996','民主进步党（民主進步黨）','驻美代表处活动执行长','TW-PARTY-012'),w('1996','1997','民主进步党（民主進步黨）','国际事务部副主任','TW-PARTY-012'),w('1997','2006','民主进步党（民主進步黨）','国际事务部主任','TW-PARTY-012'),w('2000',None,'总统府（總統府）','顾问、英文秘书及翻译'),w('2002','2008','立法院','第5、6届立法委员','TW-GOV-020'),w('2012','2020','立法院','第8、9届立法委员','TW-GOV-020'),w('2020-07','2023','驻美国台北经济文化代表处（駐美國台北經濟文化代表處）','驻美代表'),w('2024-05-20',None,'总统府（總統府）','台湾地区副领导人')]
x['biography_summary']='萧美琴，1971年生于日本神户，成长经历横跨台湾、日本与美国，长期从事政党国际事务、民意代表及对外交流工作。1993年取得欧柏林学院东亚研究学士，后取得哥伦比亚大学政治学硕士，研究专长为国际关系。1995年进入民主进步党驻美代表处工作，随后担任该党国际事务部门副主任、主任；2000年进入总统府，担任顾问、英文秘书和翻译。她曾任第5、6、8、9届立法委员，关注花莲交通、农业、性别平等、外交和人权等议题，并参与台湾民主基金会及国际自由民主组织工作。2020年转任驻美代表，2023年返台参与台湾地区领导人选举，与赖清德搭档于2024年当选，5月20日就任台湾地区副领导人。其公开活动涉及国际伙伴合作、科技人才交流与社会防卫韧性。历史任职与现职已分开记录，未确认的教育起止时间保留为空。'
x['political_stances']=[dict(date='2026-09-27',topic='科技交流与民主价值',stance_content='为北美台湾科技年会致词时，主张深化台美科技人才和新创交流，并认为前瞻科技发展应立足自由、透明与民主价值。',source='https://www.president.gov.tw/Page/695')]
x['major_achievements']=[dict(date='2024-01-13',achievement='与赖清德搭档赢得2024年台湾地区领导人选举，共获5,586,019票。',organization='总统府（總統府）')]
x['profile']={k:v for k,v in (x.get('profile') or {}).items() if k in s['properties']['profile']['properties']}
for a in x.get('social_accounts',[]):a['source_note']='原Wikidata档案保留；本轮进行了社交平台检索，未完成账号归属及平台ID的独立核验。'
x['collection_meta']=dict(collection_date='2026-11-13',phase='phase4_person_profile',data_sources=['official_website','wikipedia','news_search','web_search'],notes='本轮新核实：总统府官方简介及Wikipedia核对身份、出生地、学历和主要履历；与中央社原文交叉核对2024当选事实。现职按采集时官方页面记录。履历年份保留来源精度；2000年总统府职位结束日期未知，null不代表仍任。政策立场来自官方活动摘要，为单一直接来源。原出生精确日期保留并以Wikipedia核对；头像、四个社媒URL和平台ID保留但未经本轮独立复核。已检索Facebook/X/Instagram及LinkedIn/TikTok/YouTube，未据同名搜索结果新增账号。家庭成员未调查，避免将单一来源扩写为确定关系。',quotes=[dict(title=t,url=u) for t,u in [('总统府：萧美琴简介','https://www.president.gov.tw/Page/695'),('Hsiao Bi-khim — Wikipedia','https://en.wikipedia.org/wiki/Hsiao_Bi-khim'),('中央社：赖萧配当选','https://www.cna.com.tw/news/aipl/202401140007.aspx')]])
out=pathlib.Path('tmp/tw_enrichment');out.mkdir(exist_ok=True,parents=True);(out/p.name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

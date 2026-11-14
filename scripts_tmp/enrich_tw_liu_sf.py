import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';pid='TW-PERSON-000531';x=json.loads((B/'persons'/f'{pid}.json').read_text(encoding='utf-8'))
cv='https://www.moi.gov.tw/cp.aspx?n=27';report='https://www.moi.gov.tw/News_Content.aspx?n=2&s=342749';wiki='https://en.wikipedia.org/wiki/Liu_Shyh-fang';order='https://www.president.gov.tw/Page/294/49484';appoint='https://www.cna.com.tw/news/aipl/202404120035.aspx'
x.update(name='劉世芳',name_en='Liu Shyh-fang',gender='female',current_positions=['内政部部长'])
x['education']=[dict(institution=n,degree=d,field=f,start_date=None,end_date=None) for n,d,f in [('淡江大学（淡江大學）','bachelor','化学工程'),('俄克拉荷马州立大学（Oklahoma State University）','master','环境工程')]]
jobs=[('2002-02-01','2002-06-30','立法院','第5届立法委员','TW-GOV-020'),('2002-07-01','2004-05-20','行政院','秘书长','TW-GOV-019'),('2006-07-16','2007-02-11','总统府（總統府）','副秘书长','TW-GOV-023'),('2010-12-25','2014-12-24','高雄市政府','副市长',None),('2016-02-01','2024-01-31','立法院','第9及10届立法委员','TW-GOV-020'),('2024-05-20',None,'内政部（內政部）','部长',None)]
x['work_experience']=[dict(start_date=a,end_date=b,organization=o,position=t,org_id=i) for a,b,o,t,i in jobs]
x['biography_summary']='刘世芳是台湾地区政治人物，现任内政部部长。内政部官方履历列有淡江大学化学工程系学历和美国俄克拉荷马州立大学环境工程硕士，职业经历横跨环境行政、地方治理、立法机关及中央政府幕僚。她曾任台北市政府环境保护局局长、台中县副县长、第5届立法委员、行政院秘书长、总统府及国家安全会议副秘书长、高雄市副市长，之后再次进入立法院担任第9届及第10届委员。2024年5月接任内政部长后，其公开职责涵盖警政、民防韧性、居住及国土治理、移民与地方行政等。2026年向立法院报告业务时，她以安全韧性、安居环境和民主公益为政策主轴，说明打诈、地方组织与民众权益相关工作。本档将已发布制度修订和部门报告的执行进度与未来工作目标分开，成果明确属于内政部及跨机关团队，不视作个人独立完成，也不将机关自报数字当成本轮独立审计结论。家庭关系与个人账号缺少足够可追溯身份依据的部分保持空值。'
x['political_stances']=[dict(date='2026-10-21',topic='安全与社会韧性',stance_content='向立法院报告时主张加强打诈、防毒及第一线警政训练，推进韧性家园、保障人民安全；是其施政方针。',source=report),dict(date='2026-10-21',topic='宜居环境与国土永续',stance_content='将安居环境与永续国土发展列为内政施政重点，强调居民生活与国家发展条件。',source=report),dict(date='2026-10-21',topic='平等参政与专业人才',stance_content='主张改善性别平等参政环境，并配合多元专业人才来台发展，扩大专业人才认定领域。',source=report)]
x['major_achievements']=[dict(date='2026-06',achievement='内政部报告于6月修正发布地方行政机关及地方立法机关组织准则，以改善性别平等参政环境；属于部门制度修订事实，未评估长期效果。',organization='内政部（內政部）'),dict(date='2026-07',achievement='内政部报告专业人才归化认定标准新增量子科技等高科技专业领域；记录部门已公布制度调整，不把未来人才增加当已完成效果。',organization='内政部（內政部）')]
x['person_relationships']=[dict(person_id='TW-PERSON-000001',person_name='赖清德（賴清德）',relationship_type='superior',description='赖清德新政府于2024年公布刘世芳出任内政部长，并于5月20日由总统令特任，限定为明确任命与工作关系。',source=order,corroborating_sources=appoint)]
x['family_members']=[]
qs=[('内政部官方首长履历',cv),('内政部2026立院报告',report),('英文历史履历',wiki),('总统府任命公报',order),('CNA新内阁名单',appoint)]
x['collection_meta']=dict(collection_date='2026-11-13',phase='phase4_person_profile',data_sources=['official_website','wikipedia','news_search','web_search'],quotes=[dict(title=t,url=u) for t,u in qs],notes='已读内政部官方履历及业务报告、Wikipedia与CNA。学历以官方明确两项为准；维基另列台大MBA官方未列，暂未录入。维基出生日期信息框与正文13日/15日矛盾，故不新增精确生日。历史任期以维基与官方履历对应，现职以官方及任命公报。政策报告发布10月22日、实际列席10月21日，政策日期用活动日。两项制度成果均部门自报，不当作个人独立政绩或独立效果评估。家庭已定向查配偶父母，结果大量为其主管的新住民配偶业务及财申空栏索引，未得到可确认本人家属姓名的全文，不据其身份推测婚姻、不采财产或未成年资料。六社媒平台Facebook/X/Instagram/LinkedIn/TikTok/YouTube检索无可靠本人主页正文，TikTokrobots阻止；新骨架profile缺省不新增。已核立法院、行政院、总统府及赖清德实际画像身份，未知内政部/高雄市府org_id保持null，不使用索引自动绑定。')
for oid in ['TW-GOV-020','TW-GOV-019','TW-GOV-023']:
 z=json.loads((B/'orgs'/f'{oid}.json').read_text(encoding='utf-8'));assert z['basic_info']['country_iso3']=='TWN'
z=json.loads((B/'persons/TW-PERSON-000001.json').read_text(encoding='utf-8'));assert z['name_zh']=='赖清德'
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
(R/'tmp/tw_batch2_enriched'/f'{pid}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

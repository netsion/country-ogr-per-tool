import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';pid='TW-PERSON-000148'
x=json.loads((B/'persons'/f'{pid}.json').read_text(encoding='utf-8'))
u={'official':'https://www.taichung.gov.tw/1173576/post','culture':'https://tcmb.culture.tw/zh-tw/detail?id=733251&indexCode=Culture_Object','lunch':'https://www.cna.com.tw/news/aloc/202601090174.aspx','implemented':'https://www.cna.com.tw/news/aloc/202609160299.aspx','wiki':'https://zh.wikipedia.org/wiki/盧秀燕'}
x['name']='盧秀燕';x['birth_place']='台湾基隆';x['current_positions']=['台中市市长']
x['education']=[dict(institution=n,degree=d,field=f,start_date=None,end_date=None) for n,d,f in [('政治大学（國立政治大學）','bachelor','地政'),('淡江大学（淡江大學）','master','国际事务与战略研究')]]
x['work_experience']=[dict(start_date=a,end_date=b,organization=n,position=p,org_id=oid) for a,b,n,p,oid in [('1994','1998','台湾省议会（臺灣省議會）','省议员',None),('1999','2018','立法院','立法委员','TW-GOV-020'),('2018-12-25',None,'台中市政府（臺中市政府）','市长',None)]]
x['political_stances']=[dict(date=d,topic=t,stance_content=c,source=u[s]) for d,t,c,s in [('2026-01-09','校园营养午餐','主张中央编列全国免费营养午餐预算，将供餐视为政府责任；此为经费分担倡议，不能等同中央已采纳。','lunch'),('2022','空气品质','选举文宣主张严格控制空气污染、改善空气品质。此为竞选政策主张，不等同达成空气品质目标。','culture'),('2022','交通与居住治理','提出发展轨道捷运及公路转运，并持续建置社会住宅、降低托育负担；分别记录为施政方向，不作完工认定。','culture')]]
x['major_achievements']=[dict(date='2022-11-26',achievement='赢得2022年台中市长选举并连任；来源为文化部国家文化记忆库收录的选举文宣说明，不将竞选承诺计为成果。',organization='台中市政府（臺中市政府）'),dict(date='2026-09',achievement='任内市府在新学期实施国中小免费营养午餐，为市府及学校团队执行成果；中央社同期报道议员质疑供餐分量，政策启动不等同品质成效已获确认。',organization='台中市政府（臺中市政府）')]
x['person_relationships']=[dict(person_id='TW-PERSON-000023',person_name='林佳龙（林佳龍）',relationship_type='political_rival',description='2018年台中市长选举对手；属特定选举中的竞争关系，不推断私人关系。来源：文化部国家文化记忆库及维基履历。')]
x['family_members']=[dict(person_id=None,name='廖述嘉（廖述嘉）',relationship='spouse',industry_or_organization='曾任台中市议员；仅记录公开配偶身份。')]
x['biography_summary']='卢秀燕是台湾地区政治人物，现任台中市市长，具有新闻媒体及民意代表经历。台中市政府官方简介列有政治大学地政系学士及淡江大学国际事务与战略研究所硕士学历。她早年在华视从事新闻采访，曾任中部采访中心主任及省政特派员，之后转入公共事务，1994年当选台湾省议员，1999年至2018年间担任第4至第9届立法委员。2018年参加台中市长选举并当选，2022年再获连任。其公开政策主张涵盖空气品质、公共交通、托育与居住政策，2026年曾主张由中央编列全国免费营养午餐经费。台中随后启动国中小免费营养午餐，但供餐品质与分量受到议员质询，本档将政策实施与政策效果评价分开记录，不将竞选目标或行政团队成果全部归为个人功绩。现职已清除旧档中的立委及未明确机构的议会成员头衔。'
x['collection_meta']=dict(collection_date='2026-11-14',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia'],completeness_score=0,notes='现职依据2026-08-07更新官方简介与2026-09中央社报道；未提前采用年底换届结果。出生及早期任期精度部分依维基与文化记忆库；文化记忆库履历亦引维基，不能算完全独立。配偶依据维基及华视新闻搜索摘要交叉，华视正文403，未扩展子女资料。社交平台已检索，原账号与user_id和头像原样保留，未新增未认证账号。成就均区分选举结果、团队执行及争议。',quotes=[dict(title=k,url=v) for k,v in u.items()])
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
(R/'tmp/tw_batch2_enriched'/f'{pid}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

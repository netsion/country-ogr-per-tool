import pathlib,json,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';x=json.loads((B/'persons/TW-PERSON-000034.json').read_text(encoding='utf-8'));idx=json.loads((B/'_name_index.json').read_text(encoding='utf-8'))
x['name']='朱立倫';x['current_positions']=[]
x['education']=[dict(institution=n,degree=d,field=f,start_date=None,end_date=None) for n,d,f in [('台湾大学（國立臺灣大學）','bachelor','工商管理'),('纽约大学（New York University）','master','财务金融'),('纽约大学（New York University）','doctorate','会计学')]]
def w(s,e,n,p,i=None):return dict(start_date=s,end_date=e,organization=n,position=p,org_id=i)
x['work_experience']=[w('1999','2001','立法院','立法委员','TW-GOV-020'),w('2001','2009','桃园县政府（桃園縣政府）','县长'),w('2009','2010','行政院','副院长','TW-GOV-019'),w('2010','2018','新北市政府','市长'),w('2015','2016','中国国民党（中國國民黨）','主席','TW-PARTY-013'),w('2021','2025','中国国民党（中國國民黨）','主席','TW-PARTY-013')]
for row in x['work_experience']:
 if row['org_id']: assert json.loads((B/'orgs'/f"{row['org_id']}.json").read_text(encoding='utf-8'))['org_id']==row['org_id']
u='https://www.cna.com.tw/news/aipl/201906190196.aspx';p='https://news.pts.org.tw/article/314917';g='https://www.ntpc.gov.tw/ch/home.jsp?dataserno=201411030026&id=28&mcustomize=multimessages_view.jsp&parentpath=0,6,27'
x['political_stances']=[dict(date='2019-06-19',topic='托育公共责任',stance_content='主张托育应由国家整体政策支持，不能让县市单独努力，并可借镜新北公托合作联盟。',source=u),dict(date='2019-06-19',topic='托育供给与人员',stance_content='主张增加私立托育中心招收师资诱因，提供家长多元选择；不把建议当作已实现效果。',source=u),dict(date='2016-01-16',topic='两岸政治基础',stance_content='投票日公开重申九二共识、一中各表立场；仅记录当时本人发言。',source=p)]
x['major_achievements']=[dict(date='2014-11-03',achievement='任内八里下庄公共托育中心启用，市府当日称为全市第34家；这是市府与运营团队成果，数量属官方发布，非本轮独立审计。',organization='新北市政府'),dict(date='2014-11-03',achievement='同日八里下庄公共托老中心启用，市府称为第14家；记录已启用设施，不把未来规划数量当完成。',organization='新北市政府')]
x['person_relationships']=[];x['family_members']=[dict(person_id=None,name='高婉倩（高婉倩）',relationship='spouse',industry_or_organization='仅记录公视原文与维基确认的公开配偶身份。')]
x['biography_summary']='朱立伦是具有财会学术背景的台湾地区政治人物，曾任立法委员、桃园县县长、行政院副院长、新北市市长及中国国民党主席。其教育经历包括台湾大学工商管理学士、纽约大学财务金融硕士与会计学博士，返台后曾从事大学教学，之后进入民意代表和地方行政体系。2001年起担任桃园县县长，2009年进入行政院，2010年出任新北市升格后的首任市长，任内推进公共托育及托老设施。2015年及2021年曾担任国民党主席，2025年任期结束；本档不将旧党主席、市长或副院长继续列为现职。其公开政策关注包括托育责任分担、民间供给与两岸政治基础。具体建设成果按市府发布限定团队归因，不把政策主张当作效果评估。公开家庭仅收录配偶高婉倩，不延伸子女和财产资料。'
x['collection_meta']=dict(collection_date='2026-11-14',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia'],quotes=[dict(title=t,url=v) for t,v in [('新北市府：八里托育托老中心启用',g),('中央社：托育应是国家政策',u),('公视：朱立伦与配偶投票及两岸发言',p),('维基：朱立伦履历','https://zh.wikipedia.org/wiki/朱立倫')]],notes='未确认新的在任公职，清除旧现职。学历与早期任期仍维基单源，任期仅保留年份；2025卸任党主席依维基，官方历史页502不可读。市府设施数为官方自陈，非独立绩效审计。配偶由公视原文与维基交叉。人物合作关系缺具体证据留空。已检索社交平台，原三个账号、user_id和头像均保留，不宣称重新平台认证。')
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
(R/'tmp/tw_batch3_enriched/TW-PERSON-000034.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];b=R/'output/tw/2026-07-27';pid='TW-PERSON-000214';x=json.loads((b/'persons'/f'{pid}.json').read_text(encoding='utf-8'))
x['name']='黃敏惠';x['current_positions']=['嘉义市市长']
x['education']=[dict(institution=n,degree=d,field=f,start_date=None,end_date=None) for n,d,f in [('台湾师范大学（國立臺灣師範大學）','bachelor','国文'),('嘉义大学（國立嘉義大學）','master','管理')]]
def w(a,z,n,p):return dict(start_date=a,end_date=z,organization=n,position=p,org_id=None)
x['work_experience']=[w('1996','1999','国民大会（國民大會）','代表'),w('1999','2005','立法院','立法委员'),w('2005-12-20','2014-12-25','嘉义市政府（嘉義市政府）','市长'),w('2018-12-25',None,'嘉义市政府（嘉義市政府）','市长')]
u='https://www.cna.com.tw/postwrite/chi/446935'
x['political_stances']=[dict(date='2026-10-14',topic=t,stance_content=s,source=u) for t,s in [('财政纪律','主张不举债、不留债予下一代，并兼顾教育、社会福利与经济建设；市府供稿所列财政数字未经本轮独立审计。'),('全龄照顾','施政报告提出长者健保、育儿支持与青年就业租屋补贴等全龄支持方向，预算编列不等同所有政策已实施。'),('教育资源','主张持续免费营养午餐、增加餐食品质资源及教师员额；次年员额目标不视为当年完成。')]]
x['major_achievements']=[dict(date='2026-01-21',achievement='任内举行污水系统一期第8、9标竣工典礼，标志一期工程完成。工程跨越多个任期，属于中央、市府与工程团队共同成果；依据市府供稿，不把供稿数字当独立审计。',organization='嘉义市政府（嘉義市政府）'),dict(date='2025-10-05',achievement='市府供稿记载污水一期第8、9标于该日竣工，包含后巷管路与用户接管工程；与2026年典礼日期区分。属于同一污水项目阶段，不作为另一独立政绩叠加计算。',organization='嘉义市政府（嘉義市政府）')]
x['major_achievements']=x['major_achievements'][:1]
x['family_members']=[dict(person_id=None,name='蔡宗佑（蔡宗佑）',relationship='spouse',industry_or_organization='仅记录自由时报原文与维基交叉确认的公开配偶身份。')]
x['person_relationships']=[]
x['biography_summary']='黄敏惠是台湾地区地方政治人物，现任嘉义市市长，早年从事国文教学，后进入民意代表及地方行政工作。维基履历列有台湾师范大学国文与嘉义大学管理硕士学历；本轮尚缺学校原始学籍来源，未将其视为完成多源学历认证。她曾任国民大会代表及立法委员，2005年至2014年担任嘉义市长，2018年再度就任后继续参与城市治理。2026年10月的市府施政报告仍以市长身份说明财政纪律、全龄照顾及公共建设方向，未提前采用年底换届结果。污水一期工程涉及跨任期规划、中央补助及施工团队，本档只记录竣工与典礼等已经发生的节点，不将所有工程归因于个人，也不把后续计划当成已完成成果。旧党主席、立委及国大代表头衔已从现职移除，配偶仅保留公开实名关系。'
x['collection_meta']=dict(collection_date='2026-11-14',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia'],quotes=[dict(title=t,url=v) for t,v in [('市府供稿：2026施政报告',u),('市府供稿：污水一期竣工','https://www.cna.com.tw/postwrite/chi/424384'),('自由时报：公开配偶现场报道','https://election.ltn.com.tw/2016/news/paper/921213'),('维基：黄敏惠履历','https://zh.wikipedia.org/wiki/黃敏惠')]],notes='现职依据2026-10市府供稿与维基；独立中央社页面未显示可用正文，永续委页403，不据摘要采信。市府供稿不是中央社独立调查。学历、早期任期与出生日期仍维基单源；配偶由自由时报与维基交叉。政策预算目标不作已完成成果；污水项目仅计一项，避免重复典礼和竣工节点。人物关系缺直接任职或共同提案证据留空。已多平台检索，原三个账号/user_id及头像完整保留，不宣称重新平台认证。')
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
(R/'tmp/tw_batch3_enriched'/f'{pid}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

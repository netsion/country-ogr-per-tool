import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';x=json.loads((B/'persons/TW-PERSON-000002.json').read_text(encoding='utf-8'))
u='https://www.cna.com.tw/news/firstnews/202005205005.aspx';v='https://www.cna.com.tw/news/firstnews/201905175010.aspx';o='https://www.president.gov.tw/Page/705'
x['current_positions']=[]
x['education']=[dict(institution=n,degree=d,field='法律',start_date=None,end_date=None) for n,d in [('台湾大学（國立臺灣大學）','bachelor'),('康奈尔大学（Cornell University）','master'),('伦敦政治经济学院（London School of Economics and Political Science）','doctorate')]]
def w(a,b,n,p,i=None):return dict(start_date=a,end_date=b,organization=n,position=p,org_id=i)
x['work_experience']=[w('2000','2004','大陆委员会（大陸委員會）','主任委员'),w('2005','2006','立法院','立法委员','TW-GOV-020'),w('2006','2007','行政院','副院长','TW-GOV-019'),w('2016-05-20','2024-05-20','总统府（總統府）','台湾地区领导人','TW-GOV-023')]
x['political_stances']=[dict(date='2020-05-20',topic='两岸沟通',stance_content='就职演说以和平、对等、民主、对话作为两岸沟通原则，并反对以一国两制处理台湾问题；记录为当时本人主张。',source=u),dict(date='2020-05-20',topic='产业发展',stance_content='主张发展资讯数位、资安、精准健康、国防战略、绿电及民生战备等产业方向；属于政策布局，不能据此认定目标均已完成。',source=u),dict(date='2019-05-17',topic='婚姻平权',stance_content='同婚专法三读后公开肯定婚姻平权进展；并提醒社会包容尊重差异。',source=v)]
x['major_achievements']=[dict(date='2019-05-22',achievement='任内公布司法院释字第七四八号解释施行法；立法机关三读、行政及公民团体共同推动，不归为个人独力完成。依据总统府年表及中央社三读报道。',organization='总统府（總統府）'),dict(date='2018-07-01',achievement='任内军公教退抚制度改革措施施行；属政府与立法程序共同成果，具体长期财务效果未在本轮独立审计。依据总统府历史年表。',organization='总统府（總統府）')]
t=json.loads((B/'persons/TW-PERSON-000001.json').read_text(encoding='utf-8'));assert t['name_zh']=='赖清德'
x['person_relationships']=[dict(person_id='TW-PERSON-000001',person_name='赖清德（賴清德）',relationship_type='colleague',description='2020至2024年蔡英文与赖清德分别担任领导人及副领导人；仅记录该任期共事，不推断私人或派系关系。来源2020就职演说与维基履历。')]
x['family_members']=[]
x['biography_summary']='蔡英文是台湾地区政治人物及法律学者，2016年至2024年担任台湾地区领导人，曾多次出任民主进步党主席。她取得台湾大学法律学士、康奈尔大学法律硕士与伦敦政治经济学院法律博士学位，返台后从事法律教学及国际经贸事务，后来进入公共行政部门。其公职经历包括大陆委员会主任委员、立法委员和行政院副院长，随后转入政党领导及选举工作。任内政策议题涉及两岸关系、国际经贸、社会保障、婚姻平权、产业转型及防卫能力。2024年5月任期届满后，本档不再将领导人、党主席或早年公职列为现职。本轮关注可核实的历史决策经历和制度成果，未把官方政绩叙述等同独立效果评估。'
x['collection_meta']=dict(collection_date='2026-11-14',phase='phase4_person_profile',completeness_score=0,data_sources=['official_website','news_search','wikipedia'],quotes=[dict(title=t,url=z) for t,z in [('总统府蔡英文历史履历',o),('中央社2020就职演说',u),('中央社同婚三读发言',v),('英文维基蔡英文履历','https://en.wikipedia.org/wiki/Tsai_Ing-wen'),('INSIDE蔡英文社群经营','https://www.inside.com.tw/article/35038-tsai-ingwen-social-network')]],notes='当前无另行确认的在任公职，current_positions为空，历史头衔均已移出。出生日期及早期精确任期仍有维基单源边界。家庭检索只发现父母姓名的单源或低可靠转载，未达到交叉证据标准，保持空。社交多平台检索并读INSIDE，原四账号及user_id、头像完整保留，不宣称本轮逐个平台认证。年金施行成果为官方单源，效果与责任归因不外推。BBC页面不可读未计来源。')
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
p=R/'tmp/tw_batch3_enriched';p.mkdir(exist_ok=True);(p/'TW-PERSON-000002.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

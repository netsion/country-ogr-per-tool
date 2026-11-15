import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';pid='TW-PERSON-000533'
x=json.loads((B/'persons'/f'{pid}.json').read_text(encoding='utf-8'))
x.update(name='侯友宜',name_zh='侯友宜',gender='male',current_positions=['新北市市长'])
x['education']=[dict(institution='中央警察大学（中央警察大學）',degree='doctorate',field='犯罪防治',start_date=None,end_date=None)]
x['work_experience']=[dict(start_date=a,end_date=b,organization=o,org_id=None,position=p) for a,b,o,p in [('2006','2008','内政部警政署（內政部警政署）','署长'),('2008','2010','中央警察大学（中央警察大學）','校长'),('2010','2018','新北市政府','副市长'),('2018-12-25',None,'新北市政府','市长')]]
u='https://www.cna.com.tw/news/aipl/202308090062.aspx'
x['political_stances']=[dict(date='2023-08-09',topic='核电与减煤',stance_content='竞选期间主张在安全审查下推动既有核电延役及核四重启；属当时政策倡议，不代表已执行。',source=u),dict(date='2023-08-09',topic='再生能源与节能',stance_content='提出扩大再生能源及储能、智慧电网投入，以节能及供需管理辅助能源转型。',source=u),dict(date='2023-12-27',topic='两岸沟通',stance_content='公开主张维持两岸和平稳定，并与美国、中国大陆保持可对话关系；记录为其竞选期间主张。',source='https://www.cna.com.tw/news/aipl/202312270202.aspx')]
x['major_achievements']=[dict(date='2018-11-24',achievement='赢得新北市长选举，随后就任；本项为选举结果，不等同市政治理成效。',organization='新北市政府'),dict(date='2022-11-26',achievement='在新北市长选举中连任；结果依据所读维基履历，未列入未核实的具体施政数字。',organization='新北市政府')]
x['person_relationships']=[dict(person_id='TW-PERSON-000034',person_name='朱立伦（朱立倫）',relationship_type='superior',description='历史行政上下级：2010年受时任新北市长朱立伦邀请出任副市长；不表示当前上下级。来源：维基履历及市府副市长经历。')]
x['family_members']=[dict(person_id=None,name='任美铃（任美鈴）',relationship='spouse',industry_or_organization='仅记录中央社与维基公开确认的配偶身份。')]
x['social_accounts']=[dict(platform='facebook',account_name='侯友宜',url='https://www.facebook.com/houyuih/',source=6)]
x['biography_summary']='侯友宜是台湾地区政治人物，现任新北市市长，具有警政行政与地方治理背景。新北市政府官方简介列有中央警察大学犯罪防治研究所博士学历，并记载其曾任桃园县政府警察局局长、刑事警察局局长、警政署署长及中央警察大学校长。2010年转入新北市政府担任副市长，2018年当选市长，并于2022年连任。2023年代表中国国民党参与次年台湾地区领导人选举，其公开竞选政策涉及核电安全审查、减煤、再生能源与节能，以及两岸和平和对话。本档将竞选主张与实际施政成果分开，不将未实现的政策承诺写成个人成就；现职以本轮所读市府网页为依据，未提前采用2026年底换届结果。家庭仅保留有公开来源的配偶姓名，未知相关人物编号保持空值。'
sources=[('新北市政府：市长侯友宜简介','https://www.ntpc.gov.tw/ch/home.jsp?id=107&parentpath=0,6,106'),('维基百科：侯友宜履历','https://zh.wikipedia.org/wiki/侯友宜'),('公视：侯友宜公布能源政策','https://news.pts.org.tw/article/650477'),('中央社：能源政策',u),('中央社：公开家庭访谈','https://www.cna.com.tw/news/aloc/201811210336.aspx'),('中央社：两岸发言及配偶','https://www.cna.com.tw/news/aipl/202312270202.aspx'),('市府链接的本人Facebook','https://www.facebook.com/houyuih/')]
x['collection_meta']=dict(collection_date='2026-11-14',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia'],quotes=[dict(title=t,url=u) for t,u in sources],notes='市府现职页无精确更新日，未声称逐日核实。学历及历任职位由市府与维基交叉；具体任期及两次选举结果仍依维基单源，需后续选委会核验。政策原文由公视与中央社读取交叉，按历史竞选主张记录。配偶由中央社原文及维基确认，未扩展子女。社交媒体多平台检索，仅添加市府直接链接Facebook，其他未认证账号不收录。没有新增ID或QID。')
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
(R/'tmp/tw_batch2_enriched'/f'{pid}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

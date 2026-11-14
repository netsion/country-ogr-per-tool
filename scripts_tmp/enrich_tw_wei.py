import json,pathlib,jsonschema
p=pathlib.Path('output/tw/2026-07-27/persons/TW-PERSON-000508.json');x=json.loads(p.read_text(encoding='utf-8-sig'));s=json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'));x={k:v for k,v in x.items() if k in s['properties']}
x.update(name='魏哲家',name_en='C.C. Wei',name_zh='魏哲家',aliases=['C. C. Wei','Che-Chia Wei'],birth_date=None,current_positions=['台湾积体电路制造公司董事长兼首席执行官'],person_relationships=[])
x['birth_date_note']='公开资料仅确认出生于1953年，月日未知，不补造1月1日。'
x['education']=[dict(institution='交通大学（國立交通大學）',degree='bachelor',field='电机工程',start_date=None,end_date=None),dict(institution='耶鲁大学（Yale University）',degree='doctorate',field='电机工程',start_date=None,end_date=None)]
def w(a,b,o,t,i=None):return dict(start_date=a,end_date=b,organization=o,position=t,org_id=i)
org='台湾积体电路制造公司（台灣積體電路製造股份有限公司）'
x['work_experience']=[w(None,None,'德州仪器（Texas Instruments）','研发技术人员'),w(None,None,'意法半导体（STMicroelectronics）','逻辑与SRAM技术开发高级经理'),w(None,'1998','特许半导体（Chartered Semiconductor Manufacturing）','技术资深副总裁'),w('2009','2012',org,'业务发展资深副总经理','TW-CORP-041'),w('2012-03','2013-11',org,'共同营运长','TW-CORP-041'),w('2013-11','2018-06',org,'总经理兼共同首席执行官','TW-CORP-041'),w('2018-06','2024-06',org,'首席执行官','TW-CORP-041'),w('2024-06',None,org,'董事长兼首席执行官','TW-CORP-041')]
x['biography_summary']='魏哲家，台湾半导体产业经营者及电机工程背景专业人士，公开资料记载出生于1953年。取得交通大学电机工程学士及耶鲁大学电机工程博士学位后，曾在德州仪器研发部门担任技术人员，在意法半导体负责逻辑与SRAM技术开发，并担任特许半导体技术资深副总裁。1998年加入台积电，此后参与制造营运、主流技术业务和业务发展管理。2009年至2012年担任业务发展资深副总经理，2012年3月至2013年11月担任共同营运长，2013年11月至2018年6月担任总经理兼共同首席执行官，2018年6月起担任首席执行官，2024年6月兼任董事长。2025年7月，美国半导体产业协会宣布其与刘德音共同获选该年度罗伯特·诺伊斯奖。本档现职依据台积电官方管理团队页面，出生月日及未确认的早期任职起止日期保持为空，不将企业官方社交账号归为个人账号。'
x['political_stances']=[]
x['major_achievements']=[dict(date='2025-07-28',achievement='美国半导体产业协会宣布魏哲家与刘德音共同获选2025年度罗伯特·诺伊斯奖；该日期为公布日，非颁奖日。',organization='美国半导体产业协会（Semiconductor Industry Association）')]
x['profile']={k:v for k,v in (x.get('profile') or {}).items() if k in s['properties']['profile']['properties']}
x['collection_meta']=dict(collection_date='2026-11-13',phase='phase4_person_profile',data_sources=['official_website','wikipedia','web_search','other'],notes='本轮全文来源为台积电官方、美国半导体产业协会、Wikipedia Che-Chia Wei，三个独立发布体系。首个C. C. Wei维基链接为消歧页，已识别并转至正确人物页。现职、学历和主要经历以官方与协会交叉核对；Wikipedia称交通大学硕士但官方及协会仅列学士，未加入硕士。出生仅1953年，不补造月日；gender保留原unknown，不凭姓名推断。SIA获奖公告为2025年7月28日，颁奖计划日期不是已核实完成事件。六平台社交搜索完成，无可靠个人账号，social_accounts留空；头像保留但未重新核实其是否单人肖像。本人产业政策观点缺乏充分直接原文证据，留空。',quotes=[dict(title=t,url=u) for t,u in [('台积电：管理团队','https://www.tsmc.com/english/aboutTSMC/executives'),('SIA：2025诺伊斯奖获选公告','https://www.semiconductors.org/tsmcs-dr-c-c-wei-and-dr-mark-liu-to-receive-sias-highest-honor/'),('Che-Chia Wei — Wikipedia','https://en.wikipedia.org/wiki/Che-Chia_Wei')]])
jsonschema.Draft7Validator(s).validate(x)
out=pathlib.Path('tmp/tw_enrichment');out.mkdir(exist_ok=True,parents=True);(out/p.name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

import json,pathlib,jsonschema
root=pathlib.Path('D:/ai-workspace/apec-osint-tool')
p=json.loads((root/'output/tw/2026-07-27/persons/TW-PERSON-000288.json').read_text(encoding='utf-8-sig'))
p['name']='王世堅';p['aliases']=['王世坚'];p['birth_place']='臺北市建成區（今大同區）'
p['current_positions']=['第11届立法委员（臺北市第二选举区）','立法院财政委员会委员']
p['education']=[dict(institution='中国文化大学（中國文化大學）',degree='master',field='应用化学',start_date=None,end_date=None)]
p['work_experience']=[dict(organization=o,org_id=i,position=t,start_date=s,end_date=e) for o,i,t,s,e in [('臺北市议会（臺北市議會）',None,'第8、9届议员','1998-12-25','2005-01-31'),('立法院','TW-GOV-020','第6届立法委员','2005-02-01','2008-01-31'),('臺北市议会（臺北市議會）',None,'第11至14届议员','2010-12-25','2024-01-31'),('立法院','TW-GOV-020','第11届立法委员','2024-02-01',None)]]
p['contacts']=[dict(type='phone',value='02-2358-6868',source='https://www.ly.gov.tw/Pages/List.aspx?nodeid=46758')]
p['family_members']=[dict(person_id=None,name='林秀芬',relationship='spouse',industry_or_organization=None)]
p['person_relationships']=[dict(person_id='TW-PERSON-000073',person_name='江鵬堅',relationship_type='associate',description='维基百科记载王世堅曾在江鵬堅竞选立法委员时担任竞选总干事；仅记录该历史竞选合作，具体年份尚未核实。')]
u='https://www.cna.com.tw/news/aipl/202401040234.aspx'
p['political_stances']=[dict(date='2024-01-04',topic=t,stance_content=c,source=u) for t,c in [('住房与城市更新','公办政见发表会主张推动公办都更、加速兴建社会住宅并提升品质，开发社子岛及解决阳明山限建。属于竞选主张，非已实施成果。'),('医疗与身障福利','主张放宽身心障碍鉴定方式、提高医护薪资并改善医疗环境。'),('水资源','主张广设海水淡化厂，减轻缺水对民生、农业及工业的影响。')]]
p['major_achievements']=[]
p['biography_summary']='王世堅是台湾民主进步党政治人物，现任臺北市第二选举区第11届立法委员，2024年2月1日到职，在立法院参加财政委员会。立法院官方履历列其最高学历为中国文化大学应用化学研究所硕士，并列明其曾任第8、9、11、12、13、14届臺北市议员及第6届立法委员。他的公职经历跨越地方议会与中央国会，先于1998年进入臺北市议会，2005年至2008年任立委，2010年回到市议会，2024年再进入立法院。其2024年公开政见涵盖社会住宅、公办都市更新、医疗工作环境、身障鉴定与水资源设施；这些是本人政策主张，不能据此推定已实现。官方议事影音目录还记录其2026年10月6日院会质询，证明当期持续履职。早期竞选合作及家庭资料以公开资料限定记录，未将知名度、选举胜负或媒体表现当作治理成果。'
sources=[('立法院－王世堅委员','https://www.ly.gov.tw/Pages/List.aspx?nodeid=46758'),('公督盟－王世堅','https://ccw.org.tw/index.php/assess/47/legislator/420'),('王世堅－维基百科','https://zh.wikipedia.org/wiki/王世堅'),('北市立委政见发表 王世堅、游淑慧皆提都更议题',u),('妻力挺王世堅：他是好立委','https://news.tvbs.com.tw/politics/307053'),('王世堅开抖音了？本人严正声明','https://news.ttv.com.tw/news/11408250019400N'),('立法院王世堅质询目录','https://ivod.ly.gov.tw/Demand/ListLgltVideo/6825')]
p['collection_meta']=dict(collection_date='2026-11-15',phase='phase4_person_profile',data_sources=['official_website','wikipedia','news_search','other'],notes='已读官方、中央社、TVBS、台视、公督盟及维基正文。活动证据截止2026-10-06；未预写2026选举结果。生日1960-01-01仅维基正文支持，未找到冲突但未获得官方二次确认。硕士学历官方与公督盟相符；其余早期学历、商业经历未补为官方履历。妻子实名由TVBS及维基交叉，江鵬堅竞选合作单一维基来源、年份未核。引用立法院与江鵬堅ID已读真实画像；臺北市议会及配偶无已核ID留空。未核当期党务职务。未找到两项能证明本人贡献且已实施的治理成果，成果数组留空。原QID、头像及三平台URL/user_id完整保留；但台视2025-08-25记本人仅经营Facebook、Instagram、Threads，故原YouTube官方性存在疑问，保留仅为历史数据，不背书。镜新闻澄清页面无法读取未用其摘要。',quotes=[dict(title=t,url=v) for t,v in sources])
out=root/'tmp/tw_batch6_enriched/TW-PERSON-000288.json';out.parent.mkdir(exist_ok=True)
jsonschema.validate(p,json.loads((root/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8-sig')))
out.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
print('jsonschema PASS',len(p['biography_summary']))

import json,pathlib
p=pathlib.Path('output/tw/2026-07-27/persons/TW-PERSON-000587.json'); d=json.loads(p.read_text(encoding='utf-8'))
d.update(name_en='Hsu, Hsin-Ying',gender='female',birth_date='1972-04-23',birth_place=None,current_positions=['第十一届立法委员（新竹县第一选举区）','中国国民党2026年新竹县长候选人'])
def edu(n,g,f=None):return dict(institution=n,degree=g,field=f,start_date=None,end_date=None)
d['education']=[edu('国立交通大学','doctorate','土木工程'),edu('国立交通大学','master','土木工程'),edu('国立成功大学','bachelor','测量工程'),edu('台北市立中山女子高级中学','high_school'),edu('新竹县立新丰国中','other'),edu('新竹县立山崎国小','primary')]
def work(n,t,s=None,e=None):return dict(organization=n,position=t,start_date=s,end_date=e,org_id='TW-GOV-020' if n=='立法院' else None)
d['work_experience']=[work('立法院','第十一届立法委员','2024-02-01'),work('立法院','第八届立法委员','2012-02-01','2016-01-31'),work('新竹县议会','第十六、十七届县议员','2006','2012'),work('明新科技大学','教师'),work('内政部地政司卫星测量中心','研究员'),work('大时代测量顾问有限公司','执业测量技师'),work('民国党','主席（历史职务）','2015','2018'),work('国会政党联盟','副主席（历史职务）','2019-06','2020-03')]
d['political_stances']=[dict(date='2026-10-04',topic='劳动与育儿',stance_content='主张育儿安心1小时，以县府补助鼓励企业为育有12岁以下子女者缩短每日工时而不减薪，另推动弹性工时及女性再就业支持；均为竞选主张。',source='https://www.cna.com.tw/news/aipl/202610040118.aspx'),dict(date='2026-10-16',topic='环境与防灾',stance_content='主张串联头前溪亲水廊道、整合污染监测并公开案件进度，按上中下游条件规划保水、滞洪及海绵城市；尚属政见。',source='https://www.cna.com.tw/news/aipl/202610160223.aspx'),dict(date='2026-11-05',topic='智慧交通',stance_content='主张建立AI交通治理中心、优先改善竹北瓶颈路口号志，整合县市交通数据，倡议200亿元交通治理基金；缩短通勤时间两成为目标，非实施效果。',source='https://www.cna.com.tw/news/aloc/202611050151.aspx')]
d['major_achievements']=[dict(date='2024-12-31',organization='立法院',achievement='任内政委员会召委期间参与国土计划法审议；院会集体三读将功能分区图公告期限由4年改为10年。她在三读后要求政府补足配套。此为集体立法结果，不代表其个人版本全部通过；农业权补偿条款未入法。')]
d['family_members']=[dict(person_id=None,name=n,relationship=r,industry_or_organization=o) for n,r,o in [('徐镜兰','father','曾任新竹县新丰乡长'),('简百合','mother','教育工作者'),('徐欣怡','sister',None),('徐世勋','brother',None)]]
d['person_relationships']=[dict(person_id='TW-PERSON-000037',person_name='宋楚瑜',relationship_type='associate',description='2016年总统、副总统选举搭档：宋楚瑜为总统候选人，徐欣莹为副总统候选人；限于该次选举合作。')]
r=json.loads(pathlib.Path('tmp/social_xlsx_20261116/records.json').read_text(encoding='utf-8'))
if isinstance(r,dict):
 print(r.keys())
else:
 for x in r:
  if x.get('name')=='徐欣莹':
   d['social_accounts'].append(dict(platform=x['platform'],account_name='徐欣莹',url=x['url'],source=8 if x['platform']=='instagram' else 6,user_id=x['raw_user_id'],username=x['key'][1],nickname=None,source_note=f"用户提供社交.xlsx，工作表{x['sheet']}行{x['row']}；USER-ID={x['raw_user_id']}；PAGE-ID={x['raw_page_id']}。未独立核实实时官方认证。"))
d['contacts']=[dict(type='phone',value='02-2358-6326',source='https://www.ly.gov.tw/Pages/List.aspx?nodeid=46797')]
d['biography_summary']='徐欣莹是台湾政治人物及测量工程专业人士，现任第十一届立法委员，代表新竹县第一选举区，党籍为中国国民党。她毕业于国立成功大学测量工程学系，取得国立交通大学土木工程硕士及博士学位，曾在内政部地政司卫星测量中心任研究员、担任执业测量技师及明新科技大学教师，随后进入地方议会，历任新竹县第十六、十七届县议员及第八届立法委员。其政治经历包含创立民国党并担任主席、2016年与宋楚瑜搭档参选副总统，以及担任国会政党联盟副主席等历史阶段；这些职务不作为当前身份。2024年她重返立法院，并曾在第十一届第二会期担任内政委员会召集委员。2026年以国民党新竹县长候选人身份参与选举，下半年陆续提出劳动、环境、交通与人工智慧治理政见。截至已核读的2026年11月5日活动报道，她仍为候选人，不能预写年底选举结果。'
urls=[('立法院徐欣瑩委员','https://www.ly.gov.tw/Pages/List.aspx?nodeid=46797'),('徐欣瑩旧官网认识欣瑩','https://www.shesinging.tw/singing2012/myfile.php?f=know.html'),('徐欣瑩维基生平','https://zh.wikipedia.org/wiki/徐欣瑩'),('劳工政见','https://www.cna.com.tw/news/aipl/202610040118.aspx'),('环境永续政见','https://www.cna.com.tw/news/aipl/202610160223.aspx'),('AI智慧交通政见','https://www.cna.com.tw/news/aloc/202611050151.aspx'),('国土法三读及个人发言','https://www.cna.com.tw/news/aipl/202412310183.aspx'),('国土计划法修正部分条文','https://www.ly.gov.tw/Pages/Detail.aspx?nodeid=33324&pid=248601')]
d['collection_meta']=dict(collection_date='2026-11-17',phase='phase4_person_profile',data_sources=['official_website','government_directory','news_search','wikipedia','other'],quotes=[dict(title=t,url=u) for t,u in urls],notes='已核读立法院、本人旧官网、中央社及维基原文。最新具体活动证据截至2026-11-05。英文依立法院明载。生日依历届官方名鉴检索线索及维基，出生地未交叉确认留空。家庭父母姐弟实名依本人旧官网单源收录，父亲另有维基交叉；不收健康等私密细节。历史任职无确切日期者留空，顾问等旧官网头衔未核当期不列现职。已尝试揭弊法、新住民基本法、国土计划法三读链，只确认国土法集体结果及其审议发言，第二项个人贡献未足不凑数。社交已提取records及workbook_raw，具名表关联非实时认证；官网图片外链尚未核成账号不冒收。关联宋楚瑜及立法院均已读真实画像确认。')
out=pathlib.Path('tmp/tw_batch8_enriched/TW-PERSON-000587.json');out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
import jsonschema
jsonschema.validate(d,json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')))
print('schema PASS',len(d['social_accounts']))

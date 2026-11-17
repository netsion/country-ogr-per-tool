import json,pathlib
p=pathlib.Path('output/tw/2026-07-27/persons/TW-PERSON-000588.json'); d=json.loads(p.read_text(encoding='utf-8'))
d.update(name_en='Chang, Chia-Chun',gender='female',birth_date='1981-01-10',birth_place='雲林縣土庫鎮',current_positions=['第11届全国不分区及侨居国外国民立法委员','中国国民党2026年云林县长候选人'])
d['education']=[dict(institution=a,degree=b,field=c,start_date=None,end_date=None) for a,b,c in [('国立政治大学','doctorate','国家发展研究'),('英国南安普敦大学','master','国际关系'),('英国伦敦大学','bachelor','企业管理'),('云林县私立正心高级中学','high_school',None),('云林县虎尾镇虎尾国民小学','primary',None)]]
d['work_experience']=[dict(organization=a,position=b,org_id=None,start_date=c,end_date=e) for a,b,c,e in [('立法院','第7、8届立法委员','2008-02-01','2016-01-31'),('立法院','第11届全国不分区立法委员','2024-02-01',None),('中国国民党云林县党部','第36任主任委员','2024-05-18','2025-12-13'),('吴凤技术学院','讲师',None,None),('中国国民党中央政策会','副执行长',None,None),('中国国民党','中央评议委员、中央常务委员（历史经历）',None,None),('云林县青埔教育基金会','董事长（履历所列）',None,None),('立法院台英国会议员联谊会','会长（历史经历）',None,None),('中华民国妇女联合会云林县分会','主任委员（履历所列）',None,None),('全國青工總會','总会长（历史经历）',None,None)]]
u='https://news.nextapple.com/politics/20260509/F9EAFEDD1EBF3DD16D0BC2D9F262C9AF'
d['political_stances']=[dict(date='2026-05-09',topic=a,stance_content=b,source=u) for a,b in [('品格教育','专访中主张将礼义廉耻带回校园，以感恩、自信与同理心作为竞争力核心；属于教育政策主张。'),('双语与数位教学','提出从小学一年级推动双语教育，运用既有平板、远端技术与人工智能辅助工具弥补师资不足；尚属规划。'),('公共交通','表示将关注斗六铁路高架化推动及高铁增班需求，并以倾听乡亲实际需要作为公共事务方向。')]]
d['major_achievements']=[dict(date='2024-07-15',achievement='担任宗教团体以自然人名义登记不动产处理暂行条例第五条修正草案的提案委员之一，其与吴琪铭、王美惠、林岱桦、陈亭妃等版本并案，经院会三读通过。此为集体立法成果，不表示个人版本全部获采或行政执行效果已核实。',organization='立法院'),dict(date='2025-05',achievement='张嘉郡等29人提出的殡葬管理条例第二十一条之一修正草案，与丁学忠、刘建国等多个版本并案，官方议案进度记载已三读并于5月22日咨请公布。属于参与并案立法成果，非个人独力完成，未据此宣称执行成效。',organization='立法院')]
d['family_members']=[dict(person_id=None,name='周柏吟',relationship='spouse',industry_or_organization='曾任地方政府官员')]
d['biography_summary']='张嘉郡是中国国民党籍政治人物，出生于云林县土库镇，曾就读虎尾国小及正心中学，赴英国学习企业管理及国际关系，后取得国立政治大学国家发展研究所博士学位。返台后曾任讲师及国会助理，随后投入云林公共事务，于2008年至2016年担任第7、8届立法委员，2024年以全国不分区身份重返立法院。她亦有国民党云林县党部主任委员、中央政策会副执行长及教育基金会等经历。2026年参加云林县长选举，中央选举委员会登记汇总表记载她于9月3日以国民党推荐身份登记；此处仅记录候选人身份，不预写选举结果。她在2026年专访提出品格教育、双语与数位教学以及交通改善主张。在国会工作方面，她参与宗教团体不动产登记及殡葬管理相关修法，均须理解为多个提案版本合并审议的集体立法成果。'
r=json.loads(pathlib.Path('tmp/social_xlsx_20261116/records.json').read_text(encoding='utf-8')); d['social_accounts']=[]
for x in r:
 if x.get('name')=='张嘉郡':
  d['social_accounts'].append(dict(platform=x['platform'],url=x['url'],account_name='張嘉郡',source={'instagram':8,'facebook':6}[x['platform']],username=x['key'][1],nickname=None,user_id=x['raw_user_id'],source_note=f"用户授权社交表工作表{x['sheet']}第{x['row']}行；未独立核实实时官方认证；PAGE-ID={x.get('raw_page_id')}。Facebook另见国民党人物页实名外链。"))
qs=[('国民党张嘉郡履历','https://www1.kmt.org.tw/people.aspx?mid=38&pid=2382'),('张嘉郡专访',u),('张嘉郡履历及历史经历','https://zh.wikipedia.org/wiki/張嘉郡'),('2026候选人登记汇总表','https://www.cec.gov.tw/api/file/370f3bbf-6408-4fdc-b8d8-9b9214913f74.pdf'),('宗教团体不动产处理修法三读','https://ppg.ly.gov.tw/ppg/bills/203110056840000/details'),('殡葬管理条例并案三读','https://ppg.ly.gov.tw/ppg/bills/203110110210000/details')]
d['collection_meta']=dict(collection_date='2026-11-17',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia','government_registry','other'],quotes=[dict(title=t,url=v) for t,v in qs],notes='身份活动证据截至2026-09-03候选人登记，专访截至2026-05-09；未确认更近公务活动。中央社2026年10月两页虽打开但仅返回导航无正文，替代转载亦不可读，未据摘要采纳政策。英文名由国民党正式人物页确认。生日与配偶专访及维基交叉；配偶职业仅维基单源。父亲张荣味、姑姑张丽善及弟弟资料仅维基实名，未补足可靠报道故不收确定家庭关系；无据不收政治盟友。学历及历史经历综合正式党页、专访及维基，任职日期不详留空，部分历史职务无当期确认。两项修法官方已证提案及集体三读，未核执行效果及个人条文采纳程度。头像、QID不另猜填。已实际提取社交表具名记录USER和PAGE字段；不同字段不视为冲突。')
o=pathlib.Path('tmp/tw_batch8_enriched/TW-PERSON-000588.json');o.parent.mkdir(exist_ok=True);o.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
import jsonschema
jsonschema.validate(d,json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')))
print('jsonschema PASS')

import json,pathlib
p=pathlib.Path('output/tw/2026-07-27/persons/TW-PERSON-000577.json'); d=json.loads(p.read_text(encoding='utf-8-sig'))
d.update(name_en='WU,PEI-YI',gender='female',aliases=['吴沛忆'],current_positions=['第十一届立法委员（台北市第五选举区）','民主进步党台北市党部主任委员'],birth_date='1987-01-20',birth_place='基隆市')
d['education']=[dict(institution=i,degree=g,field=f,start_date=None,end_date=None) for i,g,f in [('国立清华大学','master','社会学'),('国立台湾大学','bachelor','政治学系政治理论组'),('台北市立景美女子高级中学','high_school',None)]]
w=[('2024-02-01',None,'立法院','第十一届立法委员'),('2018-12-25','2024-01-31','台北市议会','第十三、十四届议员'),(None,None,'美国国务院','国际领袖计划台湾代表'),(None,None,'新境界文教基金会','文化政策咨询委员'),('2016',None,'蔡英文总统竞选总部','媒体创意中心副主任'),(None,None,'民主进步党','发言人'),(None,None,'民主进步党台湾民主学院','主任'),(None,None,'台北市体育总会','理事'),(None,None,'东园球类运动推广协会','荣誉理事长'),('2026',None,'民主进步党台北市党部','主任委员')]
d['work_experience']=[dict(start_date=a,end_date=b,organization=c,position=e,org_id=None) for a,b,c,e in w]
s1='https://www.cna.com.tw/news/aipl/202501080096.aspx';s2='https://sports.ltn.com.tw/news/breakingnews/5480764';s3='https://www.pridewatch.tw/candidate/pei-yi'
d['political_stances']=[dict(date='2025-01-08',topic='宪法救济',stance_content='要求维持宪法法庭运作，支持行政院对宪法诉讼法修正案提出覆议，强调人民基本权利及婚姻平权需要司法救济保障。',source=s1),dict(date='2026-06-23',topic='体育治理与性别平等',stance_content='提案推动体育单项协会理监事任一性别比例不得少于三分之一，以扩大各性别参与运动决策。',source=s2),dict(date='2022-05-31',topic='月经平权',stance_content='要求国中女性生理用品补助纳入卫生棉条，让学生按需求选择；并提案将月经友善纳入友善店家计划。',source=s3)]
d['major_achievements']=[dict(date='2026-06-23',organization='立法院',achievement='参与提案的国民体育法第二条及第三十九条修正草案经并案审查后三读；通过体育团体理监事任一性别至少三分之一的规定，属跨提案共同立法成果，并非个人独力完成。'),dict(date='2025-05-09',organization='立法院',achievement='所提律师法第九条修正草案参与并案审查，院会三读补足未加入公会者律师证书废止规范；最终采用钟佳滨等人修正动议，内容与行政院版本接近，不将最终条文归为她个人版本。')]
d['family_members']=[dict(person_id=None,name='许家蓓',relationship='other',industry_or_organization='台北市议会前议员（已故伴侣；未据此认定法律婚姻）')]
d['person_relationships']=[dict(person_id=None,person_name='黄捷',relationship_type='associate',description='2026年5月24日公开宣布以北高连线共同推动地方党务革新；限定为该项公开合作。'),dict(person_id='TW-PERSON-000002',person_name='蔡英文',relationship_type='superior',description='2016年总统竞选期间任蔡英文竞选总部媒体创意中心副主任，限定为候选人与竞选幕僚关系。')]
raw=json.loads(pathlib.Path('tmp/social_xlsx_20261116/workbook_raw.json').read_text(encoding='utf-8-sig')); d['social_accounts']=[]
for sh in raw:
 for r in sh['rows']:
  c={v['col']:v['value'] for v in r['cells']}
  if c.get(2)=='吴沛忆':
   plat=c[3];url=c[4];d['social_accounts'].append(dict(platform=plat,url=url,account_name='吳沛憶',source={'youtube':9,'threads':24,'instagram':8,'facebook':6}[plat],user_id=c.get(5),username='Pay1Pay1' if plat=='facebook' else 'pay1pay1',nickname=None,source_note=f'用户社交.xlsx工作表{sh["sheet"]}第{r["row"]}行；USER-ID列原值保留；未独立核实实时官方认证。'+('PAGE-ID列另为'+str(c.get(6)) if plat=='facebook' else '')))
d['contacts']=[dict(type='phone',value='02-2358-6166',source='https://www.ly.gov.tw/Pages/List.aspx?nodeid=46766')]
d['biography_summary']='吳沛憶是台湾民主进步党政治人物，成长于基隆，大学就读台湾大学政治学系政治理论组，后取得清华大学社会学硕士学位。学生时期参加公共事务与学生运动，参与野草莓运动。她曾任民进党发言人、台湾民主学院主任及蔡英文总统竞选团队幕僚，随后投入台北市中正、万华地区地方政治，连续担任第十三及第十四届台北市议员。2024年起担任台北市第五选举区立法委员，进入教育及文化委员会，持续关心文化发展、体育治理、教育及多元性别权益。2026年当选民进党台北市党部主委，与黄捷提出北高连线合作推动党务。其公开政策工作包括体育团体性别比例修法及律师资格管理修法，相关成果均由立法院集体审议完成。2026年9月报道确认她卸下党团副书记长职务，转向地方辅选，不能继续将该党团职务列为现职。'
urls=[('立法院吳沛憶委员','https://www.ly.gov.tw/Pages/List.aspx?nodeid=46766'),('吳沛憶前进国会','https://www.cna.com.tw/news/aipl/202401130302.aspx'),('北高连线党务革新','https://www.cna.com.tw/news/aloc/202605240184.aspx'),('卸党团干部','https://www.ftvnews.com.tw/news/detail/2026930w0154'),('国体法并案三读','https://ppg.ly.gov.tw/ppg/bills/203110219750000/details'),('国体法性别比例',s2),('律师法三读','https://www.cna.com.tw/news/aipl/202505090206.aspx'),('宪法法庭救济',s1),('候选人性别政策',s3),('公开伴侣','https://news.tvbs.com.tw/politics/2623853'),('公开伴侣牵手照','https://www.mnews.tw/story/20240919nm013')]
d['collection_meta']=dict(collection_date='2026-11-16',phase='phase4_person_profile',data_sources=['official_website','news_search','other'],quotes=[dict(title=t,url=u) for t,u in urls],notes='全文核读立法院、中央社、民视、自由时报、TVBS、镜新闻、PrideWatch等独立来源。实际活动证据截止2026-09-30；现行立院页列第六会期但不以导航推断活动。党部主委当选有中央社报道，具体交接日未核不猜填。历史经历除市议员及竞选年份外多未载任期，null不代表现职。出生资料据维基与选举资料库，未再核原始户籍。公开伴侣由TVBS与镜新闻交叉，关系非法律婚姻；其他家庭实名未核。新境界等组织引用ID留空。律师法成果目前中央社单源，未核执行成效；国体法有议案进度和新闻双源。未将两项立法说成个人独力成果。社交资料取用户表具名行及USER列，PAGE另记；平台实时认证未核。报导者逐字稿抓取失败不作事实来源。')
out=pathlib.Path('tmp/tw_batch7_enriched/TW-PERSON-000577.json');out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
import jsonschema
jsonschema.validate(d,json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8-sig')))
print('JSONSCHEMA PASS')

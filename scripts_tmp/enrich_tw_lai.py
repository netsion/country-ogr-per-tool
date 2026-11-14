import json,pathlib
p=pathlib.Path('output/tw/2026-07-27/persons/TW-PERSON-000001.json')
x=json.loads(p.read_text(encoding='utf-8-sig'))
s=json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))
x={k:v for k,v in x.items() if k in s['properties']}
x['name']='賴清德';x['name_zh']='赖清德';x['aliases']=list(dict.fromkeys(x.get('aliases',[])+['赖清德']))
x['current_positions']=['台湾地区领导人','民主进步党主席']
x['birth_place']='台湾新北万里'
x['person_relationships']=[]
x['education']=[{'institution':'台湾大学（國立臺灣大學）','degree':'bachelor','field':'复健医学','start_date':None,'end_date':None},{'institution':'成功大学（國立成功大學）','degree':'professional','field':'学士后医学','start_date':None,'end_date':None},{'institution':'哈佛大学（Harvard University）','degree':'master','field':'公共卫生','start_date':None,'end_date':None}]
def w(a,b,o,t,i=None):return dict(start_date=a,end_date=b,organization=o,position=t,org_id=i)
x['work_experience']=[w('1996','1999','国民大会（國民大會）','国民大会代表'),w('1999','2010','立法院','立法委员','TW-GOV-020'),w('2010','2017','台南市政府（臺南市政府）','市长'),w('2017','2019','行政院','院长','TW-GOV-019'),w('2020-05-20','2024-05-20','总统府（總統府）','台湾地区副领导人'),w('2023-01-18',None,'民主进步党（民主進步黨）','主席','TW-PARTY-012'),w('2024-05-20',None,'总统府（總統府）','台湾地区领导人')]
x['biography_summary']='赖清德，1959年出生于台湾新北万里，具有医师及公共卫生教育背景。先后就读台湾大学复健医学系、成功大学学士后医学系，并取得哈佛大学公共卫生硕士学位。早年从事医疗工作，1994年参与公共事务，1996年当选国民大会代表，随后转入民意代表工作，1999年至2010年担任立法委员，关注卫生与社会福利议题。2010年当选台南市升格后的首任市长，2014年连任；2017年至2019年担任行政院院长。2020年起担任台湾地区副领导人，2023年出任民主进步党主席。2024年与萧美琴搭档参加选举并当选，5月20日就任台湾地区领导人。其公开施政议题涉及公共卫生、产业发展、能源转型与防卫韧性。本档将历史任职从现职栏分离，履历日期仅保留已确认精度。'
x['political_stances']=[dict(date='2026-09-28',topic='无人机产业与供应链',stance_content='在民雄航太暨无人机产业园区动土活动中主张持续投入资源，并与民主伙伴合作建设更安全、更有韧性的无人机供应链。',source='https://www.president.gov.tw/Page/694')]
x['major_achievements']=[dict(date='2024-01-13',achievement='与萧美琴搭档赢得2024年台湾地区领导人选举，获5,586,019票，得票率40.05%。',organization='总统府（總統府）')]
x['profile']={k:v for k,v in (x.get('profile') or {}).items() if k in s['properties']['profile']['properties']}
for a in x['social_accounts']:a['source_note']='原Wikidata档案保留；本轮搜索见X ChingteLai及其Facebook chingte互链摘要，其他账号及平台ID未重新核验。'
x['collection_meta']=dict(collection_date='2026-11-13',phase='phase4_person_profile',data_sources=['official_website','wikipedia','news_search','web_search'],notes='本轮新核实：官方履历与中央社人物专题交叉核对教育、出生地和历任职务；官方页面、Wikipedia及中央社交叉核对领导人身份，选举结果以中央社原文和官方履历确认。三个独立机构来源为总统府、Wikipedia、中央社。学校起止年未知留空；履历多数日期按官方年精度，主席就任日参考Wikipedia。社交搜索覆盖Facebook、X、Instagram、LinkedIn、TikTok、YouTube；仅X及Facebook互链摘要有结果，未将摘要当全文核实，保留原账号、头像和ID但未声称本轮复核。未重新核验家庭信息。TIME目标URL返回不相关PMI内容，排除其作为证据。来源页面可见2026年9月至11月内容，现职按采集时页面表述记录。',quotes=[dict(title=t,url=u) for t,u in [('总统府：赖清德简介','https://www.president.gov.tw/Page/694'),('Lai Ching-te — Wikipedia','https://en.wikipedia.org/wiki/Lai_Ching-te'),('中央社：赖清德人物专题','https://www.cna.com.tw/topic/newstopic/4282.aspx'),('中央社：赖萧配当选','https://www.cna.com.tw/news/aipl/202401140007.aspx')]])
out=pathlib.Path('tmp/tw_enrichment');out.mkdir(parents=True,exist_ok=True)
(out/p.name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

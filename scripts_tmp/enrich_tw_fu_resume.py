import pathlib,json,sys,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';x=json.loads((B/'persons/TW-PERSON-000141.json').read_text(encoding='utf-8'))
x['current_positions']=['第11届立法委员','中国国民党立法院党团总召集人']
x['education']=[dict(institution='淡江大学（淡江大學）',degree='master',field='中国大陆研究',start_date=None,end_date=None)]
def w(a,b,o,p,oid=None):return dict(start_date=a,end_date=b,organization=o,position=p,org_id=oid)
x['work_experience']=[w('2002-02-01','2009-12-20','立法院','立法委员','TW-GOV-020'),w('2009-12-20','2018-09-12','花莲县政府（花蓮縣政府）','县长'),w('2020-02-01',None,'立法院','立法委员','TW-GOV-020'),w('2024-02-01',None,'中国国民党立法院党团（中國國民黨立法院黨團）','总召集人')]
u=['https://www.ly.gov.tw/Pages/List.aspx?nodeid=46824','https://www.cna.com.tw/news/aipl/202601020058.aspx','https://www.cna.com.tw/news/aipl/202407160094.aspx','https://news.ipcf.org.tw/127212','https://www.ly.gov.tw/Pages/Detail.aspx?nodeid=54301&pid=240965','https://www.cna.com.tw/news/firstnews/201911260117.aspx','https://zh.wikipedia.org/wiki/傅崐萁']
x['political_stances']=[dict(date='2024-06-03',topic='东部交通建设',stance_content='主张推动花东快速道路、国道六号东延及环岛高铁相关特别条例；为建设倡议，不认定工程或法案已完成。',source=u[3]),dict(date='2024-06-05',topic='党内协商与立法程序',stance_content='主张争议法案先经党内讨论、形成共识及党团协商，再决定推动。',source=u[4]),dict(date='2024-07-16',topic='区域交通平权',stance_content='要求中央重视东部交通需求；同时表示当会期不再正面推动环岛高铁及国六延伸两案，保留进一步沟通时间。',source=u[2])]
x['major_achievements']=[dict(date='2024-02-01',achievement='就任第11届花莲县选区立法委员；为取得公职授权的结果，不等同施政成效。来源立法院个人页面。',organization='立法院'),dict(date='2026-01-02',achievement='国民党团大会以同额竞选及鼓掌方式通过其续任总召；这是党团选任结果，不是花东交通建设已经实现。来源中央社当日报道。',organization='中国国民党立法院党团（中國國民黨立法院黨團）')]
x['person_relationships']=[]
x['family_members']=[dict(person_id=None,name='徐榛蔚（徐榛蔚）',relationship='spouse',industry_or_organization='公开政治人物；中央社及维基确认配偶身份，仅记录最小关系信息。')]
x['biography_summary']='傅崐萁是台湾地区政治人物，现为第11届花莲县选区立法委员，并担任中国国民党立法院党团总召集人。立法院官方履历列有淡江大学中国大陆研究所硕士学历，以及第5、6、7、10、11届立法委员和第16、17届花莲县长经历。他于2009年底担任花莲县长，2018年结束该职务，2020年重返立法院，2024年续任第11届委员；旧档县长头衔不再作为现职。其议会活动涉及区域建设、党团协商和立法程序，公开推动花东快速道路、国道六号东延及环岛高铁相关倡议。上述建设具有财政、环境和可行性争议，本档只记录具体发言日期与立场，不把提案或政治承诺写为完成工程。2026年1月中央社原文记录国民党团通过其续任总召。家庭栏仅保留公开配偶徐榛蔚身份，不扩展其他私人资料。'
x['collection_meta']=dict(collection_date='2026-11-14',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia'],quotes=[dict(title=t,url=url) for t,url in zip(['立法院傅崐萁委员履历','中央社2026续任总召','中央社花东交通发言','原视花东交通三法','立法院转载党内协商报道','中央社公开配偶辅选报道','维基傅崐萁履历'],u)],notes='现职依据立法院第6会期资料与中央社2026续任报道，不逐日宣称核实至采集日。学历采官方硕士，未采扩展博士说法；早期精确任期和出生日期仍维基单源。三个独立来源体系为立法院、中央社、原视，维基辅助；立院转载更生日报不视为独立官方调查。公开配偶由中央社和维基确认，无对应人物画像故ID为空。人物合作关系缺足够稳定语义证据保持空，不按同场出席推断盟友。原头像和Facebook账号/user_id保留，多平台检索未确认其他本人账号，不新增。成就只记录公职与党团选任，不把建设倡议当成果。')
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
(R/'tmp/tw_batch2_enriched/TW-PERSON-000141.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];b=R/'output/tw/2026-07-27';x=json.loads((b/'persons/TW-PERSON-000136.json').read_text(encoding='utf-8'))
u=['https://www.yunlin.gov.tw/News_Content.aspx?n=1244&s=437788','https://www.cna.com.tw/news/aloc/202504060108.aspx','https://news.tvbs.com.tw/politics/1867978','https://zh.wikipedia.org/wiki/張麗善']
x['name']='張麗善';x['current_positions']=['云林县县长']
x['education']=[dict(institution='虎尾科技大学（國立虎尾科技大學）',degree='bachelor',field='工业管理',start_date=None,end_date=None)]
def w(s,e,n,p,i=None):return dict(start_date=s,end_date=e,organization=n,position=p,org_id=i)
x['work_experience']=[w('2005','2008','立法院','第6届立法委员','TW-GOV-020'),w('2016','2018','立法院','第9届立法委员','TW-GOV-020'),w('2018-12-25',None,'云林县政府（雲林縣政府）','县长')]
x['political_stances']=[dict(date='2025-04-06',topic='农产品市场多元化',stance_content='主张拓展日本及东南亚通路，降低农产品外销对单一市场的依赖；为当时政策方向，不计预估订单为实际收入。',source=u[1]),dict(date='2023-11-24',topic='冷链与农业加值',stance_content='支持县府与企业合作建设冷链理货包装通路，提升蔬果保鲜及外销竞争力；不把预期效果当独立评估。',source=u[0]),dict(date='2022-08-07',topic='地方治理问责',stance_content='受访表示接受以选举检验施政、以平常心面对连任挑战；记录其公开问责主张，不等同满意度事实。',source=u[2])]
x['major_achievements']=[dict(date='2023-11-24',achievement='任内县府合作的宜捷威大型蔬果理货包装场启用；设施由企业及县府等共同推动，非个人独力成果，依据县府发布。',organization='云林县政府（雲林縣政府）'),dict(date='2025-03',achievement='率县府及业者参加东京食品展，为已发生外销推广活动；中央社引述厂商预估订单不作为已实现销售额。',organization='云林县政府（雲林縣政府）')]
x['family_members']=[dict(person_id=None,name='张荣味（張榮味）',relationship='brother',industry_or_organization='前云林县长；TVBS与维基确认兄妹关系，仅记录公开政治家庭身份。')]
x['person_relationships']=[]
x['biography_summary']='张丽善是台湾地区政治人物，现任云林县县长，曾任第六届及第九届立法委员。她早期具有护理工作背景，后来转入社会服务及民意代表工作，2018年底就任云林县长，2022年获得连任。本档将立法委员等历史任职与县长现职分开，不提前采用2026年底换届结果。其公开施政方向包括农产品冷链、市场多元化和地方产业加值。县府与企业合作的理货包装设施启用及赴食品展推广属于具体已发生事项，但不能直接归为个人独力成果，也不能把预估订单等同销售收入。其兄张荣味曾任云林县长，关系由公开媒体原文及履历交叉确认，仅记录必要身份，不扩展私人财产、地址或其他家庭信息。社交账号与头像保留原档，本轮未声称全部重新认证。'
x['collection_meta']=dict(collection_date='2026-11-14',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia'],quotes=[dict(title=t,url=v) for t,v in zip(['云林县府冷链包装场启用','中央社农产品外销报道','TVBS人物专访与兄妹关系','维基张丽善履历'],u)],notes='县长现职有县府及新闻支持，但最近独立正文为2025年4月，未逐日核至采集日。学历及早期任期主要依维基；师大硕士与早期公报肄业记载存在时点差异，本轮未纳入该学位。出生日期沿用维基精确值。兄妹关系TVBS与维基交叉；无对应画像ID则留空。县长简介403未采。原头像及两个账号/user_id完整保留，多平台检索未确认新的本人账号。成就明确团队与活动性质，不当经济效果。')
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
p=R/'tmp/tw_batch3_enriched/TW-PERSON-000136.json';p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

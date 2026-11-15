import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';pid='TW-PERSON-000156';x=json.loads((B/'persons'/f'{pid}.json').read_text(encoding='utf-8'))
x.update(name='謝龍介',current_positions=['第11届立法委员','立法院教育及文化委员会委员'])
x['education']=[dict(institution='成功大学（國立成功大學）',degree='master',field='高阶管理',start_date=None,end_date=None)]
def w(a,b,o,p,oid=None):return dict(start_date=a,end_date=b,organization=o,position=p,org_id=oid)
x['work_experience']=[w('2002','2022','台南市议会（臺南市議會）','市议员'),w('2024-02-01',None,'立法院','第11届不分区立法委员','TW-GOV-020')]
x['political_stances']=[dict(date='2022-11-04',topic='校园供餐',stance_content='竞选期间主张营养午餐免费，记录当时政见，不等同已实施。',source='https://news.pts.org.tw/article/607924'),dict(date='2022-11-04',topic='长者医疗负担',stance_content='主张补助长者健保费，属竞选倡议而非已经完成的市政措施。',source='https://news.pts.org.tw/article/607924'),dict(date='2024-06-15',topic='国会职权修法沟通',stance_content='支持向民众说明国会职权修法过程与意旨，并与反对意见比较；仅记录本人政治立场，不作为法案效力的法律结论。',source='https://news.pts.org.tw/article/700269')]
x['major_achievements']=[dict(date='2024-02-01',achievement='就任第11届不分区立法委员；仅记录公职授权，不把提案或竞选承诺认定为立法成果。',organization='立法院')]
x['family_members']=[dict(person_id=None,name='李佳芬（李佳芬）',relationship='spouse',industry_or_organization='谢龙介配偶；中央社与TVBS确认。与韩国瑜配偶李佳芬是同名不同人，禁止合并或复用其人物ID。')]
x['person_relationships']=[]
x['biography_summary']='谢龙介是台湾地区政治人物，现为第11届不分区立法委员。立法院个人简介列有成功大学高阶管理硕士学历，并记载其担任台南市议员、国民党党务及竞选发言人的经历。其早期政治经历包括基层里长与地方议会工作，2024年进入立法院。当前官方第6会期名录列为教育及文化委员会委员，早期司法及法制委员会经历仅属过去会期，不继续当作现职。2022年参与台南市长选举时提出校园免费营养午餐和长者健保补助等政见，2024年亦参加国会职权修法的公开宣讲。这些主张与已通过或实施的制度分别记录，未将选举承诺视为完成成果。其公开配偶李佳芬与韩国瑜配偶同名，独立新闻原文明确区分两人，因此家庭关系保持未知人物ID，不凭姓名链接。'
urls=[('立院第11届谢龙介个人名录','https://www.ly.gov.tw/Pages/List.aspx?nodeid=46852'),('公视2022台南市长政见','https://news.pts.org.tw/article/607924'),('公视2024国会修法宣讲','https://news.pts.org.tw/article/700269'),('中央社两名配偶同名报道','https://www.cna.com.tw/news/aloc/201901280116.aspx'),('TVBS谢龙介补选报道确认配偶','https://news.tvbs.com.tw/politics/1100237'),('维基谢龙介履历','https://zh.wikipedia.org/wiki/謝龍介')]
x['collection_meta'].update(collection_date='2026-11-14',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia'],quotes=[dict(title=t,url=u) for t,u in urls],notes='现职依据立院第6会期个人名录；未把2026市长参选当已当选，也不沿用早期司法法制委员。早期任期及出生日期仍有维基单源边界；具体制度成果归因不足，未凑第二项。配偶由中央社与TVBS原文交叉，明确与韩国瑜配偶同名不同人，ID留null。人物关系未取得足够直接合作原文保持空。已检索社交平台，原三个账号、user_id和头像保留，不宣称全部重新平台认证。')
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
(R/'tmp/tw_batch3_enriched'/f'{pid}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';pid='TW-PERSON-000039';x=json.loads((B/'persons'/f'{pid}.json').read_text(encoding='utf-8'))
official='https://www.ly.gov.tw/Pages/List.aspx?nodeid=46793';pts='https://news.pts.org.tw/article/796253';wiki='https://zh.wikipedia.org/wiki/柯建銘'
x.update(name='柯建銘',current_positions=['第11届立法委员'])
x['education']=[dict(institution='中山医学院（中山醫學院）',degree='bachelor',field='牙医学',start_date=None,end_date=None)]
def w(s,e,o,p,i=None):return dict(start_date=s,end_date=e,organization=o,position=p,org_id=i)
x['work_experience']=[w('1993-02-01','2024-01-31','立法院','第2至10届立法委员','TW-GOV-020'),w('2024-02-01',None,'立法院','第11届立法委员','TW-GOV-020'),w('2000','2026-02-24','民主进步党立法院党团（民主進步黨立法院黨團）','总召集人'),w('2004-12-11','2005-01-15','民主进步党（民主進步黨）','代理主席','TW-PARTY-012'),w('2011-03-11','2011-04-27','民主进步党（民主進步黨）','代理主席','TW-PARTY-012')]
x['political_stances']=[dict(date='2026-02-24',topic='朝野协作',stance_content='卸任总召时主张朝野和解，并支持行政部门施政。',source=pts),dict(date='2026-02-24',topic='国会改革',stance_content='公视回顾其反对蓝白国会改革版本的立场；此为本人政治评价，不是对法案效力的法律结论。',source=pts),dict(date='2026-02-24',topic='防卫特别立法',stance_content='公视回顾其支持海空战力提升特别条例，并批评在野党反对；并非本次提出新法案。',source=pts)]
x['major_achievements']=[dict(date='2024-02-01',achievement='就任第11届不分区立法委员，属取得公职授权，不等同所有法案均个人完成。来源立院履历。',organization='立法院'),dict(date='2026-02-24',achievement='结束长期党团总召任期并交接予蔡其昌；本项为制度交接记录，不将卸任本身评价为施政绩效。来源公视报道。',organization='民主进步党立法院党团（民主進步黨立法院黨團）')]
x['person_relationships']=[dict(person_id=None,person_name='蔡其昌（蔡其昌）',relationship_type='colleague',description='2026年2月24日党团总召交接关系；蔡其昌接任，非推断私人或长期派系联盟。来源公视。')]
x['family_members']=[dict(person_id=None,name='林道春（林道春）',relationship='spouse',industry_or_organization='维基公开配偶信息；单一来源，未扩展子女或其他私事。')]
x['biography_summary']='柯建铭是台湾地区政治人物，民主进步党籍立法委员，具有牙医教育和职业背景。立法院第11届委员官方简介记载其毕业于中山医学院牙医学系，曾任第2至第10届立法委员，并历任党团总召、副总召、干事长等职务，也曾代理民主进步党主席。2024年2月1日出任第11届全国不分区及侨居外国国民选区立法委员，官方资料列其第6会期参加司法及法制委员会。2026年2月24日党团改选由蔡其昌接任总召，公视报道其完成交接并呼吁朝野和解。因此，本档不把过去党主席代理职务或总召职务继续列作现职。其议会工作涉及跨党协商、行政立法沟通与法案攻防，立场记录保留报道日期和语境，不把政治评价视作司法结论，也不把团队立法成果全部归给个人。家庭仅留公开配偶最小身份，单源边界及未充分确认资料均在采集说明标注。'
x['collection_meta'].update(collection_date='2026-11-14',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia'],quotes=[{'title':'立法院第11届柯建铭委员简介','url':official},{'title':'公视：2026年柯建铭卸任党团总召','url':pts},{'title':'维基百科：柯建铭履历及家庭','url':wiki}],notes='现职按立院第6会期与公视卸任报道；学历官方及维基交叉，早期精确任期与配偶仍维基单源。配偶非双来源确认，保持最小信息；未扩展子女。中央社政策链接仅正文壳，未凭摘要写入。政策均是公视当日报道或历史回顾，非2026新法案；尚缺逐项立法成果独立归因，不用荣誉或政绩凑数。社交媒体搜索仅发现既有Facebook/YouTube，原user_id和头像全部保留；未新增未认证账号。蔡其昌未找到对应本地画像，人物ID为空。')
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
p=R/'tmp/tw_batch2_enriched'/f'{pid}.json';p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
print(p)

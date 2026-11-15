import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';x=json.loads((B/'persons/TW-PERSON-000111.json').read_text(encoding='utf-8'))
u='https://ppg.ly.gov.tw/ppg/SittingAttachment/download/2024070572/01025409037200772002.pdf'
x['current_positions']=['第11届立法委员','立法院内政委员会委员']
x['education']=[dict(institution='青年高级中学（青年高級中學）',degree='high_school',field=None,start_date=None,end_date=None)]
x['work_experience']=[dict(organization='立法院',org_id='TW-GOV-020',position='第5至第10届立法委员',start_date='2002-02-01',end_date='2024-01-31'),dict(organization='立法院',org_id='TW-GOV-020',position='第11届立法委员',start_date='2024-02-01',end_date=None)]
x['political_stances']=[dict(date='2024-07-08',topic='原住民立委出缺补选',stance_content='内政部向委员会报告记载其提案主张原住民立委缺额应比照区域立委立即补选；这是提案主张，不代表已通过。',source=u)]
x['major_achievements']=[dict(date='2024-02-01',achievement='就任第11届山地原住民选区立法委员；仅记录公职授权，不将具体议案或施政效果归为个人完成。',organization='立法院')]
x['person_relationships']=[];x['family_members']=[]
x['biography_summary']='高金素梅是台湾地区政治人物，曾从事演艺工作，2002年起进入立法院。立法院第11届官方名录记载她为山地原住民选举区委员，学历列青年高级中学，历任第5至第10届立法委员，并列有公益基金会相关经历。当前第6会期所属内政委员会，召集委员头衔仅见第1会期，不能当作持续现职。其公共议题包括原住民选举制度及权利保障，2024年内政部报告记载她提出原住民立委出缺立即补选的修法主张，但本轮未取得该案最终通过及施行证据，因此不作为已完成立法成果。公开名录将其党籍与参与党团分别列示，本档不据此推断私人关系或其他政治结盟。家庭资料缺少充分交叉原文，保持空值；本轮没有收录健康、传闻及其他不必要私人事项。'
x['collection_meta']=dict(collection_date='2026-11-14',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia'],quotes=[dict(title='立院第11届高金素梅个人名录',url='https://www.ly.gov.tw/Pages/List.aspx?nodeid=46801'),dict(title='内政部2024年7月8日选罢法修正草案报告',url=u),dict(title='公视2026年6月报道（仅核公开立委身份）',url='https://news.pts.org.tw/article/812075'),dict(title='维基高金素梅履历',url='https://zh.wikipedia.org/wiki/高金素梅')],notes='现职依据立院第6会期名录与2026公视交叉；第1会期召委不沿用。政策只一项有明确原文日期，不凑三项；具体立法成果归因不足，只记录公职结果。早期任期与出生日期有维基单源边界。家庭关系缺多源证据保持空，不收录传闻、健康及财产。公视所述案件属于未定罪司法程序，不作为定罪事实或关系推断。原头像及三社交账号/user_id全保留，多平台检索未确认新账号；索引立法院已核真实画像。')
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
p=R/'tmp/tw_batch3_enriched/TW-PERSON-000111.json';p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

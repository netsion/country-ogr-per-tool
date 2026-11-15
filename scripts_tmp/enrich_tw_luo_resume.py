import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];b=R/'output/tw/2026-07-27';x=json.loads((b/'persons/TW-PERSON-000163.json').read_text(encoding='utf-8'))
wiki='https://zh.wikipedia.org/wiki/羅智強'; ccw='https://ccw.org.tw/assess/45/legislator/465';pts='https://news.pts.org.tw/article/767408';nt='https://newtalk.tw/news/view/2026-08-20/1054533'
x['name']='羅智強';x['current_positions']=['第11届立法委员']
x['education']=[dict(institution='政治大学（國立政治大學）',degree='master',field='法律',start_date=None,end_date=None)]
def w(s,e,o,p,oid=None):return dict(start_date=s,end_date=e,organization=o,position=p,org_id=oid)
x['work_experience']=[w('2010-03-01','2011-05-04','总统府（總統府）','发言人','TW-GOV-023'),w('2012','2013','总统府（總統府）','副秘书长','TW-GOV-023'),w('2018','2022','台北市议会（臺北市議會）','议员'),w('2024-02-01',None,'立法院','第11届立法委员','TW-GOV-020')]
x['political_stances']=[dict(date='2024',topic='都市更新与居住',stance_content='公督盟所列政见主张加快都市更新和危老重建修法，以提高更新意愿；此为倡议，不视为修法已完成。',source=ccw),dict(date='2024',topic='长期照顾',stance_content='所列政见主张减轻长照家庭税负、提供照顾者津贴及改善照护移工申请制度；不作为已实施成果。',source=ccw),dict(date='2026-08-20',topic='教师工作环境',stance_content='主张提高待遇、增加行政支援、设学校律师与教权保障制度，以回应缺师问题；属政策建议。',source=nt)]
x['major_achievements']=[dict(date='2024-01-13',achievement='当选第11届台北市第六选区立法委员；仅记录选举结果，具体票数未独立核验而不收录。',organization='立法院'),dict(date='2018',achievement='当选台北市议员；属取得公职授权，不等同所有市政倡议已实现。来源维基履历。',organization='台北市议会（臺北市議會）')]
x['person_relationships']=[]
x['family_members']=[dict(person_id=None,name='黄雪玲（黃雪玲）',relationship='spouse',industry_or_organization='仅记录公开配偶身份，维基单源待独立核验。')]
x['biography_summary']='罗智强是台湾地区政治人物，现任第11届台北市第六选区立法委员，具有政治大学法律硕士学历。其职业经历涉及政治传播、政府幕僚、地方议会与中央立法机关。早年参与辩论及公共事务，曾担任总统府发言人、副秘书长，之后参与政党事务及地方选举，2018年当选台北市议员，2022年辞去议员职位，2024年当选立法委员。本档将上述历史职务与现任立委分开，不再沿用旧档中的市议员与总统府发言人作为现职。公开政策议题包括都市更新、长期照顾、教师工作环境及议会监督。2025年宣布参选国民党主席时曾提出支持卢秀燕的选举安排，此为当时有条件的政治主张，不代表双方形成固定联盟，也不代表其当选党主席。已收录成果限于可核的公职选举结果，不将提案及竞选承诺包装成已经通过或执行的法律。'
x['collection_meta']=dict(collection_date='2026-11-14',phase='phase4_person_profile',data_sources=['news_search','official_website','wikipedia'],quotes=[{'title':t,'url':u} for t,u in [('公督盟：罗智强履历与政见',ccw),('公视：罗智强参选党主席发言',pts),('Newtalk：教师政策发言',nt),('维基百科：罗智强履历与家庭',wiki)]],notes='立院个人页两次超时，未把搜索摘要作为正文证据；公督盟、公视、Newtalk及维基均读取正文，立委身份有独立报道交叉，党团书记者任期不清不列现职。早期任期与配偶为维基单源待独立确认。人物关系缺稳定性质证据不凭同台推断。社交平台搜索未认证新账号，原三个账号及user_id和头像原样保留。选举成果仍有单源边界，未独立核票数。')
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
p=R/'tmp/tw_batch2_enriched/TW-PERSON-000163.json';p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')


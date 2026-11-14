import json,pathlib,shutil,jsonschema
p=pathlib.Path('output/tw/2026-07-27/persons/TW-PERSON-000012.json');x=json.loads(p.read_text(encoding='utf-8-sig'));keys=['political_stances','major_achievements','person_relationships','family_members'];before={k:len(x.get(k,[])) for k in keys}
b=pathlib.Path('tmp/tw_supplement_before');b.mkdir(parents=True,exist_ok=True)
if not (b/p.name).exists():shutil.copy2(p,b/p.name)
u='https://www.president.gov.tw/NEWS/39298'
def st(t,c):return dict(date='2025-06-20',topic=t,stance_content=c,source=u)
x['political_stances'] += [st('国防训练与科技创新','在公开专访中主张提高义务役训练质量，并加强创新国防技术、本土制造及传统军方与民间创新体系的衔接。'),st('全社会防卫韧性','主张除军事投资外，应加强通讯、网络、能源、交通与金融基础设施韧性，准备重要民生与医疗物资。'),st('能源组合与电网','主张能源多元化、增加本土能源能力，并投资电网韧性，降低集中系统遭扰动的影响。'),st('避免冲突与国际伙伴','表示应先强化自身防卫能力，并争取国际及跨党派伙伴支持，以威慑避免战争；记录本人主张，不把威慑效果认作已实现成果。')]
x['major_achievements'].append(dict(date='2021-01-20',achievement='以驻美代表身份正式获邀出席拜登就职典礼，为1979年以来台湾代表首次获该典礼主办单位正式邀请。该外交工作由代表处团队共同推动，不归为个人独立功绩。',organization='驻美国台北经济文化代表处（駐美國台北經濟文化代表處）'))
def rel(pid,n,t,d,a,b):return dict(person_id=pid,person_name=n,relationship_type=t,description=d,source=a,corroborating_sources=b)
x['person_relationships']=[rel('TW-PERSON-000001','赖清德（賴清德）','colleague','2024年选举与就职的正副搭档，依据官方就职典礼与独立选举报道，不推断私人亲疏。','https://www.president.gov.tw/NEWS/28424','https://www.cna.com.tw/news/aipl/202401140007.aspx'),rel('TW-PERSON-000002','蔡英文','superior','历史任命关系：2020年6月16日蔡英文任命其担任驻美代表，后于2023年离任；并非现任上下级。','https://www.president.gov.tw/News/25355','https://www.cna.com.tw/news/firstnews/202006160368.aspx')]
idx=json.loads(pathlib.Path('output/tw/2026-07-27/_name_index.json').read_text(encoding='utf-8'))
x['family_members']=[dict(person_id=idx.get('蕭清芬') or idx.get('萧清芬'),name='萧清芬（蕭清芬）',relationship='father',industry_or_organization='台南神学院（曾任院长）',source='https://www.president.gov.tw/Page/695',description='官方简介及中央社独立报道公开确认的父女关系和神学教育工作；第二来源：https://www.cna.com.tw/news/firstnews/202112085003.aspx')]
extra=[('萧美琴公开专访',u),('中央社：萧清芬与萧美琴父女关系','https://www.cna.com.tw/news/firstnews/202112085003.aspx'),('总统府：驻美代表任命','https://www.president.gov.tw/News/25355'),('中央社：萧美琴任驻美代表','https://www.cna.com.tw/news/firstnews/202006160368.aspx'),('中央社：2021正式获邀出席美总统就职','https://www.cna.com.tw/news/firstnews/202101200397.aspx'),('总统府：2024就职典礼','https://www.president.gov.tw/NEWS/28424')]
for t,a in extra:
 if not any(z['url']==a for z in x['collection_meta']['quotes']):x['collection_meta']['quotes'].append(dict(title=t,url=a))
x['collection_meta']['notes']+='\n2026-11-13四数组专项补采：政策取2025年6月20日总统府公布的本人专访问答，日期为发布日不伪造录影日。2021年1月20日正式获邀外交工作以中央社原文及本人专访回顾交叉确认。关系逐项证据：赖清德=总统府2024就职典礼与中央社202401140007；蔡英文=总统府News/25355与中央社202006160368的历史任命关系。父亲萧清芬=官方Page/695与中央社202112085003父女与神学院长公开身份；均已填source，关系补corroborating_sources。母亲官方列邱碧玉，其他来源多为Peggy Cooley或未列姓名，本轮未取得第二独立来源的姓名对应确认，故不把译名映射猜测写为确定资料。未推测婚姻状况，不扩采私人家属。没有找到更多可量化且可客观归因的个人立法政绩，未以一般活动或承诺凑成就。履历头像社媒及user_id均保持。'
s=json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'));jsonschema.Draft7Validator(s).validate(x)
out=pathlib.Path('tmp/tw_supplement');out.mkdir(parents=True,exist_ok=True);(out/p.name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(before,{k:len(x[k]) for k in keys})

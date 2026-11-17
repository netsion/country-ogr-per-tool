import json,pathlib
p=pathlib.Path('output/tw/2026-07-27/persons/TW-PERSON-000582.json'); d=json.loads(p.read_text(encoding='utf-8-sig'))
d.update(name_en='HsuYuChen',gender='female',aliases=['许宇甄'],current_positions=['第十一届立法委员（全国不分区及侨居国外国民）','中国国民党立法院党团书记长'])
d['education']=[dict(institution='国立云林科技大学',degree='master',field='企业管理',start_date=None,end_date=None),dict(institution='辅仁大学',degree='bachelor',field='统计学',start_date=None,end_date=None)]
d['work_experience']=[dict(organization=o,org_id=i,position=t,start_date=s,end_date=None) for o,i,t,s in [('立法院','TW-GOV-020','第十一届立法委员','2024-02-01'),('中国国民党','TW-PARTY-013','中央组织发展委员会主任委员（历史任职）',None),('中国国民党','TW-PARTY-013','云林县党部主任委员（历史任职）',None),('云林县工商发展投资策进会',None,'总干事（历史任职）',None),('云林县妇联会',None,'主任委员（历史任职）',None),('云林县妇工会',None,'荣誉总会长（官方经历栏）',None),('财团法人云林县云萱基金会',None,'董事（官方经历栏）',None),('大专院校（官方未载校名）',None,'大学讲师（历史经历）',None)]]
d['political_stances']=[dict(date=a,topic=b,stance_content=c,source=u) for a,b,c,u in [('2026-08-27','国防自主与无人载具产业','主张把一次性对外采购转为长期产业战略，将技术、人才和供应链留在台湾，并要求重大采购接受国会监督。','https://udn.com/news/amp/story/124984/9718355'),('2026-10-30','毒驾刑责','支持加重毒驾再犯致死刑责，认为三读表决体现对毒驾零容忍的立场。','https://udn.com/news/amp/story/6656/9847487'),('2026-09-15','预算审议程序','认为总预算三读后须给予议事人员整理校对时间，反对将津贴未入账责任归咎立法院；此为其公开主张。','https://udn.com/news/story/6656/9755571')]]
d['major_achievements']=[dict(date='2026-08-25',organization='立法院',achievement='作为高等中等教育法第五十八条修正草案提案委员之一，其等19人版本与其他十案并案审查后获三读通过；属集体立法成果，不代表个人版本全部获采纳。'),dict(date='2025-07',organization='立法院',achievement='其等18人提出身心障碍者权益保障法第五十三条修正草案，与其他委员及党团版本并案后完成三读，7月22日咨请公布；属共同立法成果，未据此声称个人条文全数获采。')]
d['family_members']=[dict(name='林启沧（林啟滄）',person_id=None,relationship='spouse',industry_or_organization='曾任全国渔会总干事'),dict(name='许育宁（許育寧）',person_id=None,relationship='sister',industry_or_organization='曾任国家政策研究基金会副执行长')]
d['person_relationships']=[dict(person_id='TW-PERSON-000034',person_name='朱立伦（朱立倫）',relationship_type='superior',description='限定历史党务上下级：2021年朱立伦任国民党主席期间，许宇甄获任中央组织发展委员会主任委员；不据此推定私人关系。')]
d['biography_summary']='许宇甄是台湾中国国民党籍政治人物，毕业于辅仁大学统计系，取得国立云林科技大学企业管理研究所硕士学位。她长期参与云林地方党务与妇女社团，曾任国民党云林县党部主任委员、云林县工商发展投资策进会总干事，以及妇联会、妇工会和云萱基金会相关职务，并有大学讲师经历。她曾在2008年及2012年列入国民党不分区立委名单，2024年进入第十一届立法院，2月1日到职。官方名单记载其历任内政委员会及司法及法制委员会等委员会成员。2026年下半年仍持续参与公开政治活动，8月就无人载具产业与国防采购监督表达意见，9月说明预算函送程序，10月以国民党团书记长身份支持加重毒驾刑责。其立法工作包括高中教育及身心障碍者权益相关修法的共同提案，相关成果应理解为并案审查和院会集体决定。'
w=json.loads(pathlib.Path('tmp/social_xlsx_20261116/workbook_raw.json').read_text(encoding='utf-8-sig'))
for sheet in w:
 for row in sheet['rows']:
  vals={c['col']:c.get('value') for c in row['cells']}
  if vals.get(2)=='许宇甄':
   platform=vals[3]; uid=str(vals.get(5,'')).split('#')[-1]; note=f"用户提供社交.xlsx，工作表{sheet['sheet']}第{row['row']}行；姓名明确对应本人物，未独立核实实时官方认证。USER-ID={vals.get(5)}"
   if vals.get(6):note+=f"；PAGE-ID={vals[6]}（单独字段，不作为USER-ID）"
   d['social_accounts'].append(dict(platform=platform,url=vals[4],account_name='許宇甄',source={'facebook':6,'instagram':8}[platform],username='jennyhsu56999',nickname=None,user_id=uid,source_note=note))
urls=[('立法院许宇甄委员简介','https://www.ly.gov.tw/Pages/List.aspx?nodeid=46808'),('许宇甄生平','https://zh.wikipedia.org/wiki/許宇甄'),('信传媒专访：许宇甄与姐姐','https://www.cmmedia.com.tw/home/articles/46102'),('联报：毒驾修法三读','https://udn.com/news/amp/story/6656/9847487'),('联报：无人载具条例','https://udn.com/news/amp/story/124984/9718355'),('联报：预算函送争议','https://udn.com/news/story/6656/9755571'),('立院高中教育法58条并案及三读','https://ppg.ly.gov.tw/ppg/bills/deliver-and-negotiation/203110222210000/details'),('立院身障权益法53条并案及三读','https://ppg.ly.gov.tw/ppg/bills/203110144290000/details'),('联报地方记者：林启沧妻子许宇甄','https://blog.udn.com/yunlinnews/2902470')]
d['collection_meta'].update(data_sources=['official_website','news_search','wikipedia','other'],quotes=[dict(title=t,url=u) for t,u in urls],notes='实际原文证据截止2026-10-30；采集2026-11-16。英文采用立法院原列HsuYuChen。学历及主要经历由立院简介核实，经历未载起讫者留空，经历栏不视为现任。书记长由下半年联报与维基交叉；8月报道仍称首席副书记长，未猜交接日。配偶由信传媒专访与联报地方记者报道交叉；姐姐仅信传媒及维基，缺第二独立直接来源。家庭ID索引未命中。朱立伦ID已读实际画像。两成果为并案集体三读，不声称个人条文全采或执行效果；身障法页面给7月11/15两院会日期，故仅精确到月。原骨架无头像及社交值，保持profile null；用户表两账号已实际提取，USER-ID/PAGE-ID分别说明，平台未独立实时认证。未凭相同handle新增其他平台。未采尚未核验的出生日期。')
out=pathlib.Path('tmp/tw_batch7_enriched/TW-PERSON-000582.json');out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
import jsonschema
jsonschema.validate(d,json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8-sig')))
print('jsonschema PASS')

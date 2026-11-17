import json,pathlib
r=pathlib.Path('D:/ai-workspace/apec-osint-tool'); p=r/'tmp/tw_batch7_enriched/TW-PERSON-000583.json'
d=json.loads((r/'output/tw/2026-07-27/persons/TW-PERSON-000583.json').read_text(encoding='utf-8'))
cna='https://www.cna.com.tw/news/aipl/202507035021.aspx'
d.update(gender='male',birth_date='1988-06-13',birth_place='臺中市',current_positions=['第十一届立法委员（台中市第五选举区）'])
d['education']=[dict(institution=i,degree=g,field=f,start_date=None,end_date=None) for i,g,f in [('國立臺中第一高級中學','high_school',None),('臺北市立大學','bachelor','社会暨公共事务'),('國立政治大學','master','政治学')]]
jobs=[('立法院','第十一届立法委员','2024-02-01',None,'TW-GOV-020'),('臺中市議會','第三、四届议员','2018-12-25','2024-01-31',None),('中國國民黨','发言人兼新媒体部主任','2017','2018','TW-PARTY-013'),('中國國民黨','青年团总团长兼中央常务委员','2010','2011','TW-PARTY-013'),('經濟部','秘书室专员',None,None,None),('青興資本投資公司','投资经理','2016','2017',None),('國立暨南國際大學','硕士学程讲师',None,None,None)]
d['work_experience']=[dict(organization=o,position=t,start_date=s,end_date=e,org_id=i) for o,t,s,e,i in jobs]
d['political_stances']=[dict(date='2025-07-03',topic=t,stance_content=x,source=cna) for t,x in [('家庭育儿','在公开答辩书中主张将育婴留职停薪津贴最长发放期由6个月延至12个月，说明已提案；不代表已经通过。'),('交通安全','主张提高无照驾驶罚锾至6万至20万元，并对酒驾及无照驾驶没入车辆，以强化吓阻；为提案主张。'),('性暴力预防','主张在保护被害人隐私前提下，允许为公共利益适度公开加害者信息，并要求评估再犯风险及对最高风险者公开信息。')]]
d['major_achievements']=[dict(date='2024-07-16',organization='立法院',achievement='参与推动加重低龄儿童受虐刑责修法；刑法相关条文经立法院集体三读，对未满7岁者施虐、致死或重伤等加重其刑至二分之一。个人参与据其公开答辩书，三读结果另经中央社报道核实，不归为个人独力成果。'),dict(date='2025-05-09',organization='立法院',achievement='参与推动纪念日及节日实施条例立法，立法院集体三读新增小年夜、教师节等放假日，并将劳动节改为全国放假。个人答辩主张还七天假，实际通过内容以人事行政总处公告的新增五个全国放假日为准。')]
d['person_relationships']=[dict(person_id=None,person_name='陳永康',relationship_type='colleague',description='2025年7月公布答辩书明确说明，陈永康为两岸人民关系条例第29条修正草案提案人，黃健豪为连署人；仅记该特定法案提案与连署合作，不推定长期政治盟友。')]
d['family_members']=[dict(person_id=None,name='葉季青',relationship='spouse',industry_or_organization=None)]
raw=json.loads((r/'tmp/social_xlsx_20261116/workbook_raw.json').read_text(encoding='utf-8'))
for sheet in raw:
 for row in sheet['rows']:
  cells={c['col']:c['value'] for c in row['cells']}
  if cells.get(2)!='黄健豪':continue
  platform=cells[3]; uid=cells[5]; url=cells[4]
  d['social_accounts'].append(dict(platform=platform,url=url,account_name='黃健豪',source={'facebook':6,'instagram':8,'threads':24}[platform],user_id=uid,username='TCBetter' if platform=='facebook' else 'gary030214',nickname=None,source_note=f'用户社交.xlsx工作表{sheet["sheet"]}第{row["row"]}行，姓名及L74关联；未独立核实实时官方认证。USER-ID列值原样保留。'+(f'PAGE-ID另列为{cells[6]}，不是USER-ID冲突；2018中选会公报外链亦为TCBetter。' if 6 in cells else '')))
d['biography_summary']='黃健豪是台中市出身的中国国民党政治人物，毕业于国立台中一中，后修读台北市立大学社会暨公共事务学系，并取得政治大学政治学硕士学位。他较早参与国民党青年工作，曾任青年团总团长及中央常务委员，随后在经济部秘书室、投资公司和大学教学等领域工作，也担任国民党发言人及新媒体部主任。2018年进入台中市议会，2022年连任，2024年转任台中市第五选举区立法委员。其公开政策主张涉及交通安全、育儿津贴、儿童保护及劳动休假制度。2025年罢免程序期间发表答辩书阐述提案与立法参与，相关政治评价存在争议；本文将其自述参与与议会集体通过结果分别表述。立法院2026年下半年议事录记载他于10月13日参与行政院施政报告质询，可确认其持续实际履职。'
d['collection_meta']=dict(collection_date='2026-11-16',phase='phase4_person_profile',data_sources=['government_directory','news_search','wikipedia','other'],quotes=[dict(title=t,url=u) for t,u in [('黃健豪－维基百科','https://zh.wikipedia.org/wiki/黃健豪'),('2018台中市第八选区选举公报','https://eebulletin.cec.gov.tw/107/05臺中市/02市議員/臺中市第08選區.pdf'),('黄健豪罢免案理由与答辩书全文',cna),('第11届第6会期第2次会议议事录','https://ppg.ly.gov.tw/ppg/SittingYuanInfo/download/agendarec1/02/pdf/11/06/02LCEWC03_110602.pdf'),('联合作品：黄健豪宣布当选','https://video.udn.com/news/1281602'),('三读加重虐童刑责','https://www.cna.com.tw/news/aipl/202407160307.aspx'),('人事行政总处新增五个放假日说明','https://www.dgpa.gov.tw/information?pid=12440&uid=2')]],notes='实际活动证据截止2026-10-13。立法院个人页反复超时，不据其摘要补英文，英文名未核保留空。教育、履历由中选会公报与百科交叉；未载任期留null，党务均历史任职。配偶实名来自2024-01-13联合报原文，尚缺第二独立实名原文，未收录无名子女。政策日期为答辩书公布日期，不冒称提案日期；成果参与为本人答辩书自述、集体通过结果另核。财划法答辩段落年份存在内部冲突，未录为成果。社交表已实际核提取，USER与PAGE分列保留。关系尝试检索盧秀燕竞选共事但当前可读原文不足，未据同台设为盟友。org非空引用已读取实际机构画像。')
p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
import jsonschema
jsonschema.validate(d,json.loads((r/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')))
print(p)

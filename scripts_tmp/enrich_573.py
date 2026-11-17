import json
from pathlib import Path
p=Path('output/tw/2026-07-27/persons/TW-PERSON-000573.json'); d=json.loads(p.read_text(encoding='utf-8'))
d.update(gender='male',birth_date='1954-06-24',birth_place='臺北市',current_positions=['桃園市市長'],aliases=['张善政'])
d['education']=[dict(institution=i,degree=g,field='土木工程',start_date=None,end_date=y) for i,g,y in [('國立臺灣大學','bachelor','1976'),('史丹佛大學','master','1977'),('康乃爾大學','doctorate','1981')]]
jobs=[('國立臺灣大學','土木工程學系教授','1983','1990'),('國家科學委員會國家高速電腦中心','主任','1991','1997'),('國家科學委員會','企劃考核處處長','1998','2000'),('宏碁','電子化事業群副總經理','2000','2010'),('Google','亞洲硬體營運總監','2010','2012'),('行政院','政務委員','2012-02-16','2014-03-02'),('科技部','部長','2014-03-03','2014-12-08'),('行政院','副院長','2014-12-08','2016-01-31'),('行政院','院長','2016-02-01','2016-05-20'),('台灣大哥大基金會','董事長','2016-07-22','2019-04-23'),('國家生技醫療產業策進會','會長','2016-06-22','2019-11-26'),('桃園市政府','市長','2022-12-25',None)]
d['work_experience']=[dict(organization=o,position=t,start_date=s,end_date=e,org_id=None) for o,t,s,e in jobs]
u1='https://news.tycg.gov.tw/News_Content.aspx?n=5016&s=1621798&sms=7885';u2='https://news.tycg.gov.tw/News_Content.aspx?n=5016&s=1856277&sms=7885';u3='https://news.tycg.gov.tw/News_Content.aspx?n=5016&s=1951560';u4='https://typass.tycg.gov.tw/latest-trend/view/c03842fc-1e10-4c72-9512-2f23721f632c'
d['political_stances']=[dict(date='2026-05-13',topic='校園營養',stance_content='主張營養午餐應著重品質而非金額競賽，增加蛋白質、在地食材及名廚參與菜單設計。',source=u1),dict(date='2026-08-30',topic='醫療照護',stance_content='支持依健康需求搭配中西醫，持續整合醫療資源、擴大服務量能，並肯定偏鄉巡迴醫療。',source=u2),dict(date='2026-11-04',topic='智慧城市',stance_content='主張以實際市政問題為導向選用科技工具，重點在改善服務及市民生活，並鼓勵各局處發掘業務課題。',source=u3)]
d['major_achievements']=[dict(date='2023-02',organization='桃園市政府',achievement='其市長任內由市府團隊實施國中小免費營養午餐；2026年5月市政新聞確認自2023年2月推動。屬市府集體施政，非個人獨力成果。'),dict(date='2026-08-31',organization='桃園市政府',achievement='其任內市府團隊將2026年2月23日開始的生生喝鮮乳政策擴大至符合資格的2至15歲、國中畢業前學幼生，每週可兌領一瓶鮮乳或豆漿；9月7日官方公告確認已實施。')]
d['family_members']=[dict(person_id=None,name='張琦雅',relationship='spouse',industry_or_organization=None)]
d['biography_summary']='張善政是臺灣工程學者、科技企業經理人與政治人物，具有臺灣大學土木工程學士、史丹佛大學碩士及康乃爾大學博士背景。早期任教臺灣大學，後主持國家高速電腦中心及國科會企劃考核業務，轉入宏碁與Google擔任主管，累積學術、政府科研及企業營運經驗。2012年進入行政院，先後擔任政務委員、首任科技部長、副院長與行政院長。卸任後參與基金會與生技產業組織，2022年當選桃園市長，同年12月25日就任。市長任內關注校園營養、醫療服務與科技治理；免費午餐及乳品補助是市府團隊實施的政策。2026年11月4日仍以市長身分主持市政會議，強調從實際問題選擇科技工具。本次不將2026年參選視為已獲連任。'
d['social_accounts']=[]
raw=json.loads(Path('tmp/social_xlsx_20261116/workbook_raw.json').read_text(encoding='utf-8'))
for sh in raw:
 if sh['sheet']!='2026-03-16':continue
 for r in sh['rows']:
  c={x['col']:x['value'] for x in r['cells']}
  if c.get(2)!='张善政':continue
  platform=c[3];uid=c.get(5)
  note=f'用户授权社交表工作表2026-03-16第{r["row"]}行；未独立核实实时官方认证。'
  if platform=='facebook':uid=None;note+='表内USER-ID为100044377241488、PAGE-ID为179708992651678，分列保留于本说明，不混填user_id；本人善政進行式履历页外链交叉支持SanCheng624 URL。'
  d['social_accounts'].append(dict(platform=platform,url=c[4],account_name='張善政',source={'facebook':6,'instagram':8,'youtube':9}[platform],user_id=uid,source_note=note))
d['collection_meta']=dict(collection_date='2026-11-16',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia','other'],quotes=[dict(title=t,url=u) for t,u in [('善政進行式本人履歷','https://portaly.cc/sangofans2023/pages/about'),('中央社：張善政贏回桃園市','https://www.cna.com.tw/news/aipl/202211260273.aspx'),('張善政人物條目','https://zh.wikipedia.org/wiki/張善政'),('營養午餐補助與政策',u1),('中醫嘉年華',u2),('智慧治理市政會議',u3),('鮮乳擴大補助已實施',u4)]],notes='已核官方、中央社、本人履歷及百科原文；實際現職活動核至2026-11-04。英文正式姓名未核留空；QID與頭像沿用原null。主要職業依本人履歷，年份部分百科單源。配偶經中央社及2026官方活動雙源確認。其他家庭不收無名子女。未核具體合作關係故留空。社交表实名链接已提取，未冒称平台实时认证。市長簡介頁428不可讀，改用本人履歷及新聞。成果為團隊已實施制度，未把捷運規劃或2026選舉當完成。')
out=Path('tmp/tw_batch7_enriched/TW-PERSON-000573.json');out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
import jsonschema
jsonschema.validate(d,json.loads(Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')))
print('jsonschema PASS',len(d['social_accounts']))

import json,pathlib
p=pathlib.Path('output/tw/2026-07-27/persons/TW-PERSON-000042.json'); d=json.loads(p.read_text(encoding='utf-8'))
d['current_positions']=['台灣民眾黨國家治理學院院長']
d['aliases']+=['柯P','阿北']
d['name_en']='Ko Wen-je'
d['education']=[dict(institution='國立臺灣大學醫學院',degree='bachelor',field='醫學',start_date=None,end_date=None),dict(institution='國立臺灣大學醫學院',degree='doctorate',field='臨床醫學',start_date=None,end_date=None)]
rows=[('1988-09','1993-06','國立臺灣大學醫學院附設醫院','外科部住院醫師'),('1993-06','1994-06','美國明尼蘇達大學','外科研究員'),('1994-06','2014-12','國立臺灣大學醫學院附設醫院','外科加護病房主任'),('2002-07','2008-08','國立臺灣大學醫學院','專任助理教授'),('2008-08','2014-12','國立臺灣大學醫學院附設醫院','創傷醫學部主任'),(None,None,'國立臺灣大學醫學院','專任教授（歷史任職）'),('2014-12-25','2022-12','臺北市政府','市長'),('2019-08-06','2025-01-01','台灣民眾黨','主席'),('2026-01-28',None,'台灣民眾黨','國家治理學院院長')]
d['work_experience']=[dict(start_date=a,end_date=b,organization=c,position=e,org_id=None) for a,b,c,e in rows]
u='https://www.cna.com.tw/news/aipl/202601290081.aspx'
d['political_stances']=[dict(date='2026-01-29',topic='陸配參政程序',stance_content='主張政府對陸配從政所涉國籍規定訂出明確流程，使人民得以遵循；屬本人意見，非已實施制度。',source=u),dict(date='2026-01-29',topic='憲政與監察制度',stance_content='主張廢除監察院，並提議從預算審議著手；屬政治主張，未視為完成修憲或廢院。',source=u),dict(date='2026-11-16',topic='司法公開與程序正義',stance_content='在自身案件二審中要求高院全程法庭直播，主張檢方負舉證責任；其司法不公指控為當事人說法，非本資料認定。',source='https://www.cna.com.tw/news/asoc/202611160182.aspx')]
d['major_achievements']=[dict(date='2016',achievement='市長任內市府團隊完成忠孝橋引道拆除，作為西區門戶計畫及北門周邊空間改善的一環；屬跨局處團隊成果。',organization='臺北市政府'),dict(date='2017',achievement='市長任內市府及跨縣市團隊完成臺北世界大學運動會籌辦與舉行；不將賽會歸為其個人獨力成果。',organization='臺北市政府')]
d['person_relationships']=[dict(person_id='TW-PERSON-000043',person_name='黃國昌',relationship_type='colleague',description='2026年1月接任國家治理學院院長時公開說明與黨主席黃國昌分工，由黃處理國會事務，自己辦理人才訓練；限此次黨務分工。')]
d['family_members']=[dict(person_id=None,name='陳佩琪',relationship='spouse',industry_or_organization=None)]
d['biography_summary']='柯文哲是臺灣外科醫師出身的政治人物，畢業於國立臺灣大學醫學系，取得臨床醫學研究所博士學位。從醫期間在臺大醫院擔任外科住院醫師，赴美國明尼蘇達大學擔任外科研究員，返臺後從事外科加護、創傷、器官移植及葉克膜相關醫療，並任臺大醫學院教師及教授。2014年底就任臺北市長，2018年連任，2022年底卸任；市府團隊在其任內推動西區門戶計畫及籌辦2017世大運。2019年創立台灣民眾黨並任首任主席，參與2024年總統選舉，2025年辭去黨主席，2026年1月獲任命為國家治理學院院長，負責政治人才訓練。2026年11月仍有公開政治表態。司法方面，臺北地院2026年3月26日就收賄、公益侵占及背信等四罪一審判處應執行17年、褫奪公權6年；截至11月16日原文，全案仍由高院上訴審理，柯文哲否認犯罪並提出程序質疑，不能把一審視為確定判決。'
r=json.loads(pathlib.Path('tmp/social_xlsx_20261116/records.json').read_text(encoding='utf-8'))
for x in r:
 if x.get('name')=='柯文哲' and x['platform']=='twitter':
  d['social_accounts'].append(dict(platform='twitter',url=x['url'],account_name='KP_Taiwan',source=3,user_id=x['raw_user_id'],username='KP_Taiwan',source_note=f"用户提供社交.xlsx：{x['sheet']}!第{x['row']}行，实名对应；未独立核实实时官方认证。与旧X链接不同，保留双账号不覆盖旧ID。"))
qs=[('總統立委選舉公報學經歷','https://www.cna.com.tw/news/aipl/202401045002.aspx'),('國家治理學院任命及分工',u),('公視：柯文哲接任國家治理學院院長','https://news.pts.org.tw/article/792946/'),('二審及一審狀態','https://www.cna.com.tw/news/asoc/202611160182.aspx'),('妻子陳佩琪陪同出庭','https://www.cna.com.tw/news/asoc/202611160156.aspx'),('普發現金政治表態','https://udn.com/news/story/6656/9879680'),('傳統基金會演講全文','https://www.gov.taipei/News_Content.aspx?n=2044902FC839D045&s=D7F322700A7138FC&sms=72544237BBE4C5F6'),('西區門戶已完成工程','https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=EAEF6E47468F761C&sms=72544237BBE4C5F6'),('世大運治理經驗','https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=7F97D4F023C88782&sms=72544237BBE4C5F6'),('柯文哲歷史履歷','https://zh.wikipedia.org/wiki/柯文哲')]
d['collection_meta']=dict(collection_date='2026-11-17',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia','other'],quotes=[dict(title=a,url=b) for a,b in qs],notes='證據截止2026-11-16；現任院長以中央社及公視2026-01-29交叉，黨網站403，未另推定公職。司法一審未確定，上訴審理中；不預寫後續。生日保留，英文沿用舊值，AP檢索全文出現Ko Wen-je，未以摘要新造。醫療細日期部分來自維基，主要職歷另以本人政府演講及選舉公報交叉；未載教授任期留空。家庭配偶可靠新聞單源，未收無名子女。關係ID讀正式黃國昌画像確認；組織ID未讀實體故null。全部舊社交/头像/QID保留；表第102/164/267/470/610行實際核列，FB USER與PAGE不同正常，原USER保留；新增表列X帳號，舊kp_taipei與新KP_Taiwan是否並存未獨立核實，不覆蓋。官網社交外鏈未取得，僅保留舊及用户表來源。兩項成果為市府團隊已實施項目，非個人獨力；未任立委不造三讀成果。初選udn AMP不可讀已換全文來源。')
out=pathlib.Path('tmp/tw_batch9_enriched/TW-PERSON-000042.json');out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
import jsonschema
jsonschema.validate(d,json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')))
print('jsonschema PASS')

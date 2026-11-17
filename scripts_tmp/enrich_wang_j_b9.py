import json
from pathlib import Path
r=Path('.')
p=json.loads((r/'output/tw/2026-07-27/persons/TW-PERSON-000027.json').read_text(encoding='utf-8'))
records=json.loads((r/'tmp/social_xlsx_20261116/records.json').read_text(encoding='utf-8'))
print('SOCIAL_MATCHES', [x for x in records if '王金平' in json.dumps(x,ensure_ascii=False)])
p['current_positions']=['中國國民黨最高顧問','財團法人臺灣癌症基金會董事長']
p['birth_place']='高雄路竹'
p['aliases']+=['公道伯']
p['education']=[dict(institution=a,degree=b,field=c,start_date=None,end_date=None) for a,b,c in [('高雄縣路竹鄉大社國小','primary',None),('省立臺南第一中學初、高中部','high_school',None),('臺灣省立師範大學','bachelor','數學')]]
p['work_experience']=[dict(organization=a,org_id=None,position=b,start_date=c,end_date=d) for a,b,c,d in [('立法院','立法委員','1976-02-01','2020-01-31'),('立法院','副院長','1993-02-01','1999-01-31'),('立法院','院長','1999-02-01','2016-01-31'),('中國國民黨','副主席','2000-06','2005-08'),('高雄縣工業會','理事長',None,None),('中國國民黨','政策會副主任委員',None,None),('中國國民黨','工作會主任兼黨團書記長',None,None),('中國國民黨','中央常務委員',None,None),('中華民國義消協會','理事長',None,None),('臺灣職棒大聯盟','會長',None,None),('臺灣癌症基金會','董事長',None,None),('中華民國立法委員協會','理事長',None,None),('國家生技醫療發展委員會','會長',None,None),('中國國民黨','最高顧問','2026-01-05',None)]]
p['person_relationships']=[dict(person_id='TW-PERSON-000199',person_name='鄭麗文',relationship_type='associate',description='2026年1月5日以國民黨主席身分與四位副主席正式拜會王金平並頒最高顧問聘書；僅記該次聘任與黨務接觸。')]
p['family_members']=[dict(person_id=None,name='陳彩蓮',relationship='spouse',industry_or_organization=None)]
p['political_stances']=[dict(date=d,topic=t,stance_content=s,source=u) for d,t,s,u in [('2026-11-12','兩岸和平','出席和平倡議大會，表示應求同存異、化解敵意，讓兩岸民眾共享安定發展。','https://newtalk.tw/news/view/2026-11-12/1070669'),('2026-01-05','朝野政治和解','接受最高顧問聘任時主張各黨拋開意識形態與自私心態，解開朝野心結，以人民與政局和諧為念。','https://news.tvbs.com.tw/politics/3091491'),('2014-04-06','貿易協議民主監督','宣布兩岸協議監督條例草案完成立法前，不召集服貿協議相關黨團協商；此為程序承諾，並非條例已完成立法。','https://news.pts.org.tw/article/266124')]]
p['major_achievements']=[]
p['social_accounts'].append(dict(platform='line',url='https://page.line.me/018vhunt',account_name='王金平',source=21,username='018vhunt',nickname=None,user_id=None,source_note='LINE公開具名頁自述王金平官方帳號，頁內提及本人Facebook與YouTube；未獨立核實即時官方認證。'))
p['biography_summary']='王金平是高雄路竹出身的國民黨政治人物，畢業於臺灣省立師範大學數學系。1976年起擔任立法委員，至2020年任期結束，歷經增額選舉與國會全面改選。1993年至1999年任立法院副院長，1999年2月至2016年1月任院長，並曾任國民黨副主席、黨團書記長及工業與公益團體職務。他的政治生涯與朝野協商及國會民主化密切相關；2014年服貿爭議期間公開承諾，在兩岸協議監督條例完成立法前不召集相關黨團協商，當時受到不同政黨不同評價。離開立法院後仍參與公共事務，2026年1月接受國民黨最高顧問聘任，同年11月12日出席民間和平倡議大會，持續呼籲朝野和解與兩岸和平。他也擔任臺灣癌症基金會董事長，惟各項公益工作的實際政策成效仍須個別查證，不能以歷史頭銜代替目前職務。'
urls=[('立法院第4屆王金平委員官方學經歷','https://www.ly.gov.tw/Pages/List.aspx?nodeid=869'),('鄭麗文親聘最高顧問','https://news.tvbs.com.tw/politics/3091491'),('王金平談雙北選情','https://news.tvbs.com.tw/politics/4049427'),('兩岸和平倡議大會','https://newtalk.tw/news/view/2026-11-12/1070669'),('從政50年感恩餐會及配偶本人發言','https://udn.com/news/story/6656/9217192'),('先立法再審查','https://news.pts.org.tw/article/266124'),('臺灣癌症基金會法人變更登記','https://www.judicial.gov.tw/tw/cp-144-1268524-9b614-1.html'),('王金平歷史任期資料','https://zh.wikipedia.org/wiki/王金平'),('LINE王金平公開帳號','https://page.line.me/018vhunt')]
p['collection_meta']=dict(collection_date='2026-11-17',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia','government_registry','social_media'],quotes=[dict(title=t,url=u) for t,u in urls],notes='實際公開政治活動證據截至2026-11-12。原三項現職均為歷史公職，已移入履歷。最高顧問由2026-01-05 TVBS全文與維基資料交叉；基金會董事長以2025-03-10法院登記確認，2026-07-28基金會名單搜索可見但原文讀取超時，故公益職務最新直接證據止於2025登記。配偶陳彩蓮由2025-12-21聯合報現場報導及本人發言單源收錄。無日期履歷均為立法院歷史經歷，不能解作現職。英文姓名由立法院全文確認。2026-11-12 TVBS線索實為選情報導，和平觀點改用Newtalk全文。舊社交兩筆及全部身份字段和source_note原樣保留；實際檢索records及workbook_raw未找到王金平具名候選，未增表內ID。LINE具名頁已讀，展示頁未輸出可提取社交目的URL，不據此推認其他帳號。已嘗試查國會五法與議事規則第五十七條的協商成果，但公報原文定位未確證王金平個別貢獻，故成果留空，不將整部法律或任內總量歸功一人。未收同台人物為政治盟友；鄭麗文引用ID已讀真實画像核身份。')
out=r/'tmp/tw_batch9_enriched/TW-PERSON-000027.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
import jsonschema
jsonschema.validate(p,json.loads((r/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')))
print('JSONSCHEMA PASS')

import json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
d=json.loads((root/'output/tw/2026-07-27/persons/TW-PERSON-000145.json').read_text(encoding='utf-8'))
ly='https://www.ly.gov.tw/Pages/Detail.aspx?nodeid=6570&pid=82062'
nft='https://www.nftu.org.tw/News/news_view.aspx?NewsID=20140114170100B8B6'
sh='https://www.shanghai.gov.cn/nw4411/20260425/6312cb27cbb84c32993ede5535f6b06b.html'
gvm='https://www.gvm.com.tw/article/15802'
ltn='https://features.ltn.com.tw/english/article/paper/892046'
court='https://www.judicial.gov.tw/tw/cp-144-1124238-26a2d-1.html'
old='https://www.ly.gov.tw/EngPages/Detail.aspx?nodeid=4970&pid=26508'
new='https://newtalk.tw/news/view/2026-11-12/1070669'
d['aliases']=list(dict.fromkeys(d['aliases']+['小辣椒','Hung, Hsiu-Chu']))
d['current_positions']=['中華青雁和平教育基金會董事長']
d['education']=[{'institution':'臺北第二女子高級中學（今臺北市立中山女子高級中學）','degree':'high_school','field':None,'start_date':None,'end_date':None},{'institution':'中國文化學院（今中國文化大學）','degree':'bachelor','field':'法律','start_date':None,'end_date':'1970'},{'institution':'美國密蘇里州立東北大學（今杜魯門州立大學）','degree':'master','field':'教育','start_date':None,'end_date':None,'note':'立法院列為教育碩士；2015-06-24自由時報記本人承認學分、時數不符教育部採認標準，不可用於公職晉用升等考試。'},{'institution':'國立政治大學','degree':'professional','field':'教育研究所進修','start_date':None,'end_date':None},{'institution':'國立臺灣師範大學','degree':'professional','field':'教育研究所進修','start_date':None,'end_date':None}]
def w(org,pos,start=None,end=None):return {'organization':org,'org_id':None,'position':pos,'start_date':start,'end_date':end}
d['work_experience']=[w('臺北縣立秀峰國民中學','教師、訓導主任','1971','1975'),w('臺北縣立板橋國民中學','訓導主任、教務主任','1975','1979'),w('國立華僑實驗高級中學','輔導組長','1979','1980'),w('中國國民黨臺北縣黨部','婦工組組長','1980','1986'),w('中國國民黨臺灣省黨部','編審','1986','1990'),w('立法院','第一屆增額至第八屆立法委員','1990','2016-01-31'),w('中國國民黨','青年工作會副主任、婦女工作會副主任、政策會立法院工作會副主任、政策會副執行長（歷史職務）'),w('中國國民黨','中央常務委員（歷史任職，未核當期）'),w('中國國民黨','副秘書長兼考核紀律委員會主任委員','2011','2012'),w('立法院','第八屆副院長','2012-02-01','2016-01-31'),w('中國國民黨','副主席','2012','2015'),w('中國國民黨','代理秘書長','2014-12-03','2015-01-18'),w('中國國民黨','主席','2016','2017'),w('中華關懷弱勢族群愛心大聯盟','理事長（歷史職務）'),w('中華民國世界土風舞總會','理事長（歷史職務）'),w('中華民國腎臟防治基金會','董事長（歷史職務）'),w('中華青雁和平教育基金會','第三屆董事長','2024-06-25',None)]
d['political_stances']=[{'date':'2011-09-13','topic':'國民教育與適性發展','stance_content':'支持十二年國教按時推行，認為初期缺點可逐步改善；要求縮小學校師資設備差距，鼓勵學生按興趣發展。','source':gvm},{'date':'2011','topic':'私校教職員退休保障','stance_content':'第七屆第八會期議案文書載其等27人提出公教人員保險法修正草案，主張為缺乏月退保障者設計公保養老年金、區隔已有月退者並由國庫補足實施前不足；屬提案，非全文獲採認。','source':'https://ppg.ly.gov.tw/ppg/download/agenda1/02/pdf/07/08/11/LCEWA01_070811_00276.pdf'},{'date':'2026-04-24','topic':'兩岸文化交流','stance_content':'訪滬會見陳通時表示兩岸都是中國人，應共同傳播中華民族故事，並期望更多臺灣人士赴大陸交流。','source':sh}]
d['major_achievements']=[{'date':'2009','organization':'立法院','achievement':'參與促成私立學校教職員退撫條例通過。立法院所載報導明列洪秀柱、黃昭順、潘維剛等多人共同努力；只確認立法階段，不將當時仍受阻的公保轉勞保算作完成。'},{'date':'2014-01-14','organization':'立法院','achievement':'參與促成公教人員保險法修正三讀，讓私校教師養老年金先行、回溯2010年起退休者；全教總當日聲明將其列為協助者之一，屬朝野、行政與教師團體集體成果，並非其個人獨力立法。'}]
d['person_relationships']=[{'person_id':'TW-PERSON-000027','person_name':'王金平','relationship_type':'colleague','description':'2012至2016年第八屆立法院院長與副院長任期共事；2014-01-14全教總同列兩人為私校年金修法協助者。僅限院務及此修法合作，不推定私人盟友。','source':nft},{'person_id':None,'person_name':'陳通','relationship_type':'associate','description':'2026-04-24以基金會董事長身分訪滬，與上海市委常委陳通會見；僅指該次公開交流。','source':sh}]
d['family_members']=[]
d['biography_summary']='洪秀柱是臺灣中國國民黨政治人物，從教育工作轉入黨務及國會，長期關注教育制度與私校教職員退休保障。她畢業於中國文化學院法律系，曾在秀峰國中、板橋國中與華僑中學服務，後任國民黨地方婦女工作及省黨部職務，並歷任中央黨務職位、第一屆增額至第八屆立法委員。2012年2月起擔任第八屆立法院副院長，任期於2016年1月底結束，其國民黨主席任職亦已屬歷史。她曾參與私校退撫及公保年金制度的推動，相關成果由多名立委、行政部門與教師團體共同促成。現可交叉確認的公益職務為中華青雁和平教育基金會董事長，2024年法人登記及2026年上海會見報導均載明。2026年仍參與兩岸公共交流，4月訪滬並表達共同傳播中華文化的主張，11月12日亦出席兩岸和平倡議活動；出席本身不等同她逐條贊同大會所有主張。其教育碩士學位由立院列載，但本人曾說明學分時數不符合教育部採認標準，須與正式採認學歷區別。'
d['collection_meta']={'collection_date':'2026-11-17','phase':'phase4_person_profile','data_sources':['official_website','government_registry','news_search','wikipedia'],'quotes':[{'title':a,'url':b} for a,b in [('立法院第八屆副院長洪秀柱',ly),('財團法人中華青雁和平教育基金會變更登記',court),('中國國民黨前主席洪秀柱訪滬',sh),('初期雖有缺點 社會共同努力必能成功',gvm),('洪秀柱坦言：碩士學位不被教部承認',ltn),('有關公保法修正三讀的說明（一）',nft),('公保轉勞保遇阻，政府逼私校教師上街頭？',old),('兩岸和平倡議大會出席照片與報導',new),('洪秀柱歷史履歷與社交外鏈','https://zh.wikipedia.org/wiki/洪秀柱')]],'notes':'按現有畫像重採，保留原QID、头像、所有舊社交原欄位。英文由立院全文確認，沿用舊拼法。基金會董事長由2024司法登記與2026-04-25上海報導交叉；最新政治活動核至2026-11-12，新頭殼圖注明確出席，只證出席，未將倡議四點歸本人。舊立委、主席、副院長均轉歷史；部分教職、黨職日期由維基生平補充，官方未載完整年月，未精確至日。使用遠見本人教育訪談、自由時報本人學位說明、立院與全教總原文等多種獨立全文。政策涵蓋教育、社會保險與兩岸文化；未取得可讀財稅原文，未據摘要採錄。成果區分2009退撫立法與2014公保年金，不誤寫2010已全面月退。家庭已檢索父親洪子瑜，未獲可靠獨立原文故不收。records.json實際查無洪秀柱具名社交條目；維基外鏈列Facebook、微博及YouTube，舊三帳全保留，未宣稱即時認證，未將機構頻道新增為個人帳號。未核其他舊公益職務當期有效，不列現職。所有引用ID王金平已讀真實畫像確認。'}
out=root/'tmp/tw_batch9_enriched/TW-PERSON-000145.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
import jsonschema
jsonschema.validate(d,json.loads((root/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')))
print('jsonschema PASS',len(d['biography_summary']))

import json,pathlib
p=pathlib.Path('output/tw/2026-07-27/persons/TW-PERSON-000574.json');d=json.loads(p.read_text('utf-8'))
d.update(name_en='Ko, Chih-En',gender='female',birth_date='1962-04-29',birth_place='屏東縣潮州鎮',current_positions=['第十一屆立法委員（全國不分區及僑居國外國民）','2026年中國國民黨高雄市長候選人'])
d['education']=[dict(institution=n,degree=g,field=f,start_date=None,end_date=None) for n,g,f in [('南加州大學','doctorate','教育心理學'),('密西根州立大學','master','教育學'),('國立政治大學','bachelor','教育學'),('臺灣省立屏東女子高級中學','high_school',None)]]
d['work_experience']=[dict(organization=n,org_id=i,position=t,start_date=s,end_date=e) for n,i,t,s,e in [('立法院','TW-GOV-020','第十一屆立法委員','2024-02-01',None),('立法院','TW-GOV-020','第九屆立法委員','2016-02-01','2020-01-31'),('國家政策研究基金會',None,'執行長',None,None),('中國國民黨','TW-PARTY-013','副秘書長兼婦女部主任',None,None),('淡江大學','TW-ACAD-021','學務長','2009',None),('淡江大學','TW-ACAD-021','教育心理與諮商研究所專任教授、所長',None,None),('高等教育評鑑中心',None,'心理學門評鑑委員',None,None),('臺灣電視公司',None,'世界真奇妙節目主持人',None,None),('國立政治大學',None,'教育研究所兼任副教授','1992',None)]]
a='https://www.cna.com.tw/news/aipl/202611100137.aspx';b='https://udn.com/vote2026/story/124652/9834625';c='https://www.cna.com.tw/news/aloc/202609070233.aspx'
d['political_stances']=[dict(date=x,topic=y,stance_content=z,source=u) for x,y,z,u in [('2026-11-10','育兒照顧','提出自行照顧0至6歲兒童且未使用定期托育之家長每年48小時喘息券，特殊需求家庭加24小時，為競選主張尚非實施成果。',a),('2026-10-24','社會住宅','主張地方興辦5000戶社宅、婚育宅比例40％，育兒家庭租期延至12年，均屬參選政策。',b),('2026-09-07','石化與環境健康','要求新四輕資訊透明、市民參與與健康優先，向居民說明健康風險及減碳規劃。',c)]]
d['major_achievements']=[dict(date='2018-05-29',organization='立法院',achievement='與王育敏提出幼兒園幼童專用車車齡不得超過出廠10年的修法要求，相關幼兒教育及照顧法條文完成三讀；為朝野審議共同成果。'),dict(date='2019-04-23',organization='立法院',achievement='為家庭教育法修法版本提案委員之一；院會三讀規定地方家庭教育中心專業人力須於施行後3年內達半數，屬跨黨及行政院共同立法成果，不能將整體條文全歸個人。')]
d['person_relationships']=[dict(person_id=None,person_name='王育敏',relationship_type='colleague',description='2018年幼兒教育及照顧法審查中共同提出幼童專用車車齡10年限制；僅指本次修法合作。')]
d['family_members']=[dict(person_id=None,name='柯文福',relationship='father',industry_or_organization='前屏東縣縣長')]
r=json.loads(pathlib.Path('tmp/social_xlsx_20261116/records.json').read_text('utf-8'));seen=set()
for x in r:
 if x.get('name')!='柯志恩' or x['platform'] in seen:continue
 seen.add(x['platform']);fb=x['platform']=='facebook';note=f"用户社交.xlsx工作表{x['sheet']}第{x['row']}行，未独立核实实时官方认证；USER-ID={x.get('raw_user_id')}；PAGE-ID={x.get('raw_page_id')}。"
 d['social_accounts'].append(dict(platform=x['platform'],url=x['url'],account_name='柯志恩',source={'facebook':6,'youtube':9,'instagram':8,'threads':24}[x['platform']],user_id=None if fb else x['raw_user_id'],username=None,nickname=None,source_note=note+('USER与PAGE不同，user_id不猜填。' if fb else '')))
d['contacts']=[dict(type='website',value='https://kochihen2026.tw/',source='競選官網'),dict(type='email',value='ly11176a@ly.gov.tw',source='https://kochihen2026.tw/about')]
d['biography_summary']='柯志恩是中國國民黨籍政治人物及教育心理學者，出生於屏東縣潮州鎮，父親柯文福曾任屏東縣長。她畢業於屏東女中及國立政治大學教育學系，赴美取得密西根州立大學教育碩士與南加州大學教育心理學博士。早年曾從事電視節目主持與製作，與梁旅珠主持世界真奇妙獲金鐘獎肯定，後在大學從事教學、研究與學生事務，曾任淡江大學教育心理與諮商研究所教授、所長及學務長。2016年進入第九屆立法院，主要關注教育、幼兒照顧與家庭政策，曾參與幼童專用車安全及家庭教育法修法。其後歷任國民黨副秘書長兼婦女部主任、國家政策研究基金會執行長。2024年再任第十一屆不分區立委，2026年以國民黨高雄市長候選人身分提出住宅、育兒及環境健康政策，11月10日出席教會家庭座談並簽署家庭友善承諾書。相關市政方案均為參選主張，未視作當選後成果。'
sources=[('立法院柯志恩委員','https://www.ly.gov.tw/Pages/List.aspx?nodeid=46792'),('認識志恩','https://kochihen2026.tw/about'),('家庭友善承諾書',a),('社宅政見',b),('中油新四輕',c),('立院三讀娃娃車車齡不得超過10年','https://news.tvbs.com.tw/politics/928514'),('家庭教育中心專業人力修法','https://www.cna.com.tw/news/aipl/201904230032.aspx'),('專訪談亡父柯文福','https://www.nownews.com/amp/news/6886297'),('柯志恩維基百科','https://zh.wikipedia.org/wiki/柯志恩')]
d['collection_meta']=dict(collection_date='2026-11-16',phase='phase4_person_profile',data_sources=['official_website','government_directory','news_search','wikipedia','other'],quotes=[dict(title=t,url=u) for t,u in sources],notes='證據活動截止2026-11-10；現任立委由立院簡歷及中央社交叉，候選人由官網與新聞交叉；未預寫年底結果。歷史履歷無日期者以null保留，不表示仍在任；召委只在第11屆第1會期確認，未列現職。父親由本人專訪報導與百科交叉，其他家庭姓名未充分核實不填。關係王育敏及父親未命中索引故ID空。兩項成果為已三讀共同立法，未主張個人獨力或執行成效。社交四平台為用戶表實名關聯，Facebook USER/PAGE分列於source_note且不猜填；已做平台檢索但未取得獨立平台認證證據。英文採立院官方格式；出生資料主要依百科。')
out=pathlib.Path('tmp/tw_batch7_enriched/TW-PERSON-000574.json');out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf-8')
import jsonschema
jsonschema.validate(d,json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text('utf-8')))

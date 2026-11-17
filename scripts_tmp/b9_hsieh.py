import json,pathlib,jsonschema
root=pathlib.Path('D:/ai-workspace/apec-osint-tool')
p=json.loads((root/'output/tw/2026-07-27/persons/TW-PERSON-000021.json').read_text(encoding='utf-8'))
p['name']='謝長廷'; p['aliases']=list(dict.fromkeys(p['aliases']+['谢长廷']))
p['name_en']='Frank Chang-ting Hsieh'
p['current_positions']=['臺灣日本關係協會會長']
p['birth_place']='臺北市大同區'
p['education']=[dict(institution='國立臺灣大學',degree='bachelor',field='法律',start_date=None,end_date=None),dict(institution='日本京都大學',degree='master',field='法哲學',start_date=None,end_date=None)]
jobs=[('1981','1989','臺北市議會','議員'),('1990','1996','立法院','立法委員'),('1998','2005','高雄市政府','市長'),('2000','2002','民主進步黨','主席'),('2005','2006','行政院','院長'),('2016-06','2024-08','臺北駐日經濟文化代表處','代表'),('2024-08','2026-01','總統府','資政'),('2026-01-06',None,'臺灣日本關係協會','會長')]
p['work_experience']=[dict(start_date=a,end_date=b,organization=c,org_id=None,position=d) for a,b,c,d in jobs]
p['person_relationships']=[dict(person_id='TW-PERSON-000096',person_name='彭明敏',relationship_type='colleague',description='1996年首次總統直選期間搭檔參選，彭明敏為總統候選人、謝長廷為副總統候選人；限該次選舉合作。中央社2026-03-14本人回憶報導。')]
p['family_members']=[dict(person_id=None,name='游芳枝',relationship='spouse',industry_or_organization=None),dict(person_id=None,name='謝維洲',relationship='son',industry_or_organization=None)]
p['political_stances']=[dict(date='2026-03-14',topic='民主憲政與轉型正義',stance_content='認為總統直選使人民成為國家主人，民主化在台灣實踐並形成命運共同體；主張持續推動轉型正義。',source='https://www.cna.com.tw/news/aipl/202603140197.aspx'),dict(date='2021-04-22',topic='核廢水資訊透明與監測',stance_content='強調排放前須處理放射性物質、將氚降至標準以下；表示台灣應要求日本即時透明資訊、洋流路線並定期檢測。此為當時主張，非本資料對安全性的判斷。',source='https://www.cna.com.tw/news/aipl/202104220427.aspx'),dict(date='2023-09-17',topic='水產加工與貿易市場分散',stance_content='倡議台灣業者爭取日本協助引進帆立貝加工設備，在台剝殼後轉銷歐美，表示駐日代表處可協助；屬建議，不當作已完成成果。',source='https://www.cna.com.tw/news/aipl/202309170003.aspx')]
p['major_achievements']=[dict(date='2021-06-04',organization='臺北駐日經濟文化代表處',achievement='參與促成日本首批124萬劑AZ疫苗援台。中央社2026-01-06回顧記載，他於2021-05-24邀美國駐日代理大使楊舟與薗浦健太郎等餐敘、提出台灣疫情情況，經各方奔走協調促成已完成援助；屬多方外交協調成果，非個人獨力取得。'),dict(date='2024-08',organization='臺北駐日經濟文化代表處',achievement='任內持續以日本地方交流推動台日合作。中央社2026-01-06回顧記載他走訪47都道府縣各逾5次，並參與促成自治體友好或姊妹交流；報導所列178對是長期集體累計成果，不視為其個人新增數量。日本台灣交流協會2025年敘勳說明亦肯定其地方交流與災害互助貢獻。')]
p['biography_summary']='謝長廷是臺灣政治人物及律師，國立臺灣大學法律系畢業，取得日本京都大學法哲學碩士。其早年參與美麗島事件辯護律師團，並由黨外運動進入選舉政治，曾任臺北市議員、立法委員及民主進步黨主席。他於1998年至2005年間擔任高雄市長，隨後擔任行政院長，政治經歷跨越地方治理、國會與中央行政。1996年曾與彭明敏搭檔參選總統、副總統。2016年6月至2024年8月出任駐日代表，持續推動台日地方交流、經貿互動及災害互助，並參與2021年日本疫苗援台的多方協調。返台後曾任總統府資政，2026年1月6日接任臺灣日本關係協會會長；舊任行政院長、市長、立委、黨主席與駐日代表均不列現職。2026年3月公開討論總統直選、民主與轉型正義，同年10月11日出席台北保安宮活動支持沈伯洋，顯示下半年仍參與公開政治活動。'
urls=[('會長簡介','https://subsite.mofa.gov.tw/aear/cp.aspx?n=5831'),('謝長廷掌台日關係協會 善的循環助深化雙邊關係','https://www.cna.com.tw/news/aipl/202601060305.aspx'),('謝長廷吹陶笛挺沈伯洋','https://news.ttv.com.tw/news/11510110001400W'),('2025年秋季外國人敘勳','https://www.koryu.or.jp/tw/?dispmid=6711&itemid=4642'),('謝長廷先生、游芳枝女士訪問記','https://dlbs.liberal.ntu.edu.tw/museum/TAIWAN/md/md05-12.htm')]+[(s['topic'],s['source']) for s in p['political_stances']]
p['collection_meta']=dict(collection_date='2026-11-17',phase='phase4_person_profile',data_sources=['official_website','news_search','other'],quotes=[dict(title=t,url=u) for t,u in urls],notes='官方會長簡介與中央社、台視交叉確認現職及2026-10-11政治活動，證據活動截止該日。官方列資政至2026-01，維基列2026-05，優先官方年月，不沿用現職。英文名依官方完整原文。主要任職年月依官方，早年律師無確切任期不造日期。生日沿用原檔並由百科交叉，家庭依台大保存中研院1999-02-20具名訪談單源收錄，僅必要關係。彭明敏引用已讀真實000096畫像。兩項成果的具體協調與自治體數字主要依中央社單源，日方僅交叉肯定交流貢獻，非個人獨力成果。保留原QID、profile和全部social原字段；實查records.json無本人物姓名或帳號匹配，未新增用戶表帳號。搜尋多平台，未找到可獨立確認新增個人帳號；中央社2026-01-06照片來源亦指向原Facebook頁。原twitter實時認證未核。')
dest=root/'tmp/tw_batch9_enriched/TW-PERSON-000021.json';dest.parent.mkdir(exist_ok=True)
jsonschema.validate(p,json.loads((root/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')))
dest.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8');print('jsonschema PASS')

import json
from pathlib import Path
p=Path('output/tw/2026-07-27/persons/TW-PERSON-000512.json')
d=json.loads(p.read_text(encoding='utf-8-sig'))
d['gender']='male'
d['birth_place']='台湾基隆市'
d['current_positions']=['政治评论员','《赵少康时间》主持人']
d['education']=[dict(institution='国立台湾大学（國立臺灣大學）',degree='bachelor',field='农业工程',start_date=None,end_date=None),dict(institution='克莱门森大学（Clemson University）',degree='master',field='机械工程',start_date=None,end_date=None)]
def work(o,p,s=None,e=None,i=None): return dict(organization=o,position=p,start_date=s,end_date=e,org_id=i)
d['work_experience']=[work('经济部国际贸易局（經濟部國際貿易局）','专员'),work('国立台湾大学（國立臺灣大學）','农业工程学系兼任副教授'),work('台北市议会（臺北市議會）','第四、五届议员','1981-12-25','1987-01-31'),work('立法院','第一届增额立法委员','1987-02-01','1991-05-31','TW-GOV-020'),work('行政院环境保护署（行政院環境保護署）','署长','1991-06-01','1992-11-15'),work('立法院','第二届立法委员','1993-02-01','1994-12-06','TW-GOV-020'),work('新党（新黨）','首届全国委员会召集人','1993-08','1994','TW-PARTY-015'),work('飞碟广播公司（飛碟廣播公司）','董事长（历史任职）'),work('中国广播公司（中國廣播公司）','董事长兼总经理','2006-12-23','2007-10-24'),work('中国广播公司（中國廣播公司）','董事长兼总经理','2009-05-04','2024-01-01')]
pts='https://news.pts.org.tw/live/52'
d['political_stances']=[dict(date='2026-03-22',topic='核能与能源成本',stance_content='在脸书评论中支持核电，批评停用核电增加发电成本；报道中的成本估算与政府欠款说法属于其政治评论，未经本画像独立审计。',source='https://news.tvbs.com.tw/politics/3157929'),dict(date='2024-01-01',topic='人工智能产业',stance_content='在副总统候选人辩论会上主张利用台湾半导体及软硬件优势发展人工智能，并认为政府相关投资规划过于保守。',source=pts),dict(date='2024-01-01',topic='宪政制度',stance_content='在辩论会回应副总统定位时主张推动内阁制及联合政府，并邀请民众党参与；这是竞选主张，未作为已实施制度记录。',source=pts)]
d['person_relationships']=[dict(person_id='TW-PERSON-000533',person_name='侯友宜',relationship_type='colleague',description='2024年总统选举共同组成国民党正副总统候选人组合；仅记录该次竞选合作。')]
d['major_achievements']=[dict(date='1993-08-10',achievement='参与创建新党并出任首届全国委员会召集人，为已发生的组织创办职业节点。',organization='新党（新黨）')]
d['family_members']=[]
d['biography_summary']='赵少康出生于台湾基隆，毕业于国立台湾大学，并取得美国克莱门森大学机械工程硕士学位。返台后曾在国际贸易局任职，也在台湾大学兼任教学，随后进入民意机关，先后担任台北市议员及增额立法委员。1991年进入行政院担任环境保护署署长，1992年离任，之后再度当选立法委员。1993年参与成立新党并出任首届全国委员会召集人。离开主要公职后转入广播与电视媒体，曾经营飞碟广播及中国广播公司，并长期从事时事评论及节目主持。2024年与侯友宜搭档参加总统选举，竞选期间于元旦宣布辞去中广董事长、总经理及董事职务。2026年仍有其主持节目的实际发布记录；本画像将其公共政策发言视为本人意见，区分竞选提案与已经实施的治理成果。'
sources=[('赵少康：生平、教育及历史任期','https://zh.wikipedia.org/wiki/趙少康'),('赵少康宣布辞中广董事长','https://www.cna.com.tw/news/aipl/202401015002.aspx'),('中广新董座出炉：NCC通过陈圣一任董总','https://www.nownews.com/news/6368110'),('副总统候选人辩论会完整报道',pts),('聽說趙少康：2026-11-04实际节目发布','https://skjaw.firstory.cc/'),('核电成本评论','https://news.tvbs.com.tw/politics/3157929')]
d['collection_meta']=dict(collection_date='2026-11-15',phase='phase4_person_profile',data_sources=['wikipedia','news_search','social_media'],quotes=[dict(title=t,url=u) for t,u in sources],notes='近期实际活动核至2026-11-04，Firstory节目页明确列主持人及39分22秒节目，不以2026-10-14访谈预告推定完成。2024-01-01辞中广董总由中央社及NOWnews继任报道交叉核实。历史教育与部分任期主要依维基，召集人结束月份与立委结束日期在维基不同段落有冲突，采用信息框立委日期、召集人仅记年份。完成本人社交检索，未据节目机构账号新增本人社交账号。家庭未获两独立原文确认故留空。出版书籍检索已尝试但书目、售书原文读取失败，未以摘要填成果；仅保留一项组织创办成果，未凑两项。中广讲师简介两次超时。原QID与头像完整保留；组织索引和实际画像已核立法院、新党，侯友宜画像已核；未确认组织ID留null。')
out=Path('tmp/tw_batch5_enriched/TW-PERSON-000512.json');out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')

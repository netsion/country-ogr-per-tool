import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';p='TW-PERSON-000041'
x=json.loads((B/'persons'/f'{p}.json').read_text(encoding='utf-8'))
x['name']='陳其邁';x['current_positions']=['高雄市市长']
x['education']=[dict(institution=n,degree=d,field=f,start_date=None,end_date=None) for n,d,f in [('中山医学院（中山醫學院）','bachelor','医学'),('台湾大学（國立臺灣大學）','master','公共卫生预防医学')]]
def w(s,e,n,pos,oid=None):return dict(start_date=s,end_date=e,organization=n,position=pos,org_id=oid)
x['work_experience']=[w('1996','2004','立法院','立法委员','TW-GOV-020'),w('2004','2005','行政院','政务委员兼发言人','TW-GOV-019'),w('2005','2005','高雄市政府','代理市长'),w('2007','2008','总统府（總統府）','副秘书长','TW-GOV-023'),w('2012','2018','立法院','立法委员','TW-GOV-020'),w('2019','2020','行政院','副院长','TW-GOV-019'),w('2020-08-24',None,'高雄市政府','市长')]
u='https://www.cna.com.tw/news/aipl/202412230025.aspx';v='https://www.cna.com.tw/news/aipl/202412250029.aspx'
x['political_stances']=[dict(date='2024-12-23',topic='产业转型',stance_content='主张以半导体投资带动传统工业升级，完善南部供应链。',source=u),dict(date='2024-12-23',topic='投资基础设施',stance_content='主张公共部门配合产业所需的水电、人才和交通服务；不将项目规划等同完工。',source=u),dict(date='2024-12-25',topic='高铁南延',stance_content='对南延方案提出条件式支持，强调建设方案须符合城市整体交通需求；属于政策讨论而非已完工成果。',source=v)]
x['major_achievements']=[dict(date='2025-Q4'.replace('-Q4',''),achievement='任内台积电高雄基地参与2奈米量产布局，中央社2026-01-01报道引述企业已进入2025年第4季量产；企业技术与中央、市府配套的共同成果，非个人独力完成，后续就业产值仍属预测。',organization='高雄市政府'),dict(date='2024-12-23',achievement='中央社专访记录市府配合台积电建厂推进再生水及周边基础设施；属市长自陈的团队配套工作，不将供水数字作为本轮独立工程审计结论。',organization='高雄市政府')]
x['person_relationships']=[dict(person_id='TW-PERSON-000011',person_name='韩国瑜（韓國瑜）',relationship_type='political_rival',description='2018年高雄市长选举中的竞争对手；仅限该场选举关系，来源维基履历，不推断私人关系。')]
x['family_members']=[dict(person_id=None,name='吴虹（吳虹）',relationship='spouse',industry_or_organization='医师；中央社及公视公开报道确认配偶身份，仅记录最小信息。')]
x['biography_summary']='陈其迈是台湾地区政治人物，现任高雄市长，具有医学和公共卫生教育背景。高雄市府官方简介列明其毕业于中山医学院医学系，并取得台湾大学公共卫生研究所预防医学硕士学位。其职业经历从医疗与公共事务延伸至立法、中央行政和地方治理，曾任立法委员、行政院政务委员兼发言人、总统府副秘书长及行政院副院长。2005年曾代理高雄市长；2018年参选市长落败，2020年参加补选并于同年8月就任，2022年连任。其公开施政重点包括产业转型及配套基础设施，推动半导体供应链在高雄发展，同时参与城市交通建设方案讨论。本档将历史立委、副院长及代理党主席身份从现职栏移除，不提前使用2026年底换届结果。项目成就记录区分企业量产、市府团队配套与未来预测；公开家庭关系仅保留配偶吴虹，不延伸未必要的私人资料。'
quotes=[('高雄市府市长简介','https://www.kcg.gov.tw/cp.aspx?Create=1&n=59C096A5BBC7AFB1'),('中央社：产业转型专访',u),('中央社：高铁南延方案',v),('中央社：高雄2奈米量产','https://www.cna.com.tw/news/aloc/202601010101.aspx'),('公视：高雄市长夫人辅选','https://news.pts.org.tw/article/413219'),('中央社：配偶吴虹辅选','https://www.cna.com.tw/news/aipl/202211220125.aspx'),('维基百科：陈其迈履历','https://zh.wikipedia.org/wiki/陳其邁')]
x['collection_meta']=dict(collection_date='2026-11-14',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia'],quotes=[dict(title=t,url=u) for t,u in quotes],notes='官方现职页未显示精确更新日期，最近所读独立现职报道为2026年1月。教育由官方和中央社交叉；早期任期精确日期及2018竞争关系依维基单源。配偶由公视及中央社原文交叉。原头像、四个平台账号与user_id完全保留，多平台搜索发现既有账号，不宣称平台认证。成就为企业与市府团队成果，市府配套为自陈，不计预测为完成。')
(R/'tmp/tw_batch2_enriched'/f'{p}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

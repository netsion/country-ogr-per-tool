import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';x=json.loads((B/'persons/TW-PERSON-000172.json').read_text(encoding='utf-8'))
x['name']='邱議瑩';x['current_positions']=['第11届立法委员']
x['education']=[dict(institution='加利福尼亚多明尼克大学（Dominican University of California）',degree='master',field=None,start_date=None,end_date=None)]
def w(s,e,o,p,oid=None):return dict(start_date=s,end_date=e,organization=o,position=p,org_id=oid)
x['work_experience']=[w('1996','2000','国民大会（國民大會）','代表'),w('2002','2005','立法院','立法委员','TW-GOV-020'),w('2005-06-10','2008-02-01','客家委员会（客家委員會）','副主任委员'),w('2008',None,'立法院','立法委员','TW-GOV-020')]
u='https://www.ftvnews.com.tw/news/detail/2025B30W0432'
x['political_stances']=[dict(date='2025-11-30',topic=t,stance_content=c,source=u) for t,c in [('交通物流','竞选演说主张建设全天运营新机场、衔接港口物流；只是规划，不认定设施已建成。'),('产业与就业','主张投入AI基础建设及传统产业升级，并提出未来五年就业目标；不将预测职位数作为已发生就业成果。'),('全龄照顾','提出增加敬老卡点数、儿童支持及临时托育资源；为附条件竞选承诺，非已实施市政。')]]
x['major_achievements']=[dict(date='2025-11-30',achievement='当日演说回顾其推动再生医疗立法的工作；仅记录本人自陈参与，不认定独力完成立法或已产生医疗效果。',organization='立法院')]
x['person_relationships']=[dict(person_id=None,person_name='李永得（李永得）',relationship_type='superior',description='历史行政上下级：2005至2008年在客家委员会分别任副主委及主委，来源维基履历与公视共事报道；不表示当前上下级。')]
x['family_members']=[dict(person_id=None,name='李永得（李永得）',relationship='spouse',industry_or_organization='仅记录公视与TVBS原文确认的公开配偶身份。')]
x['biography_summary']='邱议莹是台湾地区政治人物，担任第11届立法委员。其政治经历包括国民大会代表、立法委员及客家委员会副主任委员，之后持续参与议会工作。公开履历列有加利福尼亚多明尼克大学硕士学历，本轮未对学位取得年份作无来源推定。她在2025年的地方初选演说中提出交通物流、人工智慧与传统产业转型、全龄照顾等方向，本档将这些内容视作当时竞选主张，不作为已经实施的政策，也不把就业预测算作成果。2026年10月立法院经济委员会会议记录可见其公开质询，但不凭一次出席便推定召委身份，因此当前职位仅保留立法委员。早期任职资料与精确日期主要依维基履历，仍需后续补证。家庭仅记录公开配偶李永得的姓名与关系，不收录健康、财产或其他私人事项。'
x['collection_meta']=dict(collection_date='2026-11-14',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia'],notes='现职经2026-10立院议事记录与独立媒体交叉；不沿用旧国大代表或旧召委，不将初选当已任市长。学历及早期日期仍维基单源。成就参与为本人演说自陈，非独立绩效认定。李永得无本地画像，ID留空，配偶经公视与TVBS交叉。中央社与Newtalk政策页仅壳，未据摘要采信。已多平台检索，原三个账号/user_id和头像完全保留，未新增未认证账号。',quotes=[dict(title=t,url=v) for t,v in [('维基邱议莹履历','https://zh.wikipedia.org/wiki/邱議瑩'),('立院第6会期经济委员会会议','https://ppg.ly.gov.tw/ppg/sittings/2026100882/details?meetingDate=115%2F10%2F15'),('民视2025完整竞选演说',u),('TVBS公开配偶访谈','https://news.tvbs.com.tw/politics/3042731'),('公视公开婚姻报道','https://news.pts.org.tw/article/177158')]])
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
(R/'tmp/tw_batch3_enriched/TW-PERSON-000172.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

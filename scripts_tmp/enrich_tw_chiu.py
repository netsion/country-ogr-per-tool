import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';pid='TW-PERSON-000529';x=json.loads((B/'persons'/f'{pid}.json').read_text(encoding='utf-8'))
cv='https://www.ey.gov.tw/File/E8E118B148864E69?A=C';wiki='https://en.wikipedia.org/wiki/Chiu_Chui-cheng';appoint='https://www.cna.com.tw/news/aipl/202404250057.aspx';exchange='https://www.cna.com.tw/news/acn/202611110134.aspx';trade='https://www.cna.com.tw/news/aipl/202608210177.aspx';order='https://www.president.gov.tw/Page/294/49484'
x.update(name='邱垂正',name_en='Chiu Chui-cheng',current_positions=['大陆委员会主任委员'],gender='male')
x['education']=[dict(institution=n,degree=d,field=f,start_date=None,end_date=None) for n,d,f in [('东吴大学（東吳大學）','bachelor','政治学'),('台湾大学（國立臺灣大學）','master','国家发展'),('台湾师范大学（國立臺灣師範大學）','doctorate','政治学')]]
jobs=[(None,None,'金门大学（國立金門大學）','助理教授、副教授',None),('2016','2023','大陆委员会（大陸委員會）','副主任委员兼发言人',None),('2023','2024','海峡交流基金会（海峽交流基金會）','副董事长兼秘书长',None),('2024-05-20',None,'大陆委员会（大陸委員會）','主任委员',None)]
x['work_experience']=[dict(start_date=a,end_date=b,organization=o,position=t,org_id=i) for a,b,o,t,i in jobs]
x['biography_summary']='邱垂正是台湾地区政治人物与两岸事务研究者，现任大陆委员会主任委员。行政院官方人事履历列明，他毕业于东吴大学政治学系，取得台湾大学国家发展研究所硕士和台湾师范大学政治学研究所博士，曾任国会助理、大陆委员会机要秘书、金门大学助理教授及副教授。他于2016年进入大陆委员会担任副主任委员及发言人，后转任海峡交流基金会副董事长兼秘书长，2024年受任为大陆委员会主任委员。其学术与行政经历均围绕两岸关系及相关公共政策，近期公开发言涵盖两岸交流的风险管理、农产品贸易与市场多元化，以及防卫和经济安全韧性。记录这些表述时，本档保留其讲话主体身份，不将其对另一方意图、风险或效果的判断当成客观已证事实。官方履历及任命材料与近期中央社报道相互参照核实当前职务；部分旧任期只掌握年份，故不补造精确日期。对于尚未获取独立成效评估或双重家属身份原文的信息，保留空值并说明检索边界。'
x['political_stances']=[dict(date='2026-11-11',topic='两岸交流风险管理',stance_content='主张支持正常健康交流，并朝向去统战化、去政治化、去风险化；其有关政治风险的描述属于本人政策判断。',source=exchange),dict(date='2026-08-21',topic='农产品贸易与市场多元化',stance_content='表示支持地方协助农产品外销，倡议回到专业及科学方式处理贸易，并协助农民全球布局；相关承诺不作为已完成外销成果。',source=trade),dict(date='2026-11-11',topic='防卫与经济韧性',stance_content='主张落实和平四大支柱行动方案，强化国防、经济安全和全社会防卫韧性，并深化民主伙伴合作。',source=exchange)]
x['major_achievements']=[]
x['person_relationships']=[dict(person_id='TW-PERSON-000001',person_name='赖清德（賴清德）',relationship_type='superior',description='赖清德公布由邱垂正出任陆委会主委，任命公报确认2024年5月20日特任，限定为工作任命关系。',source=order,corroborating_sources=appoint)]
x['family_members']=[]
qs=[('行政院官方副首长学历履历',cv),('英文人物背景',wiki),('CNA国安人事',appoint),('2024年任命公报',order),('CNA交流风险讲话',exchange),('CNA农产品贸易讲话',trade)]
x['collection_meta']=dict(collection_date='2026-11-13',phase='phase4_person_profile',data_sources=['official_website','wikipedia','news_search','web_search'],quotes=[dict(title=t,url=u) for t,u in qs],notes='已读行政院官方人事履历、总统府公报、Wikipedia及CNA原文；陆委会官网履历403未作为已读来源。学历与性别由行政院PDF明确，旧任期按维基年精度，当前任命以2024-05-20公报。QID无可靠确认保持null，出生精确日期未知未新增。三项政策为本人讲话，不将两岸政治指控或风险判断当客观事实。主要成果实际搜索治理、出版、获奖及勋章；结果多误匹配邱国正，出版社页面仅返回简介壳、未直读到确定出版年份，故不把演讲或任命充数，成果暂空。家庭查配偶父母，詹孟芬仅有维基和财产申报索引线索，没有两篇独立关系原文，故不录入；不抓取财产细节。6社交平台Facebook/X/Instagram/LinkedIn/TikTok/YouTube已检索，未取得可靠本人主页，TikTok受robots限制，不绑定同名。profile原缺省保持缺省，社媒仍空。所有工作机构无已核实实际同名画像，org_id维持null；赖清德人物档已核主名及TW身份。')
z=json.loads((B/'persons/TW-PERSON-000001.json').read_text(encoding='utf-8'));assert z['name_zh']=='赖清德'
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
(R/'tmp/tw_batch2_enriched'/f'{pid}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

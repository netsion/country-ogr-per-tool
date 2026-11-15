import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];p=R/'output/tw/2026-07-27/persons/TW-PERSON-000536.json';x=json.loads(p.read_text(encoding='utf-8'))
official='https://www.motc.gov.tw/ch/app/artwebsite/view?id=10053&module=artwebsite'
annual='https://www.motc.gov.tw/ch/app/data/view?id=14&module=news&serno=e671449f-497e-4aaf-9711-e770b81d1cd5'
pts='https://news.pts.org.tw/article/728602';ltn='https://ec.ltn.com.tw/article/breakingnews/5173184';wiki='https://en.wikipedia.org/wiki/Chen_Shih-kai'
x.update(name_en='Chen Shih-kai',gender='male',current_positions=['交通部部长'],birth_date=None)
x['education']=[dict(institution=n,degree=d,field=f,start_date=None,end_date=y) for n,d,f,y in [('东海大学（東海大學）','bachelor','政治学','2002'),('台北科技大学（國立臺北科技大學）','master','经营管理EMBA','2022')]]
x['work_experience']=[dict(organization=n,org_id=i,position=t,start_date=s,end_date=e) for n,i,t,s,e in [('台中市议会（臺中市議會）',None,'市议员','2010-12','2022-12'),('行政院', 'TW-GOV-019','发言人','2024-05','2024-09'),('交通部',None,'部长','2024-09-02',None)]]
x['political_stances']=[dict(date=d,topic=t,stance_content=c,source=u) for d,t,c,u in [('2024-12-12','公共运输常客优惠','主张在既有月票外增加单一运具、跨生活圈常客优惠，并评估常态预算；当时为规划，不将其视为已上线。',pts),('2025-09-10','交通韧性与产业','主张以交通网络连接供应链及区域生活圈，将交通基础设施作为国土韧性的组成。',ltn),('2026-02-10','交通安全与偏乡服务','主张持续改善路口、驾驶教育与偏乡弹性预约服务；目标不视作已经达成。',annual)]]
x['major_achievements']=[dict(date=d,achievement=a,organization='交通部') for d,a in [('2026-01-31','任内平溪线全线复驶；依据交通部2026-02-10发布，属于铁路及工程团队成果，不归为个人独力，也未独立审计工程品质。'),('2025','任内交通部报告完成停止线与行穿线最小净距相关法规修订及省道路口照明改善；依据2026-02-10官方回顾，仅记制度和工作完成，不将事故变化作个人因果效果。')]]
x['person_relationships']=[dict(person_id='TW-PERSON-000018',person_name='卓荣泰（卓榮泰）',relationship_type='superior',description='2024年卓荣泰组阁时担任行政院发言人，后转交通部长；仅记录该行政任职关系，依据英文维基及官方历任经历，不推私人或派系联盟。')]
x['biography_summary']='陈世凯是台湾地区政治人物，现任交通部部长。交通部官方履历列有东海大学政治学系及台北科技大学经营管理EMBA硕士学历，曾担任第一至第三届台中市议员，并有民进党中央评议委员及中央常务委员经历。2024年5月进入行政院担任发言人，同年9月接任交通部长。其公开政策涉及公共运输、道路安全、偏乡移动服务与交通基础设施韧性。既有TPASS计划在其接任前已经启动，本档仅记录其任内对常客优惠和预算安排的说明，不将整个制度归为其个人创立。平溪线复驶及道路配套修订按交通部团队发布记录，未将规划项目或预期经济效果当作已经完成成果。未充分核实的家庭及本人社交账号保持空值。'
x['collection_meta'].update(data_sources=['official_website','news_search','wikipedia'],quotes=[{'title':t,'url':u} for t,u in [('交通部首长履历',official),('交通部2026新春施政回顾',annual),('公视TPASS常客优惠说明',pts),('自由财经交通韧性论坛',ltn),('英文维基陈世凯履历及英文名',wiki)]],notes='现职官方及2026-02官方发布支持，2025-09独立报道交叉。出生日期未多源核实故留null；早期精确任期与英文名仍维基辅助。具体施政成果为官方自陈和跨机关团队贡献，非独立效果审计；TPASS非本人创立。家庭仅一轮检索未充分交叉不收录。社交平台搜索未核实个人账号，不收机构账号；profile保持null。')
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
(R/'tmp/tw_batch3_enriched/TW-PERSON-000536.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

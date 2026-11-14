import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';pid='TW-PERSON-000528';x=json.loads((B/'persons'/f'{pid}.json').read_text(encoding='utf-8'))
official='https://www.president.gov.tw/Page/107';wiki='https://zh.wikipedia.org/wiki/潘孟安';appoint='https://www.cna.com.tw/news/aipl/202404250057.aspx';hand='https://www.president.gov.tw/News/28426';debt='https://www.cna.com.tw/news/aloc/202203170278.aspx';city='https://www.cna.com.tw/news/aipl/202006090288.aspx';care='https://www.cna.com.tw/postwrite/chi/301770'
x.update(name='潘孟安',name_en='Pan Men-an',current_positions=['总统府秘书长'])
x['education']=[dict(institution=n,degree='master',field=f,start_date=None,end_date=None) for n,f in [('高雄师范大学（國立高雄師範大學）','成人教育'),('台湾大学（國立臺灣大學）','国家发展')]]
jobs=[('1994','1998','车城乡民代表会（車城鄉民代表會）','乡民代表',None),('1998','2005','屏东县议会（屏東縣議會）','议员',None),('2005','2014','立法院','第6、7、8届立法委员','TW-GOV-020'),('2014','2022','屏东县政府（屏東縣政府）','县长',None),('2024-05-20',None,'总统府（總統府）','秘书长','TW-GOV-023')]
x['work_experience']=[dict(start_date=a,end_date=b,organization=o,position=t,org_id=i) for a,b,o,t,i in jobs]
x['biography_summary']='潘孟安是台湾地区政治人物，现任总统府秘书长。总统府官方履历列有高雄师范大学成人教育研究所硕士及台湾大学国家发展研究所硕士学历，并记录其从基层民意代表到地方行政首长的从政路径。他于1994年至1998年担任屏东县车城乡乡民代表，之后进入屏东县议会，2005年至2014年担任第6、7、8届立法委员，2014年至2022年任屏东县县长。县长任内的公开施政重点包括财政开源节流、交通与公共环境基础建设、医疗及长照资源等。有关减债规模在本档明确标注为县府团队和本人对外报告的数值，未作为经过本轮独立财政审计的结论。2024年赖清德公布国安及府院人事安排后，他于5月20日从林佳龙手中接下总统府秘书长印信。其当前幕僚职务与历史地方治理经历分开记录，不将旧县长头衔混入现职。家庭检索没有取得可确认具体家属全名的双重可靠原文，因此不猜测或生成空壳家庭条目。'
x['political_stances']=[dict(date='2022-03-17',topic='地方财政',stance_content='主张县政财政应开源节流、精打细算，不举新债还旧债；这是其公开财政治理主张。',source=debt),dict(date='2020-06-09',topic='偏乡基础建设与公共服务',stance_content='表示持续推动交通网、污水下水道、水系整治、医疗资源及农业等建设，以改善屏东生活条件。相关方向为施政表述，不能全数视为完工成果。',source=city),dict(date='2021-10-17',topic='社区长照',stance_content='在长照人员表扬活动表示应增设社区整体照顾资源，跟上人口老化、减轻家庭照顾负担；来源为县府供稿，非中央社记者独立报道。',source=care)]
x['major_achievements']=[dict(date='2020-06-09',achievement='在远见县市长施政满意度调查中再次获五星首长肯定；这是媒体调查评价，不等同所有政策效果的独立验证。',organization='屏东县政府（屏東縣政府）'),dict(date='2022-03-17',achievement='对外报告县府团队七年减债175.23亿元，短债归零；这是其本人及县府对外陈述、由中央社报道，本轮未独立核对财政决算，不将其全归个人。',organization='屏东县政府（屏東縣政府）')]
x['person_relationships']=[dict(person_id='TW-PERSON-000001',person_name='赖清德（賴清德）',relationship_type='superior',description='赖清德公布邀请潘孟安担任总统府秘书长，2024年5月20日完成交接，限定为明确任命工作关系。',source=appoint,corroborating_sources=hand)]
x['family_members']=[]
qs=[('总统府秘书长现职及履历',official),('人物背景线索',wiki),('CNA国安人事',appoint),('官方交接记录',hand),('CNA县政财政报道',debt),('CNA城市建设及调查评价',city),('屏东县政府长照供稿',care)]
x['collection_meta']=dict(collection_date='2026-11-13',phase='phase4_person_profile',data_sources=['official_website','wikipedia','news_search','web_search'],quotes=[dict(title=t,url=u) for t,u in qs],notes='已读总统府、Wikipedia及CNA原文，教育和任职主轴以官方为准，履历按官方年份精度，不填未知日。QID未获得可靠正文确认保持null，未新增生日及性别断言。政策3主题均有本人讲话报道；长照原文发表于10月18日但活动17日，日期用活动日，且明确为县府供稿非独立记者。减债仅为公开报告事实、不是本轮审计结果；五星奖是调查评价不作客观完美治理结论。家庭定向检索配偶父母，许多结果误指柯建铭配偶或其他群众，不可归为本人；历史未婚报道不足确认当前婚姻，未形成双可靠家属全名证据故留空。六平台Facebook/X/Instagram/LinkedIn/TikTok/YouTube检索，未取可靠个人主页原文，TikTok受robots限制，社媒保持空；profile原本缺省未新增。人物引用已核赖清德档案TW国别及主名；立法院和总统府均存在相符组织档案，未知地方机构保持null。')
for oid in ['TW-GOV-020','TW-GOV-023']:
 z=json.loads((B/'orgs'/f'{oid}.json').read_text(encoding='utf-8'));assert z['basic_info']['country_iso3']=='TWN'
z=json.loads((B/'persons/TW-PERSON-000001.json').read_text(encoding='utf-8'));assert z['name_zh']=='赖清德'
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(x)
(R/'tmp/tw_batch2_enriched'/f'{pid}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

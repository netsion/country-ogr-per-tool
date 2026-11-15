import json,pathlib,jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27'
d=json.loads((B/'persons/TW-PERSON-000030.json').read_text(encoding='utf-8'))
d['name']='唐鳳';d['current_positions']=['无任所大使']
d['education']=[]
def w(a,b,o,p,oid=None):return dict(start_date=a,end_date=b,organization=o,position=p,org_id=oid)
d['work_experience']=[w('2016','2022','行政院','数位政务委员','TW-GOV-019'),w('2022','2024','数字发展部（數位發展部）','部长'),w('2024-10-07',None,'外交部','无任所大使','TW-GOV-024')]
u='https://www.cna.com.tw/news/aipl/202502160084.aspx'
d['political_stances']=[dict(date='2025-02-15',topic=t,stance_content=s,source=u) for t,s in [('数字自由与安全','主张以民主参与及社会共识同时增进自由与安全，不将二者视为必然取舍。'),('公私协作治理','主张公民社会和私部门共同确立治理价值，政府不独占数字治理；为本人受访立场。'),('跨国数字合作','主张以具体多边项目分享台灣数字治理经验，而不只提升知名度；不将倡议当已完成合作。')]]
d['major_achievements']=[dict(date='2025',achievement='获Right Livelihood奖；颁奖机构与哥伦比亚大学交叉确认，属公开荣誉，不将评奖赞誉当独立量化绩效。',organization='正命奖基金会（Right Livelihood）'),dict(date='2020',achievement='任数位政委期间参与疫情口罩资讯工具及公民科技协作；依据颁奖机构及大学回顾，属于政府、公民黑客与社会团队共同贡献，不将平台或公共卫生效果归为个人独力。',organization='行政院')]
d['person_relationships']=[dict(person_id='TW-PERSON-000023',person_name='林佳龙（林佳龍）',relationship_type='colleague',description='2024无任所大使聘书由外交部长林佳龙副署，记录该外交任命及职务关系，不推私人联盟；来源总统府公报7746号。')]
d['family_members']=[]
d['biography_summary']='唐凤是台湾地区公民科技与数字治理实践者，具有自由软件、开放政府和公民参与方面的公共工作经历。其职业发展从开源技术社群逐步进入政府，在2016年至2022年担任行政院数位政务委员，2022年至2024年任首任数位发展部部长。2024年10月7日总统聘书列其为无任所大使，聘期至2028年5月19日；大学机构简介和中央社采访亦确认其外交角色，因此本档不再把旧部长或政委身份列为现职。其政策主张集中于开放协作、数字人权、社会共识与跨国治理经验交流。2025年获得Right Livelihood奖，其数字参与实践受到颁奖机构肯定；有关公众信任及政策成效的宣传性数字未作为本轮独立评估结论。疫情资讯服务与开放平台属于跨机关及公民社群协作，非个人独力创建全部成果。本档未扩大记录家庭、健康或其他私人事项。'
quotes=[('总统府公报7746号：2024-10-07聘书','https://www.president.gov.tw/File/Doc/7ecb901f-747d-49d7-81e4-864f8c14246a'),('哥伦比亚大学机构人物介绍','https://igp.sipa.columbia.edu/distinguished-fellows/Audrey-Tang'),('Right Livelihood官方获奖简介及社交链接','https://rightlivelihood.org/zh-hant/the-change-makers/find-a-laureate/audrey-tang/'),('中央社慕尼黑专访',u),('英文维基职业履历','https://en.wikipedia.org/wiki/Audrey_Tang')]
d['collection_meta']=dict(collection_date='2026-11-15',phase='phase4_person_profile',data_sources=['official_website','news_search','wikipedia'],quotes=[dict(title=t,url=v) for t,v in quotes],notes='总统府聘书核2024-10-07起聘及2028-05-19届期，当前角色有大学及中央社交叉；未宣称逐日确认。教育为自学经历且未核正式毕业学校，不造学历。旧公职起迄仅保留已知年份。出生日期有颁奖机构与原资料交叉。政策日期是中央社记载的15日采访，非16日发布日期。疫情项目年份据历史背景及回顾，实际贡献为团队；奖项不是量化治理成效。林佳龙真实画像已核。家庭未充分交叉不收录。已检索社交平台，保留原4账号、user_id与头像；颁奖页IG为digitalminister.one，旧账号归属变化未核清，不替换旧ID，不采同名LinkedIn。')
jsonschema.Draft7Validator(json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))).validate(d)
p=R/'tmp/tw_batch4_enriched/TW-PERSON-000030.json';p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')

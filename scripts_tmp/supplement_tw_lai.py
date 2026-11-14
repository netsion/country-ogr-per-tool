import json,pathlib,shutil,jsonschema
p=pathlib.Path('output/tw/2026-07-27/persons/TW-PERSON-000001.json');x=json.loads(p.read_text(encoding='utf-8-sig'));before={k:len(x.get(k,[])) for k in ['political_stances','major_achievements','person_relationships','family_members']}
b=pathlib.Path('tmp/tw_supplement_before');b.mkdir(parents=True,exist_ok=True)
if not (b/p.name).exists():shutil.copy2(p,b/p.name)
q=x['collection_meta']['quotes']
urls={
'speech':'https://www.president.gov.tw/Page/700',
'energy':'https://www.president.gov.tw/NEWS/40465',
'health':'https://www.president.gov.tw/NEWS/28673',
'healthcna':'https://www.cna.com.tw/news/aipl/202408220397.aspx',
'air':'https://www.ey.gov.tw/Page/9277F759E41CCD91/f5fe1246-f8a3-48ef-97cc-1a74a1889bc4',
'aircna':'https://www.cna.com.tw/news/firstnews/201806255005.aspx',
'wife':'https://www.cna.com.tw/news/aipl/202312270278.aspx',
'wife2':'https://udn.com/news/story/6656/9345949',
'appoint':'https://www.president.gov.tw/Page/294/49484',
'cabinet':'https://www.cna.com.tw/news/aipl/202404105002.aspx',
'inaug':'https://www.president.gov.tw/NEWS/28424',
'tsai':'https://www.cna.com.tw/news/firstnews/202005205002.aspx'}
for k,u in urls.items():
 if not any(z['url']==u for z in q):q.append({'title':{'speech':'赖清德2024就职演说','energy':'赖清德2026年11月2日绿色转型讲话','health':'健康台湾委员会首次会议','healthcna':'中央社：首次健康台湾委员会','air':'行政院：2018空污法修法','aircna':'中央社：空污法三读','wife':'中央社：赖清德配偶吴玫如','wife2':'联合报：赖清德与配偶吴玫如公开申报报道','appoint':'2024年5月20日任命公报','cabinet':'中央社：卓荣泰等内阁任命','inaug':'2024年就职典礼','tsai':'中央社：蔡英文赖清德2020就职'}[k],'url':u})
def stance(d,t,c,u):return dict(date=d,topic=t,stance_content=c,source=u)
x['political_stances'] += [
stance('2024-05-20','两岸对话与维持现状','在就职演说中主张维持现状，并提出在对等与尊严原则下以对话代替对抗、恢复交流。此为本人政治主张的记录，不代表事实认定。',urls['speech']),
stance('2024-05-20','国防与经济安全','在就职演说提出和平四大支柱方案，涵盖强化防卫、经济安全、两岸关系及价值外交，以提升威慑能力。',urls['speech']),
stance('2024-05-20','产业创新与民生','在就职演说主张政府和产业界合作，推动智慧永续、全球布局及产业发展，并以健康、照顾与社会支持回应民生需要；此为政策方向而非完成成果。',urls['speech']),
stance('2024-08-22','公共卫生与医疗平权','主持健康台湾推委会首次会议时主张整合区域医疗资源，改善医事人员工作环境，并培育人才、发展智慧医疗以提升健康照护。',urls['health']),
stance('2026-11-02','能源管理与净零转型','接见企业环保奖代表时主张结合产业与社会力量推进2050净零转型，并规划碳边境调节与碳排放交易制度以衔接国际；不把规划写为已实施。',urls['energy'])]
x['major_achievements'] += [
dict(date='2018-06-25',achievement='担任行政院长期间，其行政团队推动的空气污染防制法修正案经立法院三读通过，纳入空品维护区授权与不法利得追缴等制度。属于行政、立法共同完成的制度成果，不归为个人独立功绩。',organization='行政院、立法院'),
dict(date='2024-08-22',achievement='以召集人身份主持健康台湾推动委员会首次会议，启动跨领域健康政策沟通机制；记录已经举行的制度运作，不把预期寿命或癌症死亡率目标视作达成。',organization='总统府（總統府）')]
def rel(pid,n,t,d,a,b):return dict(person_id=pid,person_name=n,relationship_type=t,description=d+' 交叉证据：'+a+' ；'+b)
x['person_relationships']=[
rel('TW-PERSON-000012','萧美琴（蕭美琴）','colleague','2024年共同组成选举搭档并于5月20日就任正副领导人，是有公开选举及就职记录的工作搭档，不推断私人亲疏。',urls['inaug'],'https://www.cna.com.tw/news/aipl/202401140007.aspx'),
rel('TW-PERSON-000002','蔡英文','superior','历史工作关系：2020年至2024年赖清德担任副领导人期间，蔡英文任领导人；2024年完成交接。枚举superior表示该历史任期的职务关系，并非现任上下级。','https://www.president.gov.tw/Page/694',urls['tsai']),
rel('TW-PERSON-000018','卓荣泰（卓榮泰）','subordinate','2024年5月20日赖清德签署任命卓荣泰为行政院院长，构成明确任命和施政合作关系；不扩张推断同党盟友或私人关系。',urls['appoint'],urls['cabinet'])]
x['family_members']=[dict(person_id=None,name='吴玫如（吳玫如）',relationship='spouse',industry_or_organization=None)]
x['collection_meta']['notes'] += '\n2026-11-13四数组专项补采：政策新增两岸、国防、产业民生、公共卫生与净零主题，旧无人机政策保留。空污修法为团队与立法机关共同成果，健康委员会议为已启动机制，不宣称目标已经实现。成就证据：2018空污修法 '+urls['air']+' 与 '+urls['aircna']+'；健康委员会 '+urls['health']+' 与 '+urls['healthcna']+'。家庭逐项映射：吴玫如=配偶，以中央社独立采访 '+urls['wife']+' 与联合报记者独立申报报道 '+urls['wife2']+' 交叉确认；仅采姓名及配偶关系，未提取报道中的财产、住址或金融信息，职业未复核留空。人物关系逐项证据已写各description：萧美琴=选举与执政搭档，蔡英文=历史正副任职，卓荣泰=明确任命关系，均有官方与独立中央社来源，不以同党推断盟友。未采未成年子女及非公众亲属敏感详情，未建立未知亲属ID。'
s=json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'));jsonschema.Draft7Validator(s).validate(x)
out=pathlib.Path('tmp/tw_supplement');out.mkdir(parents=True,exist_ok=True);(out/p.name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('before',before,'after',{k:len(x.get(k,[])) for k in before})

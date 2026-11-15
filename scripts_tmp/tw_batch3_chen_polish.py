"""Add independently read official English resume and minimal spouse corroboration."""
import pathlib,json
R=pathlib.Path(__file__).resolve().parents[1];p=R/'tmp/tw_batch3_enriched/TW-PERSON-000536.json';d=json.loads(p.read_text(encoding='utf-8'))
d['family_members']=[{'person_id':None,'name':'李昱芬（李昱芬）','relationship':'spouse','industry_or_organization':'仅记录TVBS原文与经济日报公开活动报道交叉确认的配偶姓名与关系。'}]
roles=[{'organization':'民主进步党（民主進步黨）','org_id':'TW-PARTY-012','position':'中央评议委员（历史任职）','start_date':'2020-09','end_date':'2022-07'},{'organization':'民主进步党（民主進步黨）','org_id':'TW-PARTY-012','position':'中央常务委员（历史任职）','start_date':'2022-07','end_date':'2024-05'}]
present={r['position'] for r in d['work_experience']}
d['work_experience'].extend(r for r in roles if r['position'] not in present)
for rel in d['person_relationships']:
 if rel.get('person_id')=='TW-PERSON-000018':rel['description']='2024年卓荣泰组阁时担任行政院发言人，其后由卓荣泰宣布转任交通部长；仅记录该行政任职关系。来源交通部官方中英文履历及Taipei Times 2024-08-30任命报道，不推断私人或派系联盟。'
added=[('交通部英文首长履历：英文名、学历与党务经历','https://www.motc.gov.tw/en/app/artwebsite?id=9&module=artwebsite&serno=null'),('Taipei Times：卓荣泰宣布陈世凯接任交通部长','https://www.taipeitimes.com/News/taiwan/archives/2024/08/30/2003823004'),('TVBS：陈世凯就任报道，正文确认配偶李昱芬','https://news.tvbs.com.tw/life/2605122'),('经济日报：公开新船命名活动确认陈世凯配偶姓名','https://money.udn.com/money/story/5612/9313920')]
q=d['collection_meta']['quotes']
for title,url in added:
 if not any(x['url']==url for x in q):q.append({'title':title,'url':url})
d['collection_meta']['notes']=d['collection_meta']['notes'].replace('家庭仅一轮检索未充分交叉不收录。','配偶李昱芬经TVBS与经济日报公开活动原文交叉确认，仅收姓名与配偶关系，不采财产或私人活动。').replace('早期精确任期与英文名仍维基辅助。','早期精确任期仍维基辅助；英文名、学历及两段党务年月由交通部英文官方页复核。')
d['collection_meta']['notes']+=' 台视相关页面两次读取超时，不计原文证据；社交多平台搜索有同名结果未核本人，保持空。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('Added spouse corroboration and two official historical party roles')

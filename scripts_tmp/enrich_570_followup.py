import json,pathlib
f=pathlib.Path('tmp/tw_batch7_enriched/TW-PERSON-000570.json');p=json.loads(f.read_text(encoding='utf-8'))
p['social_accounts']=[dict(platform=a,account_name='郭國文',url=b,source=c,source_note='本人实名Portaly聚合页 https://portaly.cc/gogowin.tainan 明确外链；平台本体读取失败，仅核原文外链，未作实时平台认证。',username=d,nickname=None,user_id=None) for a,b,c,d in [('facebook','https://www.facebook.com/gogowin2010',6,'gogowin2010'),('instagram','https://www.instagram.com/gogowin.tainan/',8,'gogowin.tainan'),('youtube','https://www.youtube.com/@gogowin2010',9,'gogowin2010'),('threads','https://www.threads.net/@gogowin.tainan',24,'gogowin.tainan')]]
p['major_achievements'].append(dict(date='2023-04-21',organization='立法院',achievement='主提证券交易法第四十三条之一等修正草案，经与行政院及其他党团、委员版本并案审议，于2023年4月21日三读通过，将大量持股申报公告门槛由10%降至5%，新制于2024年5月10日施行。仅记录本人参与集体修法，不称个人独力成果。'))
p['collection_meta']['quotes'] += [dict(title=t,url=u) for t,u in [('郭国文证券交易法提案原文','https://ppg.ly.gov.tw/ppg/SittingRelatedDocumentRMatter/download/agenda1/02/pdf/10/06/04/LCEWA01_100604_00071.pdf'),('证券交易法并案三读议案','https://ppg.ly.gov.tw/ppg/bills/203103141110000/details'),('证交所大量取得股份申报新制实施说明','https://www.twse.com.tw/market_insights/zh/detail/ff8080818d397607018e732df54403d6'),('CNA证交法三读','https://www.cna.com.tw/news/afe/202304210058.aspx')]]
n=p['collection_meta']['notes'];n=n.replace('已检索社群并读取本人Portaly外链页，但尚未核取各平台目标URL，故账号暂空。第二项已实施个人参与成果未充分核实，保留一项。','已补本人Portaly四个平台明确外链；平台本体不可读，未声称实时认证。第二项成果已核本人主提、并案三读及实施。');n+='政策日期2020-04-01为议案关系文书印发日，并非本人发言日；关系亦限文书载明共同提案。';p['collection_meta']['notes']=n
f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
import jsonschema
jsonschema.validate(p,json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')))
print('jsonschema passed')

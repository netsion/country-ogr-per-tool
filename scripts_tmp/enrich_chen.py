import json,pathlib,jsonschema
r=pathlib.Path('D:/ai-workspace/apec-osint-tool')
p=json.loads((r/'output/tw/2026-07-27/persons/TW-PERSON-000545.json').read_text(encoding='utf-8-sig'))
p['aliases']=['陈东豪'];p['gender']='male'
p['current_positions']=['宝岛联播网《宝岛强强滚》主持人','资深媒体人、政治评论员']
p['work_experience']=[dict(start_date=None,end_date=None,organization=o,org_id=i,position=t) for o,i,t in [('新新聞',None,'记者（毕业后首份工作，早期跑调查局新闻）'),('自由時報','TW-MEDIA-011','记者（历史任职）'),('蘋果日報',None,'记者（历史任职）'),('新新聞',None,'副社长（2017年报道确认，现已卸任）'),('新新聞',None,'社务顾问（2021年报道确认，未核实是否延续至采集日）'),('寶島聯播網',None,'《宝岛强强滚》主持人')]]
p['biography_summary']='陈东豪是台湾资深媒体工作者与政治评论员，职业经历横跨政治周刊、日报与广播。依其接受放言访问时的回忆，他毕业后的第一份工作是在《新新聞》担任记者，也是该刊第一批记者之一；镜报2026年节目报道进一步说明，他初入行时负责调查局新闻，透过同事引介建立采访联系。宝岛联播网官方主持人介绍另列他曾在《自由時報》及《蘋果日報》担任记者。2017年公视报道以《新新聞》副社长身份访问他，2021年放言则称其为社务顾问、前副社长。他在采访中讨论纸本媒体亏损与数位转型，强调新闻工作仍需要辨别来源和提供解释性信息。目前宝岛联播网官网列其主持《宝岛强强滚》，内容涵盖新闻识读、健康、美食与时事。2026年4月23日，他实际参与镜报《镜爆又怎样》第15集，回忆早年采访与媒体遭监控的历史。现有证据不足以确认其学历、家庭成员或具体公共政策主张，不据政论节目标题推定政治立场。'
p['major_achievements']=[{'date':'2017','achievement':'担任《新新聞》副社长，2017年4月9日以社方主管身份接受公视采访，说明与风传媒交易协商；此为职业管理节点，不视为个人创办或收购成果。','organization':'新新聞'},{'date':'2022','achievement':'担任宝岛联播网《宝岛强强滚》节目主持人，2022年官方节目说明及采集日官方网站主持人介绍均可核实其主持工作。','organization':'寶島聯播網'}]
p['collection_meta']={'collection_date':'2026-11-15','phase':'phase4_person_profile','data_sources':['official_website','news_search','web_search'],'quotes':[{'title':t,'url':u} for t,u in [('宝岛联播网：DJ介绍（陈东豪）','https://www.baodaoradio.com.tw/web/introduce/introduce.jsp'),('新新聞卅年 社方證實將被風傳媒收購','https://news.pts.org.tw/article/354987'),('不堪虧損！創刊34年新新聞停紙本轉數位','https://www.fountmedia.io/article/94943'),('鏡爆又怎樣EP.15：國家機器監控媒體秘辛','https://www.mirrordaily.news/story/57103'),('寶島強強滾：兄弟、政黨與選舉，陳東豪主持20221205','https://www.youtube.com/watch?v=z_kU8m7boKs')]],'notes':'已读宝岛联播网官方介绍、放言访问、公视报道及镜报节目报道独立原文。近期活动明确核至2026-04-23镜爆又怎样节目；官网采集时仍列宝岛强强滚主持。原2026-11-11镜新闻YouTube线索及震传媒43143正文无法读取，未据标题采观点。2022官方YouTube节目说明经搜索工具返回完整说明，直接open失败；仅用于核历史主持节点，不提炼政策。英文名未核，name_en保留空字符串；学历、出生、家庭、关系、获奖及独立出版未找到可靠资料。检索同名学历结果为棒球教练，已排除。检索Facebook及其他社交线索，仅见报道提及本人脸书，未核其准确URL，不把媒体账号当本人账号。未发现足以填写的明确具体公共政策主张，政治内幕预测与对个人批评不作政策。历史任期起讫未载留空；自由时报ID已核正式组织画像。未新增QID。'}
out=r/'tmp/tw_batch5_enriched/TW-PERSON-000545.json';out.parent.mkdir(exist_ok=True)
jsonschema.validate(p,json.loads((r/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8-sig')))
out.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(out)

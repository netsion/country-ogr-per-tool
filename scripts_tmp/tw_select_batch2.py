import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
P=R/'output/tw/2026-07-27/persons'
rows=[
('吴钊燮','吳釗燮','Joseph Wu','国家安全会议秘书长','国安政策统筹、对外安全协调','https://www.president.gov.tw/nsc/management','https://www.president.gov.tw/News/39900'),
('郑丽文','鄭麗文','Cheng Li-wun','中国国民党主席','主要在野党路线与两岸政策、跨党合作','https://www1.kmt.org.tw/people.aspx?mid=21&pid=2500','https://www.cna.com.tw/news/aipl/202610090077.aspx'),
('黄国昌','黃國昌','Huang Kuo-chang','台湾民众党主席','第三党政策、在野合作与地方选举','https://www.tpp.org.tw/member','https://www.cna.com.tw/news/aipl/202610100100.aspx'),
('潘孟安','潘孟安','Pan Men-an','总统府秘书长','府院协调、核心行政网络','https://www.president.gov.tw/Page/107','https://www.president.gov.tw/News/39900'),
('邱垂正','邱垂正','Chiu Chui-cheng','大陆委员会主任委员','两岸交流、法规与风险政策','https://www.mac.gov.tw/cp.aspx?n=D7B7F1B4196DD582','https://www.taipeitimes.com/News/taiwan/archives/2026/07/05/2003860257'),
('蔡明彦','蔡明彥','Tsai Ming-yen','国家安全局局长','情报体系行政领导与国际安全协调','https://www.cy.gov.tw/News_Content.aspx?n=709&s=26569&sms=8912','https://www.cna.com.tw/news/aipl/202404250165.aspx'),
('刘世芳','劉世芳','Liu Shyh-fang','内政部部长','警政、民防韧性、地方及移民治理','https://www.moi.gov.tw/cp.aspx?n=27','https://www.taipeitimes.com/News/front/archives/2026/01/07/2003850210'),
('龚明鑫','龔明鑫','Kung Ming-hsin','经济部部长','产业、能源与对外经贸决策','https://www.cbc.gov.tw/tw/cp-328-184064-ef820-1.html','https://www.cna.com.tw/news/afe/202509010095.aspx'),
('管碧玲','管碧玲','Kuan Bi-ling','海洋委员会主任委员','海洋政策、海巡体系和海上执法治理','https://www.oac.gov.tw/ch/home.jsp?id=435&parentpath=0%2C425%2C434','https://www.president.gov.tw/News/39900'),
('卢秀燕','盧秀燕','Lu Shiow-yen','台中市市长','重要地方行政首长及国民党地方政治网络','https://www.taichung.gov.tw/1173576/post','https://zh.wikipedia.org/wiki/盧秀燕'),
('侯友宜','侯友宜','Hou Yu-ih','新北市市长','人口大市治理与国民党地方行政网络','https://www.ntpc.gov.tw/ch/home.jsp?id=107&parentpath=0%2C6%2C106','https://zh.wikipedia.org/wiki/侯友宜'),
('陈其迈','陳其邁','Chen Chi-mai','高雄市市长','南部产业、地方治理与执政党行政网络','https://www.kcg.gov.tw/cp.aspx?Create=1&n=59C096A5BBC7AFB1','https://zh.wikipedia.org/wiki/陳其邁'),
('傅崐萁','傅崐萁','Fu Kun-chi','第11届立法委员','国民党议会协商与关键议案动员；党团头衔须采集时再核实','https://www.ly.gov.tw/Pages/List.aspx?nodeid=46824','https://www.ly.gov.tw/Pages/Detail.aspx?nodeid=54305&pid=264177'),
('柯建铭','柯建銘','Ker Chien-ming','第11届立法委员','资深议会协商及执政党国会关系；不把历史总召直接写现职','https://www.ly.gov.tw/Pages/List.aspx?nodeid=46793','https://www.cna.com.tw/news/aipl/202601150131.aspx'),
('罗智强','羅智強','Lo Chih-chiang','第11届立法委员','在野立法与政治传播、司法法制政策参与','https://www.ly.gov.tw/Pages/List.aspx?nodeid=109','https://ccw.org.tw/assess/48/legislator/465'),
]
existing={}
for f in P.glob('TW-*.json'):
 x=json.loads(f.read_text(encoding='utf-8'))
 for k in ['name','name_zh']:
  if x.get(k):existing[x[k]]=x
out=[]
for rank,(zh,local,en,pos,reason,official,second) in enumerate(rows,1):
 old=existing.get(zh) or existing.get(local)
 out.append(dict(rank=rank,person_id=old['person_id'] if old else None,name=local,name_zh=zh,name_en=en,wikidata_qid=old.get('wikidata_qid') if old else None,has_profile=bool(old),current_position=pos,selection_reason=reason,sources=[dict(type='official',url=official),dict(type='corroboration_candidate',url=second)],verification_note='候选阶段现职依据官方在线页面；英文名/旧QID进入深采仍需交叉确认。第二来源为后续原文复核线索，不将搜索摘要当完整核验。'))
data=dict(collection_date='2026-11-13',scope='台湾地区下一批15位公开政治人物',persons=out,notes=['与首批10人无重复，9位已有档案、6位需主会话统一分配ID。','选择依据公开职责和决策影响，非政治立场判断。','不得提前把2026年底换届后的职务当现任；黄国昌不沿用旧立委职位；柯建铭不沿用历史党团总召。','蔡明彦缺可访问国安局现职页，以监察院官方资料和中央社交叉，2026年监察院月刊巡察记录另确认局长称谓，深采再核最新任免。','潘孟安、吴钊燮、管碧玲第二链接与第一链接同属官方发布体系，并非独立交叉确认，深采应补独立报道。','陆委会及民众党页面open遇403，搜索索引有当前头衔，需深采补可读取原文；不宣称已完成全部正文事实核验。'])
(R/'tmp/tw_batch2_selection.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 台湾地区下一批15人候选（2026-11-13）','','本文件仅为下一批采集队列，不是人物画像或全部现职完成交叉验证的声明。待首批10人专项补采完成后逐人执行。','','|顺序|姓名|现有ID|公开职位|选择理由|','|---|---|---|---|---|']
for x in out:lines.append(f"|{x['rank']}|{x['name_zh']}|{x['person_id'] or '待统一注册'}|{x['current_position']}|{x['selection_reason']}|")
lines+=['','## 证据与边界','']+['- '+n for n in data['notes']]
for x in out:lines+=['',f"**{x['name']}**"]+['- ['+s['type']+']('+s['url']+')' for s in x['sources']]
(R/'docs/tw_batch2_selection.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(len(out),sum(x['has_profile'] for x in out))

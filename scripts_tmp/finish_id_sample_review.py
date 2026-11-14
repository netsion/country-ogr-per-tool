"""Publish a manually adjudicated 200-row ID review. Does not alter dataset files."""
import csv,json,pathlib,hashlib
from collections import Counter,defaultdict
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'output/_id_audit'
contexts=json.loads((OUT/'sample_200_context.json').read_text(encoding='utf-8'))
KEEP={7,9,10,27,37,48,57,70,77,83,86,105,106,108,114,118,121,123,124,131,135,140,161,168,174,178,181,187,191,193,194,195}
CLEAR={1,2,3,4,5,6,8,11,13,14,15,18,20,21,22,23,24,26,28,29,30,31,32,33,35,36,39,40,41,42,43,45,46,49,53,54,55,58,59,60,61,62,63,65,68,72,73,74,75,76,78,79,80,81,82,84,85,87,90,93,94,95,96,99,102,104,109,112,115,119,120,125,126,130,132,133,134,138,141,142,146,147,150,153,155,156,157,158,160,165,169,170,171,172,179,182,183,184,185,186,188,192,199,200}
HOLD_REASONS={
12:'总统办公厅与总统职务画像不是同一实体，需确定是否允许映射元首职务。',
16:'部长个人办公室与Attorney-General部门的雇佣组织粒度不同，不能作为完全同名。',
17:'VinFast与Vingroup是不同公司层级，不能当作别名直接合并。',
19:'旧部委名称与当前工业贸易部可能有历史延续，需按任期核实改组范围。',
25:'司法机构执行委员会不等于最高法院；目标别名含整个司法系统也不足以证明同一实体。',
34:'事务总长官房是会计检查院内部单位，需先确定部门是否允许指向上级。',
38:'空军与整个国民军存在层级差异，保留原引用待统一粒度规则。',
44:'总统办公厅与总统职务画像粒度不同，不能仅凭总统字样视为相同。',
47:'第18营与马来西亚陆军属于部队层级差异，低相似不构成无关错链。',
50:'步兵旅与陆军是具体部队与上级军种的粒度差异。',
51:'注册姓名对应但status=trimmed且无画像，先处理停用注册状态，不当作无关实体。',
52:'印度尼西亚三井物产与三井物产总部可能是子公司或分支，需要明确法律实体。',
56:'CitiMortgage与Citigroup不是同一法律实体，需先决定是否接受集团聚合。',
64:'法学院与大学是院系层级差异，不能简单置空。',
66:'枢密院办公室与加拿大政府是专门机关与整个政府的粒度差异。',
67:'注册姓名相符但status=trimmed、无画像，需恢复或移除注册状态后决策。',
69:'金融监督院的局及团队与整院存在部门层级差异。',
71:'Shorcan与TMX集团存在公司层级差异，0.14低相似不证明完全无关。',
88:'官方明确Minera San Cristobal为San Cristobal Mining的子公司，不能按名称近似当同一公司。',
89:'Telecel官方明确撤回收购Areeba，引用所称原MTN/Telecel关系存在事实冲突，先修名称和历史。',
91:'经济政策局与财政部是内部局与上级部门的粒度差异。',
92:'中文写造船企业，英文及目标写化工集团，引用自身中外文矛盾，不能以英文命中判保留。',
98:'纳米自旋实验设施与东北大学是下属设施与大学的粒度差异。',
100:'注册是Sigma Alimentos，无画像；引用是Sigma Foods，官网表明后者由ALFA改名，须厘清控股与经营实体。',
101:'注册姓名相符但status=trimmed且无画像，需先解决停用身份。',
103:'BMO中国公司与蒙特利尔银行母体是不同公司层级。',
107:'The Athletic与纽约时报是产品/企业集团层级差异，非名称变体。',
110:'西部野战司令部与整个陆军是指挥层级差异。',
111:'政党执行委员会与政党本体是内部机构与上级组织的粒度差异。',
113:'财政部下属司与财政部整体的粒度不同。',
116:'官方确认2022年重组更名并分出公共建设职能，须按任期和组织沿革处理，非普通文字差异。',
117:'农协中央会与农协银行可能涉及不同法人及组织层级，不能把中央会部门直接认作银行。',
122:'注册姓名相符但已trimmed且无画像，不能仅据无文件断言身份错误。',
127:'2016—2022旧部委与当前部委职责经过变化，须核任期沿革，不能按高相似自动保留。',
128:'全国执行委员会与国家行动党本体有内部机构粒度差异。',
129:'矿建分公司与吉尔吉斯黄金公司有分支层级差异。',
136:'National Indemnity与伯克希尔集团是不同公司层级。',
137:'缓刑服务处、公共安全司与内务部存在内部层级差异。',
139:'具体师/军团与越南人民军整体有部队层级差异。',
143:'卡迪米注册姓名对应但status=trimmed且无画像，需先清理注册状态。',
144:'引用整个宗教事务部却指向其宗教和谐中心，是反向层级错位，需查实际雇主，不能作为完全匹配。',
145:'通讯技术中心与越南通讯社是内部中心与上级机构层级差异。',
148:'参议院民主党党团与整个国会层级不同，不能当同一实体。',
149:'Sagip Kapamilya项目与ABS-CBN基金会是项目与机构的粒度差异。',
151:'BOI保险经纪公司与工业银行是经营实体和集团层级差异。',
152:'总统候选人竞选委员会与共同民主党本体不是同一组织粒度。',
154:'总统安全营与几内亚武装力量是具体部队与上级军队层级差异。',
159:'NHK编成局与NHK整院存在内部部门层级差异。',
162:'引用含阿卜杜拉二世本人，目标是国王职务画像，须区分个人与职务机构。',
163:'项目协调小组与农业部是项目/部门与上级部委的粒度差异。',
164:'健康事业部与Al-Futtaim集团有事业部或子公司层级差异。',
166:'边境事务国务秘书处与内阁整体不是同一实体粒度。',
167:'Alrosa-Nyurba与Alrosa母体是不同经营实体，需按法人粒度处理。',
173:'安达拉斯大学法学院与大学是院系层级差异。',
175:'星岛新闻集团官网列星岛日报为旗下报纸，集团与报纸不能直接当同一实体。',
176:'2021—2022能源部长与石油能源部改革前后口径可能不同，且同ID注册表另指基金会，需核组织沿革。',
177:'亚洲新闻中心与雅典耀大学是内部机构与大学层级差异。',
180:'样本已过时：Step1b把本条由PE-SOE-006改为NI-ACAD-004；秘鲁与尼加拉瓜有同名UNI，须按任职国家复核，禁止再靠同名自动认定。',
189:'中文写外交部，英文细化新闻司，需统一部门粒度；实际画像确为外交部，不能被错误registry标签国防部误导。',
190:'曼谷海军基地与皇家海军是基地与军种整体的粒度差异。',
196:'信息技术与测量中心与越南电视台是内部单位与机构层级差异。',
197:'未来资产资产管理公司与金融集团是不同经营实体/母子层级。',
198:'陆军总司令部与整个皇家陆军是指挥机构与军种整体层级差异。',
}
REPLACE={97:'US-GOV-007'}
assert not (KEEP&CLEAR or KEEP&set(HOLD_REASONS) or CLEAR&set(HOLD_REASONS))
assert KEEP|CLEAR|set(HOLD_REASONS)|set(REPLACE)==set(range(1,201))
KEEP_NOTES={
7:'同一众议院，LXIV仅为立法届次限定，不是另一机构。',
10:'实际关系姓名存在name字段且为刘子平，与目标一致；审计漏读name产生空名称误报。',
37:'当前画像明确为吉尔吉斯财政部；registry中的尼日尔旧标签有误，不据此改动正确引用。',
70:'实际name字段明确为Narongrit Khamphira，与目标一致，属于读取字段错误。',
77:'银行官方确认Saudi British Bank更名Saudi Awwal Bank，属于有证据的沿革名称。',
106:'无画像但活跃auto_registered条目明确ACWA Power，身份匹配，缺画像不等于错链。',
114:'画像明确为吉尔吉斯议会；registry混入The Confessions Tour旧标签，不影响该引用的实体一致性。',
174:'无画像但活跃auto_registered条目明确越南信息传媒部MIC；本轮只确认身份，不证明当前仍存续或任职仍在任。',
178:'当前画像明确为吉尔吉斯紧急情况部；registry俄罗斯旧标签错误，不能按registry反改引用。',
181:'Mawhiba为该沙特天才创造力基金会通行简称，目标画像名称变体支持。',
187:'中文译名、尊称及拼写差异，目标是同一苏丹Ibrahim Ismail。',
193:'Organizacion de las Naciones Unidas即联合国，目标与registry一致；BOL总部等元数据另待核，不删除正确引用。',
}
SPECIAL_CLEAR={
3:'Enel X能源服务公司与Entel电信是不同公司，0.90高相似是拼写近似误判。',
4:'组织引用填入PERSON类ID，且注册身份为人物，不符合实体类型。',
15:'注册同ID是Simon Moutter/Bill Moran，而引用是Bill English，既有注册冲突也不是同一人。',
18:'SK Networks与SK hynix是不同公司，共享SK品牌不构成同一法人。',
41:'引用Silvano Garay，目标是Irma Garay（并为引用方本人），同姓及0.79不能覆盖不同人和自指问题。',
62:'无画像但registry为瑞穗信托，引用为SMBC信托；不能因都叫信托银行而混同。',
65:'私人执业是任职状态，不是商界报纸，保留履历文本，仅解除错误组织ID。',
68:'registry登记拉菲克哈里里大学医院，引用是政府部长会议，姓名词元相同但机构不同。',
96:'中文大学、英文检察院和职位叙述互相矛盾，当前军队画像无论按哪种名称都不匹配；不能直接改到大学候选。',
109:'组织引用使用人物ID，实际为Jaime Muguiro，不是塔帕丘拉市政府。',
112:'MY-PERSON-UNKNOWN-003为无注册无画像占位ID，保留人物姓名和关系文字待后续解析。',
120:'registry为IHS Kuwait，引用为KEO，均属咨询领域也不是同一公司。',
125:'组织麦当劳指向人物Robert A. McDonald，词元命中导致跨类型误链。',
141:'MY-PERSON-REL-001为无注册无画像自造关系ID，保留姓名和关系事实待解析。',
146:'引用阿尔及利亚ARPT却指向选举机构；检索候选GN-GOV-030是几内亚同名监管局，也不可替换。',
147:'人物引用指向墨西哥国立自治大学，实体类型不符。',
153:'EXT-PERSON-003为无画像无注册外部占位ID，姓名关系保留，不保留伪链接。',
165:'美国海军陆战队与美国海军是不同军种实体；同属海军部不能把Marine Corps改指Navy。',
199:'无画像的registry登记日本驻泰国使馆，引用是驻菲律宾使馆，国家不同。',
200:'MATE与APB Sumate不是同一政党，源条目备注也明确指出此ID错误却仍写入，不能按缩写近似保留。',
}
WEB={
3:['https://www.enelx.com/cl/es/privacidad'],
77:['https://www.sab.com/en/about-us/newsroom/news-year-2023/following-the-successful-merger-and-integration-of-sabb-and-alawwal-bank/'],
88:['https://www.minerasancristobal.com/v3/en/'],
89:['https://telecelgroup.com/telecel-group-issues-clarification-regarding-the-mtn-guinea-acquisition-deal/'],
100:['https://www.sigmafoods.com/en/our-history/'],
116:['https://www.dsscu.gov.mo/zh/aboutus/history','https://bo.dsaj.gov.mo/isapi/go.asp?d=rega-14-2022cn'],
175:['https://www.singtaonewscorp.com/en/business.html'],
180:['https://andina.pe/agencia/noticia-elecciones-2021-conoce-perfil-rafael-lopez-aliaga-candidato-renovacion-popular-831866.aspx','https://www.gob.pe/uni','https://posgrado.uni.edu.ni/universidad/'],
193:['https://www.un.org/es/'],
}
review=[];decisions=[]
for r in contexts:
 row=dict(r['row']);n=int(row['序号']);cat=row['类型'];key='org_id' if cat in ['work_org','related_org'] else 'person_id'
 exact=[s for s in r['sources'] if s['entry'].get(key)==row['当前ID']]
 selected=exact if exact else r['sources']
 observed=list(dict.fromkeys(str(s['entry'].get(key)) for s in selected))
 observed_names=list(dict.fromkeys(str(s['entry'].get('person_name') or s['entry'].get('org_name') or s['entry'].get('organization') or s['entry'].get('name') or '') for s in selected))
 if n in KEEP:
  action='保留';vote='0';reason=KEEP_NOTES.get(n,'引用与当前画像的本国语言、英文名或规范中文译名对应，为名称格式或翻译变体。')
 elif n in CLEAR:
  action='建议置空';vote='1';reason=SPECIAL_CLEAR.get(n,f"引用实体「{row['引用名称']}」与目标「{row['当前ID实际指向']}」明显不同；现有名称和来源上下文不支持同一身份。")
 elif n in REPLACE:
  action='建议改链';vote='';reason='引用明确为美国商务部，已存在主名称一致的US-GOV-007画像；建议逐条改向该画像，优于先置空。'
 else:action='暂缓';vote='';reason=HOLD_REASONS[n]
 category=('停用注册' if n in [51,67,101,122,143] else '名称或事实冲突' if n in [89,92,100,176] else '快照变更及跨国同名' if n==180 else '历史改组' if n in [19,116,127] else '上下级或实体粒度') if action=='暂缓' else ('有效注册无画像' if n in [106,174] else '审计姓名字段误读' if n in [10,70] else '实体一致') if action=='保留' else '明确错链' if action=='建议置空' else '已知正确画像'
 locations=[{'file':s['file'],'array':s['array'],'index':s['index'],'field':key,'expected_id':s['entry'].get(key),'expected_reference':s['entry'].get('organization') or s['entry'].get('person_name') or s['entry'].get('org_name') or s['entry'].get('name'),'owner_id':s['owner_id']} for s in selected]
 local=list(dict.fromkeys([s['file'] for s in selected]+([r['target']['file']] if r['target'] else [])+[e['file'] for e in r['registry']]))
 if n==180:local+=['output/_id_audit/step1b_undo.json','output/ni/2026-10-28/orgs/NI-ACAD-004.json']
 row.update({'助手复核结论':action,'问题分类':category,'助手建议置空(非执行授权)':vote,'复核依据':reason,'核实时实际ID':' | '.join(observed),'实际引用名称':' | '.join(observed_names),'建议正确ID':REPLACE.get(n,''),'原始引用位置':' | '.join(f"{s['file']}#{s['array']}[{s['index']}].{key}" for s in selected),'本地证据':' | '.join(local),'外部证据':' | '.join(WEB.get(n,[])),'复核状态':'已复核，仅形成建议，未执行'})
 review.append(row)
 decisions.append({'sample_number':n,'action':action,'category':category,'reason':reason,'proposed_id':REPLACE.get(n),'locations':locations,'local_evidence':local,'web_evidence':WEB.get(n,[]),'review_only':True})
with (OUT/'null_review_200_reviewed.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(review[0]));writer.writeheader();writer.writerows(review)
(OUT/'sample_200_review_decisions.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
counts=Counter(r['助手复核结论'] for r in review);strata=defaultdict(Counter)
for r in review:strata[r['建议']][r['助手复核结论']]+=1
manifest=json.loads((OUT/'sample_200_read_manifest.json').read_text(encoding='utf-8'));changed=[p for p,h in manifest.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
assert not changed,f'Dataset files changed during read-only review: {changed}'
summary={'rows_reviewed':len(review),'actions':dict(counts),'by_original_suggestion':{k:dict(v) for k,v in strata.items()},'monitored_dataset_files':len(manifest),'changed_dataset_files':changed,'review_only':True,'not_a_population_error_rate':True}
(OUT/'sample_200_review_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# ID引用200条样本复核','', '本轮只审查200条样本与当前本地画像、注册表和来源上下文，未修改任何人物/组织画像、引用ID、注册表、名称索引或头像。原始CSV保留，复核另存。','',
 '| 复核结论 | 样本条数 | 建议 |','|---|---:|---|',
 f"| 建议置空 | {counts['建议置空']} | 不同实体或无效占位ID。只解除ID，不删除姓名、履历和关系文字。 |",
 f"| 保留 | {counts['保留']} | 同一实体的名称变体、正确的name字段关系，或有相符活跃注册的缺画像身份。 |",
 f"| 暂缓 | {counts['暂缓']} | 上下级/母子公司、历史改组、停用注册、引用自身冲突或已变更快照。 |",
 f"| 建议改链 | {counts['建议改链']} | 第97条美国商务部可明确指向US-GOV-007，建议不走置空。 |",'',
 '## 原算法分组与复核结果','', '| 原建议 | 置空 | 保留 | 暂缓 | 改链 |','|---|---:|---:|---:|---:|']
for label,c in strata.items():lines.append(f"| {label} | {c['建议置空']} | {c['保留']} | {c['暂缓']} | {c['建议改链']} |")
lines+=['','样本按原算法分层抽取，并非全库随机样本。上述计数不可乘回全库当真实错误率；没有对原6974条低相似或7031条中相似作执行授权或全量结论。', '',
 '## 关键纠偏','',
 '- 第3条：Enel X与Entel不同公司，0.90不能判保留。第41条：Silvano Garay与Irma Garay不同人，且当前目标就是引用方本人。',
 '- 第10、70条：真实姓名在关系name字段中，与目标人物吻合。原审计只读person_name而产生空名称误报，应保留ID，字段规范化另处理。',
 '- 第193条：西语联合国名称与联合国画像一致，0.39低相似不是错链。',
 '- 第106、174条：存在相符的活跃注册身份但没有画像。区别缺画像与ID错误，不应全置空。第51、67、101、122、143条则是身份相符但trimmed，应先解决停用状态。',
 '- 第62、68、120、199条：虽然没有画像，却能从注册表看出分别错指其他银行、医院、公司和另一国使馆，仍是明确错链。',
 '- 第92、96条：引用自身中文/英文/职位混杂，不能用任一片段精确匹配直接补新ID。第96条当前军队ID建议解除，但正确机构须先核原始事实。',
 '- 第37、114、178、189条：实际画像与registry旧标签不一致。以当前画像主体为依据，不能用错误注册标签覆盖正确机构。',
 '- 第89条：Telecel官方称收购Areeba未完成并撤回，不能把Telecel/Areeba轻率当更名别称。',
 '- 第180条：Step1b日志确认PE-SOE-006已改为NI-ACAD-004。秘鲁、尼加拉瓜确有同名UNI，人物是秘鲁政治人物；该新补链存在明显跨国同名风险，先暂缓并核任职学校国家。本轮没有把它算进可直接执行置空条目，也没有恢复原本同样错误的矿业公司ID。', '',
 '## 后续建议','',
 '先讨论这104条置空建议和1条改链建议是否执行，再单独决定上下级/母子公司是否允许聚合指向上级画像。63条暂缓不自动处理。执行时必须重新读取并核对文件、数组索引、当前ID和引用名称，输入已变更则跳过复核，不能直接照旧CSV批量写。', '',
 f'已监测{len(manifest)}份相关画像或注册表文件的SHA-256，复核前后均未改变。头像目录未执行写入、重命名、移动或上传操作。此项证明本轮相关数据未改动，不是全库头像有效性重审。', '',
 '复核CSV中的助手建议是专业复核意见，不冒充用户批准。原确认置空列保持原样。机器可读建议均标review_only=true。', '',
 '## 重点外部证据','']
for n,urls in WEB.items():
 for u in urls:lines.append(f'- 第{n}条：[来源原文]({u})')
lines+=['','## 逐条结论','', '| 序号 | 结论 | 分类 | 依据 |','|---:|---|---|---|']
for r in review:lines.append('| '+r['序号']+' | '+r['助手复核结论']+' | '+r['问题分类']+' | '+r['复核依据'].replace('|','/')+' |')
(ROOT/'docs/id-reference-sample-review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=True))

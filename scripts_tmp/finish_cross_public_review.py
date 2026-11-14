"""Emit review opinions only. Never write profiles, registries or original CSVs."""
import csv, hashlib, json, pathlib, re, sys
from collections import Counter
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'output/_id_audit'
sys.stdout.reconfigure(encoding='utf-8')
D=json.loads((OUT/'cross_public_491_context.json').read_text(encoding='utf-8'))
assert len(D)==491
originals=['step1b_cross_public_review.csv','step1b_cross_public_priority.csv']
before={n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in originals}
decisions={}
def put(ids,decision,reason,issue,urls=()):
 for i in ids:
  decisions[i]={'conclusion':decision,'reason':reason,'issue':issue,'external_sources':list(urls)}

# Explicitly reviewed blocks: source entry context and actual target basic_info,
# rather than registry display labels or cross-country status alone.
for lo,hi in [(1,54),(55,111),(112,158),(159,238),(239,299),(300,341),(342,400),(401,448),(449,491)]:
 for i in range(lo,hi+1):
  x=D[i-1];e=x['entry'];b=x['new_target']['profile']['basic_info']
  label=x['current_reference'];target=b.get('name_en') or b.get('name_original') or b.get('name_zh')
  put([i],'保留',f'引用文字“{label}”与目标画像主体“{target}”相符；已结合本行任职/合作/股权说明检查，没有发现指向另一同名实体的冲突。仅复核实体指向，不等于背书本行所有履历、日期及比例。','本地上下文与画像身份一致')

unicef='https://www.unicef.org/kyrgyzstan/contact-us'
rferl='https://about.rferl.org/article/central-asia-in-focus-attacks-on-rfe-rls-kyrgyz-service/'
put([1],'置空','原画像是秘鲁矿业资产公司 AMSAC；新画像是尼加拉瓜 UNI。人物条目为国立工程大学讲师，现有生平及秘鲁官方候选人介绍指向秘鲁教育经历，新旧均不能作为已确认的正确目标；不得回退到矿业公司。','同名大学／原新均错',['https://andina.pe/agencia/noticia-elecciones-2021-conoce-perfil-rafael-lopez-aliaga-candidato-renovacion-popular-831866.aspx','https://www.gob.pe/uni'])
put([5,6,7,8,11,12,13,14,15,16,17,18,19],'回退','新画像明确为 UNICEF 吉尔吉斯斯坦国别办事处；本行是其他国家项目、纽约总部或其他区域任职。原 ID 无画像，但注册表仅登记 UNICEF 且类型匹配，可建议恢复原注册引用；这不会产生可点击的已建画像。后续仍需总部/国别实体归一。','总部与国别办事处混淆',[unicef])
put([9],'暂缓','新画像为 UNICEF 吉尔吉斯斯坦办事处，不能支撑柬埔寨教育项目；原 KH-INTL-006 同时登记 UNICEF 与 UNAIDS，存在 ID 碰撞，不能直接回退。需先拆分注册身份或确认独立 UNICEF ID。','新链错误且原注册ID碰撞',[unicef])
put([10],'置空','新目标为吉尔吉斯斯坦 UNICEF 办事处，与跨27国合作的机构表述不符；原 KR-INTL-001 注册主体为 APEC，亦非 UNICEF。','新旧均为其他实体',[unicef])
put([20,21,22],'暂缓','新目标为吉尔吉斯斯坦 UNICEF 办事处，本行是全球合作或纽约儿童保护部门。原 TH-IGO-001 登记 UNICEF 但使用非标准 IGO 类别，未建画像；需先确定合规总部/部门ID，不能当成已验证可回退目标。','国别办事处误用／原ID格式待修',[unicef])
put([23],'置空','HOY 的财务经理经历被连到尼日利亚 This Day；原画像为玻利维亚 El Mundo，也不是 HOY。中文“今日报”不能跨报社等同。','通用译名误配')
put([25,26],'置空','引用分别为西班牙 El País、La Nación，目标却是布基纳法索 Le Pays；原目标分别为 Falabella 零售集团、康塞普西翁大学，也不正确。','通用译名误配')
put([28],'回退','源条目明确老挝 Star Telecom／Unitel 电信运营商，新目标为玻利维亚 Unitel 电视台。原 LA-CORP-007 为同名同业唯一注册条目，无画像，可建议恢复注册引用。','品牌同名跨行业误配')
put([32],'回退','源阿拉伯文 لوريون لوجور 对应黎巴嫩 L’Orient-Le Jour，原 LB-MEDIA-015 有该报画像；新目标是玻利维亚 El Diario。旧链接实体正确。条目把1950年代经历归在1971年合并后的报纸名下，属于另一个沿革/日期核实问题。','通用中文名误配／沿革另核')
put([33],'回退','源说明明确为拉希德·尼尼2012年在摩洛哥创办的 Al Akhbar；新画像明确黎巴嫩同名报。原 MA-MEDIA-029 为该摩洛哥报唯一注册条目，无画像，可恢复原注册引用。','跨国同名报纸')
put([34,36],'置空','引用分别是墨西哥 Multimedios Canal 6 与索诺拉 Telemax；新画像为尼加拉瓜 Canal 6。原 MX-MEDIA-006 的实际画像是 Milenio 报纸，且注册表夹有 Canal 6 影子条目，不能回退到同集团报纸。','同频道编号／原ID碰撞')
put([35],'暂缓','新画像为越南24h新闻网站，源为墨西哥 Diario 24 Horas；原 MX-GOV-375 虽登记同名报纸，却误分 GOV 类别。需分配媒体合规ID，不能认定新链或旧ID已合格。','新链错误／原注册类型错误')
put([38],'回退','本行任职是阿曼 Public Authority for Radio and Television 2011—2020年主席；新目标为巴林广播电视机构。原 OM-GOV-041 是匹配的公共机构唯一注册条目，无画像，可恢复注册引用。','跨国公共机构通名误配')
put([43],'回退','本行明确 RFE/RL 总部为奥佐迪的上级；新画像仅为吉尔吉斯语部 Azattyk。原 TJ-MEDIA-011 唯一登记 RFE/RL 总机构，无画像，可恢复注册引用，后续归一总部ID。','总机构与语言服务部混淆',[rferl])
put([44,45,46,47],'置空','源为 RFE/RL 总机构、集团总裁或中亚区域管理层；新画像仅吉尔吉斯语部，原 TM-MEDIA-006 则是土库曼语部，两者都不能代表总机构。','新旧均是下属语言服务部',[rferl])
put([49],'回退','源为荷兰/比利时 Tango 无人加油站品牌，新画像为坦桑尼亚非政府组织协会 TANGO。原 KW-CORP-019 是同名同业唯一注册项，无画像，可恢复注册引用；ID前缀是登记分区，不代表品牌所在国。','缩写跨行业误配')
put([51],'置空','源为 Endesa／Enersis 在西班牙、意大利及智利的电力任职，新画像为玻利维亚 ENDE；原 CL-PARTY-031 登记西班牙 Podemos 政党，也不正确。','近名电力公司／原新均错')
put([52,53],'暂缓','Carlos Torres Vila 的 Endesa 任职不属于玻利维亚 ENDE。原 MX-GOV-270 登记 Endesa 但误分 GOV、无画像；需确认合规 Endesa 实体ID，不直接回退错误类型ID。','新链错误／原注册类型错误')
put([69],'暂缓','源为日本三角育生在東海大学信息通信学部任职，校方报道可证；新画像为台湾 Tunghai University。原 JP-GOV-496 虽同名，却误分类 GOV、无画像。需日本 Tokai University 合规ID。','日本与台湾同名高校／原类型错误',['https://www.u-tokai.ac.jp/news-campus/192891/'])
put([82],'置空','本行说明明确利比亚塔尔胡纳宰图纳大学法学院；新画像是突尼斯 Ez-Zitouna University，原 LY-ACAD-023 注册名称也明确“突尼斯”。不能仅因原ID前缀LY而回退。','同名高校／原注册语义仍是突尼斯',['https://azu.edu.ly/ar'])
put([84,95],'保留','MIT Corporation 是该校治理机构，条目职位已明确董事/校董，所连为 MIT 学校本体；作为校董任职的组织引用可以保留，无需误判为另一家同名公司。','学校治理机构映射到学校本体')
put([114,171],'暂缓','经历起始于 JPMorgan Chase 合并前（分别1998、1981年）；新画像为合并后集团。需区分历史 J.P. Morgan 主体与集团沿革映射，不能凭现代品牌直接确认历史法律实体一致。','历史前身与现集团层级待定')
put([122],'暂缓','源把1982年始于马里的 BOA 泛非子集团与其2010年后控股方 BMCE／Bank of Africa 摩洛哥混合表述；目标画像为后者。需明确引用的是直接 BOA Group 母公司还是最终控股方，再判定ID。','直接母公司与最终控股方混合')
put([148],'暂缓','源合并写韩国渣打金融控股、SC第一银行及新加坡派驻；目标画像同列 Standard Chartered PLC/Bank 为别名并混用香港总部字段。不能据集团品牌确认该段雇主的法律实体。','多实体任职合并／目标画像层级混合')
put([159,161,162,163],'回退','源为与BCM合并前的摩洛哥 Wafabank；新目标为利比亚 Wafa Bank，且其注册状态已标 excluded、未验证。原 MA-FIN-022 为匹配的历史银行唯一注册项，无画像，可恢复注册引用。','跨国近名银行／目标已排除')
put([168],'暂缓','源写伦敦 Standard Chartered Bank 雇主，目标将 PLC 与 Bank 混列别名且国别为香港；应先拆清集团/银行法人，不能仅以渣打中文品牌确认。','银行与控股公司层级待定')
put([174],'暂缓','单个 related_entities 条目同时写 NZX / ASX，ID仅指ASX；需拆为两条并分别保留各自上市历史，不能用一个目标覆盖两家交易所。','复合引用需拆分')
put([178,181,182],'回退','源明确阿曼 Ahli Bank（阿语 الأهلي）；新画像是利比亚 Aman Bank（الأمان），不是同一银行。原 OM-FIN-018 为唯一匹配注册项，无画像，可恢复注册引用。','近名银行误配',['https://cbo.gov.om/Pages/LicensedBanks.aspx'])
put([179,180],'回退','源明确约旦安曼 Arab Bank plc；新目标是巴林 Bank ABC／Arab Banking Corporation。原 OM-FIN-020 唯一登记 Arab Bank plc，无画像，可恢复注册引用，后续统一国际银行主ID。','Arab Bank与Bank ABC不同',['https://www.bank-abc.com/en/AboutABC/Pages/Fact-Sheet.aspx'])
put([193,194],'暂缓','源明确 Bank of New Zealand／BNZ，新画像 NZ-FIN-006 实际为 Kiwibank。原 PG-GOV-092 登记BNZ却误分类GOV、无画像；需先找到或分配正确银行ID。','同国不同银行／原注册类型错误',['https://www.bnz.co.nz/about-us'])
put([199],'暂缓','源将 Citibank／Citigroup 合并并跨1984—2010多个职位；新目标为集团。需明确银行法人和1998年前历史主体，不能将集团别名当成严格同一雇主证明。','银行与集团／历史主体合并')
put([213],'暂缓','组织标题写汇丰控股，但职位说明是伦敦及沙特业务分部股票销售；目标画像混列控股公司与各地银行别名。需以雇主履历确认具体法人，暂不据标题确认。','岗位实体层级待核')
put([231],'暂缓','条目自己注明实际职务是 MUFG Americas Holdings Corporation CFO，因未注册而用母集团ID；这是母子公司替代，不是精确实体匹配，应确认是否允许集团聚合或补子公司。','明确以母公司代替子公司')
put([236,237],'暂缓','源仅用HSBC品牌描述历史股权，新目标为汇丰控股；实际持股银行/保险法人尚未由本行证据确认。目标画像混列多家子公司为别名，需先核直接股东实体。','品牌与实际持股法人待核')

# World Bank (IBRD+IDA) and World Bank Group are not automatically identical.
wb='https://www.worldbank.org/lo/about'
for x in D:
 if x['new_target']['id']=='US-INTL-003':
  i=x['review_row'];label=x['current_reference']
  if 'World Bank Group' not in label and 'The World Bank Group' not in label and '世界银行集团' not in label:
   put([i],'暂缓','目标画像主体为 World Bank Group（集团）；本行写 World Bank／世界银行，未明确是否指IBRD+IDA或集团聚合口径。普通名称接近不足以作法律实体等同判断；需先确定实体粒度及对应主ID。新旧ID均暂不改。','世界银行与世界银行集团粒度待定',[wb])
put([272,274,379,399],'暂缓','一个任职条目并列世界银行及其他独立机构，单个ID只能代表其中一个，需拆分机构与各自任职时间；不能确认整条引用都指World Bank Group。','复合任职需拆分',[wb])
put([258],'回退','源为网络设备厂商 Cisco，新画像为独联体 CIS。原 CI-CORP-055 唯一登记思科且类型为CORP，无画像，可恢复注册引用；后续可与已有Cisco主画像归一。','缩写跨行业误配')
put([408],'回退','源明确黎巴嫩社会进步党机关报 anbaaonline.com；新画像为科威特 Al-Anba。原 LB-MEDIA-041 为同名党报唯一注册项，无画像，可恢复注册引用。','跨国同名报纸',['https://anbaaonline.com/about'])
put([410,411,412,413,415,416],'回退','源明确摩洛哥 Al Mada 投资控股／前SNI，新画像为伊拉克 Al Mada 媒体集团。各原ID均登记该摩洛哥控股且CORP类型正确、无画像，可恢复原注册引用；MA-CORP-089/091/092 为同实体多个ID，后续仍需去重归一。','控股集团与媒体同名',['https://www.almada.ma/fr/strategie-dinvestissement'])
put([414],'暂缓','源同时写迪拜新闻俱乐部与其举办的阿拉伯媒体论坛，新ID只代表俱乐部；需明确关系主体是主办机构还是论坛活动，先拆分复合实体。','机构与活动合并')
put([417],'置空','源明确墨西哥 Canal13／Imevisión，新画像为智利 Canal13；原画像为墨西哥 Milenio 报纸，也不正确。','同频道编号跨国误配')
put([421],'置空','源为菲律宾 China Bank Savings／CBS 储蓄银行，新画像为美国 CBS 电视网；原 PH-CORP-015 实际画像是 ICTSI 港口企业，也不正确。','缩写跨行业／原新均错',['https://www.cbs.com.ph/About_Us.aspx'])
put([422],'置空','源为菲律宾四家专业协会，其中MAP是Management Association of the Philippines；新画像为摩洛哥通讯社MAP，原画像为Mapúa大学。新旧均不匹配，且需拆分四家协会。','缩写跨行业／复合引用')
put([425,426],'置空','源为美国 Vanguard 投资集团；新画像为尼日利亚 Vanguard 报纸。原画像分别是美联储、花旗集团，虽然registry残留trimmed先锋项，实际有画像身份不符，不能回退。','同名跨行业／旧ID碰撞')
put([427,428],'回退','源为美国 Vanguard 投资集团，新画像为尼日利亚同名报纸。原US-FIN-021/047各自仅登记Vanguard、无画像，可恢复原注册引用；两个原ID仍需后续去重。','同名跨行业／原注册尚可恢复')
put([444],'回退','源明确Gawad Kalinga USA（GK USA），新画像为韩国Green Korea United。原PH-NGO-049为唯一匹配注册项、无画像，可恢复注册引用，前缀PH不等于该美国伙伴组织的法律所在地。','缩写不同机构')
put([445],'保留','目标画像name_en明确 Malaysian Red Crescent Society，虽中文原名写红十字会，但引用是同一马来西亚国家红新月会；可保留ID，中文规范名另行修订。','目标中文名待规范，实体一致')
put([472],'暂缓','源为Neil Papenfus于2007—2011年任经理的Port Services Ltd；新画像是阿尔及利亚Groupe SERPORT，缺少同一实体证据。原PG-GOV-356同名但误分GOV、无画像，需结合原履历来源确认法人和有效公司ID。','通名误配嫌疑／原类型错误')
put([481],'置空','源为SCF Management Services Dubai技术管理子公司，新画像是Dubai Holding；原RU-SOE-008实际画像是母公司Sovcomflot，也非所写子公司。新旧均不能作为该子公司的精确链接。','以地名误配集团／原为母公司')

for x in D:
 if x['new_target']['id']=='BO-INTL-008':
  put([x['review_row']],'保留','实际画像的主名称、QID Q7809、官网及内容均指UNESCO全球组织，源条目也引用UNESCO，未见误连另一国别办事处。画像country_iso3/hq_country_iso3=BOL有误，需另修；目录和国别字段不能直接替代主体判断。','链接主体一致／目标画像国别错误',['https://www.unesco.org/en/about-us/practical-info?hub=149803'])

assert set(decisions)==set(range(1,492))
manifest=json.loads((OUT/'cross_public_491_read_manifest.json').read_text(encoding='utf-8'))
assert isinstance(manifest,dict)
changed=[p for p,h in manifest.items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
assert not changed, f'Snapshot changed: {changed[:10]}'
records=[]
for x in D:
 i=x['review_row'];v=decisions[i];r=dict(x['row']);path,ptr=r['原始引用位置'].split('#',1)
 a,n,f=re.fullmatch(r'(\w+)\[(\d+)\]\.(\w+)',ptr).groups()
 live=json.loads((ROOT/path).read_text(encoding='utf-8-sig'))[a][int(n)]
 assert live.get(f)==x['current_id']==r['新ID']
 assert (live.get('organization') or live.get('org_name'))==x['current_reference']
 old=x['old_target'];new=x['new_target'];b=new['profile']['basic_info']
 if v['conclusion']=='回退' and not old.get('profile'):
  regs=[r for r in old.get('registry',[]) if r.get('org_id')==old['id'] and not r.get('person_id')]
  assert len(regs)==1 and regs[0].get('status') not in ['excluded','trimmed'], (i,regs)
 r['复核结论']=v['conclusion'];r['备注']='助手复核建议，未获执行授权。'+v['reason']
 r.update({'复核序号':i,'优先100样本':'是' if x['priority_sample'] else '否','问题分类':v['issue'],
 '当前ID校验':'与原清单新ID一致','原ID有画像':'是' if old.get('profile') else '否',
 '新画像实际名称':b.get('name_en') or b.get('name_original') or b.get('name_zh'),
 '原始条目上下文':json.dumps(x['entry'],ensure_ascii=False,separators=(',',':')),
 '画像证据位置':new['file']+'#basic_info','外部参考':' ; '.join(v['external_sources']),
 '证据范围':'本地原条目、实际画像、注册表交叉核对'+('；关键实体区别已查官方来源' if v['external_sources'] else '；本行未逐项重新外网查证'),
 '执行授权':'否；仅供讨论'})
 records.append(r)
for name,rows in [('step1b_cross_public_review_reviewed.csv',records),('step1b_cross_public_priority_reviewed.csv',[r for r in records if r['优先100样本']=='是'])]:
 with (OUT/name).open('w',encoding='utf-8-sig',newline='') as out:
  w=csv.DictWriter(out,fieldnames=list(records[0]));w.writeheader();w.writerows(rows)
summary={'review_only':True,'execution_authorized':False,'total':len(records),'priority_sample':100,
 'conclusions':dict(Counter(r['复核结论'] for r in records)),
 'priority_conclusions':dict(Counter(r['复核结论'] for r in records if r['优先100样本']=='是')),
 'machine_priority_54_conclusions':dict(Counter(r['复核结论'] for r in records[:54])),
 'outside_machine_54_not_keep':[r['复核序号'] for r in records[54:] if r['复核结论']!='保留'],
 'dataset_files_hash_checked':len(manifest),'dataset_files_changed':changed,
 'original_csv_sha256':before,'original_csv_unchanged':all(hashlib.sha256((OUT/n).read_bytes()).hexdigest()==h for n,h in before.items())}
(OUT/'cross_public_491_review_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'cross_public_491_review_decisions.json').write_text(json.dumps({'review_only':True,'execution_authorized':False,'rows':[{'review_row':i,**decisions[i]} for i in range(1,492)]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=['# Step1b 公共机构类跨国改动：491条复核意见','',
 '复核日期：2026-11-13。仅形成助手复核建议，不代表用户执行授权；没有修改画像、注册表、索引、任何引用ID或头像。台湾人物采集已按要求收尾暂停，第二批完成8/15人，未启动剩余7人。','',
 '本轮范围是所给491条引用变更，覆盖195个不同新目标ID；“公共机构类”是原清单筛选标签，实际包含商业银行、大学、媒体、企业及国际组织，不能把它理解为491条政府机构变更。所给优先100条含全部54条机器优先项。','',
 '|复核建议|优先100条|全量491条|','|---|---:|---:|']
for k in ['保留','置空','回退','暂缓']:
 report.append(f"|{k}|{summary['priority_conclusions'][k]}|{summary['conclusions'][k]}|")
report += ['', '保留348条仅表示现有引用文字、上下文与目标画像未发现主体冲突；不是对全部履历、事件、职务和股权比例的事实背书。置空19条为新旧目标均不能支持该实体。回退39条建议恢复原引用，其中只有第32条原目标已有画像；其余38条恢复的是无画像的、唯一且未被排除的注册条目，页面仍可能显示“无档案”。没有画像不等于该身份不成立，但恢复注册引用也不能解决画像缺失。暂缓85条不是确认正确，不宜纳入自动保留白名单。','',
 '## 核查方法和边界','',
 '逐条读取原始引用位置、整条任职/关系描述、原画像、新画像及其注册记录；以actual basic_info为准，不以CSV展示名或ID国别前缀替代身份。关键疑难实体区别查询了官方来源，具体链接写在CSV“外部参考”列。其他行主要是本地数据一致性复核，没有声称逐条完成独立外网事实核验。每条均保留原始上下文、画像证据位置和证据范围。','',
 '491/491条当前ID与原清单“新ID”一致，引用名称和数组位置重新校验通过。所读取675个画像/注册/引用源文件SHA256与起始快照一致，两份输入CSV字节未变。该验证只覆盖相关675文件，不代表重新做了全库头像盘点；本轮程序没有任何图片写入操作。','',
 '## 主要发现','',
 '- UNICEF 18条误连吉尔吉斯斯坦办事处：建议回退13、置空1、暂缓4。原KH-INTL-006同时登记UNICEF与UNAIDS，不能回退；TH-IGO-001格式也需处理。[UNICEF国别办公室官网](https://www.unicef.org/kyrgyzstan/contact-us)。',
 '- RFE/RL 5条误连吉尔吉斯语部：建议回退1、置空4。原土库曼语部也不能代表集团总部。[RFE/RL官方对Azattyk的定义](https://about.rferl.org/article/central-asia-in-focus-attacks-on-rfe-rls-kyrgyz-service/)。',
 '- 第69条日本Tokai University误连台湾Tunghai；第82条利比亚宰图纳大学误连突尼斯同名大学。两条不在54个机器优先项中。[日本校方任职报道](https://www.u-tokai.ac.jp/news-campus/192891/)、[利比亚校方介绍](https://azu.edu.ly/ar)。',
 '- 第193—194条BNZ误连Kiwibank，证明同国也可错；第178—182条涉及阿曼Ahli与利比亚Aman、约旦Arab Bank与巴林Bank ABC混淆。[BNZ官方](https://www.bnz.co.nz/about-us)、[阿曼央行银行名录](https://cbo.gov.om/Pages/LicensedBanks.aspx)、[Bank ABC官方身份](https://www.bank-abc.com/en/AboutABC/Pages/Fact-Sheet.aspx)。',
 '- 第258条Cisco→独联体，第410—416条中的6条摩洛哥Al Mada控股→伊拉克媒体，第421条China Bank Savings→美国CBS电视网，第425—428条Vanguard投资→尼日利亚报纸，均非名称变体。[Al Mada官方投资业务](https://www.almada.ma/fr/strategie-dinvestissement)、[China Bank Savings官方](https://www.cbs.com.ph/About_Us.aspx)。',
 '- 第408条黎巴嫩社会进步党机关报Al-Anbaa→科威特同名报纸，机器列在较低优先级；原注册项可恢复。[黎巴嫩党报官方介绍](https://anbaaonline.com/about)。',
 '- UNESCO的27条链接可保留：目标主名、QID、官网指向全球UNESCO，并非玻利维亚办事处，但目标画像把总部国别写成BOL，是另一个数据错误。不能因错误国别字段再拆出一个假身份。[UNESCO总部地址](https://www.unesco.org/en/about-us/practical-info?hub=149803)。',
 '- 世界银行74条中，明确写World Bank Group的13条保留，其余61条暂缓（其中4条是多个机构混在一条任职中）。World Bank与World Bank Group需先确定是否允许集团聚合口径，不将这61条报成已证实错链。[世行官方机构区分](https://www.worldbank.org/lo/about)。','',
 '## 暂缓项需要的决策','',
 '1. 是否允许World Bank→World Bank Group、银行法人→控股公司、历史前身→现集团这类聚合映射；建议精确身份与集团关系分开。',
 '2. 同名但原ID误分GOV、旧ID碰撞、被排除条目，先整理注册表再分配有效身份，不直接恢复。',
 '3. 多机构合并的一条任职（例如世界银行/财政部/麦肯锡、NZX/ASX、四家菲律宾协会），需要拆条；不是用一个新ID覆盖整行。','',
 '## 后续建议（尚未执行）','',
 '先讨论19条置空及第32条有画像回退；38条无画像注册回退另为一组，明确会继续显示无档案及后续去重责任。85条暂缓待粒度规则和注册表身份厘清。执行时必须重新检查引用文字、当前ID与数组位置，并为变更建立undo日志；不要直接把助手复核CSV接入现有执行器。机器优先54条之外还有27条建议置空/回退，不能只处理54条。','',
 '## 交付文件','',
 '- `output/_id_audit/step1b_cross_public_priority_reviewed.csv`：优先100条，助手已填结论及理由。',
 '- `output/_id_audit/step1b_cross_public_review_reviewed.csv`：全量491条，复核序号对应原全量文件数据行，不含表头。',
 '- `output/_id_audit/cross_public_491_review_decisions.json`：逐条建议，review_only=true、execution_authorized=false。',
 '- `output/_id_audit/cross_public_491_review_summary.json`：统计、原CSV哈希、未修改验证结果。',
 '- `output/_id_audit/cross_public_491_context.json` / `cross_public_491_read_manifest.json`：证据快照与675文件哈希。','']
(ROOT/'docs/cross-public-491-review.md').write_text('\n'.join(report),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))

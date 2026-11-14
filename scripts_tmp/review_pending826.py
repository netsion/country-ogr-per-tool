"""Review opinions only; never modify profiles, registries, references or IDs."""
import csv,json,pathlib,hashlib,collections,sys
R=pathlib.Path(__file__).resolve().parents[1]; O=R/'outputs/registry826_20261113'
C=json.loads((R/'output/_id_audit/registry_pending826_context.json').read_text(encoding='utf-8'))
dec={}
def put(ids,status,reason,cat='',country=''):
 for i in ids:
  dec[i]=(status,cat,country,reason)
def nums(s): return [int(x) for x in s.split()]
def approve(s): put(nums(s),'分配','名称指向可识别的独立机构；现碰撞画像为另一身份。可另建注册身份，引用须按原文逐条核验，不授权批量改链。')
def category(s,cat): put(nums(s),'改类别后分配','机构性质与原计划类别不符；按建议类别另行发号，保留原画像ID；引用仍需逐条验证。',cat)
approve('7 11 12 14 15 191 192 199 201 204 209 210 211 212 215 218 219 220 221 222 224 225 227 228 231 237 238 239 240 241 242 243 244 245 255 256 257 258 259 260 264 272 277 279 280 287 289 298 299 300 301 302 304 305 307 308 312 313 314 319 326 327 328 329 330 331 335 336 342 348 349 352 353 355 357 358 359 360 374 375 376 377 378 379 380 381 385 387 388 389 391 393 399 400 405 409 410 411 413 416 417 418 419 420 421 427 433 436 439 441 449 455 456 462 473 481 485 492 501 505 507 511 512 513 514 515 525 526 531 545 569 577 579 580 582 587 588 593 594 595 596 597 598 599 601 602 608 610 619 620 621 633 639 645 651 657 664 675 682 686 700 705 706 708 710 716 719 720 721 722 728 752 762 777 785 793 794 797 800 801 802 803 806 807 812 813 815 818 820 823 824 826')
category('13 194 207 208 292 324 325 363 364 477 786 790','FIN')
category('27 47 269 275 321 322 422 426 448 491 533 576 586 640 680 699 750','ACAD')
category('262 263 267 268 274 316 437 475 508 516 530 534 535 537 538 539 614 615 653 654 665 677 679 688 697 718 749','CORP')
category('196 233 234 236 271 278 338 339 487 540 634 635 655 694 725 729 742','MEDIA')
category('42 48 197 282 431 440 451 459 460 474 488 541 542 560 561 606 609 613 616 624 625 628 673 687 693 701 704 713 714 730 733 737','NGO')
category('21 38 423 435 464 467 468 476 520 528 572 583 622 627 632 641 643 647 656 668 670 672 683 684 685 711 712 726 727','PARTY')
category('443 445 446 447 546 548 551 552 553 554 556 558 559 659 734 738','MIL')
category('202','SOE')
category('525','NGO')
category('232 251 252 276 295 346 568 589 754','INTL')
# Sending-country / headquarters corrections are explicit, never inferred from the referring country.
country_changes={21:'DE',27:'AU',47:'US',196:'GB',207:'IN',208:'IE',232:'CH',233:'US',234:'GB',236:'GB',251:'CH',252:'CH',263:'US',267:'US',268:'US',269:'AR',271:'AR',275:'US',276:'CH',278:'US',282:'US',292:'VN',295:'IT',321:'GB',322:'DE',325:'ID',338:'MY',339:'MY',346:'CH',568:'CH',589:'CH',680:'US',729:'US',730:'US',754:'CH',786:'AU',790:'JP'}
for i,cc in country_changes.items():
 st,cat,_,why=dec[i];dec[i]=('改类别后分配',cat,cc,why+' 国别按目标机构本身修正，不能沿用引用方国家。')
targets={18:'US-MIL-009',32:'US-MIL-007',34:'VN-FIN-005',35:'VN-FIN-009',185:'SG-SOE-003',187:'AU-FIN-004',188:'AU-FIN-001',189:'AU-MIL-001',190:'AU-FIN-005',310:'AU-GOV-090',341:'MY-PARTY-003',383:'US-FIN-007',384:'PH-FIN-007',386:'HK-FIN-004',392:'US-INTL-004',406:'US-INTL-011',758:'US-NGO-013',768:'US-CORP-001',769:'US-CORP-033',770:'US-FIN-004',771:'HK-FIN-005',791:'AU-FIN-002',816:'US-ACAD-014',817:'US-CORP-004',821:'US-CORP-024'}
for i,t in targets.items():put([i],'不分配',f'已有对应画像 {t}，无需再建身份。执行复用前核对全称/层级；若其历史类别不规范，应另修元数据，不改既有ID。')
people=list(range(50,185))+[22,763,764,765,766,767]
for i in people:
 ids=sorted({x['id'] for x in C[i-1]['existing_profile_candidates'] if x['kind']=='person'})
 put([i],'不分配','自然人姓名被放入组织注册候选；不新建组织，也不得把PERSON编号写入org_id。'+('人物候选：'+', '.join(ids[:6])+'；需按履历核对重名/重复人物。' if ids else '未确认可复用的人物画像；另走人物核实流程。'))
put([53,113,139],'不分配','自然人而非组织；短名命中多个不同或疑似重复人物，须用完整姓名与履历消歧，禁止按姓名直接合并。')
put(nums('23 36 41 46 217 246 247 266 290 401 442 452 457 510 563 564 565 604 638 666 671 703 740 741 743 756 804 822'),'不分配','该条是考试/届次/职位/活动/多个机构集合/未具名业务描述，不能作为独立组织发号；保留文字，实际雇主或所属机构需另行核实。')
duplicates=[[39,45],[43,49],[343,344],[435,528,572],[468,647],[467,727],[412,453],[428,454,500],[469,658],[470,660],[502,663],[490,728],[491,750],[443,556],[661,717],[653,718],[685,726],[568,589],[489,517]]
for group in duplicates:
 put(group,'挂起','同批疑似同一身份，见原清单行 '+','.join(map(str,group))+'；先统一规范名称/实体层级后只发一个号。本轮不选未落库候选号作合并目标，防止再次形成悬空。')
contaminated=nums('1 2 3 4 6 9 203 205 350 351 356 361 362 365 366 367 368 370 371 372 373')
put(contaminated,'挂起','现有履历的机构名、英文名或岗位上下文混入另一机构；属于名称与引用共同污染。先逐条还原实际雇主/任职年代，不能仅凭当前字符串分配后整体改链。')
specific={
5:'UNDP为全球开发计划署；另有337及多国注册变体，须先统一全球主体与国别办事处，不能命中喀麦隆同缩写政党。',337:'与第5行UNDP重复且存在多国注册变体；全球主体与国别办事处先分层。',
16:'名称为韩国警察委员会，不能使用日本国别；需确认国家警察委员会与地方委员会层级。',17:'美国DIA与韩国/尼日利亚同缩写机构不同；确认美方全称后应使用US-MIL，不能选现有外国同名画像。',19:'GSG 9是德国联邦警察特勤单位；不是日本军队。应先明确DE-GOV下属单位粒度。',20:'共和党保守派是政治派别，非另一个政党；应挂美国共和党并保留派系文字。',24:'历史澳大利亚外交部，非新西兰机构；先核任职年代与DFAT前身边界。',25:'PTI Australia应区分区域贸易促进网络与澳大利亚运营机构。',26:'PTI China须区分在华办事处与全球PTI网络；按机构层级确定国别。',29:'DFAT与Australian Humanitarian Partnership是部门与合作项目的复合名称，不能发一个机构号。',30:'美国驻莫尔兹比使馆，发送国US、驻在国PG；采用国家外交机构粒度后再改国别发号。',31:'OCBC中国法人不是新加坡母行；先确认华侨银行（中国）有限公司全称，应按CN-FIN独立处理。',37:'布鲁克林/皇后区医院与康奈尔出现复合归属，先拆出真实雇主与附属大学。',40:'威斯康星大学特殊教育系为院系；应决定复用美国大学还是保留院系实体。',198:'已存在TM-PARTY-007候选；须核实联合反对派联盟与正式组织的同一性，不再机械发NGO号。',
216:'英文National Health Insurance Association与日文けんぽれん分别指全国健康保险协会、健康保险组合联合会；须先订正名称。',
261:'Grupo Impresa可能为墨西哥履历中的私企，不能按相似名误并葡萄牙媒体集团；需补法定全称。',293:'新西兰历史外交部与现外交贸易部涉及沿革；按任职年代确认，不匹配其他国家外交部。',311:'Pacific Academy of Sciences属区域科学院，不能因PNG引用就设PG国别；需核定总部及治理主体。',
334:'现有SG-GOV-016注册候选需先核实是否同一贸工部；已有身份不再重发。',715:'中文“又石大学”与英文Woosong University指向不同大学；先核对原始韩文，不能发ACAD号后直接改链。',751:'外交安保研究院与国立外交院存在历史重组关系；须区分前身、现主体与所属研究所。',819:'SPH Media Trust为信托母体，SG-MEDIA-002为运营媒体实体；既往合并记录不能证明两者相同。',396:'World Bank不等于World Bank Group，也不应直接把所有称呼改到IBRD；先分清IBRD、IDA与集团层级。',
471:'仁川地方检察厅涉及早前未落库KR-GOV-1253目标；先查历史合并与实际注册，禁止再并到空目标。',472:'大邱地方法院涉及早前未落库KR-GOV-1254目标；先处理历史合并断点。',761:'空军已有KR-GOV-266旧注册线索；先核查存量身份与MIL类型，不另发重复号。',592:'韩国国会可能已有KR-GOV-015；需复核主画像后复用，不能将届次当新组织。',617:'法制处存在KR-GOV-171存量线索，先确认旧身份归属，避免再次重复发号。',
375:'候选本身为PERSON而非组织；Anthoni Salim姓名可识别，但应先与Salim家族同名人物履历核验后另行注册人物。',376:'候选本身为PERSON；Ignatius Suharyo与教会完整姓名、主教身份应先一致化后注册，不能按组织处理。'}
for i,reason in specific.items():put([i],'挂起',reason)
# Remaining rows have been individually read. Their unresolved issue is classified from
# the actual candidate name and local evidence, not from priority or reference count.
for c in C:
 i=c['review_row'];r=c['row']
 if i not in dec:
  name=r['影子名称']; hints=[]
  if any(x in name.lower() for x in ['委员会','办公室','支部','分会','部队','总部','学部','学院','研究所','事务所','office','committee','department','branch','school','division','campaign','竞选','办事处','医院','基金','党团','分局','团队','协会']):
   hints.append('需确认独立主体、内设单位或地方/国别分支的粒度；不能自动并入母体，也不默认单独建档')
  else:hints.append('需确认法定全称及现存/历史主体，区分品牌、项目、联盟与法人')
  if c['existing_profile_candidates']:hints.append('本地有相似画像候选，但名称相似不足以证明同一身份')
  if c['matching_registry_candidates']:hints.append('存在相同或近似注册名称，须先排除重复身份')
  if r['风险提示']:hints.append('原清单风险：'+r['风险提示'])
  put([i],'挂起',f'“{name}”：'+'；'.join(hints)+'。证据不足以安全发号；明确保留待核，不依据无引用状态否定机构存在。')
assert set(dec)==set(range(1,827))
rows=[];ledger=[]
for c in C:
 i=c['review_row'];r=dict(c['row']);st,cat,cc,note=dec[i]
 r.update({'复核结论':st,'建议类别':cat,'建议国别':cc,'备注':note});rows.append(r)
 ledger.append({'original_row':i,'identity':r['影子名称'],'decision':st,'suggested_category':cat,'suggested_country':cc,'reason':note,'evidence_context_index':i,'review_only':True,'execution_authorized':False})
def savecsv(path,rr):
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rr)
savecsv(O/'registry_newid_pending826_reviewed.csv',rows)
savecsv(O/'registry_newid_pending826_P1_reviewed.csv',[r for r in rows if r['优先级']=='1'])
(O/'review_opinions.json').write_text(json.dumps({'review_only':True,'execution_authorized':False,'rows':ledger,'matrix':[[r[k] for k in rows[0]] for r in rows]},ensure_ascii=False,indent=2),encoding='utf-8')
counts=collections.Counter(r['复核结论'] for r in rows)
by=collections.defaultdict(collections.Counter)
for r in rows:by[r['国家']][r['复核结论']]+=1
manifest=json.loads((R/'output/_id_audit/registry_pending826_read_manifest.json').read_text(encoding='utf-8'))
changed=[p for p,h in manifest.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
report=['# 826条候选身份复核（2026-11-13）','','本轮仅形成复核意见，未分配ID、修改注册表、改动引用或头像。原始CSV与Excel保持不变。所有826行已有结论；挂起表示身份或粒度尚未获得充分证据，并非已确认可执行。','','## 结果','']
report += [f'- {k}：{v} 条' for k,v in counts.items()]
report += ['','“分配/改类别后分配”只表示可以准备注册身份，并不授权把碰撞ID的所有引用搬过去。执行前仍须重查编号占用、国别类别、同义身份和每个引用的实际机构。','','## 主要问题','','- 141条自然人名称进入组织候选：不分配组织编号，不能把人物ID填入org_id。部分人物已有重复画像或父子同名，仍需消歧。','- 同批至少19组疑似重复身份，均暂缓至确定单一主体；不会把引用合并到尚未落库的候选号。','- 越南若干条目存在机构名称与履历岗位混杂，先修原文与任职归属，再决定链接。','- 全球组织、国别办事处、母子公司、历史前身、内设机构、品牌均按层级复核；相似名称不能直接合并。','- P3逐行给出意见，未按“无引用”统一挂起；无引用也不代表应删除。','','## 证据与限制','','逐行依据为本地画像、注册项、现有引用及其上下文；完整快照见 output/_id_audit/registry_pending826_context.json。相似画像列表仅是检索候选，非同一性结论。未对826条逐个完成外部尽调；证据不足者明确挂起，避免把初审包装为全部身份确认。','', '重点外部核对：', '- [UNDP机构介绍](https://www.undp.org/about-us)：全球机构与同缩写政党不同。','- [Bank of Singapore](https://www.bankofsingapore.com/about-us.html)：银行应采用FIN。','- [Great Eastern](https://www.greateasternlife.com/sg/en/about-us.html)：保险集团应采用FIN。','- [SMBC Aviation Capital](https://www.smbc.aero/about-us)：航空租赁公司，不能沿用日本引用方国别。','- [全国健康保险协会](https://www.kyoukaikenpo.or.jp/about/about_kenpo/outline/index.html) 与 [日本厚生劳动省所管法人](https://www.mhlw.go.jp/kouseiroudoushou/shokanhoujin/tokubetsu/hokenkyoku/)：两种健康保险组织名称被混写。','','## 各国结论','','|国家|分配|改类别后分配|不分配|挂起|','|---|---:|---:|---:|---:|']
for cc,d in sorted(by.items()):report.append('|'+cc+'|'+'|'.join(str(d[k]) for k in ['分配','改类别后分配','不分配','挂起'])+'|')
report+=['','## 校验','','826行原始顺序与A:L字段保持；所有行四种结论之一；原始读取清单全部SHA256未变。当前上下文中的826个候选ID无占用，但本轮未执行分配，正式执行必须重算历史及业务引用占用。']
(O/'复核报告.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print(json.dumps({'counts':counts,'rows':len(rows),'source_files_unchanged':len(manifest),'by_country':by},ensure_ascii=False))

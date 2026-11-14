# 80条新ID抽查复核

日期：2026-11-13。已逐条复核全部80条（KR/MX/NZ/JP各20）。本轮仅生成助手意见，未分配任何新ID，未更改registry、原画像、引用、索引和头像。原始80条CSV与全量计划CSV保持不变。用户的“继续”按继续完成本轮复核理解，不视为ID变更授权。

结论：不能采用“其余按可分配执行”。原机器判断71条可分配，其中24条本轮未直接通过。并且候选ID分配器忽略了非活动条目占用的历史编号，存在再次制造身份错乱的风险。

|复核意见|数量|含义|
|---|---:|---|
|分配|51|独立身份/类别原则可用；编号仍须用修正后的分配器重新确认，引用迁移另核|
|改类别后分配|2|第24条Telmex改CORP；第67条RIKEN按科研机构ACAD口径|
|不分配|6|否定本行所提新ID或重复新身份，并不否认机构存在|
|挂起|21|历史编号占用、重复影子、跨国主体、沿革或组织粒度未解决|

“分配”是复核建议，不等于允许立即写入本行建议编号，也不是对全组引用及所有任职/股权内容的事实背书。分类是本项目当前大类下的建议：公共资助/行政执行机构用GOV，核心科研机构用ACAD，国有经营企业用SOE；不同于仅按法律形式或名称关键词分类。

## 1. 必须先修的编号问题

样本8条（1、4、5、6、8、11、12、13）的建议新ID已在注册表出现，状态均为duplicate，且旧主体与拟赋予的新主体不同。它们全部标为挂起。扩大到全量983个assign_new_id计划只检查编号占用，发现14个历史编号重用，均在韩国。这不是对983个实体完成了复核。

|拟分配ID|拟分配身份|该ID既往登记身份|
|---|---|---|
|KR-ACAD-017|Korea University|Incheon National University|
|KR-ACAD-018|Yonsei University|Korea University of Science and Technology|
|KR-ACAD-019|KAIST|KDI School of Public Policy and Management|
|KR-ACAD-020|Pohang University of Science and Technology|Korea Institute of Science and Technology|
|KR-ACAD-021|Korea Advanced Institute of Science and Technology|Institute for Basic Science|
|KR-ACAD-022|Hanyang University|Korea Research Institute of Bioscience and Biotechnology|
|KR-ACAD-023|Sogang University|Electronics and Telecommunications Research Institute|
|KR-CORP-031|LG Energy Solution|Korea Aerospace Industries|
|KR-CORP-032|Lotte Group|Samsung SDS|
|KR-CORP-033|Hyundai Steel|Nonghyup Bank|
|KR-FIN-015|Shinhan Financial Group|Bank of Korea|
|KR-MEDIA-017|Munhwa Broadcasting Corporation|Newstapa|
|KR-MEDIA-018|Yonhap News Agency|OhmyNews|
|KR-SOE-019|Korea Land and Housing Corporation|Airport Railroad Corporation|

原因可直接在scripts_tmp/registry_dedupe_plan_v2.py复现：maxseq只从现画像和active注册项计算，而active排除了duplicate等状态。编号不应因条目失活而变成空号。修正时须纳入活动/非活动/归档/合并/已预留编号，并在写入前再次检查；本轮没有修改分配器或重排编号。

## 2. 同一个实体被建议发多个ID

- 第6条KAIST与全量计划KR-ACAD-006下Korea Advanced Institute of Science and Technology是同一高校，应合为一个身份，不能分别发019和021。[KAIST官网历史全名](https://www.kaist.ac.kr/eng/)。
- 第7条Hyundai Steel与KR-CORP-022下同名影子是同一钢铁公司，不能分别发033、034。与Hyundai Motor或HD Hyundai集团也不等同。
- 第43和47条Commerce Commission是同一新西兰监管机构，合计7处引用。第43条可作为共同主身份候选，第47条标不分配，不能同时发153和174。

## 3. 机器类别提示中4条应维持原类别

|样本行|机构|复核类别|依据|
|---|---|---|
|20|Korea Airports Corporation|SOE|[官网明确state-owned company](https://www.airport.co.kr/wwweng/cms/frCon/index.do?MENU_ID=50)|
|33|CNBV|GOV|[墨西哥政府确认SHCP下属监管机关](https://www.gob.mx/cnbv/que-hacemos)|
|41|NZ On Air|GOV|[新西兰政府列为自主Crown实体及内容资助机构](https://www.mch.govt.nz/our-work/governance-and-monitoring/entities-overview)|
|50|National Council of Women NZ|NGO|[官网确认非营利注册慈善团体](https://www.ncwnz.org.nz/our-people)|

第24条Telmex确需由GOV改CORP。第69条INCJ/JIC不能只改FIN：引用把2018年后JIC与INCJ混写，需先区分具体主体及FIN/SOE口径。另有机器未提示的第67条RIKEN，建议与AIST/QST统一按ACAD科研机构处理。[RIKEN官方定义](https://www.riken.jp/en/about/)、[JIC官网](https://www.j-ic.co.jp/en/news/20260423-jic-pressrelease-en)、[INCJ官方明确为JIC子公司](https://www.incj.co.jp/newsroom/INCJ_20181211.pdf)。

## 4. 未被机器充分识别的国别与粒度问题

- 第26条Valora为瑞士公司，第27条Southern Copper为美国注册/总部公司。母公司来自墨西哥，不等于应新建另一个墨西哥身份；均挂起确认登记策略。[Valora联系页](https://valora.com/en/contact)、[Southern Copper公司备案](https://southerncoppercorp.com/eng/wp-content/uploads/sites/2/2026/04/8k260417.pdf)。
- 第53—55条Intuit、Lactalis、Vocus明确分别为美国、法国、澳大利亚集团，不同意照提案在NZ下直接分配；跨国存储策略可讨论，但不能复制出第二个“新西兰总部”身份。[Intuit总部](https://www.intuit.com/company/locations/)、[Lactalis法定地址](https://www.lactalis.com/en/legal)、[Vocus澳洲法人](https://www.vocus.com.au/privacy-policy)。
- 第40条SACSCOC不应按MX-ACAD直接建“美国南部院校协会”，需明确美国教育认证组织口径，并与SACS区分；第30条AUSJAL是跨国高校协会，不是一所大学，秘书处位置和法律注册地也需区分。
- 第52条GSJ是日本地质科研机构、当前AIST内部研究领域，不是新西兰大学或日本国交省。第56条Macquarie Asset Management是澳大利亚金融集团业务，不能直接归到NZ-CORP或直接以集团代替实际雇主。
- 第48条同组两个引用分别是现Auckland Council和2007—2010年的Auckland City Council，需分开；第25条也涉及Tlalpan旧Delegación与Alcaldía。第2、18、69条的部委/基金前后身需按日期核定。
- 第61条SMBC可以建立独立银行身份，但19条引用中4条开始于2001年成立前，须拆历史前身或核实当时雇主；不能整组迁移。第62条也有跨证券公司旧名/重组的长段任职。[SMBC官方沿革](https://www.smbc.co.jp/global/aboutus/profile/history.html)。

## 5. 三条原计划未给新编号

第51条机器拟合并韩国Progressive Party，但源明确新西兰Jim Anderton政党/联盟，标挂起；第70条日本IPA误候选为阿尔及利亚Pasteur Institute，第79条日本NARO误候选为乌干达同名研究机构。后两条日本独立身份可以分配，但必须拒绝原跨国合并目标，并重新生成未占用编号。三条均不能把空建议ID当成已通过的执行计划。[IPA官方机构定义](https://www.ipa.go.jp/about/disclosure/teikyo/soshiki.html)、[NARO官方名称](https://www.naro.go.jp/introduction/profile.html)。

## 6. 复核范围及验证

- 读取最新国别数据集的注册表、画像和全部相关引用，证据快照保留原条目、指针、候选画像、同名注册项；共23,686个输入文件通过SHA256未变校验。
- 样本由各国按引用数排序取前20，并非随机抽样，不能估计全库错误率，也不能把53条原则可用外推为983条全部可执行。
- 独立主体判断结合本地完整引用上下文，疑难分类/国别/沿革查询了官方和行业认证来源；没有声称80行的所有关系、日期、任职和股权事实均独立外网复证。
- 候选搜索沿用原有模糊匹配只作召回，没有自动采纳其结果；例如Korea University→UST、IPA→阿尔及利亚研究所、NARO→乌干达机构已人工排除。
- 现画像自己的ID、图片profile字段、头像文件、registry、原始抽样CSV及全量分配计划均未修改。

## 交付及建议顺序

1. `registry_newid_sample_80_reviewed.csv`：80行完整意见、类别/国别建议、编号占用和引用证据位置。
2. `registry_newid_sample_80_attention.csv`：29行非直接分配意见，方便优先讨论。
3. `registry_newid_reserved_14.csv`：全量983候选中14个已用历史编号证据。
4. `registry_newid_80_review_decisions.json` / `registry_newid_80_review_summary.json`：带review_only和未授权标志的结构化结果。
5. 先修编号分配器，再做跨collision_id的影子实体去重，接着明确外国主体、历史实体及业务分部粒度；最后才重新生成执行计划。51条“分配”及2条“改类别后分配”也应在新计划中逐项复验，而不是直接读助手CSV批量执行。

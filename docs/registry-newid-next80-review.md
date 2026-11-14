# 第二批80条新ID复核

日期：2026-11-13。本轮已完成80条逐项意见及必要的上轮合并复核，只写复核产物，没有更改registry、画像、引用ID、索引或图片。没有执行新的分配，也没有回退上一轮操作。

**结论：本批建议25条可分配独立身份、2条改类别后分配、25条不按原方案分配、28条挂起。先处理已确认的编号占用与合并闭合性问题，再生成执行计划。**

|意见|KR|MX|NZ|JP|合计|
|---|---:|---:|---:|---:|---:|
|分配|2|3|9|11|25|
|改类别后分配|0|0|1|1|2|
|不分配|3|12|3|7|25|
|挂起|15|5|7|1|28|

“分配”表示独立主体和类别在当前证据下原则可用，不是写入授权，也不表示本行全部职务、股权、日期与关系内容已核实。“不分配”是否定本行所提组织身份/国别/编号，不代表删除已知实体；外国实体要走主身份归一，人物要走人物修复，不能永久丢弃。

## 1. 编号分配器还缺一类保留号：已有悬空业务引用

80个建议编号均未出现在全部日期registry及deprecated注册项中，但其中3个编号已经出现在当前业务引用，合计5个位置，而且名称不是本次拟赋予的实体。只检查registry、画像和索引仍不够。

|候选编号|本次拟分配身份|当前业务引用实际写的身份|
|---|---|---|
|KR-ACAD-028|Hanyang University|Korea Institute for National Unification（统一研究院）|
|KR-CORP-035|Lotte Group|POSCO E&C；Korail Retail|
|KR-CORP-036|Amorepacific Corporation|POSCO DX；Korail Logis|

以上样本第1、3、4条均挂起。后两号在存量数据里本来就各自被两家不同公司共用；这是已有未注册ID混乱，不能通过给它们新建本次候选画像来解决。应将所有引用字段中的非空ID也纳入保留集合，并对每个已用ID的名称/主体冲突分别处理。

证据：output/kr/2026-05-04/orgs/KR-GOV-007.json#related_entities[7].org_id；KR-CORP-006.json#related_entities[2]/[4].org_id；KR-SOE-003.json#related_entities[4]/[6].org_id。完整原条目见review_summary.json的proposed_ids_already_in_references。

## 2. 上轮7条same_identity中4条目标尚未建立

|源影子ID|影子主体|merged_into|目标活动注册项|当前引用数|
|---|---|---|---|---:|
|KR-CORP-030|Amorepacific Corporation|KR-CORP-036|不存在|2|
|KR-GOV-157|新千年民主党 (새천년민주당)|KR-GOV-1249|不存在|0|
|KR-GOV-305|仁川地方检察厅（인천지방검찰청）|KR-GOV-1253|不存在|0|
|KR-GOV-208|大邱地方法院（대구지방법원）|KR-GOV-1254|不存在|0|

这4条可在registry_newid_exec_undo.json定位到same_identity动作；对应canonical在v3计划中仍为pending_review，却已归档源项并设置merged_into。其余3条（KAIST、雇佣劳动部、Commerce Commission）已存在活动目标注册项。

4个问题目标没有画像；其中KR-CORP-036已有2条业务引用，但它们指POSCO DX和Korail Logis，不是Amorepacific，而且本次61条执行日志没有将任何引用改到这4个目标。因此不能把这2条归因于刚执行的226条改链，也不能称这些只是正确新身份“暂无画像”：这4个canonical连注册身份都未建立。

处理建议：只有canonical身份通过复核且先建立后，才能归档同实体影子；本批不自动补这4个目标。尤其KR-GOV-1249拟代表新千年民主党，GOV类别本身就不合适。KR-CORP-036还有引用身份冲突，不应原号直接补建。

执行器的same_identity分支先修改old的status/merged_into，再把old写入undo，日志中的old已是修改后状态。若要回退，必须先核对真实执行前条目，不能直接把该old当完整原始快照恢复。本轮未修改执行器或运行回滚。

## 3. 人物被列为组织候选：第23、28、36、37条

- 第23条Rosaura Ruiz的114号档案把本人写作雇主，拟建MX-ACAD身份；已有102号和114号人物档案。其部长职位对应SECIHTI，已有MX-GOV-033可作核实候选，须修组织文字及任期，并另处理人物重复，不能把org_id换成人物ID。
- 第28条Fernández Carbajal的119号档案同样把本人写作董事长雇主；已有107号和119号重复人物档案。FEMSA是雇主候选，不是新增同名CORP。
- 第36条实际位于父亲MX-PERSON-000133.person_relationships[1]，说明明确是儿子Claudio的社会活动，影子却用父亲Laporte全名。若机械改到133会产生自指；须识别儿子Claudio X. González Guajardo。
- 第37条也是父亲的儿子关系，Pablo已有MX-PERSON-000134，应该走人物改链复核，不新建组织。

这4条说明仅依据collision_id前缀继承kind/category有结构性错误：必须先看引用字段期待的人物/组织类型，再验证名称究竟是自然人还是组织；work_experience中的organization也可能填错，不能只看字段名称。

## 4. 不是可直接建独立机构的条目

- 第7条“国会议员辅佐官室”未指明任何议员/届次，是通名；第18条“行政高等考试合格”是资格经历。均不分配组织ID。
- 第44条Surveyor-General是法定官员职位，不是组织。[LINZ法定岗位说明](https://www.linz.govt.nz/our-work/statutory-and-support-roles)。
- 第60条CDEM Groups指16个地区机构的集合，不应新建一个全国同名机构。[国家应急管理机构说明](https://www.civildefence.govt.nz/guidance-training/exercises/cdem-exercise-programme)。
- Claro、Bodega Aurrerá、Bait、New Zealand Story、大学网络、咨询小组及大学内设研究所等需要明确品牌/项目/部门建档规则，不能默认为独立法人。

## 5. 国别、类别及沿革

外国候选包括Georgetown（美国）、Talos（美国）、Braskem（巴西）、Iberdrola（西班牙）、ASARCO（美国）、Bimbo Bakeries USA（美国）、Generali（意大利）、Inter National Bank（美国）、伦敦JCPC、日本NIHS、中国大陆清华大学、美国索尼娱乐主体、TCL Electronics和印尼Danamon等。源说明本身已明确多项国别，机器风险提示只覆盖少数；不能按引用方所在地机械发号。

索尼旗下美国公司不等于日本母体。TCL Electronics还须分开开曼注册地与香港总部/上市地，不能只在日本/中国之间二选一。[SIE总部官方](https://www.playstation.com/en-us/corporate/about-us/)、[TCL发行人2025年报](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0429/2026042900031.pdf)。清华大学也不能选用台湾National Tsing Hua University画像来替代大陆Tsinghua。

本批两条改类建议：第53条NZIST按高等教育ACAD；第76条Sony Financial Group按金融控股FIN。第9条自由韩国党已确定应PARTY，但因重复登记及历史身份尚未归一，仍挂起；第71条企业科研公司CORP/ACAD需先统一口径。[NZIST官方过渡说明](https://www.nzist.ac.nz/about/faqs)、[索尼金融官方](https://www.sonyfg.co.jp/en/faq.html)、[丰田中央研究所公司概况](https://www.tytlabs.co.jp/en/company/profile.html)。

实体链接通过也不证明关系事实正确：第45条生产力委员会实际于2024-02-29终止，而源写2024年1月；监管部官网明确它没有取代生产力委员会，原predecessor关系需要另修。[财政部终结报告](https://www.treasury.govt.nz/publications/annual-report/new-zealand-productivity-commission-annual-report-1-july-2023-29-february-2024)、[监管部声明](https://www.regulation.govt.nz/news/building-up-from-establishment-phase/)。第56条Te Arawhiti在2025年已有更名和职权转移，不能继续当现状不变。第32条标题写Bait电商平台而官方明确MVNO业务，同样需要修文字。

## 6. 覆盖范围与验证

- 80/80行均给出结论、理由、类别/国别建议和本地引用位置；60行有原碰撞ID引用，韩国20行没有对应当前引用。另发现Talos一条复合引用，故保留61个匹配候选引用位置，不将其自动迁移。
- 证据快照含五种引用方向，故能识别person_id用了CORP编号的跨类型问题；仅扫描work/related会漏掉第36、37条。
- 23,687个输入文件SHA256校验未变，含原80条清单、v3计划、注册表和读取的画像/执行记录。仅复核与输出报告，未重新盘点头像文件，也未写入头像。
- 主要为本地身份一致性复核，疑难国别/类别/机构性质/沿革查了官方来源；不是80行所有事实逐条独立外网复证。非随机取样，不外推906条剩余计划的错误率。

## 交付与建议顺序

- output/_id_audit/registry_newid_sample_80_next_reviewed.csv：80条完整意见。
- output/_id_audit/registry_newid_sample_80_next_attention.csv：55条非直接分配意见。
- output/_id_audit/registry_newid_prior_merge_check.csv / .json：上轮7条合并闭合性证据。
- output/_id_audit/registry_newid_next80_review_summary.json：计数、5个存量引用位置、编号占用证据。
- output/_id_audit/registry_newid_next80_review_decisions.json / registry_newid_next80_context.json：逐项结构化意见及原始证据。
- output/_id_audit/registry_newid_next80_review_manifest.json：本轮输入哈希。

优先顺序：先补分配器的全引用保留号与same_identity目标存在性检查；再处理4个未闭合合并及当前编号多身份冲突；人物/考试/职位/集合不走组织分配；最后按本轮25+2条原则可用意见重新生成待执行计划。不要从助手CSV直接触发批量写入。

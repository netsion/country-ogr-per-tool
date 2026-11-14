# Step1b 公共机构类跨国改动：491条复核意见

复核日期：2026-11-13。仅形成助手复核建议，不代表用户执行授权；没有修改画像、注册表、索引、任何引用ID或头像。台湾人物采集已按要求收尾暂停，第二批完成8/15人，未启动剩余7人。

本轮范围是所给491条引用变更，覆盖195个不同新目标ID；“公共机构类”是原清单筛选标签，实际包含商业银行、大学、媒体、企业及国际组织，不能把它理解为491条政府机构变更。所给优先100条含全部54条机器优先项。

|复核建议|优先100条|全量491条|
|---|---:|---:|
|保留|59|348|
|置空|12|19|
|回退|20|39|
|暂缓|9|85|

保留348条仅表示现有引用文字、上下文与目标画像未发现主体冲突；不是对全部履历、事件、职务和股权比例的事实背书。置空19条为新旧目标均不能支持该实体。回退39条建议恢复原引用，其中只有第32条原目标已有画像；其余38条恢复的是无画像的、唯一且未被排除的注册条目，页面仍可能显示“无档案”。没有画像不等于该身份不成立，但恢复注册引用也不能解决画像缺失。暂缓85条不是确认正确，不宜纳入自动保留白名单。

## 核查方法和边界

逐条读取原始引用位置、整条任职/关系描述、原画像、新画像及其注册记录；以actual basic_info为准，不以CSV展示名或ID国别前缀替代身份。关键疑难实体区别查询了官方来源，具体链接写在CSV“外部参考”列。其他行主要是本地数据一致性复核，没有声称逐条完成独立外网事实核验。每条均保留原始上下文、画像证据位置和证据范围。

491/491条当前ID与原清单“新ID”一致，引用名称和数组位置重新校验通过。所读取675个画像/注册/引用源文件SHA256与起始快照一致，两份输入CSV字节未变。该验证只覆盖相关675文件，不代表重新做了全库头像盘点；本轮程序没有任何图片写入操作。

## 主要发现

- UNICEF 18条误连吉尔吉斯斯坦办事处：建议回退13、置空1、暂缓4。原KH-INTL-006同时登记UNICEF与UNAIDS，不能回退；TH-IGO-001格式也需处理。[UNICEF国别办公室官网](https://www.unicef.org/kyrgyzstan/contact-us)。
- RFE/RL 5条误连吉尔吉斯语部：建议回退1、置空4。原土库曼语部也不能代表集团总部。[RFE/RL官方对Azattyk的定义](https://about.rferl.org/article/central-asia-in-focus-attacks-on-rfe-rls-kyrgyz-service/)。
- 第69条日本Tokai University误连台湾Tunghai；第82条利比亚宰图纳大学误连突尼斯同名大学。两条不在54个机器优先项中。[日本校方任职报道](https://www.u-tokai.ac.jp/news-campus/192891/)、[利比亚校方介绍](https://azu.edu.ly/ar)。
- 第193—194条BNZ误连Kiwibank，证明同国也可错；第178—182条涉及阿曼Ahli与利比亚Aman、约旦Arab Bank与巴林Bank ABC混淆。[BNZ官方](https://www.bnz.co.nz/about-us)、[阿曼央行银行名录](https://cbo.gov.om/Pages/LicensedBanks.aspx)、[Bank ABC官方身份](https://www.bank-abc.com/en/AboutABC/Pages/Fact-Sheet.aspx)。
- 第258条Cisco→独联体，第410—416条中的6条摩洛哥Al Mada控股→伊拉克媒体，第421条China Bank Savings→美国CBS电视网，第425—428条Vanguard投资→尼日利亚报纸，均非名称变体。[Al Mada官方投资业务](https://www.almada.ma/fr/strategie-dinvestissement)、[China Bank Savings官方](https://www.cbs.com.ph/About_Us.aspx)。
- 第408条黎巴嫩社会进步党机关报Al-Anbaa→科威特同名报纸，机器列在较低优先级；原注册项可恢复。[黎巴嫩党报官方介绍](https://anbaaonline.com/about)。
- UNESCO的27条链接可保留：目标主名、QID、官网指向全球UNESCO，并非玻利维亚办事处，但目标画像把总部国别写成BOL，是另一个数据错误。不能因错误国别字段再拆出一个假身份。[UNESCO总部地址](https://www.unesco.org/en/about-us/practical-info?hub=149803)。
- 世界银行74条中，明确写World Bank Group的13条保留，其余61条暂缓（其中4条是多个机构混在一条任职中）。World Bank与World Bank Group需先确定是否允许集团聚合口径，不将这61条报成已证实错链。[世行官方机构区分](https://www.worldbank.org/lo/about)。

## 暂缓项需要的决策

1. 是否允许World Bank→World Bank Group、银行法人→控股公司、历史前身→现集团这类聚合映射；建议精确身份与集团关系分开。
2. 同名但原ID误分GOV、旧ID碰撞、被排除条目，先整理注册表再分配有效身份，不直接恢复。
3. 多机构合并的一条任职（例如世界银行/财政部/麦肯锡、NZX/ASX、四家菲律宾协会），需要拆条；不是用一个新ID覆盖整行。

## 后续建议（尚未执行）

先讨论19条置空及第32条有画像回退；38条无画像注册回退另为一组，明确会继续显示无档案及后续去重责任。85条暂缓待粒度规则和注册表身份厘清。执行时必须重新检查引用文字、当前ID与数组位置，并为变更建立undo日志；不要直接把助手复核CSV接入现有执行器。机器优先54条之外还有27条建议置空/回退，不能只处理54条。

## 交付文件

- `output/_id_audit/step1b_cross_public_priority_reviewed.csv`：优先100条，助手已填结论及理由。
- `output/_id_audit/step1b_cross_public_review_reviewed.csv`：全量491条，复核序号对应原全量文件数据行，不含表头。
- `output/_id_audit/cross_public_491_review_decisions.json`：逐条建议，review_only=true、execution_authorized=false。
- `output/_id_audit/cross_public_491_review_summary.json`：统计、原CSV哈希、未修改验证结果。
- `output/_id_audit/cross_public_491_context.json` / `cross_public_491_read_manifest.json`：证据快照与675文件哈希。

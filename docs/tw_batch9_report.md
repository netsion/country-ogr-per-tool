# 台湾地区第九批15人研究（2026-11-17至2026-11-20）

已执行15/15。完成指公开资料研究、写入和校验结束，不等同所有事实多源核验或完整度达到85分。各档采集日期及跨日补核说明见collection_meta。

|人物|ID|政策|成就|人物关系|家庭|来源链接|完整度|
|---|---|---:|---:|---:|---:|---:|---:|
|柯文哲|[TW-PERSON-000042](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000042.json)|3|2|1|1|10|74|
|范云|[TW-PERSON-000515](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000515.json)|4|2|1|0|9|83|
|苗博雅|[TW-PERSON-000516](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000516.json)|3|2|2|1|11|79|
|王婉谕|[TW-PERSON-000509](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000509.json)|3|2|1|1|12|77|
|王金平|[TW-PERSON-000027](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000027.json)|3|1|1|1|10|73|
|洪秀柱|[TW-PERSON-000145](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000145.json)|3|2|2|0|9|78|
|郝龙斌|[TW-PERSON-000082](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000082.json)|3|2|1|1|8|70|
|吴志扬|[TW-PERSON-000154](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000154.json)|3|2|1|1|6|72|
|苏嘉全|[TW-PERSON-000019](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000019.json)|3|2|1|2|11|74|
|谢长廷|[TW-PERSON-000021](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000021.json)|3|2|1|2|8|72|
|蔡壁如|[TW-PERSON-000044](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000044.json)|3|2|1|0|10|72|
|王兴焕|[TW-PERSON-000518](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000518.json)|3|0|1|0|7|44|
|陈明文|[TW-PERSON-000197](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000197.json)|3|0|1|1|7|64|
|李大维|[TW-PERSON-000209](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000209.json)|3|1|1|0|7|65|
|陈冲|[TW-PERSON-000125](D:/ai-workspace/apec-osint-tool/output/tw/2026-07-27/persons/TW-PERSON-000125.json)|3|1|0|1|7|60|

仅记录可追溯公开事实；空字段及单源、不可读来源、现职截止时间逐档记录。成就区分团队贡献、计划与已实施成果；家庭仅公开实名与必要关系，不采私人财产或地址。所有原头像字段、画像ID和平台user_id保留。

本轮15份真实JSON Schema均通过，严格工具结果及已知限制见下文；警告详情见复核记录。非本轮人物及组织画像与基线快照保持一致。未执行全库自动补链。71个非空引用目标已逐条核对身份，原文来源见各档collection_meta.quotes。

备份与校验：tmp/tw_batch9_20261117/；候选依据：同目录selection.json。

本批合计政策主张46条、成就23条、人物关系16条、公开家庭关系12条。
本批重采既有15份人物画像，未分配新ID、未新建画像；原有头像字段完整保留。
来源列是链接数量，不等同独立来源数量；同源转载不重复算独立核实。未知关系ID保持null，未按姓名自动补链。
本批严格检查中文姓名提示详见strict_validation.json；不修改正确中文姓名。完整度是字段覆盖指标，尚有缺项及单源边界，不等同全部事实已核实。

严格工具有1份档案仅因未核英文名留空而报必填错误；真实JSON Schema允许空字符串，已逐档注明证据限制，未编造译名。除此之外严格工具错误为0；逐项输出保留在strict_validation.json。
完整度范围为44—83分；未以猜测补足85分目标。部分政策、成果、家庭及人物关系仍有缺项。

收尾：本批仅重采既有15份人物画像，未新建身份、未分配ID，底库仍为598份；九批累计深度研究130位不同人物。71个非空引用已核对，补齐59处本批组织空引用。姓名索引无冲突。

本批社交账号共40个，原有28条账号完整保留，原有15份头像引用保持不变。原始社交.xlsx校验值未变；账号表关联与实时官方认证分开说明，USER/PAGE字段分列。现职与历史职务按近期证据重建，不沿用旧库过时头衔。

本轮明确保留的证据限制：

- 王婉谕Facebook旧user_id为fb#RHINO#102002721267282，与用户表PAGE-ID相同；表列USER-ID为100047358551344。本轮保护既有非空值，未覆盖，原档source_note及social_id_supplement.json记录待专门复核。账号URL/ID跨人物冲突检查为0，不代表这项字段语义差异已解决。
- 柯文哲保留原X账号及表内新增X账号，两账号当前归属未独立确认；表关联与实时平台认证分开说明。
- 王兴焕主要学历、职业与成果证据仍较少，未将四党合作宣布作为政策实施成果；陈明文三条政策来自2009年广告企划专访，只作历史本人主张，非当前政策或独立效果评估。两人主要成就字段保持空。李大维、陈冲各一项成果，未凑足目标数量。
- 本轮跨日继续研究：前11份采集日11月17日，剩余4份11月20日；实际近期活动及现职证据分别截止各档注明日期，不声称均已核至11月20日当天。被引用旧画像仅核对身份，未全量刷新其职务。

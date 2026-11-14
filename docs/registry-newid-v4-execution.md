# 第二批 80 条：修复与执行记录（v4）

日期：2026-11-13

## 一、先修的两处回归遗漏

### 1. 编号保留集合纳入“业务引用已用 ID”

原分配器只查 registry/画像/name_index，漏掉了“未注册但已被引用字段使用”的 ID。本批 3 个候选号即属于此类：

| 候选号 | 被引用写成的主体 |
|---|---|
| KR-ACAD-028 | Korea Institute for National Unification |
| KR-CORP-035 | POSCO E&C / Korail Retail |
| KR-CORP-036 | POSCO DX / Korail Logis |

v4 的 `ever_used` 现在包含：

- registry active/deprecated
- 画像文件 ID
- `_name_index` 中的 ID
- **所有人物/组织引用字段里的非空 org_id/person_id**（work_experience、related_entities、key_people、person_relationships、family_members、org_ids）

这 3 个号未被重新分配；本批对应行均挂起。

### 2. same_identity 合并闭合性

上轮 7 条 same_identity 中 4 条目标未建立：

| 源 ID | 目标（不存在） | 处理 |
|---|---|---|
| KR-CORP-030 Amorepacific | KR-CORP-036 | 恢复为活动注册项 |
| KR-GOV-157 新千年民主党 | KR-GOV-1249 | 恢复为活动注册项 |
| KR-GOV-305 仁川地方检察厅 | KR-GOV-1253 | 恢复为活动注册项 |
| KR-GOV-208 大邱地方法院 | KR-GOV-1254 | 恢复为活动注册项 |

4 条源项已从 `deprecated_registry` 移回 `registry`，`status=auto_registered`，移除 `merged_into`；不再出现“源已归档、目标不存在”的断链。

回滚：`output/_id_audit/merge_closure_repair_undo.json`

## 二、本批复核结论

| 意见 | 数量 | 执行 |
|---|---:|---|
| 可分配独立身份 | 25 | 已执行 |
| 改类别后分配 | 2 | 已执行（NZIST→ACAD、Sony Financial→FIN） |
| 不按原方案分配 | 25 | 未执行 |
| 挂起 | 28 | 未执行 |

人物被当作组织的 4 条（Rosaura Ruiz、Fernández Carbajal、Claudio X. González、Pablo González）均在“不分配”，未新建组织；需另走人物/关系修复。

考试资格、职位、机构集合等（国会议员辅佐官室、行政高等考试、Surveyor-General、CDEM Groups）也未分配。

## 三、v4 执行结果

- 新建 registry 身份：**27 个**
- 引用改到新 ID：**25 个位置 / 18 个文件**
- 历史编号/业务引用号重用：**0**
- 头像变更：**0**（9,001 person + 3,965 org）
- 回滚：`output/_id_audit/registry_newid_v4_undo.json`
- 汇总：`output/_id_audit/registry_newid_v4_summary.json`

### 新 ID（27）

| 国家 | 新 ID |
|---|---|
| KR | KR-GOV-1163（大邱庆北经济自由区域厅）、KR-GOV-1164（阴城郡） |
| MX | MX-CORP-094（Telcel）、MX-CORP-095（Solistica）、MX-CORP-096（Ferromex） |
| NZ | NZ-GOV-153~161（广播标准局、海外投资办公室、生产力委员会、消防服务局、农村消防管理局、体育诚信委员会、大学入学委员会、法律委员会、移民局）、NZ-ACAD-020（NZIST） |
| JP | JP-ACAD-040~044（RIETI、国立环境研究所、大阪公立大学、岐阜大学、九州工业大学）、JP-CORP-203~208（日野、丰田通商、丰田自动织机、捷太格特、索尼半导体、KADOKAWA）、JP-FIN-052（索尼金融集团） |

## 四、当前剩余

- `pending_review`：约 **826** 条
- `defer`：42 条（14 原 + 28 本批）
- `no_assign`：30 条（5 原 + 25 本批）
- 已建新身份但无画像：**88 个 / 265 条引用**
  - 清单：`output/_id_audit/newid_profile_backlog.csv`

## 五、审计变化（v4 执行前后）

| 指标 | 前 | 后 |
|---|---:|---:|
| related_org 指向错误 | 2,257 | 2,232 |
| work_org 指向错误 | 8,744 | 8,744 |
| person_rel 指向错误 | 2,801 | 2,801 |
| key_people 指向错误 | 298 | 298 |

v4 的 25 条改动全在 `related_entities`，因此只改善 related_org；新增悬空为预期“新身份暂无画像”。

**未执行：826 条 pending、42 条 defer、30 条 no_assign。**

## 六、剩余 826 条一次性复核包

已生成：

- Excel：`output/_id_audit/registry_newid_pending826_review.xlsx`
  - `全部826`：全部待复核行，带筛选/冻结表头
  - `P1优先`：190 条高优先项
  - `按国家统计`
  - `说明`
- CSV：`output/_id_audit/registry_newid_pending826_review.csv`
- P1 CSV：`output/_id_audit/registry_newid_pending826_priority.csv`

分层：

| 优先级 | 行数 | 含义 |
|---|---:|---|
| P1 | 190 | 引用≥3，或含他国名/已有画像候选/疑似非独立组织 |
| P2 | 183 | 有引用、低风险 |
| P3 | 453 | 无引用，可延后 |

- 826 行候选新 ID 已按“全部历史编号 + 业务引用 ID”重新分配；0 重复；`KR-ACAD-028`、`KR-CORP-035`、`KR-CORP-036` 未再使用。
- 610 行当前无引用；216 行有引用。
- 复核列：`复核结论` 填 `分配` / `改类别后分配` / `不分配` / `挂起`；`建议类别`、`建议国别` 仅在改类别/国别时填。

**本轮未执行任何新 ID 分配或引用修改。**

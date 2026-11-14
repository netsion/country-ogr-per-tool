# 826 条复核执行记录（v5）

日期：2026-11-13

## 一、复核结论

| 结论 | 数量 |
|---|---:|
| 建议分配 | 188 |
| 调整类别/国别后分配 | 144 |
| 不再新建 | 194 |
| 挂起待核 | 300 |

执行拆分：

- 同国分配：297
- 跨国且目标国有数据集：18
- 跨国但目标国未采集：17 → `defer_no_dataset`
- 不再新建：194 → 未执行
- 挂起：300 → 未执行

## 二、执行结果

| 项目 | 数量 |
|---|---:|
| 新建 registry 身份 | **315** |
| 引用改到新 ID | **140 个位置 / 99 个文件** |
| 涉及 registry 文件 | 11 个国家 |
| 历史/业务引用号重用 | 0 |
| 头像变更 | 0（9,001 person + 3,965 org） |

- 同国新身份写入源国家 registry。
- 18 条跨国新身份写入目标国家 registry（US/AU/MY/VN/ID/JP）。
- 17 条目标国未采集（DE/GB/CH/IN/IE/AR/IT）保持 `defer_no_dataset`。
- 旧 collision ID 的 owner 条目保留；影子条目从源 registry 移除。
- 回滚：`output/_id_audit/registry_newid_v5_undo.json`
- 汇总：`output/_id_audit/registry_newid_v5_summary.json`

## 三、审计变化

| 指标 | 前 | 后 |
|---|---:|---:|
| work_org 指向错误 | 8,744 | 8,703 |
| related_org 指向错误 | 2,232 | 2,133 |
| person_rel 指向错误 | 2,801 | 2,801 |
| key_people 指向错误 | 298 | 298 |

新增悬空是 315 个新身份暂无画像的预期结果。

## 四、新身份补画像

累计已建但无画像的新身份：**403 个 / 405 条引用**
清单：`output/_id_audit/newid_profile_backlog.csv`

## 五、剩余

- 300 条挂起（含 141 条人物姓名混入组织候选、19 组疑似重复身份、越南履历混杂等）
- 194 条不再新建
- 17 条跨国目标国未采集
- 403 个新身份待补画像

**本轮未处理挂起/不再新建项。**

## 六、专项清单（141 人物 + 19 重复身份）

已生成：

- `output/_id_audit/registry826_special_lists.xlsx`
  - `人物姓名141`
  - `重复身份19组`
  - `说明`
- `output/_id_audit/registry826_person_names_141.csv`
- `output/_id_audit/registry826_duplicate_identities_19.csv`
- `output/_id_audit/registry826_special_lists_summary.json`

### 人物姓名 141

- 全部为 `不分配`，不建组织 ID。
- 138 条理由为“自然人姓名被放入组织注册候选”，3 条为“自然人而非组织”。
- 136 条给出了人物候选 ID；5 条未给候选，需人工确认人物。
- 建议动作：按人物候选消歧/合并，或补人物档案；禁止把 PERSON ID 写进 org_id。

### 重复身份 19 组

- 19 组 / 40 条，均为 `挂起`。
- 典型：驻英国/驻美国韩国大使馆、UNDP、部分日本机构等。
- 建议动作：先统一规范名称/实体层级，确定单一主身份；本组不分配新 ID，也不把引用并入未落库候选号。
- 每组已列 `组内主身份候选（参考）`，仅为候选，不是执行授权。

**本步未分配 ID、未改引用、未合并画像。**

## 七、141 条人物姓名消歧清单

产物：

- `output/_id_audit/registry826_person_disambiguation.xlsx`
  - `汇总`、`141人物`、`候选人`、`引用明细`、`重复人物档案`
- `output/_id_audit/registry826_person_disambiguation_141.csv`
- `output/_id_audit/registry826_person_candidates.csv`
- `output/_id_audit/registry826_person_refs.csv`

结论：

- 141 条中 **139 条当前无业务引用**：只需从组织 registry 归档人物影条目，不建组织/人物 ID。
- **1 条组织字段误填人名**（第 22 行 Rosa Icela Rodríguez）：`organization` 改为“内政部 (Secretaría de Gobernación)”，保留 `org_id=MX-GOV-007`。
- **1 条人物字段误指组织**（第 135 行 Juan Pardinas）：`person_id` 改为 `MX-PERSON-000199`。
- 候选状态：132 条单候选、4 条重复人物档案、5 条无候选。
- 4 组重复人物档案：Rosa Icela（154/162）、Rosaura Ruiz（102/114）、Arturo Gutiérrez（126/171）、Ana Botín（142/685）。
- 5 条无候选：José Antonio Fernández、Gabriel Cuadra、Alejandro Domínguez、Rosa Beltrán Álvarez、David Garza Salazar。

**本步只出清单，未修改 registry、引用、画像或头像。**

## 八、141 条人物姓名清理执行记录

| 动作 | 数量 |
|---|---:|
| 从 MX org registry 归档人物影条目 | **139** |
| 修正 organization 文本（保留 org_id） | **1** |
| person_id 由组织改为人物 | **1** |
| 引用修改 | **2 个位置** |
| 头像变更 | **0**（9,001 person + 3,965 org） |

- 第 22 行：`MX-PERSON-000162.json#work_experience[0].organization`
  `罗莎·伊塞拉·罗德里格斯 (...)` → `内政部 (Secretaría de Gobernación)`，`org_id=MX-GOV-007` 保留。
- 第 135 行：`MX-PERSON-000198.json#person_relationships[2].person_id`
  `MX-MEDIA-005（改革报）` → `MX-PERSON-000199`。
- 139 条人物影条目归档为 `not_an_org`，不再占用组织 registry。
- 未处理：4 组重复人物档案（154/162、102/114、126/171、142/685）和 5 条无候选人物；留待人物档案合并。
- 回滚：`output/_id_audit/registry826_person_fix_undo.json`
- 汇总：`output/_id_audit/registry826_person_fix_summary.json`

审计变化：

| 指标 | 前 | 后 |
|---|---:|---:|
| work_org 指向错误 | 8,703 | 8,702 |
| person_rel 指向错误 | 2,801 | 2,801（ok +1、dangling -1） |
| related_org 指向错误 | 2,133 | 2,133 |

**未执行人物档案合并。**

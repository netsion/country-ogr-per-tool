# P2 批次 4–5：跨类型 / 占位符 / 自指引用清理（2026-11-13）

## 批次 4：跨类型 ID 置空

person ID 不能作为 org_id，org ID 不能作为 person_id。这类引用在 schema 上必然无效。

共置空 **459 条**：

| 数组 | 数量 | 说明 |
|---|---:|---|
| work_experience | 342 | org_id 是 person ID |
| person_relationships | 92 | person_id 是 org ID |
| related_entities | 25 | org_id 是 person ID |

保留组织/人物名称和描述文字，只把错误的 ID 字段置为 null。

## 批次 5：占位符 / 自指引用

共置空 **287 条**：

| 原因 | 数量 | 数组 |
|---|---:|---|
| 占位符 ID（UNKNOWN/REL-/EXT-/000000 等） | 222 | person_relationships 150、family_members 69、related_entities 3 |
| 自指（person_id 等于本人） | 65 | person_relationships 53、family_members 12 |

## 审计变化

| 指标 | 批次 3 后 | 批次 5 后 |
|---|---:|---:|
| work_org dangling | 6,885 | 6,543 |
| work_org null_id | 54,449 | 54,791 |
| person_rel dangling | 6,972 | 6,730 |
| person_rel null_id | 10,623 | 10,918 |
| family dangling | 280 | 211 |
| family null_id | 16,148 | 16,229 |
| related_org dangling | 5,840 | 5,812 |
| related_org null_id | 6,677 | 6,705 |

- 跨类型 459 条全部从 dangling 中移除；
- 占位符/自指 287 条按预期转为 null_id；
- 没有改任何画像 ID、registry 或头像。

## 没有动的项

### 473 条 related_entities 自指

这些不是简单自指：很多是同一 ID 下的父子/关联实体（例如母公司 ID 下挂着子公司名称），当前 ID 指错但目标实体可能值得单独建 ID。直接置空会丢失关系，留待后续“拆分子实体/补 ID”批次。

### 201 条非空、非法格式、且全库无画像/注册的 ID

例如 `MY-POL-UMNO`、`MY-PERSON-FAM-0001`、`KR-None-003`。这些 ID 当前无法解析，但可能是历史临时 ID；不在本批盲置空。清单已用于下一批复核。

## 产物

- 撤销日志：`output/_id_audit/p2_batch4_crosstype_undo.json`
- 撤销日志：`output/_id_audit/p2_batch5_placeholder_undo.json`
- 脚本：`scripts_tmp/p2_batch4_crosstype_null.py`
- 脚本：`scripts_tmp/p2_batch5_placeholder_null.py`

## P2 当前进度

- 已修正引用：315 条 relink + 459 条跨类型置空 + 287 条占位符/自指置空 = **1,061 条**
- 剩余主要工作：
  - 201 条非法格式/无解析 ID 复核；
  - 473 条 related_entities 自指/碰撞关系；
  - person_relationships / key_people / family_members 的错链；
  - 大量 `null_id` 的目标缺失引用（需抽样复核后决定是否置空）；
  - 385 个补画像项继续后置。

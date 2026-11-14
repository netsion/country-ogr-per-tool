# 826 复核：剩余组织挂起项清理记录

日期：2026-11-13

## 范围

826 条复核中的 300 条 `挂起`：

- 其中 40 条属于 19 组重复身份，已在 `registry826-duplicate-org-groups.md` 处理；WHO 2 条已由全球归一处理。
- 实际本轮处理剩余 **260 条**（300 条中 49 条已在其他操作中移除，故 registry 中只找到 251 条）。
- 处理方式：**不新建任何组织 ID**，把影子注册项归档为 `unresolved_shadow`；有引用的把错误 `org_id` 置空，文字履历保留。

## 结果

| 项目 | 数量 |
|---|---:|
| 挂起行 | 300 |
| registry 中实际归档影子条目 | **251** |
| 已在其他操作中移除/已解决 | **49** |
| 有引用并被置空 | **127 个引用位置** |
| 新建组织 ID | **0** |
| 画像修改 | **0** |
| 头像变更 | **0**（9,000 person + 3,965 org） |

- 251 条影子移入 `deprecated_registry`，`status=unresolved_shadow`，原因写 `826 defer: unresolved entity granularity`。
- 127 条引用仅把 `org_id` 置空，`organization`/`description`/日期/来源全部保留。
- 49 条未找到：均已在此前 19 组重复身份、WHO/UNDP 归一或前序操作中移除，不是丢失。

## 审计变化

| 指标 | 前 | 后 |
|---|---:|---:|
| work_org 指向错误 | 8,701 | **8,646** |
| work_org 空 ID | 54,391 | **54,450** |
| work_org 悬空 | 6,997 | **6,993** |
| related_org 指向错误 | 2,129 | **2,067** |
| related_org 空 ID | 6,613 | **6,681** |
| related_org 悬空 | 5,930 | **5,924** |

- 减少的“指向错误”= 127 条被置空引用中，原本落在 owner 画像上的部分。
- 新增空 ID = 127 条；不是删除履历。

## 回滚

- `output/_id_audit/archive_deferred_shadows_undo.json`
- 汇总：`output/_id_audit/archive_deferred_shadows_summary.json`

## 备注

- `unresolved_shadow` 条目不再进入活动 registry/name_index；以后有证据可重新建档。
- 这批没有做“实体粒度决策”，只是解除错误链接、保留待核身份。
- 剩余事项：5 条无人物候选、403 个新身份待补画像、WHO/UNDP 国别办事处是否补画像。

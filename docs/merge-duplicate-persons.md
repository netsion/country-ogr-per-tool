# 4 组重复人物档案合并记录

日期：2026-11-13

## 合并对

| 主档案（保留） | 重复档案（归档） | 主要合并内容 | 引用改链 |
|---|---|---|---:|
| MX-PERSON-000154 Rosa Icela Rodríguez | MX-PERSON-000162 | 无数组合并（162 仅为 stub） | 1 |
| MX-PERSON-000102 Rosaura Ruiz Gutiérrez | MX-PERSON-000114 | 别名“罗绍拉·鲁伊斯·古铁雷斯” | 1 |
| MX-PERSON-000126 Arturo Gutiérrez Hernández | PE-PERSON-000171 | 传记、别名、5 个职位、9 段任职、1 条教育、4 条关系、4 项成就、4 条政治立场 | 3 |
| MX-PERSON-000142 Ana Botín | US-PERSON-000685 | 别名、3 个职位、1 个联系方式、12 段任职、2 条教育、4 条关系、2 名家属、3 个社交账号、9 项成就、1 条政治立场 | 0 |

- 引用改链合计 **5 个位置**；重复 ID 残留引用 **0**。
- 4 个重复档案文件已移到 `output/_id_audit/merged_person_profiles/`，未删除。
- 4 条 person_registry 条目标 `merged` + `merged_into`，移入 deprecated。
- 2 条 person index 条目移除（另 2 个重复档案原本未进 index）。
- 回滚：`output/_id_audit/merge_duplicate_persons_undo.json`

## 合并后校验

| 主档案 | strict 结果 |
|---|---|
| MX-PERSON-000154 | 0 error / 1 warning（education[1].institution 为空，既存） |
| MX-PERSON-000102 | 0 error / 0 warning（顺手清掉 education 的 `org_id` 额外字段和 1 条自指关系） |
| MX-PERSON-000126 | 0 error / 1 warning（work[4] 组织名无中文，品牌豁免） |
| MX-PERSON-000142 | 0 error / 0 warning |

## 头像

- person 头像画像：9,001 → **9,000**（US-PERSON-000685 重复档案移除）
- org 头像：3,965 不变
- `minio-store/default/popular-person-profile/us/US-PERSON-000685.jpg` 保留为孤儿文件，未删除
- 所有保留画像的 `local_path` 文件名与 person_id 仍 100% 一致

## 审计变化

| 指标 | 前 | 后 |
|---|---:|---:|
| work_org 指向错误 | 8,702 | 8,701 |
| person_rel 指向错误 | 2,801 | 2,801（null +1，ok 不变） |
| related_org 指向错误 | 2,133 | 2,133 |

## 未处理

- 5 条无人物候选：José Antonio Fernández、Gabriel Cuadra、Alejandro Domínguez、Rosa Beltrán Álvarez、David Garza Salazar
- 19 组重复组织身份（40 条挂起）
- 其余约 260 条组织挂起项

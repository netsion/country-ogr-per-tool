# P2 批次 6：空值/非法格式 ID 清理（2026-11-13）

## 范围

只处理“字段有值，但既不是合法 org/person ID 格式、也不在任何数据集 registry/profile 中”的引用：

- 空字符串 `""`
- 自定义临时格式，如 `MY-POL-UMNO`、`MY-PERSON-FAM-0001`
- 全库无画像、无注册、无法解析的 ID

合法格式但悬空的 ID **不处理**，避免误删未来可能补建的实体。

## 执行结果

共置空 **201 条**：

| 原因 | 数量 |
|---|---:|
| 空字符串 | 122 |
| 非法格式且全库无解析 | 79 |

按数组：

| 数组 | 数量 |
|---|---:|
| person_relationships | 92 |
| family_members | 68 |
| related_entities | 21 |
| work_experience | 20 |

## 审计变化

| 指标 | 批次 5 后 | 批次 6 后 |
|---|---:|---:|
| work_org dangling | 6,543 | 6,523 |
| person_rel dangling | 6,730 | 6,709 |
| family dangling | 211 | 194 |
| related_org dangling | 5,812 | 5,791 |

`ok` 数量未减少；只把无法解析的字符串 ID 置空，名称与描述保留。

## 为什么没有继续按“低相似度”批量置空

抽样发现低相似度不等于错链，跨语言名称会出现 0 相似但实际同名：

- `Baku Stock Exchange` vs `巴库证券交易所`
- `Turkic Culture and Heritage Foundation` vs `突厥文化遗存基金会`
- `Union of Artists of Azerbaijan` vs `阿塞拜疆艺术家联合会`
- `Azerbaijan International Operating Company` vs `阿塞拜疆国际作业公司`

如果按字符串相似度批量置空，会把正确的中英文同名引用误删。剩余 `wrong_target` 必须做双语/上下文复核，不能机械阈值处理。

## 产物

- 撤销日志：`output/_id_audit/p2_batch6_invalid_ids_undo.json`
- 脚本：`scripts_tmp/p2_batch6_invalid_ids.py`

## P2 当前进度

- relink：315 条
- 跨类型置空：459 条
- 占位符/自指置空：287 条
- 空值/非法格式置空：201 条
- **合计：1,262 条**

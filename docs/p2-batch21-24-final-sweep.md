# P2 收尾批次 21–24：全自动长尾清理（2026-11-14）

## 方法

大簇清完后，剩余错误引用呈长尾分布（多为 1–4 条的小簇）。改为按"审计匹配器 + 严格名称匹配"全自动处理：

- 当前画像/注册名的正式名称、别名、历史名命中的引用**自动保留**（覆盖改名、双语、转写、历史名称假阳性）；
- 其余引用置空，名称与描述保留；
- GN/NG 全程豁免。

每一步先 dry-run + 抽样人工审核，再执行。

## 批次 21：person_relationships 收尾

- 先前批次处理后的剩余 1,464 条按同规则置空
- 抽样 60 条逐条确认均为"同姓/同名不同人"
- 另逐条处理 32 条 leftovers：
  - 26 条为跨文字转写（阿拉伯语/西里尔/繁简/中文异译，正确）→ 保留
  - 6 条明确错配（NZ David Carter→Richard Gordon、PH Consunji→Victor Lee、TJ 2 条、VN 2 条波兰人）→ 置空
- `person_rel wrong`：1,469 → **5**（其余为 GN/NG）

## 批次 22：related_entities 全量

- 1,308 条按匹配器自动置空
- 抽样 80 条确认：三星物产→KR-CORP-014、阿贡实验室→US-GOV-001、北京大学→US-ACAD-004 等均为真错配
- `related_org wrong`：1,447 → **139**（其余为 GN/NG）

## 批次 23：work_experience 全量

- 5,930 条按匹配器自动置空
- 抽样 100 条确认：乐天移动、首尔中央地方法院、财务省主计局、产业通商资源部等均为真错配
- `work_org wrong`：5,974 → **44**（其余为 GN/NG）

## 最终审计（GN/NG 豁免口径）

| 方向 | ok | wrong | dangling | null_id |
|---|---:|---:|---:|---:|
| work_org | 60,231 | **44*** | 6,530 | 62,752 |
| person_rel | 32,586 | **5*** | 6,721 | 13,763 |
| family | 1,661 | **0** | 197 | 16,297 |
| key_people | 17,996 | **12**（转写变体） | 4,765 | 2,669 |
| related_org | 18,298 | **139*** | 5,789 | 8,634 |

\* 复核确认：非 GN/NG 数据集中 `work wrong` 实际为 **0**、`related wrong` 实际为 **0**；审计残留计数全部来自 GN/NG（34 条 work 已确认）与 `registry_wrong_name`（注册名≠引用名的转写别名，属正确引用）。

## P2 全程累计

| 类型 | 数量 |
|---|---:|
| relink | 441 |
| 结构置空（跨类型/占位符/非法格式） | 947 |
| 空 ID 补已有画像 | 418 |
| 碰撞影子置空 | 226 |
| 复核样本置空 | 273 |
| 簇置空（人工） | 2,851 |
| key_people 置空 | 191 |
| person 簇置空（人工） | 955 |
| person_rel 全自动置空 | 1,464 + 6 |
| related_org 全自动置空 | 1,308 |
| work_org 全自动置空 | 5,930 |
| **合计** | **≈ 15,010** |

## 产物

- `output/_id_audit/p2_auto_person_apply.json` / `p2_auto_related_apply.json` / `p2_auto_work_apply.json`（含逐条变更）
- `output/_id_audit/p2_batch21_person_leftovers_undo.json`
- 脚本：`scripts_tmp/p2_auto_person_clusters.py`、`p2_auto_related_clusters.py`、`p2_auto_work_clusters.py`

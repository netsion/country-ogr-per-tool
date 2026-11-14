# P1 低风险元数据清理（2026-11-13）

## 范围

本轮只做低风险元数据修复，不改业务引用、不改画像 ID、不动头像：

1. org/person `_index.json` 同步
2. 清理 registry 中 `None (Actual Name)` 形式的名字污染
3. 补齐 6 个完全没有名称的 org 画像
4. 生成重复 Wikidata QID 复核清单（不自动改 QID）
5. 重建受影响数据集的 `_name_index.json`

## 1. 索引同步

| 动作 | 数量 | 明细 |
|---|---:|---|
| 新增索引条目 | 135 | ID org 103；MO person 26；TW person 6 |
| 删除失效索引条目 | 9 | MO org 3；MO person 6（均已 merged，目标文件不存在） |
| 修正索引显示名 | 8 | DZ/LA/TN 的 `None (None)`、KG 的 ` ()`、NG 的 `None (...)` 等 |
| 修正 `total_profiles` | 33 | 主要是 person index 缺该字段或数值不一致 |

修复后全量审计：

```text
person_missing_file: 0
person_id_mismatch: 0
persons_not_in_index: 0
org_missing_file: 0
org_name_mismatch: 0
orgs_not_in_index: 0
```

## 2. Registry 名字污染

清理了 **121 条** active registry 中的 `None (Actual Name)`：

```text
None (Gilan Holding)          -> Gilan Holding
None (Lao-Viet Bank)          -> Lao-Viet Bank
None (Carthage Power Company) -> Carthage Power Company
...
```

涉及 26 个最新数据集。ID、status、引用均未改变。

## 3. 6 个无名称画像

这些画像的 `basic_info` 三个名称字段全为空，已补：

| ID | name_original / name_en | name_zh |
|---|---|---|
| DZ-NGO-005 | Rassemblement Actions Jeunesse | 青年行动集会 |
| LA-FIN-006 | Lao-Viet Bank | 老越银行 |
| TN-CORP-006 | Carthage Power Company | 迦太基电力公司 |
| TN-FIN-017 | Banque tuniso-libyenne | 突尼斯-利比亚银行 |
| TN-SOE-005 | Tunisian Chemical Group (GCT) | 突尼斯化学集团 |
| TN-SOE-017 | National Real Estate Company of Tunisia (SNIT) | 突尼斯国家房地产公司 |

同时补齐 `collection_meta.quotes: []`。6 个画像 `--strict` 校验均为 **0 errors / 0 warnings**。

## 4. 重复 Wikidata QID

本轮**没有自动修改任何 QID**，只生成复核清单：

- `output/_id_audit/p1_qid_review.csv`
- 84 组：person 71、org 13
- 53 组是**同名重复档案**（同一人物/组织在多个国家数据集中各有一份画像），不是 QID 错误；后续应做档案合并，而不是清 QID
- 31 组是不同名称/变体，需要人工复核

典型需要复核的例子：

- `Q57643` 同时挂在 Thomas Sankara、约旦国王侯赛因、洪森、韩桑林、Keiko Fujimori、李显龙 6 个互不相关的人身上，明显是模板复制错误
- `Q127910` 同时挂在林冠英与阿克马沙烈
- `Q18647517` 同时挂在 Rashid Al-Maraj 与 Khalid Shawani

QID 清理涉及“哪个实体才是 QID 真正对应的对象”，不适合在 P1 盲改；留到 P2/P3 与档案合并一起做。

## 5. 名称索引

- 正确重建了 25 个最新数据集的 `_name_index.json`
- `GN/2026-11-10` 存在 `.inflight`，跳过索引重建；其 registry 名称已清理，等采集结束后再重建
- 首次批量重建时脚本把数据集目录多取了一级，生成了 26 个空的 country-level `_name_index.json`；已全部删除，并用正确日期目录重建。没有数据丢失
- 当前 53 个最新数据集的名称索引：single-character 键 0；≤3 字符键 9,571（多为合法的 3 字母缩写，未强删）

## 6. 产物

- 撤销日志：`output/_id_audit/p1_metadata_cleanup_undo.json`
- QID 复核清单：`output/_id_audit/p1_qid_review.csv`
- 名称索引修复记录：`output/_id_audit/p1_name_index_fix.json`
- 审计报告：`output/_id_audit/report_v2.json`
- 脚本：`scripts_tmp/p1_audit2.py`、`scripts_tmp/p1_apply.py`

## 7. 下一步

P1 已完成。下一步进入 **P2 全库错链清理**：

- 约 1.6 万条错误/幽灵/碰撞影子引用
- 先同国 + 主名称精确匹配
- 再做低相似错链抽样复核
- 跨国公共机构名不自动匹配

126 个 1 引用补画像项继续后置。

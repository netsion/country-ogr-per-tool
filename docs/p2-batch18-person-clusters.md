# P2 批次 18：第二批 person_relationships 错误簇（2026-11-14）

## 范围

继续处理 25 个“同姓/同名但不同人”的人物关系簇，GN/NG 豁免。

典型：

- `RU-PERSON-000400` 帕维尔·季托夫 ← 帕维尔·格拉乔夫、帕维尔·杜罗夫
- `PH-PERSON-000161` 金·德莱昂 ← Kim Jacinto-Henares、Robert Barbers
- `PH-PERSON-000186` 克里斯蒂娜·弗拉斯科 ← 其他 Garcia
- `MX-PERSON-000001` 赫尔曼·拉雷亚 ← 其他 Claudia
- `KZ-PERSON-000035` 努尔兰·别克纳扎罗夫 ← 其他努尔兰
- `RU-PERSON-000088` 尼古拉·马特维耶夫 ← 其他尼古拉

## 结果

- 保留 **52**
- 置空 **229**

## 审计变化

| 指标 | 前 | 后 |
|---|---:|---:|
| person_rel wrong | 2,036 | 1,807 |
| 错误引用合计 | 9,466 | **9,237** |

## P2 累计

| 类型 | 数量 |
|---|---:|
| relink | 441 |
| 结构置空 | 947 |
| 空 ID 补已有画像 | 418 |
| 碰撞影子置空 | 226 |
| 复核样本置空 | 273 |
| 簇置空 | 2,851 |
| key_people 置空 | 191 |
| person 簇置空 | 385 + 229 = 614 |
| **合计** | **5,961** |

## 产物

- 撤销：`output/_id_audit/p2_batch18_person_clusters_undo.json`
- 脚本：`scripts_tmp/p2_batch18_person_clusters.py`

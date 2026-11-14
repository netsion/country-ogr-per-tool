# P2 批次 19：第三批 person_relationships 错误簇（2026-11-14）

## 范围

继续处理 28 个“同姓/同名但不同人”的人物关系簇，GN/NG 豁免。

典型：

- `JO-PERSON-000007` 侯赛因·本·塔拉勒 ← 穆娜·侯赛因、侯赛因·本·阿里
- `MX-PERSON-000003` 里卡多·萨利纳斯 ← 其他里卡多
- `PH-PERSON-000205` 小罗密欧·卢马吉 ← 罗密欧·布劳纳
- `PH-PERSON-000673` 吴聪满 ← 安德鲁·戈蒂亚农
- `RU-PERSON-000158` 谢赫特尔曼 ← 其他伊戈尔
- `VN-PERSON-000041` 范世松 ← 范重交、范孝
- PH 系列大量“同姓不同人”（Tolentino、Ramos、Francisco、Aileen 等）

## 结果

- 保留 **68**
- 置空 **185**

## 审计变化

| 指标 | 前 | 后 |
|---|---:|---:|
| person_rel wrong | 1,807 | 1,623 |
| 错误引用合计 | 9,237 | **9,056** |

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
| person 簇置空 | 614 + 185 = 799 |
| **合计** | **6,146** |

## 产物

- 撤销：`output/_id_audit/p2_batch19_person_clusters_undo.json`
- 脚本：`scripts_tmp/p2_batch19_person_clusters.py`

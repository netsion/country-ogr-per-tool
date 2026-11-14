# P2 批次 8：碰撞影子引用置空（2026-11-13）

## 范围

处理 `collision_shadow` 类引用：当前 ID 同时挂着 owner 画像和另一个影子身份，引用名称匹配影子身份而不是 owner。此类引用点开一定是错的。

共置空 **226 条**：

| 方向 | 数量 |
|---|---:|
| work_org | 24 |
| related_org | 82 |
| person_rel | 105 |
| key_people | 14 |
| family | 1 |

只置空 ID，保留名称/描述。没有改画像、registry、头像。

## 典型例子

- `JP-FIN-001` owner 日本银行，引用“摩根士丹利 MUFG 证券” → 置空
- `JP-CORP-011` owner KDDI，引用“雷克萨斯” → 置空
- `KR-CORP-025` owner 三星工程，引用“现代制铁” → 置空
- `KR-GOV-014` owner 中小风险企业部，引用“产业通商资源部” → 置空

## 审计变化

| 指标 | 批次前 | 批次后 |
|---|---:|---:|
| work_org wrong | 8,378 | 8,354 |
| person_rel wrong | 2,769 | 2,664 |
| family wrong | 14 | 13 |
| key_people wrong | 298 | 287 |
| related_org wrong | 2,040 | 1,961 |

## 批次 9 试跑：没有执行

尝试把 `registry_wrong_name` 的 1,129 条也按“当前注册名不匹配”置空，但 dry-run 抽样发现大量是**同一实体的别名/翻译**，例如：

- 沙玛·本特·苏海勒·法里斯·马兹鲁伊 vs 沙玛·穆兹鲁伊（同一人）
- 阿布扎比酋长国 vs 阿布扎比政府（同一实体）
- 苏丹·本·塔赫农·阿勒纳哈扬 vs Prince Sultan bin Tahnoon Al Nahyan（同一人）
- Tod A. Laursen vs Tod Laursen（同一人）

因此批次 9 **未执行**，避免把正确别名引用误删。`registry_wrong_name` 必须做双语/上下文复核，不能按字符串直接置空。

## 产物

- 撤销日志：`output/_id_audit/p2_batch8_collision_undo.json`
- dry-run 证据：`output/_id_audit/p2_batch9_registry_mismatch_dry.json`
- 脚本：`scripts_tmp/p2_batch8_collision_null.py`、`scripts_tmp/p2_batch9_registry_mismatch.py`

## P2 累计

- relink：315
- 结构置空：947
- 空 ID 补已有画像：418
- 碰撞影子置空：226
- **合计：1,906 条**

# P2 批次 1：严格同国精确改链（2026-11-13）

## 目标

只处理 `work_experience -> org` 和 `related_entities -> org` 中最安全的一批：

- 当前 ID 指向无关画像或悬空 ID；
- 目标在同一国家、有画像；
- 引用名称与目标名称严格匹配；
- 不接受模糊相似、父子机构、跨国同名、复合任职。

## 计划

- 从 `repair_candidates.json` 中筛出 `action=replace`、`suggest_status=unique`、`scope=same_cc`
- 再用严格名称匹配复核（排除 alias，避免别名污染）：
  - 完整名称精确；
  - 中文主名精确；
  - 拉丁名精确且中文主名不冲突。
- 共 40 条候选：
  - work_org 29
  - related_org 11

逐条审核：

| 决策 | 数量 | 说明 |
|---|---:|---|
| approve | 31 | 当前 ID 明确错误或悬空，目标名称严格匹配 |
| defer | 3 | 派系名/母子机构，需人工确认 |
| reject | 6 | 跨国误配或复合任职 |

## 已执行 31 条

- work_experience：20 条
- related_entities：11 条

典型修正：

| 引用 | 原 ID | 新 ID | 说明 |
|---|---|---|---|
| 三井住友银行 | `JP-FIN-003` 三井住友金融集团 | `JP-FIN-050` 三井住友银行 | 集团 vs 银行，原链错误 |
| 世界卫生组织 | `US-INTL-004` IMF | `US-INTL-005` WHO | 原 ID 是国际货币基金组织 |
| 先锋集团 / 先锋领航 | `US-FIN-003` 美国银行 / `US-FIN-017` | `US-FIN-021` Vanguard | 原 ID 错误 |
| 工人党 | `SG-PARTY-001` 人民行动党 | `SG-PARTY-004` 新加坡工人党 | 原 ID 是执政党 |
| 马达德集团 (Al Mada) | `MA-CORP-006/090` ONA 等 | `MA-CORP-089` 马达德集团 | 统一到新主身份 |
| 联邦区立法大会/议会 | `MX-GOV-033/088/629/674` | `MX-GOV-878` 联邦区立法议会 | 历史机构同名变体 |
| 墨西哥城政府 | `MX-GOV-039` | `MX-GOV-896` 联邦区政府 | 历史机构同名变体 |
| 新西兰税务局 | `NZ-GOV-007/019` | `NZ-GOV-067` | 名称精确 |
| 商业委员会 | `NZ-GOV-018` | `NZ-GOV-152` 新西兰商务委员会 | 名称精确 |

未动任何画像、registry、头像；只改 `org_id` 字段。

## 暂缓/拒绝

### 暂缓 3 条

- `KW-PARTY-010 → KW-PARTY-007`：国家伊斯兰同盟（塔阿卢夫派）vs 国家伊斯兰同盟
- `LB-PARTY-029 → LB-PARTY-013`：复兴党黎巴嫩分支（坎索派）vs 通称分支
- `VN-GOV-079 → VN-CORP-005`：马山集团 vs Masan Rus，母子机构

### 拒绝 6 条

- `TD-GOV-008 → TD-GOV-011`：引用名称写“赤道几内亚财政与预算部”，目标是乍得财政部，跨国误配
- `VN-GOV-207 → VN-MEDIA-001`：越南通讯社 + Ha Bac 化肥公司复合引用
- `VN-CORP-007 → VN-PARTY-001`：岘港市委，不是中央党
- `VN-CORP-002 → VN-MEDIA-001`：越南通讯社 + FPT Internet Center 复合引用
- `VN-GOV-021 → VN-ACAD-005`：越南航空学院 + VIB 复合引用
- `VN-GOV-079` 另列暂缓

## 审计变化

| 指标 | 批次前 | 批次后 |
|---|---:|---:|
| work_org ok | 59,322 | 59,342 |
| work_org wrong | 8,642 | 8,634 |
| work_org dangling | 6,908 | 6,896 |
| related_org ok | 18,275 | 18,287 |
| related_org wrong | 2,054 | 2,045 |
| related_org dangling | 5,854 | 5,851 |

名称索引无需重建（只改引用 ID，不改名称/registry）。

## 产物

- 40 条决策：`output/_id_audit/p2_batch1_decisions.csv`
- 撤销日志：`output/_id_audit/p2_batch1_undo.json`
- 严格计划：`output/_id_audit/p2_strict_plan.csv`
- 100 条抽样：`output/_id_audit/p2_strict_sample.csv`

## 下一步

P2 还剩下大量 `wrong_target/dangling`，但不能再按“唯一候选”直接批量：

1. 扩展严格精确匹配到跨国的明确品牌/机构；
2. 对 `action=null_id` 的悬空/无目标引用做抽样复核，再分批置空；
3. 继续处理 person / key_people / family 方向的精确替换；
4. 385 个补画像项继续后置。

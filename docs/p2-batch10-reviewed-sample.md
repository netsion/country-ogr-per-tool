# P2 批次 10：错误引用复核样本执行（2026-11-13）

## 样本

从当前 `profile_wrong` 中抽取 173 条，逐条判断：

- 保留：同一实体改名、合并继承、双语/转写别名
- 暂缓：母子机构或语义不明确
- 置空：当前画像与引用明显无关

结果：

| 决策 | 数量 |
|---|---:|
| 保留 | 32 |
| 暂缓 | 9 |
| 置空 | 132 |

## 保留的典型

- 第一海湾银行 → 第一阿布扎比银行（合并后主体）
- 酋长铝业 EMAL → 阿联酋环球铝业 EGA（合并后主体）
- 阿联酋能源与工业部 → 能源与基础设施部（改名）
- 迪拜经济发展局 → 迪拜经济与旅游部（改名）
- 资本市场管理局 → 证券与商品管理局（职能继承）
- 巴库证券交易所 ↔ Baku Stock Exchange（双语同名）
- 阿塞拜疆总检察长办公室 ↔ 总检察院（同义）
- محمد القرغاوي ↔ محمد بن عبدالله الجرجاوي（同一人转写）
- Kate Jones ↔ Catherine Jones（同一人变体）

## 暂缓的典型

- 阿联酋总理办公室 vs 内阁事务部
- 迪拜钻石交易所 vs DMCC
- 迪拜经济发展公司/商业注册与许可公司/旅游营销公司 vs 迪拜经济与旅游部
- ADCB 埃及 vs 阿布扎比商业银行
- “Ben” vs Ben Way
- Asséto Ouédraogo vs Assétou Bado/Guire

## 置空的典型

- `AE-NGO-003` MBR 全球倡议下挂着哈利法慈善基金会、MBR 航天中心、MBR 医科大学等不同实体
- `AE-INTL-002` 国际人道城下挂 International Holding Company
- `AU-CORP-010` 澳洲航空下挂 Woodside Energy
- `AU-CORP-007` Telstra 下挂 Coles Supermarkets
- `BF-PERSON-000040` Simon Compaoré 下挂 Blaise Compaoré
- `JP-PERSON-000043` 神田真人下挂十时裕树
- 家族关系中的 Sr/Jr/世代错配

## 审计变化

| 指标 | 批次前 | 批次后 |
|---|---:|---:|
| work_org wrong | 8,354 | 8,325 |
| person_rel wrong | 2,664 | 2,631 |
| family wrong | 13 | 0 |
| key_people wrong | 287 | 250 |
| related_org wrong | 1,961 | 1,941 |

132 条置空全部消除了对应 wrong_target；没有改画像、registry、头像。

## 产物

- 决策表：`output/_id_audit/p2_wrong_review_200_decisions.csv`
- 撤销日志：`output/_id_audit/p2_batch10_review_sample_undo.json`
- 脚本：`scripts_tmp/p2_batch10_review_sample.py`

## P2 累计

| 类型 | 数量 |
|---|---:|
| relink | 315 |
| 结构置空 | 947 |
| 空 ID 补已有画像 | 418 |
| 碰撞影子置空 | 226 |
| 复核样本置空 | 132 |
| **合计** | **2,038** |

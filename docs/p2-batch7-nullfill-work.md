# P2 批次 7：空 ID 补已有画像（work_org）

## 背景

按新的验收口径：“有档案但没引用上”需要补；无画像/无注册 ID 可以接受。

本批只处理 `work_experience -> org` 中：

- `org_id` 为空；
- 引用名称能严格匹配一个**已存在画像**；
- 同国直接允许；跨国只允许 CORP/FIN/SOE/ACAD/MEDIA/NGO/INTL，并排除 GOV/MIL/PARTY 和泛化短名。

## 执行结果

- 候选 450 条
- 实际填充 **418 条**
  - 同国 30 条
  - 跨国 388 条
- 其余 32 条 person/family 候选暂缓

典型填充：

- 西太平洋银行 → `AU-FIN-002`
- 汇丰银行 → `HK-FIN-010`
- 麦肯锡公司 → `AU-GOV-075`
- 联合国教科文组织 → `BO-INTL-008`
- 日本学术振兴会 → `JP-GOV-867`
- 韩国科学技术院 → `KR-ACAD-026`
- 新西兰商务委员会 → `NZ-GOV-152`
- 世界卫生组织 → `US-INTL-005`

## 暂缓的 person/family 候选

32 条中有明显的 Sr/Jr/世代歧义，例如：

- Peter Tsiamalili **Sr** → Peter Tsiamalili **Jnr**
- Amando Tetangco **Sr** → Amando Tetangco **Jr**
- Ferdinand Marcos → Ferdinand **"Bongbong" Marcos Jr**
- Reynaldo Tamayo **Sr** → Reynaldo Sucayan Tamayo **Jr**
- John B. King **Sr** → John B. King **Jr**
- 拉希德·努尔加利耶夫（**子**）→ 拉希德·古马罗维奇·努尔加利耶夫

这类不能按名称相似直接填，留待人工/上下文复核。

## 审计变化

| 指标 | 批次前 | 批次后 |
|---|---:|---:|
| work_org ok | 59,609 | 60,027 |
| work_org null_id | 54,811 | 54,393 |
| work_org wrong | 8,378 | 8,378 |
| work_org dangling | 6,523 | 6,523 |

418 条全部进入 `ok`，没有新增错链。

## 产物

- 计划：`output/_id_audit/p2_nullfill_plan.csv`
- 抽样：`output/_id_audit/p2_nullfill_sample.csv`
- 撤销日志：`output/_id_audit/p2_batch7_nullfill_undo.json`
- 脚本：`scripts_tmp/p2_plan_nullfill.py`、`scripts_tmp/p2_batch7_nullfill_apply.py`

## P2 累计

- relink：315
- 跨类型/占位符/非法格式置空：459 + 287 + 201 = 947
- 空 ID 补已有画像：418
- **合计：1,680 条**

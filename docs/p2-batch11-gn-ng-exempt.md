# P2 批次 11：样本复核（GN/NG 豁免）

## GN/NG 临时豁免

几内亚、尼日利亚准备继续采集，数据会变动。本轮起：

- 批量扫描/修改排除 `gn`、`ng`
- 不重建其 name_index
- 不修改其 registry/画像/引用
- `output/gn/2026-11-10/.inflight` 存在，保持不动

历史已完成的修改保留，不回滚。等采集稳定后单独处理。

## 样本 B

排除 GN/NG 后，从剩余错误引用中抽取 160 条复核：

| 决策 | 数量 |
|---|---:|
| 保留 | 12 |
| 暂缓 | 7 |
| 置空 | 141 |

### 保留

- 阿联酋海军 ↔ 阿拉伯联合酋长国海军
- 阿塞拜疆武装部队 ↔ 武装力量
- 阿塞拜疆总检察长办公室 ↔ 总检察院
- Müsavat/Musavat 党
- AIOC 中英文名

### 暂缓

- dnata vs Emirates Group（母子）
- Nine Network vs Nine Entertainment（母子）
- AMP 新西兰/澳大利亚 vs AMP Group（母子）
- 布基纳法索国民议会 vs 人民立法议会

### 置空典型

- AE-NGO-003 MBR 全球倡议下挂着物种保护基金、古兰经印刷中心等不同实体
- AU-FIN-008 AMP 下挂 ISS、TNT、ING、Mitie、GPT 等
- AU-GOV-075 麦肯锡下挂贝恩咨询
- AZ-SOE-013 邮政下挂旅游、政党、媒体、土耳其军队等
- AZ-GOV-006 宪法法院下挂保护区、国防工业、青年组织等
- JP 大量 key_people 指向完全不同的政治家/企业家
- BF/BN 人物关系指向同姓但不同的人

## 审计变化

| 指标 | 前 | 后 |
|---|---:|---:|
| work_org wrong | 8,325 | 8,293 |
| person_rel wrong | 2,631 | 2,591 |
| family wrong | 0 | 0 |
| key_people wrong | 250 | 210 |
| related_org wrong | 1,941 | 1,912 |

141 条置空全部消除对应 wrong_target；没有改画像、registry、头像。

## 产物

- 样本：`output/_id_audit/p2_wrong_review_b.csv`
- 决策：`output/_id_audit/p2_wrong_review_b_decisions.csv`
- 撤销：`output/_id_audit/p2_batch11_review_sample_b_undo.json`
- 脚本：`scripts_tmp/p2_wrong_sample_b.py`、`scripts_tmp/p2_batch11_review_sample_b.py`

## P2 累计

| 类型 | 数量 |
|---|---:|
| relink | 315 |
| 结构置空 | 947 |
| 空 ID 补已有画像 | 418 |
| 碰撞影子置空 | 226 |
| 复核样本置空 | 273 |
| **合计** | **2,179** |

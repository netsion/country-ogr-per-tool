# P3 收尾：重复 Wikidata QID 清理（2026-11-14）

## 起点

- 人物 71 组 + 组织 13 组重复 QID（清单 `output/_id_audit/p1_qid_review.csv`）

## 处理原则

- **同名/同人跨数据集重复**：QID 只保留在内容更丰富的"主"画像上；其余画像保留但 QID 置空
  - 跨国镜像画像（同一人在多个国家数据集各有一份）是合法设计，**不合并档案**，只去重 QID
- **模板复制错误**（一个 QID 挂在完全无关的实体上）：只保留真正对应实体，其余全部清空
- **组织国际组织镜像**（联合国/世贸/OIC 等各国目录各一份）：保留最丰富一份，其余清空
- **GN/NG 豁免**：NG 两个日期目录（2026-07-29 / 2026-11-10）之间的重复全部不动

## 执行轮次

| 轮次 | 脚本 | 清空数 | 说明 |
|---|---|---:|---|
| 1 | `p3_qid_merge_apply.py` | 54 | 同名 53 组按"分数/条目数更多者保留" |
| 2 | `p3_qid_round2.py` | 53 | 变体名/跨名同实体组；`Q57643` 只留 Thomas Sankara |
| 3 | `p3_qid_round3.py`（inline） | 5 | 真不同实体：JP 邮政（持股公司 vs 集团）、QA 阿拉银行卡塔尔分行、NI 信仰与喜悦、MY 林冠英≠阿克马沙烈、IQ 舒瓦尼≠马拉吉 |
| 4 | round4（inline） | 2 | HK 蒋东强误挂菲律宾国家电力 QID（跨类型模板错误）；TJ 中亚大学镜像（保留 KG） |

合计清空 **114 个**错重 QID；每轮均有 undo 日志。

## 验证

- 全库扫描：**非 NG/GN 数据集重复 QID = 0 组**
- 剩余 15 组全部位于 NG 两个日期目录之间（豁免，等 NG 采集稳定后处理）
- 抽验被改文件 strict 校验：0 errors

## 审计变化

| 指标 | 前 | 后 |
|---|---:|---:|
| duplicate_wikidata persons | 71 | 0（NG 豁免口径）/ 15 组 NG 内部 |
| duplicate_wikidata orgs | 13 | 0（同上） |
| index 各项 | 0 | 0（保持） |

## 留空/存疑

- `Q4681477`（NG 阿德比西·阿坎德）：两份都在 NG 目录，豁免未动
- `Q11108502` 等 14 组 NG 内部重复：同上

## 产物

- 合并计划：`output/_id_audit/p3_qid_merge_plan.json`
- 撤销：`p3_qid_merge_undo.json`、`p3_qid_round2_undo.json`、`p3_qid_round3_undo.json`、`p3_qid_round4_undo.json`
- 脚本：`scripts_tmp/p3_qid_merge_apply.py`、`scripts_tmp/p3_qid_round2.py`

## 下一步

1. key_people 剩余 12 条转写变体人工确认（半小时内）
2. registry 碰撞收尾（153 org / 163 person ID）

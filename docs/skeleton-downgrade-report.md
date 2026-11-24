# 骨架画像降级报告（方案 A，2026-11-23）

## 背景

近期收尾的 7 个新数据集（BD/EG/GH/MA/ML/NG/SD）在 key_people 处理轮中创建了 1,840 个骨架画像（仅含姓名+职务+所属组织，无传记/教育/立场等内容）。这些骨架在下游系统没有展示价值。

按方案 A 降级：骨架档案删除，人物信息保留在所属组织的 key_people 条目里。

## 执行结果

| 动作 | 数 |
|---|---:|
| 骨架档案删除（备份到 output/_id_audit/skeleton_downgrade_backup/） | 1,840 |
| 指向骨架的引用 ID 置空（key_people/work_experience/relationships） | 1,893 |
| registry 骨架条目移入 deprecated | 1,477 |
| persons/_index.json 同步清理 | 7 个数据集 |
| MinIO 骨架头像清理 | 含在内 |

## 降级后人物数（真实采集量）

| 数据集 | 降级前 | 降级后 |
|---|---:|---:|
| BD 孟加拉 | 788 | **181** |
| EG 埃及 | 428 | **208** |
| GH 加纳 | 436 | **204** |
| MA 马里（目录 ma，实为摩洛哥数据） | 482 | **212** |
| ML 马里 | 238 | **181** |
| NG 尼日利亚 | 430 | **192** |
| SD 苏丹 | 408 | **179** |

## 验证

- 骨架画像残留：0
- 死头像路径：0
- 各数据集人物数回归真实采集值

## 信息不丢

骨架的全部信息（姓名/职务/所属组织）本来就在各组织 key_people 条目里（person_id 置空、name/title 保留）。将来如果要给某人建正式档案，key_people 条目里有完整的起始信息。

备份：骨架原文件全部在 `output/_id_audit/skeleton_downgrade_backup/{cc}/` 下，可随时恢复。

## 提交

- `cd0e4c0dc` data: Plan A skeleton downgrade
- 已推送远端

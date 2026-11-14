# P3 收尾：registry 碰撞清零（2026-11-14）

## 起点

- 153 个 org ID + 163 个 person ID 存在"一个 ID 多身份"碰撞
- person 集中在 RU 80 / SG 59 / UZ 10；org 集中在 KR 50 / JP 31 / MX 31 / NZ 26

## 处理方式

先摸底确认两类碰撞结构一致：**每个碰撞 ID 都有一个 owner 画像 + 若干 registry 影子身份**；影子身份的引用早在 P2 自动批次中已按名称置空/改链。

因此本轮只做 registry 层清理：

1. 用"owner 名 token 交集 + 该 ID 有画像"判定 owner 注册条目（初版用模糊匹配误伤 owner 短名变体，已修正后重跑）；
2. 其余影子注册条目移入 `deprecated_registry` / `deprecated_person_registry`，状态 `collision_split`；
3. 不动画像、引用、头像（引用层 P2 已处理完）；
4. 完成后重建 10 个受影响数据集的 `_name_index.json`。

## 执行

| 批次 | 范围 | 归档影子条目 |
|---|---|---:|
| RU person | RU 80 ID | 86 |
| SG/UZ/TH/KR/MX/ID/PG/VN person | 83 ID | 115 |
| 全部 org | 153 ID | 291 |
| **合计** | **236 ID** | **492** |

## 最终状态

```text
registry collisions:  org = 0   person = 0
duplicate wikidata:   persons = 0   orgs = 0（NG 目录内豁免项除外）
index:                全部 0（无缺文件/错名/未入索引）
```

| 方向 | ok | wrong | 说明 |
|---|---:|---:|---|
| work_org | 60,515 | 49 | 全部在 GN/NG |
| person_rel | 32,639 | 5 | 注册名转写别名，正确 |
| family | 1,663 | 0 | — |
| key_people | 18,047 | 7 | 转写别名，正确 |
| related_org | 18,298 | 139 | 全部在 GN/NG |

## P1+P2+P3 全程总览（2026-11-13 ～ 11-14）

| 阶段 | 内容 | 规模 |
|---|---|---|
| P1 | 索引同步 + registry 名称污染 + 无名画像补名 | 135+9+8 索引项、121 名称、6 画像 |
| P2 | 错误引用清理（人工簇 + 全自动长尾） | ≈15,010 条 |
| P3 | QID 去重 | 114 个 QID |
| P3 | key_people 转写确认 | 保留 7 / 置空 5 |
| P3 | registry 碰撞 | 归档 492 影子条目，碰撞清零 |

## 产物

- `output/_id_audit/p3_ru_person_collisions_undo.json`
- `output/_id_audit/p3_person_collisions_generic_undo.json`
- `output/_id_audit/p3_org_collisions_undo.json`
- 脚本：`scripts_tmp/p3_ru_person_collisions.py`、`p3_person_collisions_generic.py`、`p3_org_collisions_cleanup.py`

## 遗留

- GN/NG：等数据采集稳定后做一轮同样的错链 + 碰撞清理
- NG 两个日期目录的重复 QID/档案：随 GN/NG 批次处理
- 可选 enrichment（385 补画像、科技实体深化等）不阻塞任何下游

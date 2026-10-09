# 人物画像规则附则 — 科特迪瓦批次（P4 子代理必读，配合 person_collection_rules.md 使用）

> person_collection_rules.md 是主规则手册；本文件是科特迪瓦批次的补充约束。冲突时以本文件为准。

## 语言（科特迪瓦：官方语言法语）

- `name`（本国官方语言）= 法语/拉丁原名，如 `Alassane Ouattara`（科特迪瓦人名本就拉丁字母，无需转写）
- `name_zh` = 纯中文译名，如 `阿拉萨内·瓦塔拉`。获取优先级：Wikidata zh label → 中文维基 → 新华社/中文媒体通行译名（Ouattara=瓦塔拉、Gbagbo=巴博、Bédié=贝迪埃）→ 音译。**禁止留空**（这是中文母语数据集的核心字段）
- `name_en` = 拉丁原名（与 name 相同即可）
- `biography_summary` = **中文 ≥100 字**（硬性要求）
- `current_positions[]` / `work_experience[].position` / 所有描述性字段 = 纯中文
- `work_experience[].organization` / `education[].institution` / 关系人姓名 / 家人姓名 = 中文(法语)，如 `科特迪瓦民主党 (PDCI)`
- 搜索语言顺序：法语 → 英语 → 中文

## 工具与网络（本批次实测情况）

- 首选：`mcp__search-read__search`（keyword）+ `mcp__search-read__read_url`（url）——服务端工具，稳定可用
- `mcp__web_reader__webReader` **配额耗尽，禁止使用**
- curl 回退：`curl -sL --proxy http://127.0.0.1:7890 "URL"`（本地代理偶发不稳，失败就改用搜索快照交叉验证，不要死磕）
- WebSearch 可作搜索备选
- 总请求 ≤15 次，间隔 ≥1 秒（页面 3 秒）

## 去重（本批次重点）

- 写入前必须先查 `output/ci/2026-10-06/_name_index.json`：同名人物已有 person_id → **复用该 ID 更新信息**，禁止新建重复档案
- 拉丁人名拼写变体（如 Diomandé/Diomandé）视为同一人，以音译一致性判断
- 禁止修改 id_registry.json（主会话统一批量注册）

## APEC（如需提及）

科特迪瓦不是 APEC 成员。人物画像通常无需 APEC 内容；如 biography 涉及国际合作框架，如实写 AU/ECOWAS/UEMOA/OIC 等，禁止编造 APEC 关联。

## collection_meta

- `phase` = `"phase4_person_profile"`
- `collection_date` = 当天日期
- `quotes` = 对象数组 ≥3 条（Wikipedia + 官方/新闻页），禁止字符串数组、禁止空数组

## 写入后验证（不可跳过）

```bash
python .agents/skills/country-org-collector/scripts/validate_schema.py output/ci/2026-10-06 --file persons/{person_id}.json
# ERRORS → 修复 → 重验直到 0
python .agents/skills/country-org-collector/scripts/validate_schema.py output/ci/2026-10-06 --file persons/{person_id}.json --score
```

## 铁律

- 禁止编造，搜不到留空（family_members 无真实全名就删条目）
- 重要信息 ≥2 独立来源交叉确认
- 禁止修改 id_registry.json

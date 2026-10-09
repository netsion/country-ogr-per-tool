# 人物画像规则手册（P4 子代理必读 — 摩洛哥数据集）

> 本文件是摩洛哥 P4 人物子代理的规则参考。执行步骤、人物参数与路径由主会话 prompt 内联提供。

## 国家背景（影响搜索与字段）

- 官方语言：阿拉伯语；法语在政府/媒体/学术界通行。人物姓名通行拼写为**法语拉丁转写**（如 Nasser Bourita）。
- 人名搜索优先级：法语 → 阿拉伯语 → 英语。Wikipedia 优先 fr/ar/en。
- **政治时点**：2026-09-23 立法选举（PAM 97 席第一）；2026-09-29 国王任命 Fatima Ezzahra El Mansouri 为新政府首脑（首位女性），新内阁名单截至 2026-10-06 可能未完全公布。职务以最新可确认来源为准，过渡期注明「截至」时点。
- 摩洛哥非 APEC 成员：不涉及 APEC 立场内容，勿编造。
- 中文译名：参考中文媒体通行译法（新华社对摩洛哥人物的译名可用），查不到则自行音译并全档案一致。

## 字段名严格约束（禁止自创字段名）

| 数组 | 允许的字段名（仅这些） |
|------|------|
| work_experience[] | start_date \| end_date \| organization \| org_id \| position |
| education[] | institution \| degree \| field \| start_date \| end_date |
| political_stances[] | date \| topic \| stance_content \| source |
| person_relationships[] | person_id \| person_name \| relationship_type \| description |
| major_achievements[] | date \| achievement \| organization |
| social_accounts[] | platform \| account_name \| url \| source |
| family_members[] | person_id \| name \| relationship \| industry_or_organization |
| contacts[] | type \| value \| source |

必填：person_id, name, name_en, nationality, gender。**禁止写 importance_level（不在 schema 中）**；禁止空壳条目（family_members 无真实姓名就删条）。

## 字段语言规范（摩洛哥）

| 字段 | 格式 | 示例 |
|------|------|------|
| name | 拉丁拼写（法语通行形式） | `Nasser Bourita` |
| name_en | 英文/拉丁形式 | `Nasser Bourita` |
| name_zh | 中文译名 | `纳赛尔·布瑞塔` |
| aliases[] | 拼写变体 | `Bourita` |
| nationality | `MA` | |
| gender | `male` / `female` / `unknown` | |
| biography_summary | 中文（200字+） | |
| current_positions[] | 纯中文 | `外交大臣` |
| work_experience[].organization | 中文(拉丁拼写) | `外交部 (Ministère des Affaires étrangères)` |
| work_experience[].position / org_id | 中文 / ID或null | |
| education[].institution | 中文(拉丁拼写) | `穆罕默德五世大学 (Université Mohammed V)` |
| person_relationships[].person_name | 中文(拉丁拼写) | `福齐·莱贾 (Fouzi Lekjaa)` |
| family_members[].name | 中文(拉丁拼写)，真实全名 | |
| major_achievements[].organization | 中文(拉丁拼写) | |
| political_stances[] | topic/stance_content 中文 | |
| social_accounts[].platform | 小写英文枚举：facebook/x_twitter/instagram/youtube/linkedin/tiktok/threads/other 等 | |
| nationality / relationship / degree / contacts.type | 英文枚举或 ISO 代码 | |

## ID 规则

1. 本人物档案文件名即 person_id（主会话给定，勿更改）
2. 组织/他人 ID：查 `output/ma/2026-10-05/_name_index.json`
3. 未命中 → 写 `null`（JSON null，禁止 `""`）
4. 禁止自创 ID 格式；**不要修改 id_registry.json**

## 内容过滤注意（本数据集已发生 2 例）

若某条搜索结果或页面导致工具报错，立即跳过该来源换用其他来源，不要重试同一条。军事/情报/工会人物尤其注意：只采集机构性、制度性公开信息，不深挖单一敏感事件细节。

## collection_meta 规范

- `phase` = `"phase4_person_profile"`
- `collection_date` = 当天日期
- `quotes` = **对象数组** `[{"title": "...", "url": "..."}]`，≥3 条（Wikipedia + 权威来源 + 新闻），禁止字符串数组、禁止空数组
- `data_sources` = 实际使用的来源类型
- `notes` = 中文，说明来源确认情况、存疑字段、组阁过渡期注意事项

## JSON 写入方式（Windows CJK 必读）

- ❌ 禁止 `python -c "..."` 内联写入；❌ 禁止手动拼接 JSON
- ✅ 用 Write 工具直接写完整 JSON，或 Write 临时 .py + `json.dump(ensure_ascii=False, encoding='utf-8')` 执行后删除
- 中文引号用 `「」`

## 写入后验证（不可跳过；先 cd 到仓库根目录）

```bash
cd D:/claude-workspace/apec-osint-tool
# 注意：--file 接受相对 output_dir 的路径（persons/{person_id}.json）
python .agents/skills/country-org-collector/scripts/validate_schema.py output/ma/2026-10-05 --file persons/{person_id}.json
# ERRORS → 修复 → 重验直到 0
python .agents/skills/country-org-collector/scripts/validate_schema.py output/ma/2026-10-05 --file persons/{person_id}.json --score
```

## 铁律

- 禁止编造，搜索不到则留空/null
- 重要信息 ≥2 独立来源确认
- Cloudflare 拦截 → 跳过并标记 `source_blocked_cloudflare`，换替代来源
- 搜索工具首选 `mcp__search-read__search` / `mcp__search-read__read_url`，失败降级 WebSearch / mcp__web_reader__webReader

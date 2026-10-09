# 组织丰富规则手册（P3 子代理必读）— 科特迪瓦批次

> 本文件是 P3 组织丰富子代理的规则参考。执行步骤与路径由主会话 prompt 内联提供。

## 字段名严格约束（禁止自创字段名）

| 数组 | 允许的字段名（仅这些） |
|------|------|
| key_people[] | person_id \| name \| title \| title_description \| description |
| departments[] | name \| dept_id \| head \| description \| parent_dept_id |
| social_accounts[] | platform \| account_name \| url \| source |
| recent_events[] | date \| title \| description \| impact \| source |
| related_entities[] | org_id \| org_name \| org_type \| org_description \| relationship_type |
| digital_assets[] | name \| url \| description \| source |

顶层仅保留 schema 定义字段：org_id, wikidata_qid, basic_info, social_accounts, digital_assets, key_people, departments, recent_events, related_entities, core_business, industries, apec_stance, profile, collection_meta。

**常见错误**：
- ❌ departments[].name_zh/name_en → ✅ departments[].name
- ❌ related_entities[].name_zh/relationship/description → ✅ org_name/relationship_type/org_description
- ❌ related_entities[].type → ✅ related_entities[].org_type
- ❌ digital_assets[].title_zh/title_en → ✅ digital_assets[].name
- ❌ apec_stance/core_business 写成 dict → ✅ 必须为纯文本字符串

## 字段语言规范（科特迪瓦：官方语言法语）

| 字段 | 格式 | 示例 |
|------|------|------|
| basic_info.name_original | 法语原文 | `Ministère des Affaires étrangères` |
| basic_info.name_en | 英文 | `Ministry of Foreign Affairs` |
| basic_info.name_zh | 中文 | `外交部` |
| key_people[].name | 中文(法语) | `阿拉萨内·瓦塔拉 (Alassane Ouattara)` — 中文在前 |
| key_people[].title | 中文 或 中文(法语) | `部长` / `部长 (Ministre)` |
| key_people[].title_description / description | 中文 | |
| departments[].name | 中文 或 中文(法语) | |
| departments[].head | 中文(法语) | |
| related_entities[].org_name | 中文(法语) | `博瓦隆银行科特迪瓦分行 (Bank of Africa Côte d'Ivoire)` |
| recent_events[].title / description / impact | 中文 | |
| digital_assets[].name / description | 中文 | |
| core_business | 中文，200字+ | |
| apec_stance | 中文 | |
| industries | 英文枚举值（不改） | |
| social_accounts[].platform | 小写英文枚举：facebook/x_twitter/instagram/youtube/linkedin/tiktok/website/other 等 | |
| 所有 URL | 保留原样 | |

**法语人名中文译名**：采用新华社/中文媒体通行译名（如 Ouattara=瓦塔拉、Gbagbo=巴博、Bédié=贝迪埃），同一人物全库保持一致。查不到通行译名时用音译并保持一致性。

## APEC 立场（本批次特殊规则）

**科特迪瓦不是 APEC 成员**（APEC 现有 21 个成员经济体，均为太平洋沿岸国家/地区，非洲国家均未加入）。
每个组织的 `apec_stance` 必须如实说明："科特迪瓦不是APEC成员（APEC现有21个成员经济体，非洲国家均未加入）"，并简述其实际国际合作框架（如非洲联盟 AU、西非经济共同体 ECOWAS、西非货币联盟 UEMOA、伊斯兰合作组织 OIC、与主要伙伴的经贸协定等）。
**禁止**编造"某年加入APEC""主办APEC会议"等虚构内容。

## ID 规则

1. 查 `output/ci/2026-10-06/_name_index.json`
2. 命中 → 使用对应 org_id / person_id
3. 未命中 → 写 `null`（JSON null，禁止 `""`）
4. 禁止自创 ID 格式（不要写 CI-ORG-xxx 等非标准格式）
5. **不要修改 id_registry.json**（主会话统一批量注册，避免 4 路并发写冲突）

## recent_events 要求

- ≥3 条，来源以法语新闻为主（可用英文补充）
- date 必须 `YYYY-MM-DD`（仅知年月用 `YYYY-MM-01`）
- 每条必须有 `source` URL
- 只记录已确认事实；impact 可写分析性内容但注明依据

## collection_meta 规范

- `phase` = `"phase3_enriched"`
- `quotes` = **对象数组** `[{"title": "...", "url": "..."}]`，≥3 条（Wikipedia + 官网 + 新闻），禁止纯字符串数组、禁止空数组
- `data_sources` = 补充本次实际使用的来源类型（如 `"news_search"`, `"official_website"`）
- `completeness_score` = 由 validate_schema.py --score 更新

## JSON 写入方式（Windows CJK 必读）

- ❌ 禁止 `python -c "..."` 内联写入（GBK 终端破坏法文重音字符/中文）
- ❌ 禁止手动拼接 JSON 字符串
- ✅ 用 Write 工具创建临时 .py 脚本，脚本内 `json.dump(data, f, ensure_ascii=False, indent=2)` + `open(..., 'w', encoding='utf-8')`，再用 Bash 执行
- ✅ 或直接用 Write 工具写完整 JSON 文本（确保 UTF-8、引号正确转义）
- 中文引号用 `「」`

## 交叉验证与铁律

- 重要信息（人物职位、事件日期）至少 2 个独立来源确认
- **禁止编造**：搜索不到则留空/null，绝不猜测
- Cloudflare 拦截 → 跳过该来源，标记 `source_blocked_cloudflare`，换新闻/Wikipedia 替代，不尝试绕过
- 工具优先级：搜索 `mcp__search-read__search`（keyword 参数）→ 失败用 WebSearch；读取 `mcp__search-read__read_url`（url 参数）→ 失败用本地 curl + 代理 `--proxy http://127.0.0.1:7890`（加 `-L`）。`mcp__web_reader__webReader` 当前配额耗尽，不要使用
- 限速：搜索/页面间隔 ≥1 秒（普通页面 3 秒），总请求量控制在 15 次以内

## 写入后验证（不可跳过）

```bash
python .agents/skills/country-org-collector/scripts/validate_schema.py output/ci/2026-10-06 --file output/ci/2026-10-06/orgs/{org_id}.json
# ERRORS → 修复 → 重验直到 0
python .agents/skills/country-org-collector/scripts/validate_schema.py output/ci/2026-10-06 --file output/ci/2026-10-06/orgs/{org_id}.json --score
```

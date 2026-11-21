# 组织丰富规则手册（埃及 EG P3 子代理必读）

> 本文件是 P3 组织丰富子代理的规则参考。执行步骤与路径由主会话 prompt 内联提供。

## 字段名严格约束（禁止自创字段名）

| 数组 | 允许的字段名（仅这些） |
|------|------|
| key_people[] | person_id \| name \| title \| title_description \| description |
| departments[] | name \| dept_id \| head \| description \| parent_dept_id |
| social_accounts[] | platform \| account_name \| url \| source \| source_note |
| recent_events[] | date \| title \| description \| impact \| source |
| related_entities[] | org_id \| org_name \| org_type \| org_description \| relationship_type |
| digital_assets[] | name \| url \| description \| source |

顶层仅保留 schema 定义字段：org_id, wikidata_qid, basic_info, social_accounts, digital_assets, key_people, departments, recent_events, related_entities, core_business, industries, apec_stance, profile, collection_meta。

**常见错误**：
- ❌ departments[].name_zh/name_en → ✅ departments[].name
- ❌ related_entities[].name_zh/relationship/description → ✅ org_name/relationship_type/org_description
- ❌ related_entities[].type → ✅ related_entities[].org_type
- ❌ digital_assets[].title_zh/title_en → ✅ digital_assets[].name
- ❌ apec_stance/core_business 写成 dict/object → ✅ 必须为纯文本字符串

**必填项与格式**（schema 强校验）：
- `departments[].dept_id` 必填，格式 `{ISO2}-{TYPE}-{SEQ}-DEPT-{SEQ3}`，如 `EG-GOV-001-DEPT-001`、`EG-GOV-001-DEPT-002`（按组织 org_id 顺序编号）
- `departments[]` 必填 name；`head` 用 中文(阿拉伯语)
- `recent_events[]` 必填 date/title/description，且每条必须有 `source` URL；date 必须 `YYYY-MM-DD`（仅知年月用 `YYYY-MM-01`）
- `social_accounts[]` 必填 platform/url；`source` 必须为整数代码或 null（twitter=3 facebook=6 instagram=8 youtube=9 linkedin=17 telegram=19），来源说明写入 `source_note`（字符串）
- `key_people[]` 必填 name/title；`person_id` 可为 null，格式 `EG-PERSON-000001`（只在 _name_index.json 命中时填写）
- `related_entities[]` 必填 org_id/org_name/relationship_type；org_id 只在索引命中时填，否则 null（主会话统一批量注册，**不要修改 id_registry.json**）

## 字段语言规范（埃及：官方语言=阿拉伯语）

| 字段 | 格式 | 示例 |
|------|------|------|
| basic_info.name_original | 阿拉伯语 | `وزارة الخارجية` |
| basic_info.name_en | 英文 | `Ministry of Foreign Affairs` |
| basic_info.name_zh | 中文 | `外交部` |
| key_people[].name | 中文(阿拉伯语) | `阿卜杜勒-法塔赫·塞西 (عبد الفتاح السيسي)` — 中文在前 |
| key_people[].title | 中文 或 中文(阿拉伯语) | `部长` / `部长 (الوزير)` |
| key_people[].title_description / description | 中文 | |
| departments[].name | 中文 或 中文(阿拉伯语) | `政治计划司 (قطاع التخطيط)` |
| departments[].head | 中文(阿拉伯语) | |
| related_entities[].org_name | 中文(阿拉伯语) | `阿拉伯国家联盟 (جامعة الدول العربية)` |
| recent_events[].title / description / impact | 中文 | |
| digital_assets[].name / description | 中文 | |
| core_business | 中文，200字+ | |
| apec_stance | 中文 | |
| industries | 英文枚举值（不改，参考 enum_reference.md） | |
| social_accounts[].platform | 小写英文枚举：facebook/x_twitter/instagram/youtube/linkedin/telegram/tiktok/website/other | |
| 所有 URL | 保留原样 | |

**阿拉伯语人名中文译名**：优先使用新华社通行译名/中国外交部网站译名（如 塞西、马德布利、阿卜杜勒阿提）；查不到通行译名时按阿拉伯语音译规则谨慎转写并在 description 中注明"（音译）"。禁止编造职位、履历等事实信息。

## ID 规则

1. 查 `output/eg/2026-11-16/_name_index.json`
2. 命中 → 使用对应 org_id / person_id
3. 未命中 → 写 `null`（JSON null，禁止 `""`）
4. 禁止自创 ID 格式（不要写 EG-ORG-xxx 等非标准格式）
5. **不要修改 id_registry.json**（主会话统一批量注册，避免 4 路并发写冲突）

## recent_events 要求

- ≥3 条，来源以阿拉伯语新闻为主（英语补充，如 Ahram Online、Egyptian Streets、Reuters）
- date 必须 `YYYY-MM-DD`（仅知年月用 `YYYY-MM-01`）
- 每条必须有 `source` URL
- 只记录已确认事实；impact 可写分析性内容但注明依据

## APEC 立场（埃及专属规则）

**埃及不是 APEC 成员**（APEC 现有 21 个成员经济体，埃及未加入）。禁止搜索或编造任何"APEC成员""曾主办APEC会议"等内容。

`apec_stance` 按以下固定表述，并根据组织实际参与的跨区域框架微调补充：
"埃及不是APEC成员（APEC现有21个成员经济体，埃及未加入）。埃及实际参与的国际合作框架：阿拉伯国家联盟（总部开罗）、非洲联盟、COMESA、伊斯兰合作组织、金砖国家（2024年加入）。"

## collection_meta 规范

- `phase` = `"phase3_enriched"`
- `quotes` = **对象数组** `[{"title": "...", "url": "..."}]`，≥3 条（Wikipedia 阿语/英语 + 官网 + 新闻），禁止纯字符串数组、禁止空数组
- `data_sources` = 补充本次实际使用的来源类型（如 `"news_search"`, `"official_website"`, `"arabic_wikipedia"`)
- `completeness_score` = 由 validate_schema.py --score 更新

## JSON 写入方式（Windows 阿文/中文 CJK 必读）

- ❌ 禁止 `python -c "..."` 内联写入（GBK 终端破坏阿文/中文）
- ❌ 禁止手动拼接 JSON 字符串
- ✅ 用 Write 工具创建临时 .py 脚本到 `output/eg/2026-11-16/_tmp/`，脚本内 `json.dump(data, f, ensure_ascii=False, indent=2)` + `open(..., 'w', encoding='utf-8')`，再用 Bash 执行
- ✅ 执行后用脚本 `json.load()` 回读验证
- 中文引号用 `「」`
- 临时脚本只放 `_tmp/`，不要删除别人的文件（主会话统一清理）

## 交叉验证与铁律

- 重要信息（人物职位、事件日期）至少 2 个独立来源确认
- **禁止编造**：搜索不到则留空/null，绝不猜测
- Cloudflare 拦截 → 跳过该来源，换新闻/Wikipedia 替代，不尝试绕过
- 2026年2月内阁改组相关人物任命需第二独立来源交叉确认（P1 审计标记的敏感项）

## 写入后验证（不可跳过，注意 --file 是相对 output/eg/2026-11-16 的路径）

```bash
python .agents/skills/country-org-collector/scripts/validate_schema.py output/eg/2026-11-16 --file orgs/{org_id}.json
# ERRORS → 修复 → 重验直到 0
python .agents/skills/country-org-collector/scripts/validate_schema.py output/eg/2026-11-16 --file orgs/{org_id}.json --score
```

## 工具选择（严格遵守）

- **搜索首选** `mcp__search-read__search`（keyword 参数）；**读取首选** `mcp__search-read__read_url`（url 参数，format=markdown）
- 仅当首选工具报错/超时/返回空时才切换备选：`mcp__web_reader__webReader`、内置 `WebSearch`
- Cloudflare 质询页 → 直接跳过该来源，换新闻/Wikipedia 替代

## 限速（4 并发全局配额）

- 搜索/读取请求间隔 ≥1 秒
- 单组织总请求（搜索+读取）≤ 12 次；优先 Wikipedia 与官网两个高密度来源

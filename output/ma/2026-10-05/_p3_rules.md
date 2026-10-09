# 组织丰富规则手册（P3 子代理必读 — 摩洛哥数据集）

> 本文件是摩洛哥 P3 组织丰富子代理的规则参考。执行步骤与路径由主会话 prompt 内联提供。

## 国家背景（影响搜索与字段）

- 摩洛哥官方语言：**阿拉伯语**；政府/商业领域**法语**广泛使用。搜索新闻优先阿拉伯语（`أخبار`）和法语（`actualités`），英语补充。
- Wikipedia 三语页面：ar / fr / en。
- **摩洛哥不是 APEC 成员**：`apec_stance` 默认保持 `null`，除非有确凿文献证明该组织参与 APEC 相关活动，否则不填、不编造。
- **政治时点**：2026-09-23 立法选举（PAM 97 席第一），2026-09-30 国王任命 Fatima Ezzahra El Mansouri 为新政府首脑。key_people 现任职位必须以最新来源为准；内阁改组过渡期无法确认新任者时，记录前任并注明（如"截至2026年9月"）。

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
- ❌ apec_stance/core_business 写成 dict → ✅ 纯文本字符串

## 字段语言规范

| 字段 | 格式 | 示例 |
|------|------|------|
| basic_info.name_original | 阿拉伯语原文 | `وزارة الشؤون الخارجية` |
| basic_info.name_en | 英文（官方通行英文名） | `Ministry of Foreign Affairs` |
| basic_info.name_zh | 中文 | `外交部` |
| key_people[].name | **中文(法语通行拼写或阿拉伯语)**，中文在前 | `纳赛尔·布瑞塔 (Nasser Bourita)` |
| key_people[].title | 中文 或 中文(法语) | `外交大臣` / `大臣 (Ministre)` |
| key_people[].title_description / description | 中文 | |
| departments[].name | 中文 或 中文(法语) | `礼宾司 (Direction du Protocole)` |
| departments[].head | 中文(法语通行拼写) | |
| related_entities[].org_name | 中文(法语通行拼写) | `真实性与现代党 (Parti Authenticité et Modernité)` |
| recent_events[].title / description / impact | 中文 | |
| digital_assets[].name / description | 中文 | |
| core_business | 中文，200字+ | |
| apec_stance | 中文（默认 null） | |
| industries | 英文枚举值（不改） | |
| social_accounts[].platform | 小写英文枚举：facebook/x_twitter/instagram/youtube/linkedin/tiktok/website/other 等 | |
| 所有 URL | 保留原样 | |

**摩洛哥人名中文译名**：参考中文媒体通行译法（新华社对摩洛哥官员的译名可用），查不到通行译名时自行音译并在全档案保持一致。人物 `name` 本体（person 档案）沿用骨架中已有的拉丁拼写，不要改成阿拉伯文。

## ID 规则

1. 查 `output/ma/2026-10-05/_name_index.json`
2. 命中 → 使用对应 org_id / person_id
3. 未命中 → 写 `null`（JSON null，禁止 `""`）
4. 禁止自创 ID 格式（不要写 MA-ORG-xxx 等非标准格式）
5. **不要修改 id_registry.json**（主会话统一批量注册，避免 4 路并发写冲突）

## recent_events 要求

- ≥3 条，来源以阿拉伯语/法语新闻为主（英语可补充）
- date 必须 `YYYY-MM-DD`（仅知年月用 `YYYY-MM-01`）
- 每条必须有 `source` URL
- 只记录已确认事实；impact 可写分析性内容但注明依据

## collection_meta 规范

- `phase` = `"phase3_enriched"`
- `quotes` = **对象数组** `[{"title": "...", "url": "..."}]`，≥3 条（Wikipedia + 官网 + 新闻），禁止纯字符串数组、禁止空数组
- `data_sources` = 补充本次实际使用的来源类型（如 `"news_search"`, `"official_website"`）
- `completeness_score` = 由 validate_schema.py --score 更新

## JSON 写入方式（Windows 阿拉伯文/中文 CJK 必读）

- ❌ 禁止 `python -c "..."` 内联写入（GBK 终端破坏阿拉伯文/中文）
- ❌ 禁止手动拼接 JSON 字符串
- ✅ 用 Write 工具创建临时 .py 脚本（放在 output/ma/2026-10-05/tmp_*.py），脚本内 `json.dump(data, f, ensure_ascii=False, indent=2)` + `open(..., 'w', encoding='utf-8')`，再用 Bash 执行后删除临时脚本
- 中文引号用 `「」`

## 交叉验证与铁律

- 重要信息（人物职位、事件日期）至少 2 个独立来源确认
- **禁止编造**：搜索不到则留空/null，绝不猜测
- Cloudflare 拦截 → 跳过该来源，标记 `source_blocked_cloudflare`，换新闻/Wikipedia 替代，不尝试绕过
- 搜索工具首选 `mcp__search-read__search`，读取首选 `mcp__search-read__read_url`，失败自动换备选（WebSearch / mcp__web_reader__webReader）

## 写入后验证（不可跳过；先 cd 到仓库根目录）

```bash
cd D:/claude-workspace/apec-osint-tool
# 注意：--file 接受的是相对 output_dir 的路径（orgs/{org_id}.json），不要带 output/ma/... 前缀
python .agents/skills/country-org-collector/scripts/validate_schema.py output/ma/2026-10-05 --file orgs/{org_id}.json
# ERRORS → 修复 → 重验直到 0
python .agents/skills/country-org-collector/scripts/validate_schema.py output/ma/2026-10-05 --file orgs/{org_id}.json --score
```

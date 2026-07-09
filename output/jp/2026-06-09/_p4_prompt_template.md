# P4 Sub-agent Prompt Template (Japan - Person Enrichment)

> Anti-degradation: main session reads this file before dispatching each sub-agent.

## 模板

```
你是人物信息调查 Agent。任务：为 {person_id}（{name_en}）生成高质量画像。

第一步：读取必要文件（不可跳过）
1. 字段规则手册：D:/claude-workspace/apec-osint-tool/.claude/skills/country-org-collector/person_collection_rules.md
2. Schema定义：D:/claude-workspace/apec-osint-tool/.claude/skills/country-org-collector/person_profile_schema.json
3. ID映射索引：D:/claude-workspace/apec-osint-tool/output/jp/2026-06-09/_name_index.json

第二步：搜索并获取详情
1. 按 person_collection_rules.md 搜索策略执行多语言搜索（mcp__search-read__search 首选）
2. 搜索顺序：日本語 → English → 中文
3. 对搜索结果中的高价值页面，使用 mcp__search-read__read_url 读取全文
4. 至少读取 3 个不同来源的完整页面（如 Wikipedia、政府名录、官方页面）

⚠️ 中文名获取（name_zh）：
- 优先从 Wikipedia 中文版获取中文译名
- 日本人物：使用华文媒体常用译名（非新华社音译）
- 日本汉字→中文简体转换规则：製→制、鐵→铁、電→电、讀→读、賣→卖、廳→厅、氣→气、產→产、營→营、農→农、廣→广、藝→艺、藥→药、銀→银、關→关、驗→验、議→议、團→团、體→体、點→点、務→务、權→权
- 示例：読売→读卖、電通→电通、経済→经济

⚠️ 安全审查：对于涉及日本政治/军事立场的描述（如中日关系、历史问题、领土争议等），使用中性、客观的措辞，引用公开来源，不做主观评价。

第三步：组装画像并写入 {filepath}
严格遵循 person_collection_rules.md 中的字段名约束、语言规范、枚举值、自检清单。

⚠️ name 字段必须为日本語（如「岸田文雄」「藤井輝夫」），不是中文开头
⚠️ name_zh 字段必须为纯中文（如「岸田文雄」「藤井辉夫」）
⚠️ person_relationships[].person_name 格式：中文(日本語)，如「石破茂（石破茂）」
⚠️ work_experience[].organization 格式：中文(日本語)，如「外務省（外務省）」
⚠️ education[].institution 格式：中文(日本語)，如「东京大学（東京大学）」
⚠️ degree 必须为英文枚举值：bachelor/master/doctorate/null，禁止写「学士」「修士」「博士」
⚠️ platform 必须为小写英文枚举：twitter_x/facebook/instagram/youtube/linkedin/...

collection_meta 规范：
- phase = "phase4_person_profile"
- collection_date = 当天日期 YYYY-MM-DD
- quotes = [{"title": "...", "url": "..."}]（对象数组，禁止纯字符串数组或空数组）
  至少包含 Wikipedia 和其他可靠来源
- data_sources = 本次实际使用的来源类型

第四步：写入后验证（不可跳过）
1. python D:/claude-workspace/apec-osint-tool/scripts/ensure_utf8.py {filepath}
2. python D:/claude-workspace/apec-osint-tool/.claude/skills/country-org-collector/scripts/validate_schema.py D:/claude-workspace/apec-osint-tool/output/jp/2026-06-09 --file {filepath}
3. 如有 ERRORS → 修复 → 重新验证 → 直到 0 errors
4. python D:/claude-workspace/apec-osint-tool/.claude/skills/country-org-collector/scripts/validate_schema.py D:/claude-workspace/apec-osint-tool/output/jp/2026-06-09 --file {filepath} --score

铁律：禁止编造信息，搜索不到则留空。重要信息至少2个独立来源确认。

完成后返回：person_id、最终 completeness_score、搜索来源数、各字段条目数。

任务参数：
- person_id: {person_id}
- name_en: {name_en}
- name_zh: {name_zh}
- name_local: {name_local}
```

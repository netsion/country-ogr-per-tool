# P3 Sub-agent Prompt Template (Japan)

> Anti-degradation: 主会话在派发每个子代理前读取此文件，用变量替换后作为 prompt。

## 模板

```
你是组织信息丰富 Agent。任务：为 {org_id}（{org_name_en}）生成高质量画像。

第一步：读取当前骨架文件
  文件路径：{filepath}
  读取后了解当前 completeness_score 和已有字段。

ID 规则：
1. 读取 D:/claude-workspace/apec-osint-tool/output/jp/2026-06-09/_name_index.json 获取已知实体 ID 映射
2. 引用的组织/人物在 index 中存在 → 使用对应 ID
3. 不在 index 中 → org_id / person_id 写 null
4. 禁止自创 ID 格式（不要写 JP-ORG-xxx 或 JP-GOV-PRES 等非标准格式）

第二步：搜索并收集信息（按 SKILL.md §13.2 步骤执行搜索，提取所有可用字段信息）

第三步：将丰富后的完整画像写入原文件路径

## 写入方式（重要）
- 使用 Write 工具直接写入完整 JSON（不要用 python 脚本）
- 写入后执行：python scripts/ensure_utf8.py {filepath}
- 然后执行验证（见下方「写入后必须执行」）

⚠️ 必须使用以下精确字段名（不可自创字段名）：

key_people[]:        person_id | name | title | title_description | description
departments[]:       name | dept_id | head | description | parent_dept_id
social_accounts[]:   platform | account_name | url | source
recent_events[]:     date | title | description | impact | source
related_entities[]:  org_id | org_name | org_type | org_description | relationship_type
digital_assets[]:    name | url | description | source

⚠️ 字段语言规范（遵循 §7 三种格式：中文 / 中文(本国官方语言) / 本国官方语言）：
- name_original → 日本語原文（如「株式会社読売新聞グループ本社」）
- name_zh → 中文简体（如「读卖新闻集团本社」）。注意日本汉字→中文简体转换：製→制、鐵→铁、電→电、讀→读、賣→卖、廳→厅、氣→气、產→产、營→营、農→农、廣→广、藝→艺、藥→药、銀→银、關→关、驗→验、議→议、團→团、體→体、點→点、務→务、權→权
- key_people[].name → 中文(日本語汉字) 注意括号内必须是日文汉字写法，不是平假名读音（如「柳井正（柳井正）」「岸田文雄（岸田文雄）」）
- key_people[].title → 中文 or 中文(日本語)（如"社长" or "社长（社長）"）
- key_people[].title_description → 中文（如"负责集团整体经营战略"）
- key_people[].description → 中文
- recent_events[].title → 中文
- recent_events[].description → 中文（150字以上）
- recent_events[].impact → 中文
- departments[].name → 中文 or 中文(日本語)
- departments[].description → 中文
- related_entities[].org_name → 中文(日本語)
- related_entities[].org_description → 中文
- digital_assets[].name → 中文
- digital_assets[].description → 中文
- core_business → 中文（200字+）
- apec_stance → 中文
- industries 保留英文枚举值
- social_accounts[].platform 保留英文枚举值
- 所有 URL 保留原样

禁止使用的错误字段名示例：
- ❌ departments[].name_zh/name_en → ✅ departments[].name
- ❌ related_entities[].name_zh/relationship/description → ✅ related_entities[].org_name/relationship_type/org_description
- ❌ related_entities[].type → ✅ related_entities[].org_type
- ❌ digital_assets[].title_zh/title_en → ✅ digital_assets[].name
- ❌ apec_stance/core_business 写成 dict/object → ✅ 必须为纯文本字符串

⚠️ 安全审查注意：对于涉及日本政治/军事立场的描述（如中日关系、历史问题、领土争议等），使用中性、客观的措辞，引用公开来源，不做主观评价。

交叉验证：重要信息需至少 2 个独立来源确认。禁止编造：搜索不到的信息留空，绝不猜测。

## 关键要求
1. completeness_score：目标 85+，必须填满所有字段
2. social_accounts：至少3个真实社交账号（Twitter/X、Facebook、Instagram、YouTube等）
3. digital_assets：至少2个数字资产（官网页面、App、流媒体平台等）
4. key_people：至少5人，person_id 留 null（P4阶段分配）
5. departments：主要部门/分支机构（如有）
6. recent_events：至少5条近期重要事件（2024-2026年），每条必须有 source URL
7. related_entities：至少5个关联实体，relationship_type 必须是以下之一：subsidiary, parent, partner, supplier, customer, competitor, regulator, controlling_shareholder, joint_venture, strategic_alliance
8. industries：至少2个行业标签
9. profile：包含 source_url（logo或标志性图片URL），local_path 留 null

写入前更新 collection_meta：
- collection_meta.phase = "phase3_enriched"
- collection_meta.collection_date = "2026-06-11"
- collection_meta.quotes = 来源URL列表，必须是对象数组，每条含 title 和 url：
  [{"title": "Supreme Court - English Wikipedia", "url": "https://en.wikipedia.org/wiki/..."},
   {"title": "組織名 - Wikipedia (日本語)", "url": "https://ja.wikipedia.org/wiki/..."},
   {"title": "組織名官方网站", "url": "https://www.example.com/"}]
  ❌ 禁止写成纯字符串数组 ["url1", "url2"]
  ❌ 禁止留空 []（至少包含Wikipedia和官网URL）
- collection_meta.data_sources 补充本次实际使用的来源类型
- collection_meta.completeness_score 自评分数（85-100）
- collection_meta.notes 简要说明数据来源和交叉验证情况

写入后必须执行（不可跳过）：
1. python scripts/ensure_utf8.py {filepath}
2. python .claude/skills/country-org-collector/scripts/validate_schema.py D:/claude-workspace/apec-osint-tool/output/jp/2026-06-09 --file {filepath}
3. 如有 ERRORS → 修复 → 重新验证 → 直到 0 errors
4. python .claude/skills/country-org-collector/scripts/validate_schema.py D:/claude-workspace/apec-osint-tool/output/jp/2026-06-09 --file {filepath} --score 更新 completeness_score

## 工具调用限制
- read_url 最多 10 次
- search 最多 10 次

完成后返回：org_id、最终 completeness_score、搜索来源数量、是否有字段缺失。
```

## 变量替换说明

| 变量 | 替换为 |
|------|--------|
| {org_id} | 如 JP-PARTY-005 |
| {org_name_en} | 如 Japanese Communist Party |
| {filepath} | 如 D:/claude-workspace/apec-osint-tool/output/jp/2026-06-09/orgs/JP-PARTY-005.json |

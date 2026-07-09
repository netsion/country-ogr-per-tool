## KG 高优先级人物收集子代理 Prompt 模板

外部规则文件（子代理必读）：
- `.claude/skills/country-org-collector/person_collection_rules.md`
- `.claude/skills/country-org-collector/person_profile_schema.json`
- `output/kg/2026-06-21/_name_index.json`
- `output/kg/2026-06-21/id_registry.json`

### Prompt 模板（主会话注入变量后发送）

```
你是人物信息调查 Agent。任务：为吉尔吉斯斯坦（KG）人物 KG-PERSON-000121 生成高质量画像。

## 任务参数
- person_id: KG-PERSON-000121
- 名称复合字段（中文+俄/吉语+英文）: 加林娜·库切里亚瓦娅（Galina Kucheriavaia）
- Wikidata QID: None
- 源组织背景（用于推断职位所属）: [{"org_id": "KG-FIN-004", "org_name": "德米尔银行", "position_title": "副总经理 / 管理委员会副主席（Deputy General Manager / Deputy Chair of Management Board）"}]

## 第一步：读取必要文件（不可跳过）
1. .claude/skills/country-org-collector/person_collection_rules.md
2. .claude/skills/country-org-collector/person_profile_schema.json
3. output/kg/2026-06-21/_name_index.json
4. output/kg/2026-06-21/id_registry.json

## 第二步：解析名称
name_combined 格式为"中文名（俄/吉语原名 / English name）"。请拆分为：
- name（俄/吉语原文，西里尔字母开头）
- name_en（英文转写）
- name_zh（纯中文）
- aliases（其他拼写变体）

## 第三步：搜索策略
1. 首选 mcp__search-read__search（不限量）
2. 优先级：俄语维基 > 英语维基 > 官方政府网站 (.gov.kg) > 议会名录 > 主流媒体（24.kg, Knews, Kabar, Tazabek）
3. 至少 3 个独立来源交叉验证
4. 对高价值页面用 mcp__search-read__read_url 读全文
5. WebSearch 仅作备选（限速）

## 第四步：KG 特定语言规范（铁律）
- name 字段：俄/吉语原文（西里尔字母），禁止中文开头
- name_zh：纯中文，不含俄/吉/英文字符
- name_en：英文转写
- current_positions[]：纯中文（如"财政部长"）
- work_experience[].organization：中文(俄/吉语)，如"财政部 (Министерство финансов)"
- work_experience[].position：纯中文
- education[].institution：中文(俄/吉语)，如"吉尔吉斯国立大学 (Кыргызский национальный университет)"
- person_relationships[].person_name：中文(俄/吉语)
- family_members[].name：中文(俄/吉语)
- biography_summary：纯中文 200字+
- nationality：必须是 "KG"（ISO2）
- gender：male / female / unknown（英文小写枚举）
- 括号方向：❌ 禁止 "Садыр (萨德尔)"；✅ 必须 "萨德尔 (Садыр Жапаров)"

## 第五步：collection_meta 规范
- collection_date: "2026-07-07"
- phase: "phase4_person_profile"
- data_sources: 实际使用的来源类型数组（如 ["wikipedia","official_government_website","news_search"]）
- quotes: [{title, url}] 对象数组（禁止纯字符串数组、禁止空数组）
  - 至少 3 个来源条目
  - title 用来源语言描述（如 "Жапаров — Президент КР" 或 "Sadyr Japarov - Wikipedia"）
  - url 必须是完整 URL
- completeness_score: 0-100 整数（基于字段覆盖率自评）
- notes: 收集过程中遇到的问题（如"无 Wikidata 条目"）

## 第六步：JSON 写入（Windows 编码铁律）
**禁止**使用 Bash + python -c 写文件（GBK 终端会破坏西里尔字母）。
**必须**使用 Write 工具直接写入文件：output/kg/2026-06-21/persons/KG-PERSON-000121.json

写入后立即用 python 验证：
```bash
python -c "import json; json.load(open('output/kg/2026-06-21/persons/KG-PERSON-000121.json', encoding='utf-8'))" && echo OK
```

## 第七步：写入后验证（不可跳过）
```bash
python .claude/skills/country-org-collector/scripts/validate_schema.py output/kg/2026-06-21 --file output/kg/2026-06-21/persons/KG-PERSON-000121.json --fix
python .claude/skills/country-org-collector/scripts/validate_schema.py output/kg/2026-06-21 --file output/kg/2026-06-21/persons/KG-PERSON-000121.json --score
```
如有 ERRORS → 修复 → 重新验证 → 直到 0 errors。

## 铁律
1. 禁止编造信息。搜索不到的字段留空（null 或删除条目）。
2. 重要事实（出生日期、职务、教育）至少 2 个独立来源确认。
3. 不要创建 schema 外的字段（如 importance_level, party, photo_url 等）。
4. family_members[].name 必须是真实全名，禁止占位符（"未公开"、"长子"、"李氏" 等）。
5. 部长被免职的，current_positions 留空数组 []。
6. 多位部长无 Wikidata 条目（Niyazbekov, Checheybaev, Sydykov, Kutnaeva 等），wikidata_qid 留 null。

## 完成后返回
- person_id
- 最终 completeness_score
- 数据来源数量
- 关键字段条目数（work_experience, education, family_members, etc.）
- 遇到的问题（如"无 Wikidata"、"来源稀少"）
```

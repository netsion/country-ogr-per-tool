# 人物调查规则手册（埃及 EG P4 子代理必读）

> 本文件是 P4 人物画像子代理的规则参考。执行步骤与路径由主会话 prompt 内联提供。

## 读取目标文件

- 人物画像写入：`output/eg/2026-11-16/persons/{person_id}.json`（若已存在则在其基础上丰富）
- 人物 Schema：`.agents/skills/country-org-collector/person_profile_schema.json`（先读）
- 组织画像（来源组织，用于 work_experience/relationship 交叉）：`output/eg/2026-11-16/orgs/{org_id}.json`
- ID 索引：`output/eg/2026-11-16/_name_index.json`

## 字段名严格约束（禁止自创）

| 数组 | 允许的字段名 |
|------|------|
| education[] | institution \| field \| degree \| start_date \| end_date |
| work_experience[] | organization \| position \| start_date \| end_date \| org_id |
| political_stances[] | topic \| stance_content \| date \| source |
| person_relationships[] | person_name \| person_id \| relationship_type \| description |
| family_members[] | name \| relationship \| industry_or_organization |
| major_achievements[] | date \| achievement \| organization |
| social_accounts[] | platform \| account_name \| url \| source \| source_note |
| collections/quotes | collection_meta.quotes = [{"title","url"}] 对象数组 ≥3 条 |

顶层仅保留 schema 定义字段（先读 person_profile_schema.json 确认）。

**必填与格式**：
- `name` 阿拉伯语原文；`name_zh` 中文；`name_en` 英文
- `biography_summary` **中文 ≥100 字**
- education[].institution / work_experience[].organization → **中文(阿拉伯语)** 格式，如 `开罗大学 (جامعة القاهرة)`
- work_experience[].org_id → 只在 _name_index.json 命中时填，否则 null（禁改 id_registry.json）
- political_stances[].source 必填 URL
- dates：birth_date 严格 YYYY-MM-DD（仅知年月 YYYY-MM-01）；education/work 起止 flexible（YYYY/YYYY-MM/YYYY-MM-DD）
- social_accounts[].source 整数码（twitter=3 facebook=6 instagram=8 youtube=9 linkedin=17 telegram=19）

## 搜索策略（埃及人物专项）

- 优先序：维基百科（英语→阿语）→ 官方页面（政府/机构官网人物页）→ 主流媒体（Ahram Online/Reuters/Egypt Today/Daily News Egypt）→ SIS 国家信息服务
- 阿拉伯语检索关键词用 `اسم الشخص + سيرة + مصر`；英语 `"{name_en}" Egypt biography`
- 政治人物：SIS（sis.gov.eg）人物档案、内阁官网、议会官网优先
- 军方人物：公开履历仅 mod.gov.eg/官方声明，搜不到留空，禁止编造
- 每人总请求 ≤12 次；请求间隔 ≥1 秒
- **工具优先级**：搜索一律 `mcp__search-read__search`，读取一律 `mcp__search-read__read_url`；仅失败/超时/返回空时才用 `mcp__web_reader__webReader` / `WebSearch` 备选

## 敏感纪律

- 前总统（穆巴拉克/萨达特/穆尔西）：生平与司法事件按公开文献双源记录，评价性表述引来源
- 穆兄会人物（巴迪耶/阿卜杜勒-哈克）：在押/继任争议注「据多方报道」；不编造组织细节
- 军情人物：公开信息极有限，履历留空不编造
- 政治立场：political_stances 只记有来源的公开表态，逐条给 source

## collection_meta 规范

- phase = "phase4_person_profile"；collection_date = 当天
- quotes ≥3 对象数组（维基+官网/新闻）
- data_sources 记录实际来源类型

## JSON 写入方式（Windows 阿文/中文必读）

- ❌ 禁止 `python -c` 内联写入（GBK 终端破坏阿文/中文）
- ✅ 用 Write 工具创建临时 .py 脚本到 `output/eg/2026-11-16/_tmp/`，脚本内 `json.dump(data, f, ensure_ascii=False, indent=2)` + `open(..., 'w', encoding='utf-8')`，Bash 执行后 `json.load()` 回读验证
- 中文引号用 `「」`；临时脚本只放 `_tmp/`，不删别人文件

## 写入后验证（不可跳过，--file 为相对路径）

```bash
python .agents/skills/country-org-collector/scripts/validate_schema.py output/eg/2026-11-16 --file persons/{person_id}.json
# ERRORS → 修复 → 0 errors
python .agents/skills/country-org-collector/scripts/validate_schema.py output/eg/2026-11-16 --file persons/{person_id}.json --score
```

## APEC 立场

人物画像无 apec_stance 字段；勿添加。涉及国际框架描述（如 INSEAD/国际组织任职）按来源记录即可。

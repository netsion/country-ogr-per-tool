# 人物画像字段规则手册

> 本文件是子Agent的规则参考。主会话 prompt 已包含执行步骤和具体路径，子Agent只需读取本文件获取字段约束、语言规范、格式要求。
>
> **本文件是纯规则参考，不含路径参数。搜索策略中的尖括号 `<name_en>` 等表示"用该人物的英文名"，由子Agent根据任务参数自行填入，不是模板变量。**

---

## 字段名严格约束（禁止自创字段名）

| 数组 | 允许的字段名（仅这些，不可添加其他） |
|------|------|
| work_experience[] | start_date \| end_date \| organization \| org_id \| position |
| education[] | institution \| degree \| field \| start_date \| end_date |
| political_stances[] | date \| topic \| stance_content \| source |
| person_relationships[] | person_id \| person_name \| relationship_type \| description |
| major_achievements[] | date \| achievement \| organization |
| social_accounts[] | platform \| account_name \| url \| source |
| family_members[] | person_id \| name \| relationship \| industry_or_organization |
| contacts[] | type \| value \| source |

**禁止添加任何不在上述列表中的字段**（如 description、organization_en、position_en、background、year 等）。

## 字段语言规范

| 字段 | 格式 | 示例 |
|------|------|------|
| name | 本国官方语言 | `"Nguyễn Thị Phương Thảo"` / `"이재명"` / `"Lawrence Wong"` |
| name_zh | 中文 | `"阮氏芳草"` / `"李在明"` |
| name_en | 英文 | `"Nguyen Thi Phuong Thao"` / `"Lee Jae-myung"` |
| biography_summary | 中文（200字+） | |
| current_positions[] | 纯中文字符串 | `"外交部副部长"` |
| work_experience[].position | 中文 | `"经济政策局局长"` |
| work_experience[].organization | 中文(本国官方语言) | `"外交部 (Bộ Ngoại giao)"`、`"三星电子 (삼성전자)"` |
| work_experience[].org_id | 已知用 ID，未知用 JSON null | `"KR-PARTY-001"` / `null`，禁止 `""` |
| education[].institution | 中文(本国官方语言) | `"首尔大学 (서울대학교)"` |
| education[].field | 中文 | `"经济学"` |
| political_stances[].topic | 中文 | `"半导体产业政策"` |
| political_stances[].stance_content | 中文 | |
| person_relationships[].person_name | 中文(本国官方语言) | `"黎明兴 (Lê Minh Hưng)"` |
| person_relationships[].description | 中文 | |
| person_relationships[].person_id | 已知用 ID，未知用 JSON null | 禁止 `""` |
| family_members[].name | 中文(本国官方语言) | `"阮氏金 (Nguyễn Thị Kim)"`（必须是真实全名） |
| family_members[].industry_or_organization | 中文 | `"越南外交部"` |
| major_achievements[].achievement | 中文 | |
| major_achievements[].organization | 中文(本国官方语言) | `"大韩民国国会 (대한민국 국회)"` |
| social_accounts[].platform | 英文枚举值 | 见枚举表 |
| family_members[].relationship | 英文枚举值 | 见枚举表 |

**括号方向**：中文在前，括号附本国官方语言。禁止 `"이재명 (李在明)"`。

**英语国家人名中文化**：当本国官方语言为英语时（NZ/AU/US等），family_members[].name 和 person_relationships[].person_name 仍需遵循"中文(英文)"格式。中文部分使用目标国本地华文媒体标准译名；无标准译名时使用通用音译（如 "唐·布雷德 (Don Braid)"）。禁止仅写英文名。

## 枚举值速查

- social_accounts[].platform: `twitter_x` | `facebook` | `instagram` | `youtube` | `linkedin` | `telegram` | `tiktok` | `threads` | `mastodon` | `wechat` | `weibo` | `github` | `gitlab` | `medium` | `substack` | `other`
- family_members[].relationship: `spouse` | `father` | `mother` | `son` | `daughter` | `brother` | `sister` | `grandfather` | `grandmother` | `uncle` | `aunt` | `cousin` | `other`
- person_relationships[].relationship_type: `spouse` | `parent` | `child` | `sibling` | `mentor` | `mentee` | `colleague` | `superior` | `subordinate` | `political_ally` | `political_rival` | `associate` | `other`
- education[].degree: `primary` | `high_school` | `associate` | `bachelor` | `master` | `doctorate` | `professional` | `other` | `null`
- contacts[].type: `email` | `phone` | `fax` | `website` | `other`
- gender: `male` | `female` | `non_binary` | `unknown`

## 常见错误对照表

| 路径 | 正确 | 错误 |
|------|------|------|
| political_stances[] 立场内容 | `stance_content` | stance, position, content |
| major_achievements[] 成就描述 | `achievement` | description, title, content |
| person_relationships[] 关系类型 | `relationship_type` | relationship |
| social_accounts[] 平台 | `twitter_x`（小写英文） | "Facebook", "X (Twitter)" |
| family_members[] 关系 | `spouse`（英文 enum） | "妻子", "配偶", "儿子" |
| degree 非标准值 | `"bachelor"` / `null` | "学士", "학사", "undergraduate" |
| platform 大写 | `"facebook"` | "Facebook", "Naver Blog" |
| relationship_type 中文 | `"colleague"` | "同僚", "上司" |
| work_experience 日期范围 | start_date + end_date 各自独立 | `"1998-2002"` 写在单个字段 |
| nationality | `"KR"` / `"NZ"` | "韩国", "日本" |
| org_id / person_id | `"KR-PARTY-001"` / `null` | `""` 空字符串 |
| top-level 多余字段 | 仅 schema 定义字段 | photo_url, importance_level, party |
| person name 格式 | `"이재명"`（本国官方语言） | `"李在明 (이재명)"`（中文开头） |

## 必填字段规则（无法填写则删除整条，不要写空壳条目）

- `family_members[].name` — 必须是真实全名。无效占位符（`未公开`/`不详`/`配偶`/`长子`/`李氏`/`（一子）`等）→ 删除该条
- `political_stances[].stance_content` — 没有内容就不写这条
- `major_achievements[].achievement` — 没有描述就不写这条
- `major_achievements[].organization` — 当成就关联的组织可从 achievement 文本、work_experience、biography 等已有数据中推断时，必须填写（格式：中文(本国官方语言)），不可一律填 null

## 写入前自检清单（逐条验证）

1. name 是否为本国官方语言？（不是中文开头）
2. name_zh 是否为纯中文？
3. person_relationships[].person_name / family_members[].name 是否为"中文(本国官方语言)"格式？
4. work_experience[].organization / education[].institution 是否为"中文(本国官方语言)"格式？
5. 所有 degree 值是否在枚举列表内？（中文/韩文 degree → 改为英文 enum 或 null）
6. 所有 platform 值是否小写英文枚举？
7. nationality 是否为 ISO 3166-1 alpha-2？
8. 是否存在 schema 外的 top-level 字段？有则删除
9. 是否存在 work_experience/education 条目中的额外字段？有则删除
10. 所有日期字段是否独立（非范围格式）？

## ID 查找规则

1. 读取 `_name_index.json`（路径由主会话 prompt 提供）
2. 每个 organization / person_name 先查 index
3. 命中 → 使用对应 ID
4. 未命中 → 写 `null`（JSON null，禁止空字符串 `""`）
5. 禁止自创 ID 格式

## collection_meta 规范

- `phase` = `"phase4_person_profile"`
- `collection_date` = 当天日期 YYYY-MM-DD
- `quotes` = 对象数组，每条含 title 和 url：
  ```json
  [{"title": "页面标题", "url": "https://..."}]
  ```
  禁止纯字符串数组 `["url1"]`，禁止留空 `[]`
- `data_sources` = 本次实际使用的来源类型
- `notes` = 中文，简要说明数据来源确认情况、关键发现、存疑字段等

## JSON 编码规则

- 中文引号用 `「」`，不要使用 ASCII 双引号 `"..."` 作为中文引号
- 写入前确保所有 JSON 字符串值中的引号已正确转义或替换

## 搜索策略参考

多语言搜索按此顺序：目标国语言 → 英语 → 中文

| 字段 | 英语搜索 | 目标国语言搜索 |
|------|---------|--------------|
| biography | `<name_en> biography career` | `<name_local> 프로필 약력` (韩) / `<name_local> プロフィール 経歴` (日) |
| education | `<name_en> education university degree` | `<name_local> 学历 출신대학` (韩) |
| career | `<name_en> career history appointment` | `<name_local> 经历 발탁` (韩) |
| family | `<name_en> family spouse children` | `<name_local> 家族 배우자` (韩) |
| stance | `<name_en> policy stance speech` | `<name_local> 政策立场 정책 입장` (韩) |
| social | `<name_en> site:linkedin.com` 等 | — |

社交媒体搜索（每个人物必做）：
```
"<name_en>" site:facebook.com
"<name_en>" site:twitter.com OR site:x.com
"<name_en>" site:linkedin.com
"<name_en>" site:instagram.com
"<name_en>" site:tiktok.com
"<name_en>" site:youtube.com
```

## 详情获取（搜索后必做）

搜索只返回标题和摘要。必须用 `mcp__search-read__read_url` 读取高价值来源全文：
- 每次收集至少读取 3 个独立来源的完整页面
- 优先级：Wikipedia（英文本地语） > 政府名录/议会页 > 政党官网 > 主流新闻报道
- 用于交叉验证关键事实（日期、职务、家庭关系等）

高价值来源类型：
- 政府名录 → 政府官员
- 议会名录 → 国会议员
- 大学官网 leadership 页 → 学术领袖
- 企业官网 leadership/team 页 → 企业高管
- Wikipedia（目标国语言 + 英语 + 中文）

中文名（name_zh）获取优先级：
1. Wikidata `zh` label
2. Wikipedia 中文版 sitelink
3. 该国华文媒体报道
4. Web 搜索 `<person_name> 中文名`

非中文母语国家人名：不得使用大陆新华社音译，必须使用目标国家本地华文媒体标准译名。详见 `malay_name_zh_guide.md`。

## JSON 写入方式

**禁止使用 `python -c "..."` 传递完整 JSON 内容**。Shell 转义会导致中文引号、反斜杠、长文本解析失败（实测造成 260s 重试浪费）。

正确写入方式（按优先级）：
1. **Write 工具**：直接将 JSON 字符串写入目标文件路径
2. **先写脚本再执行**：用 Write 将 Python 脚本写入临时文件，再用 Bash 执行该脚本
3. **Bash + heredoc**：如必须用 Bash，用 `cat << 'EOF' > filepath` heredoc 传递（注意单引号 EOF 防止变量展开）

## 铁律

- 禁止编造信息，搜索不到则留空
- 重要信息至少 2 个独立来源确认

---
name: country-org-collector
description: 系统化收集、整理和分析指定国家的重点组织机构信息，覆盖政府、企业、NGO、学术机构、媒体等。当用户要求收集某国组织信息、研究机构、构建组织目录、映射机构关系或创建知识图谱时触发。
---

# 国家组织机构收集器（5 Phase 子代理编排流水线）

## §1 铁律：信息可靠性

**本 skill 产出的数据用于智库级研究，必须保证情报可靠性。以下为不可违反的铁律：**

1. **禁止编造信息** — 所有写入 JSON 的数据必须有可追溯的来源依据。不可凭空捏造人物姓名、职位、事件日期、数据数字等任何信息。
2. **来源可追溯** — 每条信息均需记录来源：`recent_events` 必须有 `source` URL；`political_stances` 必须有 `source`；`key_people`、`digital_assets` 等必须标注 `source` 字段。
3. **无法确认则留空** — 搜索不到可靠来源的信息时，宁可留空（`null`/`[]`），绝不猜测或编造。空字段不影响完整度评分，但虚假信息会破坏整个数据集的可信度。
4. **区分事实与推断** — 数据中只记录已确认的事实。如需添加分析性推断（如"可能影响..."），必须在 `impact` 等明确允许分析性内容的字段中使用，且应注明推断依据。
5. **交叉验证** — 重要信息（人物职位、组织关系、重大事件）应尽量从至少两个独立来源交叉确认。单一来源的可疑数据应标注不确定性。

> **违规后果**：一条未经验证的虚假信息可能导致基于整个数据集的分析结论失效。**宁可遗漏，不可编造。**

## §2 数据质量守则

> 以下规则来自 MY/SG/KR 数据集的实际收集教训，适用于所有国家。

1. **person_id 验证**（Phase 3 Agent 丰富后必做）：逐一检查 key_people 的 person_id 是否指向正确人物——比对 person JSON 中 name_en 与 org key_people 的 name
2. **人物去重**（Phase 4 创建前）：先 `grep -r "Q{QID}" persons/` 检查是否已有档案。发现重复时保留内容更丰富的档案并合并，更新所有引用
3. **名称连锁更新**（修改人物名称时）：修正名称后必须 grep 旧名更新全部位置：person 文件（name/name_zh/biography_summary）、org 文件（key_people[]/departments[]/recent_events[]/core_business）、其他 person 文件（person_relationships[]）、_index.json
4. **key_people 命名格式**：`中文名 (English name)`，如 `阿末扎希·哈米迪 (Ahmad Zahid Hamidi)`
5. **JSON 编码**：中文引号用 `「」`；写入后立即 `json.load()` 验证；`end_date` 只允许 `YYYY-MM-DD`/`YYYY-MM`/`YYYY` 或 `null`
6. **非中文母语人名**：不得使用 Wikidata 机器人批量中文标签（大陆新华社标准），必须使用目标国家本地华文媒体标准译名。详见 `malay_name_zh_guide.md`。验证：`"{name_en} site:sinchew.com.my"`

---

## §3 Phase 摘要

针对指定国家，**按 5 个 Phase 执行**收集组织机构与人物信息：

| Phase | 名称 | 执行者 | 产出 |
|-------|------|--------|------|
| **P1** | 广度扫描 | **子代理**（单次） | `_target_orgs.json`（组织清单） |
| **P2** | 数据缓存 + 骨架生成 | Python 脚本 | `_cache/` + `orgs/` 骨架画像（completeness 30-55） |
| **P3** | Agent 组织深度丰富 | **子代理**（每组织一个，最多 2 并行） | 完整组织画像（completeness 目标 85+） |
| **P4** | Agent 人物收集与深度调查 | **子代理**（每人物一个，串行） | `person_list.json` + 完整人物画像（completeness 目标 85+） |
| **P5** | 验证收尾 | Python 脚本 + 主会话 | Schema 校验 + 索引 + 完整性报告 |

**核心原则**：主会话是编排者（读进度 → 派子代理 → 验证结果 → 更新进度），子代理是执行者（搜索 + 读取 + 写入）。脚本负责结构化数据缓存（Wikidata/Wikipedia），子代理负责所有非结构化数据搜索和综合（官网、新闻、政府目录、社交媒体）。

## §4 子代理编排架构

**核心思路**：主会话只做编排和进度管理，所有重度搜索/读取/写入操作由子代理执行。主会话上下文永远保持轻量，避免上下文压缩和数据丢失。

### 主会话职责（编排者）

- 读取进度文件，确定断点
- 构建子代理 prompt（从模板注入变量）
- 派发子代理（Agent 工具）
- 等待子代理完成，验证输出文件
- 更新 `_phase_progress.json`
- 处理子代理失败（重试或跳过）

### 子代理职责（执行者）

- 读取骨架文件 / 缓存数据
- 执行所有 Web 搜索、页面读取、数据综合
- 写入完整画像文件
- 运行 `validate_schema.py` 验证
- 返回执行摘要给主会话（成功/失败 + completeness_score）

### 子代理调用规范

```
工具：Agent（subagent_type: "general-purpose"）
prompt 结构：
  1. 角色定义（你是组织/人物信息丰富 Agent）
  2. 任务目标（org_id/name/completeness 目标）
  3. 文件路径（输入骨架 + 输出位置 + schema 路径）
  4. 搜索策略（§13.2 / §14.2）
  5. 字段名约束（§13.3 / §14.3）
  6. 写入后验证指令（validate_schema.py）
  7. 网络配置提醒（代理 + User-Agent）
  8. 工具选择策略（首选 mcp__search-read，备选 WebSearch）
```

### 并行控制（仅 P3）

- **最大并行数**：2 个子代理同时运行
- **限速共享**：Wikidata SPARQL 5 次/分钟、搜索引擎 30 次/分钟是全局配额，并行子代理各自控制间隔
- **失败处理**：单个子代理失败不阻塞另一个；失败的组织放入重试队列

## §5 触发条件

当用户提出以下类型请求时激活此 skill：

- 要求"收集某国组织"或"查找某国机构"
- 想要研究或描绘某国的组织机构全景
- 请求建立某国（尤其是 APEC 成员）的组织目录
- 想要映射组织间的关系（知识图谱）
- 提到"分析某国组织"、"机构画像"、"组织情报"
- 提到 APEC、OSINT、机构研究、组织情报等关键词

## §6 APEC 成员经济体对照表

当目标国家不在下表中时，仍可继续执行，但需提示该国非 APEC 成员。

| 经济体 | ISO 代码 | Wikidata QID | OpenCorporates 代码 |
|--------|----------|-------------|-------------------|
| 澳大利亚 Australia | AU | Q408 | au |
| 文莱 Brunei | BN | Q921 | bn |
| 加拿大 Canada | CA | Q16 | ca |
| 智利 Chile | CL | Q298 | cl |
| 中国 China | CN | Q148 | cn |
| 中国香港 Hong Kong | HK | Q8646 | hk |
| 印度尼西亚 Indonesia | ID | Q252 | id |
| 日本 Japan | JP | Q17 | jp |
| 韩国 South Korea | KR | Q884 | kr |
| 马来西亚 Malaysia | MY | Q833 | my |
| 墨西哥 Mexico | MX | Q96 | mx |
| 新西兰 New Zealand | NZ | Q664 | nz |
| 巴布亚新几内亚 Papua New Guinea | PG | Q691 | pg |
| 秘鲁 Peru | PE | Q419 | pe |
| 菲律宾 Philippines | PH | Q928 | ph |
| 俄罗斯 Russia | RU | Q159 | ru |
| 新加坡 Singapore | SG | Q334 | sg |
| 中国台北 Chinese Taipei | TW | Q865 | tw |
| 泰国 Thailand | TH | Q869 | th |
| 美国 United States | US | Q30 | us |
| 越南 Vietnam | VN | Q881 | vn |

## §7 数据输出语言规范

**所有 JSON 输出文件中的描述性文本必须使用中文。**

### 适用字段

以下字段的值必须使用中文撰写（不可使用英文或混合语言）：

| 阶段 | 字段 | 说明 |
|------|------|------|
| **组织画像** | `recent_events[].title` | 事件标题，如 "GIC发布2024/25年度报告，20年年化回报率5.7%" |
| **组织画像** | `recent_events[].description` | 事件描述 |
| **组织画像** | `recent_events[].impact` | 影响评估 |
| **组织画像** | `key_people[].title_description` | 职位描述，如 "贸工部部长，兼任副总理和MAS主席" |
| **组织画像** | `key_people[].description` | 人物描述 |
| **组织画像** | `related_entities[].org_description` | 关联描述，如 "新加坡央行和金融监管机构" |
| **组织画像** | `core_business` | 核心业务描述 |
| **组织画像** | `apec_stance` | APEC立场描述 |
| **组织画像** | `digital_assets[].name` | 资产名称，如 "MTI官方网站" |
| **组织画像** | `digital_assets[].description` | 资产描述 |
| **人物画像** | `biography_summary` | 人物生平概述 |
| **人物画像** | `major_achievements[].achievement` | 成就描述 |
| **人物画像** | `political_stances[].topic` | 政治议题，如 "住房政策" |
| **人物画像** | `political_stances[].stance_content` | 立场内容 |
| **人物画像** | `person_relationships[].description` | 关系描述 |
| **人物画像** | `work_experience[].position` | 职位名称 |

### 保留英文的字段

以下字段保持英文或原始语言：
- `basic_info.name_en` — 英文名
- `basic_info.name_zh` — 中文名（可空）
- `basic_info.website` — URL
- `social_accounts.url` — URL
- `recent_events[].source` — 来源 URL
- `political_stances[].source` — 来源 URL
- `collection_meta` — 元数据

### 混合情况处理

- **人名**：中文优先，括号附英文。如 `"李显龙 (Lee Hsien Loong)"`
- **组织名**：`name_zh` 为中文，`name_en` 为英文
- **专业术语**：可用英文+中文注释，如 `"AI人工智能"`、`"GDP国内生产总值"`

> **⚠️ 非中文母语国家人名音译**：对马来语、印尼语、泰语等非中文人名，必须使用**该国本地华文媒体的标准译法**，不得使用大陆新华社音译。马来西亚华文媒体音译标准详见 `malay_name_zh_guide.md`。

---

## §8 组织分类体系

每个收集到的组织必须标注且仅标注一个主分类：

### ID 生成规则

**格式**：`{ISO2}-{TYPE}-{SEQ}`

| 组成 | 说明 |
|------|------|
| ISO2 | 组织所属国家的 ISO 3166-1 alpha-2 代码（见 APEC 对照表） |
| TYPE | 组织主分类代码：GOV / SOE / CORP / NGO / ACAD / MEDIA / FIN / INTL / PARTY / MIL |
| SEQ | 3 位顺序号，按 `{ISO2}-{TYPE}` 组合内递增，从 001 开始 |

**跨国籍组织**：按总部所在国或主要活动国分配 ISO2 前缀（如马来西亚的 DAP 用 `MY-PARTY-001`，不用 `SG-PARTY-xxx`）。

**注册表**：`output/{country_iso}/{date}/id_registry.json`

> **所有新 ID 必须先在注册表中查询和注册，再写入 profile**。注册表包含：
> - `registry`：已分配 ID 列表（org_id / name / org_type / status）
> - `counters`：按 `{ISO2}-{TYPE}` 分组的当前最大序号
>
> 新建 ID 时：读取 counters → 递增 → 写回 registry → 再写入 profile。

**related_entities 中的 org_id 规则**：
- 引用的组织如已在 registry 中，直接使用已注册的 ID
- 引用的组织如不在 registry 中，先按上述规则生成新 ID 并注册到 registry
- 不允许 `org_id: null`，所有 related_entity 必须有 ID

| 分类代码 | 标签 | 说明 |
|---------|------|------|
| GOV | 政府机构 | 国家元首、内阁、各部委、行政机关、法定机构、监管机构 |
| SOE | 国有企业 | 政府控股的企业和公司 |
| CORP | 企业公司 | 上市公司及大型私营企业 |
| NGO | 非政府组织 | NGO、慈善机构、基金会 |
| ACAD | 学术机构 | 大学、研究所、智库 |
| MEDIA | 媒体机构 | 新闻社、广播公司、出版商 |
| FIN | 金融机构 | 银行、投资公司、保险公司 |
| INTL | 国际组织 | 总部位于该国的多边组织、区域机构 |
| PARTY | 政党 | 主要政党 |
| MIL | 军事安全 | 武装力量、情报机构、安全部门 |

> **Wikidata P31 值映射、GOV 子分类详见 `sparql_org_templates.md`**。
> **代理设置、Windows 编码、工具选择策略详见 `network_config.md`**。

## §9 快速启动

**执行前必做**：确认代理可用 `curl --proxy "http://10.11.204.68:8081" -s "https://en.wikipedia.org" | head -1`，或设置环境变量 `export https_proxy=http://10.11.204.68:8081`

**"收集{某国}的组织信息"** → Phase 1 → Phase 2 → Phase 3

1. Phase 1：Agent 广度扫描，输出 `_target_orgs.json`
2. Phase 2：运行脚本 `verify_qids.py` + `batch_collect.py` + `generate_profiles.py`，输出骨架画像
3. Phase 3：Agent 逐组织深度丰富，目标 completeness 85+

**"深度收集{某组织/某类别}"** → Phase 2 + Phase 3

1. 运行 `verify_qids.py` + `batch_collect.py` + `generate_profiles.py`
2. Agent 逐组织深度丰富

**"收集人物信息"** → Phase 4

1. 从已完成的组织画像 key_people 提取人物
2. Agent 逐人物深度调查

**"验证数据"** → Phase 5

1. 运行 `validate_schema.py` 校验
2. 运行 `generate_index.py` 生成索引

---

# §10 通用规则

## 日期格式规范

所有日期字段分为两类：

**精确日期（strict）** — 必须 `YYYY-MM-DD`：
- 组织：`founded_date`、`recent_events[].date`、`collection_date`
- 人物：`birth_date`、`collection_date`
- 仅知年份时用 `YYYY-01-01`，仅知年月时用 `YYYY-MM-01`

**时间段日期（flexible）** — 允许 `YYYY` / `YYYY-MM` / `YYYY-MM-DD`：
- `education[].start_date` / `end_date`
- `work_experience[].start_date` / `end_date`
- `political_stances[].date`
- `major_achievements[].date`
- 按实际已知最高精度填写，未知填 `null`

> **写入规则**：从 Wikidata/Wikipedia 提取日期时，保留源数据的精度。不要将 `2005` 补全为 `2005-01-01`，也不要截断 `2022-06-13` 为 `2022-06`。

## 数据源优先级

1. **官方政府注册库**
2. **政府官方目录**（该国政府机构人员名录——如 SG 的 sgdi.gov.sg。提供完整的官员名单、职务、联系方式，比 Wikipedia 更新更准确。优先用于 GOV 类型组织的 key_people 和 departments 收集。）
3. **Wikidata**（结构化，通过本地 curl + 代理）
4. **Wikipedia REST API**（结构化摘要 + Wikidata QID）
5. **Wikipedia 页面**
6. **DBpedia SPARQL**（补充属性，仅本地 curl）
7. **OpenCorporates**（企业）
8. **官方网站**
9. **新闻报道**
10. **其他网络来源**

## 异常处理

- **连接重置（WinError 10054 / curl:35）**：本地未配置代理，需设置 `http_proxy`/`https_proxy` 环境变量或在请求中指定 `--proxy`
- **403 Forbidden**：本地 Python urllib 缺少 User-Agent header，需添加 `headers={'User-Agent': 'Mozilla/5.0'}`
- **SPARQL 超时**：简化查询（降低 LIMIT、去掉 P279*、缩小 VALUES）
- **页面 404**：标记 `source_unavailable`，跳到下一来源
- **数据冲突**：记录所有值和来源，按优先级选主值
- **MCP 工具失败（502 / 无输出）**：切换到本地 curl + 代理重试
- **Cloudflare JS Challenge**：直接跳过该来源，标记 `source_blocked_cloudflare`，改用 Wikipedia / 新闻搜索获取替代信息。不尝试绕过。
- **JSON 编码错误**：Agent 生成的内容可能包含 Unicode 弯引号（U+201C `"` 和 U+201D `"`），修复方法：将 `“` 和 `”` 替换为 `\"` 或直接删除。或运行 `validate_schema.py --fix`

## 工具选择

| 优先级   | 搜索工具                                  | 读取工具                                |
| -------- | ----------------------------------------- | --------------------------------------- |
| **首选** | `mcp__search-read__search`（keyword参数） | `mcp__search-read__read_url`（url参数） |
| **备选** | `WebSearch`（query参数）                  | `mcp__web_reader__webReader`（url参数） |

> **回退规则**：当首选工具请求失败（报错、超时、返回空）时，自动切换到备选工具。

## 变量约定

| 变量 | 含义 | 示例 |
|------|------|------|
| `{iso}` | 国家 ISO 3166-1 alpha-2 代码（小写），用于目录名和脚本参数 | `sg`, `my`, `kr` |
| `{COUNTRY}` | 国家英文名，用于搜索关键词 | `Singapore`, `South Korea` |
| `{date}` | 收集日期 `YYYY-MM-DD` | `2026-04-28` |
| `{COUNTRY_QID}` | 目标国家的 Wikidata QID（见 APEC 对照表） | `Q334`（新加坡） |
| `{qid}` | Wikidata 实体 ID | `Q115727460` |
| `{org_name_en}` | 组织英文名（用于搜索关键词） | `Temasek Holdings` |
| `{name_en}` | 人物英文名（用于搜索关键词） | `Lawrence Wong` |

> 路径中的 `{country_iso}` 等同于 `{iso}`，均指国家 ISO alpha-2 小写代码。

## 无 Wikidata QID 降级策略

当人物或组织没有 Wikidata QID 时，按以下降级路径处理：

| Level | 条件 | 行为 |
|-------|------|------|
| **L1** | 有 Wikidata QID | 脚本自动缓存 EntityData + Wikipedia 摘要，Agent 在此基础上丰富 |
| **L2** | 无 QID，但 Wikipedia 有页面 | 通过 Wikipedia REST API 搜索名字 → 获取 `wikibase_item` → 回到 L1 |
| **L3** | 无 QID，无 Wikipedia 页面 | 脚本跳过，Agent 直接基于 Web 搜索生成画像 |

## 完整度评分（completeness_score）

completeness_score（0-100）衡量画像数据完整程度。

**快速估算法**：已填非空字段数 / 总可选字段数 × 100。核心描述字段（biography_summary、core_business）权重更高。

### 组织画像关键得分项

| 得分区间 | 条件 |
|---------|------|
| 0-30 | 仅 basic_info，无 key_people/social_accounts/recent_events |
| 30-50 | 有 basic_info + 部分 key_people，无 recent_events |
| 50-70 | 有 key_people + social_accounts + 部分 recent_events |
| 70-85 | 有 recent_events + related_entities + core_business |
| 85-100 | 所有主要字段非空，recent_events ≥ 3，key_people ≥ 3 |

**必须项**（缺失则扣分严重）：`key_people`、`social_accounts`、`recent_events`、`core_business`。

### 人物画像关键得分项

| 得分区间 | 条件 |
|---------|------|
| 0-30 | 仅 name + nationality + gender |
| 30-50 | 有 biography_summary（英文）但缺 education/work_experience |
| 50-70 | 有 biography_summary（中文）+ 部分 work_experience |
| 70-85 | 有 work_experience（≥ 2 条）+ education + 部分 social_accounts |
| 85-100 | 所有主要字段非空，biography ≥ 100 字中文，social_accounts ≥ 2 |

**必须项**：`biography_summary`（中文、> 100 字）、`work_experience`（≥ 2 条完整记录）、`social_accounts`（≥ 2 个）。

## 限速总表

| 数据源 | 最大频率 | 最小间隔 |
|--------|---------|---------|
| Wikidata SPARQL | 5 次/分钟 | 12 秒 |
| 搜索引擎 | 30 次/分钟 | 1 秒 |
| Wikipedia 页面 | 20 次/分钟 | 3 秒 |
| OpenCorporates API | 500 次/天 | 5 秒 |
| 普通网页 | 30 次/分钟 | 1 秒 |

## 上下文中断恢复

当对话因上下文耗尽而中断并恢复时，按以下步骤接续工作：

1. **读取进度文件**：检查 `_phase_progress.json`（P3/P4 阶段进度）
2. **确定断点**：对比 `remaining` 列表和已输出文件，找出未完成的组织/人物
3. **从中断处继续**：跳过已完成的条目，从下一个开始派发子代理
4. **验证数据一致性**：运行 `validate_schema.py` 确认已写入文件符合 schema

> **编排模型优势**：主会话上下文极轻（仅进度 JSON + 编排指令），几乎不会触发上下文压缩。每个子代理独立运行，完成后上下文自动释放，不污染主会话。

---

# §11 Phase 1：广度扫描（子代理执行）

**目标**：快速梳理目标国家的核心机构清单，输出含基础信息的结构列表。

**执行方式**：主会话创建输出目录后，派发单个子代理完成全部扫描工作。

## 11.1 主会话编排步骤

1. 确认收集范围参数（国家、类别、深度等）
2. 创建输出目录：`output/{country_iso}/{YYYY-MM-DD}/`
3. 派发子代理执行扫描（使用 §11.2 prompt 模板）
4. 等待子代理完成，验证 `_target_orgs.json` 存在且 JSON 合法
5. 进入 Phase 2

## 11.2 子代理 Prompt 模板

```
你是国家组织机构广度扫描 Agent。任务：为 {COUNTRY}（ISO: {iso}）生成组织机构清单。

输出目录：{output_dir}
输出文件：{output_dir}/_target_orgs.json
Schema 文件：.claude/skills/country-org-collector/org_list_schema.json

收集范围（scope）：{scope}
  - scope=all：执行全部 SPARQL 模板（A-H）+ 全部 11 组搜索关键词
  - scope=GOV：只执行模板 H（国家权力机构）+ 搜索关键词 1-4（GOV 相关）
  - scope=GOV,SOE：执行模板 H + SOE 对应模板 + 搜索关键词 1-4 + 5/11
  - scope=GOV,CORP,FIN：类推

步骤 1 — Wikidata 结构化查询（按 scope 选择模板）：
  端点：https://query.wikidata.org/sparql
  调用方式：本地 curl + 代理 `--proxy "http://10.11.204.68:8081"`
  限速：请求间隔 ≥12 秒，每分钟 ≤5 次
  SPARQL 模板详见：.claude/skills/country-org-collector/sparql_org_templates.md
  重要：避免 wdt:P31/wdt:P279*（传递子类），改用 wdt:P31 + VALUES 列表

步骤 2 — Web 搜索补充（按 scope 选择关键词，使用 mcp__search-read__search，备选 WebSearch）：
  GOV 相关：
  1. "government ministries list {COUNTRY} executive branch cabinet"
  2. "{COUNTRY} parliament legislature judicial system courts"
  3. "list of government agencies {COUNTRY} statutory boards"
  4. "{COUNTRY} government directory officials"
  企业相关（scope 含 SOE/CORP 时）：
  5. "largest companies {COUNTRY} top"
  11. "state owned enterprises {COUNTRY}"
  NGO 相关（scope 含 NGO 时）：
  6. "major NGOs {COUNTRY} nonprofit organizations"
  学术相关（scope 含 ACAD 时）：
  7. "top universities {COUNTRY} research institutions"
  媒体相关（scope 含 MEDIA 时）：
  8. "major media organizations {COUNTRY} news outlets"
  金融相关（scope 含 FIN 时）：
  9. "largest banks financial institutions {COUNTRY}"
  政党相关（scope 含 PARTY 时）：
  10. "political parties {COUNTRY} major"

步骤 3 — 重点组织验证：
  对每类前 3 个（概览）或前 10 个（深度）组织，读取 Wikipedia/官网详情页验证
  限速：页面间隔 3-5 秒

步骤 4 — 汇总输出：
  1. 读取 org_list_schema.json 了解输出格式
  2. 生成 _target_orgs.json，确保符合 schema
  3. 写入到 {output_dir}/_target_orgs.json

数据可靠性铁律：
- 禁止编造信息，所有数据有可追溯来源
- 无法确认则留空
- 交叉验证重要信息

完成后返回：组织总数、按类别统计、是否有需人工确认的条目。
```

> **Phase 1 完成 → Phase 2**：按顺序运行 `verify_qids.py` + `batch_collect.py` + `generate_profiles.py`。

---

# §12 Phase 2：数据缓存 + 骨架生成

**目标**：验证 QID、批量采集结构化数据到缓存、从缓存生成骨架画像。

**输入**：Phase 1 的 `_target_orgs.json`

**输出**：`_cache/` 缓存目录 + `orgs/` 骨架画像（completeness 30-55）

## 12.1 脚本执行步骤

主会话按以下顺序执行脚本：

```bash
# Step 1: QID 验证
python .claude/skills/country-org-collector/scripts/verify_qids.py output/{iso}/{date}

# Step 2: 批量数据采集（Wikidata EntityData + Wikipedia REST API）
python .claude/skills/country-org-collector/scripts/batch_collect.py output/{iso}/{date}

# Step 3: 从缓存生成骨架画像 + 解析 key_people QID 为姓名
python .claude/skills/country-org-collector/scripts/generate_profiles.py output/{iso}/{date}

# Step 4: 生成名称索引（P3/P4 子代理用于 ID 查找）
python .claude/skills/country-org-collector/scripts/generate_name_index.py output/{iso}/{date}
```

> 脚本自动处理代理配置（含直连 fallback）、断点续跑、限速。代理不通时自动切换直连模式；缓存获取失败时生成最小骨架（标记 `source_unavailable`），由 P3 子代理通过 MCP 工具补全。`generate_profiles.py` 已内置 `resolve_key_people` 功能。

## 12.2 预期产出

- `_cache/` 目录：`{QID}.json`（含 wikidata + wikipedia 数据）
- `orgs/` 目录：`{org_id}.json` 骨架画像，含 basic_info、部分 social_accounts（来自 Wikidata）、key_people（已解析为姓名）、related_entities
- `id_registry.json`：已注册的 org_id 和 person_id
- 骨架画像 `core_business` 为 `null`（子代理在 Phase 3 填充）
- 骨架画像 `collection_meta.phase` 为 `"phase2_skeleton"`
- 骨架画像 completeness_score 预期 30-55

> **Phase 2 完成 → Phase 3**：主会话逐组织派发子代理深度丰富，目标 completeness 85+。

---

# §13 Phase 3：子代理组织深度丰富（最多 2 并行）

**目标**：对 Phase 2 产出的骨架画像，通过子代理逐组织深度丰富，目标 completeness 85+。

**触发方式**：Phase 2 完成后自动建议。或用户说"丰富组织信息"、"补充组织缺失字段"。

**执行方式**：主会话编排，每组织派发一个子代理，**最多 2 个子代理同时运行**。

## 13.1 主会话编排循环

```
1. 读取 _phase_progress.json（如不存在则创建，remaining = 所有骨架画像 org_id）
2. 初始化进度文件：
   {
     "phase": "P3_org_enrichment",
     "started_at": "{当前时间}",
     "last_updated": "{当前时间}",
     "completed": [],
     "remaining": ["KR-GOV-001", "KR-GOV-002", ...],
     "current": [],
     "failed": []
   }
3. WHILE remaining 不为空:
   a. 从 remaining 中取最多 2 个 org_id
   b. 为每个 org_id 读取骨架文件，构建子代理 prompt（§13.3）
   c. 同时派发 1-2 个 Agent 调用（在同一条消息中发送多个 Agent 工具调用）
   d. 等待所有子代理返回
   e. 如子代理失败（API 错误/超时）→ 自动重试 1 次（同一 prompt）
   f. 验证每个子代理的输出：
      - 文件 orgs/{org_id}.json 存在且 JSON 合法
      - completeness_score ≥ 70（低于则记录警告）
   g. 运行脚本：
      python .claude/skills/country-org-collector/scripts/resolve_ids.py {output_dir}
      python .claude/skills/country-org-collector/scripts/generate_name_index.py {output_dir}
   h. 更新 _phase_progress.json：
      - 成功：从 remaining 移到 completed
      - 失败（含重试后仍失败）：从 remaining 移到 failed，记录错误原因
   i. 报告本轮进度（已完成/总数）
4. 全部完成后报告汇总
```

## 13.2 按来源阅读策略（子代理内部执行）

**核心原则**：一次阅读/搜索的结果应同时填充多个字段，避免逐字段独立搜索造成的重复和遗漏。

**主动搜索（每个组织必做 3-4 步）**：

| Step | 操作 | 主要提取 | 顺便提取 |
|------|------|---------|---------|
| **①** | 读 Wikipedia 页面（目标国语言 + 英语 + 中文） | key_people | departments, core_business, related_entities |
| **②** | 读官网首页 + 联络页 | social_accounts（页脚图标）, digital_assets | departments 补充 |
| **③** | 搜 `"{org_name_local} 뉴스 2025 2026"` （目标国语言） | recent_events | related_entities, apec_stance |
| **④** | 搜 `"{org_name_en} APEC trade policy"` （英语，仅 APEC 相关组织） | apec_stance | recent_events 补充 |
| **⑤** | 检查仍为空的字段，做 0-2 次补充搜索 | — | — |

**被动收获（不做专门搜索，从上述来源中提取）**：
- `departments` → 从 Wikipedia 组织架构段落 + 官网组织图提取
- `core_business` → 从 Wikipedia 导言段落综合撰写
- `related_entities` → 从 Wikipedia 链接 + 新闻中提及的关联组织提取
- `digital_assets` → 从官网发现的子站点、报告链接

**关键执行规则**：
- 每次阅读/搜索后，扫描结果中**所有字段**的相关信息，不仅关注主要目标字段
- Wikipedia 三种语言页面信息可能互补（韩语有详细人事、英语有国际视角、中文有中文译名），全部提取后再综合
- 官网页脚是 social_accounts 的最可靠来源，优先于搜索引擎

## 13.3 子代理 Prompt 模板

主会话为每个组织构建以下 prompt，通过 Agent 工具派发：

```
你是组织信息丰富 Agent。任务：为 {org_id}（{org_name_en}）生成高质量画像。

第一步：读取当前骨架文件
  文件路径：{filepath}
  读取后了解当前 completeness_score 和已有字段。

ID 规则：
1. 读取 {output_dir}/_name_index.json 获取已知实体 ID 映射
2. 引用的组织/人物在 index 中存在 → 使用对应 ID
3. 不在 index 中 → org_id / person_id 写 null
4. 禁止自创 ID 格式（不要写 KR-ORG-xxx 或 KR-GOV-PRES 等非标准格式）

第二步：按以下步骤执行搜索（每步都从结果中提取所有字段信息，不要只关注主目标字段）

Step 1: 读 Wikipedia 页面（3 种语言）
  - 目标国语言：{org_name_local} 的 Wikipedia 页面
  - 英语：{org_name_en} 的 Wikipedia 页面
  - 中文：{org_name_zh} 的 Wikipedia 页面（如存在）
  提取：key_people, departments, core_business, related_entities

Step 2: 读官网
  - 读取 {website} 首页和联络页（通常为 /contact 或 /about）
  提取：social_accounts（页脚图标链接）, digital_assets, departments 补充

Step 3: 搜 recent_events（目标国语言）
  - 搜索 "{org_name_local} 뉴스 2025 2026"（韩语示例）
  提取：recent_events, 顺便收 related_entities, apec_stance

Step 4: 搜 apec_stance（英语，仅 APEC 相关组织）
  - 搜索 "{org_name_en} APEC trade policy"
  提取：apec_stance, 顺便收 recent_events 补充

Step 5: 检查缺失字段
  - 如有字段仍为空，做 0-2 次补充搜索

第三步：将丰富后的完整画像写入原文件路径

⚠️ 必须使用以下精确字段名（不可自创字段名）：

key_people[]:        person_id | name | title | title_description | description
departments[]:       name | dept_id | head | description | parent_dept_id
social_accounts[]:   platform | account_name | url | source
recent_events[]:     date | title | description | impact | source
related_entities[]:  org_id | org_name | org_type | org_description | relationship_type
digital_assets[]:    name | url | description | source

⚠️ 所有描述性字段必须用中文输出（即使来源是英文/韩文页面，也要翻译为中文）：
- key_people[].title_description → 中文（如"主管产业政策、通商交涉"）
- key_people[].description → 中文（如"1968年生，首尔大学经济学博士..."）
- recent_events[].title → 中文（如"主办APEC贸易部长会议"）
- recent_events[].description → 中文
- recent_events[].impact → 中文
- departments[].name → 中文（可括号附原文，如"企划调整室（기획조정실）"）
- departments[].description → 中文
- related_entities[].org_description → 中文
- digital_assets[].name → 中文（如"产业通商部官方网站"）
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

交叉验证：重要信息需至少 2 个独立来源确认。
禁止编造：搜索不到的信息留空，绝不猜测。

写入前更新 collection_meta：
- `collection_meta.phase` = `"phase3_enriched"`
- `collection_meta.quotes` = 本次搜索使用的所有来源 URL 列表 `[{{title, url}}]`
- `collection_meta.data_sources` 补充本次实际使用的来源类型（如 `"news_search"`, `"official_website"`）

写入后必须执行（不可跳过）：
1. 运行 `python .claude/skills/country-org-collector/scripts/validate_schema.py {output_dir} --file {filepath}`
2. 如有 ERRORS → 修复 → 重新验证 → 直到 0 errors
3. 运行 `python .claude/skills/country-org-collector/scripts/validate_schema.py {output_dir} --file {filepath} --score` 更新 completeness_score

完成后返回：org_id、最终 completeness_score、搜索来源数量、是否有字段缺失。
```

## 13.4 写入规则

子代理写入 `orgs/{org_id}.json` 前必须完成：

1. **related_entities ID 预注册** — 遍历 `related_entities`，对每个 org_id：已在 registry → 直接使用；不存在 → 创建新 ID 并注册到 `id_registry.json`
2. **key_people person_id 注册** — 新发现的人物需分配 person_id 并写入 `id_registry.json`
3. **枚举值校验** — `org_type`、`org_subtype`、`relationship_type`、`industries` 均在 schema 枚举范围内（见 `enum_reference.md`）
4. **日期格式校验** — `founded_date` 和 `recent_events[].date` 必须为 `YYYY-MM-DD`

> **注意**：当 2 个子代理并行时，可能同时写 `id_registry.json`。主会话应在每个子代理完成后检查 registry 冲突（同一 org_name 不同 org_id），如有冲突则合并。

## 13.5 进度持久化

Phase 3 开始时，主会话创建 `_phase_progress.json` 并在整个阶段维护：

```json
{
  "phase": "P3_org_enrichment",
  "started_at": "2026-04-29T10:00:00",
  "last_updated": "2026-04-29T10:25:00",
  "completed": ["KR-GOV-001", "KR-GOV-002"],
  "remaining": ["KR-GOV-003", "KR-GOV-004", "KR-GOV-005"],
  "current": [],
  "failed": []
}
```

**操作规则**：
- 派发子代理时，将 org_id 加入 `current`
- 子代理完成后：将 org_id 从 `remaining` 和 `current` 移到 `completed`，更新 `last_updated`
- 子代理失败：将 org_id 从 `remaining` 和 `current` 移到 `failed`
- 中断恢复时：读取 `remaining` 列表，跳过 `completed` 和 `current` 中的条目
- 使用 `atomic_write.save_json()` 写入确保原子性

## 13.6 限速规则

详见「限速总表」。单组织收集耗时约 3-5 分钟。2 并行时总吞吐约 2 倍。

> **并行限速注意**：Wikidata SPARQL 5 次/分钟和搜索引擎 30 次/分钟是全局配额。2 个子代理各自控制请求间隔，主会话无需额外调度。

> **建议**：如组织数量 > 20，按类别分批派发（如先 GOV，再 SOE，再 CORP...），每批完成后报告进度。

> **Phase 3 完成 → Phase 4**：主会话生成人物清单 + 逐人物派发子代理深度调查。

---

# §14 Phase 4：子代理人物收集与深度调查

**目标**：从组织画像提取人物清单 + 逐人物派发子代理深度调查，输出完整人物画像。

**触发方式**：Phase 3 完成后自动建议。或用户说"收集人物"、"深度收集人物"。

**输入**：`orgs/` 下所有已完成的组织画像 + `id_registry.json`

**输出**：`person_list.json` + `persons/{person_id}.json`

**执行方式**：主会话生成人物清单 + 编排子代理，每人物一个子代理，**串行**执行。

## 14.1 主会话编排步骤

### Step A：人物清单生成（主会话直接执行）

1. 运行辅助脚本：
```bash
python .claude/skills/country-org-collector/scripts/update_person_list.py output/{iso}/{date}
```

2. 广度搜索发现更多人物（对每个组织执行）：
```
"{org_name_en} members leadership team"
"{org_name_en} board directors executives"
"{org_name_local} 주요 인물 임원진"
```

3. Wikidata QID 匹配（对尚未有 QID 的人物）：
   - Wikipedia REST API 搜索
   - Wikidata SPARQL（参考 `sparql_person_templates.md` 模板 K）
   - Web 搜索：`"{person_name}" site:wikidata.org`

4. 分配 person_id + 评定 importance_level：

| Level | 标准 | 示例 |
|-------|------|------|
| **high** | 现任最高领导人、核心决策层 | 总理、党魁、央行行长 |
| **medium** | 部长级/副手/核心管理层 | 部长、副部长、CEO |
| **low** | 普通成员/委员/一般官员 | 普通议员、部门主管 |

输出 `person_list.json`，同时更新 `id_registry.json`。

### Step B：初始化进度 + 编排循环

```
1. 创建 _phase_progress.json：
   {
     "phase": "P4_person_enrichment",
     "started_at": "{当前时间}",
     "last_updated": "{当前时间}",
     "completed": [],
     "remaining": ["KR-PERSON-000001", "KR-PERSON-000004", ...],
     "current": null,
     "failed": []
   }
2. WHILE remaining 不为空:
   a. 从 remaining 中取 1 个 person_id
   b. 为该人物构建子代理 prompt（§14.3）
   c. 派发 Agent 调用
   d. 等待子代理返回
   e. 如子代理失败（API 错误/超时）→ 重试 1 次（相同 prompt）
   f. 验证输出文件存在且 JSON 合法
   g. 每完成 1 个人物后运行：
      python .claude/skills/country-org-collector/scripts/resolve_ids.py output/{iso}/{date}
      python .claude/skills/country-org-collector/scripts/generate_name_index.py output/{iso}/{date}
   h. 更新 _phase_progress.json
   i. 报告进度
3. 全部完成后执行质量门禁检查（§14.4）
```

## 14.2 搜索策略参考（子代理内部执行）

**多语言搜索策略**：按目标国语言 → 英语 → 中文顺序搜索。

**搜索关键词模板**（按字段类型）：

| 字段 | 英语搜索 | 目标国语言搜索 |
|------|---------|--------------|
| biography | `{name_en} biography career` | `{name_local} 프로필 약력` (韩) / `{name_local} プロフィール 経歴` (日) |
| education | `{name_en} education university degree` | `{name_local} 학력 출신대학` (韩) |
| career | `{name_en} career history appointment` | `{name_local} 경력 발탁` (韩) |
| family | `{name_en} family spouse children` | `{name_local} 가족 배우자` (韩) |
| stance | `{name_en} policy stance speech` | `{name_local} 정책 입장` (韩) |
| social | `{name_en} site:linkedin.com` 等 | — |

**社交媒体搜索模板**（对每个人物必做）：

```
"{name_en}" site:facebook.com
"{name_en}" site:twitter.com OR site:x.com
"{name_en}" site:linkedin.com
"{name_en}" site:instagram.com
```

### 高价值官方来源

| 来源 | 适用人物 | URL 模式 |
|------|---------|---------|
| 政府名录 | 政府官员 | 该国政府名录网站（如 sgdi.gov.sg） |
| 议会名录 | 国会议员 | 该国议会官网议员名录 |
| 国防部 Leadership | 军方将领 | 该国国防部官网 |
| 大学官网 Leadership | 学术领袖 | {university}.edu.*/about/leadership |
| 官网 leadership 页 | 企业高管 | 企业官网 leadership/team 页 |

### 中文名获取优先级

当 `name_zh` 为空时：
1. Wikidata `zh` label
2. Wikipedia 中文版 sitelink
3. 该国华文媒体报道
4. Web 搜索 `{person_name} 中文名`

> **⚠️ 非中文母语国家人名**：不得使用大陆新华社音译，必须使用目标国家本地华文媒体标准译名。详见 `malay_name_zh_guide.md`。

## 14.3 子代理 Prompt 模板

主会话为每个人物构建以下 prompt，通过 Agent 工具派发：

```
你是人物信息调查 Agent。任务：为 {person_id}（{name_en}）生成高质量画像。

第一步：读取当前人物文件
  文件路径：{filepath}
  如文件已存在，读取后了解当前字段状态；如不存在，创建新文件。

第二步：多语言搜索（按此顺序）
1. 目标国语言：{name_local} + 关键词
2. 英语：{name_en} + 关键词
3. 中文：{name_zh} + 关键词

必做字段（按优先级）：
1. biography_summary — 中文生平概述（200字+）
2. work_experience — 完整职业履历（≥3条，含起止日期）
3. education — 学历信息（院校、学位、专业）
4. political_stances — 政治立场（含 source URL）
5. person_relationships — 人际关系网络（含 person_id 交叉引用）
6. social_accounts — 社交媒体（LinkedIn/Twitter/Facebook/Instagram/Tiktok/Youtube）
7. family_members — 家庭信息（relationship 必须使用 enum 值：spouse/son/daughter 等；name 必须是真实姓名，搜不到则不写入该条）
8. major_achievements — 主要成就

⚠️ 字段名严格约束（写入前逐条对照）：

精确字段名（不可自创）：
work_experience[]:      start_date | end_date | organization | org_id | position
education[]:            institution | degree | field | start_date | end_date
political_stances[]:    date | topic | stance_content | source
person_relationships[]: person_id | person_name | relationship_type | description
major_achievements[]:   date | achievement | organization
social_accounts[]:      platform | account_name | url | source
family_members[]:       person_id | name | relationship | industry_or_organization
contacts[]:             type | value | source

⚠️ 所有描述性字段必须用中文输出（即使来源是英文/其他语言页面，也要翻译为中文）：
- biography_summary → 中文（200字+）
- work_experience[].position → 中文（如"经济政策局局长"）
- work_experience[].organization → 中文（如"企划财政部"）
- education[].institution → 中文（如"首尔大学"，可括号附英文）
- education[].field → 中文（如"经济学"）
- political_stances[].topic → 中文（如"半导体产业政策"）
- political_stances[].stance_content → 中文
- person_relationships[].description → 中文
- major_achievements[].achievement → 中文
- name 格式：中文优先，括号附英文，如"金正宽 (Kim Jung-kwan)"
- social_accounts[].platform 保留英文枚举值
- 所有 URL 保留原样

常见错误对照表：
| 路径 | ✅ 正确 | ❌ 错误 |
|------|---------|---------|
| political_stances[] 立场内容 | `stance_content` | stance, position, content |
| major_achievements[] 成就描述 | `achievement` | description, title, content |
| person_relationships[] 人物ID/名 | `person_id` / `person_name` | related_person, related_person_name, name |
| person_relationships[] 关系类型 | `relationship_type` | relationship |
| social_accounts[] 平台 | `twitter_x` (小写英文) | "Facebook", "X (Twitter)", "Instagram" |
| family_members[] 关系 | `spouse` (英文 enum) | "妻子", "配偶", "儿子", "父亲" |

枚举值速查（只列易错项，完整列表见 person_profile_schema.json）：
- social_accounts[].platform: twitter_x | facebook | instagram | youtube | linkedin | telegram | tiktok | threads | wechat | weibo | other
- family_members[].relationship: spouse | father | mother | son | daughter | brother | sister | grandfather | grandmother | uncle | aunt | cousin | other
- person_relationships[].relationship_type: spouse | parent | child | sibling | mentor | mentee | colleague | superior | subordinate | political_ally | political_rival | associate | other

必填字段禁止为空（无法填写则整条记录删除，不要写入空壳条目）：
- `person_relationships[].person_name` — 不知道名字就不写这条关系
- `family_members[].name` — 必须是真实全名（如"金惠京"、"张旭"）。以下均为无效占位符，出现任何一种则删除该条：`未公开`、`姓名未公开`、`不详`、`未知`、纯关系词（`配偶`/`长子`/`次子`/`长女`/`次女`/`父亲`/`母亲`/`儿子`/`女儿`/`三子`）、仅姓氏（`李氏`/`赵氏`/`韩氏`）、括号描述（`（一子）`/`（妻子）`/`（长女）`）、关系+出生信息（`长女（2006年出生）`/`长子（约1994年生）`）。不确定姓名就宁可不写这条。
- `political_stances[].stance_content` — 没有内容就不写这条
- `major_achievements[].achievement` — 没有描述就不写这条

ID 规则：
1. 读取 {output_dir}/_name_index.json 获取已知实体 ID 映射
2. 引用的组织/人物在 index 中存在 → 使用对应 ID
3. 不在 index 中 → org_id / person_id 写 null
4. 禁止自创 ID 格式（不要写 KR-ORG-xxx 或 KR-PERSON-NEW 等非标准格式）

第三步：将完整画像写入文件路径 {filepath}

写入前更新 collection_meta：
- `collection_meta.quotes` = 本次搜索使用的所有来源 URL 列表 `[{{title, url}}]`
- `collection_meta.data_sources` 补充本次实际使用的来源类型

写入后必须执行（不可跳过）：
1. 运行 `python .claude/skills/country-org-collector/scripts/validate_schema.py {output_dir} --file {filepath}`
2. 如有 ERRORS → 修复 → 重新验证 → 直到 0 errors
3. 运行 `python .claude/skills/country-org-collector/scripts/validate_schema.py {output_dir} --file {filepath} --score` 更新 completeness_score

交叉验证：重要信息需至少 2 个独立来源确认。
禁止编造：搜索不到的信息留空，绝不猜测。

完成后返回：person_id、最终 completeness_score、搜索来源数量、是否有字段缺失。
```

## 14.4 质量门禁

每批人物完成后，主会话检查：

| 检查项 | 标准 | 不达标处理 |
|--------|------|-----------|
| biography_summary 为英文 | 0 个 | 派子代理重新搜索补充中文 |
| biography_summary 为空 | 0 个（high/medium） | 派子代理重新搜索补充 |
| JSON 解析失败 | 0 个 | 修复弯引号 |
| major_achievements 格式 | 0 错误 | 确保为 `{date, achievement}` |
| political_stances 格式 | 0 错误 | 确保为 `{topic, stance_content, source}` |

## 14.5 进度持久化

Phase 4 开始时，主会话创建或复用 `_phase_progress.json`：

```json
{
  "phase": "P4_person_enrichment",
  "started_at": "2026-04-29T11:00:00",
  "last_updated": "2026-04-29T11:35:00",
  "completed": ["KR-PERSON-000001", "KR-PERSON-000004"],
  "remaining": ["KR-PERSON-000011", "KR-PERSON-000013"],
  "current": null,
  "failed": []
}
```

**操作规则**：
- 派发子代理时，设置 `current` 为该 person_id
- 子代理完成后：将 person_id 从 `remaining` 移到 `completed`，清空 `current`，更新 `last_updated`
- 子代理失败：将 person_id 从 `remaining` 移到 `failed`
- 中断恢复时：读取 `remaining` 列表跳过已完成项
- Phase 完成后可删除此文件或保留作为审计记录

## 14.6 限速规则

单人物收集耗时约 5-8 分钟。串行执行，无并行。

> **建议**：按 importance_level 分批执行（先 high，再 medium，再 low）。

> **Phase 4 完成 → Phase 5**：运行 `validate_schema.py` + `generate_index.py`。

---

# §15 Phase 5：验证收尾

**目标**：校验全部 JSON 文件符合 schema，生成索引，输出完整性报告。

**触发方式**：Phase 4 完成后自动执行，或用户说"验证"、"收尾"时激活。

## 15.1 Schema 验证

```bash
# 校验所有 org 和 person JSON
python .claude/skills/country-org-collector/scripts/validate_schema.py output/{iso}/{date}

# 自动修复 Unicode 弯引号等问题
python .claude/skills/country-org-collector/scripts/validate_schema.py output/{iso}/{date} --fix

# 跨文件交叉引用验证（P5 收尾时必做）
python .claude/skills/country-org-collector/scripts/validate_schema.py output/{iso}/{date} --cross-ref
```

校验内容：
- org_id / person_id / dept_id 格式
- 必填字段完整性
- 枚举值合规（org_type、relationship_type、industries、social_platform 等）
- 日期格式（strict vs flexible）
- Unicode 弯引号检测

**`--cross-ref` 额外检查**：
- org `key_people[].person_id` 是否在 persons/ 目录或 registry 中有对应记录
- org `related_entities[].org_id` 是否在 id_registry.json 中
- person `work_experience[].org_id` 是否在 orgs/ 目录或 registry 中有对应记录
- person `person_relationships[].person_id` 是否存在
- registry 中 status=profiled 的组织是否有对应文件

## 15.2 索引生成

```bash
python .claude/skills/country-org-collector/scripts/generate_index.py output/{iso}/{date}
```

自动生成：
- `orgs/_index.json` — 组织画像汇总（含 completeness_score 统计）
- `persons/_index.json` — 人物画像汇总（含 completeness_score 统计）

## 15.3 完整性报告

向用户报告：
- 组织画像总数、平均完整度、按类别统计
- 人物画像总数、平均完整度、按 importance_level 统计
- 缺失字段最多的 top 5 组织和人物
- Schema 校验错误数
- 建议的下一步行动

## 脚本清单

| 脚本 | Phase | 用途 |
|------|-------|------|
| `verify_qids.py` | P2 | QID 验证 |
| `batch_collect.py` | P2 | Wikidata/Wikipedia 数据缓存 |
| `generate_profiles.py` | P2 | 骨架画像生成 + key_people QID 解析 |
| `generate_name_index.py` | P2/P3/P4 | 名称→ID 索引生成（子代理用于 ID 查找） |
| `resolve_ids.py` | P3/P4 | 批量解析 null ID → 已知 ID 或分配新 ID |
| `update_person_list.py` | P4 | 人物清单辅助 |
| `generate_index.py` | P5 | 索引生成 |
| `validate_schema.py` | P5 | Schema 校验 + 自动修复 |

> **共享库**：`atomic_write.py`（原子写入、代理配置、名称标准化）。
> 所有脚本支持断点续跑，使用 temp + fsync + rename 原子写入。

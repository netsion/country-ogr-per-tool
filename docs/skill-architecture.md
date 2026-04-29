# 国家组织机构收集器（country-org-collector）执行流程与架构

## 一、总体流水线流程图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         用户触发 Skill                                   │
│           "收集某国组织" / "研究某国机构" / "建立组织目录"                │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Phase 0: 准备工作    │
                    │  · 创建输出目录       │
                    │  · 生成 _target_orgs  │
                    │  · 生成 _progress     │
                    │  · 初始化 id_registry │
                    └──────────┬───────────┘
                               │
              ═════════════════╪═════════════════
              ║   组织数据收集线  ║
              ══════════════════════════════════
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
┌──────────────────┐ ┌──────────────────┐ ┌────────────────────┐
│ 第一阶段：广度扫描 │ │ 第二阶段：深度画像 │ │ Phase 2.5: Web搜索  │
│                  │ │                  │ │   丰富组织画像       │
│ · Wikidata SPARQL│ │ · 逐组织详细收集  │ │                    │
│ · Wikipedia REST │ │ · Schema验证     │ │ · 并行Agent搜索     │
│ · DBpedia SPARQL │ │ · JSON画像输出   │ │ · 社交账号/人物/事件 │
│ · Web搜索补充    │ │                  │ │ · 目标完整度 85+    │
│                  │ │                  │ │                    │
│ 输出:             │ │ 输出:             │ │ 数据源:             │
│ _target_orgs.json│ │ orgs/*.json      │ │ MCP search+read_url│
│                  │ │                  │ │                    │
│ 脚本:            │ │ 脚本:            │ │ 方式:               │
│ (手动/Agent)     │ │ verify_qids.py   │ │ 并行子Agent         │
│                  │ │ batch_collect.py │ │                    │
│                  │ │ generate_profiles│ │                    │
│                  │ │ enrich_org_profiles││                    │
│                  │ │ resolve_key_people││                    │
└──────────────────┘ └──────────────────┘ └────────────────────┘
                               │
              ═════════════════╪═════════════════
              ║   人物数据收集线  ║
              ══════════════════════════════════
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
┌──────────────────┐ ┌──────────────────┐ ┌────────────────────┐
│ 第三阶段：人物    │ │ 第四阶段：人物    │ │ Phase 4.5: Web搜索  │
│   广度扫描       │ │   深度画像       │ │   丰富人物画像       │
│                  │ │                  │ │                    │
│ · 提取key_people │ │ · 逐人物深度调查  │ │ · 并行Agent搜索     │
│ · 组织名广度搜索 │ │ · Wikidata结构化 │ │ · 中文传记/家庭/教育 │
│ · 去重合并       │ │ · Wikipedia全文  │ │ · 社交媒体搜索       │
│ · QID匹配       │ │ · Schema验证     │ │ · 目标完整度 85+    │
│ · 分配person_id  │ │                  │ │                    │
│                  │ │ 输出:             │ │ 质量门禁:            │
│ 输出:             │ │ persons/*.json   │ │ avg_score < 80 → 继续│
│ person_list.json │ │                  │ │                    │
│                  │ │ 脚本:            │ │ 方式:               │
│ 脚本:            │ │ batch_person_    │ │ 串行子Agent         │
│ update_person_   │ │   profiles.py    │ │ (每人物一个Agent)    │
│   list.py        │ │ resolve_person_  │ │                    │
│                  │ │   qids.py        │ │                    │
└──────────────────┘ └──────────────────┘ └────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Phase 8: 收尾       │
                    │  · 生成 _index.json  │
                    │  · 验证完整性        │
                    │  · generate_index.py │
                    └──────────────────────┘
```

## 二、脚本执行序列图

| Step | 脚本名 | 输入 | 输出 | 说明 |
|------|--------|------|------|------|
| Phase 0 | (手动) | 用户指定国家 | `_target_orgs.json` `_progress.json` `id_registry.json` | 创建目录和初始配置 |
| Phase 1 | `verify_qids.py` | `_target_orgs.json` | 修正后的 `_target_orgs.json` | 使用 wbsearchentities API 交叉验证每个 QID |
| Phase 2 | `batch_collect.py` | `_target_orgs.json` | `_cache/` 目录 | Wikidata EntityData + Wikipedia REST API，支持断点续跑 |
| Phase 3 | `generate_profiles.py` | `_cache/` + `id_registry` | `orgs/{org_id}.json` | 解析缓存数据，生成初始组织画像 |
| Phase 3.5 | `enrich_org_profiles.py` | `orgs/*.json` | 更新 `orgs/*.json` | Wikipedia 全文(中+英) + DBpedia infobox，幂等可重跑 |
| Phase 3.6 | 并行 Agent 搜索 | `orgs/*.json` | 更新 `orgs/*.json` | = Phase 2.5，MCP search + read_url，4批并行 |
| Phase 4 | `resolve_key_people.py` | `orgs/*.json` | 更新 `orgs/*.json` | 解析 key_people 中 QID 为真实姓名，过滤非人物(P31≠Q5) |
| Phase 5 | `update_person_list.py` | `orgs/*.json` + `id_registry` | `person_list.json` | 提取所有 key_people，去重合并 + 分配 person_id |
| Phase 6 | `batch_person_profiles.py` | `person_list.json` | `persons/{person_id}.json` | Wikidata + Wikipedia(摘要+全文)，支持断点续跑 |
| Phase 6.5 | `resolve_person_qids.py` | `persons/*.json` | 更新 `persons/*.json` | 修复未解析 QID，恢复 degree/field |
| Phase 7 | 串行 Agent 搜索 | `persons/*.json` | 更新 `persons/*.json` | = Phase 4.5，每人物一个子Agent，质量门禁 avg<80 继续 |
| Phase 8 | `generate_index.py` | `orgs/` + `persons/` | `_index.json` | 自动生成汇总索引 |

## 三、系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                     用户界面层 (Claude Code CLI)                  │
│                                                                 │
│   用户指令 ──→ Skill 触发器 ──→ SKILL.md 解析 ──→ 分阶段调度     │
│                                                                 │
└───────────┬─────────────────────────────────────────────────────┘
            │
            │  调度指令
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                          执行引擎层                              │
│                                                                 │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────────┐   │
│  │ Python 脚本  │   │ 子Agent     │   │ 直接工具调用         │   │
│  │ (批量自动化) │   │ (Web搜索)   │   │ (单次操作)          │   │
│  │             │   │             │   │                     │   │
│  │ ·verify_qids│   │ ·MCP search │   │ ·Read/Edit/Write    │   │
│  │ ·batch_coll │   │ ·MCP read   │   │ ·Grep/Glob          │   │
│  │ ·gen_profile│   │   _url      │   │ ·Bash(curl)         │   │
│  │ ·enrich_org │   │             │   │                     │   │
│  │ ·resolve_kp │   │ 执行模式:    │   │                     │   │
│  │ ·update_pl  │   │ ·串行(人物)  │   │                     │   │
│  │ ·batch_pp   │   │ ·并行(组织)  │   │                     │   │
│  │ ·resolve_pq │   │             │   │                     │   │
│  │ ·gen_index  │   │             │   │                     │   │
│  └──────┬──────┘   └──────┬──────┘   └──────────┬──────────┘   │
│         │                 │                      │              │
│         └────────────┬────┴──────────────────────┘              │
│                      │                                          │
│            ┌─────────▼─────────┐                                │
│            │ atomic_write.py   │  共享工具库                     │
│            │ ·原子写入          │  (temp+fsync+rename)           │
│            │ ·代理管理          │  (主备切换)                     │
│            │ ·名称标准化        │  (模糊匹配)                     │
│            │ ·JSON读写          │  (UTF-8编码)                   │
│            └───────────────────┘                                │
│                                                                 │
└───────────┬─────────────────────────────────────────────────────┘
            │
            │  HTTP/API 请求 (通过代理)
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        外部数据源层                               │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │ Wikidata     │  │ Wikipedia    │  │ MCP Server         │    │
│  │              │  │              │  │ (search-read)      │    │
│  │ ·SPARQL查询  │  │ ·REST API    │  │                    │    │
│  │ ·EntityData  │  │ ·全文(中+英) │  │ ·Google搜索        │    │
│  │ ·wbsearchent │  │              │  │ ·URL读取           │    │
│  │   ities      │  │              │  │ ·图片下载          │    │
│  └──────────────┘  └──────────────┘  └────────────────────┘    │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │ DBpedia      │  │ 通用Web搜索  │  │ 社交媒体           │    │
│  │              │  │              │  │                    │    │
│  │ ·SPARQL查询  │  │ ·新闻网站    │  │ ·LinkedIn          │    │
│  │ ·Infobox提取 │  │ ·官方页面    │  │ ·Twitter/X         │    │
│  │              │  │ ·政府目录    │  │ ·Facebook          │    │
│  │              │  │              │  │ ·Instagram         │    │
│  └──────────────┘  └──────────────┘  └────────────────────┘    │
│                                                                 │
│            代理网关: http://10.11.204.68:8081                     │
│            (主备自动切换)                                         │
│                                                                 │
└───────────┬─────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        持久化存储层                               │
│                                                                 │
│  output/{country_iso}/{date}/                                   │
│  ├── _target_orgs.json        目标组织清单                       │
│  ├── _progress.json           进度追踪                           │
│  ├── id_registry.json         ID注册表(防重复)                   │
│  ├── _cache/                  原始数据缓存                       │
│  │   ├── {QID}_wikidata.json                                     │
│  │   ├── {QID}_wiki_en.json                                      │
│  │   └── {QID}_wiki_zh.json                                      │
│  ├── orgs/                    组织画像                           │
│  │   ├── _index.json          汇总索引                           │
│  │   ├── MY-GOV-001.json                                         │
│  │   ├── MY-MEDIA-007.json                                       │
│  │   └── ...                                                     │
│  └── persons/                 人物画像                           │
│      ├── _index.json          汇总索引                           │
│      ├── MY-PERSON-000001.json                                   │
│      └── ...                                                     │
│                                                                 │
│  Schema 约束:                                                    │
│  ├── org_list_schema.json     第一阶段输出验证                    │
│  ├── org_profile_schema.json  组织画像验证 (additionalProperties: │
│  │                             false)                             │
│  ├── person_list_schema.json  人物清单验证                        │
│  └── person_profile_schema.json 人物画像验证 (strict)             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 四、数据流转图

```
_target_orgs.json          id_registry.json
      │                          │
      ▼                          │
 ┌─────────┐    Wikidata/WP     │
 │ verify  │──────────────────→ │ (注册新org_id)
 │ qids.py │                    │
 └────┬────┘                    │
      │                         │
      ▼                         │
 ┌──────────┐   _cache/         │
 │ batch_   │──────────────────→│
 │ collect  │  {QID}_wikidata   │
 │          │  {QID}_wiki_en    │
 │          │  {QID}_wiki_zh    │
 └────┬─────┘                   │
      │                         │
      ▼                         │
 ┌──────────┐   orgs/*.json     │
 │ generate │──────────────────→│ (写入画像)
 │ _profiles│                   │
 └────┬─────┘                   │
      │                         │
      ▼                         │
 ┌──────────┐   orgs/*.json     │
 │ enrich_  │──────────────────→│ (更新画像)
 │ org_prof │  +部门/社交/中文   │
 └────┬─────┘                   │
      │                         │
      ▼                         │       ┌──────────┐
 ┌──────────┐   orgs/*.json     │       │ MCP      │
 │ Phase2.5 │──────────────────→│ ←──── │ search   │
 │ Agent搜索│  +事件/人物/社交   │       │ read_url │
 └────┬─────┘                   │       └──────────┘
      │                         │
      ▼                         │
 ┌──────────┐   orgs/*.json     │
 │ resolve_ │──────────────────→│
 │ key_ppl  │  QID→真实姓名     │
 └────┬─────┘                   │
      │                         │
      ▼                         │
 ┌──────────┐   person_list.json│
 │ update_  │──────────────────→│
 │ person_ls│                   │
 └────┬─────┘                   │
      │                         │
      ▼                         │
 ┌──────────┐   persons/*.json  │
 │ batch_   │──────────────────→│ (写入画像)
 │ person_p │                   │
 └────┬─────┘                   │
      │                         │
      ▼                         │
 ┌──────────┐   persons/*.json  │
 │ resolve_ │──────────────────→│ (修复QID)
 │ person_q │                   │
 └────┬─────┘                   │
      │                         │
      ▼                         │       ┌──────────┐
 ┌──────────┐   persons/*.json  │       │ MCP      │
 │ Phase4.5 │──────────────────→│ ←──── │ search   │
 │ Agent搜索│  +传记/家庭/教育   │       │ read_url │
 └────┬─────┘                   │       └──────────┘
      │                         │
      ▼                         │
 ┌──────────┐   _index.json     │
 │ generate │──────────────────→│
 │ _index   │  orgs + persons   │
 └──────────┘                   │
```

## 五、关键设计模式

| 模式 | 说明 |
|------|------|
| **原子写入** | temp file + fsync + rename，防止崩溃产生半写文件 |
| **ID注册表** | `id_registry.json` 全局唯一ID分配，防重复 |
| **断点续跑** | `_progress.json` + 缓存检查，支持中断后恢复 |
| **代理主备切换** | `setup_proxy()` 自动检测，主代理不通切备用 |
| **非人物过滤** | `P31≠Q5` 自动过滤，避免"director"等职位被当人物 |
| **严格Schema验证** | `additionalProperties: false`，禁止额外字段 |
| **并行/串行混合** | 组织丰富=并行Agent，人物丰富=串行Agent(避免重复) |
| **质量门禁** | Phase 4.5/2.5 结束时检查 avg_score，< 80 必须继续 |
| **中英双语输出** | 描述性字段中文，标识性字段英文，人名`中文（English）` |

## 六、脚本↔阶段对应关系

| 概念阶段 | 脚本步骤 | 脚本/方式 |
|---------|---------|----------|
| 第一阶段（广度扫描） | Phase 0 | 手动/Agent |
| | Phase 1 | `verify_qids.py` |
| 第二阶段（深度画像） | Phase 2 | `batch_collect.py` |
| | Phase 3 | `generate_profiles.py` |
| | Phase 3.5 | `enrich_org_profiles.py` |
| Phase 2.5（组织Web丰富） | Phase 3.6 | 并行Agent + MCP |
| 第二→三阶段（过渡） | Phase 4 | `resolve_key_people.py` |
| | Phase 5 | `update_person_list.py` |
| 第四阶段（人物画像） | Phase 6 | `batch_person_profiles.py` |
| | Phase 6.5 | `resolve_person_qids.py` |
| Phase 4.5（人物Web丰富） | Phase 7 | 串行Agent + MCP |
| 收尾 | Phase 8 | `generate_index.py` |

## 七、ID 体系

### 组织 ID

格式：`{ISO2}-{TYPE}-{SEQ}`

| 组成 | 说明 | 示例 |
|------|------|------|
| ISO2 | 国家 ISO 3166-1 alpha-2 | `MY`、`SG` |
| TYPE | 组织分类（10类） | `GOV`、`MEDIA`、`SOE` |
| SEQ | 3位顺序号 | `001`、`007` |

完整示例：`MY-GOV-001`、`MY-MEDIA-007`、`SG-FIN-003`

### 人物 ID

格式：`{ISO2}-PERSON-{SEQ(6位)}`

| 组成 | 说明 | 示例 |
|------|------|------|
| ISO2 | 国家 ISO 3166-1 alpha-2 | `MY`、`SG` |
| SEQ | 6位顺序号 | `000001`、`000528` |

完整示例：`MY-PERSON-000001`、`MY-PERSON-000528`

### 占位 ID

用于人物关系引用暂无独立档案的人物：

```
MY-PERSON-900001 ~ MY-PERSON-900999
```

不同人物使用不同区间段（900001-900002、900010-900013等）以避免冲突。

## 八、组织分类体系

| 代码 | 标签 | 说明 |
|------|------|------|
| GOV | 政府机构 | 国家元首、内阁、各部委、行政机关、法定机构 |
| SOE | 国有企业 | 政府控股的企业和公司 |
| CORP | 企业公司 | 上市公司及大型私营企业 |
| NGO | 非政府组织 | NGO、慈善机构、基金会 |
| ACAD | 学术机构 | 大学、研究所、智库 |
| MEDIA | 媒体机构 | 新闻社、广播公司、出版商 |
| FIN | 金融机构 | 银行、投资公司、保险公司 |
| INTL | 国际组织 | 总部位于该国的多边组织 |
| PARTY | 政党 | 主要政党 |
| MIL | 军事安全 | 武装力量、情报机构 |

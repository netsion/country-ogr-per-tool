# APEC OSINT 数据说明文档

> 版本: 1.0 | 更新日期: 2026-04-16 | 数据批次: 新加坡 (SG)

本文档为 Web 可视化团队提供完整的数据结构说明、字段定义、枚举值表和实际数据统计，以便快速对接开发。

---

## 1. 数据概览

| 指标 | 组织 (Organization) | 人物 (Person) |
|------|---------------------|---------------|
| **画像总数** | 48 | 38 |
| **注册总数** | 48 | 111 |
| **平均完整度** | 78/100 | 73/100 |
| **完整度范围** | 35–96 | 20–100 |

### 1.1 组织类型分布

| 类型 | 代码 | 数量 | 说明 |
|------|------|------|------|
| 政府机构 | GOV | 17 | 各部委、监管机构、司法机关 |
| 国有企业 | SOE | 8 | 政府控股企业 (Temasek/GIC 系等) |
| 企业公司 | CORP | 7 | 上市公司及大型私营企业 |
| 政党 | PARTY | 4 | 执政党及主要反对党 |
| 学术机构 | ACAD | 4 | 大学、研究所 |
| 媒体机构 | MEDIA | 3 | 广播公司、新闻社 |
| 非政府组织 | NGO | 2 | 慈善机构、基金会 |
| 金融机构 | FIN | 1 | 银行集团 |
| 国际组织 | INTL | 1 | 区域性多边组织 |
| 军事安全 | MIL | 1 | 武装力量 |

### 1.2 人物重要性分布

| 级别 | 数量 | 说明 |
|------|------|------|
| high | 23 | 国家元首、总理、首席大法官、CEO 等 |
| medium | 14 | 部长、局长、董事等 |
| low | 74 | 普通高管、议员等 |

### 1.3 人物性别分布

| 性别 | 数量 |
|------|------|
| male | 31 |
| female | 7 |

---

## 2. 目录结构

```
output/sg/2026-04-15/
├── id_registry.json          # 主注册表 (组织 + 人物 ID 索引)
├── person_list.json          # 人物清单 (含重要性评级)
├── _progress.json            # 采集进度跟踪
├── _target_orgs.json         # 目标组织列表 (含 Wikidata QID)
│
├── orgs/                      # 组织画像目录
│   ├── _index.json           # 组织索引 (汇总统计)
│   ├── SG-GOV-001.json       # 单个组织画像
│   ├── SG-GOV-002.json
│   └── ... (共 48 个文件)
│
├── persons/                  # 人物画像目录
│   ├── _index.json           # 人物索引 (汇总统计)
│   ├── SG-PERSON-000005.json # 单个人物画像
│   └── ... (共 38 个文件)
│
├── _cache/                   # 组织原始数据缓存 (Wikidata + Wikipedia)
│   └── Q*.json               # 每个 QID 一个缓存文件
│
└── _person_cache/            # 人物原始数据缓存
    └── Q*.json
```

### 2.1 文件命名规则

| 文件类型 | 命名格式 | 示例 |
|---------|---------|------|
| 组织画像 | `{org_id}.json` | `SG-GOV-001.json` |
| 人物画像 | `{person_id}.json` | `SG-PERSON-000005.json` |
| 缓存文件 | `{wikidata_qid}.json` | `Q3001103.json` |

### 2.2 ID 编码规则

```
组织 ID:  {ISO2}-{TYPE}-{SEQ}
          SG    -GOV  -001
          │      │     └── 3位顺序号
          │      └── GOV|SOE|CORP|NGO|ACAD|MEDIA|FIN|INTL|PARTY|MIL
          └── 国家 ISO 2字母代码

人物 ID:  {ISO2}-PERSON-{SEQ}
          SG    -PERSON-000005
                  └── 6位顺序号

部门 ID:  {org_id}-DEPT-{SEQ}
          SG-GOV-001-DEPT-001
```

---

## 3. 组织画像数据结构 (org_profile)

### 3.1 完整字段表

```json
{
  "org_id": "SG-GOV-001",
  "basic_info": { /* 见 3.2 */ },
  "social_accounts": [ /* 见 3.3 */ ],
  "digital_assets": [ /* 见 3.4 */ ],
  "key_people": [ /* 见 3.5 */ ],
  "departments": [ /* 见 3.6 */ ],
  "recent_events": [ /* 见 3.7 */ ],
  "related_entities": [ /* 见 3.8 */ ],
  "core_business": "Description string...",
  "industries": ["financial_services"],
  "apec_stance": "Description or null",
  "profile": { /* 见 3.9 */ },
  "collection_meta": { /* 见 3.10 */ }
}
```

### 3.2 basic_info

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name_original | string | 是 | 原语言名称 (新加坡为英文) |
| name_zh | string\|null | 否 | 中文名称 |
| name_en | string | 是 | 英文官方名称 |
| aliases | string[] | 否 | 缩写、曾用名等别名 |
| org_type | enum | 是 | 组织类型代码 (见 §5.1) |
| org_subtype | enum | 是 | 组织子类型代码 (见 §5.2) |
| country_iso3 | string | 是 | 所属国家 ISO 3166-1 alpha-3 |
| hq_country_iso3 | string | 是 | 总部所在国家 ISO 3166-1 alpha-3 |
| founded_date | string\|null | 否 | 成立日期 `YYYY-MM-DD` |
| website | string\|null | 否 | 官网 URL |

### 3.3 social_accounts

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| platform | enum | 是 | 平台代码 (见 §5.4) |
| account_name | string\|null | 否 | 账号名 / @handle |
| url | string | 是 | 主页完整 URL |
| source | string\|null | 否 | 信息来源 |

### 3.4 digital_assets

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 资产名称 (如 "eLitigation") |
| url | string | 是 | 访问地址 |
| description | string\|null | 否 | 功能描述 |
| source | string\|null | 否 | 信息来源 |

### 3.5 key_people

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| person_id | string\|null | 否 | 人物 ID，可跨引用 persons/ 画像 |
| name | string | 是 | 显示名 (含中英，如 "黄循财 (Lawrence Wong)") |
| title | string | 是 | 在本组织的职务 |
| title_description | string\|null | 否 | 职务职责描述 |
| description | string\|null | 否 | 附加信息 (任期、背景等) |

> **关联说明**: 当 `person_id` 非空时，可通过 ID 到 `persons/` 目录找到该人物的深度画像。

### 3.6 departments

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dept_id | string | 是 | 部门 ID (格式: `{org_id}-DEPT-{SEQ}`) |
| name | string | 是 | 部门名称 |
| head | string\|null | 否 | 部门负责人姓名 |
| description | string\|null | 否 | 职能描述 |
| parent_dept_id | string\|null | 否 | 上级部门 ID，null 表示顶级部门 |

> **可视化建议**: `parent_dept_id` 可构建组织架构树。

### 3.7 recent_events

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 日期 `YYYY-MM-DD` |
| title | string | 是 | 事件标题 |
| description | string | 是 | 事件详情 |
| impact | string\|null | 否 | 影响评估 |
| source | string\|null | 否 | 来源 URL |

### 3.8 related_entities

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| org_id | string | 是 | 关联组织 ID |
| org_name | string | 是 | 关联组织名称 |
| org_type | enum\|null | 否 | 组织类型代码 |
| org_description | string\|null | 否 | 关系描述 |
| relationship_type | enum | 是 | 关系类型 (见 §5.5) |

> **可视化建议**: `related_entities` 是构建知识图谱 (关系网络) 的核心数据。source = `org_id`, target = `related_entities[].org_id`, edge label = `relationship_type`。

### 3.9 profile (图片)

| 字段 | 类型 | 说明 |
|------|------|------|
| source_url | string\|null | 原始图片 URL (Wikipedia/Wikimedia Commons) |
| local_path | string\|null | 本地下载路径 (相对 output 目录，如 `photos/SG-GOV-001.png`) |

> **当前状态**: 48 个组织中有 38 个有 `source_url`，`local_path` 均为 null (未下载)。

### 3.10 collection_meta

| 字段 | 类型 | 说明 |
|------|------|------|
| collection_date | string | 采集日期 `YYYY-MM-DD` |
| phase | string | 采集阶段 (`phase2_deep_profile`) |
| data_sources | string[] | 数据来源列表 |
| completeness_score | integer | 完整度评分 0–100 |
| notes | string\|null | 采集备注 |

---

## 4. 人物画像数据结构 (person_profile)

### 4.1 完整字段表

```json
{
  "person_id": "SG-PERSON-000005",
  "wikidata_qid": "Q57643",
  "name": "黄循财",
  "name_zh": "黄循财",
  "name_en": "Lawrence Wong",
  "aliases": ["Lawrence Wong Shyun Tsai"],
  "nationality": "SG",
  "gender": "male",
  "birth_date": "1972-12-18",
  "birth_place": "Singapore",
  "contacts": [],
  "current_positions": ["Prime Minister of Singapore", "Minister for Finance"],
  "education": [ /* 见 4.2 */ ],
  "work_experience": [ /* 见 4.3 */ ],
  "person_relationships": [ /* 见 4.4 */ ],
  "social_accounts": [ /* 同组织格式 */ ],
  "family_members": [ /* 见 4.5 */ ],
  "political_stances": [ /* 见 4.6 */ ],
  "major_achievements": [ /* 见 4.7 */ ],
  "biography_summary": "Paragraph text...",
  "profile": { "source_url": "...", "local_path": null },
  "collection_meta": { /* 同组织格式，phase = phase4_person_profile */ }
}
```

### 4.2 education

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| start_date | string\|null | 否 | `YYYY`、`YYYY-MM` 或 `YYYY-MM-DD` |
| end_date | string\|null | 否 | 同上 |
| institution | string | 是 | 学校/机构名称 |
| degree | enum\|null | 否 | 学位级别 (见 §5.6) |
| field | string\|null | 否 | 专业/领域 |

### 4.3 work_experience

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| start_date | string\|null | 否 | `YYYY`、`YYYY-MM` 或 `YYYY-MM-DD` |
| end_date | string\|null | 否 | 同上。**null 表示现任** |
| organization | string | 是 | 组织名称 |
| org_id | string\|null | 否 | 组织 ID，可跨引用 orgs/ 画像 |
| position | string | 是 | 职位名称 |

> **可视化建议**: `end_date == null` 标识当前任职。`org_id` 非空时可链接到组织画像。

### 4.4 person_relationships

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| person_id | string | 是 | 关联人物 ID |
| person_name | string | 是 | 关联人物姓名 |
| relationship_type | enum | 是 | 关系类型 (见 §5.7) |
| description | string\|null | 否 | 关系描述 |

> **可视化建议**: 用于构建人物关系图谱。source = 当前 person_id, target = 关联 person_id。

### 4.5 family_members

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| person_id | string\|null | 否 | 家属人物 ID (如在库中) |
| name | string | 是 | 家属姓名 |
| relationship | enum | 是 | 亲属关系 (见 §5.8) |
| industry_or_organization | string\|null | 否 | 职业/所在组织 |

### 4.6 political_stances

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 时间点 `YYYY`/`YYYY-MM`/`YYYY-MM-DD` |
| topic | string | 是 | 议题 |
| stance_content | string | 是 | 立场/表态内容 |
| source | string\|null | 否 | 信息来源 |

### 4.7 major_achievements

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 时间点 |
| organization | string\|null | 否 | 相关组织 |
| achievement | string | 是 | 成就描述 |

---

## 5. 枚举值对照表

### 5.1 org_type (组织类型)

| 代码 | 英文 | 中文 |
|------|------|------|
| GOV | Government Agency | 政府机构 |
| SOE | State-Owned Enterprise | 国有企业 |
| CORP | Corporation | 企业公司 |
| NGO | Non-Governmental Organization | 非政府组织 |
| ACAD | Academic Institution | 学术机构 |
| MEDIA | Media Organization | 媒体机构 |
| FIN | Financial Institution | 金融机构 |
| INTL | International Organization | 国际组织 |
| PARTY | Political Party | 政党 |
| MIL | Military/Security | 军事安全 |

### 5.2 org_subtype (组织子类型) — 常见值

政府: `head_of_state`, `cabinet`, `ministry`, `statutory_board`, `regulatory_agency`, `legislature`, `judiciary`

企业: `publicly_listed`, `private_company`, `subsidiary`, `conglomerate`, `sovereign_wealth_fund`

学术: `university`, `research_institute`, `think_tank`

媒体: `broadcaster`, `newspaper`, `news_agency`, `digital_media`

政党: `ruling_party`, `opposition_party`

军事: `armed_forces`, `intelligence_agency`, `defence_technology`

> 完整列表见 `org_profile_schema.json` 的 `org_subtype_enum`。

### 5.3 industries (行业) — 常见值

`banking`, `financial_services`, `information_technology`, `telecommunications`, `aviation`, `defence_military`, `higher_education`, `healthcare`, `logistics_warehousing`, `transportation`, `real_estate`, `media_publishing`, `hospitality_tourism`, `energy_oil_gas`, `asset_management`, `fintech`, `insurance`, `public_administration`, `judicial`, `legal_services`, `semiconductors`, `pharmaceuticals`, `retail`

> 完整列表 (约 90 个) 见 `org_profile_schema.json` 的 `industry_enum`。

### 5.4 social_platform (社交平台)

| 代码 | 平台 |
|------|------|
| twitter_x | X (Twitter) |
| facebook | Facebook |
| linkedin | LinkedIn |
| youtube | YouTube |
| instagram | Instagram |
| telegram | Telegram |
| tiktok | TikTok |
| weibo | 新浪微博 |
| wechat | 微信 |
| github | GitHub |

### 5.5 relationship_type (组织间关系)

| 代码 | 含义 |
|------|------|
| parent_org | 上级组织 |
| subsidiary | 子公司/下属机构 |
| controlling_shareholder | 控股股东 |
| member_of | 隶属于 |
| regulator | 监管方 |
| regulated_by | 被监管 |
| predecessor | 前身 |
| successor | 继任 |
| partner | 合作伙伴 |
| strategic_alliance | 战略联盟 |
| supplier | 供应商 |
| customer | 客户 |

### 5.6 degree_level (学位级别)

| 代码 | 中文 |
|------|------|
| high_school | 高中 |
| associate | 大专/副学士 |
| bachelor | 学士 |
| master | 硕士 |
| doctorate | 博士 |
| professional | 专业学位 |
| other | 其他 |

### 5.7 person_relationship_type (人物关系)

家庭: `spouse`, `parent`, `child`, `sibling`

职场: `colleague`, `superior`, `subordinate`, `mentor`, `mentee`

政治/商业: `political_ally`, `political_rival`, `business_partner`, `associate`, `ally`, `rival`

### 5.8 family_relation (亲属关系)

`spouse`, `father`, `mother`, `son`, `daughter`, `brother`, `sister`, `grandfather`, `grandmother`, `uncle`, `aunt`, `cousin`, 以及各类 in-law 关系。

### 5.9 gender (性别)

`male`, `female`, `non_binary`, `unknown`

---

## 6. 索引文件说明

### 6.1 orgs/_index.json

汇总所有组织画像的索引文件，包含统计信息：

```json
{
  "country": "SG",
  "collection_date": "2026-04-15",
  "phase": "phase2_deep_profile",
  "total_profiles": 48,
  "profiles": [
    {
      "org_id": "SG-GOV-001",
      "name": "新加坡最高法院 (Supreme Court of Singapore)",
      "category": "GOV",
      "subcategory": "judiciary",
      "completeness": 78
    }
  ],
  "completeness_summary": {
    "avg_score": 78,
    "high_completeness_gt80": 20,
    "medium_completeness_50_80": 24,
    "low_completeness_lt50": 4
  }
}
```

### 6.2 persons/_index.json

```json
{
  "metadata": {
    "country": "SG",
    "total_profiles": 38,
    "collection_date": "2026-04-15"
  },
  "profiles": [
    {
      "person_id": "SG-PERSON-000005",
      "wikidata_qid": "Q57643",
      "name_en": "Lawrence Wong",
      "name_zh": "黄循财",
      "gender": "male",
      "importance_level": "high",
      "current_title": "Prime Minister",
      "completeness_score": 85,
      "file": "SG-PERSON-000005.json"
    }
  ],
  "completeness_summary": { /* 同组织格式 */ },
  "by_importance_level": { "high": 10, "medium": 12, "low": 16 }
}
```

### 6.3 id_registry.json

主注册表，包含所有组织和人物的 ID 映射：

```json
{
  "registry": [
    {
      "org_id": "SG-GOV-001",
      "name": "新加坡最高法院 (Supreme Court of Singapore)",
      "org_type": "GOV",
      "org_subtype": "judiciary",
      "wikidata_qid": "Q3001103",
      "status": "profiled",
      "notes": null
    }
  ],
  "person_registry": [
    {
      "person_id": "SG-PERSON-000005",
      "name": "黄循财 (Lawrence Wong)",
      "wikidata_qid": "Q57643",
      "status": "profiled",
      "source_orgs": ["SG-GOV-003"]
    }
  ],
  "counters": { "SG": { "GOV": 17, "SOE": 8, "CORP": 7, ... } },
  "person_counters": { "SG": 113 }
}
```

> `status` 字段: `listed` = 已发现未画像, `profiled` = 已完成深度画像。

---

## 7. 关联关系与图谱数据

### 7.1 组织↔组织 (related_entities)

存在组织间关系的记录: **31 条**

边数据提取方式:
```
source: profile.org_id
target: related_entity.org_id
label:  related_entity.relationship_type
desc:   related_entity.org_description
```

### 7.2 组织↔人物 (key_people)

有 key_people 的组织: **22/48**

关联方式:
```
org_id  ← profile.org_id
person_id ← key_people[].person_id  (可关联到 persons/ 画像)
role    ← key_people[].title
```

### 7.3 人物↔人物 (person_relationships)

存在人物关系的记录: **9 条**

### 7.4 人物↔组织 (work_experience)

有工作经历的人物: **26/38**

其中 `org_id` 非空的记录可直接关联到组织画像。

---

## 8. 数据质量与空值统计

### 8.1 组织画像字段覆盖率

| 字段 | 覆盖率 | 说明 |
|------|--------|------|
| core_business | 46/48 (96%) | 极高 |
| website | 44/48 (92%) | 高 |
| social_accounts | 38/48 (79%) | 较高 |
| profile (图片) | 38/48 (79%) | source_url 有值, local_path 未下载 |
| key_people | 22/48 (46%) | 约半数有核心人物 |
| related_entities | 部分有 | 31 条关系 |
| departments | 4/48 (8%) | 仅少数组织有部门数据 |
| recent_events | 4/48 (8%) | 仅少数组织有动态数据 |

### 8.2 人物画像字段覆盖率

| 字段 | 覆盖率 | 说明 |
|------|--------|------|
| biography_summary | 31/38 (82%) | 较高 |
| education | 30/38 (79%) | 较高 |
| work_experience | 26/38 (68%) | 中等 |
| profile (照片) | 22/38 (58%) | source_url 有值 |
| person_relationships | 少量 | 9 条关系 |
| family_members | 少量 | 公开数据稀少 |
| social_accounts | 少量 | 多数政商人物无公开社交账号 |

---

## 9. 可视化开发建议

### 9.1 推荐页面/组件

| 页面 | 数据源 | 核心展示 |
|------|--------|---------|
| 组织目录 | `orgs/_index.json` | 分类列表、搜索、完整度指示 |
| 组织详情 | `orgs/{org_id}.json` | 基础信息、社交链接、核心人物、组织架构、关联关系 |
| 人物目录 | `persons/_index.json` | 按重要性分级、搜索 |
| 人物详情 | `persons/{person_id}.json` | 简历时间线、关系图谱、教育/职业经历 |
| 关系图谱 | `orgs/*.json` + `persons/*.json` | 组织↔组织、组织↔人物、人物↔人物 三层网络 |
| 数据看板 | `id_registry.json` + 索引文件 | 分类统计、完整度分布、覆盖热力图 |

### 9.2 图谱数据提取

从画像文件中提取节点和边的方法：

```python
# 组织关系边
for profile in org_profiles:
    for rel in profile["related_entities"]:
        edge = {
            "source": profile["org_id"],
            "target": rel["org_id"],
            "type": "org-org",
            "label": rel["relationship_type"],
        }

# 组织-人物边
for profile in org_profiles:
    for kp in profile["key_people"]:
        if kp.get("person_id"):
            edge = {
                "source": profile["org_id"],
                "target": kp["person_id"],
                "type": "org-person",
                "label": kp["title"],
            }

# 人物-人物边
for person in person_profiles:
    for rel in person["person_relationships"]:
        edge = {
            "source": person["person_id"],
            "target": rel["person_id"],
            "type": "person-person",
            "label": rel["relationship_type"],
        }
```

### 9.3 日期格式注意事项

所有日期字段存在三种精度：
- `YYYY` — 仅知年份
- `YYYY-MM` — 知年月
- `YYYY-MM-DD` — 完整日期

建议前端统一处理为灵活显示，如 "1972" / "1972-12" / "1972-12-18"。

### 9.4 图片资源

- `profile.source_url`: 指向 Wikimedia Commons 等外部 URL，可直接用作 `<img src>`
- `profile.local_path`: 当前均为 null，如需离线使用需另行下载
- 注意：Wikimedia Commons 图片遵循各类开源协议 (CC-BY-SA 等)

---

## 10. API/对接建议

### 10.1 静态文件服务

所有数据为 JSON 文件，可直接用 Nginx/Express 静态托管：

```
GET /data/sg/2026-04-15/orgs/_index.json
GET /data/sg/2026-04-15/orgs/SG-GOV-004.json
GET /data/sg/2026-04-15/persons/SG-PERSON-000005.json
GET /data/sg/2026-04-15/id_registry.json
```

### 10.2 数据库导入

如需导入数据库，推荐方案：
- **MongoDB**: 直接 `json.load()` → `insert_many()`，schema-free 天然兼容
- **PostgreSQL**: 用 `jsonb` 列存储画像，`org_id`/`person_id` 做主键，`org_type` 做分区键
- **Elasticsearch**: 按字段建索引，支持全文搜索 `core_business`、`biography_summary`

### 10.3 Schema 验证

完整的 JSON Schema 文件位于：
- 组织: `.claude/skills/country-org-collector/org_profile_schema.json`
- 人物: `.claude/skills/country-org-collector/person_profile_schema.json`

可用于前端 TypeScript 类型生成或后端数据校验。

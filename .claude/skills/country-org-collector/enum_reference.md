# Enum Reference / 枚举对照表

All JSON keys and enum values use **English only**. This file provides Chinese translations for reference.

---

## JSON Key Mapping / 字段名对照

### Top-level

| English Key | 中文说明 |
|-------------|---------|
| org_id | 组织ID |
| basic_info | 基础信息 |
| social_accounts | 社交账号 |
| digital_assets | 其他数字资产 |
| key_people | 核心负责人 |
| departments | 组织架构 |
| recent_events | 近期动态 |
| related_entities | 关联实体 |
| core_business | 核心业务 |
| industries | 涉及行业 |
| apec_stance | APEC相关立场 |
| collection_meta | 收集元数据 |

### basic_info

| English Key | 中文说明 |
|-------------|---------|
| name_original | 组织名称(原语言) |
| name_zh | 中文名称 |
| name_en | 英文名称 |
| aliases | 别名(缩写、曾用名) |
| org_type | 组织类型 |
| org_subtype | 组织子类型 |
| country_iso3 | 所属国家(ISO336) |
| hq_country_iso3 | 总部所属国家(ISO336) |
| founded_date | 成立时间 (strict: YYYY-MM-DD) |
| website | 官网地址 |

### social_accounts

| English Key | 中文说明 |
|-------------|---------|
| platform | 社交平台 |
| account_name | 账号名称 |
| url | 主页URL |
| source | 信息来源 |

### digital_assets

| English Key | 中文说明 |
|-------------|---------|
| name | 名称 |
| url | URL链接 |
| description | 描述信息 |
| source | 信息来源 |

### key_people

| English Key | 中文说明 |
|-------------|---------|
| person_id | 人物ID |
| name | 姓名 |
| title | 职位 |
| title_description | 职位描述 |
| description | 补充信息 |

### departments

| English Key | 中文说明 |
|-------------|---------|
| dept_id | 部门ID |
| name | 部门名称 |
| head | 部门负责人 |
| description | 部门职责描述 |
| parent_dept_id | 上级部门ID |

### recent_events

| English Key | 中文说明 |
|-------------|---------|
| date | 时间 (strict: YYYY-MM-DD) |
| title | 事件名称 |
| description | 事件描述 |
| impact | 事件影响 |
| source | 信息来源 |

### related_entities

| English Key | 中文说明 |
|-------------|---------|
| org_id | 组织ID |
| org_name | 组织名称 |
| org_type | 组织类型 |
| org_description | 组织描述 |
| relationship_type | 关系类型 |

### collection_meta

| English Key | 中文说明 |
|-------------|---------|
| collection_date | 收集日期 |
| phase | 阶段标识 |
| data_sources | 数据来源 |
| completeness_score | 完整度评分 |
| notes | 备注 |

---

## Date Format Convention / 日期格式规范

本项目所有日期字段分为两类：

### 精确日期（strict）— 必须为 `YYYY-MM-DD`

| 字段 | 所属 schema |
|------|------------|
| `birth_date` | person |
| `founded_date` | org |
| `collection_date` | org / person |
| `recent_events[].date` | org |

规则：必须为完整 `YYYY-MM-DD`。仅知年份时用 `YYYY-01-01`，仅知年月时用 `YYYY-MM-01`。

### 时间段日期（flexible）— 允许 `YYYY` / `YYYY-MM` / `YYYY-MM-DD`

| 字段 | 所属 schema |
|------|------------|
| `education[].start_date` | person |
| `education[].end_date` | person |
| `work_experience[].start_date` | person |
| `work_experience[].end_date` | person |
| `political_stances[].date` | person |
| `major_achievements[].date` | person |

规则：按实际已知最高精度填写。未知时填 `null`。

---

## Enum: org_type / 组织类型

| Value | 中文 |
|-------|------|
| GOV | 政府机构 |
| SOE | 国有企业 |
| CORP | 企业公司 |
| NGO | 非政府组织 |
| ACAD | 学术机构 |
| MEDIA | 媒体机构 |
| FIN | 金融机构 |
| INTL | 国际组织 |
| PARTY | 政党 |
| MIL | 军事安全 |

---

## Enum: org_subtype / 组织子类型

### GOV

| Value | 中文 |
|-------|------|
| head_of_state | 国家元首 |
| cabinet | 内阁 |
| ministry | 部委 |
| statutory_board | 法定机构 |
| regulatory_agency | 监管机构 |
| legislature | 立法机关 |
| judiciary | 司法机关 |
| independent_organ | 独立国家机关 |
| gov_department | 政府部门 |
| local_government | 地方政府 |

### SOE

| Value | 中文 |
|-------|------|
| state_owned_enterprise | 国有企业 |
| sovereign_wealth_fund | 主权财富基金 |
| gov_linked_company | 政联公司 |
| gov_investment_vehicle | 政府投资机构 |

### CORP

| Value | 中文 |
|-------|------|
| publicly_listed | 上市公司 |
| private_company | 私营企业 |
| startup | 初创企业 |
| subsidiary | 子公司 |
| joint_venture | 合资企业 |
| holding_company | 控股公司 |
| conglomerate | 综合企业集团 |

### NGO

| Value | 中文 |
|-------|------|
| charity | 慈善机构 |
| foundation | 基金会 |
| advocacy_group | 倡导组织 |
| professional_association | 专业协会 |
| trade_union | 工会 |
| humanitarian_org | 人道主义组织 |
| religious_org | 宗教组织 |
| community_org | 社区组织 |

### ACAD

| Value | 中文 |
|-------|------|
| university | 大学 |
| research_institute | 研究所 |
| think_tank | 智库 |
| polytechnic | 理工学院 |
| vocational_school | 职业学校 |

### MEDIA

| Value | 中文 |
|-------|------|
| broadcaster | 广播电视公司 |
| newspaper | 报社 |
| news_agency | 通讯社 |
| digital_media | 数字媒体 |
| publisher | 出版社 |

### FIN

| Value | 中文 |
|-------|------|
| commercial_bank | 商业银行 |
| investment_bank | 投资银行 |
| insurance_company | 保险公司 |
| asset_management | 资产管理 |
| fintech | 金融科技 |
| payment_institution | 支付机构 |

### INTL

| Value | 中文 |
|-------|------|
| multilateral_org | 多边组织 |
| regional_org | 区域组织 |
| standards_body | 标准机构 |

### PARTY

| Value | 中文 |
|-------|------|
| ruling_party | 执政党 |
| opposition_party | 反对党 |
| coalition | 联盟 |

### MIL

| Value | 中文 |
|-------|------|
| armed_forces | 武装力量 |
| intelligence_agency | 情报机构 |
| security_agency | 安全机构 |
| defence_technology | 国防科技 |
| military_academy | 军事院校 |

---

## Enum: relationship_type / 关联关系类型

| Value | 中文 | 方向 |
|-------|------|------|
| parent_org | 上级组织 | 本组织 → 上级 |
| subsidiary | 下属组织 | 本组织 → 下级 |
| controlling_shareholder | 控股方 | 本组织 → 控股方 |
| minority_shareholder | 参股方 | 本组织 → 参股方 |
| sibling | 同一母公司下属 | 本组织 → 兄弟组织 |
| partner | 合作伙伴 | 双向 |
| regulator | 监管机构 | 本组织 → 监管方 |
| regulated_by | 被监管方 | 本组织 → 被监管方 |
| member_of | 成员组织 | 本组织 → 所属联盟 |
| predecessor | 前身 | 本组织 → 前身 |
| successor | 后继 | 本组织 → 后继 |
| affiliated | 关联公司 | 双向 |
| supplier | 供应商 | 本组织 → 供应商 |
| customer | 客户 | 本组织 → 客户 |
| strategic_alliance | 战略联盟 | 双向 |

---

## Enum: industry / 涉及行业

| Value | 中文 |
|-------|------|
| aerospace_defense | 航空航天与国防 |
| agriculture_food | 农业与食品 |
| asset_management | 资产管理 |
| automotive | 汽车 |
| aviation | 航空运输 |
| banking | 银行业 |
| biotechnology | 生物技术 |
| broadcasting | 广播电视 |
| chemicals | 化工 |
| civil_service | 公共服务 |
| cloud_computing | 云计算 |
| construction | 建筑 |
| consulting | 咨询 |
| consumer_electronics | 消费电子 |
| cryptocurrency_digital_assets | 加密货币与数字资产 |
| cybersecurity | 网络安全 |
| defence_military | 国防军工 |
| digital_media | 数字媒体 |
| ecommerce | 电子商务 |
| education | 教育 |
| electricity_gas | 电力与燃气 |
| electronic_components | 电子元器件 |
| energy_oil_gas | 石油天然气 |
| energy_renewable | 可再生能源 |
| engineering | 工程技术 |
| environmental_services | 环境服务 |
| financial_services | 金融服务 |
| fintech | 金融科技 |
| fisheries_aquaculture | 渔业与水产 |
| food_beverage | 食品饮料 |
| foreign_affairs | 外交事务 |
| forestry_timber | 林业 |
| gaming | 游戏娱乐 |
| healthcare | 医疗保健 |
| higher_education | 高等教育 |
| hospitality_tourism | 酒店与旅游 |
| humanitarian_aid | 人道主义援助 |
| industrial_manufacturing | 工业制造 |
| information_technology | 信息技术 |
| infrastructure | 基础设施 |
| insurance | 保险业 |
| intelligence_security | 情报安全 |
| internal_security | 内部安全 |
| international_trade | 国际贸易 |
| internet_services | 互联网服务 |
| investment | 投资 |
| judicial | 司法 |
| legal_services | 法律服务 |
| legislative | 立法 |
| logistics_warehousing | 物流仓储 |
| maritime_shipping | 海事航运 |
| media_publishing | 媒体出版 |
| metal_mining | 金属与采矿 |
| microelectronics | 微电子 |
| mining | 采矿 |
| mobile_telecommunications | 移动通信 |
| monetary_policy | 货币政策 |
| nonprofit | 非营利 |
| nuclear_energy | 核能 |
| payment_services | 支付服务 |
| petrochemicals | 石化 |
| pharmaceuticals | 制药 |
| port_operations | 港口运营 |
| professional_services | 专业服务 |
| public_administration | 公共管理 |
| public_health | 公共卫生 |
| public_transport | 公共交通 |
| railway | 铁路 |
| real_estate | 房地产 |
| regulatory | 监管 |
| research_development | 研发 |
| retail | 零售 |
| robotics | 机器人 |
| semiconductors | 半导体 |
| social_services | 社会服务 |
| software | 软件 |
| space | 航天 |
| sports | 体育 |
| steel | 钢铁 |
| supply_chain | 供应链 |
| surveillance | 监控 |
| sustainability | 可持续发展 |
| telecommunications | 电信 |
| textiles_apparel | 纺织服装 |
| think_tank | 智库 |
| tobacco | 烟草 |
| tourism | 旅游业 |
| trade_finance | 贸易金融 |
| transportation | 交通运输 |
| urban_planning | 城市规划 |
| utilities | 公用事业 |
| venture_capital | 风险投资 |
| water | 水务 |
| weapons_armaments | 武器装备 |

---

## Enum: social_platform / 社交平台

| Value | 中文 |
|-------|------|
| twitter_x | Twitter/X |
| facebook | Facebook |
| linkedin | LinkedIn |
| youtube | YouTube |
| instagram | Instagram |
| telegram | Telegram |
| tiktok | TikTok |
| threads | Threads |
| mastodon | Mastodon |
| wechat | 微信 |
| weibo | 微博 |
| github | GitHub |
| gitlab | GitLab |
| medium | Medium |
| substack | Substack |
| other | 其他 |

---

## Enum: data_sources / 数据来源

| Value | 中文 |
|-------|------|
| official_website | 官方网站 |
| wikipedia | Wikipedia |
| wikidata | Wikidata |
| news_search | 新闻搜索 |
| web_search | Web搜索 |
| opencorporates | OpenCorporates |
| government_registry | 政府注册库 |
| government_directory | 政府名录（如 sgdi.gov.sg） |
| social_media | 社交媒体 |
| annual_report | 年度报告 |
| other | 其他 |

---

# 人物字段对照 / Person Key Mapping

## Person List (Phase 3)

| English Key | 中文说明 |
|-------------|---------|
| person_id | 人物ID |
| wikidata_qid | Wikidata实体ID |
| name | 姓名 |
| name_zh | 中文名 |
| name_en | 英文名 |
| importance_level | 重要等级 |
| importance_reason | 评级理由 |
| source_orgs | 来源组织 |
| discovery_source | 发现来源 |
| nationality | 国籍 |
| notes | 备注 |

## Person Profile (Phase 4)

| English Key | 中文说明 |
|-------------|---------|
| person_id | 人物ID |
| wikidata_qid | Wikidata实体ID |
| name | 原语言姓名 |
| name_zh | 中文名 |
| name_en | 英文名 |
| aliases | 别名（昵称、外文名、异译）|
| nationality | 国籍 |
| gender | 性别 |
| birth_date | 出生日期 (strict: YYYY-MM-DD) |
| birth_place | 出生地 |
| contacts | 联系方式 |
| current_positions | 现任职务（职务名称数组）|
| education | 教育经历 |
| work_experience | 工作经历 |
| person_relationships | 人际关系 |
| social_accounts | 社交账号 |
| family_members | 家庭成员 |
| political_stances | 政治立场 |
| major_achievements | 主要成就 |
| biography_summary | 生平简介 |
| profile | 照片/头像 |
| collection_meta | 收集元数据 |

### contacts

| English Key | 中文说明 |
|-------------|---------|
| type | 联系类型 |
| value | 联系值 |
| source | 信息来源 |

### education

| English Key | 中文说明 |
|-------------|---------|
| start_date | 开始日期 (flexible: YYYY / YYYY-MM / YYYY-MM-DD) |
| end_date | 结束日期 (flexible: YYYY / YYYY-MM / YYYY-MM-DD) |
| institution | 院校名称 |
| degree | 学位等级 |
| field | 专业领域 |

### work_experience

| English Key | 中文说明 |
|-------------|---------|
| start_date | 开始日期 (flexible: YYYY / YYYY-MM / YYYY-MM-DD) |
| end_date | 结束日期 (flexible: YYYY / YYYY-MM / YYYY-MM-DD) |
| organization | 组织名称 |
| org_id | 组织ID（若在收集范围内）|
| position | 职位 |

### person_relationships

| English Key | 中文说明 |
|-------------|---------|
| person_id | 目标人物ID |
| person_name | 目标人物姓名 |
| relationship_type | 关系类型 |
| description | 关系说明 |

### family_members

| English Key | 中文说明 |
|-------------|---------|
| person_id | 人物ID（若在收集范围内）|
| name | 姓名 |
| relationship | 亲属关系 |
| industry_or_organization | 所在行业或组织 |

### political_stances

| English Key | 中文说明 |
|-------------|---------|
| date | 日期 (flexible: YYYY / YYYY-MM / YYYY-MM-DD) |
| topic | 议题 |
| stance_content | 立场内容 |
| source | 信息来源 |

### major_achievements

| English Key | 中文说明 |
|-------------|---------|
| date | 日期 (flexible: YYYY / YYYY-MM / YYYY-MM-DD) |
| organization | 关联组织 |
| achievement | 成就描述 |

---

# 人物枚举 / Person Enums

---

## Enum: importance_level / 重要等级

| Value | 中文 |
|-------|------|
| high | 高（现任最高领导人、核心决策层）|
| medium | 中（部长级/副手/核心管理层）|
| low | 低（普通成员/委员/一般官员）|

---

## Enum: discovery_source / 发现来源

| Value | 中文 |
|-------|------|
| key_people | 组织画像key_people提取 |
| web_search | Web搜索发现 |
| wikidata | Wikidata查询发现 |
| wikipedia | Wikipedia词条发现 |
| other | 其他 |

---

## Enum: gender / 性别

| Value | 中文 |
|-------|------|
| male | 男性 |
| female | 女性 |
| non_binary | 非二元性别 |
| unknown | 不详 |

---

## Enum: contact_type / 联系类型

| Value | 中文 |
|-------|------|
| phone | 电话 |
| email | 电子邮件 |
| fax | 传真 |
| website | 个人网站 |
| other | 其他 |

---

## Enum: degree_level / 学位等级

| Value | 中文 |
|-------|------|
| primary | 小学 |
| high_school | 高中 |
| associate | 副学士/专科 |
| bachelor | 学士 |
| master | 硕士 |
| doctorate | 博士 |
| professional | 专业学位（MD/JD/MBA等）|
| other | 其他 |

---

## Enum: person_relationship_type / 人物关系类型

| Value | 中文 | 方向 | 互逆关系 |
|-------|------|------|---------|
| spouse | 配偶 | 双向 | spouse |
| parent | 父/母 | A→B (A是B的父/母) | child |
| child | 子/女 | A→B (A是B的子/女) | parent |
| sibling | 兄弟姐妹 | 双向 | sibling |
| grandparent | 祖辈 | A→B (A是B的祖辈) | grandchild |
| grandchild | 孙辈 | A→B (A是B的孙辈) | grandparent |
| uncle_aunt | 叔伯姑舅姨 | A→B | cousin |
| cousin | 堂表兄弟姐妹 | 双向 | cousin |
| in_law | 姻亲 | 双向 | in_law |
| mentor | 导师 | A→B (A指导B) | mentee |
| mentee | 学生/门生 | A→B (A受B指导) | mentor |
| ally | 盟友 | 双向 | ally |
| rival | 对手 | 双向 | rival |
| colleague | 同事 | 双向 | colleague |
| superior | 上级 | A→B (A是B的上级) | subordinate |
| subordinate | 下属 | A→B (A是B的下属) | superior |
| business_partner | 商业伙伴 | 双向 | business_partner |
| political_ally | 政治盟友 | 双向 | political_ally |
| political_rival | 政治对手 | 双向 | political_rival |
| associate | 关联人 | 双向 | associate |
| other | 其他 | - | other |

---

## Enum: family_relation / 家庭关系

| Value | 中文 |
|-------|------|
| spouse | 配偶 |
| father | 父亲 |
| mother | 母亲 |
| son | 儿子 |
| daughter | 女儿 |
| brother | 兄弟 |
| sister | 姐妹 |
| grandfather | 祖父/外祖父 |
| grandmother | 祖母/外祖母 |
| uncle | 叔伯舅 |
| aunt | 姑姨婶 |
| cousin | 堂表兄弟姐妹 |
| father_in_law | 岳父/公公 |
| mother_in_law | 岳母/婆婆 |
| brother_in_law | 内兄/姐夫/小叔 |
| sister_in_law | 嫂子/弟媳/姑子 |
| son_in_law | 女婿 |
| daughter_in_law | 儿媳 |
| other | 其他 |

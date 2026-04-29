# 组织 SPARQL 模板与 API 参考

> Phase 1（广度扫描）和 Phase 2-3（组织画像）使用。按需 Read 本文件，不要在人物收集阶段加载。

## 组织分类 Wikidata P31 映射

| 分类代码 | 标签 | Wikidata 类（P31 值） |
|---------|------|---------------------|
| GOV | 政府机构 | 见下方 GOV 子分类 |
| SOE | 国有企业 | Q3230, Q582058 |
| CORP | 企业公司 | Q4830453, Q783794 |
| NGO | 非政府组织 | Q163740, Q43229, Q104932 |
| ACAD | 学术机构 | Q3918, Q31855, Q15978631 |
| MEDIA | 媒体机构 | Q192621, Q15416, Q2085381 |
| FIN | 金融机构 | Q22687, Q1290325 |
| INTL | 国际组织 | Q484652 |
| PARTY | 政党 | Q7278 |
| MIL | 军事安全 | Q176742, Q1138001 |

### GOV 子分类

| subcategory | 说明 | Wikidata 类 |
|-------------|------|------------|
| Head of State / 国家元首 | 总统、君主等 | Q12106, Q193505 |
| Executive Branch / 行政机关（内阁） | 内阁、国务委员会 | Q162919, Q4164870 |
| Ministry / 行政机关（部委） | 政府各部委 | Q648294 |
| Statutory Board / 法定机构 | 依法设立的半自治机构 | Q327333 |
| Legislature / 立法机关 | 国会、议会 | Q11204, Q190752 |
| Judiciary / 司法机关 | 最高法院、各级法院 | Q41487, Q845161 |
| Independent Organ / 独立国家机关 | 审计署、检察署、选举委员会 | Q327333, Q648294 |

## SPARQL 限速

请求间隔 ≥12 秒，每分钟 ≤5 次。

## Wikidata SPARQL 模板

**端点**：`https://query.wikidata.org/sparql`

> **重要**：所有模板避免 `wdt:P31/wdt:P279*`（传递子类），改用 `wdt:P31` + `VALUES` 列表。
> **重要**：本地 Python urllib 访问 Wikipedia 系站点必须设置 `User-Agent` header，否则返回 403 Forbidden。

### 模板 H：国家权力机构（必须优先执行）

```
SELECT ?org ?orgLabel ?orgDescription ?typeLabel ?parentLabel ?headLabel ?website
WHERE {
  ?org wdt:P17 wd:{COUNTRY_QID} .
  ?org wdt:P31 ?type .
  VALUES ?type {
    wd:Q648294    wd:Q4164870   wd:Q11204
    wd:Q190752    wd:Q41487     wd:Q845161
    wd:Q12106     wd:Q193505
  }
  OPTIONAL { ?org wdt:P749 ?parent . }
  OPTIONAL { ?org wdt:P1308 ?head . }
  OPTIONAL { ?org wdt:P856 ?website . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh" . }
} LIMIT 200
```

### 模板 A：通用组织

```
SELECT ?org ?orgLabel ?orgDescription ?typeLabel ?hqLabel ?inception ?website
WHERE {
  ?org wdt:P17 wd:{COUNTRY_QID} .
  ?org wdt:P31 ?type .
  VALUES ?type {
    wd:Q43229 wd:Q4830453 wd:Q783794 wd:Q327333 wd:Q648294
    wd:Q3918 wd:Q7278 wd:Q22687 wd:Q163740 wd:Q192621 wd:Q15416
    wd:Q3230 wd:Q176742 wd:Q484652
  }
  OPTIONAL { ?org wdt:P159 ?hq . }
  OPTIONAL { ?org wdt:P571 ?inception . }
  OPTIONAL { ?org wdt:P856 ?website . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh" . }
} LIMIT {LIMIT}
```

### 模板 B：企业公司（CORP）

```
SELECT ?org ?orgLabel ?orgDescription ?industryLabel ?employees ?revenue ?hqLabel ?ticker ?website
WHERE {
  ?org wdt:P17 wd:{COUNTRY_QID} .
  ?org wdt:P31 ?type .
  VALUES ?type { wd:Q4830453 wd:Q783794 }
  OPTIONAL { ?org wdt:P452 ?industry . }
  OPTIONAL { ?org wdt:P1128 ?employees . }
  OPTIONAL { ?org wdt:P2139 ?revenue . }
  OPTIONAL { ?org wdt:P159 ?hq . }
  OPTIONAL { ?org wdt:P249 ?ticker . }
  OPTIONAL { ?org wdt:P856 ?website . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh" . }
} LIMIT 300
```

### 模板 C：学术机构（ACAD）

```
SELECT ?org ?orgLabel ?orgDescription ?typeLabel ?established ?website
WHERE {
  ?org wdt:P17 wd:{COUNTRY_QID} .
  ?org wdt:P31 ?type .
  VALUES ?type { wd:Q3918 wd:Q31855 wd:Q15978631 }
  OPTIONAL { ?org wdt:P571 ?established . }
  OPTIONAL { ?org wdt:P856 ?website . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh" . }
} LIMIT 200
```

### 模板 D：政党（PARTY）

```
SELECT ?org ?orgLabel ?orgDescription ?ideologyLabel ?chairLabel ?founded ?website
WHERE {
  ?org wdt:P17 wd:{COUNTRY_QID} .
  ?org wdt:P31 wd:Q7278 .
  OPTIONAL { ?org wdt:P1142 ?ideology . }
  OPTIONAL { ?org wdt:P488 ?chair . }
  OPTIONAL { ?org wdt:P571 ?founded . }
  OPTIONAL { ?org wdt:P856 ?website . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh" . }
} LIMIT 100
```

### 模板 E：媒体机构（MEDIA）

```
SELECT ?org ?orgLabel ?orgDescription ?typeLabel ?hqLabel ?founded ?website
WHERE {
  ?org wdt:P17 wd:{COUNTRY_QID} .
  ?org wdt:P31 ?type .
  VALUES ?type { wd:Q192621 wd:Q15416 wd:Q2085381 wd:Q1153192 }
  OPTIONAL { ?org wdt:P159 ?hq . }
  OPTIONAL { ?org wdt:P571 ?founded . }
  OPTIONAL { ?org wdt:P856 ?website . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh" . }
} LIMIT 200
```

### 模板 F：金融机构（FIN）

```
SELECT ?org ?orgLabel ?orgDescription ?typeLabel ?hqLabel ?founded ?website
WHERE {
  ?org wdt:P17 wd:{COUNTRY_QID} .
  ?org wdt:P31 ?type .
  VALUES ?type { wd:Q22687 wd:Q1290325 }
  OPTIONAL { ?org wdt:P159 ?hq . }
  OPTIONAL { ?org wdt:P571 ?founded . }
  OPTIONAL { ?org wdt:P856 ?website . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh" . }
} LIMIT 200
```

### 模板 G：组织关系网络（Phase 2-3 画像阶段使用）

```
SELECT ?propLabel ?targetLabel ?targetDescription
WHERE {
  wd:{ORG_QID} ?prop ?target .
  ?prop wikibase:directClaim ?directProp .
  ?prop rdfs:label ?propLabel .
  FILTER(LANG(?propLabel) = "en")
  VALUES ?directProp { wdt:P749 wdt:P355 wdt:P1365 wdt:P1366 wdt:P1269 wdt:P488 wdt:P169 wdt:P463 }
  ?target rdfs:label ?targetLabel .
  FILTER(LANG(?targetLabel) = "en")
} LIMIT 100
```

## Wikidata EntityData API

当 SPARQL 查询特定实体的属性返回空结果（`{"bindings": []}`）时，使用 EntityData API 直接获取完整实体数据。

**端点**：`https://www.wikidata.org/wiki/Special/EntityData/{QID}.json`

**调用方式**：本地 curl + 代理（最稳定）

```bash
curl --proxy "http://10.11.204.68:8081" -s -L -H "User-Agent: Mozilla/5.0" \
  "https://www.wikidata.org/wiki/Special/EntityData/Q371395.json" | python -m json.tool
```

**返回结构**：`entities.{QID}.claims.{PROPERTY}` 包含该实体的所有属性声明。

**组织属性映射**：

| Wikidata 属性 | 含义 | 对应 profile 字段 |
|--------------|------|-----------------|
| P31 | 实例类型 | org_type 映射依据 |
| P17 | 国家 | country |
| P571 | 成立日期 | founded_date |
| P159 | 总部位置 | headquarters |
| P856 | 官方网站 | website |
| P488 | 主席/负责人 | key_people |
| P1142 | 意识形态 | description 补充 |
| P112 | 创始人 | description 补充 |
| P749 | 上级组织 | parent_organization |
| P355 | 子公司 | relationships |
| P154 | logo | logo_url |
| P452 | 行业 | industries |

**适用场景**：
- SPARQL 查询返回 `{"bindings": []}` 时
- 需要获取某个实体的全部属性（不需要逐条 SPARQL）
- 组织画像阶段查询单个组织的完整数据

**注意**：返回数据量大（单个实体可能 >100KB），需要通过 Python 脚本解析提取所需字段。

## Wikipedia REST API

**端点**：`https://en.wikipedia.org/api/rest_v1/page/summary/{page_title}`

**调用方式**：`mcp__search-read__read_url`（最便捷）、本地 curl/Python + 代理（备用）

**返回字段**：

| 字段 | 说明 | 用途 |
|------|------|------|
| `title` | 页面标题 | 组织名称 |
| `description` | 短描述 | 一句话定位 |
| `extract` | 首段摘要（~200字） | 组织简介 |
| `wikibase_item` | Wikidata QID | 交叉引用 Wikidata |
| `coordinates` | 经纬度 | 总部位置 |
| `thumbnail.source` | 缩略图 URL | logo/图片 |

**优势**：JSON 干净、轻量、直接提供 Wikidata QID，适合从已知组织名称快速获取结构化信息。

**局限**：需要精确的 Wikipedia 页面标题。可通过搜索结果中的链接获取标题。

**示例**：

```bash
curl --proxy "http://10.11.204.68:8081" -s -L -H "User-Agent: Mozilla/5.0" \
  "https://en.wikipedia.org/api/rest_v1/page/summary/Parliament_of_Singapore"
# 返回: {"title":"Parliament of Singapore","wikibase_item":"Q1517231","description":"Legislature of Singapore",...}
```

## DBpedia SPARQL

**端点**：`https://dbpedia.org/sparql`（必须 HTTPS）

**调用方式**：仅本地 curl（MCP 工具对含 OPTIONAL/FILTER 的复杂查询会静默失败）

**关键注意事项**：

1. **必须使用 HTTPS**，HTTP 会被拒绝（406 Not Acceptable）
2. **必须设置正确的 Accept header**：`-H "Accept: application/sparql-results+json"`
3. **用 `dbo:location` 而不是 `dbo:country`** 过滤国家（DBpedia 本体中多数组织用 location 而非 country）
4. **结果有 3 倍重复**（不同数据集图），需去重
5. **数据比 Wikidata 少**，仅作补充

**可用属性**：`dbo:establishmentDate`、`dbo:numberOfMembers`、`dbo:leader`、`dbo:electionDateLeader`、`dbo:lastElectionDate`、`dbo:description`、`dbo:location`

**SPARQL 模板 — 按国家和类型查组织**：

```
SELECT DISTINCT ?org ?label ?members ?leader
WHERE {
  ?org a dbo:Legislature .
  ?org dbo:location dbr:{COUNTRY_NAME} .
  OPTIONAL { ?org rdfs:label ?label . FILTER(lang(?label) = "en") }
  OPTIONAL { ?org dbo:numberOfMembers ?members }
  OPTIONAL { ?org dbo:leader ?leader }
} LIMIT 20
```

**SPARQL 模板 — 查特定组织的属性**：

```
SELECT ?prop ?val WHERE {
  <http://dbpedia.org/resource/{ENTITY_NAME}> ?prop ?val .
  ?prop a rdf:Property .
  FILTER(STRSTARTS(STR(?prop), "http://dbpedia.org/ontology/"))
  FILTER(!STRSTARTS(STR(?prop), "http://dbpedia.org/ontology/wiki"))
} LIMIT 50
```

**curl 示例**：

```bash
curl -s -H "Accept: application/sparql-results+json" \
  --data-urlencode 'query=SELECT DISTINCT ?org ?label WHERE { ?org a dbo:Legislature . ?org dbo:location dbr:Singapore . OPTIONAL{?org rdfs:label ?label . FILTER(lang(?label)="en")} } LIMIT 10' \
  "https://dbpedia.org/sparql?format=json"
```

# 人物 SPARQL 模板与 API 参考

> Phase 5（人物清单生成）和 Phase 6（人物画像生成）使用。按需 Read 本文件。

## SPARQL 限速

请求间隔 ≥12 秒，每分钟 ≤5 次。

## Wikidata SPARQL 模板

**端点**：`https://query.wikidata.org/sparql`

### 模板 I：查询组织关联人物（Phase 5 使用）

```
SELECT ?person ?personLabel ?personDescription ?roleLabel ?startDate ?endDate
WHERE {
  ?org wdt:P17 wd:{COUNTRY_QID} .
  ?org rdfs:label "{ORG_NAME}"@en .
  {
    ?org wdt:P488 ?person .        # 主席
  } UNION {
    ?org wdt:P169 ?person .        # CEO
  } UNION {
    ?org wdt:P1308 ?person .       # 负责人
  } UNION {
    ?org wdt:P355 ?sub .           # 子组织负责人
    ?sub wdt:P488|wdt:P169|wdt:P1308 ?person .
  } UNION {
    ?org wdt:P527 ?member .        # 组成部分成员
    ?member wdt:P488|wdt:P169|wdt:P1308 ?person .
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh" . }
}
LIMIT 100
```

### 模板 J：查询 Wikidata 中"职位持有者"（Phase 5 使用）

```
SELECT ?person ?personLabel ?positionLabel ?startDate ?endDate
WHERE {
  ?person wdt:P39 ?position .
  ?position ps:P39 ?posItem .
  ?posItem wdt:P17 wd:{COUNTRY_QID} .
  OPTIONAL { ?position pq:P580 ?startDate . }
  OPTIONAL { ?position pq:P582 ?endDate . }
  FILTER(!BOUND(?endDate) || ?endDate > "2020-01-01"^^xsd:dateTime)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh" . }
}
LIMIT 200
```

### 模板 K：按姓名搜索人物 QID（Phase 5 去重使用）

```
SELECT ?person ?personLabel ?personDescription
WHERE {
  ?person wdt:P27 wd:{COUNTRY_QID} .
  ?person rdfs:label "{PERSON_NAME}"@en .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh" . }
}
LIMIT 5
```

## Wikidata EntityData API（Phase 6 人物画像使用）

**端点**：`https://www.wikidata.org/wiki/Special/EntityData/{QID}.json`

**调用方式**：本地 curl + 代理

```bash
curl --proxy "http://127.0.0.1:7890" -s -L -H "User-Agent: Mozilla/5.0" \
  "https://www.wikidata.org/wiki/Special/EntityData/Q115727460.json" | python -m json.tool
```

**人物属性映射表**：

| Wikidata 属性 | 含义 | 对应 profile 字段 |
|--------------|------|-----------------|
| P31 | 实例类型 | 验证是人物 (Q5) |
| P21 | 性别 | gender（male ↔ Q6581097, female ↔ Q6581072） |
| P569 | 出生日期 | birth_date |
| P19 | 出生地 | birth_place |
| P27 | 国籍 | nationality |
| P735 | 名 | name_en 补充 |
| P734 | 姓 | name_en 补充 |
| P1477 | 本名 | aliases |
| P1559 | 原语言姓名 | name 补充 |
| P69 | 就读院校 | education |
| P512 | 学位等级 | education.degree |
| P812 | 专业领域 | education.field |
| P39 | 担任职位 | current_positions / work_experience |
| P108 | 雇主 | work_experience |
| P463 | 所属组织 | current_positions |
| P26 | 配偶 | family_members (spouse) |
| P22 | 父亲 | family_members (father) |
| P25 | 母亲 | family_members (mother) |
| P40 | 子女 | family_members (son/daughter) |
| P3373 | 兄弟姐妹 | family_members (brother/sister) |
| P7 | 兄弟姐妹 | family_members (brother/sister) |
| P451 | 未婚伴侣 | person_relationships |
| P6411 | 政党成员 | current_positions 补充 |
| P102 | 政党 | current_positions 补充 |
| P856 | 官方网站 | contacts (website) |
| P2002 | Twitter ID | social_accounts (twitter_x) |
| P2013 | Facebook ID | social_accounts (facebook) |
| P2397 | YouTube channel | social_accounts (youtube) |
| P4264 | Instagram username | social_accounts (instagram) |
| P6634 | LinkedIn ID | social_accounts (linkedin) |

**注意**：返回数据量大（单个实体可能 >100KB），需要通过 Python 脚本解析提取所需字段。

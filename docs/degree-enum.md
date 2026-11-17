# 学历（degree）标准与归一规则 — 外部业务系统交付版 v2

> 版本：2026-11-17 v2（含全库归一执行结果）
> 数据源：`apec-osint-tool` 人物画像 `education[].degree` 字段
> 基线：54 个数据集，37,493 条教育经历，**100% 标准枚举**（0 脏值）

## 一、标准枚举（8 值 + null）

| 枚举值 | 中文 | 判定标准 | 归一后库内分布 |
|---|---|---|---:|
| `primary` | 小学 | 小学阶段 | 1,115 |
| `high_school` | 高中/中学 | 初中、高中、中等教育、A-Level/SPM 等预科 | 3,752 |
| `associate` | 大专/副学士 | Associate degree、专科、大专文凭 | 349 |
| `bachelor` | 学士 | 本科学位：BA/BSc/LLB/BBA/MBBS 等（含荣誉学士） | 10,622 |
| `master` | 硕士 | MA/MSc/LLM/MPhil/MPA/MBA/EMBA（含在读 candidate 类） | 8,194 |
| `doctorate` | 博士 | PhD/DPhil/JD/DBA；**含荣誉博士**；博士后也归此级 | 3,241 |
| `professional` | 职业资格/专业教育 | 非学位：执业资格（律师/会计师）、研修结业、高管课程、军校/党校课程、residency | 2,865 |
| `other` | 其他 | 有信息但无法归入以上类别 | 3,439 |
| `null` | 未知/未公开 | 字段为 JSON null | 3,916 |

## 二、判定细则（外部系统实现时参照）

1. **null ≠ other**：`null` = 未采集到数据；`other` = 有信息但无法归类。业务侧应区分展示（"未知" vs "其他"）。
2. **MBA/EMBA** → `master`；细分专业看 `field` 字段。
3. **JD（Juris Doctor）/ DBA / MBBS**：虽名称含 Doctor/Bachelor，按各国学制实际等级归——JD→`doctorate`（美国法律职业博士），MBBS→`bachelor`（英联邦医学本科）。
4. **荣誉博士**（honorary doctorate）→ `doctorate`；荣誉性质应在 `note` 中注明。
5. **博士后**不是学位 → 归 `doctorate`（最高学历）。
6. **结业/研修/高管课程/执业资格**（非学位）→ `professional`。
7. **candidate / candidate_of_sciences**（苏联体系副博士候选人）→ `doctorate`。
8. **specialist**（苏联体系五年制专家学位）→ `professional`。
9. **residency**（医学住院医师阶段）→ `professional`。
10. **literal `"null"` 字符串**：视为脏数据 → 字段置 `null`。

## 三、归一执行记录（2026-11-17）

- 全库扫描发现 **609 种脏值、1,226 行** 不符合标准枚举
- 全部归一完成：`professional` 391、`doctorate` 189、`bachelor` 240、`master` 208、`high_school` 124、`primary` 21、`associate` 2、`other` 50、literal-null 清理 1
- 每条修改的原始值已写入该条目的 `note` 字段（格式：`原 degree 值「xxx」已归一为 yyy`），可追溯
- 复扫确认：**非标准值剩余 0**

### 典型映射示例

| 脏值 | 归一 |
|---|---|
| 硕士 / 学士 / 博士 / 文凭 / 证书 / 高管课程 | master / bachelor / doctorate / professional |
| phd / doctor / Doctorate | doctorate |
| MBA / MPA / LLM / MPhil / postgraduate / 研究生 | master |
| LL.B. (Hons) / BBA / MBBS / 工学学士 / 法学学士（LLB） | bachelor |
| secondary / 中学 / 初中 / A-Level / SPM / form_six / foundation | high_school |
| certificate / diploma / training / 律师资格 / 大律师资格（Barrister-At-Law） | professional |
| specialist / specialty / residency / executive_program | professional |
| candidate / candidate_of_sciences | doctorate |
| honorary / 荣誉博士学位 | doctorate |
| `"null"`（字符串） | null |

## 四、JSON Schema 片段（可直接集成）

```json
{
  "degree": {
    "type": ["string", "null"],
    "enum": [
      "primary",
      "high_school",
      "associate",
      "bachelor",
      "master",
      "doctorate",
      "professional",
      "other"
    ],
    "description": "学历等级；未知/未公开为 null；null 与 other 语义不同"
  }
}
```

## 五、机器可读对照表

```json
{
  "primary":      "小学",
  "high_school":  "高中/中学",
  "associate":    "大专/副学士",
  "bachelor":     "学士",
  "master":       "硕士",
  "doctorate":    "博士",
  "professional": "职业资格/专业教育",
  "other":        "其他",
  "null":         "未知/未公开"
}
```

## 六、产物

- 归一脚本：`scripts_tmp/degree_normalize.py`（规则可复用于下游清洗）
- 变更明细：`output/_id_audit/degree_normalize_apply.json`（1,225 条逐条记录）
- 撤销依据：每条修改的原始值同时写入画像 `education[].note`，可直接反查

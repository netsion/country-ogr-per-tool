# 20 个无画像注册项：合并 / 补建清单

- 来源：491 条跨国公共机构复核中 38 条回退所涉及的 20 个 `auto_registered` 注册 ID
- 归并为 **14 个实体组**，共 **38 条引用**
- 本清单只做规划，未创建画像、未改注册表、未改引用
- 机器可读：`output/_id_audit/registry_consolidation_plan.csv`

## P1（4 组，25 条引用）

| 实体 | 注册 ID | 引用 | 建议 | 目标 ID / 画像 |
|---|---|---:|---|---|
| 联合国儿童基金会 UNICEF | SA-INTL-015 / CI-INTL-022 / CD-INTL-034 / LY-INTL-004 | 13 | 4 个注册项合并，建全球画像 | **US-INTL-023**；QID Q740308；KG-INTL-001 是吉尔吉斯办事处，不作为全球主体 |
| 马达德集团 Al Mada | MA-CORP-089 / MA-CORP-091 / MA-CORP-092 | 6 | 3 个注册项合并，建控股集团画像 | **MA-CORP-089**；091/092 标 merged |
| 瓦法银行 Wafabank | MA-FIN-022 | 4 | 建历史银行画像 | **MA-FIN-022**；QID Q12199351；现有 MA-FIN-002 是 successor Attijariwafa，不能替代 |
| 领航投资 Vanguard | US-FIN-021 / US-FIN-047 | 2 | 2 个注册项合并，建画像 | **US-FIN-021**；QID Q849363 |

> UNICEF 13 条分布：SA 8、CI 3、CD 1、LY 1。多数描述指向全球总部/伙伴关系；全球画像可覆盖，国别办事处在描述中保留。

## P2（4 组，7 条引用）

| 实体 | 注册 ID | 引用 | 建议 | 目标 ID / 画像 |
|---|---|---:|---|---|
| 阿曼阿赫利银行 Ahli Bank | OM-FIN-018 | 3 | 建商业银行画像 | **OM-FIN-018**；不要与 LY-FIN-014（利比亚 Aman Bank）、KW-FIN-006（科威特 ABK）混同 |
| 阿拉伯银行 Arab Bank plc | OM-FIN-020 | 2 | 建约旦跨国银行画像 | **OM-FIN-020**；QID Q2629881；country_iso3=JOR；OM-FIN-005 是阿曼阿拉伯银行 OAB，不同实体 |
| 思科 Cisco | CI-CORP-055 | 1 | 合并到现有美国主画像 | **US-CORP-026**；CI-CORP-055 标 merged |
| 《新闻报》Al Akhbar（摩洛哥） | MA-MEDIA-029 | 1 | 建摩洛哥报纸画像 | **MA-MEDIA-029**；LB-MEDIA-016 是黎巴嫩 Al Akhbar，不同实体 |

## P3（6 组，6 条引用）

| 实体 | 注册 ID | 引用 | 建议 | 目标 ID / 画像 |
|---|---|---:|---|---|
| 《消息报》Al Anbaa（黎巴嫩） | LB-MEDIA-041 | 1 | 建黎巴嫩党报画像 | **LB-MEDIA-041**；不可指向 KW-MEDIA-007（科威特 Al Anba）或 LB-MEDIA-016 |
| 阿曼公共广播电视总局 PART | OM-GOV-041 | 1 | 建政府媒体机构画像 | **OM-GOV-041** |
| 星电信/Unitel（老挝） | LA-CORP-007 | 1 | 建电信合资公司画像 | **LA-CORP-007** |
| 自由欧洲电台/自由电台 RFE/RL | TJ-MEDIA-011 | 1 | 建全球总部画像 | **US-MEDIA-039**；KG-MEDIA-006/UZ-MEDIA-010 是语言部，不是母体 |
| GK USA | PH-NGO-049 | 1 | 先挂母体或暂缓 | **PH-NGO-002**（Gawad Kalinga 母体）；2017 年后已分离，建议先在描述注明，必要时再建美国分会画像 |
| Tango（无人加油站品牌） | KW-CORP-019 | 1 | 保留注册引用，暂不建画像 | **KW-CORP-019**；1 条引用，现多冠名 Q8 Easy |

## 建议执行顺序

1. **P1 合并/建画像（4 组）**：UNICEF、Al Mada、Wafabank、Vanguard。  
   - 合并注册项：UNICEF 4→1、Al Mada 3→1、Vanguard 2→1；Wafabank 单独建历史画像。
2. **P2（4 组）**：Ahli、Arab Bank、Al Akhbar 建画像；Cisco 直接并到 US-CORP-026。
3. **P3（6 组）**：按价值排序，先 Al Anbaa、PART、Unitel、RFE/RL；GK USA 先挂母体；Tango 暂不建。

每组建画像时同步：

- registry 状态 `auto_registered → profiled`（合并项标 `merged` + `merged_into`）；
- `orgs/_index.json` 增加条目；
- `_name_index.json` 增加主名/别名键；
- 引用从旧注册 ID 改到 canonical ID；
- 建 undo 日志；
- 有头像的才写 `profile`，无头像保持 `profile: null`。

---

## 执行记录（2026-11-13）：P1 已完成

| 实体 | 结果 |
|---|---|
| UNICEF | 新建 `US-INTL-023`（Q740308）；4 个注册项 `merged_into=US-INTL-023`；16 条引用改指新画像 |
| Al Mada | 新建 `MA-CORP-089`；091/092 `merged_into=MA-CORP-089`；6 条引用指向 089 |
| Wafabank | 新建 `MA-FIN-022`（Q12199351，历史主体，successor=MA-FIN-002）；5 条引用 |
| Vanguard | 新建 `US-FIN-021`（Q849363）；US-FIN-047 `merged`；2 条引用指向 021 |

- 实际改动 19 个引用位置（另有 10 条已指向 canonical，不需要改）
- 4 个新画像 `--strict` 校验：0 error / 0 warning
- org index：US 163→165，MA 129→131
- registry：4 个 canonical `profiled`，6 个旧项 `merged`
- 头像未动：9,001 person + 3,965 org，0 变更
- 回滚：`output/_id_audit/p1_consolidation_undo.json`

P2、P3 尚未执行。

---

## 执行记录（2026-11-13）：P2 已完成

| 实体 | 结果 |
|---|---|
| 阿曼 Ahli Bank SAOG | 新建 `OM-FIN-018`；3 条引用已指向该画像 |
| Arab Bank plc | 新建 `OM-FIN-020`（Q2629881，country=JOR）；2 条引用已指向该画像 |
| Al Akhbar（摩洛哥） | 新建 `MA-MEDIA-029`；1 条引用已指向该画像 |
| Cisco | `CI-CORP-055` 标 `merged_into=US-CORP-026`；1 条引用改指美国主画像 |

- 3 个新画像 `--strict` 校验：0 error / 0 warning
- org index：OM 60→62，MA 131→132
- 旧 Cisco 引用残留：0
- 头像未动：9,001 person + 3,965 org，0 变更
- 回滚：`output/_id_audit/p2_consolidation_undo.json`

P3（Al Anbaa、Oman PART、Unitel、RFE/RL、GK USA、Tango）尚未执行。

---

## 执行记录（2026-11-13）：P3 已完成

| 实体 | 结果 |
|---|---|
| 《消息报》Al Anbaa（黎巴嫩） | 新建 `LB-MEDIA-041`（Q108907305）；1 条引用指向该画像 |
| 阿曼公共广播电视总局 PART | 新建 `OM-GOV-041`；4 条引用指向该画像（历史机构，2020 撤销） |
| 星电信/Unitel（老挝） | 新建 `LA-CORP-007`；1 条引用指向该画像 |
| RFE/RL | 新建 `US-MEDIA-039`（Q485500，全球母体）；2 条引用改指；`TJ-MEDIA-011` 标 `merged_into=US-MEDIA-039` |

- 4 个新画像 `--strict` 校验：0 error / 0 warning
- org index：LB 62→63，OM 62→63，LA 100→101，US 165→166
- 头像未动：9,001 person + 3,965 org，0 变更
- 回滚：`output/_id_audit/p3_consolidation_undo.json`

**未处理（保留注册引用，未建画像）**：
- GK USA `PH-NGO-049`：美国伙伴组织，2017 年后与 Gawad Kalinga 分离；未合并到母体，仍指向 `PH-NGO-049`。
- Tango `KW-CORP-019`：低价值品牌，1 条引用，保留注册引用。

# 全库 ID 引用错乱审计报告

- 日期：2026-11-13
- 范围：53 个国家/地区最新日期目录，**17,596 个人物画像、6,013 个组织画像、258,511 条 ID 引用**
- 触发案例：Musk 档案点击 SpaceX 跳到 Cisco；关系人 Donald Trump 显示无档案

---

## 一、结论

这不是个别档案写错，而是**系统性的 ID 体系故障**，有四层原因叠加：

1. **ID 重复分配**：同一 `org_id` / `person_id` 在 registry 中挂多个不同实体。  
   - 组织：**1,209 个 ID** 有冲突，涉及 **1,882 个"影子组织"**；其中 **677 个 ID 已有正式画像**（这些画像就是"点错跳转"的落点）。
   - 人物：**448 个 ID** 有冲突，涉及 **591 个"影子人物"**；其中 **366 个 ID 已有正式画像**。
2. **名称索引被短键污染**：`_name_index.json` 有 **25,926 个 ≤3 字符的键**，`decompose_name()` 把 `Cámara` 切成 `C` + `mara de Diputados`，解析器取第一个命中 → `C` 命中 `MX-FIN-010`。这正是"众议院"跳到"陆军银行"的路径。
3. **冲突条目只修了索引、没修引用**：US 在 2026-10-04 已把 SpaceX/OpenAI 等冲突条目标为 `trimmed`，但已经写进人物档案的 `US-CORP-026` / `US-CORP-014` 没有回修。
4. **采集期缺少 ID 校验**：子代理自造 ID、占位符 ID、person ID 写进 org_id 都能落盘；validator 的交叉检查只看"ID 是否存在"，不看"ID 指向的对象名称是否与引用一致"。

**用户案例复盘**

| 现象 | 实际数据 | 机制 |
|---|---|---|
| Musk 点 SpaceX → Cisco | `work_experience`: `太空探索技术公司 (SpaceX)`，`org_id=US-CORP-026`；`US-CORP-026.json` 是 Cisco；registry 同 ID 还有一条 `SpaceX`（`trimmed`） | ID 碰撞；裁剪影子条目时未回修人物引用 |
| Musk 点 OpenAI → Ford | `OpenAI`，`org_id=US-CORP-014`；该 ID 画像是 Ford；registry 同 ID 有 `OpenAI`（`trimmed`） | 同上 |
| Trump 显示无档案 | `person_relationships[].person_id=null`；`US-PERSON-000485.json` 就是 Donald Trump | 关系人 ID 未回填 |
| xAI / SolarCity 无档案 | registry 有 `US-CORP-069` / `US-CORP-066`（`auto_registered`），但没有画像文件 | 登记了、没画像 |

---

## 二、根因证据

### 2.1 ID 分配器碰撞（最核心）

`id_registry.json` 中同一 ID 挂多个不同名字。典型例子：

| 国家 | ID | 正式画像 | 影子身份 |
|---|---|---|---|
| US | US-CORP-026 | 思科系统 | SpaceX |
| US | US-CORP-014 | 福特汽车 | OpenAI |
| US | US-GOV-001 | 美国国务院 | 阿贡国家实验室 |
| US | US-GOV-002 | 美国财政部 | 费米国家加速器实验室 |
| JP | JP-GOV-001 | 内阁官房 | 国际交流基金 |
| JP | JP-GOV-003 | 总务省 | JAXA |
| SG | SG-GOV-001 | 新加坡国会 | 新加坡金融管理局 |
| SG | SG-PARTY-001 | 人民行动党 | 工人党 |
| NZ | NZ-GOV-001 | 总理及内阁部 | 新西兰创意艺术委员会 |
| VN | VN-GOV-003 | 越南政府 | Indovina Bank |
| MX | MX-GOV-004 | 众议院 | 司法行政机构、Ricardo Monreal（人物名） |
| KR | KR-GOV-010 | 行政安全部 | 雇佣劳动部 |

人物侧同样严重：

| 国家 | person_id | 正式画像 | 影子人物 |
|---|---|---|---|
| SG | SG-PERSON-000010 | Desmond Lee | S. Iswaran（易华仁） |
| SG | SG-PERSON-000011 | Masagos Zulkifli | Tan Chuan-Jin（陈川仁） |
| SG | SG-PERSON-000012 | Chan Chun Sing | Kong Hee（康希） |
| MX | MX-PERSON-000102 | Rosaura Ruiz Gutiérrez | Vanessa Slim Domit |
| RU | RU-PERSON-000001 | Александр Дынкин | 留明 (Рюмин) |

机制：`get_next_org_id()` / `get_next_person_id()` 用 registry 计数器发号；多个子代理并行采集时各自从同一快照开始，或计数器回卷，导致同一号段被重复发放。`_reconcile_counters()` 只在单次运行开始时按磁盘最大号修正，无法防止并发。US registry 的 `US-CORP` 计数器已到 **245**，但实际只有 40 个 CORP 画像——大量"已发号、未画像"的 ID。

### 2.2 名称索引短键污染

- `_name_index.json` 全库 **338,791 个键，其中 25,926 个 ≤3 字符**。
- `decompose_name()` 的正则 `[A-Za-z][A-Za-z\-\s]*[A-Za-z]` 不认带音标的字母，`Cámara` 被切成 `C` + `mara`；`S.C.` 被切成 `S`、`C`。
- 索引生成时 `decompose_name` 的分片也会入索引，于是出现 `"C" → MX-FIN-010`、`"s" → MX-FIN-010`、`"S" → MX-CORP-001` 这类键。
- `resolve_ids.lookup_name()` 精确匹配失败后，**按分片顺序取第一个命中**。实测：
  - `联邦众议院 (Cámara de Diputados)` 的分片 `C` 命中 `MX-FIN-010`（陆军银行）；
  - `米哈雷斯...律师事务所 (Mijares, Angoitia, Cortés y Fuentes, S.C.)` 的 `S` 命中 `MX-CORP-001`。
- MX 的 `id_registry.json` 还有 **311 条人物记录混在组织 registry**（带 `person_id` + `org_id`），生成索引时把人物名映射成其雇主的 `org_id`，直接污染 **248 个键**。

### 2.3 自造 ID / 占位符 / 跨类型 ID

| 类型 | 数量 | 例子 |
|---|---:|---|
| person ID 写进 org_id | 404 条 / 87 种 | `MX-PERSON-000060` 指阿卡普尔科市政府（146 条）；`VN-PERSON-000033` 指农林部 |
| 占位符 person ID | 400 条 / 96 种 | `MY-PERSON-UNKNOWN-001`、`MY-PERSON-REL-001`、`MY-PERSON-000000`、`MY-PERSON-EXT`、`unknown` |
| 自造 org ID | — | `JP-None-001`、`JP-research_institution-001`、`US-federally_funded_research_center-001`、`MY-POL-UMNO`、`MY-GOV-SARAWAK` |

这些 ID 在 UI 上要么无档案，要么落到错误实体。现有 validator 的格式正则能拦住一部分，但历史数据集没有全量跑 `--strict`。

### 2.4 登记了但没画像

registry 状态为 `auto_registered` / `planned` / `target`，但 `orgs/` 下没有对应文件：

| 引用方向 | 有效 ID 但无画像 |
|---|---:|
| work_experience → org | 5,042 |
| person_relationships → person | 5,236 |
| family_members → person | 137 |
| key_people → person | 3,516 |
| related_entities → org | 4,728 |

这类不是"ID 错"，而是"档案未建"，UI 显示无档案是预期行为。是否补建属于内容范围决策（SpaceX、OpenAI、xAI、SolarCity 都在这一类）。

---

## 三、全库引用状态

> 分类基于"引用名称 vs 目标画像名称"的强匹配（繁简转换、尊称剥离、词元包含、中文包含）。  
> `指向无关档案` = 当前 ID 有画像，但画像与引用名称对不上；`无目标` = 全库找不到对应实体。

| 引用方向 | 总数 | 空 ID | 正确指向画像 | 有效 ID 无画像 | 可改到正确画像 | 可改到正确注册 ID | 指向无关档案 | 无目标 | 需复核 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| person.work_experience → org | 129,305 | 57,347 | 48,331 | 5,042 | 1,703 | 851 | 13,627 | 1,463 | 941 |
| person.person_relationships → person | 52,933 | 13,003 | 28,378 | 5,267 | 1,970 | 75 | 2,780 | 1,024 | 436 |
| person.family_members → person | 18,103 | 16,430 | 1,335 | 137 | 32 | 0 | 46 | 109 | 14 |
| org.key_people → person | 25,419 | 2,367 | 17,436 | 3,516 | 552 | 37 | 323 | 1,066 | 122 |
| org.related_entities → org | 32,751 | 6,554 | 16,293 | 4,739 | 957 | 238 | 2,995 | 335 | 640 |
| **合计** | **258,511** | **95,704** | **111,773** | **18,701** | **5,214** | **1,201** | **19,771** | **3,997** | **2,153** |

关键比例（在 162,807 条"非空 ID"引用中）：

- **80.2%** 正确指向画像；
- **11.5%** ID 有效但目标无画像（不是错跳，是"无档案"）；
- **14.6%（23,768 条）** 指向无关/不存在的实体，应置空；
- **3.9%（6,415 条）** 可以机械改到正确实体（其中 6,043 条为完全同名匹配）；
- **1.3%（2,153 条）** 名称歧义，需人工/LLM 复核。

> **重要修正（2026-11-13 复核）**：上表"指向无关档案"19,771 条是按严格名称匹配得到的**上界**。逐条计算引用名与当前画像名的相似度后：
> - **5,766 条相似度 ≥0.75**：多为全称/简称、繁简、多语言变体（如"印度尼西亚人民代表会议" vs "印度尼西亚共和国人民代表会议"），**当前 ID 很可能正确，不应置空**；
> - **7,031 条相似度 0.5–0.75**：疑似变体或上下级关系，需复核；
> - **6,974 条相似度 <0.5**：明确错链候选（Musk→SpaceX/OpenAI 在此列）。
>
> 因此真正"应置空"的上界是 **6,974（低相似错链）+ 3,997（无目标）= 10,971 条**，不是 23,768 条。批量置空前必须先看 200 条抽样。

### 空 ID 的可补全量

| 方向 | 空 ID | 姓名唯一匹配到画像 | 同名歧义 |
|---|---:|---:|---:|
| person_relationships | 13,003 | 2,978（其中 2,818 完全同名） | 143 |
| family_members | 16,430 | 900（其中 414 完全同名） | 376 |
| work_experience → org | 57,350 | 4,974（其中 4,925 完全同名） | 1,337 |

> Trump 属于 `person_relationships` 的 2,978 条之一，建议值 `US-PERSON-000485`；Kimbal Musk 属于 family 的 900 条之一，建议值 `US-PERSON-000791`。

---

## 四、国家热点

### 组织 ID 碰撞数

| 国家 | 碰撞 org_id 数 | 国家 | 碰撞 org_id 数 |
|---|---:|---|---:|
| KR | 549 | MX | 93 |
| NZ | 163 | VN | 50 |
| US | 156 | SG | 44 |
| JP | 116 | PG | 20 |

### 人物 ID 碰撞数

| 国家 | 碰撞 person_id 数 |
|---|---:|
| SG | 130 |
| MX | 94 |
| RU | 84 |
| NZ | 76 |
| PG | 28 |
| UZ | 13 |
| VN | 11 |

### 引用错误率最高的国家（work_experience）

| 国家 | 错误率 | 错误数 | 有效指向 |
|---|---:|---:|---:|
| KG | 33.2% | 421 | 848 |
| MX | 31.2% | 1,392 | 1,916 |
| CL | 30.5% | 879 | 1,822 |
| VN | 28.8% | 469 | 815 |
| MA | 25.5% | 297 | 808 |
| CD | 24.8% | 236 | 680 |
| BF | 23.7% | 94 | 290 |
| CM | 23.2% | 118 | 385 |
| MY | 23.2% | 263 | 872 |
| CI | 21.6% | 182 | 626 |

人物关系侧：MY 71.4% 异常（大量 `MY-PERSON-UNKNOWN-*` 占位符）、MX 67.4%、RU 51.0%、VN 43.3%、PG 31.3%。

---

## 五、次要但需一并处理的问题

1. **wikidata_qid 重复 72 组**：最严重 `Q57643` 同时挂在 Thomas Sankara、约旦国王侯赛因、洪森、韩桑林、Keiko Fujimori、李显龙 6 个互不相关的人身上，明显是模板复制错误。组织侧 12 组重复。
2. **索引文件与档案不同步**：6 个 person index 条目无文件、6 个 ID 不一致、26 个人物未进 index；7 个 org index 条目无文件、103 个组织未进 index。
3. **name_index 含 1,243 个已失效 ID**（trimmed/removed 等状态），仍可被解析器命中。
4. **NG 存在两个日期目录**（2026-07-29 / 2026-11-10），人物 ID 完全不重叠（旧 200 人 + 新数据集），当前按最新目录审计，无 ID 冲突；但下游如果同时读取两个目录会看到两套档案。

---

## 六、修复方案

### 方案 A（推荐）：先修引用，再治索引

**A1 引用回修（不动 registry / index，风险最低）**

| 动作 | 数量 | 说明 |
|---|---:|---|
| 改到正确画像 | 4,964（exact）+ 250（fuzzy 待复核） | `replace_profile`，共 5,214 |
| 改到正确注册 ID | 1,079（exact）+ 122（fuzzy 待复核） | 目标暂无画像，但 ID 正确，共 1,201 |
| 疑似正确、保留 | 5,766 | 与当前画像名相似度 ≥0.75，多为名称变体；建议保留 |
| 置空 | 10,971 | 6,974 低相似错链 + 3,997 无目标；Musk→SpaceX/OpenAI 在此列 |
| 复核 | 7,031 | 相似度 0.5–0.75，疑似变体/上下级关系 |
| 补空 person 引用 | 2,978 + 900（其中 exact 2,818 + 414） | Trump、Kimbal 在此列 |
| 补空 org 引用 | 4,974（exact 4,925） | 空 org_id 但姓名能唯一匹配画像 |
| 保留 | 130,474 | 111,773 正确画像 + 18,701 有效注册无画像 |
| 人工/LLM 复核 | 2,153 + 7,031 + 372 模糊替换 + 695 模糊补齐 | 歧义/变体/模糊匹配 |

**A2 结构治理（防复发）**

1. **registry 去重**：给 1,209 个组织影子身份、448 个人物影子身份重新分配未占用的新 ID；`trimmed` 条目保留审计价值但从索引中彻底移除。
2. **重建 `_name_index.json`**：
   - 只从画像 + 活跃且唯一的 registry 条目生成；
   - 禁止 ≤3 字符键；禁止把人物名映射到 org_id；
   - 排除 `trimmed/merged/removed/duplicate/excluded/pruned`；
   - 同名多 ID 时标记歧义，不静默取第一个。
3. **修 `decompose_name()` / `resolve_ids.py`**：
   - 先 `NFKD` 去音标再切分，`Cámara` 不能再切成 `C`；
   - 不把单字母/缩写入索引；
   - `lookup_name` 取消"按分片取第一个命中"，改为"所有分片命中必须指向同一 ID，否则判歧义"。
4. **validator 加固（`--strict` 默认开启）**：
   - `org_id` 必须存在，且目标 `basic_info` 名称/别名与 `organization` 强匹配；
   - `person_id` 必须存在且姓名匹配；
   - 禁止 person ID 作为 org_id、禁止占位符/自造 ID 格式；
   - registry 同一 ID 多身份 → error；
   - `_name_index.json` 短键/污染键检查。
5. **采集流程**：ID 分配串行化（单进程发号或文件锁）；注册前查重；每批采集结束跑一次 cross-ref + 名称一致性检查。

### 方案 B：重建 ID 命名空间

对所有国家重新编号影子 ID，重建索引后跑 `resolve_ids`。最彻底，但要改所有引用，成本高、回归风险大，不建议现在做。

### 方案 C：只修 Musk 类"点开跳错"

只处理 `profile_wrong + collision_shadow` 置空 + 补空 person 引用，不动 registry/index。能立刻消除错跳，但下一轮采集会复发。

---

## 七、建议

**建议执行 A1 + A2，暂不执行 B。**

- A1 先做，能立即消除用户可见的错跳和"有档案却显示无档案"；
- A2 必须同批做，否则下一轮采集继续产生同类脏数据；
- SpaceX/OpenAI/xAI/SolarCity 这类高频缺失组织，是否补建画像单独决策：补建后相关引用可以从"置空"改为"有效链接"。

**需要用户确认的 4 个点**

1. A1 的 23,768 条"指向无关档案/无目标"是否同意直接置空？（建议先抽样 200 条确认）
2. A1 的 6,043 条完全同名替换是否直接执行？
3. A2 的 registry 去重 + name_index 重建 + validator 加固是否现在做？
4. 是否为高频缺失组织补建画像（可先出 Top 50 清单）？

---

## 八、复现与产物

| 脚本 | 用途 |
|---|---|
| `scripts_tmp/id_integrity_audit2.py` | 全库引用完整性审计（五方向 + 名称强匹配） |
| `scripts_tmp/registry_collision_audit.py` | registry 同一 ID 多身份检测 + 引用分类 |
| `scripts_tmp/id_repair_plan.py` | 生成逐条修复计划（replace / null / fill / review） |

| 产物 | 内容 |
|---|---|
| `output/_id_audit/report_v2.json` | 引用完整性总表、分国统计、ID/index 问题 |
| `output/_id_audit/collision_report.json` | 1,209 org + 448 person 碰撞明细 |
| `output/_id_audit/repair_plan.json` | 逐条修复计划（broken + null_fill） |
| `output/_id_audit/repair_plan_summary.json` | 动作汇总、Top 缺失实体 |

---

## 九、Step 1 执行记录（2026-11-13）

**执行策略**：同国 + 仅主名称（name/name_en/name_zh/name_original）精确匹配；不带别名、不做模糊/跨国政府机构匹配；不改任何画像 ID 和头像字段。

**第一次尝试（已完整回滚）**：曾按"任意同名"补全 13,121 条，复核发现跨国同名误配（沙特交通部→卡塔尔 `QA-GOV-006`、麦肯锡→`AU-GOV-075`），已用 `step1_undo.json` 全部回滚（11,077 条回滚 + 2,044 条本就回滚，0 冲突）。

**最终执行（Step 1b）**：9,676 条 / 5,386 个文件

| 类别 | 补空引用 | 纠正错误 ID |
|---|---:|---:|
| work_experience → org | 3,018 | 1,401 |
| person_relationships → person | 2,414 | 1,522 |
| family_members → person | 295 | 9 |
| key_people → person | 0 | 430 |
| related_entities → org | 0 | 587 |
| **合计** | **5,727** | **3,949** |

- 跨国改动 704 条，全部为 CORP/FIN/SOE/ACAD/MEDIA/NGO/INTL 或人物（外国雇主/外国政要），**0 条跨国 GOV/MIL/PARTY**。
- 所有新 ID 均存在对应画像（missing_target=0）。
- 头像：9,001 person + 3,965 org，文件名与 ID 仍 100% 一致，0 变更。
- 回滚文件：`output/_id_audit/step1b_undo.json`；汇总：`step1b_summary.json`。

**审计前后**

| 方向 | 空 ID | 正确指向 | 指向错误 | 悬空 |
|---|---:|---:|---:|---:|
| work_experience → org | 57,272 → 54,283 | 54,712 → 59,173 | 9,964 → 8,934 | 7,255 → 6,883 |
| person_relationships | 13,003 → 10,589 | 28,578 → 32,521 | 3,702 → 2,853 | 7,650 → 6,977 |
| family_members | 16,430 → 16,138 | 1,369 → 1,673 | 15 → 14 | 289 → 281 |
| key_people | 2,283 → 2,328 | 17,513 → 17,951 | 567 → 304 | 4,969 → 4,802 |
| related_entities | 6,551 → 6,565 | 17,473 → 18,095 | 2,572 → 2,383 | 6,140 → 5,742 |

**Musk 案例**：Trump、Kimbal 已补上 `person_id`；SpaceX/OpenAI 仍指向 Cisco/Ford（属于 Step 2 的低相似错链，待 200 条抽样确认后置空或补画像）。

---

## 十、200 条人工复核执行（2026-11-13）

按复核结论只执行 **104 条置空 + 1 条改链**；63 条暂缓、32 条保留不动。

- 动作行：105 行；实际引用位置：**121 个**（第 97 条美国商务部在同一人物文件有 2 处）
- 修改文件：106 个；跳过：0（全部通过当前 ID/引用名/目标画像校验）
- 分类：work_org 置空 67、related_org 置空 19、person_rel 置空 30、key_people 置空 2、family 置空 1、work_org 改链 2
- 第 97 条：两处 `PE-CORP-007 → US-GOV-007`（美国商务部）
- 第 180 条（暂缓）：保持 `NI-ACAD-004` 不动，待核秘鲁/尼加拉瓜 UNI
- 头像：9,001 person + 3,965 org，文件名与 ID 仍 100% 一致，0 变更
- 回滚文件：`output/_id_audit/step2_reviewed_undo.json`

## 十一、审计字段修正

复核发现审计只读 `person_name`，漏读关系条目的 `name` 字段（第 10、70 条误报即由此产生）。已修正：

| 对象 | 原读取 | 新增回退字段 |
|---|---|---|
| person_relationships | person_name | name |
| family_members | name | person_name |
| work_experience | organization | org_name, organization_en |
| key_people | name | name_en |
| related_entities | org_name | name |
| person 画像名称 | name/name_en/name_zh | name_native, name_original, name_local, name_th, name_ms, name_ja, name_kr, name_km |
| org 画像名称 | name_zh/name_en/name_original | name, name_local, name_ru, name_ky, short_name, former_names |

修正后最新基线（含 Step 1b + 121 条复核修改）：

| 方向 | 总数 | 空 ID | 正确指向 | 指向错误 | 悬空 |
|---|---:|---:|---:|---:|---:|
| work_experience → org | 129,280 | 54,354 | 59,177 | 8,875 | 6,874 |
| person_relationships | 52,950 | 10,622 | 32,550 | 2,805 | 6,973 |
| family_members | 18,113 | 16,146 | 1,673 | 14 | 280 |
| key_people | 25,439 | 2,380 | 17,951 | 302 | 4,806 |
| related_entities | 32,841 | 6,605 | 18,130 | 2,365 | 5,741 |

## 十二、Step 1b 跨国同名风险

Step 1b 共 804 条跨国改动。抽样发现通用机构名跨国同名误配：

- PE「国立工程大学」→ `NI-ACAD-004`（尼加拉瓜 UNI，第 180 条）
- CL「国家报 (El País / La Nación)」→ `BF-MEDIA-005`（布基纳法索《国家报》）
- BO「今日报」→ `NG-MEDIA-007`（尼日利亚《今日报》）
- KW「Tango」→ `TZ-NGO-003`
- CD「UNICEF」→ `KG-INTL-001`（吉尔吉斯斯坦办事处）

结论：**跨国链接不能靠“全球唯一同名”自动认定**；同名大学、媒体、国家银行、国际组织办事处风险最高。已生成完整清单：
`output/_id_audit/step1b_cross_country_review.csv`（804 条，含原/新指向）。

处理建议（待决）：
1. 先复核高风险清单（可按 MEDIA/ACAD/SOE/NGO/INTL 筛选）；
2. 只保留明确品牌（Boeing、Visa、JPMorgan、MIT、McGill 等）和人物全名跨国链接；
3. 通用公共机构名一律置空或回退，不再自动跨国匹配。

## 十三、Step1b 跨国公共机构复核清单

按“先复核 491 条公共机构类跨国改动”生成两份只读清单：

- 全量：`output/_id_audit/step1b_cross_public_review.csv`（491 条）
- 优先样本：`output/_id_audit/step1b_cross_public_priority.csv`（100 条，含全部 54 条机器优先项）

字段：优先级、风险、机器建议、类别、引用国家、引用方、引用名称、原ID/原指向、新ID/新指向、原始引用位置、目标国别提示、复核结论（留空）、备注（留空）。

机器优先项（54 条）的判定：
- 目标名称含其本国国名，而引用名称未提（如 PE「国立工程大学」→ NI-ACAD-004）；
- 国际组织国别办事处（如 UNICEF → KG-INTL-001 吉尔吉斯斯坦办事处）；
- 通用媒体名（国家报/今日报/日报/电视台等）。

复核结论建议用四种值：`保留`（保留 Step1b 新 ID）、`置空`（解除 ID）、`回退`（恢复原 ID，仅当原 ID 确为正确画像）、`暂缓`。机器建议不作为执行授权。

## 十四、491 条跨国公共机构复核：执行前验证

对 `step1b_cross_public_review_reviewed.csv` 做了独立回读（只读）：

- 491/491 当前 ID 与清单“新ID”一致，引用名称与数组位置一致；
- 动作行 58 个位置：**19 置空 + 39 回退**；无过期、无重复位置冲突；
- 优先 100 条与全量 491 条结论一致，无冲突；
- 39 条回退中：**1 条回原有画像**（第 32 条 LB-MEDIA-015），**38 条回无画像的 `auto_registered` 注册项**；
- 38 条回退只涉及 **20 个唯一注册 ID**，主要是 UNICEF 13 条、Al Mada 6 条、Wafabank 4 条、Ahli Bank 3 条、Arab Bank 2 条、Vanguard 2 条等；
- 85 条暂缓中 **58 条是 World Bank / World Bank Group 粒度**，其余 27 条为集团/子公司、历史前身、复合任职、注册类型错误等。

**尚未执行任何 ID 修改。**

## 十五、491 条复核执行记录（A/B/C 组）

**A 组（19 置空 + 1 有画像回退）已执行**
**B 组（38 条回无画像注册项）已执行**，并生成补画像清单。
**C 组（58 条 World Bank/Group）已按“补建世行画像”执行。**

| 组 | 动作 | 位置 | 文件 |
|---|---|---:|---:|
| A | 19 置空 + 1 回退到 LB-MEDIA-015 | 20 | — |
| B | 38 回退到 20 个 auto_registered 注册 ID | 38 | — |
| C | 58 条 World Bank → 新建 US-INTL-011 (IBRD) | 58 | 55 |
| 合计 |  | **116** | — |

### B 组补画像清单

`output/_id_audit/missing_profile_backlog.csv`：20 个唯一注册 ID / 38 条引用。

重点：UNICEF 13 条（SA-INTL-015 / CI-INTL-022 / CD-INTL-034 / LY-INTL-004 四个注册项需先合并）、Al Mada 6 条（MA-CORP-089/091/092 三个注册项）、Wafabank 4 条、Ahli Bank 3 条、Arab Bank 2 条、Vanguard 2 条。回退后这些页面仍显示“无档案”。

### C 组：IBRD 画像

- 新建 `output/us/2026-09-05/orgs/US-INTL-011.json`
  - 名称：国际复兴开发银行 / International Bank for Reconstruction and Development
  - QID：Q7164；总部 USA；成立 1944-07-22；官网 worldbank.org IBRD 页面
  - key_people：彭安杰（US-PERSON-000321）；related_entities：member_of 世界银行集团（US-INTL-003）
- registry：US-INTL-011 由 `auto_registered` 改为 `profiled`
- org index：163 条；name_index 增加“世界银行 / World Bank / 国际复兴开发银行”等键
- 58 条普通 World Bank 引用改指 US-INTL-011；12 条明确写 World Bank Group 的保留 US-INTL-003；4 条复合任职仍暂缓
- 校验：`validate_schema.py --strict` 0 error / 0 warning
- 头像：未创建，`profile: null`

### 剩余暂缓

移除已处理的 58 条 World Bank 后，仍有 **27 条暂缓**：复合任职 4、国别办事处/注册格式 3、新链错误/注册类型 3、历史前身 2、同国不同银行 2、品牌与实际持股 2，其余 11 条为母子公司/集团层级等。

### 头像与回滚

- 头像仍为 9,001 person + 3,965 org，文件名与 ID 100% 一致，本轮 0 变更；
- A/B 回滚：`output/_id_audit/cross_public_undo.json`
- C 回滚：`output/_id_audit/worldbank_relink_undo.json`

## 十六、20 个无画像注册项合并/补建清单

已生成：`docs/registry-consolidation-plan.md`、`output/_id_audit/registry_consolidation_plan.csv`。

- 20 个注册 ID 归并为 14 个实体组、38 条引用；
- P1（25 条）：UNICEF 4→1（US-INTL-023）、Al Mada 3→1（MA-CORP-089）、Wafabank（MA-FIN-022）、Vanguard 2→1（US-FIN-021）；
- P2（7 条）：Ahli Bank（OM-FIN-018）、Arab Bank plc（OM-FIN-020）、Cisco→US-CORP-026、Al Akhbar（MA-MEDIA-029）；
- P3（6 条）：Al Anbaa（LB-MEDIA-041）、Oman PART（OM-GOV-041）、Unitel（LA-CORP-007）、RFE/RL（US-MEDIA-039）、GK USA（先挂 PH-NGO-002）、Tango（保留注册引用）。

尚未创建画像/合并注册项/改引用。

## 十七、A2 结构治理进度

已完成（代码层 + 索引层）：

- `decompose_name` 去音标后再切分，修复 `Cámara → C + mara`；
- `generate_name_index` 过滤 dead status、人物混入、短片段、歧义键、单字符键；
- `resolve_ids` 分解匹配必须唯一，不再取第一个命中；
- validator 增加名称一致性、跨类型 ID、占位符、registry 重复身份、name_index 抽查；
- 54 个数据集 `_name_index.json` 已重建：333,912→314,031 键，≤3 字符键 24,719→9,593，单字符键清零；备份在 `output/_id_audit/name_index_before/`。

待执行（registry 去重数据）：

- 1,209 个 org ID + 448 个 person ID 碰撞；
- 2,487 条影子条目：合并同国画像 492、分配新 ID 1,762、删除 dead 153、复核 80；
- 详见 `docs/a2-structural-governance.md` 与 `output/_id_audit/registry_dedupe_plan.csv`；
- **尚未修改 registry 去重数据。**

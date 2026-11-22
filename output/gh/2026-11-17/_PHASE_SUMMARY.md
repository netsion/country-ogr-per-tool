# 加纳数据集 P5 收尾报告

**数据集**：`output/gh/2026-11-17`（ISO: GH / QID: Q1174）
**收尾日期**：2026-11-22
**流水线**：P1 广度扫描 → P2 缓存/骨架 → P3 组织增强 → P4 人物增强 → P5 校验收尾

---

## 1. 总览

| 指标 | 数值 |
|---|---|
| 组织画像 | **96 个**，平均完整度 **94.4**，中位 96，区间 81–100 |
| 人物画像 | **204 人**，平均完整度 **82.6**，中位 **85**，区间 48–100 |
| 完整度 ≥85 的人物 | **113 人（55.4%）** |
| 人物引文来源总数 | **2,732 条**（人均 13.4 个独立 URL） |
| Schema 校验（--strict） | **0 errors** / 962 warnings |
| 交叉引用（--cross-ref） | **0 errors** / 2,263 warnings |
| 索引文件 | `orgs/_index.json`（96）、`persons/_index.json`（204）、`_name_index.json`（5,492 条） |

**裁剪记录**：P3 组织 392 → 96（OSINT 双轮裁剪）；P4 人物 457 → 205，其中 `GH-PERSON-000162` 与 `000157` 为同一自然人重复登记，重复档案已隔离至 `persons_quarantined_duplicates/`，**有效目标 204 人全部完成**。

---

## 2. 组织画像（96 个）

| 类别 | 数量 | 类别 | 数量 |
|---|---|---|---|
| GOV 政府 | 32 | MIL 军警 | 7 |
| ACAD 学术 | 14 | FIN 金融 | 6 |
| SOE 国企 | 12 | NGO | 3 |
| CORP 企业 | 11 | PARTY 政党 | 3 |
| MEDIA 媒体 | 7 | INTL 国际组织 | 1 |

覆盖：key_people 100%、recent_events 100%（全部带 source）、related_entities 100%、官网 99%。
完整度最低 5 个：GH-CORP-046（81）、GH-PARTY-059（81）、GH-ACAD-008（84）、GH-INTL-001（84）、GH-PARTY-002（84）——均因新设机构/政党缺乏长期档案。

## 3. 人物画像（204 人）

**按重要等级**（采集时 importance_level 分布）：

| 等级 | 人数 | 平均完整度 |
|---|---|---|
| high | 102 | 83.3 |
| medium | 57 | 81.0 |
| low | 45 | 83.0 |

**字段覆盖率**：

| 字段 | 覆盖 | 字段 | 覆盖 |
|---|---|---|---|
| major_achievements ≥3 | 100% | work_experience ≥3 | 95% |
| person_relationships ≥1 | 100% | education ≥1 | 93% |
| biography ≥200字 | 100% | profile 头像直链 | 90% |
| quotes ≥3 | 100% | social_accounts ≥1 | 70% |
| political_stances ≥1 | 97% | wikidata_qid | 54% |
| contacts ≥1 | 39% | family_members ≥1 | 33% |
| birth_date | 49% | | |

覆盖率的「结构性缺口」符合加纳公开数据实况：军人、公务员、法官、企业高管普遍不公开出生日期与家庭成员，社媒以机构账号为主。所有低覆盖字段均按「禁止编造」铁律留空，并在各档案 `collection_meta.notes` 逐项说明。

**完整度最低 5 人**：000148 Awal Mohammed（48）、000158 Mallam Issah Ishak（49）、000259 Eric Osei（54）、000229 John Ayiku Ocansey（54）、000330 Ahmed Hussein-Suale（54）——共同特征是无 Wikidata 条目、无公开学历与出生信息；000330 为生前卧底记者，生物信息本身不可得。

**完整度最高**：000387 Bawumia（99）、000453 Kyerematen（99）、000454 Kwame Owusu Danso（98）、000061 Afenyo-Markin（95）、000390 Kwetie（95）、000395 Asantehene（94）、000193 Mustapha Ussif（94）、000194 Oware-Mensah（93）。

---

## 4. 校验与审计结论

### 4.1 Schema（--strict）：0 errors
收尾过程修复的三类系统性问题：
1. 组织 `key_people[]` 内的非白名单字段 `source/sources`（41 处）→ 内容并入 `collection_meta.notes`（7 个文件）；
2. 人物 `work_experience[]` 内的 `org_id_note/is_current_note/country` 等非法字段（40+9+9 处）→ 同上（12 个文件）；
3. `education[]` 内的 `org_id`（1 处）→ 移除并留痕。

### 4.2 交叉引用（--cross-ref）：0 errors
- 组合模式（--strict --cross-ref）下另有 1,968 条「错误」，经**专项宽松匹配审计**确认**零真实错绑**：
  - 1,710 条为 ID 目标名写法差异（「中文(英文)」格式 vs 档案原文名、人名词序如 Naana Jane / Jane Naana、机构改名如 National Service Secretariat → Authority）；
  - 240 条为组织 `key_people` 引用 registry 已扫描但 P4 裁剪掉的人物（无档案，属裁剪预期）；
  - 18 条为 registry 中 status=listed 但未采集的人物（同上）。
- 审计脚本：`scripts_tmp/gh_p5_xref_audit.py`（宽松匹配 + 排除通用词双口径），两次均 0 条可疑。

### 4.3 五项审计专项结论

| # | 事项 | 结论 |
|---|---|---|
| ① | `GH-PERSON-000032` 身份 | **= Paul Baffoe-Bonnie（现任首席大法官）**，与 000104（配偶）、000063/000067/000068（上级/同僚引用）完全一致；旧进度注释「=代理首席大法官 Pwamang」为误记，已作废 |
| ② | KUMI-LARBI 000094/000095 碰撞风险 | **无碰撞**：000094=国防参谋长 William Agyapong（中将），000095=陆军参谋长 Lawrence Gbetanu（少将），职务与军衔独立可证 |
| ③ | TANDOH 重复登记 | **已裁决**：000162 = 000157 同一自然人（GSSTI 所长 Joseph Bremang Tandoh），保留 000157（79 分，内容更全），000162 档案已隔离 |
| ④ | `GH-GOV-046`（NDPC）档案 | **已修正**：前总干事 Mensah-Abrampa 实于 **2024-07-01 在任内去世**（GBC/Graphic 讣告双源），原「2025 年换届后卸任」表述已更正，注明继任者 Amoah 于 2025-02 获任 |
| ⑤ | 索引双 ID（Torkornoo 000062/000064、Pwamang 000063/000065） | `id_registry.json` 层遗留的重复登记；各人物档案已统一采用已建档 ID（000064/000063），引用无歧义；未改动 registry（按规范） |

### 4.4 采集期间的重大数据修正（抽样）
- **Afenyo-Markin**：所谓「副议长」实为 **ECOWAS 议会第三副议长**（区域议会），非加纳议会副议长；党内职务时间线修正为 副多数党领袖2021→多数党领袖2024-02→少数党领袖2025-01。
- **Jean Mensa**：其曾任 **IEA（经济事务研究所）** 执行主任，非 IDEG。
- **Justin Kodua**：其任 CEO 的机构为 **青年就业局（YEA）**，非 National Youth Authority。
- **Wengam**：其职务为 **移民局理事会主席**（非副局长），兼神召会总监督。
- **Wamkele Mene**：AfCFTA 秘书长宣誓日实为 **2020-03-19**（档案原记 2026-04-18 有误）。
- **Mustapha Yusif**：与青年体育部长 **Mustapha Ussif** 为同一人，拼写变体已并入 aliases。
- **Lotsu**：已于 **2026-10-09 退役**；**Mensah-Abrampa** 已于 2024 去世 —— 两者 `current_positions` 均已按实留空。
- **Agyapong**：Wikidata 无来源的 1939 年出生年份与 1988 年入伍矛盾，未采信。

---

## 5. 数据质量自律情况

- 每个关键事实 ≥2 独立来源；无法核实一律留空/null，不编造。
- 采集期间识别并剔除的污染源（抽样）：GhanaWeb 将同日就任的 Honyenyuga 履历误并入 Amadu 稿；多家社媒将非洲人权法院法官职务误置于 Adjei-Frimpong；RocketReach 同名误配（Frimpong）；FB 粉丝页虚假配偶（Amaleboba）；AI 生成报道与官方通稿矛盾（Fianko/TechLabari）；冒充移民局招募的 Facebook 假页（Andoh）。
- 内容安全过滤（1301）在政党线触发 2 次，均以「仅记客观事实、不引攻讦原文」的中性重派成功。

## 6. 建议下一步

1. **补采被裁人物（可选）**：registry 中仍有 258 名 status=listed 未采集人物，若后续情报需求变化可按需补采。
2. **头像上传**：约 184 个 `profile.source_url` 已就绪，`minio_path` 留待上传管线回填。
3. **双 ID 清理（需授权）**：Torkornoo / Pwamang 的 registry 重复登记建议在下次 registry 维护窗口合并（本次未改动）。
4. **重点人物深访**：Bawumia、Kyerematen、Asantehene、Bagbin 等 90+ 分人物可直接进入关系图谱构建。

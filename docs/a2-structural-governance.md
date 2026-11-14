# A2 结构治理：已完成项与 registry 去重计划

日期：2026-11-13

## 一、已完成的代码修复

### 1. `decompose_name()` 去音标后再切分

文件：`.agents/skills/country-org-collector/scripts/atomic_write.py`

- 先 `NFKD` 去除组合音标，再执行中/韩/英正则。
- `Cámara` 不再被切成 `C` + `mara`；`Cámara de Diputados` 正常输出。
- 这是 `MX-FIN-010` 误绑定的直接根因。

### 2. `generate_name_index.py` 防污染

文件：`.agents/skills/country-org-collector/scripts/generate_name_index.py`

- 排除 `trimmed/merged/removed/duplicate/excluded/pruned/archived/deprecated_broken_id`。
- 跳过混入组织 registry 的人物行（`person_id` 存在）。
- 分解片段过滤：CJK/韩文 <3 字符、拉丁 <4 字符、纯标点/数字不入索引。
- 同一片段命中多个 ID 时标记歧义并删除，不再“先到先得”。
- 删除单字符键（`T`、`Ъ`、`汗` 等）。

### 3. `resolve_ids.py` 不再取第一个命中

文件：`.agents/skills/country-org-collector/scripts/resolve_ids.py`

- 精确匹配优先。
- 分解匹配必须**唯一**；多个不同 ID → 返回 `ambiguous`，不写 ID。
- 过滤短片段。

### 4. `validate_schema.py` 增加 ID 完整性检查

文件：`.agents/skills/country-org-collector/scripts/validate_schema.py`

新增（`--cross-ref`）：

- `work_experience.organization` ↔ `org_id` 目标名称一致性；
- `person_relationships` ↔ `person_id` 名称一致性；
- `key_people` / `related_entities` 名称一致性；
- person ID 写进 org_id、org ID 写进 person_id → error；
- 占位符/自造 ID（`UNKNOWN`、`REL-`、`EXT-`、`000000`）→ error；
- registry 同一 ID 多身份 → warning/strict error；
- `_name_index.json` 单字符键、失效目标 ID → warning/strict error；
- 跨国引用不再误报为“注册表缺失”，降为 warning。

## 二、全库 `_name_index.json` 重建

已用修复后的生成器重建 **54 个数据集**：

| 指标 | 重建前 | 重建后 |
|---|---:|---:|
| 总键数 | 333,912 | 314,031 |
| ≤3 字符键 | 24,719 | 9,593 |
| 单字符键 | 若干（T/Ъ/汗 等） | 0 |

- 备份：`output/_id_audit/name_index_before/`
- 汇总：`output/_id_audit/name_index_rebuild_summary.json`
- MX 示例：15,711→11,125；`C`/`s`/`N`/`mara de Diputados` 消失；`Cámara de Diputados` 正确指向 `MX-GOV-004`；律师事务所不再误指 `MX-CORP-001`。
- US 示例：`IBM`、`Cisco`、`UNICEF`、`World Bank` 等精确键保留。

## 三、registry 去重计划

报告：`output/_id_audit/registry_dedupe_plan.csv`
汇总：`output/_id_audit/registry_dedupe_summary.json`

- 碰撞 ID：**1,209 个 org ID + 448 个 person ID**
- 影子条目：**2,487 条**（org 1,884 / person 603）
- 建议动作：

| 动作 | org | person | 合计 |
|---|---:|---:|---:|
| 合并到同国已有画像 | 197 | 295 | 492 |
| 分配新 ID（无画像） | 1,467 | 295 | 1,762 |
| 删除（dead status） | 153 | 0 | 153 |
| 同名歧义待复核 | 21 | 6 | 27 |
| 跨国同名待复核 | 46 | 7 | 53 |

- 新 ID 需求：**1,762 个**
- 热点：KR 953 个新 ID、MX 302、NZ 255、JP 198、US 146、SG 124、RU 150（person）。

### 风险

1. **新 ID 的类别/国别可能不准**：例如 JP-ACAD-010 下的“清华大学”会被分配 `JP-ACAD-035`，实体其实在中国。批量分配前应按实体国别/类型分桶，或仅对明确同国实体自动分配。
2. **跨国同名 53 条**：已标 `review_cross_country`，不自动合并。
3. **去重只改 registry，不改引用**：影子 ID 重新编号后，引用还需要按名称重映射；否则旧引用仍指向原共享 ID。
4. **引用重映射规模**：collision shadow 引用约千余条，需单独批量处理。

## 四、建议执行顺序

1. **安全层**：删除 153 条 dead status（无引用风险）。
2. **同国合并 492 条**：逐条按名称合并到已有画像，改 registry 状态为 merged。
3. **新 ID 分配 1,762 条**：先按 `org_type`/国别分桶，人工抽查热点国家（KR/MX/NZ/JP），再批量写入 registry。
4. **跨国/歧义 80 条**：人工复核。
5. **引用重映射**：按名称把 collision shadow 引用改到新 ID（有画像）或置空（无画像）。
6. **重建索引 + validator 全库回归**。

**尚未修改任何 registry 去重数据。**

---

## 五、安全层执行（2026-11-13）

按批准范围只做 **drop 153 + merge_to_existing 492**，不分配新 ID、不处理 80 条复核项。

| 动作 | 结果 |
|---|---|
| dead 条目归档 | 153 条移入 `deprecated_registry` / `deprecated_person_registry`，保留原始字段与 `dropped_reason` |
| 同国合并 | 492 条标 `status=merged` + `merged_into=<target>` |
| 合并条目归档 | 573 条（含之前 P1/P2/P3 的合并项）移入 deprecated，活动 registry 不再出现重复 ID |
| 引用同步 | 26 个引用位置按“名称指向影子身份”改到合并目标；14 个文件 |

引用改动样例：KR 三星工程 `KR-CORP-028→025`、NZ 财政部 `NZ-GOV-002→056`、VN 公安部 `VN-GOV-005→006`、MX Laura Itzel `MX-PERSON-000007→019`、PG key_people 4 条。

### 结果

- 活动 registry 碰撞：**1,209 org / 448 person → 863 org / 2 person**
- 头像：9,001 person + 3,965 org，0 变更
- 回滚：`output/_id_audit/registry_safe_undo.json`
- 索引已再次重建：314,448 键，≤3 字符键 9,584，单字符 0

## 六、剩余新 ID 计划（v2，尚未执行）

`output/_id_audit/registry_dedupe_plan_v2.csv`
`output/_id_audit/registry_dedupe_v2_summary.json`

- 剩余碰撞：**863 org ID + 2 person ID**
- 影子组：**993 组**
- 动作：
  - `assign_new_id`：983（org 981 + person 2）
  - `review_cross_country`：8
  - `review_ambiguous`：2
- 热点：KR 427、MX 218、NZ 115、JP 114、VN 47、SG 39、PG 20

注意：这 983 个新 ID 仍按冲突 ID 的国家/类别分配，个别实体可能属于其他国家（例如 JP 下出现“清华大学”）；批量前建议先按国别/类型抽查 KR/MX/NZ/JP。

## 七、新 ID 抽查样本（80 条，待复核）

`output/_id_audit/registry_newid_sample_80.csv`

- KR/MX/NZ/JP 各 20 条，全部有实际引用（按引用数排序）
- 71 条机器判断“可分配”
- 7 条“需确认类别”：例如 MX 墨西哥电话公司（Telmex）落在 `MX-GOV`、NZ On Air 落在 `NZ-GOV`、JP INCJ 落在 `JP-GOV`
- 2 条“需确认国别”：外国机构落在本国碰撞 ID 下（如 NZ 的日本地质调查局、MX 的美国南部院校协会）
- 复核列：`复核结论` 填 `分配` / `改类别后分配` / `不分配` / `挂起`；`备注` 写建议类别或理由

批量写入时会按复核结论调整 `new_id` 的类别（例如把 Telmex 从 `MX-GOV-861` 改为 `MX-CORP-xxx`），不会直接照 CSV 的 `建议新ID` 盲写。

## 八、新 ID 计划 v3（修正分配器 + 影子去重）

已完成：
- 编号分配器改为“全部历史编号”口径：active + deprecated + duplicate/trimmed/merged + 画像 + name_index；14 个历史重用编号全部避开。
- 影子实体去重：993 条 → 985 个 identity；KAIST 与全量 KR-ACAD-006 共用 `KR-ACAD-026`，Commerce Commission 两行共用 `NZ-GOV-152`，Hyundai Steel 两条仍 defer。
- 80 条样本结论落表：53 approved_sample、8 pending_realloc、7 same_identity、5 no_assign、14 defer（13 条样本 + 1 条全量）、906 pending_review。
- 新 ID 分配 967 个，`reused_reserved_14 = 0`。

产物：
- `output/_id_audit/registry_newid_plan_v3.csv`
- `output/_id_audit/registry_newid_plan_v3_summary.json`
- `docs/registry-newid-plan-v3.md`

**尚未写入任何新 ID 或引用。**

## 九、61 条样本执行结果

- 新建 61 个 registry 身份（`auto_registered`，暂无画像）
- 7 条 same_identity 合并，不单独发号
- 226 个引用位置改到新 ID / 共同新 ID；当前 240 条引用指向这 61 个新 ID
- 14 个历史编号零重用
- 头像 0 变更
- 回滚：`output/_id_audit/registry_newid_exec_undo.json`
- 补画像清单：`output/_id_audit/newid_profile_backlog.csv`（61 个新 ID / 240 条引用）

审计变化（执行前 → 执行后）：

| 指标 | 前 | 后 |
|---|---:|---:|
| work_org 指向错误 | 8,876 | 8,744 |
| related_org 指向错误 | 2,365 | 2,257 |
| person_rel 指向错误 | 2,805 | 2,801 |
| key_people 指向错误 | 302 | 298 |

悬空增加（work 6,869→6,983、related 5,739→5,847）是因为新身份暂无画像，属于预期“无档案”，不是错链。

下一批 80 条待复核样本已生成：
`output/_id_audit/registry_newid_sample_80_next.csv`（KR/MX/NZ/JP 各 20；60 条有引用，22 条带风险提示）。

## 十、第二批 80 条修复与执行（v4）

- 编号保留集合已纳入所有业务引用中的非空 ID；3 个“未注册但已被引用使用”的候选号未再分配。
- 上轮 4 条未闭合 same_identity 源项已恢复为活动注册项（merge_closure_repair_undo.json）。
- 本批 25 分配 + 2 改类别已执行：27 个新 registry 身份、25 个引用位置、18 个文件；0 历史号重用、0 头像变更。
- 25 不分配、28 挂起未执行；4 条人物误作组织、考试资格/职位/机构集合均未新建组织。
- 当前剩余：约 826 pending_review、42 defer、30 no_assign；88 个新身份无画像（265 条引用）。
- 详见 `docs/registry-newid-v4-execution.md`。

## 十一、826 条复核执行（v5）

- 315 条新身份已建立（297 同国 + 18 跨国目标国已有数据集）；140 个引用位置改链。
- 17 条跨国目标国未采集（DE/GB/CH/IN/IE/AR/IT）→ `defer_no_dataset`。
- 194 条不再新建、300 条挂起未执行。
- 403 个新身份暂无画像（405 条引用），清单 `newid_profile_backlog.csv`。
- 审计：work wrong 8,744→8,703、related wrong 2,232→2,133。
- 详见 `docs/registry-newid-v5-826-execution.md`。

## 十二、4 组重复人物档案合并

- 保留 154/102/126/142，归档 162/114/PE-171/US-685；5 个引用位置改到主档案。
- 4 个主档案 strict 校验 0 error；102 顺手清理 education 的 org_id 与自指关系。
- person 头像画像 9,001→9,000；US-685.jpg 作为孤儿文件保留。
- 详见 `docs/merge-duplicate-persons.md`。

## 十三、19 组重复组织身份归并

- 18 组建单一新身份（38 条影子移除，18 个新 registry ID，2 条 Mapletree 引用改链）。
- WHO 全球主体暂缓；UNDP 同名对另列。
- 审计 related_org 指向错误 2,133→2,131。
- 详见 `docs/registry826-duplicate-org-groups.md`。

## 十四、WHO / UNDP 全球主体归一

- 新建 `US-INTL-005`（WHO, Q7817）与 `US-INTL-024`（UNDP, Q161718）。
- 合并 32 条全球重复注册影子，63 个引用位置改链；7 条复合引用跳过。
- 国别/区域办事处保留；PG-INTL-003 owner 注册项补回。
- 审计：work ok 59,205→59,230、related ok 18,133→18,175。
- 详见 `docs/who-undp-normalization.md`。

## 十五、WHO/UNDP 复合引用拆条

- 5 条误判双语斜杠直接改到全球主 ID；2 条真复合 work_experience 各拆成 4 条。
- 旧 ID 残留引用 0；work ok +2、related ok +5。
- 详见 `docs/who-undp-normalization.md`。

## 十六、剩余 260 条组织挂起项清理

- 251 条 registry 影子归档为 `unresolved_shadow`，49 条此前已解决。
- 127 个错误 org_id 置空，文字履历保留；未新建 ID、未改画像/头像。
- work wrong 8,701→8,646、related wrong 2,129→2,067。
- 详见 `docs/registry826-deferred-cleanup.md`。

## 十七、18 个高引用新身份补画像

- 18 个高引用新身份已建画像（JP/MX/KR/NZ），strict 0 error。
- 146 条引用由“无画像”变为正确指向；backlog 403→385（405→259 refs）。
- OpenAI/Anthropic/SpaceX 不在 backlog，仍是 US registry 的 trimmed 冲突条目，需单独全球归一。
- 详见 `docs/newid-highref-18-profiles.md`。

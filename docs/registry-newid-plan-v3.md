# 新 ID 执行计划 v3（修正分配器 + 影子实体去重）

日期：2026-11-13  
状态：**只生成计划，未分配 ID、未改引用、未改 registry/画像/头像**

输入：
- `output/_id_audit/registry_dedupe_plan_v2.csv`
- `output/_id_audit/registry_newid_sample_80_reviewed.csv`
- `output/_id_audit/registry_newid_reserved_14.csv`

输出：
- `output/_id_audit/registry_newid_plan_v3.csv`
- `output/_id_audit/registry_newid_plan_v3_summary.json`

## 一、修正编号分配器

v2 只用“当前画像 + active registry”计算 max，排除了 duplicate/trimmed/merged 等历史条目，导致 14 个候选编号与既往登记重合。

v3 的 `ever_used` 集合包含：

- 所有 `id_registry.json` 的 `registry` / `person_registry`
- 所有 `deprecated_registry` / `deprecated_person_registry`（含 duplicate/trimmed/merged）
- 所有画像文件 ID
- 所有 `_name_index.json` 的 ID 值

分配时从“该国该类别历史最大号 + 1”开始，并逐号检查是否在 `ever_used` 中；新分配的号立即加入集合，避免同批重复。

**结果：14 个历史编号全部避开（reused_reserved_14 = []）。**

## 二、影子实体去重

v2 按 collision_id 分别发号，同一实体在多个 collision_id 下会拿到多个新 ID。v3 先按 `(国家, 规范化影子名)` 分组，并加人工别名：

- KAIST ↔ Korea Advanced Institute of Science and Technology → 同一 identity
- Commerce Commission ↔ Commerce Commission NZ → 同一 identity
- Hyundai Steel 两条 → 同一 identity（但本轮仍挂起）

结果：993 条影子记录 → **985 个 identity**，8 条被合并为 same_identity。

## 三、80 条复核结论落表

| 复核结论 | 样本条数 | v3 状态 |
|---|---:|---|
| 分配 | 51 | `approved_sample` |
| 改类别后分配 | 2 | `approved_sample` |
| 挂起（编号重用 8 条） | 8 | `pending_realloc`（已给新号，待确认） |
| 挂起（其他） | 13 | `defer` |
| 不分配 | 6 | 5 `no_assign` + 1 `same_identity`（Commerce 第二行） |

样本 21 条挂起中，8 条是“建议编号已被历史占用”，v3 已用修正分配器重发新号，但仍标记 `pending_realloc`，不算批准。

## 四、全量状态

| 状态 | 行数 | 含义 |
|---|---:|---|
| approved_sample | 53 | 80 样本中明确“分配/改类别后分配” |
| pending_realloc | 8 | 样本因编号重用挂起，已重发新号待确认 |
| same_identity | 7 | 与同组 canonical 共用新 ID，不单独发号 |
| no_assign | 5 | 样本明确不分配 |
| defer | 14 | 样本因跨国/沿革/粒度挂起 |
| pending_review | 906 | 全量计划中尚未人工复核 |
| **合计** | **993** | |

- 新 ID 分配：**967 个**（53 + 8 + 906），全部未命中历史编号
- `reused_reserved_14`：**0**

## 五、关键编号（样本）

| 实体 | 新 ID | 说明 |
|---|---|---|
| Shinhan Financial Group | `KR-FIN-016` | 避开已登记的 KR-FIN-015（Bank of Korea） |
| Korea University | `KR-ACAD-024` | 避开 KR-ACAD-017 |
| Yonsei University | `KR-ACAD-025` | 避开 KR-ACAD-018 |
| KAIST | `KR-ACAD-026` | 与全量 KR-ACAD-006 合并为同一 identity |
| POSTECH | `KR-ACAD-027` | 避开 KR-ACAD-020 |
| LG Energy Solution | `KR-CORP-034` | 避开 KR-CORP-031 |
| Munhwa Broadcasting | `KR-MEDIA-019` | 避开 KR-MEDIA-017 |
| Yonhap News | `KR-MEDIA-020` | 避开 KR-MEDIA-018 |
| Telmex | `MX-CORP-093` | 类别由 GOV 改 CORP |
| RIKEN | `JP-ACAD-038` | 类别由 GOV 改 ACAD |
| IPA | `JP-GOV-898` | 拒绝错误的阿尔及利亚合并目标 |
| NARO | `JP-ACAD-039` | 拒绝错误的乌干达合并目标 |
| Commerce Commission | `NZ-GOV-152` | 两条样本共用；第 47 行 same_identity |

Hyundai Steel 两条均 `defer`，未发号；按你的意见应先确认其与 HD 现代/现代汽车的错误关系，再决定是否共用一个主 ID。

## 六、下一步

1. 先确认 8 条 `pending_realloc` 的新号（已避开历史编号）是否接受；
2. 确认后执行 **53 + 8 = 61 条样本**的 registry 写入与引用迁移；
3. 剩余 906 条仍为 `pending_review`，需继续抽样/复核，不能直接批量；
4. 执行时仍需逐条校验引用位置、名称和当前 ID，并写 undo。

**本轮没有执行任何 ID 分配或引用修改。**

---

## 七、执行记录（2026-11-13）：61 条样本

按“执行 61 条样本”授权执行：

| 动作 | 数量 |
|---|---:|
| 新建 registry 身份（approved_sample 53 + pending_realloc 8） | **61** |
| same_identity 合并（不单独发号） | **7** |
| 引用改到新 ID / 共同新 ID | **226 个位置 / 154 个文件** |
| 当前指向新 ID 的引用总数 | **240** |
| 历史编号重用（reserved 14） | **0** |
| 头像变更 | **0**（9,001 person + 3,965 org） |

- 新 registry 条目状态为 `auto_registered`，**暂无画像**；新增 61 个新 ID 的补画像清单：
  `output/_id_audit/newid_profile_backlog.csv`（61 行 / 240 条引用）
- 旧 collision ID 的 owner 画像保持不变（抽查 KR-FIN-002、KR-ACAD-004、NZ-GOV-038、JP-GOV-002 均只剩 owner 条目）
- 回滚：`output/_id_audit/registry_newid_exec_undo.json`
- 汇总：`output/_id_audit/registry_newid_exec_summary.json`

未执行：906 条 pending_review、14 条 defer、5 条 no_assign。

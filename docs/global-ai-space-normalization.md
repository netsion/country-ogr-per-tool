# 全球 AI/航天实体归一：OpenAI / Anthropic / SpaceX / Starlink / xAI

- 执行日期：2026-11-13
- 范围：全库 53 个数据集的 registry、org 画像、person work_experience、org related_entities
- 执行脚本：`scripts_tmp/normalize_global_ai_space.py`
- 撤销日志：`output/_id_audit/global_ai_space_normalize_undo.json`

## 1. Canonical ID

| 实体 | Canonical ID | 画像 | 类型/子类型 | Wikidata |
|---|---|---|---|---|
| OpenAI | `US-CORP-249` | 新建 | CORP / private_company | Q21708200 |
| Anthropic | `US-CORP-250` | 新建 | CORP / private_company | Q116758847 |
| SpaceX | `US-CORP-251` | 新建 | CORP / private_company | Q193701 |
| Starlink | `US-CORP-252` | 新建 | CORP / subsidiary | Q127785902 |
| xAI | `US-CORP-069` | 补建 | CORP / subsidiary | Q120599684 |

ID 选择：

- `249–252` 是 US-CORP 当前最大序号 248 之后的连续空闲号；已用集合包含 registry、deprecated、profiles、name index 和所有业务引用，确认未被历史使用。
- xAI 沿用已有 `US-CORP-069`，不重新分配。
- 没有改动任何已有画像的 ID；新建画像的 `profile` 均为 `null`，未移动、未新建头像。

## 2. 注册项清理

### 2.1 已合并的重复/影子注册项

| 数据集 | 旧 ID | 旧名称 | 合并到 |
|---|---|---|---|
| AU | `AU-CORP-040` | SpaceX/Starlink | `US-CORP-252` |
| AU | `AU-CORP-087` | SpaceX Starlink | `US-CORP-252` |
| CL | `CL-CORP-071` | 星链 (Starlink / SpaceX) | `US-CORP-252` |
| JP | `JP-CORP-059` | OpenAI（OpenAI Global, LLC） | `US-CORP-249` |
| KW | `KW-航天与卫星通信企业-001` | 太空探索技术公司/星链 (SpaceX / Starlink) | `US-CORP-252` |
| PE | `PE-CORP-038` | 星链 (Starlink) | `US-CORP-252` |
| PG | `PG-CORP-031` | Starlink（SpaceX） | `US-CORP-252` |

这些条目已从各数据集 `registry` 移入 `deprecated_registry`，状态为 `merged`，并写入 `merged_into`。

### 2.2 US 碰撞 ID 下的影子项

| 旧 ID | 影子名称 | 合并到 | 说明 |
|---|---|---|---|
| `US-CORP-013` | Anthropic | `US-CORP-250` | 该 ID 的 owner 是 Tesla，Tesla 引用不受影响 |
| `US-CORP-014` | OpenAI | `US-CORP-249` | 该 ID 的 owner 是 Ford，Ford 引用不受影响 |
| `US-CORP-026` | SpaceX | `US-CORP-251` | 该 ID 的 owner 是 Cisco，Cisco 引用不受影响 |

三条原本已在 `deprecated_registry` 中（`trimmed`），本次改为 `merged` 并补 `merged_into`。

## 3. 引用修正

共修改 **35 条**引用；另有 2 条原本已指向 canonical（xAI），1 条复合引用保留空值。

| 实体 | 修改引用数 | 主要来源 |
|---|---:|---|
| OpenAI | 16 | Musk、US-217、US-679 工作经历；Amazon、Microsoft、SoftBank、K-water 等 related_entities |
| Anthropic | 3 | Amazon、Microsoft、Alphabet |
| SpaceX | 7 | Musk、Kimbal Musk、Alphabet、Tesla、Boeing、US-GOV-024、US-MIL-004 |
| Starlink | 8 | AE TDRA、Telstra、NBN、Entel Chile/Peru、Alghanim、Telikom PNG |
| xAI | 1 | Iraq Shafaq News |

### 特殊处理

- **US-CORP-013/014/026 的 owner 引用不动**：只改名称匹配 Anthropic/OpenAI/SpaceX 的引用；Tesla、Ford、Cisco 的引用逐条保留。
- **SpaceX/Starlink 复合引用归到 Starlink**：这些引用描述的是星链服务/品牌，统一到 `US-CORP-252`；SpaceX 与 Starlink 之间用 `parent_org`/`subsidiary` 关联。
- **OpenAI Foundation & OpenAI Group PBC**：`US-PERSON-000565` 的一条工作经历同时涉及两个法律实体，保留 `org_id: null`，不强行绑到 OpenAI。
- **AE Starlink Satellite Communications LLC**：描述明确为 SpaceX 旗下卫星互联网服务商，归到全球 Starlink；如果后续需要保留阿联酋本地持牌法人，可再单独拆分。
- **xAI**：画像保留 xAI 名称；Wikidata 当前实体为 `Q120599684`（SpaceXAI），已在 aliases 中保留 `SpaceXAI`，并标注 2026 年成为 SpaceX 子公司。

## 4. 名称索引

已重建以下数据集的 `_name_index.json`：

`au/2026-05-08`、`cl/2026-10-02`、`jp/2026-06-09`、`kw/2026-10-03`、`pe/2026-10-01`、`pg/2026-05-25`、`us/2026-09-05`

US 索引已验证：

- `OpenAI`、`OpenAI Global, LLC`、`OpenAI Group PBC`、`开放人工智能` → `US-CORP-249`
- `Anthropic`、`Anthropic PBC` → `US-CORP-250`
- `SpaceX`、`Space Exploration Technologies` → `US-CORP-251`
- `Starlink`、`Starlink Satellite Communications LLC`、`星链卫星通信公司` → `US-CORP-252`
- `xAI`、`X.AI`、`SpaceXAI` → `US-CORP-069`

旧影子 ID 不再作为这些名称的目标出现在索引中；`US-CORP-013/014/026` 只保留 Tesla/Ford/Cisco 的 owner 名称。

## 5. 校验与审计

- 5 个 canonical 画像：`--strict --cross-ref` 单文件校验 **0 errors / 0 warnings**。
- 全库 42 条相关技术实体引用：**0 条仍指向旧 ID 或非 canonical ID**。
- 31 个被修改的引用文件：未引入与本次实体相关的新错误；AE/AU 等文件的 strict 错误均为既有 `key_people.person_id` 缺失，与本次修改无关。
- 全量 US strict 仍有 403 条历史错误（既有数据问题，本次未新增相关错误）。
- ID 审计变化：
  - work_org：ok 59,316 → 59,322；wrong 8,646 → 8,642；dangling 6,909 → 6,908
  - related_org：ok 18,234 → 18,273；wrong 2,075 → 2,056；dangling 5,862 → 5,854

## 6. 撤销

`output/_id_audit/global_ai_space_normalize_undo.json` 包含：

- 每个 registry 的合并/新增/更新记录（含旧条目）
- 35 条引用变更的 file/array/index/old/new/ref_name
- 新建画像路径
- US `_index.json` 的总数变化

如需回滚，可按该日志恢复 registry、引用和画像文件；名称索引需重新生成。

## 7. 后续

- 本次只做 ID/注册项/引用归一，未做深度画像 enrichment；5 个画像均为最小可链接画像，后续可补高管、融资、产品、事件等。
- OpenAI Foundation / OpenAI Group PBC 若后续作为独立实体入库，应另分配 ID，不与 `US-CORP-249` 混用。
- 若需要保留阿联酋本地 Starlink 持牌法人，可从 `US-CORP-252` 拆出独立本地实体。

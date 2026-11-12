# 工作区卫生规范（临时文件与杂物管理）

> 2026-11-12 全库清理后立约。背景：历史遗留 ~28,000 个临时文件/4.8GB（根目录散件、
> 数据集内 `_tmp/`、`_cache/`、证据残留、一次性脚本混进 persons/orgs）。
> 采集子代理与管线脚本**必须**遵守本规范。

## 铁律（违反 = 数据会被误删或污染 git）

### 1. 临时文件的位置
- 抓取的证据页（html/htm/pdf/xml/txt/csv）、候选图、试跑脚本 → 一律放
  `output/<cc>/<date>/_tmp/`（已 gitignore）
- **禁止**散放在仓库根目录、数据集目录根部、`persons/`、`orgs/` 目录
- 仓库根目录 = 配置 + 文档 + 脚本目录，**抓取物一律禁入**

### 2. 用完即删
- 当轮采集任务收尾时**清空 `_tmp/`**（子代理收尾清单必须有这一项）
- `_cache/` 是管线级缓存（gitignore 已挡），跨任务可留但不得手动往里塞杂物

### 3. 脚本的位置
- 一次性脚本 → `scripts_tmp/`（有意长期保留的经评审移入 `scripts/`）
- **禁止**把 `_write_*.py`、`_enrich_*.py` 之类写进数据集目录

### 4. 数据集目录白名单（output/<cc>/<date>/）
| 允许 | 示例 |
|---|---|
| 档案 JSON | `persons/<ID>.json`、`orgs/<ID>.json` |
| 注册表/清单 | `person_list.json`、`org_list.json`、`id_registry.json`、`_target_orgs.json`、`_name_index.json`、`_phase_progress.json`、`_coverage_report.json` |
| 缓存/临时（gitignored） | `_cache/`、`_tmp/` |
| **其他任何文件不得出现** | 证据散件、脚本、图片一律不许 |

### 5. 图片
- 本地正本唯一位置：`minio-store/default/…`（gitignore）
- 数据集 photos 目录已废弃，不再使用

### 6. 进行中数据集保护（in-flight，最高优先级）
- 仍在采集/充实中的数据集，在 `output/<cc>/<date>/` 放置 **`.inflight`** 标记文件
- **任何清理脚本遇 `.inflight` 必须跳过该数据集整体**（包括 _tmp/、证据散件、队列 json）
- 队列/进度类文件（`*_queue.json`、`remaining_persons.json`、`*_progress*.json`、
  `_missing_persons*`）即使无标记也**默认保留**，不得按"散件"清理
- 收尾后删除 `.inflight` 标记，数据集才进入可清理范围

## gitignore 兜底
`.gitignore` 已按上述规则拦截（`output/**/_tmp/`、根目录抓取后缀等），
被拦 ≠ 可以乱放——磁盘整洁与 git 整洁是两回事。

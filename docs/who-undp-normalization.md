# WHO / UNDP 全球主体归一记录

日期：2026-11-13

## 目标

把全库中重复登记的 **WHO 全球主体**和 **UNDP 全球主体**合并为两个主画像；国别办事处/区域办事处保留独立身份，不并入全球主体。

## 新建主画像

| 组织 | 主 ID | QID | 总部 | 成立 | 官网 |
|---|---|---|---|---|---|
| 世界卫生组织 WHO | `US-INTL-005` | Q7817 | 瑞士日内瓦 | 1948-04-07 | who.int |
| 联合国开发计划署 UNDP | `US-INTL-024` | Q161718 | 美国纽约 | 1965-11-22 | undp.org |

- 两个画像 `--strict`：0 error / 0 warning
- US org index：166→168
- name_index：`世界卫生组织/WHO` → US-INTL-005；`联合国开发计划署/UNDP` → US-INTL-024

## 合并范围

- WHO 全球注册项：19 个 ID，移除 18 条影子（保留 US-INTL-005）
- UNDP 全球注册项：13 个 ID，移除 14 条影子（部分 ID 有两条重复项）
- 共移除 **32 条**影子注册项，均标 `merged` + `merged_into`
- 引用改链：**63 个位置**
  - WHO：25
  - UNDP：38
- **7 条复合引用跳过**：名称同时含多个机构（如“联合国开发计划署/联合国妇女署/…”或“FLACSO…与联合国开发计划署…”），不能整行改到一个机构，留待拆条。

## 明确保留的国别/区域办事处

未并入全球主体，保持独立注册身份：

- WHO：`JO-INTL-001`（约旦办事处）、`PH-INTL-003`（西太平洋区域办事处，已画像）、`PH-INTL-021`（菲律宾办事处）、`PH-INTL-022`（东南亚区域办事处）
- UNDP：`MA-INTL-013`（摩洛哥办事处）、`PE-INTL-009`（秘鲁办事处）、`TM-INTL-003`（土库曼斯坦办事处，已画像）、`JP-GOV-285`（UNDP 治理团队）

## 附带修复

- `PG-INTL-003` 的 owner 画像“联合国巴布亚新几内亚”原先没有活动 registry 条目；本次归一移除其 WHO 影子后补回 owner 注册项，避免“有画像但 registry 无条目”。
- `SG-INTL-001` 的 owner APEC 秘书处条目保持不动。

## 审计变化

| 指标 | 前 | 后 |
|---|---:|---:|
| work_org 正确指向 | 59,205 | 59,230 |
| work_org 悬空 | 7,024 | 6,999 |
| related_org 正确指向 | 18,133 | 18,175 |
| related_org 指向错误 | 2,131 | 2,129 |
| related_org 悬空 | 5,973 | 5,935 |

## 头像

- person 9,000 / org 3,965，未变
- 两个新画像无头像（`profile: null`）

## 回滚

- 归一：`output/_id_audit/who_undp_normalize_undo.json`
- PG owner 恢复：`output/_id_audit/who_undp_pg_owner_restore.json`

## 未处理

- 7 条复合引用需拆条
- WHO/UNDP 国别、区域办事处是否要单独补画像
- 其余约 260 条组织挂起项

## 七、7 条复合引用处理（2026-11-13）

复核发现 7 条“复合”中只有 2 条是真复合，另 5 条是 `UNDP / PNUD`、`OMS/WHO` 这类双语斜杠，不是多机构。

### 5 条误判复合（已直接改链）

| 文件 | 原 ID | 新 ID |
|---|---|---|
| CD-GOV-008 | CD-INTL-010 | US-INTL-024 |
| CD-GOV-012 | CD-INTL-010 | US-INTL-024 |
| CD-GOV-016 | CD-INTL-016 | US-INTL-005 |
| CD-GOV-022 | CD-INTL-016 | US-INTL-005 |
| LB-GOV-018 | LB-INTL-008 | US-INTL-024 |

### 2 条真复合（已拆条）

- `CL-PERSON-000467` work[8]：拆成 4 条
  - 联合国开发计划署（PNUD）→ `US-INTL-024`
  - 联合国妇女署（ONU Mujeres）→ null（暂无主画像）
  - 智利地方发展基金会（Fundación Chile Descentralizado）→ null
  - 智利国家人权研究所（INDH）→ null
- `CL-PERSON-000497` work[9]：拆成 4 条
  - 拉丁美洲社会科学学院（FLACSO）→ null
  - 北卡罗来纳大学教堂山分校→ null（依据原 description 中“客座教授一年”补出）
  - 联合国开发计划署（PNUD/UNDP）→ `US-INTL-024`
  - 联合国区域就业项目（PREALC）→ null

### 结果

- 7 条复合引用全部处理；旧 ID 残留引用 **0**
- work_experience 总数 +6（2 条拆成 8 条）
- work null +6（未建画像的分支）、ok +2（UNDP 分支）
- related_org ok +5、dangling −5
- 回滚：`output/_id_audit/who_undp_composite_undo.json`

审计变化：

| 指标 | 前 | 后 |
|---|---:|---:|
| work_org 总数 | 129,315 | 129,321 |
| work_org 空 ID | 54,385 | 54,391 |
| work_org ok | 59,230 | 59,232 |
| work_org 悬空 | 6,999 | 6,997 |
| related_org ok | 18,175 | 18,180 |
| related_org 悬空 | 5,935 | 5,930 |

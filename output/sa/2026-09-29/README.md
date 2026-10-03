# 沙特数据集说明（SA / 2026-09-29）

## 范围与规模

- **组织档案**：159 份（`orgs/`），平均完整度 91，覆盖 GOV/SOE/CORP/MEDIA/NGO/ACAD/FIN/INTL/PARTY/MIL 十类。
- **人物档案**：459 份（`persons/`），平均完整度 64；照片 329 张（`photos/`）。
- 收集管线：`country-org-collector` skill（5 Phase 子代理流水线），人物 P4 队列 530 项全部完成，另合并重复建档 95 项（明细见 `_p4_progress.json` 的 duplicates/notes）。

## 两项入库决策（下游必读）

1. **约 305 个 org key_people 引用的人物有意未建档**：人物清单共 834 人，P4 队列按重要性筛选 530 人，其余（多为 low importance）在第二轮补采被取消后维持"已注册未建档"状态。下游遇到 `person_id` 悬空引用（org 档案指向 `persons/` 中不存在的 ID）属**已知设计状态**，名单可在 `id_registry.json` 按 status=listed 查询。
2. **履历/教育条目内的扩展字段**（`source`、`is_current`、`note`、`org_id_note` 等，约 5,000 处）为收集过程中的**溯源与勘误约定扩展**，不在 `person_profile_schema.json` 严格模式内；保留原因是其承载来源与考证信息。使用严格 schema 校验时可将这些字段视为允许的扩展。

## 质量基线（2026-10-04 补弱收官后）

- schema 校验：618 文件 **0 errors**（标准模式；warnings 1,052 为可选字段缺省提示）。
- 中文规范：name_zh/biography/current_positions/括号方向全部合规；剩余 19 处组织名为国际品牌无官方中文名者，按「原名 (译名)」处理属合规例外。
- 头像：329 张本地照片全部经 magic bytes 验证；`profile.source_url` 已清除全部 HTML 页面型链接。仍有约 70 档案无可靠公开肖像（法官/军方/王室等，排查依据见各档 `profile_note`）。
- 社媒账号：512 条全部经实名核实（宁缺毋滥）；178 档案经六平台双语排查确无本人实名账号（排查记录见 `social_accounts_note`）。

## 已知局限

- 人物 completeness 平均 64：66 份 <50 分档案多为公开信息天然有限者（法官/军方/王室低曝光成员），各档 notes 已写明排查过程。
- `work_experience` 中约 991 条仅有组织+职务、无起止日期的条目，系公开来源仅记载任职事实所致，保留不编造。
- `profile.source_url` 个别为动态图片端点（kau/mewa/ncpd 等），可返回图片但稳定性依赖原站。

## 过程文件

`_cache/`（gitignore）内为子代理抓取的网页/PDF/脚本缓存；`_backup/` 为合并废置档案存档；进度与审计记录在 `_p4_progress.json`、`_enrich_progress.json`、`_quality_check*.json`。

# country-org-collector — 事故恢复说明（2026-11-28）

## 事故
2026-11-28 13:33 左右，同一仓库 `D:\ai-workspace\apec-osint-tool` 上并行运行的
**PS（巴勒斯坦）数据集会话**发生误删事故，清空了整个仓库：`.git`、`.agents/`、
`output/mm/`（缅甸数据集，P1-P3 成果）、`scripts_tmp/` 全部丢失。

## 恢复来源与方式（已全部完成）
### 0. 仓库与 skill 脚本
- 仓库从 git 远端完整恢复（`.git`、`.agents/` 均在），9/9 skill 脚本完整，
  无需按 transcript 重写；`generate_profiles.py` 的 `"MM": "MMR"` 映射保留
- 本说明保留为事故记录与数据验收依据

### 1. 缅甸组织画像（output/mm/2026-11-27/）
- 从 160 个 P3 子代理 transcript 提取 **147 个写入脚本**（子代理当时写入的
  `scripts_tmp/*.py`）
- 三条恢复路径：
  - AST 提取模块级 dict 字面量 → 102 个 org
  - 沙箱执行（注入最小骨架 + 拦截文件 I/O）→ 33 个 org（含 needs-skeleton 型）
  - 定点修复后执行 → 2 个 org（MM-MIL-003 引号截断、MM-ACAD-004 引号截断）
- **共恢复 137/138 个组织**；MM-PARTY-012（克钦邦人民党）从未完成（P3 三次
  尝试均被平台内容过滤拦截），文件不存在
- 恢复后全量 `validate_schema.py --score`：**0 errors**，mean 82.8 / median 83 /
  min 63 / max 100

### 2. 辅助文件（已重建并校准）
- `id_registry.json`：重建 + `resolve_ids.py --allow-register` 重跑，
  **595/595 key_people 全部挂接 person_id**；person_registry 487 人，
  person_counters MM=838
- `_name_index.json`：`generate_name_index.py` 重建（3185 条）
- `_target_orgs.json`：148 条（138 MM + 10 INTL），已补入 MM-GOV-045（SSPC），
  10 个 INTL 在 registry 中登记为 `status=excluded`
- `_phase_progress.json`：completed 137 / failed [MM-PARTY-012]

### 3. P3 层校验结果（2026-11-28）
- `--score`：137 文件，**0 errors**（409 warnings 均为 dept_id 空）
- `--strict --cross-ref`：**0 条组织级错误**；剩余 665 条均为
  “person_id 存在但 persons/ 无档案”，属 **P4 未执行**的预期状态
- 本轮修复：补 2 个 name_zh、6 个繁体/同义译名 aliases、解绑 1 处 DSTA→DSA
  误绑定（MM-ACAD-007→MM-MIL-008）、解绑 1 处 related_entities 人物引用
  （MM-MEDIA-013）、kp 非规范字段归并（source_note→description）、
  10 个 INTL 登记 excluded
- 工具修正：`validate_schema.py` KP_FIELDS 增加 `source`（SKILL §1 铁律要求
  key_people 标注来源，原白名单漏配）

## 待办
- [ ] MM-PARTY-012（克钦邦人民党）补采 → 补完为 138/138
- [ ] P4 人物画像（595 个 person_id 尚无 persons/ 档案）
- [x] 仓库从远端恢复、skill 脚本 9/9 完整（原“重写 5 个脚本”待办取消）
- [x] 恢复后人工抽查 10 个 org 画像与脚本内容一致性（全部无损）

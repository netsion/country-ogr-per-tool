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
- 陷阱：`resolve_ids --allow-register` 会顺带回填 `related_entities[].org_id`，
  其拆词匹配会把泛词组件（`Associates`、`University of Computer Studies`、
  `University` 等）误配到同词组织，甚至产生自引用。本次回填 23 处，审计后
  回退 21 处误绑（自引用/泛词），仅保留 MM-PARTY-012 → UEC、SAC 两条正确项。
  运行该脚本后必须人工复核新增的 org 级引用。
- 陷阱：`python -I` 会把脚本目录移出 sys.path，导致 `atomic_write` 导入静默
  失败、名称分解退化为整串比较，`--strict` 名称校验产生大量假报错。运行
  skill 脚本不要加 `-I`。

## 待办
- [ ] MM-PARTY-012（克钦邦人民党）补采 → 补完为 138/138
- [ ] P4 人物画像（481 个活跃 person_id 尚无 persons/ 档案）
- [x] 仓库从远端恢复、skill 脚本 9/9 完整（原“重写 5 个脚本”待办取消）
- [x] 恢复后人工抽查 10 个 org 画像与脚本内容一致性（全部无损）

## ID 体系体检（2026-11-28，P4 前必做项）
- 组织 ID：138 文件 / 148 registry（138 profiled + 10 INTL excluded），
  格式、唯一性、序列、计数器全部一致；`counters.MM.PARTY` 已对齐 12
- 人物 ID：601 条 key_people 全部挂接；清洗后 **481 个活跃人物**，
  registry 496 = 481 活跃 + 15 条 `merged_into_*` 墓碑
- 合并（同人多个 ID，15 组，均经组织内描述/任职链交叉确认）：
  000035→000001（敏昂莱）、000357→000017（副主席梭温）、
  000436→000391（钦貌伦）、000549→000221（李松枝）、
  000517→000201（珊达乌）、000539→000536（温温貌）、
  000578→000058（钦益）、000573/000580→000052（昂林德威）、
  000582→000059（貌貌温）、000575→000067（貌貌觉）、
  000574→000053（耶温乌）、000465→000115（吴佐佐）、
  000149→000021（丹林）、000572→000062（郭郭伦博士/社会福利）
- 拆分（同 ID 混入不同人，3 组 + 1 处错挂）：
  000017 拆出卫生部长 Dr. Soe Win → 000845；
  000027 拆出选委会委员 U Ko Ko Lwin → 000846；
  000115 拆出民航局长 U Zaw Zaw → 000847；
  000062 的 MOGE 主管部长引用改挂能源部长 000027
- 保留的同名不同人（不合并）：梭温（党书记 000800/副主席 000017/卫生部长 000845）、
  觉林（CB Bank/医学会）、敏图（交易所 COO/内政部副部长）、丹泰（USDP/总参谋长）、
  温敏（最高法院/前总统）、昂基（副部长/NLD 首任主席）、
  郭郭伦（能源/社会福利/选委会）、山达乌（央行副行长/党派主席）等
- 待人工/联网复核（暂不合并）：杜塔津昂（IGE/银行 CEO）、吴威漂（记者/商会副会长）
- 工具修正：`generate_name_index.py` 过滤 `merged_into_*` 墓碑条目（此前会
  把已合并 ID 继续写进索引，导致后续 resolve_ids 引用废弃 ID）
- 人物计数器双键统一：`person_counters.MM` 与 `MM-PERSON` 均 = 847
  （generate_profiles 使用前者、resolve_ids 使用后者，必须同步）

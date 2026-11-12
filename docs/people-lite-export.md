# 人物原始 JSON → lite JSONL：流程、脚本与经验

适用对象：项目 `output/<地区代码>/<YYYY-MM-DD>/persons/*-PERSON-*.json`。
输出为 UTF-8 JSONL，一行一个人物对象；各国家/地区分开输出。此流程只转换已有档案，不负责收集新人物、判断职位是否仍在任，也不修改原始 JSON。

## 1. 快速开始

要求 Python 3.10+，在项目根目录执行。安装本工具的直接依赖：

```powershell
python -m pip install -r scripts/requirements-people-lite.txt
```

先准备**人工复核过**的已故排除名单；未发现已故人员也需提供空名单，不能把“未检测到”当作“全部在世”。文件格式见第 5 节。

```powershell
# 只检查来源与配置，不发翻译请求、不生成结果文件
python scripts/export_people_lite.py --countries hk tw --exclude-ids tmp/reviewed_deceased.json --dry-run

# 正式转换：自动选各地区日期目录中最新的 persons 快照
python scripts/export_people_lite.py --countries hk tw --exclude-ids tmp/reviewed_deceased.json

# 指定快照、各地区的排除名单及人工译文：先复制并修改示例配置
python scripts/export_people_lite.py --config docs/examples/people-lite-batch.json --dry-run
python scripts/export_people_lite.py --config docs/examples/people-lite-batch.json
```

默认输出在 `tmp/people_lite/`：`hk_people_simplified.jsonl`、`tw_people_simplified.jsonl` 等。默认不会覆盖过去直接存放在 `tmp/` 下的导出结果。

如果明确需要**不排除任何已故人员**，可用 `--include-all` 替代排除名单。该参数仅表示关闭过滤，不表示程序已完成生死核验。它不能与排除名单同时使用。

所有相对路径（包括配置文件内部路径）均以**命令执行时的工作目录**为基准。示例中的日期、文件名、人物 ID 都是模板，请改成实际值；示例排除名单为空，不能当作已完成死亡核查。

## 2. 已固化的处理流程

```text
选择日期快照 → 基础校验 → 已复核排除名单 → 字段标准化与职位表述规则
 → 校验人工译文覆盖 → 去重翻译任务/读取缓存 → 调翻译接口补缺
 → 写入暂存 JSONL → 独立校验 → 比对原始文件指纹 → 发布最终文件
```

批量入口按国家独立构建和发布。某一国家失败不覆盖该国上一版最终文件，也不阻止其他国家完成；**不是整个批次的全有或全无事务**。失败时 `.staging/` 可能留有待检查结果，不能把它当作正式交付文件。

日期目录必须为合法 `YYYY-MM-DD` 且包含 `persons/`，不会误选 `photos/`、`_cache/`。需要复现结果时必须固定日期，保留缓存、规则、人工覆盖及排除名单；“最新目录”每次可能不同。

### 基础校验怎么做

- 输入目录存在且包含标准人物文件；文件根节点必须是对象。
- `person_id` 必须符合 `XX-PERSON-000001`，且与文件名一致；跨目录也不能重复。
- 名称不能为空，按 `name → name_zh → name_en` 依次兜底。
- `current_positions` 接受字符串数组；兼容历史分号字符串，拆分为数组。其他类型、数组内非字符串项报错，不能悄悄丢掉职位。
- 字符串去首尾空白，职位和别名稳定去重；输出按人物 ID 排序。
- 禁止把结果、缓存、进度、报告写进输入 `persons/`；这些文件不能互相同名。
- 不扫描资料附件或随意读取其他 JSON 文件；输入集仅为标准人物文件。

### 字段映射

| lite 字段 | 生成规则 |
| --- | --- |
| `personId` | `person_id` |
| `personAvatar` | `profile.source_url`，没有则空串；每次从原始文件重读 |
| `personName` | `name`；缺失时依次取 `name_zh`、`name_en` |
| `transPersonName.zh` | `name_zh`，缺失则用上述名称；不擅自改其繁简 |
| `transPersonName.en` | `name_en`，缺失则用上述名称；兜底值不代表英语翻译合格 |
| `transPersonName.ar/km/ru/fr/es` | 基于人物名称翻译/音译，允许人工覆盖；不是翻译人物职位 |
| `keyword` | 名称、中英文名、所有译名、aliases 稳定去重后以 `\|` 连接；历史别名中的管道符也先拆分再去重 |
| HK/TW 额外关键词 | 依据**源人物 ID 前缀**加入 `name_zh` 的 OpenCC 繁体形式；不是依据最终国籍字段判断 |
| `region` | `nationality` 若是两位字母则大写，否则回退人物 ID 的地区前缀 |
| `current_positions` | 原职位去空白、稳定去重后的数组；历史分号字符串转为数组 |
| `occupation.zh` | 原职位转简体，再应用源地区的政治表述规则 |
| `occupation.ar/km/ru/en/fr/es` | 从规范化后的中文职位翻译；逐项对应，数量、顺序保持一致 |

注意：当前 `region` 是两位字母格式检查，**不是完整 ISO 码表校验，也不是国籍推断**。国籍写成中文、数组或缺失时会回退，必须核对原始数据；不会擅自把目录地区改为 `CN` 或其他国家码。空头像、空职位数组允许存在，但不能借此认定人物已故。

## 3. 政治表述规则的边界

顺序为 OpenCC `t2s` → 按地区匹配替换；长短语优先，避免短词破坏精确表达。
内置 TW 规则包括“中华民国总统”→“台湾地区领导人”等，其他地区默认不做额外替换。自定义规则通过 `--policy` 指定，指定地区的规则**整体替换**该地区内置列表，而不是追加。

```json
{"TW":{"replacements":[["中华民国总统","台湾地区领导人"],["中华民国副总统","台湾地区副领导人"]]}}
```

规则仅处理职位派生描述，不修改人物身份、党派专名或史实，也不自动证明全部政治表述合规。含糊的“总统”、组织专名、直接引语和历史称谓应逐条审阅，不宜全局替换。

为兼容最初要求，默认 `current_positions` 保留源表述，规范化用于 `occupation`。如果**所有导出职位字段**都必须采用规范化中文，单次构建可用 `--normalized-current-positions`，校验时也必须带相同参数。批量入口目前采用默认模式；它不会宣称源职位也已被规范化。

## 4. 翻译、缓存与人工修订

默认接口：`http://10.11.204.238:8080/translate`，通过 `--translation-endpoint` 可改。
请求 `POST {"dest":"ar","content":"..."}`，解析 `{"res":{"content":"..."}}`。
连接/读取超时分别为 5/60 秒；每个文本最多请求 4 次，失败后间隔 1、2、3 秒。

缓存键为 `目标语言 + NUL + 源文本`，会合并相同翻译任务。每完成约 25 项及每组结束保存缓存；重跑仅补缺。**接口成功、非空文本、100% 均不等于语义正确。** 缓存也会保留错误译文。

名称阿语/高棉语/俄语通常需要音译；法语、西语保留拉丁字母姓名常常合理，不应为了“看起来不同”乱翻。重点检查中文原样返回、中文与外文粘连、姓名被翻成地名/职务、性别和组织专名错误。职位翻译不能只翻“成员”而保留中文党名不作解释。

人工修订使用独立 JSON，**不修改原始档案，也不污染全局翻译缓存**：

```json
{
  "TW-PERSON-000001": {
    "source_name": "原始人物名",
    "source_positions": ["原始职位"],
    "transPersonName": {"fr": "Reviewed romanized name"},
    "occupation": {"fr": ["Fonction révisée"]},
    "note": "示例：替换为真实人物 ID、原名和经核对译文"
  }
}
```

通过构建器 `--overrides` 或批量配置每国 `overrides` 传入。`source_name` 必须匹配；覆盖职位时 `source_positions` 必须匹配**去重后的原始职位数组**，防止原始资料更新后套用旧译文。职位覆盖必须给出该语言的完整数组，不能数量不齐。规则修改后也应重新审阅人工职位译文。

`zh/en` 姓名直接映射原始字段、`occupation.zh` 由规则产生，不能用覆盖配置绕过；其源数据错误应单独提出修订原始档案，不能在导出脚本中暗改。覆盖配置只能包含本次未被排除的输入人物，错 ID 或陈旧配置会失败。

任何翻译任务失败，构建器停止、不发布缺译最终文件。批量入口还支持 `--fail-on-quality-warnings`，将中文残留、缺少目标文字等启发式警告作为发布阻断；可能有专名误报，需要人工处理。未开启时警告写入报告，不等于已经审阅通过。

## 5. 已故人员：候选与复核必须分开

```powershell
python scripts/detect_deceased_people.py --input output/kh/2026-10-04/persons --output tmp/death_candidates.json --report tmp/death_scan_report.json
# 无外网时仅检查简介中的死亡线索
python scripts/detect_deceased_people.py --input output/kh/2026-10-04/persons --output tmp/death_candidates.json --report tmp/death_scan_report.json --offline
```

**行为变更：** `detect_deceased_people.py` 现在输出 `review_status=pending` 和 `candidate_person_ids`，不再直接输出可用于过滤的 `excluded_person_ids`。旧调用方如果依赖自动过滤，必须增加人工复核环节；既有人工名单仍兼容。

Wikidata P570 和简介死亡词只产生候选，不自动排除。需要核对：QID 是否本人、出生日期是否相容、简介的死亡主语是否为亲属/前任、来源是否可信、死亡是否仅为传闻。没有 QID、没有候选不能证明在世。脚本不是完整死亡名册发现工具；有外网请求错误时报告不完整，不能宣称全部核验完毕。

本次固化的防错经验：

- 之前出现过同名人物 QID 误绑，导致在世人物被关联到古代死亡年份。生卒矛盾应回查身份，不修改原始 QID 来强行使结果一致。
- P570 未知值可能是 URI；不能截取成 `http://www` 作为日期。新脚本仅接受时间字面量，并保留年/月/日精度，不捏造 1 月 1 日。
- 简介第一句可能没有死亡信息；全文线索覆盖更广，但更容易命中他人，必须人工核对主语。
- 年龄大、已卸任、职位空缺、失踪或未经证实死亡都不能直接排除。

确认后另存已复核清单（示例为空，不代表核查已完成）：

```json
{
  "review_status": "reviewed",
  "excluded_person_ids": [],
  "evidence": []
}
```

建议在 `evidence` 中逐人记录 `person_id`、核实姓名/QID、死亡日期及精度、来源链接、核验日期、审核人和备注。构建器校验 ID 格式，不会自动审计这些证据真实性；提供名单意味着操作者已复核。

## 6. 校验、报告与进度

```powershell
python scripts/validate_people_lite.py --input output/kh/2026-10-04/persons --output tmp/people_lite/kh_people_simplified.jsonl --exclude-ids tmp/reviewed_deceased.json --report tmp/people_lite/kh_manual_validation.json
python -m unittest discover -s tests -v
```

校验器不联网：检查标准 8 字段、7 种语言、非空字符串、职位数组长度/顺序约束、源字段映射、头像同步、ID 集合与排除数、重复人物、完整关键词和 HK/TW 繁体名。它独立读取生成的 JSONL 并对照原始记录，但共用标准化函数；不做独立语义翻译判定，也不联网验证头像是否可下载。

批量入口会比较整个标准人物文件集的 SHA-256 指纹，发现处理期间原始资料变化则拒绝发布。报告记录所选快照及指纹；指纹验证无法替代真正冻结的数据快照。

工作目录文件：

| 文件 | 含义 |
| --- | --- |
| `<iso>_people_simplified.jsonl` | 已通过本次门禁的最终输出 |
| `<iso>_people_translation_cache.json` | 可重用翻译缓存，不要用其他国家并发写同一文件 |
| `<iso>_people_translation_progress.json` | 当国翻译阶段进度 |
| `<iso>_people_build_report.json` | 构建报告（构建完成不等于最终发布通过） |
| `<iso>_people_validation.json` | 结构错误、质量警告、来源快照/指纹与最终状态 |
| `<iso>_people_export.log` | 子进程标准输出、错误日志 |
| `batch_progress.json` | 批次 PID、国家级总数/完成/成功/失败、每国发布结果 |
| `.export.lock` | 批量工作目录互斥锁，内容为主进程 PID |

查看实时、可量化进度：

```powershell
Get-Content tmp/people_lite/batch_progress.json -Raw
Get-Content tmp/people_lite/kh_people_translation_progress.json -Raw
Get-Process -Id (Get-Content tmp/people_lite/.export.lock -Raw) -ErrorAction SilentlyContinue
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'build_people_lite|export_people_lite' } | Select-Object ProcessId,CommandLine
```

单国进度的 `stage/language/completed/total/succeeded/failed/percent/updated_at` 针对**当前阶段、当前语言的去重文本**；成功数含已有缓存。语言切换时分母重置，不能当作整批人物完成百分比。最终 `stage=completed` 表示构建器已完成暂存文件；正式发布还需看批次该国状态。批次百分比按已结束国家数计算（含失败），必须同时看 succeeded/failed。

进度文件会被保留，不能仅凭“文件存在”或旧 `completed` 判断新任务已完成。批次开始时只以本次批次状态为准，再检查 PID、更新时间与日志。程序运行不是有效完成量；报告应给出明确分子/分母。脚本不会自动创建定时通知；需要每 5 分钟通知时，另设监控读取上述文件和进程状态。

批量默认 3 国并行，每国最多 8 个翻译请求并行，理论上共 24；服务承压时减少 `--country-workers`、`--workers`。同一工作目录禁止两个批次并发。异常终止可能留下锁：先核对 PID 和所有构建子进程均已退出，再手工删除**该工作目录内这一把锁**；不要不加检查强制解锁。单次构建器不加批次锁，操作者必须保证它不与批次共享写缓存/输出。

## 7. 重导出与恢复操作

- **仅更新头像：** 指向更新后的原始快照重跑即可；读取最新 `profile.source_url`，复用翻译缓存，无需重新翻译姓名/职位。
- **修改 `name_zh/name_en`：** 直接映射及关键词重建；其他语种依赖 `name`，不会无条件重翻。更换人物本名或职位时，新源文本形成新缓存键，旧人工覆盖会触发匹配校验。
- **已知缓存错误：** 优先用人工覆盖。需要重翻时备份缓存后仅移除明确错误的键，不能指望重跑自动识别语义错误；不要删除全部缓存浪费请求。
- **中途失败：** 查看日志/报告，修正网络、来源或译文后用同一工作目录重跑。成功缓存保留，上版最终文件保留；构建全失败时旧验证报告也可能保留，应以本次批次失败结果为准。
- **原始 JSON 有误：** 转换不是事实修复。单独确认并更正原始档案后再导出；本工具不写原始文件。

## 8. 单次构建与维护入口

需要自定义输出名、多个源目录合并或兼容规范化 current_positions 时使用底层构建器；之后需自己调用校验器。

```powershell
python scripts/build_people_lite.py --input output/hk/2026-09-01/persons output/tw/2026-09-01/persons --output tmp/custom_people.jsonl --cache tmp/custom_translation_cache.json --progress tmp/custom_progress.json --report tmp/custom_report.json --exclude-ids tmp/reviewed_deceased.json
```

配置和脚本入口：

- `scripts/build_people_lite.py`：字段处理、去重缓存、翻译、人工覆盖、原子输出。
- `scripts/export_people_lite.py`：通用批量入口、日期发现、并发、暂存校验及发布。
- `scripts/validate_people_lite.py`：可单独调用的无网络校验器。
- `scripts/detect_deceased_people.py`：待复核死亡线索，不直接决定过滤。
- `tests/test_people_lite.py`：离线回归用例，不访问翻译服务或 Wikidata。
- `docs/examples/people-lite-*.json`：配置模板。

这套工具不依赖以往 `tmp/` 中某一批国家的专用脚本。迁移时保留已审核排除名单与翻译缓存，采用固定快照，先 dry-run 再正式导出，并检查质量警告和代表性人物的语义。

# 科威特（KW）数据集完整性报告（P5 收尾）

生成日期：2026-10-06 ｜ 数据目录：output/kw/2026-10-03/

## 一、数据集总览

| 维度 | 数值 |
|------|------|
| 组织画像 | 109 份（orgs/，均含 phase3_enriched，平均完整度 90） |
| 人物画像 | 256 份（persons/，phase4_person_profile，平均完整度 60） |
| 组织类型覆盖 | GOV 30、SOE 7、FIN 9、CORP 12、ACAD 11、MEDIA 5、NGO 4、PARTY 10、MIL 5、INTL 6 等 |
| 人物覆盖口径 | 党政军全等级 + 其他类别仅 high（按项目指令裁剪） |
| 人物构成 | 女性 31 人、已故 7 人（含空军创始人等历史人物 2 名） |

## 二、校验结果

- **Schema strict**：0 errors（orgs + persons 全量；存档 `_p5_validation_strict.txt`）
- **Cross-ref**：0 errors / 158 warnings（存档 `_p5_validation_crossref.txt`）
  - warnings 全部为「注册表有 ID 但 persons/ 无画像文件」：P3 阶段组织 key_people 自动注册的约 440 人中，按「党政军全等级+其他仅 high」口径仅 256 人纳入 P4 收集，其余留档不收集——**预期裁剪，非缺陷**
- **中文规范**（person_collection_rules.md 十类检查）：合规
  - name 本国官方语言：251 人阿语原名 + 5 名外籍人士母语名（合规豁免）
  - 4 名科威特籍英文姓名已修复（راشد خزعل / شريفة العدواني / محمد العبد / فهد العثمان，经 KUNA/Al-Jarida 阿语源核实）
  - 枚举值、日期格式、组织机构中文名格式、关系人名格式：0 违规
- **头像（profile.source_url）**：图片直链 74/256（29%），网页链接类坏链 0（补弱前 19 条全部清零或置 null）
- **社媒（social_accounts）**：147/256 人有账号，共 273 条（platform 枚举全合规）

## 三、P4 执行期间的数据修正存档

- **重复 ID 合并 5 对**：000384→379、000385→023、000171→183、000421→071、000399→089（注册表标 status=trimmed + merge_into）
- **任务卡/源数据勘误 15 处**：含 063 姓名（SJC 官网笔误 الفردان→الرقدان）、085 姓名张冠李戴（صلاح خورشيد 系另一获刑者）、004/032/053/054/088 任期与法令号、036 法令号、041 姓名中间段、073 家族名、089 姓名中间段、P021 政党归属等，均已回写组织画像与清单并附勘误注记
- **P4 发现牵动组织画像修正 15+ 处**（GOV-004/009/011/012/015/018/019/022/024/025、PARTY-007 等）

## 四、已知边界与遗留复查项

1. **AOU（阿拉伯美国大学）扎伊德同名消歧**：P3 期间标记的复查项，建议后续针对 output/kw/2026-10-03/orgs/KW-ACAD-00*.json 复核
2. **000382 穆泰里**：其「科威特大学教法教授」身份为单一来源+背景高度吻合的**推定归并**，已在该档案 notes 明确标注未经同源确认
3. **人物完整度 <50 的 61 份**：集中于司法系（科威特法官不公开个人信息）与低曝光政团人物，属公开资料客观边界；如需提分可针对 40-49 区间做定向补采
4. **头像缺失 182 人**：法官系、低曝光政团人物、官网 JS 拦截（Warba/Zain/ABK 等）——客观无法获取
5. **cross-ref 158 warnings**：见上文第二节，属范围裁剪预期项

## 五、索引与产物清单

- `orgs/_index.json`（109 profiles，avg=90）
- `persons/_index.json`（256 persons，avg=60）
- `_name_index.json`（姓名→ID 索引，5937 条）
- `id_registry.json`（组织+人物注册表；person_counters KW-PERSON=408+）
- `_p5_validation_strict.txt` / `_p5_validation_crossref.txt`（本轮校验存档）
- `_qc_p4_chinese.py` / `_qc_avatar_batches.json` / `_qc_fix_list.json`（质检与补弱工作档案）

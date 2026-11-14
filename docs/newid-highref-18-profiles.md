# 18 个高引用新身份补画像记录

日期：2026-11-13

## 已建画像

| 新 ID | 实体 | QID |
|---|---|---|
| JP-FIN-050 | 三井住友银行 | Q2660418 |
| JP-FIN-051 | SMBC日兴证券 | Q17227817 |
| JP-PARTY-010 | 中道改革联合 (Centrist Reform Alliance) | Q137787102 |
| JP-ACAD-031 | 量子科学技术研究开发机构 (QST) | — |
| JP-GOV-867 | 日本学术振兴会 (JSPS) | Q199781 |
| MX-GOV-878 | 联邦区立法议会 | — |
| MX-GOV-896 | 联邦区政府 | — |
| MX-GOV-891 | 韦拉克鲁斯州政府 | — |
| KR-FIN-016 | 新韩金融集团 | Q491325 |
| KR-MEDIA-021 | 中央日报 (JoongAng Ilbo) | Q483903 |
| KR-ACAD-024 | 高丽大学 | Q39997 |
| KR-ACAD-025 | 延世大学 | Q39988 |
| KR-ACAD-026 | KAIST | Q39949 |
| KR-SOE-021 | 韩国水力核电公司 | Q6431646 |
| KR-ACAD-027 | 浦项工科大学 (POSTECH) | Q40018 |
| NZ-GOV-152 | 新西兰商务委员会 | — |
| NZ-GOV-134 | NZ On Air | Q17056081 |
| NZ-GOV-148 | 新西兰民航局 | Q5124421 |

- 18 个画像 `--strict`：**0 error / 0 warning**
- registry：18 个条目 `auto_registered → profiled`，已补 QID
- org index：JP/MX/KR/NZ 各自增加对应条目
- 头像：未创建（`profile: null`）；person 9,000 / org 3,965 不变

## 引用影响

- 18 个新身份覆盖 **146 条引用**
- 审计：
  - work_org 正确指向 59,232 → **59,316**
  - work_org 悬空 6,993 → **6,909**
  - related_org 正确指向 18,180 → **18,234**
  - related_org 悬空 5,924 → **5,862**

## 补画像 backlog 变化

- 403 个 / 405 条引用 → **385 个 / 259 条引用**
- 剩余高引用（≥5 条）：**0**
- 更新文件：`newid_profile_backlog.csv`、`_referenced.csv`、`_highref.csv`

## 关于 OpenAI / Anthropic / SpaceX

它们**不在 403 个新身份里**，也不在 126 个 1 引用项里。它们目前是 US registry 里的冲突/裁剪条目：

| 实体 | registry 条目 | 状态 |
|---|---|---|
| OpenAI | US-CORP-014 | trimmed（owner=Ford） |
| SpaceX | US-CORP-026 | trimmed（owner=Cisco） |
| Anthropic | US-CORP-013 | trimmed（owner=Tesla） |
| xAI | US-CORP-069 | auto_registered，无画像 |
| Starlink/SpaceX | AU-CORP-040/087、CL-CORP-071、KW 自造 ID、PG-CORP-031 | 多国重复注册 |

这些需要单独做“全球科技公司主体归一”，不能从 403 backlog 里处理。

## 126 个 1 引用项

- 没有 OpenAI/Anthropic/SpaceX 这类全球品牌
- 主要是地方政府、法院、大学、区域媒体、银行、协会等
- 其中较知名的区域机构：Bank of Singapore、DSTA、LG Energy Solution（这些引用数≥3，不在 126 内）
- 126 条里可优先看 1 引用但有明确官网/独立法人地位的机构；其余可低优先补建。

回滚：`output/_id_audit/newid_18_profiles_undo.json`

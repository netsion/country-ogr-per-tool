# 全局头像问题清单（Issue Tracker）

> 生成于 2026-11-11，基于 54 个数据集的全量审计（`output/_avatar_audit/`）。
> 状态：`[ ]` 待办 · `[~]` 进行中 · `[x]` 完成 · `[-]` 放弃/不改
> 每完成一项更新状态与"完成记录"。

## 背景速览

- 修复基线数据：`output/_avatar_audit/audit_result.json`（全量明细）、
  `download_candidates.json`（待下载清单）、`report.md`（总报告）
- 已完成的前置修复（2026-11-11）：目录统一 + 命名规范化（详见文末"前置已完成"）

---

## 问题列表（按建议执行顺序）

### A-1 [x] wiki File: 描述页死链修复（87 条）✅ 2026-11-11
- **现状**：`source_url` 是 `commons.wikimedia.org/wiki/File:...` 描述页，不是图片直链
- **方案**：wiki API `iiurlwidth=250` 解析直链 + 下载 + 回写 profile
- **完成记录**：`scripts_tmp/fix_avatar_links.py` 全量执行。人物侧 78/87 修复；剩余 9 条在 **orgs**（归入 A-1-org）。代理 7897，429 限流用长退避（两轮跑完全清）
- **验证**：终审计 wiki_file_page 87→9（余 9 条全在 orgs）；545 个 thumb 直链的 local 文件全数真实存在（含魔数校验）

### A-1-org [x] org 侧 wiki File: 死链（9 条）✅ 2026-11-11
- **完成记录**：`scripts_tmp/fix_org_avatar_links.py`——8 修复（解析 250px 直链 + 下载至 `photos/<ORG-ID>.<ext>` + 回写），BN-MEDIA-004 置 null（源文件为 PDF 非图片）。8/8 文件魔数验证为真图（PNG/JPEG）
- **验证**：终审计 wiki_file_page 清零

### A-2 [x] QID 页面当头像源（343 条）✅ 2026-11-11
- **现状**：`source_url` 是 `wikidata.org/wiki/Qxxxx` 页面
- **分布**：ng:200, tw:99, id:41, kg:1, my:1, qa:1
- **完成记录**：人物侧 340/343 处置完毕——有 P18 的解析直链+下载（123 张），无 P18 的 source_url 置 null（217 条，QID 页非合法头像源）；剩余 3 条在 **orgs**（KG-INTL-004、MY-ACAD-013、QA-GOV-015，归入 A-2-org）
- **验证**：终审计 qid_page 343→3（余 3 条全在 orgs）

### A-2-org [x] org 侧 QID 页（3 条）✅ 2026-11-11
- **完成记录**：同一脚本——查 P154（logo）→ P18 兜底；KG-INTL-004、MY-ACAD-013、QA-GOV-015 均无 P154/P18，source_url 置 null
- **验证**：终审计 qid_page 清零。**A-1/A-2 全量完结**：bad_url_classes 仅剩 html_page 825 + social_page 49

### A-3 [x] 社交页/API 链接（49 条）✅ 2026-11-11
- **现状**：graph.facebook.com(30)、youtube watch 页(9)、fb/ig/x/li 主页(10) 等
- **完成记录**：`scripts_tmp/fix_social_avatars.py` + 补刀——
  - graph.facebook.com `?type=large` **30 条全部下载成功**（无需 token，8KB JPEG，含 1 个 org：GN-CORP-006），source_url 保留（活的图片 API）+ 写 local_path
  - youtube watch / instagram 帖子页 10 条置 null（网页非图源；MA 9 条 + QA 1 条）
  - fb/ig/x/li 主页、过期 CDN 等其余 9 条在首轮脚本中已置 null
- **验证**：终审计 `social_page` 清零（分类器同步修正：graph.facebook.com/*/picture 认定为直链）；30/30 文件魔数校验为真 JPEG
- **审计分类器修正**：`graph.facebook.com/<name>/picture` 返回真图，归入 `other_direct_image`

### A-4 [x] html_page 非图片链接（825 条）✅ 2026-11-11
- **现状**：URL 无图片扩展名（.aspx 动态图床、Wikipedia 条目页、licdn 等）
- **方案**（四步漏斗，与用户讨论定稿）：
  1. Content-Type 探测 → 真图直接下载；2. wp 条目页 pageimages API；
  3. QID → P18/P154 兜底；4. org og:image（person 不做，避免错抓网站 logo）
- **完成记录**：
  | 步骤 | 救回 | 处置 |
  |---|---|---|
  | 步1 Content-Type 探测（77min） | **105**（.aspx/.ashx/Storage API 真图） | source_url 保留（活图端点）+ local_path |
  | 步2 wp pageimages | **79**（条目头图，org 为主） | source_url → thumb 直链 |
  | 步3 QID P18/P154 | **17** | 同上 |
  | 步4 org og:image | **82**（官网 logo） | source_url → og 图直链 |
  | 步4 清理 | — | 死URL+无图源共 **537** 置 null（86 有本地图仅清 URL、250 person、201 org/page） |
- **合计救回 283 张**（825 的 34%），置 null 537，保留活端点 105
- **验证**：终审计 bad_source_url 825→**105**，且这 105 条全部为步1实测真图端点（无图片后缀的动态图床，有 local_path，审计器误报，属合法保留）；283/283 文件存在+魔数校验
- 脚本：`scripts_tmp/a4_step1_probe.py`、`a4_step23_wiki.py`、`a4_step4_og.py`

### A-5 [x] malformed profile 字段（557 条）✅ 2026-11-11
- **现状**：`profile` 是字符串而非对象。550 条为 org 描述段落（某轮批量 enrichment 的系统性 bug，误把"机构简介"写进头像字段），7 条为裸 logo URL
- **完成记录**：`scripts_tmp/a5_fix_malformed.py`——
  - url_like 7 条 → 转成合法对象 `{"source_url", "local_path"}` 并下载落地（7/7 文件验证：AE×3 + UZ×4 logo）
  - text_like 550 条 → **置 null**。文本经抽样确认均为 `core_business` 的改写摘要（信息已有承接，无丢失）；557 条全文已备份至 `output/_avatar_audit/a5_profile_text_backup.json` 可随时找回
- **防复发**：`validate_schema.py` 的 `validate_org_profile`/`validate_person_profile` 头部新增守卫——profile 非 dict 即 error（非 strict 也报，因属 schema 硬违规）
- **验证**：终审计 malformed_profile **557→0**；BO/CI/TD 三个重灾数据集校验 0 errors（守卫生效不误报）
- 脚本：`scripts_tmp/a5_fix_malformed.py`

### A-6 [x] 统一下载 download_gap（8679 条）✅ 2026-11-12
- **方案落地**：`scripts_tmp/a6_download.py`——双通道轮询（A=28081 图片代理 / B=AnitCloud 7897）+ wikimedia URL 统一转 `Special:FilePath?width=250` API 路由（批量友好，绕开 429）+ 魔数校验 + 幂等 checkpoint + person 优先
- **过程要点**：
  - 开跑即触发 Wikimedia "robot policy" 429（直连 thumb/upload 域被封）→ 切 FilePath API 通道后 25-30/min 稳定
  - 中途修复 thumb URL 拼接 bug 与多语言 wiki（ar 等）文件名转换
  - 一次 Windows 文件锁崩溃（PermissionError）→ 加重试兜底后从磁盘真相同步 state 续跑，零损失
- **完成记录**：person 4815+331 补扫 + org 3873 + 失败复跑 425（捡回 26）三阶段全跑完
- **成果**：全库带本地图档案 4110 → **12945**（person 8967 + org 3978，净增 ~8800 张）；终审计 download_gap 8679→503（**94% 消化**），残 503 为 fbcdn 过期签名/新闻站死链/超时官网站（wikimedia 265 + 各国官网 238），已确认为不可救死链
- **顺手清理**：全库 13034 文件魔数扫描，删除 10 个历史遗留的 HTML/JSON 假图（本轮下载零污染）并悬空引用置 null
- **验证**：磁盘实测 photo 文件 13044→13034（清 10 坏图），随机抽样魔数全过；`local_missing` 32→7
- 脚本：`scripts_tmp/a6_download.py`

### B-1 [x] 剩余命名不规范 ✅ 2026-11-12
- SA-PERSON-000213_shura.png → SA-PERSON-000213.png（重命名+回写）；TH-PERSON-000474 的 PDF 引用置 null；TM-FIN-001 根目录 cbt_200manat.png → photos/TM-FIN-001.png
- **验证**：终审计 bad_naming 清零

### B-2 [x] 悬空引用 ✅ 2026-11-12
- BN×2 / MY×5 指向不存在文件的 local_path 置 null（source_url 保留供未来重下）；TH 的 PDF 引用同上
- **验证**：终审计 local_missing 清零

### B-3 [x] BO-000087 头像冲突 ✅ 2026-11-12
- 两份候选经溯源比对：根目录 217KB 版 **MD5 与 profile 当前 source_url（produccion.gob.bo 官方照）完全一致**；persons 目录 102KB 版为管线早期旧图。判定同人均为 Viviana Mariscal（与 000075 合并的重复建档），无身份风险
- 处置：217KB 版移为 `persons/photos/BO-PERSON-000087.jpg`（与 source_url 严格对应），旧 102KB 备份为 `.old102k.bak`

### B-4 [x] CL `_merged_*.json` 残留（6 个）✅ 2026-11-12
- **处置修正**：核实后发现**不是合并残留，是 renumber 后丢掉主文件名的真实人物档案**（CL-PERSON-000058 等，且 000057 还引用 000058）——不能删
- 恢复为主文件名（rename 去掉 `_merged_` 前缀）+ 照片同步改名 + local_path 回写；6 人：Miguel Fernández González、Vivianne Blanlot、Pedro Varela、Fernando Barros、Fernando Cabrera、Carlos Arrau
- **验证**：终审计 id_mismatch 清零；CL strict 校验 0 errors

### B-5 [x] 杂文件 ✅ 2026-11-12
- 删除 6 个无引用测试文件（jo `_amoush2`/`_test_batran_yt2`、kh 后缀命名、ly `_cNamroush`、us `_shah_try`；cd 的 2 个 dev_* 与 _cand_* 已在假图清理轮删除）

### B-6 [x] 孤儿文件 ✅ 2026-11-12
- 用重建的引用集精确核算：**真孤儿仅 84 个**（审计器的 12946 是全量文件清单口径，非真孤儿数）
- 82 个为历史 merge/renumber 时实体已删的遗留图 + 2 个超期版本，全部**移入回收站** `output/_avatar_audit/_orphan_trash/`（未硬删，确认无误后可清空）
- TM-FIN-001 logo 从中捞回（ref 曾是坏路径 `output/tm/...` 导致被误判孤儿）

---

## 终局状态（2026-11-12 全部收官）

### M-2 [x] 老布局散图处置（git 退跟踪 + 20 张回收）✅ 2026-11-12
- **背景**：photos 目录规范化**之前**的旧布局遗留——678 张头像裸放在 `persons/` 目录（老 `local_path` 引用已丢）+ 32 张 `_dg_frame_*`/`_azzi_*` 测试残图，均被 git 跟踪
- **核查**：678 张中 658 张为冗余（minio-store 已有同 ID 新图），**20 张为唯一照片**（AU×4、CA×1、JP×1、MX×11、SG×3——这些档案此前无任何头像），魔数验证全真图
- **处置**：
  - 20 张唯一照片 → 迁入 minio-store + 回写档案（20/20 档案 local_path/minio_path 同步验证通过）
  - 658 张冗余 → `git rm --cached`（磁盘保留，git 退跟踪）
  - 32 张测试残图 → 删文件 + 退跟踪
- **待办提醒**：**20 张新对象尚未上传 MinIO**——下次生产上传时用原脚本跑一遍即可增量补传（state 无记录会自动识别）
- **git 状态**：图片跟踪数 4339 → 3649（余量全部为待提交的 D 删除态；提交后归零）；minio-store 12946 → **12966**

### M-1 [x] MinIO 镜像迁移 + minio_path 回填 ✅ 2026-11-12
- **背景**：minio_path 初版不含桶名；用户确认新布局 `{桶=default}/{popular-person-profile|popular-org-profile}/{cc}/<ID>.<ext>`（无前导 `/`）
- **执行**：`scripts_tmp/migrate_to_minio_store.py`——12946 张图全部迁入项目根 `minio-store/`（人物 8981 + 组织 3965），同步回写两个路径字段：
  - `local_path` = `minio-store/default/<folder>/<cc>/<ID>.<ext>`（**新语义：相对项目根**）
  - `minio_path` = `default/<folder>/<cc>/<ID>.<ext>`（MinIO 对象 key）
- **连带更新**：两个 schema 的 local_path/minio_path 描述、person_collection_rules.md 头像节、avatar_audit.py 路径解析（兼容 minio-store 布局）
- **清理**：103 个空 legacy photos 目录删除；散件（bn 根目录 1 图 + cd/dz 的 photos/_tmp 临时目录）移入回收站；旧布局图片在回收站外**清零**
- **验证**：minio-store 12946 文件、随机 15/15 魔数通过、12946/12946 local_path 全部可解析、BO/CL strict 校验 0 errors
- **生产上传对账（2026-11-12 终局）**：离线包（纯 stdlib SigV4，py3.6）在生产执行完毕，`--verify` 结果 **ok=12946 missing=0 size-diff=0 / 12946**——桶内对象与本地清单、数据集 minio_path 字段三方严格一致，关单
- **备注**：`a6_download.py` 已于同日改造为直接写 minio-store 布局（下载成功即落 `minio-store/default/{folder}/{cc}/<ID>.<ext>` 并同时回写 local_path + minio_path，单测验证通过）；`backfill_minio_path.py` 旧版已过时，由 migrate 脚本统一维护

剩余三类均为**不可再修复的终态**，非问题：

| 类别 | 数量 | 说明 |
|---|---|---|
| no_profile | 6625 | 该人物/组织本就无任何可用头像源（null 合法态） |
| download_gap | 503 | 死链（fbcdn 过期签名、下线新闻站等），双通道全试过 |
| bad_source_url | 108 | 106 个活图端点（.aspx 动态图床等，有 local_path，审计误报）+ 2 个已知遗留 |

**成果总账**：全库带本地头像 4110 → **12946**（person 8967 + org 3979）；
bad_naming / id_mismatch / local_missing / malformed_profile / wiki_file_page / qid_page 全部清零。

---

## 前置已完成（2026-11-11，本清单的基线）

| 动作 | 数量 |
|---|---|
| 照片统一移入 `国家/日期/persons/photos/` + 文件名规范为标准 ID 大写 | 4203 |
| persons JSON local_path 回写 | 4107 |
| MA `local:photos/...` 伪协议修复（→local_path, source_url=null） | 18 |
| KG 指向 .json 的坏引用置 null | 7 |
| 数据集根目录散图捞回 | 2 |
| 同名同内容重复清理 | 51 |
| wrong_location 清零（4104→0）；BO strict 校验 0 错误 | — |

## 规范依据

- 字段规范：`.agents/skills/country-org-collector/person_profile_schema.json` 与
  `org_profile_schema.json` 的 `profile`（source_url / local_path / minio_path）
- 来源口径：`.agents/skills/country-org-collector/person_collection_rules.md`「头像字段（profile）」节

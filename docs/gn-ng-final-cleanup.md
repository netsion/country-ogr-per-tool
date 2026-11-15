# GN/NG 采集收尾报告（2026-11-15）

几内亚、尼日利亚采集流程结束后的一轮全面清理，直接执行到底。

## 数据面

| 目录 | 人物 | 组织 |
|---|---:|---:|
| gn/2026-11-10 | 131 | 134 |
| ng/2026-11-10 | 430（含 238 骨架） | 149 |
| ng/2026-07-29 | 200 | 141 |

两个 NG 目录 **0 个 ID 重叠**，是互补数据集（旧目录为早期批次）。

## 1. 社交/头像字段规范

- 全量字段审计（platform 枚举、source 类型、路径规范、空字符串 ID）：**0 问题**
- 头像一致性：
  - NG-1110：8 个 local_path 指向不存在文件 → 1 个补下载成功（YouTube 缩略图），7 个置空（无 source_url 不可恢复）
  - GN：120 个"有 source_url 无本地文件" → **89 个下载成功**并写入 `minio-store/default/popular-*-profile/gn/`，31 个失败保留 source_url
  - 最终全库 dead-path = 0

## 2. 中文规范

- NG-0729 org `name_zh` 空缺：从 NG-1110 同实体回填 64 个 + 手工映射表 42 个（大学/媒体/航司/政党/企业）→ **0 剩余**
- 语言规范警告仅剩品牌豁免类（Paystack、Airtel 等），符合 2026-11-12 语言政策
- `name_zh` 拉丁首字母（T.B.约书亚、阿米纳·J·穆罕默德）为政策豁免项

## 3. Strict 校验修复

- 机械修复 802 处 schema 外字段（`org_id_note`→`note`、NG-0729 的 `importance_*`、org `description/brief`、key_people `person_name/source/wikidata_qid`）
- key_people 悬空 ID：NG 329 条 → 91 条匹配到既有画像 + **238 个骨架画像创建**（35 分，待补全）；GN 全部匹配，0 创建
- 骨架画像补 `gender: unknown` 修复 schema 必填
- **最终：三个目录 strict 全部 0 errors**（GN 985 / NG-1110 1476 / NG-0729 196 warnings 为 dept_id 空、related null 等可接受项）

## 4. ID 关联

- 按名称匹配器逐条复核：
  - GN 152 条错配置空 → wrong = 0
  - NG-1110 35 条置空 → wrong = 0
  - NG-0729 3 条跨国目录改链（ThisDay→NG-MEDIA-007@1110、Dangote→NG-CORP-001@1110、Channels TV→NG-MEDIA-002@1110）→ wrong = 0
- registry 碰撞：三目录逐 ID 检查 **0 碰撞**
- 重复 QID：NG 双目录间 21 组同人不同 ID → 保留丰富副本 QID，清空另一份
- 名称索引三目录全部重建

## 5. 提交

- `a15e21e3c` data: GN/NG collection-final cleanup
- `91946f4e5` data+docs: TW batch3-5 + 索引刷新
- `5b66b132e` tools: GN/NG + TW 工作脚本
- 工作区剩余：仅 `scripts/` 下 21 个历史零散脚本（people-lite 导出等，待决：入库或删除）

## 后续可选项

- NG 238 个骨架画像的正式补全（P4 深度调查）
- GN 31 个下载失败头像的换源重试
- `scripts/` 21 个脚本的清理决策
- 远端 push

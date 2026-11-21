# 埃及（EG）采集收尾报告（2026-11-21）

按 dataset-finalization-sop.md 执行，流程与 GN/NG/TG/SD 一致。

## 数据面

- `output/eg/2026-11-16`：人物 208+220 骨架=428、组织 190
- 采集完成时 strict 已 0 errors（采集期质量好）

## 各项处理

### 1. 字段规范
- 采集期即合规，无需机械修复

### 2. ID 关联
- 幽灵 ID（不在 registry/画像）置空 **566**
- 错误引用（名称不匹配画像）置空 **26**
- key_people 悬空 230 → 链接既有画像 10 + **骨架画像 220**（含 gender=unknown、反向 work_experience 关联）
- registry 碰撞 0、重复 QID 0

### 3. 头像
- **下载成功 107 张**（28081 代理为主）→ 磁盘 254 张
- 已有 147 张保持不变
- 下载失败 45（源站问题）、非图片响应 2、无源 30
- 最终：person avatar_ok 147+新增、org avatar 全量处理

### 4. collection_meta.quotes
- 36 个档案缺 quotes → 补最小合规引用对象

### 5. 收尾验证
- **strict 0 errors**（618 文件，含 220 个新骨架）
- 名称索引重建 6,728 条
- 剩余 warnings：related description-only（588 条，可接受）等

## 提交

- `ec5bfce47` data: EG final cleanup per SOP
- 已推送远端

## 骨架画像说明

220 个骨架画像（completeness 35）由组织 key_people 反向生成，含姓名/职务/所属组织关联。与 NG（238）、TG（1）、GN 模式一致，待后续 P4 深度补全轮统一 enrichment。

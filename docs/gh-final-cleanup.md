# 加纳（GH）采集收尾报告（2026-11-23）

按 dataset-finalization-sop.md 执行，流程与 GN/NG/TG/SD/EG 一致。

## 数据面

- `output/gh/2026-11-17`：人物 204+232 骨架=436、组织 96
- 采集完成时 strict 已 0 errors（采集期质量好）

## 各项处理

### 1. 字段规范
- 采集期即合规，无需机械修复

### 2. 中文规范
- name_zh 100% 完备，0 缺失

### 3. ID 关联
- 幽灵 ID 置空 **663**、错链置空 **14**
- key_people 悬空 240 → 链接既有画像 8 + **骨架画像 232**（含 gender=unknown）
- registry 碰撞 0、重复 QID 0

### 4. 头像
- **下载成功 118 张**（28081 代理为主）→ 磁盘 145 张
- 已有 27 张保持不变
- 下载失败 61（源站问题）、死路径置空 58、非图片响应 5、无源 1

### 5. quotes
- 24 个缺失档案补最小合规引用

### 6. 收尾验证
- **strict 0 errors**（532 文件，含 232 个新骨架）
- 名称索引重建 5,300 条
- registry 碰撞 0、重复 QID 0

## 提交

- `d95dbb325` data: GH final cleanup per SOP
- 已推送远端

## 骨架画像说明

232 个骨架画像（completeness 35）由组织 key_people 反向生成。与 NG（238）、EG（220）模式一致，待后续 P4 深度补全轮统一 enrichment。

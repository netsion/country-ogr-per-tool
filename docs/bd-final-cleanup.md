# 孟加拉国（BD / Bangladesh）采集收尾报告（2026-11-24）

按 dataset-finalization-sop.md 执行，流程与 GN/NG/TG/SD/EG/GH/MA/ML 一致。

## 数据面

- `output/bd/2026-11-23`：人物 204+607 骨架=811、组织 147
- 采集完成时 strict 已 0 errors

## 各项处理

### 1. 字段规范
- 采集期即合规，无需机械修复（PHASE1 = 0）

### 2. 中文规范
- name_zh 100% 完备，0 缺失

### 3. ID 关联
- 幽灵 ID 置空 **580**
- 错链置空 **12**
- key_people 两轮链接：**171**（首轮 13 + 次轮 158）
- **骨架画像 607**（首轮 147 + 次轮 460，含 gender=unknown）
- registry 碰撞 0、重复 QID 0

### 4. 头像
- 已有 178 张在盘
- 本轮未新增下载（BD 源站多不可达）
- 最终 178 张在盘，34 个引用缺失但已置空

### 5. 收尾验证
- **strict 0 errors**（922 文件，含 607 个新骨架）
- 名称索引重建 5,759 条
- registry 碰撞 0、重复 QID 0

## 提交

- `abd45f56e` data: BD final cleanup per SOP
- 已推送远端

## 骨架画像说明

607 个骨架画像（completeness 35）由组织 key_people 反向生成，含姓名/职务/所属组织反向关联。数量较多与孟加拉政治人物密度有关。与 NG（238）、EG（220）、GH（232）、MA（270）、ML（57）合计骨架画像约 1,617 个，待后续 P4 深度补全轮统一 enrichment。

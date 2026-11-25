# 尼日尔（NE / Niger）采集收尾报告（2026-11-25）

按 dataset-finalization-sop.md 执行，流程与 GN/NG/TG/SD/EG/GH/MA/ML/BD 一致。

## 数据面

- `output/ne/2026-11-22`：人物 122、组织 57
- 无 `.inflight` 标记（采集已结束）

## 各项处理

### 1. 字段规范（PHASE 1）
- 采集期即合规，0 处修复

### 2. 中文规范
- name_zh 100% 完备，0 缺失

### 3. ID 关联（PHASE 4）
- 幽灵 ID 置空 **0**
- 错链置空 **18**（已逐条人工核对：主要模式是各部会/机构错挂到 NE-GOV-010 财政部——高教部、内政部、农业部；另有 Canal 3 Bénin ↔ Canal 3 Niger 跨国混淆、Airtel Africa plc ↔ Airtel Niger 母子公司混淆、共和国卫队 ↔ 国家卫队混用）
- registered-no-profile **74** 条按验收口径保留
- key_people 225 条**采集期即全部链接**（0 悬空），本轮无骨架生成

### 4. 头像
- **下载成功 82 张**（28081 图片代理）
- 已在盘 21 张；死路径 1 处置空
- 无源 10、下载失败 4、非图片响应 3
- 最终 103 张在盘，死路径 0

### 5. 收尾验证
- **strict 0 errors**（179 文件）
- 名称索引重建 2,217 条（1,081 org + 1,136 person）
- registry 碰撞 0、重复 QID 0

## 提交

- data: NE final cleanup per SOP
- 已推送远端

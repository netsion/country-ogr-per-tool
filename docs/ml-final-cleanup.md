# 马里（ML / Mali）采集收尾报告（2026-11-23）

> 勘误：此前报告中 `ma/2026-10-05`（MA 目录）实为**摩洛哥**数据集（country_iso3=MAR）。
> 真正的马里数据集是 `ml/2026-11-18`（country_iso3=MLI），本轮对象是它。

## 数据面

- `output/ml/2026-11-18`：人物 181+57 骨架=238、组织 74
- 无 `.inflight` 标记（采集已结束）

## 各项处理

### 1. 字段规范（PHASE 1）
- 28 处 schema 外字段修复（`org_id_note`→`note` 等）

### 2. ID 关联（PHASE 4）
- 幽灵 ID（不在 registry/画像）置空 **99**
- 错链（名称不匹配画像）置空 **26**
- registered-no-profile 保留（符合验收口径）

### 3. key_people 链接 + 骨架画像
- 链接既有画像 **3**
- 创建骨架画像 **57**（completeness 35，含 name/nationality=MLI/反向 work_experience）

### 4. 字段修正
- `nationality`: MLI → **ML**（ISO3166-1 alpha-2 应为两位，57 个骨架统一修正）

### 5. 验证
- **strict 0 errors**（312 文件）
- 名称索引重建 3,114 条
- registry 碰撞 0、重复 QID 0

## 提交

- `ffb84ee05` data: ML final cleanup per SOP
- 已推送远端

## 勘误说明

前一轮 `a661b86b6` 报告标题写的是"MA (Mali)"，实际处理的是 `ma/2026-10-05` = **摩洛哥**数据集（按目录 MA 代码误判了国名）。该轮对摩洛哥数据的清理本身是有效的（幽灵 1,079 等），只是国名标注错误。特此更正：

| 目录 | 国家 | 状态 |
|---|---|---|
| `ma/2026-10-05` | 摩洛哥（Morocco） | 已完成 SOP 收尾 |
| `ml/2026-11-18` | **马里（Mali）** | 本轮完成 SOP 收尾 |

后续若需处理真正的马里（ML）数据，本轮已覆盖。

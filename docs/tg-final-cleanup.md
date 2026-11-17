# 多哥（TG）采集收尾报告（2026-11-18）

多哥采集结束后的一轮全面清理，参照 GN/NG 流程执行到底。

## 数据面

- `output/tg/2026-11-16`：人物 205（含 1 骨架）、组织 88
- 全部 `name_zh` 完备，0 缺失

## 1. 社交/头像字段规范

- 机械 strict 修复：4 处 schema 外字段
- 头像处理：
  - **下载成功 80 张** → `minio-store/default/popular-*-profile/tg/`
  - 下载失败 48 张（source_url 死链/非图片，保留 source_url 待换源）
  - 死路径置空 17 个（local_path 指向不存在文件）
- 最终：profile 172 个、本地文件 83 个、待换源 65 个

## 2. 中文规范

- 全部 `name_zh` 完备（0 缺失）
- 语言警告仅剩品牌豁免项 + 拉丁首字母中缀豁免项（如"拉塔·D·格纳马"），符合语言政策

## 3. ID 关联

- **本轮有两次修正**：
  1. 首次自动清理误把"已注册但无画像"的 493 个引用也置空了——这违反验收口径（无画像可接受），已用 git diff 逐条**恢复**
  2. 重新按正确规则执行：只置空名称不匹配画像的错误引用 16 条 + 幽灵 ID（不在任何 registry）596 条
- 最终：filled 2,080 / **wrong 0** / registered-no-profile 保留 477（符合验收口径）
- registry 碰撞：**0**
- 重复 QID：**0**
- key_people 最后 1 个悬空（TG-FIN-006 的 Ahmed Omar El Hadi）→ 创建骨架画像 `TG-PERSON-000609`

## 4. 最终状态

- **strict 校验：0 errors**（623 warnings 为 dept_id 空、related null 等可接受项）
- 名称索引已重建：4,798 条
- 已提交 `845ee00d2` 并推送远端；随后的 TW b9 增量也已提交推送（`9b765dd5d`）

## 过程教训（已记录）

自动清理脚本必须区分"错误引用"（置空）与"注册无画像引用"（保留）——本次第一版脚本把 dangling 全部置空，靠 git diff 全量恢复。后续脚本应默认保留 registered_no_profile 类。

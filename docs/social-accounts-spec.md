# 社交账号（social_accounts）采集与规范 v2 — 外部交付对照

> 适用：orgs/*.json 与 persons/*.json 的 `social_accounts[]` 字段
> 沉淀自 2026-11 全库三轮改造（字段规范 v2 → user_id 回填 → GN/NG/TG 收尾）

## 字段结构

| 字段 | 类型 | 规范 |
|---|---|---|
| `platform` | string | 23 值小写枚举（见下表）；`twitter_x` 已废除，一律 `twitter` |
| `account_name` | string | 页面显示名或 handle |
| `url` | string | 页面完整 URL |
| `nickname` / `username` / `user_id` | string/null | 采集阶段可 null，由专用 xlsx 回填流程填充 |
| `source` | int/null | 平台数字编码（见下表）；无编码的平台为 null |
| `source_note` | string/null | 来源说明（长文本） |

## platform 枚举（23 值）与 source 编码对照

| platform | source 编码 | 备注 |
|---|---:|---|
| twitter | 3 | X/Twitter 统一用此值 |
| facebook | 6 | |
| instagram | 8 | |
| youtube | 9 | |
| odnoklassniki | 10 | |
| vkontakte | 11 | |
| weibo | 14 | |
| reddit | 15 | |
| tumblr | 16 | |
| linkedin | 17 | LinkedIn 不支持自动解析，人工采集 |
| telegram | 19 | |
| whatsapp | 20 | |
| line | 21 | |
| wechat | 23 | |
| threads | 24 | |
| snapchat | 25 | |
| tiktok | 29 | |
| github / gitlab / medium / substack / mastodon / other | null | 无编码平台 |

## 常见脏值对照

| 脏值 | 修法 |
|---|---|
| `"twitter_x"` / `"X (Twitter)"` / `"X"` | → `twitter` |
| `"Facebook"` / `"Naver Blog"` 等大写或自创 | → 小写枚举值，无法映射的 → `other` |
| `"妻子"` 等中文名出现在 platform | → 枚举值；这是 family/relationship 字段串位 |
| source 为字符串数字 | → 转 int |

## 验收口径

1. platform 全部在枚举内、全小写
2. source 类型正确（int 或 null）
3. nickname/username/user_id 允许 null（由回填流程负责）
4. 无 `twitter_x` 残留

## 已知限制（交付给外部系统时需说明）

- **LinkedIn**：平台禁止自动解析，账号由人工收集，覆盖率低于其他平台
- **nickname/username/user_id**：仅 Twitter/Facebook/Instagram/YouTube/Telegram 五平台有回填数据；其余平台为 null
- **死链账号**：抽样发现的死链/改名账号未从数据中移除（保留原文供下游判断），仅更新了 follower 数为 null

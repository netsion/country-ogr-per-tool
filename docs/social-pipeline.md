# 社交账号管线 SOP（social_accounts）

> 沉淀自 2026-11-12 social_accounts v2 改造。字段定义以两个 schema 为准
> （person/org_profile_schema.json 的 `$defs.social_account`）；枚举与
> source 码表见 skill 的 `enum_reference.md`。

## 字段结构（8 字段，additionalProperties:false）

```json
{
  "platform":   "twitter",                       // 23 值小写枚举
  "account_name": "@Rodrigo_PazP",               // 显示名或 handle（采集时写）
  "url":        "https://x.com/Rodrigo_PazP",    // 必填 URI
  "source":     3,                               // 数字平台码（映射表见 enum_reference）
  "source_note": "X平台检索确认（认证账号…）",     // 来源说明（长文本）
  "nickname":   "Rodrigo Paz Pereira",           // 平台昵称（可由后续流程回填）
  "username":   "Rodrigo_PazP",                  // @handle（可由后续流程回填）
  "user_id":    "895418197482106881"             // 平台ID（含 fb#RHINO# 等前缀）
}
```

- `platform` 一律小写；**twitter_x 已废除**，X/Twitter 全归 `twitter`
- `source` 与 platform 自动对应：twitter=3 facebook=6 instagram=8 youtube=9
  odnoklassniki=10 vkontakte=11 weibo=14 reddit=15 tumblr=16 linkedin=17
  telegram=19 whatsapp=20 line=21 wechat=23 threads=24 snapchat=25 tiktok=29；
  无码平台（mastodon/github/gitlab/medium/substack/other）→ null
- 非社交链接（官网/邮箱）放 `contacts[]`，不得塞进 social_accounts
- 三条守卫（validator 内，error 级）：platform 枚举 / source 码集合 / extra keys

## 采集阶段规则

- `nickname/username/user_id` **可不写**（留给解析流程回填），其余五字段按采集结果写
- URL 必须是账号主页，不是搜索页/分享页；无 URL 的账号条目不写
- 同一实体同一账号只写一条（按归一化 URL 去重）

## 外部解析表回填流程（xlsx → 数据）

1. 解析表主键用「链接」列，与 `social_accounts[].url` 做 URL join
2. **URL 归一化必须带域名别名**（`scripts_tmp/social_migrate.py` 的 `norm_url`）：
   `twitter.com→x.com`、`threads.net→threads.com`、`fb.com/m.facebook.com/web.facebook.com→facebook.com`、
   `m.instagram.com→instagram.com`、去 scheme/www/尾斜杠/URL 解码
3. 匹配优先级：**URL 精确 > (实体ID, 平台) + 空字段条目兜底**
   —— 同一实体同平台多账号时，严禁只按 (实体, 平台) 匹配（会串号）
4. 回填只填空字段；已有值不同记 conflict 不覆盖（人工裁决）
5. 脚本链：
   | 脚本 | 用途 |
   |---|---|
   | `scripts_tmp/social_audit.py` | 全库审计（platform 脏值/extra keys/URL 问题） |
   | `scripts_tmp/social_migrate.py` | 主迁移（归一化 + source 码 + 大表 URL join + 脏值处置），幂等 |
   | `scripts_tmp/xlsx_match_report.py` | 反向核对（xlsx 行是否都在库里） |
   | `scripts_tmp/export_true_misses.py` | 导出 xlsx 漏网清单（交解析侧补） |
   | `scripts_tmp/merge_userid_supplement.py` | 补充表回填（实体ID+URL 优先，空条目兜底） |

## 当前基线（2026-11-12）

- 全库 38,677 条；platform 脏值 0、extra keys 0、source 全部码值或 null
- 大表匹配 25,379 条（72,525 个字段值）；125 条漏网已由用户补充表回填（245 字段）
- **已知缺口（政策/待办）**：
  - linkedin 7,403 条无 identity 数据（解析不支持，用户确认暂不处理）
  - gn（几内亚）、iq（伊拉克）两国解析表未覆盖
  - xlsx 平台级缺口：FB/TW/IG/YT/TT/Threads 六平台外全缺（other/telegram/weibo 等）

## 防复发

- 新数据集的 platform 只允许枚举值；历史脏值（Facebook/twitter_x 等）由 validator
  `PLATFORM_NORMALIZE` 在 `--fix` 时自动清洗
- 迁移/回填脚本全部幂等，可重复执行；执行前先跑全库备份到
  `output/_social_audit/social_backup.json`（已 gitignore）

# 下游同步：头像（profile）与社交账号（social_accounts）字段变更说明

> 变更日期：2026-11-12 · 上游：country-org-collector 数据集（54+ 国家）
> 受影响字段：`profile`、`social_accounts`、`contacts`
> 如需旧值回滚：头像图集 `output/_avatar_audit/`、社交快照 `output/_social_audit/social_backup.json`

---

## 一、`profile`（头像/Logo）——**有破坏性变更**

### 字段对比

| 字段 | 变更前 | 变更后 | 兼容性 |
|---|---|---|---|
| `source_url` | string \| null，可为 **File: 描述页 / Wikidata QID 页 / 社交主页** | string \| null，**只允许图片直链**（wikimedia thumb / 官网图片端点等） | ⚠️ 旧坏值已批量清洗，消费方若做了“非直链降级”逻辑可简化 |
| `local_path` | string \| null，**相对数据集目录**（如 `photos/BO-PERSON-000087.jpg`、`persons/photos/...`） | string \| null，**相对项目根**（如 `minio-store/default/popular-person-profile/bo/BO-PERSON-000087.jpg`） | 🔴 **破坏**：按旧口径解析会 404 |
| `minio_path` | —（不存在） | string \| null，MinIO 对象 key（如 `default/popular-person-profile/bo/BO-PERSON-000087.jpg`，**无前导斜杠**） | 🆕 新增，推荐下游改用此字段 |
| `profile` 类型 | 允许历史脏数据为**字符串**（描述文本/裸 URL） | **只能是对象或 null**（校验器 error 级拦截） | 🔴 旧版容错代码可移除；若直接 `profile.source_url` 访问需先判型 |

### 图片存储位置

| 项 | 变更前 | 变更后 |
|---|---|---|
| 存储 | 散落在 `output/<cc>/<date>/photos/`、`persons/photos/`（并提交进 git） | 统一在 **MinIO 桶 `default`**，本地镜像 `minio-store/`（不进 git） |
| 对象 key | — | `{bucket=default}/{popular-person-profile\|popular-org-profile}/{cc}/<ID>.<ext>` |
| 目录结构 | 两种以上并存 | 人物 `popular-person-profile/{cc}/`；组织 `popular-org-profile/{cc}/` |

### 下游需要做什么

1. **取图优先读 `minio_path`**：`GET {MINIO_ENDPOINT}/{bucket}/{key}`，bucket=`default`。
2. 若仍用 `local_path`：改为**相对项目根**解析（不再是相对数据集目录）。
3. `source_url` 可为 null（无合法图源）；`local_path`/`minio_path` 也可为 null（无图）。
4. 覆盖率参考（2026-11-12）：人物 9,001/17,833（50%）、组织 3,965/6,200（63%）；其余为确实无头像源（`no_profile`）或死链（503 条），非数据缺失。MinIO 桶内 12,946 个对象已与 `minio_path` 对账通过（ok=12946 / missing=0 / size-diff=0），另有 20 个后补对象（M-2 回收头像）经增量包补传。

---

## 二、`social_accounts`（社交账号）——**有破坏性变更**

### 单条结构对比

| 字段 | 变更前 | 变更后 | 兼容性 |
|---|---|---|---|
| `platform` | 17 值枚举，**含 `twitter_x`**，实际数据混入 `Facebook/X (Twitter)/Blog/website` 等脏值 | **23 值全小写枚举**（移除 `twitter_x`，新增 whatsapp/line/snapchat/tumblr/odnoklassniki/vkontakte/reddit） | 🔴 **破坏**：`twitter_x` → `twitter`；`platform == "twitter_x"` 的判断会失效 |
| `account_name` | string \| null | 不变 | ✅ |
| `url` | string（必填） | 不变（38 条无 URL 条目已删除，URL 统一补 scheme、去空格） | ✅ |
| `source` | string \| null —— **来源说明长文本** | **integer \| null —— 平台数字编码**（见码表） | 🔴 **破坏**：类型与语义都变了 |
| `source_note` | —（原 `source` 的内容） | string \| null —— 来源说明长文本（原 `source` 原样迁移） | 🆕 读“来源说明”改读这个字段 |
| `nickname` | —（部分历史数据私加过，已清理） | string \| null —— 平台昵称 | 🆕 新增 |
| `username` | —（同上） | string \| null —— 平台 @handle | 🆕 新增 |
| `user_id` | —（同上） | string \| null —— 平台账号 ID（含 `fb#RHINO#`、`youtube#UC...` 等前缀） | 🆕 新增 |
| 其他字段 | 历史私加 `verified/followers/description/notes/handle/account_id/handle_or_url/account/follower_count` | **一律移除**（按业务方要求丢弃，业务方另有存储） | 🔴 若有消费方读这些，需要停用 |

### `source` 数字码表（platform → code）

| platform | code | platform | code | platform | code |
|---|---|---|---|---|---|
| twitter | 3 | facebook | 6 | instagram | 8 |
| youtube | 9 | odnoklassniki | 10 | vkontakte | 11 |
| weibo | 14 | reddit | 15 | tumblr | 16 |
| linkedin | 17 | telegram | 19 | whatsapp | 20 |
| line | 21 | wechat | 23 | threads | 24 |
| snapchat | 25 | tiktok | 29 | | |

> `mastodon/github/gitlab/medium/substack/other` 无编码，`source = null`。
> （`fb#RHINO#`、`telegram#` 等平台前缀串属 user_id 体系，本期未启用。）

### 数据清洗结果（消费方对账用）

| 项 | 数量 |
|---|---|
| 总条目 | 38,677 |
| platform 归一（含 283 条按 URL 域名纠错） | 7,734 条，现零脏值 |
| `source` → `source_note` 改名迁移 | 37,242 条 |
| 数字 `source` 回填 | 36,696 条（其余 1,981 条为无码平台 → null） |
| 删除无 URL 条目 / 同实体重复去重 | 38 / 13 条 |
| 官网/邮箱类误入（platform=website 等）迁移至 `contacts[]`（type=website/email） | 46 条 |
| `nickname / username / user_id` 回填 | 22,310 / 25,013 / 25,480 条 |

### 下游需要做什么

1. **消费 provenance**：`source`（字符串来源说明）→ 改读 **`source_note`**；新 `source` 是数字码（可直接用于平台枚举映射）。
2. **平台判断**：`twitter_x` 全部改为 `twitter`；枚举表以 `enum_reference.md` 为准（23 值）。
3. **新字段可空**：`nickname/username/user_id` 为 null 时不要当错误处理；`user_id` 是字符串（可能带平台前缀）。
4. **contacts 增量**：部分原 social 条目（官网/邮箱）已迁到 `contacts[]`，如做社交统计需排除。
5. **已知缺口**（数据状态，非接口问题）：linkedin 7,403 条无 identity 数据（解析不支持）；gn（几内亚）/ iq（伊拉克）两国解析表未覆盖。

---

## 三、校验器行为变更（推送前自检相关）

`validate_schema.py` 新增 error 级守卫（影响下游若复用该脚本做质量门禁）：

- `profile` 非对象/非 null → **error**
- `social_accounts[].platform` 非 23 值枚举 → **error**（原为部分 warn）
- `social_accounts[].source` 非整数编码/不在码表 → **error**
- `social_accounts[]` 出现 8 字段之外的键 → **error**

---

## 四、最小适配清单（TL;DR）

| 消费方场景 | 必改项 |
|---|---|
| 只读头像 URL | 优先 `minio_path`（桶 `default`）；或 `local_path` 按**项目根**解析 |
| 读社交来源说明 | `source` → **`source_note`** |
| 按平台过滤 | `twitter_x` → **`twitter`** |
| 读粉丝数/认证/账号简介 | 上游已移除，改用业务方自有存储 |
| 依赖 git 内图片 | 图片已移出 git，改从 MinIO 取（`minio_path` 即 key 清单） |

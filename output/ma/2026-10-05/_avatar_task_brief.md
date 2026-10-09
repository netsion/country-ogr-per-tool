# P4 头像+社交补弱批量任务说明（摩洛哥 2026-10-05）

你将处理一批人物（批次清单见主会话prompt）。对每人执行两项任务，然后逐一验证。

## 任务A：头像收集（每人必做）

1. **Wikidata P18 优先**：若人物有 wikidata_qid，访问
   `https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=<QID>&property=P18&format=json`
   （需代理 `curl --proxy http://127.0.0.1:7890`，加 User-Agent）。有P18则取文件名，
   用 `https://commons.wikimedia.org/wiki/Special:FilePath/<文件名>?width=600` 下载。
2. **无P18或无QID**：按序尝试——官方机构简历页照片、Wikipedia条目信息框图（en/fr/ar.wikipedia REST API `/page/summary/<名>` 取thumbnail）、主流媒体证件照。**宁缺毋滥**：无法确认是本人的图片不用。
3. **下载与校验**：保存为 `output/ma/2026-10-05/photos/<person_id>.jpg`（png保留png后缀）。
   校验：文件≥5KB；`file` 或首字节魔数确认为 JPEG(PNG)。HTML错误页（<5KB或含`<html`）→删除并视为未找到。
4. **写入 profile 字段**：
   ```json
   "profile": {"source_url": "<原始图片页或图片URL>", "local_path": "photos/<person_id>.jpg"}
   ```
5. **合规**：Instagram/Facebook 登录墙后的图不抓；用公开图源。查不到就保持 `profile: null`。

## 任务B：社交账号补弱（仅限清单中 social_count=0 的人）

1. 逐平台定向检索：`"<英文名>" site:linkedin.com`、`site:x.com OR site:twitter.com`、`site:facebook.com`、`site:instagram.com`
2. **采信标准**：姓名吻合+职务/单位吻合（至少两项佐证）；同名不同人一律排除。官方机构账号非个人不算。
3. 命中则追加到 `social_accounts[]`：`{"platform": "<小写枚举>", "account_name": "<账号名>", "url": "<https URL>", "source": "<判断依据，中文>"}`
4. 平台枚举：twitter_x/facebook/instagram/youtube/linkedin/telegram/tiktok/threads/other
5. 找不到就保持空数组，**不得硬凑**。

## 写入与验证（每人做完立即执行）

- 用 Write 工具或临时.py（`json.dump(ensure_ascii=False, indent=2)` + `encoding='utf-8'`）改写整个JSON（读→改→写）。
- 逐人验证：`python D:\claude-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts\validate_schema.py output/ma/2026-10-05 --file persons/<person_id>.json --strict`（--file 用相对路径）。ERRORS→修复→复验到0。
- **只允许改动**：`profile`、`social_accounts`、`social_accounts_note`、`profile_note`。其余字段一律不动。
- 临时文件用完删除。

## 汇报格式

每人一行：`person_id | 头像:成功/未找到(原因) | 社交:新增N个/维持0`，最后汇总批次小计。

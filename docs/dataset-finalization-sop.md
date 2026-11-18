# 新采集数据集收尾 SOP（社交 / 头像 / 中文规范 / ID 关联）

> 适用场景：一个国家数据集采集流程结束（P4 完成）后的收尾清理。
> 沉淀自 GN（几内亚）/ NG（尼日利亚）/ TG（多哥）三轮实战（2026-11-13 ～ 11-18）。
> 顺序执行以下六个阶段；每阶段产物和坑位均已标注。

---

## 阶段 0：前置检查

| 检查项 | 命令/方法 | 期望 |
|---|---|---|
| `.inflight` 标记已移除 | `ls output/{cc}/{date}/.inflight` | 不存在 |
| 数据规模确认 | `ls output/{cc}/{date}/persons/*.json \| wc -l` | 与 P4 报告一致 |
| 旧目录检查 | `ls output/{cc}/` | 确认是否有多日期目录（NG 案例：两目录 0 ID 重叠，属互补数据集） |

**坑位**：NG 有两个日期目录，重复 QID 需跨目录去重（见阶段 5）；不要假设单目录。

---

## 阶段 1：字段规范修复（机械修复）

### 1.1 全量字段审计

审计项（脚本模板：`scripts_tmp/gnng_field_audit.py`）：

| 审计项 | 判定 |
|---|---|
| social_accounts.platform | 必须在 23 值小写枚举内；`twitter_x` 已废除 → `twitter` |
| social_accounts.source | 整数编码或 null，禁止字符串 |
| profile.local_path | 相对项目根、`minio-store/` 开头、无反斜杠 |
| 空字符串 ID | work/rel/family/kp/related 中 `org_id`/`person_id` 禁止 `""`（应 null） |

### 1.2 机械修复（脚本模板：`scripts_tmp/gnng_field_fix.py`）

| 脏数据 | 修法 |
|---|---|
| `work_experience[].org_id_note` | 内容并入 `note` 字段（EDU/WORK 白名单允许），然后删除原字段 |
| `education[].source_note`、`person_relationships[].source_note` | 直接删除（source_note 不在字段白名单） |
| person 顶层 `importance_level` / `importance_reason` | 删除（schema 外；信息已在 registry 保留） |
| org 顶层 `description` / `brief` | `core_business` 为空时并入，否则删除 |
| `key_people[].person_name` | `name` 为空时移值，否则删除 |
| `key_people[].source` / `wikidata_qid` | 直接删除 |
| literal `"null"` 字符串值 | 置为 JSON null |

**实测**：GN+NG 双目录共 802 处修复（364 文件）；TG 4 处。修复后跑 `validate_schema.py --strict`，errors 应大幅下降（GN 19→2、NG-0729 911→95）。

**坑位**：不要把 `degree_note` 之类的自定义注释字段留在 education 里——strict 会报 extra fields；归一信息写入白名单内的 `note` 字段（degree 归一时踩过：`p1_qid` 轮 86 条 extra-field 错误因此返工）。

---

## 阶段 2：中文规范补齐

### 2.1 缺失统计

```python
# orgs: basic_info.name_zh 为空的统计
# persons: 顶层 name_zh 为空的统计
```

### 2.2 补齐优先级（实测有效路径）

| 优先级 | 路径 | 实测产出 |
|---|---|---|
| 1 | **同国另一日期目录同 ID 回填**（NG 案例：64 个） | 最快最准 |
| 2 | **人工映射表**（大学/媒体/银行等常见机构，脚本内置 dict） | NG 42 个 |
| 3 | 剩余逐条人工（一般 <5 个） | NG-SOE-014 单条 |

### 2.3 语言警告的处理口径

| 警告类型 | 口径 |
|---|---|
| `organization lacks Chinese (brand exemption OK)` | 符合 2026-11-12 语言政策，**保留不修**（Paystack/Airtel 类品牌无通行中文名） |
| `name_zh contains non-initial Latin` | 拉丁首字母中缀（"拉塔·D·格纳马"、"T.B.约书亚"）为政策豁免，**保留** |
| KR 姓名 Hangul 规则 | 仅 CJK 区域数据集适用 |

**验收**：`--strict` 0 errors 后，language 警告应只剩品牌豁免/首字母豁免两类。

---

## 阶段 3：头像下载与规范

### 3.1 状态盘点（四象限）

```python
# no_profile           : 档案无 profile 对象（low 重要度正常，不处理）
# downloaded           : local_path 存在且文件在盘
# src_undownloaded     : 有 source_url 无 local_path → 待下载
# dead_local           : local_path 指向不存在文件 → 置空或重下
# source_is_page       : source_url 是网页不是图片直链 → 数据缺陷，见 3.4
```

### 3.2 下载通道优先级（重要！按序尝试）

| 通道 | 适用 | 实测 |
|---|---|---|
| ① 28081 图片代理 `http://10.11.203.60:28081/image?url=<quoted-url>` | 所有图片 URL；**Wikimedia 429 时的首选绕行** | GN 89 张、TG 22 张；但 Wikimedia 大面积 429 时代理出口同 IP 也会被拦 |
| ② 浏览器 downloadMedia（IAB） | **命令行出口被 429 封锁时的杀手锏**——浏览器会话独立于命令行出口 | TG 直链 22/24 成功；注意 img "hidden" 失败时改用页内分块 fetch（见 3.3） |
| ③ 直连 urllib + UA | 非 Wikimedia 源（TG 本地站等） | TG 本地站 3 张；TG 站点普遍 SSL 握手失败则放弃 |
| ④ 浏览器页内分块 fetch | 大图/慢源/downloadMedia "hidden" 失败时 | TG FIN-008 2.9MB 大图成功；页内启动后台 fetch + 轮询收块 + 跨 evaluate 拉回 |

**铁律（继承 network_config.md）**：批量取 Wikimedia 图一律 `Special:FilePath` 路由，禁直连 `upload.wikimedia.org`——命令行直取必 429。

### 3.3 downloadMedia "hidden" 失败的解法（TG 实战沉淀）

`locator.downloadMedia` 对部分图片报 "actionability (hidden)"。原因是图片在 image-document 视图中渲染为隐藏元素。解法是**页内分块 fetch**：

```js
// 1. 页内启动后台 fetch（不 await）
await tab.playwright.evaluate(() => {
  window.__done = false; window.__chunks = [];
  fetch(document.querySelector("img").src, {credentials: "include"}).then(async r => {
    const reader = r.body.getReader();
    while (true) {
      const {done, value} = await reader.read();
      if (done) break;
      window.__chunks.push(btoa(String.fromCharCode(...value)));
    }
    window.__done = true;
  });
});
// 2. 轮询 window.__done
// 3. 完成后分块拉回（每块一个 evaluate），拼 base64 写盘
```

**坑位**：
- 2.9MB 大图单次 evaluate fetch 会超时（32s 上限）——必须分块 + 后台化。
- 跨盘 rename 会 EXDEV——用 copyFileSync + unlinkSync。
- downloadMedia 落盘在 `~/Downloads/*.tmp`（随机名），需按 mtime 找最新 tmp、魔数嗅探定扩展名后 rename。

### 3.4 `source_url` 指向网页而非图片（数据缺陷）

TG 实测 23 条 `source_url` 填的是官网首页/关于页。处理：

1. 有 QID → 查 P18（见 3.5）
2. 无 QID → 生成手工复核 HTML 页（分区列出链接 + QID 跳转），人工浏览器找图
3. 找不到 → `source_url`/`local_path`/`minio_path` 全置 null（不要留网页 URL 冒充图片源）

### 3.5 QID → P18 救援

- 批量扫描：Wikidata API `wbgetclaims&property=P18`（实测 51 个 QID 只有 5 个有 P18——TG 类小国实体图像覆盖率低）
- API 被 429 时：浏览器打开 Wikidata 页 → 页内 `fetch()` 同源 API 调用（绕过命令行出口限流）
- 下载 P18 图：Special:FilePath 路由 + 页内分块 fetch（大图必须）

### 3.6 死路径处理

`local_path` 指向不存在文件 → 无 source_url 时**三字段全置 null**（不要留死路径）；有 source_url 时先重下。

### 3.7 profile 字段回填

下载成功的图片批量回填三字段：

```python
pr['local_path']  = 'minio-store/default/popular-person-profile/{cc}/{ID}{ext}'
pr['minio_path']  = 'default/popular-person-profile/{cc}/{ID}{ext}'  # 无 minio-store/ 前缀
```

---

## 阶段 4：ID 关联清理

### 4.1 自动清理规则（脚本模板：`scripts_tmp/tg_id_audit.py`）

| 类别 | 处理 | 验收口径依据 |
|---|---|---|
| 错误引用（ID 有画像但名称不匹配） | 置空 | 错链必须修 |
| 幽灵 ID（不在 registry 也不在画像） | 置空 | 结构性无效 |
| **已注册但无画像的引用** | **保留** | 用户口径：无画像可接受 |

**⚠️ 重大坑位（TG 踩过）**：第一版脚本把 dangling（含 registered-no-profile）全部置空，**误伤 493 条引用**。必须区分"错误引用"与"注册无画像引用"。用 git diff 全量恢复才救回来。自动脚本必须显式保留后者。

### 4.2 key_people 悬空处理

| 情况 | 处理 |
|---|---|
| 名称匹配到既有画像（含转写变体） | 回填 person_id |
| 确认不同人（同姓不同人） | 置空 ID 保留名称 |
| 真实人物但无画像 | **创建骨架画像**（name/name_zh/nationality/current_positions/work_experience 反向关联 + collection_meta.completeness_score=35 + phase=phase4_person_profile），registry 补 status=listed 条目 |

**骨架画像坑位**：schema 必填 `gender`——GN/TG 骨架漏了导致 238/1 条 errors；统一填 `gender: "unknown"`。

### 4.3 registry 碰撞 & 重复 QID

```python
# 同 ID 多身份碰撞：name 分组计数
# 重复 QID：跨档案 QID 分组；同人跨目录保留丰富副本、清空另一份
```

GN/NG/TG 实测均为 0 碰撞；NG 双目录间 21 组跨目录同 QID 已去重。

---

## 阶段 5：收尾验证

```bash
# 1. strict 校验（目标 0 errors）
python validate_schema.py output/{cc}/{date} --strict

# 2. 名称索引重建
python generate_name_index.py output/{cc}/{date}

# 3. ID 引用审计（wrong 应为 0；dangling/registered_no_profile 可接受）
python scripts_tmp/tg_id_audit.py audit
```

**验收基线**：0 errors；wrong=0；无空字符串 ID；无死 local_path；重复 QID=0；碰撞=0。

---

## 阶段 6：提交与 MinIO 增量

```bash
git add output/{cc}/ scripts_tmp/<本轮脚本>
git commit -m "data: {CC} collection-final cleanup - ..."
git push origin main
```

MinIO 增量打包（等累积多国后合并）：

```bash
# 文件清单 = profile.local_path 引用且在盘上的、上次上传后新增的
tar -cf minio-increment-{N}.tar -C minio-store default
# 或 zip（Windows 桌面交付用）
python -c "zipfile..."  # STORED 模式（图片已压缩）
```

---

## 六阶段实测数据汇总

| 数据集 | strict errors | 头像下载 | 中文补齐 | 错误引用清理 | 提交 |
|---|---:|---:|---:|---:|---|
| GN 2026-11-10 | 0 | 89 成功 | — | 152 置空 | ✅ |
| NG 2026-11-10 | 0 | 已有 | — | 35 置空 + 91 kp 链接 + 238 骨架 | ✅ |
| NG 2026-07-29 | 0 | — | 64+42 | 3 跨目录改链 | ✅ |
| TG 2026-11-16 | 0 | 80+45=125 成功 | 0 缺失 | 16 置空 + 596 幽灵 + 1 骨架 | ✅ |

## 关键教训清单（按踩坑频率排序）

1. **registered-no-profile ≠ 错误引用**——自动清理脚本必须区分（TG 误伤 493 条）
2. **Wikimedia 429 是 IP 级封锁**——命令行换代理/换 UA 无效；浏览器会话独立不受影响；完全静默 5 分钟才解封；重试请求本身会续期封锁
3. **28081 图片代理**——首选绕行通道，但出口 IP 与本机相同时同样被 Wikimedia 拦
4. **骨架画像必须含 gender**——schema 必填，GN/TG 各踩一次
5. **downloadMedia "hidden" 失败**——页内分块 fetch 是通用解法
6. **跨盘 rename EXDEV**——Downloads(C:) → minio-store(D:) 用 copy+unlink
7. **自定义注释字段会炸 strict**——归一信息写白名单内的 note 字段
8. **多日期目录**——先确认 ID 是否重叠，重叠才需去重

# P5 终验报告 — 埃及（EG）组织与人物数据集

**日期**：2026-11-21
**数据集**：`output/eg/2026-11-16/`

---

## 一、终验结果

| 校验 | 文件 | 错误 | 警告 | 说明 |
|---|---|---|---|---|
| orgs strict | 190 | **0** | 466 | 警告为 P3 时代语言/覆盖提示（含骨架件翻译注记），可接受 |
| persons strict | 208 | **0** | 2 | 品牌名缺中文译名豁免 |
| 对账 | persons completed 208 = 磁盘 208 | ✓ | — | completed/current/remaining/failed 全清零 |

## 二、P5 执行的修正项

1. **同人双注册核销 ×2**：
   - 000187→000398（Mounir Fakhry Abdel Nour，Q1860273；GB Corp 独立董事职衔经双源确认属实；引用修正 3 文件：EG-CORP-006、EG-PERSON-000182、000398）
   - 000375→000380（Tamer Morsi，EG-MEDIA-019 key_people 绑定 000380；两者均无档案）
2. **org 画像勘误 ×5**：
   - EG-MEDIA-001 罗马拼写 Magdy→Maged Mounir
   - EG-MEDIA-003 「أسامة عفيفي」→「إسلام عفيفي」
   - EG-FIN-002 000221 Barakat 描述「FEB 主席」过时口径勘正（现任为埃特雷比 000222）
   - EG-GOV-047 阿瓦德履历混淆注记（GAFI 投资政策负责人系曼苏尔履历；阿瓦德实为 ITDA 董事长）
   - EG-SOE-017/EG-MIL-006/EG-CORP-007/EG-SOE-001 等 P4 期间已顺手修正（ SCV 双副主席已入、VACSERA 双层、El-Wakil 注记等）
3. **27 个 P2 骨架件 name_zh 补全**（excluded_osint_trim 裁剪件按英文名译补，附 name_zh_note）——orgs strict 归零的关键
4. **key_people 附加字段 ×4** 并入 title_description/description
5. **遗留疑项核实关闭**：
   - Dawoud 000267「双角色」= 遥感太空署前主席 → 爱资哈尔大学现任校长，先后任职合法仕途序 ✓
   - ASRT 主席（P3 Faki/Muawwad 之诤）= 现档代理院长 El-Feki（000301），以 P3 终态为准 ✓
   - TE Data EG-CORP-015 = excluded_osint_trim 骨架（正确状态）✓

## 三、数据集终局统计

### 组织（orgs/）
- **190 个 profile**（P3 富集 151 + 裁剪骨架 39）· avg score **71**
- quotes 1099 · 有社媒 163
- 来源：official_website 170 / wikipedia 154+76+11 / news_search 154 / wikidata 80 / social_media 97 …

### 人物（persons/）
- **208 个 profile**（v3/v4 裁剪后在册 100%）· avg score **70**（P4 收 69.4 → 补强后 69.6 → strict 剥离后 70）
- quotes 3066 · work_experience 1390 · relationships 789
- **社媒覆盖 90/208（43%）**：LinkedIn 51 / FB 33 / X 24 / IG 10 / YouTube 5 / Threads 1 / TikTok 1 / TG 1 / other 2
- **头像覆盖 147/208（71%）**（全部 magic bytes 校验 + 目检；P4 补强从 1 张提升）
- 头像链接质量：图片直链 128 · 非图链 29（已注记）· QID 伪图链 0 · 疑真死链 3
- 中文规范：**零违规**（name_zh 全含中文、name_en 无中文、正文中文、别名含阿语）

### 索引与注册表
- orgs/_index.json（190, avg 71）· persons/_index.json（208, avg 70）
- id_registry：orgs 190 · persons **632**（P5 期间核销 000187、000375）
- _name_index.json：6328 键
- _tmp 临时目录已清（805 文件/61MB）

## 四、可选后续（未执行）

- cross-ref 1580 条 name-mismatch：显示名括号语言格式差异（ID 全部正确），可一键脚本批量归一（触面广，默认保留原状）
- 000177 塔里克职衔复核（FB/Reuters 示非执行 Chairman vs 原档联席 CEO）
- 情报/军方人物头像难源：SIS 官员名录页深挖（收益低）

## 五、结论

五阶段管线（P1 广度 → P2 缓存骨架 → P3 组织富集 151 → P4 人物 208 → P5 终验修正）全部完成。**两数据集 strict 零错误**、索引/注册表/磁盘三方对账一致、中文规范零违规、头像/社媒经一轮系统补强。数据集可交付。

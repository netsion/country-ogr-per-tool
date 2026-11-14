# 台湾地区首批人物采集记录（2026-11-13）

本轮先修整底表，再逐人采集首批10人。人物总数仍为527；有效组织隔离4条后为98条，另为人物任职关联补建4个有官方来源的组织骨架，目前为102条。

完整原始备份与隔离审计：`tmp/tw_before_repair_20261113_021320/`。结构修整详情见 `docs/tw_repair_report.md`。

首批完成 10/10。完成表示本轮公开资料研究与写入结束，不表示达到85分，也不表示全部字段已核实。

| 人物 | ID | 完整度 | 教育 | 履历 | 简介字数 | 引用页数 |
|---|---|---:|---:|---:|---:|---:|
| 赖清德 | TW-PERSON-000001 | 67 | 3 | 7 | 318 | 4 |
| 萧美琴 | TW-PERSON-000012 | 64 | 2 | 8 | 342 | 3 |
| 卓荣泰 | TW-PERSON-000018 | 54 | 1 | 9 | 319 | 4 |
| 郑丽君 | TW-PERSON-000032 | 57 | 2 | 7 | 326 | 4 |
| 韩国瑜 | TW-PERSON-000011 | 64 | 2 | 5 | 343 | 4 |
| 江启臣 | TW-PERSON-000035 | 64 | 3 | 6 | 358 | 5 |
| 林佳龙 | TW-PERSON-000023 | 68 | 5 | 11 | 350 | 4 |
| 顾立雄 | TW-PERSON-000026 | 54 | 2 | 8 | 338 | 5 |
| 魏哲家 | TW-PERSON-000508 | 49 | 2 | 8 | 359 | 3 |
| 蒋万安 | TW-PERSON-000526 | 48 | 2 | 4 | 341 | 4 |

实际 JSON Schema 校验：人物错误 0 项；组织错误 73 项。完整逐项清单为 `tmp/tw_jsonschema_validation.json`。

限制与后续：

- 仍有组织细分类缺证据，保留缺失并如实报错，不为通过验证编造分类。
- 首批教育、履历、现职和简介按本轮引用来源丰富；部分出生日期仍只有单一来源，已在人物 notes 标注。
- 社交平台检索遇到访问限制或身份凭据不足，旧头像、社交账号及平台标识保留但不得视为本轮独立核验；魏哲家无可靠本人账号时留空。
- 其他517人仍为待研究候选。历史来源链接转入 quotes 仅为格式迁移，并非本轮读取或确认；notes 保留原阶段及未研究说明。
- 组织旧领导记录仍有历史任职和错绑风险，已核实首批对应关系回填，不能将其余列表视作当前领导名录。
- 已核实并纠正 TW-CORP-014：欣兴电子应为 Unimicron Technology Corp.（Q15908529），原 King Yuan Electronics 属于京元电子；原错误内容保留在备份。
- 新总统府、外交部、国防部、台北市政府均为有来源的骨架，未宣称完成组织深采。

采集证据：

**赖清德**
- [总统府：赖清德简介](https://www.president.gov.tw/Page/694)
- [Lai Ching-te — Wikipedia](https://en.wikipedia.org/wiki/Lai_Ching-te)
- [中央社：赖清德人物专题](https://www.cna.com.tw/topic/newstopic/4282.aspx)
- [中央社：赖萧配当选](https://www.cna.com.tw/news/aipl/202401140007.aspx)

**萧美琴**
- [总统府：萧美琴简介](https://www.president.gov.tw/Page/695)
- [Hsiao Bi-khim — Wikipedia](https://en.wikipedia.org/wiki/Hsiao_Bi-khim)
- [中央社：赖萧配当选](https://www.cna.com.tw/news/aipl/202401140007.aspx)

**卓荣泰**
- [行政院：卓荣泰正式上任](https://www.ey.gov.tw/Page/9277F759E41CCD91/347ac719-9b3d-4bf3-a6e0-191bbd9d3001)
- [中兴大学：第28届杰出校友卓荣泰](https://alumni.nchu.edu.tw/page-1.php?id=8cdc2a21-8ce8-419f-b6c6-f9a714c7e69b)
- [Cho Jung-tai — Wikipedia](https://en.wikipedia.org/wiki/Cho_Jung-tai)
- [中央社：卓荣泰人物专题](https://www.cna.com.tw/topic/newstopic/4491.aspx)

**郑丽君**
- [行政院：郑丽君副院长](https://www.ey.gov.tw/Page/B0DDF0F69A75E8DB/8708343d-dd7c-47c0-a3a5-336577da50da)
- [立法院：郑丽君历史名录](https://www.ly.gov.tw/Pages/List.aspx?nodeid=1784)
- [中央社：对等关税谈判小组](https://www.cna.com.tw/news/aipl/202504090185.aspx)
- [Cheng Li-chiun — Wikipedia](https://en.wikipedia.org/wiki/Cheng_Li-chun)

**韩国瑜**
- [立法院：院长韩国瑜](https://www.ly.gov.tw/Pages/Detail.aspx?nodeid=120&pid=1)
- [Han Kuo-yu — Wikipedia](https://en.wikipedia.org/wiki/Han_Kuo-yu)
- [中央社：韩国瑜当选立法院长](https://www.cna.com.tw/news/aipl/202402010152.aspx)
- [中央社：韩国瑜谈国会多元](https://www.cna.com.tw/news/aipl/202402190043.aspx)

**江启臣**
- [立法院：副院长江启臣履历](https://www.ly.gov.tw/Pages/Detail.aspx?nodeid=121&pid=2)
- [中央社：江启臣谈中央地方合作](https://www.cna.com.tw/news/aipl/202402020069.aspx)
- [Johnny Chiang — Wikipedia](https://en.wikipedia.org/wiki/Johnny_Chiang)
- [立法院：江启臣访问爱尔兰](https://www.ly.gov.tw/Pages/Detail.aspx?nodeid=117&pid=254078)
- [中央社：江启臣出访美法](https://www.cna.com.tw/news/aipl/202411110058.aspx)

**林佳龙**
- [外交部：林佳龙履历](https://www.mofa.gov.tw/MofaLeader_Content.aspx?mls=138&n=88)
- [Lin Chia-lung — Wikipedia](https://en.wikipedia.org/wiki/Lin_Chia-lung)
- [中央社：林佳龙党政经历](https://www.cna.com.tw/news/aipl/202404250078.aspx)
- [中央社：林佳龙说明外交路线](https://www.cna.com.tw/news/aipl/202404250069.aspx)

**顾立雄**
- [国防部：部长英文介绍](https://www.mnd.gov.tw/Publication/83001)
- [国防部：现任部长](https://www.mnd.gov.tw//About/Minister/dio)
- [Wellington Koo — Wikipedia](https://en.wikipedia.org/wiki/Wellington_Koo_(politician,_born_1958))
- [中央社：顾立雄履历](https://www.cna.com.tw/news/aipl/202404250074.aspx)
- [中央社：顾立雄获赠勋](https://www.cna.com.tw/news/aipl/202405150089.aspx)

**魏哲家**
- [台积电：管理团队](https://www.tsmc.com/english/aboutTSMC/executives)
- [SIA：2025诺伊斯奖获选公告](https://www.semiconductors.org/tsmcs-dr-c-c-wei-and-dr-mark-liu-to-receive-sias-highest-honor/)
- [Che-Chia Wei — Wikipedia](https://en.wikipedia.org/wiki/Che-Chia_Wei)

**蒋万安**
- [台北市政府：蒋万安市长履历](https://www.gov.taipei/News_Content_Leader.aspx?n=5A0C91ADEE6E7C46&s=5C77853F1AB78232&sms=7CAF6BD4D3E48630)
- [Chiang Wan-an — Wikipedia](https://en.wikipedia.org/wiki/Chiang_Wan-an)
- [中央社：台北市长选举结果](https://www.cna.com.tw/news/aipl/202211260299.aspx)
- [中央社：蒋万安登记参选](https://www.cna.com.tw/news/aipl/202209010099.aspx)


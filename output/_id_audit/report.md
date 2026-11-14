# 全库 ID 引用完整性审计

- 数据范围：53 个国家最新日期目录，person 17,596，org 6,017
- 生成时间：2026-11-13

## 1. 引用完整性总表

| 引用方向 | 总条数 | 已填 ID | ID 为空 | ID 悬空 | ID 指错(名称不符) | 正常 |
|---|---:|---:|---:|---:|---:|---:|
| person.work_experience.org_id → org | 129,203 | 71,931 | 57,272 | 7,255 | 17,737 | 46,939 |
| person.person_relationships.person_id → person | 53,200 | 39,930 | 13,270 | 7,650 | 4,186 | 28,094 |
| person.family_members.person_id → person | 18,103 | 1,673 | 16,430 | 289 | 74 | 1,310 |
| org.key_people.person_id → person | 25,497 | 23,225 | 2,272 | 4,966 | 1,014 | 17,245 |
| org.related_entities.org_id → org | 32,722 | 26,175 | 6,547 | 6,140 | 4,153 | 15,882 |
| org.departments.parent_dept_id → dept | 34,386 | 2,027 | 32,359 | 398 | 0 | 1,629 |

## 2. 空 person_id 的可解析性（按姓名）

| 方向 | 空 ID | 姓名可唯一定位 | 姓名重名歧义 | 姓名找不到 |
|---|---:|---:|---:|---:|
| 关系人 | 13,270 | 2,796 | 95 | 10,379 |
| 家庭成员 | 16,430 | 408 | 16 | 16,006 |

## 3. ID 体系问题

- 文件名 vs 内部 ID 不一致：0
- person_id 重复（跨目录）：0
- org_id 重复（跨目录，含 NG 双日期）：0
- person wikidata_qid 重复：72 组
- org wikidata_qid 重复：12 组

## 4. _index.json 一致性

- person_index_missing_file: 6
- person_index_dup: 0
- person_index_id_mismatch: 6
- org_index_missing_file: 3
- org_index_dup: 0
- org_index_name_mismatch: 373
- persons_not_in_index: 26
- orgs_not_in_index: 103

## 5. 各国 work_experience org 引用异常（Top 20）

| 国家 | 总数 | 空 ID | 悬空 | 指错 |
|---|---:|---:|---:|---:|
| mx | 4,465 | 9 | 1,466 | 1,465 |
| jp | 6,143 | 881 | 1,463 | 1,297 |
| kr | 11,097 | 5,436 | 0 | 2,122 |
| ph | 6,842 | 2,304 | 464 | 1,187 |
| cl | 3,912 | 1,034 | 293 | 1,095 |
| th | 5,310 | 2,344 | 350 | 758 |
| vn | 1,665 | 36 | 499 | 599 |
| pg | 1,992 | 231 | 667 | 141 |
| us | 8,137 | 4,427 | 163 | 601 |
| sa | 4,375 | 1,994 | 381 | 299 |
| ma | 1,596 | 430 | 127 | 528 |
| ru | 3,750 | 2,067 | 0 | 626 |
| kg | 3,027 | 1,758 | 0 | 620 |
| id | 5,879 | 4,524 | 0 | 522 |
| pe | 1,703 | 478 | 67 | 388 |
| my | 3,749 | 2,614 | 38 | 401 |
| nz | 5,271 | 3,385 | 212 | 208 |
| ca | 4,625 | 2,944 | 6 | 388 |
| au | 3,639 | 1,963 | 0 | 385 |
| cd | 1,331 | 378 | 61 | 268 |

## 6. 典型错配样例（Musk 相关 + 全局抽样）

### work_org

```json
[
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000003",
  "name": "Fabio Piano",
  "org_id": "AE-ACAD-022",
  "organization": "纽约大学 (New York University)",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000003",
  "name": "Fabio Piano",
  "org_id": "AE-ACAD-022",
  "organization": "纽约大学 (New York University)",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000003",
  "name": "Fabio Piano",
  "org_id": "AE-ACAD-022",
  "organization": "纽约大学 (New York University)",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000011",
  "person": "منصور بن زايد آل نهيان",
  "org_id": "AE-SOE-004",
  "organization": "阿布扎比投资局 (Abu Dhabi Investment Authority, ADIA)",
  "target": "阿布達比投資局",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000011",
  "person": "منصور بن زايد آل نهيان",
  "org_id": "AE-GOV-037",
  "organization": "阿布扎比最高石油委员会 (Supreme Petroleum Council, SPC)",
  "target": "最高石油委員會",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000011",
  "name": "منصور بن زايد آل نهيان",
  "org_id": "AE-FIN-021",
  "organization": "第一海湾银行 (First Gulf Bank, FGB)",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000011",
  "person": "منصور بن زايد آل نهيان",
  "org_id": "AE-NGO-003",
  "organization": "哈利法·本·扎耶德慈善基金会 (Khalifa bin Zayed Charity Foundation)",
  "target": "穆罕默德·本·拉希德·阿勒马克图姆全球倡议",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000019",
  "person": "سارة بنت يوسف الأميري",
  "org_id": "AE-NGO-003",
  "organization": "穆罕默德·本·拉希德航天中心 (مركز محمد بن راشد للفضاء)",
  "target": "穆罕默德·本·拉希德·阿勒马克图姆全球倡议",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000019",
  "person": "سارة بنت يوسف الأميري",
  "org_id": "AE-NGO-003",
  "organization": "穆罕默德·本·拉希德航天中心 (مركز محمد بن راشد للفضاء)",
  "target": "穆罕默德·本·拉希德·阿勒马克图姆全球倡议",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000019",
  "name": "سارة بنت يوسف الأميري",
  "org_id": "AE-GOV-039",
  "organization": "阿联酋航天局 (وكالة الإمارات للفضاء)",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000020",
  "person": "سهيل محمد فرج المزروعي",
  "org_id": "AE-GOV-012",
  "organization": "阿联酋能源部 (وزارة الطاقة)",
  "target": "能源与基础设施部",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000020",
  "person": "سهيل محمد فرج المزروعي",
  "org_id": "AE-GOV-012",
  "organization": "阿联酋能源与工业部 (وزارة الطاقة والصناعة)",
  "target": "能源与基础设施部",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000022",
  "person": "آمنة بنت عبد الله الضحاك الشامسي",
  "org_id": "AE-NGO-003",
  "organization": "穆罕默德·本·扎耶德-佐科·维多多国际红树林研究中心 (Mohamed bin Zayed - Joko Widodo International Mangrove Research Centre)",
  "target": "穆罕默德·本·拉希德·阿勒马克图姆全球倡议",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000022",
  "person": "آمنة بنت عبد الله الضحاك الشامسي",
  "org_id": "AE-NGO-003",
  "organization": "穆罕默德·本·扎耶德水资源倡议 (Mohamed bin Zayed Water Initiative)",
  "target": "穆罕默德·本·拉希德·阿勒马克图姆全球倡议",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000023",
  "person": "أحمد بن علي الصايغ",
  "org_id": "AE-FIN-002",
  "organization": "第一海湾银行 (First Gulf Bank)",
  "target": "第一阿布扎比银行",
  "issue": "mismatch"
 }
]
```

### person_rel

```json
[
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000001",
  "person": "Kevin Hall",
  "ref_name": "沙玛·穆兹鲁伊 (Shamma Al Mazrui)",
  "ref_person_id": "AE-PERSON-000065",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000003",
  "person": "Fabio Piano",
  "ref_name": "约翰·塞克斯顿 (John Sexton)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000003",
  "person": "Fabio Piano",
  "ref_name": "阿尔弗雷德·布卢姆 (Alfred Bloom)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000003",
  "person": "Fabio Piano",
  "ref_name": "玛丽特·韦斯特曼 (Mariët Westermann)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000006",
  "person": "هشام عبدالله القاسم",
  "ref_name": "马克图姆·本·穆罕默德·阿勒马克图姆 (مكتوم بن محمد آل مكتوم)",
  "ref_person_id": "AE-PERSON-000013",
  "target": "مكتوم بن محمد بن راشد آل مكتوم",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000007",
  "person": "Shayne Nelson",
  "ref_name": "里克·普德纳 (Rick Pudner)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000008",
  "person": "عبد العزيز الغرير",
  "ref_name": "阿卜杜拉·阿尔·古赖尔 (عبدالله الغرير)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000008",
  "person": "عبد العزيز الغرير",
  "ref_name": "赛义夫·艾哈迈德·阿尔·古赖尔 (Saif Ahmad Al Ghurair)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "哈姆丹·本·穆罕默德 (حمدان بن محمد)",
  "ref_person_id": "AE-PERSON-000014",
  "target": "حمدان بن محمد بن راشد آل مكتوم",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "马克图姆·本·穆罕默德 (مكتوم بن محمد)",
  "ref_person_id": "AE-PERSON-000013",
  "target": "مكتوم بن محمد بن راشد آل مكتوم",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "曼苏尔·本·扎耶德 (منصور بن زايد)",
  "ref_person_id": "AE-PERSON-000011",
  "target": "منصور بن زايد آل نهيان",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "艾哈迈德·本·赛义德 (أحمد بن سعيد)",
  "ref_person_id": "AE-PERSON-000048",
  "target": "أحمد بن سعيد آل مكتوم",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "穆罕默德·格尔加维 (محمد القرغاوي)",
  "ref_person_id": "AE-PERSON-000025",
  "target": "محمد بن عبدالله القرقاوي",
  "issue": "mismatch"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000013",
  "person": "مكتوم بن محمد بن راشد آل مكتوم",
  "ref_name": "艾哈迈德·本·穆罕默德·本·拉希德·阿勒马克图姆 (أحمد بن محمد بن راشد آل مكتوم)",
  "ref_person_id": null,
  "resolve": "unique",
  "resolved_to": "AE-PERSON-000221"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000014",
  "person": "حمدان بن محمد بن راشد آل مكتوم",
  "ref_name": "拉希德·本·穆罕默德·阿勒马克图姆 (Rashid bin Mohammed Al Maktoum)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 }
]
```

### family

```json
[
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000007",
  "person": "Shayne Nelson",
  "ref_name": "西蒂·玛丽安娜·阿卜杜拉 (Siti Mariana Abdullah)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000008",
  "person": "عبد العزيز الغرير",
  "ref_name": "阿卜杜拉·阿尔·古赖尔 (عبدالله الغرير)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000008",
  "person": "عبد العزيز الغرير",
  "ref_name": "赛义夫·艾哈迈德·阿尔·古赖尔 (Saif Ahmad Al Ghurair)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "拉希德·本·赛义德·阿勒马克图姆 (راشد بن سعيد آل مكتوم)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "拉蒂法·宾特·哈姆丹·阿勒纳哈扬 (لطيفة بنت حمدان آل نهيان)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "赛义德·本·马克图姆·本·哈希尔·阿勒马克图姆 (سعيد بن مكتوم بن حشر آل مكتوم)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "欣德·宾特·马克图姆·宾特·朱马·阿勒马克图姆 (هند بنت مكتوم بن جمعة آل مكتوم)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "哈雅·宾特·侯赛因 (هيا بنت الحسين)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "艾哈迈德·本·穆罕默德·本·拉希德·阿勒马克图姆 (أحمد بن محمد آل مكتوم)",
  "ref_person_id": null,
  "resolve": "unique",
  "resolved_to": "AE-PERSON-000221"
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "拉希德·本·穆罕默德·本·拉希德·阿勒马克图姆 (راشد بن محمد آل مكتوم)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "玛纳尔·宾特·穆罕默德·本·拉希德·阿勒马克图姆 (منال بنت محمد آل مكتوم)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "马克图姆·本·拉希德·阿勒马克图姆 (مكتوم بن راشد آل مكتوم)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000010",
  "person": "محمد بن راشد آل مكتوم",
  "ref_name": "哈姆丹·本·拉希德·阿勒马克图姆 (حمدان بن راشد آل مكتوم)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000011",
  "person": "منصور بن زايد آل نهيان",
  "ref_name": "扎耶德·本·苏尔坦·阿勒纳哈扬 (Zayed bin Sultan Al Nahyan)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 },
 {
  "cc": "ae",
  "person_id": "AE-PERSON-000011",
  "person": "منصور بن زايد آل نهيان",
  "ref_name": "法蒂玛·宾特·穆巴拉克 (Fatima bint Mubarak Al Ketbi)",
  "ref_person_id": null,
  "resolve": "not-found",
  "resolved_to": null
 }
]
```

### key_people

```json
[
 {
  "cc": "ae",
  "org_id": "AE-ACAD-001",
  "org": "阿拉伯聯合酋長國大學",
  "ref_name": "扎基·安瓦尔·努赛贝 (Zaki Anwar Nusseibeh)",
  "ref_person_id": "AE-PERSON-000058",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-001",
  "org": "阿拉伯聯合酋長國大學",
  "ref_name": "穆赫辛·谢里夫 (Mohsen Sherif)",
  "ref_person_id": "AE-PERSON-000060",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-002",
  "org": "哈利法大学",
  "ref_name": "易卜拉欣·阿尔哈吉里 (H.E. Prof. Ebrahim Al Hajri)",
  "ref_person_id": "AE-PERSON-000062",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-002",
  "org": "哈利法大学",
  "ref_name": "巴扬·谢里夫 (Dr. Bayan Sharif)",
  "ref_person_id": "AE-PERSON-000064",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-003",
  "org": "扎耶德大学",
  "ref_name": "沙玛·穆兹鲁伊 (Shamma Al Mazrui)",
  "ref_person_id": "AE-PERSON-000065",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-004",
  "org": "沙迦大学",
  "ref_name": "苏丹·本·艾哈迈德·卡西米 (Sultan bin Ahmed Al Qasimi)",
  "ref_person_id": "AE-PERSON-000066",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-004",
  "org": "沙迦大学",
  "ref_name": "埃萨姆丁·阿加米 (Esameldin Agamy)",
  "ref_person_id": "AE-PERSON-000067",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-005",
  "org": "沙迦美国大学",
  "ref_name": "谢哈·博杜尔·宾特·苏尔坦·卡西米 (Sheikha Bodour bint Sultan Al Qasimi)",
  "ref_person_id": "AE-PERSON-000069",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-005",
  "org": "沙迦美国大学",
  "ref_name": "托德·A·劳尔森 (Tod A. Laursen)",
  "ref_person_id": "AE-PERSON-000002",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-005",
  "org": "沙迦美国大学",
  "ref_name": "马蒂亚斯·鲁特 (Matthias Ruth)",
  "ref_person_id": "AE-PERSON-000070",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-005",
  "org": "沙迦美国大学",
  "ref_name": "穆罕默德·埃尔-埃利安 (Mohamed A. El-Erian)",
  "ref_person_id": "AE-PERSON-000071",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-005",
  "org": "沙迦美国大学",
  "ref_name": "龚旗煌 (Gong Qihuang)",
  "ref_person_id": "AE-PERSON-000072",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-005",
  "org": "沙迦美国大学",
  "ref_name": "伊琳娜·博科娃 (Irina Bokova)",
  "ref_person_id": "AE-PERSON-000073",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-006",
  "org": "迪拜美国大学",
  "ref_name": "凯尔·朗 (Kyle Long)",
  "ref_person_id": "AE-PERSON-000074",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-006",
  "org": "迪拜美国大学",
  "ref_name": "阿萨德·法拉 (Assaad Farah)",
  "ref_person_id": "AE-PERSON-000076",
  "issue": "dangling"
 }
]
```

### related_org

```json
[
 {
  "cc": "ae",
  "org_id": "AE-ACAD-001",
  "ref_name": "麦吉尔大学 (McGill University)",
  "ref_org_id": "AE-ACAD-011",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-002",
  "ref_name": "阿联酋航天局 (UAE Space Agency)",
  "ref_org_id": "AE-GOV-039",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-002",
  "ref_name": "技术创新研究院 (Technology Innovation Institute, TII)",
  "ref_org_id": "AE-ACAD-012",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-002",
  "ref_name": "石油研究所 (The Petroleum Institute)",
  "ref_org_id": "AE-ACAD-013",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-002",
  "ref_name": "马斯达尔理工学院 (Masdar Institute of Science and Technology)",
  "ref_org_id": "AE-ACAD-014",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-002",
  "ref_name": "哈利法科学技术研究大学 (KUSTAR)",
  "ref_org_id": "AE-ACAD-015",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-003",
  "ref_name": "韩国科学技术院 (KAIST)",
  "ref_org_id": "AE-ACAD-016",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-003",
  "ref_name": "SPARX Industries",
  "ref_org_id": "AE-CORP-014",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-004",
  "ref_name": "沙迦大学医院 (University Hospital Sharjah)",
  "ref_org_id": "AE-GOV-040",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-005",
  "ref_name": "美国学院与大学协会 (Association of American Colleges and Universities, AAC&U)",
  "ref_org_id": "AE-NGO-013",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-006",
  "ref_name": "宾夕法尼亚大学 (University of Pennsylvania)",
  "ref_org_id": "AE-ACAD-017",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-006",
  "ref_name": "IE 大学 (IE University)",
  "ref_org_id": "AE-ACAD-018",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-006",
  "ref_name": "佐治亚理工学院 (Georgia Institute of Technology)",
  "ref_org_id": "AE-ACAD-019",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-007",
  "ref_name": "伦敦玛丽女王大学 (Queen Mary University of London)",
  "ref_org_id": "AE-ACAD-020",
  "issue": "dangling"
 },
 {
  "cc": "ae",
  "org_id": "AE-ACAD-007",
  "ref_name": "美国西部学校和学院协会 (WASC/WSCUC)",
  "ref_org_id": "AE-ACAD-021",
  "issue": "dangling"
 }
]
```

# P2 批次 15–16：key_people 错误清理（2026-11-14）

## 批次 15

对 KZ/MY/TH/JP/RU 的明显错误 key_people 置空：

| 国家 | 数量 |
|---|---:|
| KZ | 63 |
| MY | 31 |
| TH | 31 |
| JP | 26 |
| RU | 22 |
| **合计** | **173** |

这些 key_people 当前 person_id 指向完全不同的人，例如：

- KZ：阿斯兰·萨林日波夫 → 阿斯兰·图基耶夫
- MY：阿米努丁哈欣 → 沙姆苏卡哈·本·莫哈末德利
- TH：帕色·勒克里莱 → 帕色·辛素帕色
- JP：大鹤哲也 → 植田和男
- RU：不同姓名的俄罗斯官员互相错配

## 批次 16

继续处理剩余明确错误的 key_people **18 条**：

- KG 2、LB 2、MX 2、PG 2、SA 2、TJ 1、UZ 4、VN 3

保留以下转写/同名变体：

- BF Asséto Ouédraogo
- CA Mario Peloin / Peloyan
- ID Fadlansyah / Fadlansia
- KG Umetov / Baydavletov / Bazarliev / Jenishbekov
- KW Yaqoub Al-Fares Rifai
- QA Khalid bin Khalifa
- SA Haifa bint Mohammed
- UZ Askarjon Gafurov

## 审计变化

| 指标 | 前 | 后 |
|---|---:|---:|
| key_people wrong | 203 | **12** |
| work_org wrong | 5,971 | 5,971 |
| person_rel wrong | 2,419 | 2,419 |
| related_org wrong | 1,447 | 1,447 |
| family wrong | 0 | 0 |
| 错误引用合计 | 10,040 | **9,849** |

剩余 12 条 key_people 基本都是转写变体，后续人工确认即可。

## P2 累计

| 类型 | 数量 |
|---|---:|
| relink | 441 |
| 结构置空 | 947 |
| 空 ID 补已有画像 | 418 |
| 碰撞影子置空 | 226 |
| 复核样本置空 | 273 |
| 簇置空 | 2,851 |
| key_people 置空 | 191 |
| **合计** | **5,347** |

## 产物

- `output/_id_audit/p2_batch15_keypeople_undo.json`
- `output/_id_audit/p2_batch16_keypeople_undo.json`
- 脚本：`scripts_tmp/p2_batch15_keypeople.py`、`scripts_tmp/p2_batch16_keypeople_remaining.py`

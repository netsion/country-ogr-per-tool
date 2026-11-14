# P2 批次 12：按错误簇批量处理（2026-11-13）

## 策略变化

逐条 150–200 条样本复核太慢。改为**按当前错误 ID 聚簇**：

- 同一个错误画像 ID 往往挂着几十到几百条无关引用；
- 每个簇抽看名称分布，保留真正属于该画像的名称，其余置空；
- 能确定目标画像的（如韩国国会）直接改链。

GN/NG 继续豁免，不参与本轮。

## 本轮处理的 9 个簇

| 当前 ID | 当前画像 | keep | relink | null |
|---|---|---:|---:|---:|
| `PH-CORP-015` | 国际集装箱码头服务 ICTSI | ICTSI 名称 | 0 | 505 |
| `MX-ACAD-001` | 墨西哥国立自治大学 UNAM | UNAM 名称 | 0 | 255 |
| `CL-SOE-007` | 圣地亚哥地铁 | Metro 名称 | 0 | 210 |
| `MX-ACAD-006` | 国家人文科学技术委员会 | CONAHCYT 名称 | 0 | 141 |
| `PE-SOE-006` | 秘鲁矿业资产公司 | Activos Mineros 名称 | 0 | 113 |
| `KR-GOV-016` | 韩国大法院 | 法院系统名称 | 126 条国会引用 → `KR-GOV-015` | 39 |
| `KR-GOV-001` | 国务会议 | 国务会议名称 | 0 | 103 |
| `JP-CORP-019` | 东京电力控股 | TEPCO 名称 | 0 | 77 |
| `UZ-SOE-005` | 乌兹别克铁路 | 铁路名称 | 0 | 74 |

合计：

- 保留 **347**
- 改链 **126**
- 置空 **1,517**

## 典型

- `KR-GOV-016` 大法院下挂 126 条韩国国会引用 → 改到 `KR-GOV-015`
- `PH-CORP-015` ICTSI 下挂 Ayala Land、San Miguel、Cebu Pacific 等 → 置空
- `MX-ACAD-001` UNAM 下挂墨西哥城政府、州议会、工会 → 置空
- `CL-SOE-007` 圣地亚哥地铁下挂 Quiñenco、Copec、ENAP 等 → 置空
- `JP-CORP-019` 东京电力下挂索尼通信、理光、RIZAP 等 → 置空
- `UZ-SOE-005` 乌兹别克铁路下挂象棋联合会、拳击协会、皮革协会等 → 置空

## 审计变化

| 指标 | 前 | 后 |
|---|---:|---:|
| work_org ok | 60,027 | 60,152 |
| work_org wrong | 8,293 | 6,864 |
| related_org wrong | 1,912 | 1,700 |
| person_rel wrong | 2,591 | 2,591 |
| key_people wrong | 210 | 210 |
| family wrong | 0 | 0 |

错误引用合计 **13,006 → 11,365**。

## 产物

- 撤销日志：`output/_id_audit/p2_cluster_apply_undo.json`
- dry-run 证据：`output/_id_audit/p2_cluster_apply_dry.json`
- 脚本：`scripts_tmp/p2_cluster_apply.py`

## P2 累计

| 类型 | 数量 |
|---|---:|
| relink | 315 + 126 = 441 |
| 结构置空 | 947 |
| 空 ID 补已有画像 | 418 |
| 碰撞影子置空 | 226 |
| 复核样本置空 | 273 |
| 簇置空 | 1,517 |
| **合计** | **3,822** |

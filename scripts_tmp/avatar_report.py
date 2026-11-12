# -*- coding: utf-8 -*-
"""Generate final avatar audit markdown report from audit_result.json."""
import json
import os
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool/output"
AD = os.path.join(BASE, "_avatar_audit")
d = json.load(open(os.path.join(AD, "audit_result.json"), encoding="utf-8"))
issues = d["issues"]
per_ds = d["per_dataset"]


def country(f):
    return os.path.relpath(f, BASE).replace("\\", "/").split("/")[0]


def by_country(sel):
    c = Counter(country(i["file"]) for i in sel)
    return ", ".join(f"{k}:{v}" for k, v in c.most_common(10))


def lines_for(sel, limit=60):
    out = []
    for i in sel[:limit]:
        out.append(f"| {os.path.relpath(i['file'], BASE).replace(chr(92), '/')} "
                   f"| {str(i.get('detail', ''))[:150]} |")
    return out


L = []
L.append("# 全局头像审计报告（54 个数据集）\n")
L.append("生成: avatar_audit.py 终轮（目录统一 + 命名规范化 + 伪协议修复之后）\n")

L.append("## 总览\n")
L.append("| 指标 | 数量 | 说明 |")
L.append("|---|---|---|")
cnt = Counter(i["type"] for i in issues)
for k, desc in [
    ("download_gap", "有直链但未下载到本地（问题4 清单）"),
    ("bad_source_url", "链接问题（问题1 清单）"),
    ("malformed_profile", "profile 字段是字符串而非对象（存量，未修改）"),
    ("local_missing", "local_path 指向不存在的文件（存量悬空）"),
    ("bad_naming", "文件名不符合 人物ID.ext 规范（问题3）"),
    ("id_mismatch", "文件名与内部 ID 不一致（CL _merged_ 残留）"),
    ("no_profile", "无头像（profile=null，非错误）"),
]:
    L.append(f"| {k} | {cnt.get(k, 0)} | {desc} |")
L.append(f"| orphans | {sum(len(v['orphan_files']) for v in per_ds.values())} "
         "| photos 目录中未被任何 JSON 引用的文件 |")
L.append("")
L.append("bad_source_url 分类: " + str(
    dict(Counter(i.get("class") for i in issues if i["type"] == "bad_source_url"))))
L.append("malformed_profile 构成: " + str(
    dict(Counter(i.get("value_type") for i in issues if i["type"] == "malformed_profile"))))
L.append("")

L.append("## 问题1：头像链接问题清单\n")
for cls in ("qid_page", "wiki_file_page", "social_page", "html_page"):
    sel = [i for i in issues if i["type"] == "bad_source_url" and i.get("class") == cls]
    L.append(f"### {cls}（{len(sel)}）— 国家分布: {by_country(sel)}\n")
    L.append("| 文件 | source_url |")
    L.append("|---|---|")
    L.extend(lines_for(sel, 15))
    L.append(f"\n（完整清单见 audit_result.json，筛选 type=bad_source_url & class={cls}）\n")

L.append("## 问题3：命名不规范（剩余）\n")
sel = [i for i in issues if i["type"] == "bad_naming"]
L.append("| 文件 | local_path |")
L.append("|---|---|")
L.extend(lines_for(sel, 30))
L.append("")

L.append("## 悬空引用 local_missing（存量，文件从未下载成功）\n")
sel = [i for i in issues if i["type"] == "local_missing"]
L.append("| 文件 | local_path |")
L.append("|---|---|")
L.extend(lines_for(sel, 40))
L.append("")

L.append("## 问题4：待统一下载清单（download_gap）\n")
sel = [i for i in issues if i["type"] == "download_gap"]
L.append(f"共 **{len(sel)}** 条，已导出 `download_candidates.json`（file + url）。\n")
L.append("国家分布: " + by_country(sel) + "\n")

L.append("## 本轮已执行的修复（问题2 + 顺手修复）\n")
L.append("| 动作 | 数量 |")
L.append("|---|---|")
L.append("| 照片移动至 国家/日期/persons/photos/（含大小写规范化） | 4203 |")
L.append("| persons JSON local_path 回写 | 4107 |")
L.append("| MA `local:photos/...` 伪协议 → local_path + source_url=null | 18 |")
L.append("| KG 指向 .json 的坏引用置 null | 7 |")
L.append("| 根目录/散落图片按 stem 捞回归位 | 2 |")
L.append("| 重复文件清理（同名同内容，保留规范名） | 51 |")
L.append("| 冲突保留待人工（同 ID 不同内容） | 1（bo-person-000087 vs BO-PERSON-000087） |")
L.append("")
L.append("wrong_location: 4104 → **0**；BO 基准数据集 strict 校验 0 错误。\n")
L.append("### 未处理的遗留（需另行决策）\n")
L.append("- malformed_profile 557（550 text_like 为 org 描述文本误入 profile 字段、"
         "7 url_like 可转为 source_url）")
L.append("- 8 个无 ID 命名的杂文件（`_test_*`/`dev_v*`/`_cand_*` 等，留在原位）")
L.append("- orphans 4489（多为历史上 dedup/renumber 遗留，PERSON 名已随迁，其余留在 photos/）")
L.append("- CL 的 6 个 `_merged_*.json` 残留文件（与头像无关，建议删除）")

with open(os.path.join(AD, "report.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(L))
print("report ->", os.path.join(AD, "report.md"))

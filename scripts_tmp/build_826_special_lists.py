# -*- coding: utf-8 -*-
"""Build special lists from the 826 review:
  1) 141 person names wrongly used as org candidates
  2) 19 duplicate-identity groups among the 300 deferrals
Outputs CSV + XLSX.
"""
import csv, json, os, re, sys
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

BASE = "D:/ai-workspace/apec-osint-tool"
REVIEW = os.path.join(BASE, "outputs/registry826_20261113/registry_newid_pending826_reviewed.csv")
OPINIONS = os.path.join(BASE, "outputs/registry826_20261113/review_opinions.json")
OUT = os.path.join(BASE, "output/_id_audit")


def main():
    rows = list(csv.DictReader(open(REVIEW, encoding="utf-8-sig")))
    op = json.load(open(OPINIONS, encoding="utf-8"))["rows"]
    assert len(rows) == len(op) == 826

    # 1) person names
    people = []
    for i, (r, o) in enumerate(zip(rows, op), 1):
        reason = o.get("reason") or ""
        if "自然人" not in reason:
            continue
        cands = re.findall(r"[A-Z]{2}-PERSON-\d{6}", reason)
        people.append({
            "原清单行": i, "国家": r["国家"], "冲突ID": r["冲突ID"],
            "现画像": r["现画像"], "影子名称": r["影子名称"],
            "引用数": r["引用数"], "人物候选": ", ".join(dict.fromkeys(cands)),
            "建议动作": ("不建组织ID；按人物候选消歧/合并（需核重名）" if cands
                         else "不建组织ID；人工确认自然人并补人物档案"),
            "复核理由": reason,
        })

    # 2) duplicate groups from explicit "见原清单行 X,Y"
    adj = defaultdict(set)
    for i, o in enumerate(op, 1):
        m = re.search(r"见原清单行\s*([0-9,\s]+)", o.get("reason") or "")
        if m:
            for n in re.findall(r"\d+", m.group(1)):
                n = int(n)
                if n != i:
                    adj[i].add(n); adj[n].add(i)
    seen, comps = set(), []
    for n in list(adj):
        if n in seen:
            continue
        stack = [n]; comp = set()
        while stack:
            x = stack.pop()
            if x in comp:
                continue
            comp.add(x); seen.add(x)
            stack += list(adj[x] - comp)
        comps.append(sorted(comp))
    comps.sort()

    dup_rows = []
    for gi, comp in enumerate(comps, 1):
        members = []
        for n in comp:
            r = rows[n - 1]
            members.append(r)
        best = max(members, key=lambda r: int(r["引用数"] or 0))
        for r in members:
            dup_rows.append({
                "组号": gi, "组内成员数": len(comp),
                "原清单行": comp[members.index(r)] if False else "",
                "国家": r["国家"], "冲突ID": r["冲突ID"], "现画像": r["现画像"],
                "影子名称": r["影子名称"], "引用数": r["引用数"],
                "组内主身份候选（参考）": f"{best['影子名称']} ({best['冲突ID']})",
                "建议动作": "只保留一个主身份；先统一规范名称/实体层级，本组不分配",
                "复核理由": (op[comp[0] - 1].get("reason") or "")[:500],
            })
    # fill original row correctly (members order == comp)
    k = 0
    for gi, comp in enumerate(comps, 1):
        for n in comp:
            dup_rows[k]["原清单行"] = n
            k += 1

    # CSVs
    p1 = os.path.join(OUT, "registry826_person_names_141.csv")
    with open(p1, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(people[0].keys())); w.writeheader(); w.writerows(people)
    p2 = os.path.join(OUT, "registry826_duplicate_identities_19.csv")
    with open(p2, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(dup_rows[0].keys())); w.writeheader(); w.writerows(dup_rows)

    # XLSX
    wb = Workbook()
    def sheet(title, data, widths):
        ws = wb.create_sheet(title)
        ws.append(list(data[0].keys()))
        for r in data:
            ws.append([r[k] for k in data[0]])
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = f"A1:{get_column_letter(len(data[0]))}{ws.max_row}"
        fill = PatternFill("solid", fgColor="1F4E78")
        for c in range(1, len(data[0]) + 1):
            cell = ws.cell(row=1, column=c)
            cell.font = Font(color="FFFFFF", bold=True); cell.fill = fill
        for c, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(c)].width = w
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = cell.alignment.copy(wrap_text=True, vertical="top")
        return ws

    ws0 = wb.active; ws0.title = "说明"
    ws0["A1"] = "826 条复核专项清单"
    ws0["A2"] = f"人物姓名混入组织候选：{len(people)} 条（均为不分配，不建组织ID）"
    ws0["A3"] = f"疑似重复身份：{len(comps)} 组 / {len(dup_rows)} 条（均为挂起，先统一主身份）"
    ws0["A4"] = "本文件只做分类整理，不授权分配 ID、改引用或合并画像。"
    sheet("人物姓名141", people, [10, 8, 16, 24, 42, 8, 34, 42, 80])
    sheet("重复身份19组", dup_rows, [8, 10, 10, 8, 16, 24, 42, 8, 42, 48, 80])
    wb.save(os.path.join(OUT, "registry826_special_lists.xlsx"))

    summary = {"person_names": len(people), "duplicate_groups": len(comps),
               "duplicate_rows": len(dup_rows),
               "duplicate_members": {str(g + 1): c for g, c in enumerate(comps)}}
    json.dump(summary, open(os.path.join(OUT, "registry826_special_lists_summary.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("->", p1); print("->", p2)
    print("->", os.path.join(OUT, "registry826_special_lists.xlsx"))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Reverse match report: which xlsx rows are NOT present in our social_accounts.

Direction: xlsx row -> any of our entries (URL normalized join).
Outputs: unmatched rows spreadsheet + per-country stats.
"""
import glob
import json
import os
import sys
import urllib.parse
from collections import Counter

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool"
XLSX = r"E:\WeCom\WXWork\1688851012089893\Cache\File\2026-11\重点国家人物组织-20261102.xlsx"
OUT = os.path.join(BASE, "output", "_social_audit", "xlsx_unmatched_rows.xlsx")


def norm_url(u):
    if not isinstance(u, str) or not u.strip():
        return None
    u = urllib.parse.unquote(u.strip())
    for pre in ("https://", "http://", "www."):
        if u.lower().startswith(pre):
            u = u[len(pre):]
    return u.rstrip("/").lower()


def main():
    # our side: URL -> list of entity files (only social_accounts urls)
    ours = {}
    for f in glob.glob("output/[a-z][a-z]/20*/persons/*.json") + \
             glob.glob("output/[a-z][a-z]/20*/orgs/*.json"):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for e in d.get("social_accounts") or []:
            if not isinstance(e, dict):
                continue
            k = norm_url(e.get("url"))
            if k:
                ours.setdefault(k, []).append(
                    os.path.relpath(f, "output").replace(os.sep, "/"))

    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    ws = wb["Merged Data"]
    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    print("xlsx header:", [str(h) for h in header])
    print("xlsx data rows:", len(rows) - 1)

    matched = unmatched = empty_url = 0
    by_cc = Counter()      # unmatched rows per country
    by_plat = Counter()
    unmatched_rows = []
    seen_keys = Counter()
    for r in rows[1:]:
        if not r or all(v in (None, "") for v in r):
            continue
        url = r[0]
        k = norm_url(url)
        if not k:
            empty_url += 1
            unmatched_rows.append((r, "EMPTY_URL"))
            continue
        seen_keys[k] += 1
        if k in ours:
            matched += 1
        else:
            unmatched += 1
            by_cc[str(r[1] or "").strip().upper()] += 1
            by_plat[str(r[6] or "").strip()] += 1
            unmatched_rows.append((r, "NOT_IN_DATASET"))

    print(f"\nmatched rows:   {matched}")
    print(f"unmatched rows: {unmatched} (+{empty_url} empty-url)")
    print(f"unique url keys: {len(seen_keys)} (dup rows: {len(rows)-1-len(seen_keys)})")
    print("\nunmatched by country (top 30):")
    for cc, n in by_cc.most_common(30):
        print(f"  {cc or '(blank)'}: {n}")
    print("\nunmatched by platform:", dict(by_plat.most_common()))

    # write unmatched spreadsheet
    out_wb = Workbook()
    ws2 = out_wb.active
    ws2.title = "Unmatched"
    out_wb.properties.creator = "Z.ai"
    cols = ["链接", "国家代码", "国家", "实体类型", "实体名称", "组织类型",
            "平台", "账号名称", "user_id", "username", "nickname",
            "max(create_date)", "原因"]
    ws2.append(cols)
    for c in ws2[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="4472C4")
    for (r, reason) in unmatched_rows:
        ws2.append(list(r)[:12] + [reason])
    widths = [50, 9, 10, 9, 32, 12, 11, 22, 20, 18, 22, 14, 14]
    for i, w in enumerate(widths, 1):
        ws2.column_dimensions[chr(64 + i) if i <= 26 else "A"].width = w
    ws2.freeze_panes = "A2"
    ws2.auto_filter.ref = f"A1:M{ws2.max_row}"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out_wb.save(OUT)
    print(f"\nunmatched rows written -> {OUT} ({ws2.max_row-1} rows)")

    # also per-country summary sheet
    ws3 = out_wb.create_sheet("ByCountry")
    ws3.append(["国家代码", "未匹配行数"])
    for cc, n in by_cc.most_common():
        ws3.append([cc or "(blank)", n])
    ws3.column_dimensions["A"].width = 12
    ws3.column_dimensions["B"].width = 14
    out_wb.save(OUT)


if __name__ == "__main__":
    main()

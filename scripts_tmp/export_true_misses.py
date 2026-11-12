# -*- coding: utf-8 -*-
"""Export the 125 true xlsx-miss entries (excl gn/iq/ng) to an Excel report."""
import glob
import json
import os
import sys
import urllib.parse
from collections import Counter

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding="utf-8")
XLSX = r"E:\WeCom\WXWork\1688851012089893\Cache\File\2026-11\重点国家人物组织-20261102.xlsx"
OUT = "D:/ai-workspace/apec-osint-tool/output/_social_audit/xlsx_true_misses_125.xlsx"

HOST_CANON = {
    "twitter.com": "x.com", "mobile.twitter.com": "x.com",
    "m.facebook.com": "facebook.com", "web.facebook.com": "facebook.com",
    "fb.com": "facebook.com", "m.instagram.com": "instagram.com",
    "threads.net": "threads.com", "m.youtube.com": "youtube.com",
    "m.tiktok.com": "tiktok.com",
}


def norm_url(u):
    if not isinstance(u, str) or not u.strip():
        return None
    u = urllib.parse.unquote(u.strip())
    for pre in ("https://", "http://", "www."):
        if u.lower().startswith(pre):
            u = u[len(pre):]
    host, sep, path = u.partition("/")
    host = HOST_CANON.get(host.lower(), host.lower())
    return ((host + sep + path).rstrip("/")).lower()


COVERED = {"facebook", "twitter", "instagram", "youtube", "tiktok", "threads"}
EXCLUDE = {"gn", "iq", "ng"}


def main():
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    ws = wb["Merged Data"]
    xkeys = set()
    for r in ws.iter_rows(min_row=2, values_only=True):
        k = norm_url(str(r[0])) if r and r[0] else None
        if k:
            xkeys.add(k)

    misses = []
    for f in glob.glob("output/[a-z][a-z]/20*/persons/*.json") + \
             glob.glob("output/[a-z][a-z]/20*/orgs/*.json"):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        cc = os.path.relpath(f, "output").split(os.sep)[0]
        if cc in EXCLUDE:
            continue
        kind = "person" if os.sep + "persons" + os.sep in f else "org"
        eid = os.path.splitext(os.path.basename(f))[0]
        if kind == "person":
            name = d.get("name") or "?"
            name_zh = d.get("name_zh") or ""
            title = ""
            cp = d.get("current_positions") or []
            if cp and isinstance(cp[0], dict):
                title = cp[0].get("title") or cp[0].get("position") or ""
        else:
            bi = d.get("basic_info") or {}
            name = bi.get("name_original") or "?"
            name_zh = bi.get("name_zh") or ""
            title = ""
        for e in d.get("social_accounts") or []:
            if not isinstance(e, dict):
                continue
            p = e.get("platform")
            if p not in COVERED:
                continue
            k = norm_url(e.get("url"))
            if k and k in xkeys:
                continue
            misses.append({
                "cc": cc.upper(), "kind": kind, "id": eid,
                "name": name, "name_zh": name_zh, "title": title,
                "platform": p, "account_name": e.get("account_name") or "",
                "url": e.get("url") or "",
                "source_note": (e.get("source_note") or "")[:80],
            })

    misses.sort(key=lambda m: (m["platform"], m["cc"], m["id"]))

    out = Workbook()
    ws2 = out.active
    ws2.title = "TrueMisses"
    out.properties.creator = "Z.ai"
    headers = ["国家", "类型", "实体ID", "姓名/名称", "中文名", "职务/类型",
               "平台", "账号名", "URL", "来源说明(截断)"]
    ws2.append(headers)
    for c in ws2[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="4472C4")
        c.alignment = Alignment(horizontal="center", vertical="center")
    for m in misses:
        ws2.append([m["cc"], m["kind"], m["id"], m["name"], m["name_zh"],
                    m["title"], m["platform"], m["account_name"], m["url"],
                    m["source_note"]])
    widths = [7, 8, 22, 26, 18, 24, 11, 24, 55, 42]
    for i, w in enumerate(widths, 1):
        ws2.column_dimensions[get_column_letter(i)].width = w
    ws2.freeze_panes = "A2"
    ws2.auto_filter.ref = f"A1:J{ws2.max_row}"

    # summary sheet: platform x country matrix
    ws3 = out.create_sheet("Summary")
    ws3.append(["平台", "漏网数"] + sorted({m["cc"] for m in misses}))
    cnt = Counter((m["platform"], m["cc"]) for m in misses)
    plats = sorted({m["platform"] for m in misses})
    ccs = sorted({m["cc"] for m in misses})
    for p in plats:
        row = [p, sum(cnt[(p, c)] for c in ccs)]
        row += [cnt[(p, c)] for c in ccs]
        ws3.append(row)
    ws3.append(["合计", len(misses)] + [sum(cnt[(p, c)] for p in plats) for c in ccs])
    for c in ws3[1]:
        c.font = Font(bold=True)
    ws3.column_dimensions["A"].width = 12
    ws3.column_dimensions["B"].width = 10
    for i in range(3, 3 + len(ccs)):
        ws3.column_dimensions[get_column_letter(i)].width = 6

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out.save(OUT)
    print(f"exported {len(misses)} rows -> {OUT}")
    print("by platform:", dict(Counter(m['platform'] for m in misses)))
    print("by country:", dict(Counter(m['cc'] for m in misses)))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Merge the 125-row user_id supplement xlsx into social_accounts.

Match: (entity ID, platform) first, then URL fallback. Fill nickname/username/
user_id only when currently empty; report conflicts (existing != new) without
overwriting. Idempotent.
Usage: python merge_userid_supplement.py [--dry]
"""
import glob
import json
import os
import sys
import urllib.parse

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool"
XLSX = r"E:\WeCom\WXWork\1688851012089893\Cache\File\2026-11\人物-user_id-20261112.xlsx"
DRY = "--dry" in sys.argv

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


def save_json(f, d):
    tmp = f + ".tmp"
    payload = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)
    os.replace(tmp, f)


def main():
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    ws = wb["Merged Data"]
    by_eid_plat = {}
    by_eid = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r or not r[3]:
            continue
        eid = str(r[3]).strip()
        plat = str(r[7] or "").strip().lower()
        url = str(r[0] or "").strip()
        rec = {
            "user_id": str(r[9]).strip() if r[9] not in (None, "") else None,
            "username": str(r[10]).strip() if r[10] not in (None, "") else None,
            "nickname": str(r[11]).strip() if r[11] not in (None, "") else None,
            "url_key": norm_url(url),
            "plat": plat,
        }
        by_eid_plat[(eid, plat)] = rec
        by_eid[eid] = rec

    stats = {"rows": len(by_eid_plat), "entities": 0, "filled": 0,
             "fields": 0, "conflicts": [], "unresolved": []}
    used = set()
    for f in sorted(glob.glob(os.path.join(BASE, "output", "[a-z][a-z]", "20*",
                                           "*", "*.json"))):
        rel = os.path.relpath(f, BASE).replace(os.sep, "/")
        if "/persons/" not in rel and "/orgs/" not in rel:
            continue
        eid = os.path.splitext(os.path.basename(f))[0]
        if eid not in by_eid and not any(k[0] == eid for k in by_eid_plat):
            continue
        d = json.load(open(f, encoding="utf-8"))
        sa = d.get("social_accounts") or []
        changed = False
        # xlsx rows for this entity
        my_rows = [(k[1], v) for k, v in by_eid_plat.items() if k[0] == eid]
        for plat, rec in my_rows:
            target = None
            # 1) exact URL match (same platform first, then any)
            k = rec["url_key"]
            if k:
                for e in sa:
                    if isinstance(e, dict) and (e.get("platform") or "").lower() == plat \
                            and norm_url(e.get("url")) == k:
                        target = e
                        break
                if target is None:
                    for e in sa:
                        if isinstance(e, dict) and norm_url(e.get("url")) == k:
                            target = e
                            break
            # 2) fallback: same platform entry with all three fields empty (the miss)
            if target is None:
                for e in sa:
                    if isinstance(e, dict) and (e.get("platform") or "").lower() == plat \
                            and not e.get("nickname") and not e.get("username") \
                            and not e.get("user_id"):
                        target = e
                        break
            if target is None:
                stats["unresolved"].append((eid, plat))
                continue
            used.add((eid, plat))
            stats["entities"] += 1 if not changed else 0
            for fld in ("nickname", "username", "user_id"):
                new = rec.get(fld)
                cur = target.get(fld)
                if new and not cur:
                    if not DRY:
                        target[fld] = new
                    stats["fields"] += 1
                    changed = True
                elif new and cur and str(new) != str(cur):
                    stats["conflicts"].append((rel, fld, str(cur)[:30], str(new)[:30]))
        if changed:
            stats["filled"] += 1
            if not DRY:
                save_json(f, d)
    unresolved = [k for k in by_eid_plat if k not in used]
    stats["unresolved"] = unresolved
    print(("DRY-RUN" if DRY else "APPLIED"),
          {k: (len(v) if isinstance(v, list) else v) for k, v in stats.items()})
    if stats["conflicts"]:
        print("conflicts (kept existing):")
        for c in stats["conflicts"][:10]:
            print("  ", c)
    if unresolved:
        print("unresolved xlsx rows:")
        for u in unresolved:
            print("  ", u)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""B1 batch NG social backfill updater.
- NG-PERSON-000456: add verified LinkedIn account (Innocent C. Ike, Access Holdings GMD/CEO).
- All other 24: keep social_accounts=[] and append marker sentence to collection_meta.notes.
Idempotent: guarded by marker text check.
"""
import json, os, io

BASE = r"D:\ai-workspace\apec-osint-tool\output\ng\2026-11-10\persons"
IDS = json.load(open(r"D:\ai-workspace\apec-osint-tool\scripts_tmp\_backfill_social_b1.json", encoding="utf-8"))

MARKER = "[2026-11-15 社媒补弱轮] 未找到可核实个人账号。"

NEW_ENTRY = {
    "platform": "linkedin",
    "account_name": "Innocent C. Ike. FCA, FCIB, ACS",
    "url": "https://www.linkedin.com/in/innocent-c-ike",
    "source": 17,
    "source_note": "本人实名LinkedIn账号：该账号以「Innocent C. Ike. FCA, FCIB, ACS」名义发布第一人称帖文（2025-09-04）「I am truly honoured to be back home as the Group Managing Director/CEO of Access Holdings Plc」，内容与本画像现任职务（Access控股集团董事总经理兼CEO，2025-08-29就任）及任命时间线吻合；帖文页经直连核验（HTTP 200，标题与署名一致）。BBC（2025-08-28）报道亦援引其官方LinkedIn账号。"
}

NEW_NOTE_456 = ("LinkedIn已核实并收录（见social_accounts）：该账号由本人以实名及现任职务发布第一人称帖文（2025-09-04），"
                "与BBC报道援引的「官方LinkedIn账号」相互印证。X/Twitter、Facebook、Instagram、TikTok未发现经核实的本人实名账号"
                "（各平台同名用户众多，均不采信），social_accounts仅收录LinkedIn一项。")

added, marked, skipped = 0, 0, []
report = []

for pid in IDS:
    path = os.path.join(BASE, pid + ".json")
    if not os.path.exists(path):
        report.append("%s: FILE MISSING" % pid)
        continue
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    trailing_nl = raw.endswith("\n")
    d = json.loads(raw)

    if pid == "NG-PERSON-000456":
        sa = d.setdefault("social_accounts", [])
        if not any(a.get("url") == NEW_ENTRY["url"] for a in sa):
            sa.append(dict(NEW_ENTRY))
            added += 1
        d["social_accounts_note"] = NEW_NOTE_456
        report.append("%s: ADDED linkedin innocent-c-ike (+note updated)" % pid)
    else:
        if d.get("social_accounts"):
            skipped.append(pid)
            report.append("%s: SKIP (non-empty social_accounts)" % pid)
            continue
        cm = d.get("collection_meta")
        if cm is None:
            report.append("%s: NO collection_meta" % pid)
            continue
        notes = cm.get("notes") or ""
        if MARKER.strip("。") in notes:
            report.append("%s: already marked" % pid)
            continue
        cm["notes"] = (notes.rstrip() + (" " if notes.rstrip() else "") + MARKER).strip()
        marked += 1
        report.append("%s: marker appended" % pid)

    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(d, ensure_ascii=False, indent=2))
        if trailing_nl:
            f.write("\n")

for line in report:
    print(line)
print("SUMMARY: added=%d marked=%d skipped=%s" % (added, marked, skipped))

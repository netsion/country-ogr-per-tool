# -*- coding: utf-8 -*-
"""Apply ONLY the human-reviewed 104 null + 1 replace rows (121 positions).

Guards:
  - re-reads each file and verifies current id == 核实时实际ID
  - verifies ref name (with field fallbacks) == 实际引用名称
  - replace target must exist and name-match
  - writes undo log; skips stale rows

Usage: python scripts_tmp/apply_reviewed_sample.py --dry|--apply
"""
import csv
import json
import os
import re
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, sig

CSV = os.path.join(BASE, "output", "_id_audit", "null_review_200_reviewed.csv")
REF_FIELDS = {
    "work_org": ["organization", "org_name", "organization_en"],
    "person_rel": ["person_name", "name"],
    "family": ["name", "person_name"],
    "key_people": ["name", "name_en"],
    "related_org": ["org_name", "name"],
}


def save_json(f, d):
    payload = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    tmp = f + ".tmp"
    last = None
    for _ in range(6):
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(payload)
            os.replace(tmp, f)
            return
        except PermissionError as e:
            last = e
            time.sleep(0.5)
    for _ in range(3):
        try:
            with open(f, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(payload)
            try:
                os.unlink(tmp)
            except OSError:
                pass
            return
        except PermissionError as e:
            last = e
            time.sleep(1.0)
    raise last


def ref_name(item, cat):
    for k in REF_FIELDS.get(cat, ["name"]):
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def parse_pos(s):
    m = re.match(r"^(.*)#([A-Za-z_]+)\[(\d+)\]\.([A-Za-z_]+)$", s.strip())
    if not m:
        return None
    return m.group(1), m.group(2), int(m.group(3)), m.group(4)


def find_profile(target_id):
    root = os.path.join(BASE, "output")
    cc = target_id.split("-")[0].lower()
    base = os.path.join(root, cc)
    if not os.path.isdir(base):
        return None
    for date in os.listdir(base):
        for sub in ("persons", "orgs"):
            p = os.path.join(base, date, sub, target_id + ".json")
            if os.path.exists(p):
                return p
    return None


def main():
    apply = "--apply" in sys.argv
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    actions = [r for r in rows if r["助手复核结论"] in ("建议置空", "建议改链")]
    stats = Counter()
    undo = []
    skipped = []
    docs = {}
    dirty = set()

    for r in actions:
        cat = r["类型"]
        expect_id = r["核实时实际ID"].strip()
        expect_name = r["实际引用名称"].strip()
        action = r["助手复核结论"]
        sug = r["建议正确ID"].strip() if action == "建议改链" else None

        if action == "建议改链":
            tf = find_profile(sug)
            if not tf:
                skipped.append([r["序号"], "target_not_found", sug])
                continue
            td = json.load(open(tf, encoding="utf-8"))
            bi = td.get("basic_info") or {}
            vals = [td.get("name"), td.get("name_en"), td.get("name_zh"),
                    bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")]
            vals += (td.get("aliases") or []) + (bi.get("aliases") or [])
            tsig = set()
            for v in vals:
                tsig |= sig(v)[0]
            if not (sig(expect_name)[0] & tsig):
                skipped.append([r["序号"], "target_name_mismatch", sug])
                continue

        positions = [p.strip() for p in (r["原始引用位置"] or "").split("|") if p.strip()]
        for pos in positions:
            parsed = parse_pos(pos)
            if not parsed:
                skipped.append([r["序号"], "bad_position", pos])
                continue
            rel, arr, idx, field = parsed
            f = os.path.join(BASE, rel.replace("\\", "/"))
            if not os.path.exists(f):
                skipped.append([r["序号"], "missing_file", rel])
                continue
            if f not in docs:
                docs[f] = json.load(open(f, encoding="utf-8"))
            d = docs[f]
            items = d.get(arr) or []
            if idx >= len(items) or not isinstance(items[idx], dict):
                skipped.append([r["序号"], "bad_index", pos])
                continue
            item = items[idx]
            cur = item.get(field)
            nm = ref_name(item, cat)
            if str(cur) != expect_id:
                skipped.append([r["序号"], "stale_id", f"{cur} != {expect_id}"])
                continue
            if nm != expect_name:
                skipped.append([r["序号"], "stale_name", f"{nm} != {expect_name}"])
                continue
            new = sug if action == "建议改链" else None
            undo.append({"file": rel, "array": arr, "index": idx, "field": field,
                         "old": cur, "new": new, "cat": cat, "ref_name": nm,
                         "seq": r["序号"], "action": action})
            item[field] = new
            dirty.add(f)
            stats[f"{cat}_{'replace' if new else 'null'}"] += 1

    if apply:
        for f in dirty:
            save_json(f, docs[f])
        with open(os.path.join(OUT, "step2_reviewed_undo.json"), "w", encoding="utf-8") as fh:
            json.dump(undo, fh, ensure_ascii=False, indent=1)
        with open(os.path.join(OUT, "step2_reviewed_summary.json"), "w", encoding="utf-8") as fh:
            json.dump({"mode": "apply", "action_rows": len(actions),
                       "positions": len(undo), "changed_files": len(dirty),
                       "by_cat": dict(stats), "skipped": skipped}, fh,
                      ensure_ascii=False, indent=1)
    else:
        with open(os.path.join(OUT, "step2_reviewed_undo_dry.json"), "w", encoding="utf-8") as fh:
            json.dump(undo, fh, ensure_ascii=False, indent=1)

    summary = {"mode": "apply" if apply else "dry",
               "action_rows": len(actions), "positions": len(undo),
               "changed_files": len(dirty), "by_cat": dict(stats),
               "skipped_count": len(skipped), "skipped": skipped[:100]}
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

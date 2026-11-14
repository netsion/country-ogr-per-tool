# -*- coding: utf-8 -*-
"""Apply the reviewed A+B groups from the 491-row cross-public review.

A: 19 x 置空
B: 39 x 回退 (1 profile + 38 registry-only)
Skips 348 保留 and 85 暂缓.

Usage: python scripts_tmp/apply_cross_public_review.py --dry|--apply
"""
import csv
import json
import os
import re
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT

CSV = os.path.join(OUT, "step1b_cross_public_review_reviewed.csv")
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


def main():
    apply = "--apply" in sys.argv
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    actions = [r for r in rows if r["复核结论"] in ("置空", "回退")]
    stats = Counter()
    undo = []
    skipped = []
    docs, dirty = {}, set()

    for r in actions:
        cat = r["类别"]
        action = r["复核结论"]
        new_id = r["新ID"].strip()
        old_id = r["原ID"].strip()
        expect_name = r["引用名称"].strip()
        parsed = parse_pos(r["原始引用位置"].strip())
        if not parsed:
            skipped.append([r["复核序号"], "bad_position"])
            continue
        rel, arr, idx, field = parsed
        f = os.path.join(BASE, rel.replace("\\", "/"))
        if not os.path.exists(f):
            skipped.append([r["复核序号"], "missing_file", rel])
            continue
        if f not in docs:
            docs[f] = json.load(open(f, encoding="utf-8"))
        d = docs[f]
        items = d.get(arr) or []
        if idx >= len(items) or not isinstance(items[idx], dict):
            skipped.append([r["复核序号"], "bad_index", r["原始引用位置"]])
            continue
        item = items[idx]
        cur = item.get(field)
        nm = ref_name(item, cat)
        if str(cur) != new_id:
            skipped.append([r["复核序号"], "stale_id", f"{cur} != {new_id}"])
            continue
        if nm != expect_name:
            skipped.append([r["复核序号"], "stale_name", f"{nm} != {expect_name}"])
            continue
        new = old_id if action == "回退" else None
        undo.append({"file": rel, "array": arr, "index": idx, "field": field,
                     "old": cur, "new": new, "cat": cat, "ref_name": nm,
                     "seq": r["复核序号"], "action": action})
        item[field] = new
        dirty.add(f)
        stats[f"{cat}_{action}"] += 1

    if apply:
        for f in dirty:
            save_json(f, docs[f])
        with open(os.path.join(OUT, "cross_public_undo.json"), "w", encoding="utf-8") as fh:
            json.dump(undo, fh, ensure_ascii=False, indent=1)
        with open(os.path.join(OUT, "cross_public_apply_summary.json"), "w",
                  encoding="utf-8") as fh:
            json.dump({"mode": "apply", "action_rows": len(actions),
                       "positions": len(undo), "changed_files": len(dirty),
                       "by_cat": dict(stats), "skipped": skipped}, fh,
                      ensure_ascii=False, indent=1)
    else:
        with open(os.path.join(OUT, "cross_public_undo_dry.json"), "w", encoding="utf-8") as fh:
            json.dump(undo, fh, ensure_ascii=False, indent=1)

    print(json.dumps({"mode": "apply" if apply else "dry",
                      "action_rows": len(actions), "positions": len(undo),
                      "changed_files": len(dirty), "by_cat": dict(stats),
                      "skipped_count": len(skipped), "skipped": skipped[:50]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

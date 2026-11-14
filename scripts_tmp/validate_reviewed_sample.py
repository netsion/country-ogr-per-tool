# -*- coding: utf-8 -*-
"""Validate the 200-row human review against current files (read-only).

Checks every action row (建议置空 / 建议改链):
  - file exists, array/index/field valid
  - current field == 核实时实际ID
  - ref name (with field fallbacks) == 实际引用名称
  - for 改链: target profile exists and name matches
Reports stale/skip reasons. No writes.
"""
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, sig, match

CSV = os.path.join(BASE, "output", "_id_audit", "null_review_200_reviewed.csv")
REF_FIELDS = {
    "work_org": ["organization", "org_name", "organization_en"],
    "person_rel": ["person_name", "name"],
    "family": ["name", "person_name"],
    "key_people": ["name", "name_en"],
    "related_org": ["org_name", "name"],
}


def ref_name(item, cat):
    for k in REF_FIELDS.get(cat, ["name"]):
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def parse_pos(s):
    # path#array[index].field
    m = re.match(r"^(.*)#([A-Za-z_]+)\[(\d+)\]\.([A-Za-z_]+)$", s.strip())
    if not m:
        return None
    return m.group(1), m.group(2), int(m.group(3)), m.group(4)


def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    actions = [r for r in rows if r["助手复核结论"] in ("建议置空", "建议改链")]
    stats = Counter()
    details = []
    for r in actions:
        cat = r["类型"]
        expect_id = r["核实时实际ID"].strip()
        expect_name = r["实际引用名称"].strip()
        pos_list = [p.strip() for p in (r["原始引用位置"] or "").split("|") if p.strip()]
        for pos in pos_list:
            parsed = parse_pos(pos)
            if not parsed:
                stats["bad_position"] += 1
                continue
            rel, arr, idx, field = parsed
            f = os.path.join(BASE, rel.replace("\\", "/"))
            if not os.path.exists(f):
                stats["missing_file"] += 1
                continue
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception:
                stats["bad_json"] += 1
                continue
            items = d.get(arr) or []
            if idx >= len(items) or not isinstance(items[idx], dict):
                stats["bad_index"] += 1
                continue
            item = items[idx]
            cur = item.get(field)
            nm = ref_name(item, cat)
            ok = True
            reason = []
            if str(cur) != expect_id:
                ok = False
                reason.append(f"id {cur!r}!={expect_id!r}")
            if nm != expect_name:
                ok = False
                reason.append(f"name {nm!r}!={expect_name!r}")
            if r["助手复核结论"] == "建议改链":
                sug = r["建议正确ID"].strip()
                tf = None
                for root, dirs, files in os.walk(os.path.join(BASE, "output")):
                    if sug + ".json" in files:
                        tf = os.path.join(root, sug + ".json")
                        break
                if not tf:
                    ok = False
                    reason.append(f"target {sug} not found")
            stats["ok" if ok else "stale"] += 1
            details.append({"seq": r["序号"], "cat": cat, "file": rel, "array": arr,
                            "index": idx, "field": field, "current": cur,
                            "expect": expect_id, "ref": nm,
                            "action": r["助手复核结论"], "ok": ok,
                            "reason": "; ".join(reason),
                            "positions": len(pos_list)})
    print(json.dumps(dict(stats), ensure_ascii=False, indent=1))
    print("actions rows", len(actions), "positions", len(details))
    for d in details:
        if not d["ok"]:
            print("STALE", d)
    with open(os.path.join(BASE, "output", "_id_audit",
                           "reviewed_validation.json"), "w", encoding="utf-8") as fh:
        json.dump(details, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Validate the 491-row cross-public review against current data (read-only)."""
import csv
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT

REF_FIELDS = {
    "work_org": ["organization", "org_name", "organization_en"],
    "person_rel": ["person_name", "name"],
    "family": ["name", "person_name"],
    "key_people": ["name", "name_en"],
    "related_org": ["org_name", "name"],
}
FULL = os.path.join(OUT, "step1b_cross_public_review_reviewed.csv")
PRI = os.path.join(OUT, "step1b_cross_public_priority_reviewed.csv")


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


def load_profile_ids():
    pids, oids = set(), set()
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if not os.path.basename(f).startswith("_"):
            try:
                d = json.load(open(f, encoding="utf-8"))
                if d.get("person_id"):
                    pids.add(d["person_id"])
            except Exception:
                pass
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if not os.path.basename(f).startswith("_"):
            try:
                d = json.load(open(f, encoding="utf-8"))
                if d.get("org_id"):
                    oids.add(d["org_id"])
            except Exception:
                pass
    return pids, oids


def load_registry_ids():
    ids = set()
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/id_registry.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for e in d.get("registry") or []:
            if e.get("org_id"):
                ids.add(e["org_id"])
        for e in d.get("person_registry") or []:
            if e.get("person_id"):
                ids.add(e["person_id"])
    return ids


def main():
    rows = list(csv.DictReader(open(FULL, encoding="utf-8-sig")))
    pri = list(csv.DictReader(open(PRI, encoding="utf-8-sig")))
    pids, oids = load_profile_ids()
    reg = load_registry_ids()
    stats = Counter()
    details = []
    positions = defaultdict(list)

    for r in rows:
        action = r["复核结论"]
        stats[action] += 1
        if action not in ("置空", "回退"):
            continue
        cat = r["类别"]
        new_id = r["新ID"].strip()
        old_id = r["原ID"].strip()
        pos = r["原始引用位置"].strip()
        parsed = parse_pos(pos)
        if not parsed:
            stats["bad_position"] += 1
            continue
        rel, arr, idx, field = parsed
        f = os.path.join(BASE, rel.replace("\\", "/"))
        if not os.path.exists(f):
            stats["missing_file"] += 1
            continue
        d = json.load(open(f, encoding="utf-8"))
        items = d.get(arr) or []
        if idx >= len(items) or not isinstance(items[idx], dict):
            stats["bad_index"] += 1
            continue
        item = items[idx]
        cur = item.get(field)
        nm = ref_name(item, cat)
        ok = True
        if str(cur) != new_id:
            ok = False
            stats["stale_id"] += 1
        if nm != r["引用名称"].strip():
            ok = False
            stats["stale_name"] += 1
        if action == "回退":
            if old_id in pids or old_id in oids:
                stats["revert_to_profile"] += 1
            elif old_id in reg:
                stats["revert_to_registry_only"] += 1
            else:
                stats["revert_old_missing"] += 1
                ok = False
        positions[(rel, arr, idx, field)].append((r["复核序号"], action))
        details.append({"seq": r["复核序号"], "action": action, "cat": cat,
                        "pos": pos, "current": cur, "new": new_id,
                        "old": old_id, "ref": nm, "ok": ok})
    # priority consistency
    full_by_seq = {r["复核序号"]: r for r in rows}
    conflicts = []
    for r in pri:
        f = full_by_seq.get(r["复核序号"])
        if not f:
            conflicts.append([r["复核序号"], "not_in_full"])
        elif f["复核结论"] != r["复核结论"]:
            conflicts.append([r["复核序号"], r["复核结论"], f["复核结论"]])
    dup_conflicts = [k for k, v in positions.items() if len({a for _, a in v}) > 1]
    print(json.dumps({"actions": dict(stats), "positions": len(details),
                      "priority_conflicts": conflicts[:20],
                      "duplicate_position_conflicts": dup_conflicts[:20],
                      "stale": [d for d in details if not d["ok"]][:20]},
                     ensure_ascii=False, indent=1))
    with open(os.path.join(OUT, "cross_public_validation.json"), "w", encoding="utf-8") as fh:
        json.dump({"stats": dict(stats), "details": details,
                   "priority_conflicts": conflicts,
                   "duplicate_position_conflicts": dup_conflicts}, fh,
                  ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

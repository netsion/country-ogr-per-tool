# -*- coding: utf-8 -*-
"""P2 batch 1: apply only manually approved strict exact relinks.

Approved = current ID is an unrelated profile or a dangling ID, while the
target profile name matches the reference exactly (or is the same renamed /
historical body). Deferred/Rejected rows are recorded but not changed.

Usage: python scripts_tmp/p2_batch1_apply.py --dry|--apply
"""
import csv
import json
import os
import sys
import time
from collections import Counter, defaultdict

BASE = "D:/ai-workspace/apec-osint-tool"
OUT = os.path.join(BASE, "output/_id_audit")
PLAN = os.path.join(OUT, "p2_strict_plan.csv")

APPROVE = {
    ("work_org", "JP-FIN-003", "JP-FIN-050"),
    ("work_org", "MX-GOV-033", "MX-GOV-878"),
    ("work_org", "MX-GOV-039", "MX-GOV-896"),
    ("work_org", "MX-GOV-088", "MX-GOV-878"),
    ("work_org", "MX-GOV-629", "MX-GOV-878"),
    ("work_org", "MX-GOV-674", "MX-GOV-878"),
    ("work_org", "MY-GOV-009", "MY-GOV-011"),
    ("work_org", "MY-ORG-000001", "MY-PARTY-004"),
    ("work_org", "NZ-GOV-019", "NZ-GOV-067"),
    ("work_org", "NZ-GOV-007", "NZ-GOV-067"),
    ("work_org", "NZ-GOV-018", "NZ-GOV-152"),
    ("work_org", "US-INTL-004", "US-INTL-005"),
    ("work_org", "US-FIN-017", "US-FIN-021"),
    ("related_org", "MA-CORP-006", "MA-CORP-089"),
    ("related_org", "MA-CORP-090", "MA-CORP-089"),
    ("related_org", "MY-GOV-MOF-EPF", "MY-SOE-004"),
    ("related_org", "SG-PARTY-001", "SG-PARTY-004"),
    ("related_org", "US-FIN-003", "US-FIN-021"),
    ("related_org", "US-FIN-017", "US-FIN-021"),
    ("related_org", "US-INTL-004", "US-INTL-005"),
}

DEFER = {
    ("work_org", "KW-PARTY-010", "KW-PARTY-007"): "faction name differs; confirm whether same party",
    ("work_org", "LB-PARTY-029", "LB-PARTY-013"): "faction name differs; confirm whether same party",
    ("work_org", "VN-GOV-079", "VN-CORP-005"): "composite/parent-subsidiary reference",
}

REJECT = {
    ("work_org", "TD-GOV-008", "TD-GOV-011"): "country mismatch: ref says Equatorial Guinea, target is Chad",
    ("work_org", "VN-GOV-207", "VN-MEDIA-001"): "composite ref: VNA + Ha Bac Fertilizer",
    ("work_org", "VN-CORP-007", "VN-PARTY-001"): "local party committee, not central party",
    ("work_org", "VN-CORP-002", "VN-MEDIA-001"): "composite ref: VNA + FPT Internet Center",
    ("work_org", "VN-GOV-021", "VN-ACAD-005"): "composite ref: aviation academy + VIB",
}


def save_json(path, obj):
    payload = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    tmp = path + ".tmp"
    last = None
    for _ in range(6):
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(payload)
            os.replace(tmp, path)
            return
        except PermissionError as e:
            last = e
            time.sleep(0.5)
    for _ in range(3):
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
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


def ref_name(item):
    for k in ("organization", "org_name", "organization_en", "company", "name", "name_en"):
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def main():
    apply = "--apply" in sys.argv
    rows = list(csv.DictReader(open(PLAN, encoding="utf-8-sig")))
    decisions = []
    for r in rows:
        key = (r["direction"], r["current_id"], r["target_id"])
        if key in APPROVE:
            decision, reason = "approve", "strict name match; current ID unrelated or dangling"
        elif key in DEFER:
            decision, reason = "defer", DEFER[key]
        elif key in REJECT:
            decision, reason = "reject", REJECT[key]
        else:
            decision, reason = "defer", "not in approved subset"
        rr = dict(r)
        rr["decision"] = decision
        rr["reason"] = reason
        decisions.append(rr)

    dpath = os.path.join(OUT, "p2_batch1_decisions.csv")
    with open(dpath, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(decisions[0].keys()))
        w.writeheader()
        w.writerows(decisions)

    by_file = defaultdict(list)
    for r in decisions:
        if r["decision"] != "approve":
            continue
        by_file[r["file"]].append(r)

    undo = []
    stats = Counter()
    for rel, items in sorted(by_file.items()):
        fp = os.path.join(BASE, rel)
        data = json.load(open(fp, encoding="utf-8"))
        dirty = False
        for r in items:
            arr = data.get(r["array"]) or []
            i = int(r["index"])
            if i >= len(arr) or not isinstance(arr[i], dict):
                stats["position_missing"] += 1
                continue
            item = arr[i]
            if item.get("org_id") != r["current_id"] or ref_name(item) != r["ref_name"]:
                stats["position_changed"] += 1
                continue
            undo.append({
                "file": rel, "array": r["array"], "index": i, "field": "org_id",
                "old": item.get("org_id"), "new": r["target_id"],
                "ref_name": r["ref_name"], "target_name": r["target_name"],
            })
            item["org_id"] = r["target_id"]
            dirty = True
            stats["refs_changed"] += 1
            stats[f"refs_{r['direction']}"] += 1
        if apply and dirty:
            save_json(fp, data)

    summary = {
        "apply": apply,
        "rows": len(decisions),
        "approved_rows": sum(1 for r in decisions if r["decision"] == "approve"),
        "deferred_rows": sum(1 for r in decisions if r["decision"] == "defer"),
        "rejected_rows": sum(1 for r in decisions if r["decision"] == "reject"),
        "refs_changed": stats["refs_changed"],
        "by_direction": {k: stats[f"refs_{k}"] for k in ("work_org", "related_org")},
        "position_missing": stats["position_missing"],
        "position_changed": stats["position_changed"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if apply:
        p = os.path.join(OUT, "p2_batch1_undo.json")
        json.dump({"summary": summary, "changes": undo}, open(p, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("undo ->", p)
        print("decisions ->", dpath)
    else:
        print("DRY")


if __name__ == "__main__":
    main()

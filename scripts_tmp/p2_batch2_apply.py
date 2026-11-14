# -*- coding: utf-8 -*-
"""P2 batch 2: cross-country exact brands/institutions + same-country person relink.

Only 34 candidates survive the type filter; decisions are manual:
  - cross-country GOV/MIL/PARTY and generic media are excluded
  - composite refs remain rejected/deferred
"""
import csv
import glob
import json
import os
import sys
import time
from collections import Counter, defaultdict

BASE = "D:/ai-workspace/apec-osint-tool"
OUT = os.path.join(BASE, "output/_id_audit")
PLAN = os.path.join(OUT, "p2_strict2_plan.csv")
ALLOWED = {"CORP", "FIN", "SOE", "ACAD", "MEDIA", "NGO", "INTL"}

APPROVE = {
    ("work_org", "BF-INTL-002", "US-INTL-024"),
    ("work_org", "JP-GOV-655", "AU-GOV-543"),
    ("work_org", "MX-GOV-247", "AU-GOV-075"),
    ("work_org", "MX-GOV-269", "AU-GOV-075"),
    ("work_org", "PH-CORP-004", "AU-GOV-075"),
    ("work_org", "VN-GOV-064", "AU-GOV-075"),
    ("related_org", "AE-ACAD-016", "KR-ACAD-026"),
    ("related_org", "BH-GOV-021", "SA-SOE-005"),
    ("related_org", "CA-ACAD-016", "AU-GOV-090"),
    ("related_org", "CI-SOE-007", "US-INTL-024"),
    ("related_org", "CL-INTL-010", "AU-GOV-543"),
    ("related_org", "JP-ACAD-023", "KR-ACAD-024"),
    ("related_org", "KR-INTL-006", "US-INTL-005"),
    ("related_org", "PG-ACAD-001", "AU-GOV-090"),
    ("related_org", "PH-FIN-038", "JP-FIN-050"),
    ("related_org", "US-university-003", "KR-ACAD-026"),
    ("related_org", "US-INTL-007", "AU-GOV-543"),
    ("person_rel", "MX-PERSON-000104", "MX-PERSON-000154"),
}

DEFER = {
    ("work_org", "KW-PARTY-010", "KW-PARTY-007"): "faction name differs",
    ("work_org", "LB-PARTY-029", "LB-PARTY-013"): "faction name differs",
    ("work_org", "VN-GOV-079", "VN-CORP-005"): "parent/subsidiary",
}

REJECT = {
    ("work_org", "LB-MEDIA-015", "BO-MEDIA-004"): "generic 日报; Latin names L'Orient-Le Jour vs El Diario",
    ("work_org", "MX-GOV-382", "MA-MEDIA-029"): "generic 新闻报; La Jornada vs Al Akhbar",
    ("work_org", "VN-GOV-207", "VN-MEDIA-001"): "composite VNA + Ha Bac",
    ("work_org", "VN-CORP-007", "VN-PARTY-001"): "local party committee",
    ("work_org", "VN-CORP-002", "VN-MEDIA-001"): "composite VNA + FPT",
    ("work_org", "VN-GOV-021", "VN-ACAD-005"): "composite aviation academy + VIB",
}


def save_json(path, obj):
    payload = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    tmp = path + ".tmp"
    for _ in range(6):
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(payload)
            os.replace(tmp, path)
            return
        except PermissionError:
            time.sleep(0.5)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)


def profile_type(oid):
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs", oid + ".json")):
        d = json.load(open(f, encoding="utf-8"))
        return (d.get("basic_info") or {}).get("org_type")
    return None


def ref_name(item):
    for k in ("organization", "org_name", "organization_en", "company", "person_name", "name", "name_en"):
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def main():
    apply = "--apply" in sys.argv
    rows = list(csv.DictReader(open(PLAN, encoding="utf-8-sig")))
    candidates = []
    for r in rows:
        if r["direction"] == "person_rel":
            eligible = r["target_cc"] == r["cc"]
            typ = "person"
        else:
            typ = profile_type(r["target_id"])
            eligible = r["target_cc"] == r["cc"] or typ in ALLOWED
        if not eligible:
            continue
        key = (r["direction"], r["current_id"], r["target_id"])
        if key in APPROVE:
            decision, reason = "approve", "strict exact; target is the correct entity"
        elif key in DEFER:
            decision, reason = "defer", DEFER[key]
        elif key in REJECT:
            decision, reason = "reject", REJECT[key]
        else:
            decision, reason = "defer", "not manually approved"
        rr = dict(r)
        rr["target_type"] = typ
        rr["decision"] = decision
        rr["reason"] = reason
        candidates.append(rr)

    dpath = os.path.join(OUT, "p2_batch2_decisions.csv")
    with open(dpath, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(candidates[0].keys()))
        w.writeheader()
        w.writerows(candidates)

    by_file = defaultdict(list)
    for r in candidates:
        if r["decision"] == "approve":
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
            field = "person_id" if r["direction"] in ("person_rel", "family", "key_people") else "org_id"
            if item.get(field) != r["current_id"] or ref_name(item) != r["ref_name"]:
                stats["position_changed"] += 1
                continue
            undo.append({
                "file": rel, "array": r["array"], "index": i, "field": field,
                "old": item.get(field), "new": r["target_id"],
                "ref_name": r["ref_name"], "target_name": r["target_name"],
                "direction": r["direction"],
            })
            item[field] = r["target_id"]
            dirty = True
            stats["refs_changed"] += 1
            stats[f"refs_{r['direction']}"] += 1
        if apply and dirty:
            save_json(fp, data)

    summary = {
        "apply": apply,
        "candidates": len(candidates),
        "approved_rows": sum(1 for r in candidates if r["decision"] == "approve"),
        "deferred_rows": sum(1 for r in candidates if r["decision"] == "defer"),
        "rejected_rows": sum(1 for r in candidates if r["decision"] == "reject"),
        "refs_changed": stats["refs_changed"],
        "by_direction": {k: stats[f"refs_{k}"] for k in ("work_org", "related_org", "person_rel")},
        "position_missing": stats["position_missing"],
        "position_changed": stats["position_changed"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if apply:
        p = os.path.join(OUT, "p2_batch2_undo.json")
        json.dump({"summary": summary, "changes": undo}, open(p, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("undo ->", p)
        print("decisions ->", dpath)
    else:
        print("DRY")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""P2 batch 2 read-only plan: strict exact relinks across org/person directions.

Extends batch 1 to:
  - org directions with global scope (cross-country exact brand/org only)
  - person_relationships, family_members, key_people (same-country target only)

Still requires a target profile, strict primary/full/Latin name match, exact
live array position, and no alias matching.
"""
import csv
import glob
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from id_integrity_audit2 import BASE, OUT, load_datasets
from p2_plan_strict import clean, core, latin_parts, strict_match


def org_names(p):
    bi = p.get("basic_info") or {}
    return [v.strip() for v in (bi.get("name_zh"), bi.get("name_en"), bi.get("name_original"))
            if isinstance(v, str) and v.strip()]


def person_names(p):
    bi = p.get("basic_info") or {}
    vals = [p.get("name"), p.get("name_en"), p.get("name_zh"), p.get("name_original"),
            bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")]
    return [v.strip() for v in vals if isinstance(v, str) and v.strip()]


def get_name(item, direction):
    keys = {
        "work_org": ("organization", "org_name", "organization_en"),
        "related_org": ("org_name", "name", "organization"),
        "person_rel": ("person_name", "name"),
        "family": ("name", "person_name"),
        "key_people": ("name", "name_en", "person_name"),
    }[direction]
    for k in keys:
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def main():
    latest, _ = load_datasets()
    cand = json.load(open(os.path.join(OUT, "repair_candidates.json"), encoding="utf-8"))

    org_profiles = {}
    person_profiles = {}
    for cc, (date, folder) in latest.items():
        for f in glob.glob(os.path.join(folder, "orgs", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            p = json.load(open(f, encoding="utf-8"))
            oid = p.get("org_id")
            if oid:
                org_profiles[oid] = {"profile": p, "names": org_names(p), "cc": cc}
        for f in glob.glob(os.path.join(folder, "persons", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            p = json.load(open(f, encoding="utf-8"))
            pid = p.get("person_id")
            if pid:
                person_profiles[pid] = {"profile": p, "names": person_names(p), "cc": cc}

    config = {
        "work_org": ("persons", "work_experience", "org_id", "org"),
        "related_org": ("orgs", "related_entities", "org_id", "org"),
        "person_rel": ("persons", "person_relationships", "person_id", "person"),
        "family": ("persons", "family_members", "person_id", "person"),
        "key_people": ("orgs", "key_people", "person_id", "person"),
    }

    rows = []
    skipped = Counter()
    for direction, (subdir, arr_name, field, target_kind) in config.items():
        for r in cand.get(direction, []):
            if r.get("action") != "replace" or r.get("suggest_status") != "unique":
                continue
            target = r.get("suggested")
            if target_kind == "org":
                if r.get("scope") not in ("same_cc", "global"):
                    skipped["bad_scope"] += 1
                    continue
                if target not in org_profiles:
                    skipped["target_no_profile"] += 1
                    continue
                tnames = org_profiles[target]["names"]
                current = r.get("org_id") if direction == "work_org" else r.get("org_id_ref")
            else:
                # person targets: first batch stays same-country to limit false links
                if not target or target[:2].lower() != r.get("cc"):
                    skipped["person_not_same_cc"] += 1
                    continue
                if target not in person_profiles:
                    skipped["target_no_profile"] += 1
                    continue
                tnames = person_profiles[target]["names"]
                current = r.get("person_id_ref")

            if not target or target == current:
                skipped["self"] += 1
                continue
            ref = r.get("organization") if direction == "work_org" else r.get("ref_name")
            kind = strict_match(ref, tnames)
            if not kind:
                skipped["strict_name_no_match"] += 1
                continue

            cc = r.get("cc")
            folder = latest.get(cc, (None, None))[1]
            if not folder:
                skipped["no_dataset"] += 1
                continue
            src_id = r.get("org_id") if direction in ("related_org", "key_people") else r.get("person_id")
            src_file = os.path.join(folder, subdir, str(src_id) + ".json")
            if not os.path.exists(src_file):
                skipped["source_file_missing"] += 1
                continue
            data = json.load(open(src_file, encoding="utf-8"))
            found = 0
            for i, item in enumerate(data.get(arr_name) or []):
                if not isinstance(item, dict):
                    continue
                if item.get(field) != current:
                    continue
                if get_name(item, direction) != ref:
                    continue
                found += 1
                rows.append({
                    "direction": direction,
                    "cc": cc,
                    "file": os.path.relpath(src_file, BASE).replace(os.sep, "/"),
                    "array": arr_name,
                    "index": i,
                    "source_id": src_id,
                    "ref_name": ref,
                    "current_id": current,
                    "target_id": target,
                    "target_name": (tnames[0] if tnames else ""),
                    "target_cc": target[:2].lower(),
                    "match_kind": kind,
                    "issue": r.get("issue"),
                })
            if not found:
                skipped["position_not_found"] += 1

    seen = set()
    unique = []
    for r in rows:
        key = (r["file"], r["array"], r["index"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(r)
    rows = unique

    # sample: up to 25 per direction
    sample = []
    for direction in config:
        sample += [r for r in rows if r["direction"] == direction][:25]
    sample = sample[:100]

    plan_path = os.path.join(OUT, "p2_strict2_plan.csv")
    with open(plan_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    sample_path = os.path.join(OUT, "p2_strict2_sample.csv")
    with open(sample_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(sample)

    summary = {
        "rows": len(rows),
        "by_direction": dict(Counter(r["direction"] for r in rows)),
        "by_match_kind": dict(Counter(r["match_kind"] for r in rows)),
        "by_issue": dict(Counter(r["issue"] for r in rows)),
        "by_scope": dict(Counter("same_cc" if r["target_cc"] == r["cc"] else "global" for r in rows)),
        "skipped": dict(skipped),
        "sample": len(sample),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    json.dump({"summary": summary, "rows": rows, "sample": sample},
              open(os.path.join(OUT, "p2_strict2_plan.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("plan ->", plan_path)
    print("sample ->", sample_path)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""P1 low-risk metadata cleanup.

1. Fix registry names polluted as "None (Actual Name)" -> "Actual Name".
2. Fill six org profiles whose basic_info has no name at all.
3. Sync org/person _index.json: add missing profiles, remove stale entries,
   fix blank/wrong display names, set total_profiles.
4. Emit a QID review CSV; do NOT clear QIDs automatically.
5. Rebuild _name_index.json for datasets whose registry/profile names changed.

Usage: python scripts_tmp/p1_apply.py --dry|--apply
"""
import csv
import glob
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from p1_audit2 import org_index_entry, person_index_entry, norm, BASE, OUT

IDX_AUDIT = os.path.join(OUT, "p1_audit.json")
GEN = os.path.join(BASE, ".agents/skills/country-org-collector/scripts/generate_name_index.py")
REG_NAME_RE = re.compile(r"^\s*None\s*\((.*)\)\s*$", re.I)


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


# Six profiles have basic_info names all null; use the meaningful part of
# the old registry name "None (Actual Name)".
PROFILE_NAMES = {
    "DZ-NGO-005": "Rassemblement Actions Jeunesse",
    "LA-FIN-006": "Lao-Viet Bank",
    "TN-CORP-006": "Carthage Power Company",
    "TN-FIN-017": "Banque tuniso-libyenne",
    "TN-SOE-005": "Tunisian Chemical Group (GCT)",
    "TN-SOE-017": "National Real Estate Company of Tunisia (SNIT)",
}


def find_profile(oid):
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs", oid + ".json")):
        return f
    return None


def main():
    apply = "--apply" in sys.argv
    plan = json.load(open(IDX_AUDIT, encoding="utf-8"))
    undo = {"registry_names": [], "profiles": [], "index": [], "name_indexes": [], "qid_review": []}
    stats = Counter()

    # 1) Registry name cleanup.
    changed_reg_dirs = set()
    for rp in sorted(glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/id_registry.json"))):
        reg = json.load(open(rp, encoding="utf-8"))
        changed = False
        for e in reg.get("registry") or []:
            old = e.get("name")
            m = REG_NAME_RE.match(old or "")
            if not m:
                continue
            new = m.group(1).strip()
            if not new or new.lower() in ("none", "null", "n/a", "()"):
                continue
            e["name"] = new
            changed = True
            stats["registry_names_fixed"] += 1
            undo["registry_names"].append({
                "file": os.path.relpath(rp, BASE).replace(os.sep, "/"),
                "id": e.get("org_id") or e.get("person_id"),
                "old": old, "new": new,
            })
        if changed:
            changed_reg_dirs.add(os.path.dirname(rp))
            if apply:
                save_json(rp, reg)

    # 2) Fill six nameless profiles.
    for oid, name in PROFILE_NAMES.items():
        fp = find_profile(oid)
        if not fp:
            stats["profile_not_found"] += 1
            continue
        p = json.load(open(fp, encoding="utf-8"))
        bi = p.setdefault("basic_info", {})
        old = {k: bi.get(k) for k in ("name_original", "name_en", "name_zh")}
        if any(isinstance(bi.get(k), str) and bi.get(k).strip() for k in ("name_original", "name_en", "name_zh")):
            stats["profiles_already_named"] += 1
            continue
        bi["name_original"] = name
        bi["name_en"] = name
        bi["name_zh"] = None
        stats["profiles_named"] += 1
        undo["profiles"].append({"file": os.path.relpath(fp, BASE).replace(os.sep, "/"),
                                 "id": oid, "old": old, "new": {"name_original": name, "name_en": name, "name_zh": None}})
        if apply:
            save_json(fp, p)

    # 3) Index sync.
    by_path = {}
    for kind in ("org", "person"):
        for row in plan["index_plan"].get(kind, []):
            by_path.setdefault(row["path"], []).append((kind, row))

    for path, rows in sorted(by_path.items()):
        idx = json.load(open(path, encoding="utf-8"))
        key = "person_id" if any(k == "person" for k, _ in rows) else "org_id"
        entries = idx.setdefault("profiles", [])
        before = len(entries)
        changed = False
        # map current entries; preserve first if duplicate
        by_id = {}
        for e in entries:
            eid = e.get(key)
            if eid and eid not in by_id:
                by_id[eid] = e
        # reconcile with actual local files
        d = os.path.dirname(path)
        files = {}
        for f in glob.glob(os.path.join(d, "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            p = json.load(open(f, encoding="utf-8"))
            pid = p.get(key)
            if pid:
                files[pid] = p
        for kind, row in rows:
            action = row["action"]
            oid = row["id"]
            if oid not in files:
                # stale or already absent; remove any entry with this ID
                if oid in by_id:
                    entries[:] = [e for e in entries if e.get(key) != oid]
                    by_id.pop(oid, None)
                    changed = True
                    stats["index_removed"] += 1
                    undo["index"].append({"path": path, "action": "remove", "id": oid})
                continue
            if action == "add":
                if oid not in by_id:
                    entry = person_index_entry(files[oid]) if kind == "person" else org_index_entry(files[oid])
                    entries.append(entry)
                    by_id[oid] = entry
                    changed = True
                    stats["index_added"] += 1
                    undo["index"].append({"path": path, "action": "add", "id": oid, "entry": entry})
                continue
            if action in ("fix_name", "dedupe_index"):
                e = by_id.get(oid)
                if e is None:
                    continue
                if kind == "org":
                    new_name = (org_index_entry(files[oid]) or {}).get("name")
                    if new_name and e.get("name") != new_name:
                        old = e.get("name")
                        e["name"] = new_name
                        changed = True
                        stats["index_names_fixed"] += 1
                        undo["index"].append({"path": path, "action": "fix_name", "id": oid,
                                              "old": old, "new": new_name})
                else:
                    # fill missing person display name from profile
                    pe = person_index_entry(files[oid])
                    old = {k: e.get(k) for k in ("name_en", "name_zh")}
                    if not norm(e.get("name_en")) and not norm(e.get("name_zh")):
                        for k in ("name_en", "name_zh", "wikidata_qid", "gender",
                                  "importance_level", "current_title", "completeness_score", "file"):
                            if pe.get(k) is not None:
                                e[k] = pe.get(k)
                        changed = True
                        stats["index_names_fixed"] += 1
                        undo["index"].append({"path": path, "action": "fix_person", "id": oid,
                                              "old": old, "new": {"name_en": e.get("name_en"),
                                                                  "name_zh": e.get("name_zh")}})
            # remove duplicate entries with same ID, keep first
            dups = [e for e in entries if e.get(key) == oid]
            if len(dups) > 1:
                keep = dups[0]
                entries[:] = [e for e in entries if e.get(key) != oid or e is keep]
                by_id[oid] = keep
                changed = True
                stats["index_deduped"] += 1

        if changed:
            # preserve deterministic order by ID
            entries.sort(key=lambda e: e.get(key, ""))
            idx["profiles"] = entries
            idx["total_profiles"] = len(entries)
            stats["index_files_changed"] += 1
            undo["index"].append({"path": path, "action": "set_total",
                                  "before": before, "after": len(entries)})
            if apply:
                save_json(path, idx)

    # 4) QID review CSV — no data change.
    qrows = []
    for kind in ("person", "org"):
        for g in plan["qid_dups"].get(kind, []):
            qrows.append({
                "kind": kind,
                "qid": g["qid"],
                "count": g["count"],
                "classification": "duplicate_profiles_same_name" if g["same_name"] else "different_or_variant_review",
                "ids": "|".join(g["ids"]),
                "names": "|".join(g["names"]),
                "locations": "|".join(g["locations"]),
            })
    qpath = os.path.join(OUT, "p1_qid_review.csv")
    if apply:
        with open(qpath, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(qrows[0].keys()))
            w.writeheader()
            w.writerows(qrows)
    undo["qid_review"] = qrows

    # 5) Rebuild name indexes for changed registry/profile datasets.
    rebuild_dirs = sorted(changed_reg_dirs)
    # add dirs for profiles changed
    for row in undo["profiles"]:
        p = os.path.join(BASE, row["file"])
        rebuild_dirs.append(os.path.dirname(os.path.dirname(p)))
    rebuild_dirs = sorted(set(rebuild_dirs))
    print("name-index rebuild dirs:", len(rebuild_dirs))
    if apply:
        for d in rebuild_dirs:
            # d is the dataset folder; never touch an active collection
            if not os.path.isdir(d) or os.path.exists(os.path.join(d, ".inflight")):
                stats["name_index_skipped_inflight"] += 1
                undo["name_indexes"].append({"dir": os.path.relpath(d, BASE).replace(os.sep, "/"),
                                             "ok": False, "skipped_inflight": True})
                continue
            r = subprocess.run([sys.executable, GEN, d], capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            ok = r.returncode == 0
            stats["name_index_rebuilt" if ok else "name_index_failed"] += 1
            undo["name_indexes"].append({"dir": os.path.relpath(d, BASE).replace(os.sep, "/"),
                                         "ok": ok, "stdout": (r.stdout or "").strip()[-500:],
                                         "stderr": (r.stderr or "").strip()[-500:]})
            print(("OK " if ok else "FAIL ") + os.path.relpath(d, BASE))
            if not ok:
                print((r.stderr or "")[-800:])

    summary = {
        "apply": apply,
        "registry_names_fixed": stats["registry_names_fixed"],
        "profiles_named": stats["profiles_named"],
        "profiles_already_named": stats["profiles_already_named"],
        "index_added": stats["index_added"],
        "index_removed": stats["index_removed"],
        "index_names_fixed": stats["index_names_fixed"],
        "index_deduped": stats["index_deduped"],
        "index_files_changed": stats["index_files_changed"],
        "name_index_rebuilt": stats["name_index_rebuilt"],
        "name_index_failed": stats["name_index_failed"],
        "qid_groups": len(qrows),
        "qid_same_name": sum(1 for x in qrows if x["classification"] == "duplicate_profiles_same_name"),
        "qid_review": sum(1 for x in qrows if x["classification"] != "duplicate_profiles_same_name"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if apply:
        path = os.path.join(OUT, "p1_metadata_cleanup_undo.json")
        json.dump({"summary": summary, **undo}, open(path, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("undo ->", path)
        print("qid review ->", qpath)
    else:
        print("DRY")


if __name__ == "__main__":
    main()

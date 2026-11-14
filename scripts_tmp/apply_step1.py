# -*- coding: utf-8 -*-
"""Step 1: avatar-neutral ID reference repair (EXACT matches only).

Applies only:
  - replace_profile with match_type == "exact"  (4,964 rows)
  - null_fill rows whose ref name exactly matches the target profile name
    (work_org 4,925 / person_rel 2,818 / family 414 = 8,157 rows)

Does NOT touch:
  - any profile's person_id / org_id
  - profile.local_path / profile.minio_path
  - avatars, minio-store, _index.json
  - fuzzy / ambiguous / null-collision rows

Writes an undo log so every change can be reverted.
Usage:
  python scripts_tmp/apply_step1.py --dry
  python scripts_tmp/apply_step1.py --apply
"""
import json
import os
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, load_datasets, sig  # noqa: E402

OUTDIR = OUT


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


def main():
    apply = "--apply" in sys.argv
    latest, _ = load_datasets()

    # ---- profile compact index (for exact verification) ----
    PC = {}
    PFILE = {}   # (kind, cc, id) -> path
    for cc, (date, folder) in latest.items():
        for f in glob_files(os.path.join(folder, "persons")):
            d = json.load(open(f, encoding="utf-8"))
            pid = d.get("person_id")
            if not pid:
                continue
            vals = [d.get("name"), d.get("name_en"), d.get("name_zh")]
            vals += d.get("aliases") or []
            c = set()
            for v in vals:
                c |= sig(v)[0]
            PC[pid] = c
            PFILE[("person", cc, pid)] = f
        for f in glob_files(os.path.join(folder, "orgs")):
            d = json.load(open(f, encoding="utf-8"))
            oid = d.get("org_id")
            if not oid:
                continue
            bi = d.get("basic_info") or {}
            vals = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")]
            vals += bi.get("aliases") or []
            c = set()
            for v in vals:
                c |= sig(v)[0]
            PC[oid] = c
            PFILE[("org", cc, oid)] = f

    plan = json.load(open(os.path.join(OUTDIR, "repair_plan.json"), encoding="utf-8"))

    # ---- build operation maps ----
    replace = defaultdict(dict)   # (cat, owner) -> {(ref_name, current): suggested}
    fill = defaultdict(dict)      # (cat, owner) -> {ref_name: suggested}
    skipped_plan = Counter()

    for x in plan["broken"]:
        if x["action"] != "replace_profile" or x.get("match_type") != "exact":
            continue
        cat = x["cat"]
        owner = x.get("person_id") if cat in ("work_org", "person_rel", "family") \
            else x.get("org_id")
        sug = x.get("suggested")
        if not owner or not sug or sug not in PC:
            skipped_plan["replace_missing_target"] += 1
            continue
        # verify exact match still holds
        if not (sig(x["ref_name"])[0] & PC[sug]):
            skipped_plan["replace_no_longer_exact"] += 1
            continue
        key = (x["ref_name"], x["current_id"])
        prev = replace[(cat, owner)].get(key)
        if prev and prev != sug:
            skipped_plan["replace_conflict"] += 1
            continue
        replace[(cat, owner)][key] = sug

    for x in plan["null_fill"]:
        cat = x["cat"]
        owner = x.get("person_id")
        sug = x.get("suggested")
        if not owner or not sug or sug not in PC:
            skipped_plan["fill_missing_target"] += 1
            continue
        if not (sig(x["ref_name"])[0] & PC[sug]):
            continue  # fuzzy fill -> Step 2
        prev = fill[(cat, owner)].get(x["ref_name"])
        if prev and prev != sug:
            skipped_plan["fill_conflict"] += 1
            continue
        fill[(cat, owner)][x["ref_name"]] = sug

    # ---- apply ----
    stats = Counter()
    undo = []
    changed_files = set()

    def note(f, arr, idx, field, old, new, cat, ref):
        undo.append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                     "array": arr, "index": idx, "field": field,
                     "old": old, "new": new, "cat": cat, "ref_name": ref})
        stats[f"{cat}_changed"] += 1

    # persons
    for cc, (date, folder) in latest.items():
        for f in glob_files(os.path.join(folder, "persons")):
            d = json.load(open(f, encoding="utf-8"))
            pid = d.get("person_id")
            if not pid:
                continue
            changed = False

            ops_r = replace.get(("work_org", pid), {})
            ops_f = fill.get(("work_org", pid), {})
            for i, w in enumerate(d.get("work_experience") or []):
                if not isinstance(w, dict):
                    continue
                nm = (w.get("organization") or "").strip()
                cur = w.get("org_id")
                if ops_r and cur and (nm, cur) in ops_r:
                    new = ops_r[(nm, cur)]
                    if new != cur:
                        note(f, "work_experience", i, "org_id", cur, new, "work_org", nm)
                        w["org_id"] = new
                        changed = True
                elif ops_f and not cur and nm in ops_f:
                    new = ops_f[nm]
                    note(f, "work_experience", i, "org_id", cur, new, "work_org", nm)
                    w["org_id"] = new
                    changed = True

            for arr, cat in [("person_relationships", "person_rel"),
                             ("family_members", "family")]:
                nk = "person_name" if cat == "person_rel" else "name"
                ops_r = replace.get((cat, pid), {})
                ops_f = fill.get((cat, pid), {})
                for i, r in enumerate(d.get(arr) or []):
                    if not isinstance(r, dict):
                        continue
                    nm = (r.get(nk) or "").strip()
                    cur = r.get("person_id")
                    if ops_r and cur and (nm, cur) in ops_r:
                        new = ops_r[(nm, cur)]
                        if new != cur:
                            note(f, arr, i, "person_id", cur, new, cat, nm)
                            r["person_id"] = new
                            changed = True
                    elif ops_f and not cur and nm in ops_f:
                        new = ops_f[nm]
                        note(f, arr, i, "person_id", cur, new, cat, nm)
                        r["person_id"] = new
                        changed = True

            if changed:
                changed_files.add(f)
                if apply:
                    save_json(f, d)

    # orgs
    for cc, (date, folder) in latest.items():
        for f in glob_files(os.path.join(folder, "orgs")):
            d = json.load(open(f, encoding="utf-8"))
            oid = d.get("org_id")
            if not oid:
                continue
            changed = False

            ops_r = replace.get(("key_people", oid), {})
            for i, kp in enumerate(d.get("key_people") or []):
                if not isinstance(kp, dict):
                    continue
                nm = (kp.get("name") or "").strip()
                cur = kp.get("person_id")
                if ops_r and cur and (nm, cur) in ops_r:
                    new = ops_r[(nm, cur)]
                    if new != cur:
                        note(f, "key_people", i, "person_id", cur, new, "key_people", nm)
                        kp["person_id"] = new
                        changed = True

            ops_r = replace.get(("related_org", oid), {})
            for i, re_ in enumerate(d.get("related_entities") or []):
                if not isinstance(re_, dict):
                    continue
                nm = (re_.get("org_name") or "").strip()
                cur = re_.get("org_id")
                if ops_r and cur and (nm, cur) in ops_r:
                    new = ops_r[(nm, cur)]
                    if new != cur:
                        note(f, "related_entities", i, "org_id", cur, new, "related_org", nm)
                        re_["org_id"] = new
                        changed = True

            if changed:
                changed_files.add(f)
                if apply:
                    save_json(f, d)

    # ---- verify ----
    missing = [u for u in undo if u["new"] not in PC]
    summary = {
        "mode": "apply" if apply else "dry",
        "changes": len(undo),
        "changed_files": len(changed_files),
        "by_cat": {k: v for k, v in sorted(stats.items())},
        "skipped_plan": dict(skipped_plan),
        "missing_target_after": len(missing),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))

    if apply:
        with open(os.path.join(OUTDIR, "step1_undo.json"), "w", encoding="utf-8") as fh:
            json.dump(undo, fh, ensure_ascii=False, indent=1)
        with open(os.path.join(OUTDIR, "step1_summary.json"), "w", encoding="utf-8") as fh:
            json.dump(summary, fh, ensure_ascii=False, indent=1)
        print("undo ->", os.path.join(OUTDIR, "step1_undo.json"))
    else:
        print("DRY RUN — no files written. Re-run with --apply")


def glob_files(folder):
    import glob
    for f in glob.glob(os.path.join(folder, "*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        yield f


if __name__ == "__main__":
    main()

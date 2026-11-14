# -*- coding: utf-8 -*-
"""A2 safe layer: archive dead registry entries + merge same-country shadows.

Only rows with action in {drop, merge_to_existing} from registry_dedupe_plan.csv.
- drop: remove from active registry list, append to deprecated_registry
- merge_to_existing: mark entry status=merged, merged_into=<target>
- refs whose current ID == collision_id and whose name matches the shadow
  (and does not match the owner profile) are remapped to the target.

Does NOT assign new IDs or touch review rows.
Usage: python scripts_tmp/apply_registry_safe.py --dry|--apply
"""
import csv
import glob
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, load_datasets, match, sig

PLAN = os.path.join(OUT, "registry_dedupe_plan.csv")


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


def eid(e, kind):
    return e.get("org_id") if kind == "org" else e.get("person_id")


def ename(e):
    return (e.get("name") or e.get("name_en") or e.get("name_zh") or "").strip()


def main():
    apply = "--apply" in sys.argv
    rows = list(csv.DictReader(open(PLAN, encoding="utf-8-sig")))
    rows = [r for r in rows if r["action"] in ("drop", "merge_to_existing")]
    latest, _ = load_datasets()

    # owner profile sigs
    owner_sig = {}
    for kind, pat, idkey in [("org", "output/[a-z][a-z]/20*/orgs/*.json", "org_id"),
                             ("person", "output/[a-z][a-z]/20*/persons/*.json", "person_id")]:
        for f in glob.glob(os.path.join(BASE, pat)):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            i = d.get(idkey)
            if not i:
                continue
            if kind == "org":
                bi = d.get("basic_info") or {}
                vals = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")]
                vals += bi.get("aliases") or []
            else:
                vals = [d.get("name"), d.get("name_en"), d.get("name_zh")]
                vals += d.get("aliases") or []
            c = set()
            for v in vals:
                c |= sig(v)[0]
            owner_sig[(kind, i)] = c

    # rows grouped by id
    by_id = defaultdict(list)
    for r in rows:
        by_id[(r["kind"], r["collision_id"])].append(r)

    # registry files per country
    regpath = {}
    for cc, (date, folder) in latest.items():
        p = os.path.join(folder, "id_registry.json")
        if os.path.exists(p):
            regpath[cc] = p

    stats = Counter()
    undo = {"registry": {}, "ref_changes": []}
    regs = {}
    for cc, p in regpath.items():
        regs[cc] = json.load(open(p, encoding="utf-8"))

    for r in rows:
        kind, cid = r["kind"], r["collision_id"]
        cc = cid[:2].lower()
        if cc not in regs:
            stats["missing_registry"] += 1
            continue
        reg = regs[cc]
        key = "registry" if kind == "org" else "person_registry"
        entries = reg.get(key) or []
        target = None
        for e in entries:
            if eid(e, kind) == cid and ename(e) == r["shadow"].strip():
                target = e
                break
        if target is None:
            # fallback: normalized name match
            for e in entries:
                if eid(e, kind) == cid and ename(e) and match(sig(r["shadow"]), (sig(ename(e))[0], [])):
                    target = e
                    break
        if target is None:
            stats[f"entry_not_found_{r['action']}"] += 1
            continue
        old = dict(target)
        if r["action"] == "drop":
            entries.remove(target)
            dep_key = "deprecated_registry" if kind == "org" else "deprecated_person_registry"
            dep = reg.setdefault(dep_key, [])
            old["dropped_reason"] = "A2 safe layer: dead status"
            dep.append(old)
            stats["dropped"] += 1
        else:
            target["status"] = "merged"
            target["merged_into"] = r["target"]
            target["notes"] = (target.get("notes") or "") + f"；A2 合并到 {r['target']}"
            stats["merged"] += 1
        undo["registry"].setdefault(regpath[cc], []).append(
            {"kind": kind, "id": cid, "name": ename(old),
             "old": old, "action": r["action"], "target": r.get("target", "")})

    if apply:
        for cc, reg in regs.items():
            save_json(regpath[cc], reg)

    # ref remap for merge rows
    merge_rows = [r for r in rows if r["action"] == "merge_to_existing"]
    merge_org_ids = {r["collision_id"] for r in merge_rows if r["kind"] == "org"}
    merge_person_ids = {r["collision_id"] for r in merge_rows if r["kind"] == "person"}
    merge_by = defaultdict(list)
    for r in merge_rows:
        merge_by[(r["kind"], r["collision_id"])].append(r)

    def resolve_shadow(kind, cid, name):
        if not name:
            return None
        # owner profile match -> leave alone
        if match(sig(name), (owner_sig.get((kind, cid), set()), [])):
            return None
        hits = []
        for r in merge_by.get((kind, cid), []):
            if match(sig(name), (sig(r["shadow"])[0], [])):
                hits.append(r["target"])
        hits = sorted(set(hits))
        return hits[0] if len(hits) == 1 else None

    ref_changes = []
    dirty = set()
    docs = {}

    def change(f, arr, idx, field, old, new, ref, kind):
        ref_changes.append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                            "array": arr, "index": idx, "field": field,
                            "old": old, "new": new, "ref_name": ref, "kind": kind})
        stats["ref_changed"] += 1

    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        dirty_f = False
        for i, w in enumerate(d.get("work_experience") or []):
            if not isinstance(w, dict):
                continue
            cid = w.get("org_id")
            nm = w.get("organization") or w.get("org_name") or ""
            if cid in merge_org_ids:
                new = resolve_shadow("org", cid, nm)
                if new and new != cid:
                    change(f, "work_experience", i, "org_id", cid, new, nm, "org")
                    w["org_id"] = new
                    dirty_f = True
        for arr in ("person_relationships", "family_members"):
            nk = "person_name" if arr == "person_relationships" else "name"
            for i, r in enumerate(d.get(arr) or []):
                if not isinstance(r, dict):
                    continue
                cid = r.get("person_id")
                nm = r.get(nk) or r.get("name") or ""
                if cid in merge_person_ids:
                    new = resolve_shadow("person", cid, nm)
                    if new and new != cid:
                        change(f, arr, i, "person_id", cid, new, nm, "person")
                        r["person_id"] = new
                        dirty_f = True
        if dirty_f:
            dirty.add(f)
            if apply:
                save_json(f, d)

    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        dirty_f = False
        for arr, field, nk, kind in [
            ("key_people", "person_id", "name", "person"),
            ("related_entities", "org_id", "org_name", "org"),
        ]:
            for i, r in enumerate(d.get(arr) or []):
                if not isinstance(r, dict):
                    continue
                cid = r.get(field)
                nm = r.get(nk) or r.get("name") or ""
                if cid in merge_person_ids:
                    new = resolve_shadow(kind, cid, nm)
                    if new and new != cid:
                        change(f, arr, i, field, cid, new, nm, kind)
                        r[field] = new
                        dirty_f = True
        if dirty_f:
            dirty.add(f)
            if apply:
                save_json(f, d)

    undo["ref_changes"] = ref_changes
    print(json.dumps({"rows": len(rows), "by_action": dict(Counter(r["action"] for r in rows)),
                      "registry_actions": {k: v for k, v in stats.items()
                                           if k in ("dropped", "merged")},
                      "ref_changes": len(ref_changes),
                      "files_changed": len(dirty),
                      "skipped": {k: v for k, v in stats.items() if k.startswith(("entry_not", "missing"))}},
                     ensure_ascii=False, indent=1))
    if apply:
        with open(os.path.join(OUT, "registry_safe_undo.json"), "w", encoding="utf-8") as fh:
            json.dump(undo, fh, ensure_ascii=False, indent=1)
        print("undo ->", os.path.join(OUT, "registry_safe_undo.json"))
    else:
        with open(os.path.join(OUT, "registry_safe_dry_undo.json"), "w", encoding="utf-8") as fh:
            json.dump(undo, fh, ensure_ascii=False, indent=1)
        print("DRY RUN — no files written; dry undo ->",
              os.path.join(OUT, "registry_safe_dry_undo.json"))


if __name__ == "__main__":
    main()

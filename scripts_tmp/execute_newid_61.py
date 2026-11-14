# -*- coding: utf-8 -*-
"""Execute the 61 reviewed sample new IDs (+7 same-identity merges).

Selected statuses:
  approved_sample (53) + pending_realloc (8)  -> create new registry identity
  same_identity (7)                          -> remove shadow entry, merged_into canonical new ID

Also remaps refs whose current ID == collision_id and whose name matches the
shadow identity (and not the owner profile).

Usage: python scripts_tmp/execute_newid_61.py --dry|--apply
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

PLAN = os.path.join(OUT, "registry_newid_plan_v3.csv")


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


def ref_name(item, kind):
    keys = (["organization", "org_name", "organization_en"] if kind == "org"
            else ["person_name", "name"] if kind in ("rel", "family")
            else ["name", "name_en"])
    for k in keys:
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def main():
    apply = "--apply" in sys.argv
    rows = list(csv.DictReader(open(PLAN, encoding="utf-8-sig")))
    selected = [r for r in rows if r["status"] in ("approved_sample", "pending_realloc",
                                                   "same_identity")]
    create = [r for r in selected if r["status"] in ("approved_sample", "pending_realloc")]
    same = [r for r in selected if r["status"] == "same_identity"]
    print("create", len(create), "same_identity", len(same))

    # verify new IDs unique and not currently registered
    used = set()
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/id_registry.json")):
        d = json.load(open(f, encoding="utf-8"))
        for key, idk in [("registry", "org_id"), ("person_registry", "person_id"),
                         ("deprecated_registry", "org_id"),
                         ("deprecated_person_registry", "person_id")]:
            for e in d.get(key) or []:
                if e.get(idk):
                    used.add(e[idk])
    bad = [r["new_id"] for r in create if r["new_id"] in used]
    dup = [k for k, v in Counter(r["new_id"] for r in create).items() if v > 1]
    print("bad_used", bad[:10], "dup", dup[:10])

    # owner sigs for collision IDs
    owner_sig = {}
    for kind, pat, idk in [("org", "output/[a-z][a-z]/20*/orgs/*.json", "org_id"),
                           ("person", "output/[a-z][a-z]/20*/persons/*.json", "person_id")]:
        for f in glob.glob(os.path.join(BASE, pat)):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            i = d.get(idk)
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

    latest, _ = load_datasets()
    regpath = {}
    regs = {}
    for cc, (date, folder) in latest.items():
        p = os.path.join(folder, "id_registry.json")
        if os.path.exists(p):
            regpath[cc] = p
            regs[cc] = json.load(open(p, encoding="utf-8"))

    undo = {"registry": {}, "ref_changes": []}
    stats = Counter()

    def eid(e, kind):
        return e.get("org_id") if kind == "org" else e.get("person_id")

    def ename(e):
        return (e.get("name") or e.get("name_en") or e.get("name_zh") or "").strip()

    # registry moves
    for r in selected:
        cid = r["collision_id"]
        cc = cid[:2].lower()
        kind = "person" if "-PERSON-" in cid else "org"
        if cc not in regs:
            stats["missing_registry"] += 1
            continue
        reg = regs[cc]
        key = "person_registry" if kind == "person" else "registry"
        entries = reg.get(key) or []
        idx = None
        for i, e in enumerate(entries):
            if eid(e, kind) == cid and ename(e) == r["shadow"].strip():
                idx = i
                break
        if idx is None:
            for i, e in enumerate(entries):
                if eid(e, kind) == cid and ename(e) and match(sig(r["shadow"]), (sig(ename(e))[0], [])):
                    idx = i
                    break
        if idx is None:
            stats["entry_not_found"] += 1
            continue
        old = entries.pop(idx)
        if r["status"] == "same_identity":
            old["status"] = "merged"
            old["merged_into"] = r["same_identity_new_id"]
            old["deprecated_reason"] = "A2 same shadow identity"
            dep = "deprecated_person_registry" if kind == "person" else "deprecated_registry"
            reg.setdefault(dep, []).append(old)
            stats["same_identity"] += 1
            undo["registry"].setdefault(regpath[cc], []).append(
                {"kind": kind, "id": cid, "name": ename(old), "action": "same_identity",
                 "old": old, "new_id": r["same_identity_new_id"]})
        else:
            new = {
                ("person_id" if kind == "person" else "org_id"): r["new_id"],
                "name": r["shadow"].strip(),
                "status": "auto_registered",
                "source": f"A2 dedupe from {cid}",
                "notes": f"独立身份，由 {cid} 的影子身份拆分（review seq {r['sample_seq']}）",
            }
            if kind == "org":
                new["org_type"] = r["category"]
            entries.append(new)
            stats["created"] += 1
            undo["registry"].setdefault(regpath[cc], []).append(
                {"kind": kind, "id": cid, "name": ename(old), "action": "create",
                 "old": old, "new": new, "new_id": r["new_id"]})
        reg[key] = entries

    if apply:
        for cc, reg in regs.items():
            save_json(regpath[cc], reg)

    # ref remap map
    by_cid = defaultdict(list)
    for r in selected:
        by_cid[(r["collision_id"], r["shadow"].strip())] = r

    def resolve(kind, cid, name):
        if not name:
            return None
        if match(sig(name), (owner_sig.get((kind, cid), set()), [])):
            return None
        hits = []
        for (rcid, rshadow), r in by_cid.items():
            if rcid == cid and match(sig(name), (sig(rshadow)[0], [])):
                hits.append(r["new_id"] or r["same_identity_new_id"])
        hits = sorted(set(hits))
        return hits[0] if len(hits) == 1 else None

    dirty = set()
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        dirty_f = False
        for i, w in enumerate(d.get("work_experience") or []):
            if not isinstance(w, dict):
                continue
            cid = w.get("org_id")
            nm = ref_name(w, "org")
            if cid in {r["collision_id"] for r in selected}:
                new = resolve("org", cid, nm)
                if new and new != cid:
                    undo["ref_changes"].append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                                "array": "work_experience", "index": i,
                                                "field": "org_id", "old": cid, "new": new,
                                                "ref_name": nm})
                    w["org_id"] = new
                    dirty_f = True
        for arr, kind in [("person_relationships", "rel"), ("family_members", "family")]:
            for i, x in enumerate(d.get(arr) or []):
                if not isinstance(x, dict):
                    continue
                cid = x.get("person_id")
                nm = ref_name(x, kind)
                if cid in {r["collision_id"] for r in selected}:
                    new = resolve("person", cid, nm)
                    if new and new != cid:
                        undo["ref_changes"].append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                                    "array": arr, "index": i,
                                                    "field": "person_id", "old": cid, "new": new,
                                                    "ref_name": nm})
                        x["person_id"] = new
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
        for arr, field, kind in [("key_people", "person_id", "person"),
                                 ("related_entities", "org_id", "org")]:
            for i, x in enumerate(d.get(arr) or []):
                if not isinstance(x, dict):
                    continue
                cid = x.get(field)
                nm = ref_name(x, "org" if kind == "org" else "person")
                if cid in {r["collision_id"] for r in selected}:
                    new = resolve(kind, cid, nm)
                    if new and new != cid:
                        undo["ref_changes"].append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                                    "array": arr, "index": i,
                                                    "field": field, "old": cid, "new": new,
                                                    "ref_name": nm})
                        x[field] = new
                        dirty_f = True
        if dirty_f:
            dirty.add(f)
            if apply:
                save_json(f, d)

    summary = {"selected": len(selected), "create": len(create), "same_identity": len(same),
               "registry": {k: v for k, v in stats.items()},
               "ref_changes": len(undo["ref_changes"]),
               "files_changed": len(dirty), "bad_used": bad, "dup": dup}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if apply:
        with open(os.path.join(OUT, "registry_newid_exec_undo.json"), "w", encoding="utf-8") as fh:
            json.dump(undo, fh, ensure_ascii=False, indent=1)
        with open(os.path.join(OUT, "registry_newid_exec_summary.json"), "w", encoding="utf-8") as fh:
            json.dump(summary, fh, ensure_ascii=False, indent=1)
        print("undo ->", os.path.join(OUT, "registry_newid_exec_undo.json"))
    else:
        with open(os.path.join(OUT, "registry_newid_exec_dry_undo.json"), "w", encoding="utf-8") as fh:
            json.dump(undo, fh, ensure_ascii=False, indent=1)
        print("DRY RUN — no files written; dry undo ->",
              os.path.join(OUT, "registry_newid_exec_dry_undo.json"))


if __name__ == "__main__":
    main()

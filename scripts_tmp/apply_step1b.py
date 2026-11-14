# -*- coding: utf-8 -*-
"""Step 1b: conservative, avatar-neutral ID reference repair.

Rules (stricter than Step 1):
  - PRIMARY names only (name/name_en/name_zh/name_original), aliases excluded
  - exact normalized-name match only (no token/substring fuzzy)
  - fills: same country only
  - replacements: same country; cross-country only for non-government orgs
    (CORP/FIN/SOE/ACAD/MEDIA/NGO/INTL) and for persons (distinctive full names)
  - never touches profile IDs / avatar fields

Usage:
  python scripts_tmp/apply_step1b.py --dry
  python scripts_tmp/apply_step1b.py --apply
"""
import glob
import json
import os
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, load_datasets, match, sig  # noqa: E402

GOV_CATS = {"GOV", "MIL", "PARTY"}


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


def id_cat(x):
    if not x:
        return "?"
    if "-PERSON-" in x:
        return "PERSON"
    import re
    m = re.match(r"^[A-Z]{2}-([A-Z_]+)-", x)
    return m.group(1) if m else "?"


def main():
    apply = "--apply" in sys.argv
    latest, _ = load_datasets()

    PRIMARY = {}   # id -> (compacts, tokens) from primary names only
    FULL = {}      # id -> (compacts, tokens) incl. aliases
    META = {}      # id -> (cc, cat)
    IDX = defaultdict(set)    # (cc, compact) -> ids
    IDXG = defaultdict(set)   # compact -> ids

    def add_primary(i, vals):
        c, t = set(), []
        for v in vals:
            x, y = sig(v)
            c |= x
            t += y
        PRIMARY[i] = (c, t)
        for x in c:
            IDX[(META[i][0], x)].add(i)
            IDXG[x].add(i)

    for cc, (date, folder) in latest.items():
        for f in glob.glob(os.path.join(folder, "persons", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            pid = d.get("person_id")
            if not pid:
                continue
            META[pid] = (cc, "PERSON")
            prim = [d.get("name"), d.get("name_en"), d.get("name_zh")]
            full = prim + (d.get("aliases") or [])
            add_primary(pid, prim)
            c, t = set(), []
            for v in full:
                x, y = sig(v)
                c |= x
                t += y
            FULL[pid] = (c, t)
        for f in glob.glob(os.path.join(folder, "orgs", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            oid = d.get("org_id")
            if not oid:
                continue
            bi = d.get("basic_info") or {}
            META[oid] = (cc, id_cat(oid))
            prim = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")]
            full = prim + (bi.get("aliases") or [])
            add_primary(oid, prim)
            c, t = set(), []
            for v in full:
                x, y = sig(v)
                c |= x
                t += y
            FULL[oid] = (c, t)

    def hits(name, cc=None, kind="org"):
        rc = sig(name)[0]
        cands = set()
        for x in rc:
            cands |= (IDX.get((cc, x), set()) if cc else IDXG.get(x, set()))
        out = []
        for i in cands:
            if kind == "person" and META[i][1] != "PERSON":
                continue
            if kind == "org" and META[i][1] == "PERSON":
                continue
            if rc & PRIMARY[i][0]:
                out.append(i)
        return sorted(set(out))

    stats = Counter()
    undo = []
    changed_files = set()
    samples = defaultdict(list)

    def change(f, arr, idx, field, old, new, cat, ref):
        undo.append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                     "array": arr, "index": idx, "field": field,
                     "old": old, "new": new, "cat": cat, "ref_name": ref})
        stats[f"{cat}_{'fill' if old in (None, '') else 'replace'}"] += 1
        if len(samples[cat]) < 8:
            samples[cat].append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                 "old": old, "new": new, "ref": ref})

    # persons
    for cc, (date, folder) in latest.items():
        for f in glob.glob(os.path.join(folder, "persons", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            pid = d.get("person_id")
            if not pid:
                continue
            dirty = False

            for i, w in enumerate(d.get("work_experience") or []):
                if not isinstance(w, dict):
                    continue
                nm = (w.get("organization") or "").strip()
                cur = w.get("org_id")
                if not nm:
                    continue
                if cur:
                    if cur in FULL and match(sig(nm), FULL[cur]):
                        continue
                    cand = [x for x in hits(nm, cc, "org") if x != cur]
                    if len(cand) == 1:
                        new = cand[0]
                    elif not cand:
                        g = [x for x in hits(nm, None, "org") if x != cur]
                        if len(g) == 1 and META[g[0]][1] not in GOV_CATS:
                            new = g[0]
                        else:
                            continue
                    else:
                        continue
                    change(f, "work_experience", i, "org_id", cur, new, "work_org", nm)
                    w["org_id"] = new
                    dirty = True
                else:
                    cand = hits(nm, cc, "org")
                    if len(cand) == 1:
                        change(f, "work_experience", i, "org_id", cur, cand[0],
                               "work_org", nm)
                        w["org_id"] = cand[0]
                        dirty = True

            for arr, cat in [("person_relationships", "person_rel"),
                             ("family_members", "family")]:
                nk = "person_name" if cat == "person_rel" else "name"
                for i, r in enumerate(d.get(arr) or []):
                    if not isinstance(r, dict):
                        continue
                    nm = (r.get(nk) or "").strip()
                    cur = r.get("person_id")
                    if not nm:
                        continue
                    if cur:
                        if cur in FULL and match(sig(nm), FULL[cur]):
                            continue
                        cand = [x for x in hits(nm, cc, "person") if x != cur]
                        if len(cand) == 1:
                            new = cand[0]
                        elif not cand and cat == "person_rel":
                            g = [x for x in hits(nm, None, "person") if x != cur]
                            new = g[0] if len(g) == 1 else None
                        else:
                            new = None
                        if new:
                            change(f, arr, i, "person_id", cur, new, cat, nm)
                            r["person_id"] = new
                            dirty = True
                    else:
                        cand = hits(nm, cc, "person")
                        if len(cand) == 1:
                            change(f, arr, i, "person_id", cur, cand[0], cat, nm)
                            r["person_id"] = cand[0]
                            dirty = True

            if dirty:
                changed_files.add(f)
                if apply:
                    save_json(f, d)

    # orgs
    for cc, (date, folder) in latest.items():
        for f in glob.glob(os.path.join(folder, "orgs", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            oid = d.get("org_id")
            if not oid:
                continue
            dirty = False

            for i, kp in enumerate(d.get("key_people") or []):
                if not isinstance(kp, dict):
                    continue
                nm = (kp.get("name") or "").strip()
                cur = kp.get("person_id")
                if not nm or not cur:
                    continue
                if cur in FULL and match(sig(nm), FULL[cur]):
                    continue
                cand = [x for x in hits(nm, cc, "person") if x != cur]
                if len(cand) == 1:
                    change(f, "key_people", i, "person_id", cur, cand[0],
                           "key_people", nm)
                    kp["person_id"] = cand[0]
                    dirty = True

            for i, re_ in enumerate(d.get("related_entities") or []):
                if not isinstance(re_, dict):
                    continue
                nm = (re_.get("org_name") or "").strip()
                cur = re_.get("org_id")
                if not nm or not cur:
                    continue
                if cur in FULL and match(sig(nm), FULL[cur]):
                    continue
                cand = [x for x in hits(nm, cc, "org") if x != cur]
                if len(cand) == 1:
                    new = cand[0]
                elif not cand:
                    g = [x for x in hits(nm, None, "org") if x != cur]
                    if len(g) == 1 and META[g[0]][1] not in GOV_CATS:
                        new = g[0]
                    else:
                        continue
                else:
                    continue
                change(f, "related_entities", i, "org_id", cur, new,
                       "related_org", nm)
                re_["org_id"] = new
                dirty = True

            if dirty:
                changed_files.add(f)
                if apply:
                    save_json(f, d)

    missing = [u for u in undo if u["new"] not in FULL]
    summary = {
        "mode": "apply" if apply else "dry",
        "changes": len(undo),
        "files": len(changed_files),
        "by_cat": dict(sorted(stats.items())),
        "missing_target": len(missing),
        "samples": {k: v for k, v in samples.items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))

    if apply:
        with open(os.path.join(OUT, "step1b_undo.json"), "w", encoding="utf-8") as fh:
            json.dump(undo, fh, ensure_ascii=False, indent=1)
        with open(os.path.join(OUT, "step1b_summary.json"), "w", encoding="utf-8") as fh:
            json.dump(summary, fh, ensure_ascii=False, indent=1)
        print("undo ->", os.path.join(OUT, "step1b_undo.json"))
    else:
        with open(os.path.join(OUT, "step1b_dry_undo.json"), "w", encoding="utf-8") as fh:
            json.dump(undo, fh, ensure_ascii=False, indent=1)
        print("DRY RUN — no files written; dry undo ->",
              os.path.join(OUT, "step1b_dry_undo.json"))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""A2: registry ID collision dedupe plan (read-only).

For every org/person ID carrying multiple identities:
  - owner profile keeps the ID
  - shadow identity with an existing profile elsewhere -> merge_to_existing
  - shadow identity with no profile -> assign a fresh unused ID
  - dead statuses (trimmed/merged/removed/...) -> drop
  - ambiguous name -> review

Output: output/_id_audit/registry_dedupe_plan.csv + summary JSON.
"""
import csv
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, match, sig

DEAD = {"trimmed", "merged", "removed", "duplicate", "excluded",
        "deprecated_broken_id", "archived", "pruned"}


def load_profiles():
    orgs, persons = {}, {}
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
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
        orgs[oid] = {"cc": oid[:2].lower(), "name": bi.get("name_zh") or bi.get("name_original"),
                     "sig": c}
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        pid = d.get("person_id")
        if not pid:
            continue
        vals = [d.get("name"), d.get("name_en"), d.get("name_zh")]
        vals += d.get("aliases") or []
        c = set()
        for v in vals:
            c |= sig(v)[0]
        persons[pid] = {"cc": pid[:2].lower(), "name": d.get("name") or d.get("name_zh"),
                        "sig": c}
    return orgs, persons


def main():
    collision = json.load(open(os.path.join(OUT, "collision_report.json"), encoding="utf-8"))
    orgs, persons = load_profiles()
    oidx, pidx = defaultdict(set), defaultdict(set)
    for i, v in orgs.items():
        for c in v["sig"]:
            oidx[c].add(i)
    for i, v in persons.items():
        for c in v["sig"]:
            pidx[c].add(i)

    # max sequence per (cc, category) from files + registry
    maxseq = defaultdict(int)
    for oid, p in orgs.items():
        m = re.match(r"^([A-Z]{2})-([A-Z_]+)-(\d+)$", oid)
        if m:
            maxseq[(m.group(1), m.group(2))] = max(maxseq[(m.group(1), m.group(2))], int(m.group(3)))
    for pid in persons:
        m = re.match(r"^([A-Z]{2})-PERSON-(\d+)$", pid)
        if m:
            maxseq[(m.group(1), "PERSON")] = max(maxseq[(m.group(1), "PERSON")], int(m.group(2)))
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/id_registry.json")):
        d = json.load(open(f, encoding="utf-8"))
        for e in d.get("registry") or []:
            oid = e.get("org_id") or ""
            m = re.match(r"^([A-Z]{2})-([A-Z_]+)-(\d+)$", oid)
            if m:
                maxseq[(m.group(1), m.group(2))] = max(maxseq[(m.group(1), m.group(2))], int(m.group(3)))
        for e in d.get("person_registry") or []:
            pid = e.get("person_id") or ""
            m = re.match(r"^([A-Z]{2})-PERSON-(\d+)$", pid)
            if m:
                maxseq[(m.group(1), "PERSON")] = max(maxseq[(m.group(1), "PERSON")], int(m.group(2)))

    def next_id(cc, cat):
        key = (cc.upper(), cat)
        maxseq[key] += 1
        n = maxseq[key]
        if cat == "PERSON":
            return f"{cc.upper()}-PERSON-{n:06d}"
        return f"{cc.upper()}-{cat}-{n:03d}"

    def find_target(name, kind, exclude, cc):
        table = orgs if kind == "org" else persons
        index = oidx if kind == "org" else pidx
        rs = sig(name)
        cands = set()
        for c in rs[0]:
            cands |= index.get(c, set())
        same = [i for i in cands if i != exclude and table[i]["cc"] == cc
                and match(rs, (table[i]["sig"], []))]
        if len(same) == 1:
            return same[0], "unique_same_country"
        if len(same) > 1:
            return None, f"ambiguous({len(same)})"
        glob = [i for i in cands if i != exclude and match(rs, (table[i]["sig"], []))]
        if len(glob) == 1:
            return glob[0], "cross_country"
        if len(glob) > 1:
            return None, f"ambiguous({len(glob)})"
        return None, "absent"

    rows = []
    for kind, key in [("org", "org"), ("person", "person")]:
        for cc, ids in collision["collisions"][kind].items():
            for cid, info in ids.items():
                owner = info.get("profile_name")
                owner_sig = None
                if kind == "org" and cid in orgs:
                    owner_sig = orgs[cid]["sig"]
                elif kind == "person" and cid in persons:
                    owner_sig = persons[cid]["sig"]
                for entry in info.get("entries") or []:
                    nm = (entry.get("name") or "").strip()
                    st = entry.get("status")
                    if not nm:
                        continue
                    # The profiled/owner entry itself is not a shadow identity.
                    if owner_sig is not None and match(sig(nm), (owner_sig, [])):
                        continue
                    if st in DEAD:
                        rows.append({"kind": kind, "collision_id": cid, "owner": owner,
                                     "shadow": nm, "status": st, "action": "drop",
                                     "target": "", "new_id": "", "note": "dead status"})
                        continue
                    target, how = find_target(nm, kind, cid, cc)
                    if target and how == "unique_same_country":
                        rows.append({"kind": kind, "collision_id": cid, "owner": owner,
                                     "shadow": nm, "status": st, "action": "merge_to_existing",
                                     "target": target, "new_id": "", "note": how})
                    elif target and how == "cross_country":
                        rows.append({"kind": kind, "collision_id": cid, "owner": owner,
                                     "shadow": nm, "status": st, "action": "review_cross_country",
                                     "target": target, "new_id": "", "note": how})
                    elif how.startswith("ambiguous"):
                        rows.append({"kind": kind, "collision_id": cid, "owner": owner,
                                     "shadow": nm, "status": st, "action": "review_ambiguous",
                                     "target": "", "new_id": "", "note": how})
                    else:
                        cat = "PERSON" if kind == "person" else re.match(
                            r"^[A-Z]{2}-([A-Z_]+)-", cid).group(1)
                        rows.append({"kind": kind, "collision_id": cid, "owner": owner,
                                     "shadow": nm, "status": st, "action": "assign_new_id",
                                     "target": "", "new_id": next_id(cc, cat),
                                     "note": "no existing profile"})
    rows.sort(key=lambda r: (r["kind"], r["action"], r["collision_id"]))
    fields = ["kind", "collision_id", "owner", "shadow", "status", "action",
              "target", "new_id", "note"]
    with open(os.path.join(OUT, "registry_dedupe_plan.csv"), "w",
              encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    summary = {
        "rows": len(rows),
        "by_kind": dict(Counter(r["kind"] for r in rows)),
        "by_action": {f"{k[0]}:{k[1]}": v for k, v in
                      Counter((r["kind"], r["action"]) for r in rows).items()},
        "collision_ids": {"org": sum(len(v) for v in collision["collisions"]["org"].values()),
                          "person": sum(len(v) for v in collision["collisions"]["person"].values())},
        "new_ids_needed": sum(1 for r in rows if r["action"] == "assign_new_id"),
    }
    with open(os.path.join(OUT, "registry_dedupe_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("plan ->", os.path.join(OUT, "registry_dedupe_plan.csv"))


if __name__ == "__main__":
    main()

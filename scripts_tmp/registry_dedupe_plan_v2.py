# -*- coding: utf-8 -*-
"""A2 v2: registry dedupe plan for the remaining ACTIVE collisions only.

Uses active registry entries (status not dead, no merged_into), groups names with
formatting-tolerant matching, then proposes merge/new-id/review. Read-only.

Output: output/_id_audit/registry_dedupe_plan_v2.csv + summary JSON.
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
        "deprecated_broken_id", "archived", "pruned", "dropped"}


def clean_name(n):
    s = (n or "").strip()
    s = re.sub(r"^[\s\(\)（）\[\]【】]+|[\s\(\)（）\[\]【】]+$", "", s)
    return s


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
            c |= sig(clean_name(v))[0]
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
            c |= sig(clean_name(v))[0]
        persons[pid] = {"cc": pid[:2].lower(), "name": d.get("name") or d.get("name_zh"),
                        "sig": c}
    return orgs, persons


def main():
    orgs, persons = load_profiles()
    oidx, pidx = defaultdict(set), defaultdict(set)
    for i, v in orgs.items():
        for c in v["sig"]:
            oidx[c].add(i)
    for i, v in persons.items():
        for c in v["sig"]:
            pidx[c].add(i)

    # active registry
    active = {"org": defaultdict(list), "person": defaultdict(list)}
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/id_registry.json")):
        d = json.load(open(f, encoding="utf-8"))
        for e in d.get("registry") or []:
            oid = e.get("org_id")
            if oid and e.get("status") not in DEAD and not e.get("merged_into"):
                active["org"][oid].append(e)
        for e in d.get("person_registry") or []:
            pid = e.get("person_id")
            if pid and e.get("status") not in DEAD and not e.get("merged_into"):
                active["person"][pid].append(e)

    maxseq = defaultdict(int)
    for oid in orgs:
        m = re.match(r"^([A-Z]{2})-([A-Z_]+)-(\d+)$", oid)
        if m:
            maxseq[(m.group(1), m.group(2))] = max(maxseq[(m.group(1), m.group(2))], int(m.group(3)))
    for pid in persons:
        m = re.match(r"^([A-Z]{2})-PERSON-(\d+)$", pid)
        if m:
            maxseq[(m.group(1), "PERSON")] = max(maxseq[(m.group(1), "PERSON")], int(m.group(2)))
    for kind, table in active.items():
        for i, entries in table.items():
            m = re.match(r"^([A-Z]{2})-([A-Z_]+)-(\d+)$", i)
            if m:
                maxseq[(m.group(1), m.group(2))] = max(maxseq[(m.group(1), m.group(2))], int(m.group(3)))

    def next_id(cc, cat):
        key = (cc.upper(), cat)
        maxseq[key] += 1
        n = maxseq[key]
        return f"{cc.upper()}-PERSON-{n:06d}" if cat == "PERSON" else f"{cc.upper()}-{cat}-{n:03d}"

    def group_names(entries):
        groups = []  # (sig, [entries])
        for e in entries:
            nm = clean_name(e.get("name"))
            if not nm:
                continue
            s = sig(nm)
            for g in groups:
                if match(s, g[0]):
                    g[1].append(e)
                    break
            else:
                groups.append((s, [e]))
        return groups

    def find_target(name, kind, exclude, cc):
        table = orgs if kind == "org" else persons
        index = oidx if kind == "org" else pidx
        rs = sig(clean_name(name))
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
    for kind in ("org", "person"):
        profiles = orgs if kind == "org" else persons
        for cid, entries in active[kind].items():
            groups = group_names(entries)
            if len(groups) <= 1:
                continue
            owner_sig = profiles.get(cid, {}).get("sig")
            owner_idx = None
            if owner_sig:
                for gi, (gs, _) in enumerate(groups):
                    if match(gs, (owner_sig, [])):
                        owner_idx = gi
                        break
            if owner_idx is None:
                owner_idx = 0
            for gi, (gs, ents) in enumerate(groups):
                if gi == owner_idx:
                    continue
                rep = ents[0]
                nm = clean_name(rep.get("name"))
                st = rep.get("status")
                if st in DEAD:
                    action, target, new, note = "drop", "", "", "dead status"
                else:
                    target, how = find_target(nm, kind, cid, cid[:2].lower())
                    if target and how == "unique_same_country":
                        action, new, note = "merge_to_existing", "", how
                    elif target and how == "cross_country":
                        action, new, note = "review_cross_country", "", how
                    elif how.startswith("ambiguous"):
                        action, new, note = "review_ambiguous", "", how
                    else:
                        cat = "PERSON" if kind == "person" else re.match(
                            r"^[A-Z]{2}-([A-Z_]+)-", cid).group(1)
                        action, new, note = "assign_new_id", next_id(cid[:2], cat), "no same-country profile"
                rows.append({"kind": kind, "collision_id": cid,
                             "owner": profiles.get(cid, {}).get("name"),
                             "shadow": nm, "status": st, "action": action,
                             "target": target or "", "new_id": new, "note": note})
    rows.sort(key=lambda r: (r["kind"], r["action"], r["collision_id"]))
    fields = ["kind", "collision_id", "owner", "shadow", "status", "action",
              "target", "new_id", "note"]
    with open(os.path.join(OUT, "registry_dedupe_plan_v2.csv"), "w",
              encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    summary = {
        "rows": len(rows),
        "collision_ids": {"org": sum(1 for k, v in active["org"].items() if len(group_names(v)) > 1),
                          "person": sum(1 for k, v in active["person"].items() if len(group_names(v)) > 1)},
        "by_kind": dict(Counter(r["kind"] for r in rows)),
        "by_action": {f"{k[0]}:{k[1]}": v for k, v in
                      Counter((r["kind"], r["action"]) for r in rows).items()},
        "new_ids_needed": sum(1 for r in rows if r["action"] == "assign_new_id"),
    }
    with open(os.path.join(OUT, "registry_dedupe_v2_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("plan ->", os.path.join(OUT, "registry_dedupe_plan_v2.csv"))


if __name__ == "__main__":
    main()

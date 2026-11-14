# -*- coding: utf-8 -*-
"""Top missing organizations by broken-reference frequency (read-only).

Uses the repair plan's null_collision / null_absent rows for work_org and
related_org, groups by (country, organization name), and annotates:
  - refs: how many references point at this missing org
  - profile_elsewhere: existing profile IDs with the same name (redirect target)
  - registry: active registry entries with the same name (status/ID)

Output: output/_id_audit/top_missing_orgs.json + .csv
Usage: python scripts_tmp/top_missing_orgs.py
"""
import csv
import glob
import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, load_datasets, match, sig  # noqa: E402

DEAD = {"trimmed", "merged", "removed", "duplicate", "excluded",
        "deprecated_broken_id", "archived", "pruned"}


def main():
    latest, _ = load_datasets()
    profiles = defaultdict(list)   # cc -> [(oid, (compacts, tokens))]
    o_comp = defaultdict(set)
    o_tok = defaultdict(set)
    regs = {}
    r_comp = defaultdict(list)
    r_tok = defaultdict(list)

    for cc, (date, folder) in latest.items():
        for f in glob.glob(os.path.join(folder, "orgs", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            bi = d.get("basic_info") or {}
            vals = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")]
            vals += bi.get("aliases") or []
            c, t = set(), []
            for v in vals:
                x, y = sig(v)
                c |= x
                t += y
            oid = d["org_id"]
            profiles[cc].append((oid, (c, t)))
            for x in c:
                o_comp[(cc, x)].add(oid)
            for ts in t:
                for w in ts:
                    if len(w) >= 4:
                        o_tok[(cc, w)].add(oid)
        rp = os.path.join(folder, "id_registry.json")
        if os.path.exists(rp):
            regs[cc] = json.load(open(rp, encoding="utf-8"))
        for e in (regs.get(cc) or {}).get("registry", []):
            if e.get("person_id") or e.get("status") in DEAD:
                continue
            oid, nm = e.get("org_id"), (e.get("name") or "").strip()
            if not oid or not nm:
                continue
            c, t = sig(nm)
            for x in c:
                r_comp[(cc, x)].append((oid, e.get("status")))
            for ts in t:
                for w in ts:
                    if len(w) >= 4:
                        r_tok[(cc, w)].append((oid, e.get("status")))

    def profile_hits(cc, name):
        rs = sig(name)
        cands = set()
        for x in rs[0]:
            cands |= o_comp.get((cc, x), set())
        if not cands and rs[1]:
            sets = [o_tok.get((cc, t), set())
                    for t in {w for ts in rs[1] for w in ts} if len(t) >= 4]
            sets = [s for s in sets if s]
            if sets:
                cands = set.intersection(*sets) if len(sets) > 1 else set(sets[0])
                if len(cands) > 3000:
                    cands = set()
        return [oid for oid, s in profiles[cc] if oid in cands and match(rs, s)]

    def registry_hits(cc, name):
        rs = sig(name)
        cands = set()
        for x in rs[0]:
            cands |= {oid for oid, _ in r_comp.get((cc, x), [])}
        if not cands and rs[1]:
            sets = [{oid for oid, _ in r_tok.get((cc, t), [])}
                    for t in {w for ts in rs[1] for w in ts} if len(t) >= 4]
            sets = [s for s in sets if s]
            if sets:
                cands = set.intersection(*sets) if len(sets) > 1 else set(sets[0])
                if len(cands) > 3000:
                    cands = set()
        out = []
        for e in (regs.get(cc) or {}).get("registry", []):
            if e.get("person_id") or e.get("status") in DEAD:
                continue
            nm = (e.get("name") or "").strip()
            if nm and e.get("org_id") in cands and match(rs, sig(nm)):
                out.append({"org_id": e.get("org_id"), "name": nm,
                            "status": e.get("status")})
        return out

    plan = json.load(open(os.path.join(OUT, "repair_plan.json"), encoding="utf-8"))
    missing = Counter()
    for x in plan["broken"]:
        if x["cat"] in ("work_org", "related_org") and x["action"] in (
                "null_collision", "null_absent"):
            missing[(x["cc"], x["ref_name"])] += 1

    rows = []
    for (cc, name), n in missing.most_common():
        rows.append({
            "cc": cc,
            "organization": name,
            "refs": n,
            "profile_elsewhere": profile_hits(cc, name)[:5],
            "registry": registry_hits(cc, name)[:5],
        })

    with open(os.path.join(OUT, "top_missing_orgs.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "top_missing_orgs.csv"), "w", encoding="utf-8-sig",
              newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "cc", "organization", "broken_refs",
                    "profile_elsewhere", "registry_entries"])
        for i, r in enumerate(rows[:100], 1):
            w.writerow([i, r["cc"], r["organization"], r["refs"],
                        ";".join(r["profile_elsewhere"]),
                        ";".join(f"{e['org_id']}:{e['status']}" for e in r["registry"])])

    print(f"rows={len(rows)} -> {os.path.join(OUT, 'top_missing_orgs.csv')}")
    for i, r in enumerate(rows[:50], 1):
        print(f"{i:>2}. {r['refs']:>3} {r['cc']} {r['organization']}")
        if r["profile_elsewhere"]:
            print(f"      profile_elsewhere={r['profile_elsewhere']}")
        if r["registry"]:
            print(f"      registry={[(e['org_id'], e['status']) for e in r['registry']]}")


if __name__ == "__main__":
    main()

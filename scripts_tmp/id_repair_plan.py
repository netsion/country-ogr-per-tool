# -*- coding: utf-8 -*-
"""Build a mechanical repair plan for broken ID references.

For every reference:
  - resolve intended entity by NAME against (a) real profiles, (b) active
    registry entries without a profile
  - decide: replace_profile | fill_profile | null_registered | null_collision |
            null_absent | review_ambiguous | keep

Pseudo-ID / cross-type-ID / placeholder-ID are all treated by name; if the name
cannot be resolved they become null_absent.

Output: output/_id_audit/repair_plan.json + repair_plan_summary.json
Usage: python scripts_tmp/id_repair_plan.py
"""
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, load_datasets, match, sig  # noqa: E402

ACTIVE = {None, "profiled", "auto_registered", "planned", "target", "listed",
          "identified", "pending", "skeleton", "registered", "active",
          "auto_registered_legacy"}
# statuses whose ID must NOT be used for linking (stale/shadow identities)
DEAD = {"trimmed", "merged", "removed", "duplicate", "excluded",
        "deprecated_broken_id", "archived", "pruned"}


def names(d, kind):
    if kind == "org":
        bi = d.get("basic_info") or {}
        vals = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")]
        vals += bi.get("aliases") or []
    else:
        vals = [d.get("name"), d.get("name_en"), d.get("name_zh")]
        vals += d.get("aliases") or []
    c, t = set(), []
    for v in vals:
        cc, tt = sig(v)
        c |= cc
        t += tt
    return c, t


def entry_name(e):
    return (e.get("name") or e.get("name_en") or e.get("name_zh") or "").strip()


def main():
    latest, _ = load_datasets()
    org_prof = {}    # oid -> (sig, name)
    per_prof = {}
    org_prof_cc = {}
    per_prof_cc = {}
    org_reg = defaultdict(list)   # oid -> [{name,status}]
    per_reg = defaultdict(list)

    for cc, (date, folder) in sorted(latest.items()):
        rp = os.path.join(folder, "id_registry.json")
        reg = json.load(open(rp, encoding="utf-8")) if os.path.exists(rp) else {}
        for e in reg.get("registry") or []:
            oid = e.get("org_id")
            if oid and not e.get("person_id") and e.get("status") not in DEAD:
                org_reg[oid].append(e)
        for e in (reg.get("registry") or []) + (reg.get("person_registry") or []):
            pid = e.get("person_id")
            if pid and e.get("status") not in DEAD:
                per_reg[pid].append(e)
        for f in glob.glob(os.path.join(folder, "orgs", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            oid = d.get("org_id")
            org_prof[oid] = names(d, "org")
            org_prof_cc[oid] = cc
        for f in glob.glob(os.path.join(folder, "persons", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            pid = d.get("person_id")
            per_prof[pid] = names(d, "person")
            per_prof_cc[pid] = cc

    # indexes
    def build_index(sig_map):
        comp = defaultdict(set)
        tok = defaultdict(set)
        for k, (c, t) in sig_map.items():
            for x in c:
                comp[x].add(k)
            for ts in t:
                for w in ts:
                    if len(w) >= 4:
                        tok[w].add(k)
        return comp, tok

    p_comp, p_tok = build_index(org_prof)
    q_comp, q_tok = build_index(per_prof)

    def build_reg_index(reg):
        comp = defaultdict(set)
        tok = defaultdict(set)
        for k, entries in reg.items():
            for e in entries:
                nm = entry_name(e)
                if not nm:
                    continue
                c, t = sig(nm)
                for x in c:
                    comp[x].add(k)
                for ts in t:
                    for w in ts:
                        if len(w) >= 4:
                            tok[w].add(k)
        return comp, tok

    or_comp, or_tok = build_reg_index(org_reg)
    pr_comp, pr_tok = build_reg_index(per_reg)

    def exact_hit(name, target_id, table):
        rc = sig(name)[0]
        tc = (table.get(target_id) or (set(), []))[0]
        return bool(rc & tc)

    def resolve(name, comp, tok, sig_map, cc=None):
        rs = sig(name)
        cands = set()
        for x in rs[0]:
            cands |= comp.get(x, set())
        if not cands and rs[1]:
            sets = [tok[t] for t in ({w for ts in rs[1] for w in ts} - {''}) if len(t) >= 4]
            if sets:
                cands = set.intersection(*sets) if len(sets) > 1 else set(sets[0])
                if len(cands) > 3000:
                    cands = set()
        hits = [k for k in cands if match(rs, sig_map[k])]
        return sorted(set(hits))

    def resolve_registry(name, reg, comp, tok):
        rs = sig(name)
        cands = set()
        for x in rs[0]:
            cands |= comp.get(x, set())
        if not cands and rs[1]:
            sets = [tok[t] for t in ({w for ts in rs[1] for w in ts} - {''}) if len(t) >= 4]
            if sets:
                cands = set.intersection(*sets) if len(sets) > 1 else set(sets[0])
                if len(cands) > 3000:
                    cands = set()
        hits = []
        for k in cands:
            if any(match(rs, sig(entry_name(e))) for e in reg[k] if entry_name(e)):
                hits.append(k)
        return sorted(set(hits))

    stats = Counter()
    by_cat = defaultdict(Counter)
    rows = []
    missing_names = Counter()

    def plan_org(cc, name, oid, cat, ref_meta, allow_global=False):
        ph_all = resolve(name, p_comp, p_tok, org_prof)
        ph_same = [x for x in ph_all if org_prof_cc.get(x) == cc]
        ph = ph_same
        if not ph and allow_global:
            ph = [x for x in ph_all if exact_hit(name, x, org_prof)]
        if oid in org_prof and oid in ph:
            action = "keep"
        elif len(ph) == 1:
            action = "replace_profile"
        elif len(ph) > 1:
            action = "review_ambiguous"
        else:
            rh_all = [x for x in resolve_registry(name, org_reg, or_comp, or_tok)
                      if x not in org_prof]
            rh_same = [x for x in rh_all if x.split("-")[0].lower() == cc]
            rh = rh_same
            if not rh and allow_global:
                rcs = sig(name)[0]
                rh = [x for x in rh_all
                      if any(rcs & sig(entry_name(e))[0]
                             for e in org_reg[x] if entry_name(e))]
            if len(rh) == 1:
                action = "keep_registered" if rh[0] == oid else "replace_registered"
            elif len(rh) > 1:
                action = "review_ambiguous"
            else:
                # id is a profile but the name points to a collision shadow
                action = "null_collision" if oid in org_prof else "null_absent"
                if action == "null_absent":
                    missing_names[(cc, name)] += 1
        stats[action] += 1
        by_cat[cat][action] += 1
        if action != "keep":
            row = dict(ref_meta)
            sug = (ph[0] if action == "replace_profile"
                   else rh[0] if action == "replace_registered" else None)
            mt = None
            if sug:
                mt = "exact" if exact_hit(name, sug, org_prof) else "fuzzy"
            row.update({"cat": cat, "cc": cc, "ref_name": name, "current_id": oid,
                        "action": action, "suggested": sug, "match_type": mt,
                        "candidates": ph[:5]})
            rows.append(row)

    def plan_person(cc, name, pid, cat, ref_meta, allow_global=True):
        ph_all = resolve(name, q_comp, q_tok, per_prof)
        ph_same = [x for x in ph_all if per_prof_cc.get(x) == cc]
        ph = ph_same
        if not ph and allow_global:
            ph = [x for x in ph_all if exact_hit(name, x, per_prof)]
        if pid in per_prof and pid in ph:
            action = "keep"
        elif len(ph) == 1:
            action = "replace_profile"
        elif len(ph) > 1:
            action = "review_ambiguous"
        else:
            rh_all = [x for x in resolve_registry(name, per_reg, pr_comp, pr_tok)
                      if x not in per_prof]
            rh_same = [x for x in rh_all if x.split("-")[0].lower() == cc]
            rh = rh_same
            if not rh and allow_global:
                rcs = sig(name)[0]
                rh = [x for x in rh_all
                      if any(rcs & sig(entry_name(e))[0]
                             for e in org_reg[x] if entry_name(e))]
            if len(rh) == 1:
                action = "keep_registered" if rh[0] == pid else "replace_registered"
            elif len(rh) > 1:
                action = "review_ambiguous"
            else:
                action = "null_collision" if pid in per_prof else "null_absent"
                if action == "null_absent":
                    missing_names[(cc, name)] += 1
        stats[action] += 1
        by_cat[cat][action] += 1
        if action != "keep":
            row = dict(ref_meta)
            sug = (ph[0] if action == "replace_profile"
                   else rh[0] if action == "replace_registered" else None)
            mt = None
            if sug:
                mt = "exact" if exact_hit(name, sug, per_prof) else "fuzzy"
            row.update({"cat": cat, "cc": cc, "ref_name": name, "current_id": pid,
                        "action": action, "suggested": sug, "match_type": mt,
                        "candidates": ph[:5]})
            rows.append(row)

    # null fill candidates
    fill_stats = Counter()
    fill_rows = []

    for cc, (date, folder) in sorted(latest.items()):
        for f in glob.glob(os.path.join(folder, "persons", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            pid = d.get("person_id")
            for w in d.get("work_experience") or []:
                if not isinstance(w, dict):
                    continue
                oid = w.get("org_id")
                name = w.get("organization") or ""
                if not oid:
                    ph = resolve(name, p_comp, p_tok, org_prof)
                    if len(ph) == 1:
                        fill_stats["org_null_fill_unique"] += 1
                        fill_rows.append({"cat": "work_org", "cc": cc, "person_id": pid,
                                          "ref_name": name, "action": "fill_profile",
                                          "suggested": ph[0]})
                    elif len(ph) > 1:
                        fill_stats["org_null_ambiguous"] += 1
                    continue
                plan_org(cc, name, oid, "work_org",
                         {"person_id": pid, "person": d.get("name")},
                         allow_global=False)
            for arr, cat, nk in [("person_relationships", "person_rel", "person_name"),
                                 ("family_members", "family", "name")]:
                for rel in d.get(arr) or []:
                    if not isinstance(rel, dict):
                        continue
                    rid = rel.get("person_id")
                    name = rel.get(nk) or ""
                    if not rid:
                        ph = resolve(name, q_comp, q_tok, per_prof)
                        if len(ph) == 1:
                            fill_stats[f"{cat}_null_fill_unique"] += 1
                            fill_rows.append({"cat": cat, "cc": cc, "person_id": pid,
                                              "ref_name": name, "action": "fill_profile",
                                              "suggested": ph[0]})
                        elif len(ph) > 1:
                            fill_stats[f"{cat}_null_ambiguous"] += 1
                        continue
                    plan_person(cc, name, rid, cat,
                                {"person_id": pid, "person": d.get("name")},
                                allow_global=(cat == "person_rel"))

        for f in glob.glob(os.path.join(folder, "orgs", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            oid = d.get("org_id")
            for kp in d.get("key_people") or []:
                if not isinstance(kp, dict):
                    continue
                rid = kp.get("person_id")
                if not rid:
                    continue
                plan_person(cc, kp.get("name") or "", rid, "key_people",
                            {"org_id": oid}, allow_global=False)
            for re_ in d.get("related_entities") or []:
                if not isinstance(re_, dict):
                    continue
                rid = re_.get("org_id")
                if not rid:
                    continue
                plan_org(cc, re_.get("org_name") or "", rid, "related_org",
                         {"org_id": oid}, allow_global=True)

    summary = {
        "generated_at": "2026-11-13",
        "actions": dict(stats),
        "by_cat": {k: dict(v) for k, v in by_cat.items()},
        "null_fill": dict(fill_stats),
        "top_missing_names": [[cc, nm, c] for (cc, nm), c in missing_names.most_common(80)],
    }
    with open(os.path.join(OUT, "repair_plan_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "repair_plan.json"), "w", encoding="utf-8") as fh:
        json.dump({"broken": rows, "null_fill": fill_rows}, fh, ensure_ascii=False, indent=1)

    print(json.dumps(summary["actions"], ensure_ascii=False, indent=1))
    print("by_cat", json.dumps(summary["by_cat"], ensure_ascii=False, indent=1))
    print("null_fill", json.dumps(summary["null_fill"], ensure_ascii=False, indent=1))
    print("top missing names:")
    for x in summary["top_missing_names"][:30]:
        print(x)
    print("plan ->", os.path.join(OUT, "repair_plan.json"))


if __name__ == "__main__":
    main()

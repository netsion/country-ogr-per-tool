# -*- coding: utf-8 -*-
"""Registry-level ID collision & reference impact audit.

Root-cause audit: the id_registry.json of several datasets contains MULTIPLE
different identities under the SAME org_id / person_id (ID allocator collisions,
usually counter rollback or concurrent registration). Only one profile file can
exist per ID, so every reference to the "shadow" identity silently lands on the
other person/org.

This script:
  1. detects org/person ID collisions (distinct normalized names, same ID)
  2. classifies every reference (work_org / person_rel / family / key_people /
     related_org) against registry + profiles:
        profile_ok | profile_wrong | collision_shadow | registered_no_profile
        | registry_wrong_name | ghost
  3. reports the impact per country and top collision cases

Usage: python scripts_tmp/registry_collision_audit.py
Output: output/_id_audit/collision_report.json + collision_report.md
"""
import glob
import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, load_datasets, match, sig  # noqa: E402


def entry_name(e):
    return (e.get("name") or e.get("name_en") or e.get("name_zh")
            or e.get("name_local") or "").strip()


def distinct_groups(entries):
    groups = []   # list of (sig, [names])
    for e in entries:
        nm = entry_name(e)
        if not nm:
            continue
        s = sig(nm)
        hit = None
        for i, (gs, names) in enumerate(groups):
            if match(s, gs):
                hit = i
                break
        if hit is None:
            groups.append((s, [nm]))
        else:
            groups[hit][1].append(nm)
    return groups


def main():
    latest, _ = load_datasets()
    os.makedirs(OUT, exist_ok=True)

    org_reg = {}    # (cc, oid) -> entries
    per_reg = {}    # (cc, pid) -> entries
    org_prof = {}   # (cc, oid) -> (sig, name)
    per_prof = {}   # (cc, pid) -> (sig, name)
    collisions = {"org": {}, "person": {}}   # cc -> id -> info

    for cc, (date, folder) in sorted(latest.items()):
        rp = os.path.join(folder, "id_registry.json")
        reg = json.load(open(rp, encoding="utf-8")) if os.path.exists(rp) else {}
        for e in reg.get("registry") or []:
            oid = e.get("org_id")
            if oid:
                org_reg[(cc, oid)] = org_reg.get((cc, oid), []) + [e]
            pid = e.get("person_id")
            if pid:  # MX contamination: person rows stored in the org registry
                per_reg[(cc, pid)] = per_reg.get((cc, pid), []) + [e]
        for e in reg.get("person_registry") or []:
            pid = e.get("person_id")
            if pid:
                per_reg[(cc, pid)] = per_reg.get((cc, pid), []) + [e]

        for f in glob.glob(os.path.join(folder, "orgs", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            bi = d.get("basic_info") or {}
            oid = d.get("org_id")
            org_prof[(cc, oid)] = (sig_org(d), bi.get("name_zh") or bi.get("name_original"))
        for f in glob.glob(os.path.join(folder, "persons", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            pid = d.get("person_id")
            per_prof[(cc, pid)] = (sig_person(d), d.get("name") or d.get("name_zh"))

    # ---- collision detection ----
    for (cc, oid), entries in org_reg.items():
        groups = distinct_groups(entries)
        if len(groups) < 2:
            continue
        prof = org_prof.get((cc, oid))
        prof_sig = prof[0] if prof else None
        shadow = [nm for gs, names in groups if not (prof_sig and match(gs, prof_sig))
                  for nm in names]
        if prof is None:
            # no profile at all: every distinct name is a shadow identity
            shadow = [nm for _, names in groups for nm in names]
        pname = prof[1] if prof else None
        collisions["org"].setdefault(cc, {})[oid] = {
            "profile_name": pname,
            "entries": [{"name": entry_name(e), "status": e.get("status")} for e in entries],
            "distinct_names": [names[0] for _, names in groups],
            "shadow_names": sorted(set(shadow)),
        }
    for (cc, pid), entries in per_reg.items():
        groups = distinct_groups(entries)
        if len(groups) < 2:
            continue
        prof = per_prof.get((cc, pid))
        prof_sig = prof[0] if prof else None
        shadow = [nm for gs, names in groups if not (prof_sig and match(gs, prof_sig))
                  for nm in names]
        if prof is None:
            shadow = [nm for _, names in groups for nm in names]
        collisions["person"].setdefault(cc, {})[pid] = {
            "profile_name": prof[1] if prof else None,
            "entries": [{"name": entry_name(e), "status": e.get("status")} for e in entries],
            "distinct_names": [names[0] for _, names in groups],
            "shadow_names": sorted(set(shadow)),
        }

    # ---- global maps (refs may point to another country's ID) ----
    g_org_prof = {oid: v for (cc, oid), v in org_prof.items()}
    g_per_prof = {pid: v for (cc, pid), v in per_prof.items()}
    g_org_reg = defaultdict(list)
    for (cc, oid), ents in org_reg.items():
        g_org_reg[oid] += ents
    g_per_reg = defaultdict(list)
    for (cc, pid), ents in per_reg.items():
        g_per_reg[pid] += ents

    # ---- reference classification ----
    def id_cc(x):
        return x.split("-")[0].lower() if x else ""

    def classify_org_ref(cc, name, oid):
        ref_sig = sig(name)
        if oid in g_org_prof:
            psig, pname = g_org_prof[oid]
            if match(ref_sig, psig):
                return "profile_ok", None
            col = collisions["org"].get(id_cc(oid), {}).get(oid)
            if col and any(match(ref_sig, sig(n)) for n in col["shadow_names"]):
                return "collision_shadow", col["profile_name"]
            return "profile_wrong", pname
        if oid in g_org_reg:
            entries = g_org_reg[oid]
            if any(match(ref_sig, sig(entry_name(e))) for e in entries if entry_name(e)):
                return "registered_no_profile", None
            return "registry_wrong_name", None
        return "ghost", None

    def classify_person_ref(cc, name, pid, prefer_cc=None):
        ref_sig = sig(name)
        if pid in g_per_prof:
            psig, pname = g_per_prof[pid]
            if match(ref_sig, psig):
                return "profile_ok", None
            col = collisions["person"].get(id_cc(pid), {}).get(pid)
            if col and any(match(ref_sig, sig(n)) for n in col["shadow_names"]):
                return "collision_shadow", col["profile_name"]
            return "profile_wrong", pname
        if pid in g_per_reg:
            entries = g_per_reg[pid]
            if any(match(ref_sig, sig(entry_name(e))) for e in entries if entry_name(e)):
                return "registered_no_profile", None
            return "registry_wrong_name", None
        return "ghost", None

    result = {
        "work_org": Counter(), "person_rel": Counter(), "family": Counter(),
        "key_people": Counter(), "related_org": Counter(),
    }
    per_country = defaultdict(lambda: defaultdict(Counter))
    shadow_rows = defaultdict(list)

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
                if not oid:
                    result["work_org"]["null_id"] += 1
                    per_country[cc]["work_org"]["null_id"] += 1
                    continue
                cls, cur = classify_org_ref(cc, w.get("organization") or "", oid)
                result["work_org"][cls] += 1
                per_country[cc]["work_org"][cls] += 1
                if cls in ("collision_shadow", "profile_wrong", "registry_wrong_name"):
                    shadow_rows["work_org"].append(
                        {"cc": cc, "person_id": pid, "ref_name": w.get("organization"),
                         "id": oid, "class": cls, "current_profile": cur})
            for arr, bucket, nk in [("person_relationships", "person_rel", "person_name"),
                                    ("family_members", "family", "name")]:
                for rel in d.get(arr) or []:
                    if not isinstance(rel, dict):
                        continue
                    rid = rel.get("person_id")
                    if not rid:
                        result[bucket]["null_id"] += 1
                        per_country[cc][bucket]["null_id"] += 1
                        continue
                    cls, cur = classify_person_ref(cc, rel.get(nk) or "", rid)
                    result[bucket][cls] += 1
                    per_country[cc][bucket][cls] += 1
                    if cls in ("collision_shadow", "profile_wrong", "registry_wrong_name"):
                        shadow_rows[bucket].append(
                            {"cc": cc, "person_id": pid, "ref_name": rel.get(nk),
                             "id": rid, "class": cls, "current_profile": cur})

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
                    result["key_people"]["null_id"] += 1
                    per_country[cc]["key_people"]["null_id"] += 1
                    continue
                cls, cur = classify_person_ref(cc, kp.get("name") or "", rid)
                result["key_people"][cls] += 1
                per_country[cc]["key_people"][cls] += 1
                if cls in ("collision_shadow", "profile_wrong", "registry_wrong_name"):
                    shadow_rows["key_people"].append(
                        {"cc": cc, "org_id": oid, "ref_name": kp.get("name"),
                         "id": rid, "class": cls, "current_profile": cur})
            for re_ in d.get("related_entities") or []:
                if not isinstance(re_, dict):
                    continue
                rid = re_.get("org_id")
                if not rid:
                    result["related_org"]["null_id"] += 1
                    per_country[cc]["related_org"]["null_id"] += 1
                    continue
                cls, cur = classify_org_ref(cc, re_.get("org_name") or "", rid)
                result["related_org"][cls] += 1
                per_country[cc]["related_org"][cls] += 1
                if cls in ("collision_shadow", "profile_wrong", "registry_wrong_name"):
                    shadow_rows["related_org"].append(
                        {"cc": cc, "org_id": oid, "ref_name": re_.get("org_name"),
                         "id": rid, "class": cls, "current_profile": cur})

    report = {
        "generated_at": "2026-11-13",
        "totals": {"persons": len(per_prof), "orgs": len(org_prof),
                   "countries": len(latest)},
        "collision_counts": {
            "org_ids": sum(len(v) for v in collisions["org"].values()),
            "person_ids": sum(len(v) for v in collisions["person"].values()),
            "org_by_cc": {cc: len(v) for cc, v in collisions["org"].items()},
            "person_by_cc": {cc: len(v) for cc, v in collisions["person"].items()},
        },
        "reference_classes": {k: dict(v) for k, v in result.items()},
        "per_country": {cc: {b: dict(c) for b, c in m.items()}
                        for cc, m in per_country.items()},
        "collisions": collisions,
        "shadow_samples": {k: v[:200] for k, v in shadow_rows.items()},
    }
    with open(os.path.join(OUT, "collision_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)

    # markdown
    L = ["# ID 碰撞与引用影响审计\n",
         f"- person 画像 {len(per_prof):,}，org 画像 {len(org_prof):,}",
         f"- 同一 org_id 挂多个不同组织：**{report['collision_counts']['org_ids']:,}** 个 ID",
         f"- 同一 person_id 挂多个不同人物：**{report['collision_counts']['person_ids']:,}** 个 ID",
         "",
         "## 引用分类\n",
         "| 引用方向 | profile_ok | profile_wrong | collision_shadow | registered_no_profile | registry_wrong_name | ghost | null_id |",
         "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for b in ("work_org", "person_rel", "family", "key_people", "related_org"):
        c = result[b]
        L.append(f"| {b} | {c.get('profile_ok',0):,} | {c.get('profile_wrong',0):,} | "
                 f"{c.get('collision_shadow',0):,} | {c.get('registered_no_profile',0):,} | "
                 f"{c.get('registry_wrong_name',0):,} | {c.get('ghost',0):,} | "
                 f"{c.get('null_id',0):,} |")
    L.append("")
    L.append("## 碰撞最严重的国家（org ID）\n")
    L.append("| 国家 | 碰撞 org_id 数 | 碰撞 person_id 数 |")
    L.append("|---|---:|---:|")
    for cc, n in sorted(report["collision_counts"]["org_by_cc"].items(),
                        key=lambda x: -x[1])[:20]:
        L.append(f"| {cc} | {n} | {report['collision_counts']['person_by_cc'].get(cc,0)} |")
    L.append("")
    L.append("## 典型案例\n")
    for cc, ids in collisions["org"].items():
        for oid, info in list(ids.items())[:3]:
            L.append(f"- **{cc} {oid}**：profile={info['profile_name']}；"
                     f"影子身份={info['shadow_names']}")
    with open(os.path.join(OUT, "collision_report.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))

    print(json.dumps(report["collision_counts"], ensure_ascii=False, indent=1))
    print(json.dumps(report["reference_classes"], ensure_ascii=False, indent=1))
    print("report ->", os.path.join(OUT, "collision_report.md"))


def sig_org(d):
    bi = d.get("basic_info") or {}
    vals = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")]
    vals += bi.get("aliases") or []
    return _union(vals)


def sig_person(d):
    vals = [d.get("name"), d.get("name_en"), d.get("name_zh")]
    vals += d.get("aliases") or []
    return _union(vals)


def _union(vals):
    compacts, tokens = set(), []
    for v in vals:
        c, t = sig(v)
        compacts |= c
        tokens += t
    return compacts, tokens


if __name__ == "__main__":
    main()

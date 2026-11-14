# -*- coding: utf-8 -*-
"""Execute 18 duplicate-organisation group identities (WHO deferred).

For each group: remove all member shadow entries from source registries, create
one canonical registry entry under the group's recommended country/category, and
redirect refs matching any member shadow to the new ID.
Usage: python scripts_tmp/execute_duplicate_org_plan.py --dry|--apply
"""
import csv, glob, json, os, re, sys, time
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, load_datasets, match, sig

PLAN = os.path.join(OUT, "registry826_duplicate_org_plan.csv")


def save_json(f, d):
    payload = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    tmp = f + ".tmp"; last = None
    for _ in range(6):
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh: fh.write(payload)
            os.replace(tmp, f); return
        except PermissionError as e: last = e; time.sleep(0.5)
    for _ in range(3):
        try:
            with open(f, "w", encoding="utf-8", newline="\n") as fh: fh.write(payload)
            try: os.unlink(tmp)
            except OSError: pass
            return
        except PermissionError as e: last = e; time.sleep(1.0)
    raise last


def loose(a, b):
    na = re.sub(r"[\s\.\,\-\'’`&·:：/\\|（）()\[\]【】]+", "", (a or "").lower())
    nb = re.sub(r"[\s\.\,\-\'’&·:：/\\|（）()\[\]【】]+", "", (b or "").lower())
    return bool(na and nb and (na == nb or (len(na) >= 4 and len(nb) >= 4 and (na in nb or nb in na))))


def ref_name(item, kind):
    keys = (["organization", "org_name", "organization_en"] if kind == "org"
            else ["person_name", "name"] if kind in ("rel", "family") else ["name", "name_en"])
    for k in keys:
        v = item.get(k)
        if isinstance(v, str) and v.strip(): return v.strip()
    return ""


def parse_members(s):
    out = []
    for part in (s or "").split("|"):
        part = part.strip()
        if "｜" not in part:
            continue
        cid, name = part.split("｜", 1)
        out.append((cid.strip(), name.strip()))
    return out


def main():
    apply = "--apply" in sys.argv
    rows = list(csv.DictReader(open(PLAN, encoding="utf-8-sig")))
    latest, _ = load_datasets()
    regpath = {}
    for cc, (date, folder) in latest.items():
        p = os.path.join(folder, "id_registry.json")
        if os.path.exists(p): regpath[cc] = p
    regs = {cc: json.load(open(p, encoding="utf-8")) for cc, p in regpath.items()}
    undo = defaultdict(list); refs = []
    stats = Counter()

    for r in rows:
        if r["处理方式"] != "create_single_identity":
            continue
        new_id = r["候选新ID"]
        tcc = new_id[:2].lower()
        if new_id in {e.get("org_id") for reg in regs.values() for e in (reg.get("registry") or [])}:
            stats["new_id_exists"] += 1; continue
        for cid, name in parse_members(r["成员明细"]):
            scc = cid[:2].lower()
            if scc not in regs:
                stats["missing_source"] += 1; continue
            reg = regs[scc]
            ents = reg.get("registry") or []
            idx = None
            for i, e in enumerate(ents):
                if e.get("org_id") == cid and (e.get("name") or "").strip() == name:
                    idx = i; break
            if idx is None:
                for i, e in enumerate(ents):
                    if e.get("org_id") == cid and loose(name, e.get("name")):
                        idx = i; break
            if idx is None:
                stats["member_not_found"] += 1; continue
            old = ents.pop(idx)
            reg["registry"] = ents
            undo[regpath[scc]].append({"action": "remove_shadow", "id": cid, "old": old,
                                       "new_id": new_id, "group": r["组号"]})
            stats["removed"] += 1
        # add target
        if tcc not in regs:
            stats["missing_target"] += 1; continue
        new = {"org_id": new_id, "name": r["推荐主身份名称"], "org_type": r["建议类别"],
               "status": "auto_registered", "source": f"A2 duplicate group {r['组号']}",
               "notes": f"合并重复组织身份组 {r['组号']}；成员数 {r['成员数']}"}
        regs[tcc].setdefault("registry", []).append(new)
        undo[regpath[tcc]].append({"action": "add_target", "new": new, "group": r["组号"]})
        stats["created"] += 1

    if apply:
        for cc, reg in regs.items(): save_json(regpath[cc], reg)

    # refs: scan using all member shadow names
    member_map = defaultdict(list)
    for r in rows:
        if r["处理方式"] != "create_single_identity": continue
        for cid, name in parse_members(r["成员明细"]):
            member_map[cid].append((name, r["候选新ID"]))
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8")); dirty = False
        for arr, field, kind in [("work_experience", "org_id", "org"),
                                 ("person_relationships", "person_id", "rel"),
                                 ("family_members", "person_id", "family")]:
            for i, x in enumerate(d.get(arr) or []):
                if not isinstance(x, dict): continue
                cid = x.get(field)
                if cid not in member_map: continue
                nm = ref_name(x, kind)
                hits = [nid for m, nid in member_map[cid] if loose(nm, m) or match(sig(nm), (sig(m)[0], []))]
                hits = sorted(set(hits))
                if len(hits) == 1:
                    refs.append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"), "array": arr,
                                 "index": i, "field": field, "old": cid, "new": hits[0], "ref_name": nm})
                    x[field] = hits[0]; dirty = True
        if apply and dirty: save_json(f, d)
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8")); dirty = False
        for arr, field, kind in [("key_people", "person_id", "person"), ("related_entities", "org_id", "org")]:
            for i, x in enumerate(d.get(arr) or []):
                if not isinstance(x, dict): continue
                cid = x.get(field)
                if cid not in member_map: continue
                nm = ref_name(x, kind)
                hits = [nid for m, nid in member_map[cid] if loose(nm, m) or match(sig(nm), (sig(m)[0], []))]
                hits = sorted(set(hits))
                if len(hits) == 1:
                    refs.append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"), "array": arr,
                                 "index": i, "field": field, "old": cid, "new": hits[0], "ref_name": nm})
                    x[field] = hits[0]; dirty = True
        if apply and dirty: save_json(f, d)

    summary = {"groups": len(rows), "created": stats["created"], "removed": stats["removed"],
               "member_not_found": stats["member_not_found"], "refs": len(refs),
               "stats": dict(stats)}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if apply:
        undo = {k: v for k, v in undo.items()}
        json.dump({"registry": undo, "ref_changes": refs},
                  open(os.path.join(OUT, "registry826_duplicate_org_undo.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("undo ->", os.path.join(OUT, "registry826_duplicate_org_undo.json"))
    else:
        undo = {k: v for k, v in undo.items()}
        json.dump({"registry": undo, "ref_changes": refs},
                  open(os.path.join(OUT, "registry826_duplicate_org_dry_undo.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("DRY")


if __name__ == "__main__":
    main()

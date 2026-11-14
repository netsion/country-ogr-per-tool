# -*- coding: utf-8 -*-
"""Close the remaining 260 deferred org candidates:
  - archive shadow registry entries as unresolved_shadow
  - for rows with current refs matching the shadow, set the org_id to null
  - never touch owner profile entries / owner refs
No new IDs, no profile changes.
Usage: python scripts_tmp/archive_deferred_shadows.py --dry|--apply
"""
import csv, glob, json, os, re, sys, time
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, load_datasets, match, sig

REVIEW = os.path.join(BASE, "outputs/registry826_20261113/registry_newid_pending826_reviewed.csv")


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


def ref_name(item, kind):
    keys = (["organization", "org_name", "organization_en"] if kind == "org"
            else ["person_name", "name"] if kind in ("rel", "family") else ["name", "name_en"])
    for k in keys:
        v = item.get(k)
        if isinstance(v, str) and v.strip(): return v.strip()
    return ""


def main():
    apply = "--apply" in sys.argv
    rows = list(csv.DictReader(open(REVIEW, encoding="utf-8-sig")))
    defer = [(i + 1, r) for i, r in enumerate(rows) if r["复核结论"] == "挂起"]
    print("defer rows", len(defer))
    latest, _ = load_datasets()
    regpath = {}
    for cc, (date, folder) in latest.items():
        p = os.path.join(folder, "id_registry.json")
        if os.path.exists(p): regpath[cc] = p
    regs = {cc: json.load(open(p, encoding="utf-8")) for cc, p in regpath.items()}

    # owner sigs
    owner = {}
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8")); oid = d.get("org_id")
        if not oid: continue
        bi = d.get("basic_info") or {}
        vals = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")] + (bi.get("aliases") or [])
        c = set()
        for v in vals: c |= sig(v)[0]
        owner[oid] = c

    undo = {"registry": defaultdict(list), "ref_changes": []}
    stats = Counter(); notfound = []

    # archive registry shadows
    for seq, r in defer:
        cid = r["冲突ID"]; cc = cid[:2].lower(); name = r["影子名称"].strip()
        if cc not in regs:
            stats["missing_registry"] += 1; continue
        reg = regs[cc]; ents = reg.get("registry") or []
        idx = None
        for i, e in enumerate(ents):
            if e.get("org_id") == cid and (e.get("name") or "").strip() == name:
                idx = i; break
        if idx is None:
            for i, e in enumerate(ents):
                nm = (e.get("name") or "").strip()
                if e.get("org_id") == cid and nm and match(sig(name), (sig(nm)[0], [])):
                    idx = i; break
        if idx is None:
            stats["not_found"] += 1; notfound.append((seq, cid, name)); continue
        old = ents.pop(idx)
        old["status"] = "unresolved_shadow"
        old["deprecated_reason"] = "826 defer: unresolved entity granularity"
        reg.setdefault("deprecated_registry", []).append(old)
        reg["registry"] = ents
        undo["registry"][regpath[cc]].append({"id": cid, "name": name, "old": old, "seq": seq})
        stats["archived"] += 1

    if apply:
        for cc, reg in regs.items(): save_json(regpath[cc], reg)

    # refs: null only refs matching shadow, not owner
    by_cid = defaultdict(list)
    for seq, r in defer:
        by_cid[r["冲突ID"]].append(r)
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8")); dirty = False
        for i, w in enumerate(d.get("work_experience") or []):
            if not isinstance(w, dict): continue
            cid = w.get("org_id")
            if cid not in by_cid: continue
            nm = ref_name(w, "org")
            if not nm: continue
            if match(sig(nm), (owner.get(cid, set()), [])):
                stats["owner_ref_skipped"] += 1; continue
            hits = [r for r in by_cid[cid] if match(sig(nm), (sig(r["影子名称"])[0], []))]
            if len(hits) == 1:
                undo["ref_changes"].append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                            "array": "work_experience", "index": i,
                                            "field": "org_id", "old": cid, "new": None,
                                            "ref_name": nm})
                w["org_id"] = None; dirty = True; stats["refs_nulled"] += 1
        if apply and dirty: save_json(f, d)
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8")); dirty = False
        for i, x in enumerate(d.get("related_entities") or []):
            if not isinstance(x, dict): continue
            cid = x.get("org_id")
            if cid not in by_cid: continue
            nm = ref_name(x, "org")
            if not nm: continue
            if match(sig(nm), (owner.get(cid, set()), [])):
                stats["owner_ref_skipped"] += 1; continue
            hits = [r for r in by_cid[cid] if match(sig(nm), (sig(r["影子名称"])[0], []))]
            if len(hits) == 1:
                undo["ref_changes"].append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                            "array": "related_entities", "index": i,
                                            "field": "org_id", "old": cid, "new": None,
                                            "ref_name": nm})
                x["org_id"] = None; dirty = True; stats["refs_nulled"] += 1
        if apply and dirty: save_json(f, d)

    summary = {"defer": len(defer), "archived": stats["archived"], "not_found": stats["not_found"],
               "refs_nulled": stats["refs_nulled"], "owner_ref_skipped": stats["owner_ref_skipped"],
               "not_found_samples": notfound[:60]}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if apply:
        undo = {"registry": {k: v for k, v in undo["registry"].items()},
                "ref_changes": undo["ref_changes"]}
        json.dump(undo, open(os.path.join(OUT, "archive_deferred_shadows_undo.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        json.dump(summary, open(os.path.join(OUT, "archive_deferred_shadows_summary.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("undo ->", os.path.join(OUT, "archive_deferred_shadows_undo.json"))
    else:
        print("DRY")


if __name__ == "__main__":
    main()

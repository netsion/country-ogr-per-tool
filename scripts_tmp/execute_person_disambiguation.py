# -*- coding: utf-8 -*-
"""Execute the 141 person-name cleanup:
  - archive 139 person-name shadow entries from org registry
  - fix 1 organization text (keep org_id)
  - fix 1 person_id from org to person
No person-profile merges.
Usage: python scripts_tmp/execute_person_disambiguation.py --dry|--apply
"""
import csv, glob, json, os, re, sys, time
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, load_datasets, match, sig

PLAN = os.path.join(OUT, "registry826_person_disambiguation_141.csv")


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


def parse_pos(s):
    m = re.match(r"^(.*)#([A-Za-z_]+)\[(\d+)\]\.([A-Za-z_]+)$", s.strip())
    return m.groups() if m else None


def main():
    apply = "--apply" in sys.argv
    rows = list(csv.DictReader(open(PLAN, encoding="utf-8-sig")))
    archive = [r for r in rows if r["建议动作"] == "archive_shadow_no_ref"]
    fix_org = [r for r in rows if r["建议动作"] == "fix_org_text_keep_org_id"]
    fix_pid = [r for r in rows if r["建议动作"] == "replace_person_id"]
    print("archive", len(archive), "fix_org", len(fix_org), "fix_pid", len(fix_pid))

    latest, _ = load_datasets()
    regpath = {}; regs = {}
    for cc, (date, folder) in latest.items():
        p = os.path.join(folder, "id_registry.json")
        if os.path.exists(p):
            regpath[cc] = p; regs[cc] = json.load(open(p, encoding="utf-8"))
    undo = {"registry": defaultdict(list), "ref_changes": []}
    stats = Counter()

    # archive 139 shadows
    for r in archive:
        cid = r["冲突ID"]; cc = cid[:2].lower(); name = r["影子名称"].strip()
        if cc not in regs:
            stats["missing_registry"] += 1; continue
        reg = regs[cc]
        entries = reg.get("registry") or []
        idx = None
        for i, e in enumerate(entries):
            if e.get("org_id") == cid and (e.get("name") or "").strip() == name:
                idx = i; break
        if idx is None:
            for i, e in enumerate(entries):
                nm = (e.get("name") or "").strip()
                if e.get("org_id") == cid and nm and match(sig(name), (sig(nm)[0], [])):
                    idx = i; break
        if idx is None:
            stats["not_found"] += 1; continue
        old = entries.pop(idx)
        orig = dict(old)
        old["status"] = "not_an_org"
        old["deprecated_reason"] = "person name in org registry (A2 person cleanup)"
        reg.setdefault("deprecated_registry", []).append(old)
        reg["registry"] = entries
        stats["archived"] += 1
        undo["registry"][regpath[cc]].append({"action": "archive_person_shadow", "id": cid,
                                              "old": orig, "archived": old, "name": name})
    if apply:
        for cc, reg in regs.items(): save_json(regpath[cc], reg)

    # fix org text
    for r in fix_org:
        pos = parse_pos(r["引用位置"])
        if not pos:
            stats["bad_pos"] += 1; continue
        rel, arr, idx, field = pos
        f = os.path.join(BASE, rel.replace("\\", "/"))
        d = json.load(open(f, encoding="utf-8"))
        item = (d.get(arr) or [])[int(idx)]
        old_org = item.get("organization")
        new_org = r["建议organization_text"]
        if apply:
            item["organization"] = new_org
            save_json(f, d)
        stats["org_text_fixed"] += 1
        undo["ref_changes"].append({"file": rel, "array": arr, "index": int(idx),
                                    "field": "organization", "old": old_org, "new": new_org})

    # fix person id
    for r in fix_pid:
        pos = parse_pos(r["引用位置"])
        if not pos:
            stats["bad_pos"] += 1; continue
        rel, arr, idx, field = pos
        f = os.path.join(BASE, rel.replace("\\", "/"))
        d = json.load(open(f, encoding="utf-8"))
        item = (d.get(arr) or [])[int(idx)]
        old = item.get(field)
        new = r["建议person_id"]
        if apply:
            item[field] = new
            save_json(f, d)
        stats["person_id_fixed"] += 1
        undo["ref_changes"].append({"file": rel, "array": arr, "index": int(idx),
                                    "field": field, "old": old, "new": new})

    summary = {"archive": len(archive), "fix_org": len(fix_org), "fix_pid": len(fix_pid),
               "stats": dict(stats), "ref_changes": len(undo["ref_changes"]),
               "registry_files": len(undo["registry"])}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if apply:
        undo["registry"] = {k: v for k, v in undo["registry"].items()}
        json.dump(undo, open(os.path.join(OUT, "registry826_person_fix_undo.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        json.dump(summary, open(os.path.join(OUT, "registry826_person_fix_summary.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("undo ->", os.path.join(OUT, "registry826_person_fix_undo.json"))
    else:
        undo["registry"] = {k: v for k, v in undo["registry"].items()}
        json.dump(undo, open(os.path.join(OUT, "registry826_person_fix_dry_undo.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("DRY")


if __name__ == "__main__":
    main()

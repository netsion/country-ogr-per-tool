# -*- coding: utf-8 -*-
"""A2: rebuild all _name_index.json files with the fixed generator.

Backs up the old index to output/_id_audit/name_index_before/.
Prints before/after stats (entries, short keys).
"""
import glob
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT

sys.path.insert(0, os.path.join(BASE, ".agents/skills/country-org-collector/scripts"))
import generate_name_index as G  # noqa: E402


def short_count(d):
    return sum(1 for k in d if len(str(k).strip()) <= 3)


def main():
    backup = os.path.join(OUT, "name_index_before")
    os.makedirs(backup, exist_ok=True)
    rows = []
    for folder in sorted(glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*"))):
        rel = os.path.relpath(folder, BASE).replace(os.sep, "/")
        parts = rel.split("/")
        cc, date = parts[1], parts[2]
        idx = os.path.join(folder, "_name_index.json")
        before = None
        if os.path.exists(idx):
            try:
                before = json.load(open(idx, encoding="utf-8"))
            except Exception:
                before = None
            dst = os.path.join(backup, f"{cc}_{date}.json")
            if not os.path.exists(dst):
                shutil.copy2(idx, dst)
        try:
            G.build_index(folder)
        except Exception as e:
            rows.append({"cc": cc, "date": date, "error": str(e)})
            continue
        after = json.load(open(idx, encoding="utf-8"))
        row = {
            "cc": cc, "date": date,
            "before": len(before) if before is not None else None,
            "after": len(after),
            "short_before": short_count(before) if before is not None else None,
            "short_after": short_count(after),
            "single_letter_after": sum(1 for k in after if len(str(k).strip()) == 1),
        }
        rows.append(row)
        print(row, flush=True)
    with open(os.path.join(OUT, "name_index_rebuild_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=1)
    tot_b = sum(r.get("before") or 0 for r in rows)
    tot_a = sum(r.get("after") or 0 for r in rows)
    sb = sum(r.get("short_before") or 0 for r in rows)
    sa = sum(r.get("short_after") or 0 for r in rows)
    print(json.dumps({"datasets": len(rows), "before": tot_b, "after": tot_a,
                      "short_before": sb, "short_after": sa,
                      "errors": [r for r in rows if r.get("error")]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Rollback Step 1 using step1_undo.json (only reverts if current == applied new)."""
import json
import os
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT


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
    # fallback: in-place write (may still fail if hard-locked)
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


def get_arr(d, name):
    return d.get(name) or []


def main():
    undo_name = "step1_undo.json"
    if "--undo" in sys.argv:
        undo_name = sys.argv[sys.argv.index("--undo") + 1]
    undo = json.load(open(os.path.join(OUT, undo_name), encoding="utf-8"))
    byfile = defaultdict(list)
    for u in undo:
        byfile[u["file"]].append(u)
    stats = Counter()
    conflicts = []
    changed = 0
    for rel, items in byfile.items():
        f = os.path.join(BASE, rel)
        if not os.path.exists(f):
            stats["missing_file"] += len(items)
            continue
        d = json.load(open(f, encoding="utf-8"))
        dirty = False
        for u in items:
            arr = get_arr(d, u["array"])
            i = u["index"]
            if i >= len(arr) or not isinstance(arr[i], dict):
                stats["bad_index"] += 1
                continue
            cur = arr[i].get(u["field"])
            if cur == u["new"]:
                arr[i][u["field"]] = u["old"]
                stats["reverted"] += 1
                dirty = True
            elif cur == u["old"]:
                stats["already_old"] += 1
            else:
                stats["conflict"] += 1
                conflicts.append({"file": rel, "array": u["array"], "index": i,
                                  "field": u["field"], "current": cur,
                                  "expected_new": u["new"], "old": u["old"]})
        if dirty:
            save_json(f, d)
            changed += 1
    out = {"reverted": stats["reverted"], "files": changed,
           "already_old": stats["already_old"], "conflict": stats["conflict"],
           "missing_file": stats["missing_file"], "bad_index": stats["bad_index"],
           "conflicts": conflicts[:200]}
    summary_name = undo_name.replace("_undo.json", "_rollback_summary.json")
    with open(os.path.join(OUT, summary_name), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "conflicts"},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

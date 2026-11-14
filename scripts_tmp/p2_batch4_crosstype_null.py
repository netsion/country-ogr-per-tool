# -*- coding: utf-8 -*-
"""P2 batch 4: remove cross-type IDs.

A person ID can never be an org_id and an org ID can never be a person_id.
These references are structurally invalid; null the ID while keeping the
organization/person name and description text.
"""
import glob
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from id_integrity_audit2 import BASE, OUT, load_datasets

PERSON_RE = re.compile(r"^[A-Z]{2}-PERSON-[0-9]{6}$")
ORG_RE = re.compile(r"^[A-Z]{2}-(?:GOV|SOE|CORP|NGO|ACAD|MEDIA|FIN|INTL|PARTY|MIL)-[0-9]{3}$")


def save_json(path, obj):
    payload = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    tmp = path + ".tmp"
    for _ in range(6):
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(payload)
            os.replace(tmp, path)
            return
        except PermissionError:
            time.sleep(0.5)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)


def main():
    apply = "--apply" in sys.argv
    latest, _ = load_datasets()
    changes = []
    stats = Counter()
    for cc, (date, folder) in sorted(latest.items()):
        for sub, arrs in (
            ("persons", (("work_experience", "org_id", PERSON_RE),
                         ("person_relationships", "person_id", ORG_RE),
                         ("family_members", "person_id", ORG_RE))),
            ("orgs", (("key_people", "person_id", ORG_RE),
                      ("related_entities", "org_id", PERSON_RE))),
        ):
            for f in glob.glob(os.path.join(folder, sub, "*.json")):
                if os.path.basename(f).startswith("_"):
                    continue
                data = json.load(open(f, encoding="utf-8"))
                dirty = False
                for arr, field, pattern in arrs:
                    for i, item in enumerate(data.get(arr) or []):
                        if not isinstance(item, dict):
                            continue
                        v = item.get(field)
                        if not isinstance(v, str) or not pattern.match(v):
                            continue
                        changes.append({
                            "file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                            "array": arr, "index": i, "field": field,
                            "old": v, "new": None,
                            "ref_name": item.get("organization") or item.get("org_name")
                                        or item.get("person_name") or item.get("name") or "",
                        })
                        item[field] = None
                        dirty = True
                        stats["refs_nulled"] += 1
                        stats[arr] += 1
                if apply and dirty:
                    save_json(f, data)

    summary = {"apply": apply, "refs_nulled": stats["refs_nulled"],
               "by_array": {k: v for k, v in stats.items() if k != "refs_nulled"}}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if apply:
        p = os.path.join(OUT, "p2_batch4_crosstype_undo.json")
        json.dump({"summary": summary, "changes": changes}, open(p, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("undo ->", p)
    else:
        print("DRY")


if __name__ == "__main__":
    main()

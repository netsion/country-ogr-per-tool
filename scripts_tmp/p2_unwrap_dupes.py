# -*- coding: utf-8 -*-
"""Repair X(X) double-wrap damage: identical-content brackets -> unwrap."""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool"
BAD = re.compile(r"^([^（(]+)[（(]\1[)）]$")


def save_json(f, d):
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    os.replace(tmp, f)


def main():
    fixed = 0
    files = 0
    for f in glob.glob(os.path.join(BASE, "output", "[a-z][a-z]", "20*", "persons", "*.json")):
        if os.path.basename(f) == "_index.json":
            continue
        d = json.load(open(f, encoding="utf-8"))
        changed = False
        for arr, key in [("person_relationships", "person_name"),
                         ("family_members", "name"),
                         ("work_experience", "organization"),
                         ("education", "institution")]:
            for it in d.get(arr) or []:
                if not isinstance(it, dict):
                    continue
                v = it.get(key) or ""
                if BAD.match(v):
                    it[key] = BAD.match(v).group(1)
                    fixed += 1
                    changed = True
        if changed:
            files += 1
            save_json(f, d)
    print(f"unwrapped: {fixed} fields in {files} files")


if __name__ == "__main__":
    main()

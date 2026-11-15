# -*- coding: utf-8 -*-
"""Fix double-wrapped org/institution names: X(X (Latin)) -> X(Latin). Then stats."""
import glob
import json
import os
import re
import sys

sys.path.insert(0, ".agents/skills/country-org-collector/scripts")
from atomic_write import load_json, save_json  # noqa: E402

BASE = "output/gn/2026-11-10"
# value like: PREFIX(PREFIX (LATIN))  -- outer prefix identical to inner prefix
PAT = re.compile(r"^(.+?)\((.+?) \((.+?)\)\)$")

fixed = []
for f in sorted(glob.glob(f"{BASE}/persons/GN-*.json")):
    pid = os.path.basename(f)[:-5]
    d = load_json(f)
    changed = False
    for it in (d.get("work_experience") or []):
        v = it.get("organization")
        if v:
            m = PAT.match(str(v))
            if m and m.group(1) == m.group(2):
                it["organization"] = f"{m.group(1)}({m.group(3)})"
                fixed.append(f"{pid} work: {v} -> {it['organization']}")
                changed = True
    for it in (d.get("education") or []):
        v = it.get("institution")
        if v:
            m = PAT.match(str(v))
            if m and m.group(1) == m.group(2):
                it["institution"] = f"{m.group(1)}({m.group(3)})"
                fixed.append(f"{pid} edu: {v} -> {it['institution']}")
                changed = True
    if changed:
        save_json(f, d)

print(f"fixed {len(fixed)} values")
for x in fixed:
    print("  ", x)

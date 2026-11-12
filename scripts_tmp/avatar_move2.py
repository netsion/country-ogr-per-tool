# -*- coding: utf-8 -*-
"""Cleanup pass 2:
  1. person avatars sitting OUTSIDE any photos dir (dataset root, persons/ root,
     images/, profiles/...) -> move into persons/photos/<ID>.<ext>, rewrite ref
  2. local_path pointing at .json files (KG) -> null out
Only touches persons/*.json. Collision-safe.
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool/output"
PERSON_STEM_I = re.compile(r"^[A-Z]{2}-PERSON-\d+$", re.I)


def norm_person_name(fn):
    stem, ext = os.path.splitext(fn)
    return stem.upper() + ext.lower() if PERSON_STEM_I.match(stem) else fn


def resolve_local(ds_root, lp):
    if not isinstance(lp, str) or not lp.strip():
        return None
    lp = lp.replace("\\", "/")
    if re.match(r"^[A-Za-z]:/", lp):
        return os.path.normpath(lp)
    m = re.match(r"^output/([a-z]{2}/\d{4}-\d{2}-\d{2})/(.*)$", lp, re.I)
    if m:
        return os.path.normpath(os.path.join(BASE, m.group(1), m.group(2)))
    return os.path.normpath(os.path.join(ds_root, lp))


def save(f, data):
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    os.replace(tmp, f)


moved, nullled, conflicts = 0, 0, []
for ds in sorted(glob.glob(os.path.join(BASE, "[a-z][a-z]", "20*"))):
    ds_root = os.path.normpath(ds)
    pdir = os.path.join(ds_root, "persons", "photos")
    for f in sorted(glob.glob(os.path.join(ds_root, "persons", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        p = d.get("profile")
        if not isinstance(p, dict):
            continue
        lp = p.get("local_path")
        if not lp:
            continue
        full = resolve_local(ds_root, lp)
        if full and full.lower().endswith(".json"):
            p["local_path"] = None
            save(f, d)
            nullled += 1
            continue
        if not full or not os.path.isfile(full):
            continue
        rel = os.path.relpath(full, ds_root).replace("\\", "/")
        if rel.startswith("persons/photos/"):
            continue
        dest = os.path.join(pdir, norm_person_name(os.path.basename(full)))
        if os.path.normcase(dest) == os.path.normcase(full):
            continue
        if os.path.exists(dest):
            if open(full, "rb").read() == open(dest, "rb").read():
                os.remove(full)
            else:
                conflicts.append(os.path.relpath(full, BASE) + " -> " +
                                 os.path.relpath(dest, BASE))
                continue
        os.makedirs(pdir, exist_ok=True)
        os.replace(full, dest)
        p["local_path"] = "persons/photos/" + os.path.basename(dest)
        save(f, d)
        moved += 1

print("pass2 moved:", moved, "| json-refs nulled:", nullled, "| conflicts:", len(conflicts))
for c in conflicts[:10]:
    print("  ", c)

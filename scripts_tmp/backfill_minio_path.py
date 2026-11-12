# -*- coding: utf-8 -*-
"""Backfill profile.minio_path for all profiles with existing local images.

Rules (confirmed by user 2026-11-12):
  - persons: minio_path = "popular-person-profile/<ID>.<ext>"   (no leading slash)
  - orgs:    minio_path = "popular-org-profile/<ID>.<ext>"     (no leading slash)
  - only when profile.local_path exists AND file exists on disk
  - idempotent: skip if minio_path already equals target
Usage: python backfill_minio_path.py [--dry]
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool/output"
DRY = "--dry" in sys.argv


def save_json(f, data):
    tmp = f + ".tmp"
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)
    os.replace(tmp, f)


def main():
    persons = orgs = skipped = missing = 0
    for ds in sorted(glob.glob(os.path.join(BASE, "[a-z][a-z]", "20*"))):
        for kind, prefix in (("persons", "popular-person-profile"),
                             ("orgs", "popular-org-profile")):
            for f in sorted(glob.glob(os.path.join(ds, kind, "*.json"))):
                try:
                    d = json.load(open(f, encoding="utf-8"))
                except Exception:
                    continue
                p = d.get("profile")
                if not isinstance(p, dict):
                    continue
                lp = p.get("local_path")
                if not lp:
                    continue
                full = os.path.join(ds, lp.replace("/", os.sep))
                if not os.path.isfile(full):
                    missing += 1
                    continue
                fname = os.path.basename(lp.replace("\\", "/"))
                target = f"{prefix}/{fname}"
                if p.get("minio_path") == target:
                    skipped += 1
                    continue
                if not DRY:
                    p["minio_path"] = target
                    save_json(f, d)
                if kind == "persons":
                    persons += 1
                else:
                    orgs += 1
    print(("DRY-RUN" if DRY else "APPLIED") +
          f": persons={persons} orgs={orgs} "
          f"already-ok={skipped} local-file-missing={missing}")


if __name__ == "__main__":
    main()

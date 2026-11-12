# -*- coding: utf-8 -*-
"""Migrate all local avatar images into minio-store/ (MinIO mirror layout).

Layout (confirmed 2026-11-12):
  minio-store/default/popular-person-profile/{cc}/<PERSON-ID>.<ext>   (persons)
  minio-store/default/popular-org-profile/{cc}/<ORG-ID>.<ext>        (orgs)

Writes per profile:
  local_path = "minio-store/default/<folder>/<cc>/<ID>.<ext>"   (relative to PROJECT ROOT)
  minio_path = "default/<folder>/<cc>/<ID>.<ext>"               (object key, no leading slash)

Old photo files are MOVED (source removed). Empty legacy photo dirs removed with --clean.
Idempotent: profiles already pointing into minio-store with existing file are only
ensured to have the right minio_path.
Usage: python migrate_to_minio_store.py [--dry] [--clean]
"""
import glob
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool/output"          # .../output
ROOT = os.path.dirname(BASE)                              # project root
STORE = os.path.join(ROOT, "minio-store")
DRY = "--dry" in sys.argv
CLEAN = "--clean" in sys.argv


def save_json(f, data):
    tmp = f + ".tmp"
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)
    os.replace(tmp, f)


def main():
    moved = already = conflict = missing = 0
    emptied_dirs = []
    for ds in sorted(glob.glob(os.path.join(BASE, "[a-z][a-z]", "20*"))):
        cc = os.path.basename(os.path.dirname(ds))
        touched_dirs = set()
        for kind, folder in (("persons", "popular-person-profile"),
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
                lp_norm = lp.replace("\\", "/")
                eid = os.path.splitext(os.path.basename(f))[0]
                fname = os.path.basename(lp_norm)
                mkey = f"default/{folder}/{cc}/{fname}"
                mlp = f"minio-store/{mkey}"
                src = os.path.join(ds, lp_norm.replace("/", os.sep))
                dst = os.path.join(STORE, mkey.replace("/", os.sep))

                if lp_norm.startswith("minio-store/"):
                    # already migrated
                    if os.path.isfile(os.path.join(ROOT, lp_norm.replace("/", os.sep))) \
                            and p.get("minio_path") == mkey:
                        already += 1
                    else:
                        p["minio_path"] = mkey
                        if not DRY:
                            save_json(f, d)
                        already += 1
                    continue

                if not os.path.isfile(src):
                    missing += 1
                    continue
                if os.path.isfile(dst):
                    if open(src, "rb").read() == open(dst, "rb").read():
                        os.remove(src)  # duplicate content already in store
                    else:
                        conflict += 1
                        print(f"CONFLICT: {src} vs {dst}")
                        continue
                else:
                    if not DRY:
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.move(src, dst)
                    moved += 1
                    touched_dirs.add(os.path.dirname(src))
                if not DRY:
                    p["local_path"] = mlp
                    p["minio_path"] = mkey
                    save_json(f, d)

        # remove now-empty legacy photo dirs
        if CLEAN and not DRY:
            for dd in (os.path.join(ds, "persons", "photos"), os.path.join(ds, "photos")):
                if os.path.isdir(dd) and not os.listdir(dd):
                    os.rmdir(dd)
                    emptied_dirs.append(os.path.relpath(dd, ROOT))

    print(("DRY-RUN" if DRY else "APPLIED") +
          f": moved={moved} already={already} conflict={conflict} missing={missing}")
    if emptied_dirs:
        print(f"removed {len(emptied_dirs)} empty legacy dirs")


if __name__ == "__main__":
    main()

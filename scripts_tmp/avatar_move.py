# -*- coding: utf-8 -*-
"""Move person avatars to <country>/<date>/persons/photos/ and rewrite local_path.

Rules:
  - files referenced by a person  -> persons/photos/<name>, local_path normalized
  - files referenced by an org    -> stay in (or move to) root photos/
  - orphan files with XX-PERSON-NNN stem -> persons/photos/
  - orphan files with org-id stem / unknown stem -> stay in place (reported)
  - collisions (dest exists, content differs) -> skip + report
  - 'local:photos/...' pseudo-scheme in source_url (MA) -> normalized to local_path
Usage: python avatar_move.py [--apply]
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = "D:/ai-workspace/apec-osint-tool/output"
DRY = "--apply" not in sys.argv

PERSON_STEM = re.compile(r"^([A-Z]{2})-PERSON-\d+$")
PERSON_STEM_I = re.compile(r"^[A-Z]{2}-PERSON-\d+$", re.I)
ORG_STEM = re.compile(r"^[A-Z]{2}-(GOV|CORP|ACAD|MEDIA|NGO|PARTY|BANK|ORG|SOE|THINK|INTL)-\d+$")


def norm_person_name(filename):
    """bo-person-000075.jpg -> BO-PERSON-000075.jpg (id uppercase, ext lowercase)."""
    stem, ext = os.path.splitext(filename)
    if PERSON_STEM_I.match(stem):
        return stem.upper() + ext.lower()
    return filename


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


def load(f):
    with open(f, encoding="utf-8") as fh:
        return json.load(fh)


def save(f, data):
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    os.replace(tmp, f)


def main():
    stats = {"moved": 0, "refs_rewritten": 0, "collisions": [], "skipped_unknown": [],
             "local_scheme_fixed": 0, "org_to_root": 0}
    datasets = sorted(glob.glob(os.path.join(BASE, "[a-z][a-z]", "20*")))
    for ds in datasets:
        ds_root = os.path.normpath(ds)
        pdir = os.path.join(ds_root, "persons", "photos")
        rdir = os.path.join(ds_root, "photos")

        # --- collect references ---
        person_files = sorted(glob.glob(os.path.join(ds_root, "persons", "*.json")))
        org_files = sorted(glob.glob(os.path.join(ds_root, "orgs", "*.json")))
        person_refs = {}   # abs file -> [person json files]
        org_refs = {}
        ma_fix = set()    # person json files carrying 'local:' scheme in source_url
        for f in person_files:
            d = load(f)
            p = d.get("profile")
            if not isinstance(p, dict):
                continue
            su, lp = p.get("source_url"), p.get("local_path")
            if isinstance(su, str) and su.strip().lower().startswith("local:"):
                ma_fix.add(f)
            if lp:
                full = resolve_local(ds_root, lp)
                if full and os.path.isfile(full):
                    person_refs.setdefault(os.path.normcase(full), []).append(f)
        for f in org_files:
            d = load(f)
            p = d.get("profile")
            if isinstance(p, dict) and p.get("local_path"):
                full = resolve_local(ds_root, p["local_path"])
                if full and os.path.isfile(full):
                    org_refs.setdefault(os.path.normcase(full), []).append(f)

        # --- plan moves over all photo files ---
        moves = {}  # src abs -> dest abs
        for photos_dir in (rdir, os.path.join(ds_root, "persons", "photos"),
                           os.path.join(ds_root, "orgs", "photos")):
            for pf in glob.glob(os.path.join(photos_dir, "*")):
                if not os.path.isfile(pf):
                    continue
                key = os.path.normcase(os.path.normpath(pf))
                stem = os.path.splitext(os.path.basename(pf))[0]
                if key in person_refs:
                    dest = os.path.join(pdir, norm_person_name(os.path.basename(pf)))
                elif key in org_refs:
                    dest = os.path.join(rdir, os.path.basename(pf))
                elif PERSON_STEM_I.match(stem):
                    dest = os.path.join(pdir, norm_person_name(os.path.basename(pf)))
                elif ORG_STEM.match(stem):
                    dest = os.path.join(rdir, os.path.basename(pf)) \
                        if photos_dir != rdir else pf
                else:
                    stats["skipped_unknown"].append(
                        os.path.relpath(pf, BASE).replace("\\", "/"))
                    continue
                dest = os.path.normpath(dest)
                if dest != os.path.normpath(pf):
                    moves[key] = dest

        # --- apply moves ---
        executed = {}  # src stem (upper) -> final basename at destination
        for key, dest in moves.items():
            if os.path.normcase(key) == os.path.normcase(dest):
                # case-only rename (same file on case-insensitive FS) — just rename
                if not DRY:
                    os.replace(key, dest)
                stats["moved"] += 1
                executed[os.path.splitext(os.path.basename(key))[0].upper()] = \
                    os.path.basename(dest)
                continue
            if os.path.exists(dest):
                a = open(key, "rb").read()
                b = open(dest, "rb").read()
                if a == b:
                    if not DRY:
                        os.remove(key)
                    stats["collisions"].append(
                        "dup-removed: " + os.path.relpath(key, BASE))
                    executed[os.path.splitext(os.path.basename(key))[0].upper()] = \
                        os.path.basename(dest)
                    continue
                stats["collisions"].append(
                    "CONFLICT kept both: " + os.path.relpath(key, BASE) +
                    " vs " + os.path.relpath(dest, BASE))
                continue
            if not DRY:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                os.replace(key, dest)
            stats["moved"] += 1
            executed[os.path.splitext(os.path.basename(key))[0].upper()] = \
                os.path.basename(dest)

        # --- rewrite person local_path refs to final location ---
        if not DRY:
            final_names = executed
            for f in person_files:
                d = load(f)
                p = d.get("profile")
                if not isinstance(p, dict):
                    continue
                lp = p.get("local_path")
                changed = False
                if lp:
                    full = resolve_local(ds_root, lp)
                    if full:
                        base_no_ext = os.path.splitext(os.path.basename(full))[0]
                        cand = final_names.get(base_no_ext.upper())
                        cur = os.path.normpath(full)
                        if cand:  # file was moved
                            new_rel = f"persons/photos/{cand}"
                        elif os.path.isfile(cur) and PERSON_STEM_I.match(base_no_ext):
                            new_rel = "persons/photos/" + norm_person_name(os.path.basename(cur))
                        else:
                            new_rel = None
                        if new_rel and lp.replace("\\", "/") != new_rel:
                            p["local_path"] = new_rel
                            changed = True
                if f in ma_fix and p.get("local_path"):
                    p["source_url"] = None
                    changed = True
                    stats["local_scheme_fixed"] += 1
                if changed:
                    save(f, d)
                    stats["refs_rewritten"] += 1

    print(("APPLIED" if not DRY else "DRY-RUN") + ":", stats["moved"], "moves;",
          stats["refs_rewritten"], "refs rewritten;", stats["local_scheme_fixed"],
          "local: scheme fixed")
    print("collisions:", len(stats["collisions"]))
    for c in stats["collisions"][:10]:
        print("  ", c)
    print("skipped unknown-stem files:", len(stats["skipped_unknown"]))
    for s in stats["skipped_unknown"][:15]:
        print("  ", s)


if __name__ == "__main__":
    main()

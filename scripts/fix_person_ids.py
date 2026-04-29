#!/usr/bin/env python3
"""
fix_person_ids.py — Reconcile person_id conflicts between profiles and registry
"""
import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
import json
import os
import glob

base_dir = r"D:\claude-workspace\apec-osint-tool\output\sg\2026-04-15"
profiles_dir = os.path.join(base_dir, "profiles")
registry_file = os.path.join(base_dir, "id_registry.json")

# Load registry
with open(registry_file, encoding="utf-8") as f:
    registry_data = json.load(f)
person_registry = registry_data["person_registry"]
person_counter = registry_data["person_counters"]["SG"]

# Build registry lookup
reg_by_id = {p["person_id"]: p for p in person_registry}

# Collect all (person_id, name, qid) from profile files
pid_to_names = {}  # person_id -> set of (name, qid)
for fpath in glob.glob(os.path.join(profiles_dir, "*.json")):
    if os.path.basename(fpath) == "_index.json":
        continue
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)
    for kp in data.get("key_people", []):
        pid = kp.get("person_id")
        if pid:
            name = kp["name"]
            desc = kp.get("description") or ""
            qid = None
            if pid not in pid_to_names:
                pid_to_names[pid] = []
            pid_to_names[pid].append((name, qid, fpath, data["org_id"]))

# Find conflicts and unregistered IDs
conflicts = []
unregistered = []
for pid, entries in sorted(pid_to_names.items()):
    names = set(e[0] for e in entries)
    if pid not in reg_by_id:
        unregistered.append((pid, names))
    elif len(names) > 1:
        # Same pid, different names - conflict!
        reg_name = reg_by_id[pid]["name"]
        if any(n != reg_name for n in names):
            conflicts.append((pid, names, reg_name))

print(f"Total person_ids in profiles: {len(pid_to_names)}")
print(f"In registry: {len(set(pid_to_names.keys()) & set(reg_by_id.keys()))}")
print(f"Unregistered: {len(unregistered)}")
print(f"Conflicts: {len(conflicts)}")

for pid, names in unregistered:
    print(f"  UNREG: {pid} -> {names}")
for pid, names, reg_name in conflicts:
    print(f"  CONFLICT: {pid} registry={reg_name}, profiles={names}")

# Fix: reassign unregistered IDs
if unregistered:
    print(f"\nFixing {len(unregistered)} unregistered person_ids...")
    # Map old pid -> new pid
    remap = {}
    for old_pid, names in unregistered:
        person_counter += 1
        new_pid = f"SG-PERSON-{person_counter:06d}"
        remap[old_pid] = new_pid
        name = list(names)[0]
        person_entry = {
            "person_id": new_pid,
            "name": name,
            "wikidata_qid": None,
            "status": "listed",
            "source_orgs": [],
        }
        person_registry.append(person_entry)
        reg_by_id[new_pid] = person_entry
        print(f"  {old_pid} -> {new_pid} ({name})")

    # Update profile files with remapped IDs
    for fpath in glob.glob(os.path.join(profiles_dir, "*.json")):
        if os.path.basename(fpath) == "_index.json":
            continue
        with open(fpath, encoding="utf-8") as f:
            data = json.load(f)
        changed = False
        for kp in data.get("key_people", []):
            old_pid = kp.get("person_id")
            if old_pid and old_pid in remap:
                kp["person_id"] = remap[old_pid]
                changed = True
        if changed:
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    # Save registry
    registry_data["person_registry"] = person_registry
    registry_data["person_counters"]["SG"] = person_counter
    with open(registry_file, "w", encoding="utf-8") as f:
        json.dump(registry_data, f, ensure_ascii=False, indent=2)
    print(f"Fixed. New counter: {person_counter}")
else:
    print("\nNo fixes needed.")

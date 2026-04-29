#!/usr/bin/env python3
"""
fix_conflicts.py — Resolve person_id conflicts from two overlapping runs
For each conflicting pid, registry version wins. First-run entries get new IDs.
"""
import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
import json
import os
import glob

base_dir = r"D:\claude-workspace\apec-osint-tool\output\sg\2026-04-15"
profiles_dir = os.path.join(base_dir, "profiles")
registry_file = os.path.join(base_dir, "id_registry.json")

with open(registry_file, encoding="utf-8") as f:
    registry_data = json.load(f)
person_registry = registry_data["person_registry"]
person_counter = registry_data["person_counters"]["SG"]

reg_by_id = {p["person_id"]: p for p in person_registry}

# Collect all (person_id, name) from profile files
pid_profile_map = {}  # pid -> [(name, fpath, org_id)]
for fpath in glob.glob(os.path.join(profiles_dir, "*.json")):
    if os.path.basename(fpath) == "_index.json":
        continue
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)
    for kp in data.get("key_people", []):
        pid = kp.get("person_id")
        if pid:
            if pid not in pid_profile_map:
                pid_profile_map[pid] = []
            pid_profile_map[pid].append((kp["name"], fpath, data["org_id"]))

# Find conflicts where profile name != registry name
remap = {}  # old_pid -> (new_pid, name)
for pid, entries in sorted(pid_profile_map.items()):
    if pid not in reg_by_id:
        continue  # already handled
    reg_name = reg_by_id[pid]["name"]
    for name, fpath, org_id in entries:
        if name != reg_name:
            # This profile entry needs a new person_id
            if pid not in remap:
                person_counter += 1
                new_pid = f"SG-PERSON-{person_counter:06d}"
                remap[pid] = {}
            # Track by name in case multiple entries share same wrong name
            if name not in remap[pid]:
                if not remap[pid]:
                    person_counter_adj = person_counter
                else:
                    person_counter += 1
                    person_counter_adj = person_counter
                new_pid = f"SG-PERSON-{person_counter_adj:06d}"
                remap[pid][name] = new_pid
                # Register new person
                person_entry = {
                    "person_id": new_pid,
                    "name": name,
                    "wikidata_qid": None,
                    "status": "listed",
                    "source_orgs": [org_id],
                }
                person_registry.append(person_entry)
                print(f"  CONFLICT FIX: {pid} '{name}' != reg '{reg_name}' -> {new_pid}")

# Apply remapping to profile files
changes = 0
for fpath in glob.glob(os.path.join(profiles_dir, "*.json")):
    if os.path.basename(fpath) == "_index.json":
        continue
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)
    changed = False
    for kp in data.get("key_people", []):
        pid = kp.get("person_id")
        name = kp.get("name")
        if pid and pid in remap and name in remap[pid]:
            kp["person_id"] = remap[pid][name]
            changed = True
            changes += 1
    if changed:
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# Save registry
registry_data["person_registry"] = person_registry
registry_data["person_counters"]["SG"] = person_counter
with open(registry_file, "w", encoding="utf-8") as f:
    json.dump(registry_data, f, ensure_ascii=False, indent=2)

print(f"\nFixed {changes} entries. New counter: {person_counter}")

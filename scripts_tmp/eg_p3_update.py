# -*- coding: utf-8 -*-
"""Reusable P3 progress updater. Usage:
python eg_p3_update.py --done id1,id2 --now id1,id2 --fail id1,id2 [--scripts]
"""
import json, sys, os, subprocess
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import load_json, save_json

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
prog = load_json(f"{BASE}/_phase_progress.json")

args = sys.argv[1:]
def get(flag):
    return args[args.index(flag)+1].split(",") if flag in args else []

done, now, fail = get("--done"), get("--now"), get("--fail")
for oid in done:
    if oid in prog["current"]: prog["current"].remove(oid)
    if oid in prog["remaining"]: prog["remaining"].remove(oid)
    if oid not in prog["completed"]: prog["completed"].append(oid)
for oid in fail:
    if oid in prog["current"]: prog["current"].remove(oid)
    if oid in prog["remaining"]: prog["remaining"].remove(oid)
    if oid not in prog["failed"]: prog["failed"].append(oid)
for oid in now:
    if oid in prog["remaining"]: prog["remaining"].remove(oid)
    if oid not in prog["current"]: prog["current"].append(oid)
prog["last_updated"] = "2026-11-17T01:00:00"
save_json(f"{BASE}/_phase_progress.json", prog)

for oid in done:
    d = load_json(f"{BASE}/orgs/{oid}.json")
    print(f"DONE {oid}: score={d['collection_meta']['completeness_score']} phase={d['collection_meta']['phase']}")

if "--scripts" in args:
    r = subprocess.run([sys.executable, ".agents/skills/country-org-collector/scripts/resolve_ids.py",
                        "output/eg/2026-11-16", "--allow-register", "--max-register", "30"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=r"D:\ai-workspace\apec-osint-tool",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONPATH": r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts"})
    tail = (r.stdout or "").strip().splitlines()[-4:]
    print("resolve_ids:", " | ".join(tail) if tail else (r.stderr or "")[-200:])
    r2 = subprocess.run([sys.executable, ".agents/skills/country-org-collector/scripts/generate_name_index.py",
                         "output/eg/2026-11-16"], capture_output=True, text=True,
                        cwd=r"D:\ai-workspace\apec-osint-tool",
                        env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONPATH": r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts"})
    tail2 = (r2.stdout or "").strip().splitlines()[-2:]
    print("name_index:", " | ".join(tail2) if tail2 else (r2.stderr or "")[-200:])

print(f"completed={len(prog['completed'])} current={prog['current']} failed={prog['failed']} remaining={len(prog['remaining'])}")
print("NEXT_4:", prog["remaining"][:4])

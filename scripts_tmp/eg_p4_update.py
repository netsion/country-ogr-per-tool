# -*- coding: utf-8 -*-
"""Reusable P4 progress updater. Usage: python eg_p4_update.py --done id1[,id2] --now id3[,id4] [--scripts]"""
import json, sys, os, subprocess
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import load_json, save_json
BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
prog = load_json(f"{BASE}/_phase_progress.json")
args = sys.argv[1:]
def get(flag): return args[args.index(flag)+1].split(",") if flag in args else []
done, now, fail = get("--done"), get("--now"), get("--fail")
for pid in done:
    if pid in prog["current"]: prog["current"].remove(pid)
    if pid in prog["remaining"]: prog["remaining"].remove(pid)
    if pid not in prog["completed"]: prog["completed"].append(pid)
for pid in fail:
    if pid in prog["current"]: prog["current"].remove(pid)
    if pid in prog["remaining"]: prog["remaining"].remove(pid)
    if pid not in prog["failed"]: prog["failed"].append(pid)
for pid in now:
    if pid in prog["remaining"]: prog["remaining"].remove(pid)
    if pid not in prog["current"]: prog["current"].append(pid)
prog["last_updated"] = "2026-11-17T12:30:00"
save_json(f"{BASE}/_phase_progress.json", prog)
for pid in done:
    try:
        d = load_json(f"{BASE}/persons/{pid}.json")
        print(f"DONE {pid}: score={d['collection_meta']['completeness_score']}")
    except Exception as e:
        print(f"DONE {pid}: file check failed {e}")
if "--scripts" in args:
    for script, args2 in [("resolve_ids.py", ["output/eg/2026-11-16", "--allow-register", "--max-register", "30"]),
                          ("generate_name_index.py", ["output/eg/2026-11-16"])]:
        r = subprocess.run([sys.executable, f".agents/skills/country-org-collector/scripts/{script}"] + args2,
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           cwd=r"D:\ai-workspace\apec-osint-tool",
                           env={**os.environ, "PYTHONIOENCODING": "utf-8",
                                "PYTHONPATH": r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts"})
        tail = (r.stdout or "").strip().splitlines()
        print(f"{script}:", tail[-2:] if tail else (r.stderr or "")[-150:])
print(f"completed={len(prog['completed'])} current={prog['current']} failed={prog['failed']} remaining={len(prog['remaining'])}")
print("NEXT:", prog["remaining"][:4])

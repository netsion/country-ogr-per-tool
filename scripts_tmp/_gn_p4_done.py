# -*- coding: utf-8 -*-
"""P4 completion handler (rebuilt per workspace-hygiene, lives in scripts_tmp/).
Validate person profile, update progress, emit next dispatch.

Usage: python scripts_tmp/_gn_p4_done.py GN-PERSON-000050 [more ids] [--next=N]
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, ".agents/skills/country-org-collector/scripts")
from atomic_write import load_json, save_json  # noqa: E402

BASE = "output/gn/2026-11-10"
VALIDATOR = ".agents/skills/country-org-collector/scripts/validate_schema.py"

args = [a for a in sys.argv[1:] if re.match(r"^GN-PERSON-\d{6}$", a)]
next_n = 1
for a in sys.argv[1:]:
    if a.startswith("--next"):
        next_n = int(a.split("=")[1]) if "=" in a else 1

progress = load_json(os.path.join(BASE, "_phase_progress.json"))
dispatch = load_json(os.path.join(BASE, "_p4_dispatch.json"))
by_id = {d["person_id"]: d for d in dispatch["order"]}

for pid in args:
    path = os.path.join(BASE, "persons", pid + ".json")
    status, detail = "completed", ""
    try:
        d = json.load(open(path, encoding="utf-8"))
        phase = (d.get("collection_meta") or {}).get("phase")
        score = (d.get("collection_meta") or {}).get("completeness_score")
        if d.get("person_id") != pid:
            status, detail = "failed", "person_id mismatch"
        elif phase != "phase4_person_profile":
            status, detail = "failed", f"phase={phase}"
        else:
            r2 = subprocess.run(
                [sys.executable, VALIDATOR, BASE, "--file", f"persons/{pid}.json"],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
            out = (r2.stdout or "") + (r2.stderr or "")
            errs = [l for l in out.splitlines() if l.strip().startswith("ERR")]
            if errs:
                status, detail = "failed", f"{len(errs)} errors: {errs[0][:90]}"
            elif isinstance(score, (int, float)) and score < 70:
                detail = f"WARN score={score}"
            else:
                detail = f"score={score}"
    except FileNotFoundError:
        status, detail = "failed", "file missing"
    except Exception as e:
        status, detail = "failed", repr(e)[:90]

    for lst in ("remaining", "current"):
        if pid in progress.get(lst, []):
            progress[lst].remove(pid)
    progress.setdefault(status, []).append(pid)
    print(f"RESULT {pid}: {status} ({detail})")

progress["last_updated"] = "2026-11-13T00:00:00"
save_json(os.path.join(BASE, "_phase_progress.json"), progress)

done = len(progress.get("completed", []))
fail = len(progress.get("failed", []))
print(f"PROGRESS completed={done}/{done + fail + len(progress['remaining']) + len(progress['current'])} failed={fail} in_flight={len(progress['current'])} remaining={len(progress['remaining'])}")

nxt = [p for p in progress.get("remaining", []) if p not in progress.get("current", [])][:next_n]
for pid in nxt:
    progress["current"].append(pid)
save_json(os.path.join(BASE, "_phase_progress.json"), progress)
for pid in nxt:
    p = by_id.get(pid, {})
    print("NEXT " + json.dumps({"person_id": pid, "name": p.get("name"), "importance": p.get("importance_level")}, ensure_ascii=False))

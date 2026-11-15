# -*- coding: utf-8 -*-
"""P4 enhancement-round completion handler.

Usage: python scripts_tmp/_gn_p4_enh_done.py GN-PERSON-0000xx [more ids] [--next=N]
Validates the person file after social/avatar enhancement, updates _p4_enhance.json
progress, prints RESULT/PROGRESS/NEXT lines for the orchestrator.
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
DISP = os.path.join(BASE, "_p4_enhance.json")

args = [a for a in sys.argv[1:] if re.match(r"^GN-PERSON-\d{6}$", a)]
next_n = 1
for a in sys.argv[1:]:
    if a.startswith("--next"):
        next_n = int(a.split("=")[1]) if "=" in a else 1

disp = load_json(DISP)
progress = disp["progress"]
by_id = {d["person_id"]: d for d in disp["order"]}

for pid in args:
    path = os.path.join(BASE, "persons", pid + ".json")
    base = by_id.get(pid, {})
    b_social = base.get("n_social") or 0
    b_weak_avatar = bool(base.get("weak_avatar"))
    status, detail = "completed", ""
    try:
        d = json.load(open(path, encoding="utf-8"))
        if d.get("person_id") != pid:
            status, detail = "failed", "person_id mismatch"
        else:
            r2 = subprocess.run(
                [sys.executable, VALIDATOR, BASE, "--file", f"persons/{pid}.json"],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
            out = (r2.stdout or "") + (r2.stderr or "")
            errs = [l for l in out.splitlines() if l.strip().startswith("ERR")]
            if errs:
                status, detail = "failed", f"{len(errs)} errors: {errs[0][:90]}"
            else:
                n_social = len(d.get("social_accounts") or [])
                prof = d.get("profile") or {}
                src = (prof.get("source_url") or "") if isinstance(prof, dict) else ""
                avatar_ok = bool(src) and ("lookaside" not in src)
                gained = n_social - b_social
                if n_social < b_social:
                    status, detail = "failed", f"social regression {b_social}->{n_social}"
                elif b_weak_avatar and not avatar_ok:
                    # no avatar yet: acceptable only if agent reported NONE-FOUND
                    status = "no_improvement"
                    detail = f"still no avatar (social {b_social}->{n_social})"
                elif gained > 0 or (b_weak_avatar and avatar_ok):
                    parts = []
                    if b_weak_avatar and avatar_ok:
                        parts.append("avatar set")
                    if gained > 0:
                        parts.append(f"social +{gained} (={n_social})")
                    detail = "; ".join(parts)
                else:
                    status = "no_improvement"
                    detail = "no changes detected"
    except FileNotFoundError:
        status, detail = "failed", "file missing"
    except Exception as e:
        status, detail = "failed", repr(e)[:90]

    for lst in ("remaining", "current"):
        if pid in progress.get(lst, []):
            progress[lst].remove(pid)
    progress.setdefault(status, []).append(pid)
    print(f"RESULT {pid}: {status} ({detail})")

progress["last_updated"] = "2026-11-14"
save_json(DISP, disp)

done = len(progress.get("completed", []))
ni = len(progress.get("no_improvement", []))
fail = len(progress.get("failed", []))
cur = len(progress.get("current", []))
rem = len(progress.get("remaining", []))
print(f"PROGRESS completed={done} no_improvement={ni} failed={fail} in_flight={cur} remaining={rem}")

nxt = [p for p in progress.get("remaining", []) if p not in progress.get("current", [])][:next_n]
for pid in nxt:
    progress["current"].append(pid)
save_json(DISP, disp)
for pid in nxt:
    p = by_id.get(pid, {})
    print("NEXT " + json.dumps({
        "person_id": pid, "name": p.get("name"), "name_zh": p.get("name_zh"),
        "tier": p.get("tier"), "n_social": p.get("n_social"), "weak_avatar": p.get("weak_avatar"),
    }, ensure_ascii=False))

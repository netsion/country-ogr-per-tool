import json, os

BASE = r"D:\ai-workspace\apec-osint-tool"
LIST = os.path.join(BASE, "scripts_tmp", "_backfill_avatar_a1.json")
PDIR = os.path.join(BASE, "output", "ng", "2026-11-10", "persons")

with open(LIST, encoding="utf-8") as f:
    pids = json.load(f)

for pid in pids:
    p = os.path.join(PDIR, pid + ".json")
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    print("=" * 70)
    print(pid, "|", d.get("name"), "| QID:", d.get("wikidata_qid"))
    for cp in (d.get("current_positions") or [])[:2]:
        print("  cur:", cp)
    print("  bio:", (d.get("biography_summary") or "")[:150])

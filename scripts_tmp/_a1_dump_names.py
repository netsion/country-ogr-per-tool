import json, os

BASE = r"D:\ai-workspace\apec-osint-tool"
LIST = os.path.join(BASE, "scripts_tmp", "_backfill_avatar_a1.json")
PDIR = os.path.join(BASE, "output", "ng", "2026-11-10", "persons")

with open(LIST, encoding="utf-8") as f:
    pids = json.load(f)

out = []
for pid in pids:
    p = os.path.join(PDIR, pid + ".json")
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    prof = d.get("profile", {})
    out.append({
        "pid": pid,
        "name": prof.get("name") or d.get("name"),
        "title": prof.get("title") or prof.get("role"),
        "org": prof.get("affiliation") or prof.get("organization"),
        "source_url": prof.get("source_url"),
        "keys": sorted(prof.keys()),
        "notes": d.get("collection_meta", {}).get("notes"),
    })

with open(os.path.join(BASE, "scripts_tmp", "_a1_names.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

for o in out:
    print(o["pid"], "|", o["name"], "|", o["title"], "|", o["org"], "| src:", o["source_url"])

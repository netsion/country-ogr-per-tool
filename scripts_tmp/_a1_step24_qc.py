import json, os

BASE = r"D:\ai-workspace\apec-osint-tool"
LIST = os.path.join(BASE, "scripts_tmp", "_backfill_avatar_a1.json")
PDIR = os.path.join(BASE, "output", "ng", "2026-11-10", "persons")

with open(LIST, encoding="utf-8") as f:
    pids = json.load(f)

ok, miss = [], []
for pid in pids:
    p = os.path.join(PDIR, pid + ".json")
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        miss.append((pid, "JSON ERROR: %s" % e))
        continue
    src = (d.get("profile") or {}).get("source_url")
    notes = (d.get("collection_meta") or {}).get("notes") or ""
    name = d.get("name")
    if src:
        ok.append((pid, name, src[:70]))
    else:
        has_note = "未找到可验证直链" in notes and "2026-11-15" in notes
        miss.append((pid, name, "note_present=%s" % has_note))

print("=== FILLED (%d) ===" % len(ok))
for pid, name, u in ok:
    print(pid, "|", name, "|", u)
print("=== MISSING (%d) ===" % len(miss))
for row in miss:
    print(row)

# spot check: verify a filled profile kept other key fields
d = json.load(open(os.path.join(PDIR, "NG-PERSON-000017.json"), encoding="utf-8"))
print("spot-check 000017 keys:", sorted(d.keys())[:8], "... work_experience:", len(d.get("work_experience", [])), "| social:", len(d.get("social_accounts", [])))

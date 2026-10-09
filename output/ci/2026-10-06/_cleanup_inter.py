import json
import os

BASE = "output/ci/2026-10-06"

# 1. Remove wrong QID (Q631 = Inter Milan FC) from target list entry for L'Inter
tpath = os.path.join(BASE, "_target_orgs.json")
with open(tpath, encoding="utf-8") as f:
    orgs = json.load(f)
for o in orgs:
    if o["id"] == "CI-MEDIA-006":
        removed = o.pop("qid", None)
        o["verification_status"] = "partial"
        print(f"1. target list: removed qid={removed} from CI-MEDIA-006")
with open(tpath, "w", encoding="utf-8") as f:
    json.dump(orgs, f, ensure_ascii=False, indent=2)

# 2. Delete wrong skeleton profile and wrong cache
for p in [os.path.join(BASE, "orgs", "CI-MEDIA-006.json"), os.path.join(BASE, "_cache", "Q631.json")]:
    if os.path.exists(p):
        os.remove(p)
        print(f"2. deleted: {p}")
    else:
        print(f"2. not found (ok): {p}")

# 3. Remove contaminated person registry entries
rpath = os.path.join(BASE, "id_registry.json")
with open(rpath, encoding="utf-8") as f:
    reg = json.load(f)
before = len(reg.get("person_registry", []))
reg["person_registry"] = [
    p for p in reg.get("person_registry", [])
    if "CI-MEDIA-006" not in (p.get("source_orgs") or [])
]
after = len(reg["person_registry"])
print(f"3. person_registry: {before} -> {after} (removed {before - after})")
with open(rpath, "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)

# verify reload
with open(tpath, encoding="utf-8") as f:
    json.load(f)
with open(rpath, encoding="utf-8") as f:
    json.load(f)
print("4. reload check OK (both files valid JSON)")

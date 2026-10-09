"""P4 prep: refresh stale person names from enriched orgs + re-rate importance per skill rules."""
import json
import glob
import re
from collections import Counter

BASE = "output/ci/2026-10-06"

# 1. build person_id -> (name, [titles]) from enriched org key_people
pid_name = {}
pid_titles = {}
for fp in glob.glob(f"{BASE}/orgs/*.json"):
    d = json.load(open(fp, encoding="utf-8"))
    if d.get("collection_meta", {}).get("phase") != "phase3_enriched":
        continue
    for kp in d.get("key_people", []) or []:
        pid = kp.get("person_id")
        if not pid:
            continue
        nm = (kp.get("name") or "").strip()
        if nm and not (nm.startswith("Q") and nm[1:].isdigit()):
            pid_name[pid] = nm
        if kp.get("title"):
            pid_titles.setdefault(pid, []).append(kp["title"])

# 2. refresh registry names
rpath = f"{BASE}/id_registry.json"
reg = json.load(open(rpath, encoding="utf-8"))
renamed = 0
for p in reg.get("person_registry", []):
    pid = p.get("person_id")
    if pid in pid_name and p.get("name") != pid_name[pid]:
        old = p.get("name")
        p["name"] = pid_name[pid]
        renamed += 1
        if old and old.startswith("Q"):
            print(f"  registry renamed (was QID): {pid} -> {pid_name[pid]}")
with open(rpath, "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)
print(f"registry names refreshed: {renamed}")

# 3. re-rate importance per skill §14.1 (max tier across titles)
HIGH = ["总统", "总理", "党魁", "总参谋长", "最高指挥官", "议长", "参议长",
        "院长", "大法官", "行长", "总司令", "Président de la République", "Premier ministre"]
MED = ["部长", "总经理", "总干事", "秘书长", "董事长", "台长", "社长", "主席",
       "总监", "副主任", "副部长", "部长级", "Ministre", "Directeur général",
       "Président", "Directeur", "Secrétaire général", "Maire"]


def rate(titles):
    blob = " ; ".join(titles)
    for kw in HIGH:
        if kw in blob:
            return "high"
    for kw in MED:
        if kw in blob:
            return "medium"
    return "low"


changed = {"high": 0, "medium": 0, "low": 0}
data = json.load(open(f"{BASE}/person_list.json", encoding="utf-8"))
for p in data["persons"]:
    pid = p.get("person_id")
    titles = list(pid_titles.get(pid, []))
    # include registry-side reason text as title evidence
    for so in p.get("source_orgs", []):
        if isinstance(so, dict) and so.get("position_title"):
            titles.append(so["position_title"])
    old = p.get("importance_level")
    new = rate(titles) if titles else (p.get("importance_level") or "low")
    p["importance_level"] = new
    p["importance_reason"] = " ; ".join(dict.fromkeys(titles))[:300] or p.get("importance_reason")
    changed[old] = changed.get(old, 0) + 1
# recount
cnt = Counter(p["importance_level"] for p in data["persons"])
data["summary"] = {"total": len(data["persons"]), "by_importance": dict(cnt)}
with open(f"{BASE}/person_list.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("re-rated:", dict(cnt))

# 4. remaining QID-named persons in list (no enriched org provides a name)
stale = [p["person_id"] for p in data["persons"] if re.match(r"^Q\d+$", p.get("name") or "")]
print("still QID-named (no enriched source):", stale)

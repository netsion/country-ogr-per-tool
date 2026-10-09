"""P4 OSINT-value trim for CORP/SOE/FIN/ACAD persons.

Keep (dispatch): current GM/CEO (总经理/总干事/总裁/PDG), board chairs (董事会主席),
founders (创始人), ministers (部长), group-level 董事总经理.
Trim (skip): functional directors (总监 with domain prefix), plain 董事, deputies
(副总/副行长/副校长), former/honorary (前/Ancien/honoraire/知名校友/荣誉), regional/
business-line heads, research unit heads, 秘书长 in corporate context.
"""
import json
import re
from collections import defaultdict

BASE = "output/ci/2026-10-06"
data = json.load(open(f"{BASE}/person_list.json", encoding="utf-8"))
reg = json.load(open(f"{BASE}/id_registry.json", encoding="utf-8"))
org_type = {r["org_id"]: r.get("org_type") for r in reg["registry"]}

TRIM_ONLY_TYPES = {"CORP", "SOE", "FIN", "ACAD"}

TRIM_PAT = re.compile(
    r"副总经理|副总干事|副总经理|副校长|副行长|副总裁|副社长|副总裁兼|"
    r"^董事$|董事（|董事\(|Administrateur de|Administrateur —|Administrateur Secrétaire|"
    r"前总干事|前总经理|前任总经理|Ancien|ancien|前校长|前负责人|honoraire|荣誉|知名校友|"
    r"总监|司长|组长|区域中心主任|业务部主任|部主任|部长（临时）|临时.*部长|"
    r"秘书长|负责人|Responsable|"
    r"Directeur (Commercial|des|du|de la|de l'|Filière|Financier|Juridique|Industriel|Technique|Régional|Logistique)"
)
KEEP_PAT = re.compile(
    r"总经理|总干事|总裁|首席执行官|PDG|董事总经理|董事会主席|董事长|创始人|"
    r"部长|校长|所长|Présidente? de l'université|Président de l'UVCI|Gouverneur|"
    r"Président$|Directeur Général$|Directeur général$|Directrice Générale$"
)


def best_titles(p):
    out = []
    for so in p.get("source_orgs", []):
        if isinstance(so, dict) and so.get("position_title"):
            out.append(so["position_title"])
    if p.get("importance_reason"):
        out.append(p["importance_reason"])
    return out


def decide(p, org_type):
    primary = (p.get("source_orgs") or [{}])[0]
    ptype = org_type.get(primary.get("org_id") if isinstance(primary, dict) else None)
    titles = best_titles(p)
    blob = " ; ".join(titles)
    # never trim high-importance persons
    if p.get("importance_level") == "high":
        return "dispatch", "high-importance"
    if ptype in TRIM_ONLY_TYPES or (ptype is None and ptype in TRIM_ONLY_TYPES):
        pass
    # person may relate to non-trim orgs too: if any source org outside the 4 types,
    # they stay (their value comes from GOV/PARTY/MEDIA etc.)
    all_types = {org_type.get(so.get("org_id")) for so in p.get("source_orgs", []) if isinstance(so, dict)}
    if not all_types or not all_types.issubset(TRIM_ONLY_TYPES):
        return "dispatch", "has source org outside CORP/SOE/FIN/ACAD"
    # within trim scope: keyword decision
    if KEEP_PAT.search(blob) and not re.search(r"前总干事|前总经理|前任总经理|Ancien Directeur", blob):
        # guard: 副总经理 contains 总经理 → require not starting with 副
        for t in titles:
            if KEEP_PAT.search(t) and not TRIM_PAT.search(t):
                return "dispatch", f"keep: {t[:40]}"
    for t in titles:
        if TRIM_PAT.search(t):
            return "skip", f"trim: {t[:40]}"
    # default: keep ambiguous (conservative)
    return "dispatch", "ambiguous default keep"


stats = defaultdict(lambda: defaultdict(int))
details = []
for p in data["persons"]:
    action, reason = decide(p, org_type)
    primary = (p.get("source_orgs") or [{}])[0]
    ptype = org_type.get(primary.get("org_id") if isinstance(primary, dict) else None)
    if ptype in TRIM_ONLY_TYPES or ptype is None:
        if ptype in TRIM_ONLY_TYPES or (ptype is None and action == "skip"):
            stats[ptype or "NONE"][action] += 1
            details.append({"person_id": p["person_id"], "name": p["name"], "org_type": ptype,
                            "importance": p["importance_level"], "action": action, "reason": reason})
    p["p4_action"] = action
    p["p4_action_reason"] = reason

with open(f"{BASE}/person_list.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("=== trim stats (CORP/SOE/FIN/ACAD only) ===")
for t in ["CORP", "SOE", "FIN", "ACAD", "NONE"]:
    if stats.get(t):
        print(f"  {t}: dispatch={stats[t]['dispatch']}, skip={stats[t]['skip']}")
n_dispatch = sum(1 for p in data["persons"] if p.get("p4_action") == "dispatch")
n_skip = sum(1 for p in data["persons"] if p.get("p4_action") == "skip")
print(f"OVERALL: dispatch={n_dispatch}, skip={n_skip}, total={n_dispatch + n_skip}")

with open(f"{BASE}/_p4_trim_corp_soe_fin_acad.json", "w", encoding="utf-8") as f:
    json.dump(details, f, ensure_ascii=False, indent=2)
print("details saved to _p4_trim_corp_soe_fin_acad.json")

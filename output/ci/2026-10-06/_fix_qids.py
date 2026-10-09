import json

QID_FIXES = {
    # id -> verified QID (via wbsearchentities, checked labels/descriptions)
    "Q620942": None,  # placeholder, real mapping below
}

FIXES = {
    # match by substring of name (ASCII-safe tokens) -> QID
    "BCEAO": "Q620942",      # Central Bank of West African States
    "CEDEAO": "Q193272",     # Economic Community of West African States
    "UEMOA": "Q1929699",     # West African Economic and Monetary Union
    "UA)": "Q7159",          # Union Africaine (UA)
    "(OCI)": "Q47543",       # Organisation of Islamic Cooperation
}

PATH = "output/ci/2026-10-06/_target_orgs.json"

with open(PATH, encoding="utf-8") as f:
    orgs = json.load(f)

fixed = []
for o in orgs:
    if o.get("qid"):
        continue
    name = o.get("name", "") or ""
    for token, qid in FIXES.items():
        if token in name:
            o["qid"] = qid
            fixed.append((o.get("id"), qid))
            break

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(orgs, f, ensure_ascii=False, indent=2)

# verify
with open(PATH, encoding="utf-8") as f:
    check = json.load(f)
n_qid = sum(1 for o in check if o.get("qid"))
print(f"Fixed: {fixed}")
print(f"Reload OK, orgs={len(check)}, with qid={n_qid}")

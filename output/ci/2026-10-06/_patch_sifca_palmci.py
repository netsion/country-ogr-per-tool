import json

BASE = "output/ci/2026-10-06"

PATCH = {
    "CI-CORP-004": {
        "name_original": "Société immobilière et financière de la côte africaine",  # from wd fr label
        "name_en": "SIFCA",  # target list name
        "org_subtype": "conglomerate",
        "aliases": ["SIFCA"],
    },
    "CI-CORP-006": {
        "name_original": "Palmci",  # from wd fr label
        "name_en": "Palmci",
        "org_subtype": "private_company",
    },
}

for oid, patch in PATCH.items():
    p = f"{BASE}/orgs/{oid}.json"
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    for k, v in patch.items():
        if v is not None:
            d["basic_info"][k] = v
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(oid, "->", patch["org_subtype"], "|", d["basic_info"]["name_original"])

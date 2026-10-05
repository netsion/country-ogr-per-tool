# -*- coding: utf-8 -*-
"""P2 skeleton org_subtype normalization: free-text -> schema enum."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ORGS_DIR = os.path.join(BASE, "orgs")

# free-text subcategory -> valid enum (flat set, cross-group OK per validator)
GENERIC = {
    # GOV
    "Ministry": "ministry",
    "Statutory Board": "statutory_board",
    "Regulatory Agency": "regulatory_agency",
    "Legislature": "legislature",
    "Judiciary": "judiciary",
    "Independent Organ": "independent_organ",
    "Executive Branch": "cabinet",
    "Head of State": "head_of_state",
    "Sovereign Wealth Fund": "sovereign_wealth_fund",
    "Regional Development Finance": "gov_investment_vehicle",
    "Youth Organization": "gov_department",
    # SOE
    "State-owned Enterprise": "state_owned_enterprise",
    "Aviation": "state_owned_enterprise",
    # CORP generic (listing status overridden per-org below)
    "Conglomerate": "conglomerate",
    "Retail": "private_company",
    "Technology": "private_company",
    "Logistics": "private_company",
    "Food & Beverage": "private_company",
    "Telecommunications": "private_company",
    "Entertainment": "private_company",
    # NGO
    "Humanitarian": "humanitarian_org",
    "Charitable Foundation": "foundation",
    "Professional Association": "professional_association",
    "Sports Association": "professional_association",
    "Youth Organization (NGO)": "community_org",
    "Civil Society": "advocacy_group",
    # ACAD
    "University": "university",
    "Research Institute": "research_institute",
    "Applied Education": "polytechnic",
    # MEDIA
    "Newspaper": "newspaper",
    "News Agency": "news_agency",
    "Broadcasting": "broadcaster",
    # FIN
    "Central Bank": "regulatory_agency",
    "Commercial Bank": "commercial_bank",
    "Islamic Bank": "commercial_bank",
    "Specialized Bank": "commercial_bank",
    "Stock Exchange": "publicly_listed",
    "Investment Company": "asset_management",
    "Insurance": "insurance_company",
    # INTL
    "International Sports Organization": "regional_org",
    # PARTY
    "De Facto Political Bloc": "coalition",
    # MIL
    "Armed Forces": "armed_forces",
    "Military Branch": "armed_forces",
    "Paramilitary": "security_agency",
    "Military College": "military_academy",
}

# CORP listing-status per-org overrides (well-established public facts; P3 verifies)
BY_NAME = {
    "Zain Group": "publicly_listed",
    "Agility Logistics": "publicly_listed",
    "Kout Food Group": "publicly_listed",
    "Mezzan Holding": "publicly_listed",
    "Kuwait National Cinema Company": "publicly_listed",
    "The Kuwaiti Danish Dairy Company": "publicly_listed",
    "Ooredoo Kuwait": "publicly_listed",
    "Alshaya Group": "private_company",
    "Alghanim Industries": "private_company",
    "Fast Telecommunications": "private_company",
    "Sakhr Software Company": "private_company",
    "National Aviation Services": "subsidiary",
    "United Networks": "subsidiary",
}

fixed, unmatched = 0, {}
for fn in sorted(os.listdir(ORGS_DIR)):
    if not fn.endswith(".json") or fn.startswith("_"):
        continue
    path = os.path.join(ORGS_DIR, fn)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    bi = data.get("basic_info", {})
    cur = bi.get("org_subtype")
    name_en = bi.get("name_en") or data.get("name_en") or ""
    new = BY_NAME.get(name_en) or GENERIC.get(cur)
    if new and new != cur:
        bi["org_subtype"] = new
        data["basic_info"] = bi
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        fixed += 1
    elif not new:
        unmatched.setdefault(cur, []).append(name_en or fn)

print(f"files fixed: {fixed}")
if unmatched:
    print("UNMATCHED (need manual map):")
    for k, v in unmatched.items():
        print(f"  {k!r}: {v}")

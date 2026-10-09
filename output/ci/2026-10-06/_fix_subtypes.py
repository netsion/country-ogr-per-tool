import json
import glob

# Map invalid org_subtype -> valid enum value (per org_profile_schema $defs.org_subtype_enum)
SIMPLE_MAP = {
    # GOV
    "head_of_state_office": "head_of_state",
    "executive_branch": "cabinet",
    "constitutional_court": "judiciary",
    "independent_electoral_commission": "independent_organ",
    "audit_institution": "independent_organ",
    "civil_registry_agency": "statutory_board",
    "civil_protection_agency": "statutory_board",
    "road_infrastructure_agency": "statutory_board",
    "investment_promotion_agency": "statutory_board",
    "agricultural_regulator": "regulatory_agency",
    # SOE
    "oil_and_gas": "state_owned_enterprise",
    "mining": "state_owned_enterprise",
    "refining": "state_owned_enterprise",
    "aviation": "state_owned_enterprise",
    "port_authority": "state_owned_enterprise",
    "forestry": "state_owned_enterprise",
    "engineering_services": "state_owned_enterprise",
    "petroleum_logistics": "state_owned_enterprise",
    # CORP
    "telecommunications": "private_company",
    "agribusiness": "private_company",
    "consumer_goods": "private_company",
    "beverages": "private_company",
    "retail": "private_company",
    "dairy": "private_company",
    "insurance": "private_company",
    "energy_utility": "private_company",
    # FIN
    "stock_exchange": "asset_management",
    # INTL
    "regional_organization": "regional_org",
    "commodity_organization": "multilateral_org",
    "development_bank": "multilateral_org",
    "agricultural_research": "multilateral_org",
    "education_organization": "multilateral_org",
    "regional_central_bank": "multilateral_org",
    "international_organization": "multilateral_org",
    # MEDIA
    "television": "broadcaster",
    "public_broadcaster": "broadcaster",
    "news_website": "digital_media",
    "publishing_house": "publisher",
    # MIL
    "gendarmerie": "armed_forces",
    # NGO
    "human_rights": "advocacy_group",
    "womens_rights": "advocacy_group",
    "humanitarian": "humanitarian_org",
    "health": "humanitarian_org",
    "child_welfare": "charity",
    # ACAD
    "public_university": "university",
    "grande_ecole": "polytechnic",
}

changes = []
for fp in glob.glob("output/ci/2026-10-06/orgs/*.json"):
    with open(fp, encoding="utf-8") as f:
        d = json.load(f)
    bi = d.get("basic_info", {})
    st = bi.get("org_subtype")
    if st in SIMPLE_MAP:
        new = SIMPLE_MAP[st]
        bi["org_subtype"] = new
        changes.append((d["org_id"], st, new))
    elif st == "political_party":
        # RHDP is the ruling party (since 2017 gov, Ouattara coalition); rest opposition
        blob = json.dumps(bi, ensure_ascii=False)
        new = "ruling_party" if "RHDP" in blob else "opposition_party"
        bi["org_subtype"] = new
        changes.append((d["org_id"], st, new))
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Updated {len(changes)} files")
for c in sorted(changes):
    print(f"  {c[0]}: {c[1]} -> {c[2]}")

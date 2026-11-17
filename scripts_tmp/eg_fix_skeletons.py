# -*- coding: utf-8 -*-
"""Patch EG skeletons: org_subtype enum + social_accounts.source integer codes."""
import sys, glob, os, json
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from generate_profiles import normalize_org_subtype, PLATFORM_CODES
from atomic_write import save_json, load_json

ORGS_DIR = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16\orgs"

# EG-specific party refinements (name_en -> subtype); generic fallback = opposition_party
PARTY_FIX = {
    "Nation's Future Party": "ruling_party",
    "National Democratic Party": "ruling_party",      # dissolved, was ruling 1978-2011
    "Freedom and Justice Party": "ruling_party",      # dissolved, was ruling 2012-2013
}

n_sub = n_soc = n_files = 0
for path in glob.glob(os.path.join(ORGS_DIR, "*.json")):
    data = load_json(path)
    if not data:
        continue
    bi = data.get("basic_info", {})
    cat = bi.get("org_type", "GOV")
    cur = bi.get("org_subtype", "")
    new_sub = normalize_org_subtype(cat, cur)
    if cat == "PARTY" and cur in PARTY_FIX:
        new_sub = PARTY_FIX[cur]
    if new_sub != cur:
        bi["org_subtype"] = new_sub
        n_sub += 1
    for acc in data.get("social_accounts", []) or []:
        src = acc.get("source")
        if isinstance(src, str):
            acc["source"] = PLATFORM_CODES.get(acc.get("platform"))
            acc["source_note"] = src
            n_soc += 1
    save_json(path, data)
    n_files += 1

print(f"files={n_files} org_subtype_fixed={n_sub} social_source_fixed={n_soc}")

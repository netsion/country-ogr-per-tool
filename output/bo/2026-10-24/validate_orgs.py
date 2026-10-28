# -*- coding: utf-8 -*-
"""Validate _target_orgs.json against org_list_schema.json (structural + semantic checks)."""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = r"D:/claude-workspace/apec-osint-tool/.agents/skills/country-org-collector/org_list_schema.json"
OUT_PATH = os.path.join(BASE, "_target_orgs.json")

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema = json.load(f)
with open(OUT_PATH, "r", encoding="utf-8") as f:
    doc = json.load(f)

errors = []
org_entry_props = set(schema["$defs"]["org_entry"]["properties"].keys())

def check(cond, msg):
    if not cond:
        errors.append(msg)

# top-level
check(set(doc.keys()) == {"metadata", "organizations", "summary"}, f"top-level keys: {set(doc.keys())}")

md = doc["metadata"]
md_props = {"country", "country_iso", "country_qid", "collection_date", "phase", "categories_covered", "subcategories_covered", "depth", "total_organizations"}
check(set(md.keys()) <= md_props, f"metadata extra keys: {set(md.keys()) - md_props}")
for k in ["country", "country_iso", "country_qid", "collection_date", "phase", "categories_covered", "total_organizations"]:
    check(k in md, f"metadata missing {k}")
check(re.match(r"^[A-Z]{2}$", md["country_iso"]) is not None, "country_iso pattern")
check(re.match(r"^Q[0-9]+$", md["country_qid"]) is not None, "country_qid pattern")
check(md["phase"] == "phase1_broad_scan", "phase const")
check(md["total_organizations"] == len(doc["organizations"]), "total_organizations mismatch")
allowed_cats = {"GOV", "SOE", "CORP", "NGO", "ACAD", "MEDIA", "FIN", "INTL", "PARTY", "MIL"}
check(set(md["categories_covered"]) <= allowed_cats, "categories_covered enum")

ids = set()
cat_counts = {}
for o in doc["organizations"]:
    extra = set(o.keys()) - org_entry_props
    check(not extra, f"{o.get('id')} extra props {extra}")
    for k in ["id", "name", "category", "country"]:
        check(k in o, f"org missing {k}: {o}")
    check(re.match(r"^[A-Z]{2}-[A-Z]+-[0-9]{3}$", o["id"]) is not None, f"id pattern {o.get('id')}")
    check(o["id"] not in ids, f"duplicate id {o['id']}")
    ids.add(o["id"])
    check(o["category"] in allowed_cats, f"category enum {o.get('category')}")
    check(re.match(r"^[A-Z]{2}$", o["country"]) is not None, f"country {o.get('country')}")
    if o.get("wikidata_qid") is not None:
        check(re.match(r"^Q[0-9]+$", o["wikidata_qid"]) is not None, f"qid pattern {o.get('wikidata_qid')}")
    if o.get("founded"):
        check(re.match(r"^\d{4}-\d{2}-\d{2}$", o["founded"]) is not None, f"founded format {o.get('founded')} in {o['id']}")
    if o.get("website"):
        check(o["website"].startswith("http"), f"website format {o.get('website')} in {o['id']}")
    check(isinstance(o.get("sources", []), list) and len(o.get("sources", [])) >= 1, f"sources missing {o['id']}")
    for s in o.get("sources", []):
        check(set(s.keys()) == {"type", "url"}, f"source keys {o['id']}")
        check(s["type"] in {"wikipedia", "wikidata", "official_website", "web_search", "news_search", "government_registry", "opencorporates", "other"}, f"source type {o['id']} {s.get('type')}")
        check(s["url"].startswith("http"), f"source url {o['id']}")
    check(o.get("verification_status") in {"verified", "unverified", "partial", "source_blocked_cloudflare", "source_unavailable"}, f"verification_status {o['id']}")
    for p in o.get("key_people", []):
        check("title" in p and "name" in p, f"key_people structure {o['id']}")
        check(p.get("since") is None or isinstance(p.get("since"), str), f"key_people since {o['id']}")
    for r in o.get("relationships", []):
        check("type" in r and "target_name" in r, f"relationship structure {o['id']}")
    cat_counts[o["category"]] = cat_counts.get(o["category"], 0) + 1
    if "aliases" in o:
        check(all(isinstance(a, str) for a in o["aliases"]), f"aliases types {o['id']}")

# summary vs actual
summ = doc["summary"]
check(set(summ.keys()) == {"by_category", "data_quality"}, f"summary keys {set(summ.keys())}")
for c, info in summ["by_category"].items():
    check(info["count"] == cat_counts.get(c, 0), f"summary count mismatch {c}: {info['count']} vs {cat_counts.get(c, 0)}")
    check(isinstance(info["top_orgs"], list) and len(info["top_orgs"]) > 0, f"top_orgs {c}")
dq = summ["data_quality"]
n_qid = sum(1 for o in doc["organizations"] if o.get("wikidata_qid"))
check(dq["verified_count"] == n_qid, f"verified_count {dq['verified_count']} vs {n_qid}")
check(dq["unverified_count"] == len(doc["organizations"]) - n_qid, "unverified_count mismatch")
check(0 <= dq["completeness_pct"] <= 100, "completeness_pct range")

if errors:
    print(f"VALIDATION FAILED: {len(errors)} errors")
    for e in errors[:40]:
        print(" -", e)
else:
    print("VALIDATION PASSED")
print(f"orgs={len(doc['organizations'])}, cats={cat_counts}, with_qid={n_qid}")

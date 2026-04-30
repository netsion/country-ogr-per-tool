#!/usr/bin/env python3
"""
generate_profiles.py — Generate skeleton org profiles from cached data + resolve key_people QIDs
Usage: python generate_profiles.py output/kr/2026-04-28
Pipeline: Phase 2 step — outputs skeleton profiles (completeness 30-55) with resolved key_people
"""

import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')

import json
import os
import time
import glob
import urllib.request
import re
from datetime import date

# Ensure sibling scripts are importable (for validate_schema)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from atomic_write import normalize_name, save_json, load_json, setup_proxy

# --- Constants ---
CACHE_DIR = "_cache"
ORGS_DIR = "orgs"
TODAY = str(date.today())

# Wikidata property mappings
SOCIAL_PROPS = {
    "P2002": ("twitter_x", "https://twitter.com/"),
    "P2013": ("facebook", "https://facebook.com/"),
    "P2397": ("youtube", "https://youtube.com/channel/"),
    "P2387": ("instagram", "https://instagram.com/"),
    "P2392": ("linkedin", "https://linkedin.com/company/"),
    "P3813": ("telegram", "https://t.me/"),
    "P4263": ("weibo", "https://weibo.com/"),
    "P2572": ("other", None),
}

LEADER_PROPS = [
    ("P6", "Head"),
    ("P169", "Chief Executive Officer"),
    ("P488", "Chair"),
    ("P1037", "Director"),
    ("P1308", "Officeholder"),
]

INDUSTRY_MAP = {
    "Q861516": "banking", "Q845706": "commercial_bank", "Q993393": "investment_bank",
    "Q1140301": "financial_services", "Q4830453": "information_technology",
    "Q879589": "telecommunications", "Q131681": "internet_services",
    "Q44532": "aviation", "Q3918": "higher_education", "Q8064": "healthcare",
    "Q42534": "logistics_warehousing", "Q39338": "transportation",
    "Q131289": "defence_military", "Q485259": "real_estate",
    "Q862410": "media_publishing", "Q338142": "broadcasting",
    "Q8674": "hospitality_tourism", "Q4742180": "asset_management",
    "Q1142467": "investment", "Q845691": "insurance",
    "Q894516": "pharmaceuticals", "Q183962": "semiconductors",
    "Q7397": "software", "Q162630": "asset_management",
}

ISO2_TO_ISO3 = {
    "SG": "SGP", "MY": "MYS", "AU": "AUS", "BN": "BRN", "CA": "CAN",
    "CL": "CHL", "CN": "CHN", "HK": "HKG", "ID": "IDN", "JP": "JPN",
    "KR": "KOR", "MX": "MEX", "NZ": "NZL", "PG": "PNG", "PE": "PER",
    "PH": "PHL", "RU": "RUS", "TH": "THA", "TW": "TWN", "US": "USA",
    "VN": "VNM",
}


# --- Wikidata helpers ---

def get_wd_value(entity, prop):
    claims = entity.get("claims", {}).get(prop, [])
    if not claims:
        return None
    snak = claims[0].get("mainsnak", {})
    if snak.get("snaktype") != "value":
        return None
    return snak.get("datavalue", {}).get("value")


def get_wd_qid_value(entity, prop):
    val = get_wd_value(entity, prop)
    if isinstance(val, dict) and "id" in val:
        return val["id"]
    return None


def get_wd_time_value(entity, prop):
    claims = entity.get("claims", {}).get(prop, [])
    if not claims:
        return None
    dates = []
    for claim in claims:
        snak = claim.get("mainsnak", {})
        if snak.get("snaktype") != "value":
            continue
        val = snak.get("datavalue", {}).get("value")
        if isinstance(val, dict) and "time" in val:
            t = val["time"].lstrip("+").split("T")[0]
            parts = t.split("-")
            if len(parts) == 3:
                y, m, d = parts
                if m == "00": m = "01"
                if d == "00": d = "01"
                dates.append(f"{y}-{m}-{d}")
    return min(dates) if dates else None


def get_wd_string_value(entity, prop):
    val = get_wd_value(entity, prop)
    return val if isinstance(val, str) else None


def get_wd_label(entity, lang="en"):
    return entity.get("labels", {}).get(lang, {}).get("value")


def get_wd_aliases(entity, lang="en"):
    return [a["value"] for a in entity.get("aliases", {}).get(lang, [])]


def _is_current_position(claim):
    quals = claim.get("qualifiers", {})
    end_time_quals = quals.get("P582", [])
    if end_time_quals:
        end_val = end_time_quals[0].get("datavalue", {}).get("value", {})
        if isinstance(end_val, dict) and "time" in end_val:
            end_str = end_val["time"].lstrip("+").split("T")[0]
            try:
                parts = end_str.split("-")
                end_dt = date(int(parts[0]), int(parts[1]), int(parts[2]))
                if end_dt < date.today():
                    return False
            except (ValueError, IndexError):
                pass
    return True


# --- Extract functions ---

def extract_social_accounts(entity):
    accounts = []
    for prop, (platform, base_url) in SOCIAL_PROPS.items():
        claims = entity.get("claims", {}).get(prop, [])
        for claim in claims[:1]:
            val = claim.get("mainsnak", {}).get("datavalue", {}).get("value")
            if isinstance(val, str):
                url = f"{base_url}{val}" if base_url else val
                accounts.append({
                    "platform": platform,
                    "account_name": val,
                    "url": url,
                    "source": "wikidata"
                })
    return accounts


def extract_key_people_qids(entity):
    """Extract key people QIDs from Wikidata leader properties."""
    people = []
    seen = set()
    for prop, default_title in LEADER_PROPS:
        claims = entity.get("claims", {}).get(prop, [])
        for claim in claims:
            qid = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
            if not qid or qid in seen:
                continue
            if not _is_current_position(claim):
                continue
            seen.add(qid)
            people.append({
                "person_id": None,
                "name": qid,
                "title": default_title,
                "title_description": None,
                "description": None,
            })
    return people


def extract_related_entities(entity, target_qids_map):
    related = []
    rel_props = [
        ("P749", "parent_org"), ("P355", "subsidiary"), ("P1365", "predecessor"),
        ("P1366", "successor"), ("P1269", "member_of"),
    ]
    for prop, rel_type in rel_props:
        claims = entity.get("claims", {}).get(prop, [])
        for claim in claims[:5]:
            qid = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
            if qid and qid in target_qids_map:
                info = target_qids_map[qid]
                related.append({
                    "org_id": info.get("org_id", qid),
                    "org_name": info.get("name_en") or info.get("name", ""),
                    "org_type": info.get("category"),
                    "org_description": None,
                    "relationship_type": rel_type
                })
    return related


def guess_industries(entity, category):
    industries = []
    claims = entity.get("claims", {}).get("P452", [])
    for claim in claims[:3]:
        qid = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
        if qid and qid in INDUSTRY_MAP:
            industries.append(INDUSTRY_MAP[qid])
    cat_defaults = {
        "GOV": ["public_administration"], "SOE": ["investment"],
        "CORP": ["financial_services"], "ACAD": ["higher_education"],
        "MEDIA": ["broadcasting"], "PARTY": ["public_administration"],
        "NGO": ["nonprofit"], "FIN": ["financial_services"],
        "INTL": ["international_trade"], "MIL": ["defence_military"],
    }
    if not industries and category in cat_defaults:
        industries = cat_defaults[category]
    return industries


def calc_completeness(profile):
    """Delegate to validate_schema.calc_org_score for consistency."""
    try:
        from validate_schema import calc_org_score
        return calc_org_score(profile)
    except ImportError:
        # Fallback if validate_schema not importable
        score = 30
        fields = [
            ("basic_info.founded_date", 5), ("basic_info.website", 5), ("basic_info.name_zh", 5),
            ("social_accounts", 10), ("key_people", 15), ("departments", 5),
            ("related_entities", 5), ("core_business", 10), ("industries", 5), ("profile", 5),
        ]
        for field, pts in fields:
            obj = profile
            for p in field.split("."):
                obj = obj.get(p) if isinstance(obj, dict) else None
            if obj and (not isinstance(obj, (list, str)) or len(obj) > 0):
                score += pts
        return min(score, 100)


# --- Key People Resolution (merged from resolve_key_people.py) ---

def fetch_wikidata_labels(qids):
    """Batch fetch labels for QIDs. Filters non-person entities."""
    results = {}
    for i in range(0, len(qids), 50):
        batch = qids[i:i+50]
        ids_str = "|".join(batch)
        url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={ids_str}&format=json&props=labels|claims"
        req = urllib.request.Request(url, headers={
            "User-Agent": "ApecOsintTool/1.0 (research; bot)",
            "Accept": "application/json",
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            for qid, entity in data.get("entities", {}).items():
                if "missing" in entity:
                    results[qid] = None
                    continue
                p31_values = []
                for p31_claim in entity.get("claims", {}).get("P31", []):
                    p31_val = p31_claim.get("mainsnak", {}).get("datavalue", {}).get("value", {})
                    if isinstance(p31_val, dict) and "id" in p31_val:
                        p31_values.append(p31_val["id"])
                is_human = "Q5" in p31_values if p31_values else True
                en_label = entity.get("labels", {}).get("en", {}).get("value")
                zh_label = entity.get("labels", {}).get("zh", {}).get("value")
                zhhans_label = entity.get("labels", {}).get("zh-hans", {}).get("value")
                if not is_human:
                    results[qid] = {"en": None, "zh": None, "is_person": False}
                    continue
                results[qid] = {
                    "en": en_label,
                    "zh": zh_label or zhhans_label,
                    "is_person": True,
                }
        except Exception as e:
            print(f"  ERROR fetching labels: {e}")
            for qid in batch:
                results[qid] = None
        time.sleep(2)
    return results


def resolve_key_people(orgs_dir, registry_data, cache_dir, country_iso):
    """Resolve QID placeholders and plain-text names in key_people to real names + person_ids."""
    person_registry = registry_data.get("person_registry", [])
    person_counter = registry_data.get("person_counters", {}).get(country_iso, 0)

    existing_by_name = {}
    existing_by_qid = {}
    for p in person_registry:
        existing_by_name[normalize_name(p.get("name") or p.get("name_en", ""))] = p
        if p.get("wikidata_qid"):
            existing_by_qid[p["wikidata_qid"]] = p

    # Collect QID placeholders and plain-text names
    qid_occurrences = {}
    plain_text_names = []

    for fpath in sorted(glob.glob(os.path.join(orgs_dir, "*.json"))):
        fname = os.path.basename(fpath)
        if fname.startswith("_"):
            continue
        data = load_json(fpath)
        for i, kp in enumerate(data.get("key_people", [])):
            name = kp.get("name", "")
            pid = kp.get("person_id")
            # QID placeholder: name starts with Q followed by digits
            if name.startswith("Q") and len(name) > 1 and name[1:].isdigit():
                qid = name
                if qid not in qid_occurrences:
                    qid_occurrences[qid] = []
                qid_occurrences[qid].append((fpath, i, data["org_id"]))
            # Plain text name without person_id
            elif not pid and name:
                plain_text_names.append((fpath, i, data["org_id"], name))

    # Resolve plain text names first
    new_persons = []
    for fpath, idx, org_id, name in plain_text_names:
        name_key = normalize_name(name)
        if name_key in existing_by_name:
            person_id = existing_by_name[name_key]["person_id"]
        else:
            person_counter += 1
            person_id = f"{country_iso}-PERSON-{person_counter:06d}"
            entry = {
                "person_id": person_id,
                "name": name,
                "wikidata_qid": None,
                "status": "listed",
                "source_orgs": [org_id],
            }
            person_registry.append(entry)
            existing_by_name[name_key] = entry
            new_persons.append(entry)
            print(f"  REGISTERED: {name} -> {person_id}")

        data = load_json(fpath)
        data["key_people"][idx]["person_id"] = person_id
        save_json(fpath, data)

    # Resolve QID placeholders
    if qid_occurrences:
        print(f"Resolving {len(qid_occurrences)} QID placeholders...")
        # Check cache and registry first
        qids_to_fetch = []
        label_cache = {}

        for qid in qid_occurrences:
            if qid in existing_by_qid:
                p = existing_by_qid[qid]
                en = p["name"].split("(")[-1].rstrip(")").strip() if "(" in p["name"] else p["name"]
                zh = p["name"].split("(")[0].strip() if "(" in p["name"] else None
                label_cache[qid] = {"en": en, "zh": zh, "existing_id": p["person_id"], "is_person": True}
                continue
            cache_file = os.path.join(cache_dir, f"{qid}.json")
            if os.path.exists(cache_file):
                try:
                    cdata = load_json(cache_file)
                    wd = cdata.get("wikidata", {})
                    if wd:
                        label_cache[qid] = {
                            "en": wd.get("labels", {}).get("en", {}).get("value"),
                            "zh": wd.get("labels", {}).get("zh", {}).get("value") or wd.get("labels", {}).get("zh-hans", {}).get("value"),
                            "is_person": True,
                        }
                    else:
                        qids_to_fetch.append(qid)
                except Exception:
                    qids_to_fetch.append(qid)
            else:
                qids_to_fetch.append(qid)

        if qids_to_fetch:
            print(f"  Fetching {len(qids_to_fetch)} QIDs from Wikidata...")
            fetched = fetch_wikidata_labels(qids_to_fetch)
            label_cache.update(fetched)

        resolved = 0
        for qid, occurrences in qid_occurrences.items():
            info = label_cache.get(qid)
            if not info or info.get("is_person") is False:
                print(f"  SKIP: {qid} - {'not a person' if info else 'no data'}")
                continue

            en_name = info.get("en")
            if not en_name:
                print(f"  FAIL: {qid} - no English label")
                continue

            zh_name = info.get("zh")
            display_name = f"{zh_name} ({en_name})" if zh_name else en_name

            person_id = info.get("existing_id")
            if not person_id:
                name_key = normalize_name(display_name)
                matched = existing_by_name.get(name_key)
                if matched:
                    person_id = matched["person_id"]
                else:
                    person_counter += 1
                    person_id = f"{country_iso}-PERSON-{person_counter:06d}"
                    entry = {
                        "person_id": person_id,
                        "name": display_name,
                        "wikidata_qid": qid,
                        "status": "listed",
                        "source_orgs": list(set(occ[2] for occ in occurrences)),
                    }
                    person_registry.append(entry)
                    existing_by_name[name_key] = entry
                    existing_by_qid[qid] = entry
                    new_persons.append(entry)

            for fpath, idx, org_id in occurrences:
                data = load_json(fpath)
                kp = data["key_people"][idx]
                kp["name"] = display_name
                kp["person_id"] = person_id
                kp["description"] = (kp.get("description") or "").replace(f"Wikidata: {qid}", "").strip() or None
                save_json(fpath, data)

            resolved += 1
            print(f"  OK: {qid} -> {display_name} ({person_id})")

        print(f"  Resolved: {resolved}, New persons: {len(new_persons)}")

    # Save registry
    registry_data["person_registry"] = person_registry
    registry_data["person_counters"][country_iso] = person_counter
    return registry_data


# --- Profile generation ---

def build_target_qids_map(targets, registry):
    qid_map = {}
    for org in targets:
        qid = org.get("qid") or org.get("wikidata_qid")
        if qid:
            for r in registry:
                if r.get("wikidata_qid") == qid:
                    org["org_id"] = r["org_id"]
                    break
            qid_map[qid] = org
    for r in registry:
        qid = r.get("wikidata_qid")
        if qid and qid not in qid_map:
            qid_map[qid] = {"name_en": r["name"], "org_id": r["org_id"], "category": r.get("org_type")}
    return qid_map


def generate_profile(org, cache_data, registry, target_qids_map, next_ids, country_iso, country_iso3):
    category = org["category"]
    wd = cache_data.get("wikidata")
    wp = cache_data.get("wikipedia")
    errors = cache_data.get("errors", [])

    # Determine org_id
    org_id = org.get("org_id")
    if not org_id:
        seq = next_ids.get(category, 0) + 1
        org_id = f"{country_iso}-{category}-{seq:03d}"
        next_ids[category] = seq
        org["org_id"] = org_id

    # Basic info
    name_en = get_wd_label(wd, "en") if wd else org.get("name_en") or org.get("name", "")
    name_zh = (get_wd_label(wd, "zh") or get_wd_label(wd, "zh-hans")) if wd else None
    name_zh = name_zh or org.get("name_zh")
    name_original = org.get("name_original") or name_en
    aliases = get_wd_aliases(wd, "en") if wd else []
    website = get_wd_string_value(wd, "P856") if wd else None
    founded = get_wd_time_value(wd, "P571") if wd else None

    # Profile image
    profile = None
    if wp and wp.get("thumbnail", {}).get("source"):
        profile = {"source_url": wp["thumbnail"]["source"], "local_path": None}

    # Social accounts from Wikidata
    social = extract_social_accounts(wd) if wd else []

    # Key people: prefer manually curated from _target_orgs.json, supplement with Wikidata
    target_kp = org.get("key_people", [])
    if target_kp:
        people = []
        for kp in target_kp:
            people.append({
                "person_id": None,
                "name": kp.get("name", ""),
                "title": kp.get("title", ""),
                "title_description": None,
                "description": None,
            })
    else:
        people = extract_key_people_qids(wd) if wd else []

    # Related entities
    related = extract_related_entities(wd, target_qids_map) if wd else []

    # Industries
    industries = guess_industries(wd, category) if wd else []

    # Data sources
    data_sources = []
    if wd: data_sources.append("wikidata")
    if wp: data_sources.append("wikipedia")
    if website: data_sources.append("official_website")
    if not data_sources: data_sources = ["web_search"]

    profile_data = {
        "org_id": org_id,
        "basic_info": {
            "name_original": name_original,
            "name_zh": name_zh,
            "name_en": name_en,
            "aliases": aliases[:5],
            "org_type": category,
            "org_subtype": org.get("org_subtype") or org.get("subcategory", ""),
            "country_iso3": country_iso3,
            "hq_country_iso3": country_iso3,
            "founded_date": founded,
            "website": website,
        },
        "social_accounts": social,
        "digital_assets": [],
        "key_people": people,
        "departments": [],
        "recent_events": [],
        "related_entities": related,
        "core_business": None,
        "industries": industries,
        "apec_stance": None,
        "profile": profile,
        "collection_meta": {
            "collection_date": TODAY,
            "phase": "phase2_skeleton",
            "data_sources": data_sources,
            "completeness_score": 0,
            "notes": "Skeleton profile from cached Wikidata + Wikipedia data" + (f"; errors: {errors}" if errors else "")
        }
    }

    profile_data["collection_meta"]["completeness_score"] = calc_completeness(profile_data)
    return profile_data


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <output_dir>")
        sys.exit(1)

    base_dir = sys.argv[1]
    dir_parts = base_dir.replace("\\", "/").rstrip("/").split("/")
    country_iso = dir_parts[-2].upper() if len(dir_parts) >= 2 else "XX"
    country_iso3 = ISO2_TO_ISO3.get(country_iso, country_iso + "P")

    cache_dir = os.path.join(base_dir, CACHE_DIR)
    orgs_dir = os.path.join(base_dir, ORGS_DIR)
    targets_file = os.path.join(base_dir, "_target_orgs.json")
    registry_file = os.path.join(base_dir, "id_registry.json")

    # Load targets
    targets_raw = load_json(targets_file)
    if isinstance(targets_raw, dict):
        targets = targets_raw.get("organizations", [])
    else:
        targets = targets_raw

    # Load registry
    registry_data = load_json(registry_file)
    registry = registry_data.get("registry", [])
    counters = registry_data.get("counters", {}).get(country_iso, {})
    next_ids = dict(counters)

    target_qids_map = build_target_qids_map(targets, registry)

    # Load existing profiles (idempotency)
    existing_profiles = set()
    if os.path.isdir(orgs_dir):
        for fname in os.listdir(orgs_dir):
            if fname.endswith(".json") and not fname.startswith("_"):
                existing_profiles.add(fname)

    print(f"=== Generate Skeleton Profiles ===")
    print(f"Targets: {len(targets)}, Already profiled: {len(existing_profiles)}")

    generated = 0
    skipped = 0
    no_cache = 0

    for i, org in enumerate(targets):
        qid = org.get("qid") or org.get("wikidata_qid")
        name_en = org.get("name_en") or org.get("name", "")
        category = org.get("category")

        existing_id = None
        for r in registry:
            if r.get("wikidata_qid") == qid:
                existing_id = r["org_id"]
                break
        expected_file = f"{existing_id}.json" if existing_id else None

        if expected_file and expected_file in existing_profiles:
            skipped += 1
            continue

        cache_file = os.path.join(cache_dir, f"{qid}.json")
        if not os.path.exists(cache_file):
            print(f"  NOCACHE: {name_en} ({qid}), generating minimal stub")
            cache_data = {"wikidata": None, "wikipedia": None, "errors": ["no_cache_file"],
                          "source_unavailable": True, "org": org}
        else:
            cache_data = load_json(cache_file)

        cache_data = load_json(cache_file)
        profile = generate_profile(org, cache_data, registry, target_qids_map, next_ids, country_iso, country_iso3)
        org_id = profile["org_id"]
        print(f"  GEN [{i+1}/{len(targets)}]: {name_en} -> {org_id} (score={profile['collection_meta']['completeness_score']})")

        profile_path = os.path.join(orgs_dir, f"{org_id}.json")
        save_json(profile_path, profile)

        if not existing_id:
            reg_entry = {
                "org_id": org_id,
                "name": f"{org.get('name_zh', '')} ({name_en})",
                "org_type": category,
                "org_subtype": org.get("org_subtype"),
                "wikidata_qid": qid,
                "status": "profiled",
                "notes": None
            }
            registry.append(reg_entry)
            if category not in next_ids or next_ids[category] < int(org_id.split("-")[-1]):
                next_ids[category] = int(org_id.split("-")[-1])
        else:
            for r in registry:
                if r["org_id"] == existing_id:
                    r["status"] = "profiled"
                    r["wikidata_qid"] = qid
                    break
        generated += 1

    # Save org registry
    registry_data["registry"] = registry
    registry_data["counters"][country_iso] = next_ids

    # Resolve key_people QIDs
    if generated > 0 or any(
        kp.get("name", "").startswith("Q") and kp["name"][1:].isdigit()
        for fpath in sorted(glob.glob(os.path.join(orgs_dir, "*.json")))
        if not os.path.basename(fpath).startswith("_")
        for kp in load_json(fpath).get("key_people", [])
    ):
        print(f"\n--- Resolving Key People ---")
        setup_proxy()
        registry_data = resolve_key_people(orgs_dir, registry_data, cache_dir, country_iso)

    # Save final registry
    save_json(registry_file, registry_data)

    print(f"\n=== Done ===")
    print(f"  Generated: {generated}, Skipped: {skipped}, No cache: {no_cache}")


if __name__ == "__main__":
    main()

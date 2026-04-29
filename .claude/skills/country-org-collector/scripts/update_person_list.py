#!/usr/bin/env python3
"""
update_person_list.py — Rebuild person_list.json from id_registry + profiles
Usage: python .claude/skills/country-org-collector/scripts/update_person_list.py output/sg/2026-04-15
"""
import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
import json
import os
import glob
from datetime import date as dt_date

from atomic_write import save_json, load_json

def determine_importance(position_title):
    """Estimate importance from position title. Expanded keyword matching for better accuracy."""
    if not position_title:
        return "low"
    t = position_title.lower()
    # High importance: heads of state/government, ministers, top judicial/central bank leaders
    high_kw = ["prime minister", "president", "chief justice", "chief executive",
               "chairman", "ceo", "managing director", "minister of foreign affairs",
               "minister of finance", "minister of defence", "minister of trade",
               "minister of", "外交部长", "财政部长", "国防部长", "长官", "部长",
               "governor", "中央银行", "chief minister", "premier"]
    # Medium importance: vice/deputy ministers, judges, directors
    medium_kw = ["vice minister", "vice-minister", "deputy minister", "次官",
                 "副部长", "第一次官", "第二次官", "副长官",
                 "judge", "director", "chief", "senior", "head",
                 "ambassador", "大使", "consul", "总领事",
                 "permanent secretary", "常任秘书"]
    if any(kw in t for kw in high_kw):
        return "high"
    if any(kw in t for kw in medium_kw):
        return "medium"
    return "low"


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <output_dir>")
        sys.exit(1)

    base_dir = sys.argv[1]
    # Determine country ISO from directory path
    dir_parts = base_dir.replace("\\", "/").rstrip("/").split("/")
    country_iso = dir_parts[-2].upper() if len(dir_parts) >= 2 else "XX"

    COUNTRY_NAMES = {
        "SG": "Singapore", "MY": "Malaysia", "AU": "Australia", "BN": "Brunei",
        "CA": "Canada", "CL": "Chile", "CN": "China", "HK": "Hong Kong",
        "ID": "Indonesia", "JP": "Japan", "KR": "South Korea", "MX": "Mexico",
        "NZ": "New Zealand", "PG": "Papua New Guinea", "PE": "Peru", "PH": "Philippines",
        "RU": "Russia", "TH": "Thailand", "TW": "Chinese Taipei", "US": "United States",
        "VN": "Vietnam",
    }
    country_name = COUNTRY_NAMES.get(country_iso, country_iso)

    registry_file = os.path.join(base_dir, "id_registry.json")
    orgs_dir = os.path.join(base_dir, "orgs")
    person_list_file = os.path.join(base_dir, "person_list.json")

    # Load registry
    reg = load_json(registry_file)
    person_registry = reg["person_registry"]

    # Build source_orgs map from orgs: person_id -> [(org_id, org_name, title)]
    person_sources = {}
    for fpath in glob.glob(os.path.join(orgs_dir, "*.json")):
        if os.path.basename(fpath) == "_index.json":
            continue
        data = load_json(fpath)
        org_id = data["org_id"]
        org_name = data["basic_info"].get("name_en", "")
        for kp in data.get("key_people", []):
            pid = kp.get("person_id")
            if pid:
                if pid not in person_sources:
                    person_sources[pid] = []
                person_sources[pid].append({
                    "org_id": org_id,
                    "org_name": org_name,
                    "position_title": kp.get("title", "")
                })

    # Build person_list entries
    persons = []
    for p in person_registry:
        pid = p["person_id"]
        name = p["name"]
        sources = person_sources.get(pid, [])

        # Parse name
        name_zh = None
        name_en = name
        if "(" in name and ")" in name:
            parts = name.split("(")
            name_zh = parts[0].strip()
            name_en = parts[1].rstrip(")").strip()
        elif any('\u4e00' <= c <= '\u9fff' for c in name):
            name_zh = name
        else:
            name_en = name

        # Determine importance
        titles = [s["position_title"] for s in sources if s["position_title"]]
        importance = "low"
        for t in titles:
            imp = determine_importance(t)
            if imp == "high":
                importance = "high"
                break
            elif imp == "medium":
                importance = "medium"

        entry = {
            "person_id": pid,
            "wikidata_qid": p.get("wikidata_qid"),
            "name": name,
            "name_zh": name_zh,
            "name_en": name_en,
            "importance_level": importance,
            "importance_reason": "; ".join(titles[:2]) if titles else None,
            "source_orgs": sources[:5],
            "discovery_source": "key_people",
            "nationality": country_iso,
            "notes": None
        }
        persons.append(entry)

    # Build person_list.json
    by_importance = {"high": 0, "medium": 0, "low": 0}
    by_source = {"key_people": 0, "web_search": 0, "wikidata": 0, "wikipedia": 0, "other": 0}
    with_qid = 0
    for p in persons:
        by_importance[p["importance_level"]] = by_importance.get(p["importance_level"], 0) + 1
        src = p.get("discovery_source", "other")
        by_source[src] = by_source.get(src, 0) + 1
        if p.get("wikidata_qid"):
            with_qid += 1

    person_list = {
        "metadata": {
            "country": country_name,
            "country_iso": country_iso,
            "collection_date": str(dt_date.today()),
            "phase": "phase4_person_list",
            "source_org_count": len(glob.glob(os.path.join(orgs_dir, "*.json"))) - 1,
            "total_persons": len(persons)
        },
        "persons": persons,
        "summary": {
            "by_importance_level": by_importance,
            "by_discovery_source": by_source,
            "data_quality": {
                "with_person_id": len(persons),
                "with_wikidata_qid": with_qid,
                "without_person_id": 0
            }
        }
    }

    save_json(person_list_file, person_list)

    print(f"Saved {len(persons)} persons to person_list.json")
    by_imp = {}
    for p in persons:
        imp = p["importance_level"]
        by_imp[imp] = by_imp.get(imp, 0) + 1
    print(f"By importance: {by_imp}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
generate_index.py — 自动生成 orgs/_index.json 和 persons/_index.json

用法:
  python .claude/skills/country-org-collector/scripts/generate_index.py output/sg/2026-04-15

功能:
  - 扫描 orgs/ 目录下的所有 {ORG_ID}.json 文件，生成 orgs/_index.json
  - 扫描 persons/ 目录下的所有 {PERSON_ID}.json 文件，生成 persons/_index.json
  - 自动计算 completeness 统计信息
  - 跳过 _index.json 自身和非 JSON 文件
"""

import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')

import json
import os
import re
from datetime import date
from collections import Counter

from atomic_write import save_json, load_json


def generate_orgs_index(base_dir):
    """Scan orgs/ directory and generate _index.json"""
    orgs_dir = os.path.join(base_dir, "orgs")
    index_path = os.path.join(orgs_dir, "_index.json")

    if not os.path.isdir(orgs_dir):
        print(f"  SKIP: {orgs_dir} not found")
        return

    entries = []
    for fname in sorted(os.listdir(orgs_dir)):
        if fname.startswith("_") or not fname.endswith(".json"):
            continue
        fpath = os.path.join(orgs_dir, fname)
        try:
            data = load_json(fpath)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"  WARN: {fname} parse error: {e}")
            continue

        bi = data.get("basic_info", {})
        meta = data.get("collection_meta", {})
        entry = {
            "org_id": data.get("org_id"),
            "name": f"{bi.get('name_zh', '')} ({bi.get('name_en', '')})".rstrip(),
            "category": bi.get("org_type"),
            "subcategory": bi.get("org_subtype"),
            "completeness": meta.get("completeness_score"),
        }
        entries.append(entry)

    if not entries:
        print(f"  SKIP: no profile files found in {orgs_dir}")
        return

    # Determine country and date from first entry or directory structure
    dir_parts = base_dir.replace("\\", "/").rstrip("/").split("/")
    country = dir_parts[-2].upper() if len(dir_parts) >= 2 else "XX"
    col_date = dir_parts[-1] if len(dir_parts) >= 1 else str(date.today())

    scores = [e["completeness"] for e in entries if e["completeness"] is not None]
    avg_score = round(sum(scores) / len(scores)) if scores else 0

    index_data = {
        "country": country,
        "collection_date": col_date,
        "phase": "phase5_validation",
        "total_profiles": len(entries),
        "profiles": entries,
        "completeness_summary": {
            "avg_score": avg_score,
            "high_completeness_gt80": sum(1 for s in scores if s > 80),
            "medium_completeness_50_80": sum(1 for s in scores if 50 <= s <= 80),
            "low_completeness_lt50": sum(1 for s in scores if s < 50),
        },
    }

    save_json(index_path, index_data)

    print(f"  OK: {index_path} ({len(entries)} profiles, avg={avg_score})")


def generate_persons_index(base_dir):
    """Scan persons/ directory and generate _index.json"""
    persons_dir = os.path.join(base_dir, "persons")
    index_path = os.path.join(persons_dir, "_index.json")

    if not os.path.isdir(persons_dir):
        print(f"  SKIP: {persons_dir} not found")
        return

    entries = []
    for fname in sorted(os.listdir(persons_dir)):
        if fname.startswith("_") or not fname.endswith(".json"):
            continue
        fpath = os.path.join(persons_dir, fname)
        try:
            data = load_json(fpath)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"  WARN: {fname} parse error: {e}")
            continue

        meta = data.get("collection_meta", {})
        entry = {
            "person_id": data.get("person_id"),
            "wikidata_qid": data.get("wikidata_qid"),
            "name_en": data.get("name_en"),
            "name_zh": data.get("name_zh"),
            "gender": data.get("gender"),
            "importance_level": _get_importance(data),
            "current_title": _get_current_title(data),
            "completeness_score": meta.get("completeness_score"),
            "file": fname,
        }
        entries.append(entry)

    if not entries:
        print(f"  SKIP: no person files found in {persons_dir}")
        return

    dir_parts = base_dir.replace("\\", "/").rstrip("/").split("/")
    country = dir_parts[-2].upper() if len(dir_parts) >= 2 else "XX"
    col_date = dir_parts[-1] if len(dir_parts) >= 1 else str(date.today())

    # Collect source orgs
    source_orgs = set()
    for e in entries:
        source_orgs.add(e.get("importance_level", "unknown"))

    scores = [e["completeness_score"] for e in entries if e["completeness_score"] is not None]
    avg_score = round(sum(scores) / len(scores)) if scores else 0

    by_level = Counter(e.get("importance_level") for e in entries)

    index_data = {
        "metadata": {
            "collection_date": col_date,
            "phase": "phase5_validation",
            "country": country,
            "total_profiles": len(entries),
        },
        "profiles": entries,
        "completeness_summary": {
            "avg_score": avg_score,
            "high_completeness_gt80": sum(1 for s in scores if s > 80),
            "medium_completeness_50_80": sum(1 for s in scores if 50 <= s <= 80),
            "low_completeness_lt50": sum(1 for s in scores if s < 50),
        },
        "by_importance_level": dict(by_level),
    }

    save_json(index_path, index_data)

    print(f"  OK: {index_path} ({len(entries)} persons, avg={avg_score})")


def _get_importance(data):
    """Try to read importance from person_list.json, fallback to heuristic"""
    # For standalone operation, estimate from current_positions
    positions = data.get("current_positions", [])
    if not positions:
        return "low"
    first_pos = str(positions[0]).lower() if positions else ""
    if any(kw in first_pos for kw in ["prime minister", "president", "chief justice", "chief executive"]):
        return "high"
    if any(kw in first_pos for kw in ["minister", "judge of appeal", "justice", "chief"]):
        return "medium"
    return "low"


def _get_current_title(data):
    """Get primary current position title"""
    positions = data.get("current_positions", [])
    return str(positions[0]) if positions else None


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <output_dir>")
        print(f"Example: python {sys.argv[0]} output/sg/2026-04-15")
        sys.exit(1)

    base_dir = sys.argv[1]
    if not os.path.isdir(base_dir):
        print(f"ERROR: {base_dir} is not a directory")
        sys.exit(1)

    print(f"Generating indexes for: {base_dir}")
    generate_orgs_index(base_dir)
    generate_persons_index(base_dir)
    print("Done.")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""P1: consolidate UNICEF / Al Mada / Vanguard and create Wafabank profile.

Creates:
  output/us/2026-09-05/orgs/US-INTL-023.json  UNICEF (global)
  output/us/2026-09-05/orgs/US-FIN-021.json   Vanguard
  output/ma/2026-10-05/orgs/MA-CORP-089.json  Al Mada
  output/ma/2026-10-05/orgs/MA-FIN-022.json   Wafabank

Merges registry IDs / refs:
  UNICEF: SA-INTL-015, CI-INTL-022, CD-INTL-034, LY-INTL-004 -> US-INTL-023
  Al Mada: MA-CORP-091, MA-CORP-092 -> MA-CORP-089
  Vanguard: US-FIN-047 -> US-FIN-021

Usage: python scripts_tmp/create_p1_profiles.py --dry|--apply
"""
import glob
import json
import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT

DATE = {"us": "2026-09-05", "ma": "2026-10-05"}


def profile(org_id, bi, related, core, industries, qid_note):
    return {
        "org_id": org_id,
        "basic_info": bi,
        "social_accounts": [],
        "digital_assets": [],
        "key_people": [],
        "departments": [],
        "recent_events": [],
        "related_entities": related,
        "core_business": core,
        "industries": industries,
        "apec_stance": None,
        "profile": None,
        "collection_meta": {
            "collection_date": "2026-11-13",
            "phase": "phase3_enriched",
            "data_sources": ["official_website", "wikidata"],
            "completeness_score": 55,
            "notes": qid_note,
            "quotes": [],
        },
    }


PROFILES = {
    "US-INTL-023": profile(
        "US-INTL-023",
        {"name_original": "United Nations Children's Fund",
         "name_zh": "联合国儿童基金会", "name_en": "United Nations Children's Fund",
         "aliases": ["UNICEF", "儿基会", "联合国儿童基金会 (UNICEF)"],
         "org_type": "INTL", "org_subtype": "multilateral_org",
         "country_iso3": "USA", "hq_country_iso3": "USA",
         "founded_date": "1946-12-11", "website": "https://www.unicef.org/",
         "wikidata_qid": "Q740308"},
        [{"org_id": "US-INTL-001", "org_name": "联合国 (United Nations)",
          "org_type": "INTL", "relationship_type": "member_of",
          "org_description": "UNICEF 是联合国系统内负责儿童权利与福祉的基金/计划，向联合国经社理事会报告。"}],
        "联合国系统内负责儿童权利、生存、发展与保护的机构，在 190 多个国家和地区开展儿童健康、营养、教育、水与卫生、保护及社会政策项目。",
        ["humanitarian_aid", "social_services"],
        "为全球 UNICEF 主体补建，合并 4 个国别注册项；国别办事处（如 KG-INTL-001）为下属机构。"),
    "US-FIN-021": profile(
        "US-FIN-021",
        {"name_original": "The Vanguard Group, Inc.",
         "name_zh": "领航投资（先锋集团）", "name_en": "The Vanguard Group",
         "aliases": ["Vanguard", "Vanguard Group", "先锋集团", "领航投资"],
         "org_type": "FIN", "org_subtype": "asset_management",
         "country_iso3": "USA", "hq_country_iso3": "USA",
         "founded_date": "1975-05-01", "website": "https://investor.vanguard.com/",
         "wikidata_qid": "Q849363"},
        [],
        "美国大型资产管理公司，以指数基金和共同基金著称；合并 US-FIN-047 重复注册项。",
        ["asset_management", "financial_services"],
        "合并 US-FIN-021 / US-FIN-047；QID Q849363。"),
    "MA-CORP-089": profile(
        "MA-CORP-089",
        {"name_original": "Al Mada",
         "name_zh": "马达德集团", "name_en": "Al Mada",
         "aliases": ["Al Mada Holding", "ONA", "Omnium Nord-Africain",
                     "SNI", "Société Nationale d'Investissement"],
         "org_type": "CORP", "org_subtype": "holding_company",
         "country_iso3": "MAR", "hq_country_iso3": "MAR",
         "founded_date": None, "website": "https://www.almada.ma/",
         "wikidata_qid": None},
        [{"org_id": "MA-FIN-002", "org_name": "Attijariwafa银行 (Attijariwafa Bank)",
          "org_type": "FIN", "relationship_type": "controlling_shareholder",
          "org_description": "Al Mada 持有 Attijariwafa Bank 约 46.5% 股份，并向董事会派驻代表。"}],
        "摩洛哥家族控股集团，前身为 ONA/SNI，投资覆盖银行、保险、零售、矿业、能源等；合并 MA-CORP-089/091/092 三个注册项。",
        ["investment", "financial_services"],
        "合并 3 个 Al Mada 注册项；QID 待补。"),
    "MA-FIN-022": profile(
        "MA-FIN-022",
        {"name_original": "Wafabank",
         "name_zh": "瓦法银行", "name_en": "Wafabank",
         "aliases": ["Wafa Bank", "Banque Wafa"],
         "org_type": "FIN", "org_subtype": "commercial_bank",
         "country_iso3": "MAR", "hq_country_iso3": "MAR",
         "founded_date": "1904-01-01", "website": None,
         "wikidata_qid": "Q12199351"},
        [{"org_id": "MA-FIN-002", "org_name": "Attijariwafa银行 (Attijariwafa Bank)",
          "org_type": "FIN", "relationship_type": "successor",
          "org_description": "2003 年 Wafabank 与 BCM 合并为 Attijariwafa Bank；本画像为历史主体。"}],
        "摩洛哥历史银行，1985 年定名 Wafabank，2003 年与 Banque Commerciale du Maroc 合并为 Attijariwafa Bank；用于承接 2003 年前的任职/沿革引用。",
        ["banking", "financial_services"],
        "历史主体画像；QID Q12199351；successor 为 MA-FIN-002。"),
}

REMAP = {
    "SA-INTL-015": "US-INTL-023",
    "CI-INTL-022": "US-INTL-023",
    "CD-INTL-034": "US-INTL-023",
    "LY-INTL-004": "US-INTL-023",
    "MA-CORP-091": "MA-CORP-089",
    "MA-CORP-092": "MA-CORP-089",
    "US-FIN-047": "US-FIN-021",
}

REG_FILES = {
    "SA-INTL-015": "output/sa/2026-09-29/id_registry.json",
    "CI-INTL-022": "output/ci/2026-10-06/id_registry.json",
    "CD-INTL-034": "output/cd/2026-10-05/id_registry.json",
    "LY-INTL-004": "output/ly/2026-10-05/id_registry.json",
    "MA-CORP-089": "output/ma/2026-10-05/id_registry.json",
    "MA-CORP-091": "output/ma/2026-10-05/id_registry.json",
    "MA-CORP-092": "output/ma/2026-10-05/id_registry.json",
    "MA-FIN-022": "output/ma/2026-10-05/id_registry.json",
    "US-FIN-021": "output/us/2026-09-05/id_registry.json",
    "US-FIN-047": "output/us/2026-09-05/id_registry.json",
    "US-INTL-023": "output/us/2026-09-05/id_registry.json",
}

INDEX_FILES = {
    "us": "output/us/2026-09-05/orgs/_index.json",
    "ma": "output/ma/2026-10-05/orgs/_index.json",
}
INDEX_ADD = {
    "us": [
        {"org_id": "US-FIN-021", "name": "领航投资（先锋集团） (The Vanguard Group)",
         "category": "FIN", "subcategory": "asset_management", "completeness": 55},
        {"org_id": "US-INTL-023", "name": "联合国儿童基金会 (UNICEF)",
         "category": "INTL", "subcategory": "multilateral_org", "completeness": 55},
    ],
    "ma": [
        {"org_id": "MA-CORP-089", "name": "马达德集团 (Al Mada)",
         "category": "CORP", "subcategory": "holding_company", "completeness": 50},
        {"org_id": "MA-FIN-022", "name": "瓦法银行 (Wafabank)",
         "category": "FIN", "subcategory": "commercial_bank", "completeness": 45},
    ],
}
NIDX = {
    "us": "output/us/2026-09-05/_name_index.json",
    "ma": "output/ma/2026-10-05/_name_index.json",
    "sa": "output/sa/2026-09-29/_name_index.json",
    "ci": "output/ci/2026-10-06/_name_index.json",
    "cd": "output/cd/2026-10-05/_name_index.json",
    "ly": "output/ly/2026-10-05/_name_index.json",
}
NIDX_ADD = {
    "US-INTL-023": ["联合国儿童基金会", "UNICEF", "United Nations Children's Fund"],
    "US-FIN-021": ["领航投资", "先锋集团", "Vanguard", "The Vanguard Group"],
    "MA-CORP-089": ["马达德集团", "Al Mada", "ONA", "SNI"],
    "MA-FIN-022": ["瓦法银行", "Wafabank", "Wafa Bank"],
}


def save_json(f, d):
    payload = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    tmp = f + ".tmp"
    last = None
    for _ in range(6):
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(payload)
            os.replace(tmp, f)
            return
        except PermissionError as e:
            last = e
            time.sleep(0.5)
    for _ in range(3):
        try:
            with open(f, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(payload)
            try:
                os.unlink(tmp)
            except OSError:
                pass
            return
        except PermissionError as e:
            last = e
            time.sleep(1.0)
    raise last


def main():
    apply = "--apply" in sys.argv
    # refs
    ref_changes = []
    counts = Counter()
    if apply:
        for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            dirty = False
            for i, w in enumerate(d.get("work_experience") or []):
                if isinstance(w, dict) and w.get("org_id") in REMAP:
                    old = w["org_id"]
                    w["org_id"] = REMAP[old]
                    counts[old] += 1
                    ref_changes.append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                        "array": "work_experience", "index": i,
                                        "field": "org_id", "old": old, "new": w["org_id"]})
                    dirty = True
            for k in ("org_ids",):
                if isinstance(d.get(k), list):
                    for i, v in enumerate(d[k]):
                        if v in REMAP:
                            old = v
                            d[k][i] = REMAP[old]
                            counts[old] += 1
                            ref_changes.append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                                "array": k, "index": i, "field": None,
                                                "old": old, "new": d[k][i]})
                            dirty = True
            if dirty:
                save_json(f, d)
        for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            dirty = False
            for i, r in enumerate(d.get("related_entities") or []):
                if isinstance(r, dict) and r.get("org_id") in REMAP:
                    old = r["org_id"]
                    r["org_id"] = REMAP[old]
                    counts[old] += 1
                    ref_changes.append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                        "array": "related_entities", "index": i,
                                        "field": "org_id", "old": old, "new": r["org_id"]})
                    dirty = True
            if dirty:
                save_json(f, d)
    else:
        # dry count only
        for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            for w in d.get("work_experience") or []:
                if isinstance(w, dict) and w.get("org_id") in REMAP:
                    counts[w["org_id"]] += 1
            if isinstance(d.get("org_ids"), list):
                for v in d["org_ids"]:
                    if v in REMAP:
                        counts[v] += 1
        for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            for r in d.get("related_entities") or []:
                if isinstance(r, dict) and r.get("org_id") in REMAP:
                    counts[r["org_id"]] += 1

    print("ref changes by old id", dict(counts), "total", sum(counts.values()))
    if not apply:
        print(json.dumps({k: list(v.keys()) for k, v in PROFILES.items()}, ensure_ascii=False, indent=1))
        print("DRY: would create", len(PROFILES), "profiles and update registry/index")
        return

    created = []
    for oid, p in PROFILES.items():
        cc = "us" if oid.startswith("US-") else "ma"
        f = os.path.join(BASE, "output", cc, DATE[cc], "orgs", oid + ".json")
        if os.path.exists(f):
            print("exists, skip", f)
            continue
        save_json(f, p)
        created.append(os.path.relpath(f, BASE).replace(os.sep, "/"))

    # registry
    reg_old = {}
    for oid, path in REG_FILES.items():
        full = os.path.join(BASE, path)
        reg = json.load(open(full, encoding="utf-8"))
        entries = reg.get("registry") or []
        target = next((e for e in entries if e.get("org_id") == oid), None)
        if target is None:
            target = {"org_id": oid, "name": PROFILES[oid]["basic_info"]["name_zh"],
                      "org_type": PROFILES[oid]["basic_info"]["org_type"],
                      "status": "profiled"}
            entries.append(target)
            reg["registry"] = entries
        reg_old.setdefault(path, {})[oid] = dict(target)
        if oid in REMAP:
            target["status"] = "merged"
            target["merged_into"] = REMAP[oid]
            target["notes"] = (target.get("notes") or "") + "；合并到 " + REMAP[oid]
        else:
            target["status"] = "profiled"
            if PROFILES[oid]["basic_info"].get("wikidata_qid"):
                target["wikidata_qid"] = PROFILES[oid]["basic_info"]["wikidata_qid"]
        save_json(full, reg)

    # org index
    idx_old = {}
    for cc, path in INDEX_FILES.items():
        full = os.path.join(BASE, path)
        d = json.load(open(full, encoding="utf-8"))
        idx_old[path] = [dict(x) for x in d.get("profiles") or []]
        for entry in INDEX_ADD[cc]:
            if not any(x.get("org_id") == entry["org_id"] for x in d["profiles"]):
                d["profiles"].append(entry)
        d["profiles"].sort(key=lambda x: x.get("org_id", ""))
        d["total_profiles"] = len(d["profiles"])
        save_json(full, d)

    # name index: remap old values, add canonical keys
    for cc, path in NIDX.items():
        full = os.path.join(BASE, path)
        if not os.path.exists(full):
            continue
        d = json.load(open(full, encoding="utf-8"))
        changed = False
        for k, v in list(d.items()):
            if v in REMAP:
                d[k] = REMAP[v]
                changed = True
        for oid, keys in NIDX_ADD.items():
            # only add canonical names in the canonical country's index or
            # the old-entity's index; harmless elsewhere
            for k in keys:
                if k not in d:
                    d[k] = oid
                    changed = True
        if changed:
            save_json(full, d)

    undo = {"created_profiles": created, "ref_changes": ref_changes,
            "registry_old": reg_old, "index_old": idx_old,
            "remap": REMAP}
    with open(os.path.join(OUT, "p1_consolidation_undo.json"), "w", encoding="utf-8") as fh:
        json.dump(undo, fh, ensure_ascii=False, indent=1)
    print(json.dumps({"created_profiles": created, "ref_changes": len(ref_changes),
                      "by_old_id": dict(counts)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

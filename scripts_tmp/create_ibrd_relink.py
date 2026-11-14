# -*- coding: utf-8 -*-
"""Create the IBRD profile (US-INTL-011) and relink 58 plain World Bank refs.

Keeps the 12 explicit World Bank Group refs on US-INTL-003.
Skips 4 composite work rows (need splitting).

Usage: python scripts_tmp/create_ibrd_relink.py --dry|--apply
"""
import csv
import json
import os
import re
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT

CSV = os.path.join(OUT, "step1b_cross_public_review_reviewed.csv")
PROFILE = os.path.join(BASE, "output/us/2026-09-05/orgs/US-INTL-011.json")
REG = os.path.join(BASE, "output/us/2026-09-05/id_registry.json")
IDX = os.path.join(BASE, "output/us/2026-09-05/orgs/_index.json")
NIDX = os.path.join(BASE, "output/us/2026-09-05/_name_index.json")

PROFILE_DATA = {
    "org_id": "US-INTL-011",
    "basic_info": {
        "name_original": "International Bank for Reconstruction and Development",
        "name_zh": "国际复兴开发银行",
        "name_en": "International Bank for Reconstruction and Development",
        "aliases": ["IBRD", "World Bank", "世界银行", "世界銀行"],
        "org_type": "INTL",
        "org_subtype": "multilateral_org",
        "country_iso3": "USA",
        "hq_country_iso3": "USA",
        "founded_date": "1944-07-22",
        "website": "https://www.worldbank.org/en/about/what-we-do/brief/ibrd",
        "wikidata_qid": "Q7164",
    },
    "social_accounts": [],
    "digital_assets": [],
    "key_people": [
        {
            "person_id": "US-PERSON-000321",
            "name": "彭安杰 (Ajay Banga)",
            "title": "行长（President）",
            "title_description": "世界银行集团行长，兼任 IBRD 行长",
            "description": "2023年6月起任世界银行集团行长；IBRD 行长由集团行长兼任。",
        }
    ],
    "departments": [],
    "recent_events": [],
    "related_entities": [
        {
            "org_id": "US-INTL-003",
            "org_name": "世界銀行集團 (World Bank Group)",
            "org_type": "INTL",
            "relationship_type": "member_of",
            "org_description": "IBRD 是世界银行集团五个成员机构之一，与 IDA、IFC、MIGA、ICSID 并列。",
        }
    ],
    "core_business": "向中等收入国家和信用良好的低收入国家提供贷款、担保、风险管理与咨询服务，是世界银行集团的主要贷款机构。",
    "industries": ["financial_services", "banking"],
    "apec_stance": None,
    "profile": None,
    "collection_meta": {
        "collection_date": "2026-11-13",
        "phase": "phase3_enriched",
        "data_sources": ["official_website", "wikidata"],
        "completeness_score": 55,
        "notes": "为区分 World Bank (IBRD) 与 World Bank Group 补建；数据来源为世界银行官网 IBRD 页面及 Wikidata Q7164。",
    },
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


def ref_name(item, cat):
    for k in (["organization", "org_name", "organization_en"] if cat == "work_org"
              else ["org_name", "name"]):
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def parse_pos(s):
    m = re.match(r"^(.*)#([A-Za-z_]+)\[(\d+)\]\.([A-Za-z_]+)$", s.strip())
    if not m:
        return None
    return m.group(1), m.group(2), int(m.group(3)), m.group(4)


def main():
    apply = "--apply" in sys.argv
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    wb = [r for r in rows if r["复核结论"] == "暂缓"
          and r["问题分类"] == "世界银行与世界银行集团粒度待定"]
    print("world bank rows", len(wb))
    if not apply:
        print(json.dumps(PROFILE_DATA, ensure_ascii=False, indent=1)[:1200])
        print("DRY: would create", PROFILE, "and relink", len(wb), "positions")
        return

    if os.path.exists(PROFILE):
        print("profile already exists; abort")
        return
    save_json(PROFILE, PROFILE_DATA)

    # registry
    reg = json.load(open(REG, encoding="utf-8"))
    found = False
    for e in reg.get("registry") or []:
        if e.get("org_id") == "US-INTL-011":
            e["status"] = "profiled"
            e["wikidata_qid"] = "Q7164"
            found = True
    if not found:
        reg.setdefault("registry", []).append({
            "org_id": "US-INTL-011", "name": "国际复兴开发银行 (IBRD)",
            "org_type": "INTL", "org_subtype": "multilateral_org",
            "wikidata_qid": "Q7164", "status": "profiled",
        })
    save_json(REG, reg)

    # org index
    idx = json.load(open(IDX, encoding="utf-8"))
    if not any(p.get("org_id") == "US-INTL-011" for p in idx.get("profiles") or []):
        entry = {"org_id": "US-INTL-011",
                 "name": "国际复兴开发银行 (International Bank for Reconstruction and Development)",
                 "category": "INTL", "subcategory": "multilateral_org",
                 "completeness": 55}
        profs = idx.setdefault("profiles", [])
        pos = next((i for i, p in enumerate(profs)
                    if p.get("org_id", "") > "US-INTL-011"), len(profs))
        profs.insert(pos, entry)
        idx["total_profiles"] = len(profs)
        save_json(IDX, idx)

    # name index
    nidx = json.load(open(NIDX, encoding="utf-8"))
    for k in ["国际复兴开发银行", "世界银行", "世界銀行", "World Bank",
              "International Bank for Reconstruction and Development"]:
        nidx.setdefault(k, "US-INTL-011")
    save_json(NIDX, nidx)

    # relink
    undo = []
    docs, dirty = {}, set()
    stats = Counter()
    skipped = []
    for r in wb:
        cat = r["类别"]
        if r["新ID"].strip() != "US-INTL-003":
            skipped.append([r["复核序号"], "unexpected_new_id", r["新ID"]])
            continue
        parsed = parse_pos(r["原始引用位置"].strip())
        if not parsed:
            skipped.append([r["复核序号"], "bad_position"])
            continue
        rel, arr, idx_name, field = parsed
        f = os.path.join(BASE, rel.replace("\\", "/"))
        if f not in docs:
            docs[f] = json.load(open(f, encoding="utf-8"))
        d = docs[f]
        items = d.get(arr) or []
        if idx_name >= len(items) or not isinstance(items[idx_name], dict):
            skipped.append([r["复核序号"], "bad_index"])
            continue
        item = items[idx_name]
        cur = item.get(field)
        nm = ref_name(item, cat)
        if str(cur) != "US-INTL-003":
            skipped.append([r["复核序号"], "stale_id", cur])
            continue
        if not ("世界银行" in nm or "world bank" in nm.lower()):
            skipped.append([r["复核序号"], "not_world_bank", nm])
            continue
        item[field] = "US-INTL-011"
        dirty.add(f)
        undo.append({"file": rel, "array": arr, "index": idx_name, "field": field,
                     "old": cur, "new": "US-INTL-011", "cat": cat,
                     "ref_name": nm, "seq": r["复核序号"]})
        stats[f"{cat}_relink"] += 1
    for f in dirty:
        save_json(f, docs[f])

    with open(os.path.join(OUT, "worldbank_relink_undo.json"), "w", encoding="utf-8") as fh:
        json.dump({"profile": PROFILE, "registry": REG, "index": IDX,
                   "name_index": NIDX, "changes": undo}, fh, ensure_ascii=False, indent=1)
    print(json.dumps({"relinked": len(undo), "files": len(dirty),
                      "by_cat": dict(stats), "skipped": skipped[:50],
                      "skipped_count": len(skipped)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

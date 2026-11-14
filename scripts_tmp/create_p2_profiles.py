# -*- coding: utf-8 -*-
"""P2: create Ahli Bank / Arab Bank / Al Akhbar profiles and merge Cisco.

Creates:
  output/om/2026-10-03/orgs/OM-FIN-018.json  Ahli Bank SAOG
  output/om/2026-10-03/orgs/OM-FIN-020.json  Arab Bank plc
  output/ma/2026-10-05/orgs/MA-MEDIA-029.json Al Akhbar (Morocco)

Merges CI-CORP-055 (Cisco) -> US-CORP-026.

Usage: python scripts_tmp/create_p2_profiles.py --dry|--apply
"""
import glob
import json
import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT


def profile(org_id, bi, related, core, industries, note):
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
            "notes": note,
            "quotes": [],
        },
    }


PROFILES = {
    "OM-FIN-018": profile(
        "OM-FIN-018",
        {"name_original": "Ahli Bank SAOG",
         "name_zh": "阿曼阿赫利银行", "name_en": "Ahli Bank SAOG",
         "aliases": ["Ahli Bank", "Ahlibank", "Al Ahli Bank", "بنك الأهلي"],
         "org_type": "FIN", "org_subtype": "commercial_bank",
         "country_iso3": "OMN", "hq_country_iso3": "OMN",
         "founded_date": "1997-01-01", "website": "https://www.ahlibank.om/",
         "wikidata_qid": None},
        [],
        "阿曼上市商业银行，提供个人、企业、公司及伊斯兰银行服务（Ahli Islamic）；在马斯喀特证券交易所上市（ABOB）。",
        ["banking", "financial_services"],
        "阿曼 Ahli Bank SAOG；不要与 LY-FIN-014（利比亚 Aman Bank）或 KW-FIN-006（科威特 ABK）混同。"),
    "OM-FIN-020": profile(
        "OM-FIN-020",
        {"name_original": "Arab Bank plc",
         "name_zh": "阿拉伯银行", "name_en": "Arab Bank plc",
         "aliases": ["Arab Bank", "البنك العربي", "Arab Bank Jordan"],
         "org_type": "FIN", "org_subtype": "commercial_bank",
         "country_iso3": "JOR", "hq_country_iso3": "JOR",
         "founded_date": "1930-07-14", "website": "https://www.arabbank.com/",
         "wikidata_qid": "Q2629881"},
        [{"org_id": "OM-FIN-005", "org_name": "阿曼阿拉伯银行 (Oman Arab Bank, OAB)",
          "org_type": "FIN", "relationship_type": "controlling_shareholder",
          "org_description": "Arab Bank plc 在 2020 年重组后持有阿曼阿拉伯银行（OAB）约 49% 股份，为其第一大股东。"}],
        "约旦安曼总部的跨国银行集团，1930 年成立，在中东、欧洲、亚洲和非洲 20 多个国家设有分支；OAB 第一大股东。",
        ["banking", "financial_services"],
        "约旦 Arab Bank plc；OM-FIN-005 是阿曼阿拉伯银行 OAB，不同实体。"),
    "MA-MEDIA-029": profile(
        "MA-MEDIA-029",
        {"name_original": "Al Akhbar",
         "name_zh": "《新闻报》", "name_en": "Al Akhbar",
         "aliases": ["الأخبار", "Al Akhbar (Morocco)", "Akhbar"],
         "org_type": "MEDIA", "org_subtype": "newspaper",
         "country_iso3": "MAR", "hq_country_iso3": "MAR",
         "founded_date": "2012-11-17", "website": "http://www.alakhbar.press.ma",
         "wikidata_qid": None},
        [],
        "摩洛哥阿拉伯语日报，2012 年 11 月 17 日由拉希德·尼尼（Rachid Niny）创办，出版商为 Awal Media，总部卡萨布兰卡。",
        ["media_publishing"],
        "摩洛哥 Al Akhbar；不要与黎巴嫩 Al Akhbar（LB-MEDIA-016）或科威特 Al Anba 混同。"),
}

REMAP = {"CI-CORP-055": "US-CORP-026"}

REG_FILES = {
    "OM-FIN-018": "output/om/2026-10-03/id_registry.json",
    "OM-FIN-020": "output/om/2026-10-03/id_registry.json",
    "MA-MEDIA-029": "output/ma/2026-10-05/id_registry.json",
    "CI-CORP-055": "output/ci/2026-10-06/id_registry.json",
}
INDEX_ADD = {
    "om": [
        {"org_id": "OM-FIN-018", "name": "阿曼阿赫利银行 (Ahli Bank SAOG)",
         "category": "FIN", "subcategory": "commercial_bank", "completeness": 55},
        {"org_id": "OM-FIN-020", "name": "阿拉伯银行 (Arab Bank plc)",
         "category": "FIN", "subcategory": "commercial_bank", "completeness": 55},
    ],
    "ma": [
        {"org_id": "MA-MEDIA-029", "name": "《新闻报》 (Al Akhbar)",
         "category": "MEDIA", "subcategory": "newspaper", "completeness": 45},
    ],
}
INDEX_FILES = {
    "om": "output/om/2026-10-03/orgs/_index.json",
    "ma": "output/ma/2026-10-05/orgs/_index.json",
}
NIDX = {
    "om": "output/om/2026-10-03/_name_index.json",
    "ma": "output/ma/2026-10-05/_name_index.json",
    "ci": "output/ci/2026-10-06/_name_index.json",
}
NIDX_ADD = {
    "OM-FIN-018": ["阿曼阿赫利银行", "Ahli Bank", "Ahlibank", "بنك الأهلي"],
    "OM-FIN-020": ["阿拉伯银行", "Arab Bank", "البنك العربي"],
    "MA-MEDIA-029": ["Al Akhbar (Morocco)", "الأخبار", "《新闻报》(Al Akhbar)"],
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
    ref_changes = []
    counts = Counter()

    def do_refs():
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
            if apply and dirty:
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
            if apply and dirty:
                save_json(f, d)

    if apply:
        do_refs()
    else:
        # dry count
        for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            for w in d.get("work_experience") or []:
                if isinstance(w, dict) and w.get("org_id") in REMAP:
                    counts[w["org_id"]] += 1
        for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            for r in d.get("related_entities") or []:
                if isinstance(r, dict) and r.get("org_id") in REMAP:
                    counts[r["org_id"]] += 1
    print("cisco refs", dict(counts))
    if not apply:
        print("DRY: would create", list(PROFILES), "and merge", REMAP)
        return

    created = []
    for oid, p in PROFILES.items():
        cc = "om" if oid.startswith("OM-") else "ma"
        date = "2026-10-03" if cc == "om" else "2026-10-05"
        f = os.path.join(BASE, "output", cc, date, "orgs", oid + ".json")
        if os.path.exists(f):
            print("exists, skip", f)
            continue
        save_json(f, p)
        created.append(os.path.relpath(f, BASE).replace(os.sep, "/"))

    reg_old = {}
    for oid, path in REG_FILES.items():
        full = os.path.join(BASE, path)
        reg = json.load(open(full, encoding="utf-8"))
        entries = reg.get("registry") or []
        target = next((e for e in entries if e.get("org_id") == oid), None)
        if target is None:
            target = {"org_id": oid, "name": PROFILES[oid]["basic_info"]["name_zh"],
                      "org_type": PROFILES[oid]["basic_info"]["org_type"]}
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
            for k in keys:
                if k not in d:
                    d[k] = oid
                    changed = True
        if changed:
            save_json(full, d)

    with open(os.path.join(OUT, "p2_consolidation_undo.json"), "w", encoding="utf-8") as fh:
        json.dump({"created_profiles": created, "ref_changes": ref_changes,
                   "registry_old": reg_old, "index_old": idx_old,
                   "remap": REMAP}, fh, ensure_ascii=False, indent=1)
    print(json.dumps({"created_profiles": created, "ref_changes": len(ref_changes),
                      "by_old_id": dict(counts)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""P3: Al Anbaa, Oman PART, Unitel, RFE/RL profiles; merge TJ RFE/RL ID.

Creates:
  output/lb/2026-09-17/orgs/LB-MEDIA-041.json
  output/om/2026-10-03/orgs/OM-GOV-041.json
  output/la/2026-09-30/orgs/LA-CORP-007.json
  output/us/2026-09-05/orgs/US-MEDIA-039.json
Merges TJ-MEDIA-011 -> US-MEDIA-039.

Leaves GK USA (PH-NGO-049) and Tango (KW-CORP-019) as registry-only/deferred.

Usage: python scripts_tmp/create_p3_profiles.py --dry|--apply
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
            "data_sources": ["official_website", "wikipedia", "wikidata"],
            "completeness_score": 50,
            "notes": note,
            "quotes": [],
        },
    }


PROFILES = {
    "LB-MEDIA-041": profile(
        "LB-MEDIA-041",
        {"name_original": "Al Anbaa",
         "name_zh": "《消息报》", "name_en": "Al Anbaa",
         "aliases": ["الأنباء", "Anbaa", "Al-Anbaa"],
         "org_type": "MEDIA", "org_subtype": "newspaper",
         "country_iso3": "LBN", "hq_country_iso3": "LBN",
         "founded_date": "1951-03-15", "website": "https://anbaaonline.com/",
         "wikidata_qid": "Q108907305"},
        [{"org_id": "LB-PARTY-006", "org_name": "社會進步黨 (黎巴嫩) (Progressive Socialist Party)",
          "org_type": "PARTY", "relationship_type": "affiliated",
          "org_description": "《消息报》是黎巴嫩社会进步党（PSP）的机关报，1951 年由 Kamal Jumblatt 创办；2012 年停印后转为 online。"}],
        "黎巴嫩阿拉伯语报纸，社会进步党机关报，1951 年 3 月 15 日由 Kamal Jumblatt 创办，2012 年 12 月停印后转为 anbaaonline.com 在线出版。",
        ["media_publishing"],
        "黎巴嫩 Al Anbaa；QID Q108907305；不要与科威特 Al Anba（KW-MEDIA-007）或黎巴嫩 Al Akhbar（LB-MEDIA-016）混同。"),
    "OM-GOV-041": profile(
        "OM-GOV-041",
        {"name_original": "Public Authority for Radio and Television",
         "name_zh": "公共广播电视总局", "name_en": "Public Authority for Radio and Television",
         "aliases": ["PART", "هيئة الإذاعة والتلفزيون"],
         "org_type": "GOV", "org_subtype": "gov_department",
         "country_iso3": "OMN", "hq_country_iso3": "OMN",
         "founded_date": "2010-10-19", "website": "https://part.gov.om/",
         "wikidata_qid": None},
        [],
        "阿曼政府广播电视机构，2010 年 10 月依第 108/2010 号皇家法令设立，管理阿曼电视台与阿曼广播；2020 年 8 月依第 95/2020 号皇家法令撤销，职能移交新闻部。本画像为历史机构。",
        ["media_publishing", "public_administration"],
        "历史机构：2020 年撤销，职能并入阿曼新闻部；用于承接 2011-2020 年任职引用。"),
    "LA-CORP-007": profile(
        "LA-CORP-007",
        {"name_original": "Star Telecom Co., Ltd.",
         "name_zh": "星电信公司（Unitel）", "name_en": "Star Telecom Co., Ltd. (Unitel)",
         "aliases": ["Unitel", "Star Telecom", "星电信"],
         "org_type": "CORP", "org_subtype": "joint_venture",
         "country_iso3": "LAO", "hq_country_iso3": "LAO",
         "founded_date": "2008-04-01", "website": "https://unitel.com.la/",
         "wikidata_qid": None},
        [{"org_id": "VN-SOE-003", "org_name": "越南军队电信集团 (Viettel)",
          "org_type": "SOE", "relationship_type": "minority_shareholder",
          "org_description": "Viettel Global 持有 Star Telecom/Unitel 49% 股份；另 51% 由老挝亚洲电信（Lao Asia Telecom）持有。"}],
        "老挝主要电信运营商，品牌 Unitel；越南 Viettel 与老挝亚洲电信的合资企业，2008 年开始运营，提供移动、宽带、数字电视与 U-Money 等服务。",
        ["telecommunications"],
        "老挝 Star Telecom/Unitel；Viettel 持股 49%；无现有画像。"),
    "US-MEDIA-039": profile(
        "US-MEDIA-039",
        {"name_original": "Radio Free Europe/Radio Liberty",
         "name_zh": "自由欧洲电台/自由电台", "name_en": "Radio Free Europe/Radio Liberty",
         "aliases": ["RFE/RL", "RFE", "RL", "自由欧洲电台", "自由电台"],
         "org_type": "MEDIA", "org_subtype": "broadcaster",
         "country_iso3": "CZE", "hq_country_iso3": "CZE",
         "founded_date": "1949-06-01", "website": "https://www.rferl.org/",
         "wikidata_qid": "Q485500"},
        [{"org_id": "KG-MEDIA-006", "org_name": "RFE/RL 吉尔吉斯语部（Azattyk）",
          "org_type": "MEDIA", "relationship_type": "affiliated",
          "org_description": "Azattyk 是 RFE/RL 的吉尔吉斯语部。"},
         {"org_id": "UZ-MEDIA-010", "org_name": "奥佐德利克电台 (Ozodlik)",
          "org_type": "MEDIA", "relationship_type": "affiliated",
          "org_description": "Ozodlik 是 RFE/RL 的乌兹别克语部。"}],
        "美国资助的国际广播机构，1949 年成立，总部位于布拉格；以 20 多种语言向中东欧、中亚、高加索和中东播出。",
        ["broadcasting", "media_publishing"],
        "全球母体画像；KG-MEDIA-006 / UZ-MEDIA-010 为语言部，不是母体。QID Q485500。"),
}

REMAP = {"TJ-MEDIA-011": "US-MEDIA-039"}

REG_FILES = {
    "LB-MEDIA-041": "output/lb/2026-09-17/id_registry.json",
    "OM-GOV-041": "output/om/2026-10-03/id_registry.json",
    "LA-CORP-007": "output/la/2026-09-30/id_registry.json",
    "US-MEDIA-039": "output/us/2026-09-05/id_registry.json",
    "TJ-MEDIA-011": "output/tj/2026-09-27/id_registry.json",
}
INDEX_ADD = {
    "lb": [{"org_id": "LB-MEDIA-041", "name": "《消息报》 (Al Anbaa)",
            "category": "MEDIA", "subcategory": "newspaper", "completeness": 50}],
    "om": [{"org_id": "OM-GOV-041", "name": "公共广播电视总局 (Public Authority for Radio and Television)",
            "category": "GOV", "subcategory": "gov_department", "completeness": 50}],
    "la": [{"org_id": "LA-CORP-007", "name": "星电信公司（Unitel） (Star Telecom)",
            "category": "CORP", "subcategory": "joint_venture", "completeness": 50}],
    "us": [{"org_id": "US-MEDIA-039", "name": "自由欧洲电台/自由电台 (RFE/RL)",
            "category": "MEDIA", "subcategory": "broadcaster", "completeness": 50}],
}
INDEX_FILES = {
    "lb": "output/lb/2026-09-17/orgs/_index.json",
    "om": "output/om/2026-10-03/orgs/_index.json",
    "la": "output/la/2026-09-30/orgs/_index.json",
    "us": "output/us/2026-09-05/orgs/_index.json",
}
NIDX = {
    "lb": "output/lb/2026-09-17/_name_index.json",
    "om": "output/om/2026-10-03/_name_index.json",
    "la": "output/la/2026-09-30/_name_index.json",
    "us": "output/us/2026-09-05/_name_index.json",
    "tj": "output/tj/2026-09-27/_name_index.json",
}
NIDX_ADD = {
    "LB-MEDIA-041": ["Al Anbaa", "الأنباء", "《消息报》(Al Anbaa)"],
    "OM-GOV-041": ["公共广播电视总局", "PART", "هيئة الإذاعة والتلفزيون"],
    "LA-CORP-007": ["星电信", "Unitel", "Star Telecom"],
    "US-MEDIA-039": ["自由欧洲电台", "自由电台", "RFE/RL", "Radio Free Europe/Radio Liberty"],
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

    print("RFE/RL refs", dict(counts))
    if not apply:
        print("DRY: would create", list(PROFILES), "and merge", REMAP)
        return

    created = []
    for oid, p in PROFILES.items():
        cc = oid.split("-")[0].lower()
        date = {"lb": "2026-09-17", "om": "2026-10-03", "la": "2026-09-30",
                "us": "2026-09-05"}[cc]
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

    with open(os.path.join(OUT, "p3_consolidation_undo.json"), "w", encoding="utf-8") as fh:
        json.dump({"created_profiles": created, "ref_changes": ref_changes,
                   "registry_old": reg_old, "index_old": idx_old,
                   "remap": REMAP}, fh, ensure_ascii=False, indent=1)
    print(json.dumps({"created_profiles": created, "ref_changes": len(ref_changes),
                      "by_old_id": dict(counts)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Global normalization for OpenAI / Anthropic / SpaceX / Starlink / xAI.

Canonical IDs (US registry, new IDs 249-252; xAI already US-CORP-069):
  OpenAI     -> US-CORP-249
  Anthropic  -> US-CORP-250
  SpaceX     -> US-CORP-251
  Starlink   -> US-CORP-252
  xAI        -> US-CORP-069

Principles:
  - never renumber an existing profile ID; these IDs are new and unused
  - only redirect refs whose name matches the target entity; Tesla/Ford/Cisco
    refs under collision IDs US-CORP-013/014/026 are left untouched
  - SpaceX/Starlink composite refs go to Starlink (the specific service/entity)
  - the OpenAI Foundation & OpenAI Group PBC composite row is left null
  - new profiles have profile=null: no avatar is moved or invented

Usage: python scripts_tmp/normalize_global_ai_space.py --dry|--apply
"""
import glob
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict

BASE = "D:/ai-workspace/apec-osint-tool"
OUT = os.path.join(BASE, "output/_id_audit")

DATASETS = {
    "au": "2026-05-08",
    "cl": "2026-10-02",
    "jp": "2026-06-09",
    "kr": "2026-05-04",
    "kw": "2026-10-03",
    "pe": "2026-10-01",
    "pg": "2026-05-25",
    "us": "2026-09-05",
    "ae": "2026-10-02",
    "iq": "2026-11-02",
}

CANON = {
    "openai": {
        "id": "US-CORP-249",
        "name": "OpenAI",
        "profile": {
            "org_id": "US-CORP-249",
            "basic_info": {
                "name_original": "OpenAI",
                "name_zh": "OpenAI",
                "name_en": "OpenAI",
                "aliases": ["OpenAI OpCo, LLC", "OpenAI Global, LLC", "OpenAI Group PBC", "开放人工智能"],
                "org_type": "CORP",
                "org_subtype": "private_company",
                "country_iso3": "USA",
                "hq_country_iso3": "USA",
                "founded_date": "2015-12-11",
                "website": "https://openai.com/",
                "wikidata_qid": "Q21708200",
            },
            "social_accounts": [],
            "digital_assets": [],
            "key_people": [],
            "departments": [],
            "recent_events": [],
            "related_entities": [
                {
                    "org_id": "US-CORP-004",
                    "org_name": "微软 (Microsoft)",
                    "org_type": "CORP",
                    "org_description": "OpenAI 的主要战略投资者与云合作伙伴，双方在 Azure 算力、模型授权与企业 AI 产品上深度合作。",
                    "relationship_type": "minority_shareholder",
                }
            ],
            "core_business": "美国人工智能研究与部署公司，开发 ChatGPT、GPT 系列模型、API 及企业级 AI 平台。",
            "industries": ["information_technology", "software", "research_development"],
            "apec_stance": None,
            "profile": None,
            "collection_meta": {
                "collection_date": "2026-11-13",
                "phase": "phase3_enriched",
                "data_sources": ["official_website", "wikidata"],
                "completeness_score": 55,
                "notes": "全球归一补建；合并各国/地区重复自动注册项，保留历史 ID 于 deprecated_registry。",
                "quotes": [],
            },
        },
    },
    "anthropic": {
        "id": "US-CORP-250",
        "name": "Anthropic",
        "profile": {
            "org_id": "US-CORP-250",
            "basic_info": {
                "name_original": "Anthropic, PBC",
                "name_zh": "Anthropic",
                "name_en": "Anthropic",
                "aliases": ["Anthropic PBC", "Anthropic AI"],
                "org_type": "CORP",
                "org_subtype": "private_company",
                "country_iso3": "USA",
                "hq_country_iso3": "USA",
                "founded_date": "2021-01-01",
                "website": "https://www.anthropic.com/",
                "wikidata_qid": "Q116758847",
            },
            "social_accounts": [],
            "digital_assets": [],
            "key_people": [],
            "departments": [],
            "recent_events": [],
            "related_entities": [
                {
                    "org_id": "US-CORP-002",
                    "org_name": "亚马逊 (Amazon)",
                    "org_type": "CORP",
                    "org_description": "Anthropic 的主要战略投资者与云合作伙伴，通过 AWS 提供算力与模型服务。",
                    "relationship_type": "minority_shareholder",
                },
                {
                    "org_id": "US-CORP-005",
                    "org_name": "Alphabet (Alphabet Inc.)",
                    "org_type": "CORP",
                    "org_description": "Anthropic 的主要战略投资者之一，通过 Google Cloud 提供算力与云服务。",
                    "relationship_type": "minority_shareholder",
                },
            ],
            "core_business": "美国人工智能安全与研究公司，开发 Claude 系列大模型及面向企业与开发者的 AI 产品。",
            "industries": ["information_technology", "software", "research_development"],
            "apec_stance": None,
            "profile": None,
            "collection_meta": {
                "collection_date": "2026-11-13",
                "phase": "phase3_enriched",
                "data_sources": ["official_website", "wikidata"],
                "completeness_score": 55,
                "notes": "全球归一补建；合并重复自动注册项，保留历史 ID 于 deprecated_registry。",
                "quotes": [],
            },
        },
    },
    "spacex": {
        "id": "US-CORP-251",
        "name": "SpaceX",
        "profile": {
            "org_id": "US-CORP-251",
            "basic_info": {
                "name_original": "Space Exploration Technologies Corp.",
                "name_zh": "太空探索技术公司",
                "name_en": "SpaceX",
                "aliases": ["SpaceX", "Space Exploration Technologies", "太空探索技术公司（SpaceX）"],
                "org_type": "CORP",
                "org_subtype": "private_company",
                "country_iso3": "USA",
                "hq_country_iso3": "USA",
                "founded_date": "2002-03-14",
                "website": "https://www.spacex.com/",
                "wikidata_qid": "Q193701",
            },
            "social_accounts": [],
            "digital_assets": [],
            "key_people": [
                {
                    "person_id": "US-PERSON-000058",
                    "name": "伊隆·马斯克 (Elon Musk)",
                    "title": "创始人、首席执行官兼首席工程师",
                    "title_description": "SpaceX 创始人及最高管理者",
                    "description": "2002 年创立 SpaceX，主导猎鹰火箭、龙飞船与星舰项目，并推动星链卫星互联网商业化。",
                }
            ],
            "departments": [],
            "recent_events": [],
            "related_entities": [
                {
                    "org_id": "US-CORP-252",
                    "org_name": "星链 (Starlink)",
                    "org_type": "CORP",
                    "org_description": "SpaceX 旗下低轨卫星互联网业务与品牌。",
                    "relationship_type": "subsidiary",
                },
                {
                    "org_id": "US-CORP-069",
                    "org_name": "xAI",
                    "org_type": "CORP",
                    "org_description": "2026 年成为 SpaceX 子公司的人工智能公司，开发 Grok 大模型。",
                    "relationship_type": "subsidiary",
                },
            ],
            "core_business": "美国航天制造与发射服务公司，开发猎鹰火箭、龙飞船、星舰及星链卫星网络。",
            "industries": ["aerospace_defense", "space"],
            "apec_stance": None,
            "profile": None,
            "collection_meta": {
                "collection_date": "2026-11-13",
                "phase": "phase3_enriched",
                "data_sources": ["official_website", "wikidata"],
                "completeness_score": 55,
                "notes": "全球归一补建；合并重复自动注册项及 US-CORP-026 下的 SpaceX 影子项。",
                "quotes": [],
            },
        },
    },
    "starlink": {
        "id": "US-CORP-252",
        "name": "Starlink",
        "profile": {
            "org_id": "US-CORP-252",
            "basic_info": {
                "name_original": "Starlink",
                "name_zh": "星链",
                "name_en": "Starlink",
                "aliases": ["Starlink Satellite Communications LLC", "星链卫星通信公司", "SpaceX Starlink"],
                "org_type": "CORP",
                "org_subtype": "subsidiary",
                "country_iso3": "USA",
                "hq_country_iso3": "USA",
                "founded_date": None,
                "website": "https://www.starlink.com/",
                "wikidata_qid": "Q127785902",
            },
            "social_accounts": [],
            "digital_assets": [],
            "key_people": [],
            "departments": [],
            "recent_events": [],
            "related_entities": [
                {
                    "org_id": "US-CORP-251",
                    "org_name": "太空探索技术公司 (SpaceX)",
                    "org_type": "CORP",
                    "org_description": "Starlink 的母公司，负责卫星制造、发射与星座运营。",
                    "relationship_type": "parent_org",
                }
            ],
            "core_business": "SpaceX 旗下低轨卫星互联网业务，提供星链宽带、海事/航空/政府通信与手机直连卫星服务。",
            "industries": ["telecommunications", "internet_services", "space"],
            "apec_stance": None,
            "profile": None,
            "collection_meta": {
                "collection_date": "2026-11-13",
                "phase": "phase3_enriched",
                "data_sources": ["official_website", "wikidata"],
                "completeness_score": 55,
                "notes": "全球归一补建；SpaceX/Starlink 复合引用统一归到 Starlink 品牌实体。",
                "quotes": [],
            },
        },
    },
    "xai": {
        "id": "US-CORP-069",
        "name": "xAI",
        "profile": {
            "org_id": "US-CORP-069",
            "basic_info": {
                "name_original": "xAI Corp.",
                "name_zh": "xAI",
                "name_en": "xAI",
                "aliases": ["X.AI", "xAI Corp.", "xAI公司", "SpaceXAI"],
                "org_type": "CORP",
                "org_subtype": "subsidiary",
                "country_iso3": "USA",
                "hq_country_iso3": "USA",
                "founded_date": "2023-07-12",
                "website": "https://x.ai/",
                "wikidata_qid": "Q120599684",
            },
            "social_accounts": [],
            "digital_assets": [],
            "key_people": [
                {
                    "person_id": "US-PERSON-000058",
                    "name": "伊隆·马斯克 (Elon Musk)",
                    "title": "创始人兼首席执行官",
                    "title_description": "xAI 创始人及最高管理者",
                    "description": "2023 年创立 xAI，主导 Grok 大模型研发；2026 年 xAI 成为 SpaceX 子公司。",
                }
            ],
            "departments": [],
            "recent_events": [],
            "related_entities": [
                {
                    "org_id": "US-CORP-251",
                    "org_name": "太空探索技术公司 (SpaceX)",
                    "org_type": "CORP",
                    "org_description": "xAI 的母公司；2026 年 xAI 成为 SpaceX 子公司。",
                    "relationship_type": "parent_org",
                },
                {
                    "org_id": "US-CORP-013",
                    "org_name": "特斯拉公司 (Tesla, Inc.)",
                    "org_type": "CORP",
                    "org_description": "与 xAI 存在创始人及业务协同关系的关联公司。",
                    "relationship_type": "affiliated",
                },
            ],
            "core_business": "美国人工智能公司，开发 Grok 大模型与 X 平台 AI 能力；2026 年成为 SpaceX 子公司。",
            "industries": ["information_technology", "software", "research_development"],
            "apec_stance": None,
            "profile": None,
            "collection_meta": {
                "collection_date": "2026-11-13",
                "phase": "phase3_enriched",
                "data_sources": ["official_website", "wikidata"],
                "completeness_score": 55,
                "notes": "沿用既有 US-CORP-069；补建画像并标注 2026 年并入 SpaceX。",
                "quotes": [],
            },
        },
    },
}

# (dataset, shadow ID, shadow name, target entity)
SHADOWS = [
    ("au", "AU-CORP-040", "SpaceX/Starlink", "starlink"),
    ("au", "AU-CORP-087", "SpaceX Starlink", "starlink"),
    ("cl", "CL-CORP-071", "星链 (Starlink / SpaceX)", "starlink"),
    ("jp", "JP-CORP-059", "OpenAI（OpenAI Global, LLC）", "openai"),
    ("kw", "KW-航天与卫星通信企业-001", "太空探索技术公司/星链 (SpaceX / Starlink)", "starlink"),
    ("pe", "PE-CORP-038", "星链 (Starlink)", "starlink"),
    ("pg", "PG-CORP-031", "Starlink（SpaceX）", "starlink"),
    ("us", "US-CORP-013", "Anthropic", "anthropic"),
    ("us", "US-CORP-014", "OpenAI", "openai"),
    ("us", "US-CORP-026", "SpaceX", "spacex"),
]

OPENAI_RE = re.compile(r"(?<![a-z])open\s*ai(?![a-z])|开放人工智能", re.I)
ANTHROPIC_RE = re.compile(r"(?<![a-z])anthropic(?![a-z])", re.I)
SPACEX_RE = re.compile(r"(?<![a-z])space\s*x(?![a-z])|space\s+exploration\s+technologies|太空探索技术", re.I)
STARLINK_RE = re.compile(r"(?<![a-z])star\s*link(?![a-z])|星链", re.I)
XAI_RE = re.compile(r"(?<![a-z])x\s*\.?\s*ai(?![a-z])", re.I)


def save_json(path, obj):
    payload = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    tmp = path + ".tmp"
    last = None
    for _ in range(6):
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(payload)
            os.replace(tmp, path)
            return
        except PermissionError as e:
            last = e
            time.sleep(0.5)
    for _ in range(3):
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
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


def ref_name(item):
    for key in ("organization", "org_name", "organization_en", "company", "name", "name_en"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def classify(name):
    """Return canonical entity key, or None/skip for non-targets."""
    if not name:
        return None
    openai = bool(OPENAI_RE.search(name))
    anthropic = bool(ANTHROPIC_RE.search(name))
    spacex = bool(SPACEX_RE.search(name))
    starlink = bool(STARLINK_RE.search(name))
    xai = bool(XAI_RE.search(name))
    # OpenAI Foundation & OpenAI Group PBC is one composite ref, not one org.
    if openai and ("基金会" in name or "foundation" in name.lower()) and "pbc" in name.lower():
        return "skip_openai_composite"
    if starlink:
        return "starlink"
    hits = [k for k, v in (("openai", openai), ("anthropic", anthropic),
                           ("spacex", spacex), ("xai", xai)) if v]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        return "skip_multi"
    return None


def main():
    apply = "--apply" in sys.argv
    datasets = {}
    for cc, date in DATASETS.items():
        folder = os.path.join(BASE, "output", cc, date)
        datasets[cc] = {
            "folder": folder,
            "registry": os.path.join(folder, "id_registry.json"),
            "index": os.path.join(folder, "orgs", "_index.json"),
        }

    regs = {}
    for cc, info in datasets.items():
        regs[cc] = json.load(open(info["registry"], encoding="utf-8"))

    undo = {"registry": defaultdict(list), "refs": [], "profiles": [], "indexes": []}
    stats = Counter()

    # 1) Archive/merge shadow registry entries.
    for cc, shadow_id, shadow_name, entity in SHADOWS:
        target = CANON[entity]["id"]
        reg = regs[cc]
        registry = reg.get("registry") or []
        idx = None
        for i, row in enumerate(registry):
            if row.get("org_id") == shadow_id and (row.get("name") or "").strip() == shadow_name:
                idx = i
                break
        if idx is not None:
            old = registry.pop(idx)
            old_original = dict(old)
            old["status"] = "merged"
            old["merged_into"] = target
            old["deprecated_reason"] = f"global {entity} normalization"
            reg["registry"] = registry
            reg.setdefault("deprecated_registry", []).append(old)
            undo["registry"][datasets[cc]["registry"]].append(
                {"action": "merge_shadow", "id": shadow_id, "name": shadow_name,
                 "target": target, "old": old_original, "new": dict(old)}
            )
            stats["shadows_merged"] += 1
            continue

        # US-CORP-013/014/026 already live in deprecated_registry.
        dep = reg.get("deprecated_registry") or []
        found = None
        for row in dep:
            if row.get("org_id") == shadow_id and (row.get("name") or "").strip() == shadow_name:
                found = row
                break
        if found is not None:
            old = dict(found)
            found["status"] = "merged"
            found["merged_into"] = target
            found["deprecated_reason"] = f"global {entity} normalization"
            undo["registry"][datasets[cc]["registry"]].append(
                {"action": "update_deprecated", "id": shadow_id, "name": shadow_name,
                 "target": target, "old": old}
            )
            stats["deprecated_updated"] += 1
            continue
        stats["shadow_not_found"] += 1
        print("WARN shadow not found:", cc, shadow_id, shadow_name)

    # 2) Ensure canonical registry entries in US.
    us = regs["us"]
    us_registry = us.setdefault("registry", [])
    for entity, spec in CANON.items():
        oid = spec["id"]
        row = next((x for x in us_registry if x.get("org_id") == oid), None)
        new_row = {
            "org_id": oid,
            "name": spec["name"],
            "org_type": "CORP",
            "status": "profiled",
            "wikidata_qid": spec["profile"]["basic_info"]["wikidata_qid"],
            "source": "global AI/space normalization",
        }
        if row is None:
            us_registry.append(new_row)
            undo["registry"][datasets["us"]["registry"]].append(
                {"action": "add_canonical", "id": oid, "new": new_row}
            )
            stats["canonical_added"] += 1
        else:
            old = dict(row)
            row["status"] = "profiled"
            row["name"] = spec["name"]
            row["org_type"] = "CORP"
            row["wikidata_qid"] = spec["profile"]["basic_info"]["wikidata_qid"]
            undo["registry"][datasets["us"]["registry"]].append(
                {"action": "update_canonical", "id": oid, "old": old, "new": dict(row)}
            )
            stats["canonical_updated"] += 1

    # 3) Prepare/apply profiles.
    for entity, spec in CANON.items():
        oid = spec["id"]
        path = os.path.join(datasets["us"]["folder"], "orgs", oid + ".json")
        if os.path.exists(path):
            stats["profiles_existing"] += 1
            print("profile exists, skip", oid)
            continue
        undo["profiles"].append({"id": oid, "path": path})
        stats["profiles_created"] += 1
        if apply:
            save_json(path, spec["profile"])
        else:
            print("prepare profile", oid, spec["profile"]["basic_info"]["name_zh"])

    # 4) Update US org index.
    idx_path = datasets["us"]["index"]
    idx = json.load(open(idx_path, encoding="utf-8"))
    old_idx = json.loads(json.dumps(idx))
    profiles = idx.setdefault("profiles", [])
    by_id = {x.get("org_id"): x for x in profiles if isinstance(x, dict)}
    for entity, spec in CANON.items():
        oid = spec["id"]
        if oid in by_id:
            continue
        bi = spec["profile"]["basic_info"]
        name = bi["name_zh"] if bi["name_zh"] == bi["name_en"] else f'{bi["name_zh"]} ({bi["name_en"]})'
        entry = {
            "org_id": oid,
            "name": name,
            "category": "CORP",
            "subcategory": bi["org_subtype"],
            "completeness": spec["profile"]["collection_meta"]["completeness_score"],
        }
        profiles.append(entry)
        by_id[oid] = entry
    profiles.sort(key=lambda x: x.get("org_id", ""))
    idx["total_profiles"] = len(profiles)
    if old_idx != idx:
        undo["indexes"].append({"path": idx_path, "old_total": old_idx.get("total_profiles"),
                                "new_total": idx["total_profiles"]})
        if apply:
            save_json(idx_path, idx)

    # 5) Redirect matching refs across all datasets.
    for f in sorted(glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json"))):
        if os.path.basename(f).startswith("_"):
            continue
        data = json.load(open(f, encoding="utf-8"))
        dirty = False
        for arr in ("work_experience",):
            for i, item in enumerate(data.get(arr) or []):
                if not isinstance(item, dict):
                    continue
                name = ref_name(item)
                entity = classify(name)
                if entity is None:
                    continue
                if entity.startswith("skip"):
                    stats[entity] += 1
                    continue
                target = CANON[entity]["id"]
                old = item.get("org_id")
                if old == target:
                    stats["refs_already_correct"] += 1
                    continue
                undo["refs"].append({
                    "file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                    "array": arr, "index": i, "field": "org_id",
                    "old": old, "new": target, "ref_name": name, "entity": entity,
                })
                item["org_id"] = target
                dirty = True
                stats["refs_changed"] += 1
                stats[f"refs_{entity}"] += 1
        if apply and dirty:
            save_json(f, data)

    for f in sorted(glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json"))):
        if os.path.basename(f).startswith("_"):
            continue
        data = json.load(open(f, encoding="utf-8"))
        dirty = False
        for arr in ("related_entities",):
            for i, item in enumerate(data.get(arr) or []):
                if not isinstance(item, dict):
                    continue
                name = ref_name(item)
                entity = classify(name)
                if entity is None:
                    continue
                if entity.startswith("skip"):
                    stats[entity] += 1
                    continue
                target = CANON[entity]["id"]
                old = item.get("org_id")
                if old == target:
                    stats["refs_already_correct"] += 1
                    continue
                undo["refs"].append({
                    "file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                    "array": arr, "index": i, "field": "org_id",
                    "old": old, "new": target, "ref_name": name, "entity": entity,
                })
                item["org_id"] = target
                dirty = True
                stats["refs_changed"] += 1
                stats[f"refs_{entity}"] += 1
        if apply and dirty:
            save_json(f, data)

    # 6) Save registries.
    if apply:
        for cc, reg in regs.items():
            save_json(datasets[cc]["registry"], reg)

    summary = {
        "apply": apply,
        "canonical": {k: v["id"] for k, v in CANON.items()},
        "shadows_merged": stats["shadows_merged"],
        "deprecated_updated": stats["deprecated_updated"],
        "shadow_not_found": stats["shadow_not_found"],
        "canonical_added": stats["canonical_added"],
        "canonical_updated": stats["canonical_updated"],
        "profiles_created": stats["profiles_created"],
        "profiles_existing": stats["profiles_existing"],
        "refs_changed": stats["refs_changed"],
        "refs_already_correct": stats["refs_already_correct"],
        "refs_by_entity": {k: stats[f"refs_{k}"] for k in CANON},
        "skipped": {k: v for k, v in stats.items() if k.startswith("skip")},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))

    payload = {
        "summary": summary,
        "registry": {k: v for k, v in undo["registry"].items()},
        "refs": undo["refs"],
        "profiles": undo["profiles"],
        "indexes": undo["indexes"],
    }
    if apply:
        path = os.path.join(OUT, "global_ai_space_normalize_undo.json")
        json.dump(payload, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("undo ->", path)
    else:
        path = os.path.join(OUT, "global_ai_space_normalize_dryrun.json")
        json.dump(payload, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("dryrun ->", path)
        print("DRY")


if __name__ == "__main__":
    main()

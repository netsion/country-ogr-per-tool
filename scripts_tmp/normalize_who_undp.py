# -*- coding: utf-8 -*-
"""Normalize global WHO / UNDP registry duplicates.

Canonical:
  WHO  -> US-INTL-005 (create profile)
  UNDP -> US-INTL-024 (create profile)
Only global entries are merged; country/regional offices are left untouched.
Refs are redirected only when the ref name matches WHO/UNDP (not the owner
profile of a collision ID such as PG-INTL-003 UN PNG or SG-INTL-001 APEC).
Usage: python scripts_tmp/normalize_who_undp.py --dry|--apply
"""
import glob, json, os, re, sys, time
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, load_datasets, match, sig

WHO_NAMES = ["世界卫生组织", "World Health Organization", "WHO", "Organisation mondiale de la Santé", "OMS", "ВОЗ", "世卫组织"]
UNDP_NAMES = ["联合国开发计划署", "United Nations Development Programme", "UNDP", "PNUD", "开发署"]
WHO_IDS = ["AU-INTL-033","CD-INTL-016","CI-INTL-027","CL-INTL-007","KR-GOV-272","KR-GOV-296","LA-INTL-008","LB-INTL-004","LY-INTL-003","MA-INTL-004","OM-INTL-018","PG-INTL-003","PH-INTL-020","RU-GOV-081","SA-INTL-009","TJ-INTL-003","TM-INTL-010","US-INTL-005","VN-INTL-001"]
UNDP_IDS = ["CD-INTL-010","CI-INTL-024","CL-INTL-009","KH-INTL-005","KW-INTL-005","LB-INTL-008","LY-INTL-022","MX-GOV-153","MX-GOV-215","SG-INTL-001","TH-INTL-029","TM-INTL-020","UZ-INTL-022"]
WHO_ID, UNDP_ID = "US-INTL-005", "US-INTL-024"


def composite(name):
    return any(x in (name or "") for x in ["/", "、", ";", "；", "与", "和", "及", "等"])


def sig_union(vals):
    c, t = set(), []
    for v in vals:
        x, y = sig(v); c |= x; t += y
    return c, t


WHO_SIG = sig_union(WHO_NAMES)
UNDP_SIG = sig_union(UNDP_NAMES)


def save_json(f, d):
    payload = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    tmp = f + ".tmp"; last = None
    for _ in range(6):
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh: fh.write(payload)
            os.replace(tmp, f); return
        except PermissionError as e: last = e; time.sleep(0.5)
    for _ in range(3):
        try:
            with open(f, "w", encoding="utf-8", newline="\n") as fh: fh.write(payload)
            try: os.unlink(tmp)
            except OSError: pass
            return
        except PermissionError as e: last = e; time.sleep(1.0)
    raise last


def profile(oid, bi, related, core, note):
    return {
        "org_id": oid, "basic_info": bi, "social_accounts": [], "digital_assets": [],
        "key_people": [], "departments": [], "recent_events": [], "related_entities": related,
        "core_business": core, "industries": ["public_health" if oid == WHO_ID else "international_trade"],
        "apec_stance": None, "profile": None,
        "collection_meta": {"collection_date": "2026-11-13", "phase": "phase3_enriched",
                            "data_sources": ["official_website", "wikidata"],
                            "completeness_score": 55, "notes": note, "quotes": []},
    }


PROFILES = {
    WHO_ID: profile(WHO_ID,
        {"name_original": "World Health Organization", "name_zh": "世界卫生组织",
         "name_en": "World Health Organization",
         "aliases": ["WHO", "世卫组织", "世界卫生组织（WHO）", "Organisation mondiale de la Santé", "OMS"],
         "org_type": "INTL", "org_subtype": "multilateral_org",
         "country_iso3": "CHE", "hq_country_iso3": "CHE",
         "founded_date": "1948-04-07", "website": "https://www.who.int/",
         "wikidata_qid": "Q7817"},
        [{"org_id": "US-INTL-001", "org_name": "联合国 (United Nations)", "org_type": "INTL",
          "relationship_type": "member_of", "org_description": "WHO 是联合国系统内负责国际公共卫生的专门机构。"}],
        "联合国系统内负责国际公共卫生的专门机构，总部日内瓦；负责全球卫生政策、疾病防控、卫生应急与标准制定。",
        "全球 WHO 主体补建；合并各国/地区的全球重复注册项，保留国别与区域办事处。"),
    UNDP_ID: profile(UNDP_ID,
        {"name_original": "United Nations Development Programme", "name_zh": "联合国开发计划署",
         "name_en": "United Nations Development Programme",
         "aliases": ["UNDP", "PNUD", "开发署", "联合国开发计划署（UNDP）"],
         "org_type": "INTL", "org_subtype": "multilateral_org",
         "country_iso3": "USA", "hq_country_iso3": "USA",
         "founded_date": "1965-11-22", "website": "https://www.undp.org/",
         "wikidata_qid": "Q161718"},
        [{"org_id": "US-INTL-001", "org_name": "联合国 (United Nations)", "org_type": "INTL",
          "relationship_type": "member_of", "org_description": "UNDP 是联合国系统内负责发展援助的机构。"}],
        "联合国系统内负责发展援助的全球网络，总部纽约；支持减贫、治理、气候、性别平等与可持续发展。",
        "全球 UNDP 主体补建；合并全球重复注册项，保留国别办事处。"),
}


def main():
    apply = "--apply" in sys.argv
    latest, _ = load_datasets()
    regpath = {}
    for cc, (date, folder) in latest.items():
        p = os.path.join(folder, "id_registry.json")
        if os.path.exists(p): regpath[cc] = p
    regs = {cc: json.load(open(p, encoding="utf-8")) for cc, p in regpath.items()}

    # owner sigs (profiles that own a collision ID)
    owner = {}
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8")); oid = d.get("org_id")
        if not oid: continue
        bi = d.get("basic_info") or {}
        vals = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")] + (bi.get("aliases") or [])
        c = set()
        for v in vals: c |= sig(v)[0]
        owner[oid] = c

    undo = {"registry": defaultdict(list), "ref_changes": [], "profiles": []}
    stats = Counter()

    # candidates: id -> (target, target_sig, label)
    cand = {}
    for i in WHO_IDS:
        if i != WHO_ID: cand[i] = (WHO_ID, WHO_SIG, "WHO")
    for i in UNDP_IDS:
        if i != UNDP_ID: cand[i] = (UNDP_ID, UNDP_SIG, "UNDP")

    # remove matching shadow registry entries
    for cid, (target, tsig, label) in cand.items():
        cc = cid[:2].lower()
        if cc not in regs:
            stats["missing_registry"] += 1; continue
        reg = regs[cc]
        ents = reg.get("registry") or []
        keep = []
        removed = 0
        for e in ents:
            if e.get("org_id") == cid and (match(sig(e.get("name")), tsig) or any(x.lower() in (e.get("name") or "").lower() for x in (WHO_NAMES if label == "WHO" else UNDP_NAMES))):
                e["status"] = "merged"; e["merged_into"] = target
                e["deprecated_reason"] = f"global {label} normalization"
                reg.setdefault("deprecated_registry", []).append(e)
                undo["registry"][regpath[cc]].append({"action": "merge_shadow", "id": cid,
                                                      "old": dict(e), "target": target})
                removed += 1
            else:
                keep.append(e)
        reg["registry"] = keep
        stats[f"removed_{label}"] += removed

    # canonical US registry + index + profile
    us = regs["us"]
    for oid, p in PROFILES.items():
        ents = us.get("registry") or []
        e = next((x for x in ents if x.get("org_id") == oid), None)
        if e is None:
            e = {"org_id": oid, "name": p["basic_info"]["name_zh"], "org_type": "INTL"}
            ents.append(e); us["registry"] = ents
        e["status"] = "profiled"
        e["name"] = p["basic_info"]["name_zh"]
        e["wikidata_qid"] = p["basic_info"]["wikidata_qid"]
    if apply:
        for cc, reg in regs.items(): save_json(regpath[cc], reg)

    idxp = os.path.join(BASE, "output/us/2026-09-05/orgs/_index.json")
    idx = json.load(open(idxp, encoding="utf-8"))
    for oid, p in PROFILES.items():
        if not any(x.get("org_id") == oid for x in idx.get("profiles") or []):
            idx["profiles"].append({"org_id": oid, "name": f"{p['basic_info']['name_zh']} ({p['basic_info']['name_en']})",
                                    "category": "INTL", "subcategory": "multilateral_org", "completeness": 55})
    idx["profiles"].sort(key=lambda x: x.get("org_id", ""))
    idx["total_profiles"] = len(idx["profiles"])
    if apply: save_json(idxp, idx)

    # refs: only names matching WHO/UNDP, and not owner profile
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8")); dirty = False
        for arr, field, kind in [("work_experience", "org_id", "org"), ("related_entities", "org_id", "org")]:
            pass
        for i, w in enumerate(d.get("work_experience") or []):
            cid = w.get("org_id")
            if cid not in cand: continue
            target, tsig, label = cand[cid]
            nm = w.get("organization") or w.get("org_name") or ""
            if nm and match(sig(nm), tsig) and not match(sig(nm), (owner.get(cid, set()), [])):
                if composite(nm):
                    stats["composite_skipped"] += 1
                    continue
                if composite(nm):
                    stats["composite_skipped"] += 1
                    continue
                undo["ref_changes"].append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                            "array": "work_experience", "index": i, "field": "org_id",
                                            "old": cid, "new": target, "ref_name": nm})
                w["org_id"] = target; dirty = True; stats["refs"] += 1
        if apply and dirty: save_json(f, d)
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8")); dirty = False
        for i, r in enumerate(d.get("related_entities") or []):
            cid = r.get("org_id")
            if cid not in cand: continue
            target, tsig, label = cand[cid]
            nm = r.get("org_name") or r.get("name") or ""
            if nm and match(sig(nm), tsig) and not match(sig(nm), (owner.get(cid, set()), [])):
                if composite(nm):
                    stats["composite_skipped"] += 1
                    continue
                if composite(nm):
                    stats["composite_skipped"] += 1
                    continue
                undo["ref_changes"].append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                            "array": "related_entities", "index": i, "field": "org_id",
                                            "old": cid, "new": target, "ref_name": nm})
                r["org_id"] = target; dirty = True; stats["refs"] += 1
        if apply and dirty: save_json(f, d)

    # create profiles
    for oid, p in PROFILES.items():
        fp = os.path.join(BASE, f"output/us/2026-09-05/orgs/{oid}.json")
        if apply:
            save_json(fp, p)
            undo["profiles"].append(fp)
    summary = {"removed_WHO": stats["removed_WHO"], "removed_UNDP": stats["removed_UNDP"],
               "refs": len(undo["ref_changes"]), "composite_skipped": stats["composite_skipped"],
               "profiles": list(PROFILES),
               "refs_by_target": dict(Counter(x["new"] for x in undo["ref_changes"]))}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if apply:
        undo["registry"] = {k: v for k, v in undo["registry"].items()}
        json.dump(undo, open(os.path.join(OUT, "who_undp_normalize_undo.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("undo ->", os.path.join(OUT, "who_undp_normalize_undo.json"))
    else:
        undo["registry"] = {k: v for k, v in undo["registry"].items()}
        json.dump(undo, open(os.path.join(OUT, "who_undp_normalize_dry_undo.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("DRY")


if __name__ == "__main__":
    main()

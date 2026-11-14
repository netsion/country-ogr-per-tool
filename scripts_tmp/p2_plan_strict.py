# -*- coding: utf-8 -*-
"""P2 batch 1 read-only plan: same-country, strict name-exact org relinks.

Only considers the current latest dataset per country and only two directions:
  work_experience -> org
  related_entities -> org

A candidate is accepted only when:
  - repair_candidates says issue in (wrong_target, dangling)
  - action == replace and suggest_status == unique and scope == same_cc
  - target ID exists and has an org profile
  - ref name strictly matches a target name (full/primary/Latin exact), not
    the loose 'match()' used by the audit
  - the exact array position is located in the live file

No data is modified.
"""
import csv
import glob
import json
import os
import random
import re
import sys
import unicodedata
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from id_integrity_audit2 import BASE, OUT, load_datasets, sig, match

LEGAL = re.compile(
    r"\b(incorporated|inc|corp|corporation|company|co|limited|ltd|llc|plc|gmbh|ag|sa|nv|bv|"
    r"holding|holdings|group|pjs|pjsc|pcc|llp|lp)\b", re.I
)
SUFFIX_ZH = re.compile(r"(股份有限公司|有限责任公司|有限公司|株式会社)$")


def clean(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[\s\.\,\-\'’`&·:：/\\|（）()\[\]【】\"“”]+", "", s)
    return s


def core(s):
    s = str(s or "").strip()
    s = re.sub(r"\s*[（(].*?[）)]\s*", "", s).strip()
    s = LEGAL.sub("", s)
    s = SUFFIX_ZH.sub("", s)
    return clean(s)


def latin_parts(s):
    out = []
    for m in re.finditer(r"[（(]([^）)]*)[）)]", str(s or "")):
        v = m.group(1).strip()
        if re.search(r"[A-Za-z]", v):
            out.append(v)
    # a fully-Latin name is itself a Latin part
    if re.search(r"[A-Za-z]", str(s or "")) and not out:
        out.append(str(s))
    return out


def names_of_org(p):
    bi = p.get("basic_info") or {}
    vals = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")]
    return [v.strip() for v in vals if isinstance(v, str) and v.strip()]


def names_of_person(p):
    vals = [p.get("name"), p.get("name_en"), p.get("name_zh"), p.get("name_original")]
    bi = p.get("basic_info") or {}
    vals += [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")]
    vals += list(p.get("aliases") or [])
    return [v.strip() for v in vals if isinstance(v, str) and v.strip()]


def strict_match(ref, target_names):
    rc_full = clean(ref)
    rc_core = core(ref)
    rl = [clean(x) for x in latin_parts(ref)]
    for tn in target_names:
        if rc_full and rc_full == clean(tn):
            return "full_exact"
        if rc_core and rc_core == core(tn):
            return "primary_exact"
        if rl and any(x == clean(tn) for x in rl):
            return "latin_exact"
    return None


def ref_name(item):
    for k in ("organization", "org_name", "organization_en", "company", "name", "name_en"):
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def main():
    latest, _ = load_datasets()
    cand = json.load(open(os.path.join(OUT, "repair_candidates.json"), encoding="utf-8"))

    orgs = {}
    for cc, (date, folder) in latest.items():
        for f in glob.glob(os.path.join(folder, "orgs", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            p = json.load(open(f, encoding="utf-8"))
            oid = p.get("org_id")
            if oid:
                orgs.setdefault(oid, {"profile": p, "names": names_of_org(p)})
        # registry names as fallback only; do not use aliases as target names here
        rp = os.path.join(folder, "id_registry.json")
        if os.path.exists(rp):
            reg = json.load(open(rp, encoding="utf-8"))
            for e in reg.get("registry") or []:
                oid = e.get("org_id")
                if not oid:
                    continue
                nm = e.get("name")
                if isinstance(nm, str) and nm.strip():
                    orgs.setdefault(oid, {"profile": None, "names": []})
                    orgs[oid]["names"].append(nm.strip())

    # strip registry-only targets: require a profile for batch 1
    org_profiles = {oid: v for oid, v in orgs.items() if v["profile"] is not None}

    rows = []
    skipped = Counter()
    for direction in ("work_org", "related_org"):
        for r in cand.get(direction, []):
            if r.get("action") != "replace" or r.get("suggest_status") != "unique":
                continue
            if r.get("scope") != "same_cc":
                skipped["not_same_cc"] += 1
                continue
            target = r.get("suggested")
            if not target or target not in org_profiles:
                skipped["target_no_profile"] += 1
                continue
            if target == (r.get("org_id") if direction == "work_org" else r.get("org_id_ref")):
                skipped["self"] += 1
                continue
            kind = strict_match(r.get("organization") if direction == "work_org" else r.get("ref_name"),
                                org_profiles[target]["names"])
            if not kind:
                skipped["strict_name_no_match"] += 1
                continue
            cc = r.get("cc")
            folder = latest.get(cc, (None, None))[1]
            if not folder:
                skipped["no_dataset"] += 1
                continue
            src_id = r.get("person_id") if direction == "work_org" else r.get("org_id")
            src_file = os.path.join(folder, "persons" if direction == "work_org" else "orgs",
                                    str(src_id) + ".json")
            if not os.path.exists(src_file):
                skipped["source_file_missing"] += 1
                continue
            data = json.load(open(src_file, encoding="utf-8"))
            arr_name = "work_experience" if direction == "work_org" else "related_entities"
            id_field = "org_id"
            found = 0
            for i, item in enumerate(data.get(arr_name) or []):
                if not isinstance(item, dict):
                    continue
                if item.get(id_field) != (r.get("org_id") if direction == "work_org" else r.get("org_id_ref")):
                    continue
                if ref_name(item) != (r.get("organization") if direction == "work_org" else r.get("ref_name")):
                    continue
                found += 1
                rows.append({
                    "direction": direction,
                    "cc": cc,
                    "file": os.path.relpath(src_file, BASE).replace(os.sep, "/"),
                    "array": arr_name,
                    "index": i,
                    "source_id": src_id,
                    "ref_name": ref_name(item),
                    "current_id": item.get(id_field),
                    "target_id": target,
                    "target_name": (org_profiles[target]["profile"].get("basic_info") or {}).get("name_zh")
                                   or (org_profiles[target]["profile"].get("basic_info") or {}).get("name_en"),
                    "match_kind": kind,
                    "issue": r.get("issue"),
                })
            if not found:
                skipped["position_not_found"] += 1

    # de-duplicate by exact position
    seen = set()
    unique = []
    for r in rows:
        key = (r["file"], r["array"], r["index"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(r)
    rows = unique

    # sample: 50 work + 50 related, deterministic
    sample = []
    for direction in ("work_org", "related_org"):
        sub = [r for r in rows if r["direction"] == direction]
        sample += sub[:50]
    sample = sample[:100]

    plan_path = os.path.join(OUT, "p2_strict_plan.csv")
    with open(plan_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    sample_path = os.path.join(OUT, "p2_strict_sample.csv")
    with open(sample_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(sample)

    summary = {
        "rows": len(rows),
        "by_direction": dict(Counter(r["direction"] for r in rows)),
        "by_match_kind": dict(Counter(r["match_kind"] for r in rows)),
        "by_issue": dict(Counter(r["issue"] for r in rows)),
        "skipped": dict(skipped),
        "sample": len(sample),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    json.dump({"summary": summary, "rows": rows, "sample": sample},
              open(os.path.join(OUT, "p2_strict_plan.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("plan ->", plan_path)
    print("sample ->", sample_path)


if __name__ == "__main__":
    main()

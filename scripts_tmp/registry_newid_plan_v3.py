# -*- coding: utf-8 -*-
"""v3 new-ID plan: ever-used allocator + shadow identity dedupe + sample review.

Reads:
  registry_dedupe_plan_v2.csv
  registry_newid_sample_80_reviewed.csv
Writes:
  registry_newid_plan_v3.csv
  registry_newid_plan_v3_summary.json
No registry/profile/reference changes.
"""
import csv
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT

V2 = os.path.join(OUT, "registry_dedupe_plan_v2.csv")
SAMPLE = os.path.join(OUT, "registry_newid_sample_80_reviewed.csv")
VALID_CATS = {"ACAD", "CORP", "FIN", "GOV", "MEDIA", "MIL", "NGO", "PARTY",
              "SOE", "INTL", "INTL_ORG"}


def norm_key(s):
    s = (s or "").lower()
    s = re.sub(r"[\s\.\,\-\'’`&·:：/\\|（）()\[\]【】]+", "", s)
    return s


def manual_key(k):
    if "kaist" in k or "koreaadvancedinstituteofscienceandtechnology" in k:
        return "kaist"
    if "commercecommission" in k:
        return "commercecommission"
    return k


def load_ever_used():
    used = set()
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/id_registry.json")):
        d = json.load(open(f, encoding="utf-8"))
        for key, idkey in [("registry", "org_id"), ("person_registry", "person_id"),
                           ("deprecated_registry", "org_id"),
                           ("deprecated_person_registry", "person_id")]:
            for e in d.get(key) or []:
                i = e.get(idkey)
                if i:
                    used.add(i)
        for e in d.get("registry") or []:
            if e.get("person_id"):
                used.add(e["person_id"])
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        if d.get("person_id"):
            used.add(d["person_id"])
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        if d.get("org_id"):
            used.add(d["org_id"])
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/_name_index.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for v in d.values():
            if isinstance(v, str) and re.match(r"^[A-Z]{2}-(PERSON|[A-Z_]+)-\d+$", v):
                used.add(v)
    return used


def main():
    plan = list(csv.DictReader(open(V2, encoding="utf-8-sig")))
    review = list(csv.DictReader(open(SAMPLE, encoding="utf-8-sig")))
    rmap = {}
    for r in review:
        rmap[(r["国家"].lower(), r["冲突ID"], r["影子名称"].strip())] = r

    used = load_ever_used()
    maxseq = defaultdict(int)
    for i in used:
        m = re.match(r"^([A-Z]{2})-([A-Z_]+)-(\d+)$", i)
        if m:
            maxseq[(m.group(1), m.group(2))] = max(maxseq[(m.group(1), m.group(2))], int(m.group(3)))

    def alloc(cc, cat):
        key = (cc.upper(), cat)
        while True:
            maxseq[key] += 1
            n = maxseq[key]
            cand = (f"{cc.upper()}-PERSON-{n:06d}" if cat == "PERSON"
                    else f"{cc.upper()}-{cat}-{n:03d}")
            if cand not in used:
                used.add(cand)
                return cand

    # sample decisions by identity group
    rows = []
    for r in plan:
        cc = r["collision_id"][:2].lower()
        rv = rmap.get((cc, r["collision_id"], r["shadow"].strip()))
        r["_sample"] = rv
        r["_key"] = manual_key(norm_key(r["shadow"]))
        r["_country"] = cc
        rows.append(r)
    groups = defaultdict(list)
    for r in rows:
        groups[(r["_country"], r["_key"])].append(r)

    out = []
    reused_14 = {x["已被使用的建议新ID"] for x in
                 csv.DictReader(open(os.path.join(OUT, "registry_newid_reserved_14.csv"),
                                     encoding="utf-8-sig"))}
    for (cc, key), members in groups.items():
        samples = [m["_sample"] for m in members if m["_sample"]]
        concl = [s["复核结论"] for s in samples]
        # canonical row: prefer approved sample, then first
        canonical = next((m for m in members if m["_sample"] and
                          m["_sample"]["复核结论"] in ("分配", "改类别后分配")), members[0])
        cs = canonical["_sample"]
        approved = any(c in ("分配", "改类别后分配") for c in concl)
        no_assign = bool(concl) and all(c == "不分配" for c in concl)
        reuse_defer = any(s.get("建议新ID是否曾登记", "").startswith("已登记") for s in samples)
        if approved:
            status = "approved_sample"
        elif no_assign:
            status = "no_assign"
        elif reuse_defer:
            status = "pending_realloc"
        elif samples:
            status = "defer"
        else:
            status = "pending_review"

        cat = None
        if cs:
            m = re.search(r"\b([A-Z]{2,}(?:_[A-Z]+)?)\b", cs.get("类别建议") or "")
            if m and m.group(1) in VALID_CATS:
                cat = m.group(1)
        if not cat:
            m = re.match(r"^[A-Z]{2}-([A-Z_]+)-", canonical.get("new_id") or "")
            cat = m.group(1) if m else "GOV"
        country = cc
        if cs:
            c = (cs.get("实体国别建议") or "").strip().lower()
            if re.fullmatch(r"[a-z]{2}", c):
                country = c
        new_id = ""
        if status in ("approved_sample", "pending_realloc", "pending_review"):
            new_id = alloc(country, cat)
        # members share identity
        for m in members:
            is_canon = m is canonical
            mstatus = status
            if not is_canon and status in ("approved_sample", "pending_realloc", "pending_review"):
                mstatus = "same_identity"
            out.append({
                "status": mstatus,
                "identity_key": key,
                "country": country,
                "collision_id": m["collision_id"],
                "owner": m["owner"],
                "shadow": m["shadow"],
                "category": cat,
                "new_id": new_id if is_canon else "",
                "same_identity_new_id": "" if is_canon else new_id,
                "sample_seq": (m["_sample"] or {}).get("复核序号", ""),
                "sample_conclusion": (m["_sample"] or {}).get("复核结论", ""),
                "sample_note": (m["_sample"] or {}).get("备注", ""),
                "old_suggested": m.get("new_id", ""),
            })

    # validate
    used_after = set()
    bad = []
    for r in out:
        if r["new_id"]:
            if r["new_id"] in used_after or r["new_id"] in reused_14:
                bad.append(r["new_id"])
            used_after.add(r["new_id"])
    summary = {
        "rows": len(out),
        "identities": len(groups),
        "status": dict(Counter(r["status"] for r in out)),
        "new_ids_allocated": len(used_after),
        "reused_reserved_14": sorted(set(bad)),
        "sample_rows": len(review),
        "sample_conclusions": dict(Counter(r["复核结论"] for r in review)),
    }
    with open(os.path.join(OUT, "registry_newid_plan_v3.csv"), "w",
              encoding="utf-8-sig", newline="") as fh:
        fields = ["status", "identity_key", "country", "collision_id", "owner",
                  "shadow", "category", "new_id", "same_identity_new_id",
                  "sample_seq", "sample_conclusion", "sample_note", "old_suggested"]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(out)
    with open(os.path.join(OUT, "registry_newid_plan_v3_summary.json"), "w",
              encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("plan ->", os.path.join(OUT, "registry_newid_plan_v3.csv"))


if __name__ == "__main__":
    main()

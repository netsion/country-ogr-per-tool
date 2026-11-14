# -*- coding: utf-8 -*-
"""v5 plan for the 826 reviewed rows.

- approved same-country: new ID in source country
- approved cross-country with target dataset: new ID in target country
- approved cross-country without target dataset: defer_no_dataset
- no_assign/defer preserved
All IDs allocated from ever_used incl. registry/history/profiles/refs.
"""
import csv, glob, json, os, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT

REVIEW = os.path.join(BASE, "outputs/registry826_20261113/registry_newid_pending826_reviewed.csv")
VALID = {"ACAD","CORP","FIN","GOV","MEDIA","MIL","NGO","PARTY","SOE","INTL"}

def cc_of(s):
    m = re.match(r"^([A-Za-z]{2})\b", (s or "").strip())
    return m.group(1).lower() if m else ""

def cat_of(s):
    m = re.search(r"\b([A-Z]{2,})\b", s or "")
    return m.group(1) if m and m.group(1) in VALID else ""

def main():
    rows = list(csv.DictReader(open(REVIEW, encoding="utf-8-sig")))
    # ever_used
    used = set()
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/id_registry.json")):
        d = json.load(open(f, encoding="utf-8"))
        for key, idk in [("registry","org_id"),("person_registry","person_id"),
                         ("deprecated_registry","org_id"),("deprecated_person_registry","person_id")]:
            for e in d.get(key) or []:
                if e.get(idk): used.add(e[idk])
        for e in d.get("registry") or []:
            if e.get("person_id"): used.add(e["person_id"])
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8"))
        if d.get("person_id"): used.add(d["person_id"])
        for w in d.get("work_experience") or []:
            if w.get("org_id"): used.add(w["org_id"])
        for x in d.get("person_relationships") or []:
            if x.get("person_id"): used.add(x["person_id"])
        for x in d.get("family_members") or []:
            if x.get("person_id"): used.add(x["person_id"])
        for x in d.get("org_ids") or []:
            if x: used.add(x)
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8"))
        if d.get("org_id"): used.add(d["org_id"])
        for x in d.get("related_entities") or []:
            if x.get("org_id"): used.add(x["org_id"])
        for x in d.get("key_people") or []:
            if x.get("person_id"): used.add(x["person_id"])
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/_name_index.json")):
        try: d = json.load(open(f, encoding="utf-8"))
        except Exception: continue
        for v in d.values():
            if isinstance(v, str) and re.match(r"^[A-Z]{2}-(PERSON|[A-Z_]+)-\d+$", v): used.add(v)
    maxseq = defaultdict(int)
    for i in used:
        m = re.match(r"^([A-Z]{2})-([A-Z_]+)-(\d+)$", i)
        if m: maxseq[(m.group(1), m.group(2))] = max(maxseq[(m.group(1), m.group(2))], int(m.group(3)))
    def alloc(cc, cat):
        key = (cc.upper(), cat)
        while True:
            maxseq[key] += 1; n = maxseq[key]
            cand = f"{cc.upper()}-PERSON-{n:06d}" if cat == "PERSON" else f"{cc.upper()}-{cat}-{n:03d}"
            if cand not in used:
                used.add(cand); return cand

    out = []
    for seq, r in enumerate(rows, 1):
        concl = r["复核结论"]
        src = r["国家"].lower()
        target = cc_of(r.get("建议国别")) or src
        cat = cat_of(r.get("建议类别")) or r["计划类别"]
        status = "defer"; new_id = ""; note = ""
        if concl == "不分配":
            status = "no_assign"
        elif concl == "挂起":
            status = "defer"
        else:
            if target != src and not os.path.isdir(os.path.join(BASE, "output", target)):
                status = "defer_no_dataset"
                note = f"目标国 {target} 未采集"
            else:
                status = "approved_sample"
                new_id = alloc(target, cat)
        out.append({"status": status, "source_country": src, "target_country": target,
                    "collision_id": r["冲突ID"], "owner": r["现画像"],
                    "shadow": r["影子名称"], "plan_category": r["计划类别"],
                    "final_category": cat, "new_id": new_id,
                    "conclusion": concl, "seq": seq,
                    "note": (r.get("备注") or "") + (("；" + note) if note else ""),
                    "ref_count": r.get("引用数", "")})
    fields = list(out[0].keys())
    p = os.path.join(OUT, "registry_newid_plan_v5_826.csv")
    with open(p, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(out)
    summary = {"rows": len(out), "status": dict(Counter(r["status"] for r in out)),
               "new_ids": sum(1 for r in out if r["new_id"]),
               "by_target": {f"{k[0]}:{k[1]}": v for k, v in
                             Counter((r["target_country"], r["status"]) for r in out).items()}}
    json.dump(summary, open(os.path.join(OUT, "registry_newid_plan_v5_826_summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("plan ->", p)

if __name__ == "__main__":
    main()

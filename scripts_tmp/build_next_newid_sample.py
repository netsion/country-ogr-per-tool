# -*- coding: utf-8 -*-
"""Next 80-row sample from v3 pending_review rows (20 each KR/MX/NZ/JP)."""
import csv, glob, json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, match, sig

CC_NAMES = {
    "kr": ["韩国", "korea"], "mx": ["墨西哥", "mexico"], "nz": ["新西兰", "new zealand"],
    "jp": ["日本", "japan"], "cn": ["中国", "china", "清华", "tsinghua"],
    "us": ["美国", "united states"], "vn": ["越南", "vietnam"],
}

def ref_name(item, kind):
    keys = (["organization", "org_name", "organization_en"] if kind == "org"
            else ["person_name", "name"])
    for k in keys:
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""

def main():
    rows = [r for r in csv.DictReader(open(os.path.join(OUT, "registry_newid_plan_v3.csv"), encoding="utf-8-sig"))
            if r["status"] == "pending_review"]
    # profiles/owner sig
    owner = {}
    for kind, pat, idk in [("org", "output/[a-z][a-z]/20*/orgs/*.json", "org_id"),
                           ("person", "output/[a-z][a-z]/20*/persons/*.json", "person_id")]:
        for f in glob.glob(os.path.join(BASE, pat)):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8")); i = d.get(idk)
            if not i:
                continue
            if kind == "org":
                bi = d.get("basic_info") or {}
                vals = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")] + (bi.get("aliases") or [])
            else:
                vals = [d.get("name"), d.get("name_en"), d.get("name_zh")] + (d.get("aliases") or [])
            c = set()
            for v in vals:
                c |= sig(v)[0]
            owner[(kind, i)] = c
    by_cid = defaultdict(list)
    for i, r in enumerate(rows):
        by_cid[r["collision_id"]].append(i)
    refs = Counter()
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        for arr, kind in [("work_experience", "org"), ("person_relationships", "person"), ("family_members", "person")]:
            for item in d.get(arr) or []:
                cid = item.get("org_id") if kind == "org" else item.get("person_id")
                if cid not in by_cid:
                    continue
                nm = ref_name(item, kind)
                if not nm or match(sig(nm), (owner.get((kind, cid), set()), [])):
                    continue
                hits = [i for i in by_cid[cid] if match(sig(nm), (sig(rows[i]["shadow"])[0], []))]
                if len(hits) == 1:
                    refs[hits[0]] += 1
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        for arr, kind in [("key_people", "person"), ("related_entities", "org")]:
            for item in d.get(arr) or []:
                cid = item.get("person_id") if kind == "person" else item.get("org_id")
                if cid not in by_cid:
                    continue
                nm = ref_name(item, kind)
                if not nm or match(sig(nm), (owner.get((kind, cid), set()), [])):
                    continue
                hits = [i for i in by_cid[cid] if match(sig(nm), (sig(rows[i]["shadow"])[0], []))]
                if len(hits) == 1:
                    refs[hits[0]] += 1
    out = []
    for cc in ("kr", "mx", "nz", "jp"):
        cand = [i for i, r in enumerate(rows) if r["collision_id"][:2].lower() == cc]
        cand.sort(key=lambda i: (-refs[i], rows[i]["new_id"]))
        for i in cand[:20]:
            r = rows[i]; hints = []
            low = r["shadow"].lower()
            for occ, names in CC_NAMES.items():
                if occ != cc and any(n.lower() in low for n in names):
                    hints.append(f"含他国名:{occ}")
            if refs[i] == 0:
                hints.append("无引用")
            out.append({"国家": cc.upper(), "冲突ID": r["collision_id"], "现画像": r["owner"],
                        "影子名称": r["shadow"], "计划类别": r["category"], "建议新ID": r["new_id"],
                        "引用数": refs[i], "风险提示": ";".join(hints),
                        "复核结论": "", "备注": ""})
    p = os.path.join(OUT, "registry_newid_sample_80_next.csv")
    with open(p, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    print("rows", len(out), "with refs", sum(1 for r in out if r["引用数"] > 0),
          "hints", sum(1 for r in out if r["风险提示"]))
    print(p)

if __name__ == "__main__":
    main()

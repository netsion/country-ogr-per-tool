# -*- coding: utf-8 -*-
"""v4 plan for next 80 reviewed rows: ever-used incl. refs + review decisions."""
import csv, glob, json, os, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT

REVIEW = os.path.join(OUT, "registry_newid_sample_80_next_reviewed.csv")
VALID = {"ACAD","CORP","FIN","GOV","MEDIA","MIL","NGO","PARTY","SOE","INTL"}

def norm_key(s):
    return re.sub(r"[\s\.\,\-\'’`&·:：/\\|（）()\[\]【】]+", "", (s or "").lower())

def main():
    rows = list(csv.DictReader(open(REVIEW, encoding="utf-8-sig")))
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
        key=(cc.upper(),cat)
        while True:
            maxseq[key]+=1; n=maxseq[key]
            cand=f"{cc.upper()}-PERSON-{n:06d}" if cat=="PERSON" else f"{cc.upper()}-{cat}-{n:03d}"
            if cand not in used:
                used.add(cand); return cand

    out=[]; groups={}
    for r in rows:
        concl=r["复核结论"]; cc=r["冲突ID"][:2].lower()
        cat=None
        m=re.search(r"\b([A-Z]{2,})\b", r.get("类别建议") or "")
        if m and m.group(1) in VALID: cat=m.group(1)
        if not cat:
            cat=r["计划类别"]
        country=cc
        cm=re.match(r"^([a-zA-Z]{2})\b", (r.get("国别建议") or "").strip())
        if cm: country=cm.group(1).lower()
        key=(country,norm_key(r["影子名称"]))
        status="defer" if concl=="挂起" else ("no_assign" if concl=="不分配" else "approved_sample")
        new_id=""
        if status=="approved_sample":
            if key in groups:
                status="same_identity"; new_id=groups[key]
            else:
                new_id=alloc(country,cat); groups[key]=new_id
        out.append({"status":status,"country":country,"collision_id":r["冲突ID"],
                    "owner":r["现画像"],"shadow":r["影子名称"],"category":cat,
                    "new_id":new_id,"same_identity_new_id":new_id if status=="same_identity" else "",
                    "sample_seq":r["复核序号"],"conclusion":concl,"note":r["备注"]})
    fields=list(out[0].keys())
    p=os.path.join(OUT,"registry_newid_plan_v4_next80.csv")
    with open(p,"w",encoding="utf-8-sig",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=fields); w.writeheader(); w.writerows(out)
    summary={"rows":len(out),"status":dict(Counter(r["status"] for r in out)),
             "new_ids":sum(1 for r in out if r["new_id"] and r["status"]=="approved_sample"),
             "identities":len(groups)}
    json.dump(summary,open(os.path.join(OUT,"registry_newid_plan_v4_next80_summary.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    for r in out:
        if r["new_id"]: print(r["sample_seq"],r["collision_id"],r["shadow"],'->',r["new_id"],r["status"])
if __name__=="__main__": main()

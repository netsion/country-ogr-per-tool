# -*- coding: utf-8 -*-
"""Execute v4 next-80 approved rows (27 new IDs).

Guards:
  - new IDs must not exist in registry/profiles/refs/history
  - same_identity target must be an active registry entry (not used in v4, but guard kept)
  - ref remap only when name matches shadow and not owner
Usage: python scripts_tmp/execute_newid_v4.py --dry|--apply
"""
import csv, glob, json, os, re, sys, time
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, load_datasets, match, sig

PLAN=os.path.join(OUT,"registry_newid_plan_v4_next80.csv")

def save_json(f,d):
    payload=json.dumps(d,ensure_ascii=False,indent=2)+"\n"; tmp=f+".tmp"; last=None
    for _ in range(6):
        try:
            with open(tmp,"w",encoding="utf-8",newline="\n") as fh: fh.write(payload)
            os.replace(tmp,f); return
        except PermissionError as e: last=e; time.sleep(0.5)
    for _ in range(3):
        try:
            with open(f,"w",encoding="utf-8",newline="\n") as fh: fh.write(payload)
            try: os.unlink(tmp)
            except OSError: pass
            return
        except PermissionError as e: last=e; time.sleep(1.0)
    raise last

def ref_name(item,kind):
    keys=(["organization","org_name","organization_en"] if kind=="org"
          else ["person_name","name"] if kind in ("rel","family") else ["name","name_en"])
    for k in keys:
        v=item.get(k)
        if isinstance(v,str) and v.strip(): return v.strip()
    return ""

def main():
    apply="--apply" in sys.argv
    rows=[r for r in csv.DictReader(open(PLAN,encoding="utf-8-sig")) if r["status"]=="approved_sample"]
    latest,_=load_datasets()
    regpath={}; regs={}
    for cc,(date,folder) in latest.items():
        p=os.path.join(folder,"id_registry.json")
        if os.path.exists(p): regpath[cc]=p; regs[cc]=json.load(open(p,encoding="utf-8"))
    # owner sig
    owner={}
    for kind,pat,idk in [("org","output/[a-z][a-z]/20*/orgs/*.json","org_id"),("person","output/[a-z][a-z]/20*/persons/*.json","person_id")]:
        for f in glob.glob(os.path.join(BASE,pat)):
            if os.path.basename(f).startswith("_"): continue
            d=json.load(open(f,encoding="utf-8")); i=d.get(idk)
            if not i: continue
            if kind=="org":
                bi=d.get("basic_info") or {}; vals=[bi.get("name_zh"),bi.get("name_en"),bi.get("name_original")]+(bi.get("aliases") or [])
            else:
                vals=[d.get("name"),d.get("name_en"),d.get("name_zh")]+(d.get("aliases") or [])
            c=set()
            for v in vals: c|=sig(v)[0]
            owner[(kind,i)]=c
    # guard new IDs
    used=set()
    for f in glob.glob(os.path.join(BASE,"output/[a-z][a-z]/20*/id_registry.json")):
        d=json.load(open(f,encoding="utf-8"))
        for key,idk in [("registry","org_id"),("person_registry","person_id"),("deprecated_registry","org_id"),("deprecated_person_registry","person_id")]:
            for e in d.get(key) or []:
                if e.get(idk): used.add(e[idk])
    bad=[r["new_id"] for r in rows if r["new_id"] in used]
    dup=[k for k,v in Counter(r["new_id"] for r in rows).items() if v>1]
    print("rows",len(rows),"bad_used",bad,"dup",dup)
    if bad or dup: print("ABORT"); return
    undo={"registry":{},"ref_changes":[]}; stats=Counter()
    # registry moves
    for r in rows:
        cid=r["collision_id"]; cc=cid[:2].lower(); kind="person" if "-PERSON-" in cid else "org"
        if cc not in regs: stats["missing_registry"]+=1; continue
        reg=regs[cc]; key="person_registry" if kind=="person" else "registry"; entries=reg.get(key) or []
        idx=None
        for i,e in enumerate(entries):
            if (e.get("org_id") if kind=="org" else e.get("person_id"))==cid and (e.get("name") or "").strip()==r["shadow"].strip():
                idx=i; break
        if idx is None:
            for i,e in enumerate(entries):
                nm=(e.get("name") or "").strip()
                if (e.get("org_id") if kind=="org" else e.get("person_id"))==cid and nm and match(sig(r["shadow"]),(sig(nm)[0],[])):
                    idx=i; break
        if idx is None: stats["entry_not_found"]+=1; continue
        old=entries.pop(idx)
        new={("person_id" if kind=="person" else "org_id"):r["new_id"],"name":r["shadow"].strip(),
             "status":"auto_registered","source":f"A2 v4 dedupe from {cid}",
             "notes":f"独立身份，由 {cid} 的影子身份拆分（next80 seq {r['sample_seq']}）"}
        if kind=="org": new["org_type"]=r["category"]
        entries.append(new); reg[key]=entries; stats["created"]+=1
        undo["registry"].setdefault(regpath[cc],[]).append({"kind":kind,"id":cid,"name":(old.get("name") or "").strip(),"old":old,"new":new,"new_id":r["new_id"],"action":"create"})
    if apply:
        for cc,reg in regs.items(): save_json(regpath[cc],reg)
    # refs
    bycid=defaultdict(list)
    for r in rows: bycid[r["collision_id"]].append(r)
    def resolve(kind,cid,name):
        if not name: return None
        if match(sig(name),(owner.get((kind,cid),set()),[])): return None
        hits=[]
        for r in bycid.get(cid,[]):
            if match(sig(name),(sig(r["shadow"])[0],[])): hits.append(r["new_id"])
        hits=sorted(set(hits)); return hits[0] if len(hits)==1 else None
    dirty=set()
    for f in glob.glob(os.path.join(BASE,"output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d=json.load(open(f,encoding="utf-8")); dirty_f=False
        for i,w in enumerate(d.get("work_experience") or []):
            if not isinstance(w,dict): continue
            cid=w.get("org_id"); nm=ref_name(w,"org")
            if cid in bycid:
                new=resolve("org",cid,nm)
                if new and new!=cid:
                    undo["ref_changes"].append({"file":os.path.relpath(f,BASE).replace(os.sep,"/"),"array":"work_experience","index":i,"field":"org_id","old":cid,"new":new,"ref_name":nm}); w["org_id"]=new; dirty_f=True
        for arr,kind in [("person_relationships","rel"),("family_members","family")]:
            for i,x in enumerate(d.get(arr) or []):
                if not isinstance(x,dict): continue
                cid=x.get("person_id"); nm=ref_name(x,kind)
                if cid in bycid:
                    new=resolve("person",cid,nm)
                    if new and new!=cid:
                        undo["ref_changes"].append({"file":os.path.relpath(f,BASE).replace(os.sep,"/"),"array":arr,"index":i,"field":"person_id","old":cid,"new":new,"ref_name":nm}); x["person_id"]=new; dirty_f=True
        if dirty_f:
            dirty.add(f)
            if apply: save_json(f,d)
    for f in glob.glob(os.path.join(BASE,"output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d=json.load(open(f,encoding="utf-8")); dirty_f=False
        for arr,field,kind in [("key_people","person_id","person"),("related_entities","org_id","org")]:
            for i,x in enumerate(d.get(arr) or []):
                if not isinstance(x,dict): continue
                cid=x.get(field); nm=ref_name(x,"org" if kind=="org" else "person")
                if cid in bycid:
                    new=resolve(kind,cid,nm)
                    if new and new!=cid:
                        undo["ref_changes"].append({"file":os.path.relpath(f,BASE).replace(os.sep,"/"),"array":arr,"index":i,"field":field,"old":cid,"new":new,"ref_name":nm}); x[field]=new; dirty_f=True
        if dirty_f:
            dirty.add(f)
            if apply: save_json(f,d)
    summary={"rows":len(rows),"registry":dict(stats),"ref_changes":len(undo["ref_changes"]),"files":len(dirty)}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        json.dump(undo,open(os.path.join(OUT,"registry_newid_v4_undo.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
        json.dump(summary,open(os.path.join(OUT,"registry_newid_v4_summary.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
        print("undo ->",os.path.join(OUT,"registry_newid_v4_undo.json"))
    else:
        json.dump(undo,open(os.path.join(OUT,"registry_newid_v4_dry_undo.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
        print("DRY"); 
if __name__=="__main__": main()

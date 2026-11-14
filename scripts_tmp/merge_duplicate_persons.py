# -*- coding: utf-8 -*-
"""Merge 4 duplicate person profile pairs.

Canonical choices:
  MX-PERSON-000154 <- MX-PERSON-000162
  MX-PERSON-000102 <- MX-PERSON-000114
  MX-PERSON-000126 <- PE-PERSON-000171
  MX-PERSON-000142 <- US-PERSON-000685
"""
import glob, json, os, re, shutil, sys, time
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT

PAIRS = [
    ("MX-PERSON-000154", "MX-PERSON-000162"),
    ("MX-PERSON-000102", "MX-PERSON-000114"),
    ("MX-PERSON-000126", "PE-PERSON-000171"),
    ("MX-PERSON-000142", "US-PERSON-000685"),
]
# stub duplicates: don't merge their work/education arrays (person-name-as-employer stubs)
MERGE_ARRAYS = {
    ("MX-PERSON-000154", "MX-PERSON-000162"): False,
    ("MX-PERSON-000102", "MX-PERSON-000114"): False,
    ("MX-PERSON-000126", "PE-PERSON-000171"): True,
    ("MX-PERSON-000142", "US-PERSON-000685"): True,
}
ARCHIVE = os.path.join(OUT, "merged_person_profiles")


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


def norm(s):
    return re.sub(r"[\s\.\,\-\'’`&·:：/\\|（）()\[\]【】]+", "", str(s or "").lower())


def key_of(arr, x):
    if arr == "work_experience":
        return (norm(x.get("organization")), norm(x.get("position")), x.get("start_date") or "")
    if arr == "education":
        return (norm(x.get("institution")), x.get("degree") or "", x.get("end_date") or "")
    if arr == "person_relationships":
        return (x.get("person_id") or norm(x.get("person_name")), x.get("relationship_type") or "")
    if arr == "family_members":
        return (x.get("person_id") or norm(x.get("name")), x.get("relation") or "")
    if arr == "social_accounts":
        return (x.get("platform") or "", norm(x.get("url") or x.get("account_name")))
    return json.dumps(x, ensure_ascii=False, sort_keys=True)


def find_file(pid):
    fs = glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons", pid + ".json"))
    return fs[0] if fs else None


def main():
    apply = "--apply" in sys.argv
    os.makedirs(ARCHIVE, exist_ok=True)
    undo = {"profiles": [], "ref_changes": [], "registry": [], "index": []}
    stats = Counter()

    for cid, did in PAIRS:
        cf, df = find_file(cid), find_file(did)
        if not cf or not df:
            stats["missing_file"] += 1; continue
        c = json.load(open(cf, encoding="utf-8"))
        d = json.load(open(df, encoding="utf-8"))
        before = json.loads(json.dumps(c))
        added = []

        # scalars
        for k in ["birth_date", "birth_place", "gender", "nationality", "wikidata_qid",
                  "name_en"]:
            if not c.get(k) and d.get(k):
                c[k] = d[k]; added.append(k)
        if len(d.get("biography_summary") or "") > len(c.get("biography_summary") or ""):
            c["biography_summary"] = d["biography_summary"]; added.append("biography_summary")

        # aliases
        aliases = list(c.get("aliases") or [])
        for v in [d.get("name"), d.get("name_zh"), d.get("name_en")] + (d.get("aliases") or []):
            if v and v not in aliases and v not in (c.get("name"), c.get("name_zh"), c.get("name_en")):
                aliases.append(v); added.append("alias:" + str(v))
        c["aliases"] = aliases

        # lists union (skip stub duplicates' arrays)
        if MERGE_ARRAYS.get((cid, did), True):
            for arr in ["current_positions", "contacts", "work_experience", "education",
                        "person_relationships", "family_members", "social_accounts",
                        "major_achievements", "political_stances"]:
                vals = list(c.get(arr) or [])
                if all(isinstance(x, str) for x in vals) and arr == "current_positions":
                    seen = {str(x).strip() for x in vals}
                    for x in d.get(arr) or []:
                        if isinstance(x, str) and x.strip() not in seen:
                            vals.append(x); seen.add(x.strip()); added.append(arr)
                    c[arr] = vals
                    continue
                seen = {key_of(arr, x) for x in vals if isinstance(x, dict)}
                for x in d.get(arr) or []:
                    if not isinstance(x, dict):
                        continue
                    k = key_of(arr, x)
                    if k not in seen:
                        vals.append(x); seen.add(k); added.append(arr)
                c[arr] = vals

        if not (c.get("profile") or {}).get("local_path") and (d.get("profile") or {}).get("local_path"):
            c["profile"] = d["profile"]; added.append("profile")
        c.setdefault("collection_meta", {})
        c["collection_meta"]["notes"] = ((c["collection_meta"].get("notes") or "")
                                         + f"；合并重复档案 {did}").strip("；")

        # refs
        for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            x = json.load(open(f, encoding="utf-8"))
            dirty = False
            for arr in ["person_relationships", "family_members"]:
                for i, item in enumerate(x.get(arr) or []):
                    if isinstance(item, dict) and item.get("person_id") == did:
                        undo["ref_changes"].append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                                    "array": arr, "index": i, "field": "person_id",
                                                    "old": did, "new": cid,
                                                    "ref_name": item.get("person_name") or item.get("name")})
                        item["person_id"] = cid; dirty = True; stats["refs"] += 1
            if apply and dirty:
                save_json(f, x)
        for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            x = json.load(open(f, encoding="utf-8"))
            dirty = False
            for i, item in enumerate(x.get("key_people") or []):
                if isinstance(item, dict) and item.get("person_id") == did:
                    undo["ref_changes"].append({"file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                                                "array": "key_people", "index": i, "field": "person_id",
                                                "old": did, "new": cid, "ref_name": item.get("name")})
                    item["person_id"] = cid; dirty = True; stats["refs"] += 1
            if apply and dirty:
                save_json(f, x)

        # registry
        cc = did[:2].lower()
        rp = glob.glob(os.path.join(BASE, f"output/{cc}/20*/id_registry.json"))
        if rp:
            rp = rp[-1]
            reg = json.load(open(rp, encoding="utf-8"))
            ents = reg.get("person_registry") or []
            keep = []
            for e in ents:
                if e.get("person_id") == did:
                    e["status"] = "merged"; e["merged_into"] = cid
                    e["deprecated_reason"] = "duplicate person profile merge"
                    reg.setdefault("deprecated_person_registry", []).append(e)
                    undo["registry"].append({"file": rp, "entry": json.loads(json.dumps(e))})
                    stats["registry_merged"] += 1
                else:
                    keep.append(e)
            reg["person_registry"] = keep
            if apply:
                save_json(rp, reg)

        # index
        ip = os.path.join(os.path.dirname(df), "_index.json")
        if os.path.exists(ip):
            idx = json.load(open(ip, encoding="utf-8"))
            old = [p for p in idx.get("profiles") or [] if p.get("person_id") == did]
            idx["profiles"] = [p for p in idx.get("profiles") or [] if p.get("person_id") != did]
            idx["total_profiles"] = len(idx["profiles"])
            undo["index"].append({"file": ip, "removed": old})
            if apply:
                save_json(ip, idx)
            stats["index_removed"] += len(old)

        # archive duplicate profile
        undo["profiles"].append({"canonical": cid, "duplicate": did,
                                 "canonical_before": before, "canonical_after": c,
                                 "duplicate_file": df, "duplicate_data": d})
        if apply:
            save_json(cf, c)
            shutil.move(df, os.path.join(ARCHIVE, did + ".json"))
            stats["profiles_merged"] += 1
        print(cid, "<-", did, "added", dict(Counter(added)), "refs", stats["refs"])

    summary = {"pairs": len(PAIRS), "stats": dict(stats),
               "added": {}, "ref_changes": len(undo["ref_changes"])}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if apply:
        json.dump(undo, open(os.path.join(OUT, "merge_duplicate_persons_undo.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("undo ->", os.path.join(OUT, "merge_duplicate_persons_undo.json"))
    else:
        json.dump(undo, open(os.path.join(OUT, "merge_duplicate_persons_dry_undo.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("DRY")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""P1 read-only audit: index sync, duplicate QIDs, name-index residue."""
import glob, json, os, re, sys, unicodedata
from collections import Counter, defaultdict

BASE = "D:/ai-workspace/apec-osint-tool"
OUT = os.path.join(BASE, "output/_id_audit")

def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[\s\.\,\-\'’`&·:：/\|（）()\[\]【】]+", "", s)

def profile_person_name(p):
    vals = [p.get("name"), p.get("name_en"), p.get("name_zh"), p.get("name_original")]
    bi = p.get("basic_info") or {}
    vals += [bi.get("name_en"), bi.get("name_zh"), bi.get("name_original")]
    for v in vals:
        if isinstance(v, str) and v.strip():
            return v.strip()
    return p.get("person_id", "")

def profile_org_name(p):
    bi = p.get("basic_info") or {}
    for v in [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original"), p.get("name")]:
        if isinstance(v, str) and v.strip():
            return v.strip()
    return p.get("org_id", "")

def org_index_entry(p):
    bi = p.get("basic_info") or {}
    cm = p.get("collection_meta") or {}
    zh = bi.get("name_zh")
    en = bi.get("name_en") or bi.get("name_original")
    name = zh if zh and en and zh == en else (f"{zh} ({en})" if zh and en else (zh or en or p.get("org_id", "")))
    return {"org_id": p.get("org_id"), "name": name,
            "category": bi.get("org_type"), "subcategory": bi.get("org_subtype"),
            "completeness": cm.get("completeness_score")}

def person_index_entry(p):
    bi = p.get("basic_info") or {}
    return {"person_id": p.get("person_id"),
            "wikidata_qid": p.get("wikidata_qid") or bi.get("wikidata_qid"),
            "name_en": p.get("name_en") or bi.get("name_en"),
            "name_zh": p.get("name_zh") or bi.get("name_zh"),
            "gender": p.get("gender") or bi.get("gender"),
            "importance_level": p.get("importance_level") or bi.get("importance_level"),
            "current_title": p.get("current_title") or bi.get("current_title"),
            "completeness_score": (p.get("collection_meta") or {}).get("completeness_score"),
            "file": p.get("person_id", "") + ".json"}

def main():
    index_plan = {"org": [], "person": []}
    profiles_person = []
    profiles_org = []
    name_index_stats = []
    for folder in sorted(glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*"))):
        if not os.path.isdir(folder): continue
        cc = os.path.basename(os.path.dirname(folder)); date = os.path.basename(folder)
        for kind, sub, entry_fn, idkey in [
            ("person", "persons", person_index_entry, "person_id"),
            ("org", "orgs", org_index_entry, "org_id"),
        ]:
            d = os.path.join(folder, sub)
            if not os.path.isdir(d): continue
            files = {}
            for f in glob.glob(os.path.join(d, "*.json")):
                if os.path.basename(f).startswith("_"): continue
                try: p = json.load(open(f, encoding="utf-8"))
                except Exception: continue
                pid = p.get(idkey)
                if pid: files[pid] = p
                if kind == "person": profiles_person.append((cc, date, p))
                else: profiles_org.append((cc, date, p))
            idxp = os.path.join(d, "_index.json")
            if not os.path.exists(idxp): continue
            idx = json.load(open(idxp, encoding="utf-8"))
            entries = idx.get("profiles") or []
            byid = {}
            for e in entries:
                pid = e.get(idkey)
                if pid: byid.setdefault(pid, []).append(e)
            for pid in sorted(set(files) - set(byid)):
                index_plan[kind].append({"action": "add", "cc": cc, "date": date,
                                         "path": idxp, "id": pid, "entry": entry_fn(files[pid])})
            for pid, es in sorted(byid.items()):
                if pid not in files:
                    index_plan[kind].append({"action": "remove_stale", "cc": cc, "date": date,
                                             "path": idxp, "id": pid, "old": es})
                elif len(es) > 1:
                    index_plan[kind].append({"action": "dedupe_index", "cc": cc, "date": date,
                                             "path": idxp, "id": pid, "old": es})
                else:
                    e = es[0]
                    p = files[pid]
                    if kind == "org":
                        pn = profile_org_name(p)
                        if not norm(e.get("name")) or norm(e.get("name")) != norm(pn):
                            # only flag if the index name doesn't match any profile name
                            vals = [((p.get("basic_info") or {}).get(k)) for k in ("name_zh","name_en","name_original")]
                            if not any(norm(e.get("name")) == norm(v) for v in vals if v):
                                index_plan[kind].append({"action": "fix_name", "cc": cc, "date": date,
                                                         "path": idxp, "id": pid, "old": e,
                                                         "new_name": entry_fn(p)["name"]})
                    else:
                        pn = profile_person_name(p)
                        if not norm(e.get("name_en")) and not norm(e.get("name_zh")):
                            index_plan[kind].append({"action": "fix_name", "cc": cc, "date": date,
                                                     "path": idxp, "id": pid, "old": e,
                                                     "new": entry_fn(p)})
        nip = os.path.join(folder, "_name_index.json")
        if os.path.exists(nip):
            try: ni = json.load(open(nip, encoding="utf-8"))
            except Exception: continue
            name_index_stats.append({
                "cc": cc, "date": date, "keys": len(ni),
                "short": sum(1 for k in ni if len(str(k).strip()) <= 3),
                "single": sum(1 for k in ni if len(str(k).strip()) <= 1),
            })

    # duplicate QID groups
    qgroups = {"person": defaultdict(list), "org": defaultdict(list)}
    for cc, date, p in profiles_person:
        q = p.get("wikidata_qid") or (p.get("basic_info") or {}).get("wikidata_qid")
        if q: qgroups["person"][q].append((cc, date, p))
    for cc, date, p in profiles_org:
        q = (p.get("basic_info") or {}).get("wikidata_qid")
        if q: qgroups["org"][q].append((cc, date, p))
    dup = {}
    for kind in ("person", "org"):
        rows = []
        for q, vals in sorted(qgroups[kind].items()):
            if len(vals) < 2: continue
            names = []
            for cc, date, p in vals:
                names.append(profile_person_name(p) if kind == "person" else profile_org_name(p))
            same = bool(names) and all(norm(names[0]) == norm(n) for n in names[1:])
            rows.append({"qid": q, "count": len(vals), "same_name": same, "names": names,
                         "ids": [p.get("person_id") if kind == "person" else p.get("org_id") for _,_,p in vals],
                         "locations": [f"{cc}/{date}" for cc,_,_ in vals]})
        dup[kind] = rows

    summary = {
        "index": {k: dict(Counter(x["action"] for x in v)) for k, v in index_plan.items()},
        "qid_dups": {k: {"groups": len(v), "same_name": sum(1 for x in v if x["same_name"]),
                         "different": sum(1 for x in v if not x["same_name"])} for k, v in dup.items()},
        "name_index": {"files": len(name_index_stats), "short": sum(x["short"] for x in name_index_stats),
                       "single": sum(x["single"] for x in name_index_stats)},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    json.dump({"summary": summary, "index_plan": index_plan, "qid_dup

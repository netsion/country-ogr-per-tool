# -*- coding: utf-8 -*-
"""Person disambiguation plan for the 141 person-name org candidates."""
import csv, glob, json, os, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, sig, match

SRC = os.path.join(OUT, "registry826_person_names_141.csv")


def loose(a, b):
    na = re.sub(r"[\s\.\,\-\'’`&·:：/\\|（）()\[\]【】]+", "", (a or "").lower())
    nb = re.sub(r"[\s\.\,\-\'’`&·:：/\\|（）()\[\]【】]+", "", (b or "").lower())
    if not na or not nb:
        return False
    return na == nb or (len(na) >= 4 and len(nb) >= 4 and (na in nb or nb in na))


def main():
    rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
    # person profiles
    prof = {}
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        pid = d.get("person_id")
        if not pid:
            continue
        vals = [d.get("name"), d.get("name_en"), d.get("name_zh")] + (d.get("aliases") or [])
        c = set()
        for v in vals:
            c |= sig(v)[0]
        prof[pid] = {"name": d.get("name"), "name_zh": d.get("name_zh"),
                     "qid": d.get("wikidata_qid"), "birth": d.get("birth_date"),
                     "pos": (d.get("current_positions") or [])[:3], "sig": c}
    # org profiles (owner names)
    orgs = {}
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        oid = d.get("org_id")
        if oid:
            bi = d.get("basic_info") or {}
            orgs[oid] = {"name_zh": bi.get("name_zh"), "name_orig": bi.get("name_original"),
                         "name_en": bi.get("name_en")}
    # refs
    by_cid = defaultdict(list)
    for r in rows:
        by_cid[r["冲突ID"]].append(r)
    refs = defaultdict(list)
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        for arr, field, nk in [("work_experience", "org_id", "organization"),
                               ("person_relationships", "person_id", "person_name"),
                               ("family_members", "person_id", "name")]:
            for i, x in enumerate(d.get(arr) or []):
                if not isinstance(x, dict):
                    continue
                cid = x.get(field)
                if cid not in by_cid:
                    continue
                nm = x.get(nk) or x.get("name") or ""
                for r in by_cid[cid]:
                    if nm and (match(sig(nm), (sig(r["影子名称"])[0], [])) or loose(nm, r["影子名称"])):
                        refs[r["原清单行"]].append({
                            "file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                            "array": arr, "index": i, "field": field, "ref_name": nm,
                            "context": json.dumps(x, ensure_ascii=False)[:600]})
                        break
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        for arr, field, nk in [("key_people", "person_id", "name"),
                               ("related_entities", "org_id", "org_name")]:
            for i, x in enumerate(d.get(arr) or []):
                if not isinstance(x, dict):
                    continue
                cid = x.get(field)
                if cid not in by_cid:
                    continue
                nm = x.get(nk) or x.get("name") or ""
                for r in by_cid[cid]:
                    if nm and (match(sig(nm), (sig(r["影子名称"])[0], [])) or loose(nm, r["影子名称"])):
                        refs[r["原清单行"]].append({
                            "file": os.path.relpath(f, BASE).replace(os.sep, "/"),
                            "array": arr, "index": i, "field": field, "ref_name": nm,
                            "context": json.dumps(x, ensure_ascii=False)[:600]})
                        break

    plan = []
    cand_rows = []
    ref_rows = []
    for r in rows:
        cands = list(dict.fromkeys(re.findall(r"[A-Z]{2}-PERSON-\d{6}", r["人物候选"])))
        cinfo = [(c, prof.get(c, {})) for c in cands]
        # duplicate profile groups among candidates
        keys = Counter((p.get("name") or c) for c, p in cinfo)
        dup_group = [k for k, v in keys.items() if v > 1]
        cand_status = ("none" if not cands else "single" if len(cands) == 1
                       else "duplicate_profiles" if dup_group else "multiple_distinct")
        rs = refs.get(r["原清单行"], [])
        types = {x["array"] for x in rs}
        if "work_experience" in types or "related_entities" in types:
            rtype = "org_field"
        elif types:
            rtype = "person_field"
        else:
            rtype = "none"

        action, sug_pid, sug_org = "", "", ""
        if not rs:
            action = "archive_shadow_no_ref"
            note = "无当前引用；从组织 registry 归档该人物影条目，不建组织 ID、不建 person ID"
        elif rtype == "org_field":
            oid = r["冲突ID"]
            o = orgs.get(oid) or {}
            sug_org = f"{o.get('name_zh') or ''} ({o.get('name_orig') or o.get('name_en') or ''})".strip()
            action = "fix_org_text_keep_org_id"
            note = f"引用是组织字段但文本填了人名；organization 改为实际雇主 {sug_org}，保留 org_id={oid}；归档人物影条目"
        else:
            # person field: pick a candidate matching the shadow
            matches = [c for c, p in cinfo if p and (match(sig(r["影子名称"]), (p["sig"], [])) or loose(r["影子名称"], p.get("name")))]
            matches = list(dict.fromkeys(matches))
            if len(matches) == 1:
                sug_pid = matches[0]
                action = "replace_person_id"
                note = f"person_id 由组织 ID 改为人物 {sug_pid}"
            else:
                action = "manual_person_disambiguation"
                note = "人物字段当前指向组织 ID；候选不唯一或未匹配，需人工消歧"
        plan.append({
            "原清单行": r["原清单行"], "国家": r["国家"], "冲突ID": r["冲突ID"],
            "现画像": r["现画像"], "影子名称": r["影子名称"], "引用数": r["引用数"],
            "引用字段类型": rtype, "引用位置": " | ".join(
                f"{x['file']}#{x['array']}[{x['index']}].{x['field']}" for x in rs),
            "引用上下文": " | ".join(x["context"] for x in rs),
            "人物候选数": len(cands), "人物候选": ", ".join(cands),
            "候选状态": cand_status,
            "重复档案提示": "; ".join(dup_group) if dup_group else "",
            "建议动作": action, "建议person_id": sug_pid,
            "建议organization_text": sug_org,
            "备注": note + "；" + r["复核理由"],
        })
        for c, p in cinfo:
            cand_rows.append({
                "原清单行": r["原清单行"], "候选person_id": c,
                "name": p.get("name"), "name_zh": p.get("name_zh"),
                "wikidata_qid": p.get("qid"), "birth_date": p.get("birth"),
                "current_positions": " / ".join(p.get("pos") or []),
                "重复候选组": ("是：" + ", ".join(dup_group)) if dup_group else "",
            })
        for x in rs:
            ref_rows.append({"原清单行": r["原清单行"], **x, "建议动作": action})

    p1 = os.path.join(OUT, "registry826_person_disambiguation_141.csv")
    with open(p1, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(plan[0].keys())); w.writeheader(); w.writerows(plan)
    p2 = os.path.join(OUT, "registry826_person_candidates.csv")
    with open(p2, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cand_rows[0].keys())); w.writeheader(); w.writerows(cand_rows)
    p3 = os.path.join(OUT, "registry826_person_refs.csv")
    with open(p3, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ref_rows[0].keys()) if ref_rows else
                           ["原清单行", "file", "array", "index", "field", "ref_name", "context", "建议动作"])
        w.writeheader(); w.writerows(ref_rows)
    summary = {
        "rows": len(plan), "actions": dict(Counter(r["建议动作"] for r in plan)),
        "refs": len(ref_rows), "candidates": len(cand_rows),
        "candidate_status": dict(Counter(r["候选状态"] for r in plan)),
        "candidate_rows": dict(Counter(r["人物候选数"] for r in plan)),
        "duplicate_candidate_rows": sum(1 for r in plan if r["重复档案提示"]),
    }
    json.dump(summary, open(os.path.join(OUT, "registry826_person_disambiguation_summary.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("->", p1); print("->", p2); print("->", p3)


if __name__ == "__main__":
    main()

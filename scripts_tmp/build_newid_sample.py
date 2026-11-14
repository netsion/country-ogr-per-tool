# -*- coding: utf-8 -*-
"""Sample 80 rows (20 each KR/MX/NZ/JP) from the v2 new-ID plan for review."""
import csv
import glob
import json
import os
import sys
from collections import defaultdict, Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, match, sig

PLAN = os.path.join(OUT, "registry_dedupe_plan_v2.csv")
CC_NAMES = {
    "kr": ["韩国", "南韩", "korea"], "mx": ["墨西哥", "mexico"],
    "nz": ["新西兰", "new zealand"], "jp": ["日本", "japan"],
    "cn": ["中国", "china", "清华", "tsinghua"], "us": ["美国", "united states"],
    "vn": ["越南", "vietnam"], "sg": ["新加坡", "singapore"],
    "pg": ["巴布亚新几内亚", "papua new guinea"], "id": ["印度尼西亚", "indonesia"],
}


CAT_WORDS = {
    "FIN": ["银行", "bank", "banking", "financial", "保险", "金融", "投资", "证券"],
    "ACAD": ["大学", "学院", "university", "college", "institute", "学校"],
    "MEDIA": ["报", "电视", "媒体", "新闻", "广播", "broadcast", "broadcasting",
              "newspaper", "media", "tv"],
    "CORP": ["公司", "集团", "corporation", "company", "group", "控股", "电信", "电话"],
    "GOV": ["部", "局", "委员会", "政府", "议会", "ministry", "government", "council", "commission"],
    "MIL": ["军", "部队", "army", "navy", "defense", "defence"],
    "PARTY": ["党", "party"],
}


def infer_cat(name):
    low = (name or "").lower()
    for cat, words in CAT_WORDS.items():
        if any(w.lower() in low for w in words):
            return cat
    return ""


def load_profiles():
    orgs, persons = {}, {}
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        oid = d.get("org_id")
        if not oid:
            continue
        bi = d.get("basic_info") or {}
        vals = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")]
        vals += bi.get("aliases") or []
        c = set()
        for v in vals:
            c |= sig(v)[0]
        orgs[oid] = (oid[:2].lower(), c, bi.get("name_zh") or bi.get("name_original"))
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        pid = d.get("person_id")
        if not pid:
            continue
        vals = [d.get("name"), d.get("name_en"), d.get("name_zh")]
        vals += d.get("aliases") or []
        c = set()
        for v in vals:
            c |= sig(v)[0]
        persons[pid] = (pid[:2].lower(), c, d.get("name") or d.get("name_zh"))
    return orgs, persons


def ref_name(item, kind):
    keys = (["organization", "org_name", "organization_en"] if kind == "work"
            else ["org_name", "name"] if kind == "related"
            else ["person_name", "name"] if kind == "rel"
            else ["name", "name_en"])
    for k in keys:
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def main():
    rows = list(csv.DictReader(open(PLAN, encoding="utf-8-sig")))
    by_cid = defaultdict(list)
    for i, r in enumerate(rows):
        by_cid[r["collision_id"]].append(i)
    orgs, persons = load_profiles()
    owner_sig = {}
    for i, v in orgs.items():
        owner_sig[("org", i)] = v[1]
    for i, v in persons.items():
        owner_sig[("person", i)] = v[1]

    refs = Counter()
    # scan refs
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        for kind, arr in [("work", "work_experience"), ("rel", "person_relationships"),
                          ("family", "family_members")]:
            for item in d.get(arr) or []:
                if not isinstance(item, dict):
                    continue
                cid = item.get("org_id") if kind == "work" else item.get("person_id")
                if cid not in by_cid:
                    continue
                nm = ref_name(item, kind)
                if not nm:
                    continue
                kind2 = "org" if kind == "work" else "person"
                if match(sig(nm), (owner_sig.get((kind2, cid), set()), [])):
                    continue
                hits = [i for i in by_cid[cid]
                        if match(sig(nm), (sig(rows[i]["shadow"])[0], []))]
                if len(hits) == 1:
                    refs[hits[0]] += 1
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        for kind, arr, field in [("key", "key_people", "person_id"),
                                 ("related", "related_entities", "org_id")]:
            for item in d.get(arr) or []:
                if not isinstance(item, dict):
                    continue
                cid = item.get(field)
                if cid not in by_cid:
                    continue
                nm = ref_name(item, kind)
                if not nm:
                    continue
                kind2 = "person" if kind == "key" else "org"
                if match(sig(nm), (owner_sig.get((kind2, cid), set()), [])):
                    continue
                hits = [i for i in by_cid[cid]
                        if match(sig(nm), (sig(rows[i]["shadow"])[0], []))]
                if len(hits) == 1:
                    refs[hits[0]] += 1

    out = []
    for cc in ("kr", "mx", "nz", "jp"):
        cand = [i for i, r in enumerate(rows) if r["collision_id"][:2].lower() == cc]
        cand.sort(key=lambda i: (-refs[i], rows[i]["status"] != "auto_registered", rows[i]["new_id"]))
        for i in cand[:20]:
            r = rows[i]
            shadow = r["shadow"]
            hints = []
            low = shadow.lower()
            for occ, names in CC_NAMES.items():
                if occ == cc:
                    continue
                if any(n.lower() in low for n in names):
                    hints.append(f"含他国名:{occ}")
            if refs[i] == 0:
                hints.append("无引用")
            if r["action"] != "assign_new_id":
                hints.append(r["action"])
            inf = infer_cat(shadow)
            newcat = r["new_id"].split("-")[1] if r["new_id"] else ""
            if inf and inf != newcat:
                hints.append(f"类别可能应为{inf}")
            out.append({
                "国家": cc.upper(), "冲突ID": r["collision_id"], "现画像": r["owner"],
                "影子名称": shadow, "注册状态": r["status"], "建议新ID": r["new_id"],
                "新ID类别": r["new_id"].split("-")[1] if r["new_id"] else "",
                "引用数": refs[i], "风险提示": ";".join(hints),
                "机器建议": "需确认国别" if any(h.startswith("含他国名") for h in hints)
                            else ("需确认类别" if any(h.startswith("类别可能") for h in hints)
                                  else ("低影响可分配" if refs[i] == 0 else "可分配")),
                "复核结论": "", "备注": "",
            })
    fields = list(out[0].keys()) if out else []
    p = os.path.join(OUT, "registry_newid_sample_80.csv")
    with open(p, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(out)
    print("rows", len(out), "with refs", sum(1 for r in out if r["引用数"] > 0),
          "foreign-hint", sum(1 for r in out if "含他国名" in r["风险提示"]))
    for r in out[:30]:
        print(r)


if __name__ == "__main__":
    main()

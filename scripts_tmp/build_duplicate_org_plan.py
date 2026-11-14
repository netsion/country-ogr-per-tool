# -*- coding: utf-8 -*-
"""Plan for the 19 duplicate organisation identity groups (826 deferrals)."""
import csv, glob, json, os, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT

SRC = os.path.join(OUT, "registry826_duplicate_identities_19.csv")
REVIEW = os.path.join(BASE, "outputs/registry826_20261113/registry_newid_pending826_reviewed.csv")

OVERRIDES = {
    "1": ("驻英国大韩民国大使馆 (Embassy of the Republic of Korea in the UK)", "GOV", "kr",
          "同一使馆的中/韩/英名称变体；保留单一外交机构身份"),
    "2": ("驻美国大韩民国大使馆 (Embassy of the Republic of Korea in the USA)", "GOV", "kr",
          "同一使馆的名称变体；保留单一外交机构身份"),
    "3": ("丰树集团 (Mapletree Investments)", "SOE", "sg",
          "淡马锡系新加坡国企；两个 collision 下的同一实体，1+1 条引用"),
    "4": ("国会国土交通委员会 (국회 국토교통위원회)", "GOV", "kr", "国会常设委员会，名称变体"),
    "5": ("第20届总统职务交接委员会 (제20대 대통령직인수위원회)", "GOV", "kr", "同一历史过渡机构"),
    "6": ("国民未来党 (국민의미래)", "PARTY", "kr", "政党，不应沿用 GOV 类别"),
    "7": ("陆军第一野战军司令部 (제1야전군사령부)", "MIL", "kr", "军事指挥机构，应改 MIL"),
    "8": ("新千年民主党 (새천년민주당)", "PARTY", "kr", "历史政党，应改 PARTY"),
    "9": ("开放国民党 (열린우리당)", "PARTY", "kr", "历史政党，应改 PARTY"),
    "10": ("司法研修院 (사법연수원)", "GOV", "kr", "司法培训机构，保留 GOV"),
    "11": ("首尔地方检察厅 (서울지방검찰청)", "GOV", "kr", "检察机关，名称变体"),
    "12": ("第17届总统职务交接委员会 (제17대 대통령직인수위원회)", "GOV", "kr", "同一历史过渡机构"),
    "13": ("首尔特别市政府 (서울특별시청)", "GOV", "kr", "首尔市政府，名称变体"),
    "14": ("世宗大学 (세종대학교)", "ACAD", "kr", "大学，应改 ACAD"),
    "15": ("首尔中央地方检察厅 (서울중앙지방검찰청)", "GOV", "kr", "检察机关，名称变体"),
    "16": ("世界卫生组织 (WHO)", "INTL", "kr", "全球组织；不应在 KR-GOV 下建号，先走全球主体归一"),
    "17": ("法务法人太平洋 (Bae, Kim & Lee LLC)", "CORP", "kr", "私营律师事务所，应改 CORP"),
    "18": ("釜山地方检察厅 (부산지방검찰청)", "GOV", "kr", "检察机关，名称变体"),
    "19": ("新政治国民会议 (새정치국민회의)", "PARTY", "kr", "历史政党，应改 PARTY"),
}
DEFER = {"16"}


def main():
    rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
    rev = list(csv.DictReader(open(REVIEW, encoding="utf-8-sig")))
    byrow = {str(i + 1): r for i, r in enumerate(rev)}
    groups = defaultdict(list)
    for r in rows:
        groups[r["组号"]].append(r)

    # ever_used incl refs
    used = set()
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/id_registry.json")):
        d = json.load(open(f, encoding="utf-8"))
        for key, idk in [("registry", "org_id"), ("person_registry", "person_id"),
                         ("deprecated_registry", "org_id"), ("deprecated_person_registry", "person_id")]:
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
            cand = f"{cc.upper()}-{cat}-{n:03d}"
            if cand not in used:
                used.add(cand); return cand

    out = []
    for gi in sorted(groups, key=int):
        members = groups[gi]
        name, cat, cc, rationale = OVERRIDES[gi]
        refs = sum(int(r["引用数"] or 0) for r in members)
        status = "defer_global" if gi in DEFER else "create_single_identity"
        new_id = "" if gi in DEFER else alloc(cc, cat)
        out.append({
            "组号": gi, "成员数": len(members), "推荐主身份名称": name,
            "国家": cc.upper(), "建议类别": cat, "处理方式": status,
            "候选新ID": new_id, "引用数": refs,
            "成员明细": " | ".join(f"{r['冲突ID']}｜{r['影子名称']}" for r in members),
            "理由": rationale,
        })
    fields = list(out[0].keys())
    p = os.path.join(OUT, "registry826_duplicate_org_plan.csv")
    with open(p, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(out)
    summary = {"groups": len(out), "create": sum(1 for r in out if r["处理方式"] == "create_single_identity"),
               "defer_global": sum(1 for r in out if r["处理方式"] == "defer_global"),
               "new_ids": sum(1 for r in out if r["候选新ID"]),
               "refs": sum(r["引用数"] for r in out)}
    json.dump(summary, open(os.path.join(OUT, "registry826_duplicate_org_plan_summary.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    for r in out: print(r)
    print("->", p)


if __name__ == "__main__":
    main()

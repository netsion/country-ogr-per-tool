# -*- coding: utf-8 -*-
"""Fix the 7 WHO/UNDP composite refs.

5 were false composites: related_entities names like "UNDP / PNUD" are one org.
2 are true multi-org work_experience rows: split into separate entries.

Usage: python scripts_tmp/split_composite_who_undp.py --dry|--apply
"""
import json, os, sys, time

BASE = "D:/ai-workspace/apec-osint-tool"
OUT = os.path.join(BASE, "output/_id_audit")


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


def main():
    apply = "--apply" in sys.argv
    undo = {"related": [], "splits": []}

    # 5 single-org related refs skipped by the over-broad composite filter
    rel = [
        ("output/cd/2026-10-05/orgs/CD-GOV-008.json", "CD-INTL-010", "US-INTL-024"),
        ("output/cd/2026-10-05/orgs/CD-GOV-012.json", "CD-INTL-010", "US-INTL-024"),
        ("output/cd/2026-10-05/orgs/CD-GOV-016.json", "CD-INTL-016", "US-INTL-005"),
        ("output/cd/2026-10-05/orgs/CD-GOV-022.json", "CD-INTL-016", "US-INTL-005"),
        ("output/lb/2026-09-17/orgs/LB-GOV-018.json", "LB-INTL-008", "US-INTL-024"),
    ]
    for relpath, old, new in rel:
        f = os.path.join(BASE, relpath)
        d = json.load(open(f, encoding="utf-8"))
        n = 0
        for i, x in enumerate(d.get("related_entities") or []):
            if x.get("org_id") == old:
                undo["related"].append({"file": relpath, "index": i, "old": old, "new": new,
                                        "org_name": x.get("org_name")})
                x["org_id"] = new; n += 1
        if apply and n:
            save_json(f, d)
        print(relpath, "changed", n)

    # split CL-PERSON-000467 work[8]
    f1 = os.path.join(BASE, "output/cl/2026-10-02/persons/CL-PERSON-000467.json")
    d1 = json.load(open(f1, encoding="utf-8"))
    arr = d1.get("work_experience") or []
    i = 8
    old = json.loads(json.dumps(arr[i]))
    base = {k: old.get(k) for k in ("position", "start_date", "end_date", "description", "source", "note")}
    splits = []
    for nm, oid in [
        ("联合国开发计划署 (PNUD)", "US-INTL-024"),
        ("联合国妇女署 (ONU Mujeres)", None),
        ("智利地方发展基金会 (Fundación Chile Descentralizado)", None),
        ("智利国家人权研究所 (INDH)", None),
    ]:
        x = dict(base); x["organization"] = nm; x["org_id"] = oid
        splits.append(x)
    undo["splits"].append({"file": "output/cl/2026-10-02/persons/CL-PERSON-000467.json",
                           "index": i, "old": old, "new": splits})
    if apply:
        d1["work_experience"] = arr[:i] + splits + arr[i + 1:]
        save_json(f1, d1)

    # split CL-PERSON-000497 work[9]
    f2 = os.path.join(BASE, "output/cl/2026-10-02/persons/CL-PERSON-000497.json")
    d2 = json.load(open(f2, encoding="utf-8"))
    arr2 = d2.get("work_experience") or []
    i = 9
    old2 = json.loads(json.dumps(arr2[i]))
    common = {"source": old2.get("source")}
    splits2 = [
        {"organization": "拉丁美洲社会科学学院 (FLACSO)", "org_id": None,
         "position": "FLACSO秘书长", "start_date": "1973", "end_date": "1975",
         "location": "阿根廷布宜诺斯艾利斯",
         "description": "1973年政变后携家人流亡布宜诺斯艾利斯，任FLACSO秘书长。",
         **common},
        {"organization": "北卡罗来纳大学教堂山分校 (University of North Carolina at Chapel Hill)",
         "org_id": None, "position": "William R. Kenan拉美研究讲席客座教授",
         "start_date": "1975", "end_date": "1975", "location": "美国北卡罗来纳州教堂山",
         "description": "离开FLACSO后赴美国北卡罗来纳大学教堂山分校任客座教授一年。",
         **common},
        {"organization": "联合国开发计划署 (PNUD/UNDP)", "org_id": "US-INTL-024",
         "position": "UNDP顾问", "start_date": "1975", "end_date": "1975",
         "location": "美国北卡罗来纳州教堂山",
         "description": "1975年任UNDP顾问。",
         **common},
        {"organization": "联合国区域就业项目 (PREALC)", "org_id": None,
         "position": "联合国PREALC区域就业项目顾问", "start_date": "1978", "end_date": "1984",
         "location": "智利圣地亚哥",
         "description": "1978年回国受聘联合国区域就业项目（PREALC），为拉美各国政府提供就业政策咨询。",
         "note": old2.get("note"), **common},
    ]
    undo["splits"].append({"file": "output/cl/2026-10-02/persons/CL-PERSON-000497.json",
                           "index": i, "old": old2, "new": splits2})
    if apply:
        d2["work_experience"] = arr2[:i] + splits2 + arr2[i + 1:]
        save_json(f2, d2)

    print(json.dumps({"related_changed": len(undo["related"]),
                      "splits": [(x["file"], len(x["new"])) for x in undo["splits"]]},
                     ensure_ascii=False, indent=1))
    if apply:
        json.dump(undo, open(os.path.join(OUT, "who_undp_composite_undo.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("undo ->", os.path.join(OUT, "who_undp_composite_undo.json"))
    else:
        print("DRY")


if __name__ == "__main__":
    main()

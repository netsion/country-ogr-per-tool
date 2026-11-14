# -*- coding: utf-8 -*-
"""P2 batch 3: manually approved high-similarity same-country relinks.

These are not strict-exact under the batch-1/2 matcher (mostly missing a
country prefix or a renamed ministry), but the current ID is an unrelated
profile and the target is the same institution. Composite/parent-subsidiary
cases are excluded.
"""
import json
import os
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from id_integrity_audit2 import BASE, OUT, load_datasets

APPROVE = {
    ("work_org", "KR-GOV-001", "KR-GOV-015"),   # 韩国国会 -> 大韩民国国会
    ("work_org", "KR-GOV-002", "KR-GOV-015"),
    ("work_org", "KR-GOV-016", "KR-GOV-015"),
    ("work_org", "KR-GOV-005", "KR-GOV-010"),   # 行政安全部
    ("work_org", "KR-MIL-001", "KR-MIL-006"),   # 合同/联合参谋本部
    ("work_org", "KR-MIL-001", "KR-MIL-002"),   # 大韩民国陆军
    ("work_org", "KR-MIL-007", "KR-MIL-001"),   # 国家情报院
    ("work_org", "VN-GOV-267", "VN-GOV-015"),   # 政府监察总署
    ("work_org", "MX-ACAD-006", "MX-GOV-022"),  # SEDATU
    ("work_org", "MX-ACAD-006", "MX-GOV-012"),  # SSPC
    ("work_org", "NZ-GOV-002", "NZ-GOV-001"),   # DPMC
    ("work_org", "CD-GOV-011", "CD-GOV-022"),   # 科学研究部
    ("work_org", "UZ-SOE-005", "UZ-GOV-012"),   # 经济部/经济财政部
    ("related_org", "NZ-GOV-001", "NZ-GOV-030"),  # 残疾人部
    ("related_org", "PE-GOV-098", "PE-GOV-025"),  # 国家司法委员会
    ("related_org", "BH-GOV-003", "BH-GOV-030"),  # 社会保险组织
    ("related_org", "TH-INTL-023", "TH-INTL-007"),  # UN-ESCAP
}


def save_json(path, obj):
    payload = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    tmp = path + ".tmp"
    for _ in range(6):
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(payload)
            os.replace(tmp, path)
            return
        except PermissionError:
            time.sleep(0.5)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)


def name_of(item, direction):
    keys = {
        "work_org": ("organization", "org_name", "organization_en"),
        "related_org": ("org_name", "name", "organization"),
    }[direction]
    for k in keys:
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def main():
    apply = "--apply" in sys.argv
    latest, _ = load_datasets()
    cand = json.load(open(os.path.join(OUT, "repair_candidates.json"), encoding="utf-8"))

    # target org profiles for name logging
    tnames = {}
    for cc, (date, folder) in latest.items():
        for f in __import__("glob").glob(os.path.join(folder, "orgs", "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            oid = d.get("org_id")
            if oid:
                bi = d.get("basic_info") or {}
                tnames[oid] = bi.get("name_zh") or bi.get("name_en") or oid

    changes = []
    stats = Counter()
    by_file = defaultdict(list)
    seen = set()
    for direction in ("work_org", "related_org"):
        for r in cand.get(direction, []):
            key = (direction, r.get("org_id") if direction == "work_org" else r.get("org_id_ref"),
                   r.get("suggested"))
            if key not in APPROVE:
                continue
            cc = r.get("cc")
            folder = latest.get(cc, (None, None))[1]
            if not folder:
                continue
            src_id = r.get("person_id") if direction == "work_org" else r.get("org_id")
            src_file = os.path.join(folder, "persons" if direction == "work_org" else "orgs",
                                    str(src_id) + ".json")
            if not os.path.exists(src_file):
                stats["source_missing"] += 1
                continue
            data = json.load(open(src_file, encoding="utf-8"))
            arr = "work_experience" if direction == "work_org" else "related_entities"
            field = "org_id"
            ref = r.get("organization") if direction == "work_org" else r.get("ref_name")
            for i, item in enumerate(data.get(arr) or []):
                if not isinstance(item, dict):
                    continue
                if item.get(field) != r.get("org_id" if direction == "work_org" else "org_id_ref"):
                    continue
                if name_of(item, direction) != ref:
                    continue
                pos = (os.path.relpath(src_file, BASE).replace(os.sep, "/"), arr, i)
                if pos in seen:
                    continue
                seen.add(pos)
                changes.append({
                    "file": pos[0], "array": arr, "index": i, "field": field,
                    "old": item.get(field), "new": r.get("suggested"),
                    "ref_name": ref, "target_name": tnames.get(r.get("suggested")),
                    "direction": direction,
                })
                by_file[pos[0]].append(changes[-1])
                stats["refs_changed"] += 1
                stats[f"refs_{direction}"] += 1

    if apply:
        for rel, items in by_file.items():
            fp = os.path.join(BASE, rel)
            data = json.load(open(fp, encoding="utf-8"))
            for ch in items:
                arr = data.get(ch["array"])
                if arr and ch["index"] < len(arr):
                    arr[ch["index"]][ch["field"]] = ch["new"]
            save_json(fp, data)

    summary = {
        "apply": apply,
        "refs_changed": stats["refs_changed"],
        "by_direction": {k: stats[f"refs_{k}"] for k in ("work_org", "related_org")},
        "files": len(by_file),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if apply:
        p = os.path.join(OUT, "p2_batch3_undo.json")
        json.dump({"summary": summary, "changes": changes}, open(p, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("undo ->", p)
    else:
        print("DRY")


if __name__ == "__main__":
    main()

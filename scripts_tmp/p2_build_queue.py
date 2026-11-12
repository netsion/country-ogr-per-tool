# -*- coding: utf-8 -*-
"""P2-0: build unique translation queue + prefill via in-dataset entity matching.

Queue item: {category, value, cc}  (unique by (value, cc))
Prefill: for family/rel names, look up the same person name in the SAME
dataset's other profiles (person_list / other jsons' name_zh) — reuse.
Also: match work/edu organization against orgs/*.json basic_info.name_zh
(organization name_zh is authoritative!). These prefills skip LLM.
Usage: python p2_build_queue.py
Outputs: output/_lang_p2/queue.json  +  prefill_map.json
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool"
OUT = os.path.join(BASE, "output", "_lang_p2")


def main():
    os.makedirs(OUT, exist_ok=True)
    # ---- build org name index: normalized org name (per cc) -> name_zh ----
    org_zh = {}
    for f in sorted(glob.glob(os.path.join(BASE, "output", "[a-z][a-z]", "20*", "orgs", "*.json"))):
        cc = os.path.relpath(f, BASE).replace(os.sep, "/").split("/")[1]
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        bi = d.get("basic_info") or {}
        zh = (bi.get("name_zh") or "").strip()
        if not zh:
            continue
        for key in (bi.get("name_original"), bi.get("name_en")):
            if key and key.strip():
                org_zh.setdefault((cc, key.strip().lower()), zh)

    # ---- person name index per cc: name -> name_zh ----
    person_zh = {}
    for f in sorted(glob.glob(os.path.join(BASE, "output", "[a-z][a-z]", "20*", "persons", "*.json"))):
        if os.path.basename(f) == "_index.json":
            continue
        cc = os.path.relpath(f, BASE).replace(os.sep, "/").split("/")[1]
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        nm = (d.get("name") or "").strip()
        zh = (d.get("name_zh") or "").strip()
        if nm and zh:
            person_zh.setdefault((cc, nm.lower()), zh)

    queue = []
    prefill = {}
    seen = set()
    for f in sorted(glob.glob(os.path.join(BASE, "output", "[a-z][a-z]", "20*",
                                           "persons", "*.json"))):
        if os.path.basename(f) == "_index.json":
            continue
        cc = os.path.relpath(f, BASE).replace(os.sep, "/").split("/")[1]
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for arr, key, cat in [
            ("person_relationships", "person_name", "rel"),
            ("family_members", "name", "family"),
            ("work_experience", "organization", "work"),
            ("education", "institution", "edu"),
        ]:
            for item in d.get(arr) or []:
                if not isinstance(item, dict):
                    continue
                v = (item.get(key) or "").strip()
                if not v:
                    continue
                ck = (cat, cc, v)
                if ck in seen:
                    continue
                seen.add(ck)
                # prefill attempts
                pf = None
                src = None
                if cat in ("family", "rel"):
                    pf = person_zh.get((cc, v.lower()))
                    src = "person_index"
                else:
                    pf = org_zh.get((cc, v.lower()))
                    src = "org_index"
                if pf:
                    prefill[f"{cat}|{cc}|{v}"] = {"zh": pf, "via": src}
                queue.append({"category": cat, "cc": cc, "value": v})

    with open(os.path.join(OUT, "queue.json"), "w", encoding="utf-8") as fh:
        json.dump(queue, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "prefill_map.json"), "w", encoding="utf-8") as fh:
        json.dump(prefill, fh, ensure_ascii=False, indent=1)

    from collections import Counter
    c = Counter((q["category"], q["cc"]) for q in queue)
    print(f"queue: {len(queue)} unique (value, cc) items | prefill available: {len(prefill)}")
    for (cat, cc), n in sorted(c.items(), key=lambda x: -x[1])[:20]:
        print(f"  {cat:7} {cc} {n}")
    cats = Counter(q["category"] for q in queue)
    print("by category:", dict(cats))


if __name__ == "__main__":
    main()

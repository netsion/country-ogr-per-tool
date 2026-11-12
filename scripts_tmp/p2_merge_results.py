# -*- coding: utf-8 -*-
"""P2-2: merge LLM translation results into person profile fields.

Join: (category, cc, value) -> zh from results files.
Apply: field = "中文(原文)"  (zh=null / brand exemption -> keep original).
Idempotent: entries already in 中文(...) form are skipped.
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool"
BATCHES = os.path.join(BASE, "output", "_lang_p2", "batches")
RESULTS = os.path.join(BASE, "output", "_lang_p2", "results")
CJK = re.compile(r"[\u4e00-\u9fff]")


def save_json(f, d):
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    os.replace(tmp, f)


def has_zh_paren(v):
    m = re.match(r"^([^（(]*)[(（]([^)）]*)[)）]\s*$", v or "")
    return bool(m and CJK.search(m.group(1)))


def main():
    results = {}
    for rf in sorted(glob.glob(os.path.join(RESULTS, "batch_*.json")) +
                     glob.glob(os.path.join(RESULTS, "sub_*.json"))):
        try:
            arr = json.load(open(rf, encoding="utf-8"))
        except Exception as e:
            print("SKIP corrupt result:", os.path.basename(rf), str(e)[:60])
            continue
        results[os.path.basename(rf).replace(".json", "")] = {
            e["i"]: e.get("zh") for e in arr if isinstance(e, dict)}
    print(f"result files: {len(results)}")

    zh_map = {}
    for rf in sorted(glob.glob(os.path.join(BATCHES, "batch_*.json")) +
                     glob.glob(os.path.join(BASE, "output", "_lang_p2",
                                            "batches_alt", "sub_*.json"))):
        bn = os.path.basename(rf).replace(".json", "")
        res = results.get(bn)
        if not res:
            continue
        items = json.load(open(rf, encoding="utf-8"))
        for it in items:
            zh = res.get(it["i"])
            if zh:
                zh_map[(it["cat"], it["cc"].lower(), it["v"])] = zh
    print(f"join map: {len(zh_map)}")

    files = [f for f in sorted(glob.glob(os.path.join(BASE, "output", "[a-z][a-z]",
                                                      "20*", "persons", "*.json")))
             if os.path.basename(f) != "_index.json"]
    changed_files = applied = skipped_brand = 0
    for f in files:
        rel = os.path.relpath(f, BASE).replace(os.sep, "/")
        cc = rel.split("/")[1]
        d = json.load(open(f, encoding="utf-8"))
        changed = False
        for arr, key, cat in [
            ("person_relationships", "person_name", "rel"),
            ("family_members", "name", "family"),
            ("work_experience", "organization", "work"),
            ("education", "institution", "edu"),
        ]:
            for item in d.get(arr) or []:
                if not isinstance(item, dict):
                    continue
                v = item.get(key) or ""
                if not v or has_zh_paren(v):
                    continue
                zh = zh_map.get((cat, cc, v))
                if not zh:
                    skipped_brand += 1
                    continue
                item[key] = f"{zh}({v})"
                applied += 1
                changed = True
        if changed:
            changed_files += 1
            save_json(f, d)
    print(f"APPLIED: fields={applied} files={changed_files} brand-skip={skipped_brand}")


if __name__ == "__main__":
    main()

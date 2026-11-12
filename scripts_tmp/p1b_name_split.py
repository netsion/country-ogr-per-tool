# -*- coding: utf-8 -*-
"""P1-2: restructure person.name where Chinese leaked into the native-name field.

Cases (confirmed policy 2026-11-12):
  1. "中文 (English)"            -> name=English, name_zh=中文 (if name_zh empty)
  2. "中文 / English"            -> split on slash
  3. KR: "曹国 (曺国, 조국)"     -> name=Hangul, name_zh=曹国, alias=曺国
  4. pure-Chinese name in MY/BN/SG (ethnic-Chinese names) -> KEEP (policy 4)
  5. KR Chinese-only name without Hangul -> left for P3 (needs Hangul generation)
Usage: python p1b_name_split.py [--dry]
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool"
DRY = "--dry" in sys.argv
CJK = re.compile(r"[\u4e00-\u9fff]")
LATIN = re.compile(r"[A-Za-z]")
HANGUL = re.compile(r"[\uac00-\ud7af]")
CJKR = {"cn", "hk", "tw", "mo"}
KEEP_PURE_CN = {"my", "sg", "bn"}  # ethnic Chinese names legal per policy 4
PAREN = re.compile(r"^([^（(]*)[(（]([^)）]*)[)）]\s*$")


def save_json(f, d):
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    os.replace(tmp, f)


def split_name(name, cc):
    """Return (new_name, new_name_zh, extra_alias) or None."""
    m = PAREN.match(name)
    if m:
        pre, inside = m.group(1).strip(), m.group(2).strip()
        # Case 3: KR "曹国 (曺国, 조국)"
        if cc == "kr":
            parts = [p.strip() for p in re.split(r"[,，]", inside) if p.strip()]
            hang = [p for p in parts if HANGUL.search(p)]
            if hang and CJK.search(pre):
                alias = [p for p in parts if not HANGUL.search(p) and p != pre]
                return (hang[0], pre, alias[0] if alias else None)
            if hang and not CJK.search(pre):
                return None
        # Case 1: "中文 (English)" — KR skipped: needs Hangul generation (P3)
        if CJK.search(pre) and inside and not CJK.search(inside) and LATIN.search(inside):
            if cc == "kr":
                return None
            return (inside, pre, None)
        return None
    # Case 2: "中文 / English"
    if "/" in name and CJK.search(name):
        parts = [p.strip() for p in name.split("/") if p.strip()]
        if len(parts) == 2:
            a, b = parts
            if CJK.search(a) and not CJK.search(b) and LATIN.search(b):
                return (b, a, None)
    return None


def main():
    fixed = 0
    review = []
    for f in sorted(glob.glob(os.path.join(BASE, "output", "[a-z][a-z]", "20*",
                                           "persons", "*.json"))):
        if os.path.basename(f) == "_index.json":
            continue
        rel = os.path.relpath(f, BASE).replace(os.sep, "/")
        cc = rel.split("/")[1]
        if cc in CJKR or cc == "jp":
            continue
        d = json.load(open(f, encoding="utf-8"))
        name = d.get("name") or ""
        if not name or not CJK.search(name):
            continue
        res = split_name(name, cc)
        if not res:
            if cc in KEEP_PURE_CN:
                continue  # legal ethnic-Chinese name
            review.append({"file": rel, "name": name,
                           "reason": "unparsed-chinese-in-name"})
            continue
        new_name, new_zh, alias = res
        if not DRY:
            d["name"] = new_name
            if new_zh and not (d.get("name_zh") or ""):
                d["name_zh"] = new_zh
            if alias:
                aliases = d.get("aliases") or []
                if isinstance(aliases, list) and alias not in aliases:
                    aliases.append(alias)
                    d["aliases"] = aliases
            save_json(f, d)
        fixed += 1
    print(("DRY-RUN" if DRY else "APPLIED"), f"name-fixed={fixed}, review={len(review)}")
    if not DRY:
        out = os.path.join(BASE, "output", "_social_audit", "p1_name_review.json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(review, fh, ensure_ascii=False, indent=1)
        print("review ->", out)


if __name__ == "__main__":
    main()

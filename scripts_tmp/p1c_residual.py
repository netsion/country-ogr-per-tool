# -*- coding: utf-8 -*-
"""P1c: residual name/name_en cleanups after P1b.

  A. name_en "Latin... (备注/中文...)" -> name_en = leading Latin part
  B. name_en "中文（Latin）"           -> name_en = Latin inside
  C. name "中文 (한글...)"             -> name = Hangul, name_zh = 中文
  D. name "非中文 (中文)"              -> name = prefix, name_zh = 中文 (if empty)
  E. Japanese-kanji names (nationality=JP) -> legal, skip
  F. name_en pure-Chinese -> leave for P3 (needs romanization)
Usage: python p1c_residual.py [--dry]
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
PAREN = re.compile(r"^([^（(]*)[(（]([^)）]*)[)）]\s*$")


def save_json(f, d):
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    os.replace(tmp, f)


def clean_name_en(en):
    """Return (new_en, kind) or (None, None)."""
    m = PAREN.match(en)
    if not m:
        return None, None
    pre, inside = m.group(1).strip(), m.group(2).strip()
    # A: Latin prefix, note/Chinese inside
    if LATIN.search(pre) and not CJK.search(pre) and CJK.search(inside):
        return pre, "A"
    # B: Chinese prefix, Latin inside
    if CJK.search(pre) and not CJK.search(inside) and LATIN.search(inside):
        return inside, "B"
    return None, None


def main():
    stats = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    review = []
    for f in sorted(glob.glob(os.path.join(BASE, "output", "[a-z][a-z]", "20*",
                                           "persons", "*.json"))):
        if os.path.basename(f) == "_index.json":
            continue
        rel = os.path.relpath(f, BASE).replace(os.sep, "/")
        d = json.load(open(f, encoding="utf-8"))
        changed = False

        # --- name_en cleanup ---
        en = d.get("name_en") or ""
        if CJK.search(en):
            new_en, kind = clean_name_en(en)
            if new_en:
                if not DRY:
                    d["name_en"] = new_en
                stats[kind] += 1
                changed = True
            elif not LATIN.search(en) and not HANGUL.search(en):
                stats["F"] += 1   # pure Chinese name_en -> P3 romanization queue
                review.append({"file": rel, "field": "name_en", "value": en,
                               "reason": "needs-romanization"})
            else:
                review.append({"file": rel, "field": "name_en", "value": en,
                               "reason": "complex-note"})

        # --- name cleanup ---
        nm = d.get("name") or ""
        if CJK.search(nm):
            m = PAREN.match(nm)
            handled = False
            if m:
                pre, inside = m.group(1).strip(), m.group(2).strip()
                if HANGUL.search(inside) and not CJK.search(inside):
                    # C: 中文 (한글)
                    if not DRY:
                        d["name"] = inside
                        if not (d.get("name_zh") or ""):
                            d["name_zh"] = pre
                    stats["C"] += 1
                    handled = True
                    changed = True
                elif not CJK.search(pre) and CJK.search(inside):
                    # D: 非中文 (中文)
                    if not DRY:
                        d["name"] = pre
                        if not (d.get("name_zh") or ""):
                            d["name_zh"] = inside
                    stats["D"] += 1
                    handled = True
                    changed = True
            if not handled:
                nat = d.get("nationality") or ""
                cc = rel.split("/")[1]
                if nat == "JP" or cc in ("cn", "hk", "tw", "mo", "my", "sg", "bn", "kr"):
                    pass  # legal: CJK regions / ethnic-Chinese / KR handled by P3
                else:
                    review.append({"file": rel, "field": "name", "value": nm,
                                   "reason": "chinese-name-non-jp"})
        if changed and not DRY:
            save_json(f, d)
    print(("DRY-RUN" if DRY else "APPLIED"), stats)
    if not DRY:
        out = os.path.join(BASE, "output", "_social_audit", "p1c_review.json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(review, fh, ensure_ascii=False, indent=1)
        print("review ->", out, f"({len(review)})")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""P1-1: swap reversed bracket order "English (中文)" -> "中文(English)".

Safety:
  - only swap when prefix has NO CJK and bracket content HAS CJK
  - skip when bracket looks like a NOTE, not a translation:
      * contains note keywords (现/原名/更名/即/位于/注/含/时任/前身/又名/简称...)
      * contains sentence punctuation 。；！？ or full-width comma with long content
      * bracket content much longer than prefix (>2.5x chars) -> suspicious
      * prefix too short (<2 chars)
  - ambiguous cases -> manual review list JSON
Usage: python p1_swap_brackets.py [--dry]
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
CJKR = {"cn", "hk", "tw", "mo"}
BR = re.compile(r"^([^（(]*)[(（]([^)）]*)[)）]\s*$")
NOTE_RE = re.compile(r"现|原名|更名|又名|前身|即|位于|注|含|时任|简称|译注|后任|曾任|创办|成立|收购|合并|上市|其中|以及|包括|美国|英国|法国|德国|日本|中国|新加坡|香港")
PUNCT_RE = re.compile(r"[。；！？]")

FIELDS = [
    ("person_relationships", "person_name"),
    ("family_members", "name"),
    ("work_experience", "organization"),
    ("education", "institution"),
]


def save_json(f, d):
    tmp = f + ".tmp"
    payload = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)
    os.replace(tmp, f)


def try_swap(v):
    """Return (new_value, None) on swap, or (None, reason) for manual review."""
    m = BR.match(v)
    if not m:
        return None, None
    pre, inside = m.group(1).strip(), m.group(2).strip()
    if not (inside and CJK.search(inside) and not CJK.search(pre)):
        return None, None
    if len(pre) < 2:
        return None, "prefix-too-short"
    if NOTE_RE.search(inside):
        return None, "bracket-looks-like-note"
    if PUNCT_RE.search(inside):
        return None, "has-sentence-punct"
    if len(inside) > len(pre) * 2.5:
        return None, "bracket-too-long"
    return f"{inside}({pre})", None


def main():
    swapped = 0
    review = []
    affected_files = 0
    for f in sorted(glob.glob(os.path.join(BASE, "output", "[a-z][a-z]", "20*",
                                           "persons", "*.json"))):
        if os.path.basename(f) == "_index.json":
            continue
        rel = os.path.relpath(f, BASE).replace(os.sep, "/")
        cc = rel.split("/")[1]
        if cc in CJKR:  # CJK-region datasets already use Chinese-first
            continue
        d = json.load(open(f, encoding="utf-8"))
        changed = False
        for arr, key in FIELDS:
            for i, item in enumerate(d.get(arr) or []):
                if not isinstance(item, dict):
                    continue
                v = item.get(key)
                if not isinstance(v, str) or not v:
                    continue
                new, reason = try_swap(v)
                if new:
                    if not DRY:
                        item[key] = new
                    swapped += 1
                    changed = True
                elif reason:
                    review.append({"file": rel, "field": f"{arr}[{i}].{key}",
                                   "value": v, "reason": reason})
        if changed:
            affected_files += 1
            if not DRY:
                save_json(f, d)
    print(("DRY-RUN" if DRY else "APPLIED"),
          f"swapped={swapped} affected_files={affected_files} review={len(review)}")
    if not DRY:
        out = os.path.join(BASE, "output", "_social_audit", "p1_bracket_review.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(review, fh, ensure_ascii=False, indent=1)
        print("review list ->", out)


if __name__ == "__main__":
    main()

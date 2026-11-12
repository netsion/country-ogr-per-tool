# -*- coding: utf-8 -*-
"""Person data language-convention audit (read-only).

Rules from person_collection_rules.md:
  - name: native official language (NOT Chinese-first)
  - name_zh: pure Chinese
  - name_en: Latin/English (no Chinese)
  - person_relationships[].person_name / family_members[].name:
      "中文(本国官方语言)" format
  - work_experience[].organization / education[].institution: same format
  - CJK regions (CN/HK/TW/MO): Chinese-first bracket order
  - KR: Hangul-first
"""
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")

CJK = re.compile(r"[\u4e00-\u9fff]")
HANGUL = re.compile(r"[\uac00-\ud7af]")
KANA = re.compile(r"[\u3040-\u30ff]")
LATIN = re.compile(r"[A-Za-z]")
ARABIC = re.compile(r"[\u0600-\u06ff]")
CYRILLIC = re.compile(r"[\u0400-\u04ff]")
THAI = re.compile(r"[\u0e00-\u0e7f]")
OTHER_SCRIPTS = re.compile(
    r"[\u0400-\u04ff\u0600-\u06ff\u0e00-\u0e7f\uac00-\ud7af\u3040-\u30ff\u0590-\u05ff\u0900-\u097f]")

CJK_REGIONS = {"cn", "hk", "tw", "mo"}
BRACKET_RE = re.compile(r"^([^（(]*)[(（]([^)）]*)[)）]\s*$")


def bracket_reversed(v):
    m = BRACKET_RE.match(v or "")
    if not m:
        return False
    before, inside = m.group(1), m.group(2)
    return bool(CJK.search(inside)) and not CJK.search(before)


def audit():
    stats = Counter()
    per_cc = defaultdict(Counter)
    examples = defaultdict(list)

    def flag(cc, key, ex):
        stats[key] += 1
        per_cc[cc][key] += 1
        if len(examples[key]) < 6:
            examples[key].append(ex)

    total = 0
    for f in sorted(glob.glob("output/[a-z][a-z]/20*/persons/*.json")):
        rel = os.path.normpath(f).replace("\\", "/")
        cc = rel.split("/")[1]
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        total += 1
        per_cc[cc]["total"] += 1
        name = d.get("name") or ""
        name_zh = d.get("name_zh") or ""
        name_en = d.get("name_en") or ""
        pid = d.get("person_id") or os.path.basename(f)

        # --- name: Chinese-first check (non-CJK countries) ---
        if cc not in CJK_REGIONS and cc != "jp":
            if name and CJK.search(name):
                flag(cc, "name_contains_chinese", f"{pid} name={name!r}")
        if cc in CJK_REGIONS:
            if name and bracket_reversed(name):
                flag(cc, "name_bracket_reversed", f"{pid} name={name!r}")
        if cc == "kr":
            if name and not HANGUL.search(name):
                flag(cc, "kr_name_no_hangul", f"{pid} name={name!r}")
            if name and bracket_reversed(name):
                flag(cc, "name_bracket_reversed", f"{pid} name={name!r}")

        # --- name_zh purity ---
        if not name_zh:
            flag(cc, "name_zh_missing", f"{pid} name={name!r}")
        else:
            if LATIN.search(name_zh):
                flag(cc, "name_zh_has_latin", f"{pid} name_zh={name_zh!r}")
            elif OTHER_SCRIPTS.search(name_zh):
                flag(cc, "name_zh_has_other_script", f"{pid} name_zh={name_zh!r}")
            elif not CJK.search(name_zh):
                flag(cc, "name_zh_no_chinese", f"{pid} name_zh={name_zh!r}")

        # --- name_en ---
        if name_en and CJK.search(name_en):
            flag(cc, "name_en_has_chinese", f"{pid} name_en={name_en!r}")
        if not name_en:
            flag(cc, "name_en_missing", f"{pid}")

        # --- relationships / family names ---
        for i, rel_ in enumerate(d.get("person_relationships") or []):
            if not isinstance(rel_, dict):
                continue
            v = rel_.get("person_name") or ""
            if not v:
                continue
            if cc not in CJK_REGIONS and not CJK.search(v):
                flag(cc, "rel_name_no_chinese", f"{pid} rel[{i}]={v!r}")
            elif bracket_reversed(v):
                flag(cc, "rel_name_bracket_reversed", f"{pid} rel[{i}]={v!r}")

        for i, fam in enumerate(d.get("family_members") or []):
            if not isinstance(fam, dict):
                continue
            v = fam.get("name") or ""
            if not v:
                continue
            if cc not in CJK_REGIONS and not CJK.search(v):
                flag(cc, "family_name_no_chinese", f"{pid} fam[{i}]={v!r}")
            elif bracket_reversed(v):
                flag(cc, "family_name_bracket_reversed", f"{pid} fam[{i}]={v!r}")

        # --- work_experience.organization / education.institution ---
        for i, w in enumerate(d.get("work_experience") or []):
            if not isinstance(w, dict):
                continue
            v = w.get("organization") or ""
            if not v:
                continue
            if cc not in CJK_REGIONS and not CJK.search(v):
                flag(cc, "work_org_no_chinese", f"{pid} work[{i}]={v!r}")
            elif bracket_reversed(v):
                flag(cc, "work_org_bracket_reversed", f"{pid} work[{i}]={v!r}")

        for i, e in enumerate(d.get("education") or []):
            if not isinstance(e, dict):
                continue
            v = e.get("institution") or ""
            if not v:
                continue
            if cc not in CJK_REGIONS and not CJK.search(v):
                flag(cc, "edu_inst_no_chinese", f"{pid} edu[{i}]={v!r}")
            elif bracket_reversed(v):
                flag(cc, "edu_inst_bracket_reversed", f"{pid} edu[{i}]={v!r}")

    print(f"persons audited: {total}\n")
    print(f"{'check':32} {'count':>7}")
    print("-" * 42)
    for k, v in stats.most_common():
        print(f"{k:32} {v:7}")
    print("\nper-country breakdown (only countries with any flag):")
    for cc, c in sorted(per_cc.items()):
        flags = sum(v for k, v in c.items() if k != "total")
        if flags:
            print(f"  {cc}: {flags} flags / {c['total']} persons")
    print("\nexamples:")
    for k, exs in examples.items():
        print(f"[{k}]")
        for e in exs:
            print("   ", e)


if __name__ == "__main__":
    audit()

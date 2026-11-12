# -*- coding: utf-8 -*-
"""Count affected persons per language check (read-only)."""
import glob
import json
import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

CJK = re.compile(r"[\u4e00-\u9fff]")
LATIN = re.compile(r"[A-Za-z]")
HANGUL = re.compile(r"[\uac00-\ud7af]")
CJKR = {"cn", "hk", "tw", "mo"}
BR = re.compile(r"^([^（(]*)[(（]([^)）]*)[)）]\s*$")


def rev(v):
    m = BR.match(v or "")
    if not m:
        return False
    b, i = m.group(1), m.group(2)
    return bool(CJK.search(i)) and not CJK.search(b)


persons = defaultdict(set)


def main():
    for f in glob.glob("output/[a-z][a-z]/20*/persons/*.json"):
        rel = os.path.normpath(f).replace(os.sep, "/")
        cc = rel.split("/")[1]
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        pid = d.get("person_id") or os.path.basename(f)
        nm = d.get("name") or ""
        zh = d.get("name_zh") or ""
        en = d.get("name_en") or ""

        def add(k):
            persons[k].add(pid)

        if cc not in CJKR and cc != "jp" and nm and CJK.search(nm):
            add("name_contains_chinese")
        if not zh:
            add("name_zh_missing")
        elif LATIN.search(zh):
            add("name_zh_has_latin")
        elif not CJK.search(zh):
            add("name_zh_no_chinese")
        if en and CJK.search(en):
            add("name_en_has_chinese")
        if not en:
            add("name_en_missing")
        if cc == "kr" and nm and not HANGUL.search(nm):
            add("kr_name_no_hangul")
        for r in d.get("person_relationships") or []:
            v = (r or {}).get("person_name") or ""
            if v:
                if cc not in CJKR and not CJK.search(v):
                    add("rel_no_chinese")
                elif rev(v):
                    add("rel_reversed")
        for r in d.get("family_members") or []:
            v = (r or {}).get("name") or ""
            if v:
                if cc not in CJKR and not CJK.search(v):
                    add("family_no_chinese")
                elif rev(v):
                    add("family_reversed")
        for w in d.get("work_experience") or []:
            v = (w or {}).get("organization") or ""
            if v:
                if cc not in CJKR and not CJK.search(v):
                    add("work_no_chinese")
                elif rev(v):
                    add("work_reversed")
        for e in d.get("education") or []:
            v = (e or {}).get("institution") or ""
            if v:
                if cc not in CJKR and not CJK.search(v):
                    add("edu_no_chinese")
                elif rev(v):
                    add("edu_reversed")

    order = ["name_contains_chinese", "name_zh_missing", "name_zh_has_latin",
             "name_en_has_chinese", "name_en_missing", "kr_name_no_hangul",
             "rel_no_chinese", "rel_reversed", "family_no_chinese",
             "family_reversed", "work_no_chinese", "work_reversed",
             "edu_no_chinese", "edu_reversed"]
    print(f"{'check':28} {'persons':>8}")
    print("-" * 40)
    for k in order:
        print(f"{k:28} {len(persons[k]):8}")
    union = set()
    for v in persons.values():
        union |= v
    print(f"{'ANY issue':28} {len(union):8}")


if __name__ == "__main__":
    main()

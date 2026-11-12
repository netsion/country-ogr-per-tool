# -*- coding: utf-8 -*-
"""Print samples per issue category from avatar audit result."""
import json
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool/output"
d = json.load(open(os.path.join(BASE, "_avatar_audit", "audit_result.json"), encoding="utf-8"))
issues = d["issues"]


def short(f):
    return os.path.relpath(f, BASE).replace("\\", "/" if os.sep == "\\" else "/")


def sample(t, n=4):
    print(f"--- {t} ({sum(1 for x in issues if x['type']==t)}) ---")
    for i in [x for x in issues if x["type"] == t][:n]:
        print("  ", short(i["file"]), "|", str(i.get("detail", ""))[:110],
              "|", i.get("class", ""), i.get("value_type", ""))


for t in ["qid_page", "wiki_file_page", "social_page", "html_page",
          "malformed_no_scheme", "local_missing", "bad_naming", "id_mismatch"]:
    # qid_page etc are classes of bad_source_url
    sel = [x for x in issues if x["type"] == "bad_source_url" and x.get("class") == t] \
        if t in ("qid_page", "wiki_file_page", "social_page", "html_page", "malformed_no_scheme") \
        else [x for x in issues if x["type"] == t]
    print(f"--- {t} ({len(sel)}) ---")
    for i in sel[:4]:
        print("  ", short(i["file"]), "|", str(i.get("detail", ""))[:110])

c = Counter(i.get("value_type") for i in issues if i["type"] == "malformed_profile")
print("--- malformed_profile value_type:", dict(c))
for i in [x for x in issues if x["type"] == "malformed_profile"][:3]:
    print("  ", short(i["file"]), "|", i.get("value_type"), "|", str(i.get("detail", ""))[:80])

c2 = Counter(short(i["file"]).split("/")[0] for i in issues if i["type"] == "wrong_location")
print("--- wrong_location by country (top 12):", dict(c2.most_common(12)))
c3 = Counter(short(i["file"]).split("/")[0] for i in issues if i["type"] == "download_gap")
print("--- download_gap by country (top 12):", dict(c3.most_common(12)))

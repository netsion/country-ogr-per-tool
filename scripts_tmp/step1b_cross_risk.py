# -*- coding: utf-8 -*-
"""Risk review for Step 1b cross-country replacements (read-only).

Flags cross-country links to generic public institutions (university / ministry /
court / state bank ...) where the reference name has no distinctive proper noun.
Typical failure: Peru person -> '国立工程大学' matched Nicaragua's UNI.

Output: output/_id_audit/step1b_cross_country_review.csv
"""
import csv
import glob
import json
import os
import re
import sys
import unicodedata
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, sig

GENERIC_CN = [
    "国立", "公立", "国家", "全国", "联邦", "中央", "人民", "政府", "共和国",
    "大学", "学院", "学校", "中学", "小学", "研究院", "研究所", "研究", "科学",
    "工程", "技术", "理工", "师范", "医科", "农业", "工业", "商业", "经济",
    "银行", "金融", "保险", "基金", "投资", "控股", "集团", "公司", "企业",
    "部", "委员会", "委员会", "法院", "法庭", "检察院", "政府", "议会", "国会",
    "中心", "协会", "学会", "联合会", "联盟", "组织", "机构", "署", "局", "厅",
    "院", "社", "台", "报", "出版社", "医院", "医疗", "卫生", "教育", "文化",
    "新闻", "广播", "电视", "通信", "电信", "能源", "电力", "石油", "矿业",
    "交通", "运输", "航空", "航天", "国防", "军事", "警察", "安全", "外交",
    "内政", "司法", "财政", "贸易", "工业", "劳工", "社会", "环境", "水利",
]
GENERIC_EN = {
    "university", "college", "school", "institute", "institution", "academy",
    "bank", "banking", "financial", "finance", "insurance", "fund", "investment",
    "holding", "group", "company", "corporation", "corp", "enterprise",
    "ministry", "department", "court", "tribunal", "prosecutor", "government",
    "parliament", "congress", "senate", "council", "committee", "commission",
    "center", "centre", "association", "society", "federation", "union",
    "organization", "organisation", "agency", "authority", "administration",
    "hospital", "medical", "health", "education", "culture", "news", "broadcast",
    "television", "telecom", "telecommunications", "energy", "electric",
    "electricity", "petroleum", "oil", "mining", "transport", "transportation",
    "aviation", "aerospace", "defense", "defence", "military", "police",
    "security", "foreign", "interior", "justice", "treasury", "trade", "industry",
    "labor", "labour", "social", "environment", "water", "national", "federal",
    "central", "state", "public", "general", "international", "national",
    "of", "the", "and", "for", "de", "del", "la", "el", "y", "e", "di", "da",
    "universidad", "nacional", "ingeniería", "ingenieria", "engineering",
    "tecnológica", "tecnologia", "technology", "politécnica", "politécnica",
    "polytechnic", "research", "sciences", "science", "arts", "humanities",
}
STOP_CN = {"的", "与", "和", "及", "在", "为", "对", "会", "公司", "集团"}


def variants(s):
    s = str(s or "")
    parts = re.findall(r"[（(]([^）)]*)[）)]", s) + [re.sub(r"[（(][^）)]*[）)]", " ", s)]
    out = []
    for p in parts:
        for x in re.split(r"[/、;；]", p):
            if x.strip():
                out.append(x.strip())
    return out


def distinctive_cn(text):
    t = text
    for w in sorted(GENERIC_CN, key=len, reverse=True):
        t = t.replace(w, "")
    t = re.sub(r"[\s·\.\,\-—、:：()（）]", "", t)
    return len(t) >= 2


def distinctive_en(text):
    t = unicodedata.normalize("NFKD", text)
    t = "".join(ch for ch in t if not unicodedata.combining(ch)).lower()
    toks = re.findall(r"[a-z][a-z\-]+", t)
    left = [x for x in toks if x not in GENERIC_EN and len(x) >= 3]
    return bool(left)


def main():
    undo = json.load(open(os.path.join(OUT, "step1b_undo.json"), encoding="utf-8"))
    names = {}
    for kind, pat, idkey in [("p", "output/[a-z][a-z]/20*/persons/*.json", "person_id"),
                             ("o", "output/[a-z][a-z]/20*/orgs/*.json", "org_id")]:
        for f in glob.glob(os.path.join(BASE, pat)):
            if os.path.basename(f).startswith("_"):
                continue
            d = json.load(open(f, encoding="utf-8"))
            i = d.get(idkey)
            if not i:
                continue
            if kind == "p":
                names[i] = d.get("name") or d.get("name_zh")
            else:
                bi = d.get("basic_info") or {}
                names[i] = bi.get("name_zh") or bi.get("name_original")

    rows = []
    for x in undo:
        cc = x["file"].split("/")[1]
        nid = str(x["new"])
        ncc = nid[:2].lower()
        if ncc == cc:
            continue
        m = re.match(r"^[A-Z]{2}-([A-Z_]+)-", nid)
        ncat = m.group(1) if m else "?"
        vs = variants(x["ref_name"])
        cn_dist = any(distinctive_cn(v) for v in vs if re.search(r"[\u4e00-\u9fff]", v))
        en_dist = any(distinctive_en(v) for v in vs if re.search(r"[A-Za-z]", v))
        distinctive = cn_dist or en_dist
        if ncat in ("ACAD", "GOV", "MIL", "PARTY", "SOE", "FIN", "NGO", "MEDIA", "INTL"):
            risk = "low" if distinctive else "high"
        else:
            risk = "low"
        rows.append({"risk": risk, "cat": x["cat"], "cc": cc, "ref_name": x["ref_name"],
                     "old": x["old"], "old_name": names.get(x["old"]),
                     "new": nid, "new_name": names.get(nid), "new_cat": ncat,
                     "file": x["file"]})
    order = {"high": 0, "medium": 1, "low": 2}
    rows.sort(key=lambda r: (order[r["risk"]], r["new_cat"], r["cc"]))
    out = os.path.join(OUT, "step1b_cross_country_review.csv")
    with open(out, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["风险", "类别", "引用国家", "引用名称", "原ID", "原指向",
                    "新ID", "新指向", "新ID类型", "文件"])
        for r in rows:
            w.writerow([r["risk"], r["cat"], r["cc"], r["ref_name"], r["old"],
                        r["old_name"], r["new"], r["new_name"], r["new_cat"],
                        r["file"]])
    print("cross-country", len(rows), "risk", dict(Counter(r["risk"] for r in rows)))
    print("high by cat", dict(Counter(r["new_cat"] for r in rows if r["risk"] == "high")))
    for r in [x for x in rows if x["risk"] == "high"][:25]:
        print(r["cc"], r["cat"], "|", r["ref_name"], "|", r["old"], "->", r["new"],
              r["new_name"])
    print("->", out)


if __name__ == "__main__":
    main()

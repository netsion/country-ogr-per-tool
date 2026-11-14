# -*- coding: utf-8 -*-
"""Build human-review tables for Step 1b cross-country public-institution links.

Outputs (read-only):
  output/_id_audit/step1b_cross_public_review.csv    (491 rows, full)
  output/_id_audit/step1b_cross_public_priority.csv  (100-row priority sample)
"""
import csv
import glob
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT

PUB = {"ACAD", "FIN", "SOE", "NGO", "MEDIA", "INTL"}
COUNTRY_CN = {
    "ae": "阿联酋", "au": "澳大利亚", "az": "阿塞拜疆", "bf": "布基纳法索",
    "bh": "巴林", "bn": "文莱", "bo": "玻利维亚", "ca": "加拿大",
    "cd": "刚果", "ci": "科特迪瓦", "cl": "智利", "cm": "喀麦隆",
    "dz": "阿尔及利亚", "gn": "几内亚", "hk": "香港", "id": "印度尼西亚",
    "iq": "伊拉克", "jo": "约旦", "jp": "日本", "kg": "吉尔吉斯斯坦",
    "kh": "柬埔寨", "kr": "韩国", "kw": "科威特", "kz": "哈萨克斯坦",
    "la": "老挝", "lb": "黎巴嫩", "ly": "利比亚", "ma": "摩洛哥",
    "mo": "澳门", "mx": "墨西哥", "my": "马来西亚", "ng": "尼日利亚",
    "ni": "尼加拉瓜", "nz": "新西兰", "om": "阿曼", "pe": "秘鲁",
    "pg": "巴布亚新几内亚", "ph": "菲律宾", "qa": "卡塔尔", "ru": "俄罗斯",
    "sa": "沙特阿拉伯", "sg": "新加坡", "td": "乍得", "th": "泰国",
    "tj": "塔吉克斯坦", "tm": "土库曼斯坦", "tn": "突尼斯", "tw": "台湾",
    "tz": "坦桑尼亚", "ug": "乌干达", "us": "美国", "uz": "乌兹别克斯坦",
    "vn": "越南",
}
COUNTRY_EN = {
    "ae": "united arab emirates", "au": "australia", "az": "azerbaijan",
    "bf": "burkina faso", "bh": "bahrain", "bn": "brunei", "bo": "bolivia",
    "ca": "canada", "cd": "democratic republic of the congo", "ci": "cote d'ivoire",
    "cl": "chile", "cm": "cameroon", "dz": "algeria", "gn": "guinea",
    "hk": "hong kong", "id": "indonesia", "iq": "iraq", "jo": "jordan",
    "jp": "japan", "kg": "kyrgyzstan", "kh": "cambodia", "kr": "south korea",
    "kw": "kuwait", "kz": "kazakhstan", "la": "laos", "lb": "lebanon",
    "ly": "libya", "ma": "morocco", "mo": "macau", "mx": "mexico",
    "my": "malaysia", "ng": "nigeria", "ni": "nicaragua", "nz": "new zealand",
    "om": "oman", "pe": "peru", "pg": "papua new guinea", "ph": "philippines",
    "qa": "qatar", "ru": "russia", "sa": "saudi arabia", "sg": "singapore",
    "td": "chad", "th": "thailand", "tj": "tajikistan", "tm": "turkmenistan",
    "tn": "tunisia", "tw": "taiwan", "tz": "tanzania", "ug": "uganda",
    "us": "united states", "uz": "uzbekistan", "vn": "vietnam",
}
BRANCH_WORDS = ["办事处", "代表处", "办公室", "分部", "分公司", "分行", "支部",
                "country office", "office in", "in china", "in vietnam"]
GENERIC_MEDIA = ["国家报", "今日报", "日报", "晚报", "时报", "早报", "周报",
                 "电视台", "电台", "通讯社", "广播", "新闻报", "论坛报",
                 "el país", "el pais", "la nación", "la nacion", "hoy",
                 "today", "daily", "times", "post", "herald", "tribune",
                 "gazette", "observer", "guardian", "independent", "telegraph"]
GENERIC_CN = ["国立", "公立", "国家", "全国", "联邦", "中央", "人民", "政府",
              "共和国", "大学", "学院", "学校", "研究院", "研究所", "研究",
              "科学", "工程", "技术", "理工", "师范", "医科", "农业", "工业",
              "商业", "经济", "银行", "金融", "保险", "基金", "投资", "控股",
              "集团", "公司", "企业", "部", "委员会", "法院", "法庭", "检察院",
              "议会", "国会", "中心", "协会", "学会", "联合会", "联盟", "组织",
              "机构", "署", "局", "厅", "院", "社", "台", "报", "出版社",
              "医院", "医疗", "卫生", "教育", "文化", "新闻", "广播", "电视",
              "通信", "电信", "能源", "电力", "石油", "矿业", "交通", "运输",
              "航空", "航天", "国防", "军事", "警察", "安全", "外交", "内政",
              "司法", "财政", "贸易", "劳工", "社会", "环境", "水利"]
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
    "central", "state", "public", "general", "international", "of", "the", "and",
    "for", "de", "del", "la", "el", "y", "e", "di", "da", "universidad",
    "nacional", "ingenieria", "engineering", "tecnologica", "technology",
    "politecnica", "polytechnic", "research", "sciences", "science", "arts",
    "humanities", "country", "office",
}


def norm_acc(s):
    s = unicodedata.normalize("NFKD", str(s))
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def variants(s):
    s = str(s or "")
    parts = re.findall(r"[（(]([^）)]*)[）)]", s) + [re.sub(r"[（(][^）)]*[）)]", " ", s)]
    out = []
    for p in parts:
        for x in re.split(r"[/、;；]", p):
            if x.strip():
                out.append(x.strip())
    return out


def distinctive(text):
    # Chinese
    t = text
    for w in sorted(GENERIC_CN, key=len, reverse=True):
        t = t.replace(w, "")
    t = re.sub(r"[\s·\.\,\-—、:：()（）]", "", t)
    if len(t) >= 2:
        return True
    # Latin (accent-folded)
    toks = re.findall(r"[a-z][a-z\-]+", norm_acc(text))
    left = [x for x in toks if x not in GENERIC_EN and len(x) >= 3]
    return bool(left)


def load_names():
    names, cats = {}, {}
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
                cats[i] = "PERSON"
            else:
                bi = d.get("basic_info") or {}
                names[i] = bi.get("name_zh") or bi.get("name_original")
                m = re.match(r"^[A-Z]{2}-([A-Z_]+)-", i)
                cats[i] = m.group(1) if m else "?"
    return names, cats


def owner_name(rel):
    f = os.path.join(BASE, rel)
    d = json.load(open(f, encoding="utf-8"))
    if "/persons/" in rel.replace("\\", "/"):
        return d.get("name") or d.get("name_zh") or ""
    bi = d.get("basic_info") or {}
    return bi.get("name_zh") or bi.get("name_original") or ""


def main():
    undo = json.load(open(os.path.join(OUT, "step1b_undo.json"), encoding="utf-8"))
    names, cats = load_names()
    rows = []
    for x in undo:
        cc = x["file"].split("/")[1]
        nid = str(x["new"])
        ncc = nid[:2].lower()
        if ncc == cc:
            continue
        ncat = cats.get(nid, "?")
        if ncat not in PUB:
            continue
        vs = variants(x["ref_name"])
        dist = any(distinctive(v) for v in vs)
        media_generic = any(g in norm_acc(x["ref_name"]) for g in GENERIC_MEDIA)
        target_name = names.get(nid) or ""
        # does target name contain its own country name while ref doesn't?
        own_cn = COUNTRY_CN.get(ncc, "")
        own_en = COUNTRY_EN.get(ncc, "")
        target_has = bool((own_cn and own_cn in target_name)
                          or (own_en and own_en in norm_acc(target_name)))
        ref_has = bool((own_cn and own_cn in x["ref_name"])
                       or (own_en and own_en in norm_acc(x["ref_name"])))
        country_mismatch = target_has and not ref_has
        branch = ncat == "INTL" and any(w in norm_acc(target_name + " " + x["ref_name"])
                                        for w in [norm_acc(w) for w in BRANCH_WORDS])
        if media_generic or country_mismatch or (not dist):
            risk = "high"
        else:
            risk = "low"
        if risk == "high" or country_mismatch or branch:
            priority = 1
        else:
            priority = 2
        if country_mismatch:
            advice = f"建议复核（目标含国别：{own_cn}，引用未提）"
        elif branch:
            advice = "建议复核（国际组织国别办事处）"
        elif media_generic or not dist:
            advice = "建议复核/置空（通用机构名）"
        else:
            advice = "建议保留（专名，需抽查）"
        rows.append({
            "优先级": priority, "风险": risk, "机器建议": advice,
            "类别": x["cat"], "引用国家": cc, "引用方": owner_name(x["file"]),
            "引用名称": x["ref_name"], "原ID": x["old"],
            "原指向": names.get(x["old"], ""), "新ID": nid,
            "新指向": target_name, "新ID类型": ncat,
            "原始引用位置": f"{x['file']}#{x['array']}[{x['index']}].{x['field']}",
            "目标国别提示": own_cn if country_mismatch else "",
            "复核结论": "", "备注": "",
        })
    rows.sort(key=lambda r: (r["优先级"], r["新ID类型"], r["引用国家"], r["类别"]))
    fields = ["优先级", "风险", "机器建议", "类别", "引用国家", "引用方", "引用名称",
              "原ID", "原指向", "新ID", "新指向", "新ID类型", "原始引用位置",
              "目标国别提示", "复核结论", "备注"]
    full = os.path.join(OUT, "step1b_cross_public_review.csv")
    with open(full, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    # priority sample: all priority-1 rows, then fill by category
    sample = [r for r in rows if r["优先级"] == 1]
    target = {"ACAD": 10, "FIN": 15, "SOE": 8, "NGO": 5, "MEDIA": 10, "INTL": 12}
    for cat, n in target.items():
        add = [r for r in rows if r["优先级"] == 2 and r["新ID类型"] == cat][:n]
        sample += add
    sample = sample[:100]
    sample.sort(key=lambda r: (r["优先级"], r["新ID类型"]))
    pri = os.path.join(OUT, "step1b_cross_public_priority.csv")
    with open(pri, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(sample)
    print("full", len(rows), "priority", len(sample))
    print("by cat", dict(Counter(r["新ID类型"] for r in rows)))
    print("by priority", dict(Counter(r["优先级"] for r in rows)))
    print("advice", dict(Counter(r["机器建议"] for r in rows)))
    for r in rows[:20]:
        print(r["优先级"], r["新ID类型"], r["引用国家"], "|", r["引用名称"], "->",
              r["新ID"], r["新指向"], "|", r["机器建议"])


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Patch BO-PERSON-000190: add verified LinkedIn, 2 more sourced stances."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000190.json")

with open(OUT, encoding="utf-8") as f:
    data = json.load(f)

# 1) Verified LinkedIn account: profile's own work history lists ENDE TRANSMISION
#    jul 2015 - ago 2017 Cochabamba, matching official BBV/ASFI records
#    (designation 2015-09-17, irrevocable resignation 2017-09-11) -> identity confirmed.
data["social_accounts"] = [
    {
        "platform": "linkedin",
        "account_name": "Arturo Iporre Salguero",
        "url": "https://bo.linkedin.com/in/arturo-iporre-salguero-0a1a1223",
        "source": "档案本人经历列有ENDE TRANSMISION（2015年7月-2017年8月，科恰班巴），与玻利维亚证券交易所及ASFI公告的任职起止（2015-09-17就任、2017-09-11辞职）吻合，确认身份",
    }
]
data["social_accounts_note"] = (
    "6项平台扫描（facebook/twitter-x/linkedin/instagram/tiktok/youtube）：LinkedIn确认1个本人账号"
    "（arturo-iporre-salguero-0a1a1223，其经历中的ENDE Transmisión任职与官方公告吻合）；"
    "bo.linkedin.com/in/jorgeiporre（电信/诺基亚背景）判定为同名不同人；"
    "bo.linkedin.com/in/arturo-iporre-874bb6140（仅列ENDE TRANSMISION职务，疑为同一人的旧档案，无法进一步确认，不收录）；"
    "Facebook存在多个同名个人档案均无法确认身份；X/Instagram/TikTok/YouTube未发现本人账号。"
)

# 2) Two more sourced stances
data["political_stances"].extend([
    {
        "date": "2014-09-10",
        "topic": "区域电力互联技术路线",
        "stance_content": "主张电力互联须与长期合同挂钩，以保障收入的稳定性、可预期性及合同承诺；指出与阿根廷同为50赫兹的互联具优势（拟议亚瓜瓜亚-塔尔塔加尔132千伏线路约75公里、交换容量至100兆瓦，另研究500千伏方案最高1350兆瓦），巴西因60赫兹频差需另行处理，认为玻利维亚区位与市场规模条件优越、与更大邻国市场的互联可转化为出口机遇",
        "source": "IBCE 2014-09-10（ENDE互联研究引语）",
    },
    {
        "date": "2013-05-07",
        "topic": "国家电力公司管理与项目连续性",
        "stance_content": "就任ENDE临时总经理时表示，公司在管理中追求的核心是达成目标，肯定前任比利亚罗埃尔任内取得可见成果，承诺延续在建电力项目、按进度计划保障全国电力供应",
        "source": "eju.tv/Los Tiempos 2013-05-07（就职引语）",
    },
])

# 3) Quotes: add LinkedIn evidence
data["collection_meta"]["quotes"].append(
    {"title": "Arturo Iporre Salguero - Partner Director - LinkedIn Bolivia（本人账号，经历含ENDE TRANSMISION 2015-2017）",
     "url": "https://bo.linkedin.com/in/arturo-iporre-salguero-0a1a1223"}
)
data["collection_meta"]["quotes"].append(
    {"title": "6 \"Arturo Iporre\" profiles | LinkedIn（同名档案目录）",
     "url": "https://bo.linkedin.com/pub/dir/Arturo/Iporre"}
)

# 4) Update notes points (4)/(5)
data["collection_meta"]["notes"] = (
    "信息核实说明：(1) 现任职务及2025-11-18新领导层背景以ENDE官网名录与ERBOL、Opinión任命报道为准；"
    "(2) 2013-2014总裁任期及2015-2017 ENDE Transmisión任期有官方决议、交易所公告及两个以上独立媒体来源；"
    "(3) 出生日期、出生地、家庭成员无公开记录，相关字段留空；"
    "(4) LinkedIn本人账号经其档案中ENDE Transmisión任职经历与官方公告比对确认，其余平台无可确认账号；"
    "(5) AUDING LATAM合伙人董事履历见其LinkedIn档案（身份已核实），但属自述性单一来源，未经独立第二来源证实，任职时间不详；"
    "(6) MBA授予院校不详；(7) name_zh沿用库内既有译名。"
)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("PATCHED", OUT)
print("social_accounts:", len(data["social_accounts"]))
print("political_stances:", len(data["political_stances"]))
print("quotes:", len(data["collection_meta"]["quotes"]))

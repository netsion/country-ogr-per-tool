# -*- coding: utf-8 -*-
"""Agent D task 2: append verified social accounts to persons with empty social_accounts.

Only accounts passing name+position+organization three-factor verification are added.
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
PERSONS = os.path.join(BASE, "persons")

# pid -> list of account dicts
ADD = {
    "BO-PERSON-000454": [
        {
            "platform": "linkedin",
            "account_name": "Nicolas Joray",
            "url": "https://ch.linkedin.com/in/nicolas-joray-35187516",
            "source": "LinkedIn 个人页：Nicolas Joray，CEO - Philanthropic organizations，单位 Fundación Patiño，所在地日内瓦大区；与本档案「帕蒂尼奥基金会总干事、常驻日内瓦」吻合。另有瑞士驻玻使馆等多条 Facebook 帖文称其「Director General de la Fundación Patiño」交叉印证。姓名+职务+机构三要素核实通过。",
        }
    ],
    "BO-PERSON-000467": [
        {
            "platform": "linkedin",
            "account_name": "Jordi Surkin",
            "url": "https://bo.linkedin.com/in/jordi-surkin-1b2aa023",
            "source": "LinkedIn 个人页：Jordi Surkin，Director de Conservación en WWF Bolivia，教育经历含 UCLA（University of California, Los Angeles），与本档案「WWF 玻利维亚办公室保护高级总监」及学术署名 Jordi Beneria-Surkin 的背景吻合；signalhire 同名档案亦标注 Director Senior de Conservación at WWF Bolivia。姓名+职务+机构三要素核实通过。注：站内另有一同名「Head of Environment at GNTP」旧档与一份疑似重复的 WWF 档案，未收录。",
        }
    ],
    "BO-PERSON-000434": [
        {
            "platform": "linkedin",
            "account_name": "Juan Pablo Chumacero Ruiz",
            "url": "https://bo.linkedin.com/in/juan-pablo-chumacero-ruiz-9855bba0",
            "source": "LinkedIn 个人页：Juan Pablo Chumacero Ruiz，Investigador en temas agrarios y desarrollo rural，单位 Fundación TIERRA；与本档案「玻利维亚土地研究基金会（Fundación TIERRA）执行主任」吻合。Fundación TIERRA 官方 Facebook 2021-08-13 公告其当选执行主任交叉印证。姓名+职务+机构三要素核实通过。",
        }
    ],
    "BO-PERSON-000469": [
        {
            "platform": "linkedin",
            "account_name": "Samuel Sangüeza-Pardo",
            "url": "https://bo.linkedin.com/in/samuel-sang%C3%BCeza-pardo-899b094",
            "source": "LinkedIn 个人页：Samuel Sangüeza-Pardo，Director Project Finance for Permanence WWF - Bolivia，教育经历 Universidad Católica Boliviana；与本档案「WWF 玻利维亚办公室永久性融资计划（PFP）项目总监」吻合。姓名+职务+机构三要素核实通过。",
        },
        {
            "platform": "facebook",
            "account_name": "Samuel Sangüeza-Pardo",
            "url": "https://www.facebook.com/samuel.sanguezapardo/",
            "source": "Facebook 同名账号，主页自我介绍列明 Director PFP at WWF Bolivia、曾任 Representante de país at WWF Bolivia，与本档案两个 WWF 玻利维亚职务逐项对应；另有多条新闻视频（Punto Vida Scc、SERNAP）以其 WWF 玻利维亚代表身份出镜。姓名+职务+机构三要素核实通过。",
        },
    ],
    "BO-PERSON-000468": [
        {
            "platform": "facebook",
            "account_name": "Alfonso Llobet Querejazu",
            "url": "https://www.facebook.com/alfyacare/",
            "source": "Facebook 账号与本人全名完全一致（Alfonso Llobet Querejazu），所在地圣克鲁斯，工作经历列明 Monitoreo y Evaluación de proyectos at WWF Bolivia，与本档案「WWF 玻利维亚办公室规划、监测与评估协调员」吻合；2025 年多家媒体报道其以 WWF 玻利维亚临时代表/负责人身份公开活动。姓名+职务+机构三要素核实通过。",
        }
    ],
}

changed = []
for pid, accounts in ADD.items():
    path = os.path.join(PERSONS, pid + ".json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if data.get("social_accounts") not in ([], None):
        raise SystemExit("social_accounts not empty for %s, abort" % pid)
    data["social_accounts"] = accounts
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    changed.append((pid, len(accounts)))
    print("OK %s +%d account(s)" % (pid, len(accounts)))

print("Updated %d persons, %d accounts total" % (len(changed), sum(n for _, n in changed)))

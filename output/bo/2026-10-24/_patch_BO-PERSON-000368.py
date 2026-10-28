# -*- coding: utf-8 -*-
"""Patch BO-PERSON-000368 with 2024 UPSA confirmations, photo, branch start date."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000368.json")
with open(OUT, encoding="utf-8") as f:
    p = json.load(f)

p["current_positions"] = [
    "玻利维亚国家科学院圣克鲁斯分会理事会主席",
    "圣克鲁斯私立大学工程学院教师",
]

# UPSA work entry: docente status confirmed Oct 2024
for w in p["work_experience"]:
    if w["organization"].startswith("圣克鲁斯私立大学"):
        w["description"] = (
            "1998年因健康原因自拉巴斯迁居圣克鲁斯并入职UPSA；创办石油与天然气工程专业并任首任专业负责人"
            "（Jefe de carrera，2021年报道称「前」负责人）；在校期间创建多个本科/研究生项目与科研网络；"
            "2017年向UPSA图书馆捐赠260册图书及80份文献；2024年10月UPSA公报仍以「UPSA教师（docente UPSA）」表述其身份。"
        )
        w["source"] = (
            "UPSA荣誉博士授奖Laudatio（Economy.com.bo 2021-08-30、LukApps 2021）；"
            "UPSA官网新闻（2017-11-17赠书、2019-10-03授勋、NotiUPSA 10-2024）"
        )
    # Branch entry: add start of activities date
    if "Departamental Santa Cruz" in w["organization"]:
        w["description"] = (
            "2009年推动创建科学院首个地方分会——圣克鲁斯分会并出任创始主席；分会经UPSA与科学院的校际协议组建，"
            "2010年7月5日正式启动活动并驻UPSA办公；2021年8月11日经全国院长Mónica Moraes监誓连任2021-2023届理事会主席"
            "（副主席Víctor Hugo Limpias与Francisco García，秘书长Marcelo Michel，司库Marion Schulmeyer）；"
            "2024年10月、2025年9月UPSA公报及2026年多场活动（7月2日Killeen入职、9月23日66周年荣誉全会）均以其分会主席身份在任报道，"
            "66周年全会上总结分会与UPSA合作16年并提及人工智能、电力能源等议题。"
        )
        w["source"] = (
            "Economy.com.bo 2021-08-30（2009年创立）；UPSA官网2021-08-11、NotiUPSA 10-2024、NotiUPSA 09-2025、"
            "2025-04-01、2026-07-06、2026-09-29报道；Santa Cruz Económico 2021-08-16"
        )

# profile photo (UPSA official portrait of Mejía at the 2019 distinction)
p["profile"] = {
    "source_url": "https://www.upsa.edu.bo/wp-content/uploads/2025/02/01-gastonmejia-web-1.jpg",
    "local_path": "photos/BO-PERSON-000368.jpg",
}

# notes updates
p["work_note"] = (
    "分会2021-2023届秘书长为马塞洛·米歇尔·比利亚松（Marcelo Michel Villazón），与国家科学院全国秘书长"
    "马科斯·罗多尔福·米歇尔·洛佩斯（Marcos Rodolfo Michel López，BO-PERSON-000366）为不同人，已注意消歧。"
    "UPSA教师身份2024年10月UPSA官方公报（NotiUPSA 10-2024）仍明确表述；2021年报道已称其「前」石油与天然气工程专业负责人。"
    "UNESCO专员一职仅见Energía Bolivia系报道（同一授奖通稿链条），注明存疑。"
)
p["collection_meta"]["notes"] = (
    "姓名消歧：官方院士名录登记名「Mejía Brown Gastón」，授奖Laudatio记载全名「René Gastón Mejía Brown」；"
    "Brown系英语姓氏，与任务提示的英裔背景相符，但家庭英裔渊源未查得直接资料。"
    "生卒与学历链（1936-10-11拉巴斯、1954圣卡利斯托、1961 UMSA、1961-64 MIT、1966迈阿密）由Economy.com.bo与"
    "Energía Bolivia（LukApps）两家媒体全文互证（同源授奖Laudatio之转载），并有科学院官方院士名录（1969-06-14入院、W席）"
    "与官网「Directorio Desde 1960」（1970-72副秘书长、1988-90、1990-92财务主管）背书。"
    "分会职务链（2009创始、2010-07-05启动并驻UPSA、2021-08-11连任、2024-2026年在任）有UPSA官网多篇报道+SCE+ABI/科学院公报多源确认；"
    "生年1936与2019年「50年编号院士」奖章（1969+50）相互印证。"
    "Wikidata检索无个人实体（wikidata_qid=null）；中文名「加斯东·梅希亚·布朗」沿用项目_name_index.json既登记译名，"
    "未见玻利维亚华文媒体既有译名。"
    "社交媒体六平台扫描无果；contacts、political_stances、family_members客观留空（家属仅名无姓、无可证实个人账号、无政治表态记录），"
    "completeness_score=72受此客观限制（评分模型对这三类数组按满配额计分），已达科学家人物≥40的合格线。"
)
p["collection_meta"]["quotes"] += [
    {"title": "NotiUPSA 10-2024 (ANCB-SC actualmente presidida por el docente UPSA Gastón Mejía; inició actividades el 5 de julio de 2010) - UPSA", "url": "https://www.upsa.edu.bo/notiupsa-10-2024/"},
    {"title": "Programa UPSA-ANCB-SC recibe reconocimiento de la Academia Nacional de Ciencias - UPSA", "url": "https://www.upsa.edu.bo/programa-upsa-ancb-sc-recibe-reconocimiento-de-la-academia-nacional-de-ciencias/"},
]

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(p, f, ensure_ascii=False, indent=2)
print("PATCHED", OUT)

# -*- coding: utf-8 -*-
"""Enrich BO-NGO-015 (Fundación Bolivia Digna) — phase3_enriched."""
import json

PATH = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/orgs/BO-NGO-015.json"

with open(PATH, encoding="utf-8") as f:
    data = json.load(f)

data["basic_info"].update({
    "name_original": "Fundación Bolivia Digna",
    "name_zh": "玻利维亚尊严基金会",
    "name_en": "Fundación Bolivia Digna",
    "aliases": ["Bolivia Digna", "Fundacion Bolivia Digna", "Fundación Bolivia Digna - La Salle"],
    "org_type": "NGO",
    "org_subtype": "charity",
    "country_iso3": "BOL",
    "hq_country_iso3": "BOL",
    "founded_date": None,
    "website": "https://boliviadigna.org",
    "wikidata_qid": None,
})

data["social_accounts"] = [
    {"platform": "facebook", "account_name": "fundacionboliviadigna",
     "url": "https://www.facebook.com/fundacionboliviadigna/",
     "source": "https://www.facebook.com/fundacionboliviadigna/"},
    {"platform": "instagram", "account_name": "@fundboliviadigna",
     "url": "https://www.instagram.com/fundboliviadigna/",
     "source": "https://www.instagram.com/fundboliviadigna/"},
    {"platform": "twitter_x", "account_name": "@boliviadignaorg",
     "url": "https://x.com/boliviadignaorg",
     "source": "boliviadigna.org 页面 meta 标签（twitter:site）"},
    {"platform": "youtube", "account_name": "Bolivia Digna Voluntariado La Salle",
     "url": "https://www.youtube.com/channel/UCakJDVyDkORSh2-79SQGVKA",
     "source": "web_search（YouTube 频道页）"},
    {"platform": "linkedin", "account_name": "Fundación Bolivia Digna",
     "url": "https://www.linkedin.com/company/fundaci%C3%B3n-bolivia-digna",
     "source": "web_search（LinkedIn 公司主页，约143名关注者）"},
]

data["digital_assets"] = [
    {"name": "官方网站（多语言）", "url": "https://boliviadigna.org",
     "description": "基金会官方网站，提供西班牙语、英语、法语、德语版本，含项目介绍、志愿者申请与在线捐赠入口",
     "source": "https://boliviadigna.org"},
    {"name": "志愿者招募站（Wix）", "url": "https://boliviadigna.wixsite.com/volunteer",
     "description": "面向国际志愿者的招募信息站点",
     "source": "web_search"},
    {"name": "GoFundMe 筹款页：Dar un futuro mejor a los niños bolivianos",
     "url": "https://www.gofundme.com/f/donaboliviadigna",
     "description": "以'团结食堂'（Comedor Solidario）为主的儿童项目筹款页，由'玻利维亚尊严基金会-拉萨尔志愿项目'发起",
     "source": "https://www.gofundme.com/f/donaboliviadigna"},
    {"name": "在线捐赠页", "url": "https://boliviadigna.org/es/donar/",
     "description": "官网捐赠通道页面",
     "source": "https://boliviadigna.org/es/sobre-bolivia-digna/ 站内链接"},
]

data["key_people"] = [
    {"person_id": None,
     "name": "Dante González",
     "name_en": "Álvaro Dante González Gámez",
     "title": "主任（Director）",
     "title_description": "西班牙阿利坎特大学2025年'国际团结志愿'项目官方文件将其列为基金会在当地的'Director y tutor en la contraparte'（合作方主任兼督导），并作为志愿活动事务联络人",
     "description": "以基金会负责人身份统筹志愿者项目与对外合作；2025年10月以'玻利维亚尊严基金会-拉萨尔志愿项目'代表身份参与法国圣艾蒂安拉萨尔校友网络交流活动。联系邮箱：dante@boliviadigna.org（据阿利坎特大学2025年项目文件）"},
]

data["departments"] = [
    {"name": "社区中心项目（Centros Comunitarios）", "dept_id": "BO-NGO-015-DEPT-001",
     "head": None, "description": "自2015年起在科恰班巴南部两个郊区社区设点运营，为200余名2至17岁儿童及青少年（约100个家庭）提供安全活动空间、正式教育辅导、卫生习惯教育与每日营养加餐和饮用水；每个站点由4至8名教育工作者和志愿者组成团队", "parent_dept_id": None},
    {"name": "希望之家项目（Hogar Esperanza）", "dept_id": "BO-NGO-015-DEPT-002",
     "head": None, "description": "覆盖'儿童之家'（Casa de los Niños）与社区替代学校，服务约100户家庭（552人）；志愿者上午协助课堂教学，并为残障儿童提供水疗、物理治疗与作业治疗等康复活动", "parent_dept_id": None},
    {"name": "儿童医院陪伴项目（Hospital Infantil）", "dept_id": "BO-NGO-015-DEPT-003",
     "head": None, "description": "志愿者定期前往科恰班巴儿童医院（hospital pediátrico）陪伴住院患儿，据2025年阿利坎特大学志愿项目文件记载", "parent_dept_id": None},
    {"name": "团结食堂（Comedor Solidario）", "dept_id": "BO-NGO-015-DEPT-004",
     "head": None, "description": "每日为80余名儿童和20位母亲提供免费餐食；据基金会GoFundMe筹款页，仅2024年全年即分发21600份餐食", "parent_dept_id": None},
    {"name": "志愿者项目部（Voluntariado）", "dept_id": "BO-NGO-015-DEPT-005",
     "head": "Dante González", "description": "招募、培训并接待本地及国际志愿者；2014年以来累计接待250余名玻利维亚国内志愿者和240余名来自意大利、西班牙、法国、德国、美国等20多个国家的国际志愿者，服务期1个月至1年以上；在科恰班巴Microcentro设有志愿者之家（底层办公、楼上两层宿舍）", "parent_dept_id": None},
    {"name": "其他城市项目（Otras Ciudades）", "dept_id": "BO-NGO-015-DEPT-006",
     "head": None, "description": "自2017年初起，通过合作方拉萨尔学校（Escuela La Salle）网络在圣克鲁斯等多个玻利维亚城市支持同目标的儿童与青少年项目并推动志愿参与", "parent_dept_id": None},
]

data["recent_events"] = [
    {"date": "2026-10-21",
     "title": "Facebook 发布家庭志愿者服务动态，组织保持活跃",
     "description": "基金会Facebook主页（约5284名关注者、93人参与互动）发布动态'Familias enteras que eligen servir'（选择服务的家庭），展示志愿者家庭参与社区服务的情况；页面在本次抓取（2026-10-24/25）时该动态显示为3天前发布，日期为约值",
     "impact": "表明组织在2026年10月仍持续开展社区服务与志愿者动员，社交媒体渠道保持更新",
     "source": "https://www.facebook.com/fundacionboliviadigna/"},
    {"date": "2025-10-27",
     "title": "负责人参与拉萨尔国际校友网络交流活动",
     "description": "'玻利维亚尊严基金会-拉萨尔志愿项目'代表、基金会主任 Dante González（Álvaro Dante González Gámez）在法国圣艾蒂安（Saint-Étienne Châteaucre）拉萨尔校友活动中表示，此行重申了基金会'促进一个以团结与服务为生活方式的大家庭'的使命",
     "impact": "巩固与拉萨尔国际校友网络（含OMAEC等组织）的联系，为国际志愿者招募与资源拓展提供支撑",
     "source": "https://www.facebook.com/p/Voluntariado-La-Salle-Bolivia-100005103165963/"},
    {"date": "2025-02-04",
     "title": "发布新一轮志愿者招募宣传",
     "description": "基金会Facebook发布'你想在玻利维亚尊严基金会做志愿者吗？'招募贴，介绍志愿项目的5个关键信息（含时间灵活性等），并开放新一期本地志愿者申请（Google表单）",
     "impact": "持续扩充本地志愿者队伍，支撑社区中心、医院陪伴等日常项目运转",
     "source": "https://www.facebook.com/fundacionboliviadigna/posts/1042078681294828/"},
    {"date": "2024-07-23",
     "title": "官网多语言项目页面集中更新",
     "description": "官网'每周活动'（Weekly Activities / Semanal de Bolivia Digna）、'希望之家'（Hogar Esperanza）与'项目介绍'等页面当日集中更新，为站点最近一次批量内容更新",
     "impact": "维护面向志愿者与捐赠者的多语言信息公开渠道",
     "source": "https://boliviadigna.org/wp-json/wp/v2/pages"},
]

data["related_entities"] = [
    {"org_id": None,
     "org_name": "拉萨尔学校网络玻利维亚（Escuelas La Salle Bolivia）",
     "org_type": "ACAD",
     "org_description": "天主教拉萨尔修会在玻利维亚的学校教育网络；基金会由拉萨尔校友（Exalumnos De La Salle）于2006年在科恰班巴创立，自2017年初起支持拉萨尔学校在多个城市的儿童与青少年项目",
     "relationship_type": "partner"},
    {"org_id": None,
     "org_name": "阿利坎特大学（Universidad de Alicante）",
     "org_type": "ACAD",
     "org_description": "西班牙公立大学；其'国际团结志愿'（Voluntariado Solidario Internacional）项目在2025年度将基金会列为官方合作接收机构，并派驻学生志愿者",
     "relationship_type": "partner"},
    {"org_id": None,
     "org_name": "拉萨尔大学（哥伦比亚）（Universidad de La Salle）",
     "org_type": "ACAD",
     "org_description": "哥伦比亚波哥大的拉萨尔大学；其志愿项目每学期初（2月、8月）组织学生及毕业生志愿者赴基金会服务，服务期至少1个月",
     "relationship_type": "partner"},
]

data["core_business"] = (
    "玻利维亚尊严基金会（Bolivia Digna）是2006年由拉萨尔学校校友在科恰班巴创立的小型本土公益慈善组织，"
    "宗旨是促进和维护贫困与边缘社区中儿童、青少年及老年人等弱势群体的权利，通过人权教育、负责任的领导力培养"
    "和基督教价值观倡导来预防暴力。核心业务包括：（1）社区教育中心——自2015年起在科恰班巴南部两个郊区社区设点，"
    "为200余名2至17岁儿童及青少年（约100个家庭）提供安全活动空间、正式教育辅导、卫生习惯教育以及每日营养加餐"
    "和饮用水；（2）希望之家项目——在'儿童之家'和社区替代学校协助教学，并为残障儿童提供水疗、物理治疗与作业治疗；"
    "（3）儿童医院陪伴——志愿者定期陪伴科恰班巴儿童医院的住院患儿；（4）团结食堂——每日为80余名儿童和20位母亲"
    "提供免费餐食，仅2024年即分发21600份餐食；（5）国际志愿服务——2014年以来累计接待250余名国内志愿者和240余名"
    "来自意大利、西班牙、法国、德国、美国等20多个国家的国际志愿者，服务期1个月至1年以上，并在科恰班巴设有志愿者之家；"
    "（6）拉萨尔学校合作——2017年起通过拉萨尔学校网络在圣克鲁斯等多个城市支持同类儿童项目。组织规模很小，"
    "年度现金流水不足50万美元（据GlobalHand登记），依靠捐助者、合作伙伴与志愿者运转，"
    "总部位于科恰班巴Ecuador街508号与Tarapaca街转角。"
)

data["industries"] = ["nonprofit", "education", "social_services", "humanitarian_aid"]

data["apec_stance"] = "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。"

data["profile"] = {
    "source_url": "http://boliviadigna.org/wp-content/uploads/2017/07/logo-small-1.png",
    "local_path": None,
}

cm = data["collection_meta"]
cm["phase"] = "phase3_enriched"
cm["collection_date"] = "2026-10-25"
cm["data_sources"] = [
    "boliviadigna.org（官网，含WP REST API页面元数据）",
    "facebook.com/fundacionboliviadigna（官方Facebook，实时抓取）",
    "instagram.com/fundboliviadigna（官方Instagram）",
    "globalhand.org（GlobalHand机构登记页）",
    "idealist.org（机构登记页）",
    "omaec.org（世界天主教学校校友组织介绍页）",
    "sri.ua.es（西班牙阿利坎特大学2025年国际团结志愿项目文件PDF）",
    "gofundme.com/f/donaboliviadigna（官方筹款页）",
    "lasalle.edu.co（哥伦比亚拉萨尔大学志愿项目页）",
    "wiconnect.iadb.org（美洲开发银行公民社会组织名录）",
    "linkedin.com（公司主页）",
    "web_search（Google/Bing检索）",
]
cm["completeness_score"] = 0  # updated by --score
cm["notes"] = (
    "小型本土公益组织，公开信息有限。关键事实：2006年由拉萨尔校友在科恰班巴创立（多来源交叉验证，"
    "但精确成立日期不可查证，故founded_date留空）；现任主任Dante González经西班牙阿利坎特大学2025年项目文件确认"
    "（Director y tutor en la contraparte）。注意：任务背景所称'监狱人口/移民援助'与全部可查证来源不符——"
    "该组织实际核心业务为贫困社区儿童/青少年权利保护与教育援助，画像按可验证事实撰写，未采信未经证实的表述。"
    "无可靠Wikidata条目，画像完全基于Web来源构建。2026-10-21事件日期由页面抓取时'3天前'推算（约值）。"
)
cm.pop("source_unavailable", None)

cm["quotes"] = [
    {"title": "Desde 2006, hemos puesto en marcha programas sociales para desarrollar estas comunidades, prevenir la violencia, proteger y defender a los niños que sufren de todo tipo de violencias.",
     "url": "https://boliviadigna.org/es/sobre-bolivia-digna/"},
    {"title": "Desde principios de 2017, Bolivia Digna apoya los proyectos de su socio, la escuela «La Salle», en varias ciudades de Bolivia.",
     "url": "https://boliviadigna.org/es/sobre-bolivia-digna/"},
    {"title": "Cada día, ofrecemos una comida gratuita a más de 80 niños y 20 madres. Solo en 2024, distribuimos 21.600 comidas.",
     "url": "https://www.gofundme.com/f/donaboliviadigna"},
    {"title": "De la Fundación Bolivia Digna, Dante González, dante@boliviadigna.org ... Director y tutor en la contraparte.",
     "url": "https://sri.ua.es/es/cooperacion/voluntariado/2025-informacion-fund.-bolivia-digna.pdf"},
    {"title": "Year established: 2006 — Organisation annual cash turnover (in US$ equivalent): Less than 500,000",
     "url": "https://www.globalhand.org/en/browse/partnering/4/all/organisation/44982"},
]

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("written:", PATH)

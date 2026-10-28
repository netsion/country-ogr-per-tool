# -*- coding: utf-8 -*-
"""Enrich BO-ACAD-006 (Universidad Pública de El Alto) - phase3_enriched."""
import json

PATH = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/orgs/BO-ACAD-006.json"

with open(PATH, encoding="utf-8") as f:
    data = json.load(f)

data["basic_info"]["name_original"] = "Universidad Pública de El Alto"
data["basic_info"]["name_zh"] = "埃尔阿尔托公立大学"
data["basic_info"]["name_en"] = "Public University of El Alto"
data["basic_info"]["aliases"] = ["UPEA", "Universidad Pública de El Alto"]

data["social_accounts"] = [
    {
        "platform": "facebook",
        "account_name": "UPEA digital",
        "url": "https://www.facebook.com/UPEAdigital/",
        "source": "https://www.facebook.com/UPEAdigital/",
    },
    {
        "platform": "facebook",
        "account_name": "UPEA Televisión Canal Universitario 25.1",
        "url": "https://www.facebook.com/upeatelevisioncanal25/",
        "source": "https://www.facebook.com/upeatelevisioncanal25/",
    },
    {
        "platform": "youtube",
        "account_name": "UPEA digital (@upea_digital)",
        "url": "https://www.youtube.com/@upea_digital",
        "source": "https://www.youtube.com/@upea_digital",
    },
    {
        "platform": "tiktok",
        "account_name": "UPEA Televisión (@upeatelevisionoficial)",
        "url": "https://www.tiktok.com/@upeatelevisionoficial",
        "source": "https://www.tiktok.com/@upeatelevisionoficial",
    },
]

data["digital_assets"] = [
    {
        "name": "UPEA 机构门户网站",
        "url": "https://www.upea.edu.bo/",
        "description": "埃尔阿尔托公立大学官方网站，发布招生、专业、事件与机构新闻（www.upea.bo 重定向至此）。",
        "source": "https://es.wikipedia.org/wiki/Universidad_P%C3%BAblica_de_El_Alto",
    },
    {
        "name": "UPEA digital 官方 YouTube 频道",
        "url": "https://www.youtube.com/@upea_digital",
        "description": "学校官方 YouTube 频道，由公共关系与传播处（Relaciones Públicas y Comunicación）管理。",
        "source": "https://www.youtube.com/@upea_digital",
    },
    {
        "name": "UPEA Televisión 大学电视台（25.1 频道）",
        "url": "https://www.facebook.com/upeatelevisioncanal25/",
        "description": "学校所属大学电视台（埃尔阿尔托 25.1 频道），通过 Facebook 页面发布学术活动与机构动态。",
        "source": "https://www.facebook.com/upeatelevisioncanal25/",
    },
]

data["key_people"] = [
    {
        "person_id": None,
        "name": "卡洛斯·孔多里·蒂蒂里科 (Carlos Condori Titirico)",
        "title": "校长",
        "title_description": "Rector",
        "description": "现任UPEA校长，2023年以「SOMOS U」竞选组合（搭档埃弗拉因·钱比）单一候选名单当选，任期2023-2026，据报以约95%得票率就任。2026年主政期间推动科研立校与学术单位认证计划（年初已有24个学业单位获CEUB认证），并于2026年10月牵头联合玻利维亚大学体系（CEUB）就国家「50/50」税收分成方案编制高教部门技术建议。多份2026年官方与媒体来源确认其现任身份。",
    },
    {
        "person_id": None,
        "name": "埃弗拉因·钱比·巴尔加斯 (Efraín Chambi Vargas)",
        "title": "副校长",
        "title_description": "Vicerrector",
        "description": "现任UPEA副校长，2023年与校长孔多里以「SOMOS U」组合一同当选。2026年2月开学典礼上宣布认证路线图：4月前再认证3-4个学业单位、年底累计达34个，并推动设立学术质量处（Departamento de Calidad Académica）统筹认证与自评工作。",
    },
]

data["departments"] = [
    {
        "name": "Área de Ciencias de la Salud（健康科学学部）",
        "dept_id": None,
        "head": None,
        "description": "下设医学、牙科学、护理学、营养与饮食学及义齿技术专业，按学年制培养，是学校报考热度最高的学部之一。",
        "parent_dept_id": None,
    },
    {
        "name": "Área de Ingeniería, Desarrollo Tecnológico y Productivo（工程技术与生产发展学部）",
        "dept_id": None,
        "head": None,
        "description": "下设电子工程、电气工程、企业生产工程、汽车电子工程、纺织工程与环境工程6个学期制专业，面向制造业与生产部门培养技术人才。",
        "parent_dept_id": None,
    },
    {
        "name": "Área de Ciencias Económicas y Financieras（经济与金融科学学部）",
        "dept_id": None,
        "head": None,
        "description": "下设经济学、公共会计、企业管理、旅游与酒店管理及国际贸易专业；其教学楼曾发生2021年3月2日学生集会后护栏坍塌致8死的重大事故。",
        "parent_dept_id": None,
    },
    {
        "name": "Área de Ciencias Agrícolas（农业科学学部）",
        "dept_id": None,
        "head": None,
        "description": "下设兽医与动物生产、动物科学与畜牧工业工程、农学工程3个学期制专业，服务高原农业区，并建有遗传改良中心。",
        "parent_dept_id": None,
    },
    {
        "name": "Área de Ciencias Sociales（社会科学学部）",
        "dept_id": None,
        "head": None,
        "description": "下设社会学、社会工作、社会传播、心理学、发展科学、历史及语言学与语言7个专业，学年制与学期制并存。",
        "parent_dept_id": None,
    },
    {
        "name": "Área de Ciencias de la Educación（教育科学学部）",
        "dept_id": None,
        "head": None,
        "description": "下设教育科学、学前教育及心理运动与体育3个学期制专业，培养基础教育师资。",
        "parent_dept_id": None,
    },
    {
        "name": "Área de Ciencias y Artes del Hábitat（人居科学与艺术学部）",
        "dept_id": None,
        "head": None,
        "description": "下设建筑学与造型艺术2个学期制专业，聚焦城市快速扩张背景下埃尔阿尔托的人居建设与艺术创作。",
        "parent_dept_id": None,
    },
    {
        "name": "Área de Ciencia y Tecnología（科学技术学部）",
        "dept_id": None,
        "head": None,
        "description": "下设天然气与石化工程、土木工程2个学期制专业，对接玻利维亚碳氢化合物与基础设施行业需求。",
        "parent_dept_id": None,
    },
    {
        "name": "Carreras sin área（直属专业·副校长代管）",
        "dept_id": None,
        "head": None,
        "description": "不隶属任何学部、由副校长代行部长管理的专业群：法律（年制）、政治学（年制）、系统工程（学期制）、物理与替代能源科学（学期制）。",
        "parent_dept_id": None,
    },
]

data["recent_events"] = [
    {
        "date": "2026-02-10",
        "title": "2026学年开学：确立科研立校与学业认证路线图",
        "description": "UPEA在埃尔阿尔托主校区以升旗仪式和特别大会开启2026学年。校长卡洛斯·孔多里表示大学「不仅在数量而且在质量上成长」，强调科研应为立校支柱；副校长埃弗拉因·钱比宣布4月前再认证3-4个学业单位、年底达到34个获CEUB认证单位（覆盖90%目标），并推进学术质量处（Departamento de Calidad Académica）建设。",
        "impact": "全年学术质量议程明确：认证单位从24个增至34个、新设学术质量处，将直接提升学历的国际互认与竞争力。",
        "source": "https://www.eabolivia.com/el-alto-noticias/29849-upea-apuesta-por-la-investigacion-cientifica-este-2026.html",
    },
    {
        "date": "2026-05-29",
        "title": "UPEA历史上首次获选为全国大学代表大会（XV Congreso）主办校",
        "description": "在第14届全国大学代表大会期间，玻利维亚大学体系确认UPEA将主办第15届全国大学代表大会（XV Congreso Nacional de Universidades），系建校26年来首次获此资格；同期CEUB完成新一届执行委员会改选。校方与官方媒体均称其为「历史性、开创性」的决定。",
        "impact": "确立UPEA在玻利维亚公立大学体系中的全国性地位，未来将承办大学体系最高决策会议，带动基础设施与学术形象提升。",
        "source": "https://www.eldiario.net/portal/2026/05/31/ceub-con-nuevo-ejecutivo/",
    },
    {
        "date": "2026-10-21",
        "title": "校长孔多里宣布联合大学体系编制「50/50」财税分成技术方案",
        "description": "校长卡洛斯·孔多里经RTP电视台表示，UPEA正与CEUB大学体系的各公立大学共同准备关于国家「50/50」税收共同参与分配方案的技术建议，目标是强化高等教育融资并改善大学基础设施。",
        "impact": "若国会采纳，公立大学将在国家财税分配中获得制度性份额，直接改善UPEA的经费与基建投入前景。",
        "source": "https://www.facebook.com/rtpbolivia/videos/el-rector-de-la-upea-carlos-condori-inform%C3%B3-que-la-universidad-prepara-una-propu/1751806449453092/",
    },
    {
        "date": "2026-10-23",
        "title": "与国家特别项目署（UPRE）签署实习与定向工作协议",
        "description": "UPEA与多民族国家政府特别项目署（UPRE）签署合作协定，高年级学生与毕业生可在UPRE执行的国家项目中开展实习与定向研究。UPRE署长恩里克·布鲁诺转达总统罗德里戈·帕斯关于政府与大学合作的指示；校长孔多里表示每年将选派最优秀学生参与。",
        "impact": "打通公立大学与国家项目部门的产学通道，为埃尔阿尔托青年提供实践与就业出口，契合新政府青年政策。",
        "source": "https://www.eabolivia.com/el-alto-noticias/30112-upea-y-upre-firman-convenio-para-que-universitarios-realicen-pasantias.html",
    },
    {
        "date": "2026-02-24",
        "title": "维亚查疏解校区举行2026学年开学典礼",
        "description": "UPEA在拉巴斯省维亚查市的疏解校区（sede desconcentrada de Viacha）举行2026学年开学典礼，校方致辞肯定校长孔多里主政下学校在基础设施与办学现代化方面的进展，展示学校向省会以外市镇延伸的多校区办学布局。",
        "impact": "巩固UPEA覆盖拉巴斯省十余市镇的分校网络，扩大高原地区居民的高等教育可及性。",
        "source": "https://www.facebook.com/upeatelevisioncanal25/videos/se-inaugur%C3%B3-la-gesti%C3%B3n-acad%C3%A9mica-2026-en-la-sede-desconcentrada-de-viacha-con-la/1455521502863084/",
    },
]

data["related_entities"] = [
    {
        "org_id": "BO-ACAD-001",
        "org_name": "圣安德烈斯大学 (Universidad Mayor de San Andrés, UMSA)",
        "org_type": "ACAD",
        "org_description": "拉巴斯市公立自治大学，玻利维亚历史最悠久、规模最大的高校之一。1989年曾与埃尔阿尔托社会机构签订协议设立技术类学部，为UPEA的直接前身。",
        "relationship_type": "predecessor",
    },
    {
        "org_id": "BO-GOV-008",
        "org_name": "玻利维亚教育部 (Ministerio de Educación)",
        "org_type": "GOV",
        "org_description": "玻利维亚主管教育政策的中央政府部门。依2000年第2115号创设法，在UPEA获得自治前曾通过机构发展委员会（CDI）参与其治理。",
        "relationship_type": "affiliated",
    },
    {
        "org_id": None,
        "org_name": "玻利维亚大学执行委员会 (Comité Ejecutivo de la Universidad Boliviana, CEUB)",
        "org_type": "ACAD",
        "org_description": "玻利维亚公立自治大学体系的协调与决策机构，负责学业单位认证及全国大学代表大会（Congreso Nacional de Universidades）的召集。",
        "relationship_type": "member_of",
    },
    {
        "org_id": None,
        "org_name": "国家特别项目署 (Unidad de Proyectos Especiales, UPRE)",
        "org_type": "GOV",
        "org_description": "多民族国家政府下属特别项目执行单位，在总统罗德里戈·帕斯政府期间奉命与大学开展合作。",
        "relationship_type": "partner",
    },
]

data["core_business"] = (
    "埃尔阿尔托公立大学（UPEA）是玻利维亚拉巴斯省埃尔阿尔托市的公立自治大学，2000年9月5日依据第2115号法律、"
    "在埃尔阿尔托市民长期社会运动推动下创建，2003年11月经修法确认大学自治。学校实行教师—学生共治制度，由校长、"
    "副校长、各学部部长（Decano）及各专业主任构成管理体系。学术上设8个学部（健康科学、工程技术与生产发展、经济与金融、"
    "农业科学、社会科学、教育科学、人居科学与艺术、科学技术），另有法律、政治学、系统工程、物理与替代能源等直属专业，"
    "共37个本科专业，覆盖医学、工程、社会经济与技术领域；并在维亚查、阿查卡奇、卡拉纳维、索拉塔等拉巴斯省多个市镇设有"
    "十余处分校。截至2017年注册学生47861人、毕业8578人，目前约5.5万人在读，是玻利维亚规模增长最快的公立大学之一。"
    "学校近年以科研和学术认证为战略重点：截至2026年初已有24个学业单位获CEUB认证，目标年底达34个；2026年5月更首次获选"
    "为全国大学代表大会（XV Congreso）主办校。经费主要依赖国家预算，2018年经学生动员促成国会增拨7000万玻利维亚诺。"
)

data["apec_stance"] = (
    "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入），UPEA与APEC机制不存在直接关联。"
    "作为玻利维亚公立高校，UPEA的对外合作主要在西班牙语美洲框架内展开：国内层面通过玻利维亚大学执行委员会（CEUB）"
    "参与大学体系协调，机构层面则与政府部门（如国家特别项目署UPRE）签署实习合作协议；本次检索未见其发布任何与APEC"
    "相关的立场文件、研究项目或合作安排。"
)

cm = data["collection_meta"]
cm["collection_date"] = "2026-10-24"
cm["phase"] = "phase3_enriched"
cm["data_sources"] = [
    "wikidata",
    "wikipedia",
    "official_website",
    "eabolivia.com",
    "eldiario.net",
    "rtpbolivia (Facebook)",
    "UPEA Televisión (Facebook)",
    "noticiasfides.com",
    "cepabol.noticias.bo",
]
cm["notes"] = (
    "Phase 3 enrichment: rector Carlos Condori Titirico and vicerrector Efraín Chambi Vargas verified via "
    "Spanish Wikipedia infobox plus 2026 press (eabolivia, RTP). Departments (8 areas + direct-report careers) "
    "and regional sedes from Wikipedia. Recent events (2026 academic opening & accreditation roadmap, XV Congreso "
    "host designation, 50/50 budget proposal, UPRE internship agreement) corroborated by at least one mainstream "
    "source each; key facts cross-checked with 2+ independent sources where available. Person IDs left null: no "
    "entries in _name_index.json for Condori/Chambi."
)
cm["quotes"] = [
    {
        "title": "UPEA apuesta por la investigación científica este 2026",
        "url": "https://www.eabolivia.com/el-alto-noticias/29849-upea-apuesta-por-la-investigacion-cientifica-este-2026.html",
    },
    {
        "title": "UPEA y UPRE firman convenio para que universitarios realicen pasantías",
        "url": "https://www.eabolivia.com/el-alto-noticias/30112-upea-y-upre-firman-convenio-para-que-universitarios-realicen-pasantias.html",
    },
    {
        "title": "CEUB con nuevo ejecutivo (confirma UPEA sede del XV Congreso de Universidades)",
        "url": "https://www.eldiario.net/portal/2026/05/31/ceub-con-nuevo-ejecutivo/",
    },
    {
        "title": "El rector de la UPEA, Carlos Condori: propuesta técnica sobre el 50-50 junto a las universidades del CEUB",
        "url": "https://www.facebook.com/rtpbolivia/videos/el-rector-de-la-upea-carlos-condori-inform%C3%B3-que-la-universidad-prepara-una-propu/1751806449453092/",
    },
]

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("OK - written", PATH)

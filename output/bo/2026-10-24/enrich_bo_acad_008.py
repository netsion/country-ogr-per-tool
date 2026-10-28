# -*- coding: utf-8 -*-
"""Enrich BO-ACAD-008 (Universidad Católica Boliviana San Pablo) profile JSON."""
import json

OUT = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/orgs/BO-ACAD-008.json"

with open(OUT, "r", encoding="utf-8") as f:
    data = json.load(f)

# ---------- basic_info ----------
data["basic_info"]["name_zh"] = "玻利维亚圣保罗天主教大学"
data["basic_info"]["founded_date"] = "1966-07-16"
aliases = set(data["basic_info"].get("aliases") or [])
aliases.update(["UCB", "Universidad Católica Boliviana", "La Cato",
                "Bolivian Catholic University San Pablo"])
data["basic_info"]["aliases"] = sorted(aliases)

# ---------- social_accounts ----------
data["social_accounts"] = [
    {
        "platform": "facebook",
        "account_name": "UCB - Sede La Paz (@UCB.BOLIVIA)",
        "url": "https://www.facebook.com/UCB.BOLIVIA",
        "source": "facebook.com（约15万关注，官方认证主页）+ lpz.ucb.edu.bo 页脚"
    },
    {
        "platform": "instagram",
        "account_name": "@ucbnacional",
        "url": "https://www.instagram.com/ucbnacional/",
        "source": "instagram.com（UCB 全国官方账号）"
    },
    {
        "platform": "instagram",
        "account_name": "@ucbsantacruz",
        "url": "https://www.instagram.com/ucbsantacruz/",
        "source": "instagram.com（圣克鲁斯校区官方账号，约1.7万粉丝）"
    },
    {
        "platform": "twitter_x",
        "account_name": "@ucatolicasc",
        "url": "https://x.com/ucatolicasc",
        "source": "x.com（圣克鲁斯校区官方账号）"
    },
    {
        "platform": "linkedin",
        "account_name": "Universidad Católica Boliviana - UCB",
        "url": "https://bo.linkedin.com/company/universidad-catolica-boliviana-san-pablo-regional-la-paz",
        "source": "linkedin.com（官方公司主页，约5900关注）"
    },
    {
        "platform": "youtube",
        "account_name": "Universidad Católica - UCB Santa Cruz (@ucbsantacruzbo)",
        "url": "https://www.youtube.com/@ucbsantacruzbo",
        "source": "youtube.com（圣克鲁斯校区官方频道）"
    }
]

# ---------- digital_assets ----------
data["digital_assets"] = [
    {
        "name": "拉巴斯校区门户网站",
        "url": "https://lpz.ucb.edu.bo/",
        "description": "UCB 主校区官方网站，发布校区新闻、招生、院系与学术信息",
        "source": "es.wikipedia.org + www.ucb.edu.bo"
    },
    {
        "name": "科恰班巴校区门户网站",
        "url": "https://cba.ucb.edu.bo/",
        "description": "UCB 科恰班巴校区官网（1971年设立的第二个校区）",
        "source": "es.wikipedia.org + www.ucb.edu.bo"
    },
    {
        "name": "圣克鲁斯校区门户网站",
        "url": "https://www.scz.ucb.edu.bo/",
        "description": "UCB 圣克鲁斯-德拉谢拉校区官网",
        "source": "es.wikipedia.org + www.ucb.edu.bo"
    },
    {
        "name": "塔里哈校区门户网站",
        "url": "https://tja.ucb.edu.bo/",
        "description": "UCB 塔里哈校区官网",
        "source": "es.wikipedia.org + www.ucb.edu.bo"
    },
    {
        "name": "UCB Santa Cruz YouTube 频道",
        "url": "https://www.youtube.com/@ucbsantacruzbo",
        "description": "UCB 圣克鲁斯校区官方视频频道，发布学术活动与宣传内容",
        "source": "youtube.com"
    }
]

# ---------- key_people ----------
data["key_people"] = [
    {
        "person_id": None,
        "name": "何塞·富恩特斯·卡诺 (P. José Fuentes Cano)",
        "title": "国家校长（Rector Nacional）",
        "title_description": "天主教神父（Padre），2021年4月在玻利维亚主教大会（CEB）第108届大会（科恰班巴）上被任命为 UCB 国家校长，任职至今",
        "description": "自2021年起统辖 UCB 全国四个校区及神学学部；2025年10月获西班牙国王费利佩六世授予民事功绩勋章十字勋章（Cruz Oficial de la Orden del Mérito Civil）；2026年10月代表 UCB 与玻利维亚航天局签署纳米卫星合作协议，并推动玻利维亚首部空间法的学术倡议。"
    },
    {
        "person_id": None,
        "name": "莫妮卡·达萨 (Mónica Daza)",
        "title": "国家学术副校长（Vicerrectora Académica Nacional）",
        "title_description": "博士（Dra.），负责全国学术事务",
        "description": "2025年8月以国家学术副校长身份出席 UCB 官方活动并发表讲话（官网新闻）。"
    },
    {
        "person_id": None,
        "name": "希梅娜·佩雷斯·阿雷纳斯 (Ximena Peres Arenas)",
        "title": "拉巴斯校区校长（Rectora Sede La Paz）",
        "title_description": "博士（Dra.），2025年6月被任命为拉巴斯校区校长",
        "description": "领导 UCB 主校区拉巴斯校区的学术与管理工作，2025年6月经官网正式宣布就任。"
    }
]

# ---------- departments ----------
data["departments"] = [
    {
        "name": "拉巴斯校区 (Sede La Paz)",
        "dept_id": None,
        "head": "希梅娜·佩雷斯·阿雷纳斯 (Ximena Peres Arenas)",
        "description": "UCB 总部所在地及主校区，1966年建校之地，位于拉巴斯市；在校生规模最大，设六大院系与中央图书馆（2006年建成，6层、200个阅读座位）",
        "parent_dept_id": None
    },
    {
        "name": "科恰班巴校区 (Sede Cochabamba)",
        "dept_id": None,
        "head": None,
        "description": "UCB 第二个校区，1971年2月26日正式启动（以哲学专业开学）；设有圣保罗神学学部与 Seton 护理学部",
        "parent_dept_id": None
    },
    {
        "name": "圣克鲁斯校区 (Sede Santa Cruz)",
        "dept_id": None,
        "head": None,
        "description": "UCB 圣克鲁斯-德拉谢拉校区，医学与牙医学等专业获 ARCU-SUR（MERCOSUR）区域认证",
        "parent_dept_id": None
    },
    {
        "name": "塔里哈校区 (Sede Tarija)",
        "dept_id": None,
        "head": None,
        "description": "UCB 塔里哈校区，开设约15个本科专业，学生团队曾获 2025 年 Banco Unión 全国黑客松冠军",
        "parent_dept_id": None
    },
    {
        "name": "拉普拉塔学术校区 (Sede La Plata, Sucre)",
        "dept_id": None,
        "head": None,
        "description": "位于国家首都苏克雷的学术校区，由已故大主教、UCB 大校长蒙斯·里卡多·森特利亚斯大力推动设立",
        "parent_dept_id": None
    },
    {
        "name": "矿坑圣母校区 (Sede Virgen del Socavón, Oruro)",
        "dept_id": None,
        "head": None,
        "description": "位于奥鲁罗的校区，以奥鲁罗主保圣人'矿坑圣母'命名",
        "parent_dept_id": None
    },
    {
        "name": "经济、管理与金融学部 (Facultad de Ciencias Económicas, Administrativas y Financieras)",
        "dept_id": None,
        "head": None,
        "description": "开设工商管理、经济学、公共会计、商业工程、旅游管理、金融工程、营销与数字媒体、经济与商业智能等专业",
        "parent_dept_id": None
    },
    {
        "name": "社会科学与人类学部 (Facultad de Ciencias Sociales y Humanas)",
        "dept_id": None,
        "head": None,
        "description": "开设社会传播、人类学、哲学与文学、神学、心理学、心理教育学等专业",
        "parent_dept_id": None
    },
    {
        "name": "法律与政治科学学部 (Facultad de Derecho y Ciencias Políticas)",
        "dept_id": None,
        "head": None,
        "description": "开设法学与政治学及国际关系专业；学生辩论队多次在国际模拟法庭竞赛中获奖",
        "parent_dept_id": None
    },
    {
        "name": "工程学部 (Facultad de Ingeniería)",
        "dept_id": None,
        "head": None,
        "description": "开设环境、生物医学、土木、系统/软件、电信、工业、机电一体化、化学、生物技术、农业企业、物联网、能源、生物化学与生物工程等专业；Waskiri Sat 纳米卫星项目由该学部机电一体化专业团队主导",
        "parent_dept_id": None
    },
    {
        "name": "建筑与平面设计系 (Departamento de Arquitectura y Diseño Gráfico)",
        "dept_id": None,
        "head": None,
        "description": "开设建筑学、室内建筑、平面设计与数字设计专业",
        "parent_dept_id": None
    },
    {
        "name": "健康系 (Departamento de Salud)",
        "dept_id": None,
        "head": None,
        "description": "开设医学、牙医学、运动机能学与物理治疗、护理学专业；其国际培训中心（ITC）2026年1月获美国心脏协会（AHA）认证",
        "parent_dept_id": None
    },
    {
        "name": "生产与竞争力学院 (Escuela de la Producción y la Competitividad, ePC)",
        "dept_id": None,
        "head": None,
        "description": "位于拉巴斯的精英学院，聚焦创业、企业发展与国际商务，开设商业与数据科学、国际商务、企业创建等课程，是玻利维亚学术层次最高的商科项目之一",
        "parent_dept_id": None
    },
    {
        "name": "圣保罗神学学部 (Facultad de Teología \"San Pablo\")",
        "dept_id": None,
        "head": None,
        "description": "UCB 依托天主教会背景设立的神学学部（科恰班巴），2026年10月举办'受造物的灵性'跨大洲神学大会，回应气候变化挑战",
        "parent_dept_id": None
    }
]

# ---------- recent_events ----------
data["recent_events"] = [
    {
        "date": "2026-10-14",
        "title": "UCB 将于2028年11月发射玻利维亚首颗纳米卫星 Waskiri Sat",
        "description": "2026年10月13日，UCB 在埃尔阿尔托 Amachuma 地面站与玻利维亚航天局（ABE）签署机构间合作协议：ABE 提供地面段基础设施、技术设备与专业人员，UCB 主导卫星设计与项目管理。纳米卫星 Waskiri Sat（意为'好学的孩子'）由拉巴斯校区机电一体化专业毕业生及在校生团队建造，用于地球观测、环境研究与自然灾害预防；双方还签署谅解备忘录，共同推动玻利维亚首部《空间法》的制定。",
        "impact": "国家级里程碑——玻利维亚首颗由大学主导研制的纳米卫星，确立 UCB 在本国 STEM 与航天科技教育领域的领先地位，并为国家空间立法提供学术支撑",
        "source": "https://www.ucb.edu.bo/hito-historico-la-u-c-b-pondra-en-orbita-el-primer-nanosatelite-boliviano-en-noviembre-de-2028/"
    },
    {
        "date": "2026-09-24",
        "title": "大学大校长蒙斯·里卡多·森特利亚斯逝世，大校长职位空缺",
        "description": "UCB 大校长（Gran Canciller）、苏克雷大主教蒙斯·里卡多·埃内斯托·森特利亚斯·古斯曼（Ricardo Ernesto Centellas Guzmán，1962-2026）在奥鲁罗逝世。他于2024年11月经玻利维亚主教授予当选 UCB 大校长，2015-2021年曾任玻利维亚主教大会主席，是苏克雷拉普拉塔学术校区设立的主要推动者。",
        "impact": "中高——UCB 教会治理最高职位出现空缺，新任大校长人选有待玻利维亚主教大会决定，为教会-大学关系带来不确定性",
        "source": "https://www.ucb.edu.bo/en-memoria-de-nuestro-gran-canciller-mons-ricardo-centellas-1962-2026/"
    },
    {
        "date": "2026-03-11",
        "title": "拉巴斯与圣克鲁斯校区获 MERCOSUR 大学课程区域认证（ARCU-SUR）",
        "description": "2026年3月11日（星期三），UCB 拉巴斯与圣克鲁斯校区正式获颁南共市大学课程区域认证体系（ARCU-SUR）证书，工业工程等专业获得区域认证；此前圣克鲁斯校区医学、牙医学专业亦完成 ARCU-SUR 六年期再认证。认证证书由玻利维亚教育部颁发。",
        "impact": "中高——专业课程获南共市成员国（含智利）互认，提升学历国际流动性与 UCB 国际化水平",
        "source": "https://lpz.ucb.edu.bo/ingenieria-industrial-de-la-ucb-recibe-la-acreditacion-ante-el-sistema-arcu-sur-mercosur/"
    },
    {
        "date": "2026-01-13",
        "title": "获美国心脏协会（AHA）国际培训中心认证，为玻利维亚大学中唯一",
        "description": "UCB 国际培训中心（ITC）正式获得美国心脏协会（American Heart Association）认证，成为玻利维亚唯一获此全球心血管急救培训权威机构认证的大学，标志着本国健康培训领域的重要里程碑。",
        "impact": "中高——在医疗急救培训领域形成全国独家资质，强化健康系与医学专业的竞争优势",
        "source": "https://elpais.bo/tarija/20260113_la-ucb-marca-un-hito-en-la-salud-boliviana-al-obtener-la-acreditacion-internacional-de-la-american-heart-association.html"
    },
    {
        "date": "2025-10-23",
        "title": "西班牙国王费利佩六世授予国家校长民事功绩勋章十字勋章",
        "description": "西班牙国王费利佩六世授予 UCB 国家校长何塞·富恩特斯·卡诺神父民事功绩勋章十字勋章（Cruz Oficial de la Orden del Mérito Civil），表彰其对教育与西班牙语世界文化交流的贡献。",
        "impact": "中——国际层面对 UCB 及其领导层的认可，体现其与西班牙学术界的紧密联系",
        "source": "https://www.ucb.edu.bo/el-rey-felipe-vi-condecora-al-rector-nacional-de-la-u-c-b-con-la-cruz-oficial-de-la-orden-del-merito-civil/"
    }
]

# ---------- related_entities ----------
data["related_entities"] = [
    {
        "org_id": "BO-GOV-035",
        "org_name": "玻利维亚航天局 (Agencia Boliviana Espacial)",
        "org_type": "government_agency",
        "org_description": "负责玻利维亚航天活动与空间基础设施的国家机构，运营位于埃尔阿尔托的 Amachuma 地面站",
        "relationship_type": "strategic_alliance"
    },
    {
        "org_id": "BO-GOV-008",
        "org_name": "玻利维亚教育部 (Ministerio de Educación)",
        "org_type": "government_ministry",
        "org_description": "高等教育主管部门，负责大学课程质量认证并向 UCB 颁发 MERCOSUR ARCU-SUR 区域认证证书",
        "relationship_type": "regulator"
    },
    {
        "org_id": None,
        "org_name": "玻利维亚主教大会 (Conferencia Episcopal Boliviana)",
        "org_type": "religious_organization",
        "org_description": "玻利维亚天主教会主教团，UCB 的创立与主管机构，负责任命大学国家校长与大校长",
        "relationship_type": "parent_org"
    },
    {
        "org_id": "BO-ACAD-001",
        "org_name": "圣安德烈斯大学 (Universidad Mayor de San Andrés)",
        "org_type": "university",
        "org_description": "玻利维亚规模最大的公立大学（拉巴斯），与 UCB 同属玻利维亚大学体系（Sistema de la Universidad Boliviana）",
        "relationship_type": "sibling"
    },
    {
        "org_id": None,
        "org_name": "美国心脏协会 (American Heart Association)",
        "org_type": "international_organization",
        "org_description": "全球心血管急救培训标准制定机构，2026年1月认证 UCB 国际培训中心（ITC）",
        "relationship_type": "partner"
    }
]

# ---------- core_business / apec_stance ----------
data["core_business"] = (
    "玻利维亚圣保罗天主教大学（UCB）是玻利维亚最主要的天主教会私立大学，1966年由热纳罗·普拉塔·武洛蒙席"
    "（Monseñor Gennaro Prata Vuolo）创立，隶属玻利维亚主教大会，1994年经法律确认为享有学术与经济自治的公法机构，"
    "并纳入玻利维亚大学体系（Sistema de la Universidad Boliviana）。总部位于拉巴斯，在科恰班巴、圣克鲁斯、塔里哈、"
    "苏克雷（La Plata）和奥鲁罗设有校区，并在农村地区设有多所农民学术单位（Unidades Académicas Campesinas）。"
    "设经济管理与金融、社会科学与人文、法律与政治科学、工程、建筑与平面设计、健康六大院系，另有圣保罗神学学部和"
    "生产与竞争力学院（ePC），提供52个本科专业（85个本科项目）及研究生课程，现有本科生约1.7万人、研究生约2000人。"
    "设有民主研究所、社会经济研究所等数十个研究机构，2022年QS世界大学排名将其列为玻利维亚最佳与最具声望的大学。"
    "课程获国内认证及 MERCOSUR ARCU-SUR 区域认证，健康培训中心获美国心脏协会认证，并主导玻利维亚首颗大学纳米卫星"
    "Waskiri Sat 项目，2028年拟发射入轨。"
)
data["apec_stance"] = "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。"

# ---------- collection_meta ----------
data["collection_meta"] = {
    "collection_date": "2026-10-24",
    "phase": "phase3_enriched",
    "data_sources": [
        "wikidata",
        "es.wikipedia.org",
        "www.ucb.edu.bo",
        "lpz.ucb.edu.bo",
        "ceb.bo",
        "elpais.bo",
        "facebook.com",
        "instagram.com",
        "x.com",
        "linkedin.com",
        "youtube.com",
        "search_engine"
    ],
    "completeness_score": 85,
    "quotes": [
        {
            "title": "¡Hito Histórico! La U.C.B. pondrá en órbita el primer nanosatélite boliviano en noviembre de 2028",
            "url": "https://www.ucb.edu.bo/hito-historico-la-u-c-b-pondra-en-orbita-el-primer-nanosatelite-boliviano-en-noviembre-de-2028/"
        },
        {
            "title": "En memoria de nuestro Gran Canciller: Mons. Ricardo Centellas (1962-2026)",
            "url": "https://www.ucb.edu.bo/en-memoria-de-nuestro-gran-canciller-mons-ricardo-centellas-1962-2026/"
        },
        {
            "title": "La carrera de Ingeniería Industrial de la UCB recibe la acreditación ante el Sistema ARCU-SUR (MERCOSUR)",
            "url": "https://lpz.ucb.edu.bo/ingenieria-industrial-de-la-ucb-recibe-la-acreditacion-ante-el-sistema-arcu-sur-mercosur/"
        },
        {
            "title": "La UCB marca un hito en la salud boliviana al obtener la acreditación internacional de la American Heart Association",
            "url": "https://elpais.bo/tarija/20260113_la-ucb-marca-un-hito-en-la-salud-boliviana-al-obtener-la-acreditacion-internacional-de-la-american-heart-association.html"
        }
    ],
    "notes": "Phase3 enrichment 2026-10-24: rector confirmed via 2026-10 official news (P. José Fuentes Cano, in office since 2021-04); Gran Canciller vacant after death of Mons. Ricardo Centellas (2026-09); person_id/dept_id null where name_index has no entry; ID registry untouched."
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("WROTE", OUT)
print("key_people:", len(data["key_people"]), "| departments:", len(data["departments"]),
      "| recent_events:", len(data["recent_events"]), "| related_entities:", len(data["related_entities"]),
      "| social:", len(data["social_accounts"]), "| assets:", len(data["digital_assets"]))

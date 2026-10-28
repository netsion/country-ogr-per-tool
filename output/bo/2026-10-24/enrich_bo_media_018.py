#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enrich BO-MEDIA-018 (Agencia de Noticias Fides) phase3 profile."""
import json

FP = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\orgs\BO-MEDIA-018.json"

with open(FP, encoding="utf-8") as f:
    data = json.load(f)

# ---------- basic_info ----------
data["basic_info"]["name_zh"] = "菲德斯通讯社"
data["basic_info"]["name_en"] = "Agencia de Noticias Fides"
data["basic_info"]["aliases"] = ["ANF", "Noticias Fides", "Agencia Fides", "Agencia de Noticias Fides (ANF)"]
data["basic_info"]["founded_date"] = "1963-08-05"
data["basic_info"]["website"] = "https://www.noticiasfides.com"
data["basic_info"]["org_subtype"] = "news_agency"

# ---------- social_accounts ----------
data["social_accounts"] = [
    {
        "platform": "facebook",
        "account_name": "ANF Noticias Fides (@ANFidesBolivia)",
        "url": "https://www.facebook.com/ANFidesBolivia/",
        "source": "noticiasfides.com 页脚及 Facebook 认证主页（约44万粉丝）"
    },
    {
        "platform": "twitter_x",
        "account_name": "@noticiasfides",
        "url": "https://x.com/noticiasfides",
        "source": "noticiasfides.com 页脚"
    },
    {
        "platform": "instagram",
        "account_name": "@noticiasfides",
        "url": "https://www.instagram.com/noticiasfides/",
        "source": "ANF 官方 Instagram 帖子（2026-08-05 周年帖等）"
    },
    {
        "platform": "youtube",
        "account_name": "Agencia de Noticias Fides (@agenciadenoticiasfides2497)",
        "url": "https://www.youtube.com/@agenciadenoticiasfides2497",
        "source": "noticiasfides.com 页脚及 YouTube 频道页"
    },
    {
        "platform": "tiktok",
        "account_name": "ANF Noticias Fides (@noticiasfides)",
        "url": "https://www.tiktok.com/@noticiasfides",
        "source": "TikTok 官方账号页（约9.4万粉丝、190万点赞）"
    }
]

# ---------- digital_assets ----------
data["digital_assets"] = [
    {
        "name": "ANF 数字新闻门户（noticiasfides.com）",
        "url": "https://www.noticiasfides.com/",
        "description": "ANF 官方网站，2019年12月机构重组后成为主要发布平台，设政治、经济、社会、安全、司法、民主、可持续发展、原住民、创新与教育等频道，另设视频中心（Videos ANF）、意见专栏和新闻检索器（Buscador）。",
        "source": "https://www.noticiasfides.com/"
    }
]

# ---------- key_people ----------
data["key_people"] = [
    {
        "person_id": "BO-PERSON-000410",
        "name": "塞尔希奥·蒙特斯（Sergio Montes, S.J.）",
        "name_en": "Sergio Montes Rondón",
        "title": "总裁 / 台长（Director General）",
        "title_description": "ANF 及菲德斯集团（Grupo Fides）最高负责人",
        "description": "玻利维亚耶稣会神父。2013年5月3日被任命为 ANF 总裁，接替创始人何塞·格拉蒙特·德·莫拉加斯神父，任职至今（LinkedIn 及西语维基百科均列其为现任总裁）。曾先后执掌《Cuarto Intermedio》杂志、菲德斯电台（Radio Fides）、圣克鲁斯电台（Radio Santa Cruz）。2024年12月23日又获耶稣会玻利维亚省省会长贝尔纳多·梅尔卡多神父任命兼任 Radio Fides 台长。毕业于玻利维亚天主教大学（哲学、神学、政治学）和西班牙纳瓦拉大学。2025年12月5日获拉巴斯记者协会（APLP）颁发的爱德华多·佩雷斯·伊里瓦内奖章（媒体创新与管理类）。"
    },
    {
        "person_id": "BO-PERSON-000411",
        "name": "南希·瓦卡弗洛尔（Nancy Vacaflor）",
        "name_en": "Nancy Vacaflor",
        "title": "信息总监（Directora Informativa del Grupo Fides）",
        "title_description": "统筹 ANF 与 Radio Fides 编辑内容的资深新闻主管",
        "description": "菲德斯集团信息总监，长期主管 ANF 编辑业务。2019年玻利维亚政治危机后，曾以通讯社新闻主管（jefa de prensa）身份代表 ANF 与阿涅斯临时政府签订合作协议（据西语维基百科，该协议当时引发争议）。2025年12月代表身在异地的总裁塞尔希奥·蒙特斯领取拉巴斯记者协会奖章。"
    },
    {
        "person_id": None,
        "name": "何塞·格拉蒙特·德·莫拉加斯（José Gramunt de Moragas, S.J.）",
        "name_en": "José Gramunt de Moragas",
        "title": "创始人（已故）",
        "title_description": "ANF 创办人、首任总裁",
        "description": "西班牙裔耶稣会神父兼记者，1963年8月5日在拉巴斯创立玻利维亚第一家通讯社 ANF 并长期担任总裁，直至2013年5月由塞尔希奥·蒙特斯接任（已去世，官方介绍中标注 +）。"
    }
]

# ---------- departments ----------
data["departments"] = [
    {
        "name": "政治报道部（Política）",
        "dept_id": None,
        "head": None,
        "description": "负责国内政治、政党、国会与民主制度报道，为官网核心频道之一。",
        "parent_dept_id": None
    },
    {
        "name": "经济报道部（Economía）",
        "dept_id": None,
        "head": None,
        "description": "负责宏观经济、财政、燃料与物价、企业及货币政策等经济新闻。",
        "parent_dept_id": None
    },
    {
        "name": "安全与司法报道部（Seguridad / Justicia）",
        "dept_id": None,
        "head": None,
        "description": "负责治安、禁毒、检调司法与反腐议题报道。",
        "parent_dept_id": None
    },
    {
        "name": "社会报道部（Sociedad，含人权/原住民/可持续发展）",
        "dept_id": None,
        "head": None,
        "description": "覆盖社会、健康、教育、人权、原住民（Pueblos Indígenas）、可持续发展（Desarrollo Sostenible）及妇女儿童与老年人议题，设有\"妇女、儿童与老年人\"等专栏。",
        "parent_dept_id": None
    },
    {
        "name": "国际报道部（Mundo）",
        "dept_id": None,
        "head": None,
        "description": "编译国际新闻，服务玻利维亚读者。",
        "parent_dept_id": None
    },
    {
        "name": "评论与视听部（Opinión / Videos）",
        "dept_id": None,
        "head": None,
        "description": "运营社论（Editorial ANF）、外部专栏作者网络及视频产品（含 Hablar de Bolivia con una taza de café 等栏目）。",
        "parent_dept_id": None
    }
]

# ---------- recent_events ----------
data["recent_events"] = [
    {
        "date": "2026-08-05",
        "title": "ANF 庆祝创立63周年",
        "description": "ANF 在官网、Facebook、Instagram、YouTube 等平台庆祝创立63周年（1963年8月5日由耶稣会神父何塞·格拉蒙特·德·莫拉加斯创立），重申63年独立报道与服务玻利维亚的承诺。",
        "impact": "巩固其作为玻利维亚最古老通讯社的品牌公信力，展示跨数字平台的持续运营与影响力。",
        "source": "https://www.instagram.com/p/Db2B5unEZbu/"
    },
    {
        "date": "2026-03-22",
        "title": "Fides en las Ánforas 地方选举特别报道",
        "description": "3月22日玻利维亚地方选举日，菲德斯集团（含 ANF）启动\"Fides en las Ánforas\"选举特别报道，部署采编团队提供投票进程与计票信息（4月19日第二轮选举延续了该报道机制）。",
        "impact": "强化 ANF 在选举报道领域的专业形象，扩大其数字平台受众触达。",
        "source": "https://www.facebook.com/ANFidesBolivia/videos/1856819735706614/"
    },
    {
        "date": "2025-12-05",
        "title": "总裁塞尔希奥·蒙特斯获拉巴斯记者协会奖章",
        "description": "拉巴斯记者协会（APLP）向菲德斯集团总裁、ANF 台长塞尔希奥·蒙特斯神父授予爱德华多·佩雷斯·伊里瓦内奖章（媒体创新与管理卓越奖），奖章由信息总监南希·瓦卡弗洛尔代领；Radio Fides 主持人约翰·阿兰迪亚同场获阿德拉·萨穆迪奥职业轨迹奖章。",
        "impact": "行业机构对 ANF/菲德斯集团媒体管理创新的正式认可，提升机构声誉。",
        "source": "https://www.noticiasfides.com/democracia/sergio-montes-y-john-arandia-del-grupo-fides-fueron-distinguidos-por-la-asociacion-de-periodistas-de-la-paz"
    },
    {
        "date": "2025-10-19",
        "title": "总统大选第二轮投票特别报道",
        "description": "10月19日玻利维亚总统大选第二轮投票日，菲德斯集团（含 ANF）启动\"Fides en las Ánforas\"特别报道，实时提供选举信息；此前的8月17日首轮投票亦进行了同类特别报道。",
        "impact": "在2025年玻利维亚大选周期（政局重大变动）中提供全流程选举新闻服务，巩固其全国性通讯社地位。",
        "source": "https://www.facebook.com/RadioFidesBolivia/posts/1252470680244810/"
    },
    {
        "date": "2024-12-23",
        "title": "耶稣会任命塞尔希奥·蒙特斯兼任 Radio Fides 台长",
        "description": "玻利维亚耶稣会省省会长贝尔纳多·梅尔卡多神父任命时任 ANF 总裁的塞尔希奥·蒙特斯神父兼任 Radio Fides 台长，ANF 与 Radio Fides自此由同一负责人领导（菲德斯集团一体化管理）。",
        "impact": "强化 ANF 与 Radio Fides 的集团化协同，为2025-2026年集团统一选举报道与获奖奠定组织基础。",
        "source": "https://www.jesuitas.org.bo/noticias/provincial-de-la-compania-de-jesus-nombra-al-p-sergio-montes-sj-director-de-radio-fides-bolivia"
    }
]

# ---------- related_entities ----------
data["related_entities"] = [
    {
        "org_id": "BO-MEDIA-014",
        "org_name": "Radio Fides（菲德斯电台）",
        "org_type": "MEDIA",
        "org_description": "玻利维亚耶稣会经营的知名私营广播电台，与 ANF 同属菲德斯集团（Grupo Fides）。ANF 初创时隶属 Radio Fides 新闻服务，1970年代末独立；2024年12月起两机构由塞尔希奥·蒙特斯统一领导。",
        "relationship_type": "sibling"
    },
    {
        "org_id": "BO-GOV-032",
        "org_name": "ATT（玻利维亚电信与交通运输监管审计局）",
        "org_type": "GOV",
        "org_description": "玻利维亚电信、广播频率与交通运输监管机构，菲德斯集团的广播及媒体信号传输业务处于其监管框架之下。",
        "relationship_type": "regulated_by"
    },
    {
        "org_id": None,
        "org_name": "Compañía de Jesús en Bolivia（玻利维亚耶稣会）",
        "org_type": "NGO",
        "org_description": "天主教耶稣会玻利维亚省，ANF 的创办者与所属母体；ANF 是其非营利社会传播事业（apostolate）之一。",
        "relationship_type": "parent_org"
    }
]

# ---------- core_business / apec_stance / industries ----------
data["core_business"] = (
    "菲德斯通讯社（Agencia de Noticias Fides，ANF）是玻利维亚第一家、也是历史最悠久的通讯社，"
    "1963年8月5日由耶稣会神父何塞·格拉蒙特·德·莫拉加斯（José Gramunt de Moragas, S.J.）在拉巴斯创立，"
    "是玻利维亚耶稣会（Compañía de Jesús）的非营利社会传播事业。其核心业务为面向全国新闻媒体的通讯社通稿服务："
    "每日以西班牙语发布政治、经济、社会、安全、司法、民主选举、人权、原住民、可持续发展等领域的文字新闻与新闻图片，"
    "订户覆盖全国50余家报纸、电台和电视台；同时运营数字新闻门户 noticiasfides.com（2019年12月机构重组后转为纯数字发布），"
    "并生产视频、评论专栏及\"AND\"软性特刊等内容。编辑总部位于拉巴斯（Av. Sucre #853, Zona Norte），"
    "在圣克鲁斯、科恰班巴等主要城市设有记者网络。ANF 与菲德斯电台（Radio Fides）同属\"菲德斯集团\"（Grupo Fides）媒体体系，"
    "共享总裁与信息总监资源，凭借六十余年的独立报道在玻利维亚私营媒体界具有较高公信力与行业影响力。"
)
data["apec_stance"] = (
    "玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。因此 ANF 作为玻利维亚媒体机构"
    "不直接参与APEC事务，公开资料中亦未检索到该机构针对APEC的专门立场或报道专题。"
)
data["industries"] = ["broadcasting", "media_publishing", "digital_media", "nonprofit"]

# ---------- collection_meta ----------
data["collection_meta"] = {
    "collection_date": "2026-10-24",
    "phase": "phase3_enriched",
    "data_sources": [
        "wikidata",
        "wikipedia",
        "noticiasfides.com",
        "es.wikipedia.org",
        "en.wikipedia.org",
        "jesuitas.org.bo",
        "urgente.bo",
        "facebook.com/ANFidesBolivia",
        "x.com/noticiasfides",
        "instagram.com/noticiasfides",
        "youtube.com/@agenciadenoticiasfides2497",
        "tiktok.com/@noticiasfides",
        "bo.linkedin.com"
    ],
    "quotes": [
        {
            "title": "Quiénes somos - ANF Agencia de Noticias Fides Bolivia（官网关于页：1963年由耶稣会创立、玻利维亚第一家通讯社）",
            "url": "https://www.noticiasfides.com/paginas/anf/quienes-somos"
        },
        {
            "title": "El sacerdote Sergio Montes, nuevo director de la Agencia Fides - ANF（2013-05-03 蒙特斯接任总裁）",
            "url": "https://www.noticiasfides.com/nacional/sociedad/el-sacerdote-sergio-montes-nuevo-director-de-la-agencia-fides-330266-330253"
        },
        {
            "title": "Sergio Montes y John Arandia del Grupo Fides fueron distinguidos por la Asociación de Periodistas de La Paz（2025-12-05 获奖报道）",
            "url": "https://www.noticiasfides.com/democracia/sergio-montes-y-john-arandia-del-grupo-fides-fueron-distinguidos-por-la-asociacion-de-periodistas-de-la-paz"
        },
        {
            "title": "Agencia de Noticias Fides - Wikipedia（西语维基百科：创立、沿革、2019年重组转纯数字）",
            "url": "https://es.wikipedia.org/wiki/Agencia_de_Noticias_Fides"
        },
        {
            "title": "Provincial de la Compañía de Jesús nombra al P. Sergio Montes, SJ director de Radio Fides Bolivia（2024-12-23 兼任任命）",
            "url": "https://www.jesuitas.org.bo/noticias/provincial-de-la-compania-de-jesus-nombra-al-p-sergio-montes-sj-director-de-radio-fides-bolivia"
        }
    ],
    "completeness_score": data.get("collection_meta", {}).get("completeness_score"),
    "notes": "2026-10-24 phase3 富集：经西语/英语维基百科、官网关于页与页脚、耶稣会玻利维亚省官网及 ANF 社媒多源核实。现任总裁塞尔希奥·蒙特斯（2013年至今，index 命中 BO-PERSON-000410）、集团信息总监南希·瓦卡弗洛尔（index 命中 BO-PERSON-000411）；创始人何塞·格拉蒙特·德·莫拉加斯已故，person_id 留空。玻利维亚非APEC成员，apec_stance 按事实填写。近期事件5条（2024-12至2026-08）均有可溯来源。"
}

with open(FP, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK: BO-MEDIA-018 enriched ->", FP)

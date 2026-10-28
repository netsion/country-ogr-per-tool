# -*- coding: utf-8 -*-
"""Build BO-PERSON-000462.json profile for Alberto Mosquera López.
Sources verified 2026-10-26:
  [S1] wvi.org appointment article (published 2012-10-04; announcement 2012-09-20)
  [S2] YouTube XTOTVBolivia zeTPrJG9G80 (2020-07-30) - "el ecuatoriano Alberto Mosquera,
       Director Ejecutivo de World Vision Bolivia"
  [S3] InfoRSE 2020-12-19 - Director Nacional mentioned; Oscar Montes a.i. delivered
  [S4] YouTube Conferencia Episcopal Boliviana fSBYJjphF-U (2019-03-19)
  [S5] YouTube productoraastro KBNJu9xNooU - Caritas Boliviana agreement, lunes 24 de junio
       (Monday 24 June = 2013-06-24)
  [S6] YouTube PTV Bolivia bIt6sFyA5sM (2019-03-11; event 2019-03-08)
  [S7] Facebook puntovidascc video 1069618153686471 - retirement interview
  [S8] Facebook WorldVisionBO video 562736575376663 - Camiri honour
  [S9] LinkedIn ec.linkedin.com/in/alberto-mosquera-aa210523b (DDG cached snippet)
  [S10] ZoomInfo 8610299089 (DDG cached snippet) - "Country Director for Bolivia and Ecuador"
  [S11] YouTube World Vision Bolivia VjvjZlDHfpM (2012-03-29) - predecessor Peter Fenoy
  [S12] YouTube BlogsNoticias qY5hoN3r8nc (2023-11-12) - successor Juan Carlos Ramirez in office
"""
import json
import os

OUT = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons\BO-PERSON-000462.json"

profile = {
    "person_id": "BO-PERSON-000462",
    "wikidata_qid": None,
    "name": "Alberto Mosquera López",
    "name_en": "Alberto Mosquera Lopez",
    "name_zh": None,
    "aliases": [
        "Alberto Mosquera Lopez",
        "Alberto Mosquera L.",
        "Ing. Alberto Mosquera"
    ],
    "nationality": "EC",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "contacts": [],
    "current_positions": [],
    "education": [],
    "work_experience": [
        {
            "start_date": None,
            "end_date": "2012",
            "organization": "世界宣明会厄瓜多尔分会 (World Vision Ecuador)",
            "org_id": None,
            "position": "国家主任",
            "description": "赴玻利维亚之前曾任世界宣明会厄瓜多尔分会国家主任；厄瓜多尔董事会对其离任不舍。具体起止年份未见公开记载。",
            "source": "https://www.wvi.org/article/alberto-mosquera-lopez-appointed-new-national-director-wv-bolivia"
        },
        {
            "start_date": "2012-09-20",
            "end_date": "2022",
            "organization": "世界宣明会玻利维亚分会 (World Vision Bolivia)",
            "org_id": "BO-NGO-009",
            "position": "国家主任",
            "description": "2012年9月20日由世界宣明会拉美及加勒比区域主任 Stefan Pleisnitzer 宣布任命并即时生效，此前已主持玻利维亚国家办公室过渡期工作，接替 Peter Fenoy。任内机构覆盖50多个市政、惠及9万余名儿童及其家庭。约2022年卸任（卸任访谈见 Punto Vida Scc 节目；继任者 Juan Carlo Ramírez 至迟于2023年已在任）。",
            "source": "https://www.wvi.org/article/alberto-mosquera-lopez-appointed-new-national-director-wv-bolivia",
            "end_date_note": "确切卸任月份未见权威公开来源；公开证据显示在任至2020年12月（InfoRSE），继任者2023年已公开以国家主任身份活动"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000461",
            "person_name": "胡安·卡洛斯·拉米雷斯 (Juan Carlos Ramírez)",
            "relationship_type": "other",
            "description": "继任者：Alberto Mosquera 约2022年卸任后接任世界宣明会玻利维亚分会国家主任（Director País），2023-11-12 代表机构获玻利维亚全国工业商会 resilience 奖时在任。部分来源写作 Juan Carlo Ramírez Gutiérrez。",
            "source": "https://www.youtube.com/watch?v=qY5hoN3r8nc"
        },
        {
            "person_id": None,
            "person_name": "彼得·费诺伊 (Peter Fenoy)",
            "relationship_type": "other",
            "description": "前任国家主任：2012-03-29 仍以世界宣明会玻利维亚国家主任身份接受 ATB 采访；2012年9月由 Alberto Mosquera 接任。",
            "source": "https://www.youtube.com/watch?v=VjvjZlDHfpM"
        },
        {
            "person_id": None,
            "person_name": "斯特凡·普莱斯尼策 (Stefan Pleisnitzer)",
            "relationship_type": "superior",
            "description": "时任世界宣明会拉美及加勒比区域主任（LACRO），2012-09-20 宣布对 Alberto Mosquera 的国家主任任命并即时生效。",
            "source": "https://www.wvi.org/article/alberto-mosquera-lopez-appointed-new-national-director-wv-bolivia"
        },
        {
            "person_id": None,
            "person_name": "胡安·卡洛斯·贝拉斯克斯 (Juan Carlos Velásquez)",
            "relationship_type": "associate",
            "description": "玻利维亚明爱（Cáritas Boliviana）执行书记，2013-06-24 与 Alberto Mosquera 共同签署世界宣明会玻利维亚分会与明爱为期两年的机构间合作协议。",
            "source": "https://www.youtube.com/watch?v=KBNJu9xNooU"
        },
        {
            "person_id": None,
            "person_name": "奥斯卡·蒙特斯 (Oscar Montes)",
            "relationship_type": "colleague",
            "description": "世界宣明会玻利维亚分会同事：2020-12-19 在 InfoRSE「Resiliencia 2020」活动上以代理国家主任（Director Nacional a.i.）身份代出国在外的 Mosquera 致辞；2023-04 以机构质量项目总监身份出席40周年活动。",
            "source": "https://www.inforse.com.bo/2020/12/19/world-vision-bolivia/"
        }
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Alberto Mosquera",
            "url": "https://ec.linkedin.com/in/alberto-mosquera-aa210523b",
            "source": "DuckDuckGo 检索快照（2026-10-26）：自述拥有约20年国际非政府组织工作经验，社会政策硕士等多个硕士学位"
        }
    ],
    "family_members": [],
    "political_stances": [
        {
            "date": "2020-12-19",
            "topic": "新冠疫情下的企业社会责任",
            "stance_content": "以「la solidaridad nunca estuvo en cuarentena」（团结/互助从未被隔离）为口号，呼吁企业界在疫情与隔离期间坚持社会责任与跨部门互助，向脆弱群体尤其是儿童倾斜资源。",
            "source": "https://www.inforse.com.bo/2020/12/19/world-vision-bolivia/"
        },
        {
            "date": "2019-03",
            "topic": "消除对儿童的暴力",
            "stance_content": "主导「Huellas de Ternura」（温柔的脚印）全国行走活动，提出「我们需要所有人共同消除针对儿童的暴力」倡议，并为电视主持人 Casimira Lema 授予活动大使称号。",
            "source": "https://www.youtube.com/watch?v=bIt6sFyA5sM"
        }
    ],
    "major_achievements": [
        {
            "date": "2012-09-20",
            "achievement": "获任世界宣明会玻利维亚分会国家主任：由拉美及加勒比区域主任 Stefan Pleisnitzer 正式宣布、即时生效；此前已主持该国国家办公室过渡期工作并获管理层肯定。",
            "organization": "世界宣明会玻利维亚分会 (World Vision Bolivia)"
        },
        {
            "date": "2013-06-24",
            "achievement": "与玻利维亚明爱（Cáritas Boliviana）签署为期两年的机构间合作协议，合作涵盖卫生（含艾滋病防治培训）、食品安全、人道主义援助、倡导与动员等领域。",
            "organization": "世界宣明会玻利维亚分会 (World Vision Bolivia)"
        },
        {
            "date": "2019-03",
            "achievement": "领导「Huellas de Ternura」（温柔的脚印）反对暴力侵害儿童全国行走活动，并促成电视节目主持人 Casimira Lema 出任活动大使。",
            "organization": "世界宣明会玻利维亚分会 (World Vision Bolivia)"
        },
        {
            "date": "2020-12-19",
            "achievement": "新冠疫情期间领导机构人道响应：以「团结从未被隔离」为口号参与 Resiliencia 2020 企业联合行动，为瓜拉尼 Itakise 社区清洁饮水（WASH）项目筹集逾1.2万玻利维亚诺，任内机构覆盖50多个市政、服务9万余名儿童。",
            "organization": "世界宣明会玻利维亚分会 (World Vision Bolivia)"
        }
    ],
    "biography_summary": "阿尔贝托·莫斯基拉·洛佩斯（Alberto Mosquera López），厄瓜多尔籍国际发展从业者，工程师（「Ing.」）出身，拥有社会政策等多个硕士学位，在国际非政府组织领域从业约二十年。赴玻前曾任世界宣明会厄瓜多尔分会国家主任。2012年9月20日，世界宣明会拉美及加勒比区域主任斯特凡·普莱斯尼策宣布其出任世界宣明会玻利维亚分会国家主任并即时生效；此前他已在玻利维亚主持过渡期工作，接替同年3月仍在任的彼得·费诺伊。十年任内，他于2013年与玻利维亚明爱签署两年期机构间合作协议（涵盖卫生、食品安全与人道援助），2019年主导「温柔的脚印」反对暴力侵害儿童全国行动，新冠疫情期间以「团结从未被隔离」为口号组织人道响应、联合企业界为瓜拉尼社区清洁饮水项目筹资；任内机构覆盖50多个市政、惠及9万余名儿童。约2022年卸任，由胡安·卡洛斯·拉米雷斯接任，其卸任访谈见诸圣克鲁斯节目《Punto Vida》。注意与玻利维亚电视主持人及巴拿马拳击手等同名者区分。",
    "profile": {
        "source_url": "https://i.ytimg.com/vi/fSBYJjphF-U/hqdefault.jpg",
        "local_path": "photos/BO-PERSON-000462.jpg"
    },
    "collection_meta": {
        "collection_date": "2026-10-26",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "news_search",
            "web_search",
            "social_media"
        ],
        "notes": "核心事实（2012-09-20任命、前任Peter Fenoy、厄瓜多尔任职背景）由世界宣明会国际官网2012-10-04公告直接确认；2020年在任状态由玻利维亚InfoRSE行业媒体（2020-12-19）与XTOTV访谈（2020-07-30）交叉验证。国籍：任务参数原设为玻利维亚（BO），但两个独立来源（XTOTVBolivia视频描述明确称「el ecuatoriano Alberto Mosquera」；wvi.org公告载明其此前任世界宣明会厄瓜多尔国家主任）均指向厄瓜多尔籍，故按证据记为EC并在nationality_note说明。卸任精确月份未获权威来源：公开证据显示在任至2020-12，继任者Juan Carlo Ramírez至迟2023-11已在任，故end_date记为2022并加注。同名区分：非玻利维亚电视主持人/记者Alberto Mosquera，亦非巴拿马拳击手Alberto Mosquera。birth_date/birth_place/教育院校/家庭信息无公开来源，留空；LinkedIn个人页详情因登录墙仅取得检索快照。补注：访问环境受限（搜索工具配额、Internet Archive临时下线、玻媒Cloudflare拦截），主要经YouTube、DDG快照与直取原文页完成。completeness_score约56，低于85目标系客观信息有限（无维基/维基数据条目，出生与家庭不公开），已达标下限45。",
        "quotes": [
            {
                "title": "Alberto Mosquera Lopez appointed as new National Director for WV Bolivia | World Vision International",
                "url": "https://www.wvi.org/article/alberto-mosquera-lopez-appointed-new-national-director-wv-bolivia"
            },
            {
                "title": "Toto Salcedo: Alberto Mosquera de Visión Mundial | XTOTVBolivia (YouTube, 2020-07-30)",
                "url": "https://www.youtube.com/watch?v=zeTPrJG9G80"
            },
            {
                "title": "World Vision Bolivia - InfoRSE (2020-12-19)",
                "url": "https://www.inforse.com.bo/2020/12/19/world-vision-bolivia/"
            },
            {
                "title": "VIDEO: Alberto Mosquera - Visión Mundial Bolivia | Conferencia Episcopal Boliviana (YouTube, 2019-03-19)",
                "url": "https://www.youtube.com/watch?v=fSBYJjphF-U"
            },
            {
                "title": "FIRMA CONVENIO CÁRITAS BOLIVIANA VISIÓN MUNDIAL BOLIVIA | productoraastro (YouTube)",
                "url": "https://www.youtube.com/watch?v=KBNJu9xNooU"
            },
            {
                "title": "08/03/19 LIC. ALVERTO MOSQUERA REPRESENTANTE DE VISION MUNDIAL | PTV Bolivia (YouTube, 2019-03-11)",
                "url": "https://www.youtube.com/watch?v=bIt6sFyA5sM"
            },
            {
                "title": "Entrevista con Alberto Mosquera - Director Nacional World Vision Bolivia (Punto Vida Scc, Facebook)",
                "url": "https://www.facebook.com/puntovidascc/videos/entrevista-con-alberto-mosquera-director-nacional-world-vision-bolivia/1069618153686471/"
            },
            {
                "title": "World Vision Bolivia recibe condecoración en Camiri | WorldVisionBO (Facebook)",
                "url": "https://www.facebook.com/WorldVisionBO/videos/world-vision-bolivia-representado-por-su-director-nacional-alberto-mosquerarecib/562736575376663/"
            },
            {
                "title": "Alberto Mosquera - LinkedIn (EC)",
                "url": "https://ec.linkedin.com/in/alberto-mosquera-aa210523b"
            },
            {
                "title": "Alberto Mosquera - Country Director for Bolivia and Ecuador | ZoomInfo",
                "url": "https://www.zoominfo.com/p/Alberto-Mosquera/8610299089"
            },
            {
                "title": "ATB ENTREVISTA AL DIRECTOR NACIONAL DE VISIÓN MUNDIAL BOLIVIA Dr. PETER FENOY | World Vision Bolivia (YouTube, 2012-03-29)",
                "url": "https://www.youtube.com/watch?v=VjvjZlDHfpM"
            }
        ]
    },
    "identity_note": "须与以下同名者区分：（1）玻利维亚电视主持人/记者 Alberto Mosquera（媒体界人士，非本人）；（2）巴拿马拳击手 Alberto Mosquera（职业拳手，非本人）。本条目人物为世界宣明会系统内的国际发展从业者。",
    "nationality_note": "任务参数原设 nationality=BO，但检索证据显示其为厄瓜多尔籍：（1）XTOTVBolivia 2020-07-30 访谈视频描述明确写作「el ecuatoriano Alberto Mosquera, Director Ejecutivo de World Vision Bolivia」；（2）世界宣明会国际官网2012年公告载明其赴玻前任职世界宣明会厄瓜多尔分会国家主任、厄瓜多尔董事会对其离任不舍；（3）其 LinkedIn 档案挂于 ec.linkedin.com；（4）ZoomInfo 聚合其头衔为「Country Director for Bolivia and Ecuador」。故按证据记为 EC。",
    "position_note": "称谓随年份略有差异：2012年任命公告与2020年InfoRSE报道称「Director Nacional（国家主任）」；2020-07-30 XTOTV 访谈称「Director Ejecutivo（执行主任）」；ZoomInfo 聚合头衔为「Country Director」。均为同一职务的不同表述。",
    "work_note": "LinkedIn 检索快照自述拥有约20年国际非政府组织工作经验。2020-12 InfoRSE 活动中其因出国由 Oscar Montes 以代理国家主任（a.i.）身份代为致意，佐证当时仍在任。另曾以国家主任身份代表机构接受卡米里（Camiri）市政府授勋（Facebook WorldVisionBO 官方账号视频，具体日期未显示）。",
    "education_note": "教育经历无权威公开来源。LinkedIn 检索快照显示头衔为「Master en Políticas Sociales | Master Calidad y …」（社会政策硕士及另一质量方向硕士学位），就读院校未能核实，故 education 数组留空。",
    "social_accounts_note": "六项扫描（2026-10-26）：LinkedIn 个人页命中1条（ec.linkedin.com/in/alberto-mosquera-aa210523b，详情受登录墙限制）；Facebook 上的相关视频均发布于机构账号（WorldVisionBO）或节目账号（Punto Vida Scc），非其个人账号；未检索到本人 X/Twitter、Instagram、TikTok、YouTube 个人账号。",
    "family_note": "无公开资料披露其家庭成员。",
    "name_zh_note": "未检索到玻利维亚/厄瓜多尔华文媒体对该人物的既有中文译名，故 name_zh 置 null；简介中采用音译「阿尔贝托·莫斯基拉·洛佩斯」仅为行文需要。"
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("written:", OUT)
print("bytes:", os.path.getsize(OUT))

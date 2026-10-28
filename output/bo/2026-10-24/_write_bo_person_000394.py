# -*- coding: utf-8 -*-
"""Build BO-PERSON-000394 Pamela Garcia (Bolivision Gerente de Prensa)."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000394.json")

person = {
    "person_id": "BO-PERSON-000394",
    "wikidata_qid": None,
    "name_zh": "帕梅拉·加西亚",
    "name": "Pamela García",
    "name_en": "Pamela Garcia",
    "aliases": ["Pamela Garcia", "T. Pamela García Ecos"],
    "nationality": "BO",
    "gender": "female",
    "birth_date": None,
    "birth_place": None,
    "contacts": [],
    "current_positions": [
        "Bolivisión（玻利维亚私营电视网，Red Bolivisión）新闻总监 (Gerente de Prensa)"
    ],
    "education": [],
    "work_experience": [
        {
            "start_date": None,
            "end_date": None,
            "organization": "Bolivisión（玻利维亚私营电视网，Red Bolivisión） (Bolivisión)",
            "org_id": "BO-MEDIA-009",
            "position": "新闻总监 (Gerente de Prensa)",
            "description": "统管 Red Bolivisión 全国新闻采编与《Noticias Bolivisión Al Día》各档新闻（Edición Central、Segunda Edición 及圣克鲁斯版等）的制作播出。官方社媒与本人 LinkedIn 亦称「全国新闻总监 (Gerente Nacional de Prensa)」。至少 2024 年 5 月已公开可见于此职：该台 Gran Poder 2024 官方视频称其为「nuestra gerente [de prensa] a nivel nacional」。",
            "source": "es.wikipedia.org（Bolivisión 条目信息框 Personas clave）; x.com/BolivisionNoti（2024-11-23 推文）; bo.linkedin.com（本人档案标题）; facebook.com/red.bolivision（GranPoder2024/GranPoder2025 官方视频）",
            "note": "任职起始时间未见公开记录；西语维基百科信息框拼写 Pamela Garcia（无重音），其余来源（本人 LinkedIn、官方社媒、媒体报道）均作 Pamela García。"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "Bolivisión（玻利维亚私营电视网，Red Bolivisión） (Bolivisión)",
            "org_id": "BO-MEDIA-009",
            "position": "新闻节目制作人 (Productora de noticieros)",
            "description": "2012 年 6 月前已任新闻杂志《Al Día》制作人——主持人 Pamela Muñoz 在专访中回忆，其加入 Bolivisión 的邀请即出自「Al Día 制作人 Pamela García」与时任新闻主编 Víctor Hugo Rosales。2014 年 11 月玻利维亚《El Diario》日报电视指南专访中，台方负责人介绍其为该台三档新闻节目的四名制作人之一（与 María Luisa Callejas、Nery Prado、Lucía Quispe 并列）。",
            "source": "televisionenbolivia.blogspot.com（2012-06 Pamela Muñoz 专访）; pub.eldiario.net（2014-11-09「El equipo de Bolivisión」）",
            "note": "起止年份不详；本人 LinkedIn 自述媒体从业逾 20 年。"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "Bolivisión（玻利维亚私营电视网，Red Bolivisión） (Bolivisión)",
            "org_id": "BO-MEDIA-009",
            "position": "《El Carnavalero》节目制作人 (Productora de El Carnavalero)",
            "description": "2013 年 1 月玻利维亚电视行业博客报道确认其担任 Bolivisión 狂欢节专题节目《El Carnavalero》制作人，并引述其说法称该节目「力求博得电视观众一笑」；节目覆盖奥鲁罗、圣克鲁斯、科恰班巴、塔里哈与拉巴斯等地主要狂欢节活动。",
            "source": "televisionenbolivia.blogspot.com（2013-01-30「Bolivisión se viste de colores」）",
            "note": "与新闻制作人职务并行，任止时间不详。"
        }
    ],
    "person_relationships": [
        {
            "person_id": None,
            "person_name": "埃塞基埃尔·塞雷斯 (Ezequiel Serres)",
            "relationship_type": "colleague",
            "description": "西语维基百科 Bolivisión 条目信息框「Personas clave」栏与其并列列出，任该台圣克鲁斯第 4 频道新闻主编 (Jefe de Prensa, Canal 4 Santa Cruz)，分管圣克鲁斯版新闻。",
            "source": "es.wikipedia.org（Bolivisión 条目信息框）"
        },
        {
            "person_id": None,
            "person_name": "维克托·乌戈·罗萨莱斯 (Víctor Hugo Rosales)",
            "relationship_type": "superior",
            "description": "2012 年时任 Bolivisión 新闻主编 (jefe de prensa)，与加西亚共同向主持人 Pamela Muñoz 发出加入该台的邀请；2014 年《El Diario》该台新闻团队专访的台方受访负责人，加西亚彼时为其团队中的新闻制作人。",
            "source": "televisionenbolivia.blogspot.com（2012-06）; pub.eldiario.net（2014-11-09）"
        },
        {
            "person_id": None,
            "person_name": "帕梅拉·穆尼奥斯 (Pamela Muñoz)",
            "relationship_type": "colleague",
            "description": "2012 年经加西亚与时任新闻主编罗萨莱斯邀请加入 Bolivisión，其后成为《Al Día》新闻杂志及该台新闻节目主持人。",
            "source": "televisionenbolivia.blogspot.com（2012-06 Pamela Muñoz 专访）"
        },
        {
            "person_id": None,
            "person_name": "卡门·金塔纳 (Carmen Quintana)",
            "relationship_type": "superior",
            "description": "2014 年 11 月报道时任 Bolivisión 总经理 (gerente general)，加西亚彼时任该台新闻制作人，属其管理层上级。",
            "source": "pub.eldiario.net（2014-11-09「El equipo de Bolivisión」）"
        }
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "T. Pamela García Ecos",
            "url": "https://bo.linkedin.com/in/t-pamela-garc%C3%ADa-ecos-8b1292280",
            "source": "WebSearch 检索摘要（2026-10-27）：档案标题「Gerente Nacional de Prensa BOLIVISIÓN en Red Bolivisión」，所在地 La Paz, Bolivia"
        }
    ],
    "family_members": [],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2024-11",
            "organization": "玻利维亚众议院 (Cámara de Diputados)",
            "achievement": "获玻利维亚众议院表彰，以肯定其新闻职业生涯——Bolivisión 官网新闻以「Gerenta de noticias condecorada por su trayectoria」（获表彰的女新闻总监）为题报道；官方 X 账号 @BolivisionNoti 与 Facebook 账号 Noticias Bolivisión 于 2024-11-23 发布。"
        },
        {
            "date": "2023",
            "organization": "Bolivisión（玻利维亚私营电视网） (Bolivisión)",
            "achievement": "作为主要推动者之一参与发起 Red Bolivisión 全国性冬季衣物捐助公益活动「Te abrazo, te abrigo」（口号「Unidos contra el frío」；官方称其为玻利维亚规模最大的团结互助捐赠活动），该活动此后连年续办；台方晨间节目《Al Día Tu Día》官方账号称其为该活动「主要推动者之一」。"
        }
    ],
    "public_activities": [
        "2024-05：作为「全国新闻总监」率 Bolivisión 团队参加拉巴斯 Gran Poder 节庆（Fiesta Mayor），台方官方账号发布视频记录（#GranPoder2024）。",
        "2025：再度出镜该台 GranPoder2025 官方视频，头衔标注为「Gerente Nacional de Prensa de Red Bolivisión」。",
        "2023 年起：多次代表台方出席「Te abrazo, te abrigo」公益活动相关活动并在《Al Día Tu Día》官方账号出镜发声。"
    ],
    "biography_summary": "帕梅拉·加西亚（Pamela García，西语维基百科信息框拼写 Pamela Garcia，LinkedIn 档案全名显示为 T. Pamela García Ecos）是玻利维亚私营电视网 Bolivisión（Red Bolivisión，阿尔瓦维斯集团旗下）的新闻总监（Gerente de Prensa，官方社媒与本人 LinkedIn 亦称全国新闻总监 Gerente Nacional de Prensa），西语维基百科 Bolivisión 条目信息框「Personas clave」栏将其列为该台关键人物，与圣克鲁斯第 4 频道新闻主编埃塞基埃尔·塞雷斯并列。她是一名拥有逾 20 年从业经历的新闻工作者：至少 2012 年年中前即已担任该台新闻杂志《Al Día》制作人，2013 年 1 月兼任狂欢节专题节目《El Carnavalero》制作人，2014 年 11 月《El Diario》日报专访中已被介绍为该台三档新闻节目的四名制作人之一。2023 年她作为主要推动者之一参与发起该台全国性冬季衣物捐助公益活动「Te abrazo, te abrigo」。2024 年 11 月，玻利维亚众议院（Cámara de Diputados）授予她表彰，以肯定其新闻职业生涯；此前 2024 年 5 月起她已以「全国新闻总监」身份率队参加拉巴斯 Gran Poder 节庆报道。其出生日期、出生地、学历与家庭情况均未见公开权威记录。",
    "profile": None,
    "identity_note": "注意区分同名者：美国等地存在多名 Pamela Garcia / Pam Garcia（含政界、体育界人士），与本档案对象无关。本档案全部事实均限定于玻利维亚媒体行业来源（Bolivisión 官方渠道、玻利维亚媒体行业报道及本人 LinkedIn），未混入任何同名者信息。",
    "name_note": "本国官方语言（西语）原名以重音拼写 Pamela García 为准（本人 LinkedIn、雇主官方社媒及玻利维亚媒体一致用法）；西语维基百科 Bolivisión 条目信息框作无重音的 Pamela Garcia，已列入 aliases。",
    "name_zh_note": "「帕梅拉·加西亚」为本项目清单与 orgs/BO-MEDIA-009.json 既定的项目音译（内部惯例），本次检索未发现玻利维亚华文媒体或权威中文媒体的既有标准译名，为保持跨文件一致沿用该译名。",
    "birth_date_note": "未检索到任何公开来源披露其出生日期或年龄。",
    "birth_place_note": "未检索到出生地信息；仅 LinkedIn 显示现居玻利维亚拉巴斯（La Paz, Bolivia）。",
    "nationality_note": "依据 LinkedIn 所在地（La Paz, Bolivia）及其至少自 2012 年起长期任职玻利维亚 Bolivisión 推断国籍为玻利维亚（BO）；未见明确国籍声明或双重国籍信息。",
    "gender_note": "女性：来源中以阴性形式指称（gerenta、reconocida、impulsoras 等）。",
    "position_note": "官方称谓两种写法实为同一职务：西语维基百科信息框作「Gerente de Prensa」；官方社媒与本人 LinkedIn 作「Gerente Nacional de Prensa」（全国新闻总监）。",
    "work_note": "制作人时期与新闻总监时期之间的晋升时间未见公开记录（2014 年 11 月仍为制作人，2024 年 5 月已任总监）。原官网获奖文章 redbolivision.tv.bo 链接已删除（「Recurso eliminado permanentemente」），获奖事实经官方 X 账号推文（全文经 X syndication API 取得）与官网镜像页交叉确认。",
    "education_note": "公开渠道（LinkedIn 索引摘要、多语种新闻检索）均未获任何学历信息，education 留空。",
    "family_note": "未检索到任何家庭成员公开信息，family_members 留空。",
    "social_accounts_note": "6 项社媒扫描结果：LinkedIn 已确证（bo.linkedin.com/es.linkedin.com 同一档案号 8b1292280，64 名关注者）；X/TikTok/YouTube 未发现可确证的个人账号；Instagram 候选账号 @pashmypame1（603 名关注者）无法确认属本人，未收录；Facebook 仅见 Red Bolivisión、Noticias Bolivisión、Al Día Tu Día 等官方账号发布涉其内容，未发现可确证的个人主页。",
    "collection_meta": {
        "collection_date": "2026-10-27",
        "phase": "phase4_person_profile",
        "data_sources": [
            "wikipedia",
            "official_website",
            "news_search",
            "web_search",
            "social_media"
        ],
        "completeness_score": 48,
        "notes": "身份判定：Pamela García 为 Bolivisión（BO-MEDIA-009）新闻总监，由西语维基百科 Bolivisión 条目信息框（Personas clave: Pamela Garcia, Gerente de Prensa）、该台官方 X/Facebook 账号（2024-11-23 众议院表彰报道）、本人 LinkedIn 档案（T. Pamela García Ecos，Gerente Nacional de Prensa BOLIVISIÓN en Red Bolivisión，La Paz）及台方 Gran Poder 2024/2025 官方视频多来源一致确认。重音拼写：以 Pamela García 为准；LinkedIn 全名「T. Pamela García Ecos」中「T.」所指（疑为教名缩写）与母姓「Ecos」均未获第二来源核实，仅作别名收录。职业生涯（2012《Al Día》制作人、2013《El Carnavalero》制作人、2014 三档新闻制作人之一、2024 众议院表彰）均有可直取全文的独立来源；其中「2012 年前已任制作人」与「罗萨莱斯时任新闻主编」出自 2012 年 Pamela Muñoz 专访全文，「2014 年制作人身份」出自《El Diario》专访全文，两处交叉印证其 2012-2014 年制作人经历。name_zh「帕梅拉·加西亚」为项目内部既定音译（与 _name_index.json、orgs/BO-MEDIA-009.json 一致），无外部权威译名，已加注说明。completeness_score=48（验证脚本 calc_person_score 客观计算）：出生日期、出生地、学历、家庭、Wikidata 条目、照片及 LinkedIn 以外的个人社媒账号在公开渠道客观不可得（对女性电视新闻高管属常见情况），在仅收录经核实事实的前提下该分数已接近公开信息允许的上限，故低于 50 的差额原因如上说明。",
        "quotes": [
            {
                "title": "Bolivisión - Wikipedia, la enciclopedia libre（信息框 Personas clave: Pamela Garcia, Gerente de Prensa; Ezequiel Serres, Jefe de Prensa Canal 4 Santa Cruz）",
                "url": "https://es.wikipedia.org/wiki/Bolivisi%C3%B3n"
            },
            {
                "title": "El equipo de Bolivisión - El Diario（玻利维亚，2014-11-09，电视指南专访：三档新闻节目四名制作人含 Pamela García）",
                "url": "https://www.pub.eldiario.net/noticias/2014/2014_11/nt141109/laguia.php?n=24&-el-equipo-de-bolivision"
            },
            {
                "title": "Pamela Muñoz | Modelo y presentadora de tv - Televisión, Radio y Periódicos（2012-06：邀请其加入 Bolivisión 的是「Al Día 制作人 Pamela García」与新闻主编 Víctor Hugo Rosales）",
                "url": "https://televisionenbolivia.blogspot.com/2012/06/pamela-munoz-modelo-y-presentadora-de.html"
            },
            {
                "title": "Bolivisión se viste de colores - Televisión, Radio y Periódicos（2013-01-30：Pamela García, productora de El Carnavalero）",
                "url": "https://televisionenbolivia.blogspot.com/2013/01/bolivision-se-viste-de-colores.html"
            },
            {
                "title": "Nuevamente premian el trabajo de Bolivisión - Bolivisión 官网（镜像页：Gerenta de noticias condecorada por su trayectoria）",
                "url": "https://bo-bolivision-origin.mediatiquepress.com/noticia/nuevamente-premian-el-trabajo-de-bolivision/"
            },
            {
                "title": "@BolivisionNoti 官方推文（2024-11-23：Pamela García, gerente de Prensa de la Red Bolivisión fue reconocida por la Cámara de Diputados）",
                "url": "https://x.com/BolivisionNoti/status/1860284478427369637"
            },
            {
                "title": "T. Pamela García Ecos - LinkedIn（Gerente Nacional de Prensa BOLIVISIÓN en Red Bolivisión；La Paz, Bolivia；逾 20 年媒体从业）",
                "url": "https://bo.linkedin.com/in/t-pamela-garc%C3%ADa-ecos-8b1292280"
            },
            {
                "title": "Noticias Bolivisión Facebook（2024-11-23：Pamela García… fue reconocida por la Cámara de Diputados）",
                "url": "https://www.facebook.com/NoticiasBolivision/posts/969393301893126"
            },
            {
                "title": "#GranPoder2024 | Red Bolivisión 官方视频（2024-05：gerente de prensa a nivel nacional, Pamela García）",
                "url": "https://www.facebook.com/red.bolivision/videos/granpoder2024-el-equipo-de-bolivisi%C3%B3n-presente-en-la-fiesta-mayor-nuestra-gerent/2900644246749455"
            },
            {
                "title": "#GranPoder2025 | Red Bolivisión 官方视频（Pamela García, Gerente Nacional de Prensa de Red Bolivisión）",
                "url": "https://www.facebook.com/red.bolivision/videos/granpoder2025-pamela-garc%C3%ADa-jefa-de-prensa-de-red-bolivisi%C3%B3n-nos-muestra-que-la-/1030067375966121"
            },
            {
                "title": "Al Día Tu Día Facebook（Pamela García, gerente nacional de Prensa…una de las principales impulsoras de #TeAbrazoTeAbrigo）",
                "url": "https://www.facebook.com/aldiatudia/videos/1651833592702383"
            },
            {
                "title": "T. Pamela García Ecos LinkedIn 帖（Te abrazo, te abrigo：2023 年诞生于 Red Bolivisión 的公益活动）",
                "url": "https://es.linkedin.com/posts/t-pamela-garc%C3%ADa-ecos-8b1292280_te-abrazo-te-abrigo-una-campa%C3%B1a-que-naci%C3%B3-activity-7344461791189450752-ieTZ"
            }
        ]
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(person, f, ensure_ascii=False, indent=2)
print("WROTE", OUT)
print("bytes:", os.path.getsize(OUT))

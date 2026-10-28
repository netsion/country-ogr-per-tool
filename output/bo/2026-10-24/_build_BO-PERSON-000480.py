# -*- coding: utf-8 -*-
"""Build BO-PERSON-000480.json — Dante González, Director of Fundación Bolivia Digna."""
import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OUT = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons\BO-PERSON-000480.json"

LQ = chr(12300)  # 「
RQ = chr(12301)  # 」

profile = {
    "person_id": "BO-PERSON-000480",
    "wikidata_qid": None,
    "name_zh": None,
    "name": "Dante Gonz" + chr(225) + "lez",
    "name_en": "Dante Gonzalez",
    "aliases": [chr(193) + "lvaro Dante Gonz" + chr(225) + "lez G" + chr(225) + "mez"],
    "nationality": "BO",
    "gender": "male",
    "gender_note": "性别经基金会官方YouTube频道2021年发布视频的截帧画面目视确认（出镜者为男性，身穿拉萨尔志愿项目/基金会制服）",
    "birth_date": None,
    "birth_place": None,
    "contacts": [
        {
            "type": "email",
            "value": "dante@boliviadigna.org",
            "source": "https://sri.ua.es/es/cooperacion/voluntariado/2025-informacion-fund.-bolivia-digna.pdf"
        }
    ],
    "current_positions": ["玻利维亚尊严基金会主任"],
    "education": [],
    "work_experience": [
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚尊严基金会 (Fundaci" + chr(243) + "n Bolivia Digna)",
            "org_id": "BO-NGO-015",
            "position": "主任"
        }
    ],
    "person_relationships": [
        {
            "person_id": None,
            "person_name": "伊格纳西" + chr(183) + "纳瓦罗" + chr(183) + "索里亚 (Ignasi Navarro Soria)",
            "relationship_type": "associate",
            "description": "西班牙阿利坎特大学「国际团结志愿」项目大学方联络人（enlace UA-Fundaci" + chr(243) + "n Bolivia Digna）；两人于2025年度项目官方文件中分别作为大学方与基金会方（合作机构方）联系人并列列示，为该跨国志愿服务项目的对口工作伙伴"
        }
    ],
    "social_accounts": [],
    "family_members": [],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2021-11-23",
            "achievement": "以主任（Director）身份出镜基金会拉萨尔志愿项目官方YouTube频道，发布年度大型圣诞募捐活动「GRAN CAMPA" + chr(209) + "A NAVIDE" + chr(209) + "A」官方邀请视频，呼吁公众为科恰班巴Mercado Campesino、Arocag" + chr(252) + "a、Tackoloma三个社区项目的儿童及青少年捐赠衣物、玩具与米面糖等食品（募捐期为11月8日至12月15日）",
            "organization": "玻利维亚尊严基金会 (Fundaci" + chr(243) + "n Bolivia Digna)"
        },
        {
            "date": "2025",
            "achievement": "被西班牙阿利坎特大学2025年度「国际团结志愿」（Voluntariado Solidario Internacional）项目官方文件列为基金会的合作方主任兼督导（Director y tutor en la contraparte）及志愿事务联络人，负责接待和指导赴玻国际志愿者并对接项目事务",
            "organization": "玻利维亚尊严基金会 (Fundaci" + chr(243) + "n Bolivia Digna)"
        },
        {
            "date": "2025-10",
            "achievement": "以「玻利维亚尊严基金会-拉萨尔志愿项目」代表身份赴法国圣艾蒂安参加拉萨尔国际校友网络交流活动，重申基金会「促进一个以团结与服务为生活方式的大家庭」的使命（单一来源：基金会关联Facebook页面记录，已注明）",
            "organization": "玻利维亚尊严基金会 (Fundaci" + chr(243) + "n Bolivia Digna)"
        }
    ],
    "biography_summary": (
        "Dante Gonz" + chr(225) + "lez（据基金会关联社媒记录全名为 " + chr(193) + "lvaro Dante Gonz" + chr(225) + "lez G" + chr(225) + "mez）是玻利维亚科恰班巴公益组织" + LQ + "玻利维亚尊严基金会" + RQ + "（Fundaci" + chr(243) + "n Bolivia Digna）的现任主任。该基金会由拉萨尔学校校友于2006年在科恰班巴创立，属拉萨尔志愿项目（Voluntariado La Salle）依托机构，致力于促进贫困与边缘社区中儿童、青少年及老年人等弱势群体的权利，开展社区教育中心、残障儿童康复协助、住院患儿陪伴、团结食堂与国际志愿服务等项目。Gonz" + chr(225) + "lez以主任身份统筹基金会事务并主管志愿者项目部：2021年11月，他以" + LQ + "主任" + RQ + "身份出镜基金会官方YouTube频道发布年度圣诞募捐活动邀请视频；2025年，西班牙阿利坎特大学" + LQ + "国际团结志愿" + RQ + "项目官方文件将其列为基金会的合作方主任兼督导（Director y tutor en la contraparte）及志愿事务联络人，联系邮箱为dante@boliviadigna.org；2025年10月，他以基金会-拉萨尔志愿项目代表身份赴法国圣艾蒂安参加拉萨尔国际校友交流活动。"
    ),
    "profile": {
        "source_url": "https://i.ytimg.com/vi/m0hOK-rtBRE/maxres2.jpg",
        "local_path": "photos/BO-PERSON-000480.jpg"
    },
    "identity_note": "同名消歧声明：「Dante Gonz" + chr(225) + "lez」为中等常见西语姓名组合。本画像身份经两个相互独立的来源锚定至玻利维亚尊严基金会主任——(1) 西班牙阿利坎特大学2025年「国际团结志愿」项目官方文件（列其基金会邮箱并注明 Director y tutor en la contraparte）；(2) 基金会官方YouTube频道2021年视频标题（Invitaci" + chr(243) + "n del Director Dante Gonz" + chr(225) + "lez），视频截帧显示出镜者身穿拉萨尔志愿项目/基金会制服。未发现其他同名者与该机构的公开关联记录，不存在需拆分的同名条目。",
    "aliases_note": "全名 " + chr(193) + "lvaro Dante Gonz" + chr(225) + "lez G" + chr(225) + "mez 仅见于基金会关联Facebook页面「Voluntariado La Salle Bolivia」相关记录（已收录于组织档案BO-NGO-015并引该页面为源），本次复核时Facebook正文因登录墙无法直接读取，全名未能获得第二独立来源，以别名形式谨慎收录。",
    "position_note": "「主任」（西语阳性形式 Director，而非 Directora）头衔由官方频道视频标题与阿利坎特大学项目文件双重确认；职级表述另见大学文件中的合作方主任兼督导（Director y tutor en la contraparte）。",
    "work_note": "任现职起止时间不详。可核实的最早公开职务证据为2021年11月23日官方频道视频，最晚为2025年10月赴法交流记录与2025年大学项目文件。据组织档案BO-NGO-015，其同时主管基金会志愿者项目部（Voluntariado，负责招募接待本地及国际志愿者）。",
    "social_accounts_note": "六平台扫描结果：未发现其个人社媒账号。(1) Facebook：基金会主页 facebook.com/fundacionboliviadigna（约5584关注者）与志愿项目页 facebook.com/p/Voluntariado-La-Salle-Bolivia-100005103165963（约586关注者）均为机构账号，页面可见文本无其个人署名内容；(2) Instagram：@fundboliviadigna（约1916关注者、606帖）为机构账号，无其个人提及；(3) YouTube：官方频道 Bolivia Digna Voluntariado La Salle (UCakJDVyDkORSh2-79SQGVKA) 有其出镜视频（见major_achievements）；(4) X/Twitter：机构账号 @boliviadignaorg 存在（据官网meta），无个人账号；(5) LinkedIn：仅机构公司主页，未检索到其个人档案；(6) TikTok：未发现机构或个人账号。故 social_accounts 留空。",
    "profile_note": "头像取自基金会官方YouTube频道2021年11月23日视频「GRAN CAMPA" + chr(209) + "A NAVIDE" + chr(209) + "A - Invitaci" + chr(243) + "n del Director Dante Gonz" + chr(225) + "lez」（videoId m0hOK-rtBRE）第2采样帧，出镜者即视频标题所指的主任本人，身穿拉萨尔志愿项目制服，已本地保存。",
    "collection_meta": {
        "collection_date": "2026-10-27",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "social_media",
            "web_search",
            "other"
        ],
        "completeness_score": 36,
        "notes": (
            "身份与数据来源确认：(1) 核心事实双源交叉验证——主任职务由阿利坎特大学2025年项目文件（sri.ua.es PDF全文）与基金会官方YouTube频道视频标题独立确认；邮箱dante@boliviadigna.org、合作方主任兼督导身份见大学文件全文。(2) 同名消歧：身份锚定依据见identity_note；全名为单一来源（见aliases_note），Saint-" + chr(201) + "tienne交流活动（2025-10）亦为单一来源（组织档案所引Facebook页面），谨慎采信并已逐条注明。(3) 组织背景（2006年拉萨尔校友创立、弱势儿童权利保护宗旨等）经官网、OMAEC2016年专文与Wayback存档联系页交叉确认。(4) 检索限制说明：WebSearch与web_reader MCP当日配额耗尽，全程改用Bing/Google News RSS直取+原文页curl抓取；Bing严格短语检索「Dante Gonz" + chr(225) + "lez」+「Bolivia Digna」零命中；玻利维亚媒体（Los Tiempos、ANF、Opin" + chr(243) + "n）站内检索未见其个人报道；官网WP REST API检索「Dante」0命中（Wayback CDX显示2017年站内曾有dante页面后删除）。(5) 缺失字段说明：出生日期、出生地、教育背景、家庭成员、个人社媒、政见经西语+英语多轮多平台检索未见公开资料，均留空/空数组，属客观不可得而非调查遗漏。(6) name_zh：查证无既有中文译名，置null。(7) completeness_score=36，低于40目标线：人物为小型本土NGO负责人，公开足迹有限，评分按校准脚本客观计算；所有可验证字段均已填充，未以推测性条目凑分。机构工作涉及弱势儿童保护等敏感领域，本画像仅记录职务与公开活动事实。"
        ),
        "quotes": [
            {
                "title": "FAQS - Voluntariado Solidario Internacional - Opci" + chr(243) + "n Fundaci" + chr(243) + "n Bolivia Digna (Universidad de Alicante, 2025)",
                "url": "https://sri.ua.es/es/cooperacion/voluntariado/2025-informacion-fund.-bolivia-digna.pdf"
            },
            {
                "title": "GRAN CAMPA" + chr(209) + "A NAVIDE" + chr(209) + "A - Invitaci" + chr(243) + "n del Director Dante Gonz" + chr(225) + "lez (YouTube, 2021-11-23)",
                "url": "https://www.youtube.com/watch?v=m0hOK-rtBRE"
            },
            {
                "title": "Bolivia Digna Voluntariado La Salle - YouTube (official channel)",
                "url": "https://www.youtube.com/channel/UCakJDVyDkORSh2-79SQGVKA"
            },
            {
                "title": "Fundaci" + chr(243) + "n Bolivia Digna - OMAEC (2016-12-06)",
                "url": "https://www.omaec.org/bolivia-digna/"
            },
            {
                "title": "SOBRE BOLIVIA DIGNA - Fundaci" + chr(243) + "n Bolivia Digna (official website)",
                "url": "https://boliviadigna.org/es/sobre-bolivia-digna/"
            },
            {
                "title": "CONTACTO - Fundaci" + chr(243) + "n Bolivia Digna (Wayback Machine, 2026-05-15)",
                "url": "http://web.archive.org/web/20260515110745/https://boliviadigna.org/es/contacto/"
            },
            {
                "title": "Voluntariado La Salle Bolivia - Facebook (page record)",
                "url": "https://www.facebook.com/p/Voluntariado-La-Salle-Bolivia-100005103165963/"
            }
        ]
    }
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)

# quick self-check
d = json.load(open(OUT, encoding="utf-8"))
print("written:", OUT)
print("bytes:", len(open(OUT, "rb").read()))
print("bio len:", len(d["biography_summary"]))
print("name:", d["name"])
print("aliases:", d["aliases"])
print("achievements:", len(d["major_achievements"]), "| quotes:", len(d["collection_meta"]["quotes"]))
print("top-level keys:", len(d.keys()))

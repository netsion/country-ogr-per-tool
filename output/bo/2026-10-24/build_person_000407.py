# -*- coding: utf-8 -*-
"""Build BO-PERSON-000407 (Amilcar Torrico, Gerente General de Red ATB) profile JSON."""
import json
import os
import urllib.request

OUT = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000407.json"
PHOTO_DIR = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/photos"

profile_source_url = (
    "https://scontent-sea5-1.xx.fbcdn.net/v/t15.5256-10/"
    "854189018_1459419109483554_2716266437702559916_n.jpg"
    "?_nc_cat=104&ccb=1-7&_nc_sid=596eb7&_nc_ohc=K2a6yOt4hu8Q7kNvwGjx4O_"
    "&_nc_oc=AdoWAorybObFyGRszkzD1JHjnU5Naw1hhBqFPZiNWzoxP-Kci0GOLTY31pmn2R0fDlw"
    "&_nc_zt=23&_nc_ht=scontent-sea5-1.xx&_nc_gid=Mp7cwVpx31MyNmOsdhvt3g"
    "&_nc_ss=7020f&oh=00_AQP8EsY9DkeWqf6MDuB1eDJYQPyrntskGAJBYtD3DEw3Cg&oe=6AE568E5"
)
local_path = None
try:
    os.makedirs(PHOTO_DIR, exist_ok=True)
    proxy = urllib.request.ProxyHandler({"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
    opener = urllib.request.build_opener(proxy)
    req = urllib.request.Request(
        profile_source_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    img = opener.open(req, timeout=60).read()
    if len(img) > 5000:
        p = os.path.join(PHOTO_DIR, "BO-PERSON-000407.jpg")
        with open(p, "wb") as f:
            f.write(img)
        local_path = "photos/BO-PERSON-000407.jpg"
        print("photo saved:", p, len(img), "bytes")
    else:
        print("photo too small, skip:", len(img))
except Exception as e:
    print("photo download failed:", e)

data = {
    "person_id": "BO-PERSON-000407",
    "wikidata_qid": None,
    "name": "Amílcar Torrico",
    "name_en": "Amilcar Torrico",
    "name_zh": None,
    "aliases": ["Amilcar Torrico"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "birth_note": "出生日期未见公开报道。ATB 官方 2026-10-21 帖文提及他与妻子于建台 42 周年当日（10 月 20 日）庆祝结婚 19 周年，可推知其结婚纪念日约为 2007 年 10 月 20 日，但帖文未涉及其出生日期。",
    "name_zh_note": "任务清单拟定译名「阿米尔卡·托里科」。经核查：维基数据无该人物条目（wbsearchentities 检索 0 命中）、中文维基百科无条目、未检索到任何华文媒体报道既定译名，按规则置 null，译名待可靠中文来源核证后启用。",
    "name_en_note": "玻利维亚媒体中 Amílcar Torrico（带重音）与 Amilcar Torrico（不带重音）两种拼写并存，aliases 收录不带重音变体。",
    "position_note": "报道中职务表述有 gerente general de ATB（ATB 总经理）、gerente general de la Red ATB（ATB 广播网总经理）、gerente de la Red ATB 等，均指同一职务。任命的确切日期未见公布：2025-12-12 前台长 Iturri 被新董事会解职，2026-01-13 Torrico 已以「新任总经理」身份公开确认人事变动，其上任时间应处于该窗口内。",
    "contacts": [
        {
            "type": "website",
            "value": "http://www.atb.com.bo",
            "source": "其执掌机构 Red ATB 官方网站（本次采集已访问核实）；ATB 官网未公布总经理个人直联电话或邮箱，官网页脚所载联系方式均为各城市商务人员（vromero@、cfigueroa@、comercialcbb@atb.com.bo 等），不属于本人。",
        }
    ],
    "current_positions": ["玻利维亚ATB电视台（Red ATB）总经理"],
    "education": [],
    "education_note": "公开资料未检索到其学历、毕业院校等教育信息。",
    "work_experience": [
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚ATB电视台 (Red ATB)",
            "org_id": "BO-MEDIA-011",
            "position": "总经理",
        }
    ],
    "person_relationships": [
        {
            "person_id": None,
            "person_name": "海梅·伊图里·萨尔蒙 (Jaime Iturri Salmón)",
            "relationship_type": "other",
            "description": "前任。伊图里（绰号「吉米」Jimmy）为 ATB 前台长及 Invesbol 时期主要股东（前实际控制人），2025-12-12 被 ATB 新董事会解职、劳动关系于 2025 年 12 月终止；Torrico 作为新任总经理于 2026-01-13 公开确认其离任并签署公开信称「将铭记 Jimmy Iturri 在频道的领导，其多年任期已到终点，为 ATB 的更新让路」，标志与 Iturri 时代的切割。Iturri 离任背景涉欠薪、社保欠缴及对其在 ATB、PAT 收购与管理中涉嫌违规的指控（尚未判决）。",
        },
        {
            "person_id": None,
            "person_name": "玛丽亚·雷内·杜申·奎利亚尔 (María Renee Duchén Cuéllar)",
            "relationship_type": "colleague",
            "description": "同属 ATB 核心管理团队：Duchén 任拉巴斯及全国广播网新闻部主任，Torrico 任总经理；西语维基百科 ATB 条目「关键人物」（personas clave）将两人并列。",
        },
        {
            "person_id": None,
            "person_name": "安赫拉·莫拉 (Ángela Mora)",
            "relationship_type": "colleague",
            "description": "新管理层成员：Torrico 于 2026-01-13 宣布 ATB 更新阶段时，同时宣布莫拉将在频道领导层中承担重要角色（rol protagónico en la dirección）。",
        },
        {
            "person_id": None,
            "person_name": "卡门·梅尔加·苏亚雷斯 (Carmen Melgar Suárez)",
            "relationship_type": "colleague",
            "description": "ATB 健康节目《Medicina al Rescate》主持人；2026-10-01 与 Torrico 共同出席玻利维亚众议院致敬医务工作者活动（Torrico 以 Red ATB 总经理身份、梅尔加以节目记者身份）。",
        },
    ],
    "social_accounts": [],
    "social_accounts_note": "已按要求完成 6 平台扫描（Facebook/X-Twitter/LinkedIn/Instagram/TikTok/YouTube）：Facebook 仅见 ATB 官方账号 atbmediabol 发布其言行，未发现可核实的本人账号；LinkedIn 检索到 8 个同名档案（玻利维亚拉巴斯学生、阿根廷 Banco Galicia 技术主管、美国人士等），均无法确认为本人；X/Twitter、TikTok、YouTube 未发现本人账号；Instagram @torricoillanes（Amilcar Torrico Illanes）同名者无法核实为本人。故 social_accounts 留空，防同名误挂。",
    "family_members": [],
    "family_note": "ATB 官方 2026-10-21 帖文证实其已婚（与妻子共同庆祝结婚 19 周年），但配偶姓名及其子女信息均未见公开报道，按规则（family_members[].name 须为真实全名）不列具体条目。网络检索摘要中出现的配偶姓名说法相互矛盾且无法溯源到原文，不予采信。",
    "political_stances": [
        {
            "date": "2026-01-13",
            "topic": "公开立场：频道编辑定位与去党派化",
            "stance_content": "以新任总经理身份宣布 ATB 更新阶段时，提出要让 ATB 成为「全家人平等共同观看的频道」（el canal de la familia），以节目改版与管理重组回应前 Iturri 时期的编辑倾向争议；其表态聚焦经营与节目，未表达党派立场。",
            "source": "Visión360 (2026-01-13)",
        },
        {
            "date": "2026-10-21",
            "topic": "公开立场：新闻职业操守",
            "stance_content": "在 ATB 建台 42 周年之际表示，目标是延续 ATB 的遗产、强化团队承诺，并「继续坚持基于诚实与客观的新闻」（un periodismo basado en la honestidad y la objetividad）。",
            "source": "ATB Media 官方 Facebook (2026-10-21)",
        },
    ],
    "major_achievements": [
        {
            "date": "2026-01-13",
            "achievement": "以新任总经理身份公开确认前台长海梅·「吉米」·伊图里离任，并签署公开信宣布 ATB 进入「更新阶段」，启动管理与节目结构全面改版，承诺打造「有能力、专业化」的新团队。",
            "organization": "玻利维亚ATB电视台 (Red ATB)",
        },
        {
            "date": "2026-04-15",
            "achievement": "在拉巴斯米拉弗洛雷斯区 Av. Argentina 总部主持发布 ATB 新品牌形象与全新节目单，口号更新为「Estamos de vuelta」（我们回来了），恢复「家庭频道」（el canal de la familia）定位。",
            "organization": "玻利维亚ATB电视台 (Red ATB)",
        },
        {
            "date": "2026-05-01",
            "achievement": "宣布 ATB 以「Estamos de vuelta」为主题重返 2026 年科恰班巴国际博览会（FEXCO 2026），设立新展台并获 FIPAZ（国际博览会行业协会）对频道社会贡献的表彰，推动频道商业与公共形象重启。",
            "organization": "玻利维亚ATB电视台 (Red ATB)",
        },
        {
            "date": "2026-10-01",
            "achievement": "作为 Red ATB 总经理出席玻利维亚众议院致敬医务工作者活动（同席有《Medicina al Rescate》主持人 Carmen Melgar Suárez），并代表频道接受对其新闻历程与对玻利维亚新闻业贡献的表彰。",
            "organization": "玻利维亚众议院 (Cámara de Diputados)",
        },
    ],
    "biography_summary": (
        "阿米尔卡·托里科（Amílcar Torrico）是玻利维亚全国性私营电视台 ATB（Red ATB）现任总经理"
        "（Gerente General），于前实际控制人海梅·「吉米」·伊图里·萨尔蒙（Jaime Iturri Salmón）离任后执掌该台。"
        "2025-12-12，ATB 新董事会决定不再续任伊图里的职务，结束其延续至 2025 年 12 月的劳动关系；"
        "2026-01-13，托里科首次以「新任总经理」身份见诸报道，公开确认伊图里离任，并签署公开信宣布 ATB 进入"
        "「更新阶段」，同时宣布安赫拉·莫拉（Ángela Mora）将在领导层中承担重要角色。此后他主导频道全面重塑："
        "2026-04-15 在拉巴斯总部发布新品牌形象与新节目单（口号「Estamos de vuelta」，恢复「家庭频道」定位），"
        "同年 5 月宣布重返 FEXCO 2026 展会，10 月 1 日代表 ATB 出席玻利维亚众议院致敬医生活动并接受对频道"
        "新闻贡献的表彰。其个人早年履历（出生日期、学历、入台前职业）均未见公开报道；其就任正值 ATB 深陷欠薪、"
        "社保欠缴及前管理层司法调查的危机期（2025-2026），与玻利维亚 2025 年 11 月政府换届后的媒体格局变动相叠。"
        "现有公开信息显示其任命系企业董事会层面重组所致，暂无证据表明其为帕斯新政府直接任命。"
    ),
    "profile": {
        "source_url": profile_source_url,
        "local_path": local_path,
    },
    "profile_note": (
        "配图取自 ATB Media 官方 Facebook 2026-10-21 发布的 Torrico 出镜致辞视频缩略图"
        "（Amílcar Torrico, gerente general de ATB, recordó los desafíos...）。"
        "该人物无维基数据条目、无维基百科人像，Facebook CDN 直链会过期，本地已存副本。"
    ),
    "collection_meta": {
        "collection_date": "2026-10-26",
        "phase": "phase4_person_profile",
        "data_sources": [
            "news_search",
            "web_search",
            "wikipedia",
            "official_website",
            "government_directory",
            "social_media",
        ],
        "notes": (
            "数据来源：精读 6 个独立全文来源——Visión360 报道两篇（2026-01-13 确认 Iturri 离任；2026-04-15 新品牌发布）、"
            "Los Tiempos（2026-01-14，转 Urgente.bo，含 Torrico 署名公开信引文）、西语维基百科 ATB 条目全文、"
            "玻利维亚众议院官网新闻页（2026-10-01 活动出席名单）、ATB 官网首页（联系方式核实）；"
            "另直接核读 ATB Media 官方 Facebook 帖文 4 条（42 周年双重庆祝、42 周年致辞视频、FEXCO 2026 重返、"
            "Expocruz 2026 露天音乐会）。关键发现：Torrico 系 Iturri 之后的新任总经理，Iturri 于 2025-12-12 被新董事会"
            "解职、Torrico 至迟于 2026-01-13 以新总经理身份公开活动；2026 年频道完成品牌与节目改版。"
            "存疑与留空说明：①全名（母姓）未见任何来源公布，name 按通行拼写；②出生日期、出生地、学历、入台前职业"
            "查无公开资料，相应字段留空；③任命精确日期未公布，仅能框定在 2025-12 至 2026-01 窗口（见 position_note）；"
            "④配偶已婚事实有官方帖文佐证但姓名未公开，family_members 留空；⑤本人社交媒体账号未能核实（同名者多，"
            "LinkedIn 8 个同名档案均不符），social_accounts 留空；⑥未检索到帕斯新政府直接任命的证据，"
            "biography 中仅作审慎表述；⑦name_zh 因无可靠既有译名按指示置 null。"
            "completeness_score 说明：目标 85 分受公开信息客观限制——教育、家庭、社媒三类核心维度经多语言检索后"
            "确无可用事实，已尽力以 4 条主要成就、4 条人物关系、2 条公开立场、200+ 字中文传记补足，最终分数见"
            "collection_meta.completeness_score。注意勿与同台新闻部主任 María Renee Duchén（BO-PERSON-000408 待派）、"
            "前控制人 Jaime Iturri（BO-PERSON-000409 待派）混淆；玻利维亚 Torrico 为常见姓氏，"
            "检索中已排除警察总监、众议员、制片人等同名者。"
        ),
        "quotes": [
            {
                "title": "ATB anuncia una etapa de renovación y confirma la salida de Jaime Iturri — Visión360 (2026-01-13)",
                "url": "https://www.vision360.bo/noticias/2026/01/13/38377-atb-anuncia-una-etapa-de-renovacion-y-confirma-la-salida-de-jaime-iturri",
            },
            {
                "title": "Nuevo gerente de ATB confirma salida de Jaime Iturri y anuncia renovación — Los Tiempos (2026-01-14)",
                "url": "https://lostiempos.com/actualidad/pais/20260114/nuevo-gerente-atb-confirma-salida-jaime-iturri-anuncia-renovacion",
            },
            {
                "title": "ATB (canal de televisión) — Wikipedia (español)",
                "url": "https://es.wikipedia.org/wiki/ATB_(canal_de_televisi%C3%B3n)",
            },
            {
                "title": "ATB estrena marca y renueva su parrilla de programación — Visión360 (2026-04-15)",
                "url": "https://www.vision360.bo/noticias/2026/04/15/40800-atb-estrena-marca-y-renueva-su-parrilla-de-programacion",
            },
            {
                "title": "Cámara de Diputados de Bolivia 新闻页：致敬医生活动出席者含 Red ATB 总经理 Amílcar Torrico (2026-10-01)",
                "url": "https://diputados.gob.bo/prensa-noticias-back",
            },
            {
                "title": "ATB Media 官方 Facebook：DOBLE FESTEJO — ATB 42 周年暨 Torrico 结婚 19 周年 (2026-10-21)",
                "url": "https://www.facebook.com/atbmediabol/posts/122240954276554356",
            },
            {
                "title": "ATB Media 官方 Facebook 视频：Amílcar Torrico, gerente general de ATB, recordó los desafíos (2026-10-21)",
                "url": "https://www.facebook.com/atbmediabol/videos/2679519202496572",
            },
            {
                "title": "ATB Media 官方 Facebook 视频：ATB relanza su presencia en la FEXCO 2026 (2026-05-01)",
                "url": "https://www.facebook.com/atbmediabol/videos/2403152720190141",
            },
        ],
    },
}

bio = data["biography_summary"]
print("biography_summary length:", len(bio))
assert len(bio) >= 200, "biography_summary must be >= 200 chars"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("written:", OUT)

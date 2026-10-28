# -*- coding: utf-8 -*-
"""Build BO-PERSON-000226 person profile JSON (Christian Hausherr Ariñez)."""
import json
import os

OUT_DIR = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24"
PERSONS_DIR = os.path.join(OUT_DIR, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

profile = {
    "person_id": "BO-PERSON-000226",
    "wikidata_qid": None,
    "name": "Christian Hausherr Ariñez",
    "name_en": "Christian Hausherr Arinez",
    "name_zh": None,
    "aliases": ["Christian Hausherr"],
    "nationality": "BO",
    "country_iso3": "BOL",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "birth_date_note": "公开资料（新闻报道、ASFI 登记卡、访谈及 LinkedIn）均未披露出生日期与出生地",
    "contacts": [
        {
            "type": "email",
            "value": "chausherr@bcp.com.bo",
            "source": "ASFI 证券市场登记卡（Banco de Crédito de Bolivia S.A.，2022 年归档快照所载登记邮箱，推断为其企业邮箱）"
        }
    ],
    "current_positions": [
        "玻利维亚信贷银行总经理",
        "玻利维亚私营银行协会第二副主席"
    ],
    "education": [
        {
            "institution": "威斯康星大学 (Universidad de Wisconsin)",
            "degree": "bachelor",
            "field": "经济学"
        },
        {
            "institution": "罗切斯特大学西蒙商学院 (University of Rochester - Simon Business School)",
            "degree": "master",
            "field": "金融与公司战略"
        }
    ],
    "work_experience": [
        {
            "organization": "花旗银行 (Citigroup)",
            "org_id": None,
            "position": "银行业务岗位（纽约，职业生涯起点，具体职务未公开）",
            "start_date": None,
            "end_date": None
        },
        {
            "organization": "秘鲁信贷银行 (Banco de Crédito del Perú)",
            "org_id": None,
            "position": "国际债券发行业务负责人（主导 BCP 秘鲁首次国际债券发行，具体职级未公开）",
            "start_date": None,
            "end_date": None
        },
        {
            "organization": "玻利维亚信贷银行 (Banco de Crédito de Bolivia)",
            "org_id": "BO-FIN-003",
            "position": "金融与资本市场部总经理",
            "start_date": "2012-07-17",
            "end_date": "2024"
        },
        {
            "organization": "玻利维亚信贷银行 (Banco de Crédito de Bolivia)",
            "org_id": "BO-FIN-003",
            "position": "总经理",
            "start_date": "2024-10",
            "end_date": None
        },
        {
            "organization": "玻利维亚私营银行协会 (Asociación de Bancos Privados de Bolivia)",
            "org_id": None,
            "position": "第二副主席",
            "start_date": "2025-03",
            "end_date": None
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000646",
            "person_name": "路易斯·阿曼多斯 (Luis Almandoz)",
            "relationship_type": "colleague",
            "description": "Hausherr 的 BCP 玻利维亚总经理职位前任（秘鲁籍）。2024 年 10 月 Hausherr 接任该职，阿曼多斯返回秘鲁出任 Credicorp 集团中小企业业务与渠道部总经理。"
        },
        {
            "person_id": "BO-PERSON-000261",
            "person_name": "罗纳德·古铁雷斯·洛佩斯 (J. Ronald Gutiérrez López)",
            "relationship_type": "colleague",
            "description": "玻利维亚牧业银行（Banco Ganadero）总经理，2025 年 3 月当选玻利维亚私营银行协会（ASOBAN）2025-2026 届主席；Hausherr 在同一届理事会中出任第二副主席，两人为协会同僚。"
        },
        {
            "person_id": "BO-PERSON-000647",
            "person_name": "阿里埃尔·穆斯塔法 (Ariel Mustafá)",
            "relationship_type": "associate",
            "description": "拉巴斯阿尔蒂米拉画廊（Galería Altamira）主理人，2020 年与 Hausherr 及丹妮埃拉·埃斯皮诺萨三人共同编辑出版《Arte contemporáneo en Bolivia》一书。"
        },
        {
            "person_id": "BO-PERSON-000648",
            "person_name": "丹妮埃拉·埃斯皮诺萨 (Daniela Espinoza)",
            "relationship_type": "associate",
            "description": "阿尔蒂米拉画廊联合主理人，《Arte contemporáneo en Bolivia》（2020）共同编辑。"
        }
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Christian Hausherr",
            "url": "https://bo.linkedin.com/in/christian-hausherr-1a27403",
            "source": "LinkedIn 公开主页（其玻利维亚 BCP 总经理身份与 BCP 官方帖文转发活动相互印证）；注意与德意志银行同名高管（christian-hausherr-784670b）非同一人"
        }
    ],
    "family_members": [],
    "political_stances": [
        {
            "date": "2024",
            "topic": "金融普惠与数字化",
            "stance_content": "在就任总经理前后宣布 BCP 将在玻利维亚投资逾 5000 万美元，推动 600 万玻利维亚人获得银行服务，称「期望我国每 10 位居民中至少 5 人能够通过数字平台和我们的移动钱包 YAPE 获得并受益于我们的金融服务」。",
            "source": "El Deber（2024-10-09）"
        },
        {
            "date": "2025-11",
            "topic": "银行业对外开放与融资多元化",
            "stance_content": "在「Visión Bolivia 2025」论坛「Capital Futuro」分论坛上主张玻利维亚银行业向国际融资开放：称目前银行体系资金几乎完全依赖国内存款（居民、企业与社保基金），外部融资几乎不存在，限制了对大型生产项目的支持；开放国际市场可让国家更快增长、以不同条件为长期项目融资，并建议允许公共长期社保基金管理公司（Gestora Pública）将部分退休金资产投资海外，以分散风险、改善收益。",
            "source": "Nueva Economía（2025-11-10）"
        },
        {
            "date": "2025-11",
            "topic": "金融数字化与减少现金使用",
            "stance_content": "指出玻利维亚 60%-70% 的经济活跃人口已使用移动钱包或银行应用，但 95% 的人口仍以现金为主要支付手段；提出数字化三支柱（获得工具、了解金融产品、主动使用），并表示「我们最主要的敌人仍然是现金」，主张加强国民数字金融能力培训。",
            "source": "Nueva Economía（2025-11-10）"
        },
        {
            "date": "2026-09",
            "topic": "气候变化与经济韧性",
            "stance_content": "在其推动下 BCP 举办「玻利维亚面对厄尔尼诺」（Bolivia Frente al Niño）论坛，召集 500 余名公共部门、企业、国际组织、学术界与公民社会代表研讨 2026-2027 年厄尔尼诺现象的气候情景与经济影响，并提出「气候适应也是一个经济挑战」，主张提早预判风险、强化跨部门协调以保护就业与民生。",
            "source": "Christian Hausherr LinkedIn 帖文及 BCP 官方账号（2026-09）"
        }
    ],
    "major_achievements": [
        {
            "date": "2024-10",
            "achievement": "获任命出任玻利维亚信贷银行（BCP）总经理（2024 年 10 月 1 日就任），接替返回秘鲁 Credicorp 集团任职的 Luis Almandoz。",
            "organization": "玻利维亚信贷银行 (Banco de Crédito de Bolivia)"
        },
        {
            "date": "2020-12",
            "achievement": "与画廊主 Ariel Mustafá、Daniela Espinoza 共同编辑出版《Arte contemporáneo en Bolivia》（玻利维亚当代艺术）参考图录，收录 53 位艺术家、700 余幅作品图和 4 篇专文，填补该国当代艺术文献 35 年的出版空白；2020 年 12 月 15 日在拉巴斯 Hotel Casa Grande 举行首发。",
            "organization": "阿尔蒂米拉画廊 (Galería Altamira)"
        },
        {
            "date": "2025-03",
            "achievement": "当选玻利维亚私营银行协会（ASOBAN）2025-2026 届理事会第二副主席。",
            "organization": "玻利维亚私营银行协会 (Asociación de Bancos Privados de Bolivia)"
        },
        {
            "date": "2024",
            "achievement": "主导宣布 BCP 逾 5000 万美元的在玻投资计划，目标推动 600 万玻利维亚人实现银行账户覆盖（bancarización），并大力推广移动钱包 YAPE。",
            "organization": "玻利维亚信贷银行 (Banco de Crédito de Bolivia)"
        },
        {
            "date": "2026",
            "achievement": "其领导下 BCP 在 ICC Bolivia 2026（企业诚信公约）评估中，于 37 家受评企业里获得最高评级 AAA+（仅 8 家企业获此评级）。",
            "organization": "玻利维亚信贷银行 (Banco de Crédito de Bolivia)"
        }
    ],
    "biography_summary": "克里斯蒂安·豪塞尔·阿里涅斯（Christian Hausherr Ariñez）是玻利维亚经济学家，现任玻利维亚信贷银行（Banco de Crédito de Bolivia，简称 BCP，属秘鲁 Credicorp 金融控股集团）总经理，2024 年 10 月 1 日就任，接替返回秘鲁集团任职的 Luis Almandoz。他毕业于威斯康星大学经济学专业，拥有罗切斯特大学（西蒙商学院）金融与公司战略硕士学位，银行业生涯始于纽约花旗银行。他在 Credicorp 集团工作逾 15 年，曾于秘鲁信贷银行主导该行首次国际债券发行；2012 年 7 月起任 BCP 玻利维亚金融与资本市场部总经理，并负责 Credibolsa、Credifondo、Crediseguro 等集团公司的管理，是玻利维亚「信贷金融集团」（Grupo Financiero Crédito，旗下 6 家公司）组建与巩固的重要参与者。2025 年 3 月，他当选玻利维亚私营银行协会（ASOBAN）2025-2026 届第二副主席。任内他公开主张银行业向国际融资开放、深化金融普惠与数字化，宣布逾 5000 万美元投资以推动 600 万玻利维亚人实现银行化。他自认是阅读爱好者与玻利维亚艺术收藏者，2020 年曾与他人合编出版《Arte contemporáneo en Bolivia》一书。",
    "profile": {
        "source_url": "https://brujuladigital.net/images/news/es/b_38338_christian-hausherr-es-el-nuevo-gerente-general-del-bcp-1.jpg",
        "local_path": "photos/BO-PERSON-000226.jpg"
    },
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "news_search",
            "web_search",
            "social_media",
            "government_registry"
        ],
        "notes": "关键事实均以 ≥2 个独立来源交叉验证：总经理任命与就任时间（El Deber、Brújula Digital、Los Tiempos、La República、MarketScreener、ASFI 登记卡快照）、学历与经历（El Deber、Trendsetter Bolivia TST Nº31、LinkedIn）、ASOBAN 第二副主席（El Día/ABI、El Mundo、CADECOCRUZ）、艺术图录合编（Zoe Radio/Página Siete 全文、El Diario、okey.bo）。ASFI 证券市场登记卡（2022 年归档快照，经 Wayback Machine 直取全文）确认其玻利维亚国籍、经济学家职业资格、2012-07-17 出任 BCP 玻利维亚金融与资本市场部总经理，并列有其登记邮箱 chausherr@bcp.com.bo（推断为企业邮箱）；该卡亦载明 BCP 股权结构：Inversiones Credicorp Bolivia S.A. 95.84%、Credicorp Ltd. 4.07%。查证后留空的字段：出生日期/出生地（无公开来源）；family_members（无公开信息）；wikidata_qid（无 Wikidata 条目）；name_zh 置 null——中文媒体无既有可靠译名，_name_index.json 中的「克里斯蒂安·豪塞尔·阿里涅斯」仅为本项目内部音译，未见任何中文媒体使用。社交媒体仅 LinkedIn 可确证归属；Instagram 账号 hausherr.christian 因无法核实是否本人未收录；Facebook/X/TikTok/YouTube 未发现可归因账号（Facebook 及 YouTube 上的「Christian Hausherr」均为瑞士/德国同名者，已排除）。Citigroup 与 BCP 秘鲁任职期间的具体职务名称及起止年份公开资料未披露，相关条目日期留空。ID 说明：person_relationships 中 Luis Almandoz（BO-PERSON-000646）、Ariel Mustafá（BO-PERSON-000647）、Daniela Espinoza（BO-PERSON-000648）为更新版 _name_index.json 已注册 ID，予以采用；秘鲁信贷银行（BCP 秘鲁）与玻利维亚私营银行协会（ASOBAN）未收录于 _name_index.json，org_id 置 null——自动富集流程曾将 ASOBAN 误关联至 BO-INTL-004（实为拉美一体化协会 ALADI）、将 BCP 秘鲁误关联至 BO-FIN-003（实为 BCP 玻利维亚），均系同前缀误匹配，已纠正为 null。ASOBAN 主席任期 El Día 报道为 2025-2026 届、El Mundo 标题作 2025-2027 届，本档案采用 Hausherr 当选届次表述「2025-2026 届」。",
        "quotes": [
            {
                "title": "Christian Hausherr es el nuevo gerente general del BCP - El Deber",
                "url": "https://eldeber.com.bo/te-puede-interesar/christian-hausherr-es-el-nuevo-gerente-general-del-bcp/"
            },
            {
                "title": "Christian Hausherr, CEO del BCP - Trendsetter Bolivia TST Nº 31",
                "url": "https://www.trendsetterbolivia.com/tst/christian-hausherr"
            },
            {
                "title": "Ronald Gutiérrez López es elegido como nuevo Presidente de la Asociación de Bancos Privados de Bolivia - El Día (ABI)",
                "url": "https://eldia.com.bo/2025-03-27/economia/ronald-gutierrez-lopez-es-elegido-como-nuevo-presidente-de-la-asociacion-de-bancos-privados-de-bolivia.html"
            },
            {
                "title": "Tarjeta de Registro - Banco de Crédito de Bolivia S.A. (ASFI, 2022 归档快照)",
                "url": "https://appweb.asfi.gob.bo/Reportes_asp/rmi/tarjeta.asp?c=51828&t=2"
            },
            {
                "title": "Christian Hausherr Ariñez: Positions, Relations and Network - MarketScreener",
                "url": "https://www.marketscreener.com/insider/CHRISTIAN-HAUSHERR-ARINEZ-A30PTQ/"
            },
            {
                "title": "Christian Hausherr - Gerente General del Banco de Crédito de Bolivia - LinkedIn",
                "url": "https://bo.linkedin.com/in/christian-hausherr-1a27403"
            },
            {
                "title": "BCP plantea abrir la banca al financiamiento internacional y fortalecer la inclusión digital - Nueva Economía",
                "url": "https://nuevaeconomia.com.bo/news/bcp-plantea-abrir-la-banca-al-financiamiento-internacional-y-fortalecer-la-inclusin-digital"
            },
            {
                "title": "35 años de arte contemporáneo plasmados en más de 300 páginas - Zoe Radio Bolivia (源: Página Siete)",
                "url": "https://zoeradiobolivia.com/2020/12/16/35-anos-de-arte-contemporaneo-plasmados-en-mas-de-300-paginas/"
            },
            {
                "title": "Christian Hausherr es el nuevo gerente general del BCP - Brújula Digital",
                "url": "https://brujuladigital.net/economia/2024/10/09/christian-hausherr-es-el-nuevo-gerente-general-del-bcp-38338"
            }
        ]
    }
}

out_path = os.path.join(PERSONS_DIR, "BO-PERSON-000226.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE", out_path)
print("bio_len =", len(profile["biography_summary"]))

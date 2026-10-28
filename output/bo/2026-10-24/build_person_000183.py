# -*- coding: utf-8 -*-
"""Build person profile JSON for BO-PERSON-000183 (José Fernando Córdova Eguivar)."""
import json
import os

OUT_DIR = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons"
OUT_FILE = os.path.join(OUT_DIR, "BO-PERSON-000183.json")

person = {
    "person_id": "BO-PERSON-000183",
    "wikidata_qid": None,
    "name": "José Fernando Córdova Eguivar",
    "name_en": "Jose Fernando Cordova Eguivar",
    "name_zh": "何塞·费尔南多·科尔多瓦·埃吉瓦尔",
    "aliases": [
        "José Córdova Eguivar",
        "Fernando Córdova",
        "Dr. Ing. José Fernando Córdova Eguivar"
    ],
    "nationality": "BO",
    "gender": "male",
    "birth_date": "1954-03-17",
    "birth_place": "奥鲁罗 (Oruro)",
    "current_positions": [
        "玻利维亚国家矿业公司临时执行总裁 (Presidente Ejecutivo Interino, COMIBOL)"
    ],
    "work_experience": [
        {
            "start_date": "1997-09",
            "end_date": "1998",
            "organization": "德国某跨国公司 (empresa transnacional alemana)",
            "org_id": None,
            "position": "冶金工程师（哥伦比亚桑坦德省苏拉塔河去污染项目）"
        },
        {
            "start_date": "2025-12-08",
            "end_date": None,
            "organization": "玻利维亚国家矿业公司 (Corporación Minera de Bolivia)",
            "org_id": "BO-SOE-002",
            "position": "临时执行总裁（Presidente Ejecutivo Interino / a.i.）"
        }
    ],
    "education": [],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000068",
            "person_name": "马尔科·安东尼奥·卡尔德龙·德拉巴尔卡·金塔尼利亚 (Marco Antonio Calderón de la Barca Quintanilla)",
            "relationship_type": "superior",
            "description": "玻利维亚矿业与冶金部部长；2025年12月8日在矿业部主持其COMIBOL临时执行总裁就职（posesión）仪式"
        },
        {
            "person_id": "BO-PERSON-000001",
            "person_name": "罗德里戈·帕斯·佩雷拉 (Rodrigo Paz Pereira)",
            "relationship_type": "superior",
            "description": "玻利维亚总统；对其任命属于帕斯政府矿业部门「现代化与机构强化」整体改组人事安排"
        },
        {
            "person_id": "BO-PERSON-000070",
            "person_name": "潘菲洛·马尔卡·尼娜 (Pánfilo Marca Nina)",
            "relationship_type": "colleague",
            "description": "同日（2025-12-08）由矿业部长共同授职的合作社矿业副部长（Viceministro de Cooperativas Mineras）"
        },
        {
            "person_id": "BO-PERSON-000069",
            "person_name": "沃尔特·路易斯·兰迪瓦尔·卡斯特多 (Walter Luis Landívar Castedo)",
            "relationship_type": "colleague",
            "description": "同日（2025-12-08）被任命为矿业政策、监管与监察副部长（Viceministro de Política Minera, Regulación y Fiscalización）"
        },
        {
            "person_id": "BO-PERSON-000180",
            "person_name": "豪尔赫·雷内·贝略特·拉托雷 (Jorge René Bellot La Torre)",
            "relationship_type": "colleague",
            "description": "同日（2025-12-08）被任命为矿业地质服务局（SERGEOMIN）执行主任；2026年8月两人分别代表COMIBOL与SERGEOMIN签署五年期勘探合作协议"
        },
        {
            "person_id": None,
            "person_name": "乌戈·马塞洛·阿萨贝·巴斯克斯 (Hugo Marcelo Arzabe Vásquez)",
            "relationship_type": "colleague",
            "description": "同日（2025-12-08）被任命为温托冶金公司（Empresa Metalúrgica Vinto）总经理，同属矿业国企新领导层"
        },
        {
            "person_id": None,
            "person_name": "埃德温·沃尔夫 (Edwin Wolf)",
            "relationship_type": "associate",
            "description": "哥伦比亚工程师；1998年6月与其一同在哥伦比亚桑坦德省遭FARC绑架，同年8月3日一同获释，二人当时同在苏拉塔河从事去污染工程"
        }
    ],
    "social_accounts": [
        {
            "platform": "twitter_x",
            "account_name": "Jose Fernando Cordova Eguivar (@jose_eguivar)",
            "url": "https://x.com/jose_eguivar",
            "source": "X搜索索引显示全名完全匹配的账号（2020年12月注册，66条帖文、18名关注者）；账号是否为本人运营未经官方验证，谨慎采信"
        }
    ],
    "family_members": [],
    "contacts": [
        {
            "type": "website",
            "value": "https://www.comibol.gob.bo",
            "source": "COMIBOL《2025年度公共账目报告》其署名页（Pagina web: www.comibol.gob.bo）；机构官网，非个人联系方式"
        },
        {
            "type": "phone",
            "value": "+591 2 2682100",
            "source": "COMIBOL《2025年度公共账目报告》其署名页（Teléfono: 2682100）；拉巴斯中央办公室总机，非个人私人电话"
        }
    ],
    "political_stances": [
        {
            "date": "2025-12-09",
            "topic": "COMIBOL机构现代化与效率",
            "stance_content": "就任时承诺「我们要推动现代化、整顿秩序、提高工作效率」（Vamos a trabajar para modernizar, organizar y hacer más eficientes nuestras tareas），称方法理顺后一切开始流畅，改革可能需要时间",
            "source": "https://eju.tv/2025/12/cordova-se-traza-el-reto-de-modernizar-y-hacer-mas-eficiente-a-comibol/"
        },
        {
            "date": "2026-04-13",
            "topic": "国有矿业的社会与生产价值",
            "stance_content": "主张国有矿业应按其社会和生产效益来评价：2025年COMIBOL经济流动额逾21.48亿玻利维亚诺、向国库直接转移逾1.56亿诺，并出资4950万诺资助「胡安西托·平托」助学金",
            "source": "https://lapatria.bo/dinero-negocios/comibol-reporta-movimiento-economico-de-bs-2-148-millones-en-2025/"
        },
        {
            "date": "2026-04-20",
            "topic": "打击矿石盗窃（jukeo）",
            "stance_content": "在胡阿努尼矿业公司（Empresa Minera Huanuni）新总经理就职时要求其遏制jukeo（矿石盗窃）并提升公司产量",
            "source": "https://hemeroteca.larazon.bo/economia-y-empresa/2026/04/20/comibol-posesiona-a-velasco-como-gerente-de-la-empresa-minera-huanuni/"
        },
        {
            "date": "2026-09-03",
            "topic": "托克公司（Trafigura）商业合同争议",
            "stance_content": "针对媒体关于COMIBOL子公司与托克公司违规交易的报道公开否认：「具体而言，Corocoro与Trafigura之间不存在任何合同」，并说明2026年科罗科罗铜三次公开招标均未授标、Colquiri锌招标中托克被取消资格",
            "source": "https://larazon.bo/economia-y-empresa/2026/09/06/comibol-niega-contratos-con-trafigura-por-cobre-de-corocoro-y-zinc-de-colquiri/"
        },
        {
            "date": "2026-10-02",
            "topic": "国有矿业振兴与勘探扩张",
            "stance_content": "在COMIBOL成立74周年之际表示「是时候向前看，让COMIBOL再次伟大」，主张多生产、多勘探、推进新项目以强化国有矿业",
            "source": "https://lapatria.bo/cultura-viva/historia-y-geografia/comibol-celebra-anos-historia-minera-bolivia/"
        }
    ],
    "major_achievements": [
        {
            "date": "2025-12-08",
            "achievement": "被矿业部长卡尔德龙任命为COMIBOL临时执行总裁，与两名副部长及温托、SERGEOMIN等国企新负责人同期就任，成为帕斯政府矿业整顿班子的核心成员，获COMIBOL工会与董事会当场表态支持",
            "organization": "玻利维亚国家矿业公司 (Corporación Minera de Bolivia)"
        },
        {
            "date": "2026-03",
            "achievement": "率COMIBOL参加在加拿大多伦多举行的PDAC 2026国际矿业大会，向国际投资者推介Mesa de Plata（Eureka/Machu Socavón）、Cerro Manomó、Rincón del Tigre、Fénix、Real del Monte Pulacayo等7个银金及稀土、铌、铂族项目",
            "organization": "玻利维亚国家矿业公司 (Corporación Minera de Bolivia)"
        },
        {
            "date": "2026-05-04",
            "achievement": "在2026年度公共账目听证会上公布COMIBOL年度规划：预计收入60.32亿玻利维亚诺、创汇7.865亿美元，并设定Huanuni、Colquiri、Corocoro、Karachipampa等下属企业生产目标",
            "organization": "玻利维亚国家矿业公司 (Corporación Minera de Bolivia)"
        },
        {
            "date": "2026-08-20",
            "achievement": "与SERGEOMIN签署为期五年的机构间协议，在COMIBOL专属矿区内联合开展地形、地质、地球化学、地球物理研究及勘探钻探与矿产资源估算",
            "organization": "玻利维亚国家矿业公司 (Corporación Minera de Bolivia)"
        },
        {
            "date": "2026-09-06",
            "achievement": "针对媒体曝光的与托克公司（Trafigura）约3100万至3400万美元交易质疑，主导发布官方公报逐项澄清，否认Corocoro与Colquiri存在任何合同，平息腐败争议",
            "organization": "玻利维亚国家矿业公司 (Corporación Minera de Bolivia)"
        }
    ],
    "biography_summary": "何塞·费尔南多·科尔多瓦·埃吉瓦尔（José Fernando Córdova Eguivar），玻利维亚冶金工程师，1954年3月17日生于奥鲁罗。据玻利维亚ANF/Fides通讯社1998年8月报道，其于1997年9月赴哥伦比亚为一家德国跨国公司从事河流去污染工程，1998年6月在桑坦德省遭FARC游击队绑架，同年8月3日在奥卡尼亚获释，报道以全名+冶金工程师+奥鲁罗籍三重信息与其现身份吻合。此后长期从事冶金与矿业工程工作（具体履历公开资料有限），持有工程博士学位头衔（Dr. Ing.，见COMIBOL及科罗科罗矿业公司官方材料）。2025年12月8日，在罗德里戈·帕斯政府矿业部门整体改组中，被矿业与冶金部长马尔科·卡尔德龙任命为玻利维亚国家矿业公司（COMIBOL）临时执行总裁，肩负「现代化、整顿、提高效率」使命，获公司工会与董事会支持。任内主持编制2026年度预算（预计收入逾60.3亿玻利维亚诺），率团参加多伦多PDAC 2026推介7个勘探项目，签署COMIBOL-SERGEOMIN五年勘探协议，并于2026年9月公开否认COMIBOL子公司与托克（Trafigura）公司存在合同、回应腐败质疑。截至2026年10月仍以「临时/代理」名义执掌COMIBOL。",
    "birth_date_note": "出生于1954年3月17日的依据为玻利维亚ANF/Fides通讯社1998年8月3日对其遭FARC绑架获释的报道（当时44岁、冶金工程师、生于奥鲁罗），全名与现任COMIBOL临时执行总裁完全一致；因系单一来源且年代较早，置信度中等",
    "birth_place_note": "出生地奥鲁罗（Oruro）来源同上（ANF/Fides 1998-08-03报道）；其家庭当时亦居住于奥鲁罗",
    "education_note": "公开来源仅确认其职业身份为冶金工程师（metalurgista / ingeniero metalúrgico）并持有Dr. Ing.（工程博士）头衔（COMIBOL 2025年终账目报告PDF、科罗科罗矿业公司官网、ABI报道照片说明）；具体毕业院校与学位授予时间未见公开报道，故education留空",
    "family_note": "1998年ANF报道提及其家庭居住于奥鲁罗，但未披露任何家庭成员姓名；另注意区分：玻利维亚还有一位同名同姓矿业分析师/前COMIBOL执行总裁Héctor (Reynaldo) Córdova Eguivar（Fundación Jubileo研究员），二者并非同一人，亦未发现可靠来源证明两人存在亲属关系，故family_members留空",
    "social_accounts_note": "六平台扫描结果：X存在全名完全匹配的个人账号@jose_eguivar（未验证本人运营）；Facebook、Instagram、LinkedIn、TikTok、YouTube均未发现可确认的个人账号；其公开活动影像主要由COMIBOL官方账号（Facebook: comibol.oficial、X: @comibol_oficial）及矿业部账号发布",
    "position_note": "2025-12-08由矿业部长授职时的职务名称为「Presidente Ejecutivo Interino」（临时执行总裁），COMIBOL官方及ABI报道中亦使用「Presidente Ejecutivo a.i.」；截至2026年9-10月仍以interino/a.i.名义任职",
    "work_note": "1998年至2025年间的职业履历公开来源未见报道（仅1998年ANF报道证实其在哥伦比亚为德国跨国公司从事去污染工程直至同年8月获释）；contacts所列为COMIBOL官方报告公布的机构联系方式，非个人私人联系方式",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "news_search",
            "web_search",
            "social_media",
            "government_directory"
        ],
        "notes": "①任命与就任事实由Brújula Digital、La Razón、El Deber、Red Uno、eju.tv、ABI等至少6家独立媒体于2025-12-08/09报道交叉确认；就任日期以部长授职日2025-12-08为准，12月9日为向公司技术队伍正式亮相。②生平关键信息（1954-03-17生于奥鲁罗、冶金工程师、1997-1998年在哥伦比亚为德国跨国公司工作并遭FARC绑架获释）来自ANF/Fides 1998-08-03报道，全名+职业+家乡三重匹配，属单一来源、年代较早，已在birth_date_note标注置信度。③教育院校无公开来源，education留空。④同名同姓的Héctor Córdova Eguivar（前COMIBOL总裁、Fundación Jubileo研究员）为另一人，未发现亲属关系证据，未混入。⑤BNamericas公司档案快照中出现「Córdova, former deputy minister of mining」字样，因付费墙无法核实指代对象且无其他来源印证，未采纳。⑥X账号@jose_eguivar仅凭全名匹配收录，已加谨慎采信说明；LinkedIn/Instagram/TikTok/YouTube未发现个人账号。⑦org_id按_name_index.json映射：COMIBOL=BO-SOE-002；关联人物ID：卡尔德龙部长=BO-PERSON-000068、帕斯总统=BO-PERSON-000001、马尔卡副部长=BO-PERSON-000070、兰迪瓦尔副部长=BO-PERSON-000069、贝略特=BO-PERSON-000180。⑧completeness_score客观受限说明：该人物为2025年12月方就任的技术官僚型临时高管，无Wikipedia/Wikidata条目（已实测检索为空）、教育院校从未公开、家庭成员从未披露、1998-2025年职业履历无媒体报道、经六平台扫描无可确认的个人社媒账号（仅X一个全名匹配账号），education(权重8)、family(3)、profile(1)、wikidata(2)等分项在「禁止编造」铁律下无法填充，故评分客观上限约65-70；所有已填字段均有来源支撑。",
        "quotes": [
            {
                "title": "Córdova se traza el reto de modernizar y hacer más eficiente a Comibol (eju.tv, 2025-12-09)",
                "url": "https://eju.tv/2025/12/cordova-se-traza-el-reto-de-modernizar-y-hacer-mas-eficiente-a-comibol/"
            },
            {
                "title": "Ministro de Minería posesiona nuevas autoridades en busca de fortalecer el sector (Brújula Digital, 2025-12-09)",
                "url": "https://brujuladigital.net/economia/2025/12/09/ministro-de-mineria-posesiona-nuevas-autoridades-en-busca-de-fortalecer-el-sector-54769"
            },
            {
                "title": "Ingeniero secuestrado por las FARC liberado sano y salvo (ANF/Fides, 1998-08-03)",
                "url": "https://www.noticiasfides.com/nacional/sociedad/oruro-240193"
            },
            {
                "title": "COMIBOL proyecta más de Bs 6.031 millones en ingresos y 786,5 millones de dólares en divisas para 2026 (ABI, 2026-05-04)",
                "url": "https://abi.bo/comibol-proyecta-mas-de-bs-6-031-millones-en-ingresos-y-7865-millones-de-dolares-en-divisas-para-2026/"
            },
            {
                "title": "Comibol celebra 74 años de historia minera en Bolivia (La Patria, 2026-10-02)",
                "url": "https://lapatria.bo/cultura-viva/historia-y-geografia/comibol-celebra-anos-historia-minera-bolivia/"
            },
            {
                "title": "Comibol reporta movimiento económico de Bs 2.148 millones en 2025 (La Patria, 2026-04-13)",
                "url": "https://lapatria.bo/dinero-negocios/comibol-reporta-movimiento-economico-de-bs-2-148-millones-en-2025/"
            },
            {
                "title": "EQUIPO DIRECTIVO - Empresa Minera Corocoro (COMIBOL子公司官网)",
                "url": "https://www.mineracorocoro.com/institucional/estructura-organizacional/equipo-directivo.html"
            },
            {
                "title": "COMUNICADO COMIBOL: estado de procesos de comercialización Corocoro y Colquiri (COMIBOL官方公报, 2026-09-06)",
                "url": "https://www.comibol.gob.bo/images/noticias/COMUNICADO_COMIBOL_comercializaci%C3%B3nCorocoro_Colquiri_OK.pdf"
            },
            {
                "title": "Comibol niega contratos con Trafigura por cobre de Corocoro y zinc de Colquiri (La Razón, 2026-09-06)",
                "url": "https://larazon.bo/economia-y-empresa/2026/09/06/comibol-niega-contratos-con-trafigura-por-cobre-de-corocoro-y-zinc-de-colquiri/"
            },
            {
                "title": "Bolivia: Comibol y Sergeomin acuerdan impulsar la prospección y exploración geológico-minera (Mineria Pan-Americana, 2026-08-20)",
                "url": "https://mineria-pa.com/2026/08/20/bolivia-comibol-y-sergeomin-acuerdan-impulsar-la-prospeccion-y-exploracion-geologico-minera/"
            },
            {
                "title": "En Minería designan a dos viceministros y a ejecutivos de Comibol, Vinto y Sergeomin (eju.tv, 2025-12-08)",
                "url": "https://eju.tv/2025/12/en-mineria-designan-a-dos-viceministros-y-a-ejecutivos-de-comibol-vinto-y-sergeomin/"
            }
        ]
    }
}

os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(person, f, ensure_ascii=False, indent=2)

print("WROTE:", OUT_FILE)
print("bytes:", os.path.getsize(OUT_FILE))

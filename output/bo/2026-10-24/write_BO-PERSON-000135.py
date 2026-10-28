# -*- coding: utf-8 -*-
"""Write BO-PERSON-000135 person profile JSON (Gustavo Antonio Ávila Mercado)."""
import json
import os

PROFILE = {
    "person_id": "BO-PERSON-000135",
    "wikidata_qid": None,
    "name_zh": "古斯塔沃·安东尼奥·阿维拉·梅尔卡多",
    "name": "Gustavo Antonio Ávila Mercado",
    "name_en": "Gustavo Antonio Ávila Mercado",
    "aliases": ["Gustavo Ávila", "Gustavo Ávila Mercado"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": "1985-10-04",
    "birth_place": "塔里哈省 (Tarija)",
    "birth_date_note": "出生日期1985-10-04仅见于西班牙语维基百科（单一来源待核）；OEP官方简介及多家媒体仅载明其出生于塔里哈省（departamento de Tarija），未给出确切日期。",
    "birth_place_note": "出生地为玻利维亚塔里哈省，由OEP官网权威简介载明，Red Uno、Vision 360等多家媒体报道一致。",
    "contacts": [
        {
            "type": "website",
            "value": "https://web.oep.org.bo/",
            "source": "OEP官网（其任职机构多民族选举机构官方网站）"
        }
    ],
    "current_positions": [
        "最高选举法院院长",
        "最高选举法院法官（代表行政机构）"
    ],
    "education": [
        {
            "institution": "玻利维亚圣保罗天主教大学塔里哈分校 (Universidad Católica San Pablo de Tarija)",
            "degree": "bachelor",
            "field": "法学"
        },
        {
            "institution": "费利佩·帕拉松学校 (Colegio Felipe Palazón)",
            "degree": "high_school",
            "field": None
        }
    ],
    "work_experience": [
        {
            "start_date": "2004",
            "end_date": None,
            "organization": "多民族选举机构 (Órgano Electoral Plurinacional)",
            "org_id": "BO-GOV-026",
            "position": "选举宣传员、培训员与协调员"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "塔里哈省选举法院 (Tribunal Electoral Departamental de Tarija)",
            "org_id": None,
            "position": "书记处助理、顾问兼书记长"
        },
        {
            "start_date": "2011",
            "end_date": "2017",
            "organization": "塔里哈省立法议会 (Asamblea Legislativa Departamental de Tarija)",
            "org_id": None,
            "position": "秘书长"
        },
        {
            "start_date": "2017-11-13",
            "end_date": None,
            "organization": "塔里哈省选举法院 (Tribunal Electoral Departamental de Tarija)",
            "org_id": None,
            "position": "法官兼院长"
        },
        {
            "start_date": "2021-07-02",
            "end_date": "2024-04-03",
            "organization": "塔里哈省选举法院 (Tribunal Electoral Departamental de Tarija)",
            "org_id": None,
            "position": "法官"
        },
        {
            "start_date": "2024-04-03",
            "end_date": None,
            "organization": "最高选举法院 (Tribunal Supremo Electoral)",
            "org_id": "BO-GOV-026",
            "position": "法官（代表行政机构）"
        },
        {
            "start_date": "2025-12-22",
            "end_date": None,
            "organization": "最高选举法院 (Tribunal Supremo Electoral)",
            "org_id": "BO-GOV-026",
            "position": "院长"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000136",
            "person_name": "希梅娜·卡马乔·戈苏埃塔 (Ximena Camacho Goyzueta)",
            "relationship_type": "colleague",
            "description": "2025年12月21日在新一届最高选举法院首次全体会议（Sala Plena）上，卡马乔与阿维拉分别当选副院长与院长，二人共同主持新一届TSE领导层。"
        },
        {
            "person_id": "BO-PERSON-000484",
            "person_name": "路易斯·阿尔塞 (Luis Arce)",
            "relationship_type": "associate",
            "description": "2024年4月时任总统阿尔塞以第5141号最高法令任命阿维拉为最高选举法院法官（代表行政机构），接替迪娜·丘基米亚（Dina Chuquimia）。"
        },
        {
            "person_id": "BO-PERSON-000001",
            "person_name": "罗德里戈·帕斯·佩雷拉 (Rodrigo Paz Pereira)",
            "relationship_type": "superior",
            "description": "2026年2月11日总统帕斯以第5545号最高法令批准（ratificar）阿维拉继续担任最高选举法院法官（代表行政机构）。"
        },
        {
            "person_id": "BO-PERSON-000140",
            "person_name": "卡洛斯·奥尔蒂斯·克萨达 (Carlos Ortiz Quezada)",
            "relationship_type": "colleague",
            "description": "同为最高选举法院法官（2025年12月新一届Sala Plena成员），二人共同负责新选民册（Padrón Electoral）的设计与重构工作。"
        },
        {
            "person_id": None,
            "person_name": "迪娜·丘基米亚 (Dina Chuquimia)",
            "relationship_type": "associate",
            "description": "2024年4月阿维拉经第5141号最高法令接替丘基米亚出任最高选举法院法官（代表行政机构），后者亦为阿尔塞总统所任命。"
        }
    ],
    "social_accounts": [],
    "family_members": [
        {
            "person_id": None,
            "name": "费尔南多·阿维拉·庞塞 (Fernando Ávila Ponce)",
            "relationship": "father",
            "industry_or_organization": None
        },
        {
            "person_id": None,
            "name": "伊丽莎白·梅尔卡多·卢汉 (Elizabeth Mercado Luján)",
            "relationship": "mother",
            "industry_or_organization": None
        },
        {
            "person_id": None,
            "name": "米歇尔·弗洛雷斯·佩雷斯 (Michelle Flores Pérez)",
            "relationship": "spouse",
            "industry_or_organization": None
        },
        {
            "person_id": None,
            "name": "费尔南多·阿维拉·梅尔卡多 (Fernando Ávila Mercado)",
            "relationship": "brother",
            "industry_or_organization": None
        }
    ],
    "political_stances": [
        {
            "date": "2021-07-02",
            "topic": "2019年选举舞弊指控与司法案件",
            "stance_content": "重返塔里哈省选举法院就任时表示，2019年选举进程令其「痛苦」但其本人依法履职；自称曾居家羁押逾一年并出席每次听证以证明清白，并要求指控制造「所谓舞弊」者拿出证据、向司法机构主张，称指控「必须严肃且负责任」。同时反问：当年在塔里哈省获胜的是卡洛斯·梅萨，何来为某一方造假的动机。",
            "source": "Vision 360（2024-04-04，引2021年7月2日其公开表态）"
        },
        {
            "date": "2026-07-29",
            "topic": "选举合法性与民主原则",
            "stance_content": "以TSE院长身份向美洲国家组织（OEA）选举观察团重申：人民通过选举表达的自主意志是政治权力的唯一合法来源。",
            "source": "OEP Fuente Directa（fuentedirecta.oep.org.bo，2026-07-29）"
        }
    ],
    "major_achievements": [
        {
            "date": "2017-11-17",
            "achievement": "就任塔里哈省选举法院法官数日后，经全会（Sala Plena）全票当选该法院院长",
            "organization": "塔里哈省选举法院 (Tribunal Electoral Departamental de Tarija)"
        },
        {
            "date": "2024-04-03",
            "achievement": "经阿尔塞总统第5141号最高法令被任命为最高选举法院法官（代表行政机构），成为行政机构在TSE的代表",
            "organization": "最高选举法院 (Tribunal Supremo Electoral)"
        },
        {
            "date": "2025-12-21",
            "achievement": "在玻利维亚TSE换届、六名新任法官就职后，于新一届全体会议首次会议上当选最高选举法院院长",
            "organization": "最高选举法院 (Tribunal Supremo Electoral)"
        },
        {
            "date": "2026-02-11",
            "achievement": "获帕斯总统以第5545号最高法令批准留任最高选举法院法官（代表行政机构），任期为六年",
            "organization": "最高选举法院 (Tribunal Supremo Electoral)"
        },
        {
            "date": "2026-03-22",
            "achievement": "以院长身份主持全国次国家级（地区与市政）选举，选出9名省长及约5000名地方官员，并启用快速计票系统（SIREPRE）",
            "organization": "最高选举法院 (Tribunal Supremo Electoral)"
        },
        {
            "date": "2026-10-04",
            "achievement": "率美洲选举机构间联盟（UNIORE）国际观察团赴秘鲁观察地方选举，据报道系首位担此职的玻利维亚人",
            "organization": "美洲选举机构间联盟观察团 (Misión de Observación Electoral de la UNIORE)"
        }
    ],
    "biography_summary": "古斯塔沃·安东尼奥·阿维拉·梅尔卡多，玻利维亚法学家、选举管理官员，现任多民族选举机构最高选举法院（TSE）院长。出生于塔里哈省（据西语维基百科为1985年10月4日），毕业于玻利维亚圣保罗天主教大学塔里哈分校法学专业（以优异成绩毕业），持有公共管理文凭、选举法专业资格，以及宪法学与刑法学两个硕士学位（院校未公开）。自2004年起深耕选举系统逾二十年，历任选举宣传员、培训员、协调员及省选举法院书记处助理、顾问、书记长；2011至2017年任塔里哈省立法议会秘书长。2017年11月就任塔里哈省选举法院法官并全票当选院长。2019年选举危机中因选举罪指控被拘捕、居家羁押逾一年，后获撤销起诉（sobreseído），2021年7月由阿尔塞总统任命重返塔里哈省选举法院。2024年4月3日经第5141号最高法令出任最高选举法院法官（代表行政机构），接替迪娜·丘基米亚。2025年12月21日在TSE换届后的首次全体会议上当选院长，次日宣誓就职，随后主持2026年3月全国次国家级选举。2026年2月11日获帕斯总统以第5545号最高法令批准留任。同年10月率UNIORE观察团赴秘鲁观察选举，系首位担此职的玻利维亚人。其公开表态集中于选举行政与司法事项，未见可查证的党派政治立场。",
    "work_note": "据OEP官方简介，其自2004年起在选举领域任职；据Vision 360（引TED塔里哈官方资料），其在选举机构共工作约九年，先后担任宣传员、培训员、协调员、书记处助理、顾问及书记长。2024年4月3日就任TSE法官的日期以OEP官网及ANF报道为准（第5141号最高法令签署于2024年4月4日前后）。2025年12月21日经全体会议当选院长，12月22日宣誓就职（swissinfo、Opinión、La Patria报道）。法官法定任期六年。",
    "education_note": "据OEP官网及Vision 360（引TED塔里哈官方资料）：法学专业以优异成绩毕业于玻利维亚圣保罗天主教大学塔里哈分校；中学就读于塔里哈Felipe Palazón学校。另持有公共管理文凭（diplomado en Gestión Pública）、选举法专业（especialidad en derecho electoral）、宪法学硕士学位（maestría en Derecho Constitucional）；La Razón与El Diario（2025-12-21/22）另载其持有刑法学硕士学位（maestría en Derecho Penal）。上述文凭/硕士/专业的授予院校公开资料未载明，故未单列条目。",
    "family_note": "据TED塔里哈选举法院官方资料（经Vision 360转引）：其父为费尔南多·阿维拉·庞塞，母为伊丽莎白·梅尔卡多·卢汉，有三个兄弟姐妹；与妻子米歇尔·弗洛雷斯·佩雷斯育有一子（姓名未公开，故未单列条目）。另据CTV La Paz（2026年4月13日）报道，其兄弟名为费尔南多·阿维拉·梅尔卡多（Fernando Ávila Mercado）。",
    "social_accounts_note": "已按6项平台完成扫描（facebook、x/twitter、linkedin、instagram、tiktok、youtube）：未发现其个人社交媒体账号。其公开活动信息主要出现在机构账号中，包括TSE官方Facebook（facebook.com/TSEBolivia）、TSE官方Instagram（instagram.com/tse_bolivia）、Fuente Directa（fuentedirecta.oep.org.bo）及各地省选举法院（TED）账号，另有媒体对其采访内容（Radio Fides YouTube频道等）。",
    "position_note": "其TSE法官身份为「代表行政机构」（en representación del Órgano Ejecutivo）的设计/任命职位：2024年4月由阿尔塞任命（DS 5141），2026年2月11日获帕斯以DS 5545批准留任。2025年12月TSE全面换届期间曾任代理院长（presidente en ejercicio），2025年12月21日经新一届全体会议正式选举为院长，副院长为希梅娜·卡马乔。",
    "political_stances_note": "作为选举管理机构负责人须保持党派政治中立，故不收录党派立场。以下条目为其有据可查的公开声明（属选举行政与司法事项的制度性表态）：2021年就2019年案件自辩依法履职并要求指控者举证（Vision 360）；2026年7月向OEA观察团重申人民意志为政治权力唯一合法来源（OEP Fuente Directa）。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "government_directory",
            "news_search",
            "web_search",
            "wikipedia",
            "social_media"
        ],
        "notes": "生平核心事实均经至少2个独立来源交叉确认：教育背景与家庭（Vision 360引TED塔里哈官方资料 + OEP官网）；2024年任命细节（Opinión、Brújula Digital、El País BO、Correo del Sur等多家报道DS 5141并确认接替Dina Chuquimia）；院长当选（ANF/Fides、Correo del Sur、Brújula Digital、swissinfo、Opinión、El Post，2025-12-21选举、12-22宣誓）；2026年批准留任（ABI、El Deber、Opinión、参议院官方FB发布DS 5545）；双硕士（La Razón、El Diario）。存疑字段：出生日期1985-10-04仅见于西语维基百科单源，已注明待核；硕士/专业资格授予院校未查明；未发现个人社交媒体账号（6平台扫描，均仅见于TSE及媒体机构账号）。political_stances仅收录制度性公开声明，不含党派立场。中文名沿用项目既有译名（_name_index.json）。关联ID：OEP=BO-GOV-026；希梅娜·卡马乔=BO-PERSON-000136；路易斯·阿尔塞=BO-PERSON-000484；罗德里戈·帕斯=BO-PERSON-000001；卡洛斯·奥尔蒂斯=BO-PERSON-000140。Wikidata无条目（检索为空）。",
        "quotes": [
            {
                "title": "Vocales | Órgano Electoral Plurinacional（OEP官方法官名录·权威简历）",
                "url": "https://web.oep.org.bo/institucional/vocales/"
            },
            {
                "title": "Gustavo Antonio Ávila Mercado asume como vocal del Tribunal Supremo Electoral（OEP官网新闻，2024-04-04）",
                "url": "https://web.oep.org.bo/institucional-institucional/gustavo-antonio-avila-mercado-asume-como-vocal-del-tribunal-supremo-electoral/"
            },
            {
                "title": "¿Quién es Gustavo Ávila, el nuevo vocal del TSE designado por el presidente Arce?（Visión 360，2024-04-04）",
                "url": "https://www.vision360.bo/noticias/2024/04/04/2006-quien-es-gustavo-vila-el-nuevo-vocal-del-tse-designado-por-el-presidente-arce"
            },
            {
                "title": "Gustavo Ávila es el nuevo vocal del TSE por designación de Arce（Opinión，2024-04-04，DS 5141/接替Dina Chuquimia）",
                "url": "https://www.opinion.com.bo/articulo/pais/gustavo-avila-es-nuevo-vocal-tse-presidente-arce-designa/20240404120608941852.html"
            },
            {
                "title": "Arce reemplaza a Dina Chuquimia con Gustavo Ávila como vocal designado ante el TSE（Brújula Digital，2024-04-04）",
                "url": "https://brujuladigital.net/politica/2024/04/04/arce-reemplaza-a-dina-chuquimia-con-gustavo-avila-como-vocal-designado-ante-el-tse-31826"
            },
            {
                "title": "¿Quién es Gustavo Ávila Mercado, el nuevo presidente del TSE?（Red Uno，2025-12-21）",
                "url": "https://www.reduno.com.bo/noticias/quien-es-gustavo-avila-mercado-el-nuevo-presidente-del-tse--20251221145431"
            },
            {
                "title": "Sala Plena elige al vocal Gustavo Ávila como presidente del TSE（Agencia de Noticias Fides，2025-12-21）",
                "url": "https://www.noticiasfides.com/nacional/politica/sala-plena-elige-al-vocal-gustavo-avila-como-presidente-del-tse"
            },
            {
                "title": "Gustavo Ávila es elegido presidente del TSE y Ximena Camacho vicepresidenta（Correo del Sur，2025-12-21）",
                "url": "https://correodelsur.com/politica/20251221/gustavo-avila-es-elegido-presidente-del-tse-y-ximena-camacho-vicepresidenta.html"
            },
            {
                "title": "Paz ratifica a Gustavo Ávila como representante del Ejecutivo en el Tribunal Supremo Electoral（ABI，2026-02-11）",
                "url": "https://abi.bo/paz-ratifica-a-gustavo-avila-como-representante-ejecutivo-en-el-tribunal-supremo-electoral/"
            },
            {
                "title": "Gustavo Ávila es ratificado como representante del Ejecutivo en el TSE（Opinión，2026-02-11）",
                "url": "https://www.opinion.com.bo/pais/paz-ratifica-gustavo-avila-como-representante-ejecutivo-tribunal-supremo-electoral/20260211184804988499.html"
            },
            {
                "title": "Gustavo Ávila Mercado - Wikipedia, la enciclopedia libre（西语维基百科，出生日期单源）",
                "url": "https://es.wikipedia.org/wiki/Gustavo_%C3%81vila_Mercado"
            },
            {
                "title": "Presidente del TSE encabeza misión de observación en elecciones locales de Perú（Brújula Digital，2026-10-02）",
                "url": "https://brujuladigital.net/politica/2026/10/02/presidente-del-tse-encabeza-mision-de-observacion-en-elecciones-locales-de-peru-67201"
            },
            {
                "title": "Gustavo Ávila asume la presidencia del Tribunal Supremo Electoral（La Razón，2025-12-21，双硕士信息）",
                "url": "https://larazon.bo/nacional/2025/12/21/gustavo-avila-asume-la-presidencia-del-tribunal-supremo-electoral/"
            },
            {
                "title": "Gustavo Ávila asume la presidencia del TSE con el reto de fortalecer su institucionalidad（El Post，2025-12-21）",
                "url": "https://elpost.com.bo/2025/12/21/gustavo-avila-asume-la-presidencia-del-tse-con-el-reto-de-fortalecer-su-institucionalidad/"
            }
        ]
    }
}


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "BO-PERSON-000135.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(PROFILE, f, ensure_ascii=False, indent=2)
    print("WROTE:", out_path)
    # quick self check
    with open(out_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("person_id:", data["person_id"])
    print("name:", data["name"])
    print("biography_summary length:", len(data["biography_summary"]))
    print("work_experience entries:", len(data["work_experience"]))
    print("education entries:", len(data["education"]))
    print("family_members entries:", len(data["family_members"]))
    print("person_relationships entries:", len(data["person_relationships"]))
    print("major_achievements entries:", len(data["major_achievements"]))
    print("quotes:", len(data["collection_meta"]["quotes"]))


if __name__ == "__main__":
    main()

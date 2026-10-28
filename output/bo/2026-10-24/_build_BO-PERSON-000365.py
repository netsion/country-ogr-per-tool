# -*- coding: utf-8 -*-
"""Build BO-PERSON-000365 Manuel Arellano Ramirez person profile."""
import json
import os

person = {
    "person_id": "BO-PERSON-000365",
    "wikidata_qid": None,
    "name": "Manuel Arellano Ramírez",
    "name_en": "Manuel Arellano Ramirez",
    "name_zh": "曼努埃尔·阿雷利亚诺·拉米雷斯",
    "aliases": [
        "Manuel Enrique Arellano Ramírez",
        "Manuel E. Arellano Ramirez",
        "Acad. Manuel Arellano"
    ],
    "nationality": "BO",
    "gender": "male",
    "birth_date": "1945-01-28",
    "birth_place": "拉巴斯 (La Paz), 玻利维亚",
    "birth_date_note": "出生日期出自其2023年《Académicos de Número de la Academia Nacional de Ciencias - Bolivia》一书中的自述（Nací en La Paz, Bolivia, el 28 de enero de 1945），经搜索引擎索引ResearchGate书稿全文获得，目前为单一来源，待进一步核实。",
    "birth_place_note": "同上，出自其书中自述「生于玻利维亚拉巴斯」，单一来源。",
    "name_note": "官方权威名录（科学院官网）写法为 Manuel E. Arellano Ramirez；《EL DIARIO》2024-08-11 访谈与院士文集给出全名 Manuel Enrique Arellano Ramírez。",
    "name_zh_note": "中文名沿用本批次 _name_index.json 既有条目「曼努埃尔·阿雷利亚诺·拉米雷斯 (Manuel Arellano Ramírez)」。",
    "contacts": [],
    "current_positions": [
        "玻利维亚国家科学院院长"
    ],
    "education": [
        {
            "institution": "坎皮纳斯州立大学 (Universidade Estadual de Campinas)",
            "degree": "doctorate",
            "field": "物理学（固体物理/磁弹性）",
            "start_date": None,
            "end_date": "1979",
            "country": "巴西 (Brazil)",
            "description": "博士论文《Contribuição magnetoelástica às constantes elásticas do hólmio》（磁弹性对稀土金属钬弹性常数的贡献），1979年于UNICAMP完成，导师为 Daltro Garcia Pinatti；DOI: 10.47749/t/unicamp.1979.44389。",
            "source": "OpenAlex 作者档案 A5024759663 与 UNICAMP 知识库 DOI 记录；Escavador 收录的导师 Daltro Garcia Pinatti 履历条目交叉证实。"
        }
    ],
    "work_experience": [
        {
            "organization": "玻利维亚国家科学院 (Academia Nacional de Ciencias de Bolivia)",
            "org_id": "BO-ACAD-016",
            "position": "编号院士 (Académico de Número)",
            "start_date": "1993-10-20",
            "end_date": None,
            "is_current": "true",
            "location": "拉巴斯 (La Paz), 玻利维亚",
            "description": "1993年10月20日入选编号院士（Z席/Silla z），研究领域为固体物理与材料（Física del estado sólido, Materiales）；入院工作报告主题为《大学研究所与国家研究中心的经费资助》。科学院官网会员名录显示状态 Activo（在任）。",
            "source": "科学院官网「Académicos de Número Activos」名录（Ingreso 20/10/1993、Ámbito、Trabajo de ingreso）。"
        },
        {
            "organization": "玻利维亚国家科学院 (Academia Nacional de Ciencias de Bolivia)",
            "org_id": "BO-ACAD-016",
            "position": "理事会图书管理员 (Bibliotecario del Directorio)",
            "start_date": "2012",
            "end_date": "2014",
            "is_current": "false",
            "location": "拉巴斯 (La Paz), 玻利维亚",
            "description": "在2012-2014届理事会中担任图书管理员（Bibliotecario）。",
            "source": "科学院官网「Directorio desde 1960」历史名录。"
        },
        {
            "organization": "玻利维亚国家科学院 (Academia Nacional de Ciencias de Bolivia)",
            "org_id": "BO-ACAD-016",
            "position": "院长 (Presidente)",
            "start_date": "2024-06",
            "end_date": None,
            "is_current": "true",
            "location": "拉巴斯 (La Paz), 玻利维亚",
            "description": "领导2024-2027届理事会（副院长 Rónanth Zavaleta Mercado、学术秘书长 Marcos Michel López、司库 Celeste Rodríguez Quevedo）。任内主持新院士就职典礼（2025-03）、建院66周年纪念暨首届全国科学院大会（2026-09，圣克鲁斯UPSA），推动科学院就教育、卫生、能源等国家议题形成科学建议。",
            "start_date_note": "《EL DIARIO》2024-08-11 访谈称其于2024年6月就任；新理事会正式就职典礼（posesión）于2024年7月举行；科学院官网历史名录标注任期2024-2027。",
            "source": "科学院官网「Nómina de autoridades」「Directorio desde 1960」；《EL DIARIO》2024-07-21 与 2024-08-11 报道；UPSA 新闻稿。"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000366",
            "person_name": "马科斯·米歇尔·洛佩斯 (Marcos Rodolfo Michel López)",
            "relationship_type": "colleague",
            "description": "科学院学术秘书长（Secretario General），2021-2024与2024-2027两届理事会共事，为Arellano院长班子的核心成员。",
            "source": "《EL DIARIO》2024-07-21 新理事会报道；科学院官网「Directorio desde 1960」。"
        },
        {
            "person_id": "BO-PERSON-000367",
            "person_name": "卡洛斯·阿吉雷·巴斯托斯 (Carlos Aguirre Bastos)",
            "relationship_type": "colleague",
            "description": "科学院前院长（expresidente），2026年9月66周年系列活动中获颁「50年编号院士荣誉勋章」，与Arellano共同出席；亦为2023年院士文集《Académicos de Número》联合主编。",
            "source": "科学院官网新闻（2026-09）；UPSA 66周年报道。"
        },
        {
            "person_id": "BO-PERSON-000368",
            "person_name": "加斯东·梅希亚·布朗 (Gastón Mejía Brown)",
            "relationship_type": "colleague",
            "description": "国家科学院圣克鲁斯分会（ANCB-SC）主席，与Arellano共同主持2025年3月新院士就职典礼及2026年9月66周年纪念大会。",
            "source": "UPSA 新闻稿（2025-04-01、2026-09-29）。"
        },
        {
            "person_id": None,
            "person_name": "莫妮卡·莫拉莱斯·拉米雷斯 (Mónica Moraes Ramírez)",
            "relationship_type": "colleague",
            "description": "科学院前任院长（2021-2024届Presidenta、该院首位女性院长），2024年7月主持新理事会就职典礼，将院长职务交接给Arellano。",
            "source": "《EL DIARIO》2024-07-21 报道（图片说明）；科学院官网「Directorio desde 1960」2021-2024届名录。"
        },
        {
            "person_id": None,
            "person_name": "罗南斯·萨瓦莱塔·梅尔卡多 (Rónanth Zavaleta Mercado)",
            "relationship_type": "colleague",
            "description": "2024-2027届理事会副院长（Vicepresidente），Arellano的副手。",
            "source": "《EL DIARIO》2024-07-21 报道；科学院官网「Nómina de autoridades」。"
        }
    ],
    "social_accounts": [],
    "social_accounts_note": "对 LinkedIn、Facebook、X(Twitter)、Instagram、TikTok、YouTube 六个平台进行检索扫描，未发现可确认归属本人的社交媒体账号（同名结果均为其他人员，如西班牙经济学家 Manuel Arellano、墨西哥人士等，已排除）。科学院机构账号为 facebook.com/academiadeciencias.bolivia 与 x.com/ANC_Bolivia，属机构而非本人。",
    "family_members": [],
    "family_note": "公开资料中未检索到其家庭成员信息。",
    "political_stances": [],
    "political_stances_note": "无公开党派政治立场记录。其公开发言限于科学与机构事务，强调科学院作为独立科学共同体「基于科学事实和数据」就水、能源、社会议题向各级政府提供可选用的科学意见（EL DIARIO 访谈，2024-08-11）。",
    "major_achievements": [
        {
            "date": "1979",
            "achievement": "获巴西坎皮纳斯州立大学（UNICAMP）物理学博士学位，博士论文《磁弹性对钬弹性常数的贡献》（导师 Daltro Garcia Pinatti）。",
            "organization": "坎皮纳斯州立大学 (Universidade Estadual de Campinas)"
        },
        {
            "date": "1993-10-20",
            "achievement": "入选玻利维亚国家科学院编号院士（Académico de Número，Z席），研究领域为固体物理与材料，入院报告主题为大学研究所与国家研究中心的经费资助。",
            "organization": "玻利维亚国家科学院 (Academia Nacional de Ciencias de Bolivia)"
        },
        {
            "date": "2024",
            "achievement": "当选玻利维亚国家科学院院长（2024-2027届），领导全国最高科学荣誉机构的理事会，7月举行正式就职典礼。",
            "organization": "玻利维亚国家科学院 (Academia Nacional de Ciencias de Bolivia)"
        },
        {
            "date": "2026-09",
            "achievement": "主持建院66周年纪念大会暨首届全国科学院全国大会（圣克鲁斯UPSA），提出加强新一代科研人员参与、改进科学传播，并围绕教育、卫生、经济、能源等议题组织形成提交国家当局的文件与建议。",
            "organization": "玻利维亚国家科学院 (Academia Nacional de Ciencias de Bolivia)"
        }
    ],
    "biography_summary": "曼努埃尔·恩里克·阿雷利亚诺·拉米雷斯（Manuel Enrique Arellano Ramírez）是玻利维亚固体物理与材料领域资深科学家，现任玻利维亚国家科学院（ANCB）院长（2024-2027届）。据其自述1945年1月28日生于拉巴斯，1979年在巴西坎皮纳斯州立大学（UNICAMP）获物理学博士学位，博士论文研究磁弹性对稀土金属钬弹性常数的贡献。1993年10月20日入选国家科学院编号院士（Académico de Número，Z席），入院报告主题为大学研究所与国家研究中心的经费资助。2012-2014年任科学院理事会图书管理员；2024年6月就任院长、7月正式就职，接替首任女性院长莫妮卡·莫拉莱斯。任内主持2025年3月圣克鲁斯新院士就职典礼、2026年9月建院66周年纪念暨首届全国科学院大会，主张加强新一代科研人员参与、改进科学传播，推动科学院就教育、卫生、能源等国家议题形成基于科学事实的建议，供各级政府采用。其公开表态强调科学院作为独立科学共同体，以科学数据和事实为基础就水、能源与社会议题发表意见。",
    "profile": {
        "source_url": "https://aciencias.gob.bo/wp-content/uploads/2026/03/manuelarellanoA-1.jpg",
        "local_path": "persons/photos/BO-PERSON-000365.jpg"
    },
    "work_note": "科学院官网会员名录其条目另标注「Lugar: Exterior」，与其实际在拉巴斯主持院务的公开活动不符，疑为网站数据录入问题，未采信。",
    "identity_note": "姓名消歧：本档案主体为玻利维亚国家科学院院长 Manuel (Enrique) Arellano Ramírez，非哥伦比亚 electrónica 学者 Iván Darío Arellano-Ramírez（Universidad Tecnológica de Pereira）、非西班牙计量经济学家 Manuel Arellano (CEMFI)、非墨西哥政界人士 Manuel Arellano Méndez。依据：科学院官网权威名录（固体物理领域、编号院士）、EL DIARIO 访谈（全名+院长职务）、UNICAMP 博士论文记录（姓名与领域吻合）相互印证。",
    "collection_meta": {
        "collection_date": "2026-10-27",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "news_search",
            "web_search",
            "social_media",
            "other"
        ],
        "completeness_score": 58,
        "notes": "数据来源确认情况：院长职务、理事会构成、任期2024-2027、1993年入院士与2012-2014图书管理员职务均由科学院官网（nomina-de-autoridades、academico-activo、directorio-desde-1960）与《EL DIARIO》两篇报道（2024-07-21、2024-08-11，经Wayback Machine存档全文）双源确认；UNICAMP物理学博士（1979）由OpenAlex/UNICAMP DOI记录与Escavador导师履历两个独立来源确认；2025-2026年院务活动由UPSA两篇新闻稿与科学院官网新闻双源确认。关键发现：其全名中间名Enrique经访谈与院士文集确认；出生日期1945-01-28仅见其书中自述（单源，已在birth_date_note标注）；无个人社交媒体账号；家庭成员与个人联系方式无公开资料；无党派政治立场记录。completeness_score=58（低于85），原因：科学家公开信息有限——社交媒体、家庭、个人联系方式、本科学历均无公开可靠来源，为客观信息缺口而非检索不足。",
        "quotes": [
            {
                "title": "Academia de Ciencias continúa impulsando investigación en el país - EL DIARIO (2024-08-11)",
                "url": "https://www.eldiario.net/portal/2024/08/11/academia-de-ciencias-continua-impulsando-investigacion-en-el-pais/"
            },
            {
                "title": "ANC tiene nuevo directorio - EL DIARIO (2024-07-21)",
                "url": "https://www.eldiario.net/portal/2024/07/21/anc-tiene-nuevo-directorio/"
            },
            {
                "title": "Nómina de autoridades - Academia Nacional de Ciencias (aciencias.gob.bo)",
                "url": "https://aciencias.gob.bo/index.php/nomina-de-autoridades/"
            },
            {
                "title": "Académicos de Número Activos - Academia Nacional de Ciencias (aciencias.gob.bo)",
                "url": "https://aciencias.gob.bo/index.php/membresia/academico-activo/"
            },
            {
                "title": "Directorio desde 1960 - Academia Nacional de Ciencias (aciencias.gob.bo)",
                "url": "https://aciencias.gob.bo/index.php/directorio-desde-1960/"
            },
            {
                "title": "Nuevo ingreso a la Academia Nacional de Ciencias de Bolivia - UPSA (2025-04-01)",
                "url": "https://congresopatrimonio.upsa.edu.bo/en/noticias-upsa/2491-nuevo-ingreso-a-la-academia-nacional-de-ciencias-de-bolivia"
            },
            {
                "title": "Academia Nacional de Ciencias de Bolivia conmemora su 66 aniversario con una Sesión de Honor en la UPSA - UPSA (2026-09-29)",
                "url": "https://www.upsa.edu.bo/academia-nacional-de-ciencias-de-bolivia-conmemora-su-66-aniversario-con-una-sesion-de-honor-en-la-upsa/"
            },
            {
                "title": "Primera Conferencia Nacional de la Academia Nacional de Ciencias de Bolivia - ANC nota de prensa (2026-09-24)",
                "url": "https://aciencias.gob.bo/index.php/nota_prensa/primera-conferencia-nacional-de-la-academia-nacional-de-ciencias-de-bolivia/"
            },
            {
                "title": "ACADÉMICOS DE NÚMERO DE LA ACADEMIA NACIONAL DE CIENCIAS - BOLIVIA, Primera edición (Moraes & Aguirre eds., 2023) - ResearchGate",
                "url": "https://www.researchgate.net/publication/377443566_ACADEMICOS_DE_NUMERO_DE_LA_ACADEMIA_NACIONAL_DE_CIENCIAS_-BOLIVIA_Primera_edicion"
            },
            {
                "title": "Contribuição magnetoelástica às constantes elásticas do hólmio (1979, UNICAMP) - OpenAlex",
                "url": "https://doi.org/10.47749/t/unicamp.1979.44389"
            },
            {
                "title": "Daltro Garcia Pinatti - Escavador (cita a tese de doutorado de M.E. Arellano Ramirez, UNICAMP 1979)",
                "url": "https://www.escavador.com/sobre/958675/daltro-garcia-pinatti"
            }
        ]
    }
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000365.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(person, f, ensure_ascii=False, indent=2)
print("written", out)

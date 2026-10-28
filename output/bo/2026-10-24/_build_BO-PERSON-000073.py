# -*- coding: utf-8 -*-
"""Build person profile JSON for BO-PERSON-000073 (Zenón Pedro Mamani Ticona)."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000073.json")

profile = {
    "person_id": "BO-PERSON-000073",
    "wikidata_qid": None,
    "name": "Zenón Pedro Mamani Ticona",
    "name_en": "Zenón Pedro Mamani Ticona",
    "name_zh": "塞农·佩德罗·马马尼·蒂科纳",
    "aliases": ["Zenón Mamani", "Zenón Mamani Ticona"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "birth_date_note": "公开报道未披露出生日期与出生地；2025年2月就任部长时媒体亦未提及年龄。",
    "profile": {
        "source_url": "https://lapatria.bo/wp-content/uploads/2026/02/264055.jpg",
        "local_path": "photos/BO-PERSON-000073.jpg"
    },
    "contacts": [],
    "current_positions": [],
    "education": [
        {
            "institution": "圣安德烈斯大学 (Universidad Mayor de San Andrés)",
            "degree": "bachelor",
            "field": "经济学",
            "start_date": None,
            "end_date": None
        }
    ],
    "education_note": "据 La Patria 与 Red Uno 报道：经济学士（UMSA），公共预算与企业和机构战略规划专家，并修有「基于成果的公共预算」文凭课程（院校未披露）。",
    "work_experience": [
        {
            "start_date": "2025-02-12",
            "end_date": "2025-11-08",
            "organization": "生产发展与多元经济部 (Ministerio de Desarrollo Productivo y Economía Plural)",
            "org_id": "BO-GOV-012",
            "position": "部长"
        },
        {
            "start_date": "2025-03-26",
            "end_date": None,
            "organization": "发展规划部 (Ministerio de Planificación del Desarrollo)",
            "org_id": "BO-GOV-017",
            "position": "临时部长（兼任）"
        },
        {
            "start_date": "2020-11-12",
            "end_date": "2025-02-12",
            "organization": "经济与公共财政部 (Ministerio de Economía y Finanzas Públicas)",
            "org_id": "BO-GOV-005",
            "position": "预算与财政会计副部长"
        },
        {
            "start_date": "2006",
            "end_date": None,
            "organization": "经济与公共财政部 (Ministerio de Economía y Finanzas Públicas)",
            "org_id": "BO-GOV-005",
            "position": "公共职业阶梯（实习生、预算分析师、单位主管、司长）"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "国家石油公司 (Yacimientos Petrolíferos Fiscales Bolivianos, YPFB)",
            "org_id": "BO-SOE-001",
            "position": "董事会成员"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "矿业融资基金 (Fondo de Financiamiento para la Minería, Fofim)",
            "org_id": None,
            "position": "董事会成员"
        }
    ],
    "position_note": "2025年2月12日获总统阿尔塞授职为生产发展与多元经济部长，接替因病去职的内斯托尔·万卡·丘拉；2025年11月8日随阿尔塞政府结束卸任，次日帕斯政府任命奥斯卡·马里奥·胡斯蒂尼亚诺为该部临时部长。2025年3月26日依第5355号最高法令在发展规划部长缺席期间临时兼任该职。",
    "work_note": "据其就任演说（La Patria）、Vision360 与 Red Uno 报道：2006年以实习生身份进入经济与公共财政部（时任部长为阿尔塞），历任预算分析师、省与发展基金单位、多年预算管理与公营企业单位等单位主管及司长，其间兼任国家石油公司（YPFB）与矿业融资基金（Fofim）董事会成员；一度离开公职，2020年由经济部长蒙特内格罗邀其出任预算与财政会计副部长。阿尔塞称自其大学时代即认识他（或为其大学讲师）。",
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000484",
            "person_name": "路易斯·阿尔塞 (Luis Arce)",
            "relationship_type": "superior",
            "description": "阿尔塞自其大学时代相识，称其为可信赖的资深公务员；2006年阿尔塞任经济部长时马马尼以实习生进入该部，2025年2月12日由阿尔塞授职为生产发展与多元经济部长。"
        },
        {
            "person_id": "BO-PERSON-000074",
            "person_name": "内斯托尔·万卡·丘拉 (Néstor Huanca Chura)",
            "relationship_type": "colleague",
            "description": "马马尼的部长职位前任（2025年2月因健康原因卸任），两人同属阿尔塞内阁；2026年1月15日同日因Emapa补贴面粉案被拘留，为同案被告。"
        },
        {
            "person_id": None,
            "person_name": "马塞洛·蒙特内格罗 (Marcelo Montenegro)",
            "relationship_type": "superior",
            "description": "经济与公共财政部长；2020年11月12日授职马马尼为预算与财政会计副部长，马马尼在就任部长时称其为「老师、兄弟」。"
        },
        {
            "person_id": None,
            "person_name": "富兰克林·弗洛雷斯 (Franklin Flores)",
            "relationship_type": "associate",
            "description": "国家食品生产支持公司（Emapa）总经理，属马马尼主管的生产部门国营企业负责人之一；2025年3月27日主持马马尼召集的面包行业对话，后成为Emapa补贴面粉案主要涉案人并处于预防性羁押中。"
        },
        {
            "person_id": "BO-PERSON-000072",
            "person_name": "奥斯卡·马里奥·胡斯蒂尼亚诺·平托 (Óscar Mario Justiniano Pinto)",
            "relationship_type": "other",
            "description": "职务接任者：2025年11月9日帕斯政府任命胡斯蒂尼亚诺为生产发展与多元经济部临时部长，接替马马尼卸任后的该部职务。"
        }
    ],
    "social_accounts": [],
    "social_accounts_note": "六平台扫描（facebook / twitter_x / linkedin / instagram / tiktok / youtube）未发现可核验的本人账号：Facebook存在同名个人主页（zenon.mamaniticona.3）但无法确认归属；LinkedIn有30余名同名用户；其余平台均为媒体机构账号发布与其相关的报道。",
    "family_members": [],
    "family_note": "公开报道未披露配偶、子女等家庭成员信息。",
    "political_stances": [
        {
            "date": "2025-02-12",
            "topic": "工业化与进口替代",
            "stance_content": "就任生产发展与多元经济部长时承诺延续「进口替代工业化」路线：推进170个规划工业项目中的至少53个建设（总投资超320亿玻利维亚诺），兼顾旅游业与微型和小型企业发展，以实现市场多元化与粮食安全。",
            "source": "https://abi.bo/index.php/component/content/article/36-notas/noticias/economia/60510-zenon-mamani-es-posesionado-como-nuevo-ministro-de-desarrollo-productivo-y-economia-plural?Itemid=101"
        },
        {
            "date": "2025-03-27",
            "topic": "补贴面粉与面包价格（粮食安全）",
            "stance_content": "通报国家食品生产支持公司（Emapa）补贴面粉已惠及约1,995名面包师，用于维持每单位面包0.50玻利维亚诺的价格；指出部分面包师存在证照伪造或不符合卫生条件问题，并邀请行业对话以化解拟议的48小时罢工。",
            "source": "https://historico.abi.bo/index.php/economia2/62162-harina-subvencionada-beneficia-a-cerca-de-2-000-panificadores-gobierno-invita-a-dialogar-y-evitar-paro"
        },
        {
            "date": "2025-06-05",
            "topic": "畜牧业出口政策（牛肉出口）",
            "stance_content": "与农牧业部门达成协议后解释：在确认国内市场供应充足、牧业界承诺增加供给并接受交叉管控的前提下，以「受控且协调」的方式恢复2025年2月5日起暂停的牛肉出口，预计可创造约1亿美元收入。",
            "source": "https://www.opinion.com.bo/pais/gobierno-rehabilita-exportacion-carne-acuerdo-productores/20250605000024973817.html"
        },
        {
            "date": "2024-01-24",
            "topic": "社会道路封锁对经济的影响",
            "stance_content": "作为预算与财政会计副部长表示，每个封锁日给国家造成的损失超过1.28亿美元，称封锁措施「毫无意义与理由」、损害国家经济发展。",
            "source": "https://www.hoybolivia.com/Noticia.php?IdNoticia=360124"
        }
    ],
    "major_achievements": [
        {
            "date": "2025-02-12",
            "achievement": "获任命为生产发展与多元经济部长（阿尔塞政府末任），负责推进含170个规划工业项目中至少53个、总投资逾320亿玻利维亚诺的进口替代工业化计划。",
            "organization": "生产发展与多元经济部 (Ministerio de Desarrollo Productivo y Economía Plural)"
        },
        {
            "date": "2020-11-12",
            "achievement": "出任经济与公共财政部预算与财政会计副部长，主管公共预算与财政会计事务逾四年，直至2025年2月转任部长。",
            "organization": "经济与公共财政部 (Ministerio de Economía y Finanzas Públicas)"
        },
        {
            "date": "2025-06-05",
            "achievement": "在确认国内供应充足的前提下，与农牧业界达成五点协议，推动以受控、协调方式恢复牛肉出口，预计创造约1亿美元出口收入。",
            "organization": "生产发展与多元经济部 (Ministerio de Desarrollo Productivo y Economía Plural)"
        },
        {
            "date": "2025-03-26",
            "achievement": "依第5355号最高法令，在发展规划部长缺席期间被指定临时兼任发展规划部长。",
            "organization": "发展规划部 (Ministerio de Planificación del Desarrollo)"
        }
    ],
    "biography_summary": "塞农·佩德罗·马马尼·蒂科纳，玻利维亚经济学家、技术官僚型官员，阿尔塞政府末任生产发展与多元经济部长。圣安德烈斯大学（UMSA）经济学学士，专长公共预算及企业与机构战略规划，并修有「基于成果的公共预算」文凭课程。2006年以实习生身份进入经济与公共财政部（时值阿尔塞执掌该部），由技术员、单位主管至司长逐级晋升；一度离开公职后，于2020年11月12日回归出任预算与财政会计副部长，任职逾四年，被视为阿尔塞信任的经济团队资深成员。2025年2月12日获阿尔塞授职，接替因病去职的内斯托尔·万卡·丘拉出任生产发展与多元经济部长，肩负延续进口替代工业化（170个工业项目中先建53个，投资超320亿玻利维亚诺）、保障粮食安全与维持补贴面包价格的使命；任内曾依第5355号法令临时兼任发展规划部长（2025年3月26日），并主导以受控方式恢复牛肉出口（预计创汇约1亿美元）。2025年11月8日随阿尔塞政府结束而卸任。2026年1月因国家食品生产支持公司（Emapa）「补贴面粉案」被拘留，1月18日获居家拘留等替代措施；检方指有害合同主要订立于其前任任内、而其在任期间对相关报告与审计「不作为」，马马尼被押解时公开表示自己无罪；同年6月3日在第二起刑事程序中因涉嫌渎职与反经济行为（涉国家损失约340万玻利维亚诺）被判处六个月预防性羁押。",
    "collection_meta": {
        "phase": "phase4_person_profile",
        "collection_date": "2026-10-25",
        "data_sources": [
            "news_search",
            "web_search",
            "wikipedia",
            "social_media",
            "government_registry"
        ],
        "quotes": [
            {
                "title": "¿Cuál es el perfil profesional de Zenón Mamani, el nuevo ministro de Desarrollo Productivo y Economía Plural? (Red Uno, 2025-02-12)",
                "url": "https://www.reduno.com.bo/nacional/cual-es-el-perfil-profesional-de-zenon-mamani-el-nuevo-ministro-de-desarrollo-productivo-y-economia-plural--2025212901"
            },
            {
                "title": "El Presidente Arce destaca trayectoria de Zenón Mamani tras posesionarlo como ministro (La Patria, 2025-02-12)",
                "url": "https://lapatria.bo/enfoque-nacional/el-presidente-arce-destaca-trayectoria-de-zenon-mamani-tras-posesionarlo-como-ministro/"
            },
            {
                "title": "Zenón Mamani es posesionado como Ministro de Desarrollo Productivo con la misión de continuar el proceso de industrialización (ABI, 2025-02-12)",
                "url": "https://abi.bo/index.php/component/content/article/36-notas/noticias/economia/60510-zenon-mamani-es-posesionado-como-nuevo-ministro-de-desarrollo-productivo-y-economia-plural?Itemid=101"
            },
            {
                "title": "Zenón Mamani Ticona asume como nuevo Ministro de Desarrollo Productivo y Economía Plural en Bolivia (Calle Bolivia, 2025-02-12)",
                "url": "https://callebolivia.com/2025/02/12/zenon-mamani-ticona-asume-como-nuevo-ministro-de-desarrollo-productivo-y-economia-plural-en-bolivia/"
            },
            {
                "title": "Cabinet of Luis Arce (Wikipedia, en)",
                "url": "https://en.wikipedia.org/wiki/Cabinet_of_Luis_Arce"
            },
            {
                "title": "Dictan detención preventiva para Néstor Huanca y domiciliaria para Zenón Mamani por caso harina subvencionada (ANF / Noticias Fides, 2026-01-18)",
                "url": "https://www.noticiasfides.com/nacional/seguridad/dictan-detencion-preventiva-para-nestor-huanca-y-domiciliaria-para-zenon-mamani-por-caso-harina-subvencionada"
            },
            {
                "title": "Encarcelan a exministro Zenón Mamani por corrupción en Emapa (La Patria, 2026-06)",
                "url": "https://lapatria.bo/actualidad/encarcelan-a-exministro-zenon-mamani-por-corrupcion-en-emapa/"
            },
            {
                "title": "Exministro Zenón Mamani es enviado a la cárcel con detención preventiva por seis meses (Eju.tv, 2026-06)",
                "url": "https://eju.tv/2026/06/exministro-zenon-mamani-es-enviado-a-la-carcel-con-detencion-preventiva-por-seis-meses/"
            },
            {
                "title": "Harina subvencionada beneficia a cerca de 2.000 panificadores, Gobierno invita a dialogar y evitar paro (ABI, 2025-03-27)",
                "url": "https://historico.abi.bo/index.php/economia2/62162-harina-subvencionada-beneficia-a-cerca-de-2-000-panificadores-gobierno-invita-a-dialogar-y-evitar-paro"
            },
            {
                "title": "Gobierno rehabilita la exportación de carne tras acuerdo con productores (Opinion/ERBOL, 2025-06-05)",
                "url": "https://www.opinion.com.bo/pais/gobierno-rehabilita-exportacion-carne-acuerdo-productores/20250605000024973817.html"
            },
            {
                "title": "Aprehenden a dos exministros de Arce por caso de harina subvencionada de Emapa (El Post, 2026-01-15)",
                "url": "https://elpost.com.bo/2026/01/15/aprehenden-a-dos-exministros-de-arce-por-caso-de-harina-subvencionada-de-emapa/"
            },
            {
                "title": "Empresarios: Bloqueos afectan gravemente a la economía nacional (Hoy Bolivia, 2024-01-24)",
                "url": "https://www.hoybolivia.com/Noticia.php?IdNoticia=360124"
            },
            {
                "title": "Conozca a Zenón Mamani, que escaló de pasante a ministro de Desarrollo Productivo (Vision360, 2025-02-12)",
                "url": "https://www.vision360.bo/noticias/2025/02/12/19979-conozca-a-zenon-mamani-que-escalo-de-pasante-a-ministro-de-desarrollo-productivo"
            },
            {
                "title": "Decreto Presidencial N° 5355 (26-03-2025) — Pixi Legal",
                "url": "https://www.pixilegal.com/normativa/decreto-5355-2025-03-26"
            },
            {
                "title": "Paz posesiona a su gabinete de 15 ministros y sorprende con la designación del empresario cruceño Óscar Mario Justiniano (EL DÍA, 2025-11-09)",
                "url": "https://eldia.com.bo/2025-11-09/economia/paz-posesiona-a-su-gabinete-de-15-ministros-y-sorprende-con-la-designacion-del-empresario-cruceno-oscar-mario-justiniano.html"
            },
            {
                "title": "Zenón Pedro Mamani Ticona es el nuevo Ministro de Desarrollo Productivo y Economía Plural en sustitución de Néstor Huanca (MDPyEP, produccion.gob.bo, 2025-02-12)",
                "url": "https://produccion.gob.bo/nota_prensa/zenon-pedro-mamani-ticona-es-el-nuevo-ministro-de-desarrollo-productivo-y-economia-plural-en-sustitucion-de-nestor-huanca/"
            }
        ],
        "notes": "关键事实核验情况：①就任（2025-02-12，接替因病去职的Néstor Huanca Chura）与此前任预算与财政会计副部长（2020-11-12授职）有ABI、La Patria、Red Uno、Calle Bolivia、Unitel、El Diario及英文Wikipedia阿尔塞内阁页等多源印证；②卸任日期2025-11-08依据阿尔塞内阁当日结束、帕斯政府2025-11-09任命Óscar Mario Justiniano为该部临时部长（EL DÍA、Wikipedia、El Post「2025年2月至11月在任」）；③2026年1月Emapa补贴面粉案拘留与1月18日居家拘留措施（ANF、El Post、Opinión、Unitel等），2026年6月3日第二起案件预防性羁押六个月（La Patria、Eju.tv）——此为司法指控、非定罪；检方称有害合同主要订立于其前任任内、马马尼任内呈「不作为」，本人公开否认（El Post）；④教育背景（UMSA经济学士、公共预算与企业战略规划专家、基于成果的公共预算文凭课程）出自La Patria与Red Uno；⑤出生日期/出生地、家庭成员经多轮检索未见于公开报道，置空（未编造）；⑥Wikidata无本人条目（两次检索确认，wikidata_qid=null）；⑦社交媒体六平台扫描无本人可核验账号（详见social_accounts_note）；⑧name_zh沿用项目索引既有译名，另见中国商务部《对外投资合作国别（地区）指南·玻利维亚（2025年版）》「塞农·佩德罗·马马尼」；⑨发展规划部临时兼职据第5355号最高法令（Pixi Legal数据库）；⑩照片为La Patria就任报道题图（已目检为国旗背景发布会场景）；⑪completeness_score受限说明：评分器空缺项（出生日期/地、Wikidata、社交账号、家庭成员、联系方式）对该层级技术官僚均无公开可查信息，为遵守「禁止编造」铁律不予填占，属客观上限而非收集缺失。"
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("written:", OUT)
print("bytes:", os.path.getsize(OUT))

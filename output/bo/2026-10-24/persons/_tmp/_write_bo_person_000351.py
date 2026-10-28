# -*- coding: utf-8 -*-
"""Build BO-PERSON-000351.json — Eva Foronda Franco, Decana Académica, Unifranz La Paz."""
import json
import os

OUT = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000351.json"

profile = {
    "person_id": "BO-PERSON-000351",
    "wikidata_qid": None,
    "name": "Eva Foronda Franco",
    "name_en": "Eva Foronda Franco",
    "name_zh": None,
    "aliases": ["Eva Foronda"],
    "nationality": "BO",
    "gender": "female",
    "birth_date": None,
    "birth_place": None,
    "contacts": [
        {
            "type": "website",
            "value": "https://unifranz.edu.bo",
            "source": "所在机构弗朗茨·塔马约私立大学（Unifranz）官方网站",
        }
    ],
    "current_positions": [
        "弗朗茨·塔马约私立大学（Unifranz）拉巴斯校区学术院长"
    ],
    "education": [],
    "work_experience": [
        {
            "organization": "弗朗茨·塔马约私立大学 (Universidad Privada Franz Tamayo)",
            "org_id": "BO-ACAD-012",
            "position": "拉巴斯校区学术院长",
            "start_date": None,
            "end_date": None,
            "description": "至迟于2023年1月已以「Decana Académica de UNIFRANZ La Paz」头衔活动（2023-01-26发布的TecMilenio师资培训报道即用此头衔）；2019年6月拉巴斯学术院长一职仍由Roberto Oblitas Zamora担任，据此其转任时间应在2019年年中至2023年年初之间，具体任命日期未见公开披露，截至2026年9月仍在任（Red Uno报道）。任内为Unifranz「aprender haciendo（在学习中做）」体验式教育模型的主要学术代言人：2026年4月经ANF/Fides通讯社阐释以学生为中心、以整合项目与真实案例取代机械记忆的教学与评价改革，2026年9月经Red Uno阐释面向2030届毕业生的能力培养。2025年1月率拉巴斯校区学术代表团赴西班牙蒙德拉贡大学（Universidad de Mondragón）交流15天，深化校企一体化的「学习—实践」合作；2025年11月以「文化城市」学术支柱负责人身份参与Futures Week 2025拉巴斯活动（与千年项目、RIBER等合作）；2025年12月代表大学阐释进入QS Stars国际评级的意义（高就业率、社会影响与治理）；并参与推动与哥伦比亚UDI等高校的双学位项目及国际教育奖项、TecMilenio「Docentes 360」师资培训等项目。",
            "source": "Unifranz官网博客多篇（TecMilenio文2023-01-26；蒙德拉贡代表团文2025-01-14；Futures Week文2025-11-06；QS评级文2025-12-17；双学位文2025-12-31；International Educators Awards文2024-03）；ANF/Noticias Fides（2026-04-08）；Red Uno（2026-09-10）；Unifranz官网学术主管名录页（未列各校区院长，职务以官网博客与媒体报道为准）",
        },
        {
            "organization": "弗朗茨·塔马约私立大学 (Universidad Privada Franz Tamayo)",
            "org_id": "BO-ACAD-012",
            "position": "商业工程学专业主任",
            "start_date": None,
            "end_date": None,
            "description": "2017年9月已以「jefe de carrera（专业负责人）」身份率40名商业工程学学生赴玻利维亚装瓶企业EMBOL S.A.参访（Unifranz官网2017-09-29发布，署名Ing. Eva Foronda Franco）；2019年6月25日以「Directora de la Carrera de Ingeniería Comercial」身份获玻利维亚众议院教育与卫生委员会表彰，列入拉巴斯校区36名杰出教师名单（时任全国校长Verónica Ágreda、拉巴斯学术院长Roberto Oblitas同列）。其后至迟于2023年年初转任拉巴斯校区学术院长，卸任该主任职务的确切日期未见披露。",
            "source": "Unifranz官网《Vista a la Planta EMBOL S.A.》（2017-09-29）；Unifranz官网《Docentes Unifranz fueron reconocidos por la Comisión de Educación y Salud de la Cámara de Diputados》（2019-06-25）",
        },
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000348",
            "person_name": "韦罗妮卡·阿格雷达·德帕索斯 (Verónica Ágreda de Pazos)",
            "relationship_type": "superior",
            "description": "Unifranz全国校长，为其所在大学的最高学术负责人；二人早在2019年6月众议院表彰名单中即同列（当时Verónica已任全国校长、Eva任商业工程学专业主任），Eva任拉巴斯校区学术院长期间仍在其领导的全国治理架构内工作。",
            "source": "Unifranz官网学术主管名录页；《Docentes Unifranz fueron reconocidos...》（2019-06-25）",
        },
        {
            "person_id": "BO-PERSON-000349",
            "person_name": "奥斯卡·阿格雷达 (Óscar Ágreda)",
            "relationship_type": "superior",
            "description": "Unifranz总裁执行官（Presidente Ejecutivo），大学最高执行负责人；Eva作为校区学术院长在其领导的大学治理体系内任职。",
            "source": "Unifranz官网学术主管名录页",
        },
        {
            "person_id": "BO-PERSON-000350",
            "person_name": "埃里克·蒙塔尼奥 (Erick Gustavo Montaño)",
            "relationship_type": "superior",
            "description": "Unifranz全国学术副校长（Vicerrector Académico Nacional），全国学术条线负责人；Eva所任拉巴斯校区学术院长同属该学术管理条线，二人多次共同出现在大学学术活动报道中。",
            "source": "Unifranz官网学术主管名录页；Unifranz官网博客学术活动报道",
        },
        {
            "person_id": None,
            "person_name": "佩德罗·萨恩斯·穆尼奥斯 (Pedro Sáenz Muñoz)",
            "relationship_type": "superior",
            "description": "Unifranz拉巴斯校区副校长（Vicerrector Sede La Paz），为Eva所在校区的直接校领导；2019年6月众议院表彰活动中即以该职身份出席。",
            "source": "Unifranz官网学术主管名录页；《Docentes Unifranz fueron reconocidos...》（2019-06-25）",
        },
    ],
    "social_accounts": [],
    "family_members": [],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2019-06-25",
            "achievement": "以商业工程学专业主任身份获玻利维亚众议院教育与卫生委员会授予的杰出教师表彰文凭，列入拉巴斯校区36名获奖教师名单（由众议员Gabriel Miranda Valdez颁发）。",
            "organization": "玻利维亚众议院教育与卫生委员会 (Comisión de Educación y Salud de la Cámara de Diputados)",
        },
        {
            "date": "2024-03",
            "achievement": "在其学术院长任内，拉巴斯校区举办首届Unifranz国际教育者奖（International Educators Awards）颁奖夜，表彰17名在国际化教学中作出贡献的教师；拉巴斯校区成为全国四个校区中唯一囊括全部四个奖项类别（含COIL国际协作课堂「Distinguished Global Educator」奖）的校区，其本人以学术院长身份总结国际化项目成果。",
            "organization": "弗朗茨·塔马约私立大学 (Universidad Privada Franz Tamayo)",
        },
        {
            "date": "2025-01",
            "achievement": "率拉巴斯校区学术代表团（含医学主任Griselda Vargas等）赴西班牙蒙德拉贡大学开展为期15天的交流访问，考察其课堂设计与大学—企业一体化培养模式，推进双方合作项目落地（系2024年10月蒙德拉贡教师回访玻利维亚四校区的回访行程）。",
            "organization": "弗朗茨·塔马约私立大学 (Universidad Privada Franz Tamayo)",
        },
    ],
    "biography_summary": "埃娃·福龙达·佛朗哥（Eva Foronda Franco）是玻利维亚弗朗茨·塔马约私立大学（Unifranz）拉巴斯校区学术院长（Decana Académica），工程师（Ing.）出身，长期在Unifranz拉巴斯校区任职。2017年9月她已以商业工程学专业负责人身份带领学生赴EMBOL装瓶厂开展实践参访，2019年6月以商业工程学专业主任身份获玻利维亚众议院教育与卫生委员会杰出教师表彰；2019年年中至2023年年初之间转任拉巴斯校区学术院长并任职至今。任内她是Unifranz「在学习中做」（aprender haciendo）体验式教育模型的主要学术代言人，多次通过ANF/Fides通讯社、Red Uno等媒体阐释以学生为中心、以整合项目与真实案例取代机械记忆的教学与评价改革，主张教育应培养批判性思维与可迁移能力以对接劳动力市场。2025年1月她率学术代表团赴西班牙蒙德拉贡大学交流，推动大学—企业一体化培养经验的本土化；同年11月参与Futures Week 2025拉巴斯活动并主导「文化城市」议题，倡导以教育奠定城市与民主文化的根基；2025年12月代表大学阐释进入QS Stars国际评级的意义，并支持与哥伦比亚UDI等高校的双学位国际化项目。作为家族企业型大学中的校区级学术主管，她与全国校长韦罗妮卡·阿格雷达、总裁执行官奥斯卡·阿格雷达及全国学术副校长埃里克·蒙塔尼奥构成Unifranz全国—校区两级领导架构。",
    "birth_date_note": "所查公开来源（Unifranz官网、ANF/Fides、Red Uno及各类活动报道）均未披露其出生日期。",
    "name_note": "全名Eva Foronda Franco经Unifranz官网2017年EMBOL参访报道（署名Ing. Eva Foronda Franco）及哥伦比亚UDI大学新闻页（Jefe de Ingeniería Comercial UNIFRANZ）核实；媒体与官网博客多简作Eva Foronda。消歧说明：本档案以「Unifranz学术院长」职务为锚，与UPB圣克鲁斯校区副校长Carlos Foronda Rojas（BO-PERSON-000331）非同一人。",
    "name_zh_note": "_name_index.json拟定译名「埃娃·福龙达」；检索未发现中文媒体既有译名、Wikidata中文标签或中文维基百科条目，依规则name_zh置null，传记文本沿用拟定音译（姓Franco音译作「佛朗哥」）。",
    "education_note": "未检索到其学历学位的公开信息；官方与媒体报道仅以「Ing.（工程师）」称呼，推测持有工程类（很可能为商业工程学）学位，但毕业院校、学位层级与年份均无来源证实，education依铁律留空。",
    "family_note": "未见任何公开来源披露其家庭成员或婚姻状况，family_members留空。",
    "social_accounts_note": "社交媒体六平台扫描结果：LinkedIn仅命中西班牙同名同姓公证人Eva Foronda Rodriguez（Universidad de Valladolid，定居Simancas，非同一人）；X平台存在@EvaForonda账号，但2013年注册后零关注、零粉丝、零推文，无法归属于本人；Facebook、Instagram、YouTube、TikTok上相关内容均发布于Unifranz各校区官方账号（如facebook.com/UnifranzLpOficial、youtube.com/@UnifranzOficial），未发现经核实的个人账号，social_accounts依铁律留空。",
    "position_note": "职务头衔在来源中存在两种表述：官网博客及活动报道多作「decana académica de Unifranz La Paz（拉巴斯校区学术院长）」，ANF/Fides、Red Uno及El Deber等全国性报道简作「decana académica de Unifranz」；Unifranz官网「Autoridades académicas」全国主管名录页不列各校区学术院长，故本档案采用更精确的「拉巴斯校区学术院长」并注明简写变体。",
    "profile_note": "Unifranz官网相关报道配图均为活动现场合影或校园场景（如2024年3月国际教育者奖颁奖礼配图），未能确认可归属于本人的个人肖像照，profile字段不填。",
    "collection_meta": {
        "collection_date": "2026-10-27",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "news_search",
            "web_search",
            "social_media"
        ],
        "completeness_score": 58,
        "notes": "数据来源确认：Unifranz官网（学术主管名录页+8篇官网博客，发布日期经页面datePublished元数据核实）为职务与活动主源；ANF/Noticias Fides通讯社（2026-04-08）与Red Uno电视台（2026-09-10）两个独立媒体源交叉验证其现任职务与学术主张；哥伦比亚UDI大学新闻页佐证其全名与2018年前后专业主任职务（该页因网络超时未能全文直读，仅作辅助佐证，相关事实以直读的Unifranz页面为准）。关键发现：①全名Eva Foronda Franco（母姓Franco）；②职务锚定拉巴斯校区学术院长，至迟2023年1月上任、截至2026年9月在任，就任精确日期不可得；③消歧完成：与UPB副校长Carlos Foronda Rojas（BO-PERSON-000331）及西班牙公证人Eva Foronda Rodriguez均非同一人。存疑与缺口：出生日期/出生地、学历学位、家庭成员均无公开来源，相应字段依铁律留空并在注中说明；无个人社媒账号（六个平台扫描仅命中同名他人或机构账号）；无Wikidata条目；El Deber（2026年2月前后）有同类QS报道但因403未能直读，未列为引用。评分缺口说明：completeness_score未达85的剩余缺口属客观不可得——校区级学术院长公开披露的个人信息有限（无出生信息、无学历披露、无家族信息、无个人社媒、无既有中文译名）。",
        "quotes": [
            {
                "title": "Autoridades académicas | Universidad Privada Franz Tamayo（Unifranz官网学术主管名录页）",
                "url": "https://unifranz.edu.bo/universidad/autoridades/"
            },
            {
                "title": "Una delegación de Unifranz viaja a Mondragón para fortalecer lazos académicos（Unifranz官网博客, 2025-01-14）",
                "url": "https://unifranz.edu.bo/blog/una-delegacion-de-unifranz-viaja-a-mondragon-para-fortalecer-lazos-academicos/"
            },
            {
                "title": "Aprender haciendo: la experiencia de Unifranz que redefine la formación universitaria（ANF/Noticias Fides, 2026-04-08）",
                "url": "https://www.noticiasfides.com/innovacion-y-educacion/aprender-haciendo-la-experiencia-de-unifranz-que-redefine-la-formacion-universitaria"
            },
            {
                "title": "¿Qué debería aprender un universitario que se graduará en 2030?（Red Uno, 2026-09-10）",
                "url": "https://www.reduno.com.bo/educacion-e-innovacion/que-deberia-aprender-un-universitario-que-se-graduara-en-2030-202691012828"
            },
            {
                "title": "La Paz, ciudad culta: uno de los pilares de Futures Week（Unifranz官网博客, 2025-11-06）",
                "url": "https://unifranz.edu.bo/blog/la-paz-ciudad-culta-uno-de-los-pilares-de-futures-week/"
            },
            {
                "title": "TecMilenio forma «Docentes 360» de UNIFRANZ（Unifranz官网博客, 2023-01-26）",
                "url": "https://unifranz.edu.bo/blog/tecmilenio-forma-docentes-360-de-unifranz/"
            },
            {
                "title": "Unifranz La Paz celebró la excelencia docente con los International Educators Awards（Unifranz官网博客, 2024-03）",
                "url": "https://unifranz.edu.bo/blog/unifranz-la-paz-celebro-la-excelencia-docente/"
            },
            {
                "title": "Docentes Unifranz fueron reconocidos por la Comisión de Educación y Salud de la Cámara de Diputados（Unifranz官网, 2019-06-25）",
                "url": "https://unifranz.edu.bo/blog/docentes-unifranz-fueron-reconocidos-por-la-comision-de-educacion-y-salud-de-la-camara-de-diputados/"
            },
            {
                "title": "Vista a la Planta EMBOL S.A.（Unifranz官网博客, 2017-09-29，署名Ing. Eva Foronda Franco）",
                "url": "https://unifranz.edu.bo/blog/vista-a-la-planta-embol-s-a/"
            },
            {
                "title": "Cómo la educación superior impulsa estrategias para conectar formación y empleo（Unifranz官网博客, 2025-12-17，QS Stars评级阐释）",
                "url": "https://unifranz.edu.bo/blog/como-la-educacion-superior-impulsa-estrategias-para-conectar-formacion-y-empleo/"
            },
            {
                "title": "Dos títulos, un solo futuro: la doble titulación para la globalización del saber（Unifranz官网博客, 2025-12-31）",
                "url": "https://unifranz.edu.bo/blog/dos-titulos-un-solo-futuro-la-doble-titulacion-para-la-globalizacion-del-saber/"
            }
        ]
    },
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE", OUT)
print("bytes:", os.path.getsize(OUT))

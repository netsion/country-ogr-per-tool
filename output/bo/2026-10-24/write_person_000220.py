# -*- coding: utf-8 -*-
"""Generate BO-PERSON-000220 Gabriela Sanchez Salas person profile JSON."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000220.json")

profile = {
    "person_id": "BO-PERSON-000220",
    "wikidata_qid": None,
    "name": "Gabriela Sánchez Salas",
    "name_en": "Gabriela Sanchez Salas",
    "name_zh": "加夫列拉·桑切斯·萨拉斯",
    "aliases": ["Ing. Gabriela Sánchez Salas", "MSc. Gabriela Sánchez Salas"],
    "nationality": "BO",
    "gender": "female",
    "birth_date": None,
    "birth_place": None,
    "contacts": [
        {
            "type": "email",
            "value": "fiscalizacion@esm.gob.bo",
            "source": "ESM官网「透明度与人力资源」页面"
        }
    ],
    "current_positions": ["穆通钢铁公司总监察"],
    "education": [
        {
            "institution": "圣安德烈斯大学 (Universidad Mayor de San Andrés)",
            "degree": "bachelor",
            "field": "土木工程",
            "start_date": None,
            "end_date": None
        },
        {
            "institution": "玻利维亚军事工程学院「安东尼奥·何塞·德·苏克雷元帅」 (Escuela Militar de Ingeniería Mariscal Antonio José de Sucre)",
            "degree": "master",
            "field": "结构工程（桥梁评估方向）",
            "start_date": None,
            "end_date": "2015"
        }
    ],
    "work_experience": [
        {
            "start_date": None,
            "end_date": None,
            "organization": "穆通钢铁公司 (Empresa Siderúrgica del Mutún)",
            "org_id": "BO-SOE-009",
            "position": "总监察"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚总统部 (Ministerio de la Presidencia)",
            "org_id": "BO-GOV-006",
            "position": "公职人员"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "独立执业 (Independiente)",
            "org_id": None,
            "position": "结构领域专家"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000215",
            "person_name": "阿尔瓦罗·特赫里纳·奥利维拉 (Álvaro Tejerina Olivera)",
            "relationship_type": "colleague",
            "description": "同为帕斯政府矿业国企整顿期间穆通钢铁公司新一届管理层成员：特赫里纳于2025年12月31日经最高决议第32186号出任代理执行总裁，桑切斯·萨拉斯同期出任总监察，同属矿业与冶金部主管下的ESM执行层。"
        },
        {
            "person_id": "BO-PERSON-000068",
            "person_name": "马尔科·安东尼奥·卡尔德龙·德拉巴尔卡·金塔尼利亚 (Marco Antonio Calderón de la Barca Quintanilla)",
            "relationship_type": "superior",
            "description": "时任矿业与冶金部部长，为ESM的上级主管部委负责人；2025年12月31日在拉巴斯主持ESM管理层任命（特赫里纳出任代理执行总裁），桑切斯·萨拉斯同批出任总监察，任命序列上为其上级。"
        },
        {
            "person_id": None,
            "person_name": "胡斯托·路易斯·埃内斯托·利纳雷斯·古斯曼 (Justo Luis Ernesto Linares Guzmán)",
            "relationship_type": "other",
            "description": "ESM前任总监察（工程监察）：其2026年1月8日任内月度报告（ESM-FISC/INF N° 001/2026）为任职末期文件，桑切斯·萨拉斯随后接任该职位；2026年2月ESM对利纳雷斯及前总裁阿尔瓦多等前高管提起刑事控告（涉嫌反经济行为、渎职等）。"
        }
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Gabriela Sánchez Salas",
            "url": "https://bo.linkedin.com/in/gabriela-s%C3%A1nchez-salas-69348667",
            "source": "搜索摘要：结构领域专家（Especialista en el Área de Estructuras）、独立执业、毕业于UMSA，玻利维亚，约219名关注者"
        },
        {
            "platform": "facebook",
            "account_name": "gabriela.sanchezsalas.1",
            "url": "https://www.facebook.com/gabriela.sanchezsalas.1/",
            "source": "搜索摘要：曾就读圣安德烈斯大学（UMSA）与圣卡利斯托学校（Colegio San Calixto），曾任职GMLP"
        },
        {
            "platform": "other",
            "account_name": "GabrielaSanchezSalas",
            "url": "https://www.slideshare.net/GabrielaSanchezSalas",
            "source": "SlideShare个人主页：土木工程师，上传桥梁荷载承载力评估等演示文稿"
        }
    ],
    "family_members": [],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2015",
            "achievement": "在玻利维亚军事工程学院（EMI）完成硕士论文《玻利维亚桥梁评估精度——引入美国联邦公路管理局（FHWA）荷载评级方法的影响》，导师为胡安·安赫尔·龙达·巴斯克斯博士（Juan Ángel Ronda Vásquez）",
            "organization": "玻利维亚军事工程学院「安东尼奥·何塞·德·苏克雷元帅」 (Escuela Militar de Ingeniería Mariscal Antonio José de Sucre)"
        },
        {
            "date": "2026-01",
            "achievement": "以「MSc.」头衔受邀担任工程专业网络研讨会主讲人，主题为「好的设计不只是计算——正确应用设计准则」（2026年1月24日经Google Meet线上举行）",
            "organization": None
        },
        {
            "date": "2026",
            "achievement": "出任穆通钢铁公司总监察（Fiscal General），为帕斯政府矿业国企整顿后与代理执行总裁特赫里纳同批到任的新管理层成员，负责公司项目监察与合规职能",
            "organization": "穆通钢铁公司 (Empresa Siderúrgica del Mutún)"
        }
    ],
    "biography_summary": "加夫列拉·桑切斯·萨拉斯（Gabriela Sánchez Salas）是玻利维亚土木工程师，现任国有穆通钢铁公司（ESM）总监察（Fiscal General）。她毕业于拉巴斯圣安德烈斯大学（UMSA）土木工程专业，2015年在玻利维亚军事工程学院（EMI）完成结构工程方向硕士论文，研究引入美国联邦公路管理局（FHWA）荷载评级方法对玻利维亚公路桥梁评估精度的影响。LinkedIn与SlideShare资料显示她长期从事结构工程工作，曾以独立执业工程师身份开展桥梁荷载承载力评估，并关注拉巴斯城市岩土滑坡风险治理。第三方公职人员数据库（LatamVerify）记录显示2023年8月她任职于玻利维亚总统部。2026年初，在罗德里戈·帕斯政府整顿矿业国企的背景下，她接替卷入刑事控告的前任总监察利纳雷斯出任ESM总监察，与2025年12月31日获任代理执行总裁的阿尔瓦罗·特赫里纳同属矿业与冶金部确认的新一届管理层，任职期间正值穆通钢铁厂2025年2月投产后的前管理层追责与运营恢复关键阶段。她还受邀担任结构设计主题网络研讨会主讲人。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": ["official_website", "news_search", "web_search", "social_media", "other"],
        "notes": "1) 现任职务以ESM官网「透明度与人力资源」页面为准（ING. GABRIELA SÁNCHEZ SALAS – FISCAL GENERAL，官方邮箱fiscalizacion@esm.gob.bo）；确切任命日期未见公开文件，据公开报道与任务背景推断为2025年12月31日矿业部任命代理执行总裁特赫里纳（最高决议32186号）前后的同批调整；前总监察利纳雷斯2026年1月8日签署末期月度报告后卸任，构成接任时间上界。2) 学历来源：EMI硕士论文摘要（Scribd英/西双版本，LA PAZ 2015，导师Juan Ángel Ronda Vásquez）及LinkedIn/Facebook资料（UMSA土木工程、中学就读Colegio San Calixto）；UMSA学位层级按玻利维亚Ingeniero Civil惯例标注为bachelor，属合理推断。3) 总统部公职记录来自LatamVerify公职人员数据库（快照2023-08-17），单一来源同名记录，具体岗位不详。4) LinkedIn（结构领域专家、独立执业）与Facebook（曾任职GMLP，推断为拉巴斯市政府）信息来自搜索结果摘要（原页面需登录），GMLP经历未列入工作经历以免过度推断。5) Scribd一份《项目监察手册》(Manual de Fiscalización de Proyectos) 署名栏列有其名（Profesional en Obras Civiles），所属机构不详，未列入正式字段。6) 2025年前后其LinkedIn账号曾在ISSMGE GeoWB拉巴斯岩土技术考察团帖子下发表技术评论。7) 家庭成员、政治立场、出生日期/地点均无公开信息，留空。8) name_zh沿用既有索引译名「加夫列拉·桑切斯·萨拉斯」（未找到中文媒体报道，属标准音译，保留既有写法）。9) 无Wikidata条目。10) 完整性说明：人物为技术官僚，媒体曝光度低，公开信息有限，多个计分字段客观无法填充。11) 上级关系人卡尔德龙·德拉巴尔卡（时任矿业与冶金部部长，BO-PERSON-000068）来自El Deber报道及ESM法律文书（ESM受矿业部管辖），任命主持信息见El Deber与任务背景。",
        "quotes": [
            {
                "title": "Transparencia y Recursos Humanos - Empresa Siderúrgica del Mutún (ESM官网)",
                "url": "https://esm.gob.bo/transparencia.php"
            },
            {
                "title": "Posesionan a Álvaro Tejerina como presidente interino de la Siderúrgica del Mutún - El Deber",
                "url": "https://eldeber.com.bo/economia/posesionan-alvaro-tejerina-presidente-interino-siderurgica-mutun_1767396446"
            },
            {
                "title": "GABRIELA SANCHEZ SALAS - 55006 Perfil del Funcionario Público - LatamVerify",
                "url": "https://latamverify.com/profile/bo/fp/gabriela-sanchez-salas-55006.html"
            },
            {
                "title": "BRIDGE EVALUATION IN BOLIVIA (EMI硕士论文摘要, Postulante: Gabriela Sanchez Salas, La Paz 2015) - Scribd",
                "url": "https://www.scribd.com/document/953635798/BRIDGE-EVALUATION-IN-BOLIVIA"
            },
            {
                "title": "EVALUACION DE PUENTES EN BOLIVIA (tesis de maestría de Gabriela Sánchez Salas) - Scribd",
                "url": "https://es.scribd.com/doc/293177769/EVALUACION-DE-PUENTES-EN-BOLIVIA"
            },
            {
                "title": "QUERELLA ESM 02 DE MARZO 2026 (ESM对前高管刑事控告, 提及前总裁Tejerina与前总监察Linares) - Scribd",
                "url": "https://es.scribd.com/document/1075735840/QUERELLA-ESM-02-DE-MARZO-para-impresion"
            },
            {
                "title": "Gabriela Sánchez Salas - Ingeniero - LinkedIn Bolivia",
                "url": "https://bo.linkedin.com/in/gabriela-s%C3%A1nchez-salas-69348667"
            },
            {
                "title": "Gabriela Sánchez Salas - Facebook个人主页",
                "url": "https://www.facebook.com/gabriela.sanchezsalas.1/"
            },
            {
                "title": "Gabriela Sanchez Salas, Ingeniero civil - SlideShare",
                "url": "https://www.slideshare.net/GabrielaSanchezSalas"
            },
            {
                "title": "Evaluacion de capacidad de carga de un puente bolivia (演示文稿) - SlideShare",
                "url": "https://es.slideshare.net/slideshow/evaluacion-de-capacidad-de-carga-de-un-puente-bolivia/61045585"
            },
            {
                "title": "ESAM Sucre网络研讨会帖子（主讲人MSc. Gabriela Sánchez Salas, 2026-01-24） - Facebook",
                "url": "https://www.facebook.com/esamsucre2/posts/914771987787335"
            },
            {
                "title": "ISSMGE GeoWB mission to La Paz, Bolivia（Gabriela Sánchez Salas技术评论） - LinkedIn",
                "url": "https://www.linkedin.com/posts/fernando-marinho-8a62593b_as-part-of-its-commitment-to-fostering-international-activity-7323894651805921280-1Vkn"
            }
        ]
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE", OUT)
print("bytes:", os.path.getsize(OUT))

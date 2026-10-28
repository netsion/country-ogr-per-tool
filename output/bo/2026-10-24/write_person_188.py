# -*- coding: utf-8 -*-
"""Write BO-PERSON-000188 person profile JSON (Jorge Arnaldo Saenz Castillo)."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000188.json")

profile = {
    "person_id": "BO-PERSON-000188",
    "wikidata_qid": None,
    "name": "Jorge Arnaldo Saenz Castillo",
    "name_en": "Jorge Arnaldo Saenz Castillo",
    "name_zh": "豪尔赫·阿纳尔多·塞恩斯·卡斯蒂略",
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "contacts": [
        {
            "type": "phone",
            "value": "+(591 4) 4120900 / 4520317",
            "source": "ENDE官网《权威名录》(Nómina de Autoridades) 所列联系电话（公司机构线路，非个人专线）"
        },
        {
            "type": "fax",
            "value": "+(591 4) 4520318",
            "source": "ENDE官网《权威名录》(Nómina de Autoridades) 所列传真（公司机构线路）"
        },
        {
            "type": "email",
            "value": "ende@ende.bo",
            "source": "ENDE官网《权威名录》(Nómina de Autoridades) 所列机构邮箱（公司公共邮箱，非个人邮箱）"
        }
    ],
    "current_positions": [
        "玻利维亚国家电力公司（ENDE）企业发展和经济部总经理"
    ],
    "education": [],
    "work_experience": [
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚国家电力公司 (Empresa Nacional de Electricidad)",
            "org_id": "BO-SOE-003",
            "position": "企业发展和经济部总经理"
        },
        {
            "start_date": "2022-10-10",
            "end_date": "2022-10-14",
            "organization": "CRECER发展金融机构 (CRECER IFD - Institución Financiera de Desarrollo)",
            "org_id": None,
            "position": "全国内部审计总经理（临时代理）"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000186",
            "person_name": "马里奥·拉赖恩·萨阿维德拉 (Mario Larrain Saavedra)",
            "relationship_type": "colleague",
            "description": "ENDE临时总裁（2025年11月18日帕斯政府能源部门领导层更替中获任）；塞恩斯·卡斯蒂略同批进入改组后的ENDE新一届高管团队，任企业发展和经济部总经理"
        },
        {
            "person_id": None,
            "person_name": "费利佩·桑切斯·古斯曼 (Felipe Sanchez Guzman)",
            "relationship_type": "colleague",
            "description": "塞恩斯·卡斯蒂略的职务前任：2024年（至2025年初）以临时代理身份担任ENDE企业发展和经济部总经理，2025年11月领导层更替后由塞恩斯接任"
        },
        {
            "person_id": "BO-PERSON-000189",
            "person_name": "吉列尔莫·莫拉莱斯·拉伊诺夫 (Guillermo Morales Rainoff)",
            "relationship_type": "colleague",
            "description": "同届ENDE高管团队成员，任电力系统运营总经理（临时代理）"
        },
        {
            "person_id": "BO-PERSON-000190",
            "person_name": "豪尔赫·阿图罗·伊波雷·萨尔盖罗 (Jorge Arturo Iporre Salguero)",
            "relationship_type": "colleague",
            "description": "同届ENDE高管团队成员，任项目执行总经理"
        }
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "JORGE Arnaldo Saenz Castillo",
            "url": "https://bo.linkedin.com/in/jorge-arnaldo-saenz-castillo-5abb00255",
            "source": "LinkedIn检索结果，姓名完全一致；档案显示经历CRECER IFD、所在地Totora，与ASFI 2022年披露的CRECER IFD任职记录吻合，可信度较高；档案全文未能访问"
        },
        {
            "platform": "youtube",
            "account_name": "@jorgearnaldosaenzcastillo6509",
            "url": "https://www.youtube.com/channel/UCJPvyaXhuJSdvPH64LJGftg",
            "source": "YouTube及IDCrawl聚合检索，姓名完全一致；内容仅为个人音乐歌单，身份吻合度为中等置信"
        }
    ],
    "family_members": [],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2025-11",
            "achievement": "在罗德里戈·帕斯政府2025年11月18日能源部门领导层更替后，出任国家电力公司（ENDE）企业发展和经济部总经理，进入公司新一届高管团队",
            "organization": "玻利维亚国家电力公司 (Empresa Nacional de Electricidad)"
        },
        {
            "date": "2026-06",
            "achievement": "以企业发展和经济部总经理身份被指定为ENDE公开招标采购程序负责人（Responsable de Procesos de Contratación），主持多项公开招标（2026年6月、9月决议及10月SICOES招标档案均有署名）",
            "organization": "玻利维亚国家电力公司 (Empresa Nacional de Electricidad)"
        }
    ],
    "biography_summary": "豪尔赫·阿纳尔多·塞恩斯·卡斯蒂略（Jorge Arnaldo Saenz Castillo）为玻利维亚公职与企业高管，现任国家电力公司（ENDE）企业发展和经济部总经理（Gerente de Desarrollo Empresarial y Economía），公司驻地科恰班巴。其职业背景偏重金融与内部审计：2022年10月在玻利维亚发展金融机构CRECER IFD任职期间，因全国内部审计总经理米格尔·阿尔贝托·佩雷斯·阿兰迪亚病假，被指定临时代理该职（2022年10月10日至14日，载于玻利维亚金融监管局ASFI重大事项披露）。2025年11月罗德里戈·帕斯就任总统后，碳氢化合物与能源部于11月18日依据最高决议完成能源部门领导层更替，马里奥·拉赖恩·萨阿维德拉出任ENDE临时总裁；塞恩斯·卡斯蒂略随后进入ENDE新一届高管团队，接替此前临时代理同职的费利佩·桑切斯·古斯曼。2026年公开记录显示其多次以企业发展和经济部总经理身份担任ENDE公开招标采购程序负责人（2026年6月、9月决议及10月SICOES招标档案均有署名）。2026年10月反对派议员阿德里安娜·希门尼斯公布的国企薪资名册显示，ENDE该职位月薪约为3.8万玻利维亚诺。其出生日期、学历、家庭情况及公开政策立场均未见公开报道。",
    "profile": None,
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "news_search",
            "web_search",
            "social_media",
            "government_registry"
        ],
        "notes": "1) 现职三源互证：ENDE官网《权威名录》（2026-10访问全文）确认其职务；SICOES/Infosiscon FORM100（2026-10-06全文）及ENDE 2026年6月/9月招标决议均以其职衔署名。2) 2025-11-18任命背景：能源部（MHE）官网、Opinión、ERBOL三源全文确认帕斯政府能源部门班子就任及Larrain出任ENDE临时总裁，但报道仅逐一列出6名部委级/总裁级人选，未列各总经理，故塞恩斯个人获任精确日期未获直接文献，work_experience中start_date留空。3) CRECER IFD履历：ASFI 2022-10-11披露全文确认其临时代理全国内部审计总经理（2022-10-10至10-14），与LinkedIn档案（经历CRECER IFD、所在地Totora）互证；另两条ASFI披露摘要（2021-12-15、2019-12-18）亦出现同名人物，因全文多次抓取失败无法核实机构与职务细节，未写入结构化字段。4) 社交账号6项扫描：LinkedIn、YouTube姓名完全一致（前者有CRECER IFD交叉佐证，较高可信；后者仅个人歌单，中等置信）；Facebook仅有群组欢迎帖提及（非个人主页，未收录）；X/Twitter、Instagram、TikTok未检出同名账号。5) 未找到：出生日期/地、教育背景、家庭成员、政治立场、Wikidata条目、中文媒体报道（name_zh沿用既有音译）。6) 薪资信息为职位级公开名册（对应2024年12月/2025年11月名册），非其个人薪资的直接确认。7) ASFI与ende.bo部分PDF在当前网络环境直连超时，全文获取依赖web_reader与search-read快照。8) completeness_score约51：该人物为低曝光技术官僚，出生、教育、家庭、政治立场等字段客观上无公开信息，在不编造前提下无法达到70分。",
        "quotes": [
            {
                "title": "NÓMINA DE AUTORIDADES | ENDE Corporación",
                "url": "https://www.ende.bo/nomina-autoridades"
            },
            {
                "title": "PERFIL COMPLETO - Mario Larrain | ENDE Corporación",
                "url": "https://www.ende.bo/prerfil-presidente/28"
            },
            {
                "title": "Ministerio de Hidrocarburos y Energías conforma su equipo con la posesión de nuevas autoridades del sector energético (MHE, 2025-11-18)",
                "url": "https://www.mhe.gob.bo/2025/11/18/ministerio-de-hidrocarburos-y-energias-conforma-su-equipo-con-la-posesion-de-nuevas-autoridades-del-sector-energetico/"
            },
            {
                "title": "Ministro de Hidrocarburos posesiona a 6 autoridades; Mario Larraín es el presidente de ENDE (Opinión, 2025-11-18)",
                "url": "https://www.opinion.com.bo/pais/ministro-hidrocarburos-posesiona-6-autoridades-mario-larrain-es-presidente-ende/20251118174631983804.html"
            },
            {
                "title": "El Ministro de Hidrocarburos posesiona a nuevos viceministros y autoridades del área energética (ERBOL, 2025-11-18)",
                "url": "https://erbol.com.bo/economía/el-ministro-de-hidrocarburos-posesiona-nuevos-viceministros-y-autoridades-del-área"
            },
            {
                "title": "Switches de acceso para ENDE-USTI - SICOES FORM 100 (2026-10-06) via Infosiscon",
                "url": "https://infosiscon.com/switches-de-acceso-para-ende-usti-lct803573.html"
            },
            {
                "title": "Reporte Informativo ASFI al 11/10/2022 - CRECER IFD Hecho Relevante (Gerente Nacional de Auditoría Interna a.i.)",
                "url": "https://appweb2.asfi.gob.bo/PaginasPublicas2/VistaHechosRelevantes/VisorDocumentos.aspx?variable1=8cae9554-fbd5-4259-9df1-445fdd3d4617"
            },
            {
                "title": "Diputada denuncia salarios de Bs 88.000 en Huanuni y de Bs 41.000 y Bs 40.000 en ENDE (Cabildeo Digital, 2026-10-16)",
                "url": "https://www.cabildeodigital.com/2026/10/diputada-denuncia-salarios-de-bs-88000.html"
            },
            {
                "title": "JORGE Arnaldo Saenz Castillo - LinkedIn",
                "url": "https://bo.linkedin.com/in/jorge-arnaldo-saenz-castillo-5abb00255"
            },
            {
                "title": "Jorge Arnaldo Saenz Castillo - YouTube Channel",
                "url": "https://www.youtube.com/channel/UCJPvyaXhuJSdvPH64LJGftg"
            }
        ]
    }
}


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print("WROTE:", OUT)
    # quick sanity re-read
    with open(OUT, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("person_id:", data["person_id"])
    print("bio_len:", len(data["biography_summary"]))
    print("quotes:", len(data["collection_meta"]["quotes"]))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Build BO-PERSON-000263 Adolfo Guzmán Rodriguez (Banco Ganadero CFO) profile."""
import json
import os

OUT = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000263.json"

profile = {
    "person_id": "BO-PERSON-000263",
    "wikidata_qid": None,
    "name": "Adolfo Guzmán Rodriguez",
    "name_en": "Adolfo Guzman Rodriguez",
    "name_zh": None,
    "aliases": ["Adolfo Guzmán Rodríguez", "Adolfo Guzman", "Adolfo Guzmán R."],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "contacts": [
        {
            "type": "email",
            "value": "aguzman@bg.com.bo",
            "source": "AmCham Bolivia Directorio 2024（Calaméo 名录）",
        },
        {
            "type": "phone",
            "value": "+591 3 317-3080",
            "source": "IFC Ganadero Loan (IFC-35504) 项目问询联系方式（Early Warning System 页面列于其名下，银行为牧业银行总机）",
        },
    ],
    "current_positions": [
        "玻利维亚牧业银行 (Banco Ganadero S.A.) 财务总经理 (Gerente de Finanzas)",
        "牧业投资基金管理公司 (GanaSafi S.A.) 董事长 (Presidente del Directorio)",
    ],
    "education": [
        {
            "institution": "芝加哥大学 (University of Chicago)",
            "degree": None,
            "field": None,
        }
    ],
    "work_experience": [
        {
            "organization": "玻利维亚牧业银行 (Banco Ganadero S.A.)",
            "org_id": "BO-FIN-011",
            "position": "财务总经理 (Gerente de Finanzas)",
            "start_date": "1998-04-14",
            "end_date": None,
        },
        {
            "organization": "牧业投资基金管理公司 (GanaSafi S.A.)",
            "org_id": None,
            "position": "董事长 (Presidente del Directorio)",
            "start_date": None,
            "end_date": None,
        },
        {
            "organization": "玻利维亚中央银行 (Banco Central de Bolivia)",
            "org_id": "BO-FIN-001",
            "position": "国际储备副总经理 (Subgerente de Reservas Internacionales)",
            "start_date": None,
            "end_date": None,
        },
        {
            "organization": "玻利维亚中央银行 (Banco Central de Bolivia)",
            "org_id": "BO-FIN-001",
            "position": "市场分析师/专业分析师 (Analista de Mercado / Profesional Analista)",
            "start_date": None,
            "end_date": None,
        },
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000261",
            "person_name": "罗纳德·古铁雷斯·洛佩斯 (J. Ronald Gutiérrez López)",
            "relationship_type": "superior",
            "description": "古铁雷斯自2003年起任玻利维亚牧业银行总经理，是古兹曼的直接上司；古兹曼在古铁雷斯外出期间多次代行总经理职权（Gerente General a.i.，如2016年2月、6月、8月及2023年11月27日至29日）。两人同时在银行关联的投资基金管理公司 GanaSafi 董事会共事（古兹曼任董事长、古铁雷斯任副董事长）。",
        },
        {
            "person_id": None,
            "person_name": "卡洛斯·胡安·阿诺德·萨尔迪亚斯·波索 (Carlos Juan Arnold Saldias Pozo)",
            "relationship_type": "subordinate",
            "description": "阿诺德任投资基金管理公司 GanaSafi S.A. 总经理（2022年年报高管名录），向以古兹曼为董事长的董事会汇报。",
        },
        {
            "person_id": "BO-PERSON-000259",
            "person_name": "费尔南多·莫纳斯特里奥·涅梅 (Fernando Monasterio Nieme)",
            "relationship_type": "superior",
            "description": "莫纳斯特里奥家族控股牧业银行，费尔南多·莫纳斯特里奥·涅梅任银行董事会主席（Presidente，官网高管名录），为古兹曼在治理层面的最高上级。",
        },
        {
            "person_id": None,
            "person_name": "威尔弗雷多·查孔·阿甘多尼亚 (Wilfredo Chacón Argandoña)",
            "relationship_type": "colleague",
            "description": "查孔任牧业银行运营总经理（Gerente de Operaciones），与古兹曼同属银行核心高管团队（2024年报与官网高管名录），并同样多次代行总经理职权。",
        },
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Adolfo Guzman",
            "url": "https://bo.linkedin.com/in/adolfo-guzm%C3%A1n-b2812927",
            "source": "LinkedIn 搜索摘要（头衔 CFO en Banco Ganadero，约807名关注者）",
        }
    ],
    "family_members": [],
    "political_stances": [
        {
            "date": "2009-04-07",
            "topic": "玻利维亚央行外汇买卖价差管制（汇率政策）",
            "stance_content": "针对央行「银行买卖美元价差不得超过一美分」的新规，古兹曼表态不认为利润空间压缩会抑制银行业，牧业银行将照常买卖美元；并称不会因此产生官方渠道之外的黑市——「我不认为会出现额外的黑市或其他市场，因为如今已有运作良好的平行市场」（源页面标注日期2009-04-07，内容指向汇率新政，日期以页面为准）。",
            "source": "El Día（eldia.com.bo）新闻报道全文",
        }
    ],
    "major_achievements": [
        {
            "date": "2015-10",
            "achievement": "主管发行3500万玻利维亚诺次级债券（Bonos Subordinados），期限7年、票面利率3.64%，创2015年玻利维亚金融系统次级债券最低发行利率，为银行打开逾3.5亿诺的新增放贷空间。",
            "organization": "玻利维亚牧业银行 (Banco Ganadero S.A.)",
        },
        {
            "date": "2014-08",
            "achievement": "以财务总经理身份参与牧业银行与安第斯开发公司（CAF）最高1000万美元信贷额度协议的签署，扩大银行对企业的融资供给。",
            "organization": "玻利维亚牧业银行 (Banco Ganadero S.A.)",
        },
        {
            "date": "2021-11",
            "achievement": "作为银行发言人宣布牧业银行连续第三年获得摩根大通「Elite Quality Recognition Award 2021」国际支付质量奖（全年逾1万笔对外支付、成功率超过99%），并介绍银行 GanaMóvil、GanaNet 等数字化服务布局。",
            "organization": "玻利维亚牧业银行 (Banco Ganadero S.A.)",
        },
    ],
    "biography_summary": "阿道夫·古斯曼·罗德里格斯（Adolfo Guzmán Rodriguez）是玻利维亚经济学家，现任玻利维亚牧业银行（Banco Ganadero S.A.，总部圣克鲁斯、Monasterio 家族控股的商业银行）财务总经理（Gerente de Finanzas/CFO），自1998年4月14日起出任该职至今已逾27年，是玻利维亚大型商业银行中任职时间最长的财务高管之一。此前他长期在玻利维亚中央银行任职，历任专业分析师、市场分析师和国际储备副总经理。除主管银行财务条线外，他还担任银行关联投资基金管理公司 GanaSafi S.A. 董事长（2022年年报署名），并在总经理古铁雷斯外出期间多次代行总经理职权（Gerente General a.i.，如2016年2月、6月、8月及2023年11月27日至29日）。他是银行对外发声的主要高管之一，代表银行就次级债券发行（2015年3.64%最低利率）、CAF与国际金融公司（IFC）信贷合作、摩根大通国际支付质量奖、外汇监管新政、数字化转型（GanaMóvil、GanaNet）等议题公开发言，并曾在 Management 杂志等媒体撰文提供理财建议。其LinkedIn资料显示曾就读芝加哥大学；ASFI监管文件显示其2016年时50岁、玻利维亚籍。",
    "profile": {"source_url": None, "local_path": None},
    "identity_note": "本档案人物为玻利维亚牧业银行（Banco Ganadero）财务总经理，经银行官网高管名录（2026-10-25 现网读取）、银行2024年年报、ASFI 债券招募说明书及 Los Tiempos/Opinión/El Día 等多家媒体交叉确认；玻利维亚存在多名同名「Adolfo Guzmán」（含政界人士），均与本档案无涉。",
    "name_spelling_note": "姓氏重音核实：现任雇主银行官网高管名录与2024年年报作「Rodriguez」（无重音），ASFI 债券招募说明书、GanaSafi 文件及部分媒体作「Rodríguez」（有重音）；本档案 name 采用现任雇主官方拼写（无重音），有重音变体保留于 aliases。",
    "birth_date_note": "无公开出生日期；ASFI 债券招募说明书（数据截至2016-09-30，Cuadro 16）记载时年50岁，据此推算约1965-1966年生，未确证故 birth_date 置空。",
    "position_note": "职务为 Gerente de Finanzas（财务总经理），媒体亦称 gerente Financiero、gerente nacional de finanzas；LinkedIn 头衔为 CFO en Banco Ganadero。2023-11-27至29、2016年2月/6月/8月等总经理缺勤期间多次代行总经理职权（Gerente General a.i.，见 ASFI 监管登记卡及债券文件）。",
    "education_note": "芝加哥大学信息仅来自本人 LinkedIn 资料（单一来源），就读项目与学位未知；其经济学家（Economista）职业资格见 ASFI 官方文件。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "annual_report",
            "government_registry",
            "news_search",
            "web_search",
            "social_media",
            "other",
        ],
        "notes": "数据来源确认情况：现任职务（1998-04-14起任牧业银行财务总经理）由银行官网高管名录、2024年年报（PDF原文提取）、ASFI债券招募说明书（Cuadro 16官方履历表：经济学家、玻利维亚籍、1998-04-14入职即任现职、此前任职玻利维亚中央银行国际储备副总经理）三重官方来源确认；GanaSafi董事长职务由GanaSafi 2022年年报（PDF原文署名）确认；2015债券发行（Opinión全文）、2021摩根大通奖（Los Tiempos全文）、外汇政策表态（El Día全文，该文页面标注2009-04-07但内容指向2011年11月汇改，日期存疑，故未据此断言任职起点）均为精读全文来源；Guzmán R.代行总经理（2023-11-27至29）来自ASFI监管登记卡页搜索摘要（appweb.asfi.gob.bo 站点本机直连失败，未能全文核验）；邮箱aguzman@bg.com.bo来自AmCham名录（单一来源）。关键发现：入职牧业银行前任职玻利维亚中央银行（BO-FIN-001），是银行子公司GanaSafi董事长。存疑字段：教育（芝加哥大学）仅LinkedIn单一来源，学位与专业未知；出生日期仅有2016年50岁间接记录；无个人Facebook/Twitter/Instagram/TikTok账号检出；name_zh经中文检索未发现可靠既有译名，置null。中层高管公开信息有限，completeness_score受限于客观可得信息。",
        "quotes": [
            {
                "title": "Directores y Principales Ejecutivos | Banco Ganadero S.A.（银行官网高管名录）",
                "url": "https://www.bg.com.bo/institucional/directores-ejecutivos/",
            },
            {
                "title": "Memoria Anual 2024 - Banco Ganadero S.A.（银行2024年报PDF）",
                "url": "https://prodbgwebportal.blob.core.windows.net/assets/pdf/Memorias_BGA_2024.pdf",
            },
            {
                "title": "Prospecto Bonos Subordinados Banco Ganadero V - ASFI（官方招募说明书PDF，含主要高管履历表）",
                "url": "https://www.asfi.gob.bo/sites/default/files/2025-08/Bonos%20Subordinados%20Banco%20Ganadero%20V.pdf",
            },
            {
                "title": "Memoria Anual 2022 - GanaSafi S.A.（GanaSafi年报PDF，董事长署名）",
                "url": "https://www.ganasafi.com.bo/docs/Memoria_GanaSafi_Completa_2022.pdf",
            },
            {
                "title": "Exitosa colocación de bonos del Banco Ganadero - Opinión（2015-10-16）",
                "url": "https://www.opinion.com.bo/articulo/economia/exitosa-colocaci-oacute-n-bonos-banco-ganadero/20151016195100533473.html",
            },
            {
                "title": "Banco Ganadero recibe premio a la excelencia por sus servicios de comercio exterior - Los Tiempos（2021-11-24）",
                "url": "https://www.lostiempos.com/actualidad/economia/20211124/banco-ganadero-recibe-premio-excelencia-sus-servicios-comercio-exterior",
            },
            {
                "title": "El BCB apunta a sostener las reservas y frenar dolarización - El Día",
                "url": "https://www.eldia.com.bo/noticia.php?id=4335&id_cat=397",
            },
            {
                "title": "Ganadero Loan (IFC-35504) - Early Warning System（IFC项目页，Finance Manager联系方式）",
                "url": "https://ewsdata.rightsindevelopment.org/projects/35504-ganadero-loan/",
            },
            {
                "title": "Tarjeta de Registro - ASFI（牧业银行监管登记卡，代行总经理记录）",
                "url": "https://appweb.asfi.gob.bo/Reportes_asp/rmi/tarjeta.asp?c=51863&t=2",
            },
            {
                "title": "Adolfo Guzman - CFO en Banco Ganadero - LinkedIn",
                "url": "https://bo.linkedin.com/in/adolfo-guzm%C3%A1n-b2812927",
            },
            {
                "title": "¿Quiénes somos? - GanaSafi（董事长名录页）",
                "url": "https://www.ganasafi.com.bo/quienes-somos",
            },
            {
                "title": "CAF y Banco Ganadero firman contrato de línea de crédito por hasta USD 10 millones（2014-08-25）",
                "url": "https://www.caf.com/es/actualidad/noticias/caf-y-banco-ganadero-firman-contrato-de-linea-de-credito-por-hasta-usd-10-millones/",
            },
            {
                "title": "RECONOCIMIENTO BANCO GANADERO RECIBE PREMIO A LA EXCELENCIA - Nueva Economía（2021-11-24）",
                "url": "https://nuevaeconomia.com.bo/news/RECONOCIMIENTO%20BANCO%20GANADERO%20RECIBE%20PREMIO%20A%20LA%20EXCELENCIA",
            },
            {
                "title": "Podcast d'Innova - Adolfo Guzmán - Gerente de finanzas Banco Ganadero - YouTube",
                "url": "https://www.youtube.com/watch?v=fafGliKcbHY",
            },
            {
                "title": "Programa de Emisiones de Bonos Banco Ganadero I - ASFI（2018，主要高管名录）",
                "url": "https://www.asfi.gob.bo/sites/default/files/2025-08/Programa%20de%20Emisiones%20de%20Bonos%20Banco%20Ganadero%20I.pdf",
            },
        ],
    },
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE", OUT)
print("bytes:", os.path.getsize(OUT))

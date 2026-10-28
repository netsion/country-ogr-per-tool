# -*- coding: utf-8 -*-
"""Write person profile BO-PERSON-000246 (Jose Vicente Herrera Amenabar)."""
import json
import os

profile = {
    "person_id": "BO-PERSON-000246",
    "wikidata_qid": None,
    "name_zh": None,
    "name": "José Vicente Herrera Amenabar",
    "name_en": "Jose Vicente Herrera Amenabar",
    "aliases": ["José Vicente Herrera Amenábar"],
    "nationality": "BO",
    "gender": "male",
    "contacts": [],
    "current_positions": ["玻利维亚国民联盟银行总经理"],
    "education": [
        {
            "institution": "霍特国际商学院 (Hult International Business School)",
            "degree": "master",
            "field": "工商管理（MBA）",
            "note": "信息来自其LinkedIn档案标题「MBA Hult Business School」；就读年份与校区不详。",
            "source": "https://bo.linkedin.com/in/jose-vicente-herrera-amenabar-a7b612196"
        }
    ],
    "work_experience": [
        {
            "organization": "玻利维亚国民联盟银行 (Banco Unión S.A.)",
            "org_id": "BO-FIN-007",
            "position": "总经理",
            "position_en": "Gerente General",
            "start_date": "2025-12-05",
            "end_date": None,
            "description": "2025年12月初经董事会决议出任总经理，接替被免去职务的前任总经理马塞洛·伦索·希门尼斯·科尔多瓦 (Marcelo Renzo Jiménez Cordova)；任命于2025-12-05经玻利维亚证券交易所重大信息公告披露，银行官方社媒同日宣布。现任于银行官网「Directorio y Plantel Ejecutivo」名录在列。",
            "source": "https://www.bbv.com.bo/Publicacionv3/View_Publicacion/Detalle_HR1.aspx?Publicacion=651541"
        },
        {
            "organization": "玻利维亚信贷银行 (Banco de Crédito de Bolivia)",
            "org_id": "BO-FIN-003",
            "position": "零售银行部总经理",
            "position_en": "Gerente de División Banca Minorista",
            "start_date": "2025-07-01",
            "end_date": "2025-11-28",
            "description": "ASFI高管登记卡记录：自2025-07-01起执掌零售银行部（此前任企业银行东方地区区域总经理）；2025-11-27提出辞职以转任Banco Unión，最后工作日为2025-11-28。",
            "source": "https://appweb.asfi.gob.bo/Reportes_asp/rmi/tarjeta.asp?c=51828&t=2"
        },
        {
            "organization": "玻利维亚信贷银行 (Banco de Crédito de Bolivia)",
            "org_id": "BO-FIN-003",
            "position": "企业银行区域总经理（东方地区）",
            "position_en": "Gerente de Área Banca Empresas (Región Oriente)",
            "start_date": "2023-07-01",
            "end_date": "2025-06-30",
            "description": "ASFI高管登记卡记录（2023-06-28重大事项）：自2023-07-01起任企业银行区域总经理，此前任客户体验与数字化转型服务总经理。其LinkedIn亦以「企业银行与公司业务区域总经理」描述该段经历。",
            "source": "https://appweb.asfi.gob.bo/Reportes_asp/rmi/tarjeta.asp?c=51828&t=2"
        },
        {
            "organization": "玻利维亚信贷银行 (Banco de Crédito de Bolivia)",
            "org_id": "BO-FIN-003",
            "position": "客户体验与数字化转型服务总经理",
            "position_en": "Gerente de Servicio Experiencia Cliente Transformación Digital",
            "start_date": "2022-09-01",
            "end_date": "2023-06-30",
            "description": "ASFI高管登记卡记录（2022-09-30重大事项）：自2022-09-01加入BCP出任该职，接替转任企业银行区域总经理的安德烈斯·库恩·桑吉内斯 (Andrés Kuhn Sangines)。",
            "source": "https://appweb.asfi.gob.bo/Reportes_asp/rmi/tarjeta.asp?c=51828&t=2"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000245",
            "person_name": "鲁本·马里奥·费鲁菲诺·戈伊蒂亚 (Rubén Mario Ferrufino Goitia)",
            "relationship_type": "superior",
            "description": "Banco Unión S.A. 董事会主席，为其直接上级；2025年12月主持董事会会议决定任命其为总经理。"
        },
        {
            "person_id": None,
            "person_name": "马塞洛·伦索·希门尼斯·科尔多瓦 (Marcelo Renzo Jiménez Cordova)",
            "relationship_type": "colleague",
            "description": "Banco Unión S.A. 前任总经理；2025年12月董事会决议免去其职务，由本人接任总经理。"
        }
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Jose Vicente Herrera Amenabar",
            "url": "https://bo.linkedin.com/in/jose-vicente-herrera-amenabar-a7b612196",
            "source": "LinkedIn公开档案（LinkedIn目录页与AeroLeads索引交叉印证；档案主页因访问限制未逐字核读）"
        }
    ],
    "family_members": [],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2026",
            "achievement": "获第11届「美洲金融创新者奖」（Premios a los Innovadores Financieros en las Américas，Fintech Americas主办）金融普惠（Inclusión Financiera）类金奖（Oro），获奖身份为总经理。",
            "organization": "玻利维亚国民联盟银行 (Banco Unión S.A.)"
        },
        {
            "date": "2026-03-30",
            "achievement": "代表银行与德国Sparkassenstiftung für internationale Kooperation基金会签署机构间合作协议，推动金融教育与金融普惠项目（含面向女性创业者的培训计划），并表示该联盟将扩大金融教育覆盖面、帮助更多人做出明智的财务决策。",
            "organization": "玻利维亚国民联盟银行 (Banco Unión S.A.)"
        }
    ],
    "biography_summary": "何塞·比森特·埃雷拉·阿梅纳瓦尔（José Vicente Herrera Amenabar），玻利维亚银行家，现任国家控股的玻利维亚国民联盟银行（Banco Unión S.A.）总经理：2025年12月经董事会决议接替被免职的马塞洛·伦索·希门尼斯·科尔多瓦出任该职，任命于12月5日经玻利维亚证券交易所重大信息公告及银行官方社媒宣布。此前任职于玻利维亚信贷银行（BCP）：2022年9月加入任客户体验与数字化转型服务总经理，2023年7月升任企业银行区域总经理（东方地区），2025年7月执掌零售银行部，同年11月28日离职转投Banco Unión。据其LinkedIn档案，拥有霍特国际商学院MBA学位。执掌Banco Unión后主推金融普惠与数字化转型：2026年3月代表银行与德国Sparkassenstiftung基金会签署金融教育合作协议；同年在Fintech Americas第11届「美洲金融创新者奖」中获金融普惠类金奖。出生日期、出生地及家庭情况未见公开报道。",
    "social_accounts_note": "六平台社媒扫描（facebook/twitter_x/instagram/tiktok/youtube/linkedin）结果：仅找到本人LinkedIn档案；Facebook、Instagram、X上均有Banco Unión官方账号发布其就任与出席活动的帖子（2025-12-05就任官宣、2026年Bolivian Business CEO Summit等），但均属企业账号而非本人账号；未发现经证实的本人Facebook/X/Instagram/TikTok/YouTube账号。",
    "name_zh_note": "未检索到可靠既有中文全名译名。中文媒体中仅0xzx（繁体中文加密资讯站，2026-04-30）以姓氏「埃雷拉」指代，不构成标准全名译名，故name_zh置null。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": ["official_website", "government_registry", "news_search", "web_search", "social_media", "other"],
        "quotes": [
            {
                "title": "Directorio y Plantel Ejecutivo - Banco Unión S.A.",
                "url": "https://bancounion.com.bo/GrupoUnion/BUSAPlantelEjecutivo"
            },
            {
                "title": "HECHO RELEVANTE - Banco Unión S.A.（玻利维亚证券交易所重大信息公告，2025-12-05）",
                "url": "https://www.bbv.com.bo/Publicacionv3/View_Publicacion/Detalle_HR1.aspx?Publicacion=651541"
            },
            {
                "title": "Tarjeta de Registro ASFI - Banco de Crédito de Bolivia S.A.（玻利维亚金融体系监管局高管登记卡）",
                "url": "https://appweb.asfi.gob.bo/Reportes_asp/rmi/tarjeta.asp?c=51828&t=2"
            },
            {
                "title": "Banco Unión y fundación alemana fortalecen alianza para impulsar la educación financiera - Correo del Sur (2026-03-30)",
                "url": "https://correodelsur.com/economia/20260330/banco-union-y-fundacion-alemana-fortalecen-alianza-para-impulsar-la-educacion-financiera.html"
            },
            {
                "title": "Ganadores - 11a Edición Premios a Los Innovadores Financieros en Las Américas - Fintech Americas",
                "url": "https://www.fintechamericas.co/premios-innovadores-financieros/ganadores"
            },
            {
                "title": "Jose Vicente Herrera Amenabar - LinkedIn",
                "url": "https://bo.linkedin.com/in/jose-vicente-herrera-amenabar-a7b612196"
            },
            {
                "title": "Bienvenido, José Vicente Herrera Amenabar, Gerente General de Banco Unión S.A. - Facebook Banco Unión (2025-12-05)",
                "url": "https://www.facebook.com/BancoUnionSA/posts/bienvenido-jos%C3%A9-vicente-herrera-amenabar-gerente-general-de-banco-uni%C3%B3n-sa-elban/1268389045319041/"
            }
        ],
        "notes": "核心事实均有官方来源支撑并交叉验证：现任职务见银行官网领导名录；任命经过见玻利维亚证券交易所2025-12-05重大信息公告；BCP任职完整时间线（2022-09入职、2023-07升任、2025-07转任零售银行部、2025-11-28离职）见ASFI高管登记卡（政府登记源）；获奖见Fintech Americas第11届获奖者页（该届颁奖典礼于2026年3月迈阿密举行）。出生日期、出生地、家庭、政见等未检索到公开资料，相应字段留空。存疑事项：中文媒体0xzx（2026-04-30）报道其任内银行Yasta钱包推出USDT相关服务，但原文页无法直取核实，未列入正式条目。姓名在ASFI记录中存在带重音（Amenábar）与不带重音（Amenabar）两种拼写，已将带重音变体列入aliases。"
    }
}

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "persons", "BO-PERSON-000246.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)

print("WROTE:", out_path)
print("bytes:", os.path.getsize(out_path))

# -*- coding: utf-8 -*-
"""Generate BO-PERSON-000250 person profile JSON (Juan Ricardo Mertens Olmos)."""
import json
import os

profile = {
    "person_id": "BO-PERSON-000250",
    "wikidata_qid": None,
    "name_zh": None,
    "name": "Juan Ricardo Mertens Olmos",
    "name_en": "Juan Ricardo Mertens Olmos",
    "aliases": ["Ricardo Mertens", "Ricardo Mertens Olmos"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "birth_date_note": "未查到确切出生日期。多家媒体讣告称其殁年59岁（Red Uno、Actualidad Contenidos，2025-02），个别社交媒体帖称60岁；2014年7月专访自述49岁，据此推断约1964-1965年出生，未获权威来源证实，故 birth_date 留空。",
    "is_deceased": True,
    "death_date": "2025-02-09",
    "death_place": "圣克鲁斯-德拉谢拉 (Santa Cruz de la Sierra)",
    "death_note": "2025-02-03凌晨在帕尔马索拉（Palmasola）监狱突发心脏问题被紧急送医（先送San Juan de Dios医院，后转Las Américas诊所），诊断为两支动脉阻塞、感染性休克（septicemia）、急性心肌梗死并急性肾衰竭；02-04接受心脏手术及两次导管手术并透析，02-09凌晨因多器官衰竭病亡，殁年59岁。02-10遗体在圣克鲁斯Las Misiones灵堂守灵后安葬。系Fassil案同案人员中唯一仍被预防性羁押者。家属律师Carlos Soria称其病症系在狱中进食所致、相关指控从未被证实；其死后案件依法应终结，辩护方并宣布将提起国际诉讼。来源：Opinion、El Deber、Los Tiempos、Correo del Sur（2025-02-09/10）、eju.tv、Vision360（2025-02-10）。",
    "current_positions": [],
    "work_experience": [
        {
            "start_date": None,
            "end_date": "2023-04-26",
            "organization": "法西尔银行 (Banco Fassil)",
            "org_id": "BO-FIN-009",
            "position": "董事长"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "圣克鲁斯金融集团 (Santa Cruz Financial Group)",
            "org_id": None,
            "position": "董事长"
        },
        {
            "start_date": "2009",
            "end_date": "2013",
            "organization": "UPSA基金会 (Fundación UPSA)",
            "org_id": "BO-ACAD-010",
            "position": "董事会主席"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "圣克鲁斯工业、商业、服务业与旅游商会 (CAINCO)",
            "org_id": None,
            "position": "副主席"
        }
    ],
    "work_note": "1）法西尔银行：媒体普遍称其为Fassil创始人/联合创始人（该行前身为1996-08-12设立的私营金融基金FFP Fassil）；2014年7月专访自述其所在圣克鲁斯金融集团于2006年注资Fassil并主导重组，其时已任银行与集团董事长；2014-07-21该行依第393号法转型为综合银行（Banco Múltiple）；鼎盛期（2022-09）资产约46.4亿美元，为玻利维亚最大银行之一。2023-03发生挤兑，2023-04-26被ASFI干预，他于4月末被捕（Opinion称2023-04-27起预防性羁押，El Deber称2023年3月起在押），羁押于Palmasola监狱PC-7（高危险区），系同案唯一在押者；罪名涉及金融犯罪与非法获利洗白（legitimación de ganancias ilícitas），案件2023-09经宪法法院裁定移交拉巴斯审理；曾拒绝检方「认罪换三年刑期」的简化程序，坚持开庭自证清白。2）圣克鲁斯金融集团：董事长，并任Financial Group S.A.法定代表；OAS案件档案及媒体报道称检方指控其通过该公司转移逾1300万美元资金并曾向第三方转移财产以隐匿所得（均系指控）。3）UPSA基金会：任职年份以UPSA官网权威名录为准。4）CAINCO副主席：CAINCO官方Instagram/Facebook讣告帖确认，具体任期不详。",
    "education": [],
    "education_note": "仅知其职业为经济学家（economista，2014年专访PERFIL栏及多家讣告均提及），就读院校、学位与毕业年份均查无可靠来源，故不编造条目。",
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000251",
            "person_name": "卡洛斯·阿尔贝托·科洛德罗·洛佩斯 (Carlos Alberto Colodro López)",
            "relationship_type": "colleague",
            "description": "2023-04-26 Fassil被ASFI干预后受任为银行干预人（interventor），接替Mertens的管理层并主持资产与存贷款分配；同年5月27日自圣克鲁斯Ambassador商务中心15楼坠亡。"
        },
        {
            "person_id": None,
            "person_name": "埃尔南·苏亚雷斯·瓦卡·迪斯 (Hernán Suárez Vaca Diez)",
            "relationship_type": "colleague",
            "description": "Fassil高管（副职管理层），2023年4月25日夜间与Mertens一同被FELCC签发逮捕令拘捕（同批被捕的还有Hermes Hugo Saucedo Camacho）。"
        },
        {
            "person_id": None,
            "person_name": "埃尔梅斯·乌戈·绍塞多·卡马乔 (Hermes Hugo Saucedo Camacho)",
            "relationship_type": "colleague",
            "description": "Fassil高管，2023年4月25日夜间与Mertens同批被FELCC逮捕令通缉，次日晨自首。"
        },
        {
            "person_id": None,
            "person_name": "马里亚诺·梅迪纳 (Mariano Medina)",
            "relationship_type": "associate",
            "description": "Mertens的辩护律师，多次对外通报其健康状况、为其申请法医评估，并在其死后向拉巴斯法院提交死亡证明申请诉讼终结；透露检方曾多次提出三年刑期的简化程序被其委托人拒绝。"
        }
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Juan Ricardo Mertens Olmos",
            "url": "https://bo.linkedin.com/in/juan-ricardo-mertens-olmos-84899523",
            "source": "LinkedIn搜索结果（姓名与「董事长/玻利维亚」信息吻合）"
        },
        {
            "platform": "linkedin",
            "account_name": "Ricardo Mertens Olmos",
            "url": "https://bo.linkedin.com/in/ricardo-mertens-olmos-6252a19",
            "source": "LinkedIn搜索结果（职务标注Santa Cruz de la Sierra Financial Group S.A.董事长，与本人吻合）"
        }
    ],
    "social_accounts_note": "6项社交媒体扫描结果：LinkedIn发现上述2个个人档案；Facebook、X/Twitter、Instagram、TikTok、YouTube 均未发现可确证为本人所有的账号（各平台大量相关内容均为UNITEL、El Deber、La Razón、Abya Yala等媒体账号发布的报道）。",
    "family_members": [
        {
            "person_id": None,
            "name": "洛雷娜·伊瓦涅斯 (Lorena Ibáñez)",
            "relationship": "spouse",
            "industry_or_organization": None
        }
    ],
    "family_note": "配偶Lorena Ibáñez及四名子女的信息来自2014年7月Consultorio Económico专访的PROFILE栏（「CASADO CON LORENA IBÁÑEZ, CUATRO HIJOS」），子女未具名，故不设条目。法西尔银行董事名册中的替补董事Kathya Lorena Mertens Ibáñez姓氏组合（父姓Mertens+母姓Ibáñez）与其家庭结构吻合，疑为其女儿，但无直接来源证实，未列入family_members。2025-02-10遗体在圣克鲁斯Las Misiones灵堂守灵，家属亲友到场。",
    "political_stances": [
        {
            "date": "2014-07-24",
            "topic": "政府利率管制政策（金融服务法与监管利率最高限令）",
            "stance_content": "在Fassil转型综合银行仪式上公开质疑政府利率管制的可持续性，称「很少有机构能跟上政府所寻求的目标」：监管利率低于通胀，只有能够自我革新的机构才能存续，部分机构将被迫结盟、被出售或合并；同时表示Fassil愿开展联盟、并购，目标是「不做最大的银行，而做最好的银行」。",
            "source": "IBCE Data Trade转载新闻报道（2014-07-24）"
        },
        {
            "date": "2021",
            "topic": "金融监管与银行清偿力（ASFI对Fassil的调查）",
            "stance_content": "ASFI应议员请求就Fassil对「新圣克鲁斯」（Nueva Santa Cruz）地产项目融资启动调查、舆论质疑其扩张时，作为银行总裁公开为银行辩护，呼吁不要怀疑金融体系的清偿能力，并代表圣克鲁斯金融集团起诉ASFI负责人雷纳尔多·尤赫拉（Reynaldo Yujra）涉嫌泄露该行机密信息。",
            "source": "Wikipedia（西语）Banco Fassil 条目"
        }
    ],
    "major_achievements": [
        {
            "date": "1996",
            "achievement": "作为创始团队核心参与创立法西尔私营金融基金（Fondo Financiero Privado Fassil），多家媒体称其为该行创始人；该机构日后发展为玻利维亚最大银行之一。",
            "organization": "法西尔银行 (Banco Fassil)"
        },
        {
            "date": "2006",
            "achievement": "通过圣克鲁斯金融集团对Fassil注资并主导深度重组，2006至2014年银行资产由1520万美元增至8.623亿美元（增长57倍），使其跻身玻利维亚商业银行第七大、净资产第五大机构（2014年数据）。",
            "organization": "圣克鲁斯金融集团 (Santa Cruz Financial Group)"
        },
        {
            "date": "2014-07-21",
            "achievement": "推动FFP Fassil依《金融服务法》（第393号法）转型为综合银行（Banco Múltiple）并正式更名法西尔银行，任首任董事长。",
            "organization": "法西尔银行 (Banco Fassil)"
        },
        {
            "date": "2022-09",
            "achievement": "其执掌下的法西尔银行资产规模达约46.4亿美元，跻身玻利维亚银行业前列（维基百科引述数据）。",
            "organization": "法西尔银行 (Banco Fassil)"
        },
        {
            "date": "2009",
            "achievement": "出任圣克鲁斯私立大学UPSA基金会董事会主席（2009-2013），主持基金会发展与成长。",
            "organization": "UPSA基金会 (Fundación UPSA)"
        }
    ],
    "biography_summary": "胡安·里卡多·梅尔滕斯·奥尔莫斯（Juan Ricardo Mertens Olmos，约1964/1965年生）是玻利维亚银行家、经济学家，圣克鲁斯企业界代表人物，生前为法西尔银行（Banco Fassil）主要股东兼董事长、圣克鲁斯金融集团（Santa Cruz Financial Group）董事长。Fassil前身为1996年设立的私营金融基金，2006年经其主导的集团注资重组后高速扩张，2014年7月转型为综合银行，鼎盛时期资产约46.4亿美元（2022年9月），为玻利维亚最大银行之一。2023年3月该行爆发挤兑，4月26日被金融体系监管局（ASFI）干预，他于4月末被捕，在帕尔马索拉（Palmasola）监狱PC-7区候审，因金融犯罪及非法获利洗白指控成为同案唯一被预防性羁押者，曾拒绝检方三年刑期的认罪协商、坚持自证清白。他亦曾任圣克鲁斯工业、商业、服务业与旅游商会（CAINCO）副主席及UPSA基金会董事会主席（2009-2013）。2025年2月3日他在狱中心脏骤停送医，2月9日凌晨因感染性休克并多器官衰竭在圣克鲁斯Las Américas诊所病亡，殁年59岁，次日安葬。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "news_search",
            "web_search",
            "wikipedia",
            "official_website",
            "social_media"
        ],
        "notes": "数据确认情况：死亡日期/地点/死因、ASFI干预、被捕与羁押、拒绝认罪协商等关键事实经Opinion、El Deber（两篇）、Los Tiempos、Correo del Sur、Wikipedia（西语）等多个独立来源全文交叉验证；UPSA基金会任职经UPSA官网直接确认；CAINCO副主席来自CAINCO官方账号讣告帖（单一来源，已注明）；2014年转型与业绩数据经Consultorio Económico专访与IBCE转载报道双源确认。存疑字段：出生日期未获权威记录（殁年59岁为多数来源，个别帖称60岁），birth_date留空；教育机构与学位查无，education留空；name_zh经西/英/中三语及Wikidata检索未发现既有标准中文译名，置null；本人无Wikidata条目，wikidata_qid置null；董事名册中Kathya Lorena Mertens Ibáñez疑为其女但未证实，仅记于family_note；无公开个人联系方式，contacts留空。羁押起点存在2023-03与2023-04两种表述（El Deber vs Opinion/Reuters），采用多数来源的2023年4月末。completeness_score未达85的原因：评分所涉出生日期/出生地/中文名、教育经历、个人联系方式、Wikidata条目及更多社媒账号经多轮检索确无可靠公开来源，依「禁止编造」铁律留空。",
        "quotes": [
            {
                "title": "Murió Ricardo Mertens, expresidente del Banco Fassil; desde Palmasola, buscó 'demostrar inocencia' (Opinion)",
                "url": "https://www.opinion.com.bo/pais/murio-ricardo-mertens-expresidente-banco-fassil-palmasola-busco-demostrar-inocencia/20250209104543966601.html"
            },
            {
                "title": "La extinción de cargos de Mertens depende de La Paz y el caso Fassil sigue abierto (El Deber)",
                "url": "https://eldeber.com.bo/santa-cruz/la-extincion-de-cargos-de-mertens-depende-de-la-paz-y-el-caso-fassil-sigue-abierto_503249/"
            },
            {
                "title": "Fallece Ricardo Mertens, expresidente del banco Fassil, tras complicaciones de salud en Santa Cruz (Los Tiempos)",
                "url": "https://www.lostiempos.com/actualidad/pais/20250209/fallece-ricardo-mertens-expresidente-del-banco-fassil-complicaciones-salud"
            },
            {
                "title": "Fallece el expresidente y socio del Banco Fassil (Correo del Sur)",
                "url": "https://correodelsur.com/seguridad/20250210/fallece-el-expresidente-y-socio-del-banco-fassil.html"
            },
            {
                "title": "Fallece el expresidente del Banco Fassil, Ricardo Mertens (El Deber)",
                "url": "https://eldeber.com.bo/pais/fallece-el-expresidente-del-banco-fassil-ricardo-mertens_503001/"
            },
            {
                "title": "Banco Fassil - Wikipedia, la enciclopedia libre",
                "url": "https://es.wikipedia.org/wiki/Banco_Fassil"
            },
            {
                "title": "Ricardo Mertens Olmos. Es el presidente del directorio del nuevo Banco Fassil y accionista de Santa Cruz Financial Group (Consultorio Económico, 2014)",
                "url": "https://consultorioeconomico.blogspot.com/2014/07/ricardo-mertens-olmos-es-el-presidente.html"
            },
            {
                "title": "FALLECE RICARDO MERTENS EXPRESIDENTE DEL BANCO FASSIL (Actualidad Contenidos / Red Uno)",
                "url": "https://actualidadcontenidos.com.bo/fallece-ricardo-mertens-expresidente-del-banco-fassil/"
            },
            {
                "title": "Nuestras autoridades presidentes y rectores - UPSA (Fundación UPSA directivos)",
                "url": "https://www.upsa.edu.bo/somos-upsa/presidentes-y-rectores/"
            },
            {
                "title": "Bolivia takes control of Banco Fassil, executives arrested (Reuters)",
                "url": "https://www.reuters.com/business/finance/bolivia-takes-control-banco-fassil-executives-arrested-2023-04-27/"
            },
            {
                "title": "Mertens: pocas entidades podrán lograr lo que el Gobierno busca (IBCE Data Trade, 2014-07-24)",
                "url": "https://ibce.org.bo/principales-noticias-bolivia/noticias-nacionales-detalle.php?id=44610&idPeriodico=7&fecha=2014-07-24"
            },
            {
                "title": "Fallecido Mertens, expresidente del Banco Fassil, ¿qué pasará con el proceso en su contra? (eju.tv)",
                "url": "https://eju.tv/2025/02/fallecido-mertens-expresidente-del-banco-fassil-que-pasara-con-el-proceso-en-su-contra/"
            }
        ]
    }
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000250.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("Written:", out_path)
print("biography_summary length:", len(profile["biography_summary"]))

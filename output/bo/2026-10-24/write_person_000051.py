# -*- coding: utf-8 -*-
"""Build BO-PERSON-000051 (Juan Carlos Pimentel Castillo) person profile JSON."""
import json
import os

OUT_DIR = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons"
OUT_PATH = os.path.join(OUT_DIR, "BO-PERSON-000051.json")

profile = {
    "person_id": "BO-PERSON-000051",
    "wikidata_qid": None,
    "name": "Juan Carlos Pimentel Castillo",
    "name_en": "Juan Carlos Pimentel",
    "name_zh": "胡安·卡洛斯·皮门特尔",
    "aliases": ["Juan Carlos Pimentel Castillo", "Juan Carlos Pimentel"],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "birth_note": "公开报道未见其出生日期与出生地。其兄何塞·安东尼奥·皮门特尔·卡斯蒂略1949年生于波托西Catavi，但无资料可证实本人的出生信息，不作外推。",
    "current_positions": [],
    "position_note": "2025年11月13日就任教育部正规教育副部长；2026年8月14-15日提交「不可撤回」辞呈并于8月15日获部长里卡多·埃里克·圣希内斯·查韦斯接受；2026年8月25日由卢斯·希门尼斯·克伊斯佩（Luz Jiménez Quispe）接任。截至采集日（2026-10-25）已无在任公职，故current_positions留空。",
    "contacts": [],
    "education": [],
    "education_note": "教育部官方履历称其为「maestro de formación y pedagogo」（师范出身的教育学专家），但毕业院校、学位与年份均未见于公开资料，education按规则留空。",
    "work_experience": [
        {
            "start_date": "1996-01-24",
            "end_date": "1997-08-06",
            "organization": "玻利维亚国家教育秘书处 (Secretaría Nacional de Educación)",
            "org_id": None,
            "position": "国家教育秘书（部长级）",
            "description": "在总统冈萨洛·桑切斯·德洛萨达（Goni）第一政府中主管全国教育事务。ANF1996年2月5日报道以其「Secretario Nacional de Educación」身份介绍1996学年与教育改革实施安排；西班牙文维基百科教育部大臣一览表列其任期为1996年1月24日至1997年8月6日（1年6个月13天）。",
            "source": "https://es.wikipedia.org/wiki/Ministerio_de_Educaci%C3%B3n_(Bolivia)"
        },
        {
            "start_date": "2025-11-13",
            "end_date": "2026-08-15",
            "organization": "玻利维亚教育部 (Ministerio de Educación)",
            "org_id": "BO-GOV-008",
            "position": "正规教育副部长",
            "description": "由教育部长贝亚特里斯·加西亚·德·阿查在罗德里戈·帕斯政府中任命（2025-11-13就职）；负责规划2026学年、遏制教育质量恶化。2026年6月10日圣希内斯接任部长后仍任原职；2026年8月中旬因课程改革推进方式的分歧提交「不可撤回」辞呈，8月15日辞呈获接受，8月25日由卢斯·希门尼斯·克伊斯佩接任。",
            "source": "https://www.minedu.gob.bo/index.php?option=com_content&view=article&id=8203:ministra-de-educacion-fortalece-su-equipo-con-tres-nuevos-viceministros&catid=182&Itemid=854"
        }
    ],
    "work_note": "教育部官方履历及其它报道描述其为教师、教育学专家并曾任教师工会（gremio de maestros）代表，具体任教机构与年份未公开。另据玻利维亚教育研究与行动中心（CEBIAE）官方Facebook2026年4月对其专访，其曾有在CEBIAE工作的经历（职务与起止时间不详），因职务不详未单列work_experience条目。La Prensa/Erbol（2025-11-13）亦确认其曾在Goni政府中任职。",
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000049",
            "person_name": "里卡多·埃里克·圣希内斯·查韦斯 (Ricardo Erick Sanjinés Chávez)",
            "relationship_type": "superior",
            "description": "2026年6月10日接替加西亚出任教育部长，成为其直属上级；2026年8月15日接受其辞呈，并称「理念分歧是任何转型过程的一部分」，同时批准教育课程改革继续推进。"
        },
        {
            "person_id": "BO-PERSON-000559",
            "person_name": "贝亚特里斯·加西亚·德·阿查 (Beatriz García de Achá)",
            "relationship_type": "superior",
            "description": "2025年11月9日至2026年6月2日任教育部长；2025年11月13日主持其正规教育副部长就职仪式并对其评价甚高。"
        },
        {
            "person_id": "BO-PERSON-000001",
            "person_name": "罗德里戈·帕斯·佩雷拉 (Rodrigo Paz Pereira)",
            "relationship_type": "superior",
            "description": "玻利维亚总统（2025年11月就任）。其所组教育部门班子（先后任部长的加西亚与圣希内斯）分别主持了其就职与辞职程序。"
        },
        {
            "person_id": None,
            "person_name": "埃德加·卡迪马·加尔松 (Édgar Cadima Garzón)",
            "relationship_type": "colleague",
            "description": "教育部中等教育总局局长，与其共事；2026年8月15日两人同日辞职获接受。卡迪马在辞函中公开批评沿用MAS时期课程大纲，称仅靠数学、语文两科补强及Puente、Starlink、Avanza+等修补性项目无法解决学习危机；媒体报道此次辞职事件暴露了教育部内部在课程改革上的分歧。"
        },
        {
            "person_id": "BO-PERSON-000052",
            "person_name": "安娜·卡德纳斯·安古洛 (Ana Cárdenas Angulo)",
            "relationship_type": "colleague",
            "description": "2025年11月13日与其同日就职的高等教育副部长，同属教育部副部长班子。"
        },
        {
            "person_id": "BO-PERSON-000560",
            "person_name": "卢斯·希门尼斯·克伊斯佩 (Luz Jiménez Quispe)",
            "relationship_type": "other",
            "description": "其继任者：2026年8月25日由教育部长圣希内斯任命为正规教育副部长，接替其空出的职位。"
        }
    ],
    "social_accounts": [],
    "social_accounts_note": "2026-10-25对facebook、x/twitter、linkedin、instagram、tiktok、youtube六个平台进行检索扫描，未发现可核实归属其本人的社交账号；其公开活动影像与发言均经媒体机构账号（Unitel、La Razón、RTP、El Deber、ANF等）或教育部官方账号发布。",
    "family_members": [
        {
            "person_id": None,
            "name": "何塞·安东尼奥·皮门特尔·卡斯蒂略 (José Antonio Pimentel Castillo)",
            "relationship": "brother",
            "industry_or_organization": "玻利维亚国营矿业公司 (COMIBOL)；曾任玻利维亚矿业冶金部",
            "description": "胞兄。原为矿工工会领导人，MAS籍众议员（2006-2010，波托西）、矿业冶金部长（2010-2012），2017年1月出任玻利维亚国营矿业公司（COMIBOL）总裁；1949年生于波托西Catavi。",
            "source": "La Prensa/Erbol 2025-11-13（兄弟关系）；es.wikipedia José Pimentel（全名与履历）"
        }
    ],
    "family_note": "兄弟关系由La Prensa与Erbol（引ANF稿）2025年11月13日报道交叉确认（「hermano de José Pimentel, expresidente de Comibol en la gestión de Evo Morales」）；其兄全名与详细履历据西班牙文维基百科José Pimentel条目。",
    "political_stances": [
        {
            "date": "2025-11-13",
            "topic": "2026学年与教育质量",
            "stance_content": "就任副部长时表示，国家面临经济危机带来的重大挑战，工作重点是规划2026学年，使其成为遏制教育质量持续恶化的起点；主张恢复教育部的专业属性、提升技术人员素质；称「我们不是来摧毁的，而是要在既有基础上建设和前进」，「愿这一任期能为国家教育带来成功」。",
            "source": "https://www.minedu.gob.bo/index.php?option=com_content&view=article&id=8203:ministra-de-educacion-fortalece-su-equipo-con-tres-nuevos-viceministros&catid=182&Itemid=854"
        },
        {
            "date": "2025-11-18",
            "topic": "教育改革与对话机制",
            "stance_content": "宣布教育部将开启广泛对话进程，推动教育体系与全球科技和科学发展接轨的改革；称「如果系统的基础一切照旧，仅宣称『教育将会怎样』是不够的」，国家需要的是真实转型而非意向声明；已启动与城市及农村教师工会联合会的会谈，并将扩大至玻利维亚私立学校协会（Andecop）等表达参与意愿的部门。",
            "source": "https://historico.abi.bo/index.php/component/content/article/37-notas/noticias/sociedad/70997-viceministro-pimentel-anuncia-apertura-total-al-dialogo-para-construir-un-sistema-educativo-acorde-a-los-avances-cientificos?Itemid=101"
        },
        {
            "date": "2026-06-22",
            "topic": "线下复课与远程教学",
            "stance_content": "在全国道路封锁与社会冲突期间学校普遍转为虚拟授课后，指示全国正规教育系统自6月23日起恢复线下教学（对师生到校时间给予弹性）；称虚拟课堂「完全低效」，因为国内不具备技术条件、行政部门也无能力监督其开展；并承认此前一个月教学进度「很糟」，需要加快学习恢复进程。",
            "source": "https://eju.tv/2026/06/educacion-instruye-retorno-a-las-clases-presenciales-a-partir-de-este-martes/"
        },
        {
            "date": "2026-06-23",
            "topic": "Starlink卫星互联网进校园",
            "stance_content": "针对为偏远学校接入星链（Starlink）卫星互联网以支撑远程教学的方案表示「星链解决不了问题」，认为在国内基础条件下依赖卫星互联网开展虚拟教学并不可行。",
            "source": "https://www.facebook.com/rtpbolivia/posts/rtpinformastarlink-no-resolver%C3%A1-el-problema-afirma-el-viceministro-de-educaci%C3%B3n-/1360181276310168/"
        }
    ],
    "major_achievements": [
        {
            "date": "1996-01-24",
            "organization": "玻利维亚国家教育秘书处 (Secretaría Nacional de Educación)",
            "achievement": "被桑切斯·德洛萨达政府任命为国家教育秘书（部长级，西班牙文维基百科教育部大臣表列任期1996-01-24至1997-08-06），主管全国教育；任内负责1996学年开学组织与教育改革（Reforma Educativa）实施，宣布向332个教育核心区投放教学模块和教师指导材料，并处理与教师工会的谈判。"
        },
        {
            "date": "2025-11-18",
            "organization": "玻利维亚教育部 (Ministerio de Educación)",
            "achievement": "上任一周内启动与城市及农村教师工会联合会、私立学校协会（Andecop）等部门的广泛教育对话进程，为教育体系与课程更新凝聚共识。"
        },
        {
            "date": "2026-06-22",
            "organization": "玻利维亚教育部 (Ministerio de Educación)",
            "achievement": "在全国道路封锁与社会冲突致学校转入虚拟授课后，决策并部署全国正规教育系统于6月23日恢复线下教学。"
        }
    ],
    "biography_summary": "胡安·卡洛斯·皮门特尔·卡斯蒂略（Juan Carlos Pimentel Castillo），玻利维亚资深教育家。师范出身的教育学专家（maestro de formación y pedagogo），长期执教并曾任教师工会代表，亦曾在玻利维亚教育研究与行动中心（CEBIAE）工作。1996年1月24日，他在冈萨洛·桑切斯·德洛萨达（Goni）第一政府中被任命为国家教育秘书（部长级），主管全国教育至1997年8月，任内负责教育改革实施，包括向332个教育核心区投放教学模块与教师指导材料。2025年11月13日，他在罗德里戈·帕斯政府中被教育部长贝亚特里斯·加西亚·德·阿查任命为教育部正规教育副部长，负责规划2026学年、遏制教育质量恶化，并启动与教师工会及私立教育部门的对话。2026年6月，他在全国道路封锁导致学校转为远程授课后主导恢复线下教学，称虚拟课堂「完全低效」。2026年8月中旬，因与继任部长里卡多·圣希内斯在课程改革推进方式上的分歧，他提交「不可撤回」辞呈，8月15日获接受，8月25日由卢斯·希门尼斯·克伊斯佩接任。其兄何塞·安东尼奥·皮门特尔·卡斯蒂略曾在莫拉莱斯政府任矿业冶金部长及玻利维亚矿业公司（COMIBOL）总裁。",
    "profile": {
        "source_url": "https://www.minedu.gob.bo/images/noticias/2025/POSESION_2.jpeg",
        "local_path": None
    },
    "profile_note": "教育部官网2025年11月13日三位新任副部长就职仪式照片（合影，含本人在任画面），未单独裁切个人头像。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "wikipedia",
            "news_search",
            "web_search",
            "social_media"
        ],
        "notes": "2026-10-25完成多语种（西语为主）检索，全文精读13个独立来源：教育部官网任命与辞职公告（2篇）、La Prensa/Erbol/Opinión任命报道（含Goni政府任职、兄弟关系）、ANF/Noticias Fides 1996年档案（国家教育秘书身份）、西班牙文维基百科教育部大臣表（1996-1997任期）及José Pimentel条目、El Deber/El Día辞职报道（课程分歧背景）、eju.tv（复课与虚拟教学表态）、ABI（对话改革）、minedu继任者公告。关键事实（1996-1997任职、2025-11-13任命、2026-08-15辞职获接受、兄弟关系）均有≥2独立来源。未发现：出生日期/地点、学历院校、个人社交账号、维基数据条目、个人联系方式，相应字段留空。本人无中文媒体译名可考，沿用既有译名「胡安·卡洛斯·皮门特尔」。注意：任务背景所称「现任副部长」已过时，其已于2026年8月卸任（详见position_note）。completeness_score说明：得分为56分（--score实测），低于70的期望值，原因在于评分模型中birth_date/birth_place、education（院校）、social_accounts、contacts等结构性字段因公开资料中客观不存在而无法填写（各占较大权重），而非检索遗漏；已填写的内容性字段（work_experience、political_stances、person_relationships、major_achievements、family_members、biography_summary）均有可靠来源支撑，其中工作履历、立场、成就已达或接近该类别计分上限。遵循「禁止编造」铁律，不以推测性条目凑分。",
        "quotes": [
            {
                "title": "Ministra de Educación fortalece su equipo con tres nuevos viceministros (Ministerio de Educación, 2025-11-13)",
                "url": "https://www.minedu.gob.bo/index.php?option=com_content&view=article&id=8203:ministra-de-educacion-fortalece-su-equipo-con-tres-nuevos-viceministros&catid=182&Itemid=854"
            },
            {
                "title": "Posesionan a nuevos viceministros de Educación; Juan Carlos Pimentel fue funcionario de Goni (La Prensa, 2025-11-13)",
                "url": "https://laprensa.bo/posesionan-nuevos-viceministros-de-educacion-juan-carlos-pimentel-fue-funcionario-de-goni"
            },
            {
                "title": "Posesionan a nuevos viceministros de Educación, uno de ellos fue funcionario de Goni (Erbol, 2025-11-13)",
                "url": "https://erbol.com.bo/gente/posesionan-nuevos-viceministros-de-educaci%C3%B3n-uno-de-ellos-fue-funcionario-de-goni"
            },
            {
                "title": "Posesionan a nuevos viceministros de Educación (Opinión, 2025-11-13)",
                "url": "https://www.opinion.com.bo/pais/posesionan-nuevos-viceministros-educacion/20251113192035983543.html"
            },
            {
                "title": "Gobierno espera que año escolar 1996 sea un éxito (ANF/Noticias Fides, 1996-02-05)",
                "url": "https://www.noticiasfides.com/nacional/sociedad/anf-el-secretario-nacional-de-educacion-juan-carlos-251072"
            },
            {
                "title": "Ministerio de Educación (Bolivia) - Wikipedia en español（教育部大臣一览表）",
                "url": "https://es.wikipedia.org/wiki/Ministerio_de_Educaci%C3%B3n_(Bolivia)"
            },
            {
                "title": "Ministro de Educación acepta renuncias y anunciará en breve nuevos profesionales (Ministerio de Educación, 2026-08-15)",
                "url": "https://www.minedu.gob.bo/index.php?option=com_content&view=article&id=8436:ministro-edu-acepta-renuncias&catid=182:noticias&Itemid=854"
            },
            {
                "title": "Renuncia de dos autoridades de Educación expone diferencias en cambio de malla curricular (El Deber, 2026-08-15)",
                "url": "https://eldeber.com.bo/pais/renuncia-dos-autoridades-educacion-expone-diferencias-cambio-malla-curricular_1786796831"
            },
            {
                "title": "Educación: renuncian el viceministro de Educación Regular y el director de Secundaria (El Día/Unitel, 2026-08-15)",
                "url": "https://www.eldia.com.bo/2026-08-15/politica/educacion-renuncian-el-viceministro-de-educacion-regular-y-el-director-de-secundaria.html"
            },
            {
                "title": "Educación instruye retorno a las clases presenciales a partir de este martes (eju.tv, 2026-06-22)",
                "url": "https://eju.tv/2026/06/educacion-instruye-retorno-a-las-clases-presenciales-a-partir-de-este-martes/"
            },
            {
                "title": "Viceministro Pimentel anuncia apertura total al diálogo para construir un sistema educativo acorde a los avances científicos (ABI, 2025-11-18)",
                "url": "https://historico.abi.bo/index.php/component/content/article/37-notas/noticias/sociedad/70997-viceministro-pimentel-anuncia-apertura-total-al-dialogo-para-construir-un-sistema-educativo-acorde-a-los-avances-cientificos?Itemid=101"
            },
            {
                "title": "Ministro de Educación posesiona a Luz Jiménez como nueva Viceministra de Educación Regular (Ministerio de Educación, 2026-08-25)",
                "url": "https://www.minedu.gob.bo/index.php?option=com_content&view=article&id=8443:min-edu-posesion-nueva-vicemin-educ-reg&catid=182:noticias&Itemid=854"
            },
            {
                "title": "#RTPInforma \"Starlink no resolverá el problema\", afirma el viceministro de Educación Juan Carlos Pimentel (RTP Facebook, 2026-06-23)",
                "url": "https://www.facebook.com/rtpbolivia/posts/rtpinformastarlink-no-resolver%C3%A1-el-problema-afirma-el-viceministro-de-educaci%C3%B3n-/1360181276310168/"
            },
            {
                "title": "José Pimentel - Wikipedia en español（胞兄履历）",
                "url": "https://es.wikipedia.org/wiki/Jos%C3%A9_Pimentel"
            }
        ]
    }
}

os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)

# quick self-checks
print("written:", OUT_PATH)
print("bio_len:", len(profile["biography_summary"]))
print("quotes:", len(profile["collection_meta"]["quotes"]))
print("work:", len(profile["work_experience"]), "stances:", len(profile["political_stances"]),
      "rels:", len(profile["person_relationships"]), "achv:", len(profile["major_achievements"]),
      "family:", len(profile["family_members"]), "edu:", len(profile["education"]),
      "social:", len(profile["social_accounts"]), "contacts:", len(profile["contacts"]))

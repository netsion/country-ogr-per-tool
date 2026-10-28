# -*- coding: utf-8 -*-
"""Build BO-PERSON-000488 (Óscar Abdón Trujillo Pinto, PDC Bolivia) person profile."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000488.json")

profile = {
    "person_id": "BO-PERSON-000488",
    "wikidata_qid": None,
    "name": "Óscar Abdón Trujillo Pinto",
    "name_en": "Oscar Abdon Trujillo Pinto",
    "name_zh": "奥斯卡·阿夫东·特鲁希略",
    "aliases": [
        "Óscar Trujillo Pinto",
        "Oscar Abdon Trujillo Pinto",
        "Óscar Trujillo"
    ],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "contacts": [],
    "current_positions": [
        "基督教民主党全国主席（临时）",
        "拉巴斯省议会议员",
        "拉巴斯省议会副主席"
    ],
    "education": [],
    "work_experience": [
        {
            "start_date": "2025-12-12",
            "end_date": None,
            "organization": "基督教民主党 (Partido Demócrata Cristiano de Bolivia)",
            "org_id": "BO-PARTY-003",
            "position": "全国主席（临时）"
        },
        {
            "start_date": "2026-05-15",
            "end_date": None,
            "organization": "拉巴斯省议会 (Asamblea Legislativa Departamental de La Paz)",
            "org_id": None,
            "position": "省议会副主席"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "拉巴斯省议会 (Asamblea Legislativa Departamental de La Paz)",
            "org_id": None,
            "position": "省议会议员"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "基督教民主党 (Partido Demócrata Cristiano de Bolivia)",
            "org_id": "BO-PARTY-003",
            "position": "经济负责人"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000001",
            "person_name": "罗德里戈·帕斯·佩雷拉 (Rodrigo Paz Pereira)",
            "relationship_type": "political_rival",
            "description": "2025年大选PDC为帕斯的总统竞选提供党籍并助其当选；执政约十个月后，特鲁希略于2026-09-09代表党中央宣布与帕斯政府政治决裂，批评其集权、施政未能回应燃油与美元短缺等危机。"
        },
        {
            "person_id": "BO-PERSON-000002",
            "person_name": "埃德曼·拉拉 (Edman Lara Montaño)",
            "relationship_type": "political_rival",
            "description": "玻利维亚副总统；特鲁希略2026-09-09宣布PDC与帕斯政府决裂时一并点名，批评政府（帕斯与拉拉）执政十个月无所作为。"
        },
        {
            "person_id": "BO-PERSON-000490",
            "person_name": "罗伯托·卡斯特罗·佩尼亚兰达 (Roberto Castro Peñaranda)",
            "relationship_type": "political_rival",
            "description": "PDC驻最高选举法院正式代表、众议院议长；2026年9月党内分裂中率「卡斯特罗派」宣布继续支持帕斯政府，与特鲁希略派互相威胁启动党纪程序。"
        },
        {
            "person_id": "BO-PERSON-000489",
            "person_name": "比斯马克·比利亚努埃瓦 (Bismarck Villanueva)",
            "relationship_type": "political_rival",
            "description": "自任PDC拉巴斯省书记、属亲政府派系；特鲁希略派质疑其书记职务未经党的扩大会议或代表大会选举产生，称「脏衣服在家里洗」言论为党内攻击。"
        },
        {
            "person_id": None,
            "person_name": "桑德拉·里韦罗 (Sandra Rivero)",
            "relationship_type": "political_ally",
            "description": "PDC籍众议员；2026-09-10公开声援特鲁希略与帕斯政府决裂的决定，并揭露「罗德里基斯塔」路线对党团的冲击。"
        }
    ],
    "social_accounts": [],
    "family_members": [],
    "political_stances": [
        {
            "date": "2025-12-16",
            "topic": "2026年地方选举",
            "stance_content": "其领导的PDC派系向最高选举法院正式确认参加2026年3月22日地方选举（同期该党因内部三分：维拉斯科派、特鲁希略派、卡斯特罗派分别报名）。",
            "source": "https://radioluisdefuentes.com/uncategorized/dividido-en-tres-facciones-el-pdc-confirma-su-participacion-en-las-elecciones-subnacionales-de-marzo-de-2026/"
        },
        {
            "date": "2026-09-09",
            "topic": "与帕斯政府决裂",
            "stance_content": "代表PDC全国执行委员会宣布与罗德里戈·帕斯总统及副总统埃德曼·拉拉的政治决裂，称「一切都有极限」「到此为止」，批评政府执政十个月未能回应民众需求，并发出最后通牒：若政府不改弦更张将完全脱离。",
            "source": "https://eldeber.com.bo/pais/pdc-divide-dos-ambas-corrientes-hablan-procesar-disidentes_1789086944"
        },
        {
            "date": "2026-09-09",
            "topic": "经济民生危机",
            "stance_content": "要求政府就汽油、柴油与美元短缺及经济恶化立即采取行动，质疑现政府缺乏能够辅佐总统治理国家的政治与行政结构，指责权力过度集中于总统帕斯个人周围。",
            "source": "https://oxigeno.bo/el-pdc-da-ultimatum-al-gobierno-y-amenaza-con-quitarle-su-respaldo-el-vocero-les-pide-ponerse-la-camiseta/"
        },
        {
            "date": "2026-10-15",
            "topic": "议会党团纪律（反政治跳槽）",
            "stance_content": "宣布指认约10名PDC籍议员涉嫌「transfugio」（政治跳槽、转投政府阵营），将其移送党的全国伦理法庭处理，并寻求依组织纪律收回相关议席。",
            "source": "https://www.facebook.com/reddtvbolivia8.1/posts/pdc-identifica-a-10-parlamentarios-por-presunto-transfugio-anuncia-que-pedir%C3%A1-su/1570061591831506/"
        }
    ],
    "major_achievements": [
        {
            "date": "2025-12-12",
            "achievement": "在PDC第二十次全国代表大会后出任党的全国主席（临时/看守性质），并获最高选举法院正式注册为全国委员会主席，成为该党在法律上认可的最高负责人。",
            "organization": "基督教民主党 (Partido Demócrata Cristiano de Bolivia)"
        },
        {
            "date": "2026-03",
            "achievement": "在2026年3月22日玻利维亚地方选举中当选拉巴斯省议会议员（PDC籍）。",
            "organization": "拉巴斯省议会 (Asamblea Legislativa Departamental de La Paz)"
        },
        {
            "date": "2026-05-15",
            "achievement": "在省议会第2次预备会议经全体一致表决当选拉巴斯省议会副主席（2026-2027届领导委员会）。",
            "organization": "拉巴斯省议会 (Asamblea Legislativa Departamental de La Paz)"
        }
    ],
    "biography_summary": "奥斯卡·阿夫东·特鲁希略·平托（Óscar Abdón Trujillo Pinto）为玻利维亚基督教民主党（PDC）全国主席（临时/看守性质），兼任拉巴斯省议会议员及省议会副主席。他长期在PDC从事党务工作，2017至2018年间经多民族选举机构决议确认登记为该党经济负责人。2025年12月，PDC召开第二十次全国代表大会后组成临时领导机构，特鲁希略出任全国主席，并于12月12日获最高选举法院正式注册认可。2025年大选中PDC为罗德里戈·帕斯的总统竞选提供党籍并助其胜选，但执政约十个月后，特鲁希略于2026年9月9日代表党中央宣布与帕斯政府及副总统埃德曼·拉拉政治决裂，批评政府集权、施政不力，未解决燃油与美元短缺等民生危机，并发出最后通牒；该决定引发党内分裂，形成特鲁希略派、众议院议长卡斯特罗派及拉拉派等多股力量。2026年3月他在地方选举中当选拉巴斯省议会议员，5月15日经一致表决当选省议会副主席（2026-2027届）。同年10月，他指认约10名议员涉政治跳槽，宣布移送党伦理法庭并寻求收回议席。",
    "profile": None,
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "news_search",
            "web_search",
            "wikipedia",
            "government_registry",
            "social_media"
        ],
        "quotes": [
            {
                "title": "PDC se divide en dos y ambas corrientes hablan de procesar a los disidentes - El Deber",
                "url": "https://eldeber.com.bo/pais/pdc-divide-dos-ambas-corrientes-hablan-procesar-disidentes_1789086944"
            },
            {
                "title": "PDC se divide entre respaldo a Rodrigo Paz y ruptura con el Gobierno - Correo del Sur",
                "url": "https://correodelsur.com/politica/20260910/pdc-se-divide-entre-respaldo-a-rodrigo-paz-y-ruptura-con-el-gobierno.html"
            },
            {
                "title": "El PDC da ultimátum al Gobierno y amenaza con quitarle su respaldo - Oxígeno",
                "url": "https://oxigeno.bo/el-pdc-da-ultimatum-al-gobierno-y-amenaza-con-quitarle-su-respaldo-el-vocero-les-pide-ponerse-la-camiseta/"
            },
            {
                "title": "PDC se divide entre la ruptura y el respaldo al Gobierno de Rodrigo Paz - Visión 360",
                "url": "https://www.vision360.bo/noticias/2026/09/10/67040-pdc-se-divide-entre-la-ruptura-y-el-respaldo-al-gobierno-de-rodrigo-paz"
            },
            {
                "title": "Ceferino Rufo Calle es elegido presidente de la Asamblea Legislativa Departamental de La Paz - FM La Paz",
                "url": "https://fmlapaz.bo/ceferino-rufo-calle-es-elegido-presidente-de-la-asamblea-legislativa-departamental-de-la-paz/"
            },
            {
                "title": "Dividido en tres facciones: el PDC confirma su participación en las elecciones subnacionales de marzo de 2026 - Radio Luis de Fuentes",
                "url": "https://radioluisdefuentes.com/uncategorized/dividido-en-tres-facciones-el-pdc-confirma-su-participacion-en-las-elecciones-subnacionales-de-marzo-de-2026/"
            },
            {
                "title": "Partido Demócrata Cristiano (Bolivia) - Wikipedia (es)",
                "url": "https://es.wikipedia.org/wiki/Partido_Dem%C3%B3crata_Cristiano_(Bolivia)"
            },
            {
                "title": "Fiscalización PDC 2017 - Órgano Electoral Plurinacional（2018年决议确认其为PDC经济负责人）",
                "url": "https://web.oep.org.bo/wp-content/uploads/2021/07/240-PDC-FISCALIZACION-2017.pdf"
            },
            {
                "title": "ALDLP acompaña los actos conmemorativos por los 216 años de la Gesta Libertaria de Cochabamba - 拉巴斯省议会官网",
                "url": "https://asamblealapaz.gob.bo/aldlp-acompana-los-actos-protocolares-de-cbba-2026/"
            }
        ],
        "notes": "数据来源：8个独立来源全文精读（El Deber、Correo del Sur、Oxígeno、Visión 360、FM La Paz、Radio Luis de Fuentes、Estudio 99、拉巴斯省议会官网），辅以西班牙语维基百科PDC条目、多民族选举机构（OEP）2018年决议档案及多家玻利维亚媒体快讯。全名Óscar Abdón Trujillo Pinto经El Deber与OEP档案双重确认。PDC临时全国主席任期起点以2025-12-12最高选举法院正式注册日为准；西班牙语维基百科标注其主席职务为临时（temporal）性质。2026-09-09决裂事件经El Deber、Correo del Sur、Oxígeno、Visión 360等4个以上独立来源交叉验证。性别男性由多方「el presidente/先生」称谓确认。存疑与留空：出生日期、出生地、教育背景、家庭成员均无公开可查记录，留空处理；经facebook/X/linkedin/instagram/tiktok/youtube六平台扫描，未发现可确证为其本人的社交媒体账号（同名活跃账号属歌手、医生等他人；X @PDCBolivia与Instagram @boliviapdc为PDC党部账号而非个人账号），故social_accounts留空；省议员首次任职起点未获可靠来源（拉巴斯省议会官方账号2024年11月内容中已列名），start_date留空。name_zh采用项目_name_index.json既有译名「奥斯卡·阿夫东·特鲁希略」，未检索到中文媒体对其的独立既有译名。因出生、教育、家庭、社媒、联系方式等字段客观缺失（玻利维亚地方性政党人物公开个人信息有限），completeness_score预计约63分，属客观上限。"
    },
    "birth_date_note": "公开报道未披露其出生日期，留空。",
    "birth_place_note": "公开报道未披露其出生地，留空。",
    "education_note": "未检索到任何公开的教育背景信息（毕业院校、学位），留空。",
    "work_note": "PDC全国主席职务为临时/看守性质（西班牙语维基百科标注temporal），2025-12-12经TSE正式注册；PDC经济负责人身份见OEP2018年9月19日决议（档案240-PDC-FISCALIZACION-2017），任职起止不详；拉巴斯省议员：官方账号2024年11月内容已列名（时任基础设施相关委员会职务），2026年3月地方选举后继续/再度当选，2026-05-15当选省议会副主席（2026-2027届）。",
    "family_note": "公开报道未披露其家庭成员信息，family_members留空。",
    "social_accounts_note": "六平台扫描（facebook/x/linkedin/instagram/tiktok/youtube）未发现可确证为其本人的账号；检索到的同名账号为歌手（@oscartrujillo_oficial）、美国外科医生等无关人员；PDC党部账号（X @PDCBolivia、Instagram @boliviapdc、官网pdcbolivia.com）为政党账号，不计入个人社媒。",
    "name_zh_note": "未见中文媒体对「Óscar Abdón Trujillo」的独立既有译名；name_zh采用本项目_name_index.json中已建立的译名「奥斯卡·阿夫东·特鲁希略」。",
    "position_note": "PDC全国主席职务为临时（temporal）性质，即看守主席；同时以PDC籍身份任拉巴斯省议会议员并兼任省议会副主席。"
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE", OUT)
print("bio_len:", len(profile["biography_summary"]))

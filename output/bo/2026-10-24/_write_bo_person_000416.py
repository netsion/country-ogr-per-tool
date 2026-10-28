# -*- coding: utf-8 -*-
"""Build BO-PERSON-000416 (Johnny Dueri) person profile JSON."""
import json

data = {
    "person_id": "BO-PERSON-000416",
    "wikidata_qid": None,
    "name": "Johnny Dueri",
    "name_en": "Johnny Dueri",
    "name_zh": None,
    "name_zh_note": "检索中文媒体与百科均未见该人物的既有标准中文译名，故置 null。杜埃里（Dueri）为巴勒斯坦裔玻利维亚家族姓氏（家族源自伯利恒）。",
    "aliases": [
        "Miguel Johnny Dueri Saba",
        "Jhonny Dueri",
        "Ing. Johnny Dueri"
    ],
    "aliases_note": "法律全名 Miguel Johnny Dueri Saba（名取自父亲 Miguel，母姓 Saba）：见玻利维亚公共工程部第 RM 438-2016 号部长决议备案（2016-06-17 备忘录）、选举机构 OEP 媒体备案文件及 YPFB 采购文件，多份政府文件一致；「Jhonny」为玻利维亚媒体与社交平台常见拼写变体（Vio Justicia Bolivia、Radio Fides 等）；「Ing.（工程师）」头衔见电台官网《Quiénes Somos》。",
    "nationality": "BO",
    "gender": "male",
    "is_deceased": False,
    "birth_date": None,
    "birth_place": None,
    "contacts": [
        {
            "type": "website",
            "value": "https://www.panamericana.bo",
            "source": "Radio Panamericana 官网（其技术部负责人及业主总经理职务关联页面）"
        },
        {
            "type": "phone",
            "value": "+591 2 2782534",
            "source": "amarillas.com.bo 玻利维亚工商黄页及供应商通讯录（其名下企业 Artes Gráficas Discolandia 登记电话，非个人号码）"
        }
    ],
    "current_positions": [
        "泛美电台技术部负责人",
        "泛美电台业主总经理",
        "泛美电台持牌公司法定代表"
    ],
    "education": [],
    "work_experience": [
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚泛美电台 (Radio Panamericana)",
            "org_id": "BO-MEDIA-015",
            "position": "技术部负责人 (Responsable del Departamento Técnico)"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚泛美电台 (Radio Panamericana)",
            "org_id": "BO-MEDIA-015",
            "position": "业主总经理 (Gerente Propietario)"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "迪斯科兰迪亚印刷公司 (Artes Gráficas Discolandia)",
            "org_id": None,
            "position": "业主"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000414",
            "person_name": "亨利·杜埃里 (Henry Dueri)",
            "relationship_type": "sibling",
            "description": "兄弟：巴勒斯特裔专题报道《Páginas Árabes》（2015-08-14）载创始人 Miguel Dueri 与妻子 Miriam Saba 育有五子女——Johnny、Henry、Denise、Isabel、Juliette；《El Diario》2022-09-12 台庆报道图片说明中 Johnny 与 Henry、Juliette、Denise Dueri 并列出现，交叉印证。Henry 现任泛美电台总经理，备案全名 Henry Juan Dueri Saba 与 Johnny 的「名+Dueri+Saba」命名模式一致，佐证同胞关系。"
        },
        {
            "person_id": "BO-PERSON-000413",
            "person_name": "塞尔希奥·杜埃里 (Sergio Dueri)",
            "relationship_type": "colleague",
            "description": "同台共事：Sergio 任泛美电台执行台长并主持数字新闻平台，与 Johnny 同属经营电台的杜埃里家族成员。从辈分推断 Sergio 更可能为 Johnny 的侄辈（Sergio 常驻拉巴斯、其社交平台同名主页母姓候选为 Sansur，与 Johnny 母姓 Saba 不同），但公开资料未载明具体亲属关系，故记 colleague。"
        },
        {
            "person_id": "BO-PERSON-000749",
            "person_name": "塞西莉亚·杜埃里 (Cecilia Dueri)",
            "relationship_type": "colleague",
            "description": "同台家族成员：电台官网《Quiénes Somos》载 Cecilia Dueri 与 Germán Núñez、Mabel Pasten 共同负责行政与销售部门；与 Johnny 的具体亲缘关系未获公开证实，故记 colleague。"
        }
    ],
    "social_accounts": [],
    "social_accounts_note": "六平台扫描（facebook/twitter_x/linkedin/instagram/tiktok/youtube）均未找到可归属本人的个人账号：Facebook 存在同名公共目录页（es-la.facebook.com/public/Johnny-Dueri）但内容不可核验；LinkedIn 姓氏目录列有「Johnny Dueri, Bolivia」但无独立可核验主页；Instagram、X、TikTok 检索无结果；YouTube「Testimonio de Vida - Johnny Dueri Saba」及 Facebook 多条讲道视频为教会页面（拉巴斯基督教会、El Sonido de la Vida、Discolandia Bolivia）发布的内容而非其个人账号，故 social_accounts 留空。",
    "family_members": [
        {
            "person_id": None,
            "name": "米格尔·杜埃里 (Miguel Dueri)",
            "relationship": "father",
            "industry_or_organization": "玻利维亚泛美电台（创始人、业主）"
        },
        {
            "person_id": None,
            "name": "米里亚姆·萨巴 (Miriam Saba)",
            "relationship": "mother",
            "industry_or_organization": None
        },
        {
            "person_id": "BO-PERSON-000414",
            "name": "亨利·杜埃里 (Henry Dueri)",
            "relationship": "brother",
            "industry_or_organization": "玻利维亚泛美电台（总经理）"
        },
        {
            "person_id": None,
            "name": "德妮丝·杜埃里 (Denise Dueri)",
            "relationship": "sister",
            "industry_or_organization": None
        },
        {
            "person_id": None,
            "name": "伊莎贝尔·杜埃里 (Isabel Dueri)",
            "relationship": "sister",
            "industry_or_organization": None
        },
        {
            "person_id": None,
            "name": "朱丽叶·杜埃里 (Juliette Dueri)",
            "relationship": "sister",
            "industry_or_organization": None
        }
    ],
    "political_stances": [],
    "major_achievements": [
        {
            "date": "2022-01",
            "achievement": "以业主总经理身份处置发射台土地侵占危机：拉巴斯 Villa Ingenio（埃尔阿尔托）发射塔区域遭「Villa Ingenio 社区成员」强行占地并扬言炸毁发射塔，其出示1982年6月3日地契（其父 Miguel Dueri 购得原 Villa Ingenio 庄园 43,216 平方米土地），经警方斡旋与占地方达成协议，保障电台全国及国际信号连续播出（Opinión、Noticias Fides、电台官网2022-01-07报道）。",
            "organization": "玻利维亚泛美电台 (Radio Panamericana)"
        },
        {
            "date": "2016-06",
            "achievement": "以持牌公司法定代表身份就玻利维亚电信监管总局（ATT）启动的频率执照撤销程序（RE-TL LP 32-2016）向公共工程部提交申辩备忘录，该案后由第 RM 438-2016 号部长决议处理（备案原文载「Miguel Johnny Dueri Saba, en representación de Somera Ltda. – Radio Panamericana」）。",
            "organization": "索梅拉广播有限公司 (SOMERA Ltda.)"
        }
    ],
    "biography_summary": "Johnny Dueri（法律全名 Miguel Johnny Dueri Saba，暂无通行中文译名）是玻利维亚拉巴斯知名私营新闻电台泛美电台（Radio Panamericana，1972年7月17日开播）技术部负责人（Responsable del Departamento Técnico），官网《Quiénes Somos》以「Ing. Johnny Dueri」载明其主持负责发射机、卫星与传输系统的技术部；同时他具业主总经理（gerente propietario）身份，并任电台持牌公司索梅拉广播有限公司（SOMERA Ltda.）法定代表，多份政府备案文件可证。他是电台创始人、巴勒斯坦伯利恒出身实业家米格尔·杜埃里（2015年7月30日去世）与妻子米里亚姆·萨巴（1952年成婚）的五名子女之一，兄弟姐妹为 Henry（现任总经理）、Denise、Isabel 与 Juliette，电台创办至今始终由杜埃里家族经营。2016年6月他代表 SOMERA Ltda. 就 ATT 启动的执照撤销程序向公共工程部申辩；2022年1月以业主总经理身份处置 Villa Ingenio 发射台土地侵占及发射塔被扬言炸毁事件，出示1982年地契并与社区达成协议；2022年9月与兄弟姐妹共同出席电台50周年台庆；2026年前后仍以家族代表身份处理该土地纠纷后续。另在拉巴斯奥夫拉赫斯区经营迪斯科兰迪亚印刷公司（Artes Gráficas Discolandia）。多个教会来源显示一名全名相同（Johnny Dueri Saba）者为拉巴斯基督教会牧师/讲员，很可能为同一人但未获第二独立来源确证。",
    "profile": None,
    "public_activities": "2026年（电台54周年期间）：以业主家族代表身份偕律师到泛美电台现场处理 Villa Ingenio 土地侵占纠纷后续，出示产权文件（Vio Justicia Bolivia Facebook 帖子）；2022-09-12：与兄弟 Henry、姐妹 Juliette 和 Denise 及拉巴斯市长 Iván Arias 共同出席电台50周年台庆（《El Diario》报道图片说明）；2022-01-07：在电台《正午新闻》（noticiero meridiano）通报与 Villa Ingenio 占地方达成协议、保障信号播出（Opinión、电台官网报道）；2016-06-17：代表 SOMERA Ltda. 就 ATT 执照撤销程序向公共工程部提交申辩备忘录（RM 438-2016 备案）；另以 YPFB（玻利维亚国家石油公司）采购文件所示 Radio Panamericana–Somera Ltda. 代表身份参与最高200万玻利维亚诺的合同事项。",
    "family_relationship_note": "父母与四名兄弟姐妹（Henry、Denise、Isabel、Juliette）来自巴勒斯特裔专题媒体《Páginas Árabes》2015-08-14 对其父母的专题报道（五子女名单）；Denise 与 Juliette 另有《El Diario》2022-09-12 台庆报道图片说明交叉印证；Isabel 仅《Páginas Árabes》单一来源，采信程度较低。Henry 与 Johnny 的同胞关系另有两点旁证：备案全名同为「名+Dueri+Saba」模式，且二人分别在电台任总经理与技术部负责人。与 Sergio Dueri、Cecilia Dueri 同为家族成员但具体亲缘未获证实。注：任务原描述称电台为「圣克鲁斯克罗地亚裔家族」，经核实电台总部在拉巴斯，家族为巴勒斯坦（伯利恒）移民后裔，与该描述不符，以核实证据为准。",
    "nationality_note": "玻利维亚（BO）：以 SOMERA Ltda. 法定代表身份出现于玻利维亚政府备案文件；家族为巴勒斯坦移民后裔——其父 Miguel Dueri 出生于伯利恒（Belén, Palestina），20岁来拉巴斯，1952年与出身当地阿拉伯社群的 Miriam Saba 成婚（Noticias Fides、《Páginas Árabes》）。",
    "position_note": "三重身份均有独立来源：①技术部负责人——电台官网《Quiénes Somos》（页面最后更新2022-09-05）及西语维基百科（引用同页，2020-03-08 访问版本）双源；②业主总经理——电台官网2022-01-07报道原文「El gerente propietario de Radio Panamericana, Johnny Dueri」及 Opinión/Fides 同事件报道；③SOMERA Ltda. 法定代表——OEP EDRM 2021 备案、OOPP RM 438-2016 号部长决议、OEP SIMPE 2026 大选媒体资费备案、YPFB 采购文件四份文件一致。官网《Quiénes Somos》未注明部门信息的原始生效日期，技术负责人任职起始时间不明。",
    "work_note": "电台持股与控制权：泛美电台为杜埃里家族企业，西语维基百科载所有者为 Sociedad Mercantil de Radiodifusión Ltda.（SOMERA Ltda.，隶属 Grupo Dueri）；Johnny 为该公司法定代表并具业主总经理（gerente propietario）身份，据此可推断其在家族企业中具所有者地位，但玻利维亚工商登记的具体持股比例无公开可查数据，故未填写具体股构信息。名下另登记有迪斯科兰迪亚印刷公司（Artes Gráficas Discolandia de Miguel Johnny Dueri Saba，拉巴斯奥夫拉赫斯区 Héctor Ormachea 街5390号，主营第三方印刷服务；amarillas.com.bo 工商黄页，数据源自工商注册）。",
    "education_note": "教育背景无任何公开资料：官网仅称其「Ing.（工程师）」，该头衔在玻利维亚常用于工程从业者也含尊称用法，不能据此推断其学历与学位，education 留空。",
    "birth_note": "出生日期与出生地均无公开资料；仅知其父1952年成婚、家族扎根拉巴斯，其本人成年后活动均在拉巴斯。",
    "collection_meta": {
        "collection_date": "2026-10-27",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "wikipedia",
            "news_search",
            "web_search",
            "social_media",
            "government_registry"
        ],
        "completeness_score": 46,
        "notes": "身份核实：①法律全名 Miguel Johnny Dueri Saba 由 OEP EDRM 2021、OOPP RM 438-2016 部长决议、OEP SIMPE 2026 资费备案、YPFB 采购文件四份政府文件一致载明（均以搜索引擎索引快照形式获取——OOPP 与 YPFB 两份 PDF 已直接下载但为纯扫描件无文本层且环境无 OCR，SIMPE 与 OEP 服务器自本环境不可直连）；②技术部负责人职务经电台官网《Quiénes Somos》原文精读与西语维基百科双源确认；③业主总经理身份经电台官网 2022-01-07 报道原文、Opinión、Noticias Fides 多源确认；④家族关系（父创办人 Miguel Dueri、母 Miriam Saba、兄弟 Henry、姐妹 Denise/Isabel/Juliette）经《Páginas Árabes》专题全文与《El Diario》台庆报道交叉确认。关键修正：任务背景所述「圣克鲁斯克罗地亚裔」与证据不符——电台总部与家族企业均在拉巴斯，家族源自巴勒斯坦伯利恒（阿拉伯基督徒社群），已按核实证据记录。存疑与留空：①出生日期/地点、学历均无公开资料；②教会来源显示同名同全名（Johnny Dueri Saba）牧师/讲员，很可能为本人（Discolandia 企业页面转发其讲道、见证视频用全名）但未获第二独立来源确证，仅记入传记与活动、不入结构化字段；③Isabel Dueri 为单一来源；④与 Sergio（疑似侄辈）/Cecilia 的具体亲缘未证实，均记 colleague；⑤wikidata 无本人条目；⑥name_zh 无既有译名置 null；⑦个人社交账号六平台扫描均无法归属，social_accounts 留空；⑧持具体持股比例的工商/股构数据无公开来源。完整性说明：completeness_score=46，缺失项集中在学历、出生信息、个人社交账号、政治立场等客观无公开数据的字段，已达中层技术/家族企业管理岗可核实的上限。",
        "quotes": [
            {
                "title": "Quiénes Somos - Radio Panamericana 官网（技术部由 Ing. Johnny Dueri 主持；家族分工；1972-07-17 开播）",
                "url": "https://www.panamericana.bo/estaticas/quienes-somos.html"
            },
            {
                "title": "Johnny Dueri | Últimas noticias - Radio Panamericana tags 页（gerente propietario 身份）",
                "url": "https://www.panamericana.bo/tags/johnny-dueri"
            },
            {
                "title": "Gerente de Radio Panamericana da cuenta de acuerdo con avasalladores para garantizar regularidad en la señal de la emisora - Radio Panamericana（2022-01-07）",
                "url": "https://www.panamericana.bo/articulo/nacional/gerente-radio-panamericana-da-cuenta-acuerdo-avasalladores-garantizar-regularidad-senal-emisora/20220107221150005496.html"
            },
            {
                "title": "Radio Panamericana está de aniversario - El Diario（2022-09-12，50周年台庆，Johnny 与 Henry、Juliette、Denise Dueri 同框）",
                "url": "https://www.eldiario.net/portal/2022/09/12/radio-panamericana-esta-de-aniversario"
            },
            {
                "title": "Radioemisora denuncia intentos de volar torres de transmisión - Opinión（2022-01-07，发射塔危机与1982年地契）",
                "url": "https://www.opinion.com.bo/pais/radioemisora-denuncia-intentos-volar-torres-transmision/20220107174211850421.html"
            },
            {
                "title": "Radioemisora denuncia intentos de volar torres de transmisión - Noticias Fides (ANF)（2022-01，同事件独立报道）",
                "url": "https://www.noticiasfides.com/nacional/sociedad/radioemisora-denuncia-intentos-de-volar-torres-de-transmision-413246"
            },
            {
                "title": "Miriam, Miguel y un amor que comenzó con unas palabras en árabe - Páginas Árabes（2015-08-14，五子女名单：Johnny、Henry、Denise、Isabel、Juliette）",
                "url": "https://paginasarabes.com/2015/08/14/miriammiguel-y-un-amor-que-comenzo-con-unas-palabras-en-arabe"
            },
            {
                "title": "Las últimas palabras de Miguel Dueri - Noticias Fides (ANF)（2015-08，父辈生平：伯利恒出生、1952年成婚）",
                "url": "https://www.noticiasfides.com/nacional/sociedad/las-ultimas-palabras-de-miguel-dueri-que-tus-palabras-vayan-a-parar-a-la-puerta-del-paraiso-355244-355198"
            },
            {
                "title": "Radio Panamericana (Bolivia) - Wikipedia, la enciclopedia libre（技术部负责人、SOMERA Ltda. 所有权、Grupo Dueri）",
                "url": "https://es.wikipedia.org/wiki/Radio_Panamericana_(Bolivia)"
            },
            {
                "title": "Resolución Ministerial Nº 438-2016 - Ministerio de Obras Públicas（2016-06-17 备忘录：Miguel Johnny Dueri Saba 代表 Somera Ltda. – Radio Panamericana）",
                "url": "https://www.oopp.gob.bo/wp-content/uploads/2020/antiguos/RM_438-2016_RJ_SOMERA_RADIO_POANAMERICANA_c_Res_Rev_RE-TL_LP_32-2016.PDF"
            },
            {
                "title": "Formulario de registro y acreditación de Radio Panamericana (SOMERA Ltda.) ante el OEP（Johnny Dueri Saba 为法定代表）",
                "url": "https://www.oep.org.bo/wp-content/uploads/2021/01/03_PANAMERICANA_EDRM_2021.pdf"
            },
            {
                "title": "Tarifario digital de Radio Panamericana - Elecciones Subnacionales 2026 - OEP SIMPE（Johnny Dueri Saba 为 REPRESENTANTE LEGAL）",
                "url": "https://simpe.oep.org.bo/storage/medios/m-697/acreditaciones/1166/a4cf7994__tarifario-digital-de-radio-panamericana-elecciones-subnacionales-2026.pdf"
            },
            {
                "title": "YPFB 采购合同文件（Miguel Johnny Dueri Saba 代表 Radio Panamericana – Somera Ltda.，合同额最高 Bs 2,000,000）",
                "url": "https://contrataciones.ypfb.gob.bo/comun/downloadFile/1071000000071457"
            },
            {
                "title": "Artes Gráficas Discolandia de Miguel Johnny Dueri Saba - amarillas.com.bo（名下印刷企业工商黄页）",
                "url": "https://amarillas.com.bo/empresa/artes-graficas-discolandia-de-miguel-johnny-dueri-saba"
            },
            {
                "title": "54 años de Radio Panamericana - Vio Justicia Bolivia Facebook（2026，Jhonny Dueri 以家族代表身份携律师到场）",
                "url": "https://www.facebook.com/viojusticiabolivia/posts/54-a%C3%B1os-de-radio-panamericana-reconocemos-su-destacada-trayectoria-y-su-invaluab/1341127631531738"
            },
            {
                "title": "Mensaje: La Consejería de Jehová - Ptr. Johnny Dueri - Congregación Cristiana La Paz Facebook（同名讲员，归属待证）",
                "url": "https://www.facebook.com/CongregacionCristiana.LaPaz/videos/908206845594919"
            }
        ]
    }
}

out = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000416.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("written", out)
bio = data["biography_summary"]
print("bio_len:", len(bio))

# -*- coding: utf-8 -*-
"""Build BO-PERSON-000409 Jaime 'Jimmy' Iturri Salmon profile JSON."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "persons", "BO-PERSON-000409.json")

profile = {
    "person_id": "BO-PERSON-000409",
    "wikidata_qid": None,
    "name_zh": None,
    "name": "Jaime Iturri Salmón",
    "name_en": "Jaime Iturri Salmon",
    "aliases": [
        "Jimmy Iturri",
        "Jaime 'Jimmy' Iturri Salmón",
        "Jimmy",
        "Jaime Iturri Salmon"
    ],
    "nationality": "BO",
    "gender": "male",
    "birth_date": "1963-01-01",
    "birth_place": "México",
    "contacts": [],
    "current_positions": [],
    "education": [
        {
            "institution": "玻利维亚天主教大学 (Universidad Católica Boliviana)",
            "field": "传播学",
            "start_date": None,
            "end_date": None,
            "note": "2015年玻利维亚文学中心人物页（第七届新闻与文学论坛参会者自介）称其「曾在该校学习传播（estudió comunicación）」，未说明是否获得学位及就读年份"
        },
        {
            "institution": "圣安德烈斯大学 (Universidad Mayor de San Andrés)",
            "field": "文学",
            "start_date": None,
            "end_date": None,
            "note": "同上来源称其「在该校学习文学（estudió literatura）」，未说明是否获得学位及就读年份；另称其时为该校特聘教师（docente contratado）"
        }
    ],
    "work_experience": [
        {
            "start_date": None,
            "end_date": None,
            "organization": "《最后一点钟报》 (Ultima Hora)",
            "org_id": None,
            "position": "总编辑 (Editor General)",
            "note": "2015年人物自介称曾任该报总编辑，具体任职年份未披露；该报为玻利维亚拉巴斯老牌日报"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "《La Quinta!》新闻杂志 (La Quinta!)",
            "org_id": None,
            "position": "主编 (Editor en Jefe)",
            "note": "2015年人物自介称曾任该杂志主编，具体任职年份未披露"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "《El Extra报》 (El Extra)",
            "org_id": None,
            "position": "社长 (Director)",
            "note": "2015年人物自介称曾任该报负责人（director），具体任职年份未披露"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "拉巴斯市政府 (Gobierno Autónomo Municipal de La Paz)",
            "org_id": None,
            "position": "市政二百周年纪念代表 (Delegado Municipal para el Bicentenario)",
            "note": "2015年人物自介称曾任「1809年7月16日革命二百周年」市政代表，对应2009年前后，具体任职年份未披露"
        },
        {
            "start_date": None,
            "end_date": "2019-11",
            "organization": "玻利维亚ATB电视台 (Red ATB)",
            "org_id": "BO-MEDIA-011",
            "position": "内容总监兼《Anoticiando》主持人 (Director de Contenidos y conductor de Anoticiando)",
            "note": "至迟于2013年5月已任此职（《理性报》hemeroteca 2013-05-17专访）；2013年5月9日与同台主持Ramón Grimalt在直播中发生冲突后一度离开荧屏，其后回归；2015年5月仍以内容总监身份接受ANF采访（eju.tv转录）；es-Wikipedia载其于2019年11月10日Evo Morales辞职后辞去ATB职务，其后于2020年1月因ATB-PAT案遭检方逮捕令而流亡阿根廷（其本人在ATB《La Noche》专访中自述「那一年我在流亡」）"
        },
        {
            "start_date": "2020",
            "end_date": "2025-12",
            "organization": "玻利维亚ATB电视台 (Red ATB)",
            "org_id": "BO-MEDIA-011",
            "position": "总经理 (Gerente General)",
            "note": "es-Wikipedia将2020-2025年标注为「Iturri第二时期」，其于Arce就任总统后重返；2025年5月Urgente.bo称其为「导演兼股东（director y accionista）」，2025年多家媒体称其「gerente general」；2025-12-12新董事会决定不予续聘、结束其2014年以来对该台的掌控（es-Wikipedia引Visión360），2025年12月正式终止与ATB的劳动关系；2026-01-13继任总经理Amílcar Torrico致客户信正式确认其离任（Visión360、Los Tiempos）"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "圣安德烈斯大学 (Universidad Mayor de San Andrés)",
            "org_id": None,
            "position": "特聘教师 (Docente Contratado)",
            "note": "2015年人物自介称其时为该校特聘教师并任国际组织顾问；另称曾在六所大学及Simón Bolívar高等师范学校（Normal Superior Simón Bolívar）任教；现况无公开资料"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000407",
            "person_name": "阿米尔卡·托里科 (Amílcar Torrico)",
            "relationship_type": "colleague",
            "description": "同台ATB：Torrico于2026年1月接任总经理，2026-01-13以致客户信方式公开确认Iturri离任并宣布ATB进入「新阶段」（Visión360、Los Tiempos转载）",
            "source": "https://www.vision360.bo/noticias/2026/01/13/38377-atb-anuncia-una-etapa-de-renovacion-y-confirma-la-salida-de-jaime-iturri"
        },
        {
            "person_id": "BO-PERSON-000408",
            "person_name": "玛丽亚·雷内·杜亨·奎利亚尔 (María Renee Duchén Cuéllar)",
            "relationship_type": "colleague",
            "description": "同台ATB：2014年Invesbol入主后的节目改版中，资深主播Duchén以《Anoticiando》主持人身份回归（es-Wikipedia）；Duchén后任ATB拉巴斯及全国新闻网新闻部主任，与Iturri的管理层任期重叠",
            "source": "https://es.wikipedia.org/wiki/ATB_(canal_de_televisi%C3%B3n)"
        },
        {
            "person_name": "劳尔·马塞洛·乌尔塔多 (Raúl Marcelo Hurtado)",
            "person_id": None,
            "relationship_type": "business_partner",
            "description": "2014年共同组成Invesbol从西班牙Akaishi Investments手中购得ATB股权（es-Wikipedia业主表：Iturri持55%、Hurtado持31%），Hurtado任ATB董事长；两人共同控制ATB至2021年Invesbol解散、ATBMedia接手；2020年1月Hurtado曾因PAT案被捕",
            "source": "https://es.wikipedia.org/wiki/ATB_(canal_de_televisi%C3%B3n)"
        },
        {
            "person_name": "路易斯·内姆塔拉 (Luis Nemtala)",
            "person_id": None,
            "relationship_type": "associate",
            "description": "同为Invesbol组成成员（es-Wikipedia）；2019年Iturri离任期间Nemtala任ATB总经理并就政府广告费问题公开表态（es-Wikipedia引2020年5月报道）",
            "source": "https://es.wikipedia.org/wiki/ATB_(canal_de_televisi%C3%B3n)"
        }
    ],
    "social_accounts": [],
    "family_members": [
        {
            "person_id": None,
            "name": "胡利奥·海梅·伊图里·萨利纳斯 (Julio Jaime Iturri Salinas)",
            "relationship": "father",
            "industry_or_organization": "律师；曾任玻利维亚电力公司（COBEE）法律顾问35年",
            "description": "Pandora Papers（Connectas，2021-11-03）披露：其于2011年与配偶（Iturri之母，未披露姓名）经Trident Trust在英属维尔京群岛设立离岸公司Fufurufu Inc.，为三名子女设信托（两名儿子各持33.33%、女儿持33.34%）；约四年后公司解散；其称设立目的为保全家庭积蓄与遗产",
            "source": "https://www.connectas.org/pandora-papers-bolivia-jimmy-iturri/"
        }
    ],
    "political_stances": [
        {
            "date": "2013-05",
            "topic": "编辑立场与党派关系",
            "stance_content": "在《Anoticiando》直播中为其社会主义倾向辩护，称应「通过与不公正作斗争来拯救国家」，被同台主持Grimalt指为穿上Evo Morales的MAS-IPSP「球衣」；事后接受《理性报》专访否认MAS党员身份，称自己14岁起即为左派，并否认因冲突被停职",
            "source": "https://hemeroteca.larazon.bo/la-revista/2013/05/17/jaime-iturri-espero-volver-algun-momento-a-las-pantallas"
        },
        {
            "date": "2015-05",
            "topic": "新闻独立性",
            "stance_content": "在ATB节目《Corto Verano》专访中称「我不相信（新闻）独立性，我相信专业性」（No creo en la independencia, creo en el profesionalismo），肯定Evo Morales的领导地位，并称「MAS团结了所有左翼、左翼最优秀的干部都去了MAS」（ANF通稿，eju.tv转录）",
            "source": "https://eju.tv/2015/05/jaime-iturri-no-cree-en-la-independencia-periodstica-destaca-liderazgo-de-evo-y-critica-a-otros-periodistas"
        }
    ],
    "major_achievements": [
        {
            "date": "2015",
            "achievement": "截至2015年已出版著作23部，兼具新闻与文学双重身份，曾参加第七届新闻与文学论坛（7º Foro Periodismo y Literatura）",
            "organization": "玻利维亚文学中心 (Centro de Literatura Boliviana CSIP)"
        },
        {
            "date": "2014",
            "achievement": "与Marcelo Hurtado、Luis Nemtala组成Invesbol，从西班牙Akaishi Investments手中购得ATB股权，使该全国性电视网重回玻利维亚资本手中；Invesbol期间持55%为第一大股东（2014-2021）",
            "organization": "玻利维亚ATB电视台 (Red ATB)"
        },
        {
            "date": "2014",
            "achievement": "Invesbol入主后主导节目改版：创办全国唯一的调查新闻纪录片栏目《Documentos ATB》，扩大圣克鲁斯制作基地，并促成老牌新闻栏目《Anoticiando》资深主播María René Duchén回归",
            "organization": "玻利维亚ATB电视台 (Red ATB)"
        }
    ],
    "biography_summary": "海梅·「吉米」·伊图里·萨尔蒙（Jaime 'Jimmy' Iturri Salmón）是玻利维亚资深新闻工作者与媒体管理者，1963年生于墨西哥。据玻利维亚文学中心2015年人物页，他曾就读于玻利维亚天主教大学（传播）与圣安德烈斯大学（文学），拥有五个研究生学位，出版著作23部，早年曾任《最后一点钟报》总编辑、《La Quinta!》杂志主编、《El Extra报》社长及拉巴斯市政府二百周年纪念代表，并在多所大学任教。至迟于2013年5月出任ATB电视台内容总监并主持政论节目《Anoticiando》；2014年与Marcelo Hurtado、Luis Nemtala组成Invesbol购得ATB股权（持55%为第一大股东），任内创办调查栏目《Documentos ATB》、推动ATB Digital数字信号。2019年11月10日Evo Morales辞职后其辞去ATB职务；2020年1月30日因ATB-PAT案被玻利维亚检方下令逮捕（时居阿根廷）。2020年Arce政府上台后重返ATB，以总经理身份执掌至2025年；2021年11月Pandora Papers曝光其为英属维尔京群岛离岸公司Fufurufu Inc.受益人之一（其本人否认所有权，称系其父管理家产所用）。2025年ATB爆发欠薪与Gestora养老金欠缴危机，5月工会公开抗议，10月拉巴斯工人中央（COD）宣布其为「工人公敌」；同年12月12日新董事会决定不予续聘，结束其2014年以来对ATB的掌控，2026年1月13日继任总经理Amílcar Torrico正式对外确认其离任。",
    "profile": {
        "source_url": "http://cd1.eju.tv/wp-content/uploads/2015/05/image_thumb17.png",
        "local_path": "photos/BO-PERSON-000409.png"
    },
    "birth_date_note": "仅年份可查：玻利维亚文学中心2015年人物页记载「México 1963」，月日不可考，按schema惯例置01-01；单一来源（人物自介性质），未获第二独立来源印证",
    "birth_place_note": "同上来源仅记载生于墨西哥（México）；二级转述（Elias Blanco书评博客，未经直取核验）称生于墨西哥城（México D.F.），故具体城市存疑，保守记为「México」",
    "name_zh_note": "无玻利维亚华文媒体既有译名；项目内部索引与BO-MEDIA-011组织档案使用「海梅·『吉米』·伊图里·萨尔蒙（Jaime 'Jimmy' Iturri Salmón）」作为检索名，按任务参数name_zh置null，档案内关系条目沿用该内部译名格式",
    "position_note": "职务称谓沿革：2013-05（《理性报》专访）及2015-05（ANF/eju.tv）均为「Director de Contenidos」兼《Anoticiando》主持人；2014-2021年为ATB控股股东（Invesbol 55%，es-Wikipedia业主表）；2025-05 Urgente.bo称「director y accionista」；2025年es-Wikipedia及Urgente.bo多处称「gerente general」；2019-11-10至2020年间任职中断（辞任并流亡阿根廷，2020年重返）；2025-12-12被新董事会解职，2026-01-13由继任者Torrico公开确认",
    "work_note": "企业层面记录（均来自公开报道）：①2014年Akaishi Investments向玻利维亚公司Invesbol出售ATB股权，es-Wikipedia业主表载Invesbol期间Iturri持55%、Raúl Marcelo Hurtado持31%（2014年起），2021年Invesbol解散后由ATBMedia持100%，ATB现由ATBMedia所有、Illimani de Comunicaciones S.A.运营；②2020-01-30玻利维亚检察机构因ATB-PAT案（参议员Carmen Eva Gonzales举报18人以勒索手段取得ATB、PAT等媒体）对Iturri发出逮捕令（aprehensión）（Erbol、Fides），FELCC称其时在阿根廷；③2025-05-01 ATB工会（Sindicato de Trabajadores de ATB Illimani）公开抗议被拖欠工资6-7个月、Gestora/AFP缴款停缴，拉巴斯信号暂停、制作人员被强制集体休假（Urgente.bo直取）；④2025-10-04拉巴斯工人中央（COD）决议宣布Iturri为「工人公敌」，并追提ATB在2017-2019年获逾1.07亿玻利维亚诺政府广告款问题（es-Wikipedia引EL DIA）；⑤2025-12-01 ATB商务经理Víctor Branimir Flores因涉嫌侵占职工Gestora养老金缴款被刑事立案，工会代表称欠缴最长达40个月、涉及250余名职工，Iturri面对Fides提问仅答「我没有什么要向你们声明的」（es-Wikipedia引Fides）；⑥Iturri在ATB《La Noche》专访自述：「我们平均每年营收1400万美元，2020年只营收380万」，并将2020年停缴归因于时任当局停发政府广告（es-Wikipedia引述）；⑦2025-12-12新董事会决定不予续聘，2026-01-13继任总经理Torrico致客户信确认（Visión360、Los Tiempos直取）；⑧另有2022-11-16国家新闻伦理法庭（TNEP）因其《Anoticiando》节目对CONADE代表Manuel Morales的不实指控裁定其败诉并须更正（El País BO直取）",
    "shareholding_and_control": "2014-2021：经Invesbol控制ATB（es-Wikipedia业主表：Invesbol持ATB 100%，其中Iturri 55%、Hurtado 31%，2021年Invesbol解散）；2021年起：ATB 100%股权转入ATBMedia名下，Iturri的股权控制关系随之变更；2025-12-12：新董事会解除其职务，其对该台的控制期结束。另：2021-11-03 Pandora Papers披露其为BVI离岸公司Fufurufu Inc.受益人之一（与其两名兄弟姐妹并列，子女生母/父共同设立，子女各约33%），公司约存续四年后解散；Iturri本人回应称从未拥有该公司，系其父Julio Jaime Iturri Salinas为管理家庭积蓄与遗产所设（Connectas直取全文）",
    "family_note": "2015年人物自介称「有三个孩子（tiene tres hijos）」，未披露姓名，故不建family_members条目；母亲未披露姓名；父亲Julio Jaime Iturri Salinas信息见family_members条目（Pandora Papers）",
    "education_note": "除上述两段学习经历外，2015年人物自介另称拥有五个研究生学位（cinco posgrados），未披露授予院校与专业，无法建条目；另自介称曾在六所大学及Normal Superior Simón Bolívar任教",
    "social_accounts_note": "六平台扫描（facebook/twitter_x/instagram/linkedin/tiktok/youtube，多语关键词组合）未发现可核实的本人实名社交账号：检索命中均为第三方内容（Los Tiempos官方推特2021-11-03转引Connectas报道、新闻类Facebook主页转载其离台消息、玻利维亚文学中心机构账号等）；es-Wikipedia存在「Jimmy Iturri」条目但为红链（未建条目），无Wikidata条目，故social_accounts留空",
    "identity_note": "注意区分：①西班牙安达卢西亚的ITURRI集团（劳保装备企业，fundacioniturri.org）与本人无关，仅姓氏相同；②其父Julio Jaime Iturri Salinas姓名相近（见于Pandora Papers），引用时注意区分父子；③玻利维亚新闻界另有同名风险低，但「Jimmy Iturri」为本人物通用称呼（ATB台长语境下无歧义）",
    "collection_meta": {
        "collection_date": "2026-10-26",
        "phase": "phase4_person_profile",
        "data_sources": [
            "wikipedia",
            "news_search",
            "web_search",
            "social_media",
            "other"
        ],
        "notes": "数据来源确认：直取全文并核验的独立来源共8个——es-Wikipedia《ATB (canal de televisión)》（业主表+编年史）、Connectas Pandora Papers调查报道（2021-11-03全文）、Erbol ATB-PAT逮捕令报道（2020-01-30全文）、《理性报》hemeroteca专访（2013-05-17全文）、eju.tv/ANF专访（2015-05-01全文）、El País BO伦理法庭裁决报道（2022-11-16全文）、Urgente.bo欠薪危机报道（2025-05-02全文）、玻利维亚文学中心人物页（2015-07-29全文）；另经web reader读取Visión360（2026-01-13）、Fides、La Voz Bolivia、Los Tiempos（2026-01-14直取全文）等离任确认报道。关键发现：其ATB控制期横跨Invesbol（2014-2021）与ATBMedia（2021-2025）两段，2025年欠薪/Gestora危机是去职直接背景；职务终点（2025-12-12新董事会解职、2026-01-13公开确认）有≥2独立来源。存疑与局限：①出生信息（1963年生于墨西哥）仅文学中心人物自介单来源；②教育经历为自介、未证实学位；③五个研究生学位无院校信息；④无个人实名社交账号、无Wikidata/Wikipedia个人条目、无个人联系方式；⑤「Inversores de Radiodifusión S.A.」作为Invesbol全称的说法仅见于搜索摘要，未在直取原文中出现，故本档案仅用「Invesbol」；⑥同事Torrico（BO-PERSON-000407）、Duchén（BO-PERSON-000408）档案据索引在建，关系按colleague记录。completeness_score约72：缺失项主要系公开个人生平信息客观有限（无社交账号/联系方式/Wikidata/照片外字段），核心职业事实均有2个以上独立来源。",
        "quotes": [
            {
                "title": "ATB anuncia una etapa de renovación y confirma la salida de Jaime Iturri (Visión 360, 2026-01-13)",
                "url": "https://www.vision360.bo/noticias/2026/01/13/38377-atb-anuncia-una-etapa-de-renovacion-y-confirma-la-salida-de-jaime-iturri"
            },
            {
                "title": "Nuevo gerente de ATB confirma salida de Jaime Iturri y anuncia renovación (Los Tiempos, 2026-01-14)",
                "url": "https://www.lostiempos.com/actualidad/pais/20260114/nuevo-gerente-atb-confirma-salida-jaime-iturri-anuncia-renovacion"
            },
            {
                "title": "Ordenan aprehensión de Jimmy Iturri, exejecutivo y accionista de ATB (Agencia Fides)",
                "url": "https://www.noticiasfides.com/nacional/seguridad/ordenan-aprehension-de-jimmy-iturri-exejecutivo-y-accionista-de-atb-403419"
            },
            {
                "title": "Ordenan aprehensión de Jaime Iturri y otros dos ejecutivos por caso ATB-PAT (Erbol, 2020-01-30)",
                "url": "https://erbol.com.bo/seguridad/ordenan-aprehensi%C3%B3n-de-jaime-iturri-y-otros-dos-ejecutivos-por-caso-atb-pat"
            },
            {
                "title": "Jimmy Iturri, el periodista boliviano que figura como beneficiario de una offshore (Connectas, 2021-11-03)",
                "url": "https://www.connectas.org/pandora-papers-bolivia-jimmy-iturri/"
            },
            {
                "title": "JAIME ITURRI SALMÓN – Centro de Literatura Boliviana CSIP (2015-07-29)",
                "url": "https://encuentroescritores.wordpress.com/2015/07/29/jaime-iturri-salmon/"
            },
            {
                "title": "Jaime Iturri: 'Espero volver algún momento a las pantallas' (La Razón hemeroteca, 2013-05-17)",
                "url": "https://hemeroteca.larazon.bo/la-revista/2013/05/17/jaime-iturri-espero-volver-algun-momento-a-las-pantallas"
            },
            {
                "title": "Jaime Iturri no cree en la independencia periodística, destaca liderazgo de Evo y critica a otros periodistas (eju.tv/ANF, 2015-05-01)",
                "url": "https://eju.tv/2015/05/jaime-iturri-no-cree-en-la-independencia-periodstica-destaca-liderazgo-de-evo-y-critica-a-otros-periodistas"
            },
            {
                "title": "Tribunal Nacional de Ética Periodística falla en contra de Jaime Iturri por mentir en su programa (El País BO, 2022-11-16)",
                "url": "https://elpais.bo/nacional/20221116_tribunal-nacional-de-etica-periodistica-falla-en-contra-de-jaime-iturri-por-mentir-en-su-programa.html"
            },
            {
                "title": "Trabajadores de ATB denuncian falta de pago hace 6 meses y pausa de transmisiones en La Paz (Urgente.bo, 2025-05-02)",
                "url": "https://www.urgente.bo/noticia/trabajadores-de-atb-denuncian-falta-de-pago-hace-6-meses-y-pausa-de-transmisiones-en-la-paz"
            },
            {
                "title": "ATB (canal de televisión) - Wikipedia, la enciclopedia libre",
                "url": "https://es.wikipedia.org/wiki/ATB_(canal_de_televisi%C3%B3n)"
            },
            {
                "title": "Jimmy Iturri se va de ATB por varias irregularidades (La Voz Bolivia)",
                "url": "https://lavozbolivia.com/jimmy-iturri-se-va-de-atb-por-varias-irregularidades"
            }
        ]
    }
}


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    # quick re-read check
    with open(OUT, encoding="utf-8") as f:
        data = json.load(f)
    print("written:", OUT)
    print("person_id:", data["person_id"])
    print("bio_len:", len(data["biography_summary"]))
    print("work_entries:", len(data["work_experience"]))
    print("edu_entries:", len(data["education"]))
    print("rel_entries:", len(data["person_relationships"]))
    print("stance_entries:", len(data["political_stances"]))
    print("achieve_entries:", len(data["major_achievements"]))
    print("family_entries:", len(data["family_members"]))
    print("social_entries:", len(data["social_accounts"]))
    print("contact_entries:", len(data["contacts"]))
    print("quotes:", len(data["collection_meta"]["quotes"]))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Build BO-PERSON-000314 (Walter Arízaga Cervantes, USFX rector) profile JSON."""
import json
import os

USFX_ZH = "圣弗朗西斯科·哈维尔皇家教廷大学 (Universidad Mayor, Real y Pontificia de San Francisco Xavier de Chuquisaca)"

data = {
    "person_id": "BO-PERSON-000314",
    "wikidata_qid": None,
    "name": "Walter Arízaga Cervantes",
    "name_en": "Walter Arizaga Cervantes",
    "name_zh": None,
    "aliases": [
        "Ing. Walter Arízaga Cervantes",
        "Walter Arízaga",
        "Walter Arizaga Cervantes"
    ],
    "nationality": "BO",
    "gender": "male",
    "birth_date": None,
    "birth_place": None,
    "contacts": [
        {
            "type": "email",
            "value": "rectorado@usfx.bo",
            "source": "USFX官网页脚校长办公室（Rectorado）联系邮箱，属校长职务公用邮箱"
        },
        {
            "type": "website",
            "value": "https://www.usfx.bo",
            "source": "USFX大学官网"
        }
    ],
    "current_positions": [
        "圣弗朗西斯科·哈维尔皇家教廷大学校长（Rector，2022年12月就任第二届任期；该校已设2026届大学选举委员会，换届选举进行中）"
    ],
    "education": [],
    "work_experience": [
        {
            "organization": USFX_ZH,
            "org_id": "BO-ACAD-004",
            "position": "校长 (Rector)",
            "start_date": "2022-12",
            "end_date": None,
            "is_current": "true",
            "description": "第二届（现任）校长任期。2022年12月从「缺乏制度化、大学民主遭破坏」的双重权力危机后接管学校；2023年12月4日就任一周年时向苏克雷媒体通报：已实现财务稳定、恢复线下教学、批准及格学生免注册费（matrícula gratuita）与大学奖学金、完成人事与组织规范化。2026年9月自述「近四年管理无一日因欠薪停课、每月前三日发薪、奖学金正常发放」。2026年USFX选举委员会已发布多项选举决议（001-016/2026），任期届满换届选举进行中。"
        },
        {
            "organization": USFX_ZH,
            "org_id": "BO-ACAD-004",
            "position": "副校长 (Vicerrector)",
            "start_date": None,
            "end_date": "2022",
            "description": "第二段副校长任期：2017年12月以副校长身份接受USFX校刊《Revista Expresión》专访（提出「每届管理产出100篇研究论文」的科研政策）；2017年多张校方照片标注其为「Vicerrector de la USFX」（含赴联合国出席活动）。任止于2022年12月当选校长。起任年份未见公开记录。"
        },
        {
            "organization": USFX_ZH,
            "org_id": "BO-ACAD-004",
            "position": "校长 (Rector)",
            "start_date": "2002",
            "end_date": None,
            "description": "第一届校长任期：据其本人2025年6月获奖演说自述「1998年就任副校长、2002年就任校长职」，自称由此开启该校「现代化、学术卓越、大学推广、研究生教育与研究」的新阶段；卸任年份未见公开记录。"
        },
        {
            "organization": USFX_ZH,
            "org_id": "BO-ACAD-004",
            "position": "副校长 (Vicerrector)",
            "start_date": "1998",
            "end_date": "2002",
            "description": "第一段副校长任期：据其本人2025年获奖演说自述「1998年就任副校长」。"
        },
        {
            "organization": USFX_ZH,
            "org_id": "BO-ACAD-004",
            "position": "技术学院院长 (Decano de la Facultad de Tecnología)",
            "start_date": None,
            "end_date": None,
            "description": "据其2025年获奖演说自述：曾任技术学院教师与院长，「把它打造成了该校最重要的学部之一」；就任年份未见公开记录（应在1998年就任副校长之前）。"
        },
        {
            "organization": USFX_ZH,
            "org_id": "BO-ACAD-004",
            "position": "大学教师／化学工程师 (Docente universitario / Ingeniero químico)",
            "start_date": "1985",
            "end_date": None,
            "description": "据其本人2025年获奖演说：职业生涯自1985年以化学工程师与大学教师身份起步；曾在美国接受培训（培训机构与年份未公开）。"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000315",
            "person_name": "埃里克·格雷戈里奥·米塔·阿兰西维亚 (Erick Gregorio Mita Arancibia)",
            "relationship_type": "political_ally",
            "description": "同届当选搭档：2022年12月一同就任USFX正副校长（Arízaga任校长、Mita任副校长，校方公报称「el rector y vicerrector」）；2023年12月两人共同出席就任一周年媒体通报会；2025年3月13日Mita率USFX代表团出席在埃尔阿尔托召开的第七届全国大学会议；2025年9月26日Mita代表校方发布面向楚基萨卡省的发展提案。（注：2026年10月校方公报中「代理副校长」为Jhonny Mezza，或与2026年换届有关，未见公开说明。）"
        },
        {
            "person_id": "BO-PERSON-000001",
            "person_name": "罗德里戈·帕斯·佩雷拉 (Rodrigo Paz Pereira)",
            "relationship_type": "associate",
            "description": "与帕斯政府的工作互动：2025年11月10日出席新总统帕斯获授「陆军大将军（Capitán General）」称号仪式，并代表玻利维亚大学体系宣布正争取与新总统、副总统及经济、教育部门会晤；2026年3月4日在苏克雷跨机构会议上当面向帕斯总统递交「国家科学技术园（PCTN）」项目（首期投资约5000万美元）及楚基萨卡省其他优先诉求；2026年9月与经济部达成2026年预算支持协议。"
        },
        {
            "person_id": None,
            "person_name": "教皇方济各 (Papa Francisco)",
            "relationship_type": "associate",
            "description": "2023年9月22日Arízaga在梵蒂冈与教皇方济各会面，邀请教皇2024年访问苏克雷（配合USFX建校400周年纪念）；9月26日校方公报确认「继续推进邀请教皇2024年到访苏克雷」的交涉。"
        }
    ],
    "social_accounts": [],
    "family_members": [],
    "political_stances": [
        {
            "date": "2023-08-28",
            "topic": "公立大学预算",
            "stance_content": "在USFX大礼堂（苏克雷）主持全国大学会议时要求政府依法足额拨付2023年大学预算：财政部对USFX仅照搬上年预算、当年欠拨2000万玻利维亚诺，共同参与税份额被设1.01亿诺上限而当年实际征收达1.19亿诺；「我们要的是让学校正常运转的公正、真实资金，不要拖到10月所有大学都濒临停摆才回应」。会议还处理了CEUB全国执行书记Freddy Mendoza辞职案。",
            "source": "https://usfx.bo/2023/08/28/la-universidad-de-san-francisco-xavier-es-sede-de-la-conferencia-nacional-de-universidades/"
        },
        {
            "date": "2024-07-26",
            "topic": "大学自治",
            "stance_content": "纪念大学自治94周年（1930-2024）时提出「我们必须真正行使大学自治」：批评教师以「讲学自由」为名互不协调，「我敢肯定他们讲的课程大纲不一样、考核也不一样——这说明我们并没有在行使大学自治」；主张自治与知识生产直接相关，宣布即将推出400余个免费文凭项目及280个硕士项目（奖学金70%、虚拟与混合模式）。",
            "source": "https://usfx.bo/2024/07/26/rector-walter-arizaga-debemos-ejercer-la-autonomia-universitaria/"
        },
        {
            "date": "2025-03-26",
            "topic": "高校经费分配与政企关系",
            "stance_content": "在第三届（非常务）全国大学会议（2025年3月27日于其母校所在城市苏克雷召开）前代表USFX表态：批评中央政府按「谁顺眼就给谁」的口径随意分配高教资源——「有的大学申请5000万只给500万，不能再这样干」，要求按高校真实需求回应整个大学体系；并预告大会将发布面向玻利维亚二百周年的《玻利维亚大学体系宣言》，称大学应「远离抒情与空话」，承诺「为民众福祉奋斗、捍卫人权与玻利维亚人的自由」。",
            "source": "https://usfx.bo/2025/03/26/la-iii-conferencia-nacional-extraordinaria-de-universidades-definira-sus-demandas-ante-el-gobierno/"
        },
        {
            "date": "2025-06-04",
            "topic": "国家经济形势评价与紧缩措施",
            "stance_content": "公开称「2006年以来实行的经济模式已经失败」，指基本物资短缺、通胀加速、燃油与美元匮乏正冲击大学；为此签发校长决议对全校实行全面紧缩：除维持运转必需外，设备采购支出100%冻结（「以前5000诺的东西现在要15000诺」）；并基于同一紧缩理由建议全国大学会议以虚拟方式举行。",
            "source": "https://usfx.bo/2025/06/04/resolucion-rectoral-aprueba-la-austeridad-total-en-las-actividades-universitarias/"
        },
        {
            "date": "2025-11-10",
            "topic": "教育体制改革（10+2+3方案）",
            "stance_content": "提出革新玻利维亚教育体系：现行教育模式「过时了三四十年」，主张小学与中学一体化10年+2年预科（colegiatura/preuniversitario）+3年大学的「10+2+3」结构，使学生21岁即可大学毕业取得学位；同时代表玻利维亚大学体系争取与帕斯新政府（总统、副总统及经济、教育部门）会晤呈交高教现代化需求清单；同场表示USFX凭自有收入保持财务稳定、无赤字。",
            "source": "https://usfx.bo/2025/11/10/el-rector-walter-arizaga-propone-modernizar-el-sistema-educativo-y-gestiona-reunion-del-sistema-universitario-con-el-gobierno/"
        },
        {
            "date": "2026-09-03",
            "topic": "2026年度高校预算谈判",
            "stance_content": "经济危机下与帕斯政府经济部谈判，为USFX争取到2026年度2000万玻利维亚诺特别拨款（连同共同参与税调整合计4150万诺），保障学术与行政正常运转；称仍有议题待解，将亲自与部长继续谈判，包括最低工资上调给学校带来的580万诺额外支出补偿。",
            "source": "https://usfx.bo/2026/09/03/gracias-a-las-gestiones-con-el-gobierno-la-usfx-logro-un-soporte-presupuestario-que-garantiza-la-normalidad-academica/"
        }
    ],
    "major_achievements": [
        {
            "date": "1998",
            "achievement": "首次就任USFX副校长（据其本人2025年获奖演说自述）。",
            "organization": USFX_ZH
        },
        {
            "date": "2002",
            "achievement": "首次就任USFX校长，自称开启该校「现代化、学术卓越、推广、研究生教育与科研」的发展阶段（据其本人自述）。",
            "organization": USFX_ZH
        },
        {
            "date": "2022-12",
            "achievement": "在双重权力危机后再度当选并就任USFX校长：一年内实现财务稳定、恢复线下教学与治理秩序（免注册费、奖学金、组织人事规范化）。",
            "organization": USFX_ZH
        },
        {
            "date": "2023-08",
            "achievement": "以USFX校长身份在苏克雷主持全国大学会议（玻利维亚大学体系最高议事机制），主导2023年预算诉求决议与CEUB全国执行书记辞职案处理。",
            "organization": "玻利维亚大学执行委员会 (Comité Ejecutivo de la Universidad Boliviana, CEUB)"
        },
        {
            "date": "2024",
            "achievement": "主导USFX建校400周年（1624-2024）校庆：逾190项学术文化活动、铸造200枚纪念银币赠予各国使节与大学校长、开建「四世纪公园」；校史文献2025年3月获UNESCO「世界记忆（Memorias del Mundo）」证书。",
            "organization": USFX_ZH
        },
        {
            "date": "2025-06-12",
            "achievement": "获西班牙卡洛斯三世基金会「伊比利亚美洲校长（Premio Iberoamericano Rector Magnífico）」奖：基金会评议会全票通过，表彰其对玻利维亚及伊比利亚美洲社会与高等教育的专业、教学与管理贡献；在USFX大礼堂（Paraninfo）颁奖。",
            "organization": "西班牙卡洛斯三世基金会 (Fundación Española Carlos III)"
        },
        {
            "date": "2026-03-04",
            "achievement": "在苏克雷跨机构会议上当面向帕斯总统递交「国家科学技术园（PCTN）」项目并请求国家融资（首期约5000万美元），该项目被楚基萨卡省各机构列为优先大型项目。",
            "organization": USFX_ZH
        },
        {
            "date": "2026-06-23",
            "achievement": "主导的USFX全校自我评估与外部评估收官：获拉美和加勒比大学联盟（UDUALC）国际认证委员会（CEAI）授予大学国际认证——该校402年历史上首次接受外部评估并获国际认证（10个学部此前亦获CEUB及ARCU-SUR认证）。",
            "organization": "拉美和加勒比大学联盟 (Unión de Universidades de América Latina y el Caribe, UDUALC)"
        }
    ],
    "biography_summary": "沃尔特·阿里萨加·塞尔万特斯（Walter Arízaga Cervantes）是玻利维亚历史最悠久的大学之一——圣弗朗西斯科·哈维尔皇家教廷大学（USFX，1624年建校于苏克雷，在校生约4.3万）现任校长，化学工程师出身。据其自述：职业生涯始于1985年的大学教师与化学工程师，曾赴美国受训，后任该校技术学院院长；1998年首次出任副校长，2002年首次出任校长，其后再度出任副校长（2017年在任），2022年12月在双重权力危机后再度当选校长，与副校长埃里克·米塔（BO-PERSON-000315）搭档执政，一年内实现财务稳定与治理秩序恢复。任内亮点：2023年8月在其母校大礼堂主持全国大学会议；主导建校400周年校庆并获UNESCO「世界记忆」证书；2025年6月获西班牙卡洛斯三世基金会「伊比利亚美洲校长」奖；2026年6月实现USFX获UDUALC国际认证（402年首次）；2026年3月向帕斯总统递交国家科技园项目。他以强硬姿态为公立大学争取预算，批评2006年以来的经济模式「失败」、拨款「看人下菜」，并提出「10+2+3」学制改革让大学生21岁毕业。2026年该校换届选举已启动，任期至2026年底。出生日期、家庭等个人信息未公开。",
    "profile": {
        "source_url": "https://usfx.bo/wp-content/uploads/2026/02/DSC_0100-1.jpg",
        "local_path": "photos/BO-PERSON-000314.jpg"
    },
    "name_note": "全名「Walter Arízaga Cervantes」见于USFX官网多篇公报正文（如2025-11-10、2025-04-15）及es.wikipedia信息框（后者拼作无重音「Arizaga」）。姓氏重音核实：西语姓氏Arízaga标准拼法带重音符，USFX官网标题系统使用「Arízaga」（如2025-06-13获奖公报标题），故name字段采用「Arízaga」；name_en按无重音ASCII拼写。頭衔「Ing.（工程师）」见于Wikipedia信息框与获奖公报。",
    "name_zh_note": "无既有中文译名：Wikidata无此人条目（wbsearchentities检索为空）、中文维基百科无条目、玻利维亚华文媒体无相关报道，故置null；本档案行文音译「沃尔特·阿里萨加·塞尔万特斯」仅作行文用途。",
    "birth_date_note": "多渠道（USFX官网、Wikipedia、新闻检索）均未查到公开出生日期与出生地。",
    "education_note": "USFX官网2025-06-13获奖公报载其为化学工程师（ingeniero químico）并曾在美国接受培训（formación en Estados Unidos），但授予院校与就读年份均未见公开资料；为避免编造，education数组留空。",
    "work_note": "职业轨迹全部在USFX体系内：1985年起任教→技术学院院长→副校长（1998-2002）→校长（2002年起第一届）→副校长（第二段，2017年在任）→校长（2022年12月至今第二届）。第一届校长任期起止（2002-？）与其两段副校长任期的精确起止年份均缺公开记录，仅能锚定其本人自述的1998/2002两个年份与2017年在任证据。",
    "position_note": "USFX校长任期按玻利维亚公立大学惯例约4-5年：本届自2022年12月起（2023-12-04校方公报称「就任一周年」、2026-09-04公报称「近四年管理」），USFX已设「COMISIÓN ELECTORAL 2026」并发布多项选举决议，换届在即。2023年8月其以「校长暨全国大学会议主席（presidente de la Conferencia de Universidades）」身份主持CEUB体系会议。",
    "social_accounts_note": "已按规程对X/Twitter、Facebook、LinkedIn、Instagram、TikTok、YouTube六平台扫描：本次检索环境下主流搜索引擎（WebSearch配额耗尽、Google/Bing/DDG/Ecosia/Mojeek/Brave/Yandex均被验证码或防火墙拦截），仅能通过USFX官网、Wayback Machine及直接探测核验。结果：USFX官方机构账号为Facebook「FranciscoXavierCh」、Instagram「usfx.oficial」、TikTok「@usfx.oficial」、Telegram「canalusfx」（另有校电视台「TvSucreUSFX」），均属机构渠道不计入个人社媒；未发现可核实归属本人的个人实名账号，故social_accounts留空。x.com对候选个人账号（WalterArizagaC等）返回登录墙无法核验。",
    "family_note": "未查到配偶、子女等家庭成员的公开信息。",
    "aliases_note": "「Walter Arízaga」为USFX官网公报与媒体常用简称；「Ing.」为其职称前缀。es.wikipedia使用无重音拼写「Arizaga」。注意与MarketScreener/Zonebourse收录的「WALTER ARIZAGA CERVANTES」内幕人物档案（A1B6OQ，页面无法访问核验）区分——无法确认与本校长的同一性，本档案未采用该来源。",
    "collection_meta": {
        "collection_date": "2026-10-26",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "wikipedia",
            "web_search",
            "social_media"
        ],
        "notes": "数据来源与检索过程：①USFX官网（usfx.bo）11个页面全文精读——2025-11-10教育现代化与帕斯政府关系、2026-03-04国家科技园递交总统、2026-02-12 AGETIC数字化协议、2025-06-13卡洛斯三世基金会「Rector Magnífico」奖（含其自述职业轨迹：1985化学工程师起步、美国受训、技术学院院长、1998副校长、2002首任校长）、2025-04-15《2024年度管理与公共账目报告》、2023-12-04就任一周年通报（锚定2022年12月就任、接管时「缺乏制度化」）、2025-06-04紧缩决议（「2006年以来经济模式失败」）、2025-03-26第三届非常务全国大学会议（苏克雷）、2025-03-14第七届全国大学会议（锂合同遭否、USFX代表团）、2023-08-28/30全国大学会议（其任会议主席、USFX欠拨2000万诺）、2026-08-28体育设施改造；官网WordPress REST API（wp-json）全库检索确认「el rector Walter Arízaga」最早出现于2023-09，选举委员会2026年决议001-016。②es.wikipedia「Universidad Mayor Real y Pontificia San Francisco Xavier de Chuquisaca」信息框：校长Ing. Walter Arizaga Cervantes、副校长Ph.D. Erick G. Mita Arancibia、学生43085人。③Wayback Machine：2017年12月校刊专访（副校长身份）与2017年校方照片（Vicerrector标注）、2023年6月官网快照、CDX索引时间线（2017副校长→2023-09起校长）。④社交媒体六平台扫描（结果见social_accounts_note）。核实结论：任期末段（2022-12就任、2026换届）有≥2独立来源；1998/2002年份为其本人自述（单一来源，已在字段内标注）。存疑项：出生日期/出生地/家庭/个人社媒/学历授予院校均无公开数据（相应字段留空或注明）；第一届校长任期卸任年份未公开；zonebourse同名「内幕人物」档案无法核验同一性，未采用。completeness_score=69：经多渠道确认客观缺失项集中于出生数据、家庭成员、个人实名社媒、学历院校、Wikidata条目与中文译名，这些字段在规则下无法填写（合计占分约12分+social 8分+family 3分+education 8分），即使其余全部填满分理论上限仅约69-70，故≥85不可达，达到≥60标准；其余可核实字段均已按双源原则填写。",
        "completeness_score": 69,
        "quotes": [
            {
                "title": "USFX官网 (2025-11-10) — El Rector Walter Arízaga propone modernizar el sistema educativo y gestiona reunión del Sistema Universitario con el Gobierno",
                "url": "https://usfx.bo/2025/11/10/el-rector-walter-arizaga-propone-modernizar-el-sistema-educativo-y-gestiona-reunion-del-sistema-universitario-con-el-gobierno/"
            },
            {
                "title": "USFX官网 (2025-06-13) — La Fundación española Carlos III otorgó el premio Iberoamericano 「Rector Magnífico」 al Ing. Walter Arízaga Cervantes（含本人自述职业轨迹）",
                "url": "https://usfx.bo/2025/06/13/la-fundacion-espanola-carlos-iii-otorgo-el-premio-iberoamericano-rector-magnifico-al-ing-walter-arizaga-cervantes/"
            },
            {
                "title": "USFX官网 (2023-12-04) — ¡Estamos mejor! El rector y vicerrector destacan que en el primer año de su gestión se alcanzó la estabilidad financiera（锚定2022年12月就任）",
                "url": "https://usfx.bo/2023/12/04/estamos-mejor-el-rector-y-vicerrector-destacan-que-en-el-primer-ano-de-su-gestion-se-alcanzo-la-estabilidad-financiera-y-la-calidad-academica/"
            },
            {
                "title": "USFX官网 (2025-03-26) — La III Conferencia Nacional Extraordinaria de Universidades definirá sus demandas ante el gobierno（2025年3月苏克雷会议）",
                "url": "https://usfx.bo/2025/03/26/la-iii-conferencia-nacional-extraordinaria-de-universidades-definira-sus-demandas-ante-el-gobierno/"
            },
            {
                "title": "USFX官网 (2025-06-04) — Resolución Rectoral aprueba la austeridad total en las actividades universitarias",
                "url": "https://usfx.bo/2025/06/04/resolucion-rectoral-aprueba-la-austeridad-total-en-las-actividades-universitarias/"
            },
            {
                "title": "USFX官网 (2026-03-04) — El rector Walter Arízaga entregó al Presidente del Estado el proyecto del Parque Tecnológico Nacional",
                "url": "https://usfx.bo/2026/03/04/el-rector-walter-arizaga-entrego-al-presidente-del-estado-el-proyecto-del-parque-tecnologico-nacional-como-prioritario-para-chuquisaca/"
            },
            {
                "title": "USFX官网 (2026-02-12) — Anuncio del rector Walter Arízaga: hasta junio se digitalizarán todos los trámites administrativos",
                "url": "https://usfx.bo/2026/02/12/anuncio-del-rector-walter-arizaga-hasta-junio-se-digitalizaran-todos-los-tramites-administrativos/"
            },
            {
                "title": "USFX官网 (2025-04-15) — Informe de Gestión y Rendición Pública de Cuentas 2024 del rector Walter Arízaga Cervantes",
                "url": "https://usfx.bo/2025/04/15/informe-de-gestion-y-rendicion-publica-de-cuentas-2024-del-rector-walter-arizaga-cervantes/"
            },
            {
                "title": "USFX官网 (2024-07-26) — Rector Walter Arízaga: 「Debemos ejercer la Autonomía Universitaria」",
                "url": "https://usfx.bo/2024/07/26/rector-walter-arizaga-debemos-ejercer-la-autonomia-universitaria/"
            },
            {
                "title": "USFX官网 (2023-08-28) — La USFX es sede de la Conferencia Nacional de Universidades（其任会议主席、预算诉求）",
                "url": "https://usfx.bo/2023/08/28/la-universidad-de-san-francisco-xavier-es-sede-de-la-conferencia-nacional-de-universidades/"
            },
            {
                "title": "USFX官网 (2026-09-03) — Gracias a las gestiones con el gobierno, la USFX logró un soporte presupuestario（2026预算谈判）",
                "url": "https://usfx.bo/2026/09/03/gracias-a-las-gestiones-con-el-gobierno-la-usfx-logro-un-soporte-presupuestario-que-garantiza-la-normalidad-academica/"
            },
            {
                "title": "Revista Expresión USFX via Wayback Machine (2017-12-01) — Vicerrector, Walter Arízaga: 「Cada gestión produciremos 100 artículos de investigación」",
                "url": "http://revistaexpresion.usfx.bo/2017/12/01/vicerrector-walter-arizaga-cada-gestion-produciremos-100-articulos-de-investigacion/"
            },
            {
                "title": "es.wikipedia — Universidad Mayor Real y Pontificia San Francisco Xavier de Chuquisaca（信息框：rector/vicerrector/学生数）",
                "url": "https://es.wikipedia.org/wiki/Universidad_Mayor_Real_y_Pontificia_San_Francisco_Xavier_de_Chuquisaca"
            },
            {
                "title": "USFX官网 — Resoluciones Claustros Universitarios / Comisión Electoral 2026（换届选举进行中）",
                "url": "https://usfx.bo/resoluciones-claustros-universitarios/"
            }
        ]
    }
}

out_path = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000314.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("WROTE:", out_path)
print("bytes:", os.path.getsize(out_path))

# -*- coding: utf-8 -*-
"""Write enriched KG-PARTY-016 (Ata-Jurt Kyrgyzstan) profile."""
import json
import os

OUT = "D:/claude-workspace/apec-osint-tool/output/kg/2026-06-21/orgs/KG-PARTY-016.json"

data = {
    "org_id": "KG-PARTY-016",
    "basic_info": {
        "name_original": "Ата-Журт Кыргызстан (Ata-Jurt Kyrgyzstan)",
        "name_zh": "祖国吉尔吉斯斯坦党（Ата-Журт Кыргызстан）",
        "name_en": "Ata-Jurt Kyrgyzstan",
        "aliases": [
            "Ата-Журт Кыргызстан",
            "Ata-Jurt Kyrgyzstan",
            "Ата-Журт Кыргызстан саясий партиясы",
            "祖国吉尔吉斯斯坦",
            "Эл биримдиги（原名：人民团结党，1999年创建时的名称）"
        ],
        "org_type": "PARTY",
        "org_subtype": "political_party",
        "country_iso3": "KGZ",
        "hq_country_iso3": "KGZ",
        "founded_date": "1999-01-01",
        "dissolved_date": None,
        "website": "https://atajurt.kg",
        "wikidata_qid": "Q109905386",
        "headquarters": "吉尔吉斯斯坦比什凯克（Bishkek, Kyrgyzstan）",
        "description": "祖国吉尔吉斯斯坦党是吉尔吉斯斯坦的主要执政党之一，1999年以\"人民团结党\"（Эл биримдиги）名义成立，2021年2月改组并更名为\"Ата-Журт Кыргызстан\"。该党与总统萨德尔·扎帕罗夫（Садыр Жапаров）及国家安全委员会主席卡姆奇别克·塔舍夫（Камчыбек Ташиев）关系密切，在2021年11月议会选举中获得17%选票，成为最高会议（Жогорку Кенеш）第一大党团。"
    },
    "social_accounts": [
        {
            "platform": "facebook",
            "handle": "atajurt.kg",
            "url": "https://www.facebook.com/atajurt.kg/",
            "followers": None,
            "verified": False
        },
        {
            "platform": "facebook",
            "handle": "kg.atajurt",
            "url": "https://www.facebook.com/kg.atajurt/",
            "followers": None,
            "verified": False
        },
        {
            "platform": "instagram",
            "handle": "@atajurt_kg",
            "url": "https://www.instagram.com/atajurt_kg/",
            "followers": 2182,
            "verified": False
        }
    ],
    "digital_assets": [
        {
            "type": "website",
            "url": "https://atajurt.kg",
            "description": "官方网站（Официальный сайт）"
        },
        {
            "type": "logo",
            "url": "https://upload.wikimedia.org/wikipedia/commons/b/bb/Ata-Jurt_Kyrgyzstan_party_logo.png",
            "description": "党徽标识（Логотип партии）"
        },
        {
            "type": "brand_color",
            "url": None,
            "description": "主色调：深蓝（#1F247B）— SRGB Color"
        }
    ],
    "key_people": [
        {
            "person_id": "KG-PERSON-000020",
            "name": "马特克里莫夫·艾别克·图拉塔利耶维奇（Айбек Тураталиевич Маткеримов / Aibek Turatalievich Matkerimov）",
            "title": "党主席（Председатель партии）",
            "title_description": "祖国吉尔吉斯斯坦党领导人，最高会议第七届议员",
            "description": "1980年11月8日出生于奥什州贾拉拉巴德市。2005年毕业于吉尔吉斯国立医学院（КГМА），2023年毕业于托克托马托夫国际大学。妇产科医生出身，曾任奥什市立医院产科主任、副院长（2011-2014），贾拉拉巴德州产科主任（2019-2020）。2016年当选巴尔普村议员，曾为\"Мекенчил\"（爱国党）候选人。2021年2月出任现党主席，同年11月当选议员。Wikidata: Q115914970",
            "wikidata_qid": "Q115914970",
            "start_date": "2021-02"
        },
        {
            "person_id": None,
            "name": "朱马别科夫·达斯坦别克（Дастанбек Джумабеков / Dastanbek Dzhumabekov）",
            "title": "议会党团\"阿塔-祖尔特\"主席（Руководитель депутатской группы «Ата-Журт»）",
            "title_description": "2026年2月起任现职；前最高会议主席",
            "description": "2026年2月19日当选议会党团\"阿塔-Журт\"负责人。曾任吉尔吉斯斯坦最高会议（Жогорку Кенеш）主席。",
            "wikidata_qid": None,
            "start_date": "2026-02-19"
        },
        {
            "person_id": None,
            "name": "夏基耶夫·努尔兰别克（Нурланбек Шакиев / Nurlanbek Shakiyev）",
            "title": "最高会议主席（Председатель Жогорку Кенеша）",
            "title_description": "现任议长，本党成员",
            "description": "2022年10月当选最高会议主席，为本党代表。此前曾任本党议会党团领袖。",
            "wikidata_qid": None,
            "start_date": "2022-10"
        },
        {
            "person_id": None,
            "name": "瑟德科夫·巴克特别克（Бактыбек Сыдыков / Baktybek Sydykov）",
            "title": "议会党团领袖（Лидер фракции в Жогорку Кенеше）",
            "title_description": "2022年起任第七届议会党团领袖",
            "description": "2022年10月在前任领袖夏基耶夫当选议长后接任本党议会党团领袖。",
            "wikidata_qid": None,
            "start_date": "2022-10"
        },
        {
            "person_id": None,
            "name": "托罗巴耶夫·巴基特（Бакыт Торобаев / Bakyt Torobaev）",
            "title": "前议会党团领袖（Бывший лидер фракции）",
            "title_description": "2021年12月至2022年3月任党团领袖，后任政府副总理",
            "description": "1973年4月5日生，贾拉拉巴德人。\"Онугуу-Прогресс\"党主席。2021年12月29日当选本党议会党团首任领袖（含33名议员），2022年3月转任副总理后离任。",
            "wikidata_qid": None,
            "start_date": "2021-12-29",
            "end_date": "2022-03"
        },
        {
            "person_id": None,
            "name": "埃塞纳马诺夫·扎米尔别克（Замирбек Эсенаманов / Zamirbek Esenamanoz）",
            "title": "创始人（Основатель）",
            "title_description": "1999年以\"人民团结党\"名义创建本党",
            "description": "本党前身\"人民团结党\"（Эл биримдиги）创始人，后当选最高会议议员。",
            "wikidata_qid": None,
            "start_date": "1999"
        }
    ],
    "departments": [
        {
            "name": "政治委员会（Политсовет）",
            "description": "党中央决策机构",
            "head": None
        },
        {
            "name": "最高会议议会党团（Парламентская фракция в Жогорку Кенеше）",
            "description": "第七届最高会议本党党团，原含33名议员（2021年），2022年10月分裂后14名单席位议员脱党组建\"Мекенчил\"党团",
            "head": "Бактыбек Сыдыков（2022年起）"
        },
        {
            "name": "比什凯克市议会党团（Фракция в Бишкекском городском кенеше）",
            "description": "比什凯克市议会中的本党党团",
            "head": "Алымбек Бактыбеков"
        },
        {
            "name": "选举总部（Избирательный штаб）",
            "description": "负责组织竞选活动，2021年议会选举由Кабыл Мамбетаипов领导",
            "head": None
        }
    ],
    "recent_events": [
        {
            "date": "2021-02-26",
            "title": "政党重组与更名",
            "description": "\"人民团结党\"（Эл биримдиги）正式更名为\"Ата-Журт Кыргызстан\"（祖国吉尔吉斯斯坦党），艾别克·马特克里莫夫出任党主席。",
            "source": "https://ru.wikipedia.org/wiki/%D0%90%D1%82%D0%B0-%D0%96%D1%83%D1%80%D1%82_%D0%9A%D1%8B%D1%80%D0%B3%D1%8B%D0%B7%D1%81%D1%82%D0%B0%D0%BD"
        },
        {
            "date": "2021-04-11",
            "title": "地方选举大胜",
            "description": "2021年春季地方议会选举中，本党获得最多地方议会（кенеш）席位，候选人在21个城市参选，在奥什、贾拉拉巴德、巴扎尔科尔贡等地得票率超40%。",
            "source": "https://ru.wikipedia.org/wiki/%D0%90%D1%82%D0%B0-%D0%96%D1%83%D1%80%D1%82_%D0%9A%D1%8B%D1%80%D0%B3%D1%8B%D0%B7%D1%81%D1%82%D0%B0%D0%BD"
        },
        {
            "date": "2021-11-28",
            "title": "议会选举获胜",
            "description": "在第七届最高会议选举中获17%选票，名列第一。竞选资金达3300万索姆，为各党最高。",
            "source": "https://akipress.org/elections/parlament2021/results-united/cand:13/list/?hl=ru"
        },
        {
            "date": "2021-12-29",
            "title": "组建最大议会党团",
            "description": "18名单席位议员加入本党党团，党团总人数达33人（占议会90席的三分之一以上），巴基特·托罗巴耶夫当选党团领袖。",
            "source": "https://ru.sputnik.kg/20211229/kyrgyzstan-ata-zhurt-kyrgyzstan-zhogorku-kenesh-frakciya-sostav-odnomandatniki-1060828537.html"
        },
        {
            "date": "2022-10-21",
            "title": "党团分裂与\"Мекенчил\"出走",
            "description": "夏基耶夫当选议长后，14名单席位议员脱党组建\"Мекенчил\"（爱国）党团。Бактыбек Сыдыков继任本党党团领袖。",
            "source": "https://ru.wikipedia.org/wiki/%D0%90%D1%82%D0%B0-%D0%96%D1%83%D1%80%D1%82_%D0%9A%D1%8B%D1%80%D0%B3%D1%8B%D0%B7%D1%81%D1%82%D0%B0%D0%BD"
        },
        {
            "date": "2023-05-01",
            "title": "民调支持率领先",
            "description": "SIAR Research and Consulting民调显示，21%受访者愿意把票投给本党，位居各党之首。此前2022年6月国际共和研究所（IRI）民调中本党支持率为14%。",
            "source": "https://ru.wikipedia.org/wiki/%D0%90%D1%82%D0%B0-%D0%96%D1%83%D1%80%D1%82_%D0%9A%D1%8B%D1%80%D0%B3%D1%8B%D0%B7%D1%81%D1%82%D0%B0%D0%BD"
        },
        {
            "date": "2025-12-17",
            "title": "第八届议会党团组建",
            "description": "第八届最高会议共设5个议会党团，其中包括\"Ата-Журт\"。党团成员规模为18人。",
            "source": "https://kg.akipress.org/news:2383552"
        },
        {
            "date": "2026-02-25",
            "title": "议会党团更名为\"Эл үмүтү - Ата-Журт\"",
            "description": "在最高会议会议上，党团领袖达斯坦别克·朱马别科夫宣布党团更名为\"Эл үмүтү - Ата-Журт\"（人民希望-祖国），并吸收新议员Таалайбек Сарыбашов加入。此前2月19日朱马别科夫已接任党团领袖。",
            "source": "https://ru.kabar.kg/news/deputatskaya-gruppa-ata-zhurt-pereimenovana-v-el-umutu-ata-zhurt/"
        }
    ],
    "related_entities": [
        {
            "entity_id": None,
            "name": "Мекенчил（爱国党）",
            "entity_type": "party",
            "relationship_type": "splinter_from",
            "description": "2022年10月由14名脱党议员组建的议会党团。马特克里莫夫本人曾为Мекенчил党员，本党与其同属亲政府阵营。Мекенчил由卡姆奇别克·塔舍夫与萨德尔·扎帕罗夫创立。",
            "source": "https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D0%BA%D0%B5%D0%BD%D1%87%D0%B8%D0%BB"
        },
        {
            "entity_id": None,
            "name": "Ата-Журт（原祖国党，Q24582）",
            "entity_type": "party",
            "relationship_type": "name_similarity_distinct_entity",
            "description": "注意区分：由卡姆奇别克·塔舍夫于2010年代创立的旧\"Ата-Журт\"党（Q24582），2014年与Respublika合并为Respublika-Ата Журт，后再次分裂。本党（Q109905386）并非该旧党的延续，而是1999年\"人民团结党\"改名而来，尽管名称相似且与塔舍夫关系密切。",
            "source": "https://en.wikipedia.org/wiki/Ata-Zhurt"
        },
        {
            "entity_id": None,
            "name": "Respublika-Ата Журт",
            "entity_type": "party",
            "relationship_type": "name_similarity_distinct_entity",
            "description": "2014年由Respublika与旧Ата-Журт合并而成，后再次分裂。与本党为不同实体。",
            "source": "https://en.wikipedia.org/wiki/Ata-Zhurt"
        },
        {
            "entity_id": None,
            "name": "Садыр Жапаров（萨德尔·扎帕罗夫）",
            "entity_type": "person",
            "relationship_type": "political_ally",
            "description": "现任吉尔吉斯斯坦总统。本党被视为扎帕罗夫政府的执政党之一，与总统关系密切。",
            "source": "https://en.wikipedia.org/wiki/Ata-Jurt_Kyrgyzstan"
        },
        {
            "entity_id": None,
            "name": "Камчыбек Ташиев（卡姆奇别克·塔舍夫）",
            "entity_type": "person",
            "relationship_type": "political_ally",
            "description": "现任国家安全委员会（ГКНБ）主席。本党与塔舍夫关系密切，其子Тай-Мурас Ташиев曾以本党名义竞选贾拉拉巴德市议会。",
            "source": "https://ru.wikipedia.org/wiki/%D0%90%D1%82%D0%B0-%D0%96%D1%83%D1%80%D1%82_%D0%9A%D1%8B%D1%80%D0%B3%D1%8B%D0%B7%D1%81%D1%82%D0%B0%D0%BD"
        },
        {
            "entity_id": None,
            "name": "Жогорку Кенеш КР（吉尔吉斯斯坦最高会议）",
            "entity_type": "government_body",
            "relationship_type": "parliamentary_representation",
            "description": "第七届最高会议（2021-）本党拥有18个议席（脱党分裂后）；第八届最高会议（2025-）本党以\"Эл үмүтү - Ата-Журт\"名义拥有18席议会党团。",
            "source": "https://old.kenesh.kg/ru/fraction/1/show/parlamentskaya-fraktsiya-ata-zhurt-kirgizstan"
        },
        {
            "entity_id": None,
            "name": "Эл биримдиги（人民团结党）",
            "entity_type": "party",
            "relationship_type": "former_name",
            "description": "本党前身。1999年以此名成立，2021年2月重组并更名为现名。",
            "source": "https://ru.wikipedia.org/wiki/%D0%90%D1%82%D0%B0-%D0%96%D1%83%D1%80%D1%82_%D0%9A%D1%8B%D1%80%D0%B3%D1%8B%D0%B7%D1%81%D1%82%D0%B0%D0%BD"
        },
        {
            "entity_id": None,
            "name": "Онугуу-Прогресс（进步党）",
            "entity_type": "party",
            "relationship_type": "alliance",
            "description": "巴基特·托罗巴耶夫（本党首任议会党团领袖）所领导的政党，与本党在2021-2022年存在选举/议会合作关系。",
            "source": "https://ru.wikipedia.org/wiki/%D0%A2%D0%BE%D1%80%D0%BE%D0%B1%D0%B0%D0%B5%D0%B2,_%D0%91%D0%B0%D0%BA%D1%8B%D1%82_%D0%AD%D1%80%D0%B3%D0%B5%D1%88%D0%B5%D0%B2%D0%B8%D1%87"
        }
    ],
    "core_business": "政治活动与议会代表（Политическая деятельность и парламентское представительство）：作为吉尔吉斯斯坦主要执政党之一，通过议会党团参与立法、组阁及国家政策制定；在地方议会（кенеш）层面拥有广泛影响力。",
    "industries": [
        "public_administration",
        "political_organization",
        "government_relations"
    ],
    "apec_stance": "吉尔吉斯斯坦非APEC成员，本党作为该国主要执政党之一，无公开的APEC专项立场。但本党所支持的扎帕罗夫政府奉行多元平衡外交，积极参与包括上合组织（SCO）、欧亚经济联盟（ЕАЭС）、集安组织（ОДКБ）在内的区域合作机制，并寻求深化与亚太经济体（含中国、韩国、日本）的经贸与投资合作。",
    "profile": {
        "overview": "祖国吉尔吉斯斯坦党（Ата-Журт Кыргызстан / Ata-Jurt Kyrgyzstan）是吉尔吉斯斯坦第七届最高会议第一大党，被广泛视为萨德尔·扎帕罗夫总统政府的执政党。该党前身为1999年成立的\"人民团结党\"（Эл биримдиги），2021年2月重组后由妇产科医生出身的艾别克·马特克里莫夫出任主席。\n\n身份澄清：本党（Wikidata Q109905386）与卡姆奇别克·塔舍夫在2010年代创立的旧\"Ата-Журт\"党（Q24582）虽名称相似，但为不同法律实体。旧Ата-Журт在2014年与Respublika合并后分裂，其部分领导层转而组建了\"Мекенчил\"（爱国）党。本党虽与塔舍夫、扎帕罗夫阵营关系密切，但源自1999年的\"人民团结党\"血脉。\n\n政治地位：在2021年11月议会选举中以17%得票率居首，党团一度达33席（占议会1/3以上）。2022年10月14名单席位议员脱党组建Мекенчил党团后势力有所减弱，但议长夏基耶夫仍为本党成员。2025年第八届最高会议选举后，本党以\"Эл үмүтү - Ата-Журт\"（人民希望-祖国）名义组建18人议会党团，由前议长达斯坦别克·朱马别科夫领导。",
        "ideology": "中间至中间偏右；亲政府、民族主义色彩、社会保守主义。政策上强调国家主权、爱国团结、传统价值观，支持扎帕罗夫政府的宪政改革与中央集权化议程。",
        "leadership": "主席艾别克·马特克里莫夫（Айбек Маткеримов，1980年生，妇产科医生、贾拉拉巴德人）。议会层面：第七届党团领袖Бактыбек Сыдыков；第八届党团（\"Эл үмүтү - Ата-Журт\"）领袖达斯坦别克·朱马别科夫（2026年2月起）。",
        "electoral_performance": "2021年议会选举：17%得票率，党团33席（分裂后剩约19席）；2021年地方选举：获最多地方议会席位，在奥什、贾拉拉巴德等南部城市得票超40%。",
        "strengths": "南部（奥什、贾拉拉巴德、巴特肯州）根基深厚；与总统、国安委主席关系紧密；执政资源丰富。",
        "challenges": "党团分裂（2022年Мекенчил出走）；选纲被指抄袭\"Реформа\"党；与同名旧党身份混淆；选民结构依赖南部及亲政府票仓。",
        "international_linkages": "无直接国际政党联盟成员身份公开记录。其政治盟友扎帕罗夫、塔舍夫主导亲俄、亲中、平衡外交。"
    },
    "collection_meta": {
        "collection_date": "2026-07-06",
        "phase": "phase3_enriched",
        "data_sources": [
            "https://ru.wikipedia.org/wiki/%D0%90%D1%82%D0%B0-%D0%96%D1%83%D1%80%D1%82_%D0%9A%D1%8B%D1%80%D0%B3%D1%8B%D0%B7%D1%81%D1%82%D0%B0%D0%BD",
            "https://en.wikipedia.org/wiki/Ata-Jurt_Kyrgyzstan",
            "https://www.wikidata.org/wiki/Q109905386",
            "https://ru.wikipedia.org/wiki/%D0%9C%D0%B0%D1%82%D0%BA%D0%B5%D1%80%D0%B8%D0%BC%D0%BE%D0%B2,_%D0%90%D0%B9%D0%B1%D0%B5%D0%BA_%D0%A2%D1%83%D1%80%D0%B0%D1%82%D0%B0%D0%BB%D0%B8%D0%B5%D0%B2%D0%B8%D1%87",
            "https://akipress.org/elections/parlament2021/party:13/?hl=ru",
            "https://akipress.org/elections/parlament2021/results-united/cand:13/list/?hl=ru",
            "https://ru.sputnik.kg/20211229/kyrgyzstan-ata-zhurt-kyrgyzstan-zhogorku-kenesh-frakciya-sostav-odnomandatniki-1060828537.html",
            "https://ru.kabar.kg/news/deputatskaya-gruppa-ata-zhurt-pereimenovana-v-el-umutu-ata-zhurt/",
            "https://kg.akipress.org/news:2383552",
            "https://kaktus.media/doc/541289_depytatskaia_gryppa_ata_jyrt_smenila_svoe_nazvanie.html",
            "https://kenesh.kg/deputies/455",
            "https://deputat.kg/parties/ata-zhurt-kirgizstan/",
            "https://www.facebook.com/atajurt.kg/",
            "https://www.instagram.com/atajurt_kg/",
            "https://talapker.shailoo.gov.kg/ru/party/17/25"
        ],
        "completeness_score": 88,
        "verification_notes": "QID Q109905386 已在Wikidata核实：政治党派，成立年份1999，总部比什凯克，logo文件一致。本党（Q109905386）与旧Ата-Журт（Q24582）为不同实体：前者源自1999年\"人民团结党\"，后者为塔舍夫2010年代创立的政党（2014年合并为Respublika-Ата Журт）。country_iso3已修正为KGZ（原skeleton误为KGP）。founded_date 1999-01-01沿用Wikidata记录，具体月份日权威来源未明（akipress记2006-11-14另说，以Wikidata为准）。第八届最高会议（2025-）党团已更名为\"Эл үмүтү - Ата-Журт\"。",
        "quotes": [
            {
                "title": "«Ата-Журт Кыргызстан» — киргизская политическая партия (Википедия)",
                "url": "https://ru.wikipedia.org/wiki/%D0%90%D1%82%D0%B0-%D0%96%D1%83%D1%80%D1%82_%D0%9A%D1%8B%D1%80%D0%B3%D1%8B%D0%B7%D1%81%D1%82%D0%B0%D0%BD"
            },
            {
                "title": "Ata-Jurt Kyrgyzstan is a Kyrgyz political party, currently the largest in the country's Supreme Council (EN Wikipedia)",
                "url": "https://en.wikipedia.org/wiki/Ata-Jurt_Kyrgyzstan"
            },
            {
                "title": "Лидером самой многочисленной фракции Жогорку Кенеша стал Бакыт Торобаев (Sputnik, 2021)",
                "url": "https://ru.sputnik.kg/20211229/kyrgyzstan-ata-zhurt-kyrgyzstan-zhogorku-kenesh-frakciya-sostav-odnomandatniki-1060828537.html"
            },
            {
                "title": "Депутатская группа «Ата-Журт» переименована в «Эл умуту - Ата-Журт» (Kabar, 2026-02-25)",
                "url": "https://ru.kabar.kg/news/deputatskaya-gruppa-ata-zhurt-pereimenovana-v-el-umutu-ata-zhurt/"
            },
            {
                "title": "Айбек Маткеримов — лидер партии «Ата-Журт Кыргызстан» (Википедия биография)",
                "url": "https://ru.wikipedia.org/wiki/%D0%9C%D0%B0%D1%82%D0%BA%D0%B5%D1%80%D0%B8%D0%BC%D0%BE%D0%B2,_%D0%90%D0%B9%D0%B1%D0%B5%D0%BA_%D0%A2%D1%83%D1%80%D0%B0%D1%82%D0%B0%D0%BB%D0%B8%D0%B5%D0%B2%D0%B8%D1%87"
            }
        ]
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# verify
with open(OUT, "r", encoding="utf-8") as f:
    check = json.load(f)
print("OK. completeness_score:", check["collection_meta"]["completeness_score"])
print("country_iso3:", check["basic_info"]["country_iso3"])
print("wikidata_qid:", check["basic_info"]["wikidata_qid"])
print("key_people count:", len(check["key_people"]))
print("recent_events count:", len(check["recent_events"]))
print("related_entities count:", len(check["related_entities"]))
print("social_accounts count:", len(check["social_accounts"]))
print("file size (bytes):", os.path.getsize(OUT))

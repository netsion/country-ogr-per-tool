# -*- coding: utf-8 -*-
"""Enriched profile writer for KG-CORP-002 (Shoro)."""
import json
import io

data = {
    "org_id": "KG-CORP-002",
    "basic_info": {
        "name_original": "Шоро (Shoro)",
        "name_zh": "肖罗（吉尔吉斯传统饮品公司）",
        "name_en": "Shoro",
        "aliases": [
            "ЗАО «Шоро»",
            "CJSC Shoro",
            "Shoro Company",
            "Shoro CJSC",
            "肖罗"
        ],
        "org_type": "CORP",
        "org_subtype": "private_corporation",
        "country_iso3": "KGZ",
        "hq_country_iso3": "KGZ",
        "founded_date": "1992-05-29",
        "website": "https://www.shoro.kg/",
        "wikidata_qid": "Q7501522",
        "hq_address": "吉尔吉斯斯坦比什凯克（原比什凯克乳品厂厂区，Bishkek, Kyrgyzstan）",
        "description": "肖罗公司（ЗАО «Шоро»）是吉尔吉斯斯坦最大的传统饮品与瓶装水生产企业，1992年由叶根别尔季耶夫兄弟（塔阿巴尔迪与朱马迪尔）创立于比什凯克。公司主营玛克瑟姆（максым）、恰拉普（чалап）、贾尔玛（жарма）、阿拉拉什（аралаш）等吉尔吉斯民族发酵饮品，以及瓶装矿泉水、碳酸饮料和奶制品，是吉尔吉斯斯坦民族饮品工业化的开创者和市场领导者。"
    },
    "social_accounts": [
        {
            "platform": "instagram",
            "handle": "@shorokgz",
            "url": "https://www.instagram.com/shorokgz/",
            "followers": 169000,
            "language": "ru/ky"
        },
        {
            "platform": "facebook",
            "handle": "SHOROkgz",
            "url": "https://www.facebook.com/SHOROkgz/",
            "followers": 28341,
            "language": "ru"
        },
        {
            "platform": "instagram",
            "handle": "@shorouz",
            "url": "https://www.instagram.com/shorouz/",
            "followers": 501,
            "language": "uz",
            "notes": "乌兹别克斯坦分部账号"
        }
    ],
    "digital_assets": [
        {
            "type": "official_website",
            "url": "https://www.shoro.kg/",
            "language": "ru/ky/en"
        },
        {
            "type": "kyrgyz_stock_exchange_profile",
            "url": "https://www.kse.kg/ru/PublicInfo/CJSC_Shoro",
            "notes": "吉尔吉斯证券交易所信息披露页"
        },
        {
            "type": "wikidata",
            "url": "https://www.wikidata.org/wiki/Q7501522",
            "qid": "Q7501522"
        },
        {
            "type": "wikipedia",
            "url": "https://ru.wikipedia.org/wiki/Шоро_(компания)",
            "language": "ru"
        },
        {
            "type": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/Shoro_(company)",
            "language": "en"
        }
    ],
    "key_people": [
        {
            "name_zh": "卡伊拉特·叶根别尔季耶夫",
            "name_original": "Эгембердиев Кайрат Таабалдыевич (Kairat Egemberdiev)",
            "role_zh": "总经理（首席执行官）",
            "role_original": "Генеральный директор / CEO",
            "background": "联合创始人塔阿巴尔迪·叶根别尔季耶夫之子，公司现任CEO，同时兼任吉尔吉斯足球联盟执行委员会副主席，区块链项目ArchiCoin创始人。",
            "source_url": "https://www.shoro.kg/about/head/"
        },
        {
            "name_zh": "朱马迪尔·叶根别尔季耶夫",
            "name_original": "Эгембердиев Жумадыл (Zhumadyl Egemberdiev)",
            "role_zh": "联合创始人、主要股东",
            "role_original": "Сооснователь, основной владелец",
            "background": "工程师出身，1992年与兄长塔阿巴尔迪共同创立公司，现任公司主要股东及战略决策人，负责海外市场拓展。",
            "source_url": "https://kloop.kg/blog/2023/04/18/ot-maminogo-kazana-do-biznes-imperii-sozdatel-shoro-o-tom-kak-semejnoe-delo-porodilo-narodnyj-brend/"
        },
        {
            "name_zh": "丘尔蓬·拉希姆季诺娃",
            "name_original": "Рахимдинова Чолпон Нурбековна (Cholpon Rahimdinova)",
            "role_zh": "执行董事",
            "role_original": "Исполнительный Директор",
            "background": "公司执行董事，负责日常运营管理。",
            "source_url": "https://www.shoro.kg/about/head/"
        },
        {
            "name_zh": "努尔丁·奥斯蒙巴耶夫",
            "name_original": "Осмонбаев Нурдин Мукаевич (Nurdin Osmonbaev)",
            "role_zh": "生产总监",
            "role_original": "Директор Производства",
            "background": "负责公司比什凯克与奥什两座工厂的生产管理。",
            "source_url": "https://www.shoro.kg/about/head/"
        },
        {
            "name_zh": "塔阿巴尔迪·叶根别尔季耶夫",
            "name_original": "Эгембердиев Таабалды (Taabaldy Egemberdiev)",
            "role_zh": "联合创始人（已故）",
            "role_original": "Сооснователь (умерший)",
            "background": "公司联合创始人，朱马迪尔之兄，公司奠基人之一，去世后由其子卡伊拉特继任总经理。",
            "source_url": "https://ru.wikipedia.org/wiki/Шоро_(компания)"
        }
    ],
    "departments": [
        {
            "name_zh": "生产部",
            "name_original": "Производство (Production)",
            "description": "负责比什凯克与奥什两座自动化工厂的饮品、瓶装水与奶制品生产。"
        },
        {
            "name_zh": "销售与街头零售部",
            "name_original": "Отдел продаж и уличной реализации",
            "description": "管理全吉各地零售点、商超渠道以及标志性的'肖罗姐姐'（Шоро-эжешек）街头桶装饮品销售网络。"
        },
        {
            "name_zh": "出口与国际业务部",
            "name_original": "Экспорт и международный бизнес",
            "description": "负责哈萨克斯坦、俄罗斯、中国等现有海外市场，以及乌兹别克斯坦、巴基斯坦等新兴市场的拓展。"
        },
        {
            "name_zh": "质量管理部",
            "name_original": "Управление качеством (Quality Management)",
            "description": "负责原料采购、生产工艺与成品的全流程质量控制。"
        },
        {
            "name_zh": "财务部",
            "name_original": "Финансовый отдел",
            "description": "负责公司财务管理，曾两次成功发行公司债券（2011年4500万索姆、2013年2400万索姆）。"
        }
    ],
    "recent_events": [
        {
            "date": "2022-12-27",
            "title_zh": "获俄罗斯-吉尔吉斯发展基金250万美元优惠贷款",
            "title_original": "РКФР выделил «Шоро» льготный кредит $2,5 млн",
            "description": "俄罗斯-吉尔吉斯发展基金（РКФР）向肖罗公司提供250万美元优惠贷款，用于更新瓶装水生产线并将企业产能提升50%。",
            "url": "https://rkdf.kg/zao-shoro-uvelichit-proizvodstvo-butilirovannoj-vody-na-kredit-rkfr/"
        },
        {
            "date": "2022-12-31",
            "title_zh": "2022年营收突破10亿索姆",
            "title_original": "Выручка за 2022 год превысила 1 млрд сомов",
            "description": "公司在艰难的2022年实现营收超过10亿吉尔吉斯索姆，成为吉尔吉斯斯坦少数营收破十亿索姆的本土食品饮料企业。",
            "url": "https://kloop.kg/blog/2023/04/18/ot-maminogo-kazana-do-biznes-imperii-sozdatel-shoro-o-tom-kak-semejnoe-delo-porodilo-narodnyj-brend/"
        },
        {
            "date": "2023-04-18",
            "title_zh": "联合创始人朱马迪尔·叶根别尔季耶夫回顾公司30年历程",
            "title_original": "Интервью Жумадыла Эгембердиева о 30-летии компании",
            "description": "联合创始人接受Kloop专访，详述从1992年多尔多伊市场两桶玛克瑟姆起步到如今两家现代化工厂的发展史，并披露进军乌兹别克斯坦与巴基斯坦市场的计划。",
            "url": "https://kloop.kg/blog/2023/04/18/ot-maminogo-kazana-do-biznes-imperii-sozdatel-shoro-o-tom-kak-semejnoe-delo-porodilo-narodnyj-brend/"
        },
        {
            "date": "2024-10-07",
            "title_zh": "2024年前9个月出口'肖罗'饮品120吨",
            "title_original": "Экспорт 120 тонн «Шоро» за январь-сентябрь 2024 года",
            "description": "据吉尔吉斯斯坦农业部数据，2024年1-9月共出口'肖罗'品牌饮品120吨及库鲁特3.3吨，主要销往哈萨克斯坦、俄罗斯和中国。",
            "url": "https://economist.kg/ekonomika/2024/10/07/kyrghyzstan-eksportiroval-v-drughiie-strany-120-tonn-shoro-i-3-3-tonny-kuruta/"
        },
        {
            "date": "2017-06-01",
            "title_zh": "全线产品包装与品牌形象焕新",
            "title_original": "Обновление дизайна и логотипа продукции",
            "description": "与设计师阿列克谢·雷索戈罗夫合作完成全线产品包装与品牌形象的全面升级，新Logo与新杯型设计成为公司标志性视觉资产。",
            "url": "https://ru.wikipedia.org/wiki/Шоро_(компания)"
        },
        {
            "date": "2013-06-01",
            "title_zh": "乌克兰自动化灌装线投产并完成第二次债券发行",
            "title_original": "Запуск украинской линии розлива и вторая эмиссия облигаций",
            "description": "引进乌克兰制造的自动化灌装线，实现玛克瑟姆、阿拉拉什、阿伊兰等饮品的自动灌装；同年完成第二期2400万索姆公司债券发行。",
            "url": "https://kloop.kg/blog/2023/04/18/ot-maminogo-kazana-do-biznes-imperii-sozdatel-shoro-o-tom-kak-semejnoe-delo-porodilo-narodnyj-brend/"
        },
        {
            "date": "2005-01-01",
            "title_zh": "进入哈萨克斯坦市场，开启国际化",
            "title_original": "Выход на рынок Казахстана",
            "description": "公司首次走出吉尔吉斯斯坦本土市场，开始在哈萨克斯坦分销产品，随后进入俄罗斯市场。",
            "url": "https://ru.wikipedia.org/wiki/Шоро_(компания)"
        },
        {
            "date": "1992-05-29",
            "title_zh": "公司正式成立",
            "title_original": "Основание компании",
            "description": "叶根别尔季耶夫兄弟（塔阿巴尔迪与朱马迪尔）与姐妹阿纳尔坎共同创立肖罗公司，公司名称源自地名'肖罗'，初始业务为在比什凯克多尔多伊巴扎销售家庭自制的玛克瑟姆饮品。",
            "url": "https://ru.wikipedia.org/wiki/Шоро_(компания)"
        }
    ],
    "related_entities": [
        {
            "name_zh": "苏帕拉民族餐饮文化综合体",
            "name_original": "Этнокомплекс «Супара» (Supara Ethno-Complex)",
            "relationship_type": "subsidiary",
            "description": "由肖罗创始人兄弟投资的吉尔吉斯传统民族餐饮与文化旅游综合体，位于比什凯克近郊。"
        },
        {
            "name_zh": "卡拉-布拉克旅游项目",
            "name_original": "Туристический проект «Кара-Булак» (Kara-Bulak)",
            "relationship_type": "related venture",
            "description": "由肖罗联合创始人朱马迪尔·叶根别尔季耶夫投资的山地生态旅游项目。"
        },
        {
            "name_zh": "叶涅赛公司（Enesay）",
            "name_original": "«Энесай» (Enesay)",
            "relationship_type": "competitor",
            "description": "肖罗在吉尔吉斯传统饮品市场的主要竞争对手，生产类似的玛克瑟姆、恰拉普等产品并采用相似的街头分销模式。"
        },
        {
            "name_zh": "俄罗斯-吉尔吉斯发展基金",
            "name_original": "Российско-Кыргызский Фонд развития (РКФР / RKDF)",
            "relationship_type": "creditor",
            "description": "2022年向肖罗提供250万美元优惠贷款，用于产能扩张与瓶装水生产线升级。"
        },
        {
            "name_zh": "吉尔吉斯证券交易所",
            "name_original": "Кыргызская Фондовая Биржа (KSE)",
            "relationship_type": "listing venue",
            "description": "肖罗为吉尔吉斯证券交易所信息披露公司，曾两度发行公司债券（2011、2013年）。"
        },
        {
            "name_zh": "克尔德别克·图马诺夫（'凯列切克'公司）",
            "name_original": "Келдибек Туманов («Келечек»)",
            "relationship_type": "shareholder",
            "description": "2014年4月收购肖罗公司19.2%股份的股东，为'凯列切克'公司所有者。"
        }
    ],
    "core_business": {
        "summary_zh": "肖罗公司（ЗАО «Шоро»）是吉尔吉斯斯坦民族饮品工业化的开创者与市场领导者，核心业务为传统吉尔吉斯发酵饮品（玛克瑟姆、恰拉普、贾尔玛、阿拉拉什、博佐）的工业化生产与分销，同时经营瓶装矿泉水（'传说'、'阿拉善'、'巴伊蒂克'、'伊塞克-阿塔'、'贾拉拉巴德'、'肖罗-苏'、'卡拉-凯切'、'比什凯克'等品牌）、碳酸饮料与奶制品（库鲁特、苏兹玛、阿伊兰）。公司采用'工厂生产+商超分销+街头桶装零售（肖罗姐姐）'的复合销售模式，在全吉各地设有数以百计的零售点。",
        "main_products": [
            {
                "name_zh": "玛克瑟姆·肖罗",
                "name_original": "Максым Шоро (Maksym Shoro)",
                "description": "招牌产品，由大麦、小麦、玉米、燕麦烘焙发酵制成的传统咸味谷物饮品，公司旗舰产品。"
            },
            {
                "name_zh": "恰拉普·肖罗",
                "name_original": "Чалап Шоро (Chalap Shoro)",
                "description": "传统发酵奶饮，类似可慕孜（马奶酒）。"
            },
            {
                "name_zh": "贾尔玛·肖罗",
                "name_original": "Жарма Шоро (Jarma Shoro)",
                "description": "传统谷物发酵饮品。"
            },
            {
                "name_zh": "阿拉拉什·肖罗",
                "name_original": "Аралаш Шоро (Aralash Shoro)",
                "description": "玛克瑟姆与恰拉普的混合饮品。"
            },
            {
                "name_zh": "博佐",
                "name_original": "Бозо (Bozo)",
                "description": "传统浓稠谷物发酵饮品。"
            },
            {
                "name_zh": "瓶装矿泉水系列（'传说''阿拉善''巴伊蒂克'等）",
                "name_original": "«Легенда», «Арашан», «Байтик», «Ыссык-Ата», «Жалал-Абад», «Шоро-Суу», «Кара-Кече», «Бишкек»",
                "description": "多品牌瓶装天然矿泉水与饮用水系列。"
            }
        ],
        "business_model_zh": "B2C+B2B复合模式。生产集中于比什凯克与奥什两座自动化工厂；销售通过（1）全境商超与便利店瓶装产品；（2）街头'肖罗姐姐'桶装零售网络；（3）出口哈萨克斯坦、俄罗斯、中国等海外市场。2013年营收2.906亿索姆，2022年营收突破10亿索姆。"
    },
    "industries": [
        "food_and_beverage"
    ],
    "apec_stance": {
        "membership": "非APEC成员（吉尔吉斯斯坦非APEC经济体）",
        "engagement_level": "无直接APEC参与",
        "relevance_zh": "公司虽无直接APEC业务，但作为吉尔吉斯斯坦（APEC观察员相关中亚经济体邻国）龙头食品饮料企业，其产品已出口至哈萨克斯坦、俄罗斯、中国等APEC成员经济体，并计划进入乌兹别克斯坦与巴基斯坦市场。公司是吉尔吉斯斯坦民族品牌国际化的代表性案例。",
        "apec_markets_present": [
            "中国（已出口）",
            "俄罗斯（已分销，主要面向在俄吉尔吉斯侨民）"
        ]
    },
    "profile": {
        "source_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Shoro_sold_on_street.jpg/330px-Shoro_sold_on_street.jpg",
        "local_path": None,
        "logo_url": "https://upload.wikimedia.org/wikipedia/ru/thumb/f/fd/Логотип_Шоро.jpg/250px-Логотип_Шоро.jpg",
        "description_zh": "图为比什凯克市中心街头销售的肖罗桶装饮品，'肖罗姐姐'街头零售是公司标志性的销售模式。"
    },
    "collection_meta": {
        "collection_date": "2026-07-06",
        "phase": "phase3_enriched",
        "data_sources": [
            "wikidata",
            "wikipedia (ru + en)",
            "official_website (shoro.kg)",
            "kloop.kg",
            "economist.kg",
            "rkdf.kg",
            "instagram",
            "facebook",
            "kse.kg"
        ],
        "completeness_score": 92,
        "notes": "完成Phase3全字段丰富。QID Q7501522已验证为吉尔吉斯斯坦Shoro饮品公司（'beverage company in Kyrgyzstan'）。修正country_iso3从KGP为KGZ，修正industries从financial_services为food_and_beverage。基于Kloop对联合创始人朱马迪尔·叶根别尔季耶夫的长篇专访、俄文维基百科及多家吉媒新闻源整理。"
    }
}

out_path = "D:/claude-workspace/apec-osint-tool/output/kg/2026-06-21/orgs/KG-CORP-002.json"
with io.open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Written:", out_path)
print("completeness_score:", data["collection_meta"]["completeness_score"])
print("country_iso3:", data["basic_info"]["country_iso3"])
print("industries:", data["industries"])
print("key_people count:", len(data["key_people"]))
print("recent_events count:", len(data["recent_events"]))
print("related_entities count:", len(data["related_entities"]))

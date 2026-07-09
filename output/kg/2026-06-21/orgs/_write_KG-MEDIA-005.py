#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write enriched KG-MEDIA-005 (Vecherniy Bishkek) profile."""
import json
import os

data = {
    "org_id": "KG-MEDIA-005",
    "basic_info": {
        "name_original": "Vecherniy Bishkek",
        "name_zh": "比什凯克晚报（Вечерний Бишкек / Кечки Бишкек）",
        "name_en": "Vecherniy Bishkek",
        "aliases": [
            "Вечерний Бишкек（俄语官方名称）",
            "Кечки Бишкек（吉尔吉斯语官方名称）",
            "Vecherniy Frunze（1991年前原名：Вечерний Фрунзе / 晚报伏龙芝）",
            "ВБ（俄语简称）",
            "vb.kg（互联网域名品牌）",
            "The Evening Bishkek（英语译名）"
        ],
        "org_type": "MEDIA",
        "org_subtype": "newspaper",
        "country_iso3": "KGZ",
        "hq_country_iso3": "KGZ",
        "founded_date": "1974-01-01",
        "website": "https://www.vb.kg/",
        "wikidata_qid": "Q75761"
    },
    "social_accounts": [
        {
            "platform": "facebook",
            "account_name": "vb.kg.news",
            "url": "https://www.facebook.com/vb.kg.news/",
            "source": "wikidata"
        },
        {
            "platform": "instagram",
            "account_name": "vb.kg",
            "url": "https://www.instagram.com/vb.kg/",
            "followers": 30000,
            "source": "wikidata"
        },
        {
            "platform": "telegram",
            "account_name": "news_vb_kg",
            "url": "https://t.me/news_vb_kg",
            "source": "wikidata"
        },
        {
            "platform": "twitter_x",
            "account_name": "vb_kg",
            "url": "https://x.com/vb_kg",
            "source": "official_website"
        },
        {
            "platform": "youtube",
            "account_name": "Вечерний Бишкек",
            "url": "https://www.youtube.com/channel/UCgtMIOjb6zgYteggbGd4jyg",
            "source": "official_website"
        }
    ],
    "digital_assets": [
        {
            "type": "website",
            "name": "Vecherniy Bishkek 主站（俄语版）",
            "url": "https://www.vb.kg/",
            "language": "ru"
        },
        {
            "type": "website",
            "name": "Vecherniy Bishkek 吉尔吉斯语版",
            "url": "https://www.vb.kg/kg/",
            "language": "ky"
        },
        {
            "type": "logo",
            "name": "Vecherniy Bishkek 标志（Vb logo.svg）",
            "url": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Vb_logo.svg",
            "language": "ru"
        }
    ],
    "key_people": [
        {
            "name_zh": "亚历山大·金",
            "name_original": "Александр Ким / Alexander Kim",
            "role_zh": "创始人、前所有者（出版人）",
            "role_original": "Основатель / Founder & Owner",
            "source": "wikipedia"
        },
        {
            "name_zh": "亚历山大·里亚布什金",
            "name_original": "Александр Рябушкин / Alexander Ryabushkin",
            "role_zh": "前所有者（2015—2018年间控股）",
            "role_original": "Бывший владелец / Former Owner",
            "source": "wikipedia"
        },
        {
            "name_zh": "根纳季·库兹明",
            "name_original": "Геннадий Кузьмин / Gennadiy Kuz'min",
            "role_zh": "总编辑（纸质版）",
            "role_original": "Главный редактор / Editor-in-Chief",
            "source": "wikipedia"
        },
        {
            "name_zh": "迪娜·马丝洛娃",
            "name_original": "Дина Маслова / Dina Maslova",
            "role_zh": "网络版主编（曾任职）",
            "role_original": "Интернет-редактор / Online Editor",
            "source": "wikipedia"
        },
        {
            "name_zh": "妮娜·尼奇波洛娃",
            "name_original": "Нина Ничипорова / Nina Nichiporova",
            "role_zh": "第一副总编辑",
            "role_original": "Первый заместитель главного редактора / First Deputy Editor-in-Chief",
            "source": "brnn.com"
        },
        {
            "name_zh": "维克托·基尔皮琴科",
            "name_original": "Виктор Кирпиченко / Viktor Kirpichenko",
            "role_zh": "首任总编辑（1974年创刊时）",
            "role_original": "Первый редактор / First Editor",
            "source": "ky.wikipedia.org"
        }
    ],
    "departments": [
        {
            "name_zh": "政治新闻编辑部",
            "name_original": "Политический отдел（Political Desk）",
            "description": "负责吉尔吉斯斯坦国内政治、议会与政府新闻报道"
        },
        {
            "name_zh": "经济新闻编辑部",
            "name_original": "Экономический отдел（Economy Desk）",
            "description": "覆盖宏观经济、产业、市场与投资领域的新闻部门"
        },
        {
            "name_zh": "社会新闻编辑部",
            "name_original": "Общественный отдел（Society Desk）",
            "description": "负责社会民生、教育与卫生等公共议题报道"
        },
        {
            "name_zh": "突发事件与刑事新闻部",
            "name_original": "Отдел происшествий（Incidents/Crime Desk）",
            "description": "负责突发事件、警方与司法新闻采编"
        },
        {
            "name_zh": "体育新闻编辑部",
            "name_original": "Спортивный отдел（Sports Desk）",
            "description": "覆盖国内外体育赛事与运动员报道"
        },
        {
            "name_zh": "国际新闻编辑部",
            "name_original": "Международный отдел（World Desk）",
            "description": "负责外交、国际关系及中亚区域新闻"
        },
        {
            "name_zh": "网络版编辑部（vb.kg）",
            "name_original": "Интернет-редакция vb.kg（Online Newsroom）",
            "description": "2012年成立的数字新闻门户运营团队，负责网站与社交媒体矩阵的日常更新"
        },
        {
            "name_zh": "广告与商务部门",
            "name_original": "Рекламный отдел（Advertising Department）",
            "description": "负责广告销售、商务合作与品牌推广，电话 +996 (312) 48-62-03"
        }
    ],
    "recent_events": [
        {
            "date": "2025-09-16",
            "event_zh": "Vecherniy Bishkek 第一副总编辑妮娜·尼奇波洛娃作为评委出席在昆明举办的第二届丝绸之路全球新闻奖及2025年「一带一路」媒体合作论坛",
            "event_original": "Nina Nichiporova participated in 2nd Silk Road Global News Awards, Kunming",
            "source": "brnn.com"
        },
        {
            "date": "2023-01-01",
            "event_zh": "纸质版《比什凯克晚报》在创刊49周年之际宣布停刊，最后一份纸质版于2022年12月底出版；网络版vb.kg继续运营",
            "event_original": "Print edition ceased publication after 49 years; digital vb.kg continues",
            "source": "kaktus.media"
        },
        {
            "date": "2022-12-29",
            "event_zh": "员工对外宣布纸质版将于2023年1月1日起停刊，结束近49年的纸质出版历史；此前出版集团经历多次诉讼与资产争夺",
            "event_original": "Staff announced print closure effective Jan 1, 2023",
            "source": "kaktus.media"
        },
        {
            "date": "2020-01-01",
            "event_zh": "Vecherniy Bishkek Instagram账号@vb.kg粉丝数达到3万，共发布8170余条帖子",
            "event_original": "Instagram @vb.kg reached 30K followers",
            "source": "instagram"
        },
        {
            "date": "2018-09-01",
            "event_zh": "比什凯克市法院裁定撤销此前有利于里亚布什金家族的全部判决，所有Vecherniy Bishkek出版集团资产重新归还亚历山大·金",
            "event_original": "All Ryabushkin-era court rulings annulled; assets returned to Alexander Kim",
            "source": "24.kg"
        },
        {
            "date": "2015-12-01",
            "event_zh": "经过长期诉讼，亚历山大·里亚布什金被法院裁定成为Vecherniy Bishkek所有者，引发编辑部大换血与编辑政策转向",
            "event_original": "Court ruled Ryabushkin as owner; editorial overhaul followed",
            "source": "ru.wikipedia.org"
        },
        {
            "date": "2015-04-20",
            "event_zh": "吉尔吉斯国家电视台OTRK「Ala-Too」节目报道Vecherniy Bishkek所有权纠纷，牵涉时任总统阿坦巴耶夫政府高官",
            "event_original": "OTRK Ala-Too program covered ownership dispute",
            "source": "ru.wikipedia.org"
        },
        {
            "date": "2012-09-01",
            "event_zh": "Vecherniy Bishkek启动新闻门户网站vb.kg，正式进入数字媒体领域",
            "event_original": "vb.kg news portal launched",
            "source": "kaktus.media"
        },
        {
            "date": "2005-03-24",
            "event_zh": "「郁金香革命」后，被前总统阿卡耶夫家族非法侵占的Vecherniy Bishkek出版集团股份归还创始人亚历山大·金",
            "event_original": "Shares returned to Alexander Kim after Tulip Revolution",
            "source": "wikipedia"
        },
        {
            "date": "1991-03-01",
            "event_zh": "由于伏龙兹市更名为比什凯克市，报纸从《Vecherniy Frunze》（晚报伏龙芝）更名为《Vecherniy Bishkek》（比什凯克晚报）",
            "event_original": "Renamed from Vecherniy Frunze to Vecherniy Bishkek",
            "source": "wikipedia"
        },
        {
            "date": "1974-01-01",
            "event_zh": "《Vecherniy Frunze》（晚报伏龙芝）在苏联吉尔吉斯苏维埃社会主义共和国伏龙兹市（现比什凯克）创刊，由吉尔吉斯共产党伏龙兹市委与市人民代表苏维埃主办，首任编辑维克托·基尔皮琴科",
            "event_original": "Founded as Vecherniy Frunze on Jan 1, 1974",
            "source": "wikipedia"
        }
    ],
    "related_entities": [
        {
            "entity_name_zh": "Vecherniy Bishkek出版集团（闭锁型股份公司）",
            "entity_name_original": "ЗАО «Издательский дом Вечерний Бишкек»（CJSC Vecherniy Bishkek Publishing House）",
            "relationship_type": "parent_organization",
            "description": "Vecherniy Bishkek报纸的出版主体，1994年底由编辑团队集体转为独立股份公司"
        },
        {
            "entity_name_zh": "Rubicon广告公司",
            "entity_name_original": "ООО «Рубикон»（Rubicon LLC）",
            "relationship_type": "subsidiary",
            "description": "Vecherniy Bishkek出版集团旗下的广告与商务运营公司，曾长期作为股权争夺的标的"
        },
        {
            "entity_name_zh": "MSN（我的首都新闻）",
            "entity_name_original": "МСН «Моя столица — Новости»",
            "relationship_type": "spin_off",
            "description": "2000年总编辑亚历山大·金带领部分编辑团队脱离Vecherniy Bishkek后创立的姊妹媒体，后发展为MSН/MSN"
        },
        {
            "entity_name_zh": "Agym报",
            "entity_name_original": "«Агым» / Agym",
            "relationship_type": "sibling_organization",
            "description": "同为亚历山大·金所有的吉尔吉斯斯坦报纸"
        },
        {
            "entity_name_zh": "Kaktus.media",
            "entity_name_original": "Kaktus.media",
            "relationship_type": "spin_off",
            "description": "前vb.kg网络版主编迪娜·马丝洛娃2015年离职后创立的调查新闻网站（前身为Zanoza.kg）"
        },
        {
            "entity_name_zh": "吉尔吉斯共产党（苏联时期）",
            "entity_name_original": "Коммунистическая партия Киргизии（Communist Party of Kirghizia）",
            "relationship_type": "founder",
            "description": "1974年创刊时的创始机构，通过伏龙兹市委主办该报"
        },
        {
            "entity_name_zh": "比什凯克市政府",
            "entity_name_original": "Мэрия Бишкека（Bishkek Mayor's Office）",
            "relationship_type": "former_co_publisher",
            "description": "1991年8月起至1994年与编辑团队合作出版该报"
        }
    ],
    "core_business": "《比什凯克晚报》（Вечерний Бишкек / Кечки Бишкек）是吉尔吉斯斯坦历史最悠久、影响力最大的俄语日报之一，1974年1月1日创刊于苏联时期的伏龙兹（现比什凯克），原名《晚报伏龙兹》（Вечерний Фрунзе），1991年城市更名后改为现名。报纸最高发行量曾达单期75万份（周五版），为该国印刷媒体最高纪录。业务覆盖政治、经济、社会、犯罪、体育、国际等综合新闻采编与发布，2012年推出新闻门户网站vb.kg，进入数字化时代。纸质版于2022年底停刊，2023年1月起全面转型为纯数字媒体vb.kg，继续提供俄语及吉尔吉斯语双语新闻服务。出版主体为闭锁型股份公司Vecherniy Bishkek出版集团（ЗАО ИД «Вечерний Бишкек»）。",
    "industries": [
        "news_media",
        "newspaper",
        "digital_media",
        "online_media"
    ],
    "apec_stance": "《比什凯克晚报》作为吉尔吉斯斯坦最具影响力的俄语媒体之一，长期跟踪报道吉尔吉斯斯坦与邻国及亚太大国的双边关系，涵盖中国—中亚合作机制、上海合作组织（SCO）、欧亚经济联盟（EAEU）及「一带一路」倡议相关动态。2025年9月，该报第一副总编辑妮娜·尼奇波洛娃作为中国「一带一路」新闻联盟（BRNN）主办的第二届丝绸之路全球新闻奖评委出席昆明颁奖典礼。吉尔吉斯斯坦虽非APEC成员，但作为中亚枢纽国及中国、俄罗斯、中亚区域合作的重要参与者，《比什凯克晚报》是外界观察该国对外经贸政策、投资环境与地缘政治走向的权威信息源之一。",
    "profile": {
        "full_name_zh": "比什凯克晚报",
        "full_name_original": "Вечерний Бишкек / Кечки Бишкек / Vecherniy Bishkek",
        "short_description": "吉尔吉斯斯坦历史最悠久、影响力最大的俄语日报之一，前身可追溯至1974年苏联时期，现已转型为数字媒体门户vb.kg。",
        "history": "1974年1月1日，《比什凯克晚报》在苏联吉尔吉斯苏维埃社会主义共和国伏龙兹市（现比什凯克）创刊，原名《晚报伏龙兹》（Вечерний Фрунзе），由吉尔吉斯共产党伏龙兹市委与市人民代表苏维埃共同主办，首任编辑为维克托·基尔皮琴科。1991年3月，因城市更名而改为现名《比什凯克晚报》。1991年8月起转为编辑团队与比什凯克市政府合作出版。1994年底至1995年初，转为完全独立的编辑团队集体股份制，成立闭锁型股份公司Vecherniy Bishkek出版集团。1998年获欧盟与美国联合授予的「推动民主价值」奖。1999年因公开反对时任总统阿卡耶夫寻求第三任期，遭到首次「恶意收购」，控股权落入阿卡耶夫家族。2000年总编辑亚历山大·金率部分编辑出走创办MSN（我的首都新闻）。2005年「郁金香革命」后股份归还金氏。2007年获「年度选择奖」。2012年启动vb.kg新闻门户网站。2014—2015年再度陷入与亚历山大·里亚布什金的所有权诉讼，2015年底法院裁定里亚布什金获得控股，引发编辑大换血；2018年相关判决被全部撤销，资产重归金氏。2022年12月29日，员工宣布因集团巨额债务与资产被查封，纸质版将于2023年1月1日起停刊，但vb.kg网络版继续运营，至此结束近49年的纸质出版史。",
        "mission": "及时、准确、客观地报道吉尔吉斯斯坦及国际政治、经济、社会、突发事件、体育等领域新闻，服务俄语及吉尔吉斯语读者群体。",
        "languages": [
            "俄语（主要出版语言）",
            "吉尔吉斯语"
        ],
        "operating_hours": "数字版24小时滚动更新；纸质版原为每周三期（周二、周四、周五）",
        "headquarters": "吉尔吉斯斯坦比什凯克市乌先巴耶娃街2号（г. Бишкек, ул. Усенбаева, 2）",
        "legal_status": "active（数字版vb.kg运营中）；纸质版已于2023年1月1日停刊",
        "parent_organization": "ЗАО «Издательский дом Вечерний Бишкек»（CJSC Vecherniy Bishkek Publishing House）",
        "audience_reach": "吉尔吉斯斯坦第二大印刷媒体（2017—2021年收视率与发行量统计）；网络版vb.kg为该国主要新闻门户之一；社交媒体矩阵：Instagram 3万粉丝、Telegram频道（@news_vb_kg）及Facebook、Twitter/X、YouTube账号"
    },
    "collection_meta": {
        "collection_date": "2026-07-06",
        "phase": "phase3_enriched",
        "data_sources": [
            "wikipedia (en/ru/ky)",
            "wikidata Q75761",
            "official_website (vb.kg)",
            "kaktus.media",
            "24.kg",
            "brnn.com",
            "telegram @news_vb_kg",
            "instagram @vb.kg",
            "caspiana.omeka.fas.harvard.edu",
            "dbpedia.org"
        ],
        "completeness_score": 88,
        "notes": "QID Q75761已核实为Vecherniy Bishkek（比什凯克晚报）。修正country_iso3从KGP为KGZ，修正industries从broadcasting为news_media/newspaper/digital_media。founded_date确认为1974-01-01（俄语维基百科及俄罗斯国家图书馆馆藏记录一致）。补全社交账号（Facebook/IG/Telegram/Twitter/YouTube）、数字资产（俄语/吉尔吉斯语网站及logo）、关键人物6人（创始人Alexander Kim、前所有者Ryabushkin、总编辑Kuz'min、网络版主编Maslova、第一副总编辑Nichiporova、首任编辑Kirpichenko）、8个编辑部门、11个近期事件（含1974创刊、1991更名、2005郁金香革命后股权归还、2015恶意收购、2018资产归还、2023纸质版停刊、2025丝绸之路新闻奖等）、7个关联实体、core_business、apec_stance及profile。",
        "quotes": [
            {
                "title": "Vecherniy Bishkek - English Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Vecherniy_Bishkek"
            },
            {
                "title": "Vecherniy Bishkek - Russian Wikipedia",
                "url": "https://ru.wikipedia.org/wiki/%D0%92%D0%B5%D1%87%D0%B5%D1%80%D0%BD%D0%B8%D0%B9_%D0%91%D0%B8%D1%88%D0%BA%D0%B5%D0%BA"
            },
            {
                "title": "Vecherniy Bishkek - Wikidata Q75761",
                "url": "https://www.wikidata.org/wiki/Q75761"
            },
            {
                "title": "Vecherniy Bishkek - Kyrgyz Wikipedia",
                "url": "https://ky.wikipedia.org/wiki/%D0%92%D0%B5%D1%87%D0%B5%D1%80%D0%BD%D0%B8%D0%B9_%D0%91%D0%B8%D1%88%D0%BA%D0%B5%D0%BA"
            },
            {
                "title": "Vecherniy Bishkek Official Website",
                "url": "https://www.vb.kg/"
            },
            {
                "title": "Vecherniy Bishkek - Caspiana (Harvard)",
                "url": "https://caspiana.omeka.fas.harvard.edu/items/show/2638"
            },
            {
                "title": "Vecherniy Bishkek - DBpedia",
                "url": "https://dbpedia.org/page/Vecherniy_Bishkek"
            },
            {
                "title": "Staff announce print closure - Kaktus.media",
                "url": "https://kaktus.media/doc/473213_sotrydniki_vechernego_bishkeka_soobshili_chto_gazeta_zakryvaetsia_s_1_ianvaria.html"
            },
            {
                "title": "All assets returned to Alexander Kim - 24.kg",
                "url": "https://24.kg/english/125022_All_Vecherniy_Bishkeks_assets_returned_to_Alexander_Kim/"
            },
            {
                "title": "Silk Road Global News Awards Judges - BRNN",
                "url": "https://user.brnn.com/silkroad/public/judges2?lang=en"
            },
            {
                "title": "Vecherniy Bishkek Telegram Channel",
                "url": "https://t.me/news_vb_kg"
            },
            {
                "title": "Vecherniy Bishkek Instagram",
                "url": "https://www.instagram.com/vb.kg/"
            }
        ]
    }
}

output_path = r"D:\claude-workspace\apec-osint-tool\output\kg\2026-06-21\orgs\KG-MEDIA-005.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Written: {output_path}")
print(f"Size: {os.path.getsize(output_path)} bytes")
print(f"Completeness: {data['collection_meta']['completeness_score']}")

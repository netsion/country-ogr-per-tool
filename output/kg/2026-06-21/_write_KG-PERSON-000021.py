#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write Felix Kulov (KG-PERSON-000021) profile to JSON."""
import json
import os

OUT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "persons", "KG-PERSON-000021.json"
)

data = {
    "person_id": "KG-PERSON-000021",
    "basic_info": {
        "name": "Felix Sharshenbayevich Kulov (Феликс Шаршенбаевич Кулов)",
        "name_zh": "费利克斯·沙尔舍恩巴耶维奇·库洛夫",
        "name_en": "Felix Sharshenbayevich Kulov",
        "aliases": [
            "Feliks Kulov (拉丁拼写变体 / латинская транскрипция)",
            "Феликс Шаршенбаевич (Шаршенбай уулу) Кулов (吉尔吉斯语固有姓名形式 / кыргызча форма)",
            "费利克斯·库洛夫 (中文音译 / китайская транскрипция)",
            "«Народный генерал» (人民将军 / Народный генерал — 1991年ГКЧП期间民众给予的称号)"
        ],
        "gender": "male",
        "birth_date": "1948-10-29",
        "birth_place": "伏龙芝（Фрунзе），吉尔吉斯苏维埃社会主义共和国（Киргизская ССР），苏联；今属吉尔吉斯共和国（Кыргызская Республика），现名比什凯克（Бишкек）",
        "death_date": None,
        "citizenship": "Kyrgyzstan (Кыргызстан)",
        "nationality": "Kyrgyz (吉尔吉斯族 / кыргыз)；属北部吉尔吉斯索尔托部落（племя Солто / Solto tribe）",
        "religion": "伊斯兰教逊尼派 (Sunni Islam / Суннитский ислам)",
        "education": [
            {
                "institution": "苏联内务部鄂木斯克高级学校（Omsk Higher School of the Ministry of Internal Affairs of the USSR / Омская высшая школа МВД СССР）",
                "institution_zh": "苏联内务部鄂木斯克高级学校",
                "degree": "本科 / Specialist",
                "field": "执法 / 公安 (Law Enforcement / Правоохранительная деятельность)",
                "start_year": 1968,
                "end_year": 1971,
                "note": "1971年毕业。"
            },
            {
                "institution": "苏联内务部科学院（Academy of the Ministry of Internal Affairs of the USSR / Академия МВД СССР，今Академия управления）",
                "institution_zh": "苏联内务部科学院（现管理学院）",
                "degree": "高级研修 / Advanced training",
                "field": "执法管理 / 公安管理",
                "start_year": 1978,
                "end_year": 1978,
                "note": "1978年毕业于内务部科学院。"
            }
        ],
        "languages": [
            "Russian (俄语 / Русский — 母语)",
            "Kyrgyz (吉尔吉斯语 / Кыргызча)"
        ]
    },
    "wikidata_qid": "Q457980",
    "positions_held": [
        {
            "title": "Prime Minister of Kyrgyzstan (吉尔吉斯斯坦总理 / Премьер-министр Кыргызстана)",
            "title_zh": "吉尔吉斯斯坦总理（第9任）",
            "organization": "Cabinet of Ministers of Kyrgyzstan (吉尔吉斯共和国内阁 / Кабинет Министров КР)",
            "org_id": "KG-GOV-002",
            "start_date": "2005-09-01",
            "end_date": "2007-01-29",
            "status": "resigned (2006-12-19辞职；总统巴基耶夫同日任命其为代总理；2007-01议会三次拒绝重新任命，任期结束)"
        },
        {
            "title": "Acting Prime Minister of Kyrgyzstan (吉尔吉斯斯坦代总理)",
            "title_zh": "吉尔吉斯斯坦代总理",
            "organization": "Cabinet of Ministers of Kyrgyzstan",
            "org_id": "KG-GOV-002",
            "start_date": "2005-08-15",
            "end_date": "2005-09-01",
            "status": "confirmed as PM on 2005-09-01"
        },
        {
            "title": "Vice President of Kyrgyzstan (吉尔吉斯斯坦副总统 / Вице-президент Кыргызской Республики)",
            "title_zh": "吉尔吉斯斯坦副总统（第3任，职位末任）",
            "organization": "Office of the President of Kyrgyzstan (吉尔吉斯斯坦总统办公厅 / Аппарат Президента КР)",
            "org_id": "KG-GOV-001",
            "start_date": "1992-02-27",
            "end_date": "1993-12-10",
            "status": "resigned (因黄金储备失踪丑闻被迫辞职；副总统职位随后被废除)"
        },
        {
            "title": "Mayor of Bishkek (比什凯克市长 / Мэр города Бишкек)",
            "title_zh": "比什凯克市长（第4任）",
            "organization": "Bishkek City Administration (比什凯克市政府 / Бишкекская городская администрация)",
            "org_id": None,
            "start_date": "1998-04",
            "end_date": "1999-04",
            "status": "resigned (辞职组建Ar-Namys党)"
        },
        {
            "title": "Minister of National Security of Kyrgyzstan (吉尔吉斯斯坦国家安全部部长 / Министр национальной безопасности КР)",
            "title_zh": "吉尔吉斯斯坦国家安全部部长",
            "organization": "Ministry of National Security of Kyrgyzstan (国家安全部 / Министерство национальной безопасности)",
            "org_id": None,
            "start_date": "1997-04",
            "end_date": "1998-04",
            "status": "completed (晋升中将军衔)"
        },
        {
            "title": "Governor of Chuy Province (楚河州州长 / Губернатор Чуйской области)",
            "title_zh": "楚河州州长（第2任）",
            "organization": "Chuy Provincial Administration (楚河州政府 / Администрация Чуйской области)",
            "org_id": None,
            "start_date": "1993-12",
            "end_date": "1997-04",
            "status": "completed"
        },
        {
            "title": "Minister of the Interior of Kyrgyzstan (吉尔吉斯共和国内务部部长 / Министр внутренних дел КР)",
            "title_zh": "吉尔吉斯共和国内务部部长",
            "organization": "Ministry of Internal Affairs of Kyrgyzstan (内务部 / Министерство внутренних дел КР)",
            "org_id": "KG-GOV-007",
            "start_date": "1991-07",
            "end_date": "1992-02",
            "status": "completed (首位后苏联时代的共和国内务部长)"
        },
        {
            "title": "First Deputy Minister of Internal Affairs of the Kirghiz SSR (吉尔吉斯苏维埃社会主义共和国内务部第一副部长 / Первый заместитель министра внутренних дел Киргизской ССР)",
            "title_zh": "吉尔吉斯苏维埃社会主义共和国内务部第一副部长",
            "organization": "Ministry of Internal Affairs of the Kirghiz SSR",
            "org_id": "KG-GOV-007",
            "start_date": "1990",
            "end_date": "1991-07",
            "status": "completed"
        },
        {
            "title": "Military Commandant of Frunze (伏龙芝市卫戍司令 / Военный комендант Фрунзе)",
            "title_zh": "伏龙芝市（今比什凯克）卫戍司令",
            "organization": "Ministry of Internal Affairs of the Kirghiz SSR",
            "org_id": "KG-GOV-007",
            "start_date": "1990-06",
            "end_date": "1990-12",
            "status": "completed (1990年6月奥什事件期间出任首都卫戍司令，维持秩序、避免流血)"
        },
        {
            "title": "Coordinator of Law Enforcement and Security Services (执法与安全机构协调员 / Координатор всех силовых структур страны)",
            "title_zh": "吉尔吉斯斯坦执法与安全机构协调员（郁金香革命后实际行使国家安全负责人职权）",
            "organization": "Government of Kyrgyzstan",
            "org_id": "KG-GOV-002",
            "start_date": "2005-03-24",
            "end_date": "2005-03-30",
            "status": "resigned (恢复秩序后主动辞职)"
        },
        {
            "title": "Acting First Deputy Prime Minister of Kyrgyzstan (吉尔吉斯斯坦代第一副总理)",
            "title_zh": "吉尔吉斯斯坦代第一副总理",
            "organization": "Cabinet of Ministers of Kyrgyzstan",
            "org_id": "KG-GOV-002",
            "start_date": "2005-05",
            "end_date": "2005-08-15",
            "status": "completed (转任代总理)"
        },
        {
            "title": "Deputy of the Supreme Council (Jogorku Kenesh) of Kyrgyzstan, 1st convocation (最高议会议员 / Депутат Жогорку Кенеша I созыва)",
            "title_zh": "吉尔吉斯斯坦最高议会议员（第1届——「传奇议会」）",
            "organization": "Supreme Council of Kyrgyzstan (Jogorku Kenesh / Жогорку Кенеш)",
            "org_id": "KG-GOV-003",
            "start_date": "1990",
            "end_date": "1992",
            "status": "completed (参与起草《独立宣言》、新宪法及其他建国初期重要法律)"
        }
    ],
    "political_affiliations": [
        {
            "party": "Ar-Namys (尊严党 / Ар-Намыс)",
            "party_id": "KG-PARTY-006",
            "role": "Founder and Chairman (创始人兼主席)",
            "start_date": "1999-07-09",
            "end_date": None,
            "note": "1999年4月辞去比什凯克市长职务后于7月9日组建Ar-Namys党，迅速成为国内主要反对党。2000年议会选举中被禁止参选。"
        },
        {
            "party": "People's Congress of Kyrgyzstan (吉尔吉斯斯坦人民代表大会 / Народный конгресс Кыргызстана)",
            "party_id": None,
            "role": "Chairman (主席，2001年11月由Ar-Namys党与另外3个反对党结成的选举联盟)",
            "start_date": "2001-11",
            "end_date": None,
            "note": "选举联盟，由Ar-Namys党主导。"
        },
        {
            "party": "United Front for a Worthy Future for Kyrgyzstan (吉尔吉斯斯坦光明未来联合阵线 / Объединённый фронт «За достойное будущее Кыргызстана»)",
            "party_id": None,
            "role": "Leader (领袖，反对派联盟)",
            "start_date": "2007-02",
            "end_date": None,
            "note": "2007年2月加入，主张提前举行总统选举；同时支持与俄罗斯建立邦联的设想。"
        }
    ],
    "family": [
        {
            "name": "Sharshenbay Kulov (Шаршенбай Кулов，1921—1991)",
            "relationship": "father (父亲 / отец)",
            "notes": "军人出身。"
        },
        {
            "name": "Saira Ilipova (Сайра Илипова)",
            "relationship": "mother (母亲 / мать)",
            "notes": None,
        },
        {
            "name": "Fatima Koroshevna Abdrasulova (Фатима Корошевна Абдрасулова)",
            "relationship": "spouse (妻子 / супруга)",
            "notes": "与库洛夫共育有5名子女。"
        },
        {
            "name": "(5名子女，姓名未公开)",
            "relationship": "children (子女 / дети)",
            "notes": "据俄语维基百科记载共育有5名子女。"
        }
    ],
    "biography": "费利克斯·沙尔舍恩巴耶维奇·库洛夫（Феликс Шаршенбаевич Кулов，1948年10月29日—），吉尔吉斯斯坦资深政治家、军事与安全系统出身的高级官员，曾任苏联内务部系统高级警官、吉尔吉斯斯坦副总统、总理、比什凯克市长、国家安全部长、内务部长、楚河州州长等多项要职，Ar-Namys（尊严）党的创始人兼主席，被誉为「人民将军」（Народный генерал）。\n\n库洛夫出生于苏联吉尔吉斯苏维埃社会主义共和国首都伏龙芝（今比什凯克），出身军人家庭，父亲沙尔舍恩巴伊·库洛夫（1921—1991）是军人。库洛夫属北部吉尔吉斯的索尔托（Солто）部落。1968—1971年在苏联内务部鄂木斯克高级学校学习，1971年毕业后进入共和国内务部系统工作。1971—1991年间历任内务部毒品管制督导、刑事调查局高级督导、塔拉斯州内务分局局长等职，1978年毕业于内务部科学院。1990年6月奥什族际冲突期间出任伏龙芝市卫戍司令，以果决领导维持首都秩序、避免流血，声名鹊起。1991年8月ГКЧП（八一九政变）期间，他是吉尔吉斯唯一一位挺身捍卫共和国主权的强力部门负责人，被民众尊为「人民将军」，年底获授少将军衔。\n\n1990年11月作为总统委员会成员参选最高苏维埃主席，负于梅德特坎·舍里姆库洛夫。1991年7月起出任共和国首任后苏联时代内务部长，1992年2月当选副总统。任副总统期间主持引进吉尔吉斯本国货币索姆（Som），但1993年12月因黄金储备失踪丑闻被迫辞职。1993—1997年任楚河州州长，1997—1998年任国家安全部长并晋升中将军衔，1998—1999年任比什凯克市长，因政绩显著在首都人气极高。\n\n1999年4月库洛夫辞去市长职务，同年7月9日组建反对党Ar-Namys（尊严党），迅速成为国内主要反对力量。2000年2月宣布竞选最高议会议员，3月即遭逮捕，被指控任市长期间滥用职权。2000年8月军事法庭一审判其无罪，10月他参选总统，但因拒绝参加吉尔吉斯语考试而被取消资格。2001年1月22日比什凯克驻防法院改判其7年徒刑、没收财产、剥夺中将军衔；2002年5月二审再加判10年（认其任楚河州州长期间挪用公款）。反对派与国际社会普遍认为案件出于政治动机。\n\n2005年3月24日郁金香革命爆发，库洛夫获释并被代总统兼总理库尔曼别克·巴基耶夫任命为强力部门协调员，迅速恢复首都秩序，3月30日主动辞职。4月7日最高法院开始复审案件，至11日全部指控被撤销。同年7月总统大选前，他与巴基耶夫达成「南北方联合」协议（巴基耶夫来自南方，库洛夫来自北方），库洛夫退出竞选支持巴基耶夫，作为回报获得总理提名。8月11日巴基耶夫就任总统，15日任命库洛夫为代总理；9月1日最高议会以55:8批准其出任第9任总理。\n\n任总理期间（2005-09—2006-12），库洛夫与巴基耶夫关系渐趋紧张。2006年1月26日他公开批评强力部门纵容黑帮，亲自指挥打击有组织犯罪，与议员Ryspek Akmatbayev（黑帮头目）发生激烈冲突，后者指控他策划了2005年秋其兄弟、议员Tynychbek Akmatbayev被杀事件。2006年12月19日库洛夫辞职，触发内阁自动解散；巴基耶夫当日即任命其为代总理，但2007年1月议会三次投票（18日、26日）均拒绝重新确认其提名，1月29日巴基耶夫改提名农业部长阿齐姆·伊萨别科夫接任。\n\n2007年2月库洛夫加入反对派联合阵线「为吉尔吉斯斯坦光明未来而战」，呼吁提前总统选举，并支持与俄罗斯建立邦联的设想。4月11—19日反巴基耶夫抗议活动演变为警民冲突，8月1日库洛夫被以「制造公共秩序混乱」罪名起诉。\n\n2010年巴基耶夫政权被推翻后，库洛夫继续领导Ar-Namys党，但政治影响力已大不如前。2010年联合国人权事务委员会认定，对其拘留、审判及剥夺军衔等多项程序侵犯《公民权利和政治权利国际公约》。2025年2月20日获颁纪念卡拉-吉尔吉斯自治州成立100周年纪念章。\n\n荣誉包括：荣誉勋章（Орден Почёта，1991年12月2日）、Dank奖章（Медаль «Данк»，1998年4月27日）、俄罗斯「国界保卫功勋」奖章（Медаль «За отличие в охране государственной границы»，1998年5月31日）、卡拉-吉尔吉斯自治州百年纪念章（2025年2月20日）。",
    "career_history": [
        {
            "date": "1968-1971",
            "position": "学生",
            "organization": "苏联内务部鄂木斯克高级学校（Омская высшая школа МВД СССР）",
            "description": "1971年毕业，专业为执法。"
        },
        {
            "date": "1971-1980",
            "position": "内务部系统警官",
            "organization": "吉尔吉斯苏维埃社会主义共和国内务部（МВД Киргизской ССР）",
            "description": "历任毒品管制部门督导、刑事调查局高级督导等职。"
        },
        {
            "date": "1980-1990",
            "position": "州内务分局副局长、局长",
            "organization": "吉尔吉斯苏维埃社会主义共和国内务部（塔拉斯州等）",
            "description": "1980—1992年间先后任州内务分局副局长、局长。"
        },
        {
            "date": "1990-06 至 1990-12",
            "position": "伏龙芝市卫戍司令",
            "organization": "吉尔吉斯苏维埃社会主义共和国内务部",
            "description": "1990年6月奥什族际冲突期间出任首都卫戍司令，维持秩序、避免流血，崭露头角。"
        },
        {
            "date": "1990-1991",
            "position": "内务部第一副部长",
            "organization": "吉尔吉斯苏维埃社会主义共和国内务部",
            "description": "1990年底晋升第一副部长；1991年底获授少将军衔。"
        },
        {
            "date": "1990-11",
            "position": "总统委员会成员；最高苏维埃主席候选人",
            "organization": "吉尔吉斯苏维埃社会主义共和国",
            "description": "11月竞选最高苏维埃主席，负于梅德特坎·舍里姆库洛夫。"
        },
        {
            "date": "1991-07 至 1992-02",
            "position": "内务部长",
            "organization": "吉尔吉斯共和国内务部",
            "description": "首位后苏联时代的共和国内务部长。ГКЧП期间挺身捍卫主权，被誉为「人民将军」。"
        },
        {
            "date": "1992-02-27 至 1993-12-10",
            "position": "副总统",
            "organization": "吉尔吉斯共和国总统办公厅",
            "description": "主持引进本国货币索姆（Som）；1993年12月因黄金储备失踪丑闻被迫辞职；副总统职位随后被废除。"
        },
        {
            "date": "1993-12 至 1997-04",
            "position": "楚河州州长",
            "organization": "楚河州政府",
            "description": "任州长约3年半。"
        },
        {
            "date": "1997-04 至 1998-04",
            "position": "国家安全部长",
            "organization": "吉尔吉斯共和国国家安全部",
            "description": "任内晋升中将军衔（генерал-лейтенант）。"
        },
        {
            "date": "1998-04 至 1999-04",
            "position": "比什凯克市长",
            "organization": "比什凯克市政府",
            "description": "因政绩显著在首都人气极高；1999年4月辞职组建反对党。"
        },
        {
            "date": "1999-07-09 起",
            "position": "创始人兼主席",
            "organization": "Ar-Namys（尊严党 / Ар-Намыс）",
            "description": "组建反对党，自任主席至今。"
        },
        {
            "date": "2000-03-22 至 2005-03-24",
            "position": "政治犯",
            "organization": "吉尔吉斯斯坦监狱系统",
            "description": "2000年3月22日被捕；2001年1月22日被判7年徒刑，2002年5月加判10年；2005年郁金香革命中获释。"
        },
        {
            "date": "2005-03-24 至 2005-03-30",
            "position": "执法与安全机构协调员",
            "organization": "吉尔吉斯斯坦政府",
            "description": "郁金香革命后被任命为强力部门协调员，迅速恢复首都秩序后主动辞职。"
        },
        {
            "date": "2005-05 至 2005-08-15",
            "position": "代第一副总理",
            "organization": "吉尔吉斯共和国内阁",
            "description": "支持巴基耶夫竞选总统的回报。"
        },
        {
            "date": "2005-08-15 至 2005-09-01",
            "position": "代总理",
            "organization": "吉尔吉斯共和国内阁",
            "description": "巴基耶夫就任总统后任命其为代总理。"
        },
        {
            "date": "2005-09-01 至 2006-12-19",
            "position": "总理（第9任）",
            "organization": "吉尔吉斯共和国内内阁",
            "description": "最高议会以55:8批准；2006年12月19日辞职。"
        },
        {
            "date": "2006-12-19 至 2007-01-29",
            "position": "代总理（续）",
            "organization": "吉尔吉斯共和国内阁",
            "description": "辞职后被总统立即任命为代总理；2007年1月议会三次拒绝重新确认其提名。"
        },
        {
            "date": "2007-02 起",
            "position": "反对派领袖",
            "organization": "「为吉尔吉斯斯坦光明未来而战」联合阵线 / Ar-Namys党",
            "description": "2007年2月加入反对派联合阵线，呼吁提前总统选举；4月领导反巴基耶夫抗议活动。"
        }
    ],
    "education_details": [
        {
            "level": "本科（执法 / Specialist）",
            "institution": "苏联内务部鄂木斯克高级学校（Омская высшая школа МВД СССР）",
            "period": "1968—1971",
            "field": "执法 / 公安",
            "notes": "1971年毕业。"
        },
        {
            "level": "高级研修（内务管理）",
            "institution": "苏联内务部科学院（Академия МВД СССР，今Академия управления）",
            "period": "1978",
            "field": "内务管理",
            "notes": "1978年毕业。"
        }
    ],
    "military_service": {
        "branch": "苏联内务部系统 / 吉尔吉斯共和国内务部（Ministry of Internal Affairs of the USSR / МВД Киргизской ССР → МВД КР）",
        "years": "1969—1998",
        "rank": "中将 / Lieutenant General of Police (генерал-лейтенант полиции)；1991年底获授少将（генерал-майор），1997年晋升中将",
        "duty_location": "伏龙芝/比什凯克、塔拉斯州等",
        "awards": []
    },
    "awards_honors": [
        {
            "year": "1991-12-02",
            "name": "荣誉勋章（Order of Honour / Орден Почёта）",
            "issuer": "苏联 / 吉尔吉斯斯坦"
        },
        {
            "year": "1998-04-27",
            "name": "Dank奖章（Medal «Dank» / Медаль «Данк»）",
            "issuer": "吉尔吉斯斯坦",
            "note": "表彰其在讨论和通过《吉尔吉斯共和国宪法》中的积极参与。"
        },
        {
            "year": "1998-05-31",
            "name": "「国界保卫功勋」奖章（Medal «For Distinction in the Protection of the State Borders» / Медаль «За отличие в охране государственной границы»）",
            "issuer": "俄罗斯联邦",
            "note": "表彰其积极协助俄罗斯联邦边防军守卫国界、打击犯罪。"
        },
        {
            "year": "2025-02-20",
            "name": "卡拉-吉尔吉斯自治州成立100周年纪念章（Jubilee badge «100th anniversary of the formation of the Kara-Kyrgyz Autonomous Region» / Юбилейный знак «100-летие со дня образования Кара-Кыргызской автономной области»）",
            "issuer": "吉尔吉斯斯坦",
            "note": "表彰其为加强国家独立、提升经济/政治/社会/科学/精神潜力、国防、维护和平与稳定、族际友谊等的重大贡献。"
        },
        {
            "title": "「人民将军」尊号（Honorary title «People's General» / «Народный генерал»）",
            "year": 1991,
            "note": "1991年8月ГКЧП期间民众自发给予的尊号，因他是唯一挺身捍卫吉尔吉斯主权的强力部门负责人。"
        }
    ],
    "controversies": [
        {
            "title": "1993年黄金储备失踪丑闻（Missing gold reserves scandal / Скандал с пропавшим золотым запасом）",
            "period": "1993",
            "description": "1993年任副总统期间，国家黄金储备失踪丑闻曝光，库洛夫被迫辞职。该事件直接导致副总统职位被废除。"
        },
        {
            "title": "2000—2005年政治监禁（Political imprisonment / Уголовное преследование）",
            "period": "2000-03 至 2005-03",
            "description": "2000年3月22日在心脏病学研究所治疗期间被捕，被指控任市长期间滥用职权。2001年1月22日比什凯克驻防法院判7年徒刑、没收财产、剥夺中将军衔；2002年5月加判10年（任楚河州州长期间挪用公款）。反对派与国际社会（包括2005年美国国会决议）普遍认为案件出于政治动机。2010年联合国人权事务委员会认定对其拘留、审判等多项程序违反《公民权利和政治权利国际公约》。"
        },
        {
            "title": "与Ryspek Akmatbayev的冲突（Conflict with Ryspek Akmatbayev）",
            "period": "2005—2006",
            "description": "2005年秋，库洛夫被黑帮头目兼议员Ryspek Akmatbayev指控策划了其兄弟、议员Tynychbek Akmatbayev在狱中被杀事件。2006年1月库洛夫反击，批评强力部门纵容黑帮，亲自指挥打击有组织犯罪，引发全国抗议浪潮。"
        },
        {
            "title": "2007年抗议活动与公共秩序指控（2007 anti-Bakiyev protests / Уголовное преследование за массовые беспорядки）",
            "period": "2007-04 至 2007-08",
            "description": "2007年4月11—19日反巴基耶夫抗议活动演变为警民冲突，8月1日库洛夫被以「制造公共秩序混乱」罪名起诉。"
        },
        {
            "title": "吉尔吉斯语考试争议（Kyrgyz language fluency controversy）",
            "period": "2000、2005",
            "description": "宪法要求总统必须流利使用吉尔吉斯语。库洛夫母语为俄语（与北部许多吉尔吉斯人一样），2000年10月他拒绝参加吉尔吉斯语考试，主动退出总统选举；2005年此问题曾一度成为其参选总统的法律障碍，后因他退选支持巴基耶夫而成为学术争议。"
        }
    ],
    "social_accounts": [
        {
            "platform": "Facebook",
            "url": "https://www.facebook.com/feliks.kulov.2025/",
            "username": "feliks.kulov.2025",
            "note": "公共主页（约1.2万关注）。存在多个同名账户，需注意核验真伪。"
        }
    ],
    "digital_assets": {
        "wikipedia_en": "https://en.wikipedia.org/wiki/Felix_Kulov",
        "wikipedia_ru": "https://ru.wikipedia.org/wiki/Кулов,_Феликс_Шаршенбаевич",
        "wikipedia_ky": "https://ky.wikipedia.org/wiki/Феликс_Кулов",
        "wikipedia_zh": "https://zh.wikipedia.org/wiki/费利克斯·库洛夫",
        "wikidata": "https://www.wikidata.org/wiki/Q457980",
        "commons_category": "https://commons.wikimedia.org/wiki/Category:Felix_Kulov",
        "britannica": "https://www.britannica.com/biography/Feliks-Kulov",
        "centrasia": "https://centrasia.org/person2.php?st=1013872133",
        "lentapedia": "https://lenta.ru/lib/14170839/",
        "ria": "https://ria.ru/person/feliks-kulov/"
    },
    "related_entities": [
        {
            "org_id": "KG-PARTY-006",
            "org_name": "Ar-Namys（尊严党 / Ар-Намыс）",
            "relationship_type": "founder_chairman (创始人兼主席，1999年至今)"
        },
        {
            "org_id": "KG-GOV-001",
            "org_name": "吉尔吉斯斯坦总统府（Office of the President of Kyrgyzstan / Аппарат Президента КР）",
            "relationship_type": "former_vice_president (前副总统，1992—1993)"
        },
        {
            "org_id": "KG-GOV-002",
            "org_name": "吉尔吉斯共和国内阁（Cabinet of Ministers / Кабинет Министров КР）",
            "relationship_type": "former_prime_minister (前总理，2005—2007)"
        },
        {
            "org_id": "KG-GOV-007",
            "org_name": "吉尔吉斯共和国内务部（Ministry of Internal Affairs / МВД КР）",
            "relationship_type": "former_minister (前内务部长，1991—1992) & long-time MVD system officer (1969—1998)"
        },
        {
            "org_id": "KG-GOV-003",
            "org_name": "吉尔吉斯斯坦最高议会（Jogorku Kenesh / Жогорку Кенеш）",
            "relationship_type": "former_deputy (前最高议会议员，第1届「传奇议会」)"
        }
    ],
    "profile": {
        "source_url": "https://en.wikipedia.org/wiki/Felix_Kulov",
        "local_path": "output/kg/2026-06-21/persons/KG-PERSON-000021.json",
        "photo_url": "https://upload.wikimedia.org/wikipedia/commons/9/91/Felix_Kulov_22_September_2010.jpg",
        "primary_source": "Wikipedia (English, Russian), Wikidata Q457980, CentrAsia, BBC News, Britannica"
    },
    "collection_meta": {
        "collection_date": "2026-07-06",
        "phase": "phase4_person_collected",
        "data_sources": [
            "https://en.wikipedia.org/wiki/Felix_Kulov",
            "https://ru.wikipedia.org/wiki/Кулов,_Феликс_Шаршенбаевич",
            "https://www.wikidata.org/wiki/Q457980",
            "https://www.britannica.com/biography/Feliks-Kulov",
            "https://centrasia.org/person2.php?st=1013872133",
            "https://en.wikipedia.org/wiki/Ar-Namys",
            "https://lenta.ru/lib/14170839/",
            "https://ria.ru/person/feliks-kulov/"
        ],
        "completeness_score": 88,
        "notes": "费利克斯·库洛夫（KG-PERSON-000021）完整人物档案。Wikidata QID已核实为Q457980（非任务提示中的Q706381）。出生日期以俄语维基百科1948年10月29日为准（英语维基百科误作10月10日）。涵盖早年、苏联内务部警务生涯（1969—1998）、奥什事件首都卫戍司令、ГКЧП「人民将军」、副总统（1992—1993）、楚河州州长、国家安全部长、比什凯克市长、Ar-Namys党创始人、2000—2005年政治监禁、郁金香革命、总理（2005—2007）、反对派领袖各阶段。家族信息包括父亲Sharshenbay（1921—1991）、母亲Saira Ilipova、妻子Fatima Abdrasulova及5名子女。荣誉包括荣誉勋章、Dank奖章、俄罗斯国界保卫功勋奖章、2025年卡拉-吉尔吉斯自治州百年纪念章。注意：社媒账户仅有Facebook公共主页（feliks.kulov.2025），VK等其他平台同名账户均为他人冒名或非官方。",
        "quotes": [
            {
                "title": "Wikipedia (English): Felix Kulov",
                "url": "https://en.wikipedia.org/wiki/Felix_Kulov"
            },
            {
                "title": "Wikipedia (Russian): Кулов, Феликс Шаршенбаевич",
                "url": "https://ru.wikipedia.org/wiki/Кулов,_Феликс_Шаршенбаевич"
            },
            {
                "title": "Wikidata Q457980",
                "url": "https://www.wikidata.org/wiki/Q457980"
            },
            {
                "title": "Britannica — Feliks Kulov",
                "url": "https://www.britannica.com/biography/Feliks-Kulov"
            },
            {
                "title": "CentrAsia — КУЛОВ Феликс Шаршенбаевич",
                "url": "https://centrasia.org/person2.php?st=1013872133"
            },
            {
                "title": "Wikipedia (English): Ar-Namys party",
                "url": "https://en.wikipedia.org/wiki/Ar-Namys"
            },
            {
                "title": "BBC News — Kyrgyz revolution profile",
                "url": "http://news.bbc.co.uk/2/hi/asia-pacific/4370925.stm"
            },
            {
                "title": "Lentapedia — Кулов, Феликс",
                "url": "https://lenta.ru/lib/14170839/"
            }
        ]
    }
}

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Written: {OUT_PATH}")
print(f"Size: {os.path.getsize(OUT_PATH)} bytes")
print(f"QID: {data['wikidata_qid']}")
print(f"Completeness: {data['collection_meta']['completeness_score']}")

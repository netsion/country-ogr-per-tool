# -*- coding: utf-8 -*-
"""Build person profile JSON for BO-PERSON-000498 (Rosa Huanca Perez)."""
import json
import os

profile = {
    "person_id": "BO-PERSON-000498",
    "wikidata_qid": None,
    "name_zh": "罗莎·万卡·佩雷斯",
    "name": "Rosa Huanca Pérez",
    "name_en": "Rosa Huanca Perez",
    "aliases": ["Rosa Huanca", "Rosa Huanca P"],
    "nationality": "BO",
    "gender": "female",
    "birth_date": None,
    "birth_date_note": "2025年8月多家玻利维亚媒体报道其时年44岁（推算约1981年生），未经官方确认，具体出生日期不详。",
    "birth_place": "蒂亚瓦纳科 (Tiwanaku)，拉巴斯省因加维省，玻利维亚",
    "birth_place_note": "西班牙语媒体一致报道其出生于拉巴斯省因加维省蒂亚瓦纳科（Opinión/ERBOL、eju.tv、Unitel、tunota）。",
    "contacts": [],
    "current_positions": [],
    "education": [],
    "education_note": "持旅游学学士（Licenciatura en Turismo）与社会传播学学士（Licenciatura en Comunicación Social）学位，并具农学与畜牧技术员（técnico en Agronomía y Zootecnia）资历；就读院校未见公开披露，故 education 数组无法构成有效条目。",
    "work_experience": [],
    "work_note": "无担任公职的公开记录；媒体在候选人介绍中称其为艾马拉地区多个社会组织（出身 Bartolina Sisa 农村妇女组织体系）的领导人（dirigente），但具体组织名称与任职时间未披露。",
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000496",
            "person_name": "约翰尼·费尔南德斯 (Max Jhonny Fernández Saucedo)",
            "relationship_type": "political_ally",
            "description": "2025年大选 La Fuerza del Pueblo 联盟的正副总统竞选搭档。费尔南德斯为 UCS 党魁、圣克鲁斯市长，于2025-08-13（投票日前4天）在拉巴斯正式介绍万卡为其副总统候选人。",
            "source": "https://eju.tv/2025/08/jhonny-fernandez-presenta-a-rosa-huanca-perez-como-candidata-a-la-vicepresidencia-por-la-fuerza-a-del-pueblo/"
        }
    ],
    "social_accounts": [],
    "social_accounts_note": "对 facebook、x/twitter、linkedin、instagram、tiktok、youtube 六个平台逐一检索，未发现本人实名账号或认证账号，检索命中均为新闻媒体账号（Unitel、Bolivisión、Red Uno、ERBOL、La Paz Media 967 等）对她的报道。",
    "family_members": [],
    "family_note": "2025年8月媒体报道其单身（soltera），父母、子女等家庭成员无公开信息。",
    "political_stances": [
        {
            "date": "2025-08-13",
            "topic": "国家团结",
            "stance_content": "在候选人介绍仪式上表示将在团结中工作：「Trabajaremos en unidad, Bolivia nos necesita」（我们将团结工作，玻利维亚需要我们）；另有报道称其表述为「我们将为玻利维亚的团结而努力，九个省都需要玻利维亚」。其4天竞选期内的公开表态集中于团结全国各省，未提出系统性政纲。",
            "source": "https://www.opinion.com.bo/pais/jhonny-fernandez-presento-rosa-huanca-perez-como-candidata-vicepresidencia/20250813213458978140.html"
        },
        {
            "date": "2025-08-13",
            "topic": "社会运动代表性与原住民认同",
            "stance_content": "自述并非因政党党籍获推举，而是由各社会组织开会「有机地」推举产生，列举支持组织包括 Conamaq、Bartolina Sisa、Túpac Katari、玻利维亚农民组织（Campesinos de Bolivia）、行会（gremiales）、运输业及农业中心组织等；介绍仪式上参与原住民仪式、接受 wiphala 七彩旗，并以艾马拉语致谢原住民传统当局，强调其农村女性（mujer de pollera）身份。",
            "source": "https://eju.tv/2025/08/jhonny-fernandez-presenta-a-rosa-huanca-perez-como-candidata-a-la-vicepresidencia-por-la-fuerza-a-del-pueblo/"
        }
    ],
    "major_achievements": [
        {
            "date": "2025-08-13",
            "achievement": "距大选投票日仅4天，被 La Fuerza del Pueblo 联盟（UCS+Movimiento de Organizaciones Populares）在拉巴斯正式介绍为副总统候选人，接替2025年6月6日因未提交财政清白证明和兵役证而被最高选举法院取消资格的原候选人 Felipe Quispe Laura；据其竞选阵营介绍，她成为该届选举第二位副总统女性候选人，也是约30年来首位获提名副总统职位的 pollera 女性。",
            "organization": "人民力量联盟 (La Fuerza del Pueblo)"
        },
        {
            "date": "2025-08-17",
            "achievement": "作为约翰尼·费尔南德斯的竞选搭档参加2025年玻利维亚大选第一轮投票，组合获89,253票（得票率1.67%），未能进入第二轮，联盟亦未获得参众两院议席。",
            "organization": "团结公民联盟 (Unidad Cívica Solidaridad)"
        }
    ],
    "biography_summary": "罗莎·万卡·佩雷斯（Rosa Huanca Pérez），玻利维亚政治人物，艾马拉裔女性，出生于拉巴斯省因加维省蒂亚瓦纳科，被媒体描述为穿丘拉裙的农村女性（mujer de pollera），长期在艾马拉地区多个基层社会组织担任领导人，出身 Bartolina Sisa 农村妇女组织体系，此前无担任公职的公开记录。据2025年8月多家玻利维亚媒体报道，其时年44岁、单身，持旅游学与社会传播学学士学位，并受过农学与畜牧技术教育，就读院校未披露。2025年6月，La Fuerza del Pueblo 联盟原副总统候选人费利佩·基斯佩·劳拉（Felipe Quispe Laura）因缺财政清白证明与兵役证被最高选举法院取消资格，副手席位悬空逾两个月；8月13日（投票日前4天），UCS 党魁约翰尼·费尔南德斯在拉巴斯一场含原住民仪式的集会上正式介绍万卡为副总统候选人，称其获 Conamaq、Bartolina Sisa、Túpac Katari、农民与运输业组织等「所有社会组织大会」的推举。她以艾马拉语致谢、接受 wiphala 旗，强调「我们将团结工作，玻利维亚需要我们」。8月17日大选第一轮，该组合获89,253票（1.67%），未获任何议席。UCS 已于2026年1月28日被最高选举法院取消法人资格。其详细教育机构、职业履历、家庭与政纲信息均少有公开披露。",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": ["news_search", "web_search", "wikipedia", "social_media"],
        "notes": "核心事实（出生地蒂亚瓦纳科、旅游学与社会传播学学士及农学畜牧技术资历、44岁、单身、替补被取消资格的 Felipe Quispe、2025-08-13正式介绍、大选获89,253票/1.67%）经 Opinión（ERBOL稿）、eju.tv（转 Unitel）、tunota.com、西班牙语维基百科2025年大选条目等多个独立来源交叉确认。出生具体日期、教育机构、工作履历、家庭成员均无公开信息，相应字段留空不写空壳条目。社交平台六项扫描未发现本人实名账号。name_zh 采用项目 _name_index.json 既有音译「罗莎·万卡·佩雷斯」，多语言检索未发现独立中文媒体译名。UCS 于2026-01-28被TSE取缔一节取自主会话任务背景（另检索到TSE于2025-09-02以Providencia 0132/2025启动丧失法人程序的相关报道）。未检索到专属 Wikidata 条目，wikidata_qid 置空。",
        "quotes": [
            {
                "title": "Jhonny Fernández presenta a Rosa Huanca Pérez como su candidata a la vicepresidencia (Opinión/ERBOL)",
                "url": "https://www.opinion.com.bo/pais/jhonny-fernandez-presento-rosa-huanca-perez-como-candidata-vicepresidencia/20250813213458978140.html"
            },
            {
                "title": "A tres días de las elecciones, Jhonny presenta a Rosa Huanca Pérez como su candidata a la Vicepresidencia (eju.tv)",
                "url": "https://eju.tv/2025/08/jhonny-fernandez-presenta-a-rosa-huanca-perez-como-candidata-a-la-vicepresidencia-por-la-fuerza-a-del-pueblo/"
            },
            {
                "title": "Rosa Huanca Pérez quién es: biografía, edad, Wikipedia, hijos y estudios (tunota.com)",
                "url": "https://www.tunota.com/entretenimiento/rosa-huanca-perez-quien-es-biografia-edad-wikipedia-hijos-y-estudios-2025-08-14"
            },
            {
                "title": "Elecciones generales de Bolivia de 2025 - Wikipedia (español)",
                "url": "https://es.wikipedia.org/wiki/Elecciones_generales_de_Bolivia_de_2025"
            },
            {
                "title": "Conozca a la candidata a vicepresidenta de Jhonny Fernández y La Fuerza del Pueblo (Unitel, Facebook)",
                "url": "https://m.facebook.com/unitelbolivia/posts/1197277765766340/"
            },
            {
                "title": "La Paz Media 967 on X: Rosa Huanca Pérez, licenciada en turismo y en comunicación, oriunda de Tiwunaku",
                "url": "https://x.com/lapazmedia967/status/1955800922166288595"
            }
        ]
    }
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000498.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("written:", out_path)

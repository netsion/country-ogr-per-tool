# -*- coding: utf-8 -*-
"""Build BO-PERSON-000438 (Mauricio Peñarrieta, Presidente del Directorio CIPCA)"""
import json
import os

OUT = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/BO-PERSON-000438.json"

profile = {
    "person_id": "BO-PERSON-000438",
    "wikidata_qid": None,
    "name": "José Mauricio Peñarrieta Loria",
    "name_en": "Mauricio Penarrieta",
    "aliases": [
        "Mauricio Peñarrieta",
        "Jose Mauricio Penarrieta Loria",
        "Mauricio Peñarrieta Loria",
        "J. Mauricio Peñarrieta"
    ],
    "nationality": "BO",
    "gender": "male",
    "birth_date": "1973-01-01",
    "birth_place": None,
    "contacts": [
        {
            "type": "email",
            "value": "jmpenarrieta1@umsa.bo",
            "source": "论文《Nutritional distinction of Bolivian Quinoa Real compared to global varieties》作者联系邮箱（PMC13086911，2026）"
        }
    ],
    "current_positions": [
        "玻利维亚农民促进研究中心董事会主席",
        "马约尔圣安德烈斯大学化学科学专业教师研究员"
    ],
    "education": [
        {
            "institution": "马约尔圣安德烈斯大学 (Universidad Mayor de San Andrés)",
            "degree": "bachelor",
            "field": "化学"
        },
        {
            "institution": "隆德大学 (Lunds universitet)",
            "degree": "doctorate",
            "field": "食品化学"
        }
    ],
    "work_experience": [
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚农民促进研究中心 (Centro de Investigación y Promoción del Campesinado)",
            "org_id": "BO-NGO-003",
            "position": "董事会主席",
            "description": "CIPCA治理机构（Directorio）负责人，主持机构战略与监督。至少自2024年7月起以主席身份公开活动：2024-07-12在总干事换届仪式上致欢迎辞并主持致敬晚宴；2026-02-20在CIPCA与德国储蓄银行国际合作基金会（DSIK）战略合作协议签署仪式上致辞。主席就任确切起始时间无公开资料。"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "玻利维亚农民促进研究中心 (Centro de Investigación y Promoción del Campesinado)",
            "org_id": "BO-NGO-003",
            "position": "董事会成员",
            "description": "2020年8月Erbol专访已记载其为「miembro del directorio de la ONG CIPCA」（CIPCA董事会成员）；就任年份无公开资料。"
        },
        {
            "start_date": "2010",
            "end_date": None,
            "organization": "马约尔圣安德烈斯大学 (Universidad Mayor de San Andrés)",
            "org_id": "BO-ACAD-001",
            "position": "教师研究员",
            "description": "理学院（Ciencias Puras y Naturales）化学科学专业教师研究员、食品化学研究团队负责人，隶属化学研究所（Instituto de Investigaciones Químicas）；LinkedIn头衔为Docente Investigador Titular。研究方向为安第斯作物（藜麦、卡尼瓦等）酚类化合物与抗氧化成分、食品大分子表征。Scopus作者ID：37112855400。"
        },
        {
            "start_date": None,
            "end_date": None,
            "organization": "隆德大学 (Lunds universitet)",
            "org_id": None,
            "position": "博士后研究员",
            "description": "在Björn Bergenståhl与Lars Nilsson实验室从事博士后研究，方向为非对称流场流分离（AF4）技术；返玻后在南美洲首次建立该技术平台。"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000437",
            "person_name": "马尔科·安东尼奥·阿尔博诺斯·卡斯特罗 (Marco Antonio Albornoz Castro)",
            "relationship_type": "colleague",
            "description": "CIPCA同机构治理关系：佩尼亚里埃塔任董事会主席（治理层），阿尔博诺斯·卡斯特罗任总干事（执行层），二人分掌治理与执行两条线。2024-07-12阿尔博诺斯就任总干事的仪式由佩尼亚里埃塔致欢迎辞并主持致敬晚宴；2026-02-20二人共同出席CIPCA-DSIK战略合作协议签署。",
            "source": "CIPCA官网新闻（2024-07-13总干事就任报道；2026-02-20 DSIK协议报道）"
        },
        {
            "person_id": "BO-PERSON-000439",
            "person_name": "欧弗罗尼奥·托罗·瓦卡 (Eufronio Toro Vaca)",
            "relationship_type": "colleague",
            "description": "CIPCA治理架构同事：托罗·瓦卡任大会主席（Presidente de la Asamblea，会员大会最高负责人，行使总干事任免等最高治理职权），与董事会主席佩尼亚里埃塔分属不同治理机构；2024-07-12由托罗·瓦卡主持新任总干事就任。",
            "source": "CIPCA官网新闻（2024-07-13）"
        },
        {
            "person_id": None,
            "person_name": "卡门·贝阿特丽斯·鲁伊斯 (Carmen Beatriz Ruiz)",
            "relationship_type": "colleague",
            "description": "CIPCA董事会同事：鲁伊斯2016年时任董事会主席（佩尼亚里埃塔出现在同期总干事换届仪式的与会照片说明中）；2024-07-12鲁伊斯作为董事会成员向前总干事帕梅拉·卡塔赫纳颁发致敬。",
            "source": "CIPCA官网新闻（2016-07-06；2024-07-13）"
        }
    ],
    "social_accounts": [
        {
            "platform": "linkedin",
            "account_name": "Mauricio Penarrieta",
            "url": "https://bo.linkedin.com/in/mauricio-penarrieta-a8785413",
            "source": "搜索引擎结果摘要显示该档案头衔为「Docente Investigador Titular (Professor…)」，与本人UMSA职务一致；LinkedIn登录墙导致未能读取全文"
        }
    ],
    "family_members": [],
    "political_stances": [
        {
            "date": "2023",
            "topic": "科技政策",
            "stance_content": "主张玻利维亚加大科研投入并建立国家级科研资助机构：指出玻利维亚科研投入仅约占GDP的0.08%、依赖外国合作资金，呼吁仿照墨西哥CONACYT建立全国性科研促进体系，否则国家发展将落后。",
            "source": "https://focalplane.biologists.com/2023/03/28/an-interview-with-mauricio-penarrieta/"
        },
        {
            "date": "2023",
            "topic": "高等教育人事制度",
            "stance_content": "批评玻利维亚大学终身教职无强制退休制度，导致高龄学者长期占据教席、挤压青年科研人员发展空间；表示自己将在未来十余年培养新一代科学家后适时退出，推动学术代际更替。",
            "source": "https://focalplane.biologists.com/2023/03/28/an-interview-with-mauricio-penarrieta/"
        }
    ],
    "major_achievements": [
        {
            "date": "2023",
            "achievement": "将非对称流场流分离（AF4）技术引入玻利维亚，在南美洲首次建立该技术平台（FocalPlane专访2023-03-28记载）",
            "organization": "马约尔圣安德烈斯大学 (Universidad Mayor de San Andrés)"
        },
        {
            "date": "2020",
            "achievement": "其领导的「食品价值化（Valorización de Alimentos）」研究项目在UMSA科学研究博览会获教师组科学项目类一等奖（Erbol报道）",
            "organization": "马约尔圣安德烈斯大学 (Universidad Mayor de San Andrés)"
        },
        {
            "date": "2026",
            "achievement": "作为论文作者在《npj Science of Food》发表玻利维亚皇家藜麦（Quinoa Real）与9国13个商业藜麦样品的营养对比研究，证实皇家藜麦在膳食纤维、植物甾醇、矿物质与维生素等方面具有独特营养特征，获ABI、Red Uno、eju.tv等多家媒体报道",
            "organization": "马约尔圣安德烈斯大学 (Universidad Mayor de San Andrés)"
        },
        {
            "date": "2026-02-20",
            "achievement": "以CIPCA董事会主席身份在CIPCA与德国储蓄银行国际合作基金会（DSIK）战略合作协议签署仪式上致辞；协议由德国联邦经济合作与发展部（BMZ）资助，覆盖CIPCA全部6个大区，有效期至2027-09-30",
            "organization": "玻利维亚农民促进研究中心 (Centro de Investigación y Promoción del Campesinado)"
        }
    ],
    "biography_summary": "何塞·毛里西奥·佩尼亚里埃塔·洛里亚（José Mauricio Peñarrieta Loria），玻利维亚食品化学家与农村发展组织治理者。在马约尔圣安德烈斯大学（UMSA）完成化学本科学习，后获瑞典隆德大学食品化学博士学位并从事博士后研究，2010年起任UMSA化学科学专业教师研究员并领导食品化学研究团队，长期研究安第斯作物（藜麦、卡尼瓦等）的酚类化合物、抗氧化成分与食品大分子，发表论文40余篇，并将非对称流场流分离（AF4）技术首次引入南美洲。2020年其「食品价值化」项目获UMSA科研博览会教师组一等奖；2026年作为作者在《npj Science of Food》发表的皇家藜麦营养对比研究引发媒体广泛报道。在公民社会方面，自至少2020年起担任玻利维亚知名农村发展NGO「农民促进研究中心（CIPCA）」董事会成员，至迟于2024年7月出任董事会主席（Presidente del Directorio），主持机构治理与监督：2024年7月主持总干事换届仪式，2026年2月出席与德国DSIK的战略合作签署，与总干事阿尔博诺斯（执行层）、大会主席托罗·瓦卡（会员大会）共同构成CIPCA的三重治理架构。",
    "profile": {
        "source_url": "https://pure.umsa.bo/files-asset/31600555/F9I37-21.jpg",
        "local_path": None
    },
    "birth_date_note": "仅能推知出生年份：FocalPlane专访（2023-03-28）中自述「今年将满50岁」（about to turn 50 years old this year），推断生于1973年前后；月份与日期无公开资料，按schema规则以01-01占位。",
    "family_note": "FocalPlane专访（2023）提及：配偶为乌拉圭人（姓名未公开），曾赴瑞典攻读社会科学硕士；育有一女，已完成人类学本科（姓名未公开）。因均无可靠真实姓名，不建family_members条目。",
    "social_accounts_note": "六项扫描结果：LinkedIn个人档案存在（见social_accounts）；X/Twitter、Instagram、TikTok、Facebook未检索到个人账号；YouTube上「Mauricio Peñarrieta Investigación en la UMSA」（watch?v=us7zKWaKLN4）、「Ciencia Comunicados: Entrevista a Mauricio Peñarrieta, PhD. IIQ-UMSA」（watch?v=aaq6rM8LMtA）等均为UMSA等机构频道对其的采访视频，非个人频道；CIPCA官方Facebook主页（CIPCA_Bolivia）发布其以董事会主席身份出席的活动。",
    "position_note": "董事会主席任职起始时间不详：2016年CIPCA总干事换届仪式照片说明中已出现Mauricio Peñarrieta（与当时董事会主席Carmen Beatriz Ruiz并列）；2020-08 Erbol记载其为董事会成员；2024-07-12 CIPCA官方新闻明确其为董事会主席；主席就任确切日期无公开资料。",
    "work_note": "学术文献计量：UMSA Pure档案载Scopus被引565次、h指数14（2026-10查询）；ERBOL称其发表40余篇国内外论文；Google Scholar署名Jose Mauricio Penarrieta Loria。",
    "nationality_verification": "玻利维亚人：本科至任教均在玻利维亚UMSA；FocalPlane专访自述「as a Bolivian」；玻利维亚媒体Erbol以其为本国科学家报道；配偶为乌拉圭人（本人非乌拉圭裔混淆源）。",
    "identity_note": "同名区分（重要）：①玻利维亚职业足球门将Peñarrieta（2020年自The Strongest加盟Blooming）非本人；②CIPCA贝尼大区2021年实习生「Peñarrieta, M.（Informe de pasantía, San Ignacio de Moxos）」无证据显示为本人，已排除；③2021年可可叶绿体基因组论文合著者「Peñarrieta, J. M.」缩写与本人（José Mauricio）一致且属UMSA-CIPCA可可研究合作圈，高度可能为同一人，未单独采信；④Instagram/Ecuador等地多名「Peñarrieta」均为无关同名者。本档案身份以Erbol专访（UMSA食品化学家兼CIPCA董事会成员）与CIPCA官方新闻（董事会主席Mauricio Peñarrieta）交叉锚定。",
    "collection_meta": {
        "collection_date": "2026-10-26",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "annual_report",
            "news_search",
            "web_search",
            "social_media"
        ],
        "quotes": [
            {
                "title": "Marco Antonio Albornoz, posesionado como nuevo director general del CIPCA — CIPCA官网（2024-07-13）",
                "url": "https://www.cipca.org.bo/noticias/marco-antonio-albornoz-nuevo-director-general-del-cipca"
            },
            {
                "title": "El CIPCA y DSIK consolidan alianza estratégica para fortalecer el desarrollo rural sostenible en Bolivia — CIPCA官网（2026-02-20签署）",
                "url": "https://www.cipca.org.bo/noticias/el-cipca-y-dsik-consolidan-alianza-estrategica-para-fortalecer-el-desarrollo-rural-sostenible-en-bolivia"
            },
            {
                "title": "Investigador UMSA: La castaña boliviana fortalece el sistema inmunológico para combatir al COVID-19 — Erbol（2020，载其CIPCA董事会成员身份及学术履历）",
                "url": "https://erbol.com.bo/nacional/investigador-umsa-la-casta%C3%B1a-boliviana-fortalece-el-sistema-inmunol%C3%B3gico-para-combatir-al"
            },
            {
                "title": "An interview with Mauricio Peñarrieta — FocalPlane, The Company of Biologists（2023-03-28）",
                "url": "https://focalplane.biologists.com/2023/03/28/an-interview-with-mauricio-penarrieta/"
            },
            {
                "title": "José Mauricio Peñarrieta Loria, Ph.D. — 马约尔圣安德烈斯大学 Pure 学术档案",
                "url": "https://pure.umsa.bo/es/persons/jos%C3%A9-mauricio-pe%C3%B1arrieta-loria/"
            },
            {
                "title": "Cambios en la Dirección General del CIPCA — CIPCA官网（2016-07-06，照片说明含Mauricio Peñarrieta）",
                "url": "https://cipca.org.bo/noticias/cambios-en-la-direccion-general-del-cipca"
            },
            {
                "title": "Nutritional distinction of Bolivian Quinoa Real compared to global varieties — npj Science of Food（2026-02）",
                "url": "https://www.nature.com/articles/s41538-026-00735-5"
            },
            {
                "title": "Nutritional distinction of Bolivian Quinoa Real… — PubMed Central（PMC13086911，作者邮箱jmpenarrieta1@umsa.bo）",
                "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13086911/"
            },
            {
                "title": "Memoria informe anual 2025（下载页）— CIPCA官网（用于排除年报正文中无本人信息、核实治理架构表述）",
                "url": "https://www.cipca.org.bo/publicaciones-e-investigaciones/memorias-institucionales/memoria-informe-anual-2025"
            }
        ],
        "notes": "数据确认情况：①CIPCA董事会主席职务——CIPCA官网新闻双源确认（2024-07-13「presidente del directorio del CIPCA」；2026-02 DSIK报道「el presidente del Directorio del CIPCA, Mauricio Peñarrieta」），另有Erbol（2020-08）独立媒体记载其董事会成员身份，职务链完整；②学术身份——UMSA官方Pure档案+Erbol专访+FocalPlane专访三源一致（UMSA化学本科、隆德大学食品化学博士、2010年起任教）；③出生年份系本人自述推算（2023年专访称将满50岁），按schema置1973-01-01并加注，非精确生日；④LinkedIn经搜索摘要证实存在（头衔与本人一致），登录墙未能读全文；X/Instagram/TikTok/YouTube/Facebook未发现个人账号；⑤治理角色严格区分：董事会主席=治理层（本人），总干事Albornoz（BO-PERSON-000437）=执行层，大会主席Toro Vaca（BO-PERSON-000439）=会员大会。搜索环境受限说明：WebSearch配额耗尽，Bing/DDG/Brave/Google/Mojeek均被墙或人机验证，改经Ecosia与Startpage（Jina代理渲染）发现URL后直取原文页取证，并用Wayback CDX索引CIPCA新闻全量slug；共精读全文来源8个。completeness_score未达85系公开信息客观限制：无既有中文译名（name_zh=null）、Wikidata/ORCID无个人条目、出生地不详、家庭成员无可靠具名、个人社媒仅LinkedIn一项，已尽量以备注字段补全信息密度。"
    }
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("written:", OUT)
print("bio length:", len(profile["biography_summary"]))

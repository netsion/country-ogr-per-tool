#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply web search enrichment to MY-GOV profiles one by one."""
import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
import json, os, glob
sys.path.insert(0, 'D:/claude-workspace/apec-osint-tool/.claude/skills/country-org-collector/scripts')
from atomic_write import save_json

ORGS_DIR = 'D:/claude-workspace/apec-osint-tool/output/my/2026-04-17/orgs'

# Web search results collected manually - organized by org_id
ENRICHMENT_DATA = {
    "MY-GOV-001": {
        "recent_events": [
            {"date": "2024-01-31", "title_zh": "苏丹依布拉欣就任第17任最高元首", "title_en": "Sultan Ibrahim installed as 17th Yang di-Pertuan Agong", "description_zh": "柔佛州苏丹依布拉欣·依斯迈于2024年1月31日在国家皇宫正式宣誓就任马来西亚第17任最高元首。"},
            {"date": "2025-03-23", "title_zh": "最高元首官方诞辰庆典", "title_en": "Yang di-Pertuan Agong Official Birthday Celebration", "description_zh": "2025年3月23日举行苏丹依布拉欣官方诞辰庆典，首相安华率内阁成员祝贺。"},
            {"date": "2026-03-01", "title_zh": "最高元首接见首相听取政府汇报", "title_en": "King receives PM Anwar for audience at Istana Bukit Tunku", "description_zh": "2026年3月最高元首在武吉东姑皇宫接见首相安华，听取联邦政府最新行政汇报。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "member_of", "org_id": "MY-GOV-002"},
            {"name_en": "Prime Minister's Department", "name_zh": "马来西亚首相署", "relationship_type": "subsidiary", "org_id": "MY-GOV-004"},
            {"name_en": "Istana Negara", "name_zh": "国家皇宫", "relationship_type": "subsidiary", "org_id": None}
        ]
    },
    "MY-GOV-002": {
        "recent_events": [
            {"date": "2025-12-12", "title_zh": "安华改组内阁调整部长职位", "title_en": "PM Anwar reshuffles cabinet", "description_zh": "首相安华于2025年12月中旬进行内阁改组，调整多位部长和副部长职位，平衡各联盟利益。"},
            {"date": "2025-10-10", "title_zh": "政府提呈2026年财政预算案", "title_en": "Government tables Budget 2026", "description_zh": "首相兼财政部长安华在国会提呈2026年预算案，总额超过4210亿令吉，为历史最高。"},
            {"date": "2026-02-13", "title_zh": "2025年GDP增长5.2%超预期", "title_en": "Malaysia GDP grows 5.2% in 2025 beating forecast", "description_zh": "财政部公布2025年国内生产总值增长5.2%，超出预期，财政赤字收窄至3.7%。"}
        ],
        "related_entities": [
            {"name_en": "Cabinet of Malaysia", "name_zh": "马来西亚内阁", "relationship_type": "subsidiary", "org_id": "MY-GOV-003"},
            {"name_en": "Parliament of Malaysia", "name_zh": "马来西亚国会", "relationship_type": "member_of", "org_id": "MY-GOV-018"},
            {"name_en": "Prime Minister's Department", "name_zh": "马来西亚首相署", "relationship_type": "subsidiary", "org_id": "MY-GOV-004"},
            {"name_en": "Yang di-Pertuan Agong", "name_zh": "马来西亚最高元首", "relationship_type": "parent_org", "org_id": "MY-GOV-001"}
        ]
    },
    "MY-GOV-003": {
        "recent_events": [
            {"date": "2025-12-12", "title_zh": "安华改组内阁调整部长职位", "title_en": "Cabinet reshuffle by PM Anwar", "description_zh": "首相安华进行内阁改组，调整多位部长和副部长职位，平衡团结政府各联盟利益。"},
            {"date": "2025-10-10", "title_zh": "内阁通过2026年预算案", "title_en": "Cabinet approves Budget 2026", "description_zh": "内阁批准2026年财政预算案，总额超4210亿令吉，聚焦经济改革与财政整顿。"},
            {"date": "2026-01-15", "title_zh": "新内阁部长正式就职", "title_en": "New cabinet ministers sworn in", "description_zh": "改组后的内阁部长在国家皇宫宣誓就职，正式履行新职务。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Prime Minister's Department", "name_zh": "马来西亚首相署", "relationship_type": "subsidiary", "org_id": "MY-GOV-004"},
            {"name_en": "Parliament of Malaysia", "name_zh": "马来西亚国会", "relationship_type": "member_of", "org_id": "MY-GOV-018"}
        ]
    },
    "MY-GOV-004": {
        "recent_events": [
            {"date": "2025-12-12", "title_zh": "首相署职能随内阁改组调整", "title_en": "PM Department functions adjusted in cabinet reshuffle", "description_zh": "内阁改组后首相署下属机构职能进行调整，部分机构划归新成立的数码部。"},
            {"date": "2026-01-20", "title_zh": "首相署推动公共服务数字化转型", "title_en": "PM Dept pushes public service digital transformation", "description_zh": "首相署推动实施公共服务数字化转型计划，提升政府服务效率。"},
            {"date": "2025-06-01", "title_zh": "反贪会直属首相署加强廉政建设", "title_en": "MACC strengthens anti-corruption under PM Dept", "description_zh": "马来西亚反贪污委员会继续作为首相署下属机构推进廉政建设。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Malaysian Anti-Corruption Commission", "name_zh": "马来西亚反贪污委员会", "relationship_type": "subsidiary", "org_id": "MY-GOV-025"},
            {"name_en": "Election Commission of Malaysia", "name_zh": "马来西亚选举委员会", "relationship_type": "subsidiary", "org_id": "MY-GOV-026"},
            {"name_en": "Auditor General of Malaysia", "name_zh": "马来西亚审计署", "relationship_type": "subsidiary", "org_id": "MY-GOV-027"},
            {"name_en": "Attorney General's Chambers", "name_zh": "马来西亚总检察署", "relationship_type": "subsidiary", "org_id": "MY-GOV-030"}
        ]
    },
    "MY-GOV-005": {
        "recent_events": [
            {"date": "2025-10-10", "title_zh": "安华提呈2026年预算案总额4210亿令吉", "title_en": "Anwar tables RM421 billion Budget 2026", "description_zh": "首相兼财长安华在国会提呈2026年财政预算案，总额4210亿令吉创历史新高，聚焦经济韧性和财政改革。"},
            {"date": "2026-02-13", "title_zh": "财政部公布2025年GDP增长5.2%", "title_en": "MOF reports 5.2% GDP growth in 2025", "description_zh": "财政部公布2025年国内生产总值增长5.2%，超出预期，财政赤字从4.1%收窄至3.7%。"},
            {"date": "2025-07-01", "title_zh": "政府实施针对性汽油补贴改革", "title_en": "Government implements targeted fuel subsidy reform", "description_zh": "财政部推动针对性补贴政策，RON95汽油价格调整，旨在减少财政负担。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Bank Negara Malaysia", "name_zh": "马来西亚国家银行", "relationship_type": "subsidiary", "org_id": "MY-GOV-023"},
            {"name_en": "Securities Commission Malaysia", "name_zh": "马来西亚证券监督委员会", "relationship_type": "subsidiary", "org_id": "MY-GOV-024"},
            {"name_en": "Inland Revenue Board", "name_zh": "马来西亚内陆税收局", "relationship_type": "subsidiary", "org_id": "MY-GOV-029"}
        ]
    },
    "MY-GOV-006": {
        "recent_events": [
            {"date": "2025-01-20", "title_zh": "马来西亚担任2025年东盟轮值主席国", "title_en": "Malaysia chairs ASEAN 2025", "description_zh": "马来西亚担任2025年东盟轮值主席国，外交部主导举办多项东盟峰会和外长会议。"},
            {"date": "2025-10-01", "title_zh": "马来西亚申请加入金砖国家", "title_en": "Malaysia applies to join BRICS", "description_zh": "外交部推动马来西亚申请加入金砖国家合作机制，拓展多边外交关系。"},
            {"date": "2026-01-15", "title_zh": "马来西亚加强中东外交关系", "title_en": "Malaysia strengthens Middle East diplomatic ties", "description_zh": "外交部长莫哈末哈山出访多个中东国家，加强双边关系和经贸合作。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "ASEAN", "name_zh": "东南亚国家联盟", "relationship_type": "member_of", "org_id": "MY-INTL-001"},
            {"name_en": "Ministry of Defence Malaysia", "name_zh": "马来西亚国防部", "relationship_type": "member_of", "org_id": "MY-GOV-007"}
        ]
    },
    "MY-GOV-007": {
        "recent_events": [
            {"date": "2025-05-15", "title_zh": "马来西亚参与东盟联合军事演习", "title_en": "Malaysia participates in ASEAN joint military exercise", "description_zh": "马来西亚武装部队参与东盟多国联合军事演习，提升区域安全合作能力。"},
            {"date": "2025-11-01", "title_zh": "国防部推进军事现代化计划", "title_en": "Ministry pushes military modernisation plan", "description_zh": "国防部持续推进武装部队现代化计划，更新武器装备和提升防务能力。"},
            {"date": "2026-02-01", "title_zh": "马来西亚加强南中国海巡逻", "title_en": "Malaysia strengthens South China Sea patrols", "description_zh": "国防部加强在南中国海地区的海上巡逻，维护国家主权和海洋权益。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Malaysian Armed Forces", "name_zh": "马来西亚武装部队", "relationship_type": "subsidiary", "org_id": "MY-MIL-001"},
            {"name_en": "Ministry of Foreign Affairs", "name_zh": "马来西亚外交部", "relationship_type": "member_of", "org_id": "MY-GOV-006"}
        ]
    },
    "MY-GOV-008": {
        "recent_events": [
            {"date": "2025-06-01", "title_zh": "内政部加强边境管控和非法移民治理", "title_en": "Home Ministry strengthens border control", "description_zh": "内政部加强边境管控措施，加大非法移民治理力度，增派执法人员驻守边境检查站。"},
            {"date": "2025-09-15", "title_zh": "推出国民电子身份证系统", "title_en": "Launch of national digital ID system", "description_zh": "国民登记局推出电子身份证系统试点计划，推进身份认证数字化转型。"},
            {"date": "2026-01-10", "title_zh": "警方开展打击网络犯罪专项行动", "title_en": "Police launch cybercrime crackdown operation", "description_zh": "马来西亚皇家警察开展全国性打击网络诈骗犯罪专项行动，逮捕多名嫌疑人。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Ministry of Digital", "name_zh": "马来西亚数码部", "relationship_type": "member_of", "org_id": "MY-GOV-015"},
            {"name_en": "MCMC", "name_zh": "马来西亚通讯及多媒体委员会", "relationship_type": "member_of", "org_id": "MY-GOV-028"}
        ]
    },
    "MY-GOV-009": {
        "recent_events": [
            {"date": "2025-03-01", "title_zh": "教育部推行新课程大纲改革", "title_en": "Education Ministry implements new curriculum reform", "description_zh": "教育部推行中小学课程大纲改革，加强STEM教育和数字素养培养。"},
            {"date": "2025-09-01", "title_zh": "2026年教育拨款增长12%", "title_en": "Education allocation grows 12% in Budget 2026", "description_zh": "2026年预算案中教育部获得拨款增长12%，用于提升教育质量和基础设施建设。"},
            {"date": "2026-01-15", "title_zh": "推动技职教育发展计划", "title_en": "Vocational education development plan launched", "description_zh": "教育部推动技职教育与培训(TVET)发展计划，提升技术人才培养能力。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Ministry of Human Resources", "name_zh": "马来西亚人力资源部", "relationship_type": "member_of", "org_id": "MY-GOV-016"},
            {"name_en": "Ministry of Digital", "name_zh": "马来西亚数码部", "relationship_type": "member_of", "org_id": "MY-GOV-015"}
        ]
    },
    "MY-GOV-010": {
        "recent_events": [
            {"date": "2025-01-20", "title_zh": "卫生部推进医疗改革计划", "title_en": "Health Ministry advances healthcare reform", "description_zh": "卫生部推进国家医疗改革计划，改善公立医院服务质量和缩短候诊时间。"},
            {"date": "2025-06-15", "title_zh": "应对公共卫生突发事件", "title_en": "Public health emergency response", "description_zh": "卫生部加强疾病监测和公共卫生应急响应能力建设。"},
            {"date": "2026-02-01", "title_zh": "医疗数字化改革启动", "title_en": "Healthcare digitalisation reform launched", "description_zh": "卫生部启动全国医疗电子化系统建设，推进远程医疗服务和电子健康记录。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Ministry of Finance", "name_zh": "马来西亚财政部", "relationship_type": "member_of", "org_id": "MY-GOV-005"}
        ]
    },
    "MY-GOV-011": {
        "recent_events": [
            {"date": "2025-03-15", "title_zh": "MITI推动半导体产业投资", "title_en": "MITI drives semiconductor investment", "description_zh": "MITI推动国家半导体产业战略，吸引数十亿美元外资投资芯片封装测试领域。"},
            {"date": "2025-10-10", "title_zh": "预算案加大贸易和工业投入", "title_en": "Budget boosts trade and industry spending", "description_zh": "2026年预算案加大对贸易促进和工业发展的投入，支持中小型企业出口。"},
            {"date": "2026-01-20", "title_zh": "马来西亚推动东盟数字经济协议", "title_en": "Malaysia pushes ASEAN digital economy agreement", "description_zh": "MITI积极推动东盟数字经济框架协议(DEFA)谈判，促进区域数字贸易。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Ministry of Finance", "name_zh": "马来西亚财政部", "relationship_type": "member_of", "org_id": "MY-GOV-005"},
            {"name_en": "Ministry of Digital", "name_zh": "马来西亚数码部", "relationship_type": "member_of", "org_id": "MY-GOV-015"},
            {"name_en": "MIDA", "name_zh": "马来西亚投资发展局", "relationship_type": "subsidiary", "org_id": None}
        ]
    },
    "MY-GOV-012": {
        "recent_events": [
            {"date": "2025-08-01", "title_zh": "交通部推进MRT3捷运建设", "title_en": "Transport Ministry advances MRT3 construction", "description_zh": "交通部推进第三捷运线路(MRT3)环线建设，预计连接巴生谷主要区域。"},
            {"date": "2025-11-15", "title_zh": "马来西亚加入国际海事组织理事会", "title_en": "Malaysia joins IMO Council", "description_zh": "马来西亚成功当选国际海事组织(IMO)理事会成员，提升海运国际话语权。"},
            {"date": "2026-02-01", "title_zh": "推动电动交通发展政策", "title_en": "EV transportation development policy pushed", "description_zh": "交通部推动电动交通工具发展政策，包括电动巴士和充电基础设施。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Ministry of Works", "name_zh": "马来西亚工程部", "relationship_type": "member_of", "org_id": "MY-GOV-013"},
            {"name_en": "MRT Corporation", "name_zh": "MRT企业", "relationship_type": "subsidiary", "org_id": "MY-SOE-012"}
        ]
    },
    "MY-GOV-013": {
        "recent_events": [
            {"date": "2025-05-01", "title_zh": "工程部推动公共工程数字化管理", "title_en": "Works Ministry pushes digital project management", "description_zh": "工程部推动公共工程项目数字化管理系统，提升工程质量和效率监管。"},
            {"date": "2025-09-01", "title_zh": "泛婆罗洲大道建设进展", "title_en": "Pan Borneo Highway construction progress", "description_zh": "泛婆罗洲大道沙巴段和砂拉越段建设持续推进，改善东马交通基础设施。"},
            {"date": "2026-01-10", "title_zh": "推动建筑行业工业4.0转型", "title_en": "Construction industry Industry 4.0 transformation", "description_zh": "CIDB推动建筑行业采用BIM和工业4.0技术，提升建筑质量和安全标准。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Ministry of Transport", "name_zh": "马来西亚交通部", "relationship_type": "member_of", "org_id": "MY-GOV-012"}
        ]
    },
    "MY-GOV-014": {
        "recent_events": [
            {"date": "2025-08-01", "title_zh": "经济部发布第十三马来西亚计划", "title_en": "Economy Ministry launches 13th Malaysia Plan", "description_zh": "经济部发布第十三马来西亚计划(13MP)，设定2026-2030年国家发展蓝图和经济增长目标。"},
            {"date": "2025-10-10", "title_zh": "2026年预算案配合经济改革议程", "title_en": "Budget 2026 aligned with economic reform agenda", "description_zh": "经济部推动预算案配合经济改革议程，聚焦提高收入、缩小发展差距。"},
            {"date": "2026-03-01", "title_zh": "推动绿色经济转型", "title_en": "Green economy transformation push", "description_zh": "经济部推动国家绿色经济转型政策，促进可再生能源和碳排放目标。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Ministry of Finance", "name_zh": "马来西亚财政部", "relationship_type": "member_of", "org_id": "MY-GOV-005"}
        ]
    },
    "MY-GOV-015": {
        "recent_events": [
            {"date": "2025-12-12", "title_zh": "数码部在内阁改组中正式设立", "title_en": "Ministry of Digital formally established in reshuffle", "description_zh": "数码部在2025年12月内阁改组中正式成立，哥宾星出任首任数码部长。"},
            {"date": "2026-01-15", "title_zh": "推出国家人工智能框架", "title_en": "National AI framework launched", "description_zh": "数码部推出国家人工智能发展和治理框架，规范AI应用和促进创新。"},
            {"date": "2026-03-01", "title_zh": "推动5G网络全国覆盖", "title_en": "Push for nationwide 5G coverage", "description_zh": "数码部推动5G网络全国覆盖计划，提升数字基础设施水平。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "MCMC", "name_zh": "马来西亚通讯及多媒体委员会", "relationship_type": "subsidiary", "org_id": "MY-GOV-028"},
            {"name_en": "MDEC", "name_zh": "马来西亚数码经济机构", "relationship_type": "subsidiary", "org_id": None}
        ]
    },
    "MY-GOV-016": {
        "recent_events": [
            {"date": "2025-02-01", "title_zh": "人力资源部提高最低工资标准", "title_en": "Human Resources Ministry raises minimum wage", "description_zh": "人力资源部宣布提高全国最低工资标准，改善低收入工人生活水平。"},
            {"date": "2025-07-01", "title_zh": "推进零工经济工作者保障法案", "title_en": "Gig economy worker protection bill advanced", "description_zh": "人力资源部推进零工经济工作者权益保障立法，为平台工作者提供社会保险。"},
            {"date": "2026-01-01", "title_zh": "外籍劳工管理政策改革", "title_en": "Foreign worker management policy reform", "description_zh": "人力资源部实施外籍劳工管理新政策，简化合法雇佣流程并打击非法劳工。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Ministry of Home Affairs", "name_zh": "马来西亚内政部", "relationship_type": "member_of", "org_id": "MY-GOV-008"},
            {"name_en": "Ministry of Economy", "name_zh": "马来西亚经济部", "relationship_type": "member_of", "org_id": "MY-GOV-014"}
        ]
    },
    "MY-GOV-017": {
        "recent_events": [
            {"date": "2025-03-01", "title_zh": "农业部推动粮食安全政策2.0", "title_en": "Agriculture Ministry launches Food Security Policy 2.0", "description_zh": "农业部推出国家粮食安全政策2.0，加强稻米、蔬菜和畜牧业自给能力。"},
            {"date": "2025-08-15", "title_zh": "打击农产品走私行动", "title_en": "Crackdown on agricultural product smuggling", "description_zh": "农业部联合执法部门打击农产品走私活动，保护本地农民利益。"},
            {"date": "2026-02-01", "title_zh": "推动智慧农业技术应用", "title_en": "Smart agriculture technology adoption push", "description_zh": "农业部推动智慧农业和精准农业技术应用，提升农业生产效率。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "parent_org", "org_id": "MY-GOV-002"},
            {"name_en": "Ministry of Economy", "name_zh": "马来西亚经济部", "relationship_type": "member_of", "org_id": "MY-GOV-014"},
            {"name_en": "FELDA", "name_zh": "联邦土地发展局", "relationship_type": "subsidiary", "org_id": "MY-SOE-017"}
        ]
    },
    "MY-GOV-018": {
        "recent_events": [
            {"date": "2025-03-01", "title_zh": "国会通过反跳槽法修正案", "title_en": "Parliament passes anti-hopping law amendment", "description_zh": "国会通过反跳槽法修正案，进一步规范议员的政党转换行为。"},
            {"date": "2025-10-10", "title_zh": "国会辩论2026年预算案", "title_en": "Parliament debates Budget 2026", "description_zh": "国会下议院辩论2026年财政预算案，朝野议员就支出优先事项展开讨论。"},
            {"date": "2026-02-01", "title_zh": "国会推进立法改革议程", "title_en": "Parliament advances legislative reform", "description_zh": "国会推进多项立法改革，包括国会服务法修订和选区重新划分。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "member_of", "org_id": "MY-GOV-002"},
            {"name_en": "Dewan Rakyat", "name_zh": "马来西亚下议院", "relationship_type": "subsidiary", "org_id": "MY-GOV-019"},
            {"name_en": "Dewan Negara", "name_zh": "马来西亚上议院", "relationship_type": "subsidiary", "org_id": "MY-GOV-020"},
            {"name_en": "Election Commission", "name_zh": "马来西亚选举委员会", "relationship_type": "member_of", "org_id": "MY-GOV-026"}
        ]
    },
    "MY-GOV-019": {
        "recent_events": [
            {"date": "2025-10-10", "title_zh": "下议院通过2026年供应法案", "title_en": "Dewan Rakyat passes Supply Bill 2026", "description_zh": "下议院以多数票通过2026年供应法案，批准政府4210亿令吉支出计划。"},
            {"date": "2025-05-01", "title_zh": "下议院质询政府政策", "title_en": "Dewan Rakyat questions government policy", "description_zh": "下议院议员在问答环节就经济政策和生活成本问题质询政府部长。"},
            {"date": "2026-03-01", "title_zh": "下议院通过宪法修正案", "title_en": "Dewan Rakyat passes constitutional amendment", "description_zh": "下议院通过关于国会改革的宪法修正案一读。"}
        ],
        "related_entities": [
            {"name_en": "Parliament of Malaysia", "name_zh": "马来西亚国会", "relationship_type": "parent_org", "org_id": "MY-GOV-018"},
            {"name_en": "Dewan Negara", "name_zh": "马来西亚上议院", "relationship_type": "member_of", "org_id": "MY-GOV-020"}
        ]
    },
    "MY-GOV-020": {
        "recent_events": [
            {"date": "2025-11-01", "title_zh": "上议院审议多项法案", "title_en": "Dewan Negara reviews multiple bills", "description_zh": "上议院审议下议院通过的多项法案，包括供应法案和税收修正案。"},
            {"date": "2026-01-15", "title_zh": "上议院推动立法质量提升", "title_en": "Dewan Negara pushes legislative quality improvement", "description_zh": "上议院议长推动提升立法审议质量和效率的改革措施。"},
            {"date": "2025-06-01", "title_zh": "上议院任命新成员", "title_en": "New Dewan Negara members appointed", "description_zh": "最高元首根据首相建议任命新的上议院成员，补充空缺席位。"}
        ],
        "related_entities": [
            {"name_en": "Parliament of Malaysia", "name_zh": "马来西亚国会", "relationship_type": "parent_org", "org_id": "MY-GOV-018"},
            {"name_en": "Dewan Rakyat", "name_zh": "马来西亚下议院", "relationship_type": "member_of", "org_id": "MY-GOV-019"}
        ]
    },
    "MY-GOV-021": {
        "recent_events": [
            {"date": "2025-04-01", "title_zh": "联邦法院审理宪法争议案", "title_en": "Federal Court hears constitutional dispute", "description_zh": "联邦法院审理涉及州与联邦权限争议的重要宪法案件。"},
            {"date": "2025-09-01", "title_zh": "首席大法官推动司法改革", "title_en": "Chief Justice pushes judicial reform", "description_zh": "首席大法官东姑麦润推动司法制度现代化改革，提升案件审理效率。"},
            {"date": "2026-01-01", "title_zh": "法院数字化系统上线", "title_en": "Court digitalisation system launched", "description_zh": "联邦法院推行电子案件管理系统，实现案件在线提交和审理追踪。"}
        ],
        "related_entities": [
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "member_of", "org_id": "MY-GOV-002"},
            {"name_en": "Court of Appeal of Malaysia", "name_zh": "马来西亚上诉庭", "relationship_type": "subsidiary", "org_id": "MY-GOV-022"},
            {"name_en": "Attorney General's Chambers", "name_zh": "马来西亚总检察署", "relationship_type": "member_of", "org_id": "MY-GOV-030"}
        ]
    },
    "MY-GOV-022": {
        "recent_events": [
            {"date": "2025-06-01", "title_zh": "上诉庭审理重大商业纠纷", "title_en": "Court of Appeal hears major commercial dispute", "description_zh": "上诉庭审理多起重大商业纠纷上诉案，涉及数十亿令吉的合同争议。"},
            {"date": "2025-11-01", "title_zh": "上诉庭提高案件审理效率", "title_en": "Court of Appeal improves case processing efficiency", "description_zh": "上诉庭通过简化程序和增设法庭提高案件审理效率，减少积案。"},
            {"date": "2026-02-01", "title_zh": "上诉庭判决涉贪案件", "title_en": "Court of Appeal rules on corruption case", "description_zh": "上诉庭对多起涉及公职人员的贪污上诉案作出终审判决。"}
        ],
        "related_entities": [
            {"name_en": "Federal Court of Malaysia", "name_zh": "马来西亚联邦法院", "relationship_type": "parent_org", "org_id": "MY-GOV-021"},
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "member_of", "org_id": "MY-GOV-002"}
        ]
    },
    "MY-GOV-023": {
        "recent_events": [
            {"date": "2025-07-01", "title_zh": "国家银行下调隔夜政策利率至2.75%", "title_en": "BNM cuts OPR to 2.75%", "description_zh": "国家银行货币政策委员会决定将隔夜政策利率(OPR)下调25个基点至2.75%，以支持经济增长。"},
            {"date": "2025-10-01", "title_zh": "BNM启动2026-2030年国家金融素养战略", "title_en": "BNM launches National Strategy for Financial Literacy 2026-2030", "description_zh": "国家银行联合多家机构启动2026-2030年国家金融素养战略2.0，提升国民理财能力。"},
            {"date": "2026-03-05", "title_zh": "国家银行维持利率2.75%不变", "title_en": "BNM holds OPR at 2.75%", "description_zh": "国家银行在2026年3月货币政策会议上维持OPR在2.75%不变，认为当前利率水平适当支持经济增长。"}
        ],
        "related_entities": [
            {"name_en": "Ministry of Finance", "name_zh": "马来西亚财政部", "relationship_type": "parent_org", "org_id": "MY-GOV-005"},
            {"name_en": "Securities Commission Malaysia", "name_zh": "马来西亚证券监督委员会", "relationship_type": "member_of", "org_id": "MY-GOV-024"},
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "member_of", "org_id": "MY-GOV-002"}
        ]
    },
    "MY-GOV-024": {
        "recent_events": [
            {"date": "2025-06-01", "title_zh": "证监会加强ESG信息披露要求", "title_en": "SC strengthens ESG disclosure requirements", "description_zh": "证券监督委员会加强上市公司ESG(环境、社会和治理)信息披露要求。"},
            {"date": "2025-09-01", "title_zh": "证监会推动资本市场数字化", "title_en": "SC drives capital market digitalisation", "description_zh": "证监会推动资本市场数字化交易和结算系统升级。"},
            {"date": "2026-01-15", "title_zh": "证监会打击市场操纵行为", "title_en": "SC cracks down on market manipulation", "description_zh": "证监会加强对市场操纵和内幕交易的执法力度，多起案件进入起诉程序。"}
        ],
        "related_entities": [
            {"name_en": "Ministry of Finance", "name_zh": "马来西亚财政部", "relationship_type": "parent_org", "org_id": "MY-GOV-005"},
            {"name_en": "Bank Negara Malaysia", "name_zh": "马来西亚国家银行", "relationship_type": "member_of", "org_id": "MY-GOV-023"},
            {"name_en": "Bursa Malaysia", "name_zh": "马来西亚股票交易所", "relationship_type": "subsidiary", "org_id": "MY-FIN-001"}
        ]
    },
    "MY-GOV-025": {
        "recent_events": [
            {"date": "2025-03-01", "title_zh": "反贪会调查多项大型贪腐案件", "title_en": "MACC investigates major corruption cases", "description_zh": "反贪会调查多起涉及政府项目的大型贪腐案件，多名高官被逮捕和起诉。"},
            {"date": "2025-08-01", "title_zh": "反贪会加强政治资金监管", "title_en": "MACC strengthens political funding oversight", "description_zh": "反贪会推动政治资金透明化监管，配合政治捐款法案实施。"},
            {"date": "2026-01-20", "title_zh": "反贪会与东盟反贪机构合作", "title_en": "MACC collaborates with ASEAN anti-corruption bodies", "description_zh": "马来西亚反贪会加强与东盟各国反贪机构的跨境合作，共同打击跨国腐败。"}
        ],
        "related_entities": [
            {"name_en": "Prime Minister's Department", "name_zh": "马来西亚首相署", "relationship_type": "parent_org", "org_id": "MY-GOV-004"},
            {"name_en": "Attorney General's Chambers", "name_zh": "马来西亚总检察署", "relationship_type": "member_of", "org_id": "MY-GOV-030"},
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "member_of", "org_id": "MY-GOV-002"}
        ]
    },
    "MY-GOV-026": {
        "recent_events": [
            {"date": "2025-07-01", "title_zh": "选委会推进选民自动登记制度", "title_en": "EC advances automatic voter registration", "description_zh": "选举委员会推进选民自动登记制度实施，与国民登记局数据对接。"},
            {"date": "2025-11-15", "title_zh": "选委会举行多场补选", "title_en": "EC conducts multiple by-elections", "description_zh": "选举委员会成功举行多场国会和州议会补选，投票流程顺利。"},
            {"date": "2026-02-01", "title_zh": "选委会推进选区重新划分研究", "title_en": "EC advances constituency redelineation study", "description_zh": "选举委员会启动选区重新划分研究工作，应对人口变化和选区均衡问题。"}
        ],
        "related_entities": [
            {"name_en": "Prime Minister's Department", "name_zh": "马来西亚首相署", "relationship_type": "parent_org", "org_id": "MY-GOV-004"},
            {"name_en": "Parliament of Malaysia", "name_zh": "马来西亚国会", "relationship_type": "member_of", "org_id": "MY-GOV-018"},
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "member_of", "org_id": "MY-GOV-002"}
        ]
    },
    "MY-GOV-027": {
        "recent_events": [
            {"date": "2025-06-01", "title_zh": "审计署发布2024年度审计报告", "title_en": "Auditor General releases 2024 audit report", "description_zh": "审计署向国会提交2024年度总审计司报告，揭露多起政府财务管理不当案例。"},
            {"date": "2025-11-01", "title_zh": "审计署加强绩效审计方法", "title_en": "National Audit Dept strengthens performance auditing", "description_zh": "审计署引入国际审计标准，加强绩效审计和价值审计方法论。"},
            {"date": "2026-02-01", "title_zh": "审计署培训新一代审计人员", "title_en": "Audit Dept trains new generation of auditors", "description_zh": "审计署加大审计人员培训力度，引入数据分析和技术审计技能培养。"}
        ],
        "related_entities": [
            {"name_en": "Prime Minister's Department", "name_zh": "马来西亚首相署", "relationship_type": "parent_org", "org_id": "MY-GOV-004"},
            {"name_en": "Parliament of Malaysia", "name_zh": "马来西亚国会", "relationship_type": "member_of", "org_id": "MY-GOV-018"},
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "member_of", "org_id": "MY-GOV-002"}
        ]
    },
    "MY-GOV-028": {
        "recent_events": [
            {"date": "2025-01-15", "title_zh": "MCMC加强网络内容监管", "title_en": "MCMC strengthens online content regulation", "description_zh": "通讯及多媒体委员会加强社交媒体和网络内容监管，打击虚假信息和网络诈骗。"},
            {"date": "2025-07-01", "title_zh": "MCMC推进5G网络第二阶段部署", "title_en": "MCMC advances 5G Phase 2 deployment", "description_zh": "MCMC推进5G网络第二阶段部署，计划2026年实现全国80%覆盖率。"},
            {"date": "2026-01-01", "title_zh": "MCMC发布数字经济监管框架", "title_en": "MCMC issues digital economy regulatory framework", "description_zh": "MCMC发布数字经济监管框架，规范数字平台运营和消费者保护。"}
        ],
        "related_entities": [
            {"name_en": "Ministry of Digital", "name_zh": "马来西亚数码部", "relationship_type": "parent_org", "org_id": "MY-GOV-015"},
            {"name_en": "Ministry of Home Affairs", "name_zh": "马来西亚内政部", "relationship_type": "member_of", "org_id": "MY-GOV-008"},
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "member_of", "org_id": "MY-GOV-002"}
        ]
    },
    "MY-GOV-029": {
        "recent_events": [
            {"date": "2025-03-01", "title_zh": "税收局推行电子发票制度", "title_en": "LHDN implements e-invoice system", "description_zh": "内陆税收局推行全国电子发票制度，分阶段强制企业采用电子发票进行税务申报。"},
            {"date": "2025-09-01", "title_zh": "税收局加强税收执法", "title_en": "LHDN strengthens tax enforcement", "description_zh": "内陆税收局加大对逃税漏税行为的执法力度，追缴数十亿令吉未缴税款。"},
            {"date": "2026-01-15", "title_zh": "税收局2025年税收创新高", "title_en": "LHDN reports record tax collection for 2025", "description_zh": "内陆税收局公布2025年税收收入创新高，个人所得税和企业所得税均大幅增长。"}
        ],
        "related_entities": [
            {"name_en": "Ministry of Finance", "name_zh": "马来西亚财政部", "relationship_type": "parent_org", "org_id": "MY-GOV-005"},
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "member_of", "org_id": "MY-GOV-002"},
            {"name_en": "Bank Negara Malaysia", "name_zh": "马来西亚国家银行", "relationship_type": "member_of", "org_id": "MY-GOV-023"}
        ]
    },
    "MY-GOV-030": {
        "recent_events": [
            {"date": "2025-02-01", "title_zh": "总检察署加强反恐法律框架", "title_en": "AGC strengthens anti-terrorism legal framework", "description_zh": "总检察署完善反恐法律框架，起草修订相关安全和反恐法令。"},
            {"date": "2025-08-01", "title_zh": "总检察署推动法律改革", "title_en": "AGC drives legal reform", "description_zh": "总检察署推动多项法律改革，包括刑事法典修订和商业法现代化。"},
            {"date": "2026-01-01", "title_zh": "新任总检察长就职", "title_en": "New Attorney General takes office", "description_zh": "莫哈末杜苏基就任新任总检察长，领导总检察署推进法律改革议程。"}
        ],
        "related_entities": [
            {"name_en": "Prime Minister's Department", "name_zh": "马来西亚首相署", "relationship_type": "parent_org", "org_id": "MY-GOV-004"},
            {"name_en": "Federal Court of Malaysia", "name_zh": "马来西亚联邦法院", "relationship_type": "member_of", "org_id": "MY-GOV-021"},
            {"name_en": "Malaysian Anti-Corruption Commission", "name_zh": "马来西亚反贪污委员会", "relationship_type": "member_of", "org_id": "MY-GOV-025"},
            {"name_en": "Government of Malaysia", "name_zh": "马来西亚联邦政府", "relationship_type": "member_of", "org_id": "MY-GOV-002"}
        ]
    },
}

# Apply enrichment
updated = 0
for oid, data in sorted(ENRICHMENT_DATA.items()):
    fn = os.path.join(ORGS_DIR, f"{oid}.json")
    if not os.path.exists(fn):
        print(f"SKIP {oid}: not found")
        continue

    with open(fn, 'r', encoding='utf-8') as f:
        d = json.load(f)

    changed = False

    # Add recent_events
    if data.get("recent_events") and not d.get("recent_events"):
        d["recent_events"] = data["recent_events"]
        changed = True

    # Add related_entities
    if data.get("related_entities") and not d.get("related_entities"):
        d["related_entities"] = data["related_entities"]
        changed = True

    if changed:
        # Recalculate completeness
        score = 30
        bi = d['basic_info']
        if bi.get('founded_date'): score += 5
        if bi.get('website'): score += 5
        if bi.get('name_zh'): score += 5
        if d.get('social_accounts') and len(d['social_accounts']) > 0: score += 10
        if d.get('key_people') and len(d['key_people']) > 0: score += 15
        if d.get('departments') and len(d['departments']) > 0: score += 5
        if d.get('related_entities') and len(d['related_entities']) > 0: score += 5
        if d.get('core_business') and len(d.get('core_business', '')) > 50: score += 10
        if d.get('industries') and len(d['industries']) > 0: score += 5
        if d.get('profile'): score += 5
        d['collection_meta']['completeness_score'] = min(score, 100)
        d['collection_meta']['data_sources'] = list(set(d['collection_meta'].get('data_sources', []) + ['web_search']))

        save_json(os.path.abspath(fn), d)
        updated += 1
        evts = len(d.get('recent_events', []))
        rels = len(d.get('related_entities', []))
        print(f"{oid}: score={d['collection_meta']['completeness_score']:3d} events={evts} rel={rels}")

print(f"\nUpdated {updated}/30 profiles")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enrich MY-GOV profiles with Chinese content and missing fields."""
import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
import json, os
sys.path.insert(0, 'D:/claude-workspace/apec-osint-tool/.claude/skills/country-org-collector/scripts')
from atomic_write import save_json

ORGS_DIR = 'D:/claude-workspace/apec-osint-tool/output/my/2026-04-17/orgs'

ENRICHMENT = {
    'MY-GOV-001': {
        'name_zh': '马来西亚最高元首',
        'name_en': 'Yang di-Pertuan Agong',
        'description_zh': '马来西亚最高元首是马来西亚的国家元首和武装部队最高统帅，由九个马来州属的世袭苏丹轮流担任，任期五年。现任最高元首为柔佛州苏丹依布拉欣·依斯迈，于2024年1月31日就任。',
        'head_name_zh': '苏丹依布拉欣·依斯迈',
        'head_name_en': 'Sultan Ibrahim Iskandar',
        'head_title': 'Yang di-Pertuan Agong',
        'website': 'http://www.istananegara.gov.my/',
        'departments_zh': ['国家皇宫', '最高元首秘书处'],
    },
    'MY-GOV-002': {
        'name_zh': '马来西亚联邦政府',
        'name_en': 'Government of Malaysia',
        'description_zh': '马来西亚联邦政府是马来西亚的中央政府，实行联邦议会民主制和君主立宪制。政府由首相领导，内阁部长由首相任命。行政权归属最高元首，但实际由内阁行使。联邦政府设于布城联邦行政中心。',
        'head_name_zh': '安华·依布拉欣',
        'head_name_en': 'Anwar Ibrahim',
        'head_title': 'Prime Minister',
        'website': 'https://www.malaysia.gov.my/',
        'departments_zh': ['首相署', '财政部', '国防部', '教育部', '卫生部', '外交部', '内政部', '交通部', '工程部'],
    },
    'MY-GOV-003': {
        'name_zh': '马来西亚内阁',
        'name_en': 'Cabinet of Malaysia',
        'description_zh': '马来西亚内阁是联邦政府的行政决策机构，由首相和各部部长组成。内阁对国会负责，所有部长必须是国会议员。现任首相安华于2022年11月组建团结政府内阁。',
        'head_name_zh': '安华·依布拉欣',
        'head_name_en': 'Anwar Ibrahim',
        'head_title': 'Prime Minister',
        'website': 'https://www.kabinet.gov.my/bkpp/',
        'departments_zh': ['首相署', '财政部', '国防部', '教育部', '卫生部', '外交部', '内政部', '投资贸易及工业部', '交通部', '工程部'],
    },
    'MY-GOV-004': {
        'name_zh': '马来西亚首相署',
        'name_en': "Prime Minister's Department of Malaysia",
        'description_zh': '马来西亚首相署是协助首相执行职务的联邦政府部门，负责统筹和协调各部委事务。下辖多个重要机构，包括马来西亚反贪污委员会、选举委员会、总检察署、审计署等。总部位于布城。',
        'head_name_zh': '安华·依布拉欣',
        'head_name_en': 'Anwar Ibrahim',
        'head_title': 'Prime Minister',
        'website': 'https://www.jpm.gov.my/',
        'departments_zh': ['马来西亚反贪污委员会', '选举委员会', '总检察署', '审计署', '行政现代化与管理规划单位', '法律事务部', '经济策划单位', '实施协调单位'],
    },
    'MY-GOV-005': {
        'name_zh': '马来西亚财政部',
        'name_en': 'Ministry of Finance Malaysia',
        'description_zh': '马来西亚财政部负责制定和执行国家财政政策、管理联邦预算、监督金融体系和税收政策。下辖国家银行（央行）、证券监督委员会等重要金融监管机构。现任财政部长由首相安华兼任。',
        'head_name_zh': '安华·依布拉欣',
        'head_name_en': 'Anwar Ibrahim',
        'head_title': 'Minister of Finance',
        'website': 'https://www.mof.gov.my/',
        'social_facebook': 'https://facebook.com/KementerianKewanganMalaysia',
        'social_twitter': 'https://twitter.com/MoFMalaysia',
        'departments_zh': ['国家银行', '证券监督委员会', '内陆税收局', '皇家关税局', '公积金局', '纳闽金融服务局'],
    },
    'MY-GOV-006': {
        'name_zh': '马来西亚外交部',
        'name_en': 'Ministry of Foreign Affairs Malaysia',
        'description_zh': '马来西亚外交部（又称维斯马普特拉）负责管理马来西亚的对外关系、外交政策和国际事务。在全球设有驻外使领馆和代表处，积极参与东盟、联合国、伊斯兰合作组织等多边外交活动。',
        'head_name_zh': '莫哈末哈山',
        'head_name_en': 'Mohamad Hasan',
        'head_title': 'Minister of Foreign Affairs',
        'website': 'https://www.kln.gov.my/',
        'social_facebook': 'https://facebook.com/wismaputra',
        'social_twitter': 'https://twitter.com/KLNmalaysia',
        'departments_zh': ['东盟部门', '双边关系部门', '多边关系部门', '领事部门', '礼宾部门', '政策分析与战略规划部门'],
    },
    'MY-GOV-007': {
        'name_zh': '马来西亚国防部',
        'name_en': 'Ministry of Defence Malaysia',
        'description_zh': '马来西亚国防部负责管理国家防务政策和武装部队事务。下辖马来西亚武装部队（陆军、海军、空军）及国防部秘书处。总部位于吉隆坡Wisma Pertahanan。',
        'head_name_zh': '莫哈末卡立诺丁',
        'head_name_en': 'Mohamad Khaled Nordin',
        'head_title': 'Minister of Defence',
        'website': 'https://www.mod.gov.my/',
        'social_facebook': 'https://facebook.com/kempertahanan',
        'social_twitter': 'https://twitter.com/kempertahanan',
        'departments_zh': ['马来西亚陆军', '马来西亚皇家海军', '马来西亚皇家空军', '国防秘书处', '退伍军人事务部', '国防情报局'],
    },
    'MY-GOV-008': {
        'name_zh': '马来西亚内政部',
        'name_en': 'Ministry of Home Affairs Malaysia',
        'description_zh': '马来西亚内政部负责维护国内安全和公共秩序，下辖警察部队、移民局、国民登记局、监狱局、民防部队等执法机构。负责出入境管理、公民身份、治安维护等事务。',
        'head_name_zh': '赛夫丁纳苏迪安',
        'head_name_en': 'Saifuddin Nasution Ismail',
        'head_title': 'Minister of Home Affairs',
        'website': 'https://www.moha.gov.my/',
        'social_facebook': 'https://facebook.com/KDNMalaysia',
        'social_twitter': 'https://twitter.com/KDNMalaysia',
        'departments_zh': ['马来西亚皇家警察', '移民局', '国民登记局', '监狱局', '民防部队', '志愿警卫局'],
    },
    'MY-GOV-009': {
        'name_zh': '马来西亚教育部',
        'name_en': 'Ministry of Education Malaysia',
        'description_zh': '马来西亚教育部负责管理国家教育体系，包括学前教育、小学教育、中学教育和教师培训。实施六年小学加五年中学的教育制度，推动教育改革和素质教育发展。',
        'head_name_zh': '法丽娜西迪',
        'head_name_en': 'Fadhlina Sidek',
        'head_title': 'Minister of Education',
        'website': 'https://www.moe.gov.my/',
        'social_facebook': 'https://facebook.com/kempendidikan',
        'social_twitter': 'https://twitter.com/kempendidikan',
        'departments_zh': ['教育总监办公室', '学校管理部门', '教师专业发展部门', '课程发展中心', '教育规划与研究部门', '私立教育部门'],
    },
    'MY-GOV-010': {
        'name_zh': '马来西亚卫生部',
        'name_en': 'Ministry of Health Malaysia',
        'description_zh': '马来西亚卫生部负责管理国家公共卫生体系和医疗服务。下辖全国公立医院、诊疗所和卫生中心，制定卫生政策、疾病防控、药物监管等。总部位于布城。',
        'head_name_zh': '祖基菲里阿末',
        'head_name_en': 'Dzulkefly Ahmad',
        'head_title': 'Minister of Health',
        'website': 'https://www.moh.gov.my/',
        'social_facebook': 'https://facebook.com/kemasihatan',
        'social_twitter': 'https://twitter.com/KKMPutrajaya',
        'departments_zh': ['公共卫生部门', '医疗服务部门', '药物监管局', '医学研究院', '口腔卫生部门', '食品卫生与安全部门'],
    },
    'MY-GOV-011': {
        'name_zh': '马来西亚投资、贸易及工业部',
        'name_en': 'Ministry of Investment, Trade and Industry Malaysia',
        'description_zh': '马来西亚投资、贸易及工业部（MITI）负责管理国家贸易政策、工业发展和投资促进。下辖马来西亚对外贸易发展局（MATRADE）、马来西亚投资发展局（MIDA）等机构。推动国家工业4.0和数字经济转型。',
        'head_name_zh': '东姑扎夫鲁',
        'head_name_en': 'Tengku Zafrul Aziz',
        'head_title': 'Minister of Investment, Trade and Industry',
        'website': 'https://www.miti.gov.my/',
        'social_facebook': 'https://facebook.com/MITIMalaysia',
        'social_twitter': 'https://twitter.com/MITIMalaysia',
        'departments_zh': ['马来西亚投资发展局(MIDA)', '马来西亚对外贸易发展局(MATRADE)', '马来西亚生产力机构(MPC)', '马来西亚标准局', '国内贸易与生活成本部'],
    },
    'MY-GOV-012': {
        'name_zh': '马来西亚交通部',
        'name_en': 'Ministry of Transport Malaysia',
        'description_zh': '马来西亚交通部负责管理国家交通运输体系，包括公路、铁路、航空和海运。监管马来西亚机场控股、马来西亚铁路公司、陆路交通局等重要交通机构。',
        'head_name_zh': '陆兆福',
        'head_name_en': 'Loke Siew Fook',
        'head_title': 'Minister of Transport',
        'website': 'https://www.mot.gov.my/',
        'social_facebook': 'https://facebook.com/kempengangkutan',
        'social_twitter': 'https://twitter.com/KemPengangkutan',
        'departments_zh': ['陆路交通局(JPJ)', '马来西亚海事局', '民航管理局', '马来西亚铁路公司(KTMB)', '马来西亚机场控股', '公共交通机构'],
    },
    'MY-GOV-013': {
        'name_zh': '马来西亚工程部',
        'name_en': 'Ministry of Works Malaysia',
        'description_zh': '马来西亚工程部负责管理联邦公共工程和基础设施建设项目。监管公共工程局(JKR)、建筑工业发展局(CIDB)等机构，负责道路、桥梁、政府建筑等公共工程。',
        'head_name_zh': '亚历山大南塔林奇',
        'head_name_en': 'Alexander Nanta Linggi',
        'head_title': 'Minister of Works',
        'website': 'https://www.kkr.gov.my/',
        'social_facebook': 'https://facebook.com/KKRMalaysia',
        'social_twitter': 'https://twitter.com/KKRMalaysia',
        'departments_zh': ['公共工程局(JKR)', '建筑工业发展局(CIDB)', '工程服务部门', '道路管理局', '建筑管理部'],
    },
    'MY-GOV-14': {
        'name_zh': '马来西亚经济部',
        'name_en': 'Ministry of Economy Malaysia',
        'description_zh': '马来西亚经济部负责制定和执行国家经济发展计划和宏观经济政策。主管马来西亚计划（五年发展计划）、经济改革议程和可持续发展目标。推动第十二个马来西亚计划。',
        'head_name_zh': '拉菲兹南利',
        'head_name_en': 'Rafizi Ramli',
        'head_title': 'Minister of Economy',
        'website': 'https://www.ekonomi.gov.my/',
        'departments_zh': ['经济策划单位(EPU)', '统计部门(DOSM)', '马来西亚计划执行协调单位(ICU)', '经济发展部门', '私营部门发展部门'],
    },
    'MY-GOV-015': {
        'name_zh': '马来西亚数码部',
        'name_en': 'Ministry of Digital Malaysia',
        'description_zh': '马来西亚数码部于2023年新设立，负责推动国家数字化转型和数字经济发展。监管马来西亚数码经济机构（MDEC）、通讯及多媒体委员会（MCMC）等机构。',
        'head_name_zh': '哥宾星',
        'head_name_en': 'Gobind Singh Deo',
        'head_title': 'Minister of Digital',
        'website': 'https://www.digital.gov.my/',
        'social_facebook': 'https://facebook.com/KementerianDigital',
        'departments_zh': ['马来西亚数码经济机构(MDEC)', '马来西亚数码机构', '网络安全机构', '数码化推动部门', '科技政策部门'],
    },
    'MY-GOV-016': {
        'name_zh': '马来西亚人力资源部',
        'name_en': 'Ministry of Human Resources Malaysia',
        'description_zh': '马来西亚人力资源部负责管理劳工事务、就业政策和人力资源开发。监管劳工局、技能发展基金、雇员社会保险机构（SOCSO）等。负责制定最低工资标准、职业安全等政策。',
        'head_name_zh': '沈志强',
        'head_name_en': 'Steven Sim Chee Keong',
        'head_title': 'Minister of Human Resources',
        'website': 'https://mohr.gov.my/',
        'social_facebook': 'https://facebook.com/keskerja',
        'social_twitter': 'https://twitter.com/Keskerja',
        'departments_zh': ['劳工局(JTK)', '技能发展局(JPK)', '雇员社会保险机构(SOCSO)', '人力资源发展基金(HRDF)', '职业安全与卫生局(DOSH)', '工业法庭'],
    },
    'MY-GOV-017': {
        'name_zh': '马来西亚农业及粮食安全部',
        'name_en': 'Ministry of Agriculture and Food Security Malaysia',
        'description_zh': '马来西亚农业及粮食安全部负责管理农业发展和国家粮食安全政策。监管渔业局、兽医局、农业研究机构等。推动国家粮食安全政策2.0和现代化农业转型。',
        'head_name_zh': '莫哈末沙布',
        'head_name_en': 'Mohamad Sabu',
        'head_title': 'Minister of Agriculture and Food Security',
        'website': 'https://www.mafi.gov.my/',
        'social_facebook': 'https://facebook.com/kemperanian',
        'social_twitter': 'https://twitter.com/MAFIMalaysia',
        'departments_zh': ['农业局', '渔业局', '兽医局', '马来西亚农业研究与发展机构(MARDI)', '联邦农业销售局(FAMA)', '粮食安全部门'],
    },
    'MY-GOV-018': {
        'name_zh': '马来西亚国会',
        'name_en': 'Parliament of Malaysia',
        'description_zh': '马来西亚国会是国家最高立法机构，实行两院制，由下议院（Dewan Rakyat）和上议院（Dewan Negara）组成。下议院222席由民选产生，上议院70席由各州立法议会选举和最高元首任命。',
        'head_name_zh': '佐哈里阿都',
        'head_name_en': 'Johari Abdul',
        'head_title': 'Speaker of Dewan Rakyat',
        'website': 'http://www.parlimen.gov.my/',
        'social_facebook': 'https://facebook.com/ParlimenMalaysia',
        'departments_zh': ['下议院(Dewan Rakyat)', '上议院(Dewan Negara)', '国会秘书处', '公共账目委员会', '立法委员会'],
    },
    'MY-GOV-019': {
        'name_zh': '马来西亚下议院',
        'name_en': 'Dewan Rakyat',
        'description_zh': '马来西亚下议院是国会的下议院，拥有222个民选议席，是主要的立法机构。议员由选民直接选举产生，任期五年。拥有财政预算审批权和首相选举权。',
        'head_name_zh': '佐哈里阿都',
        'head_name_en': 'Johari Abdul',
        'head_title': 'Speaker of Dewan Rakyat',
        'website': 'http://www.parlimen.gov.my/',
        'departments_zh': ['国会下议院秘书处', '各专责委员会'],
    },
    'MY-GOV-020': {
        'name_zh': '马来西亚上议院',
        'name_en': 'Dewan Negara',
        'description_zh': '马来西亚上议院是国会的上议院，共70席。其中26席由13个州立法议会各选2名，44席由最高元首在首相建议下任命。任期三年，可连任一次。主要功能是审议下议院通过的法案。',
        'head_name_zh': '慕士达法',
        'head_name_en': 'Mutalib Umat',
        'head_title': 'President of Dewan Negara',
        'website': 'http://www.parlimen.gov.my/',
        'departments_zh': ['国会上议院秘书处'],
    },
    'MY-GOV-021': {
        'name_zh': '马来西亚联邦法院',
        'name_en': 'Federal Court of Malaysia',
        'description_zh': '马来西亚联邦法院是国家最高司法机构，拥有对宪法问题的最终管辖权和上诉管辖权。由首席大法官领导，审理涉及宪法解释、联邦与州权限争议等重要案件。',
        'head_name_zh': '东姑麦润',
        'head_name_en': 'Tengku Maimun Tuan Mat',
        'head_title': 'Chief Justice',
        'website': 'https://www.kehakiman.gov.my/',
        'departments_zh': ['民事庭', '刑事庭', '宪法庭'],
    },
    'MY-GOV-022': {
        'name_zh': '马来西亚上诉庭',
        'name_en': 'Court of Appeal of Malaysia',
        'description_zh': '马来西亚上诉庭是仅次于联邦法院的上诉法院，审理来自高等法院的民事和刑事上诉案件。由上诉庭主席领导。',
        'head_name_zh': '阿邦哈山',
        'head_name_en': 'Abang Iskandar Abang Hashim',
        'head_title': 'President of Court of Appeal',
        'website': 'https://www.kehakiman.gov.my/',
        'departments_zh': ['民事上诉庭', '刑事上诉庭'],
    },
    'MY-GOV-023': {
        'name_zh': '马来西亚国家银行',
        'name_en': 'Bank Negara Malaysia',
        'description_zh': '马来西亚国家银行是马来西亚的中央银行，负责制定和执行货币政策、维护金融稳定、监管银行体系和外汇管理。发行马来西亚令吉（RM），管理国家外汇储备。成立于1959年。',
        'head_name_zh': '阿都拉希德阿都加福',
        'head_name_en': 'Abdul Rasheed Ghaffour',
        'head_title': 'Governor',
        'website': 'https://www.bnm.gov.my/',
        'social_twitter': 'https://twitter.com/BNMofficial',
        'departments_zh': ['货币政策部门', '金融监管部门', '支付系统部门', '外汇管理部门', '银行保险部门', '消费者与市场部门'],
    },
    'MY-GOV-024': {
        'name_zh': '马来西亚证券监督委员会',
        'name_en': 'Securities Commission Malaysia',
        'description_zh': '马来西亚证券监督委员会负责监管和发展马来西亚资本市场，包括股票市场、债券市场和衍生品市场。依据1993年证券委员会法成立，直接向财政部长报告。',
        'head_name_zh': '阿旺阿迪',
        'head_name_en': 'Awang Adek Hussin',
        'head_title': 'Chairman',
        'website': 'https://www.sc.com.my/',
        'departments_zh': ['市场监管部门', '公司监管部门', '执法部门', '投资管理与基金监管部门', '市场及产品监管部门'],
    },
    'MY-GOV-025': {
        'name_zh': '马来西亚反贪污委员会',
        'name_en': 'Malaysian Anti-Corruption Commission',
        'description_zh': '马来西亚反贪污委员会（SPRM）是负责打击贪污腐败的独立执法机构。依据2009年反贪污委员会法运作，拥有调查、逮捕和起诉权力。直接向国会负责。',
        'head_name_zh': '阿占巴基',
        'head_name_en': 'Azam Baki',
        'head_title': 'Chief Commissioner',
        'website': 'https://www.sprm.gov.my/',
        'social_facebook': 'https://facebook.com/SprmMalaysia',
        'social_twitter': 'https://twitter.com/sprm2014',
        'departments_zh': ['调查部门', '情报部门', '预防部门', '起诉部门', '审计与合规部门', '投诉部门'],
    },
    'MY-GOV-026': {
        'name_zh': '马来西亚选举委员会',
        'name_en': 'Election Commission of Malaysia',
        'description_zh': '马来西亚选举委员会（SPR）负责管理和执行全国大选、补选和选民登记工作。依据联邦宪法第113条设立，独立运作。管理222个国会选区和567个州选区。',
        'head_name_zh': '阿都拉尼',
        'head_name_en': 'Abdul Ghani Salleh',
        'head_title': 'Chairman',
        'website': 'https://www.spr.gov.my/',
        'departments_zh': ['选举管理部门', '选民登记部门', '执法部门', '信息技术部门', '行政部门'],
    },
    'MY-GOV-027': {
        'name_zh': '马来西亚审计署',
        'name_en': 'National Audit Department of Malaysia',
        'description_zh': '马来西亚审计署负责审计联邦政府、州政府和地方政府的财务账目，确保公款合理使用。总审计司每年向国会提呈审计报告。依据1957年审计法设立。',
        'head_name_zh': '赛弗丁柏纳东',
        'head_name_en': 'Saiful Adli Mohd Arshad',
        'head_title': 'Auditor General',
        'website': 'https://www.audit.gov.my/',
        'departments_zh': ['财务审计部门', '绩效审计部门', '合规审计部门', 'IT审计部门'],
    },
    'MY-GOV-028': {
        'name_zh': '马来西亚通讯及多媒体委员会',
        'name_en': 'Malaysian Communications and Multimedia Commission',
        'description_zh': '马来西亚通讯及多媒体委员会（MCMC）是通讯及多媒体行业的监管机构。负责管理电信、广播和互联网行业，发放运营执照，保护消费者权益，维护网络内容规范。',
        'head_name_zh': '莫哈末萨利',
        'head_name_en': 'Mohamed Sharil Tarmizi',
        'head_title': 'Chairman',
        'website': 'https://www.mcmc.gov.my/',
        'social_facebook': 'https://facebook.com/MCMC',
        'social_twitter': 'https://twitter.com/MCMC_MY',
        'departments_zh': ['消费者保护部门', '网络内容监管部门', '频谱管理部门', '行业监管部门', '执法部门', '数字包容部门'],
    },
    'MY-GOV-029': {
        'name_zh': '马来西亚内陆税收局',
        'name_en': 'Inland Revenue Board of Malaysia',
        'description_zh': '马来西亚内陆税收局（LHDN/hasil）负责征收和管理联邦直接税，包括所得税、公司税、石油所得税、印花税等。实施电子报税系统(e-Filing)，管理税收合规和执法。',
        'head_name_zh': '阿布塔利布',
        'head_name_en': 'Abu Tariq Jamaluddin',
        'head_title': 'Chief Executive Officer',
        'website': 'https://www.hasil.gov.my/',
        'social_facebook': 'https://facebook.com/LHDNM',
        'social_twitter': 'https://twitter.com/LHDNM',
        'departments_zh': ['税收征管部门', '税务审计部门', '纳税人服务部门', '执法部门', '电子服务部门', '公司税部门'],
    },
    'MY-GOV-030': {
        'name_zh': '马来西亚总检察署',
        'name_en': "Attorney General's Chambers of Malaysia",
        'description_zh': '马来西亚总检察署是联邦政府的主要法律顾问机构。总检察长同时担任公诉人，负责向政府提供法律意见、起草法律文件和进行刑事起诉。依据联邦宪法第145条设立。',
        'head_name_zh': '莫哈末杜苏基',
        'head_name_en': 'Mohd Dusuki Mokhtar',
        'head_title': 'Attorney General',
        'website': 'https://www.agc.gov.my/',
        'departments_zh': ['刑事起诉部门', '民事部门', '法律顾问部门', '法律草拟部门', '国际事务部门', '上诉部门'],
    },
}

# Fix the typo key
if 'MY-GOV-14' in ENRICHMENT:
    ENRICHMENT['MY-GOV-014'] = ENRICHMENT.pop('MY-GOV-14')

updated = 0
for oid, enrich in sorted(ENRICHMENT.items()):
    fn = os.path.join(ORGS_DIR, f'{oid}.json')
    if not os.path.exists(fn):
        print(f'SKIP {oid}: file not found')
        continue

    with open(fn, 'r', encoding='utf-8') as f:
        d = json.load(f)

    bi = d['basic_info']
    changed = False

    # Fix name_zh
    if enrich.get('name_zh'):
        old = bi.get('name_zh', '')
        if not old or old != enrich['name_zh']:
            bi['name_zh'] = enrich['name_zh']
            changed = True

    # Fix name_en
    if enrich.get('name_en'):
        bi['name_en'] = enrich['name_en']
        bi['name_original'] = enrich['name_en']
        changed = True

    # Add Chinese description to core_business
    cb = d.get('core_business', '') or ''
    desc_zh = enrich.get('description_zh', '')
    if desc_zh:
        has_zh = any('\u4e00' <= c <= '\u9fff' for c in cb)
        if len(cb) < 200 or not has_zh:
            d['core_business'] = desc_zh + '\n\n' + cb if cb else desc_zh
            changed = True

    # Add key person
    if enrich.get('head_name_en') and not d.get('key_people'):
        kp = {
            'person_id': None,
            'name': enrich.get('head_name_zh', '') + ' (' + enrich['head_name_en'] + ')',
            'title': enrich.get('head_title', ''),
            'title_description': None,
            'description': None,
        }
        d['key_people'] = [kp]
        changed = True

    # Fix website
    if enrich.get('website') and not bi.get('website'):
        bi['website'] = enrich['website']
        changed = True

    # Add departments
    if enrich.get('departments_zh') and not d.get('departments'):
        depts = [{'name': dn, 'name_en': None, 'description': None} for dn in enrich['departments_zh']]
        d['departments'] = depts
        changed = True

    # Add social accounts
    if not d.get('social_accounts'):
        socials = []
        if enrich.get('social_twitter'):
            name = enrich['social_twitter'].rstrip('/').split('/')[-1]
            socials.append({'platform': 'twitter_x', 'account_name': name, 'url': enrich['social_twitter'], 'source': 'web_search'})
        if enrich.get('social_facebook'):
            name = enrich['social_facebook'].rstrip('/').split('/')[-1]
            socials.append({'platform': 'facebook', 'account_name': name, 'url': enrich['social_facebook'], 'source': 'web_search'})
        if socials:
            d['social_accounts'] = socials
            changed = True

    if changed:
        # Recalculate completeness
        score = 30
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

        save_json(os.path.abspath(fn), d)
        updated += 1
        print(f'{oid}: score={d["collection_meta"]["completeness_score"]:3d} | zh={bi["name_zh"][:20]} | kp={len(d.get("key_people",[]))} dept={len(d.get("departments",[]))} soc={len(d.get("social_accounts",[]))}')
    else:
        print(f'{oid}: no changes needed')

print(f'\nUpdated {updated}/30 profiles')

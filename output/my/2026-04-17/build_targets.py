#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build _target_orgs.json for Malaysia overview collection"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

target_orgs = [
  # ===== GOV: Government Institutions =====
  {"category": "GOV", "name_en": "Yang di-Pertuan Agong", "name_zh": "马来西亚最高元首", "org_subtype": "head_of_state", "qid": "Q331859"},
  {"category": "GOV", "name_en": "Government of Malaysia", "name_zh": "马来西亚政府", "org_subtype": "cabinet", "qid": "Q15973746"},
  {"category": "GOV", "name_en": "Cabinet of Malaysia", "name_zh": "马来西亚内阁", "org_subtype": "cabinet", "qid": "Q5779753"},
  {"category": "GOV", "name_en": "Prime Minister's Department", "name_zh": "马来西亚首相署", "org_subtype": "gov_department", "qid": "Q55618239"},
  # Ministries
  {"category": "GOV", "name_en": "Ministry of Finance Malaysia", "name_zh": "马来西亚财政部", "org_subtype": "ministry", "qid": "Q6868956"},
  {"category": "GOV", "name_en": "Ministry of Foreign Affairs Malaysia", "name_zh": "马来西亚外交部", "org_subtype": "ministry", "qid": "Q6868989"},
  {"category": "GOV", "name_en": "Ministry of Defence Malaysia", "name_zh": "马来西亚国防部", "org_subtype": "ministry", "qid": "Q6868977"},
  {"category": "GOV", "name_en": "Ministry of Home Affairs Malaysia", "name_zh": "马来西亚内政部", "org_subtype": "ministry", "qid": "Q6868984"},
  {"category": "GOV", "name_en": "Ministry of Education Malaysia", "name_zh": "马来西亚教育部", "org_subtype": "ministry", "qid": "Q6868973"},
  {"category": "GOV", "name_en": "Ministry of Health Malaysia", "name_zh": "马来西亚卫生部", "org_subtype": "ministry", "qid": "Q6868982"},
  {"category": "GOV", "name_en": "Ministry of International Trade and Industry (MITI)", "name_zh": "马来西亚国际贸易与工业部", "org_subtype": "ministry", "qid": "Q6868988"},
  {"category": "GOV", "name_en": "Ministry of Transport Malaysia", "name_zh": "马来西亚交通部", "org_subtype": "ministry", "qid": "Q6868999"},
  {"category": "GOV", "name_en": "Ministry of Works Malaysia", "name_zh": "马来西亚工程部", "org_subtype": "ministry", "qid": "Q6869002"},
  {"category": "GOV", "name_en": "Ministry of Natural Resources and Environmental Sustainability", "name_zh": "马来西亚天然资源及环境永续部", "org_subtype": "ministry", "qid": None},
  {"category": "GOV", "name_en": "Ministry of Economy", "name_zh": "马来西亚经济部", "org_subtype": "ministry", "qid": None},
  {"category": "GOV", "name_en": "Ministry of Digital", "name_zh": "马来西亚数码部", "org_subtype": "ministry", "qid": None},
  {"category": "GOV", "name_en": "Ministry of Human Resources", "name_zh": "马来西亚人力资源部", "org_subtype": "ministry", "qid": "Q6868986"},
  {"category": "GOV", "name_en": "Ministry of Agriculture and Food Security", "name_zh": "马来西亚农业及粮食安全部", "org_subtype": "ministry", "qid": "Q6868967"},
  # Legislature
  {"category": "GOV", "name_en": "Parliament of Malaysia", "name_zh": "马来西亚国会", "org_subtype": "legislature", "qid": "Q850503"},
  {"category": "GOV", "name_en": "Dewan Rakyat", "name_zh": "马来西亚下议院", "org_subtype": "legislature", "qid": "Q3379859"},
  {"category": "GOV", "name_en": "Dewan Negara", "name_zh": "马来西亚上议院", "org_subtype": "legislature", "qid": "Q3379860"},
  # Judiciary
  {"category": "GOV", "name_en": "Federal Court of Malaysia", "name_zh": "马来西亚联邦法院", "org_subtype": "judiciary", "qid": "Q5016965"},
  {"category": "GOV", "name_en": "Court of Appeal of Malaysia", "name_zh": "马来西亚上诉庭", "org_subtype": "judiciary", "qid": "Q5449601"},
  # Regulatory / Statutory
  {"category": "GOV", "name_en": "Bank Negara Malaysia", "name_zh": "马来西亚国家银行（央行）", "org_subtype": "regulatory_agency", "qid": "Q1648252"},
  {"category": "GOV", "name_en": "Securities Commission Malaysia", "name_zh": "马来西亚证券监督委员会", "org_subtype": "regulatory_agency", "qid": "Q7442418"},
  {"category": "GOV", "name_en": "Malaysian Anti-Corruption Commission (MACC)", "name_zh": "马来西亚反贪污委员会", "org_subtype": "independent_organ", "qid": "Q6743566"},
  {"category": "GOV", "name_en": "Election Commission of Malaysia", "name_zh": "马来西亚选举委员会", "org_subtype": "independent_organ", "qid": "Q1320133"},
  {"category": "GOV", "name_en": "Auditor General of Malaysia", "name_zh": "马来西亚审计署", "org_subtype": "independent_organ", "qid": "Q4818671"},
  {"category": "GOV", "name_en": "Malaysian Communications and Multimedia Commission (MCMC)", "name_zh": "马来西亚通讯及多媒体委员会", "org_subtype": "regulatory_agency", "qid": "Q6714388"},
  {"category": "GOV", "name_en": "Inland Revenue Board of Malaysia (LHDN)", "name_zh": "马来西亚内陆税收局", "org_subtype": "statutory_board", "qid": "Q6032772"},
  {"category": "GOV", "name_en": "Attorney General's Chambers of Malaysia", "name_zh": "马来西亚总检察署", "org_subtype": "gov_department", "qid": "Q4818655"},

  # ===== SOE: State-Owned / GLCs =====
  {"category": "SOE", "name_en": "Petronas", "name_zh": "马来西亚国家石油公司", "org_subtype": "state_owned_enterprise", "qid": "Q221692"},
  {"category": "SOE", "name_en": "Khazanah Nasional", "name_zh": "马来西亚国库控股", "org_subtype": "sovereign_wealth_fund", "qid": "Q1781564"},
  {"category": "SOE", "name_en": "Permodalan Nasional Berhad (PNB)", "name_zh": "马来西亚国民投资机构", "org_subtype": "sovereign_wealth_fund", "qid": "Q4206786"},
  {"category": "SOE", "name_en": "Employees Provident Fund (EPF)", "name_zh": "雇员公积金局", "org_subtype": "sovereign_wealth_fund", "qid": "Q5371576"},
  {"category": "SOE", "name_en": "Retirement Fund Incorporated (KWAP)", "name_zh": "退休基金局", "org_subtype": "sovereign_wealth_fund", "qid": "Q7314079"},
  {"category": "SOE", "name_en": "Armed Forces Fund Board (LTAT)", "name_zh": "武装部队基金局", "org_subtype": "sovereign_wealth_fund", "qid": "Q11497665"},
  {"category": "SOE", "name_en": "Tenaga Nasional Berhad (TNB)", "name_zh": "马来西亚国家能源", "org_subtype": "gov_linked_company", "qid": "Q7694861"},
  {"category": "SOE", "name_en": "Telekom Malaysia Berhad (TM)", "name_zh": "马来西亚电信", "org_subtype": "gov_linked_company", "qid": "Q1623452"},
  {"category": "SOE", "name_en": "Sime Darby Berhad", "name_zh": "森那美集团", "org_subtype": "gov_linked_company", "qid": "Q7518764"},
  {"category": "SOE", "name_en": "Malaysia Airlines Berhad", "name_zh": "马来西亚航空", "org_subtype": "gov_linked_company", "qid": "Q1881272"},
  {"category": "SOE", "name_en": "Malaysia Airports Holdings Berhad", "name_zh": "马来西亚机场控股", "org_subtype": "gov_linked_company", "qid": "Q6713699"},
  {"category": "SOE", "name_en": "MRT Corporation", "name_zh": "MRT企业", "org_subtype": "gov_linked_company", "qid": "Q6715471"},
  {"category": "SOE", "name_en": "Prasarana Malaysia", "name_zh": "马来西亚基建公司", "org_subtype": "gov_linked_company", "qid": "Q4209298"},
  {"category": "SOE", "name_en": "PLUS Malaysia Berhad", "name_zh": "南北大道公司", "org_subtype": "gov_linked_company", "qid": "Q7116810"},
  {"category": "SOE", "name_en": "Lembaga Tabung Haji", "name_zh": "马来西亚朝圣基金局", "org_subtype": "gov_linked_company", "qid": "Q4022849"},
  {"category": "SOE", "name_en": "UEM Group Berhad", "name_zh": "UEM集团", "org_subtype": "gov_linked_company", "qid": "Q7873321"},
  {"category": "SOE", "name_en": "FELDA", "name_zh": "马来西亚联邦土地发展局", "org_subtype": "gov_linked_company", "qid": "Q5422585"},
  {"category": "SOE", "name_en": "Boustead Holdings Berhad", "name_zh": "宝德集团", "org_subtype": "gov_linked_company", "qid": "Q4950735"},
  {"category": "SOE", "name_en": "Bank Rakyat", "name_zh": "人民银行", "org_subtype": "gov_linked_company", "qid": "Q4856633"},
  {"category": "SOE", "name_en": "MISC Berhad", "name_zh": "马来西亚国际船务", "org_subtype": "gov_linked_company", "qid": "Q6715393"},
  {"category": "SOE", "name_en": "DRB-HICOM Berhad", "name_zh": "DRB-HICOM集团", "org_subtype": "gov_linked_company", "qid": "Q5205296"},
  {"category": "SOE", "name_en": "MMC Corporation Berhad", "name_zh": "MMC集团", "org_subtype": "gov_linked_company", "qid": "Q6714965"},
  {"category": "SOE", "name_en": "Malakoff Corporation Berhad", "name_zh": "马拉科夫公司", "org_subtype": "gov_linked_company", "qid": "Q6711697"},
  {"category": "SOE", "name_en": "Agrobank", "name_zh": "农业银行", "org_subtype": "gov_linked_company", "qid": "Q4694216"},

  # ===== CORP: Major Corporations =====
  {"category": "CORP", "name_en": "CIMB Group Holdings", "name_zh": "联昌银行集团", "org_subtype": "publicly_listed", "qid": "Q3045976"},
  {"category": "CORP", "name_en": "Public Bank Berhad", "name_zh": "大众银行", "org_subtype": "publicly_listed", "qid": "Q3046561"},
  {"category": "CORP", "name_en": "Axiata Group", "name_zh": "亚通集团", "org_subtype": "publicly_listed", "qid": "Q792500"},
  {"category": "CORP", "name_en": "YTL Corporation", "name_zh": "杨忠礼集团", "org_subtype": "publicly_listed", "qid": "Q842437"},
  {"category": "CORP", "name_en": "Hong Leong Group Malaysia", "name_zh": "丰隆集团（马来西亚）", "org_subtype": "publicly_listed", "qid": "Q4206859"},
  {"category": "CORP", "name_en": "CelcomDigi Berhad", "name_zh": "天地通数码", "org_subtype": "publicly_listed", "qid": "Q3268530"},
  {"category": "CORP", "name_en": "IOI Corporation", "name_zh": "IOI集团", "org_subtype": "publicly_listed", "qid": "Q5971008"},
  {"category": "CORP", "name_en": "Kuala Lumpur Kepong Berhad", "name_zh": "吉隆坡甲洞集团", "org_subtype": "publicly_listed", "qid": "Q24259"},
  {"category": "CORP", "name_en": "Genting Group", "name_zh": "云顶集团", "org_subtype": "publicly_listed", "qid": "Q5532412"},
  {"category": "CORP", "name_en": "Grab Holdings", "name_zh": "Grab控股", "org_subtype": "publicly_listed", "qid": "Q20873932"},
  {"category": "CORP", "name_en": "Marrybrown", "name_zh": "玛利亚快餐", "org_subtype": "private_company", "qid": "Q3380773"},
  {"category": "CORP", "name_en": "Petronas Chemicals Group", "name_zh": "国油石化集团", "org_subtype": "publicly_listed", "qid": "Q7168409"},

  # ===== FIN: Financial Institutions =====
  {"category": "FIN", "name_en": "Bursa Malaysia", "name_zh": "马来西亚交易所", "org_subtype": "asset_management", "qid": "Q930547"},
  {"category": "FIN", "name_en": "Bank Islam Malaysia", "name_zh": "马来西亚伊斯兰银行", "org_subtype": "commercial_bank", "qid": "Q4115279"},
  {"category": "FIN", "name_en": "AmBank Group", "name_zh": "安联银行集团", "org_subtype": "commercial_bank", "qid": "Q4132947"},
  {"category": "FIN", "name_en": "RHB Bank", "name_zh": "RHB银行", "org_subtype": "commercial_bank", "qid": "Q4207443"},
  {"category": "FIN", "name_en": "Affin Bank", "name_zh": "Affin银行", "org_subtype": "commercial_bank", "qid": "Q4688929"},
  {"category": "FIN", "name_en": "Bank Pembangunan Malaysia", "name_zh": "马来西亚发展银行", "org_subtype": "commercial_bank", "qid": None},

  # ===== ACAD: Academic Institutions =====
  {"category": "ACAD", "name_en": "Universiti Malaya", "name_zh": "马来亚大学", "org_subtype": "university", "qid": "Q665667"},
  {"category": "ACAD", "name_en": "Universiti Kebangsaan Malaysia (UKM)", "name_zh": "马来西亚国民大学", "org_subtype": "university", "qid": "Q839508"},
  {"category": "ACAD", "name_en": "Universiti Sains Malaysia (USM)", "name_zh": "马来西亚理科大学", "org_subtype": "university", "qid": "Q1141385"},
  {"category": "ACAD", "name_en": "Universiti Putra Malaysia (UPM)", "name_zh": "马来西亚博特拉大学", "org_subtype": "university", "qid": "Q1414514"},
  {"category": "ACAD", "name_en": "Universiti Teknologi Malaysia (UTM)", "name_zh": "马来西亚工艺大学", "org_subtype": "university", "qid": "Q802983"},
  {"category": "ACAD", "name_en": "Universiti Teknologi MARA (UiTM)", "name_zh": "马来西亚玛拉工艺大学", "org_subtype": "university", "qid": "Q1543660"},
  {"category": "ACAD", "name_en": "International Islamic University Malaysia (IIUM)", "name_zh": "马来西亚国际伊斯兰大学", "org_subtype": "university", "qid": "Q1373085"},
  {"category": "ACAD", "name_en": "Universiti Utara Malaysia (UUM)", "name_zh": "马来西亚北方大学", "org_subtype": "university", "qid": "Q1414516"},
  {"category": "ACAD", "name_en": "Universiti Malaysia Sabah (UMS)", "name_zh": "马来西亚沙巴大学", "org_subtype": "university", "qid": "Q1141387"},
  {"category": "ACAD", "name_en": "Universiti Malaysia Sarawak (UNIMAS)", "name_zh": "马来西亚砂拉越大学", "org_subtype": "university", "qid": "Q1141386"},
  {"category": "ACAD", "name_en": "Taylor's University", "name_zh": "泰勒大学", "org_subtype": "university", "qid": "Q841775"},
  {"category": "ACAD", "name_en": "Sunway University", "name_zh": "双威大学", "org_subtype": "university", "qid": "Q4475815"},
  {"category": "ACAD", "name_en": "Institute of Strategic and International Studies Malaysia (ISIS)", "name_zh": "马来西亚战略与国际问题研究所", "org_subtype": "think_tank", "qid": "Q6041640"},

  # ===== MEDIA: Media Organizations =====
  {"category": "MEDIA", "name_en": "Radio Televisyen Malaysia (RTM)", "name_zh": "马来西亚广播电视", "org_subtype": "broadcaster", "qid": "Q177747"},
  {"category": "MEDIA", "name_en": "Astro Malaysia Holdings", "name_zh": "马来西亚Astro集团", "org_subtype": "broadcaster", "qid": "Q3242264"},
  {"category": "MEDIA", "name_en": "Media Prima Berhad", "name_zh": "首要媒体集团", "org_subtype": "broadcaster", "qid": "Q6807754"},
  {"category": "MEDIA", "name_en": "The Star (Malaysia)", "name_zh": "星报", "org_subtype": "newspaper", "qid": "Q3538418"},
  {"category": "MEDIA", "name_en": "New Straits Times", "name_zh": "新海峡时报", "org_subtype": "newspaper", "qid": "Q3265894"},
  {"category": "MEDIA", "name_en": "Utusan Malaysia", "name_zh": "马来西亚前锋报", "org_subtype": "newspaper", "qid": "Q3538445"},
  {"category": "MEDIA", "name_en": "Malaysiakini", "name_zh": "当今大马", "org_subtype": "digital_media", "qid": "Q14955038"},
  {"category": "MEDIA", "name_en": "Free Malaysia Today", "name_zh": "今日自由大马", "org_subtype": "digital_media", "qid": None},
  {"category": "MEDIA", "name_en": "Bernama", "name_zh": "马来西亚国家新闻社", "org_subtype": "news_agency", "qid": "Q822992"},

  # ===== PARTY: Political Parties =====
  {"category": "PARTY", "name_en": "United Malays National Organisation (UMNO)", "name_zh": "马来民族统一机构", "org_subtype": "ruling_party", "qid": "Q1668154"},
  {"category": "PARTY", "name_en": "People's Justice Party (PKR)", "name_zh": "人民公正党", "org_subtype": "opposition_party", "qid": "Q1756601"},
  {"category": "PARTY", "name_en": "Democratic Action Party (DAP)", "name_zh": "民主行动党", "org_subtype": "opposition_party", "qid": "Q1185837"},
  {"category": "PARTY", "name_en": "Malaysian Islamic Party (PAS)", "name_zh": "马来西亚伊斯兰党", "org_subtype": "opposition_party", "qid": "Q1547025"},
  {"category": "PARTY", "name_en": "Barisan Nasional (BN)", "name_zh": "国民阵线", "org_subtype": "coalition", "qid": "Q808210"},
  {"category": "PARTY", "name_en": "Pakatan Harapan (PH)", "name_zh": "希望联盟", "org_subtype": "coalition", "qid": "Q20976241"},
  {"category": "PARTY", "name_en": "Perikatan Nasional (PN)", "name_zh": "国民联盟", "org_subtype": "coalition", "qid": "Q66360472"},
  {"category": "PARTY", "name_en": "Malaysian Chinese Association (MCA)", "name_zh": "马来西亚华人公会", "org_subtype": "opposition_party", "qid": "Q1886920"},
  {"category": "PARTY", "name_en": "Malaysian Indian Congress (MIC)", "name_zh": "马来西亚印度国民大会党", "org_subtype": "opposition_party", "qid": "Q958983"},
  {"category": "PARTY", "name_en": "National Trust Party (Amanah)", "name_zh": "国家诚信党", "org_subtype": "opposition_party", "qid": "Q4919308"},
  {"category": "PARTY", "name_en": "Parti Pesaka Bumiputera Bersatu (PBB)", "name_zh": "土保党", "org_subtype": "ruling_party", "qid": "Q4918646"},
  {"category": "PARTY", "name_en": "Gabungan Parti Sarawak (GPS)", "name_zh": "砂拉越政党联盟", "org_subtype": "coalition", "qid": "Q56242328"},
  {"category": "PARTY", "name_en": "Gabungan Rakyat Sabah (GRS)", "name_zh": "沙巴人民联盟", "org_subtype": "coalition", "qid": "Q97553035"},
  {"category": "PARTY", "name_en": "Parti Pribumi Bersatu Malaysia (Bersatu)", "name_zh": "土著团结党", "org_subtype": "opposition_party", "qid": "Q26740588"},
  {"category": "PARTY", "name_en": "Socialist Party of Malaysia (PSM)", "name_zh": "马来西亚社会主义党", "org_subtype": "opposition_party", "qid": "Q857555"},
  {"category": "PARTY", "name_en": "United Sabah Party (PBS)", "name_zh": "沙巴团结党", "org_subtype": "opposition_party", "qid": "Q1635641"},
  {"category": "PARTY", "name_en": "Sarawak United Peoples' Party (SUPP)", "name_zh": "砂拉越人民联合党", "org_subtype": "opposition_party", "qid": "Q1100205"},

  # ===== NGO: Non-Governmental Organizations =====
  {"category": "NGO", "name_en": "Malaysian Red Crescent Society", "name_zh": "马来西亚红新月会", "org_subtype": "humanitarian_org", "qid": "Q6713814"},
  {"category": "NGO", "name_en": "MERCY Malaysia", "name_zh": "马来西亚慈悲援助", "org_subtype": "humanitarian_org", "qid": "Q6715785"},
  {"category": "NGO", "name_en": "Transparency International Malaysia", "name_zh": "透明国际马来西亚分会", "org_subtype": "advocacy_group", "qid": "Q7835260"},
  {"category": "NGO", "name_en": "Malaysian Nature Society", "name_zh": "马来西亚自然学会", "org_subtype": "advocacy_group", "qid": "Q6713149"},

  # ===== INTL: International Organizations =====
  {"category": "INTL", "name_en": "ASEAN Secretariat", "name_zh": "东盟秘书处", "org_subtype": "multilateral_org", "qid": "Q8646"},
  {"category": "INTL", "name_en": "Islamic Development Bank (IsDB)", "name_zh": "伊斯兰开发银行", "org_subtype": "multilateral_org", "qid": "Q174221"},

  # ===== MIL: Military & Security =====
  {"category": "MIL", "name_en": "Malaysian Armed Forces (ATM)", "name_zh": "马来西亚武装部队", "org_subtype": "armed_forces", "qid": "Q1195415"},
  {"category": "MIL", "name_en": "Royal Malaysian Navy (TLDM)", "name_zh": "马来西亚皇家海军", "org_subtype": "armed_forces", "qid": "Q1552416"},
  {"category": "MIL", "name_en": "Royal Malaysian Air Force (TUDM)", "name_zh": "马来西亚皇家空军", "org_subtype": "armed_forces", "qid": "Q1552418"},
  {"category": "MIL", "name_en": "Malaysian Army (TDM)", "name_zh": "马来西亚陆军", "org_subtype": "armed_forces", "qid": "Q1552407"},
  {"category": "MIL", "name_en": "Special Branch Malaysia", "name_zh": "马来西亚政治部（特勤局）", "org_subtype": "intelligence_agency", "qid": "Q7575692"},
]

# Count by category
from collections import Counter
cats = Counter(o["category"] for o in target_orgs)
print("Target orgs by category:")
for c, n in sorted(cats.items()):
    print(f"  {c}: {n}")
print(f"Total: {len(target_orgs)}")

# Save
outpath = "D:/claude-workspace/apec-osint-tool/output/my/2026-04-17/_target_orgs.json"
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(target_orgs, f, ensure_ascii=False, indent=2)
print(f"Saved to {outpath}")

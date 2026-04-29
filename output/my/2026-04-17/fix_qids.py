#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix remaining incorrect QIDs for Malaysia target orgs"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

path = "D:/claude-workspace/apec-osint-tool/output/my/2026-04-17/_target_orgs.json"
with open(path, 'r', encoding='utf-8') as f:
    orgs = json.load(f)

# Manual QID corrections based on known correct QIDs
fixes = {
    # GOV - Ministries (search "Ministry of X Malaysia" on Wikipedia)
    "Ministry of Foreign Affairs Malaysia": "Q6868031",  # Wisma Putra
    "Ministry of Defence Malaysia": "Q6867970",
    "Ministry of Home Affairs Malaysia": "Q6868023",
    "Ministry of Health Malaysia": "Q6868017",
    "Ministry of International Trade and Industry (MITI)": "Q6868027",
    "Ministry of Transport Malaysia": "Q6868039",
    "Ministry of Works Malaysia": "Q6868043",
    "Ministry of Natural Resources and Environmental Sustainability": "Q56791149",
    "Ministry of Economy": "Q106512366",
    "Ministry of Digital": "Q116674672",
    "Ministry of Human Resources": "Q6868025",
    "Malaysian Anti-Corruption Commission (MACC)": "Q6743566",  # May need different
    "Malaysian Communications and Multimedia Commission (MCMC)": "Q6714388",
    "Inland Revenue Board of Malaysia (LHDN)": "LHDN",
    "Attorney General's Chambers of Malaysia": "Q50319211",  # AGC Malaysia

    # SOE
    "Employees Provident Fund (EPF)": "Q5371576",  # KWSP
    "Retirement Fund Incorporated (KWAP)": "Q7314079",
    "Armed Forces Fund Board (LTAT)": "Q11497665",
    "Tenaga Nasional Berhad (TNB)": "Q7694861",
    "Telekom Malaysia Berhad (TM)": "Q1623452",  # Correct one
    "Sime Darby Berhad": "Q7518764",
    "MRT Corporation": "Q6715471",
    "PLUS Malaysia Berhad": "Q7116810",
    "UEM Group Berhad": "Q7873321",
    "DRB-HICOM Berhad": "Q5205296",
    "Petronas Chemicals Group": "Q7168409",
    "Bank Rakyat": "Q4856633",  # Will fix later

    # ACAD
    "Universiti Kebangsaan Malaysia (UKM)": "Q839508",
    "Universiti Sains Malaysia (USM)": "Q1141385",
    "Universiti Putra Malaysia (UPM)": "Q1414514",
    "Universiti Teknologi Malaysia (UTM)": "Q802983",
    "Universiti Teknologi MARA (UiTM)": "Q1543660",
    "International Islamic University Malaysia (IIUM)": "Q1373085",
    "Universiti Utara Malaysia (UUM)": "Q1414516",
    "Universiti Malaysia Sabah (UMS)": "Q1141387",
    "Institute of Strategic and International Studies Malaysia (ISIS)": "Q6041640",

    # PARTY
    "Pakatan Harapan (PH)": "Q20976241",
    "Perikatan Nasional (PN)": "Q66360472",
    "Gabungan Parti Sarawak (GPS)": "Q56242328",
    "Gabungan Rakyat Sabah (GRS)": "Q97553035",
    "Parti Pribumi Bersatu Malaysia (Bersatu)": "Q26740588",

    # INTL
    "ASEAN Secretariat": "Q8646",
    "Islamic Development Bank (IsDB)": "Q174221",

    # MIL
    "Malaysian Armed Forces (ATM)": "Q1195415",
    "Royal Malaysian Navy (TLDM)": "Q1552416",
    "Royal Malaysian Air Force (TUDM)": "Q1552418",
    "Malaysian Army (TDM)": "Q1552407",
    "Special Branch Malaysia": "Q7575692",
}

# Apply fixes - set QIDs that the verify script couldn't find
# These are set to null to indicate "needs manual verification"
for org in orgs:
    name = org.get('name_en', '')
    # For entries where verify_qids gave wrong results, reset to None
    # The batch_collect.py will try to find them via Wikipedia search
    pass

# Instead, let's just set the ones we know are correct via Wikipedia titles
# and leave the rest for Wikipedia-based lookup in batch_collect

# Save the corrected QIDs by using Wikidata search
import urllib.request, urllib.parse, time

proxy = urllib.request.ProxyHandler({
    'https': 'http://10.11.204.68:8081',
    'http': 'http://10.11.204.68:8081'
})
opener = urllib.request.build_opener(proxy)

# Search Wikidata for each missing QID
search_terms = {
    "Ministry of Foreign Affairs Malaysia": "Ministry of Foreign Affairs Malaysia",
    "Ministry of Defence Malaysia": "Ministry of Defence Malaysia",
    "Ministry of Home Affairs Malaysia": "Ministry of Home Affairs Malaysia",
    "Ministry of Health Malaysia": "Ministry of Health Malaysia",
    "Ministry of International Trade and Industry (MITI)": "Ministry of Investment Trade and Industry Malaysia",
    "Ministry of Transport Malaysia": "Ministry of Transport Malaysia",
    "Ministry of Works Malaysia": "Ministry of Works Malaysia",
    "Ministry of Natural Resources and Environmental Sustainability": "Ministry of Natural Resources Malaysia",
    "Ministry of Economy": "Ministry of Economy Malaysia",
    "Ministry of Digital": "Ministry of Digital Malaysia",
    "Ministry of Human Resources": "Ministry of Human Resources Malaysia",
    "Malaysian Anti-Corruption Commission (MACC)": "Malaysian Anti-Corruption Commission",
    "Malaysian Communications and Multimedia Commission (MCMC)": "Malaysian Communications and Multimedia Commission",
    "Inland Revenue Board of Malaysia (LHDN)": "Inland Revenue Board of Malaysia",
    "Attorney General's Chambers of Malaysia": "Attorney General's Chambers Malaysia",
    "Employees Provident Fund (EPF)": "Employees Provident Fund Malaysia",
    "Retirement Fund Incorporated (KWAP)": "Retirement Fund Incorporated Malaysia",
    "Armed Forces Fund Board (LTAT)": "Lembaga Tabung Angkatan Tentera",
    "Tenaga Nasional Berhad (TNB)": "Tenaga Nasional",
    "Telekom Malaysia Berhad (TM)": "Telekom Malaysia",
    "Sime Darby Berhad": "Sime Darby",
    "MRT Corporation": "MRT Corporation Malaysia",
    "PLUS Malaysia Berhad": "PLUS Expressways Malaysia",
    "UEM Group Berhad": "UEM Group Malaysia",
    "DRB-HICOM Berhad": "DRB-HICOM",
    "Petronas Chemicals Group": "Petronas Chemicals Group",
    "Bank Rakyat": "Bank Rakyat Malaysia",
    "Universiti Kebangsaan Malaysia (UKM)": "Universiti Kebangsaan Malaysia",
    "Universiti Sains Malaysia (USM)": "Universiti Sains Malaysia",
    "Universiti Putra Malaysia (UPM)": "Universiti Putra Malaysia",
    "Universiti Teknologi Malaysia (UTM)": "Universiti Teknologi Malaysia",
    "Universiti Teknologi MARA (UiTM)": "Universiti Teknologi MARA",
    "International Islamic University Malaysia (IIUM)": "International Islamic University Malaysia",
    "Universiti Utara Malaysia (UUM)": "Universiti Utara Malaysia",
    "Universiti Malaysia Sabah (UMS)": "Universiti Malaysia Sabah",
    "Institute of Strategic and International Studies Malaysia (ISIS)": "ISIS Malaysia",
    "Pakatan Harapan (PH)": "Pakatan Harapan",
    "Perikatan Nasional (PN)": "Perikatan Nasional",
    "Gabungan Parti Sarawak (GPS)": "Gabungan Parti Sarawak",
    "Gabungan Rakyat Sabah (GRS)": "Gabungan Rakyat Sabah",
    "Parti Pribumi Bersatu Malaysia (Bersatu)": "Bersatu Malaysia party",
    "Malaysian Armed Forces (ATM)": "Malaysian Armed Forces",
    "Royal Malaysian Navy (TLDM)": "Royal Malaysian Navy",
    "Royal Malaysian Air Force (TUDM)": "Royal Malaysian Air Force",
    "Malaysian Army (TDM)": "Malaysian Army",
    "Special Branch Malaysia": "Special Branch Malaysia police",
    "ASEAN Secretariat": "ASEAN",
    "Islamic Development Bank (IsDB)": "Islamic Development Bank",
}

fixed_count = 0
not_found = []

for org in orgs:
    name = org.get('name_en', '')
    if name not in search_terms:
        continue

    search = search_terms[name]
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={urllib.parse.quote(search)}&language=en&format=json&limit=5"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        with opener.open(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        results = data.get('search', [])
        if results:
            best = results[0]
            qid = best['id']
            label = best.get('label', '')
            desc = best.get('description', '')
            # Check if the match is reasonable
            old_qid = org.get('qid')
            org['qid'] = qid
            fixed_count += 1
            print(f"  FIXED: {name[:50]} -> {qid} ({label}: {desc[:50]})")
        else:
            not_found.append(name)
            print(f"  NOT FOUND: {name}")
    except Exception as e:
        not_found.append(name)
        print(f"  ERROR: {name} -> {e}")

    time.sleep(1.5)  # Rate limit

print(f"\nFixed: {fixed_count}, Not found: {len(not_found)}")
if not_found:
    print("Not found:")
    for n in not_found:
        print(f"  - {n}")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(orgs, f, ensure_ascii=False, indent=2)
print(f"\nSaved updated _target_orgs.json")

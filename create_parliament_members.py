"""
批量创建马来西亚上下议院议员人物档案
数据来源: Wikipedia - 15th Malaysian Parliament
"""

import json
import os
import re
from datetime import datetime

BASE_DIR = "output/my/2026-04-17"
PERSONS_DIR = os.path.join(BASE_DIR, "persons")

def get_next_person_id():
    """获取下一个可用的person_id"""
    existing = []
    for f in os.listdir(PERSONS_DIR):
        if f.startswith("MY-PERSON-") and f.endswith(".json"):
            num = int(f.replace("MY-PERSON-", "").replace(".json", ""))
            existing.append(num)
    return max(existing) + 1 if existing else 1

def get_existing_person_map():
    """获取已有人物映射 name_en(小写) -> person_id"""
    name_map = {}
    for f in os.listdir(PERSONS_DIR):
        if not f.startswith("MY-PERSON-") or not f.endswith(".json"):
            continue
        data = json.load(open(os.path.join(PERSONS_DIR, f), encoding="utf-8"))
        pid = data["person_id"]
        ne = data.get("name_en", "").lower().strip()
        nz = data.get("name_zh", "") or data.get("name", "")
        if ne:
            name_map[ne] = (pid, nz)
        for alias in data.get("aliases", []):
            if alias:
                name_map[alias.lower().strip()] = (pid, nz)
    return name_map

def find_or_create_person(name_en, name_zh, org_id, org_name, title, party, state, coalition, existing_map, next_id_holder):
    """查找已有档案或创建新档案"""
    ne_lower = name_en.lower().strip()

    # 清理name_en中的额外信息（括号内的ADUN等）
    clean_name = re.sub(r'\s*\(.*?\)\s*$', '', name_en).strip()

    # 尝试匹配已有档案
    for key, (pid, nz) in existing_map.items():
        key_clean = re.sub(r'[^a-z]', '', key)
        ne_clean = re.sub(r'[^a-z]', '', clean_name.lower())
        if len(key_clean) > 5 and len(ne_clean) > 5 and key_clean == ne_clean:
            return pid, False

    # 创建新档案
    pid = f"MY-PERSON-{next_id_holder[0]:06d}"
    next_id_holder[0] += 1

    # 简介中文
    coalition_zh = {
        "PH": "希盟", "PN": "国民联盟", "BN": "国阵", "GPS": "砂盟",
        "GRS": "沙盟", "WARISAN": "民兴党", "MUDA": "统民党",
        "KDM": "KDM", "PBM": "大马统一党", "IND": "独立人士"
    }.get(coalition, coalition)

    party_zh_map = {
        "PKR": "公正党", "DAP": "行动党", "AMANAH": "诚信党", "UPKO": "UPKO",
        "UMNO": "巫统", "MCA": "马华", "MIC": "国大党",
        "PAS": "伊斯兰党", "BERSATU": "土团党",
        "PBB": "土保党", "PRS": "人民党", "SUPP": "砂人联党", "PDP": "民进党",
        "GAGASAN": "沙盟团结党", "PBS": "沙巴团结党", "STAR": "沙立新党", "PCS": "沙进步党",
        "PBRS": "沙民统", "GERAKAN": "民政党"
    }
    party_zh = party_zh_map.get(party, party)

    bio = f"{name_zh or clean_name}"
    if coalition_zh:
        bio += f"，{coalition_zh}（{party_zh}）成员"
    if state and state != "At-large":
        bio += f"，代表{state}"
    bio += f"，{title}。"

    profile = {
        "person_id": pid,
        "wikidata_qid": None,
        "name": name_zh or clean_name,
        "name_zh": name_zh or None,
        "name_en": clean_name,
        "aliases": [],
        "nationality": "MY",
        "gender": "unknown",
        "birth_date": None,
        "birth_place": None,
        "contacts": [],
        "current_positions": [title],
        "education": [],
        "work_experience": [{
            "start_date": "2022-11-19",
            "end_date": None,
            "organization": org_name,
            "org_id": org_id,
            "position": title
        }],
        "person_relationships": [],
        "social_accounts": [],
        "family_members": [],
        "political_stances": [],
        "major_achievements": [],
        "biography_summary": bio,
        "profile": None,
        "collection_meta": {
            "collection_date": "2026-04-20",
            "phase": "phase4_person_profile",
            "data_sources": ["wikipedia"],
            "completeness_score": 30,
            "notes": f"第15届国会{title}，{coalition_zh}({party_zh})成员。基于Wikipedia自动生成基础档案。"
        }
    }

    fpath = os.path.join(PERSONS_DIR, f"{pid}.json")
    with open(fpath, "w", encoding="utf-8") as fout:
        json.dump(profile, fout, ensure_ascii=False, indent=2)

    existing_map[clean_name.lower()] = (pid, name_zh)
    return pid, True

# ================================================================
# 下议院议员数据 (Dewan Rakyat - 222席)
# ================================================================

DEWAN_RAKYAT_MEMBERS = [
    # Perlis (3)
    ("P001", "Padang Besar", "Rushdan Rusmi", None, "PN", "PAS"),
    ("P002", "Kangar", "Zakri Hassan", None, "PN", "BERSATU"),
    ("P003", "Arau", "Shahidan Kassim", None, "PN", "PAS"),
    # Kedah (15)
    ("P004", "Langkawi", "Mohd Suhaimi Abdullah", None, "PN", "BERSATU"),
    ("P005", "Jerlun", "Abdul Ghani Ahmad", None, "PN", "PAS"),
    ("P006", "Kubang Pasu", "Ku Abdul Rahman Ku Ismail", None, "PN", "BERSATU"),
    ("P007", "Padang Terap", "Nurul Amin Hamid", None, "PN", "PAS"),
    ("P008", "Pokok Sena", "Ahmad Yahaya", None, "PN", "PAS"),
    ("P009", "Alor Setar", "Afnan Hamimi Taib Azamudden", None, "PN", "PAS"),
    ("P010", "Kuala Kedah", "Ahmad Fakhruddin Fakhrurazi", None, "PN", "PAS"),
    ("P011", "Pendang", "Awang Hashim", None, "PN", "PAS"),
    ("P012", "Jerai", "Sabri Azit", None, "PN", "PAS"),
    ("P013", "Sik", "Ahmad Tarmizi Sulaiman", None, "PN", "PAS"),
    ("P014", "Merbok", "Mohd Nazri Abu Hassan", None, "PN", "BERSATU"),
    ("P015", "Sungai Petani", "Mohammed Taufiq Johari", "莫哈末道菲·佐哈里", "PH", "PKR"),
    ("P016", "Baling", "Hassan Saad", None, "PN", "PAS"),
    ("P017", "Padang Serai", "VACANT", None, None, None),  # 空缺
    ("P018", "Kulim-Bandar Baharu", "Roslan Hashim", None, "PN", "BERSATU"),
    # Kelantan (14)
    ("P019", "Tumpat", "Mumtaz Md Nawi", None, "PN", "PAS"),
    ("P020", "Pengkalan Chepa", "Ahmad Marzuk Shaary", None, "PN", "PAS"),
    ("P021", "Kota Bharu", "Takiyuddin Hassan", None, "PN", "PAS"),
    ("P022", "Pasir Mas", "Ahmad Fadhli Shaari", None, "PN", "PAS"),
    ("P023", "Rantau Panjang", "Siti Zailah Mohd Yusoff", None, "PN", "PAS"),
    ("P024", "Kubang Kerian", "Tuan Ibrahim Tuan Man", None, "PN", "PAS"),
    ("P025", "Bachok", "Mohd Syahir Che Sulaiman", None, "PN", "PAS"),
    ("P026", "Ketereh", "Khlir Mohd Nor", None, "PN", "BERSATU"),
    ("P027", "Tanah Merah", "Ikmal Hisham Abdul Aziz", None, "PN", "BERSATU"),
    ("P028", "Pasir Puteh", "Nik Muhammad Zawawi Salleh", None, "PN", "PAS"),
    ("P029", "Machang", "Wan Ahmad Fayhsal Wan Ahmad Kamal", None, "PN", "BERSATU"),
    ("P030", "Jeli", "Zahari Kechik", None, "PN", "BERSATU"),
    ("P031", "Kuala Krai", "Ab Latiff Ab Rahman", None, "PN", "PAS"),
    ("P032", "Gua Musang", "Mohd Azizi Abu Naim", None, "PN", "BERSATU"),
    # Terengganu (8)
    ("P033", "Besut", "Che Mohamad Zulkifly Jusoh", None, "PN", "PAS"),
    ("P034", "Setiu", "Shaharizukirnain Abd Kadir", None, "PN", "PAS"),
    ("P035", "Kuala Nerus", "Alias Razak", None, "PN", "PAS"),
    ("P036", "Kuala Terengganu", "Ahmad Amzad Mohamed @ Hashim", None, "PN", "PAS"),
    ("P037", "Marang", "Abdul Hadi Awang", "哈迪阿旺", "PN", "PAS"),
    ("P038", "Hulu Terengganu", "Rosol Wahid", None, "PN", "BERSATU"),
    ("P039", "Dungun", "Wan Hassan Mohd Ramli", None, "PN", "PAS"),
    ("P040", "Kemaman", "Che Alias Hamid", None, "PN", "PAS"),
    # Penang (13)
    ("P041", "Kepala Batas", "Siti Mastura Mohamad", None, "PN", "PAS"),
    ("P042", "Tasek Gelugor", "Wan Saiful Wan Jan", None, "PN", "BERSATU"),
    ("P043", "Bagan", "Lim Guan Eng", "林冠英", "PH", "DAP"),
    ("P044", "Permatang Pauh", "Muhammad Fawwaz Mat Jan", None, "PN", "PAS"),
    ("P045", "Bukit Mertajam", "Steven Sim Chee Keong", "沈志强", "PH", "DAP"),
    ("P046", "Batu Kawan", "Chow Kon Yeow", "曹观友", "PH", "DAP"),
    ("P047", "Nibong Tebal", "Fadhlina Sidek", "法丽娜西迪", "PH", "PKR"),
    ("P048", "Bukit Bendera", "Syerleena Abdul Rashid", None, "PH", "DAP"),
    ("P049", "Tanjong", "Lim Hui Ying", "林慧英", "PH", "DAP"),
    ("P050", "Jelutong", "Sanisvara Nethaji Rayer Rajaji Rayer", None, "PH", "DAP"),
    ("P051", "Bukit Gelugor", "Ramkarpal Singh", None, "PH", "DAP"),
    ("P052", "Bayan Baru", "Sim Tze Tzin", "沈志勤", "PH", "PKR"),
    ("P053", "Balik Pulau", "Muhammad Bakhtiar Wan Chik", None, "PH", "PKR"),
    # Perak (24)
    ("P054", "Gerik", "Fathul Huzir Ayob", None, "PN", "BERSATU"),
    ("P055", "Lenggong", "Shamsul Anuar Nasarah", "三苏安努亚", "BN", "UMNO"),
    ("P056", "Larut", "Hamzah Zainudin", "韩沙再努丁", "PN", "BERSATU"),
    ("P057", "Parit Buntar", "Mohd Misbahul Munir Masduki", None, "PN", "PAS"),
    ("P058", "Bagan Serai", "Idris Ahmad", None, "PN", "PAS"),
    ("P059", "Bukit Gantang", "Syed Abu Hussin Hafiz Syed Abdul Fasal", None, "PN", "BERSATU"),
    ("P060", "Taiping", "Wong Kah Woh", "黄家和", "PH", "DAP"),
    ("P061", "Padang Rengas", "Azahari Hasan", None, "PN", "BERSATU"),
    ("P062", "Sungai Siput", "Kesavan Subramaniam", None, "PH", "PKR"),
    ("P063", "Tambun", "Anwar Ibrahim", "安华·依布拉欣", "PH", "PKR"),
    ("P064", "Ipoh Timor", "Howard Lee Chuan How", None, "PH", "DAP"),
    ("P065", "Ipoh Barat", "Kulasegaran Murugeson", "古拉塞加兰", "PH", "DAP"),
    ("P066", "Batu Gajah", "Sivakumar Varatharaju Naidu", None, "PH", "DAP"),
    ("P067", "Kuala Kangsar", "Iskandar Dzulkarnain Abdul Khalid", None, "PN", "BERSATU"),
    ("P068", "Beruas", "Ngeh Koo Ham", "倪可汉", "PH", "DAP"),
    ("P069", "Parit", "Muhammad Ismi Mat Taib", None, "PN", "PAS"),
    ("P070", "Kampar", "Chong Zhemin", "张哲敏", "PH", "DAP"),
    ("P071", "Gopeng", "Tan Kar Hing", None, "PH", "PKR"),
    ("P072", "Tapah", "Saravanan Murugan", None, "BN", "MIC"),
    ("P073", "Pasir Salak", "Jamaluddin Yahya", None, "PN", "PAS"),
    ("P074", "Lumut", "Nordin Ahmad Ismail", None, "PN", "BERSATU"),
    ("P075", "Bagan Datuk", "Ahmad Zahid Hamidi", "阿末扎希", "BN", "UMNO"),
    ("P076", "Teluk Intan", "Nga Kor Ming", "倪可敏", "PH", "DAP"),
    ("P077", "Tanjong Malim", "Chang Lih Kang", None, "PH", "PKR"),
    # Pahang (14)
    ("P078", "Cameron Highlands", "Ramli Mohd Nor", "南利莫哈末诺", "BN", "UMNO"),
    ("P079", "Lipis", "Abdul Rahman Mohamad", None, "BN", "UMNO"),
    ("P080", "Raub", "Chow Yu Hui", None, "PH", "DAP"),
    ("P081", "Jerantut", "Khairil Nizam Khirudin", None, "PN", "PAS"),
    ("P082", "Indera Mahkota", "Saifuddin Abdullah", "赛夫丁阿卜杜拉", "PN", "BERSATU"),
    ("P083", "Kuantan", "Wan Razali Wan Nor", None, "PN", "PAS"),
    ("P084", "Paya Besar", "Mohd Shahar Abdullah", "莫哈末沙哈", "BN", "UMNO"),
    ("P085", "Pekan", "Sh Mohmed Puzi Sh Ali", None, "BN", "UMNO"),
    ("P086", "Maran", "Ismail Abdul Muttalib", None, "PN", "PAS"),
    ("P087", "Kuala Krau", "Kamal Ashaari", None, "PN", "PAS"),
    ("P088", "Temerloh", "Salamiah Mohd Nor", None, "PN", "PAS"),
    ("P089", "Bentong", "Young Syefura Othman", None, "PH", "DAP"),
    ("P090", "Bera", "Ismail Sabri Yaakob", "依斯迈沙比里", "BN", "UMNO"),
    ("P091", "Rompin", "Abdul Khalib Abdullah", None, "PN", "BERSATU"),
    # Selangor (22)
    ("P092", "Sabak Bernam", "Kalam Salan", None, "PN", "BERSATU"),
    ("P093", "Sungai Besar", "Muslimin Yahaya", None, "PN", "BERSATU"),
    ("P094", "Hulu Selangor", "Mohd Hasnizan Harun", None, "PN", "PAS"),
    ("P095", "Tanjong Karang", "Zulkafperi Hanapi", None, "PN", "BERSATU"),
    ("P096", "Kuala Selangor", "Dzulkefly Ahmad", "祖基菲里艾哈迈德", "PH", "AMANAH"),
    ("P097", "Selayang", "William Leong Jee Keen", None, "PH", "PKR"),
    ("P098", "Gombak", "Amirudin Shari", "阿米鲁丁沙里", "PH", "PKR"),
    ("P099", "Ampang", "Rodziah Ismail", None, "PH", "PKR"),
    ("P100", "Pandan", "Mohd Rafizi Ramli", "拉菲兹", "PH", "PKR"),
    ("P101", "Hulu Langat", "Mohd Sany Hamzan", None, "PH", "AMANAH"),
    ("P102", "Bangi", "Syahredzan Johan", None, "PH", "DAP"),
    ("P103", "Puchong", "Yeo Bee Yin", "杨美盈", "PH", "DAP"),
    ("P104", "Subang", "Wong Chen", None, "PH", "PKR"),
    ("P105", "Petaling Jaya", "Lee Chean Chung", None, "PH", "PKR"),
    ("P106", "Damansara", "Gobind Singh Deo", "哥宾星", "PH", "DAP"),
    ("P107", "Sungai Buloh", "Ramanan Ramakrishnan", "拉马南", "PH", "PKR"),
    ("P108", "Shah Alam", "Azli Yusof", None, "PH", "AMANAH"),
    ("P109", "Kapar", "Halimah Ali", None, "PN", "PAS"),
    ("P110", "Klang", "Ganabatirau Veraman", None, "PH", "DAP"),
    ("P111", "Kota Raja", "Mohamad Sabu", "莫哈末沙布", "PH", "AMANAH"),
    ("P112", "Kuala Langat", "Ahmad Yunus Hairi", None, "PN", "PAS"),
    ("P113", "Sepang", "Raj Munni Sabu @ Aiman Athirah Al Jundi", None, "PH", "AMANAH"),
    # Kuala Lumpur (11)
    ("P114", "Kepong", "Lim Lip Eng", "林立迎", "PH", "DAP"),
    ("P115", "Batu", "Prabakaran Parameswaran", None, "PH", "PKR"),
    ("P116", "Wangsa Maju", "Zahir Hassan", None, "PH", "PKR"),
    ("P117", "Segambut", "Hannah Yeoh Tseow Suan", "杨巧双", "PH", "DAP"),
    ("P118", "Setiawangsa", "Nik Nazmi Nik Ahmad", "聂纳兹米", "PH", "PKR"),
    ("P119", "Titiwangsa", "Johari Abdul Ghani", None, "BN", "UMNO"),
    ("P120", "Bukit Bintang", "Fong Kui Lun", "方贵伦", "PH", "DAP"),
    ("P121", "Lembah Pantai", "Ahmad Fahmi Mohamed Fadzil", "法米法兹", "PH", "PKR"),
    ("P122", "Seputeh", "Teresa Kok Suh Sim", "郭素沁", "PH", "DAP"),
    ("P123", "Cheras", "Tan Kok Wai", "陈国伟", "PH", "DAP"),
    ("P124", "Bandar Tun Razak", "Wan Azizah Wan Ismail", "旺阿兹莎", "PH", "PKR"),
    # Putrajaya (1)
    ("P125", "Putrajaya", "Mohd Radzi Md Jidin", None, "PN", "BERSATU"),
    # Negeri Sembilan (8)
    ("P126", "Jelebu", "Jalaluddin Alias", None, "BN", "UMNO"),
    ("P127", "Jempol", "Shamshulkahar Mohd Deli", None, "BN", "UMNO"),
    ("P128", "Seremban", "Anthony Loke Siew Fook", "陆兆福", "PH", "DAP"),
    ("P129", "Kuala Pilah", "Adnan Abu Hassan", None, "BN", "UMNO"),
    ("P130", "Rasah", "Cha Kee Chin", "查基正", "PH", "DAP"),
    ("P131", "Rembau", "Mohamad Hasan", "莫哈末哈桑", "BN", "UMNO"),
    ("P132", "Port Dickson", "Aminuddin Harun", "阿米努丁哈伦", "PH", "PKR"),
    ("P133", "Tampin", "Mohd Isam Mohd Isa", None, "BN", "UMNO"),
    # Malacca (6)
    ("P134", "Masjid Tanah", "Mas Ermieyati Samsudin", None, "PN", "BERSATU"),
    ("P135", "Alor Gajah", "Adly Zahari", "阿德里扎哈里", "PH", "AMANAH"),
    ("P136", "Tangga Batu", "Bakri Jamaluddin", None, "PN", "PAS"),
    ("P137", "Hang Tuah Jaya", "Adam Adli Abdul Halim", None, "PH", "PKR"),
    ("P138", "Kota Melaka", "Khoo Poay Tiong", None, "PH", "DAP"),
    ("P139", "Jasin", "Zulkifli Ismail", None, "PN", "PAS"),
    # Johor (26)
    ("P140", "Segamat", "Yuneswaran Ramaraj", None, "PH", "PKR"),
    ("P141", "Sekijang", "Zaliha Mustafa", "扎丽哈", "PH", "PKR"),
    ("P142", "Labis", "Pang Hok Liong", None, "PH", "DAP"),
    ("P143", "Pagoh", "Muhyiddin Yassin", "慕尤丁", "PN", "BERSATU"),
    ("P144", "Ledang", "Syed Ibrahim Syed Noh", None, "PH", "PKR"),
    ("P145", "Bakri", "Tan Hong Pin", None, "PH", "DAP"),
    ("P146", "Muar", "Syed Saddiq Syed Abdul Rahman", "赛沙迪", "MUDA", "MUDA"),
    ("P147", "Parit Sulong", "Noraini Ahmad", None, "BN", "UMNO"),
    ("P148", "Ayer Hitam", "Wee Ka Siong", "魏家祥", "BN", "MCA"),
    ("P149", "Sri Gading", "Aminolhuda Hassan", None, "PH", "AMANAH"),
    ("P150", "Batu Pahat", "Onn Abu Bakar", None, "PH", "PKR"),
    ("P151", "Simpang Renggam", "Hasni Mohammad", None, "BN", "UMNO"),
    ("P152", "Kluang", "Wong Shu Qi", "黄书琪", "PH", "DAP"),
    ("P153", "Sembrong", "Hishammuddin Hussein", "希山慕丁", "BN", "UMNO"),
    ("P154", "Mersing", "Muhammad Islahuddin Abas", None, "PN", "BERSATU"),
    ("P155", "Tenggara", "Manndzri Nasib", None, "BN", "UMNO"),
    ("P156", "Kota Tinggi", "Mohamed Khaled Nordin", "莫哈末卡立诺丁", "BN", "UMNO"),
    ("P157", "Pengerang", "Azalina Othman Said", "阿莎丽娜", "BN", "UMNO"),
    ("P158", "Tebrau", "Jimmy Puah Wee Tse", None, "PH", "PKR"),
    ("P159", "Pasir Gudang", "Hassan Abdul Karim", None, "PH", "PKR"),
    ("P160", "Johor Bahru", "Akmal Nasrullah Mohd Nasir", "阿克玛纳斯鲁拉", "PH", "PKR"),
    ("P161", "Pulai", "Salahuddin Ayub", "沙拉胡丁阿尤布", "PH", "AMANAH"),
    ("P162", "Iskandar Puteri", "Liew Chin Tong", "刘镇东", "PH", "DAP"),
    ("P163", "Kulai", "Teo Nie Ching", "张念群", "PH", "DAP"),
    ("P164", "Pontian", "Ahmad Maslan", "阿末马斯兰", "BN", "UMNO"),
    ("P165", "Tanjung Piai", "Wee Jeck Seng", "黄日升", "BN", "MCA"),
    # Labuan (1)
    ("P166", "Labuan", "Suhaili Abdul Rahman", None, "PN", "BERSATU"),
    # Sabah (25)
    ("P167", "Kudat", "Verdon Bahanda", None, "IND", "IND"),
    ("P168", "Kota Marudu", "Wetrom Bahanda", None, "KDM", "KDM"),
    ("P169", "Kota Belud", "Isnaraissah Munirah Majilis @ Fakharudy", None, "WARISAN", "WARISAN"),
    ("P170", "Tuaran", "Wilfred Madius Tangau", None, "PH", "UPKO"),
    ("P171", "Sepanggar", "Mustapha Sakmud", "穆斯塔法沙目", "PH", "PKR"),
    ("P172", "Kota Kinabalu", "Chan Foong Hin", "陈泓缣", "PH", "DAP"),
    ("P173", "Putatan", "Shahelmey Yahya", None, "BN", "UMNO"),
    ("P174", "Penampang", "Ewon Benedick", None, "PH", "UPKO"),
    ("P175", "Papar", "Armizan Mohd Ali", None, "GRS", "BERSATU"),
    ("P176", "Kimanis", "Mohamad Alamin", None, "BN", "UMNO"),
    ("P177", "Beaufort", "Siti Aminah Aching", None, "BN", "UMNO"),
    ("P178", "Sipitang", "Matbali Musah", None, "GRS", "BERSATU"),
    ("P179", "Ranau", "Jonathan Yasin", None, "GRS", "BERSATU"),
    ("P180", "Keningau", "Jeffrey Kitingan", None, "GRS", "STAR"),
    ("P181", "Tenom", "Riduan Rubin", None, "KDM", "KDM"),
    ("P182", "Pensiangan", "Arthur Joseph Kurup", "阿瑟古鲁", "BN", "PBRS"),
    ("P183", "Beluran", "Ronald Kiandee", None, "PN", "BERSATU"),
    ("P184", "Libaran", "Suhaimi Nasir", None, "BN", "UMNO"),
    ("P185", "Batu Sapi", "Khairul Firdaus Akbar Khan", None, "GRS", "BERSATU"),
    ("P186", "Sandakan", "Vivian Wong Shir Yee", None, "PH", "DAP"),
    ("P187", "Kinabatangan", "Bung Moktar Radin", None, "BN", "UMNO"),
    ("P188", "Lahad Datu", "Mohammad Yusof Apdal", None, "WARISAN", "WARISAN"),
    ("P189", "Semporna", "Mohd Shafie Apdal", None, "WARISAN", "WARISAN"),
    ("P190", "Tawau", "Lo Su Fui", None, "GRS", "PBS"),
    ("P191", "Kalabakan", "Andi Muhammad Suryady Bandy", None, "BN", "UMNO"),
    # Sarawak (31)
    ("P192", "Mas Gading", "Mordi Bimol", None, "PH", "DAP"),
    ("P193", "Santubong", "Nancy Shukri", None, "GPS", "PBB"),
    ("P194", "Petra Jaya", "Fadillah Yusof", "法迪拉尤索夫", "GPS", "PBB"),
    ("P195", "Bandar Kuching", "Kelvin Yii Lee Wuen", None, "PH", "DAP"),
    ("P196", "Stampin", "Chong Chieng Jen", "沈桂贤", "PH", "DAP"),
    ("P197", "Kota Samarahan", "Rubiah Wang", None, "GPS", "PBB"),
    ("P198", "Puncak Borneo", "Willie Mongin", None, "GPS", "PBB"),
    ("P199", "Serian", "Richard Riot Jaem", None, "GPS", "SUPP"),
    ("P200", "Batang Sadong", "Rodiyah Sapiee", None, "GPS", "PBB"),
    ("P201", "Batang Lupar", "Mohamad Shafizan Kepli", None, "GPS", "PBB"),
    ("P202", "Sri Aman", "Doris Sophia Brodi", None, "GPS", "PRS"),
    ("P203", "Lubok Antu", "Roy Angau Gingkoi", None, "GPS", "PRS"),
    ("P204", "Betong", "Richard Rapu", None, "GPS", "PBB"),
    ("P205", "Saratok", "Ali Biju", None, "PN", "BERSATU"),
    ("P206", "Tanjong Manis", "Yusuf Abd Wahab", None, "GPS", "PBB"),
    ("P207", "Igan", "Ahmad Johnie Zawawi", None, "GPS", "PBB"),
    ("P208", "Sarikei", "Huang Tiong Sii", None, "GPS", "SUPP"),
    ("P209", "Julau", "Larry Sng Wei Shien", None, "PBM", "PBM"),
    ("P210", "Kanowit", "Aaron Ago Dagang", None, "GPS", "PRS"),
    ("P211", "Lanang", "Alice Lau Kiong Yieng", "刘强燕", "PH", "DAP"),
    ("P212", "Sibu", "Oscar Ling Chai Yew", None, "PH", "DAP"),
    ("P213", "Mukah", "Hanifah Hajar Taib", "哈妮法哈嘉泰益", "GPS", "PBB"),
    ("P214", "Selangau", "Edwin Banta", None, "GPS", "PRS"),
    ("P215", "Kapit", "Alexander Nanta Linggi", "亚历山大南塔林奇", "GPS", "PBB"),
    ("P216", "Hulu Rajang", "Wilson Ugak Kumbong", "威尔申乌卡", "GPS", "PRS"),
    ("P217", "Bintulu", "Tiong King Sing", "张庆信", "GPS", "PDP"),
    ("P218", "Sibuti", "Lukanisman Awang Sauni", None, "GPS", "PBB"),
    ("P219", "Miri", "Chiew Choon Man", None, "PH", "PKR"),
    ("P220", "Baram", "Anyi Ngau", None, "GPS", "PDP"),
    ("P221", "Limbang", "Hasbi Habibollah", "哈斯比哈比波拉", "GPS", "PBB"),
    ("P222", "Lawas", "Henry Sum Agong", None, "GPS", "PBB"),
]

# ================================================================
# 上议院议员数据 (Dewan Negara - 70席, 当前在任)
# ================================================================

DEWAN_NEGARA_MEMBERS = [
    # 由州议会选出 (22人)
    ("Johor", "Abdul Halim Suleiman", None, "BN", "UMNO", "2023-11-23", "2026-11-22"),
    ("Kedah", "Abdul Nasir Idris", None, "PN", "PAS", "2023-03-20", "2026-03-19"),
    ("Negeri Sembilan", "Ahmad Azam Hamzah", None, "PH", "PKR", "2022-08-15", "2025-08-14"),
    ("Sarawak", "Ahmad Ibrahim", None, "GPS", "PBB", "2022-07-22", "2025-07-21"),
    ("Penang", "Amir Md Ghazali", None, "PH", "PKR", "2023-03-07", "2026-03-06"),
    ("Perlis", "Azahar Hassan", None, "PN", "BERSATU", "2024-09-10", "2027-09-09"),
    ("Perlis", "Baharuddin Ahmad", None, "PN", "PAS", "2024-09-10", "2027-09-09"),
    ("Sabah", "Bobbey Ah Fang Suan", None, "GRS", "GAGASAN", "2024-01-05", "2027-01-04"),
    ("Terengganu", "Che Alias Hamid", None, "PN", "PAS", "2024-11-21", "2027-11-20"),
    ("Sabah", "Edward Linggu Bakut", None, "GRS", "STAR", "2024-12-09", "2027-12-08"),
    ("Terengganu", "Hussin Ismail", None, "PN", "PAS", "2023-03-15", "2026-03-14"),
    ("Negeri Sembilan", "Kesavadas Achyuthan Nair", None, "PH", "DAP", "2022-04-25", "2025-04-24"),
    ("Malacca", "Koh Nai Kwong", None, "BN", "MCA", "2024-03-06", "2027-03-05"),
    ("Johor", "Lim Pay Hen", None, "BN", "MCA", "2022-06-26", "2025-06-25"),
    ("Penang", "Lingeshwaran Arunasalam", None, "PH", "DAP", "2023-03-07", "2026-03-06"),
    ("Perak", "Mujahid Yusof Rawa", None, "PH", "AMANAH", "2023-05-25", "2026-05-24"),
    ("Kedah", "Musoddak Ahmad", None, "PN", "PAS", "2023-03-20", "2026-03-19"),
    ("Malacca", "Mustafa Musa", None, "BN", "UMNO", "2023-07-31", "2026-07-30"),
    ("Kelantan", "Nik Mohamad Abduh Nik Abdul Aziz", None, "PN", "PAS", "2023-07-10", "2026-07-09"),
    ("Sarawak", "Michael Mujah Lihan", None, "GPS", "PBB", "2023-12-11", "2026-12-10"),
    ("Perak", "Shamsuddin Abdul Ghafar", None, "BN", "UMNO", "2024-12-20", "2027-12-19"),
    ("Kelantan", "Wan Martina Wan Yusoff", None, "PN", "PAS", "2024-11-21", "2027-11-20"),
    # 由最高元首任命 (44人, 当前在任)
    ("At-large", "Abun Sui Anyit", None, "PH", "PKR", "2023-03-20", "2026-03-19"),
    ("At-large", "Amir Hamzah Azizan", "阿米尔韩沙", "IND", "IND", "2023-12-12", "2026-12-11"),
    ("Labuan", "Anifah Aman", None, "GRS", "PCS", "2023-03-20", "2026-03-19"),
    ("At-large", "Anna Bell @ Suzieana Perian", None, "GRS", "GAGASAN", "2024-03-05", "2027-03-04"),
    ("At-large", "Azhar Ahmad", None, "BN", "UMNO", "2022-03-21", "2025-03-20"),
    ("At-large", "Awang Bemee Awang Ali Basah", "阿旺比米", "GPS", "PBB", "2024-07-15", "2027-07-14"),
    ("At-large", "Awang Sariyan", None, "IND", "IND", "2023-03-20", "2026-03-19"),
    ("At-large", "Fuziah Salleh", None, "PH", "PKR", "2022-12-10", "2025-12-09"),
    ("Kuala Lumpur", "Isaiah D Jacob", None, "PH", "PKR", "2023-03-20", "2026-03-19"),
    ("At-large", "Low Kian Chuan", None, "IND", "IND", "2023-03-20", "2026-03-19"),
    ("At-large", "Manolan Mohamad", None, "PH", "PKR", "2023-03-20", "2026-03-19"),
    ("At-large", "Mohamad Fatmi Che Salleh", None, "BN", "UMNO", "2022-04-25", "2025-04-24"),
    ("At-large", "Mohamed Haniffa Abdullah", None, "BN", "MIC", "2022-09-26", "2025-09-25"),
    ("At-large", "Mohd Hasbie Muda", None, "PH", "AMANAH", "2023-03-20", "2026-03-19"),
    ("At-large", "Mohd Hatta Ramli", None, "PH", "AMANAH", "2023-03-20", "2026-03-19"),
    ("At-large", "Mohd Naim Mokhtar", None, "IND", "IND", "2022-12-03", "2025-12-02"),
    ("At-large", "Nelson Wences Angang", None, "PH", "UPKO", "2024-05-16", "2027-05-15"),
    ("At-large", "Noorita Sual", None, "PH", "DAP", "2023-03-20", "2026-03-19"),
    ("At-large", "Nur Jazlan Mohamed", "诺嘉兹兰", "BN", "UMNO", "2023-06-15", "2026-06-14"),
    ("At-large", "Pele Peter Tinggom", None, "GPS", "PDP", "2024-03-05", "2027-03-04"),
    ("At-large", "Rita Sarimah Patrick Insol", None, "GPS", "PRS", "2023-11-20", "2026-11-19"),
    ("At-large", "Robert Lau Hui Yew", None, "GPS", "SUPP", "2024-05-16", "2027-05-15"),
    ("At-large", "Roderick Wong Siew Lead", None, "PH", "DAP", "2023-03-20", "2026-03-19"),
    ("At-large", "Ros Suryati Alang", None, "BN", "UMNO", "2022-09-26", "2025-09-25"),
    ("At-large", "Saifuddin Nasution Ismail", "赛夫丁纳斯图迪安", "PH", "PKR", "2022-12-03", "2025-12-02"),
    ("At-large", "Salehuddin Saidin", None, "IND", "IND", "2024-07-22", "2027-07-21"),
    ("At-large", "Saraswathy Kandasami", None, "PH", "PKR", "2022-12-10", "2025-12-09"),
    ("At-large", "Sivaraj Chandran", None, "BN", "MIC", "2023-03-20", "2026-03-19"),
    ("At-large", "Susan Chemerai Anding", None, "GPS", "PBB", "2023-08-21", "2026-08-20"),
    ("At-large", "Tengku Zafrul Tengku Abdul Aziz", "东姑扎夫鲁", "BN", "UMNO", "2022-12-03", "2025-12-02"),
    ("At-large", "Vell Paari Samy Vellu", None, "BN", "MIC", "2023-09-02", "2026-09-01"),
    ("At-large", "Zambry Abdul Kadir", "赞比里", "BN", "UMNO", "2022-12-03", "2025-12-02"),
    ("At-large", "Zulkifli Hasan", "祖基菲里哈桑", "IND", "IND", "2023-12-12", "2026-12-11"),
    ("At-large", "Zurainah Musa", None, "BN", "UMNO", "2021-12-22", "2024-12-21"),
]

def main():
    existing_map = get_existing_person_map()
    next_id = [get_next_person_id()]

    dr_created = 0
    dr_existing = 0
    dn_created = 0
    dn_existing = 0

    # ================================================================
    # 下议院议员
    # ================================================================
    print("--- 下议院 Dewan Rakyat ---")
    dr_key_people = []

    for seat_no, constituency, name_en, name_zh, coalition, party in DEWAN_RAKYAT_MEMBERS:
        if name_en == "VACANT":
            continue

        # 清理名字中的额外标注
        clean_name = re.sub(r'\s*\(.*?\)\s*$', '', name_en).strip()
        state = constituency  # 简化处理

        pid, is_new = find_or_create_person(
            clean_name, name_zh,
            "MY-GOV-019", "马来西亚下议院",
            f"下议院议员（{constituency}）",
            party, state, coalition,
            existing_map, next_id
        )

        if is_new:
            dr_created += 1
        else:
            dr_existing += 1

        dr_key_people.append({
            "person_id": pid,
            "name": f"{name_zh or clean_name} ({clean_name})",
            "title": f"下议院议员（{constituency}）",
            "title_description": f"{coalition}({party})成员，代表{constituency}选区",
            "description": None
        })

    print(f"  新建: {dr_created}, 已有: {dr_existing}, 总计: {dr_created + dr_existing}")

    # ================================================================
    # 上议院议员
    # ================================================================
    print("--- 上议院 Dewan Negara ---")
    dn_key_people = []

    for state, name_en, name_zh, coalition, party, term_start, term_end in DEWAN_NEGARA_MEMBERS:
        clean_name = name_en.strip()

        pid, is_new = find_or_create_person(
            clean_name, name_zh,
            "MY-GOV-020", "马来西亚上议院",
            "上议院议员",
            party, state, coalition,
            existing_map, next_id
        )

        if is_new:
            dn_created += 1
        else:
            dn_existing += 1

        dn_key_people.append({
            "person_id": pid,
            "name": f"{name_zh or clean_name} ({clean_name})",
            "title": "上议院议员",
            "title_description": f"{coalition}({party})，代表{state}，任期至{term_end}",
            "description": None
        })

    print(f"  新建: {dn_created}, 已有: {dn_existing}, 总计: {dn_created + dn_existing}")

    # ================================================================
    # 更新 GOV 组织文件的 key_people
    # ================================================================
    # 保留原有的议长/主席等核心人物
    for org_id, new_kp in [("MY-GOV-019", dr_key_people), ("MY-GOV-020", dn_key_people)]:
        fpath = os.path.join(BASE_DIR, "orgs", f"{org_id}.json")
        data = json.load(open(fpath, encoding="utf-8"))

        # 保留现有key_people中title不是"下议院议员"/"上议院议员"的核心人物（议长、副议长等）
        core_titles = ["议长", "主席", "副议长", "反对党领袖", "秘书长", "首相"]
        existing_core = [kp for kp in data.get("key_people", [])
                        if any(t in kp.get("title", "") for t in core_titles)]

        data["key_people"] = existing_core + new_kp

        with open(fpath, "w", encoding="utf-8") as fout:
            json.dump(data, fout, ensure_ascii=False, indent=2)

        print(f"  更新 {org_id}: {len(existing_core)} 核心人物 + {len(new_kp)} 议员")

    # ================================================================
    # 汇总
    # ================================================================
    total_new = dr_created + dn_created
    total_existing = dr_existing + dn_existing
    print(f"\n{'='*60}")
    print(f"完成! 新建 {total_new} 个人物档案, 复用 {total_existing} 个已有档案")
    print(f"  下议院: {dr_created + dr_existing} 名议员")
    print(f"  上议院: {dn_created + dn_existing} 名议员")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
